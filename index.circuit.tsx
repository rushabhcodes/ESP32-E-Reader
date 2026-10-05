/**
 * ESP32 E-Reader Rev. B
 *
 * Board-level composition. Electrical data and exact PCB placements live in
 * design-data.ts; functional blocks live in circuit-sections.tsx.
 */

import { Fragment } from "react";
import { assembly } from "tscircuit";
import batteryEnvelopeUrl from "./assets/enclosure/battery-envelope-DO-NOT-PRINT.glb";
import antennaEnvelopeUrl from "./assets/enclosure/antenna-envelope-DO-NOT-PRINT.glb";
import partitionUrl from "./assets/enclosure/battery-partition.glb";
import button1Url from "./assets/enclosure/button-1.glb";
import button2Url from "./assets/enclosure/button-2.glb";
import button3Url from "./assets/enclosure/button-3.glb";
import button4Url from "./assets/enclosure/button-4.glb";
import displayPanelUrl from "./assets/enclosure/display-panel.glb";
import frontShellUrl from "./assets/enclosure/front-shell.glb";
import rearCoverUrl from "./assets/enclosure/rear-cover.glb";
import { CircuitSections } from "./circuit-sections";
import { nets, traceThicknessByNet } from "./design-data";
import { createPreExpansionAutorouter } from "./pre-expansion-autorouter";

const enclosureMountingHoles = [
	{ name: "MOUNT_TL", x: -27, y: 44.75 },
	{ name: "MOUNT_TR", x: 27, y: 44.75 },
] as const;

// The compact tactile switches fit inside the display-width lower section.
const boardOutline = [
	{ x: -26.25, y: 48.08 },
	{ x: 26.25, y: 48.08 },
	{ x: 29.79, y: 46.62 },
	{ x: 31.25, y: 43.08 },
	{ x: 31.25, y: -44 },
	{ x: 30.37, y: -46.12 },
	{ x: 28.25, y: -47 },
	{ x: -28.25, y: -47 },
	{ x: -30.37, y: -46.12 },
	{ x: -31.25, y: -44 },
	{ x: -31.25, y: 43.08 },
	{ x: -29.79, y: 46.62 },
];

// A 2 mm router creates rounded slot ends; avoid impossible square corners.
const displayFpcSlot = [-1, 1].flatMap((side) =>
	Array.from({ length: 17 }, (_, i) => {
		const angle = (side === 1 ? -Math.PI / 2 : Math.PI / 2) + i * Math.PI / 16;
		return { x: side * 12 + Math.cos(angle), y: Math.sin(angle) };
	}),
);

