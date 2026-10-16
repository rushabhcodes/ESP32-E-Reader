import { Fragment } from "react";
import {
	controlButtonCaptions,
	schematicGroups,
	schematicLayout,
} from "./schematic-layout";
import { functionalSymbolFor } from "./functional-schematic-symbols";
import {
	aliasForPin,
	type ChipSpec,
	capacitors,
	chips,
	diodes,
	inductors,
	noConnectAliases,
	pinLabelsFor,
	polarizedPinLabels,
	resistors,
	schematicPlacementFor,
	supplierPartNumbersFor,
	testpoints,
} from "./design-data";
import { SMMS0420_100M } from "./imports/SMMS0420_100M";
import { BQ24073RGTR } from "./imports/BQ24073RGTR";
import { DM3AT_SF_PEJM5 } from "./imports/DM3AT_SF_PEJM5";
import { DW01A } from "./imports/DW01A";
import { ESP32_C3_WROOM_02U_N4 } from "./imports/ESP32_C3_WROOM_02U_N4";
import { EVQP7C01P } from "./imports/EVQP7C01P";
import { FH34SRJ_24S_0_5SH_50_ } from "./imports/FH34SRJ_24S_0_5SH_50_";
import { FS8205A } from "./imports/FS8205A";
import { MSK12C02_HB } from "./imports/MSK12C02_HB";
import { MBR0530T1G } from "./imports/MBR0530T1G";
import { SMMS0420_1R5M } from "./imports/SMMS0420_1R5M";
import { TPS63021DSJR } from "./imports/TPS63021DSJR";
import { S2B_PH_K_S_LF__SN_ } from "./imports/S2B_PH_K_S_LF__SN_";
import { SI1308EDL_T1_GE3 } from "./imports/SI1308EDL_T1_GE3";
import { SKRPACE010 } from "./imports/SKRPACE010";
import { TYPE_C_31_M_12 } from "./imports/TYPE_C_31_M_12";
import { USBLC6_2SC6 } from "./imports/USBLC6_2SC6";

