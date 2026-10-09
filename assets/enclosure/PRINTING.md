# Rev. C: five-piece printable reader enclosure

Print **five parts**: front bezel, main body, battery tray, rear cover and one
connected button strip. Rev. B used eleven pieces. The main body now includes
the display retaining frame; the battery guides and removable side-port roofs
are part of the rear cover.
The compact Alps navigation switches and PCB layout are unchanged.

Download [the complete print ZIP](esp32-reader-printable-stls.zip), or import
[the 220 × 220 mm print plate](reader-print-plate.3mf). The 3MF contains five
separate objects already oriented on the bed, in millimetres, at 100% scale.
It contains geometry only: **select your actual printer and PETG filament
preset before slicing**. Printer-specific G-code is deliberately not supplied.
The ZIP's five STLs are bed-oriented. The repository's separate `stl/`
directory retains PCB coordinates for CAD inspection.
All `DO-NOT-PRINT` files and the cushioning/fastener GLBs are inspection models.

## Print setup

Working assumption: FDM, 0.4 mm nozzle. Use PETG for the button strip's flexible
arms; the three case pieces and tray can use PETG as well. Start with 0.2 mm
layers, three walls, five top/bottom layers and 20% gyroid infill. The strip's
0.8 mm arms are four layers thick at this setting. Use your filament's tested
printer preset for temperature, cooling and speed. A smooth plate may need a
release layer for PETG; follow your plate manufacturer's instructions.

| Part | Bed-oriented file | Orientation | Supports |
| --- | --- | --- | --- |
| Front bezel | [front-bezel.stl](print/front-bezel.stl) | Outside/front face down | Inspect pilot and pocket features in preview |
| Main body with screen retainer | [main-body.stl](print/main-body.stl) | Flat display-retainer face down | Side ports are open to the rear for board installation |
| Battery tray | [battery-partition.stl](print/battery-partition.stl) | Flat battery-contact face down; four feet up | No guides under the flat slab |
| Rear cover with battery guides | [rear-cover.stl](print/rear-cover.stl) | Outside face down; guides and port roofs up | Small generated supports may appear near tongue/guide junctions |
| Connected button strip | [button-strip.stl](print/button-strip.stl) | Four key faces down | Enable removable build-plate supports below the raised rail/arms |

[fdm-reference.ini](fdm-reference.ini) records the geometry-check settings:
0.4 mm nozzle, 0.2 mm layers, snug build-plate supports, 45° threshold,
0.2 mm support contact gap, and bridge support disabled. Inspect support
interfaces below the small strip; remove them without cutting its arms.
Add a brim if your printer needs it. On a smaller bed, print the individual
STLs instead of scaling the plate down.

