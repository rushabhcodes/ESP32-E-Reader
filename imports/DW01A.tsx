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
			footprint="dfn6_p0.95mm_w3.3702mm_pw0.532mm_pl1.072mm_pin1location(leftside,bottom)"
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2927799.obj?uuid=229b69761e2c45dba6a83d8866dec72d",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2927799.step?uuid=229b69761e2c45dba6a83d8866dec72d",
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
