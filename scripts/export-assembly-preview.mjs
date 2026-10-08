import { createServer } from "node:http";
import { readFile, writeFile, mkdtemp, rm, mkdir } from "node:fs/promises";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const output = path.resolve(process.argv[2] ?? path.join(root, "dist/index/assembly.glb"));
const circuit = JSON.parse(await readFile(path.join(root, "dist/index/circuit.json"), "utf8"));
if (circuit.some((item) => item.type.endsWith("_error")))
	throw new Error("Build the circuit without errors before exporting the assembly");

// The CLI resolves remote CAD but cannot fetch ./ paths from a JSON export.
// Serve only the referenced local CAD files, on loopback, for this export.
const localModels = new Map();
for (const item of circuit.filter((item) => item.type === "cad_component")) {
	for (const key of ["model_glb_url", "model_obj_url", "model_step_url"]) {
		if (!item[key]?.startsWith("./")) continue;
		const relative = item[key].slice(2);
		const absolute = path.resolve(root, relative);
		if (!absolute.startsWith(root) || ![".glb", ".obj", ".step"].includes(path.extname(absolute)))
			throw new Error(`Unsupported local CAD path: ${relative}`);
		localModels.set("/" + relative, await readFile(absolute));
	}
}
const server = createServer((request, response) => {
	const key = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
	const bytes = localModels.get(key);
	if (!bytes) { response.writeHead(404); response.end(); return; }
	response.writeHead(200, { "Content-Type": key.endsWith(".glb") ? "model/gltf-binary" : "text/plain" });
	response.end(bytes);
});
await new Promise((resolve, reject) => {
	server.once("error", reject);
	server.listen(0, "127.0.0.1", resolve);
});
const temporary = await mkdtemp(path.join(tmpdir(), "reader-assembly-"));
try {
	const base = `http://127.0.0.1:${server.address().port}`;
	for (const item of circuit.filter((item) => item.type === "cad_component")) {
		for (const key of ["model_glb_url", "model_obj_url", "model_step_url"])
			if (item[key]?.startsWith("./")) item[key] = base + "/" + item[key].slice(2);
	}
	const input = path.join(temporary, "assembly.circuit.json");
	await writeFile(input, JSON.stringify(circuit));
	await mkdir(path.dirname(output), { recursive: true });
	const child = spawn(process.execPath, [path.join(root, "node_modules/.bin/tsci"), "export", input, "--format", "glb", "--output", output], { cwd: root });
	let diagnostics = "";
	for (const stream of [child.stdout, child.stderr]) stream.on("data", (chunk) => { diagnostics += chunk; process.stdout.write(chunk); });
	const code = await new Promise((resolve, reject) => { child.once("error", reject); child.once("exit", resolve); });
	if (code !== 0 || /Failed to fetch (GLB|OBJ)/i.test(diagnostics))
		throw new Error("Assembly export failed or substituted a missing CAD model");
} finally {
	await new Promise((resolve) => server.close(resolve));
	await rm(temporary, { recursive: true, force: true });
}
