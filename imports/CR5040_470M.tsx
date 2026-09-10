import type { InductorProps } from "@tscircuit/props";

export const CR5040_470M = (props: Omit<InductorProps, "inductance">) => {
	return (
		<inductor
			inductance="47uH"
			supplierPartNumbers={{
				jlcpcb: ["C520357"],
			}}
			manufacturerPartNumber="CR5040-470M"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin1"]}
						pcbX="1.999996mm"
						pcbY="0mm"
						width="2.1239988mm"
						height="4.2200068mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="-1.999996mm"
						pcbY="0mm"
						width="2.1239988mm"
						height="4.2200068mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -2.5262078000000656, y: 2.2624034000000393 },
							{ x: -2.5262078000000656, y: 2.5262078000000656 },
							{ x: 2.526207799999952, y: 2.5262078000000656 },
							{ x: 2.526207799999952, y: 2.2624034000000393 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -2.5262078000000656, y: -2.2624033999999256 },
							{ x: -2.5262078000000656, y: -2.5262078000000656 },
							{ x: 2.526207799999952, y: -2.5262078000000656 },
							{ x: 2.526207799999952, y: -2.2624033999999256 },
						]}
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="-0.0127mm"
						pcbY="3.54mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -3.3233999999999924, y: 2.7899999999999636 },
							{ x: 3.298000000000002, y: 2.7899999999999636 },
							{ x: 3.298000000000002, y: -2.764599999999973 },
							{ x: -3.3233999999999924, y: -2.764599999999973 },
							{ x: -3.3233999999999924, y: 2.7899999999999636 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C520357.obj?uuid=0acce46b82494539a4589a0e8b12d880",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C520357.step?uuid=0acce46b82494539a4589a0e8b12d880",
				pcbRotationOffset: 90,
				modelOriginPosition: { x: 0, y: 0, z: -0.01 },
			}}
			{...props}
		/>
	);
};
