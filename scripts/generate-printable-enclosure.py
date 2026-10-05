"""Generate dimensioned prototype STLs (millimetres) for the Rev. B reader.

Run: blender --background --python scripts/generate-printable-enclosure.py
The cell dimensions are the published *nominal* SparkFun PRT-13855 pack dimensions.
See assets/enclosure/PRINTING.md before fitting a real cell or powering a board.
"""

from math import cos, pi, sin
from pathlib import Path
import json
from zipfile import ZipFile, ZIP_DEFLATED

import bpy
import bmesh


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "enclosure" / "stl"
OUT.mkdir(parents=True, exist_ok=True)

# PCB coordinates: +Z is the component/battery side; front display faces -Z.
CASE_W, CASE_H, CASE_Y, CORNER_R = 68.0, 109.5, 5.75, 5.0
INNER_W, INNER_H = 64.0, 105.5
FRONT_Z, FRONT_BACK_Z = -6.5, -4.1
BACK_INNER_Z, BACK_OUTER_Z = 13.1, 14.6
PARTITION_LOW, PARTITION_HIGH = 4.6, 6.0
CELL_W, CELL_H, CELL_T = 49.2, 68.8, 5.6
CELL_X, CELL_Y = -6.2, -5.0
CELL_BASE = PARTITION_HIGH
LID_FASTENERS = ((-30.0, -45.0), (30.0, -45.0), (-22.0, 56.0), (22.0, 56.0))


def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def prism(name, width, height, radius, low, high, x=0, y=0):
    radius = min(radius, width / 2, height / 2)
    corners = [
        (x + width / 2 - radius, y - height / 2 + radius, -pi / 2),
        (x + width / 2 - radius, y + height / 2 - radius, 0),
        (x - width / 2 + radius, y + height / 2 - radius, pi / 2),
        (x - width / 2 + radius, y - height / 2 + radius, pi),
    ]
    outline = []
    for cx, cy, start in corners:
        for step in range(17):
            angle = start + step * pi / 32
            outline.append((cx + radius * cos(angle), cy + radius * sin(angle)))
    count = len(outline)
    verts = [(px, py, low) for px, py in outline]
    verts += [(px, py, high) for px, py in outline]
    faces = [tuple(reversed(range(count))), tuple(range(count, count * 2))]
    for i in range(count):
        j = (i + 1) % count
        faces.append((i, j, count + j, count + i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def box(name, dims, center):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def boolean(target, other, operation):
    bpy.context.view_layer.objects.active = target
    mod = target.modifiers.new(operation.lower(), "BOOLEAN")
    mod.operation = operation
    mod.solver = "EXACT"
    mod.object = other
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other, do_unlink=True)


def cut(target, other):
    boolean(target, other, "DIFFERENCE")


def add(target, other):
    boolean(target, other, "UNION")


report = {}


def export(obj, filename):
    # Triangulate and check that every edge has exactly two adjacent faces.
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bad = sum(not edge.is_manifold for edge in bm.edges)
    volume = bm.calc_volume(signed=True)
    unseen = set(bm.verts)
    islands = 0
    while unseen:
        islands += 1
        todo = [unseen.pop()]
        while todo:
            v = todo.pop()
            for edge in v.link_edges:
                other = edge.other_vert(v)
                if other in unseen:
                    unseen.remove(other)
                    todo.append(other)
    bm.free()
    coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
    bounds = [[min(v[i] for v in coords), max(v[i] for v in coords)] for i in range(3)]
    report[filename] = {"nonmanifold_edges": bad, "connected_shells": islands, "signed_volume_mm3": round(volume, 3), "bounds_mm": [[round(q, 3) for q in pair] for pair in bounds]}
    if bad or volume <= 0 or islands != 1:
        raise RuntimeError(f"{filename}: {bad} non-manifold edges, {islands} islands, volume {volume}")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=str(OUT / filename), export_selected_objects=True, apply_modifiers=True)
    if filename in {"front-shell.stl", "battery-partition.stl", "rear-cover.stl", "battery-envelope-DO-NOT-PRINT.stl", "antenna-envelope-DO-NOT-PRINT.stl"} or filename.startswith("button-"):
        bpy.ops.export_scene.gltf(
            filepath=str(OUT.parent / filename.replace(".stl", ".glb")),
            export_format="GLB", export_yup=False, use_selection=True,
        )


