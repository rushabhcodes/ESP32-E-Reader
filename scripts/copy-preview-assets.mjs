import { copyFile, mkdir, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("../", import.meta.url));
const modelExtensions = new Set([".glb", ".obj", ".step"]);
let copiedModels = 0;

async function copyModels(relativeDirectory) {
	const entries = await readdir(path.join(projectRoot, relativeDirectory), {
		withFileTypes: true,
	});

	for (const entry of entries) {
		const relativePath = path.join(relativeDirectory, entry.name);
		if (entry.isDirectory()) {
			await copyModels(relativePath);
		} else if (entry.isFile() && modelExtensions.has(path.extname(entry.name))) {
			// Circuit JSON retains these paths; the hosted viewer needs them too.
			const destination = path.join(projectRoot, "dist", relativePath);
			await mkdir(path.dirname(destination), { recursive: true });
			await copyFile(path.join(projectRoot, relativePath), destination);
			copiedModels += 1;
		}
	}
}

await copyModels("assets");
await copyModels("imports");
console.log(`Copied ${copiedModels} local 3D model assets to dist.`);
