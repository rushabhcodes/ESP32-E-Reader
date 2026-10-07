import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import mounts from "../assets/enclosure/pcb-mounts.json";

const near = (a, b) => Math.abs(a - b) < 1e-6;
const distanceToSegment = (point, a, b) => {
	const dx = b.x - a.x;
	const dy = b.y - a.y;
	const lengthSquared = dx * dx + dy * dy;
	const t = lengthSquared
		? Math.max(
				0,
				Math.min(
					1,
					((point.x - a.x) * dx + (point.y - a.y) * dy) / lengthSquared,
				),
			)
		: 0;
	return Math.hypot(point.x - a.x - t * dx, point.y - a.y - t * dy);
};
const insideRing = (point, vertices) => {
	let inside = false;
	for (let i = 0, j = vertices.length - 1; i < vertices.length; j = i++) {
		const a = vertices[i],
			b = vertices[j];
		if (
			a.y > point.y !== b.y > point.y &&
			point.x < ((b.x - a.x) * (point.y - a.y)) / (b.y - a.y) + a.x
		) {
			inside = !inside;
		}
	}
	return inside;
};
const ringDistance = (point, vertices) =>
	Math.min(
		...vertices.map((a, i) =>
			distanceToSegment(point, a, vertices[(i + 1) % vertices.length]),
		),
	);
const distanceToPour = (point, pour) => {
	assert.equal(pour.shape, "brep", "Unsupported copper pour geometry");
	const { outer_ring, inner_rings } = pour.brep_shape;
	if (!insideRing(point, outer_ring.vertices))
		return ringDistance(point, outer_ring.vertices);
	const containingHoles = inner_rings.filter((ring) =>
		insideRing(point, ring.vertices),
	);
	return containingHoles.length
		? Math.min(
				...containingHoles.map((ring) => ringDistance(point, ring.vertices)),
			)
		: 0;
};

export function checkPcbMounts(circuit) {
	assert(
		circuit.some((e) => e.type === "pcb_trace"),
		"Missing routed PCB copper",
	);
	const board = circuit.find((e) => e.type === "pcb_board");
	assert(board?.outline, "Missing PCB outline");
	assert.equal(mounts.mounts.length, 4, "Both ends require two screw points");
	const pours = circuit.filter((e) => e.type === "pcb_copper_pour");
	if (pours.length)
		assert.deepEqual([...new Set(pours.map((e) => e.layer))].sort(), [
			"bottom",
			"inner1",
			"inner2",
			"top",
		]);
	const report = [];
	for (const mount of mounts.mounts) {
		const holes = circuit.filter(
			(e) => e.type === "pcb_hole" && near(e.x, mount.x) && near(e.y, mount.y),
		);
		assert.equal(holes.length, 1, `Missing or duplicate ${mount.name} hole`);
		assert(
			near(holes[0].hole_diameter, mounts.holeDiameter),
			`Wrong ${mount.name} diameter`,
		);
		const keepout = circuit.find(
			(e) =>
				e.type === "pcb_keepout" &&
				near(e.center.x, mount.x) &&
				near(e.center.y, mount.y),
		);
		assert(
			keepout?.shape === "circle" &&
				near(keepout.radius, mounts.copperKeepoutRadius),
			`Missing ${mount.name} screw keepout`,
		);
		assert.deepEqual([...keepout.layers].sort(), [
			"bottom",
			"inner1",
			"inner2",
			"top",
		]);
		assert(insideRing(mount, board.outline), `${mount.name} lies outside PCB`);
		const outlineDistance = Math.min(
			...board.outline.map((a, i) =>
				distanceToSegment(
					mount,
					a,
					board.outline[(i + 1) % board.outline.length],
				),
			),
		);
		assert(
			outlineDistance >=
				mounts.holeDiameter / 2 + board.min_board_edge_clearance,
			`${mount.name} drill too close to edge`,
		);
		let traceDistance = Infinity;
		let padDistance = Infinity;
		for (const element of circuit) {
			if (element.type === "pcb_trace") {
				for (let i = 1; i < element.route.length; i++) {
					const a = element.route[i - 1],
						b = element.route[i];
					traceDistance = Math.min(
						traceDistance,
						distanceToSegment(mount, a, b) -
							Math.max(a.width ?? 0, b.width ?? 0) / 2,
					);
				}
			} else if (
				element.type === "pcb_via" ||
				element.type === "pcb_plated_hole"
			) {
				const diameter =
					element.outer_diameter ??
					Math.hypot(element.outer_width ?? 0, element.outer_height ?? 0);
				padDistance = Math.min(
					padDistance,
					Math.hypot(mount.x - element.x, mount.y - element.y) - diameter / 2,
				);
			} else if (element.type === "pcb_smtpad") {
				let distance;
				if (element.x !== undefined) {
					// A circumscribed circle also covers rotated rectangular pads.
					const radius =
						element.radius ??
						Math.hypot(element.width ?? 0, element.height ?? 0) / 2;
					distance =
						Math.hypot(mount.x - element.x, mount.y - element.y) - radius;
				} else {
					const xs = element.points.map((p) => p.x),
						ys = element.points.map((p) => p.y);
					distance = Math.hypot(
						Math.max(Math.min(...xs) - mount.x, 0, mount.x - Math.max(...xs)),
						Math.max(Math.min(...ys) - mount.y, 0, mount.y - Math.max(...ys)),
					);
				}
				padDistance = Math.min(padDistance, distance);
			}
		}
		assert(
			traceDistance >= keepout.radius,
			`${mount.name} overlaps routed copper`,
		);
		assert(
			padDistance >= keepout.radius,
			`${mount.name} overlaps pad/via envelope`,
		);
		const pourDistance = pours.length
			? Math.min(...pours.map((pour) => distanceToPour(mount, pour)))
			: null;
		// The exported circular keepout uses a 32-sided polygon; its apothem
		// is slightly smaller than the specified radius.
		if (pourDistance !== null)
			assert(
				pourDistance >= keepout.radius * Math.cos(Math.PI / 32) - 1e-5,
				`${mount.name} overlaps copper pour keepout`,
			);
		report.push({
			name: mount.name,
			holeEdgeToBoardEdge: outlineDistance - mounts.holeDiameter / 2,
			traceClearanceFromKeepout: traceDistance - keepout.radius,
			conservativePadClearanceFromKeepout: padDistance - keepout.radius,
			copperPourClearanceFromHole:
				pourDistance === null ? null : pourDistance - mounts.holeDiameter / 2,
		});
	}
	return report;
}

if (import.meta.main) {
	const circuit = JSON.parse(
		await readFile(process.argv[2] ?? "dist/index/circuit.json", "utf8"),
	);
	console.log(JSON.stringify(checkPcbMounts(circuit), null, 2));
}
