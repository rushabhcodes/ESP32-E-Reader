/**
 * ESP32 E-Reader Rev. B
 *
 * Board-level composition. Electrical data and exact PCB placements live in
 * design-data.ts; functional blocks live in circuit-sections.tsx.
 */

import { Fragment } from "react";
import { CircuitSections } from "./circuit-sections";
import { nets, traceThicknessByNet } from "./design-data";
import { createPreExpansionAutorouter } from "./pre-expansion-autorouter";

const enclosureMountingHoles = [
	{ name: "MOUNT_TL", x: -27, y: 44.75 },
	{ name: "MOUNT_TR", x: 27, y: 44.75 },
	{ name: "MOUNT_BL", x: -27.5, y: -44 },
	{ name: "MOUNT_BR", x: 27.5, y: -44 },
] as const;

export default function ESP32EReader() {
	return (
		<board
			title="ESP32 E-Reader Rev. B"
			width="62.5mm"
			height="96.16mm"
			borderRadius="5mm"
			layers={4}
			thickness="1.6mm"
			doubleSidedAssembly
			minViaHoleDiameter="0.2mm"
			minViaPadDiameter="0.42mm"
			// 0.1 mm copper clearance + 0.11 mm annulus gives 0.21 mm
			// drill-to-trace clearance, above JLCPCB's 0.2 mm minimum.
			minTraceToPadEdgeClearance="0.1mm"
			autorouter={{
				algorithmFn: createPreExpansionAutorouter,
				allowViaInPad: false,
			}}
		>
			{/* M2.5 enclosure screws with clearance for printed standoffs/screw heads. */}
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

			{/* ESP32-C3-WROOM-02 antenna zone: no copper or routing on either side. */}
			<keepout
				shape="rect"
				width="18.2mm"
				height="6.65mm"
				pcbX={0.25}
				pcbY={44.755}
				layers={["top", "inner1", "inner2", "bottom"]}
			/>

			{/* Keep GND layer transitions clear of the nearby top-layer SPI clock. */}
			<keepout
				shape="circle"
				radius="0.25mm"
				pcbX={-0.35}
				pcbY={-8.34}
				layers={["inner2"]}
			/>

			<CircuitSections />

			{Object.entries(nets).map(([name, connections]) => (
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
				shape="rect"
				width="35mm"
				height="2mm"
				pcbX={0}
				pcbY={-39.92}
			/>

			<silkscreentext text="BATT" pcbX={-22} pcbY={43} fontSize="1mm" />
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
				pcbY={-16}
				pcbRotation={90}
				fontSize="1mm"
			/>
			<silkscreentext text="EPD" pcbX={1} pcbY={-23} fontSize="1mm" />
			<silkscreentext text="MICRO SD" pcbX={-22} pcbY={-38} fontSize="1mm" />
			<silkscreentext
				text="ESP32 E-Reader  Rev. B"
				pcbX={13}
				pcbY={-37}
				fontSize="1mm"
			/>
		</board>
	);
}
