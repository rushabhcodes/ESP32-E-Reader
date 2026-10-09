import localC202112obj from "../assets/components/C202112.obj";
import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: "NC1",
	pin2: "GDR",
	pin3: "RESE",
	pin4: "NC4",
	pin5: "VSH2",
	pin6: "TSCL",
	pin7: "TSDA",
	pin8: "GND8",
	pin9: "BUSY",
	pin10: "RST",
	pin11: "DC",
	pin12: "CS",
	pin13: "SCLK",
	pin14: "MOSI",
	pin15: "VDDIO",
	pin16: "VDD",
	pin17: "GND17",
	pin18: "VDD1",
	pin19: "NC19",
	pin20: "VSH1",
	pin21: "PREVGH",
	pin22: "VSL",
	pin23: "PREVGL",
	pin24: "VCOM",
	pin25: "SHIELD1",
	pin26: "SHIELD2",
} as const;

export const FH12_24S_0_5SH_55_ = (props: ChipProps<typeof pinLabels>) => {
	return (
		<chip
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C202112"],
			}}
			manufacturerPartNumber="FH12-24S-0.5SH(55)"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin12"]}
						pcbX="0.249936mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin13"]}
						pcbX="-0.249936mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin14"]}
						pcbX="-0.750062mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin15"]}
						pcbX="-1.249934mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin16"]}
						pcbX="-1.75006mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin17"]}
						pcbX="-2.249932mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin18"]}
						pcbX="-2.750058mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin19"]}
						pcbX="-3.24993mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin20"]}
						pcbX="-3.750056mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin21"]}
						pcbX="-4.249928mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin22"]}
						pcbX="-4.750054mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin23"]}
						pcbX="-5.249926mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin24"]}
						pcbX="-5.750052mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin25"]}
						pcbX="7.795514mm"
						pcbY="-1.36276715mm"
						width="1.5999968mm"
						height="2.2999954mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin26"]}
						pcbX="-7.795514mm"
						pcbY="-1.36276715mm"
						width="1.5999968mm"
						height="2.2999954mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin11"]}
						pcbX="0.750316mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin10"]}
						pcbX="1.250442mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin9"]}
						pcbX="1.750568mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin8"]}
						pcbX="2.25044mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin7"]}
						pcbX="2.750312mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin6"]}
						pcbX="3.250184mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin5"]}
						pcbX="3.750564mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="4.250182mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin3"]}
						pcbX="4.750308mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="5.250434mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin1"]}
						pcbX="5.75056mm"
						pcbY="1.81276625mm"
						width="0.2800096mm"
						height="1.3999972mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -7.550073800000007, y: -2.762764350000012 },
							{ x: -7.550073800000007, y: -4.362761149999997 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -7.550073800000007, y: -4.412773750000014 },
							{ x: 7.549921400000002, y: -4.412773750000014 },
							{ x: 7.549921400000002, y: -2.762764350000012 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 7.549921400000002, y: 0.03723004999999091 },
							{ x: 7.549921400000002, y: 1.2372276499999941 },
							{ x: 6.121704799999989, y: 1.2372276499999941 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: -6.121196800000007, y: 1.2372276499999941 },
							{ x: -7.550073800000007, y: 1.2372276499999941 },
							{ x: -7.550073800000007, y: 0.03723004999999091 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 5.8501026, y: 0.31414085000000114 },
							{ x: 5.450052599999992, y: -0.0859091500000062 },
							{ x: 6.2498985999999945, y: -0.0859091500000062 },
							{ x: 5.8501026, y: 0.31414085000000114 },
						]}
					/>
					<silkscreenpath
						route={[
							{ x: 6.499072600000005, y: 1.6882808499999982 },
							{ x: 6.375884219950663, y: 1.563192321495336 },
							{ x: 6.500342599999996, y: 1.4393673297605005 },
							{ x: 6.624800980049315, y: 1.563192321495336 },
							{ x: 6.501612599999987, y: 1.6882808499999982 },
						]}
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="0.009906mm"
						pcbY="-5.41734575mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -8.837994000000009, y: -4.6673457499999955 },
							{ x: 8.857805999999997, y: -4.6673457499999955 },
							{ x: 8.857805999999997, y: 2.7668542499999944 },
							{ x: -8.837994000000009, y: 2.7668542499999944 },
							{ x: -8.837994000000009, y: -4.6673457499999955 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					localC202112obj,
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: -0.000012699999984988608,
					y: 1.3889803499999942,
					z: -0.05,
				},
			}}
			{...props}
		/>
	);
};
