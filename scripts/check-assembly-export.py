"""Fail a Gerber export if its BOM or critical pick-and-place rows regress.

SW7 uses the exact JLCPCB C221660 footprint. Its three collinear pads prevent
tscircuit from inferring a pin-1 corner, so the 90-degree placement is checked
explicitly against the C&K JS102011SAQN terminal drawing.
"""

import csv
import io
import json
import re
import sys
from pathlib import Path
from zipfile import ZipFile


EXPECTED = {
    "U1": ("C54313", "top", "0"),
    "U2": ("C7519", "top", "90"),
    "U3": ("C2927799", "top", "90"),
    "U4": ("C2926676", "top", "0"),
    "U5": ("C202140", "top", "0"),
    "L2": ("C133190", "top", "0"),
    "SW2": ("C139797", "bottom", "180"),
    "SW3": ("C139797", "bottom", "180"),
    "SW4": ("C139797", "bottom", "180"),
    "SW6": ("C139797", "bottom", "180"),
    "SW7": ("C221660", "top", "90"),
}

SUPPLIER_FOOTPRINTS = {
    "USBLC6_2SC6.tsx": "C7519",
    "DW01A.tsx": "C2927799",
    "SKRPACE010.tsx": "C139797",
    "JS102011SAQN.tsx": "C221660",
}


def rows_by_designator(archive: ZipFile, filename: str):
    rows = csv.DictReader(io.StringIO(archive.read(filename).decode("utf-8-sig")))
    result = {}
    for row in rows:
        ref = row["Designator"]
        if ref in result:
            raise ValueError(f"Duplicate {ref} in {filename}")
        result[ref] = row
    return result


def main(path: Path):
    imports = Path(__file__).resolve().parents[1] / "imports"
    for filename, part in SUPPLIER_FOOTPRINTS.items():
        if f'footprint="jlcpcb:{part}"' not in (imports / filename).read_text():
            raise ValueError(f"{filename}: expected exact supplier footprint {part}")

    for filename, part in {
        "BQ24074RGTR.tsx": "C54313",
        "ESP32_C3_WROOM_02U_N4.tsx": "C2926676",
        "TPS63021DSJR.tsx": "C202140",
        "SMMS0420_1R5M.tsx": "C133190",
    }.items():
        source = (imports / filename).read_text()
        if part not in source or "<smtpad" not in source:
            raise ValueError(f"{filename}: missing exact supplier footprint for {part}")

    with ZipFile(path) as archive:
        bom = rows_by_designator(archive, "bom.csv")
        placements = rows_by_designator(archive, "pick_and_place.csv")

        drill = archive.read("drill-L1-L4.drl").decode()
        if "METRIC" not in drill:
            raise ValueError("Expected metric drill file")
        drills = [float(size) for size in re.findall(r"^T\d+C([0-9.]+)$", drill, re.M)]
        if not drills or min(drills) < 0.3 - 1e-6:
            raise ValueError("Export contains plated drills below 0.30 mm")
        if not any(abs(size - 0.3) < 1e-6 for size in drills):
            raise ValueError("Export is missing the expected 0.30 mm via tool")

    if bom.keys() != placements.keys():
        raise ValueError("BOM and pick-and-place designators differ")
    missing = [ref for ref, row in bom.items() if not row["JLCPCB Part #"]]
    if missing:
        raise ValueError(f"Missing JLCPCB part numbers: {', '.join(missing)}")

    for ref, (part, layer, rotation) in EXPECTED.items():
        if bom[ref]["JLCPCB Part #"] != part:
            raise ValueError(f"{ref}: expected JLCPCB {part}")
        row = placements[ref]
        if (row["Layer"], row["Rotation"]) != (layer, rotation):
            raise ValueError(f"{ref}: expected {layer} rotation {rotation}°")

    circuit_path = path.parent / "index" / "circuit.json"
    circuit = json.loads(circuit_path.read_text())
    source_names = {
        item["source_component_id"]: item["name"]
        for item in circuit
        if item.get("type") == "source_component"
    }
    # Guard the fabrication settings in the actual routed artifact, not only JSX.
    errors = [item for item in circuit if item["type"].endswith("_error")]
    if errors:
        raise ValueError(f"Circuit has {len(errors)} unresolved errors; do not fabricate")
    vias = [item for item in circuit if item["type"] == "pcb_via"]
    if not vias or not any(item["type"] == "pcb_trace" for item in circuit):
        raise ValueError("Expected a fully routed board with vias")
    for via in vias:
        if via["hole_diameter"] < 0.3 - 1e-6 or via["outer_diameter"] < 0.6 - 1e-6:
            raise ValueError(f"Nonstandard via size: {via}")
        if set(via["layers"]) != {"top", "inner1", "inner2", "bottom"}:
            raise ValueError("Only ordinary through vias are allowed")
    for hole in (item for item in circuit if item["type"] == "pcb_hole"):
        if hole.get("hole_shape") == "circle" and hole["hole_diameter"] < 0.5 - 1e-6:
            raise ValueError("NPTH below JLCPCB 0.50 mm minimum")
    j2 = [item for item in circuit if item["type"] == "pcb_component"
          and source_names.get(item.get("source_component_id")) == "J2"]
    if len(j2) != 1 or abs(j2[0]["center"]["x"]) > 1e-6:
        raise ValueError("J2 must remain centered at X = 0")
    j2_source_id = j2[0]["source_component_id"]
    ground_id = next(item["source_net_id"] for item in circuit
                     if item["type"] == "source_net" and item["name"] == "GND")
    for pin in (6, 7):
        port = next(item for item in circuit if item["type"] == "source_port"
                    and item.get("source_component_id") == j2_source_id
                    and item.get("pin_number") == pin)
        grounded = any(item["type"] == "source_trace"
                       and port["source_port_id"] in item.get("connected_source_port_ids", [])
                       and ground_id in item.get("connected_source_net_ids", [])
                       for item in circuit)
        if port.get("do_not_connect") or not grounded:
            raise ValueError(f"J2 pin {pin} must have its unused sensor input tied to GND")
    print(f"Fabrication sizes checked: {len(vias)} vias at least 0.30/0.60 mm; J2 centered.")

    sw7_ids = {
        item["pcb_component_id"]
        for item in circuit
        if item.get("type") == "pcb_component"
        and source_names.get(item.get("source_component_id")) == "SW7"
    }
    if len(sw7_ids) != 1:
        raise ValueError("Expected exactly one SW7 PCB component")
    sw7_pads = {
        item["port_hints"][0]: item
        for item in circuit
        if item.get("type") == "pcb_smtpad"
        and item.get("pcb_component_id") in sw7_ids
    }
    if set(sw7_pads) != {"pin1", "pin2", "pin3"}:
        raise ValueError("SW7 must have exactly three numbered pads")
    if not all(pad["layer"] == "top" for pad in sw7_pads.values()):
        raise ValueError("SW7 pads must be on the top layer")
    if not (sw7_pads["pin1"]["y"] < sw7_pads["pin2"]["y"] < sw7_pads["pin3"]["y"]):
        raise ValueError("SW7 pad 1 must be below pads 2 and 3")

    print(f"Assembly export checked: {len(bom)} BOM and placement rows; no missing part numbers.")
    print("SW7: C221660 top-side 90° placement and pad-1-down order match the reviewed supplier drawing.")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
