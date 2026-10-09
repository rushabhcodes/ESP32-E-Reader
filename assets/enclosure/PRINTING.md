# Rev. E: two-piece, 16.8 mm snap-fit enclosure

Print **two parts**: `front-chassis` and `rear-cover`. The front chassis includes
all four navigation keys, their independent PETG spring leaves and
six releasable screen clips and four cover latch receivers. The rear cover includes
PCB cantilever bosses, four integral cover snap tabs, battery guides and two
supports for the upper display border. There is no printed tray,
separate bezel, button strip or loose display-retaining frame.

The nominal outside envelope is **68 × 111 × 16.8 mm**, 1.2 mm thinner than
Rev. D's 18.0 mm (6.7%), and reduced from Rev. C's 21.1 mm. The battery is
shifted toward the button end to clear the ESP32 module, allowing the rear
cover to move 1.2 mm closer to the PCB. The screen support, navigation keys,
PCB, component placement and electrical connections are unchanged.
Four side snap tabs replace the cover screws. Print both Rev. E shells together;
the front receivers and rear hooks form a matched pair.
The same protected pack is centered at X −6.0, Y −8.5 mm and attaches to the
rear cover with two nonconductive adhesive strips. The 0.2 mm insulating liner,
0.5 mm adhesive and 1.2 mm rear wall are retained.

Download [the print ZIP](esp32-reader-printable-stls.zip) or import the
[220 × 220 mm 3MF plate](reader-print-plate.3mf). It contains exactly two separate
objects, already oriented, in millimetres at 100% scale. Select your actual
printer and PETG preset. The ZIP also contains the two oriented STLs, this guide
and the geometry specifications and validation reports. No printer-specific G-code is supplied.
Files under `stl/` retain PCB coordinates for inspection. Files marked
`DO-NOT-PRINT` represent gauges, the battery, film or purchased supplies.

## Printing

Working setup: FDM with a 0.4 mm nozzle, PETG, 0.2 mm layers, three walls,
five top/bottom layers and 20% gyroid infill. PETG is required for the integral
key leaves, cover snap tabs and releasable display clips. Both shells print with their flat
outside face on the bed; no enclosure tilting or scaling is required.

Use removable snug supports, including supports that start on the part, at a
45° threshold with a 0.2 mm contact gap. The reference profile enables supports
under bridges. Inspect the six screen leaves, four button leaves, four cover
snap leaves, PCB screw features and seam tongue in the slicer. All those regions are accessible while
the shells are empty. Carefully remove support without cutting the spring
leaves. The battery pocket is open, so no support is trapped in a closed cavity.
Use your printer's calibrated temperature, cooling and speed settings. Follow
its plate instructions for PETG release layers and add a brim if required.

