# ESP32 E-Reader Rev. B

A four-layer, battery-powered e-reader PCB built around the ESP32-C3 and a
high-resolution four-color e-paper display. This repository contains the
[tscircuit](https://tscircuit.com/) implementation of the Rev. B hardware,
including the schematic, PCB layout, component data, and fabrication export
workflow.

## At a glance

| Specification | Current design |
| --- | --- |
| Enclosure outside | 68.0 × 109.5 × **21.1 mm**; prototype CAD, not a measured print |
| PCB | 62.5 × 95.08 × 1.6 mm; four copper layers |
| Display | EastRising ER-EPD3.97-1RY; 3.97 in, 480 × 800, four colors, no frontlight |
| Processor | ESP32-C3-WROOM-02-N4; 4 MB flash, Wi-Fi, Bluetooth LE |
| Storage | MicroSD over SPI |
| Battery | Protected 1-cell LiPo, 3.7 V nominal; modeled around 2000 mAh SparkFun PRT-13855 |
| Battery envelope | 49.2 × 68.8 × 5.6 mm nominal, excluding unverified lead and plug |
| USB | USB-C for charging and native ESP32-C3 USB data |
| Input | Four recessed navigation buttons, wake, reset, main power switch |

This repository is the **hardware and printable enclosure prototype**. It
does not contain e-reader firmware. Battery runtime, display cable fit, and
final printed fit have not been measured on an assembled device.

![Front of the dimensioned e-reader print prototype](assets/enclosure/printable-front.png)

![Exploded view of the screen, PCB, partition, battery and rear cover](assets/enclosure/printable-exploded.png)

## Display

The intended display is the **EastRising ER-EPD3.97-1RY**.

| Specification | Value |
| --- | --- |
| Display type | Reflective black, white, red, and yellow e-paper |
| Diagonal | 3.97 inches |
| Resolution | 480 × 800 pixels |
| Panel outline | 56.24 × 96.62 × 0.9 mm |
| Active area | 51.84 × 86.40 mm |
| Controller | SSD2677 |
| Interface | 4-wire SPI |
| E-paper connector | 24-pin, 0.5 mm-pitch FPC (J2) |

J2 is a Hirose `FH12-24S-0.5SH(55)` connector. The board provides the panel's
SPI signals and the external high-voltage bias network required by the
SSD2677. This reflective display has no frontlight, so the former frontlight
connector and boost-driver circuit are not fitted.

The centered 26 × 2 mm PCB slot allows a display FPC to pass from the front of
the assembly to J2 immediately above it on the component side. Moving J2
about 12 mm toward the slot shortens the required folded tail path. The
MicroSD socket is higher on the left edge, with its enclosure opening moved
to match. A panel whose integral tail cannot reach J2 still requires a
24-conductor, 0.5 mm-pitch extension cable and a compatible FPC/FFC coupler.
Select the cable contact orientation (same-side or
opposite-side contacts) only after checking pin 1 at both the display tail and
J2; reversing the contact orientation reverses the pin order. The supplier
lists this panel's connection as a soldering FPC, so confirm the actual tail
is compatible with the selected ZIF connector before ordering the board.

The 3D assembly includes an `assembly.screen` element attached to J2. Its
model shows the [EastRising panel outline and active-area
dimensions](https://www.buydisplay.com/3-97-inch-quad-color-e-paper-screen-e-ink-display-480x800)
on the front side of the PCB. The flexible tail and its fold through the slot
are not modeled.

> [!IMPORTANT]
> Do not select a panel based only on the “4.2-inch” description or the 24-pin
> connector. Many e-paper panels use similar FPCs but have different pinouts,
> resolutions, controllers, dimensions, and voltage requirements. The PCB and
> firmware are designed for the **ER-EPD3.97-1RY** pinout. Verify the full
> part number before purchasing or connecting a display.

## Hardware overview

| Function | Implementation |
| --- | --- |
| MCU | ESP32-C3-WROOM-02-N4, 4 MB flash, Wi-Fi and Bluetooth LE |
| Display | EastRising ER-EPD3.97-1RY, 480 × 800 four-color e-paper |
| Storage | MicroSD card over shared SPI |
| USB | USB-C power, native USB data, CC resistors, and USB ESD protection |
| Battery | Single-cell LiPo through a 2-pin JST-PH connector |
| Charging | MCP73831-2 linear LiPo charger |
| Battery protection | DW01A with FS8205A dual MOSFET |
| Logic supply | ME6211C33M5 3.3 V LDO |
| Controls | Back, Confirm, Left, Right, Wake, Reset/Enable, and main power switch |
| Board | 62.5 × 95.08 mm, 1.6 mm thick, four copper layers |

### Parts and supplies for one prototype

| Item | Selection / requirement |
| --- | --- |
| U4 microcontroller | ESP32-C3-WROOM-02-N4 |
| Display | EastRising ER-EPD3.97-1RY, matching the **verified** J2 pinout |
| J2 display connector | Hirose FH12-24S-0.5SH(55), 24 positions at 0.5 mm pitch |
| J4 MicroSD socket | Hirose DM3AT-SF-PEJM5 |
| J1 USB-C receptacle | GCT USB4105-GF-A |
| BT1 battery header | JST S2B-PH-K-S(LF)(SN), 2-pin, 2.0 mm pitch, side entry |
| Battery | Protected 3.7 V nominal single-cell pack; modeled PRT-13855, 2000 mAh, 49.2 × 68.8 × 5.6 mm |
| Navigation switches | 4 × Alps Alpine SKRPACE010, bottom-side assembly |
| Other controls | 2 × Panasonic EVQP7C01P (S1/S2); 1 × C&K JS102011SAQN (SW7) |
| Printed parts | Front shell, battery partition, rear cover, and 4 separate button caps |
| Assembly supplies | 2 suitable M2.5 PCB screws, 4 nominal M2.5 × 6 mm cover screws, display-safe perimeter adhesive, and thin nonconductive cell cushioning |

The [source component list and LCSC/JLCPCB mappings](design-data.ts) and the
[generated BOM](#fabrication-files) cover the remaining passives, charger,
protection devices, ESD device, and e-paper bias circuit. The USB-C body and
the display FPC fold are missing from the 3D collision model. Confirm the
delivered display tail, battery plug polarity, and screw fit before assembly.

The four navigation buttons share one ESP32 ADC input through a resistor
ladder. The e-paper display and MicroSD card share the SPI clock and MOSI lines
while using independent chip-select signals. USB D+ and D− connect directly to
the ESP32-C3's native USB pins.

The four front navigation controls use the same **Alps Alpine SKRPACE010**
bottom-side tactile switch listed in the [original reader's
BOM](https://github.com/IS7V4N/ESP32_E-Reader). Each switch is 4.2 × 3.2 ×
2.5 mm, with 0.2 mm travel and 2.55 N operating force according to the
[manufacturer](https://tech.alpsalpine.com/e/products/category/tact-switch/sub/02/series/skrp/).
They sit on 14 mm centers within the 62.5 mm board width. Moving the row 4 mm
closer to the display removes 5 mm from the lower PCB edge while keeping about
2 mm between the panel outline and the button openings. Four separate slim
case caps reproduce the reference reader's recessed front-button appearance;
they are not hot-swappable. This requires bottom-side assembly. Printable caps
include a rear retention flange and nominal 0.14 mm clearance to the switch
body, but actuation and print fit need a physical prototype. Check the actual
display ribbon width and fold radius against the 26 mm FPC slot before ordering
the PCB.

## Dimensioned enclosure print prototype

The slim case has a **68.0 × 109.5 × 21.1 mm** outside envelope. From front
through back it contains the display, 62.5 × 95.08 mm PCB, a 1.4 mm rigid
partition, a protected 2000 mAh LiPo compartment, and a removable rear cover.
The case separates the battery from the component side of the board. The
selected [SparkFun PRT-13855 pack](https://www.sparkfun.com/lithium-ion-battery-2ah.html)
has published **49.2 × 68.8 × 5.6 mm nominal dimensions**. It sits left of BT1
in an extended guide pocket, with 1.5 mm nominal clearance to the rear cover.
The partition has a local opening for BT1 and its lead. BT1's side-entry
mating face points toward the opening, so the plug enters from the bottom of
the PCB before the partition is seated. The thinner front section moves the
display 1.5 mm closer to the PCB; check its short FPC fold on a real sample.
Verify BT1 polarity against the actual battery plug before connection.
SparkFun's store currently restricts international shipment of this pack;
equivalent 2000 mAh packs must be checked for the complete protected-pack
envelope, lead, plug, and polarity before substitution.

| Thickness contribution | mm |
| --- | ---: |
| Front outer face to PCB center | 6.5 |
| PCB center to battery base, including partition | 6.0 |
| Nominal battery thickness | 5.6 |
| Nominal battery-to-cover clearance | 1.5 |
| Rear cover | 1.5 |
| **Modeled outside thickness** | **21.1** |

The pack gives 2000 mAh in a 5.6 mm nominal thickness. A 1200 mAh, 5 mm
pack would save 0.6 mm in this stack but reduce rated capacity by 40%.
Actual runtime has not been measured; the LDO may stop regulating before the
cell reaches its protection cutoff. The [full coordinate and tolerance
table](assets/enclosure/PRINTING.md) describes the printed parts.

![BT1 facing the partition cable opening](assets/enclosure/printable-battery-connector.png)

The [printable STL files and full dimension table](assets/enclosure/PRINTING.md)
include the shell, partition, rear cover, and four independent front caps.
The [component inventory](assets/enclosure/component-inventory.csv) lists
all 86 PCB references with footprint size and available 3D model envelopes.
The source models have missing body geometry for J1 (USB-C) and omit the
screen FPC fold, real battery lead, and manufacturing tolerances. The meshes
are manifold, but the first physical print and fit measurements remain
necessary before treating the case as a finished product.

![Open-back view of the battery compartment](assets/enclosure/printable-open-back.png)

![Side view of the slim enclosure](assets/enclosure/printable-side.png)

The outer silhouette follows the [Xteink X3 product](https://www.xteink.com/products/xteink-x3)
and the original [Rev. B KiCad project](https://github.com/IS7V4N/ESP32_E-Reader),
whose enclosure source mesh is unpublished. The front navigation switches
remain low-profile tactile buttons, and motion controls remain a later
hardware revision. The power-switch side slot is open for access, but a
coupled thumb slider is not included in the printable set.

## Board construction

The layer arrangement is:

```text
Top      — components and signals
Inner 1  — GND plane
Inner 2  — 3.3 V plane
Bottom   — components and signals
```

Ground fills are also present on the top and bottom layers. The
ESP32-C3-WROOM-02 antenna area has a keepout across all four copper layers.
The design uses 0.2 mm ordinary signal traces, 0.5 mm battery/USB/3.3 V
routes, 0.4–0.6 mm e-paper charge-pump routes, and 0.2/0.42 mm via drill/pad
diameters.

![PCB layout](__snapshots__/index.circuit-pcb.snap.svg)

## Repository layout

```text
.
├── index.circuit.tsx       # Board outline, planes, keepouts, and net routing
├── circuit-sections.tsx    # Functional schematic sections and components
├── design-data.ts          # Parts, placement, sourcing, nets, and trace widths
├── imports/                # Imported component footprints and models
├── __snapshots__/          # PCB, schematic, and 3D reference renders
├── assets/enclosure/       # Printable STLs, assembly GLBs, guide, and renders
├── scripts/                # Enclosure generation and clearance checks
├── tscircuit.config.json   # tscircuit project configuration
└── package.json            # Build, validation, and export commands
```

The design currently contains 86 components and 49 connected nets. Placement,
board geometry, and electrical intent are transcribed from the Rev. B KiCad
design; PCB routing is generated from the netlist by tscircuit's local
autorouter.

## Getting started

Install [Bun](https://bun.sh/) and then install the project dependencies:

```sh
bun install
```

Open the interactive tscircuit development view:

```sh
bun run dev
```

Type-check and build the design:

```sh
bun run typecheck
bun run build:pcb
```

`build:pcb` also generates a PCB preview image. For a longer release build with
an increased autorouter timeout, use:

```sh
bun run build:release
```

## Validation

Run the checks in this order so connectivity errors are caught before layout
and routing issues:

```sh
bunx tsci check netlist index.circuit.tsx
bunx tsci check schematic-placement index.circuit.tsx
bunx tsci check placement index.circuit.tsx
bunx tsci check trace-length index.circuit.tsx
bunx tsci check routing-difficulty index.circuit.tsx
bun run build
bunx tsci check shorts dist/index/circuit.json
```

Update the checked-in schematic, PCB, and 3D snapshots with:

```sh
bun run snapshot:update
```

The latest routed build produced **191 traces, zero routing errors**, and the
Gerber-derived shorts check found **no shorts**. The enclosure meshes have
one connected shell each and no non-manifold edges. The modeled shell,
partition, cell, cover, button caps, and available component meshes have no
unintended solid intersections. See [mesh-check.json](assets/enclosure/stl/mesh-check.json)
and [clearance-check.json](assets/enclosure/stl/clearance-check.json).
These checks do not validate the unmodeled USB-C body, display tail and bend,
battery lead and plug, button travel, or print tolerances.

`tsci check placement` currently exits with one **BT1 suboptimal-orientation
suggestion**: rotating the header would uncross its direct pad-connection
lines. BT1 is deliberately oriented with its mating face toward the case's
cable opening. The placement report lists zero placement DRC errors and zero
warnings; the routed build and shorts check above still pass. Inspect the
physical lead path and polarity before fabrication rather than changing that
orientation based only on the heuristic.

## Printable enclosure

The [print package](assets/enclosure/esp32-reader-printable-stls.zip)
contains the seven printable parts and the dimensioned guide. The separate
[STLs](assets/enclosure/stl/) and [print instructions](assets/enclosure/PRINTING.md)
are also available. Do **not** print the `battery-envelope-DO-NOT-PRINT` file;
it is a fit gauge.

To regenerate the meshes from source, install Blender and run:

```sh
blender --background --python scripts/generate-printable-enclosure.py
```

The generator updates the STL files, matching GLBs for the tscircuit
assembly, mesh checks, and ZIP package. The [print guide](assets/enclosure/PRINTING.md)
also gives the component-clearance and preview-render commands.

## Fabrication files

Generate the manufacturing archive with:

```sh
bun run export:gerbers
```

The output is written to `dist/esp32-e-reader-gerbers.zip` and includes the
four copper layers, solder mask, paste, silkscreen, fabrication and edge-cut
Gerbers, plated/non-plated drill files, BOM, and pick-and-place CSV files.
The export completes, but the CLI cannot verify pick-and-place rotation for
U1, U2, U3, SW2, SW3, SW4, SW6, and SW7 against supplier pin-1 data. Check
those placements manually against the component drawings before ordering
assembled boards.

> [!CAUTION]
> This is a prototype hardware design, not a certified consumer product. Review the
> schematic, battery polarity, component voltage ratings, PCB clearances, BOM,
> and fabrication outputs before ordering or powering a board. E-paper bias
> rails generate voltages well above the 3.3 V logic rail.

## Power, charging, and bring-up

- R9 is 2.5 kΩ on MCP73831 PROG, giving approximately **400 mA** programmed
  charge current. Verify the delivered pack's permitted charging current and
  measure the actual rate before relying on it.
- SW7 is the hard main-power control. It switches the ME6211 LDO enable input
  between the battery rail and an off-state pull-down, so the switch does not
  carry the ESP32 or display load current. S2 remains a firmware wake/power
  button.
- Charge the battery only with SW7 **OFF** and a battery connected. U1 is an
  MCP73831 charger; its VBAT output also feeds U5 and the system. There is no
  power-path/load-sharing circuit, so operating the reader while charging can
  disturb charge termination. USB-only operation without a battery is not
  supported. A future revision intended for simultaneous charging and use
  needs a dedicated power path, such as an integrated load-sharing charger.
  SW7 does not electrically interlock charging and operation; this is an
  operating requirement.
- R30 pulls ESP32-C3 GPIO8 high on the MCU side of the 20 Ω SPI-clock series
  resistor R27. Closing JP1 pulls GPIO9 low for ROM download mode; GPIO8 must
  stay high when reset is released. During bring-up, connect the display and SD
  card, close JP1, reset with S1, confirm USB ROM download/programming works,
  then open JP1 and confirm normal boot. Check GPIO8 at U4 during reset if
  programming is unreliable. See the [ESP32-C3 boot-mode table](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html).
- U5 is a 3.3 V LDO, so V3V3 cannot remain regulated through the full LiPo
  discharge range. The ESP32-C3 module requires 3.0–3.6 V at its supply; the
  LDO also needs load-dependent dropout headroom. The minimum usable battery
  voltage has **not** been verified. Before field use, measure battery voltage
  at TP1 and V3V3 at TP2 during Wi-Fi transmit, SD writes, and display refresh
  at low state of charge. Set a firmware low-battery shutdown threshold that
  keeps V3V3 above 3.0 V and within every peripheral's specified range under
  those loads, with margin. The firmware threshold is not implemented in this
  hardware repository. Use a buck-boost supply if operation through the full
  cell discharge range is required. See
  the [ESP32-C3-WROOM-02 supply specification](https://documentation.espressif.com/esp32-c3-wroom-02_datasheet_en.html)
  and [ME6211 datasheet](https://datasheet.lcsc.com/szlcsc/Nanjing-Micro-One-Elec-ME6211C33M5G-N_C82942.pdf).
