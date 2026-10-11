# ESP32 E-Reader Rev. B

A four-layer, battery-powered e-reader PCB built around the ESP32-C3 and a
high-resolution four-color e-paper display. This repository contains the
[tscircuit](https://tscircuit.com/) implementation of the Rev. B hardware,
including the schematic, PCB layout, component data, and fabrication export
workflow.

## At a glance

| Specification | Current design |
| --- | --- |
| Enclosure outside | 68.0 × 116.81 × **16.8 mm**; prototype CAD, not a measured print |
| PCB | 62.5 × 95.08 × 1.6 mm; four copper layers |
| Display | Waveshare 3.97inch e-Paper (G), raw display only; 480 × 800, four colors, no frontlight |
| Processor | ESP32-C3-WROOM-02U-N4; 4 MB flash, Wi-Fi, Bluetooth LE, external antenna |
| Storage | MicroSD over SPI |
| Battery | Protected 1-cell LiPo, 3.7 V nominal; modeled around 2000 mAh SparkFun PRT-13855 |
| Battery envelope | 49.2 × 68.8 × 5.6 mm nominal, excluding unverified lead and plug |
| USB | USB-C for charging and native ESP32-C3 USB data |
| Input | Four recessed navigation buttons, wake, reset, main power switch |

This repository is the **hardware and printable enclosure prototype**. It
does not contain e-reader firmware. Battery runtime, display cable fit, and
final printed fit have not been measured on an assembled device.

![Front of the dimensioned e-reader print prototype](assets/enclosure/printable-front.png)

![Exploded view of the screen, PCB, battery and rear cover](assets/enclosure/printable-exploded.png)

## Display

The selected screen is the **Waveshare 3.97inch e-Paper (G)**: black, white,
red and yellow, 800 × 480 landscape / 480 × 800 portrait, with an SSD2677.
The [manufacturer manual](https://www.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B_%28G%29_Manual)
and [Rev. 1.0 raw-panel datasheet](https://files.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B_G/3.97inch_e-Paper_G.pdf)
are the design basis. Buy the exact **(G)** model from
[Robu India, SKU R254505](https://robu.in/product/waveshare-3-97inch-e-paper-display/).
The retail kit includes a driver HAT; this PCB connects directly to the raw
panel's ribbon and supplies its boost circuit, so the HAT is not installed.
Confirm the kit's panel label before assembly.

**The PCB order is still gated by the delivered screen tail.** Rev. H corrects
the early fold and replaces the FH12 socket with a short-contact candidate,
[Hirose FH34SRJ-24S-0.5SH(50), C324726](https://www.lcsc.com/product-detail/C324726.html).
It has 24 contacts at 0.5 mm pitch and accepts either contact face. The exact
supplier footprint and local OBJ/STEP are bundled. Its recommended tail has a
shorter exposed area than FH12, but the panel's full tolerances are not contained
in Hirose's recommended drawing. Nominal matching dimensions alone cannot
establish acceptance. See [the ordering gate](ORDERING.md) and
[interface report](assets/enclosure/stl/display-interface-check.json).

The [display import](imports/Waveshare_3_97inch_ePaper_G.tsx) and
[shared dimensions](assets/enclosure/display-connection.json) position the
56.24 × 96.62 mm glass at Y +15.31 and model its maximum 1.10 mm thickness.
Its 51.84 × 86.40 mm active area is at Y +18.22. The offset L-shaped tail has a
12.50 mm tip at X +21.87, a 33.66 mm longitudinal projection, 3.00 ± 0.30 mm
stiffener and 1.70 ± 0.30 mm exposed contacts.

The first **15.00 mm stays flat**, through the bonded/driver region, before
bending at the OEM positioning line (17.40 − 2.40 mm). The tail wraps around
the bottom PCB edge at Y −48.60; the old PCB slot is removed. It returns above
the PCB at Z +1.70 before settling into J2, centered at
**X +21.87, Y −35.08101 mm**, with PCB and supplier rotation 0°.
Socket pin 1 is +X in the canonical footprint. The panel mechanical drawing
does not establish its pin-1 direction; CAD finger numbering is only socket
numbering. Verify panel numbering independently before ordering/powering.
The two main 0.6 mm bends remain installation assumptions, not an OEM rating.
The [ribbon preview](assets/enclosure/display-ribbon-connection.png) shows
this nominal route.

The two-part transparent snap-fit enclosure is **68 × 116.81 × 16.8 mm**.
The lower end grows 1.00 mm from Rev. F to clear the edge wrap; thickness is
unchanged. The custom GLB compensates the 180° rotation that `assembly.screen`
derives from J2’s −Y insertion direction. The fit check compares source solids
with every native exported display vertex. The navigation switches and complete printed keys now sit in two pairs at
X ±16.5 and ±27.5 mm, entirely beside the front ribbon corridor. The integral
front floor shields the tail between the pairs. No key flange is notched for
the ribbon. The lower mounts are at (−25.5, −36.5) and (+28, −29) mm. R6 and the
lowest screen clips move to Y −22 mm to clear the right mount. All four PCB
mounts remain. BT1 stays at X +26, Y −4, with its matching lead notch.

The [Waveshare reference schematic](https://files.waveshare.com/wiki/3.97inch_e-Paper_HAT%2B_G/3.97inch_e-Paper_HAT%2B.pdf)
specifies a **10 µH** display boost inductor. L1 now uses the exact supplier
footprint and local CAD for [SMMS0420-100M, C133195](https://www.lcsc.com/product-detail/C133195.html),
a 2 mm-high shielded part with a 1.6 A current rating and 2 A saturation current. J2 pins **1, 4, 6, 7 and 19
are left open**; pin 8 is tied to GND for four-wire SPI. VDDIO and VCI remain
at 3.3 V. All other SPI, control and charge-pump pins follow the raw-panel table.
BUSY is active low. Firmware must use the Waveshare SSD2677 four-color driver
and initialization sequence; this repository does not yet include reader firmware.

J2's dual contacts permit the installed exposed face toward the PCB. Confirm
full insertion and locking, the actual reinforced tip thickness, contact width,
contact exposure and stiffener length, and screen pin numbering on a sample.
Do not force or crease the ribbon. The PCB order gate remains closed until
that evidence is recorded; no physical sample has been tested.

## Hardware overview

| Function | Implementation |
| --- | --- |
| MCU | ESP32-C3-WROOM-02U-N4, 4 MB flash, Wi-Fi and Bluetooth LE |
| Display | Waveshare 3.97inch e-Paper (G) raw 480 × 800 four-color panel |
| Storage | MicroSD card over shared SPI |
| USB | USB-C power, native USB data, CC resistors, and USB ESD protection |
| Battery | Single-cell LiPo through a 2-pin JST-PH connector |
| Charging | BQ24074 power-path LiPo charger, 500 mA USB input limit |
| Battery protection | DW01A with FS8205A dual MOSFET |
| Logic supply | TPS63021 fixed 3.3 V buck-boost converter |
| Controls | Back, Confirm, Left, Right, Wake, Reset/Enable, and main power switch |
| Board | 62.5 × 95.08 mm, 1.6 mm thick, four copper layers |

### Parts and supplies for one prototype

| Item | Selection / requirement |
| --- | --- |
| U4 microcontroller | ESP32-C3-WROOM-02U-N4 with external U.FL antenna |
| Display | Waveshare 3.97inch e-Paper (G); use the raw panel from the retail kit |
| External antenna | Taoglas FXP75.07.0045B, 45 mm cable; rear-cover adhesive mount |
| J2 display connector | Hirose FH34SRJ-24S-0.5SH(50), 24 positions at 0.5 mm pitch |
| J4 MicroSD socket | Hirose DM3AT-SF-PEJM5 |
| J1 USB-C receptacle | GCT USB4105-GF-A |
| BT1 battery header | JST S2B-PH-K-S(LF)(SN), 2-pin, 2.0 mm pitch, side entry |
| Battery | Protected 3.7 V nominal single-cell pack; modeled PRT-13855, 2000 mAh, 49.2 × 68.8 × 5.6 mm |
| Navigation switches | 4 × Alps Alpine SKRPACE010, bottom-side assembly |
| Other controls | 2 × Panasonic EVQP7C01P (S1/S2); 1 × SHOU HAN MSK12C02-HB / C431541 (SW7) |
| Printed parts | Two: front chassis with integral keys, screen clips and latch receivers; transparent snap-fit rear cover with PCB supports and battery guides |
| Assembly supplies | 4 M2.5 × 4 mm internal PCB screws (head ≤5 mm diameter, ≤2.5 mm high), display-border pads, 0.2 mm insulating battery liner and two 0.5 mm nonconductive adhesive strips; zero cover screws |

The [source component list and LCSC/JLCPCB mappings](design-data.ts) and the
[generated BOM](#fabrication-files) cover the remaining passives, charger,
protection devices, ESD device, and e-paper bias circuit. The USB-C body is
checked against the printable case using the local GCT manufacturer OBJ;
the antenna cable and mating plug remain unmodeled. The display fold is nominal CAD. Confirm the delivered display tail, battery plug polarity,
antenna cable path, and screw fit before assembly.

The four navigation buttons share one ESP32 ADC input through a resistor
ladder. The e-paper display and MicroSD card share the SPI clock and MOSI lines
while using independent chip-select signals. USB D+ and D− connect directly to
the ESP32-C3's native USB pins.

The four front navigation controls use the same **Alps Alpine SKRPACE010**
bottom-side tactile switch listed in the [original reader's
BOM](https://github.com/IS7V4N/ESP32_E-Reader). Each switch is 4.2 × 3.2 ×
2.5 mm, with 0.2 mm travel and 2.55 N operating force according to the
[manufacturer](https://tech.alpsalpine.com/e/products/category/tact-switch/sub/02/series/skrp/).
Their X centers are −27.5, −16.5, +16.5 and +27.5 mm within the 62.5 mm board width. The Waveshare glass
leaves 6.9 mm between its lower edge and the navigation key openings. Four
slim key caps and independent PETG leaf arms are integral to the front chassis. This requires bottom-side switch assembly. Each key has a nominal
0.04 mm rest gap and 0.25 mm total stroke, giving about 0.21 mm switch
compression. Force, return and print fit need a physical prototype. Check the actual
display ribbon width and fold radius against the edge-wrap route before ordering
the PCB.

## Dimensioned enclosure print prototype

The redesigned Rev. H enclosure uses **two printed parts** in a
**68.0 × 116.81 × 16.8 mm** envelope. The Waveshare screen and edge wrap add 5.81 mm
across the upper and lower ends while retaining the 16.8 mm thickness.
Moving the same battery toward the button end avoids stacking it over the
ESP32 module. The front chassis combines the screen
ledge, six releasable padded border clips and four independently moving keys.
The transparent rear cover combines the PCB cantilever supports, battery guides,
four integral snap leaves and two extra supports for the upper screen border.

The PCB fastens to the rear cover from its display-facing underside. The
front chassis therefore has a clear path for screen installation. Four side
snap hooks engage matching receivers in the front chassis. Recessed side
windows allow releasing them with a plastic pick. Four M2.5 screws retain
the PCB; the cover uses no screws. The selected protected
[SparkFun PRT-13855 pack](https://www.sparkfun.com/lithium-ion-battery-2ah.html)
has **49.2 × 68.8 × 5.6 mm nominal dimensions**. It bonds to the inside rear
cover with two nonconductive foam adhesive strips; a thin insulating liner
covers its PCB-facing surface. No separate battery tray needs printing.
The battery is now centered at X −6.0, Y −8.5 mm and lowered from Z 4.9 to
Z 3.7. The rear wall remains 1.2 mm thick. The screen's padded ledge, six clips
and two upper supports are adjusted for the Waveshare glass thickness and active-area offset.
Print both Rev. H shells as a pair. The battery loads through the open upper
end of its guides and slides 9.5 mm toward the lower stop before fitting the PCB.

| Thickness contribution | mm |
| --- | ---: |
| Front outer face to PCB center | 5.8 |
| PCB center to battery base | 3.7 |
| Nominal battery thickness | 5.6 |
| Battery mounting adhesive | 0.5 |
| Rear cover | 1.2 |
| **Modeled outside thickness** | **16.8** |

The battery liner has 0.25 mm nominal clearance above the lower PCB mounting
bosses; electronic clearances are recorded in the regenerated CAD report. The shifted battery's liner clears the
ESP32 module by 1.63 mm in Y. These are CAD measurements; actual pack thickness,
swelling allowance, wires and printed tolerances need a prototype check.

The actual CAD materials use alpha blending: 0.38 opacity for the front,
0.22 for the rear. The hosted viewer and native export use 0.5 opacity through
the explicit translucency flags. This lets you see the components inside. Clear PETG FDM
prints are normally translucent; the CAD appearance does not predict glass-like
clarity. The design assumes a 0.4 mm nozzle and PETG flexures. Physical fit,
clip force, key fatigue, battery retention and cable routing need a prototype.

![Display held on padded border ledges and integral side clips](assets/enclosure/display-retainer-installed.png)

The [print ZIP](assets/enclosure/esp32-reader-printable-stls.zip) contains exactly
**two bed-oriented STLs**, the [220 × 220 mm 3MF plate](assets/enclosure/reader-print-plate.3mf),
and the [print and assembly guide](assets/enclosure/PRINTING.md). Both parts
print flat, outside face on the bed. Use removable supports under the spring
leaves and projecting features, including supports that start on the model.
The open battery pocket leaves them accessible for removal.

The [component inventory](assets/enclosure/component-inventory.csv) records
PCB references, footprint sizes and model envelopes. `bun run export:assembly`
resolves the local CAD and writes `dist/index/assembly.glb`; missing OBJ/GLB
fetches fail the export. Supplier OBJ models are bundled for browser rendering.
The supplier STEP archives ([1](assets/components/supplier-step-models-1.zip), [2](assets/components/supplier-step-models-2.zip), [3](assets/components/supplier-step-models-3.zip), [4](assets/components/supplier-step-models-4.zip)) preserve
original source models without loading large STEP duplicates in the preview.
Source URLs and hashes remain in `assets/components/sources.json`.

Four PCB mounting holes locate the board: the upper pair is at
X ±27, Y 44.75 mm; the lower mounts are at (−25.5, −36.5) and (+28, −29) mm. Each 2.7 mm hole has
a 3.2 mm copper keepout on every layer. The board seats at Z +0.8 on rear-cover
bosses and the M2.5 × 4 mm screws enter from the underside. The Rev. H connector, middle keys, lower holes and edge-wrap geometry require
fresh routing; cached copper from earlier geometry is rejected.
Run `bun scripts/check-pcb-mounts.mjs` after the routed build to check drills,
board edges and copper. The enclosure check verifies screwdriver access with
the front chassis removed.

![PCB mounting points in the two-part enclosure](assets/enclosure/printable-pcb-mounts.png)

![Electronics with the rear cover removed](assets/enclosure/printable-open-back.png)

![Transparent side view of the 16.8 mm enclosure](assets/enclosure/printable-side.png)

The front navigation switches remain the low-profile SKRPACE010 parts. The
power switch is accessible through a side slot; a coupled thumb slider is not
included. Display flex, battery plug polarity, actual lead lengths and antenna
coax routing still require sample verification before assembly.

## Board construction

The layer arrangement is:

```text
Top      — components and signals
Inner 1  — GND plane
Inner 2  — 3.3 V plane
Bottom   — components and signals
```

Ground fills are also present on the top and bottom layers. U4 is the
external-antenna ESP32-C3-WROOM-02U variant. Its antenna cable leads to the
Taoglas FXP75 film modeled at X = 25, Y = 44 mm under the plastic rear cover.
The old PCB-antenna copper keepout has been removed.
The design requests 0.2 mm ordinary signal traces, 0.5 mm battery/USB/3.3 V
routes, and 0.4–0.6 mm e-paper charge-pump routes. Fine-pitch escapes may be narrowed by the autorouter; inspect the routed
artifact rather than assuming every segment uses the requested net width. Vias request 0.30/0.60 mm drill/pad diameters, with a 0.15 mm radial
annulus. Routing requires 0.20 mm hole-to-trace and via-hole-to-via-hole
clearance, 0.45 mm plated-hole-to-hole clearance, and 0.30 mm board-edge
clearance. Via-in-pad routing is disabled.

![PCB layout](__snapshots__/index.circuit-pcb.snap.svg)

### JLCPCB fabrication settings

Use four-layer FR-4, 1.6 mm thickness, standard copper (1 oz outer / 0.5 oz
inner), green solder mask and standard routing tolerances. The board fits
inside 100 × 100 mm. Choose ordinary through vias and tenting, with no
blind/buried vias or filled/capped via-in-pad service. Check the live quote;
these settings target standard fabrication, not a guaranteed price.

[JLCPCB's manufacturing capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/)
(accessed 6 October 2026) state that 0.20/0.25 mm holes with pads below
0.45 mm incur extra charges. The former 0.20/0.42 mm vias met that condition;
the new 0.30/0.60 mm target avoids it. The 2.7 mm mounting holes and 2 mm
mounting holes exceed the 0.5 mm NPTH minimum; the ribbon wraps outside the PCB.
Select 0.30 mm as the order's minimum via drill only after checking the
exported drill file.

For assembly, compare lead-free HASL with ENIG in the quote and assembly
preview; J2's 0.5 mm pitch and the QFN parts benefit from ENIG's flat surface.
Double-sided assembly, extended parts and surface finish can affect cost
separately from via drilling. Retain the four layers for the present routing
and planes; a two-layer cost reduction would require a separate redesign.

## Repository layout

```text
.
├── index.circuit.tsx       # Board outline, planes, keepouts, and net routing
├── circuit-sections.tsx    # Functional schematic sections and components
├── design-data.ts          # Parts, placement, sourcing, nets, and trace widths
├── schematic-layout.ts     # Explicit positions for all 94 parts on five sheets
├── imports/                # Imported component footprints and models
├── __snapshots__/          # PCB, schematic, and 3D reference renders
├── assets/enclosure/       # Printable STLs, assembly GLBs, guide, and renders
├── scripts/                # Enclosure generation and clearance checks
├── tscircuit.config.json   # tscircuit project configuration
└── package.json            # Build, validation, and export commands
```

Placement, board geometry, and electrical intent are transcribed from the Rev. B KiCad
design; PCB routing is generated from the netlist by tscircuit's local
autorouter.

The schematic groups parts by function, with dedicated power, display,
storage, and control sections. `functional-schematic-symbols.tsx` arranges
chip pins for readable signal flow while retaining physical pin identities.
The controls sheet shows the navigation buttons on one ADC bus with their
resistors below and names beside each key. The SKRPACE010 symbol explicitly
maps its active contacts to physical pins 1 and 4. After building, run
`bun scripts/check-controls-schematic.mjs` to verify the visible bus and
resistor connections, including terminals missed by ordinary style checks.
The Waveshare connector, edge-wrap route, battery socket and boost inductor require
fresh routing. `verified-pcb-routes.json` stores the validated routing baseline;
its guard compares all physical geometry, connectivity, keepouts, widths and
rules. Any physical change invokes routing again. Check the guard with
`bun scripts/check-routing-cache.mjs`.

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

Cloud builds use a 40-minute worker limit from `tscircuit.config.json`. The
default 10-minute limit stopped release 1.0.51 during PCB routing, before the
schematic, PCB, and 3D artifacts could be generated.

The cloud prebuild also copies local GLB, OBJ, and STEP models into `dist` at
the paths referenced by circuit JSON, so the hosted 3D view can load them.

## Validation

Run the checks in this order so connectivity errors are caught before layout
and routing issues:

```sh
bunx tsci check netlist index.circuit.tsx
bunx tsci check schematic-placement index.circuit.tsx
bunx tsci check placement index.circuit.tsx
bunx tsci check trace-length index.circuit.tsx
bunx tsci check routing-difficulty index.circuit.tsx
bun run build:release
bunx tsci check shorts dist/index/circuit.json --layer all
```

Update the checked-in schematic, PCB, and 3D snapshots with:

```sh
bun run snapshot:update
```

The Waveshare adaptation builds locally with **227 routed traces and 176
ordinary through vias**, with zero build errors and no Gerber-derived shorts
on top, bottom, inner1 or inner2. Netlist, schematic placement, PCB placement,
TypeScript, mounting-hole copper clearance and the 87-row assembly export pass.
The offset ribbon and screen clear the PCB, component meshes, battery and case
in the nominal CAD checks. Sampled enclosure assembly/release paths pass.
The export guard verifies the offset J2 location and requires pins 1, 4, 6, 7
and 19 to remain open. It rejects build errors, missing supplier IDs and
nonstandard drills. Connector pitch follows the Waveshare raw-panel datasheet.
J2 intentionally accepts the internal ribbon from the −Y side with the case
open. The canonical C324726 footprint places socket pin 1 on +X, with 0°
PCB/CAD and supplier placement rotation. The edge-access heuristic warns
because +X is the nearest outer edge; the actual internal tail enters from −Y
with the case open, and is checked separately in CAD.
The regenerated two-part meshes are manifold. PrusaSlicer 2.9.6+arch5 slices
both parts and their 3MF plate without warnings using the 0.4 mm / 0.2 mm
reference PETG profile. The plate estimate, including supports, is recorded in the current slice report. Toolpath presence for the springs, clips, snaps and upper screen
supports, bed bounds and selected layers were checked. See the
[slice report](assets/enclosure/stl/printability-check.json) and
[toolpath inspection](assets/enclosure/stl/toolpath-check.json).
The ribbon's separate drawing check requires supplier/sample acceptance; its
collision-free CAD does not establish compatibility. A target-printer slice,
physical screen-tail, battery lead, button travel and printed-fit checks remain
necessary.

## Printable enclosure

![Two parts arranged for printing on a 220 mm bed](assets/enclosure/reader-print-plate.png)

The [print package](assets/enclosure/esp32-reader-printable-stls.zip)
contains two bed-oriented STLs, a geometry-only
[3MF plate](assets/enclosure/reader-print-plate.3mf), and the
[print instructions](assets/enclosure/PRINTING.md). The separate
[STLs](assets/enclosure/print/) are also available. Files marked `DO-NOT-PRINT`
are inspection gauges. The integral keys, cover snaps and screen clips require PETG and removable
supports beneath their projecting leaves. Choose your actual printer and filament
preset before slicing; no printer-specific G-code is supplied.

To regenerate the meshes from source, install Blender and run:

```sh
blender --background --python-exit-code 1 --python scripts/generate-printable-enclosure.py
```

The generator updates the STL files, matching GLBs for the tscircuit
assembly, mesh checks, and ZIP package. The [print guide](assets/enclosure/PRINTING.md)
also gives the component-clearance and preview-render commands.

After the release checks pass, commit the source and publish with
`bun run push:release`, then push the commit to GitHub. This command runs
`tsci push` from the committed runtime files, with original STEP
models in their small ZIP archives, because direct `tsci push`
does not honor `.gitignore` and can upload local check fixtures and caches.
Prebuild restores downloads and PNG previews from tracked STEP/STL/JSON sources
because the Git importer omits ZIP and image files. Re-rendering also refreshes
the checksummed preview restore sources.

## Fabrication files

Generate the manufacturing archive with:

```sh
bun run build:release
bun run export:gerbers
```

`export:gerbers` first runs the display-interface ordering gate and exits
without creating an archive while supplier/sample qualification is missing.
Once qualified, it uses the just-built `dist/index/circuit.json`, so it does not
routinely rerun the autorouter. The output is written to
`dist/esp32-e-reader-gerbers.zip` and includes the
four copper layers, solder mask, paste, silkscreen, fabrication and edge-cut
Gerbers, plated/non-plated drill files, BOM, and pick-and-place CSV files.
All BOM rows have JLCPCB part numbers, including the four SKRPACE010
navigation switches (C139797). U1, U2, U3, U4, U5, L1, L2, SW2, SW3, SW4, and
SW6 use imported supplier footprints for assembly placement. `export:gerbers`
checks the BOM, critical placement rows, absence of build errors, Waveshare J2 position,
through-via geometry, and the actual minimum plated drill before accepting
the archive.

SW7 uses the exact C431541 supplier footprint and model: three switch contacts,
four grounded metal-case solder feet, and two locator holes. The schematic
labels its terminals ON (1), COM (2), OFF (3), and CASE (4). Pin 2 remains the
common contact driving U5 EN; pin 1 selects `SYS_OUT`, and pin 3 selects the
100 kΩ off-state pull-down. Its top-side 90° rotation places contact 1 below
contacts 2 and 3 and points the actuator into the existing side opening. The
export check validates the contacts, case ground, footprint, and placement
against the [supplier drawing](https://datasheet.lcsc.com/datasheet/pdf/21c16deb74d468a7f4a81f736600ec0e.pdf?productCode=C431541).
Confirm the SW7 orientation in the assembler's placement preview.

> [!CAUTION]
> This is a prototype hardware design, not a certified consumer product. Review the
> schematic, battery polarity, component voltage ratings, PCB clearances, BOM,
> and fabrication outputs before ordering or powering a board. E-paper bias
> rails generate voltages well above the 3.3 V logic rail.

### Release checks requiring physical parts

The ribbon document check still requires connector-tail tolerance acceptance,
physical panel pin numbering and installed bend-radius confirmation. **Do not release a full assembly order yet.** Resolve those
findings, then mate a sample selected panel with the validated connector and
confirm pin 1, contact side, full insertion, fold and latch closure. Fit the exact protected battery and its keyed
plug in a printed case, then inspect the USB-C body, antenna cable, and lid
closure. On a prototype PCB, measure charge termination while reading,
3.3 V ripple and transient response at low battery, and Wi-Fi performance
with the lid and battery installed. The antenna choice may also require
regional RF compliance testing because its published 2.5 dBi peak gain
exceeds the module datasheet's certified-antenna gain limits. Programming,
screen refresh, SD I/O, and low-battery shutdown still need firmware bring-up.

## Power, charging, and bring-up

- U1 is a [BQ24074 power-path charger](https://www.ti.com/lit/ds/symlink/bq24074.pdf).
  Its BAT pins charge the cell while its separate OUT pins feed the reader.
  EN1 = high and EN2 = low select the 500 mA USB input-current limit.
  R9 = 2.5 kΩ sets about **356 mA** nominal fast-charge current
  (890 AΩ / 2500 Ω). Dynamic power management reduces charging when the
  system uses more of the USB budget. R31 = 10 kΩ holds TS in its valid
  no-thermistor range; the two-wire pack provides no cell temperature signal.
  Charge only within the pack's specified temperature range, and verify the
  pack's allowed rate. Confirm actual current, termination, and thermal
  behavior with and without system load on a prototype. Battery-free operation
  also needs a load test: the 500 mA USB input budget may not cover simultaneous
  Wi-Fi, SD-card, and display peaks.
- SW7 drives U5's EN pin from `SYS_OUT`; it does not carry load current.
  This lets the regulator turn on from either a connected battery or USB.
  S2 remains a firmware-controlled wake button.
- U5 is the [TPS63021 fixed 3.3 V buck-boost
  converter](https://www.ti.com/lit/ds/symlink/tps63021.pdf). L2 is a
  shielded 1.5 µH inductor rated 5 A, with two 10 µF input capacitors and
  three nominal 22 µF/25 V output capacitors close to U5. The converter
  operates from the charger OUT node whether USB is present or not. Check
  the effective ceramic capacitance under DC bias, the switching loop, rail
  ripple, and transient response at the actual Wi-Fi, SD, and display loads.
- R30 pulls ESP32-C3 GPIO8 high on the MCU side of the 20 Ω SPI-clock series
  resistor R27. Closing JP1 pulls GPIO9 low for ROM download mode; GPIO8 must
  remain high through reset. Test programming with the display and SD card
  connected, then open JP1 and confirm normal boot. See the
  [ESP32-C3 boot-mode table](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c3/schematic-checklist.html).
- Measure battery voltage at TP1 and 3.3 V at TP2 during low-state-of-charge
  Wi-Fi transmit, SD writes, and display refresh. Set a firmware low-battery
  shutdown threshold with margin above the battery protection cutoff. This
  repository does not implement that firmware.
