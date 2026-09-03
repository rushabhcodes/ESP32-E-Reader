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
bun run snapshot
bun run snapshot:update
```

The fabrication archive is written to
`dist/esp32-e-reader-gerbers.zip`. It contains four copper layers, solder mask,
paste, silkscreen, fabrication and edge-cut Gerbers, plated/non-plated drill
files, BOM, and pick-and-place CSVs.
