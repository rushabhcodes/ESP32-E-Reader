import type { SimpleRouteJson, SimplifiedPcbTrace } from "tscircuit";
import verified from "./verified-pcb-routes.json";
import { routingIdentity } from "./routing-identity";

// Preserve the published, DRC-checked PCB when only schematic presentation
// changes. Geometry, connectivity, widths, keepouts and rules must all match.
export function getVerifiedPcbRoutes(input: SimpleRouteJson) {
	const previous = routingIdentity(verified.input as SimpleRouteJson);
	const current = routingIdentity(input);
	if (previous.signature !== current.signature) return undefined;

	const currentIds = new Map(
		[...current.identities].map(([id, identity]) => [identity, id]),
	);
	const replaceIds = (value: unknown): unknown => {
		if (typeof value === "string") {
			const identity = previous.identities.get(value);
			return identity ? (currentIds.get(identity) ?? value) : value;
		}
		if (Array.isArray(value)) return value.map(replaceIds);
		if (value && typeof value === "object") {
			return Object.fromEntries(
				Object.entries(value).map(([key, item]) => [key, replaceIds(item)]),
			);
		}
		return value;
	};
	return replaceIds(verified.traces) as SimplifiedPcbTrace[];
}
