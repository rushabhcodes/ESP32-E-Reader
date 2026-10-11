import objPath from "../assets/components/C133195.obj"
import type { InductorProps } from "@tscircuit/props"

export const SMMS0420_100M = (props: Omit<InductorProps, "inductance">) => {
  return (
    <inductor
      inductance="10uH"
      supplierPartNumbers={{
  "jlcpcb": [
    "C133195"
  ]
}}
      manufacturerPartNumber="SMMS0420-100M"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="2.277999mm" pcbY="0mm" width="1.7239996mm" height="1.9200114mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-2.277999mm" pcbY="0mm" width="1.7239996mm" height="1.9200114mm" shape="rect" />
<silkscreenpath route={[{"x":-2.376322400000049,"y":1.112393000000111},{"x":-2.376322400000049,"y":2.2262084000000186},{"x":2.3760684000000083,"y":2.2262084000000186},{"x":2.3760684000000083,"y":1.112393000000111}]} />
<silkscreenpath route={[{"x":-2.376322400000049,"y":-1.1123929999999973},{"x":-2.376322400000049,"y":-2.226208399999905},{"x":2.3760684000000083,"y":-2.226208399999905},{"x":2.3760684000000083,"y":-1.1123929999999973}]} />
<silkscreentext text="{NAME}" pcbX="-0.012827mm" pcbY="3.286mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-3.399727000000098,"y":2.5359999999999445},{"x":3.3740729999998393,"y":2.5359999999999445},{"x":3.3740729999998393,"y":-2.4851999999999634},{"x":-3.399727000000098,"y":-2.4851999999999634},{"x":-3.399727000000098,"y":2.5359999999999445}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.00012700000002041634, y: -0.000012700000070253736, z: -0.01 },
      }}
      {...props}
    />
  )
}
