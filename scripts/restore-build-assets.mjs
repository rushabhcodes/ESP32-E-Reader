import { readFile, writeFile, mkdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import { gunzipSync } from "fflate";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");

export async function restoreBuildAssets() {
  const manifest = JSON.parse(await readFile(path.join(root, "assets/enclosure/binary-sources/manifest.json"), "utf8"));
  for (const item of manifest) {
    const destination = path.resolve(root, item.path);
    if (!destination.startsWith(path.join(root, "assets/enclosure") + path.sep))
      throw new Error(`Invalid binary asset path: ${item.path}`);
    const existing = await readFile(destination).catch((error) => {
      if (error.code !== "ENOENT") throw error;
    });
    if (existing) {
      if (digest(existing) !== item.sha256)
        throw new Error(`Stale binary backup: ${item.path}; run python3 scripts/package-build-assets.py`);
      continue;
    }
    const source = JSON.parse(await readFile(path.join(root, item.source), "utf8"));
    if (source.path !== item.path || source.sha256 !== item.sha256)
      throw new Error(`Binary source does not match manifest: ${item.path}`);
    const bytes = Buffer.from(gunzipSync(Buffer.from(source.gzip_base64, "base64")));
    if (bytes.length !== item.bytes || digest(bytes) !== item.sha256)
      throw new Error(`Reconstructed binary differs: ${item.path}`);
    await mkdir(path.dirname(destination), { recursive: true });
    await writeFile(destination, bytes);
  }
}

if (import.meta.main) await restoreBuildAssets();
