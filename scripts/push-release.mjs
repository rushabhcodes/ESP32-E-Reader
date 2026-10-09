import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdir, mkdtemp, readFile, rm } from "node:fs/promises";
import { homedir, tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
if (execFileSync("git", ["status", "--porcelain"], { cwd: root, encoding: "utf8" }).trim())
  throw new Error("Commit all release changes before publishing.");
const api = "https://registry-api.tscircuit.com/";
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
async function post(route, body, token) {
  const response = await fetch(new URL(route, api), {
    method: "POST", headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify(body), signal: AbortSignal.timeout(120000),
  });
  if (!response.ok) throw new Error(`Registry ${route}: HTTP ${response.status}`);
  return response.json();
}

// tsci ignores dotfiles, but does not honor .gitignore. Start with committed
// files. Preserve original STEP models in Git and the downloadable ZIP while
// omitting individual STEP copies from the browser's build source.
const temporary = await mkdtemp(path.join(tmpdir(), "reader-release-"));
try {
  const archive = path.join(temporary, "source.tar"), project = path.join(temporary, "project");
  await mkdir(project);
  execFileSync("git", ["archive", "--format=tar", "--output", archive, "HEAD"], { cwd: root });
  execFileSync("tar", ["-xf", archive, "-C", project]);
  const committed = execFileSync("git", ["ls-files", "-z"], { cwd: root, encoding: "utf8" }).split("\0").filter(Boolean);
  for (const file of committed.filter((file) => file.toLowerCase().endsWith(".step")))
    await rm(path.join(project, file));
  const files = committed.filter((file) => !file.split("/").some((part) => part.startsWith(".")) && !file.toLowerCase().endsWith(".step") && !file.startsWith("dist/") && !file.startsWith("node_modules/"));
  const pkg = JSON.parse(await readFile(path.join(project, "package.json"), "utf8"));
  const expected = pkg.version;
  const child = spawn(process.execPath, [path.join(root, "node_modules/.bin/tsci"), "push", "index.circuit.tsx", "--compress"], { cwd: project, stdio: "inherit" });
  const code = await new Promise((resolve, reject) => { child.once("error", reject); child.once("exit", resolve); });
  const published = JSON.parse(await readFile(path.join(project, "package.json"), "utf8")).version;
  if (published !== expected) throw new Error(`Published ${published}; commit package.json to match the registry version.`);
  const packageName = pkg.name.replace(/^@tsci\//, "").replace(".", "/");
  const identity = { package_name_with_version: `${packageName}@${expected}` };
  const { filesystem_map: remote } = await post("package_releases/get_filesystem_map", identity);
  if (Object.keys(remote).length !== files.length) throw new Error(`Release source has ${Object.keys(remote).length} files; expected ${files.length}.`);
  for (const file of files) {
    const source = await readFile(path.join(project, file)), uploaded = remote[file];
    if (typeof uploaded !== "string" || ![Buffer.from(uploaded, "utf8"), Buffer.from(uploaded, "base64")].some((bytes) => digest(bytes) === digest(source)))
      throw new Error(`Missing or changed release source: ${file}`);
  }
  // The CLI uses short request timeouts. Only recover a timeout after proving
  // that every intended source file exists and matches the committed bytes.
  if (code !== 0) {
    const config = JSON.parse(await readFile(path.join(homedir(), ".config/tscircuit-nodejs/config.json"), "utf8"));
    if (!config.sessionToken) throw new Error(`tsci push exited ${code}; no session available to finalize verified upload.`);
    await post("package_releases/update", { ...identity, ready_to_build: true }, config.sessionToken);
    console.log("Recovered completed upload after verifying every source file.");
  }
  console.log(`Verified ${files.length} committed runtime files for ${identity.package_name_with_version}.`);
} finally {
  await rm(temporary, { recursive: true, force: true });
}
