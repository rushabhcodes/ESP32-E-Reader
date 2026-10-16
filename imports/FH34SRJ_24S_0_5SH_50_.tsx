import objPath from "../assets/components/C324726.obj"
import type { ConnectorProps } from "@tscircuit/props"

const pinLabels = {
	pin1: "NC1",
	pin2: "GDR",
	pin3: "RESE",
	pin4: "NC4",
	pin5: "VSH2",
	pin6: "NC6",
	pin7: "NC7",
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

export const FH34SRJ_24S_0_5SH_50_ = (props: ConnectorProps) => {
  return (
    <connector
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C324726"
  ]
}}
      manufacturerPartNumber="FH34SRJ-24S-0.5SH(50)"
      footprint={<footprint insertionDirection="from_bottom">
        <smtpad portHints={["pin1"]} pcbX="5.750052mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="5.25018mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="4.750054mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="4.250182mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="3.750056mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="3.250184mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="2.750058mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="2.250186mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="1.75006mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="1.250188mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="0.750062mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="0.25019mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="-0.249936mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="-0.749808mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="-1.249934mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="-1.749806mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="-2.249932mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="-2.749804mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="-3.24993mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="-3.749802mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="-4.249928mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="-4.7498mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="-5.249926mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="-5.749798mm" pcbY="1.250061mm" width="0.2500122mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="-6.75005mm" pcbY="-1.250061mm" width="0.5999988mm" height="0.999998mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="6.75005mm" pcbY="-1.250061mm" width="0.5999988mm" height="0.999998mm" shape="rect" />
<silkscreenpath route={[{"x":7.000138399999969,"y":-0.6243574000001217},{"x":7.000138399999969,"y":2.050059400000009}]} />
<silkscreenpath route={[{"x":-6.999884399999928,"y":-0.6243574000001217},{"x":-6.999884399999928,"y":2.050059400000009}]} />
<silkscreenpath route={[{"x":7.000138399999969,"y":2.050059400000009},{"x":-6.999884399999928,"y":2.050059400000009}]} />
<silkscreenpath route={[{"x":7.000138399999969,"y":0.8632697999998982},{"x":6.131280600000082,"y":0.8632697999998982}]} />
<silkscreenpath route={[{"x":-6.249873199999911,"y":-1.7499330000000555},{"x":6.250127200000179,"y":-1.7499330000000555}]} />
<silkscreenpath route={[{"x":7.000138399999969,"y":-0.6243574000001217},{"x":6.98957200000018,"y":-0.6243574000001217}]} />
<silkscreenpath route={[{"x":-6.131026599999814,"y":0.8632697999998982},{"x":-6.999884399999928,"y":0.8632697999998982}]} />
<silkscreenpath route={[{"x":-6.131026599999814,"y":0.8632697999998982},{"x":-6.999884399999928,"y":0.8632697999998982}]} />
<silkscreentext text="{NAME}" pcbX="0.002032mm" pcbY="3.062861mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-7.296468000000004,"y":2.312860999999998},{"x":7.300531999999976,"y":2.312860999999998},{"x":7.300531999999976,"y":-1.997139000000061},{"x":-7.296468000000004,"y":-1.997139000000061},{"x":-7.296468000000004,"y":2.312860999999998}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: -0.00010160000010728254, y: 0.19998760000007676, z: -0.02 },
      }}
      {...props}
    />
  )
}