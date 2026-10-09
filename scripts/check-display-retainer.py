"""Check exported display mounting meshes, pad contact and installation paths.

Run after build/export: blender --background --python-exit-code 1 --python
scripts/check-display-retainer.py -- /tmp/esp-reader-current.glb
Checks nominal geometry, not pad force, thread strength or drop resistance.
"""

import json
import math
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
STL = ROOT / "assets/enclosure/stl"
SPEC = json.loads((ROOT / "assets/enclosure/display-retainer.json").read_text())
DISPLAY = json.loads((ROOT / "assets/enclosure/display-connection.json").read_text())
MOUNTS = json.loads((ROOT / "assets/enclosure/pcb-mounts.json").read_text())
INPUT = Path(sys.argv[sys.argv.index("--") + 1])
FRAME, SCREWS = SPEC["frame"], SPEC["fasteners"]
EPS = 1e-4
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)


def bounds(obj):
    points = [obj.matrix_world @ Vector(p) for p in obj.bound_box]
    return [(min(p[i] for p in points), max(p[i] for p in points)) for i in range(3)]


def overlap(a, b):
    if any(min(q[1], r[1]) - max(q[0], r[0]) < 1e-5
           for q, r in zip(bounds(a), bounds(b))):
        return 0.0
    test = a.copy()
    test.data = a.data.copy()
    bpy.context.collection.objects.link(test)
    bpy.context.view_layer.objects.active = test
    mod = test.modifiers.new("solid-overlap", "BOOLEAN")
    mod.operation, mod.solver, mod.object = "INTERSECT", "EXACT", b
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bm = bmesh.new()
    bm.from_mesh(test.data)
    value = round(abs(bm.calc_volume(signed=True)), 6)
    bm.free()
    bpy.data.objects.remove(test, do_unlink=True)
    return value


def tree(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.transform(obj.matrix_world)
    result = BVHTree.FromBMesh(bm)
    bm.free()
    return result


def hit_z(obj, x, y, z, direction):
    point, *_ = tree(obj).ray_cast(Vector((x, y, z)), Vector((0, 0, direction)))
    return round(point.z, 5) if point is not None else None


def near(actual, expected):
    return actual is not None and abs(actual - expected) < 2e-5


def stl(name):
    bpy.ops.wm.stl_import(filepath=str(STL / (name + ".stl")))
    obj = bpy.context.object
    obj.name = name
    return obj


def glb(filename, translation=(0, 0, 0)):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(ROOT / "assets/enclosure" / filename))
    objects = [obj for obj in set(bpy.data.objects) - before if obj.type == "MESH"]
    for obj in objects:
        obj.matrix_world = Matrix.Translation(Vector(translation)) @ Matrix.Rotation(-math.pi / 2, 4, "X") @ obj.matrix_world
    return objects


shell = stl("front-bezel")
frames = [stl("main-body")]
case_parts = [stl(name) for name in ("battery-partition", "rear-cover", "battery-envelope-DO-NOT-PRINT")]
buttons = [stl(f"button-{i}-DO-NOT-PRINT") for i in range(1, 5)]
pads = glb("display-cushioning.glb")
fasteners = glb("display-retainer-fasteners.glb")
display_parts = glb("display-panel.glb", (0, DISPLAY["connector"]["centerY"], DISPLAY["connector"]["boardSurfaceZ"]))
panel = next(obj for obj in display_parts if "nominal-outline" in obj.name)
rear_pads = [obj for obj in pads if "rear-pad" in obj.name]
assert len(pads) == 20 and len(rear_pads) == 10 and len(fasteners) == 6

circuit = json.loads((ROOT / "dist/index/circuit.json").read_text())
pcb_sources = {item["source_component_id"] for item in circuit if item["type"] == "pcb_component"}
pcb_refs = {item["name"] for item in circuit if item["type"] == "source_component" and item["source_component_id"] in pcb_sources}
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(INPUT))
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
components = []
published_frames = []
for obj in set(bpy.data.objects) - before:
    if obj.type != "MESH":
        continue
    obj.matrix_world = conversion @ obj.matrix_world
    if obj.name in pcb_refs or obj.name in ("Box0", "MeshWithTextures0"):
        components.append(obj)
    if obj.name == "main_body":
        published_frames.append(obj)
