import type { ChipProps } from "@tscircuit/props"

export const pinLabels = {
  pin1: ["VINA"],
  pin2: ["GND"],
  pin3: ["FB"],
  pin4: ["VOUT1"],
  pin5: ["VOUT2"],
  pin6: ["L22"],
  pin7: ["L21"],
  pin8: ["L11"],
  pin9: ["L12"],
  pin10: ["VIN1"],
  pin11: ["VIN2"],
  pin12: ["EN"],
  pin13: ["PS_SYNC"],
  pin14: ["PG"],
  pin15: ["PGND"]
} as const

const pinAttributes = {
  pin1: {requiresPower: true},
  pin2: {requiresGround: true},
  pin10: {requiresPower: true},
  pin11: {requiresPower: true},
  pin15: {requiresGround: true}
} as const

export const TPS63021DSJR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C202140"
  ]
}}
      manufacturerPartNumber="TPS63021DSJR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-1.5000986mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.9999726mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.4998466mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="0.0000254mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.5001514mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="0.5001514mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="0.0000254mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="-0.4998466mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="-0.9999726mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="-1.5000986mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="1.5001494mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="1.0000234mm" pcbY="-1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="1.5001494mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="1.0000234mm" pcbY="1.450086mm" width="0.2500122mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin15"]} points={[{x: "-2.1999956mm", y: "0.7900162mm"}, {x: "-2.1999956mm", y: "0.5900166mm"}, {x: "-1.4299946mm", y: "0.5900166mm"}, {x: "-1.4299946mm", y: "0.3300222mm"}, {x: "-2.1999956mm", y: "0.3300222mm"}, {x: "-2.1999956mm", y: "0.1300226mm"}, {x: "-1.4299946mm", y: "0.1300226mm"}, {x: "-1.4299946mm", y: "-0.1299718mm"}, {x: "-2.1999956mm", y: "-0.1299718mm"}, {x: "-2.1999956mm", y: "-0.3299714mm"}, {x: "-1.4299946mm", y: "-0.3299714mm"}, {x: "-1.4299946mm", y: "-0.5899658mm"}, {x: "-2.1999956mm", y: "-0.5899658mm"}, {x: "-2.1999956mm", y: "-0.7899654mm"}, {x: "2.1999956mm", y: "-0.7899654mm"}, {x: "2.1999956mm", y: "-0.5899658mm"}, {x: "1.4299946mm", y: "-0.5899658mm"}, {x: "1.4299946mm", y: "-0.3299714mm"}, {x: "2.1999956mm", y: "-0.3299714mm"}, {x: "2.1999956mm", y: "-0.1299718mm"}, {x: "1.4299946mm", y: "-0.1299718mm"}, {x: "1.4299946mm", y: "0.1300226mm"}, {x: "2.1999956mm", y: "0.1300226mm"}, {x: "2.1999956mm", y: "0.3300222mm"}, {x: "1.4299946mm", y: "0.3300222mm"}, {x: "1.4299946mm", y: "0.5900166mm"}, {x: "2.1999956mm", y: "0.5900166mm"}, {x: "2.1999956mm", y: "0.7900162mm"}, {x: "-2.1999956mm", y: "0.7900162mm"}]} shape="polygon" />
<silkscreenpath route={[{"x":2.099995799999874,"y":1.100023199999896},{"x":2.099995799999874,"y":1.6000222000000122},{"x":1.9299935999998752,"y":1.6000222000000122}]} />
<silkscreenpath route={[{"x":2.099995799999874,"y":-1.0999724000000697},{"x":2.099995799999874,"y":-1.5999713999999585},{"x":1.9299935999998752,"y":-1.5999713999999585}]} />
<silkscreenpath route={[{"x":-2.099995799999988,"y":1.100023199999896},{"x":-2.099995799999988,"y":1.6000222000000122},{"x":-1.9299935999999889,"y":1.6000222000000122}]} />
<silkscreenpath route={[{"x":-1.9299935999999889,"y":-1.5999713999999585},{"x":-2.099995799999988,"y":-1.5999713999999585},{"x":-2.099995799999988,"y":-1.0999724000000697}]} />
<silkscreenpath route={[{"x":-1.9507200000000466,"y":-1.9760945999998967},{"x":-2.0744417869628933,"y":-2.1017165560874673},{"x":-1.9494500000001835,"y":-2.226074947892698},{"x":-1.8244582130372464,"y":-2.101716556087581},{"x":-1.948180000000093,"y":-1.9760945999998967}]} />
<silkscreentext text="{NAME}" pcbX="-0.0149606mm" pcbY="2.791462mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.462060600000086,"y":2.0414619999999104},{"x":2.4321393999999827,"y":2.0414619999999104},{"x":2.4321393999999827,"y":-2.4971380000000636},{"x":-2.462060600000086,"y":-2.4971380000000636},{"x":-2.462060600000086,"y":2.0414619999999104}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C202140.obj?uuid=fdc829583767408e90d29293c58f907c",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C202140.step?uuid=fdc829583767408e90d29293c58f907c",
        pcbRotationOffset: 90,
        modelOriginPosition: { x: -0.000025399999913133797, y: 0, z: 0 },
      }}
      {...props}
    />
  )
}