const renderChip = (spec: ChipSpec) => {
	const half = Math.ceil(spec.pins.length / 2);
	const schematicPlacement = schematicPlacementFor(spec.name);
	const symbol = functionalSymbolFor(spec.name);
	const importedCommon = {
		name: spec.name,
		pcbX: spec.pcbX,
		pcbY: spec.pcbY,
		pcbRotation: spec.pcbRotation,
		layer: spec.layer,
		supplierPartNumbers: supplierPartNumbersFor(spec.name),
		...schematicPlacement,
		...(symbol ? { symbol } : {}),
	};

	if (spec.name === "J2")
		return (
			<FH34SRJ_24S_0_5SH_50_
				key={spec.name}
				{...importedCommon}
				pcbY={spec.pcbY}
				noConnect={["pin1", "pin4", "pin6", "pin7", "pin19", "pin25", "pin26"]}
			/>
		);
	if (spec.name === "J4")
		return (
			<DM3AT_SF_PEJM5
				key={spec.name}
				{...importedCommon}
				noConnect={["pin10", "pin11", "pin12", "pin13", "pin14"]}
			/>
		);
	// Turn BT1's keyed mating face toward the partition lead slot (-Y).
	// Its right-side position clears the Waveshare ribbon and battery pouch.
	if (spec.name === "BT1")
		return (
			<S2B_PH_K_S_LF__SN_
				key={spec.name}
				{...importedCommon}
				pcbX={spec.pcbX - 0.975}
				pcbY={spec.pcbY + 2}
				pcbRotation={180}
				schPinArrangement={{ topSide: ["pin1"], bottomSide: ["pin2"] }}
			/>
		);
	if (spec.name === "Q1")
		return <FS8205A key={spec.name} {...importedCommon} />;
	if (spec.name === "Q2")
		return <SI1308EDL_T1_GE3 key={spec.name} {...importedCommon} />;
	if (spec.name === "U1")
		return (
			<BQ24073RGTR
				key={spec.name}
				{...importedCommon}
				noConnect={["pin7", "pin14"]}
			/>
		);
	if (spec.name === "U2")
		return (
			<USBLC6_2SC6
				key={spec.name}
				{...importedCommon}
				noConnect={["pin1", "pin4"]}
			/>
		);
	if (spec.name === "U3")
		return <DW01A key={spec.name} {...importedCommon} noConnect={["pin4"]} />;
	if (spec.name === "U4")
		return (
			<ESP32_C3_WROOM_02U_N4
				key={spec.name}
				{...importedCommon}
				noConnect={["pin11"]}
			/>
		);
	if (spec.name === "U5")
		return (
			<TPS63021DSJR key={spec.name} {...importedCommon} noConnect={["pin14"]} />
		);
	if (spec.name === "S1" || spec.name === "S2")
		return <EVQP7C01P key={spec.name} {...importedCommon} />;
	if (["SW2", "SW3", "SW4", "SW6"].includes(spec.name))
		return (
			<SKRPACE010
				key={spec.name}
				{...importedCommon}
				noConnect={["pin2", "pin3"]}
			/>
		);
	if (spec.name === "SW7")
		return <MSK12C02_HB key={spec.name} {...importedCommon} />;

	const common = {
		name: spec.name,
		manufacturerPartNumber: spec.value,
		footprint: spec.footprint,
		pinLabels: pinLabelsFor(spec.pins),
		noConnect: noConnectAliases(spec),
		pcbX: spec.pcbX,
		pcbY: spec.pcbY,
		pcbRotation: spec.pcbRotation,
		layer: spec.layer,
		supplierPartNumbers: supplierPartNumbersFor(spec.name),
		doNotPlace: spec.name === "JP1",
		schPinArrangement: {
			leftSide: spec.pins.slice(0, half).map(aliasForPin),
			rightSide: spec.pins.slice(half).map(aliasForPin),
		},
		...schematicPlacement,
	};

	if (spec.name === "J1")
		return (
			<TYPE_C_31_M_12
				key={spec.name}
				{...importedCommon}
				noConnect={["SBU1", "SBU2"]}
				pcbX={spec.pcbX}
				pcbY={spec.pcbY}
				pcbRotation={spec.pcbRotation}
			/>
		);
	if (spec.kind === "connector")
		return <connector key={spec.name} {...common} />;
	if (spec.kind === "pushbutton")
		return <pushbutton key={spec.name} {...common} />;
	return <chip key={spec.name} {...common} />;
};

const SheetHeadings = ({ sheet }: { sheet: string }) => (
	<Fragment>
		{sheet === "controls" &&
			controlButtonCaptions.map(({ reference, text }) => (
				<Fragment key={reference}>
					<schematictext
						text={text}
						schX={schematicLayout[reference].schX + 0.65}
						schY={schematicLayout[reference].schY}
						anchor="left"
						fontSize={0.24}
					/>
				</Fragment>
			))}
		{schematicGroups
			.filter((group) => group.sheet === sheet)
			.map((group) => (
				<Fragment key={group.name}>
					<schematictext
						text={group.title}
						schX={group.x}
						schY={group.y}
						fontSize={0.38}
						anchor="center"
					/>
				</Fragment>
			))}
	</Fragment>
);

