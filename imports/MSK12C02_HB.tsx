import { createElement, Fragment } from "react";
import localC431541obj from "../assets/components/C431541.obj";
import type { SwitchProps } from "@tscircuit/props";

// The four case feet need separate pad aliases, sharing the electrical CASE alias.
// Supplier numbering: common is 2, throws are 1/3, and the case feet share 4.
export const MSK12C02_HB = (props: SwitchProps) =>
	createElement("switch", {
		type: "spdt",
		pinLabels: { pin1: "ON", pin2: "COM", pin3: "OFF", pin4: "CASE" },
		displayName: "SPDT power enable",
		symbol: (
			<symbol>
				<schematicrect width={1.2} height={0.6} isFilled={false} />
				<schematictext text="{REF}" schY={0.2} fontSize={0.2} />
				<port
					name="ON"
					aliases={["pin1"]}
					pinNumber={1}
					direction="left"
					schX={-1}
					schY={0.1}
				/>
				<port
					name="COM"
					aliases={["pin2"]}
					pinNumber={2}
					direction="left"
					schX={-1}
					schY={-0.1}
				/>
				<port
					name="OFF"
					aliases={["pin3"]}
					pinNumber={3}
					direction="right"
					schX={1}
					schY={-0.1}
				/>
				{["CASE_A", "CASE_B", "CASE_C", "CASE_D"].map((name, index) => (
					<Fragment key={name}>
						<port
							name={name}
							aliases={index === 0 ? ["pin4", "CASE"] : ["CASE"]}
							pinNumber={index === 0 ? 4 : undefined}
							direction="right"
							schX={1}
							schY={0.1}
						/>
					</Fragment>
				))}
			</symbol>
		),
		supplierPartNumbers: { jlcpcb: ["C431541"] },
		manufacturerPartNumber: "MSK12C02-HB",
		footprint: (
			<footprint>
				<hole pcbX="1.500124mm" pcbY="-0.75603735mm" diameter="0.9000236mm" />
				<hole pcbX="-1.49987mm" pcbY="-0.75603735mm" diameter="0.9000236mm" />
				<smtpad
					portHints={["pin1"]}
					pcbX="-2.249932mm"
					pcbY="1.49389465mm"
					width="0.5999988mm"
					height="1.524mm"
					shape="rect"
				/>
				<smtpad
					portHints={["pin2"]}
					pcbX="0.750062mm"
					pcbY="1.49389465mm"
					width="0.5999988mm"
					height="1.524mm"
					shape="rect"
				/>
				<smtpad
					portHints={["pin3"]}
					pcbX="2.250186mm"
					pcbY="1.49389465mm"
					width="0.5999988mm"
					height="1.524mm"
					shape="rect"
				/>
				<smtpad
					portHints={["CASE_A"]}
					pcbX="-3.599942mm"
					pcbY="0.39407465mm"
					width="1.1999976mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["CASE_B"]}
					pcbX="-3.599942mm"
					pcbY="-1.90589535mm"
					width="1.1999976mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["CASE_C"]}
					pcbX="3.599942mm"
					pcbY="-1.90589535mm"
					width="1.1999976mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<smtpad
					portHints={["CASE_D"]}
					pcbX="3.599942mm"
					pcbY="0.39407465mm"
					width="1.1999976mm"
					height="0.6999986mm"
					shape="rect"
				/>
				<silkscreenpath
					route={[
						{ x: 3.301060199999938, y: -0.20600035000006756 },
						{ x: 3.301060199999938, y: -1.3436663500001487 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -3.216300399999909, y: -1.3436663500001487 },
						{ x: -3.216300399999909, y: -0.20600035000006756 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 0.22324059999994006, y: -3.775182950000044 },
						{ x: 1.4983206000000564, y: -3.775182950000044 },
						{ x: 1.4983206000000564, y: -2.174982949999958 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: -2.7499564000000873, y: -2.1559329500000786 },
						{ x: 2.7500579999999673, y: -2.1559329500000786 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 0.2229866000000129, y: -2.1747797500000843 },
						{ x: 0.2229866000000129, y: -3.7748019499999828 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 2.768904799999973, y: 0.7439850499998784 },
						{ x: 2.7589226000000053, y: 0.7439850499998784 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 1.7189195999999356, y: 0.7439850499998784 },
						{ x: 1.2811760000000731, y: 0.7439850499998784 },
					]}
				/>
				<silkscreenpath
					route={[
						{ x: 0.21892259999992802, y: 0.7439850499998784 },
						{ x: -1.7188180000000557, y: 0.7439850499998784 },
					]}
				/>
				<silkscreentext
					text="{NAME}"
					pcbX="0.00508mm"
					pcbY="3.25360865mm"
					anchorAlignment="center"
					fontSize="1mm"
				/>
				<fabricationnotepath
					route={[
						{ x: 0.20005040000000918, y: -2.2059963500000777 },
						{ x: 1.5000477999999475, y: -2.2059963500000777 },
						{ x: 1.5000477999999475, y: -3.805993150000063 },
						{ x: 0.20005040000000918, y: -3.805993150000063 },
						{ x: 0.20005040000000918, y: -2.2059963500000777 },
					]}
					strokeWidth="0.254mm"
				/>
				<courtyardoutline
					outline={[
						{ x: -4.448620000000005, y: 2.503608649999933 },
						{ x: 4.458779999999933, y: 2.503608649999933 },
						{ x: 4.458779999999933, y: -4.06699135000008 },
						{ x: -4.448620000000005, y: -4.06699135000008 },
						{ x: -4.448620000000005, y: 2.503608649999933 },
					]}
				/>
			</footprint>
		),
		cadModel: {
			objUrl: localC431541obj,
			pcbRotationOffset: 0,
			modelOriginPosition: {
				x: 0,
				y: 0.7529190500000822,
				z: -0.0000011000000000871424,
			},
		},
		...props,
	});
