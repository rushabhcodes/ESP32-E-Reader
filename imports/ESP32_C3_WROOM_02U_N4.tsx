import type { ChipProps } from "@tscircuit/props"

export const pinLabels = {
  pin1: ["3V3"],
  pin2: ["EN"],
  pin3: ["IO4"],
  pin4: ["IO5"],
  pin5: ["IO6"],
  pin6: ["IO7"],
  pin7: ["IO8"],
  pin8: ["IO9"],
  pin9: ["GND1"],
  pin10: ["IO10"],
  pin11: ["RXD"],
  pin12: ["TXD"],
  pin13: ["IO18"],
  pin14: ["IO19"],
  pin15: ["IO3"],
  pin16: ["IO2"],
  pin17: ["IO1"],
  pin18: ["IO0"],
  pin19: ["GND2"],
  pin20: ["GND3"],
  pin21: ["GND4"],
  pin22: ["GND5"],
  pin23: ["GND6"],
  pin24: ["GND7"],
  pin25: ["GND8"],
  pin26: ["GND9"],
  pin27: ["GND10"]
} as const

const pinAttributes = {
  pin1: {requiresPower: true},
  pin9: {requiresGround: true},
  pin19: {requiresGround: true},
  pin20: {requiresGround: true},
  pin21: {requiresGround: true},
  pin22: {requiresGround: true},
  pin23: {requiresGround: true},
  pin24: {requiresGround: true},
  pin25: {requiresGround: true},
  pin26: {requiresGround: true},
  pin27: {requiresGround: true}
} as const

export const ESP32_C3_WROOM_02U_N4 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2926676"
  ]
}}
      manufacturerPartNumber="ESP32-C3-WROOM-02U-N4"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-8.9000076mm" pcbY="5.999988mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-8.9000076mm" pcbY="4.500118mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-8.9000076mm" pcbY="2.999994mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-8.9000076mm" pcbY="1.500124mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-8.9000076mm" pcbY="0mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-8.9000076mm" pcbY="-1.49987mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-8.9000076mm" pcbY="-2.999994mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-8.9000076mm" pcbY="-4.499864mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="-8.9000076mm" pcbY="-5.999988mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="8.9000076mm" pcbY="-5.999988mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="8.9000076mm" pcbY="-4.500118mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="8.9000076mm" pcbY="-2.999994mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="8.9000076mm" pcbY="-1.500124mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="8.9000076mm" pcbY="0mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="8.9000076mm" pcbY="1.49987mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="8.9000076mm" pcbY="2.999994mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="8.9000076mm" pcbY="4.499864mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="8.9000076mm" pcbY="5.999988mm" width="1.499997mm" height="0.8999982mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="2.059686mm" pcbY="0.900176mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="0.959866mm" pcbY="0.899922mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="-0.140208mm" pcbY="0.899922mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="-0.140208mm" pcbY="-0.199898mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="0.959866mm" pcbY="-0.199898mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="2.059686mm" pcbY="-0.199898mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="2.059686mm" pcbY="-1.299972mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="0.959866mm" pcbY="-1.299972mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin27"]} pcbX="-0.140208mm" pcbY="-1.299972mm" width="0.6999986mm" height="0.6999986mm" shape="rect" />
<silkscreenpath route={[{"x":-9.017000000000053,"y":6.681139799999983},{"x":-9.017000000000053,"y":7.366050799999925},{"x":9.016999999999825,"y":7.366050799999925},{"x":9.016999999999825,"y":6.681114399999956}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-6.985000000000014},{"x":9.016999999999825,"y":-6.985000000000014},{"x":9.016999999999825,"y":-6.681139800000096}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-6.681139800000096},{"x":-9.017000000000053,"y":-6.985000000000014}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-5.181092000000035},{"x":-9.017000000000053,"y":-5.318861600000105}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-3.681094999999914},{"x":-9.017000000000053,"y":-3.8188138000000436}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-2.18109800000002},{"x":-9.017000000000053,"y":-2.318816800000036}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":-0.6811264000000392},{"x":-9.017000000000053,"y":-0.8188197999999147}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":0.8188705999999684},{"x":-9.017000000000053,"y":0.681151800000066}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":2.3188675999998623},{"x":-9.017000000000053,"y":2.18114879999996}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":3.8188645999999835},{"x":-9.017000000000053,"y":3.681145799999854}]} />
<silkscreenpath route={[{"x":-9.017000000000053,"y":5.318836199999964},{"x":-9.017000000000053,"y":5.181142799999975}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":5.181142799999975},{"x":9.016999999999825,"y":5.318836199999964}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":3.681145799999854},{"x":9.016999999999825,"y":3.818839199999843}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":2.18114879999996},{"x":9.016999999999825,"y":2.318842199999949}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":0.6811263999999255},{"x":9.016999999999825,"y":0.8188451999999415}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":-0.818870600000082},{"x":9.016999999999825,"y":-0.6811771999999792}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":-2.3189184000001433},{"x":9.016999999999825,"y":-2.1811742000001004}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":-3.818890000000124},{"x":9.016999999999825,"y":-3.681222000000048}]} />
<silkscreenpath route={[{"x":9.016999999999825,"y":-5.318861600000105},{"x":9.016999999999825,"y":-5.181168199999888}]} />
<silkscreencircle pcbX="-9.525mm" pcbY="6.731mm" radius="0.100076mm" />
<silkscreentext text="{NAME}" pcbX="0mm" pcbY="8.4422mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-9.902000000000157,"y":7.692200000000071},{"x":9.901999999999816,"y":7.692200000000071},{"x":9.901999999999816,"y":-7.387400000000071},{"x":-9.902000000000157,"y":-7.387400000000071},{"x":-9.902000000000157,"y":7.692200000000071}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2926676.obj?uuid=99c92cd30bdf44c49576fce166ebf2be",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2926676.step?uuid=99c92cd30bdf44c49576fce166ebf2be",
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0.000012700000070253736, y: 0, z: -0.01 },
      }}
      {...props}
    />
  )
}
