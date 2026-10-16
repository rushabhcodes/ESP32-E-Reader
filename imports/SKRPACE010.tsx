import { createElement } from "react";
import localC139797obj from "../assets/components/C139797.obj";
import type { SwitchProps } from "@tscircuit/props";

// A normally-open momentary switch; the active physical terminals are 1 and 4.
export const SKRPACE010 = (props: SwitchProps) =>
	createElement("switch", {
		type: "spst",
		pinLabels: { pin1: "pin1", pin2: "pin2", pin3: "pin3", pin4: "pin4" },
		symbol: (
			<symbol>
				<schematictext
					text="{REF}"
					schX={-0.1}
					schY={0.35}
					anchor="bottom_right"
					fontSize={0.22}
				/>
				<schematicline x1={0} y1={-0.55} x2={0} y2={-0.15} />
				<schematicline x1={0} y1={0.15} x2={0} y2={0.55} />
				<schematicline x1={-0.25} y1={-0.15} x2={-0.25} y2={0.15} />
				<schematicline x1={-0.25} y1={0} x2={-0.45} y2={0} />
				<port
					name="pin1"
					pinNumber={1}
					direction="down"
					schX={0}
					schY={-0.55}
					schStemLength={0.4}
				/>
				<port
					name="pin2"
					pinNumber={2}
					direction="left"
					schX={-0.9}
					schY={-0.1}
				/>
				<port
					name="pin3"
					pinNumber={3}
					direction="left"
					schX={-0.9}
					schY={0.1}
				/>
				<port
					name="pin4"
					pinNumber={4}
					direction="up"
					schX={0}
					schY={0.55}
					schStemLength={0.4}
				/>
			</symbol>
		),
		supplierPartNumbers: { jlcpcb: ["C139797"] },
		manufacturerPartNumber: "SKRPACE010",
		footprint: (
			<footprint>
				<smtpad
					portHints={["pin1"]}
					pcbX="-2.100072mm"
					pcbY="1.074928mm"
					width="1.0500106mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["pin2"]}
					pcbX="2.100072mm"
					pcbY="1.074928mm"
					width="1.0500106mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["pin3"]}
					pcbX="-2.100072mm"
					pcbY="-1.074928mm"
					width="1.0500106mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["pin4"]}
					pcbX="2.100072mm"
					pcbY="-1.074928mm"
					width="1.0500106mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<silkscreenpath
					route={[
						{ x: -0.5080000000000382, y: 1.0160000000000764 },
						{ x: 0.5079999999999245, y: 1.0160000000000764 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -0.5080000000000382, y: -1.0159999999999627 },
						{ x: 0.5079999999999245, y: -1.0159999999999627 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 2.199893999999972, y: 0.5438140000001113 },
						{ x: 2.199893999999972, y: -0.5438139999999976 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 1.3664184000000432, y: 1.5238729999999805 },
						{ x: -1.366418400000157, y: 1.5238729999999805 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -2.1998940000000857, y: 0.5438140000001113 },
						{ x: -2.1998940000000857, y: -0.5438139999999976 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -1.3810995999999705, y: -1.5499079999999594 },
						{ x: 1.3810995999998568, y: -1.5499079999999594 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 0.5079999999999245, y: 1.0160000000000764 },
						{ x: 0.7511447149161086, y: 0.9864768865048745 },
						{ x: 0.9801587427964478, y: 0.8996233220636896 },
						{ x: 1.18173262077255, y: 0.7604869201419433 },
						{ x: 1.3441516077479037, y: 0.5771537826788062 },
						{ x: 1.4579765025682718, y: 0.36027856523526225 },
						{ x: 1.516592216083609, y: 0.1224652671394324 },
						{ x: 1.516592216083609, y: -0.1224652671394324 },
						{ x: 1.4579765025682718, y: -0.36027856523514856 },
						{ x: 1.3441516077479037, y: -0.5771537826788062 },
						{ x: 1.18173262077255, y: -0.7604869201418296 },
						{ x: 0.9801587427964478, y: -0.8996233220635759 },
						{ x: 0.7511447149161086, y: -0.9864768865047608 },
						{ x: 0.5079999999999245, y: -1.0159999999999627 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -0.5080000000000382, y: -1.0159999999999627 },
						{ x: -0.7511447149162223, y: -0.9864768865047608 },
						{ x: -0.9801587427965615, y: -0.8996233220635759 },
						{ x: -1.1817326207726637, y: -0.7604869201418296 },
						{ x: -1.3441516077480173, y: -0.5771537826788062 },
						{ x: -1.4579765025684992, y: -0.36027856523514856 },
						{ x: -1.5165922160837226, y: -0.1224652671394324 },
						{ x: -1.5165922160837226, y: 0.1224652671394324 },
						{ x: -1.4579765025684992, y: 0.36027856523526225 },
						{ x: -1.3441516077480173, y: 0.5771537826788062 },
						{ x: -1.1817326207726637, y: 0.7604869201419433 },
						{ x: -0.9801587427965615, y: 0.8996233220636896 },
						{ x: -0.7511447149162223, y: 0.9864768865048745 },
						{ x: -0.5080000000000382, y: 1.0160000000000764 },
					]}
				/>
				<silkscreentext
					text="{NAME}"
					pcbX="0.0127mm"
					pcbY="2.6256mm"
					anchorAlignment="center"
					fontSize="1mm"
				/>
				<courtyardoutline
					outline={[
						{ x: -2.8662000000001626, y: 1.8756000000000768 },
						{ x: 2.891599999999812, y: 1.8756000000000768 },
						{ x: 2.891599999999812, y: -1.8501999999998588 },
						{ x: -2.8662000000001626, y: -1.8501999999998588 },
						{ x: -2.8662000000001626, y: 1.8756000000000768 },
					]}
				/>
			</footprint>
		),
		cadModel: {
			objUrl: localC139797obj,
			pcbRotationOffset: 0,
			modelOriginPosition: {
				x: 0.000012700000070253736,
				y: 0.00012700000002041634,
				z: -0.01,
			},
		},
		...props,
	});
