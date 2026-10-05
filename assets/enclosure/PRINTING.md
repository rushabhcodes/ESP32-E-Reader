# Rev. B enclosure: dimensioned print prototype

All dimensions below are in **millimetres**. STL files are already in mm scale.
The [print package](esp32-reader-printable-stls.zip) contains all seven case
pieces and this guide.
Use [front-shell.stl](stl/front-shell.stl),
[battery-partition.stl](stl/battery-partition.stl),
[rear-cover.stl](stl/rear-cover.stl), and four individual `button-N.stl` files.
`battery-envelope-DO-NOT-PRINT.stl` and `antenna-envelope-DO-NOT-PRINT.stl` are fit gauges for CAD inspection, not case parts.
The editable source of truth is the parameterized [Blender generator](../../scripts/generate-printable-enclosure.py).

## Coordinate system and stack

The PCB is centered at X = 0, Y = 0 and occupies Z = −0.8 to +0.8.
The screen/front side is negative Z; the component/battery side is positive Z.
The enclosure outside is **68.0 W × 109.5 H × 21.1 T**, X = −34.0 to +34.0,
Y = −49.0 to +60.5, Z = −6.5 to +14.6. Corner radius is 5.0.

| Item | Nominal body / opening | Position or Z span | Source / allowance |
| --- | ---: | --- | --- |
| PCB | 62.5 × 95.08 × 1.6 | X ±31.25; Y −47.0…48.08; Z ±0.8 | tsci `pcb_board`; 0.75 side gap to 64.0 inner case |
| Display panel | 56.24 × 96.62 × 0.9 | center X 0, Y 10.5; Z −4.65…−3.75 | [EastRising panel listing](https://www.buydisplay.com/3-97-inch-quad-color-e-paper-screen-e-ink-display-480x800); FPC omitted |
| Display FPC slot | 26 × 2 | center X 0, Y −36.2 | 1 mm-radius ends; J2 centered at X 0; verify actual panel pinout and fold |
| External Wi-Fi antenna film | 5.9 × 4.1 × 0.24 | center X 25, Y 44; Z 12.86…13.10 | [Taoglas FXP75.07.0045B](https://www.taoglas.com/product/atom-fxp75-2-4ghz-flex-super-micro-pcb-antenna/), 45 mm cable not modeled |
| Display rebate | 56.8 × 97.2 | Z −4.8…−4.1 | 0.28 each side, 0.29 each end; 0.15 front gap for perimeter adhesive |
| Visible screen window | 52.8 × 87.2 | center Y 10.5 | 0.48 each side and 0.4 each end beyond 51.84 × 86.4 active area |
| Front wall | 2.4 deep | Z −6.5…−4.1 | screen lip 1.7 deep after rebate |
| Upper board fasteners | 2 × M2.5 screw paths | X ±27, Y 44.75 | 2.7 PCB holes; 2.0 printed pilot, test screw/material fit |
| Lower board support | 65.0 × 1.2 ledge | Y −46.3; top Z −0.8 | avoids button body Y −44.1…−40.9 |
| BT1 side-entry battery header | 6.0 × 7.7 in model | X 19.05…25.05, Y −36.275…−28.575, Z up to 5.85 | rotated 180° so keyed mating face points −Y into the local partition cutout; [JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) |
| Rigid partition slab | 63.0 × 80.0 × 1.4 | center Y −5.0; Z 4.6…6.0 | rests on side ledges; locally opened around BT1 |
| BT1 and lead opening | 8.0 × 15.0 | center X 22, Y −34 | cutout X 18…26, Y −41.5…−26.5, through slab and right guide |
| Chosen cell: SparkFun PRT-13855 | **49.2 × 68.8 × 5.6**, 2000 mAh | center X −6.2, Y −5; Z 6.0…11.6 | [SparkFun published nominal size](https://www.sparkfun.com/lithium-ion-battery-2ah.html); protected JST-PH pack |
| Battery guide pocket | about 51.1 × 71.5 inner span | X −31.0…20.15; Y −40.6…30.6 | cell X −30.8…18.4, Y −39.4…29.4; right guide opens at BT1 |
| Cell-to-cover clearance | 1.5 above nominal cell | cell top 11.6, cover underside 13.1 | shared by foam, cable/label thickness and cell variation; no guaranteed swelling limit |
| Rear cover | 68.0 × 109.5 × 1.5 | Z 13.1…14.6 | locating tongue 63.4 × 104.9, 0.3 lateral gap in case |
| Rear-cover screws | 4 × M2.5 | lower X ±30, Y −45; upper X ±22, Y +56 | 2.7 cover clearances; 2.0 blind case pilots, 7.0 boss diameter; partition has lower-boss reliefs |
| Four front caps | 9.6 × 4.0 visible each | X −21, −7, +7, +21; Y −42.5 | openings 10.8 × 5.2, 0.6 nominal gap per edge |
| USB-C J1 body | 8.94 wide × 7.35 long × 3.31 high | footprint center X 26.41, Y 36.26 | [GCT USB4105 drawing](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/5492/USB4105.pdf); local manufacturer OBJ checked against case |
| USB-C side opening | 11.0 Y × 7.0 Z | +X edge; Y 30.8…41.8 | 1.03 nominal side clearance about 8.94 connector width; inspect real part |
| MicroSD side opening | 16.0 Y × 7.0 Z | −X edge; Y −26.5…−10.5 | J4 CAD Y −25.42…−11.57 |
| Power switch side opening | 11.0 Y × 7.0 Z | +X edge; Y 8.6…19.6 | SW7 CAD Y 9.605…18.605 |

The cell ends at Y = 29.4. The external antenna film is centered at Y = 44
on the inside rear cover, at least 12.55 mm from the nominal cell envelope
in plan view. Its 45 mm micro-coax reaches U4's first-generation U.FL-compatible
socket in principle; route and secure it against the real PCB and case before
closing the lid. The film is roughly 17 mm behind the display plane, but the
nearby copper, screws, pack, and hand may still detune it. Measure Wi-Fi range
and throughput on an assembled prototype. The battery's right edge is
X = 18.4, 0.65 left of BT1's nominal model body. This narrow clearance and
the unplugged lead path require physical checking.

The 21.1 mm stack is 6.5 mm in front of the PCB center, 6.0 mm from PCB
center to cell base (including the partition), 5.6 mm of nominal cell, 1.5 mm
of clearance, and a 1.5 mm rear cover. The slimmer 1200 mAh Adafruit 258
would save only 0.6 mm at the battery layer while giving 40% less capacity.
The former 2500 mAh Adafruit 328 would add 1.7 mm at that layer and would
need a different cell pocket. The 3.3 V buck-boost converter supports the cell discharge range electrically;
only a measured discharge test can establish usable runtime.

## Assembly and printing

1. Print the shell with its front face on the bed, the cover flat, the partition
   flat, and the caps front-face down. Keep slicer scale at 100%. The booleans
   are modeled as solid, connected, manifold meshes; no supports have been
   validated for a specific printer or material.
2. Put thin, display-compatible perimeter adhesive in the 0.15 deep rebate
   gap and seat the display from the rear without pressing on the active area.
   Verify the FPC tail orientation and bend first. Route the centered tail
   through the PCB slot at X = 0 mm to J2 at X = 0 mm. Inspect the actual
   panel contact face and pin 1 before inserting the tail.
3. Install the four caps from behind, then the PCB on its edge ledges. Use two
   suitable M2.5 screws at the upper mounting holes after measuring pilot-hole
   fit on a printed sample. Do not drive screws into the display.
4. Orient the pack so its lead exits toward the lower-right partition cutout. Plug
   its JST-PH housing into BT1 from the −Y side before seating the partition.
   On this PCB, BT1 pin 1 (`BATT_P`) is at approximately X 21.05 and pin 2
   (`BATT_N_RAW`) at X 23.05; verify polarity at the actual plug. Pass only the
   flexible lead through the opening. Seat the partition on the side
   ledges with the cell guides facing the rear. Keep the lead clear of hard
   edges; add insulation and strain relief suitable for the chosen cable.
5. Place the cell inside the guides without bending or compressing its pouch.
   Place thin, nonconductive cushioning as appropriate for the *measured* pack.
   Attach the Taoglas FXP75 antenna film to the inside rear cover near X = 25,
   Y = 44 mm. With the cover held near the open case, route its 45 mm coax to
   U4 and seat the U.FL-compatible plug without side loading it. Keep the
   cable clear of the lid screws and cell.
   Close the rear cover with four suitable M2.5 screws at the case's end bosses.
   A nominal 6 mm screw enters about 4.5 mm past the 1.5 mm lid. The modeled
   pilot is 4.0 mm deep; confirm pilot diameter and screw depth on a print
   before assembly.

The PCB entries are inventoried in [component-inventory.csv](component-inventory.csv):
PCB footprint size and, where tsci supplies it, the tessellated 3D model's
width, length and Z limits. [component-envelopes.csv](component-envelopes.csv)
contains the raw model boxes. **These are nominal CAD bounds, not certified
manufacturer maximum dimensions.** J1 (USB-C) uses the local manufacturer OBJ
for the inventory and clearance check; JP1 and six test pads have no
body mesh in the exported assembly; the FPC tail, antenna coax/plug, battery lead/connector,
solder fillets, adhesive, and possible battery swelling are also unmodeled.

The selected cell is longer than the former 2500 mAh pack but 1.7 mm thinner.
SparkFun's page lists nominal size only; measure the delivered pack including
its protection board, lead exit and connector before
closing the cover. Its protection circuit is not a substitute for correct
charger settings or battery temperature management. This board's BQ24074 charge setting is approximately 356 mA and it has a
separate power-path output; verify current and termination electrically with
and without the reader operating. Its TS pin uses a fixed 10 kΩ resistor, so
it cannot sense cell temperature.
SparkFun currently states that this pack cannot be shipped internationally
from its store. If purchasing elsewhere, match the complete protected-pack
envelope and verify JST-PH polarity. A local 2000 mAh pack advertised as
68 × 50 × 5 mm is [listed by Fab.to.Lab](https://www.fabtolab.com/power-batteries/Power-sources/batteries/rechargeable-cells/lipo-3.7v-1S),
but its connector and actual protected-pack size need confirmation before
substitution.

## Verification status

Blender's checks in [mesh-check.json](stl/mesh-check.json) report **0 non-manifold
edges and 1 connected shell** for each STL. A triangle-BVH intersection review
in [clearance-check.json](stl/clearance-check.json) against the exported PCB
assembly found only intentional shell/PCB seating contacts and expected
contacts between separate case parts. Boolean solid-overlap volume is zero for
the shell, partition, cover, and nominal battery envelope; no modeled
component or USB-C body shell intersection or cell/shell crossing was found. This does not
verify real cell tolerance, cable bend, fastener fit,
button travel, display attachment, airtightness, RF performance, or print
shrinkage. **Print and measure a prototype before relying on these parts as a
finished enclosure.**

Regenerate using `blender --background --python scripts/generate-printable-enclosure.py`.
Build the circuit and export a 3D GLB before regenerating the component table:
`blender --background --python scripts/export-component-envelopes.py -- /tmp/esp-reader-current.glb`
then `python scripts/build-enclosure-inventory.py`. Recheck fit with
`blender --background --python scripts/check-enclosure-clearance.py -- /tmp/esp-reader-current.glb`.
