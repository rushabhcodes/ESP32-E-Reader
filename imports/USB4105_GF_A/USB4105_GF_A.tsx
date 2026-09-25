import objPath from "./USB4105_GF_A.obj";
import stepPath from "./USB4105_GF_A.step";
import type { ConnectorProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["EH1"],
	pin2: ["EH2"],
	pin3: ["EH3"],
	pin4: ["EH4"],
	pin5: ["A12", "GND1"],
	pin6: ["B1", "GND2"],
	pin7: ["A9", "VBUS1"],
	pin8: ["B4", "VBUS2"],
	pin9: ["B5", "CC2"],
	pin10: ["A8", "SBU1"],
	pin11: ["B6", "DP2"],
	pin12: ["A7", "DN1"],
	pin13: ["A6", "DP1"],
	pin14: ["B7", "DN2"],
	pin15: ["A5", "CC1"],
	pin16: ["B8", "SBU2"],
	pin17: ["B9", "VBUS3"],
	pin18: ["A4", "VBUS4"],
	pin19: ["B12", "GND3"],
	pin20: ["A1", "GND4"],
} as const;

export const USB4105_GF_A = (props: ConnectorProps) => {
	return (
		<connector
			standard="usb_c"
			pinCount={20}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C3020560"],
			}}
			manufacturerPartNumber="USB4105-GF-A"
			footprint={
				<footprint>
					<hole pcbX="2.890012mm" pcbY="1.0646474mm" diameter="0.649986mm" />
					<hole pcbX="-2.890012mm" pcbY="1.0646474mm" diameter="0.649986mm" />
					<platedhole
						portHints={["pin1"]}
						pcbX="-4.320032mm"
						pcbY="1.5444534mm"
						holeWidth="0.700024mm"
						holeHeight="1.700022mm"
						outerWidth="1.0999978mm"
						outerHeight="2.0999958mm"
						shape="pill"
					/>
					<platedhole
						portHints={["pin2"]}
						pcbX="4.320032mm"
						pcbY="1.5444534mm"
						holeWidth="0.700024mm"
						holeHeight="1.700022mm"
						outerWidth="1.0999978mm"
						outerHeight="2.0999958mm"
						shape="pill"
					/>
					<platedhole
						portHints={["pin3"]}
						pcbX="4.320032mm"
						pcbY="-2.6356246mm"
						holeWidth="0.700024mm"
						holeHeight="1.4000226mm"
						outerWidth="1.0999978mm"
						outerHeight="1.7999964mm"
						shape="pill"
					/>
					<platedhole
						portHints={["pin4"]}
						pcbX="-4.320032mm"
						pcbY="-2.6356246mm"
						holeWidth="0.700024mm"
						holeHeight="1.4000226mm"
						outerWidth="1.0999978mm"
						outerHeight="1.7999964mm"
						shape="pill"
					/>
					<smtpad
						portHints={["pin5"]}
						pcbX="3.350006mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin6"]}
						pcbX="3.050032mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin7"]}
						pcbX="2.549906mm"
						pcbY="2.1098574mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin8"]}
						pcbX="2.249932mm"
						pcbY="2.1098574mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin9"]}
						pcbX="1.75006mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin10"]}
						pcbX="1.24968mm"
						pcbY="2.1106194mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin11"]}
						pcbX="0.750062mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin12"]}
						pcbX="0.249936mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin13"]}
						pcbX="-0.249936mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin14"]}
						pcbX="-0.750062mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin15"]}
						pcbX="-1.249934mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin16"]}
						pcbX="-1.75006mm"
						pcbY="2.1106194mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin17"]}
						pcbX="-2.249932mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin18"]}
						pcbX="-2.549906mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin19"]}
						pcbX="-3.050032mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin20"]}
						pcbX="-3.350006mm"
						pcbY="2.1096034mm"
						width="0.2999994mm"
						height="1.1500104mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: 4.4699935999999525, y: -1.5190659999998388 },
							{ x: 4.4699935999999525, y: 0.2778824000001805 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -4.469993600000066, y: -3.7522085999999035 },
							{ x: -4.469993600000066, y: -5.254948799999966 },
							{ x: 4.4699935999999525, y: -5.254948799999966 },
							{ x: 4.4699935999999525, y: -3.7522085999999035 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -4.469993600000066, y: 0.2778824000001805 },
							{ x: -4.469993600000066, y: -1.5190659999998388 },
						]}
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="-0.018288mm"
						pcbY="3.6902474mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -5.132387999999992, y: 2.9402474000000893 },
							{ x: 5.0958120000000235, y: 2.9402474000000893 },
							{ x: 5.0958120000000235, y: -5.509952599999906 },
							{ x: -5.132387999999992, y: -5.509952599999906 },
							{ x: -5.132387999999992, y: 2.9402474000000893 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl: objPath,
				stepUrl: stepPath,
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0,
					y: 1.5075092000000494,
					z: -0.0000020000000000575113,
				},
			}}
			{...props}
		/>
	);
};