[fdm-reference.ini](fdm-reference.ini) records geometry-check settings; it is not
a calibrated machine preset. Prusa's guides describe [printing tolerances and
orientation](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
and [support placement](https://help.prusa3d.com/article/support-material_1698).
The reference PrusaSlicer 2.9.6 plate uses about **32.2 g of PETG**, including
**1.5 g of support**, with an estimated **3 h 49 min** on the reference profile.
The exact results are recorded in [printability-check.json](stl/printability-check.json).
Actual printer speed and material settings change those estimates. A successful
slice verifies generated toolpaths. Fit, switch force, clip release force and
printed fatigue still require a physical prototype.

## Transparent cover

The actual front and rear GLBs use alpha blending: the smoke-tinted front has
0.38 opacity, and the rear has 0.22 opacity. The hosted tscircuit view and native
export apply 0.5 opacity through the explicit translucency flag on both shells.
These views show the electronics through the enclosure. That visual opacity does not
predict an actual print's optical clarity.

Clear PETG may be used for both parts. Normal FDM layers produce a translucent
cover; it will not look like glass. Keep the PETG flexures if printing the front
in another color. Resin would require separate flexibility and tolerance
validation; the included geometry and slicing checks assume PETG FDM.

## Required nonprinted supplies

- Four M2.5 × 4 mm PCB screws, head diameter ≤5 mm and head height ≤2.5 mm.
  The board clamps against the rear-cover boss underside at Z +0.8. Screws
  enter from the display-facing side, with heads at Z −3.3…−0.8 and tips at
  Z 3.2. Prepare the nominal 2.0 mm pilots before fitting electronics.
- Display-compatible nonconductive cushioning: ten front border pads,
  installed thickness 0.15 mm; six small rear clip pads and two upper support
  pads, installed thickness 0.35 mm. Never place a hard clip on bare glass.
  Locations are recorded in the generator and [enclosure-design.json](enclosure-design.json).
- A 49.4 × 69 × 0.2 mm nonconductive PET or suitable equivalent liner, including
  its thin adhesive, on the PCB-facing battery surface. It is an insulating
  sheet, not a printed part. Keep edges away from connector contacts.
- Two pouch-compatible, nonconductive foam adhesive strips, nominally
  10 × 50 × 0.5 mm, to attach the battery's rear face to the inside cover.
  Use an adhesive suitable for your actual protected pack and PETG. The guides
  locate the pack; adhesive retention must be tested on the real materials.

The case uses **four internal PCB screws**, with **zero cover screws**. Hardware envelopes
are nominal; head shapes, threads, tolerances and printer shrinkage need testing.

## Assembly

1. Print, remove supports, clear/tap PCB screw pilots and inspect both empty shells.
   Dry-fit the cover and release all four tabs through the side windows with
   a plastic pick. The nominal inward release movement is 0.6 mm. Check that
   each tab springs back and its hook engages before installing electronics.
   Check all four integral keys for independent movement and return. Their
   nominal 0.25 mm key stroke includes a 0.04 mm rest gap and about 0.21 mm switch
   compression. A worn key requires replacing the front chassis, which is the
   tradeoff for eliminating separate printed buttons.
2. Fit the ten thin front pads to the screen ledge. Attach the six small pads to
   the undersides of the side clip lips and the two pads to the rear cover's
   upper screen supports. Spread the six side leaf tips outward using plastic
   picks, keeping force on the clips rather than the display. The CAD release
   check uses 1.0 mm lateral tip movement. Lower the panel straight into its
   rebate, then release the clips gently. They bear only on the padded border.
   Stop if the panel cannot seat or any clip presses its active area.
3. With the PCB removed, dry-fit the battery loading path. Enter through the
   open upper end of the guides with the pack centered at X −6.0, Y −2.0.
   Lift it toward the lid, leaving 0.1 mm stand-off, then slide it 6.5 mm toward
   the lower stop to Y −8.5. This passes above the lower PCB mounting bosses.
   Apply the insulating liner to the PCB-facing pack surface and use the two
   adhesive strips with accessible release pull tabs. Leave their release film
   in place while locating the pack; peel and bond once it is in position.
   Verify the real adhesive, release-film thickness and pull-tab access during
   the dry fit. Do not squeeze or bend the pouch to complete the loading path.
   The nominal 49.2 × 68.8 × 5.6 mm protected pack is centered at X −6.0,
   Y −8.5; its PCB-facing surface is Z 3.7. Guides allow 0.2 mm nominal edge
   clearance. Verify the complete pack envelope, labels, lead and adhesive fit.
4. Attach the antenna film near X 25, Y 44 on the rear cover. Seat the PCB
   straight into the rear cover from its open display-facing side, against the
   four cantilever bosses at Z +0.8. Fit the four M2.5 × 4 screws from the
   PCB underside. This leaves access to the pilots and avoids posts crossing
   the glass insertion path.
5. Bring the two loaded halves together without tension on the display tail.
   Feed the panel tail through the PCB slot. Open J2's latch, insert the tail
   with contacts toward the PCB, then close it. J2 remains the selected 24-pin,
   0.5 mm Hirose connector. Confirm the delivered panel's pin 1, contact side,
   stiffener and permitted fold radius; the installed ribbon model is nominal.
   Connect the battery to BT1: pin 1 `BATT_P` is near X 21.05, pin 2
   `BATT_N_RAW` near X 23.05. Confirm actual keyed plug polarity. Route the
   battery lead through the guide notch and antenna coax to U4 without trapping
   either. Real cable slack and installation access need a physical sample.
6. Lower the loaded rear cover and attached PCB straight onto the front chassis.
   Its two upper support columns pass beyond the PCB and cushion the top
   screen border. Align the seam, then press at each latch location until all
   four hooks engage. The tongue sets alignment and the perimeter seam sets
   closure depth. Do not force a lid over a trapped wire or pack.

To open the cover, press the recessed hooks inward through the four side
windows with a plastic pick. Keep the first pair released while releasing the
other pair, then lift the loaded rear cover straight. Avoid twisting the screen
or pulling on the ribbon.

For screen service, disconnect the display tail and remove the loaded rear cover, then release the six screen clips. No loose retaining frame needs dismantling.

## Geometry and validation

The PCB origin is retained: screen/front is negative Z, battery/rear positive Z.

| Feature | Nominal dimensions / position |
| --- | --- |
| Outside | 68 × 111 × 16.8; X ±34, Y −50.5…60.5, Z −5.8…11.0; radius 5 |
| Front display ledge | Floor Z −4.8, 1.0 mm minimum front material; ten 0.15 mm pads |
| Panel / visible window | 56.24 × 96.62 × 0.9 / 52.8 × 87.2; center Y 10.5 |
| Screen pocket | 56.8 × 97.2; 0.28/0.29 mm nominal edge clearance |
| Side clips | Six; tip Y −27, 3, 27; 14 mm spring leaves; padded face Z −3.4 |
| Upper rear supports | X ±12, Y 55.4; padded face Z −3.4, beyond the PCB outline |
| PCB | 62.5 × 95.08 × 1.6; Z ±0.8; four original mount positions |
| Shell seam | Z 5.4; 0.2 mm side tongue clearance and 0.3 mm end clearance |
| Rear outside face | Z 11.0; 1.2 mm flat cover, with four integral snap leaves |
| Battery stack | 0.2 mm liner at Z 3.5…3.7; cell at 3.7…9.3; 0.5 mm adhesive to Z 9.8 |
| Guides | 0.8 mm; side X −31.2/19.2; lower stop Y −43.5; upper loading end open |
| Cover snaps | Four; sides X ±32.6, tip Y −5/24; 14 mm beams, 0.8 mm thick |
| Snap engagement / release | 0.4 mm radial engagement; 0.2 mm vertical play; 0.6 mm inward release |
| Snap receivers | 0.8 mm retaining walls; accessible 6 × 1.5 mm side windows |
| USB/SD/switch access | Front-wall openings reach the seam to clear the attached PCB at closure |

The lower PCB mounting bosses set this revision's height limit. The liner
has 0.25 mm nominal clearance above their Z 3.25 tops and about 0.59 mm above
L1, the tallest electronic body under the shifted battery. Its edge is 1.63 mm
below the ESP32 module in Y. During loading, the 0.1 mm lid stand-off leaves
0.15 mm nominal clearance over the lower bosses.
The same battery capacity and insulation are retained. Confirm the actual pack
thickness and clearance on a prototype, including any swelling allowance;
do not force closure onto the pack. Actual battery cables, antenna coax,
printed shrinkage, adhesive strength and flexure fatigue are not simulated.
The snap checks verify hook retention, geometric release, and sampled closing
and opening paths. They do not predict snap force or cycle life.

Regenerate and verify using:

```sh
blender --background --python-exit-code 1 --python scripts/generate-printable-enclosure.py
bun run build
bun run export:assembly
blender --background --python-exit-code 1 --python scripts/check-enclosure-clearance.py -- dist/index/assembly.glb
blender --background --python-exit-code 1 --python scripts/check-display-connection.py -- dist/index/assembly.glb
python3 scripts/check-printability.py /path/to/prusa-slicer
blender --background --python-exit-code 1 --python scripts/render-printable-enclosure.py
```

Generated reports under `stl/` record mesh integrity, nominal clearances,
independent key strokes, sampled screen/PCB/battery/cover assembly paths,
CAD transparency and slicer output. The source still contains the original
supplier STEP models; the hosted STEP archives ([1](../components/supplier-step-models-1.zip), [2](../components/supplier-step-models-2.zip), [3](../components/supplier-step-models-3.zip), [4](../components/supplier-step-models-4.zip), [5](../components/supplier-step-models-5.zip))
preserve them without loading large STEP duplicates in the browser preview.
