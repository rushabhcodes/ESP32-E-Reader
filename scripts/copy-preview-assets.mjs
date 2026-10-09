import { copyFile, mkdir, readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../", import.meta.url));
const files = [
  "assets/components/sources.json", "assets/components/supplier-step-archives.json",
  "imports/USB4105_GF_A/USB4105_GF_A.obj",
];
for (const name of await readdir(path.join(root, "assets/components")))
  if (name.endsWith(".obj")) files.push("assets/components/" + name);
const archives = JSON.parse(await readFile(path.join(root, "assets/components/supplier-step-archives.json"), "utf8"));
files.push(...archives.map((archive) => archive.path));
const enclosure = [
  "front-chassis.glb", "rear-cover.glb", "display-panel.glb", "display-cushioning.glb",
  "pcb-cover-fasteners.glb", "battery-envelope-DO-NOT-PRINT.glb",
  "antenna-envelope-DO-NOT-PRINT.glb", "battery-liner-DO-NOT-PRINT.glb", "battery-adhesive-DO-NOT-PRINT.glb",
  "print/front-chassis.stl", "print/rear-cover.stl", "reader-print-plate.3mf",
  "esp32-reader-printable-stls.zip", "PRINTING.md", "fdm-reference.ini", "enclosure-design.json",
  "pcb-mounts.json", "display-connection.json", "component-inventory.csv", "component-envelopes.csv",
  "printable-front.png", "printable-open-back.png", "printable-side.png", "printable-exploded.png",
  "display-retainer-installed.png", "display-ribbon-connection.png", "printable-pcb-mounts.png", "reader-print-plate.png",
  "stl/mesh-check.json", "stl/clearance-check.json", "stl/assembly-check.json",
  "stl/display-retainer-check.json", "stl/display-connection-check.json", "stl/printability-check.json",
];
files.push(...enclosure.map((name) => "assets/enclosure/" + name));
// The browser loads OBJ/GLB. Keep supplier STEP originals together in a ZIP;
// copying every STEP twice made registry finalization exceed its time limit.
for (const file of files) {
  const destination = path.join(root, "dist", file);
  await mkdir(path.dirname(destination), { recursive: true });
  await copyFile(path.join(root, file), destination);
}
console.log(`Copied ${files.length} browser models, print files and previews to dist.`);
