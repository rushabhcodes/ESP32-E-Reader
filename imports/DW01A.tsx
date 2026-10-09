import localC2927799obj from "../assets/components/C2927799.obj";
import localC2927799step from "../assets/components/C2927799.step";
import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["OD"],
	pin2: ["CSI"],
	pin3: ["OC"],
	pin4: ["NC"],
	pin5: ["VDD"],
	pin6: ["VSS"],
} as const;

const pinAttributes = {
	pin4: { doNotConnect: true },
	pin5: { requiresPower: true },
	pin6: { requiresGround: true },
} as const;

export const DW01A = (props: ChipProps<typeof pinLabels>) => {
	return (
		<chip
			pinLabels={pinLabels}
			pinAttributes={pinAttributes}
			supplierPartNumbers={{
				jlcpcb: ["C2927799"],
			}}
			manufacturerPartNumber="DW01A"
			footprint="jlcpcb:C2927799"
			cadModel={{
				objUrl:
					localC2927799obj,
				stepUrl:
					localC2927799step,
				pcbRotationOffset: 90,
				modelOriginPosition: {
					x: -0.000012700000070253736,
					y: 0.000012700000070253736,
					z: -0.048939,
				},
			}}
			{...props}
		/>
	);
};
