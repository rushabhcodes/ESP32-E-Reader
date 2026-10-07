import { Fragment } from "react";
import { schematicLayout } from "./schematic-layout";
import { pinLabels as chargerPins } from "./imports/BQ24074RGTR";
import { pinLabels as mcuPins } from "./imports/ESP32_C3_WROOM_02U_N4";
import { pinLabels as regulatorPins } from "./imports/TPS63021DSJR";
import { pinLabels as sdPins } from "./imports/DM3AT_SF_PEJM5";
const physicalPinLabels: Record<string, Record<string, readonly string[]>> = {
	U1: chargerPins,
	U4: mcuPins,
	U5: regulatorPins,
	J4: sdPins,
};

const functionalSymbols: Record<string, string> = {
	U1: "BQ24074RGTR",
	U4: "ESP32-C3-WROOM-02U-N4",
	U5: "TPS63021DSJR",
	J4: "DM3AT-SF-PEJM5",
	J2: "FH12-24S-0.5SH",
};

// Explicit symbols reserve space at the corners for supply and ground labels.
// Every port retains its physical pin number; only the schematic changes.
export function functionalSymbolFor(reference: string) {
	const arrangement = schematicLayout[reference]?.schPinArrangement;
	if (!functionalSymbols[reference] || !arrangement) return undefined;
	const sides = Object.entries(arrangement).map(([side, pins]) => ({
		side,
		pins: Array.isArray(pins) ? pins : [],
	}));
	const sideCount = Math.max(
		...sides
			.filter(({ side }) => side === "leftSide" || side === "rightSide")
			.map(({ pins }) => pins.length),
	);
	const endCount = Math.max(
		1,
		...sides
			.filter(({ side }) => side === "topSide" || side === "bottomSide")
			.map(({ pins }) => pins.length),
	);
	const width = Math.max(2.8, (endCount - 1) * 0.3 + 1.2);
	const height = Math.max(3.2, (sideCount - 1) * 0.5 + 2.2);
	const pinsWithPlacement = sides.flatMap(({ side, pins }) =>
		pins.map((pin, index) => ({ side, pin, index, count: pins.length })),
	);
	// Schematic placement must not reorder physical ports: their stable IDs also
	// feed the PCB router. J2 retains the imported connector's original order.
	const importedJ2Order = [
		2,
		3,
		4,
		5,
		6,
		7,
		8,
		1,
		...Array.from({ length: 18 }, (_, i) => i + 9),
	];
	const numberOf = (pin: string | number) =>
		Number(String(pin).replace("pin", ""));
	pinsWithPlacement.sort((a, b) =>
		reference === "J2"
			? importedJ2Order.indexOf(numberOf(a.pin)) -
				importedJ2Order.indexOf(numberOf(b.pin))
			: numberOf(a.pin) - numberOf(b.pin),
	);
	return (
		<symbol>
			<schematicrect
				schX={0}
				schY={0}
				width={width}
				height={height}
				isFilled={false}
				strokeWidth={0.04}
			/>
			<schematictext
				text="{REF}"
				schX={width / 2 - 0.15}
				schY={height / 2 - 0.15}
				anchor="top_right"
				fontSize={0.22}
			/>
			<schematictext
				text={functionalSymbols[reference]}
				schX={width / 2 + 0.2}
				schY={height / 2 + 0.1}
				anchor="left"
				fontSize={0.16}
			/>
			{pinsWithPlacement.map(({ side, pin, index, count }) => {
				const number = Number(String(pin).replace("pin", ""));
				const horizontal = side === "leftSide" || side === "rightSide";
				const x = horizontal
					? side === "leftSide"
						? -width / 2
						: width / 2
					: (index - (count - 1) / 2) * 0.3;
				const y = horizontal
					? ((count - 1) / 2 - index) * 0.5
					: side === "topSide"
						? height / 2
						: -height / 2;
				const direction =
					side === "leftSide"
						? "left"
						: side === "rightSide"
							? "right"
							: side === "topSide"
								? "up"
								: "down";
				const dx = direction === "left" ? -1 : direction === "right" ? 1 : 0;
				const dy = direction === "up" ? 1 : direction === "down" ? -1 : 0;
				return (
					<Fragment key={pin}>
						<port
							name={
								physicalPinLabels[reference]?.[`pin${number}`]?.[0] ??
								`pin${number}`
							}
							aliases={[`pin${number}`]}
							pinNumber={number}
							direction={direction}
							schX={x + dx * 0.35}
							schY={y + dy * 0.35}
							schStemLength={0.35}
						/>
						<schematictext
							text={String(number)}
							schX={x + dx * 0.18 + (horizontal ? 0 : 0.08)}
							schY={y + dy * 0.18 + (horizontal ? 0.12 : 0)}
							fontSize={0.12}
						/>
					</Fragment>
				);
			})}
		</symbol>
	);
}
