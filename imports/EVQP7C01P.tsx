import type { PushButtonProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["pin1"],
	pin2: ["pin2"],
	pin3: ["1"],
	pin4: ["2"],
} as const;

export const EVQP7C01P = (props: PushButtonProps<typeof pinLabels>) => {
	const { name = "SW1", ...restProps } = props;

	return (
		<pushbutton
			name={name}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C388883"],
			}}
			manufacturerPartNumber="EVQP7C01P"
			footprint={
				<footprint>
					<hole pcbX="0mm" pcbY="0.899922mm" diameter="0.7999984mm" />
					<hole pcbX="0mm" pcbY="-0.899922mm" diameter="0.7999984mm" />
					<smtpad
						portHints={["pin1"]}
						pcbX="-1.800098mm"
						pcbY="0.750062mm"
						width="1.3999972mm"
						height="1.0999978mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="-1.800098mm"
						pcbY="-0.750062mm"
						width="1.3999972mm"
						height="1.0999978mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin3"]}
						pcbX="1.800098mm"
						pcbY="0.750062mm"
						width="1.3999972mm"
						height="1.0999978mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="1.800098mm"
						pcbY="-0.750062mm"
						width="1.3999972mm"
						height="1.0999978mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -0.8499856000000818, y: -1.4500097999999753 },
							{ x: -0.850010999999995, y: -2.1500083999999333 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -0.8499856000000818, y: -2.1500083999999333 },
							{ x: 0.8499855999999681, y: -2.1500083999999333 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 0.8499855999999681, y: -2.1500083999999333 },
							{ x: 0.8499855999999681, y: -1.4500097999999753 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -0.3406393999999864, y: -2.1500083999999333 },
							{ x: -0.3406393999999864, y: -1.4500097999999753 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 0.32778700000005756, y: -2.1500083999999333 },
							{ x: 0.32778700000005756, y: -1.4500097999999753 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -0.9249409999999898, y: 1.450009800000089 },
							{ x: -0.21722080000006372, y: 1.450009800000089 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 0.21722079999995003, y: 1.450009800000089 },
							{ x: 0.9249409999999898, y: 1.450009800000089 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -0.9249409999999898, y: -1.4500097999999753 },
							{ x: -0.21722080000006372, y: -1.4500097999999753 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 0.21722079999995003, y: -1.4500097999999753 },
							{ x: 0.9249409999999898, y: -1.4500097999999753 },
						]}
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="0.0127mm"
						pcbY="2.4986mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<fabricationnotepath
						route={[
							{ x: -0.8400034000000005, y: -1.4400021999999808 },
							{ x: -0.8400034000000005, y: -2.080005999999912 },
							{ x: 0.8599931999999626, y: -2.080005999999912 },
							{ x: 0.8599931999999626, y: -1.4400021999999808 },
							{ x: -0.8400034000000005, y: -1.4400021999999808 },
						]}
						strokeWidth="0.254mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -2.7391999999999825, y: 1.7486000000000104 },
							{ x: 2.7645999999998594, y: 1.7486000000000104 },
							{ x: 2.7645999999998594, y: -2.408999999999878 },
							{ x: -2.7391999999999825, y: -2.408999999999878 },
							{ x: -2.7391999999999825, y: 1.7486000000000104 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C388883.obj?uuid=47afa358d3094fbf913052f46a4feca9",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C388883.step?uuid=47afa358d3094fbf913052f46a4feca9",
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: -0.006997699999942597,
					y: -0.014002400000163173,
					z: -0.0000010000000000287557,
				},
			}}
			{...restProps}
		/>
	);
};
