# Rev. B enclosure: dimensioned print prototype

All dimensions below are in **millimetres**. STL files are already in mm scale.
The [print package](esp32-reader-printable-stls.zip) contains all eleven case
pieces and this guide.
Use [front-shell.stl](stl/front-shell.stl),
[battery-partition.stl](stl/battery-partition.stl),
[rear-cover.stl](stl/rear-cover.stl), four individual `button-N.stl` files,
and four `display-retainer-{lower,upper}-{left,right}.stl` sections.
The cushioning and retainer-fastener GLBs represent assembly supplies; do not print them.
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
| Display panel | 56.24 × 96.62 × 0.9 | center X 0, Y 10.5; Z −4.65…−3.75 | [EastRising panel listing](https://www.buydisplay.com/3-97-inch-quad-color-e-paper-screen-e-ink-display-480x800); nominal installed flex included |
| Display FPC slot | 26 × 2 | center X 0, Y −38.41 | 1 mm-radius ends; J2 at X 0, Y −32.34 |
| Display ribbon | 12.5 wide; 0.1 flexible body, 0.3 reinforced tip | nominal 11.316 mm path with 0.6 mm-radius bends | 24-pin 0.5 mm listing basis; actual flex construction and bend limits need a sample |
| External Wi-Fi antenna film | 5.9 × 4.1 × 0.24 | center X 25, Y 44; Z 12.86…13.10 | [Taoglas FXP75.07.0045B](https://www.taoglas.com/product/atom-fxp75-2-4ghz-flex-super-micro-pcb-antenna/), 45 mm cable not modeled |
| Display rebate | 56.8 × 97.2 | Z −4.8…−3.6 | 0.28 each side, 0.29 each end; 0.15 front gap for soft border pads |
| Display retaining frame | four 1.4-thick sections; combined 63.6 × 95 envelope | center Y 10.5; Z −3.25…−1.85 | 15-wide center openings; side gaps Y 41…48.5 clear PCB posts; 1.05 clearance to PCB underside |
| Display border cushioning | 10 front and 10 rear strips: six 1.4 × 10 and four 10 × 1.4 on each face | front Z −4.8…−4.65; rear Z −3.75…−3.25 | rear 0.6 free thickness, nominal 0.5 installed; all strips outside active area |
| Frame screws / hard stops | 6 × M1.6 × 4 countersunk; head ≤3 diameter, 90° | X ±30.1; Y −25, +25, +52; stop top Z −3.25 | 1.8 clearance, 3.2 countersink mouth; 1.25 tap pilots to Z −6.05; screw tip Z −5.85 |
| Visible screen window | 52.8 × 87.2 | center Y 10.5 | 0.48 each side and 0.4 each end beyond 51.84 × 86.4 active area |
| Front wall | 2.4 deep | Z −6.5…−4.1 | screen lip 1.7 deep after rebate |
| Upper board fasteners | 2 × M2.5 screw paths | X ±27, Y 44.75 | 2.7 PCB holes; boss Z −3.55…−0.8, 0.2 clear of nominal glass; 2.0 pilot to Z −3.4 |
| Lower board fasteners | 2 × M2.5 screw paths | X ±28, Y −40.0 | 2.7 PCB holes; 5.6 boss diameter; boss Z −3.65…−0.8; 2.0 pilot to Z −3.45 |
| PCB screws / keepouts | 4 × M2.5 × 4 mm | head ≤5.0 diameter, ≤2.5 high; PCB upper face Z +0.8 | tip Z −3.2; lower pilot gives 0.25 tip clearance; 3.2 radius copper keepout on all four layers |
| Lower board support | 65.0 × 1.2 ledge | Y −46.3; top Z −0.8 | avoids button body Y −44.1…−40.9 |
| BT1 side-entry battery header | 6.0 × 7.7 in model | X 19.05…25.05, Y −36.275…−28.575, Z up to 5.85 | rotated 180° so keyed mating face points −Y into the local partition cutout; [JST PH drawing](https://www.jst-mfg.com/product/pdf/eng/ePH.pdf) |
| Rigid partition slab | 63.0 × 80.0 × 1.4 | center Y −5.0; Z 4.6…6.0 | rests on side ledges; locally opened around BT1 |
| Lower screw access | 3.2 radius notches in partition ledges | centered on lower PCB screws; through ledge Z 3.2…4.6 | clears a 5 mm driver before the partition is installed; lower mounts sit clear of the cover posts; case walls remain intact |
| BT1 and lead opening | 8.0 × 15.0 | center X 22, Y −34 | cutout X 18…26, Y −41.5…−26.5, through slab and right guide |
| Chosen cell: SparkFun PRT-13855 | **49.2 × 68.8 × 5.6**, 2000 mAh | center X −6.2, Y −5; Z 6.0…11.6 | [SparkFun published nominal size](https://www.sparkfun.com/lithium-ion-battery-2ah.html); protected JST-PH pack |
| Battery guide pocket | about 51.1 × 71.5 inner span | X −31.0…20.15; Y −40.6…30.6 | cell X −30.8…18.4, Y −39.4…29.4; right guide opens at BT1 |
| Cell-to-cover clearance | 1.5 above nominal cell | cell top 11.6, cover underside 13.1 | shared by foam, cable/label thickness and cell variation; no guaranteed swelling limit |
| Rear cover | 68.0 × 109.5 × 1.5 | Z 13.1…14.6 | locating tongue 63.4 × 104.9, 0.3 lateral gap in case |
| Rear-cover screws | 4 × M2.5 | lower X ±30, Y −46; upper X ±22, Y +56 | 2.7 cover clearances; 2.0 blind case pilots, 7.0 boss diameter; partition has lower-boss reliefs |
| Four front caps | 9.6 × 4.0 visible each | X −21, −7, +7, +21; Y −42.5 | openings 10.8 × 5.2, 0.6 nominal gap per edge |
| Outer cap flange reliefs | 3.2 radius at lower PCB screw points | only caps at X ±21; flange Z −4.06…−3.65 | 0.4 radial boss clearance; 0.2 nominal stroke leaves 0.2 between cap body and boss underside |
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

1. Print the shell with its front face on the bed, the cover and partition flat,
   the caps front-face down, and all four frame sections pad-side down
   (countersinks facing up). Keep slicer scale at 100%. The booleans
   are modeled as solid, connected, manifold meshes; no supports have been
   validated for a specific printer or material.
   Tap the six nominal 1.25 mm retainer pilots for M1.6 × 0.35 machine screws,
   check screw fit, and clear debris before fitting the glass.
2. Place ten thin, display-compatible nonconductive front pads in the rebate,
   at the border coordinates in [display-retainer.json](display-retainer.json).
   Their installed thickness is 0.15 mm. Seat the display from the rear without
   pressing on the active area. Adhesive may locate pads on the case; the frame
   provides retention without bonding the glass to the shell.
3. Attach the ten rear border pads to the undersides of the frame sections.
   Nominal 0.6 mm free thickness compresses to 0.5 mm when the sections reach
   their hard stops. Use soft, display-compatible nonconductive material and
   measure its actual compression; stiff tape or oversized pads can stress glass.
   Insert each lower section 3.8 mm toward the center and 0.15 mm above its
   installed height, slide it outward below the PCB ledges, then lower it onto
   its stops. For each upper section, enter 10 mm toward the center and 8 mm
   toward the buttons, lower to 0.15 mm above its installed height, slide 8 mm
   toward the top, then 10 mm outward and lower onto its stop. This clears the
   lid posts and PCB posts. Reverse these moves for removal. The shell has
   local 3.6 mm service notches through the ledges for the lower screw drivers.
   Fit six [M1.6 × 4 countersunk screws with 3 mm heads and 90° cones](https://www.accu.co.uk/api/product-datasheet?id=474255).
   Countersunk screw length includes the head. Seat them gently against the
   fixed stops; do not force a section that rocks or needs excess pad compression.
   Screw heads sit flush at Z −1.85 and tips end at −5.85, 0.2 above pilot floors.
   This frame clears the PCB underside by 1.05 mm. Its center openings leave
   the ribbon free and let the sections lift out after removing the PCB.
   Verify the FPC tail orientation and bend first. Route the centered tail
   through the PCB slot at X = 0 mm to J2 at X = 0 mm. Inspect the actual
   panel contact face and pin 1 before inserting the tail. Open J2's flip latch,
   insert the reinforced tip toward +Y with contacts facing the PCB, and close
   the latch. The orange ribbon/blue stiffener model is nominal installation
   geometry under the supplier listing's 0.5 mm pitch assumption. It is not a
   manufacturer flex model; the PDF's conflicting 0.8 mm tip is not reproduced.
   Check the delivered cable width, contact face, 0.3 mm tip thickness and
   permitted bend radius before using this fold.
4. Install the four caps from behind, with the relieved outer flanges facing
   their adjacent lower bosses, then put the PCB on its edge ledges. Secure
   all four PCB mounting holes using M2.5 × 4 mm screws with heads no larger
   than 5 mm diameter and 2.5 mm high. Measure pilot-hole and screw fit on a
   printed sample; the nominal 2.0 mm pilots require a suitable self-tapping
   screw or a tapped pilot for machine screws. A 4 mm shaft ends at Z −3.2,
   0.25 above the lower pilot bottom and 0.2 above the upper pilot bottom.
   Check full button travel before fitting
   the battery partition. Do not use longer PCB screws or drive into the display.
5. Orient the pack so its lead exits toward the lower-right partition cutout. Plug
   its JST-PH housing into BT1 from the −Y side before seating the partition.
   On this PCB, BT1 pin 1 (`BATT_P`) is at approximately X 21.05 and pin 2
   (`BATT_N_RAW`) at X 23.05; verify polarity at the actual plug. Pass only the
   flexible lead through the opening. Seat the partition on the side
   ledges with the cell guides facing the rear. Keep the lead clear of hard
   edges; add insulation and strain relief suitable for the chosen cable.
6. Place the cell inside the guides without bending or compressing its pouch.
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
body mesh in the exported assembly; the antenna coax/plug, battery lead/connector,
solder fillets, adhesive, and possible battery swelling are also unmodeled.
The installed FPC is checked as nominal CAD against the emitted PCB cutout,
connector cavity, component meshes and printed parts with
`scripts/check-display-connection.py`. Sample fit remains necessary.
The frame, installed pads and fastener envelopes are modeled separately.
`scripts/check-display-retainer.py` checks hard-stop seating, pad contact and
active-area exclusion, flush-head clearance, driver access before PCB insertion,
and the section installation paths through the fixed enclosure ledges.

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

Regenerate using `blender --background --python-exit-code 1 --python scripts/generate-printable-enclosure.py`.
Build the circuit, then export all local CAD with
`bun run export:assembly /tmp/esp-reader-current.glb` before regenerating the component table:
`blender --background --python-exit-code 1 --python scripts/export-component-envelopes.py -- /tmp/esp-reader-current.glb`
then `python scripts/build-enclosure-inventory.py`. Recheck fit with
`blender --background --python-exit-code 1 --python scripts/check-enclosure-clearance.py -- /tmp/esp-reader-current.glb`.

Check the nominal display/ribbon assembly against the PCB slot and socket:
`blender --background --python-exit-code 1 --python scripts/check-display-connection.py -- /tmp/esp-reader-current.glb`.

Check the retaining frame and supplies:
`blender --background --python-exit-code 1 --python scripts/check-display-retainer.py -- /tmp/esp-reader-current.glb`.
