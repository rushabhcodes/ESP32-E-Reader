/**
 * ESP32 E-Reader Rev. B
 *
 * Board-level composition. Electrical data and exact PCB placements live in
 * design-data.ts; functional blocks live in circuit-sections.tsx.
 */

import { Fragment } from "react";
import { CircuitSections } from "./circuit-sections";
import { nets } from "./design-data";
import { manualRoutesByNet, planeConnectionsByNet } from "./routing-data";

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
			routingDisabled
			isViaInPadAllowed
		>
			<CircuitSections />

			{Object.keys(nets).map((name) => (
				<Fragment key={name}>
					<net
						name={name}
						isGroundNet={name === "GND"}
						isPowerNet={["GND", "V3V3", "USB_VBUS", "BATT_P"].includes(name)}
					/>
				</Fragment>
			))}

			{Object.entries(planeConnectionsByNet).flatMap(([name, connections]) =>
				connections.map((connection, index) => (
					<Fragment key={`${name}-plane-${index}`}>
						<trace
							from={connection.from}
							to={`net.${name}`}
							thickness={connection.thickness}
							pcbPath={connection.pcbPath}
						/>
					</Fragment>
				)),
			)}

			{Object.entries(manualRoutesByNet).flatMap(([name, routes]) => [
				<Fragment key={`${name}-net-root`}>
					<trace
						from={routes[0]?.to ?? nets[name][0]}
						to={`net.${name}`}
						pcbPath={[]}
					/>
				</Fragment>,
				...routes.map((route, index) => (
					<Fragment key={`${name}-route-${index}`}>
						<trace
							from={route.from}
							to={`net.${name}`}
							thickness={route.thickness}
							pcbPath={route.pcbPath}
						/>
					</Fragment>
				)),
			])}

			<cutout
				name="ENCLOSURE_SLOT"
				shape="rect"
				width="35mm"
				height="2mm"
				pcbX={5.75}
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
				text="POWER"
				pcbX={-28}
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
			<silkscreentext text="EPD FL" pcbX={20} pcbY={-23} fontSize="1mm" />
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