# Front panel and deep open-back shell are one printed part. Both the screen
# and PCB can be loaded through the rear opening before the partition goes in.
reset()
main = prism("front-shell", CASE_W, CASE_H, CORNER_R, FRONT_Z, FRONT_BACK_Z, y=CASE_Y)
cut(main, prism("visible-screen-window", 52.8, 87.2, 1.8, FRONT_Z - .1, FRONT_BACK_Z + .1, y=10.5))
# A rear pocket retains the 56.24 x 96.62 display perimeter. 0.28 mm side
# clearance and 0.29 mm end clearance are deliberate prototype allowances.
cut(main, prism("panel-rebate", 56.8, 97.2, 1.3, -4.8, FRONT_BACK_Z + .1, y=10.5))
for x in (-21.0, -7.0, 7.0, 21.0):
    cut(main, prism("button-opening", 10.8, 5.2, 2.5, FRONT_Z - .1, FRONT_BACK_Z + .1, x=x, y=-42.5))
frame = prism("shell-wall", CASE_W, CASE_H, CORNER_R, FRONT_BACK_Z - .05, BACK_INNER_Z, y=CASE_Y)
cut(frame, prism("shell-interior", INNER_W, INNER_H, 3.1, FRONT_BACK_Z - .15, BACK_INNER_Z + .1, y=CASE_Y))
add(main, frame)
# Through-wall ports are sized from the corresponding CAD model envelopes.
cut(main, box("usb-port", (10, 11.0, 7.0), (34, 36.3, 1.8)))
cut(main, box("sd-port", (10, 16.0, 7.0), (-34, -18.5, 1.8)))
cut(main, box("switch-port", (10, 11.0, 7.0), (34, 14.1, 2.0)))
# Partition rests on two rails above the tallest modeled component (BT1).
add(main, box("partition-left-ledge", (4.2, 80.0, 1.4), (-30.35, -6.5, 3.9)))
# The right ledges avoid SW7, whose model reaches Z 4.35.
for y, length in ((-22.0, 31.0), (24.0, 10.0)):
    add(main, box("partition-right-ledge", (4.2, length, 1.4), (30.35, y, 3.9)))
# PCB is supported only along its edges, clear of underside button bodies.
for x in (-31.6, 31.6):
    add(main, box("pcb-edge-ledge", (1.4, 82.0, 0.8), (x, 3.0, -1.2)))
# Two upper M2.5 board holes are above an integral bridge and blind pilot.
# These nominal 2.0 mm pilots suit a prototype self-tapping screw only after
# material-specific test. The lower board edge rests on a continuous ledge.
for x in (-27.0, 27.0):
    add(main, box("mount-bridge", (7.0, 5.6, 3.2), (x + (3.0 if x > 0 else -3.0), 44.75, -2.4)))
    add(main, prism("mount-boss", 5.6, 5.6, 2.8, -4.0, -0.8, x=x, y=44.75))
    cut(main, prism("mount-pilot", 2.0, 2.0, 1.0, -4.05, -0.75, x=x, y=44.75))
add(main, box("pcb-lower-edge-ledge", (65.0, 1.2, 0.8), (0.0, -46.3, -1.2)))
# Four lid screws live beyond the battery's Y span. Their bosses merge into
# the end walls and do not pass through the PCB or the partition.
for x, y in LID_FASTENERS:
    add(main, prism("lid-screw-boss", 7.0, 7.0, 3.5, 6.6, BACK_INNER_Z, x=x, y=y))
    cut(main, prism("lid-screw-pilot", 2.0, 2.0, 1.0, 9.1, BACK_INNER_Z + .1, x=x, y=y))
export(main, "front-shell.stl")

# Rigid insulator: 1.4 mm slab, a 49.2 x 68.8 mm cell pocket, and a wire
# opening beside BT1. The cell is offset left of BT1 to avoid stacking them.
reset()
partition = prism("battery-partition", 63.0, 80.0, 2.0, PARTITION_LOW, PARTITION_HIGH, y=-5.0)
for x in (-31.25, 20.4):
    add(partition, box("cell-side-guide", (0.5, 70.8, 1.4), (x, -5.0, 6.7)))
for y in (-40.9, 30.9):
    add(partition, box("cell-end-guide", (50.2, 0.6, 1.4), (-6.2, y, 6.7)))
