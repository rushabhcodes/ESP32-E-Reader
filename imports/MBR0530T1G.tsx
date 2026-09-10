import type { DiodeProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["cathode", "neg"],
	pin2: ["anode", "pos"],
} as const;

export const MBR0530T1G = (props: DiodeProps) => {
	const { name = "D1", ...restProps } = props;

	return (
		<diode
			name={name}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C82046"],
			}}
			manufacturerPartNumber="MBR0530T1G"
			footprint="smdpads2_p3.4mm_pw1.2mm_ph0.95mm"
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C82046.obj?uuid=e9d505c99b6c436aaf827a29c5ba4f84",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C82046.step?uuid=e9d505c99b6c436aaf827a29c5ba4f84",
				pcbRotationOffset: 0,
				modelOriginPosition: { x: 0, y: 0.000012699999999199463, z: -0.6 },
			}}
			{...restProps}
		/>
	);
};
