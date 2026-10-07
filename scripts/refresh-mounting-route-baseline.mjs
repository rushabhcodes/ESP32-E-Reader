import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import {
	getSimpleRouteJsonFromCircuitJson,
	unrouteCircuitJson,
} from "tscircuit";
import { getVerifiedPcbRoutes } from "../verified-pcb-routes.ts";
import { routingIdentity } from "../routing-identity.ts";
import mounts from "../assets/enclosure/pcb-mounts.json";
import { checkPcbMounts } from "./check-pcb-mounts.mjs";

// A controlled baseline refresh for added mounting holes outside existing
// copper. The production guard stays strict. Existing geometry, connectivity,
// and every routing rule must match; a full build and shorts check follow.
const [beforePath, placementPath] = process.argv.slice(2);
assert(
	beforePath && placementPath,
	"Supply the previous circuit and new unrouted placement JSON",
);
const before = JSON.parse(await readFile(beforePath, "utf8"));
const placement = JSON.parse(await readFile(placementPath, "utf8"));
const baselinePath = new URL("../verified-pcb-routes.json", import.meta.url);
const baseline = JSON.parse(await readFile(baselinePath, "utf8"));
const inputFor = (circuit) => {
	const input = getSimpleRouteJsonFromCircuitJson({
		circuitJson: unrouteCircuitJson(circuit).filter(
			(e) => e.type !== "pcb_via",
		),
		subcircuit_id: "subcircuit_source_group_0",
		minTraceWidth: 0.15,
		nominalTraceWidth: 0.15,
		ignoreExistingTopLevelPcbRouteState: true,
	}).simpleRouteJson;
	input.allowViaInPad = false;
	if (input.traces?.length === 0) delete input.traces;
	return input;
};
assert.equal(
	routingIdentity(inputFor(before)).signature ===
		routingIdentity(baseline.input).signature,
	true,
	"Previous PCB does not match the verified baseline",
);
const input = inputFor(placement);
assert.equal(
	getVerifiedPcbRoutes(input),
	undefined,
	"Physical additions must invalidate the old production baseline",
);
const addedMounts = mounts.mounts.filter(
	(mount) =>
		!before.some(
			(e) =>
				e.type === "pcb_hole" &&
				Math.abs(e.x - mount.x) < 1e-6 &&
				Math.abs(e.y - mount.y) < 1e-6,
		),
);
assert.equal(
	addedMounts.length,
	2,
	"Expected exactly two added mounting holes",
);
const addedObstacles = input.obstacles.filter((obstacle) =>
	addedMounts.some(
		(mount) =>
			Math.abs(obstacle.center.x - mount.x) < 1e-6 &&
			Math.abs(obstacle.center.y - mount.y) < 1e-6,
	),
);
assert.equal(
	addedObstacles.length,
	4,
	"Expected two drills and two circular keepouts",
);
for (const mount of addedMounts) {
	const obstacles = addedObstacles.filter(
		(o) => Math.abs(o.center.x - mount.x) < 1e-6,
	);
	assert(
		obstacles.some(
			(o) =>
				o.isNonPlatedHole &&
				o.shape === "circle" &&
				o.width === mounts.holeDiameter &&
				o.height === mounts.holeDiameter,
		),
	);
	assert(
		obstacles.some(
			(o) =>
				o.type === "oval" &&
				o.width === mounts.copperKeepoutRadius * 2 &&
				o.height === mounts.copperKeepoutRadius * 2,
		),
	);
	for (const obstacle of obstacles) {
		assert.deepEqual([...obstacle.layers].sort(), [
			"bottom",
			"inner1",
			"inner2",
			"top",
		]);
		assert.deepEqual(obstacle.connectedTo, []);
	}
}
// Removing only these four additions must recover the complete previous
// routing input. This also remaps generated pad/hole/port IDs safely.
// Core's search bounds enclose obstacles and the outline with a 1 mm margin.
// Added keepouts can extend that search region without changing the PCB
// outline. Admit only the bounds derived from these four additions.
const expectedBounds = { ...baseline.input.bounds };
for (const obstacle of addedObstacles) {
	expectedBounds.minX = Math.min(
		expectedBounds.minX,
		obstacle.center.x - obstacle.width / 2 - 1,
	);
	expectedBounds.maxX = Math.max(
		expectedBounds.maxX,
		obstacle.center.x + obstacle.width / 2 + 1,
	);
	expectedBounds.minY = Math.min(
		expectedBounds.minY,
		obstacle.center.y - obstacle.height / 2 - 1,
	);
	expectedBounds.maxY = Math.max(
		expectedBounds.maxY,
		obstacle.center.y + obstacle.height / 2 + 1,
	);
}
assert.deepEqual(
	input.bounds,
	expectedBounds,
	"Unexpected routing search bounds change",
);
const previousGeometry = {
	...input,
	bounds: baseline.input.bounds,
	obstacles: input.obstacles.filter((o) => !addedObstacles.includes(o)),
};
const traces = getVerifiedPcbRoutes(previousGeometry);
assert(traces, "Existing obstacles, rules, or electrical connections changed");
const clearance = checkPcbMounts([
	// The routing-disabled build's provisional pours are regenerated after
	// restoring traces. Check the finished pours in the full build instead.
	...placement.filter((e) => e.type !== "pcb_copper_pour"),
	...traces,
	...before.filter((e) => e.type === "pcb_via"),
]);
await writeFile(baselinePath, JSON.stringify({ input, traces }));
console.log(
	JSON.stringify(
		{
			addedMounts: addedMounts.map((m) => m.name),
			unchangedExistingRoutingInput: true,
			preservedTraces: traces.length,
			clearance,
		},
		null,
		2,
	),
);