# BT1 protrudes through this local cutout; its mating face points toward -Y.
cut(partition, box("bt1-header-and-lead-clearance", (8.0, 15.0, 4.0), (22.0, -34.0, 5.5)))
for x in (-30.0, 30.0):
    cut(partition, prism("lower-lid-boss-relief", 8.0, 8.0, 4.0, 4.5, 8.1, x=x, y=-45.0))
export(partition, "battery-partition.stl")

# Rear cover has a short locating tongue with 0.3 mm clearance per side and
# four M2.5 screw holes into end-wall bosses. Verify printed pilot fit.
reset()
cover = prism("rear-cover", CASE_W, CASE_H, CORNER_R, BACK_INNER_Z, BACK_OUTER_Z, y=CASE_Y)
tongue = prism("rear-cover-tongue", 63.4, 104.9, 2.8, BACK_INNER_Z - 1.2, BACK_INNER_Z + .05, y=CASE_Y)
cut(tongue, prism("tongue-interior", 60.8, 102.3, 1.8, BACK_INNER_Z - 1.3, BACK_INNER_Z + .15, y=CASE_Y))
for x, y in LID_FASTENERS:
    cut(tongue, prism("lid-boss-tongue-relief", 8.0, 8.0, 4.0, BACK_INNER_Z - 1.3, BACK_INNER_Z + .15, x=x, y=y))
add(cover, tongue)
for x, y in LID_FASTENERS:
    cut(cover, prism("lid-screw-clearance", 2.7, 2.7, 1.35, BACK_INNER_Z - .1, BACK_OUTER_Z + .1, x=x, y=y))
export(cover, "rear-cover.stl")

reset()
for idx, x in enumerate((-21.0, -7.0, 7.0, 21.0), 1):
    cap = prism(f"key-{idx}", 9.6, 4.0, 1.7, -6.4, -4.05, x=x, y=-42.5)
    add(cap, prism("retaining-flange", 11.6, 6.0, 2.2, -4.06, -3.65, x=x, y=-42.5))
    add(cap, prism("button-plunger", 2.2, 2.2, .6, -3.7, -3.45, x=x, y=-42.5))
    export(cap, f"button-{idx}.stl")

# Envelope file is for non-printing fit inspection only.
reset()
cell = prism("SparkFun-PRT-13855-nominal-body", CELL_W, CELL_H, 1.4, CELL_BASE, CELL_BASE + CELL_T, x=CELL_X, y=CELL_Y)
export(cell, "battery-envelope-DO-NOT-PRINT.stl")

# Taoglas FXP75.07.0045B antenna film, bonded to the inside rear cover.
# The 45 mm micro-coax exits toward U4; the cable and U.FL plug remain to be
# checked with a physical sample and are intentionally not represented here.
reset()
antenna = prism("Taoglas-FXP75-nominal-film", 5.9, 4.1, .2, 12.86, 13.10, x=25.0, y=44.0)
export(antenna, "antenna-envelope-DO-NOT-PRINT.stl")

# `assembly.screen` positions this display model relative to J2. Keep it in
# the same generator so legacy visual-case scripts cannot overwrite the new
# enclosure files by accident.
reset()
panel = prism("Waveshare-3.97inch-e-Paper-G-outline", 56.24, 96.62, 1.0, -4.65, -3.75, x=0.0, y=40.0)
active = prism("480x800-active-area", 51.84, 86.4, .3, -4.71, -4.65, x=0.0, y=40.0)
bpy.ops.object.select_all(action="DESELECT")
for obj in (panel, active):
    obj.select_set(True)
bpy.context.view_layer.objects.active = panel
bpy.ops.export_scene.gltf(filepath=str(OUT.parent / "display-panel.glb"), export_format="GLB", export_yup=False, use_selection=True)

(OUT / "mesh-check.json").write_text(json.dumps(report, indent=2) + "\n")
with ZipFile(OUT.parent / "esp32-reader-printable-stls.zip", "w", ZIP_DEFLATED, compresslevel=9) as package:
    for name in ("front-shell.stl", "battery-partition.stl", "rear-cover.stl", *(f"button-{i}.stl" for i in range(1, 5))):
        package.write(OUT / name, name)
    package.write(OUT.parent / "PRINTING.md", "PRINTING.md")
print(json.dumps(report, indent=2))