assert len(published_frames) == 1, "Missing retaining frame in the circuit assembly"
for part in frames:
    emitted = next(obj for obj in published_frames if obj.name == part.name.replace("-", "_"))
    assert len(emitted.data.vertices) > 50, "Fallback frame mesh"
    assert all(abs(a - b) < .001 for q, r in zip(bounds(part), bounds(emitted)) for a, b in zip(q, r)), "Assembly frame transform mismatch"

obstacles = [shell, *case_parts, *buttons, *display_parts, *components]
collisions = {part.name: {obj.name: v for obj in obstacles if (v := overlap(part, obj)) > EPS} for part in frames}
for button in buttons:
    button.location.z += MOUNTS["buttonTravel"]
    bpy.context.view_layer.update()
    for part in frames:
        if (v := overlap(part, button)) > EPS:
            collisions[part.name][button.name + "-pressed"] = v
    button.location.z -= MOUNTS["buttonTravel"]
bpy.context.view_layer.update()
assert not any(collisions.values()), f"Frame collision: {collisions}"

contacts = []
for pad in pads:
    b = bounds(pad)
    x, y = (sum(b[i]) / 2 for i in (0, 1))
    # Guard against pads crossing the actual 51.84 x 86.4 active rectangle.
    outside_active = (b[0][1] <= -25.92 or b[0][0] >= 25.92
                      or b[1][1] <= DISPLAY["panel"]["centerY"] - 43.2
                      or b[1][0] >= DISPLAY["panel"]["centerY"] + 43.2)
    assert outside_active, f"Pad loads active area: {pad.name}"
    # STL/glTF float32 contact faces can differ slightly after import.
    # Test the pad interior with a 0.0001 mm inset;
    # the unchanged outer faces are independently checked by contact rays.
    probe = pad.copy()
    probe.data = pad.data.copy()
    bpy.context.collection.objects.link(probe)
    matrix = pad.matrix_world
    for v in probe.data.vertices:
        world = matrix @ v.co
        for i in range(3):
            world[i] += .0001 if abs(world[i] - b[i][0]) < 1e-5 else -.0001
        v.co = matrix.inverted() @ world
    probe.data.update()
    pad_overlaps = {obj.name: value for obj in [shell, *frames, *display_parts, *components]
                    if (value := overlap(probe, obj)) > EPS}
    bpy.data.objects.remove(probe, do_unlink=True)
    assert not pad_overlaps, f"Pad collision: {pad.name}, {b}, {pad_overlaps}"
    if "rear-pad" in pad.name:
        owner = next(part for part in frames if near(hit_z(part, x, y, -3.4, 1), FRAME["frontZ"]))
        assert abs(b[2][0] - DISPLAY["panel"]["backZ"]) < 1e-5
        assert abs(b[2][1] - FRAME["frontZ"]) < 1e-5
        assert near(hit_z(panel, x, y, -3.6, -1), DISPLAY["panel"]["backZ"])
        assert abs(b[2][1] - b[2][0] - SPEC["cushioning"]["rearInstalledThickness"]) < 1e-5
        contacts.append({"pad": pad.name, "owner": owner.name, "glass_z": b[2][0], "frame_z": b[2][1], "outside_active_area": True})
    else:
        assert abs(b[2][1] - DISPLAY["panel"]["frontZ"]) < 1e-5
        assert near(hit_z(shell, x, y, -4.7, -1), b[2][0])
        glass_front = hit_z(panel, x, y, -4.9, 1)
        assert near(glass_front, DISPLAY["panel"]["frontZ"]), f"Front pad contact: {pad.name}, {(x,y)}, glass hit {glass_front}"

