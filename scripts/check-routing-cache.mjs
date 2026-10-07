import assert from "node:assert/strict";
import verified from "../verified-pcb-routes.json";
import { getVerifiedPcbRoutes } from "../verified-pcb-routes.ts";

assert.equal(getVerifiedPcbRoutes(verified.input).length, 228);

// Regenerating database IDs or reordering input elements must preserve routes
// and reconnect their endpoints to the newly generated physical port IDs.
const rename = (value) => {
	if (
		typeof value === "string" &&
		/^pcb_(port|smtpad|plated_hole|hole)_\d+$/.test(value)
	)
		return `${value}_regenerated`;
	if (typeof value === "string" && /^connectivity_net\d+$/.test(value))
		return `connectivity_net${Number(value.slice(16)) + 10000}`;
	if (Array.isArray(value)) return value.map(rename);
	if (value && typeof value === "object")
		return Object.fromEntries(
			Object.entries(value).map(([key, item]) => [key, rename(item)]),
		);
	return value;
};
const regenerated = rename(verified.input);
regenerated.obstacles.reverse();
regenerated.connections.reverse();
for (const connection of regenerated.connections)
	connection.pointsToConnect.reverse();
const regeneratedRoutes = getVerifiedPcbRoutes(regenerated);
assert.ok(
	regeneratedRoutes,
	"Generated IDs and element order must not invalidate verified routes",
);
assert.equal(
	JSON.stringify(regeneratedRoutes),
	JSON.stringify(rename(verified.traces)),
	"Endpoints must follow regenerated port IDs",
);

const physicalChanges = [
	(input) => {
		input.obstacles[0].center.x += 0.1;
	},
	(input) => {
		input.obstacles[0].width += 0.1;
	},
	(input) => {
		input.obstacles[0].layers = ["bottom"];
	},
	(input) => {
		input.obstacles[0].connectedTo.push("source_net_new");
	},
	(input) => {
		input.connections[0].pointsToConnect[0].x += 0.1;
	},
	(input) => {
		input.connections[0].width += 0.1;
	},
	(input) => {
		input.minBoardEdgeClearance += 0.1;
	},
	(input) => {
		input.outline[0].x += 0.1;
	},
	(input) => {
		input.allowViaInPad = true;
	},
];
for (const change of physicalChanges) {
	const input = structuredClone(verified.input);
	change(input);
	assert.equal(
		getVerifiedPcbRoutes(input),
		undefined,
		"Physical change must invalidate verified routes",
	);
}
console.log(
	"Verified route reuse, endpoint remapping, and physical-change invalidation passed.",
);
