import { Fragment } from "react";
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
	schematicHeights,
	schematicPlacementFor,
	supplierPartNumbersFor,
	testpoints,
} from "./design-data";
import { CR5040_470M } from "./imports/CR5040_470M";
import { BQ24074RGTR } from "./imports/BQ24074RGTR";
import { DM3AT_SF_PEJM5 } from "./imports/DM3AT_SF_PEJM5";
import { DW01A } from "./imports/DW01A";
import { ESP32_C3_WROOM_02U_N4 } from "./imports/ESP32_C3_WROOM_02U_N4";
import { EVQP7C01P } from "./imports/EVQP7C01P";
import { FH12_24S_0_5SH_55_ } from "./imports/FH12_24S_0_5SH_55_";
import { FS8205A } from "./imports/FS8205A";
import { JS102011SAQN } from "./imports/JS102011SAQN";
import { MBR0530T1G } from "./imports/MBR0530T1G";
import { SMMS0420_1R5M } from "./imports/SMMS0420_1R5M";
import { TPS63021DSJR } from "./imports/TPS63021DSJR";
import { S2B_PH_K_S_LF__SN_ } from "./imports/S2B_PH_K_S_LF__SN_";
import { SI1308EDL_T1_GE3 } from "./imports/SI1308EDL_T1_GE3";
import { SKRPACE010 } from "./imports/SKRPACE010";
import { USB4105_GF_A } from "./imports/USB4105_GF_A/USB4105_GF_A";
import { USBLC6_2SC6 } from "./imports/USBLC6_2SC6";

const renderChip = (spec: ChipSpec) => {
	const half = Math.ceil(spec.pins.length / 2);
	const schematicPlacement = schematicPlacementFor(spec.name);
	const importedCommon = {
		name: spec.name,
		pcbX: spec.pcbX,
		pcbY: spec.pcbY,
		pcbRotation: spec.pcbRotation,
		layer: spec.layer,
		supplierPartNumbers: supplierPartNumbersFor(spec.name),
		schHeight: schematicHeights[spec.name],
		...schematicPlacement,
	};

	if (spec.name === "J2")
		return (
			<FH12_24S_0_5SH_55_
				key={spec.name}
				{...importedCommon}
				pcbY={spec.pcbY + 0.03723375}
				noConnect={["pin1", "pin4", "pin19", "pin25", "pin26"]}
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
	// Move it 2 mm inward for plug insertion room at the PCB's lower edge.
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
		return (
			<FS8205A
				key={spec.name}
				{...importedCommon}
			/>
		);
	if (spec.name === "Q2")
		return <SI1308EDL_T1_GE3 key={spec.name} {...importedCommon} />;
	if (spec.name === "U1")
		return <BQ24074RGTR key={spec.name} {...importedCommon} noConnect={["pin7", "pin14", "pin15"]} />;
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
			<TPS63021DSJR
				key={spec.name}
				{...importedCommon}
				noConnect={["pin14"]}
			/>
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
		return (
			<JS102011SAQN
				key={spec.name}
				{...importedCommon}
				pcbX={spec.pcbX - 1.75}
			/>
		);

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
		schHeight: schematicHeights[spec.name],
		...schematicPlacement,
	};

	if (spec.name === "J1")
		return (
			<USB4105_GF_A
				key={spec.name}
				{...importedCommon}
				noConnect={["SBU1", "SBU2"]}
				pcbX={spec.pcbX - 1.57}
				pcbY={spec.pcbY}
				pcbRotation={spec.pcbRotation}
				schWidth={1.385}
			/>
		);
	if (spec.kind === "connector")
		return <connector key={spec.name} {...common} />;
	if (spec.kind === "pushbutton")
		return <pushbutton key={spec.name} {...common} />;
	return <chip key={spec.name} {...common} />;
};

export const BatteryUsbSection = () => (
	<schematicsection
		name="battery_usb_section"
		displayName="Battery, Protection, USB & Charging"
	/>
);

export const McuPowerSection = () => (
	<schematicsection
		name="mcu_power_section"
		displayName="3.3 V Rail & ESP32-C3"
	/>
);

export const DisplayPowerSection = () => (
	<schematicsection
		name="display_power_section"
		displayName="E-Paper Interface & Bias Rails"
	/>
);

export const StorageSection = () => (
	<schematicsection name="storage_section" displayName="Micro SD Storage" />
);

export const ControlsSection = () => (
	<schematicsection name="controls_section" displayName="User Controls" />
);

export const CircuitSections = () => (
	<Fragment>
		<schematicsheet
			name="battery_usb"
			displayName="Battery, Protection, USB & Charging"
			sheetIndex={0}
		/>
		<schematicsheet
			name="mcu_power"
			displayName="3.3 V Rail & ESP32-C3"
			sheetIndex={1}
			sheetSize="ANSI_B"
		/>
		<schematicsheet
			name="display_power"
			displayName="E-Paper Interface & Bias Rails"
			sheetIndex={2}
			sheetSize="ANSI_B"
		/>
		<schematicsheet
			name="storage"
			displayName="Micro SD Storage"
			sheetIndex={3}
		/>
		<schematicsheet
			name="controls"
			displayName="User Controls"
			sheetIndex={4}
		/>
		<BatteryUsbSection />
		<McuPowerSection />
		<DisplayPowerSection />
		<StorageSection />
		<ControlsSection />

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
				schOrientation="vertical"
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
				<CR5040_470M
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
			<MBR0530T1G
				key={spec.name}
				name={spec.name}
				pcbX={spec.pcbX}
				pcbY={spec.pcbY}
				pcbRotation={spec.pcbRotation}
				layer={spec.layer}
				supplierPartNumbers={supplierPartNumbersFor(spec.name)}
				{...schematicPlacementFor(spec.name)}
			/>
		))}

		{chips.map(renderChip)}

		{testpoints.map((testpoint) => (
			<testpoint
				key={testpoint.name}
				name={testpoint.name}
				footprintVariant="pad"
				padShape="circle"
				padDiameter="1.5mm"
				doNotPlace
				pcbX={testpoint.pcbX}
				pcbY={testpoint.pcbY}
				{...schematicPlacementFor(testpoint.name)}
			/>
		))}
	</Fragment>
);
