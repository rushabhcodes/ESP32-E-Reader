import { Fragment } from "react";
import localC2830320obj from "../assets/components/C2830320.obj";
import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["S1"],
	pin2: ["D1_D2_A"],
	pin3: ["S2"],
	pin4: ["G2"],
	pin5: ["D1_D2_B"],
	pin6: ["G1"],
} as const;

export const FS8205A = (props: ChipProps<typeof pinLabels>) => {
	return (
		<mosfet
			channelType="n"
			mosfetMode="enhancement"
			// One physical package containing two common-drain N-channel MOSFETs.
			// Explicit ports avoid assigning a single-FET symbol's pin roles.
			symbol={
				<symbol>
					<schematicrect width={1.6} height={0.8} isFilled={false} />
					<schematictext text="{REF}" schY={0.3} fontSize={0.2} />
					{Object.entries(pinLabels).map(([pin, labels], index) => (
						<Fragment key={pin}>
							<port
								name={labels[0]}
								aliases={[pin]}
								pinNumber={index + 1}
								direction={index < 3 ? "left" : "right"}
								schX={index < 3 ? -1.2 : 1.2}
								schY={index < 3 ? 0.2 - index * 0.2 : -0.2 + (index - 3) * 0.2}
								schStemLength={0.4}
							/>
							<schematictext
								text={labels[0]}
								schX={index < 3 ? -0.7 : 0.7}
								schY={index < 3 ? 0.2 - index * 0.2 : -0.2 + (index - 3) * 0.2}
								anchor={index < 3 ? "left" : "right"}
								fontSize={0.1}
							/>
						</Fragment>
					))}
				</symbol>
			}
			supplierPartNumbers={{
				jlcpcb: ["C2830320"],
			}}
			manufacturerPartNumber="FS8205A"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin3"]}
						pcbX="1.35001mm"
						pcbY="0.94996mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="1.35001mm"
						pcbY="-0mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin1"]}
						pcbX="1.35001mm"
						pcbY="-0.94996mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin6"]}
						pcbX="-1.35001mm"
						pcbY="-0.94996mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin5"]}
						pcbX="-1.35001mm"
						pcbY="-0mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="-1.35001mm"
						pcbY="0.94996mm"
						width="1.0999978mm"
						height="0.5999988mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -0.899998200000141, y: 1.5499080000000731 },
							{ x: 0.9000236000000541, y: 1.5499080000000731 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -0.899998200000141, y: -1.5501111999999466 },
							{ x: 0.9000236000000541, y: -1.5501111999999466 },
						]}
					/>
					<silkscreencircle pcbX="1.397mm" pcbY="-1.651mm" radius="0.127mm" />
					<silkscreentext
						text="{NAME}"
						pcbX="0.012446mm"
						pcbY="2.562354mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -2.1425540000000183, y: 1.8123540000000276 },
							{ x: 2.167445999999927, y: 1.8123540000000276 },
							{ x: 2.167445999999927, y: -2.015045999999984 },
							{ x: -2.1425540000000183, y: -2.015045999999984 },
							{ x: -2.1425540000000183, y: 1.8123540000000276 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl: localC2830320obj,
				pcbRotationOffset: 180,
				modelOriginPosition: {
					x: 0.000025399999913133797,
					y: -0.0000889000000370288,
					z: -0.048939,
				},
			}}
			{...props}
		/>
	);
};
