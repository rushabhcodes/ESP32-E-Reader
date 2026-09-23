import { Fragment } from "react";
import { CR5040_470M } from "./imports/CR5040_470M";
import { DM3AT_SF_PEJM5 } from "./imports/DM3AT_SF_PEJM5";
import { ESP32_C3_WROOM_02_N4 } from "./imports/ESP32_C3_WROOM_02_N4";
import { EVQP7C01P } from "./imports/EVQP7C01P";
import { FH12_24S_0_5SH_55_ } from "./imports/FH12_24S_0_5SH_55_";
import { JS102011SAQN } from "./imports/JS102011SAQN";
import { ME6211C33M5G_N } from "./imports/ME6211C33M5G_N";
import { MBR0530T1G } from "./imports/MBR0530T1G";
import { S2B_PH_K_S_LF__SN_ } from "./imports/S2B_PH_K_S_LF__SN_";
import { SI1308EDL_T1_GE3 } from "./imports/SI1308EDL_T1_GE3";
import { SKRPACE010 } from "./imports/SKRPACE010";
import {
	type ChipSpec,
	aliasForPin,
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
	if (spec.name === "BT1")
		return (
			<S2B_PH_K_S_LF__SN_
				key={spec.name}
				{...importedCommon}
				pcbX={spec.pcbX - 0.975}
				pcbRotation={0}
			/>
		);
	if (spec.name === "Q2")
		return <SI1308EDL_T1_GE3 key={spec.name} {...importedCommon} />;
	if (spec.name === "U4")
		return (
			<ESP32_C3_WROOM_02_N4
				key={spec.name}
				{...importedCommon}
				noConnect={["pin11"]}
			/>
		);
	if (spec.name === "U5")
		return (
			<ME6211C33M5G_N
				key={spec.name}
				{...importedCommon}
				pcbRotation={(spec.pcbRotation ?? 0) - 90}
				noConnect={["pin4"]}
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
			<connector
				key={spec.name}
				name="J1"
				manufacturerPartNumber="USB4105-GF-A"
				supplierPartNumbers={supplierPartNumbersFor(spec.name)}
				standard="usb_c"
				pinCount={16}
				pinLabels={pinLabelsFor(spec.pins)}
				noConnect={noConnectAliases(spec)}
				pcbX={spec.pcbX}
				pcbY={spec.pcbY}
				pcbRotation={-90}
				schPinArrangement={{
					leftSide: ["P_1", "P_2", "P_3", "P_4", "P_5", "P_6", "P_7", "P_8"],
					rightSide: [
						"P_16",
						"P_15",
						"P_14",
						"P_13",
						"P_12",
						"P_11",
						"P_10",
						"P_9",
					],
				}}
				schHeight={1.4}
				{...schematicPlacement}
				footprint={
					<footprint insertionDirection="from_top">
						<smtpad
							shape="rect"
							width="0.6mm"
							height="1.15mm"
							pcbX={-3.2}
							pcbY={-3.68}
							portHints={["pin1"]}
						/>
						<smtpad
							shape="rect"
							width="0.6mm"
							height="1.15mm"
							pcbX={-2.4}
							pcbY={-3.68}
							portHints={["pin2"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={-1.25}
							pcbY={-3.68}
							portHints={["pin6"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={-0.25}
							pcbY={-3.68}
							portHints={["pin5"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={0.25}
							pcbY={-3.68}
							portHints={["pin4"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={1.25}
							pcbY={-3.68}
							portHints={["pin3"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={-1.75}
							pcbY={-3.68}
							portHints={["pin10"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={-0.75}
							pcbY={-3.68}
							portHints={["pin9"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={0.75}
							pcbY={-3.68}
							portHints={["pin8"]}
						/>
						<smtpad
							shape="rect"
							width="0.3mm"
							height="1.15mm"
							pcbX={1.75}
							pcbY={-3.68}
							portHints={["pin7"]}
						/>
						<smtpad
							shape="rect"
							width="0.6mm"
							height="1.15mm"
							pcbX={2.4}
							pcbY={-3.68}
							portHints={["pin11"]}
						/>
						<smtpad
							shape="rect"
							width="0.6mm"
							height="1.15mm"
							pcbX={3.2}
							pcbY={-3.68}
							portHints={["pin12"]}
						/>
						<platedhole
							shape="pill"
							outerWidth="1mm"
							outerHeight="2.1mm"
							holeWidth="0.6mm"
							holeHeight="1.7mm"
							pcbX={-4.32}
							pcbY={-3.105}
							portHints={["pin13"]}
						/>
						<platedhole
							shape="pill"
							outerWidth="1mm"
							outerHeight="1.8mm"
							holeWidth="0.6mm"
							holeHeight="1.4mm"
							pcbX={-4.32}
							pcbY={1.075}
							portHints={["pin14"]}
						/>
						<platedhole
							shape="pill"
							outerWidth="1mm"
							outerHeight="2.1mm"
							holeWidth="0.6mm"
							holeHeight="1.7mm"
							pcbX={4.32}
							pcbY={-3.105}
							portHints={["pin15"]}
						/>
						<platedhole
							shape="pill"
							outerWidth="1mm"
							outerHeight="1.8mm"
							holeWidth="0.6mm"
							holeHeight="1.4mm"
							pcbX={4.32}
							pcbY={1.075}
							portHints={["pin16"]}
						/>
						<hole diameter="0.65mm" pcbX={-2.89} pcbY={-2.605} />
						<hole diameter="0.65mm" pcbX={2.89} pcbY={-2.605} />
						<silkscreenrect width="9.4mm" height="7.2mm" pcbY="-0.25mm" />
						<courtyardrect width="10.64mm" height="8.94mm" pcbY="-0.29mm" />
					</footprint>
				}
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
		name="battery_usb"
		displayName="Battery, Protection, USB & Charging"
	/>
);

export const McuPowerSection = () => (
	<schematicsection name="mcu_power" displayName="3.3 V Rail & ESP32-C3" />
);

export const DisplayPowerSection = () => (
	<schematicsection
		name="display_power"
		displayName="E-Paper Interface & Bias Rails"
	/>
);

export const StorageSection = () => (
	<schematicsection name="storage" displayName="Micro SD Storage" />
);

export const ControlsSection = () => (
	<schematicsection name="controls" displayName="User Controls" />
);

export const CircuitSections = () => (
	<Fragment>
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