This approach follows Prusa's guidance on [orientation, wall thickness and
print tolerances](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)
and [support placement](https://help.prusa3d.com/article/support-material_1698).
Slicing verifies toolpaths, not the fit or durability of an actual print.

## Hardware and cushioning

- Six M1.6 × 4 mm countersunk screws, head diameter ≤3 mm, 90° head, to attach
  the front bezel to the body. Nominal 1.25 mm pilots must be cleared and tapped
  M1.6 × 0.35 **before installing the display**. Countersunk length includes
  the head. [Specified screw dimensions](https://www.accu.co.uk/api/product-datasheet?id=474255).
- Four M2.5 × 4 mm PCB screws, head diameter ≤5 mm, height ≤2.5 mm. The body's
  nominal 2 mm pilots are through holes; prepare suitable M2.5 threads and
  remove debris. A 4 mm shaft ends at Z −3.2, behind the glass. Do not use
  longer PCB screws.
- Two M2.5 × 6 mm countersunk rear-cover screws, 90° head, diameter ≤5 mm.
  Cover clearance is 2.7 mm; countersink mouth is 5.2 mm. The body pilot floor
  is Z 8.1; the installed screw tip is 8.6, leaving 0.5 mm nominal clearance.
  Two M1.6 × 4 mm countersunk screws (same type as the bezel) secure the lower
  cover at X ±21, Y −48.9. These pilots end at Z 10.1; tips at 10.6 leave
  0.5 mm clearance. The narrow posts sit outside the board insertion envelope.
- Ten front and ten rear strips of soft, display-compatible, nonconductive
  cushioning. Front installed thickness is 0.15 mm; rear free thickness is
  nominally 0.6 mm, compressed to 0.5 mm at the hard stops. Coordinates and
  dimensions are in [display-retainer.json](display-retainer.json).
- Thin nonconductive battery cushioning/adhesive appropriate to the measured
  protected cell. Keep the pack secured without squeezing or bending it.

Tap/drill and test the empty printed case first. Screw pilots, flexible-arm
force, lid fit, shrinkage and elephant foot need a prototype. Relieve a tight
fit gradually; do not force the display, PCB or battery into an undersized print.

## Assembly

1. Remove supports and inspect the five parts. Check each button independently
   before fitting electronics. Place the strip into the bezel's four openings;
   its long rail and four roots seat in the shallow lower pockets. The rail is
   captured when the body meets the bezel. The flexible arms remain free.
2. Put the ten thin front pads in the display rebate, then place the raw panel
   without pressing its active area. Attach the ten rear pads to the body's
   integral retainer at the matching border coordinates. Place the body over
   the bezel straight along Z. Seat its six fixed stops and fit the six M1.6
   screws from the rear, before fitting the PCB. Stop if it rocks or requires
   excessive force; pad softness and actual compression are not simulated.
3. Lower the PCB into the open rear. Four bosses align with its four mounting
   holes; there are no fixed tray ledges obstructing this
   path; the lower cover posts sit beyond the board edge. Feed the centered display tail through the PCB slot before seating
   the board. Secure the PCB with four M2.5 × 4 screws. Check all four buttons
   for return and independent actuation.
4. Connect the display to J2 at X 0, Y −32.34. Open the FH12 latch, insert the
   reinforced tip toward +Y with exposed contacts toward the PCB, and close
   it. The installed orange/blue CAD ribbon uses the supplier listing's
   24-pin, 0.5 mm pitch assumption selected for this project. Check the actual
   panel contact face, pin 1, 0.3 mm reinforced tip and allowed bend radius.
   The nominal 0.6 mm bends are not a manufacturer-approved fold specification.
5. Connect the protected battery to BT1 from its −Y side. Verify plug polarity:
   PCB pin 1 `BATT_P` is near X 21.05, pin 2 `BATT_N_RAW` near X 23.05.
   Lower the tray over the installed PCB screws: four hollow feet surround
   their heads and land on FR-4 at the mounting-hole borders. The tray's lower
   right opening clears BT1 and its flexible lead. Keep wires off hard edges.
6. Place the nominal 49.2 × 68.8 × 5.6 mm cell at X −6.2, Y −5, on the tray.
   The rear cover's guides locate its sides when closed. Use suitable thin
   cushioning/adhesive to retain the measured cell; the nominal 1.5 mm gap above
   it is shared by tolerances, labels, wiring and cushioning.
7. Attach the Taoglas antenna film to the inside rear cover near X 25, Y 44.
   Route its 45 mm coax to U4 without loading the connector or trapping it.
   Lower the cover straight into the body; its three port roofs fit between
   the open side-wall edges and its guides surround the cell. Fit the two upper
   countersunk M2.5 screws and two lower countersunk M1.6 screws. Do not press a cover
   closed over a cable or a cell that does not fit.

To service the screen, remove the cover, battery/tray, disconnect the FPC and
remove the PCB. Remove six bezel screws; the bezel and body separate directly.
No loose perimeter frame sections or complicated sliding insertion remain.

## Nominal geometry

Coordinates below retain the PCB origin; screen/front is negative Z.
The PCB occupies Z −0.8…+0.8. Dimensions are millimetres.

| Feature | Size / position |
| --- | --- |
| Outside case | 68 × 111 × 21.1; X ±34, Y −50.5…60.5, Z −6.5…14.6; corner radius 5 |
| Bezel/body joint | Z −3.25; six border hard stops set the rear cushioning gap |
| Raw display | 56.24 × 96.62 × 0.9, center Y 10.5, Z −4.65…−3.75 |
| Display rebate | 56.8 × 97.2; floor Z −4.8; nominal lateral gaps 0.28/0.29 |
| Active area / visible window | 51.84 × 86.4 / 52.8 × 87.2, center Y 10.5 |
| Integral display retainer | 1.4 thick, Z −3.25…−1.85; PCB underside clearance 1.05 |
| Bezel screws | X ±30.1; Y −25, 25, 52; M1.6 × 4; pilot floor −6.05 |
| PCB | 62.5 × 95.08 × 1.6; four unchanged 2.7 mounting holes |
| PCB mounts | X ±27, Y 44.75; X ±28, Y −40; support Z −0.8; through pilots 2 |
| Display slot / J2 | Slot 26 × 2, Y −38.41; J2 24 × 0.5 pitch, Y −32.34 |
| Installed display flex | 12.5 wide; 0.1 body, 0.3 reinforced tip; nominal path 11.316 long |
| Battery tray | Main slab 63 × 80 × 1.4 at Y −5, Z 4.6…6; upper mounting arms added |
| Tray feet | Four 7 diameter sleeves, 5.4 head cavities; seat on PCB top Z 0.8 |
| Chosen battery envelope | SparkFun PRT-13855, 49.2 × 68.8 × 5.6, X −6.2, Y −5, Z 6…11.6 |
| Rear cover | 1.5 thick at Z 13.1…14.6; 0.3 lateral locating-tongue clearance |
| Cover guides | 0.8 thick; Z 6.3…13.1; left/right X −31.4/20.4; ends Y −40.9/30.9 |
| Cover closure | Two M2.5 screws at X ±22, Y 56; two M1.6 screws at X ±21, Y −48.9 |
| Visible keys | Four 9.6 × 4; X −21, −7, 7, 21, Y −42.5; nominal movement +0.2 Z |
| Button-strip arms | Four approximately 10.4-long, 0.8-wide, 0.8-thick leaves; common rail 54 × 0.8 × 0.8 |
| USB-C opening | +X wall, Y 30.8…41.8; 11 Y × 7 Z |
| MicroSD opening | −X wall, Y −26.5…−10.5; 16 Y × 7 Z |
| Power-switch opening | +X wall, Y 8.6…19.6; 11 Y × 7 Z |

Panel dimensions follow [EastRising's listing](https://www.buydisplay.com/3-97-inch-quad-color-e-paper-screen-e-ink-display-480x800).
Battery size follows [SparkFun's nominal specification](https://www.sparkfun.com/lithium-ion-battery-2ah.html).
Antenna dimensions follow [Taoglas FXP75](https://www.taoglas.com/product/atom-fxp75-2-4ghz-flex-super-micro-pcb-antenna/).
Actual flex construction, protected-cell envelope and antenna cable routing
still require delivered parts. The charger uses a fixed TS resistor and cannot
measure cell temperature; electrical verification remains separate from case fit.

The guides have nominal 0.2 mm clearance to the left cell edge and case wall,
and 0.3 mm clearance above the tray. The lower lip is 1.5 mm longer than Rev. B to keep the small cover posts
outside the unchanged board. The port roofs now lift off with the cover, so
connectors pass through the open wall slots during PCB installation.

## Model loading and checks

The sixteen imported electronic component models are now checked-in OBJ/STEP
assets with their original source URLs and SHA-256 checksums in
[components/sources.json](../components/sources.json). All local CAD, print
files and previews are copied into the hosted release. PCB screws, cover
screws, bezel screws, display pads, panel, flex and the five case parts have
separate native 3D assembly entries. PCB-only test pads do not need body meshes.
Antenna coax/plug, the battery's real lead/plug, solder fillets, material
shrinkage and cell swelling remain unmodeled.

[mesh-check.json](stl/mesh-check.json) checks one connected, manifold solid per
part. [clearance-check.json](stl/clearance-check.json) checks component/USB/body
clearance, screw access and independent button travel. [assembly-check.json](stl/assembly-check.json) verifies native model presence,
tray seating and sampled straight PCB/tray/cover insertion paths.
[printability-check.json](stl/printability-check.json) records the reference
PrusaSlicer run for all five STLs and the complete plate. The display checks
cover border-pad contact, fixed stops, ribbon/contact orientation and nominal
installation geometry. These checks do not establish physical button force,
fatigue life, thread strength, glass loading or drop resistance. Print a
prototype and measure the fit before relying on it as a finished enclosure.

Regeneration was checked with Blender 5.1.2 (Manifold boolean solver) and
PrusaSlicer 2.9.6. Regenerate and check:

```sh
blender --background --python-exit-code 1 --python scripts/generate-printable-enclosure.py
bun run build
bun run export:assembly /tmp/esp-reader-current.glb
blender --background --python-exit-code 1 --python scripts/check-enclosure-clearance.py -- /tmp/esp-reader-current.glb
blender --background --python-exit-code 1 --python scripts/check-display-connection.py -- /tmp/esp-reader-current.glb
blender --background --python-exit-code 1 --python scripts/check-display-retainer.py -- /tmp/esp-reader-current.glb
blender --background --python-exit-code 1 --python scripts/check-enclosure-assembly.py -- /tmp/esp-reader-current.glb
python3 scripts/check-printability.py /path/to/prusa-slicer
blender --background --python-exit-code 1 --python scripts/render-printable-enclosure.py
```
