import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const circuitFile = path.resolve(process.argv[2] ?? path.join(root, "dist/index/circuit.json"));
const base = process.argv[3];
const circuit = JSON.parse(await readFile(circuitFile, "utf8"));
const paths = new Set();
for (const cad of circuit.filter((item) => item.type === "cad_component")) {
	for (const key of ["model_obj_url", "model_step_url", "model_glb_url"]) {
		if (!cad[key]) continue;
		assert(cad[key].startsWith("./"), `Unbundled model: ${cad[key]}`);
		paths.add(cad[key].slice(2));
	}
}
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const manifest = JSON.parse(await readFile(path.join(root, "assets/components/sources.json"), "utf8"));
for (const item of manifest) {
	assert.equal(digest(await readFile(path.join(root, item.path))), item.sha256, `Changed supplier CAD: ${item.path}`);
}
// These files must be directly downloadable from the hosted release as well.
for (const filename of ["reader-print-plate.3mf", "esp32-reader-printable-stls.zip", "PRINTING.md", "fdm-reference.ini"])
	paths.add("assets/enclosure/" + filename);
for (const filename of ["front-bezel", "main-body", "battery-partition", "rear-cover", "button-strip"])
	paths.add(`assets/enclosure/print/${filename}.stl`);
const results = [];
const todo = [...paths];
async function worker() {
	while (todo.length) {
		const relative = todo.shift();
		const source = await readFile(path.join(root, relative));
		assert(source.length > 0, `Empty asset: ${relative}`);
		if (relative.endsWith(".glb")) {
			assert.equal(source.subarray(0, 4).toString(), "glTF");
			assert.equal(source.readUInt32LE(4), 2);
			assert.equal(source.readUInt32LE(8), source.length);
			const json = JSON.parse(source.subarray(20, 20 + source.readUInt32LE(12)).toString());
			assert(json.meshes?.length, `Missing GLB mesh: ${relative}`);
			assert((json.buffers ?? []).every((buffer) => !buffer.uri), `External GLB buffer: ${relative}`);
		}
		if (relative.endsWith(".obj")) assert(/^v /m.test(source.toString()) && /^f /m.test(source.toString()), `Invalid OBJ: ${relative}`);
		const target = base ? new URL(relative, base).href : path.join(root, "dist", relative);
		const deployed = base
			? await fetch(target, { signal: AbortSignal.timeout(60000) }).then(async (response) => {
				assert.equal(response.status, 200, `Unavailable model/file: ${target}`);
				return Buffer.from(await response.arrayBuffer());
			})
			: await readFile(target);
		assert.equal(digest(deployed), digest(source), `Asset does not match source: ${target}`);
		results.push({ path: relative, bytes: source.length, sha256: digest(source), matches_source: true });
	}
}
await Promise.all([worker(), worker(), worker()]);
await mkdir(path.join(root, "checks/model-assets"), { recursive: true });
await writeFile(path.join(root, "checks/model-assets", base ? "published.json" : "local.json"), JSON.stringify({ circuit: circuitFile, base: base ?? "dist", assets: results.sort((a, b) => a.path.localeCompare(b.path)) }, null, 2) + "\n");
console.log(`Verified ${results.length} bundled models and print files; all match source.`);
