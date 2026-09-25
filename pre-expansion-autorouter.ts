import {
	type AutorouterCompleteEvent,
	type AutorouterErrorEvent,
	type AutorouterProgressEvent,
	type GenericLocalAutorouter,
	type SimpleRouteJson,
	type SimplifiedPcbTrace,
	SOLVERS,
} from "tscircuit";

type EventHandlers = {
	complete: Array<(event: AutorouterCompleteEvent) => void>;
	error: Array<(event: AutorouterErrorEvent) => void>;
	progress: Array<(event: AutorouterProgressEvent) => void>;
};

/**
 * Runs the standard local routing pipeline through trace-width and DRC repair,
 * then returns its traces before the optional power-trace expansion pass.
 * Explicit net widths and copper pours still define the board's power copper.
 */
export class PreExpansionAutorouter implements GenericLocalAutorouter {
	readonly input: SimpleRouteJson;
	isRouting = false;

	private readonly solver;
	private readonly eventHandlers: EventHandlers = {
		complete: [],
		error: [],
		progress: [],
	};
	private timeoutId?: ReturnType<typeof setTimeout>;
	private cycleCount = 0;

	constructor(input: SimpleRouteJson) {
		this.input = input;
		this.solver = new SOLVERS.AutoroutingPipelineSolver9_PreloadedTraceGraph(
			input as ConstructorParameters<
				typeof SOLVERS.AutoroutingPipelineSolver9_PreloadedTraceGraph
			>[0],
		);
	}

	start() {
		if (this.isRouting) return;
		this.isRouting = true;
		this.runCycle();
	}

	stop() {
		this.isRouting = false;
		if (this.timeoutId !== undefined) clearTimeout(this.timeoutId);
		this.timeoutId = undefined;
	}

	on(
		event: "complete" | "error" | "progress",
		callback:
			| ((event: AutorouterCompleteEvent) => void)
			| ((event: AutorouterErrorEvent) => void)
			| ((event: AutorouterProgressEvent) => void),
	) {
		(this.eventHandlers[event] as Array<typeof callback>).push(callback);
	}

	solveSync(): SimplifiedPcbTrace[] {
		this.solver.solveUntilPhase("powerTraceExpansionSolver");
		if (this.solver.failed) {
			throw new Error(this.solver.error || "Routing failed");
		}
		return this.getTraces();
	}

	private getTraces(): SimplifiedPcbTrace[] {
		return [
			...this.solver.getUpdatedPreloadedTraces(),
			...this.solver.getNewTracesBeforePowerExpansion(),
		];
	}

	private runCycle = () => {
		if (!this.isRouting) return;

		try {
			const cycleStartedAt = Date.now();
			const initialIterations = this.solver.iterations;

			while (
				Date.now() - cycleStartedAt < 250 &&
				!this.solver.failed &&
				!this.solver.solved &&
				this.solver.getCurrentPhase() !== "powerTraceExpansionSolver"
			) {
				this.solver.step();
			}

			if (this.solver.failed) {
				throw new Error(this.solver.error || "Routing failed");
			}

			if (
				this.solver.solved ||
				this.solver.getCurrentPhase() === "powerTraceExpansionSolver"
			) {
				this.isRouting = false;
				const event: AutorouterCompleteEvent = {
					type: "complete",
					traces: this.getTraces(),
				};
				for (const handler of this.eventHandlers.complete) handler(event);
				return;
			}

			this.cycleCount += 1;
			const elapsedMs = Math.max(Date.now() - cycleStartedAt, 1);
			const event: AutorouterProgressEvent = {
				type: "progress",
				steps: this.cycleCount,
				progress: this.solver.progress,
				phase: this.solver.getCurrentPhase(),
				iterationsPerSecond:
					((this.solver.iterations - initialIterations) / elapsedMs) * 1000,
			};
			for (const handler of this.eventHandlers.progress) handler(event);

			this.timeoutId = setTimeout(this.runCycle, 0);
		} catch (cause) {
			this.isRouting = false;
			const event: AutorouterErrorEvent = {
				type: "error",
				error: cause instanceof Error ? cause : new Error(String(cause)),
			};
			for (const handler of this.eventHandlers.error) handler(event);
		}
	};
}

export const createPreExpansionAutorouter = async (input: SimpleRouteJson) =>
	new PreExpansionAutorouter(input);
