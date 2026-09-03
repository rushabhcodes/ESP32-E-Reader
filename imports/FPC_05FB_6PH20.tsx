import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["pin1"],
	pin2: ["pin2"],
	pin3: ["pin3"],
	pin4: ["pin4"],
	pin5: ["pin5"],
	pin6: ["pin6"],
	pin7: ["pin7"],
	pin8: ["pin8"],
} as const;

export const FPC_05FB_6PH20 = (props: ChipProps<typeof pinLabels>) => {
	return (
		<chip
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C2856827"],
			}}
			manufacturerPartNumber="FPC-05FB-6PH20"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin8"]}
						pcbX="2.799969mm"
						pcbY="-1.4749653mm"
						width="1.999996mm"
						height="1.7999964mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin7"]}
						pcbX="-2.799969mm"
						pcbY="-1.4749653mm"
						width="1.999996mm"
						height="1.7999964mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin1"]}
						pcbX="1.250061mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="0.749935mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin3"]}
						pcbX="0.250063mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="-0.250063mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin5"]}
						pcbX="-0.749935mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin6"]}
						pcbX="-1.250061mm"
						pcbY="1.7749647mm"
						width="0.2999994mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -3.250031599999943, y: -0.3439032999998517 },
							{ x: -3.250031599999943, y: 1.6739489000001413 },
							{ x: -1.6510253999999804, y: 1.6739489000001413 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -3.250031599999943, y: -3.725024299999859 },
							{ x: -3.250031599999943, y: -2.6061796999999842 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 3.2499808000001167, y: -3.725024299999859 },
							{ x: -3.250031599999943, y: -3.725024299999859 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 3.2499808000001167, y: -0.3439032999998517 },
							{ x: 3.2499808000001167, y: 1.649945900000148 },
							{ x: 1.6311117999999851, y: 1.649945900000148 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 3.2499808000001167, y: -3.725024299999859 },
							{ x: 3.2499808000001167, y: -2.6061796999999842 },
						]}
					/>
					<silkscreencircle
						pcbX="1.999869mm"
						pcbY="2.1498687mm"
						radius="0.133096mm"
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="-0.001143mm"
						pcbY="3.6639647mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<fabricationnotepath
						route={[
							{ x: -1.5999967999999853, y: -3.249993499999846 },
							{ x: -1.5999967999999853, y: -0.3499992999999222 },
							{ x: 1.6999966000000768, y: -0.3499992999999222 },
							{ x: 1.6999966000000768, y: -3.249993499999846 },
							{ x: 1.499997000000235, y: -3.249993499999846 },
							{ x: 1.499997000000235, y: -0.5499988999998777 },
							{ x: -1.3999971999999161, y: -0.5499988999998777 },
							{ x: -1.3999971999999161, y: -3.249993499999846 },
							{ x: -1.5999967999999853, y: -3.249993499999846 },
						]}
						strokeWidth="0.254mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -4.0484429999999065, y: 2.913964700000065 },
							{ x: 4.0461570000001075, y: 2.913964700000065 },
							{ x: 4.0461570000001075, y: -3.986835299999939 },
							{ x: -4.0484429999999065, y: -3.986835299999939 },
							{ x: -4.0484429999999065, y: 2.913964700000065 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2856827.obj?uuid=3b8a25b70b4242b9af209a241c828aaf",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2856827.step?uuid=3b8a25b70b4242b9af209a241c828aaf",
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0.000012699999842880061,
					y: -1.7749569000000749,
					z: 0,
				},
			}}
			{...props}
		/>
	);
};
