import localC139797obj from "../assets/components/C139797.obj";
import type { ChipProps } from "@tscircuit/props";
import type { AnyCircuitElement } from "circuit-json";
import buttonSymbol from "./SKRPACE010.symbol.json";

const pinLabels = {
	pin1: ["pin1"],
	pin2: ["pin2"],
	pin3: ["pin3"],
	pin4: ["pin4"],
} as const;

// The built-in pushbutton assigns schematic terminals to pins 1 and 2.
// This four-pad part uses pins 1 and 4. Keep ports on the component so the
// supplier pads and schematic wires share their original physical identities.
export const SKRPACE010 = (props: ChipProps<typeof pinLabels>) => {
	const { name = "SW1", ...restProps } = props;

	return (
		<chip
			name={name}
			pinLabels={pinLabels}
			schPinArrangement={{
				topSide: ["pin4"],
				bottomSide: ["pin1"],
				leftSide: ["pin3", "pin2"],
			}}
			// The standard 0.4 mm pin stems put the active terminals at y = ±0.55.
			schWidth={1}
			schHeight={0.3}
			symbol={buttonSymbol as AnyCircuitElement[]}
			supplierPartNumbers={{
				jlcpcb: ["C139797"],
			}}
			manufacturerPartNumber="SKRPACE010"
			footprint="jlcpcb:C139797"
			cadModel={{
				objUrl:
					localC139797obj,
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0.000012700000070253736,
					y: 0.00012700000002041634,
					z: -0.01,
				},
			}}
			{...restProps}
		/>
	);
};
