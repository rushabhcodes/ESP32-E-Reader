import { copyFile, mkdir, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = fileURLToPath(new URL("../", import.meta.url));
const previewExtensions = new Set([".glb", ".obj", ".step", ".png", ".stl", ".3mf", ".zip", ".md", ".ini", ".json", ".csv"]);
let copiedAssets = 0;

async function copyModels(relativeDirectory) {
	const entries = await readdir(path.join(projectRoot, relativeDirectory), {
		withFileTypes: true,
	});

	for (const entry of entries) {
		const relativePath = path.join(relativeDirectory, entry.name);
		if (entry.isDirectory()) {
			await copyModels(relativePath);
		} else if (entry.isFile() && previewExtensions.has(path.extname(entry.name))) {
			// Circuit JSON and README retain these paths; hosted views need them.
			const destination = path.join(projectRoot, "dist", relativePath);
			await mkdir(path.dirname(destination), { recursive: true });
			await copyFile(path.join(projectRoot, relativePath), destination);
			copiedAssets += 1;
		}
	}
}

await copyModels("assets");
await copyModels("imports");
console.log(`Copied ${copiedAssets} local preview assets to dist.`);
