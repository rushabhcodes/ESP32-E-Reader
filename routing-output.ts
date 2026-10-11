import type { SimpleRouteJson, SimplifiedPcbTrace } from "tscircuit";

/** Discard a disconnected solver seed only when a complete replacement exists.
 * Pipeline9 can return both an inner-layer seed and its route with endpoint vias.
 * Keeping the seed creates floating copper and bypasses the connector keepout.
 */
export function removeSupersededRoutingSeeds(
  input: SimpleRouteJson,
  traces: SimplifiedPcbTrace[],
) {
  const near = (a: { x: number; y: number }, b: { x: number; y: number }) =>
    Math.hypot(a.x - b.x, a.y - b.y) < 1e-5;
  const complete = (trace: SimplifiedPcbTrace) => {
    const connection = input.connections.find(c => c.name === trace.connection_name);
    if (connection?.pointsToConnect.length !== 2) return undefined;
    if (near(connection.pointsToConnect[0], connection.pointsToConnect[1])) return undefined;
    const wires = trace.route.filter(p => p.route_type === "wire");
    if (wires.length < 2) return false;
    const terminals = [wires[0], wires[wires.length - 1]].map(wire =>
      connection.pointsToConnect.findIndex(point => near(point, wire)));
    if (terminals.includes(-1) || terminals[0] === terminals[1]) return false;
    let layer = wires[0].layer;
    if (trace.route[0].route_type !== "wire") return undefined;
    let previous: Extract<SimplifiedPcbTrace["route"][number], { route_type: "wire" | "via" }> = wires[0];
    for (const point of trace.route) {
      if (point.route_type === "via") {
        if (!near(previous, point) || point.from_layer !== layer) return false;
        layer = point.to_layer;
      } else if (point.route_type === "wire") {
        if (point.layer !== layer || (previous.route_type === "via" && !near(previous, point))) return false;
      } else return undefined;
      previous = point;
    }
    return [wires[0], wires[wires.length - 1]].every(wire => {
      const point = connection.pointsToConnect.find(p => near(p, wire));
      if (!point) return false;
      const layers = point.layers ?? [point.layer];
      return layers.includes(wire.layer) || trace.route.some(p =>
        p.route_type === "via" && near(p, wire) &&
        (layers.includes(p.from_layer) || layers.includes(p.to_layer)));
    });
  };
  const sameTerminals = (a: SimplifiedPcbTrace, b: SimplifiedPcbTrace) => {
    const aPorts = a.connectsTo ?? [], bPorts = b.connectsTo ?? [];
    return a.connection_name === b.connection_name && aPorts.length === 2 &&
      bPorts.length === 2 && aPorts.every(id => bPorts.includes(id));
  };
  return traces.filter(trace => complete(trace) !== false ||
    !traces.some(replacement => replacement !== trace &&
      sameTerminals(trace, replacement) && complete(replacement) === true));
}
