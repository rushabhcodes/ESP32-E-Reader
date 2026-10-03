import type { InductorProps } from "@tscircuit/props"

export const SMMS0420_1R5M = (props: Omit<InductorProps, "inductance">) => {
  return (
    <inductor
      inductance="1.5uH"
      supplierPartNumbers={{
  "jlcpcb": [
    "C133190"
  ]
}}
      manufacturerPartNumber="SMMS0420-1R5M"
      footprint={<footprint>
        <smtpad portHints={["pin2"]} pcbX="-2.032mm" pcbY="0mm" width="1.3999972mm" height="1.8999962mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="2.032mm" pcbY="0mm" width="1.3999972mm" height="1.8999962mm" shape="rect" />
<silkscreenpath route={[{"x":-2.376449399999956,"y":1.1123929999999973},{"x":-2.376449399999956,"y":2.2262084000000186},{"x":2.3759414000001016,"y":2.2262084000000186},{"x":2.3759414000001016,"y":1.1123929999999973}]} />
<silkscreenpath route={[{"x":-2.376449399999956,"y":-1.1123929999999973},{"x":-2.376449399999956,"y":-2.2262084000000186},{"x":2.3759414000001016,"y":-2.2262084000000186},{"x":2.3759414000001016,"y":-1.1123929999999973}]} />
<silkscreentext text="{NAME}" pcbX="0.004572mm" pcbY="3.2352mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.97592799999984,"y":2.485200000000077},{"x":2.985072000000173,"y":2.485200000000077},{"x":2.985072000000173,"y":-2.459799999999973},{"x":-2.97592799999984,"y":-2.459799999999973},{"x":-2.97592799999984,"y":2.485200000000077}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C133190.obj?uuid=2516a1e7eb834d2794cc1600df3863b3",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C133190.step?uuid=2516a1e7eb834d2794cc1600df3863b3",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.00012699999979304266, y: 0, z: -0.1 },
      }}
      {...props}
    />
  )
}