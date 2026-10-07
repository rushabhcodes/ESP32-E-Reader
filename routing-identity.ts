import type { SimpleRouteJson } from "tscircuit";

/** Stable physical identities, independent of schematic-generated database IDs. */
export function routingIdentity(input: SimpleRouteJson) {
	const identities = new Map<string, string>();
	const idShapes = new Map<string, Set<string>>();
	const addShape = (id: string, shape: string) => {
		const shapes = idShapes.get(id) ?? new Set<string>();
		shapes.add(shape);
		idShapes.set(id, shapes);
	};
	const shapes = input.obstacles.map((obstacle) => {
		const { connectedTo, circuitJsonMetadata, obstacleId, ...shape } = obstacle;
		return JSON.stringify(sortedObject(shape));
	});
	const shapeNumbers = new Map(
		[...new Set(shapes)].sort().map((shape, index) => [shape, index]),
	);
	for (const [index, obstacle] of input.obstacles.entries()) {
		const { circuitJsonMetadata, obstacleId } = obstacle;
		const identity = String(shapeNumbers.get(shapes[index]));
		const metadata = circuitJsonMetadata as Record<string, string> | undefined;
		for (const [key, id] of Object.entries(metadata ?? {})) {
			if (key.endsWith("_id")) addShape(id, `${key}:${identity}`);
		}
		if (obstacleId) addShape(obstacleId, `obstacle:${identity}`);
	}
	for (const [id, shapes] of idShapes) {
		identities.set(id, JSON.stringify([...shapes].sort()));
	}
	const normalize = (value: unknown): unknown => {
		if (typeof value === "string") return identities.get(value) ?? value;
		if (Array.isArray(value)) return value.map(normalize);
		if (value && typeof value === "object") {
			return Object.fromEntries(
				Object.entries(value)
					.sort(([a], [b]) => a.localeCompare(b))
					.map(([key, item]) => {
						if (key === "connectedTo" || key === "offBoardConnectsTo") {
							// These IDs are an extra alias for the full connectivity set below.
							// Their numbers also count schematic objects and are not stable.
							const ids = (item as string[]).filter(
								(id) => !/^connectivity_net\d+$/.test(id),
							);
							return [key, ids.map(normalize).sort()];
						}
						if (key === "pointsToConnect" || key === "layers") {
							return [
								key,
								(item as unknown[]).map(normalize).sort(compareJson),
							];
						}
						return [key, normalize(item)];
					}),
			);
		}
		return value;
	};
	const { obstacles, connections, ...settings } = input;
	return {
		identities,
		signature: JSON.stringify({
			settings: normalize(settings),
			obstacles: obstacles.map(normalize).sort(compareJson),
			connections: connections.map(normalize).sort(compareJson),
		}),
	};
}

function compareJson(a: unknown, b: unknown) {
	return JSON.stringify(a).localeCompare(JSON.stringify(b));
}

function sortedObject(value: unknown): unknown {
	if (Array.isArray(value)) return value.map(sortedObject).sort(compareJson);
	if (!value || typeof value !== "object") return value;
	return Object.fromEntries(
		Object.entries(value)
			.sort(([a], [b]) => a.localeCompare(b))
			.map(([key, item]) => [key, sortedObject(item)]),
	);
}
