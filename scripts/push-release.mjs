import { execFileSync, spawn } from "node:child_process";
import { mkdir, mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
if (execFileSync("git", ["status", "--porcelain"], { cwd: root, encoding: "utf8" }).trim())
	throw new Error("Commit all release changes before publishing.");

// tsci push does not use .gitignore. Publish exactly the committed tree so
// local check fixtures, caches and build logs cannot enter the cloud build.
const temporary = await mkdtemp(path.join(tmpdir(), "reader-release-"));
try {
	const archive = path.join(temporary, "source.tar");
	const project = path.join(temporary, "project");
	await mkdir(project);
	execFileSync("git", ["archive", "--format=tar", "--output", archive, "HEAD"], { cwd: root });
	execFileSync("tar", ["-xf", archive, "-C", project]);
	const expected = JSON.parse(await readFile(path.join(project, "package.json"), "utf8")).version;
	const child = spawn(process.execPath, [path.join(root, "node_modules/.bin/tsci"), "push", "index.circuit.tsx"],
		{ cwd: project, stdio: "inherit" });
	const code = await new Promise((resolve, reject) => {
		child.once("error", reject);
		child.once("exit", resolve);
	});
	if (code !== 0) throw new Error(`tsci push exited with ${code}`);
	const published = JSON.parse(await readFile(path.join(project, "package.json"), "utf8")).version;
	if (published !== expected)
		throw new Error(`Published ${published}; update and commit package.json to match the registry version.`);
} finally {
	await rm(temporary, { recursive: true, force: true });
}