mount_checks = []
for mount in SCREWS["positions"]:
    x, y = mount["x"], mount["y"]
    stop_z = [hit_z(shell, x + dx, y + dy, -3.0, -1) for dx, dy in ((1.1, 0), (-1.1, 0), (0, 1.1), (0, -1.1))]
    assert all(near(z, FRAME["frontZ"]) for z in stop_z), "Missing retainer hard stop"
    pilot_floor = hit_z(shell, x, y, -3.0, -1)
    assert near(pilot_floor, SCREWS["pilotFloorZ"])
    tip_z = FRAME["backZ"] - SCREWS["length"]
    assert tip_z - pilot_floor >= .19
    screw = next(obj for obj in fasteners if abs(sum(bounds(obj)[0]) / 2 - x) < .001 and abs(sum(bounds(obj)[1]) / 2 - y) < .001)
    assert not any(overlap(screw, obj) > EPS for obj in [*frames, *pads, *display_parts, *components])
    # Threads intentionally cut into pilot material; the head/driver must fit.
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=SCREWS["driverDiameter"] / 2,
        depth=22, location=(x, y, FRAME["backZ"] + 11.05))
    driver = bpy.context.object
    driver_overlap = overlap(driver, shell) + overlap(driver, frames[0])
    bpy.data.objects.remove(driver, do_unlink=True)
    assert driver_overlap <= EPS, f"Blocked frame screw driver at {mount}"
    mount_checks.append({"x": x, "y": y, "stop_z": stop_z, "pilot_floor_z": pilot_floor, "tip_clearance_mm": round(tip_z - pilot_floor, 3), "driver_shell_overlap_mm3": driver_overlap})

# Sample the complete insertion/removal route with the PCB absent. Rear pad
# free thickness is used here, so raised sections do not rub the glass.
paths = []
for part in frames:
    lift = .15
    points = [(0, 0, 24), (0, 0, lift), (0, 0, 0)]
    carried = [part] + [pad for pad in rear_pads if next(c["owner"] for c in contacts if c["pad"] == pad.name) == part.name]
    original_matrices = {obj: obj.matrix_world.copy() for obj in carried}
    original_data = {}
    for pad in carried[1:]:
        original_data[pad] = pad.data
        pad.data = pad.data.copy()
        matrix = pad.matrix_world
        for v in pad.data.vertices:
            world = matrix @ v.co
            if abs(world.z - DISPLAY["panel"]["backZ"]) < 1e-5:
                world.z -= SPEC["cushioning"]["rearFreeThickness"] - SPEC["cushioning"]["rearInstalledThickness"]
                v.co = matrix.inverted() @ world
        pad.data.update()
    sample_count, max_overlap = 0, 0
    for a, b in zip(points, points[1:]):
        steps = max(1, math.ceil((Vector(b) - Vector(a)).length / .5))
        # Final pad compression is intended; test rigid part on final seating.
        for step in range(steps + 1):
            offset = Vector(a).lerp(Vector(b), step / steps)
            for obj in carried:
                obj.matrix_world = Matrix.Translation(offset) @ original_matrices[obj]
            bpy.context.view_layer.update()
            for obj in carried if b[2] else [part]:
                for obstacle in [shell, panel, *[other for other in frames if other != part]]:
                    value = overlap(obj, obstacle)
                    max_overlap = max(max_overlap, value)
                    assert value <= EPS, f"Installation collision: {part.name}, {tuple(offset)}, {obj.name}, {obstacle.name}: {value}"
            sample_count += 1
    for obj in carried:
        obj.matrix_world = original_matrices[obj]
    for pad, data in original_data.items():
        pad.data = data
    paths.append({"part": part.name, "offset_waypoints_mm": points, "samples": sample_count, "max_step_mm": .5, "max_overlap_mm3": max_overlap})

report = {"frame_solid_overlaps_mm3": collisions, "rear_pad_contacts": contacts,
          "front_pads_seated": 10, "hard_stops_and_screws": mount_checks,
          "installation_paths": paths, "frame_to_pcb_underside_clearance_mm": round(-.8 - FRAME["backZ"], 3),
          "basis": SPEC["basis"], "unverified": ["pad compression force", "printed tolerances", "thread strength", "drop resistance"]}
(STL / "display-retainer-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
