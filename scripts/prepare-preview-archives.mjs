import { readFile, writeFile, access } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { zipSync, strToU8 } from "fflate";

const root = fileURLToPath(new URL("../", import.meta.url));
const enclosure = path.join(root, "assets/enclosure");
const options = { level: 9, mtime: new Date(1980, 0, 1, 0, 0, 0) };
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const exists = (file) => access(file).then(() => true, () => false);
export const previewImages = [
  "printable-front.png", "printable-open-back.png", "printable-side.png", "printable-exploded.png",
  "display-retainer-installed.png", "display-ribbon-connection.png", "printable-pcb-mounts.png", "reader-print-plate.png",
];

// Git-linked releases omit ZIP/3MF binaries. Recreate them from tracked
// STEP/STL/JSON sources using the same pinned encoder as local packaging.
export async function preparePreviewArchives({ supplier = true, print = true, images = true, updateSupplier = false } = {}) {
  if (images) {
    for (const name of previewImages) {
      const destination = path.join(enclosure, name);
      if (await exists(destination)) continue;
      const source = JSON.parse(await readFile(path.join(enclosure, "preview-sources", name + ".json"), "utf8"));
      const bytes = Buffer.from(source.base64, "base64");
      if (digest(bytes) !== source.sha256) throw new Error(`Reconstructed preview differs: ${name}`);
      await writeFile(destination, bytes);
    }
  }
  if (supplier) {
    const manifestPath = path.join(root, "assets/components/supplier-step-archives.json");
    const archives = JSON.parse(await readFile(manifestPath, "utf8"));
    for (const archive of archives) {
      const destination = path.join(root, archive.path);
      if (updateSupplier || !(await exists(destination))) {
        const entries = {};
        for (const member of [...archive.step_files, "assets/components/sources.json"])
          entries[member] = new Uint8Array(await readFile(path.join(root, member)));
        const bytes = zipSync(entries, options);
        if (bytes.length > 3 * 1024 * 1024) throw new Error(`Split supplier archive: ${archive.path}`);
        if (updateSupplier) { archive.bytes = bytes.length; archive.sha256 = digest(bytes); }
        else if (digest(bytes) !== archive.sha256) throw new Error(`Reconstructed CAD archive differs: ${archive.path}`);
        await writeFile(destination, bytes);
      }
    }
    if (updateSupplier) await writeFile(manifestPath, JSON.stringify(archives, null, 2) + "\n");
  }
  if (print) {
    const { xml } = JSON.parse(await readFile(path.join(enclosure, "print-plate-model.json"), "utf8"));
    const plate = zipSync({
      "[Content_Types].xml": strToU8('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'),
      "_rels/.rels": strToU8('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'),
      "3D/3dmodel.model": strToU8(xml),
    }, options);
    await writeFile(path.join(enclosure, "reader-print-plate.3mf"), plate);
    const entries = {};
    for (const name of ["front-chassis", "rear-cover"])
      entries[name + ".stl"] = new Uint8Array(await readFile(path.join(enclosure, "print", name + ".stl")));
    entries["reader-print-plate.3mf"] = plate;
    for (const name of ["PRINTING.md", "fdm-reference.ini", "pcb-mounts.json", "display-connection.json", "enclosure-design.json", "stl/mesh-check.json", "stl/printability-check.json", "stl/clearance-check.json"])
      entries[name] = new Uint8Array(await readFile(path.join(enclosure, name)));
    await writeFile(path.join(enclosure, "esp32-reader-printable-stls.zip"), zipSync(entries, options));
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const supplierOnly = process.argv.includes("--supplier");
  const printOnly = process.argv.includes("--print");
  await preparePreviewArchives({ supplier: !printOnly, print: !supplierOnly, images: !supplierOnly && !printOnly, updateSupplier: supplierOnly });
}
