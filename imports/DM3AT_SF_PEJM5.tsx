import type { ChipProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["DAT2"],
	pin2: ["pin2"],
	pin3: ["CMD"],
	pin4: ["VDD"],
	pin5: ["CLK"],
	pin6: ["VSS"],
	pin7: ["DAT0"],
	pin8: ["DAT1"],
	pin9: ["SW_B"],
	pin10: ["pin10"],
	pin11: ["SW_A"],
	pin12: ["pin12"],
	pin13: ["pin13"],
	pin14: ["pin14"],
} as const;

const pinAttributes = {
	pin4: { requiresPower: true },
	pin6: { requiresGround: true },
} as const;

export const DM3AT_SF_PEJM5 = (props: ChipProps<typeof pinLabels>) => {
	return (
		<chip
			pinLabels={pinLabels}
			pinAttributes={pinAttributes}
			supplierPartNumbers={{
				jlcpcb: ["C114218"],
			}}
			manufacturerPartNumber="DM3AT-SF-PEJM5"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin14"]}
						pcbX="4.32491515mm"
						pcbY="7.72502265mm"
						width="0.999998mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin13"]}
						pcbX="6.67492315mm"
						pcbY="-7.37502335mm"
						width="1.2999974mm"
						height="1.8999962mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin12"]}
						pcbX="-6.82492285mm"
						pcbY="-6.92493535mm"
						width="0.999998mm"
						height="2.7999944mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin11"]}
						pcbX="-6.82492285mm"
						pcbY="-2.77508335mm"
						width="0.999998mm"
						height="0.7999984mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin10"]}
						pcbX="-6.82492285mm"
						pcbY="3.42505665mm"
						width="0.999998mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin9"]}
						pcbX="-5.87496285mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin8"]}
						pcbX="-4.92500285mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin7"]}
						pcbX="-3.82492885mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin6"]}
						pcbX="-2.72510885mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin5"]}
						pcbX="-1.62503485mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="-0.52496085mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin3"]}
						pcbX="0.57511315mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="1.67493315mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin1"]}
						pcbX="2.77500715mm"
						pcbY="7.72502265mm"
						width="0.6999986mm"
						height="1.1999976mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -6.368992849999927, y: 7.725022650000028 },
							{ x: -7.511992849999842, y: 7.725022650000028 },
							{ x: -7.511992849999842, y: -8.530977349999944 },
							{ x: -7.38499284999989, y: -8.530977349999944 },
							{ x: 7.601007149999987, y: -8.530977349999944 },
							{ x: 7.601007149999987, y: 7.725022650000028 },
							{ x: 5.061007150000137, y: 7.725022650000028 },
						]}
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="0.04450715mm"
						pcbY="9.33411465mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<fabricationnotepath
						route={[
							{ x: -6.1749876499999345, y: -8.124983749999956 },
							{ x: -6.1749876499999345, y: 0.17499965000013162 },
							{ x: 5.0249899500000765, y: 0.17499965000013162 },
							{ x: 5.124989750000054, y: -8.124983749999956 },
							{ x: 4.724990550000143, y: -8.124983749999956 },
							{ x: 4.724990550000143, y: -0.12499974999991537 },
							{ x: -5.874988249999888, y: -0.12499974999991537 },
							{ x: -5.874988249999888, y: -8.124983749999956 },
							{ x: -6.1749876499999345, y: -8.124983749999956 },
						]}
						strokeWidth="0.254mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -7.761992849999842, y: 8.58411465000006 },
							{ x: 7.851007149999987, y: 8.58411465000006 },
							{ x: 7.851007149999987, y: -8.781485349999912 },
							{ x: -7.761992849999842, y: -8.781485349999912 },
							{ x: -7.761992849999842, y: 8.58411465000006 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C114218.obj?uuid=969c0967dc6241d2ada5963291ad54a4",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C114218.step?uuid=969c0967dc6241d2ada5963291ad54a4",
				pcbRotationOffset: 0,
				modelOriginPosition: {
					x: 0.004997449999905257,
					y: 0.16199104999998815,
					z: -1.89,
				},
			}}
			{...props}
		/>
	);
};
