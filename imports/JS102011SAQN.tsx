import localC221660obj from "../assets/components/C221660.obj";
import localC221660step from "../assets/components/C221660.step";
import type { SwitchProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["pin1"],
	pin2: ["pin2"],
	pin3: ["pin3"],
} as const;

export const JS102011SAQN = (props: SwitchProps) => {
	const { name = "SW1", ...restProps } = props;

	return (
		<switch
			name={name}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C221660"],
			}}
			manufacturerPartNumber="JS102011SAQN"
			footprint="jlcpcb:C221660"
			cadModel={{
				objUrl:
					localC221660obj,
				stepUrl:
					localC221660step,
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0,
					y: 1.7459756499999777,
					z: -0.8000016000000002,
				},
			}}
			{...restProps}
		/>
	);
};
