import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const tolerance = 1e-6;
const pointKey = ({ x, y }) =>
	`${Math.round(x / tolerance)},${Math.round(y / tolerance)}`;
const liesOn = (point, edge) => {
	const dx = edge.to.x - edge.from.x;
	const dy = edge.to.y - edge.from.y;
	const cross = (point.x - edge.from.x) * dy - (point.y - edge.from.y) * dx;
	return (
		Math.abs(cross) < tolerance &&
		point.x >= Math.min(edge.from.x, edge.to.x) - tolerance &&
		point.x <= Math.max(edge.from.x, edge.to.x) + tolerance &&
		point.y >= Math.min(edge.from.y, edge.to.y) - tolerance &&
		point.y <= Math.max(edge.from.y, edge.to.y) + tolerance
	);
};

export function checkControlsSchematic(circuit) {
	const sheet = circuit.find(
		(e) => e.type === "schematic_sheet" && e.name === "controls",
	);
	assert(sheet, "Missing controls sheet");
	const components = new Map(
		circuit
			.filter((e) => e.type === "source_component")
			.map((e) => [e.name, e]),
	);
	const pin = (reference, number) => {
		const component = components.get(reference);
		const source = circuit.find(
			(e) =>
				e.type === "source_port" &&
				e.source_component_id === component?.source_component_id &&
				e.pin_number === number,
		);
		assert(source, `Missing physical pin ${reference}.${number}`);
		const schematic = circuit.find(
			(e) =>
				e.type === "schematic_port" &&
				e.source_port_id === source.source_port_id &&
				e.schematic_sheet_id === sheet.schematic_sheet_id,
		);
		assert(schematic, `Missing schematic terminal ${reference}.${number}`);
		return {
			name: `${reference}.${number}`,
			source,
			point: schematic.center,
			componentId: schematic.schematic_component_id,
		};
	};
	const continuousWire = (pins) => {
		const net = pins[0].source.subcircuit_connectivity_map_key;
		assert(net, `Missing net for ${pins[0].name}`);
		assert(
			pins.every((p) => p.source.subcircuit_connectivity_map_key === net),
			"Expected pins to share one electrical net",
		);
		const edges = circuit
			.filter(
				(e) =>
					e.type === "schematic_trace" &&
					e.schematic_sheet_id === sheet.schematic_sheet_id &&
					e.subcircuit_connectivity_map_key === net,
			)
			.flatMap((e) => e.edges);
		const points = new Map(
			[
				...pins.map((p) => p.point),
				...edges.flatMap((e) => [e.from, e.to]),
			].map((p) => [pointKey(p), p]),
		);
		const graph = new Map([...points.keys()].map((key) => [key, new Set()]));
		for (const edge of edges) {
			const start = pointKey(edge.from);
			for (const [key, point] of points) {
				if (!liesOn(point, edge)) continue;
				graph.get(start).add(key);
				graph.get(key).add(start);
			}
		}
		const reached = new Set();
		const queue = [pointKey(pins[0].point)];
		for (const key of queue) {
			if (reached.has(key)) continue;
			reached.add(key);
			queue.push(...graph.get(key));
		}
		for (const p of pins) {
			assert(
				reached.has(pointKey(p.point)),
				`No continuous schematic wire from ${pins[0].name} to ${p.name}`,
			);
		}
	};

	continuousWire([
		pin("R11", 2),
		...["SW2", "SW3", "SW4", "SW6"].map((ref) => pin(ref, 4)),
	]);
	for (const [resistor, button] of [
		["R1", "SW2"],
		["R3", "SW3"],
		["R6", "SW4"],
	]) {
		continuousWire([pin(resistor, 1), pin(button, 1)]);
	}
	continuousWire([pin("R10", 2), pin("S2", 2)]);
	for (const reference of ["SW2", "SW3", "SW4", "SW6"]) {
		for (const number of [1, 4]) {
			const terminal = pin(reference, number);
			assert(
				circuit.some(
					(e) =>
						e.type === "schematic_line" &&
						e.schematic_component_id === terminal.componentId &&
						[
							pointKey({ x: e.x1, y: e.y1 }),
							pointKey({ x: e.x2, y: e.y2 }),
						].includes(pointKey(terminal.point)),
				),
				`Switch symbol does not touch terminal ${terminal.name}`,
			);
		}
	}
	return "Controls schematic: all four ADC terminals, common bus, resistor branches, and wake pull-up are connected.";
}

if (import.meta.main) {
	const path = process.argv[2] ?? "dist/index/circuit.json";
	console.log(checkControlsSchematic(JSON.parse(await readFile(path, "utf8"))));
}