function EReaderBoard() {
	return (
		<board
			title="ESP32 E-Reader Rev. B"
			width="62.5mm"
			height="95.08mm"
			outline={boardOutline}
			doubleSidedAssembly
			layers={4}
			thickness="1.6mm"
			minViaHoleDiameter="0.3mm"
			minViaPadDiameter="0.6mm"
			minViaEdgeToPadEdgeClearance="0.25mm"
			// Standard-cost through vias, with a 0.15 mm radial annulus.
			minViaHoleEdgeToViaHoleEdgeClearance="0.2mm"
			minPlatedHoleDrillEdgeToDrillEdgeClearance="0.45mm"
			minTraceToHoleEdgeClearance="0.2mm"
			minBoardEdgeClearance="0.3mm"
			minTraceToPadEdgeClearance="0.1mm"
			autorouter={{
				algorithmFn: createPreExpansionAutorouter,
				allowViaInPad: false,
			}}
		>
			{/* Upper M2.5 mounting holes; the lower edge seats in case rails. */}
			{enclosureMountingHoles.map(({ name, x, y }) => (
				<Fragment key={name}>
					<hole diameter="2.7mm" pcbX={x} pcbY={y} />
					<keepout
						shape="circle"
						radius="3.2mm"
						pcbX={x}
						pcbY={y}
						layers={["top", "inner1", "inner2", "bottom"]}
					/>
				</Fragment>
			))}

			{/* Keep GND layer transitions clear of the nearby top-layer SPI clock. */}
			<keepout
				shape="circle"
				radius="0.25mm"
				pcbX={-0.35}
				pcbY={-8.34}
				layers={["inner2"]}
			/>
			{/* The RESE escape must not drill through J2's adjacent pin-3
			    contact. Keep its via clear of the connector pad on buried layers. */}
			<keepout
				shape="circle"
				radius="0.65mm"
				pcbX={4.72}
				pcbY={-28.19}
				layers={["inner1", "inner2", "bottom"]}
			/>

			{/* Fine-pitch contacts must stay free of through-drills, including
			    vias on their own net. Top copper remains available for escapes. */}
			<keepout
				shape="rect"
				width="13mm"
				height="1.8mm"
				pcbX={0}
				pcbY={-27.68723375}
				layers={["inner1", "inner2", "bottom"]}
			/>
			{/* Keep layer-transition pads clear of the C28 pin-2 edge. */}
			<keepout
				shape="rect"
				width="1.6mm"
				height="1.225mm"
				pcbX={-5.9}
				pcbY={-11.57}
				layers={["inner1", "inner2", "bottom"]}
			/>

			<CircuitSections />

			{/* Route the display D/C and reset signals as explicit point-to-point
			    connections. The net-level autorouter split these two paths into
			    disconnected copper segments beside J2's fine-pitch contacts. */}
			<trace from={nets.EPD_DC[0]} to={nets.EPD_DC[1]} thickness="0.2mm" />
			<trace from={nets.EPD_RST[0]} to={nets.EPD_RST[1]} thickness="0.2mm" />
			<trace from={nets.EPD_RST[1]} to={nets.EPD_RST[2]} thickness="0.2mm" />
			{Object.entries(nets).filter(([name]) => !["EPD_DC", "EPD_RST"].includes(name)).map(([name, connections]) => (
				<Fragment key={name}>
					<net
						name={name}
						isGroundNet={name === "GND"}
						isPowerNet={["GND", "V3V3", "USB_VBUS", "BATT_P"].includes(name)}
					/>
					{connections.map((connection, index) => (
						<Fragment key={`${name}-${index}`}>
							<trace
								from={connection}
								to={`net.${name}`}
								thickness={traceThicknessByNet[name] ?? "0.2mm"}
							/>
						</Fragment>
					))}
				</Fragment>
			))}

			{/* Four-layer fills provide short returns and a dedicated 3.3 V plane. */}
			<copperpour
				name="GND_FILL_TOP"
				connectsTo="net.GND"
				layer="top"
				clearance="0.2mm"
				boardEdgeMargin="0.3mm"
			/>
			<copperpour
				name="GND_FILL_BOTTOM"
				connectsTo="net.GND"
				layer="bottom"
				clearance="0.2mm"
				boardEdgeMargin="0.3mm"
			/>
			<copperpour
				name="GND_PLANE_INNER1"
				connectsTo="net.GND"
				layer="inner1"
				clearance="0.2mm"
				boardEdgeMargin="0.3mm"
			/>
			<copperpour
				name="V3V3_PLANE_INNER2"
				connectsTo="net.V3V3"
				layer="inner2"
				clearance="0.2mm"
				boardEdgeMargin="0.3mm"
			/>

			<cutout
				name="DISPLAY_FPC_SLOT"
				shape="polygon"
				points={displayFpcSlot}
				pcbX={0}
				pcbY={-36.2}
			/>

			<silkscreentext text="BATT" pcbX={25} pcbY={-25} fontSize="1mm" />
			<silkscreentext
				text="USB"
				pcbX={27}
				pcbY={31}
				pcbRotation={90}
				fontSize="1mm"
			/>
			<silkscreentext
				text="WAKE"
				pcbX={-28}
				pcbY={20}
				pcbRotation={90}
				fontSize="1mm"
			/>
			<silkscreentext
				text="MAIN PWR"
				pcbX={25}
				pcbY={20}
				pcbRotation={90}
				fontSize="1mm"
			/>
			<silkscreentext
				text="EN"
				pcbX={-28}
				pcbY={-31}
				pcbRotation={90}
				fontSize="1mm"
			/>
			<silkscreentext text="EPD" pcbX={1} pcbY={-23} fontSize="1mm" />
			<silkscreentext text="MICRO SD" pcbX={-22} pcbY={-28} fontSize="1mm" />
			<silkscreentext
				text="ESP32 E-Reader  Rev. B"
				pcbX={13}
				pcbY={-23}
				fontSize="1mm"
			/>
		</board>
	);
}

export default function ESP32EReader() {
	return (
		<assembly.device name="ESP32_E_READER">
			<EReaderBoard />
			<assembly.screen
				name="EPD1"
				connectsTo=".J2"
				width="56.24mm"
				height="96.62mm"
				modelUrl={displayPanelUrl}
			/>
			<assembly.cadassembly
				name="battery_envelope"
				cadModel={{ glbUrl: batteryEnvelopeUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="wifi_antenna_envelope"
				cadModel={{ glbUrl: antennaEnvelopeUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="front_shell"
				cadModel={{ glbUrl: frontShellUrl, modelUnitToMmScale: 1 }}
			/>
			{[button1Url, button2Url, button3Url, button4Url].map((url, i) => (
				<assembly.cadassembly
					key={i}
					name={`button_${i + 1}`}
					cadModel={{ glbUrl: url, modelUnitToMmScale: 1 }}
				/>
			))}
			<assembly.cadassembly
				name="battery_partition"
				cadModel={{ glbUrl: partitionUrl, modelUnitToMmScale: 1 }}
			/>
			<assembly.cadassembly
				name="rear_cover"
				cadModel={{ glbUrl: rearCoverUrl, modelUnitToMmScale: 1 }}
			/>
		</assembly.device>
	);
}
