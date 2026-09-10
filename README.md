# ESP32 E-Reader Rev. B

A four-layer tscircuit implementation of the ESP32-C3 e-reader board in
`/home/rushabh/ESP32_E-Reader/Hardware/PCB`.

The design contains 94 components and 53 connected nets. Component placement
and board geometry are transcribed from the Rev. B KiCad design. PCB traces are
generated from the electrical netlist by tscircuit's local autorouter, with the
original per-net 0.2–0.6 mm trace widths retained as routing constraints.
Imported EasyEDA footprints are kept in `imports/`; source-board convention
corrections are applied there where the EasyEDA geometry is mirrored relative
to KiCad.

## Commands

```sh
bun install
bun run typecheck
bun run build:pcb
bun run export:gerbers
```

Useful validation commands:

```sh
bunx tsci check netlist index.circuit.tsx
bunx tsci check schematic-placement index.circuit.tsx
bunx tsci check placement index.circuit.tsx
bunx tsci check shorts index.circuit.tsx
bun run build:release
bun run snapshot
bun run snapshot:update
```

The fabrication archive is written to
`dist/esp32-e-reader-gerbers.zip`. It contains four copper layers,
solder mask, paste, silkscreen, fabrication and edge-cut Gerbers,
plated/non-plated drill files, BOM, and pick-and-place CSVs.

The top, bottom, and inner-1 copper layers have GND fills; inner-2 is the 3.3 V
plane, matching the Rev. B KiCad stackup. The ESP32-C3-WROOM-02 antenna region
has an explicit keepout on all four copper layers.

Trace widths follow the electrical intent of the original Rev. B layout:
0.5 mm for battery, USB power, and 3.3 V distribution; 0.4-0.6 mm for the
pulsed e-paper charge-pump and frontlight boost paths; and 0.2 mm for ordinary
logic. Ground pins use short 0.2 mm escapes into the GND fills. The
original's isolated 0.8-1.0 mm pad expansions are represented by the pours and
the sustained per-net widths because tscircuit currently assigns width per net.

Via drill/pad diameters are constrained to 0.2/0.42 mm, with 0.1 mm
trace-to-pad clearance targeting at least 0.21 mm drill-to-trace spacing.
