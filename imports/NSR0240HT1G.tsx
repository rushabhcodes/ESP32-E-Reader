import type { DiodeProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["cathode", "neg"],
	pin2: ["anode", "pos"],
} as const;

export const NSR0240HT1G = (props: DiodeProps) => {
	const { name = "D1", ...restProps } = props;

	return (
		<diode
			name={name}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C152519"],
			}}
			manufacturerPartNumber="NSR0240HT1G"
			footprint="smdpads2_p2.3449mm_pw1mm_ph0.7mm_cyw3.8528mm_cyh2.1002mm"
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C152519.obj?uuid=7459fe65e23146c0a8d836e46a0add72",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C152519.step?uuid=7459fe65e23146c0a8d836e46a0add72",
				pcbRotationOffset: 0,
				modelOriginPosition: { x: 0, y: 0.00011430000006384944, z: 0 },
			}}
			{...restProps}
		/>
	);
};