export const CircuitSections = () => (
	<Fragment>
		<schematicsheet
			name="battery_usb"
			displayName="Battery, Protection, USB & Charging"
			sheetIndex={0}
		>
			<SheetHeadings sheet="battery_usb" />
		</schematicsheet>
		<schematicsheet
			name="mcu_power"
			displayName="3.3 V Rail & ESP32-C3"
			sheetIndex={1}
		>
			<SheetHeadings sheet="mcu_power" />
		</schematicsheet>
		<schematicsheet
			name="display_power"
			displayName="E-Paper Interface & Bias Rails"
			sheetIndex={2}
		>
			<SheetHeadings sheet="display_power" />
		</schematicsheet>
		<schematicsheet
			name="storage"
			displayName="Micro SD Storage"
			sheetIndex={3}
		>
			<SheetHeadings sheet="storage" />
		</schematicsheet>
		<schematicsheet name="controls" displayName="User Controls" sheetIndex={4}>
			<SheetHeadings sheet="controls" />
		</schematicsheet>
		{schematicGroups.map((group) => (
			<Fragment key={group.name}>
				<schematicsection name={group.name} displayName={group.title} />
			</Fragment>
		))}

		{capacitors.map((spec) => (
			<capacitor
				key={spec.name}
				name={spec.name}
				capacitance={spec.value}
				footprint={spec.footprint}
				supplierPartNumbers={supplierPartNumbersFor(spec.name)}
				pcbX={spec.pcbX}
				pcbY={spec.pcbY}
				pcbRotation={spec.pcbRotation}
				layer={spec.layer}
				schRotation={-90}
				{...schematicPlacementFor(spec.name)}
			/>
		))}
		{resistors.map((spec) => (
			<resistor
				key={spec.name}
				name={spec.name}
				resistance={spec.value}
				footprint={spec.footprint}
				supplierPartNumbers={supplierPartNumbersFor(spec.name)}
				pcbX={spec.pcbX}
				pcbY={spec.pcbY}
				pcbRotation={spec.pcbRotation}
				layer={spec.layer}
				{...schematicPlacementFor(spec.name)}
			/>
		))}
		{inductors.map((spec) =>
			spec.name === "L1" ? (
				<SMMS0420_100M
					key={spec.name}
					name={spec.name}
					pcbX={spec.pcbX}
					pcbY={spec.pcbY}
					pcbRotation={spec.pcbRotation}
					layer={spec.layer}
					supplierPartNumbers={supplierPartNumbersFor(spec.name)}
					{...schematicPlacementFor(spec.name)}
				/>
			) : spec.name === "L2" ? (
				<SMMS0420_1R5M
					key={spec.name}
					name={spec.name}
					pcbX={spec.pcbX}
					pcbY={spec.pcbY}
					pcbRotation={spec.pcbRotation}
					layer={spec.layer}
					{...schematicPlacementFor(spec.name)}
				/>
			) : (
				<inductor
					key={spec.name}
					name={spec.name}
					inductance={spec.value}
					footprint={spec.footprint}
					supplierPartNumbers={supplierPartNumbersFor(spec.name)}
					pcbX={spec.pcbX}
					pcbY={spec.pcbY}
					pcbRotation={spec.pcbRotation}
					layer={spec.layer}
					{...schematicPlacementFor(spec.name)}
				/>
			),
		)}

		<led
			name="D1"
			supplierPartNumbers={supplierPartNumbersFor("D1")}
			color="red"
			pinLabels={polarizedPinLabels}
			footprint="0805"
			pcbX={-29.62440000000001}
			pcbY={34.475}
			pcbRotation={90}
			layer="top"
			{...schematicPlacementFor("D1")}
		/>

		{diodes.map((spec) => (
			<Fragment key={spec.name}>
				<MBR0530T1G
					name={spec.name}
					pcbX={spec.pcbX}
					pcbY={spec.pcbY}
					pcbRotation={spec.pcbRotation}
					layer={spec.layer}
					pcbSx={{ "& silkscreentext": { visibility: "hidden" } }}
					supplierPartNumbers={supplierPartNumbersFor(spec.name)}
					{...schematicPlacementFor(spec.name)}
				/>
				<silkscreentext
					text={spec.name}
					pcbX={spec.pcbX + 3.4}
					pcbY={spec.pcbY}
					fontSize="0.75mm"
					layer={spec.layer}
				/>
			</Fragment>
		))}

		{chips.map(renderChip)}

		{testpoints.map((testpoint) => (
			<testpoint
				key={testpoint.name}
				name={testpoint.name}
				footprintVariant="pad"
				padShape="circle"
				padDiameter="1.5mm"
				footprint={
					<footprint>
						<smtpad portHints={["pin1"]} shape="circle" radius="0.75mm" />
						<courtyardcircle radius="1mm" />
					</footprint>
				}
				doNotPlace
				pcbX={testpoint.pcbX}
				pcbY={testpoint.pcbY}
				{...schematicPlacementFor(testpoint.name)}
			/>
		))}
	</Fragment>
);
