"""Fail a Gerber export if its BOM or critical pick-and-place rows regress.

SW7 uses the exact JLCPCB C431541 footprint. Check its asymmetric contact
spacing, four grounded case feet, locator holes, and side-facing placement
against the SHOU HAN MSK12C02-HB supplier drawing.
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
    "J2": ("C324726", "top", "0"),
    "L1": ("C133195", "top", "270"),
    "L2": ("C133190", "top", "0"),
    "SW2": ("C139797", "bottom", "180"),
    "SW3": ("C139797", "bottom", "180"),
    "SW4": ("C139797", "bottom", "180"),
    "SW6": ("C139797", "bottom", "180"),
    "SW7": ("C431541", "top", "90"),
}

SUPPLIER_FOOTPRINTS = {
    "USBLC6_2SC6.tsx": "C7519",
    "DW01A.tsx": "C2927799",
    "SKRPACE010.tsx": "C139797",
    "MSK12C02_HB.tsx": "C431541",
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
    spec = json.loads((imports.parent / "assets/enclosure/display-connection.json").read_text())
    if len(j2) != 1 or any(abs(j2[0]["center"][axis] - spec["connector"]["center" + axis.upper()]) > 1e-6 for axis in ("x", "y")):
        raise ValueError("J2 must match the Waveshare L-tail connector position")
    if j2[0].get("pin1_location") != "topside_right":
        raise ValueError("J2 pin 1 must match the canonical FH34SRJ footprint")
    j2_source_id = j2[0]["source_component_id"]
    for pin in (1, 4, 6, 7, 19):
        port = next(item for item in circuit if item["type"] == "source_port"
                    and item.get("source_component_id") == j2_source_id
                    and item.get("pin_number") == pin)
        connected = any(item["type"] == "source_trace"
                        and port["source_port_id"] in item.get("connected_source_port_ids", [])
                        for item in circuit)
        if not port.get("do_not_connect") or connected:
            raise ValueError(f"Waveshare J2 pin {pin} must be left open")
    print(f"Fabrication sizes checked: {len(vias)} vias at least 0.30/0.60 mm; Waveshare connector/NC pins checked.")

    sw7_ids = {
        item["pcb_component_id"]
        for item in circuit
        if item.get("type") == "pcb_component"
        and source_names.get(item.get("source_component_id")) == "SW7"
    }
    if len(sw7_ids) != 1:
        raise ValueError("Expected exactly one SW7 PCB component")
    all_sw7_pads = [
        item for item in circuit
        if item.get("type") == "pcb_smtpad"
        and item.get("pcb_component_id") in sw7_ids
    ]
    contacts = {item["port_hints"][0]: item for item in all_sw7_pads
                if item["port_hints"][0] in {"pin1", "pin2", "pin3"}}
    case_pads = [item for item in all_sw7_pads if "pin4" in item["port_hints"]]
    if len(all_sw7_pads) != 7 or len(contacts) != 3 or len(case_pads) != 4:
        raise ValueError("SW7 needs three contact pads and four metal-case solder feet")
    pcb_ports = {item["pcb_port_id"]: item for item in circuit if item["type"] == "pcb_port"}
    source_ports = {item["source_port_id"]: item for item in circuit if item["type"] == "source_port"}
    for pad in all_sw7_pads:
        port = pcb_ports.get(pad.get("pcb_port_id"))
        if port is None:
            raise ValueError("SW7 pad is not bound to an electrical PCB port")
        physical_pin = int(pad["port_hints"][0].removeprefix("pin"))
        if f"pin{physical_pin}" not in source_ports[port["source_port_id"]]["port_hints"]:
            raise ValueError("SW7 pad maps to the wrong schematic pin")
    if not all(pad["layer"] == "top" for pad in all_sw7_pads):
        raise ValueError("SW7 pads must be on the top layer")
    if not (contacts["pin1"]["y"] < contacts["pin2"]["y"] < contacts["pin3"]["y"]):
        raise ValueError("SW7 pad 1 must be below pads 2 and 3")
    for a, b, pitch in [("pin1", "pin2", 3.0), ("pin2", "pin3", 1.5)]:
        if abs(contacts[b]["y"] - contacts[a]["y"] - pitch) > 0.01:
            raise ValueError(f"SW7 {a}/{b} contact spacing must be {pitch} mm")
        if abs(contacts[b]["x"] - contacts[a]["x"]) > 0.001:
            raise ValueError("SW7 contacts must remain collinear")
    sw7_source_id = next(item["source_component_id"] for item in circuit
                         if item["type"] == "source_component" and item["name"] == "SW7")
    expected_nets = {1: "SYS_OUT", 2: "POWER_ENABLE", 3: "POWER_OFF_PULLDOWN", 4: "GND"}
    net_ids = {item["name"]: item["source_net_id"] for item in circuit
               if item["type"] == "source_net"}
    for pin, net in expected_nets.items():
        port_id = next(item["source_port_id"] for item in circuit
                       if item["type"] == "source_port"
                       and item["source_component_id"] == sw7_source_id
                       and item["pin_number"] == pin
                       and item["name"] == {1: "ON", 2: "COM", 3: "OFF", 4: "CASE"}[pin])
        if not any(item["type"] == "source_trace"
                   and port_id in item.get("connected_source_port_ids", [])
                   and net_ids[net] in item.get("connected_source_net_ids", [])
                   for item in circuit):
            raise ValueError(f"SW7 pin {pin} must connect to {net}")
    # The supplier's four case feet get separate PCB ports with internal ties.
    parent = {}
    def connected_group(identity):
        parent.setdefault(identity, identity)
        if parent[identity] != identity:
            parent[identity] = connected_group(parent[identity])
        return parent[identity]
    groups = [item.get("connected_source_port_ids", []) + item.get("connected_source_net_ids", [])
              for item in circuit if item["type"] == "source_trace"]
    groups += [group for item in circuit if item["type"] == "source_component"
               for group in item.get("internally_connected_source_port_ids", [])]
    for members in groups:
        for member in members[1:]:
            parent[connected_group(member)] = connected_group(members[0])
    for pad in all_sw7_pads:
        pin = int(pad["port_hints"][0].removeprefix("pin"))
        source_port = pcb_ports[pad["pcb_port_id"]]["source_port_id"]
        if connected_group(source_port) != connected_group(net_ids[expected_nets[pin]]):
            raise ValueError(f"SW7 pad {pin} is not electrically tied to {expected_nets[pin]}")
    locator_holes = [item for item in circuit if item["type"] == "pcb_hole"
                     and item.get("pcb_component_id") in sw7_ids]
    if len(locator_holes) != 2 or any(abs(item["hole_diameter"] - 0.9) > 0.01
                                     for item in locator_holes):
        raise ValueError("SW7 needs the supplier's two 0.9 mm locator holes")

    print(f"Assembly export checked: {len(bom)} BOM and placement rows; no missing part numbers.")
    print("SW7: C431541 top-side 90°, asymmetric contacts, grounded case feet, and locator holes verified.")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
