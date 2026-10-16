import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

// A visible pad can still be absent from the router's connectivity graph.
// Catch this before accepting a build or exporting assembly files.
const circuit = JSON.parse(
	await readFile(process.argv[2] ?? "dist/index/circuit.json", "utf8"),
);
const sourceComponents = new Map(
	circuit
		.filter((e) => e.type === "source_component")
		.map((e) => [e.source_component_id, e]),
);
const pcbComponents = new Map(
	circuit
		.filter((e) => e.type === "pcb_component")
		.map((e) => [e.pcb_component_id, e]),
);
const sourcePorts = new Map(
	circuit
		.filter((e) => e.type === "source_port")
		.map((e) => [e.source_port_id, e]),
);
const pcbPorts = new Map(
	circuit.filter((e) => e.type === "pcb_port").map((e) => [e.pcb_port_id, e]),
);
const pads = circuit.filter(
	(e) =>
		["pcb_smtpad", "pcb_plated_hole"].includes(e.type) && e.port_hints?.length,
);
const missing = [];
for (const pad of pads) {
	const component = pcbComponents.get(pad.pcb_component_id);
	const name =
		sourceComponents.get(component?.source_component_id)?.name ??
		pad.pcb_component_id;
	const pcbPort = pcbPorts.get(pad.pcb_port_id);
	const sourcePort = sourcePorts.get(pcbPort?.source_port_id);
	if (
		!pcbPort ||
		!sourcePort ||
		sourcePort.source_component_id !== component?.source_component_id ||
		pcbPort.pcb_component_id !== pad.pcb_component_id
	)
		missing.push(`${name}: ${pad.port_hints.join("/")}`);
}
assert.equal(
	missing.length,
	0,
	`Pads missing electrical port associations:\n${missing.join("\n")}`,
);
console.log(`Verified electrical port associations for ${pads.length} pads.`);
