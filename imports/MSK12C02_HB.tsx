import localC431541obj from "../assets/components/C431541.obj";
import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["ON"],
	pin2: ["COM"],
	pin3: ["OFF"],
	pin4: ["CASE"],
} as const;

export const MSK12C02_HB = (props: ChipProps<typeof pinLabels>) => {
	const { name = "SW1", ...restProps } = props;
	return (
		<chip
			name={name}
			pinLabels={pinLabels}
			displayName="SPDT power enable"
			supplierPartNumbers={{ jlcpcb: ["C431541"] }}
			manufacturerPartNumber="MSK12C02-HB"
			footprint="jlcpcb:C431541"
			// Preserve supplier numbering: common is 2; the four case feet share 4.
			cadModel={{
				objUrl: localC431541obj,
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0,
					y: 0.7529190500000822,
					z: -0.0000011000000000871424,
				},
			}}
			{...restProps}
		/>
	);
};
