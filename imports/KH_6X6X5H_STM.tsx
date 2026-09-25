import type { PushButtonProps } from "@tscircuit/props";

const pinLabels = {
	pin1: ["pin1"],
	pin2: ["pin2"],
	pin3: ["pin3"],
	pin4: ["pin4"],
} as const;

export const KH_6X6X5H_STM = (props: PushButtonProps<typeof pinLabels>) => {
	const { name = "SW1", ...restProps } = props;

	return (
		<pushbutton
			name={name}
			pinLabels={pinLabels}
			supplierPartNumbers={{
				jlcpcb: ["C2837531"],
			}}
			manufacturerPartNumber="KH-6X6X5H-STM"
			footprint={
				<footprint>
					<smtpad
						portHints={["pin1"]}
						pcbX="-4.549902mm"
						pcbY="2.250059mm"
						width="2.2999954mm"
						height="1.499997mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin2"]}
						pcbX="4.549902mm"
						pcbY="2.249805mm"
						width="2.2999954mm"
						height="1.499997mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin3"]}
						pcbX="-4.549902mm"
						pcbY="-2.250059mm"
						width="2.2999954mm"
						height="1.499997mm"
						shape="rect"
					/>
					<smtpad
						portHints={["pin4"]}
						pcbX="4.549902mm"
						pcbY="-2.250059mm"
						width="2.2999954mm"
						height="1.499997mm"
						shape="rect"
					/>
					<silkscreenpath
						route={[
							{ x: -2.999994000000129, y: 2.9998669999999947 },
							{ x: 2.999994000000015, y: 2.9998669999999947 },
							{ x: 2.999994000000015, y: -3.0001210000000356 },
							{ x: -2.999994000000129, y: -3.0001210000000356 },
							{ x: -2.999994000000129, y: 2.9998669999999947 },
						]}
					/>
					<silkscreencircle pcbX="0mm" pcbY="-0.000127mm" radius="1.529334mm" />
					<silkscreencircle
						pcbX="2.032mm"
						pcbY="-2.032127mm"
						radius="0.508mm"
					/>
					<silkscreencircle
						pcbX="-2.032mm"
						pcbY="-2.032127mm"
						radius="0.508mm"
					/>
					<silkscreencircle pcbX="2.032mm" pcbY="2.031873mm" radius="0.508mm" />
					<silkscreencircle
						pcbX="-2.029968mm"
						pcbY="2.030349mm"
						radius="0.508mm"
					/>
					<silkscreentext
						text="{NAME}"
						pcbX="0.0127mm"
						pcbY="4.022473mm"
						anchorAlignment="center"
						fontSize="1mm"
					/>
					<courtyardoutline
						outline={[
							{ x: -5.939600000000155, y: 3.272472999999991 },
							{ x: 5.964999999999918, y: 3.272472999999991 },
							{ x: 5.964999999999918, y: -3.247327000000041 },
							{ x: -5.939600000000155, y: -3.247327000000041 },
							{ x: -5.939600000000155, y: 3.272472999999991 },
						]}
					/>
				</footprint>
			}
			cadModel={{
				objUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2837531.obj?uuid=0a2a6eed7e284a95867695201df5c190",
				stepUrl:
					"https://modelcdn.tscircuit.com/easyeda_models/assets/C2837531.step?uuid=0a2a6eed7e284a95867695201df5c190",
				pcbRotationOffset: 0,
				modelOriginPosition: { x: 0, y: 0.0004999999999999449, z: -0.5 },
			}}
			{...restProps}
		/>
	);
};
