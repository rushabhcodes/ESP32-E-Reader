"""Check the installed display GLB against routed PCB/component and case CAD.

Run after export: blender --background --python-exit-code 1 --python
scripts/check-display-connection.py -- /tmp/esp-reader-current.glb
This checks nominal meshes; the delivered flex construction remains unverified.
"""

import json
from pathlib import Path
import sys
from math import pi
import bpy
import bmesh
from mathutils import Matrix, Vector
from importlib import import_module

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
display = import_module("display-flex")
SPEC = display.SPEC
INPUT = Path(sys.argv[sys.argv.index("--") + 1])
circuit = json.loads((ROOT / "dist/index/circuit.json").read_text())
sources = {item["name"]: item["source_component_id"] for item in circuit if item["type"] == "source_component"}
j2 = next(item for item in circuit if item["type"] == "cad_component" and item.get("source_component_id") == sources["J2"])
screen = next(item for item in circuit if item["type"] == "cad_component" and item.get("source_component_id") == sources["EPD1"])
assert j2["position"] == screen["position"], "Screen must follow the actual J2 CAD anchor"
assert abs(j2["position"]["y"] - SPEC["connector"]["centerY"]) < 1e-6
assert abs(j2["position"]["z"] - SPEC["connector"]["boardSurfaceZ"]) < 1e-6
assert j2["rotation"]["z"] == 0


def intersection(a, b):
    test = a.copy()
    test.data = a.data.copy()
    bpy.context.collection.objects.link(test)
    bpy.context.view_layer.objects.active = test
    modifier = test.modifiers.new("overlap", "BOOLEAN")
    modifier.operation = "INTERSECT"
    modifier.solver = "EXACT"
    modifier.object = b
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh = bmesh.new()
    mesh.from_mesh(test.data)
    value = abs(mesh.calc_volume(signed=True))
    mesh.free()
    bpy.data.objects.remove(test, do_unlink=True)
    return round(value, 6)


def prism(name, points, low, high):
    n = len(points)
    verts = [(p["x"], p["y"], z) for z in (low, high) for p in points]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2 * n))]
    faces += [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(mesh)
    bm.free()
    return obj


bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(ROOT / "assets/enclosure/display-panel.glb"))
parts = [obj for obj in set(bpy.data.objects) - before if obj.type == "MESH"]
for obj in parts:
    obj.matrix_world = Matrix.Translation(Vector(tuple(screen["position"][key] for key in ("x", "y", "z")))) @ Matrix.Rotation(-pi / 2, 4, "X") @ obj.matrix_world
panel = next(obj for obj in parts if "nominal-outline" in obj.name)
flex = next(obj for obj in parts if "flex-polyimide" in obj.name)
stiffener = next(obj for obj in parts if "stiffener" in obj.name)
contacts = [obj for obj in parts if "EPD-contact-" in obj.name]
assert len(contacts) == 24, "Missing mating contacts"
panel_points = [panel.matrix_world @ v.co for v in panel.data.vertices]
assert abs(min(p.z for p in panel_points) - SPEC["panel"]["frontZ"]) < 1e-5
assert abs(max(p.z for p in panel_points) - SPEC["panel"]["backZ"]) < 1e-5
path = display.flex_path()
from math import hypot
length = sum(hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))
assert abs(length - SPEC["flex"]["nominalTailLength"]) < SPEC["flex"]["tailLengthTolerance"]
assert abs(max((stiffener.matrix_world @ v.co).y for v in stiffener.data.vertices) - path[-1][0]) < 1e-5
assert all(max((obj.matrix_world @ v.co).z for v in obj.data.vertices) < SPEC["flex"]["entryZ"] for obj in contacts), "Bottom-contact socket needs exposed fingers toward -Z"
for obj in contacts:
    pin = int(obj.name.rsplit("-", 1)[1])
    source_port = next(item for item in circuit if item["type"] == "source_port" and item.get("source_component_id") == sources["J2"] and item.get("pin_number") == pin)
    pcb_port = next(item for item in circuit if item["type"] == "pcb_port" and item.get("source_port_id") == source_port["source_port_id"])
    points = [obj.matrix_world @ v.co for v in obj.data.vertices]
    assert abs((max(p.x for p in points) + min(p.x for p in points)) / 2 - pcb_port["x"]) < .02, f"Contact {pin} reversed or offset"

# Construct the FR-4 solid from the emitted outline and actual routed cutout.
board = next(item for item in circuit if item["type"] == "pcb_board")
pcb = prism("actual-PCB-outline", board["outline"], -board["thickness"] / 2, board["thickness"] / 2)
slot = next(item for item in circuit if item["type"] == "pcb_cutout" and item["shape"] == "polygon")
slot_y = (min(p["y"] for p in slot["points"]) + max(p["y"] for p in slot["points"])) / 2
assert abs(slot_y - SPEC["slot"]["centerY"]) < 1e-6, "Wrong display cutout"
cutter = prism("actual-display-slot", slot["points"], -1, 1)
bpy.context.view_layer.objects.active = pcb
modifier = pcb.modifiers.new("display-slot", "BOOLEAN")
modifier.operation = "DIFFERENCE"
modifier.solver = "EXACT"
modifier.object = cutter
bpy.ops.object.modifier_apply(modifier=modifier.name)
bpy.data.objects.remove(cutter, do_unlink=True)
obstacles = [pcb]
for name in ["front-shell", "battery-partition", "rear-cover", "battery-envelope-DO-NOT-PRINT", *[f"button-{i}" for i in range(1, 5)]]:
    bpy.ops.wm.stl_import(filepath=str(ROOT / "assets/enclosure/stl" / (name + ".stl")))
    obj = bpy.context.object
    obj.name = name
    obstacles.append(obj)

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(INPUT))
pcb_refs = {item["name"] for item in circuit if item["type"] == "source_component" and item["source_component_id"] in {e["source_component_id"] for e in circuit if e["type"] == "pcb_component"}}
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
components = []
for obj in set(bpy.data.objects) - before:
    if obj.type == "MESH" and obj.name in pcb_refs:
        obj.matrix_world = conversion @ obj.matrix_world
        components.append(obj)
connector = next(obj for obj in components if obj.name == "J2")
assert len(connector.data.vertices) > 100, "Missing real connector model"
obstacles += [obj for obj in components if obj != connector]
overlaps = {part.name: {obj.name: value for obj in obstacles if (value := intersection(part, obj)) > 1e-5} for part in (panel, flex, stiffener)}
# Insulating ribbon and stiffener must fit the modeled mating cavity. The
# exposed conductive contact faces intentionally mate with socket contacts.
connector_overlaps = {part.name: intersection(part, connector) for part in (flex, stiffener)}
report = {"nominal_installed_length_mm": round(length, 6), "nominal_tail_length_mm": SPEC["flex"]["nominalTailLength"], "bend_radius_mm": SPEC["flex"]["bendRadius"], "modeled_contacts": len(contacts), "contact_face": "bottom (-Z)", "slot_center_y_mm": slot_y, "connector_center_y_mm": j2["position"]["y"], "solid_overlaps_mm3": overlaps, "connector_insulation_overlaps_mm3": connector_overlaps, "basis": SPEC["basis"]}
(ROOT / "assets/enclosure/stl/display-connection-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
assert not any(overlaps.values()), "Display assembly collision"
assert not any(value > 1e-5 for value in connector_overlaps.values()), "Ribbon does not fit the connector cavity"
