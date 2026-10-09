"""Generate dimensioned prototype STLs (millimetres) for the Rev. C reader.

Run: blender --background --python scripts/generate-printable-enclosure.py
The cell dimensions are the published *nominal* SparkFun PRT-13855 pack dimensions.
See assets/enclosure/PRINTING.md before fitting a real cell or powering a board.
"""

from math import cos, pi, sin
from pathlib import Path
import json
import sys
from zipfile import ZipFile, ZIP_DEFLATED

import bpy
import bmesh


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from importlib import import_module
display_flex = import_module("display-flex")
PCB_MOUNTS = json.loads((ROOT / "assets/enclosure/pcb-mounts.json").read_text())
RETAINER = json.loads((ROOT / "assets/enclosure/display-retainer.json").read_text())
OUT = ROOT / "assets" / "enclosure" / "stl"
OUT.mkdir(parents=True, exist_ok=True)

# PCB coordinates: +Z is the component/battery side; front display faces -Z.
CASE_W, CASE_H, CASE_Y, CORNER_R = 68.0, 111.0, 5.0, 5.0
INNER_W, INNER_H = 64.0, 107.0
FRONT_Z, FRONT_BACK_Z = -6.5, -4.1
BODY_FRONT_Z = -3.25
BACK_INNER_Z, BACK_OUTER_Z = 13.1, 14.6
PARTITION_LOW, PARTITION_HIGH = 4.6, 6.0
CELL_W, CELL_H, CELL_T = 49.2, 68.8, 5.6
CELL_X, CELL_Y = -6.2, -5.0
CELL_BASE = PARTITION_HIGH
LID_FASTENERS = ((-22.0, 56.0), (22.0, 56.0))
LID_LOWER_FASTENERS = ((-21.0, -48.9), (21.0, -48.9))


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
    mod.solver = "MANIFOLD"
    mod.object = other
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other, do_unlink=True)


def cut(target, other):
    boolean(target, other, "DIFFERENCE")


def add(target, other):
    boolean(target, other, "UNION")


def wedge(name, profile, low, high, along_x=False):
    n = len(profile)
    vertices = [(t, q, z) if along_x else (q, t, z) for t in (low, high) for q, z in profile]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    bm = bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh); bpy.context.collection.objects.link(obj)
    return obj


def cone(name, bottom_diameter, top_diameter, low, high, x, y):
    bpy.ops.mesh.primitive_cone_add(
        vertices=64, radius1=bottom_diameter / 2,
        radius2=top_diameter / 2, depth=high - low,
        location=(x, y, (low + high) / 2))
    obj = bpy.context.object
    obj.name = name
    return obj


def export_glb(objects, filename):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=str(OUT.parent / filename),
                              export_format="GLB", export_yup=False,
                              use_selection=True)


report = {}


def export(obj, filename):
    # Triangulate and check that every edge has exactly two adjacent faces.
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    # Exact booleans can leave coincident vertices on an intersected ledge.
    # Weld only numerical seams (0.00001 mm), then validate the actual mesh.
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm, edges=list(bm.edges), dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    obj.data.update()
    bad = sum(not edge.is_manifold for edge in bm.edges)
    bad_edges = [[[round(c, 7) for c in v.co] for v in edge.verts]
                 for edge in bm.edges if not edge.is_manifold]
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
        print("Non-manifold edge coordinates:", bad_edges)
        raise RuntimeError(f"{filename}: {bad} non-manifold edges, {islands} islands, volume {volume}")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=str(OUT / filename), export_selected_objects=True, apply_modifiers=True)
    if filename in {"front-bezel.stl", "main-body.stl", "button-strip.stl", "battery-partition.stl", "rear-cover.stl", "battery-envelope-DO-NOT-PRINT.stl", "antenna-envelope-DO-NOT-PRINT.stl"} or filename.startswith("display-retainer-"):
        bpy.ops.export_scene.gltf(
            filepath=str(OUT.parent / filename.replace(".stl", ".glb")),
            export_format="GLB", export_yup=False, use_selection=True,
        )


# Front bezel lifts off the body for display access without a loose frame.
reset()
main = prism("front-bezel", CASE_W, CASE_H, CORNER_R, FRONT_Z, FRONT_BACK_Z, y=CASE_Y)
cut(main, prism("visible-screen-window", 52.8, 87.2, 1.8, FRONT_Z - .1, FRONT_BACK_Z + .1, y=10.5))
# A rear pocket retains the 56.24 x 96.62 display perimeter. 0.28 mm side
# clearance and 0.29 mm end clearance are deliberate prototype allowances.
for x in (-21.0, -7.0, 7.0, 21.0):
    cut(main, prism("button-opening", 10.8, 5.2, 2.5, FRONT_Z - .1, FRONT_BACK_Z + .1, x=x, y=-42.5))
frame = prism("bezel-edge", CASE_W, CASE_H, CORNER_R, FRONT_BACK_Z - .05, BODY_FRONT_Z, y=CASE_Y)
cut(frame, prism("shell-interior", INNER_W, INNER_H, 3.1, FRONT_BACK_Z - .15, BODY_FRONT_Z + .1, y=CASE_Y))
add(main, frame)
# Independent hard stops set pad compression without loading the glass with
# screw torque. These small bosses sit entirely outside the panel pocket.
frame_spec, screws = RETAINER["frame"], RETAINER["fasteners"]
for mount in screws["positions"]:
    x, y = mount["x"], mount["y"]
    diameter = screws["bossDiameter"]
    add(main, prism("display-retainer-stop", diameter, diameter, diameter / 2,
                    screws["bossBaseZ"], frame_spec["frontZ"], x=x, y=y))
    pilot = screws["pilotDiameter"]
    cut(main, prism("display-retainer-tap-pilot", pilot, pilot, pilot / 2,
                    screws["pilotFloorZ"], frame_spec["frontZ"] + .05, x=x, y=y))
# The static button-strip rail is captured between bezel and body.
cut(main, box("button-rail-pocket", (54.4, 1.0, .85), (0, -47.55, -3.625)))
for x in (-21, -7, 7, 21):
    cut(main, box("button-leaf-root-pocket", (1.2, 2.1, .85), (x - 5.2, -47.0, -3.625)))
add(main, box("button-rail-seat", (54, .8, .05), (0, -47.55, -4.075)))
cut(main, prism("panel-rebate", 56.8, 97.2, 1.3, -4.8, -3.6, y=10.5))
export(main, "front-bezel.stl")

# Display retention and body walls print together, flat on their front face.
reset()
main = prism("main-body", CASE_W, CASE_H, CORNER_R, BODY_FRONT_Z, BACK_INNER_Z, y=CASE_Y)
cut(main, prism("body-interior", INNER_W, INNER_H, 3.1, BODY_FRONT_Z - .1, BACK_INNER_Z + .1, y=CASE_Y))
retainer = prism("integral-display-retainer", 64.4, frame_spec["height"], frame_spec["cornerRadius"], BODY_FRONT_Z, frame_spec["backZ"], y=frame_spec["centerY"])
cut(retainer, prism("unloaded-active-area", frame_spec["windowWidth"], frame_spec["windowHeight"], 1.8, BODY_FRONT_Z - .1, frame_spec["backZ"] + .1, y=frame_spec["centerY"]))
cut(retainer, box("ribbon-service-opening", (15, 7, 3), (0, -37.5, -2.5)))
add(main, retainer)
add(main, box("button-rail-clamp", (64.4, 1.2, 1.4), (0, -47.55, -2.55)))
# Through-wall ports are sized from the corresponding CAD model envelopes.
cut(main, box("usb-port", (10, 11.0, 15.0), (34, 36.3, 5.8)))
cut(main, box("sd-port", (10, 16.0, 15.0), (-34, -18.5, 5.8)))
cut(main, box("switch-port", (10, 11.0, 14.8), (34, 14.1, 5.9)))
# Four M2.5 mounting points share coordinates with the PCB source. Lower
# bosses clear a depressed cap body; outer cap flanges receive local relief.
# Nominal 2.0 mm pilots require a material-specific screw-fit test.
for mount in PCB_MOUNTS["mounts"]:
    x, y = mount["x"], mount["y"]
    low, high = mount["bossBaseZ"], PCB_MOUNTS["supportZ"]
    diameter = PCB_MOUNTS["bossDiameter"]
    bridge = box("mount-bridge", (7.0, diameter, high - low),
                 (30.0 if x > 0 else -30.0, y, (low + high) / 2))
    boolean(bridge, prism("mount-bridge-case-boundary", CASE_W, CASE_H,
                          CORNER_R, low - .1, high + .1, y=CASE_Y), "INTERSECT")
    add(main, bridge)
    add(main, prism("mount-boss", diameter, diameter, diameter / 2,
                    low, high, x=x, y=y))
    pilot = PCB_MOUNTS["pilotDiameter"]
    cut(main, prism("mount-pilot", pilot, pilot, pilot / 2,
                    mount["pilotBaseZ"], high + .05, x=x, y=y))
# Cover screw posts sit outside the complete board insertion envelope.
for x, y in LID_FASTENERS:
    boss = prism("lid-screw-boss", 7, 7, 3.5, BODY_FRONT_Z, BACK_INNER_Z, x=x, y=y)
    add(main, boss)
    cut(main, prism("lid-screw-pilot", 2, 2, 1, 8.1, BACK_INNER_Z + .1, x=x, y=y))
for x, y in LID_LOWER_FASTENERS:
    add(main, prism("lower-lid-post", 3.2, 3.2, 1.6, BODY_FRONT_Z, BACK_INNER_Z, x=x, y=y))
    cut(main, prism("lower-lid-pilot", 1.25, 1.25, .625, 10.1, BACK_INNER_Z + .1, x=x, y=y))
for mount in screws["positions"]:
    x, y = mount["x"], mount["y"]
    diameter = screws["clearanceDiameter"]
    cut(main, prism("bezel-screw-clearance", diameter, diameter, diameter / 2, BODY_FRONT_Z - .1, frame_spec["backZ"] + .1, x=x, y=y))
    depth = (screws["countersinkDiameter"] - diameter) / 2
    cut(main, cone("bezel-90-degree-countersink", diameter, screws["countersinkDiameter"] + .2, frame_spec["backZ"] - depth, frame_spec["backZ"] + .1, x, y))
    if y < 40:
        diameter = screws["driverDiameter"] + .4
        cut(main, prism("bezel-driver-service-notch", diameter, diameter, diameter / 2, -1.7, 5.0, x=x, y=y))
main.data.materials.append(display_flex.material("body-charcoal", (.09, .105, .12)))
export(main, "main-body.stl")

# Pads and screws are purchased/cut assembly supplies, never printed parts.
# Show their installed dimensions in CAD; pad compression is not simulated.
reset()
pad_objects = []
panel_spec = display_flex.SPEC["panel"]
for idx, pad in enumerate(RETAINER["cushioning"]["pads"], 1):
    for face, low, high in (
        ("front", panel_spec["frontZ"] - RETAINER["cushioning"]["frontInstalledThickness"], panel_spec["frontZ"]),
        ("rear", panel_spec["backZ"], frame_spec["frontZ"]),
    ):
        obj = box(f"display-{face}-pad-{idx}",
                  (pad["width"], pad["height"], high - low),
                  (pad["x"], pad["y"], (low + high) / 2))
        obj.data.materials.append(display_flex.material("display-soft-pad", (.32, .34, .36)))
        pad_objects.append(obj)
export_glb(pad_objects, "display-cushioning.glb")
reset()
fastener_objects = []
for idx, mount in enumerate(screws["positions"], 1):
    top = frame_spec["backZ"]
    head_bottom = top - (screws["headDiameter"] - 1.6) / 2
    obj = cone(f"display-retainer-screw-{idx}", 1.6, screws["headDiameter"],
               head_bottom, top, mount["x"], mount["y"])
    add(obj, prism("M1.6-nominal-thread-envelope", 1.6, 1.6, .8,
                    top - screws["length"], head_bottom + .01,
                    x=mount["x"], y=mount["y"]))
    obj.data.materials.append(display_flex.material("retainer-fastener", (.65, .67, .69)))
    fastener_objects.append(obj)
export_glb(fastener_objects, "display-retainer-fasteners.glb")

# Rigid insulator: 1.4 mm slab on four removable feet, with a wire
# opening beside BT1. The cell is offset left of BT1 to avoid stacking them.
reset()
partition = prism("battery-partition", 63.0, 80.0, 2.0, PARTITION_LOW, PARTITION_HIGH, y=-5.0)
# Four removable tray feet land on the PCB's mounting-hole keepouts.
# The cavity clears each installed screw head. There are no fixed body rails
# above the board, so the PCB and tray both lower straight in from the rear.
for mount in PCB_MOUNTS["mounts"]:
    x, y = mount["x"], mount["y"]
    if y > 35:
        add(partition, box("upper-tray-mount-arm", (7.0, 12.0, 1.4), (x, 40.0, 5.3)))
    foot = prism("tray-foot", 7, 7, 3.5, .8, PARTITION_HIGH, x=x, y=y)
    cut(foot, prism("pcb-screw-head-cavity", 5.4, 5.4, 2.7, .7, PARTITION_LOW, x=x, y=y))
    add(partition, foot)
# BT1 protrudes through this local cutout; its mating face points toward -Y.
cut(partition, box("bt1-header-and-lead-clearance", (8.0, 15.0, 4.0), (22.0, -34.0, 5.5)))
for x, y in LID_FASTENERS:
    if y < 0:
        cut(partition, prism("lower-lid-boss-relief", 8.0, 8.0, 4.0, 4.5, 8.1, x=x, y=y))
export(partition, "battery-partition.stl")

# Rear cover has a short locating tongue with 0.3 mm clearance per side and
# two M2.5 upper and two M1.6 lower screws. Verify printed pilot fit.
reset()
cover = prism("rear-cover", CASE_W, CASE_H, CORNER_R, BACK_INNER_Z, BACK_OUTER_Z, y=CASE_Y)
tongue = prism("rear-cover-tongue", 63.4, 106.4, 2.8, BACK_INNER_Z - 1.2, BACK_INNER_Z + .05, y=CASE_Y)
cut(tongue, prism("tongue-interior", 60.8, 103.8, 1.8, BACK_INNER_Z - 1.3, BACK_INNER_Z + .15, y=CASE_Y))
for x, y in (*LID_FASTENERS, *LID_LOWER_FASTENERS):
    cut(tongue, prism("lid-boss-tongue-relief", 8.0, 8.0, 4.0, BACK_INNER_Z - 1.3, BACK_INNER_Z + .15, x=x, y=y))
add(cover, tongue)
for x, y in LID_FASTENERS:
    cut(cover, prism("lid-screw-clearance", 2.7, 2.7, 1.35, BACK_INNER_Z - .1, BACK_OUTER_Z + .1, x=x, y=y))
    cut(cover, cone("lid-countersink", 2.7, 5.4, 13.35, 14.7, x, y))
for x in (-31.4, 20.4):
    add(cover, box("cell-side-guide", (0.8, 70.8, 6.8), (x, -5.0, 9.7)))
for y in (-40.9, 30.9):
    add(cover, box("cell-end-guide", (50.2, 0.8, 6.8), (-6.2, y, 9.7)))
cut(cover, box("battery-lead-guide-notch", (8, 15, 4), (22, -34, 7.0)))
# The upper part of each side port lifts off with the lid. Leave .2 mm
# clearance at each body/cover edge; PCB connectors can enter vertically.
for x, y, width, low in ((33, 36.3, 10.6, 5.3), (-33, -18.5, 15.6, 5.3), (33, 14.1, 10.6, 5.5)):
    add(cover, box("removable-port-roof", (1.9, width, 13.15 - low), (x, y, (13.15 + low) / 2)))
for x, y in LID_LOWER_FASTENERS:
    cut(cover, prism("lower-lid-clearance", 1.8, 1.8, .9, 13, 14.7, x=x, y=y))
    cut(cover, cone("lower-lid-countersink", 1.8, 3.4, 13.9, 14.7, x, y))
export(cover, "rear-cover.stl")

reset()
strip = box("button-strip-rail", (54, .8, .8), (0, -47.55, -3.65))
for idx, x in enumerate((-21.0, -7.0, 7.0, 21.0), 1):
    cap = prism(f"key-{idx}", 9.6, 4.0, 1.7, -6.4, -4.05, x=x, y=-42.5)
    flange = prism("retaining-flange", 11.6, 6.0, 2.2, -4.06, -3.65, x=x, y=-42.5)
    for mount in PCB_MOUNTS["mounts"]:
        if mount["buttonFlangeRelief"] and abs(x - mount["x"]) < 11.6 / 2 + PCB_MOUNTS["bossDiameter"] / 2 + .4:
            diameter = PCB_MOUNTS["bossDiameter"] + .8
            cut(flange, prism("mount-boss-flange-relief", diameter, diameter,
                              diameter / 2, -4.2, -3.4,
                              x=mount["x"], y=mount["y"]))
    add(cap, flange)
    add(cap, prism("button-plunger", 2.2, 2.2, .6, -3.7, -3.45, x=x, y=-42.5))
    # Inspection-only rigid key geometry permits independent stroke checks.
    export(cap, f"button-{idx}-DO-NOT-PRINT.stl")
    add(strip, cap)
    add(strip, box("independent-key-leaf", (11.2, .8, .8), (x, -46.3, -3.65)))
    add(strip, box("leaf-fixed-root", (.8, 1.7, .8), (x - 5.2, -47.0, -3.65)))
    add(strip, box("leaf-key-tip", (.8, 2.8, .8), (x + 5.2, -45.3, -3.65)))
strip.data.materials.append(display_flex.material("PETG-button-strip", (.25, .26, .28)))
# Preserve a face edge at the clamp boundary for independent stroke review.
bm = bmesh.new(); bm.from_mesh(strip.data)
bmesh.ops.bisect_plane(bm, geom=list(bm.verts)+list(bm.edges)+list(bm.faces), dist=1e-6,
                      plane_co=(0, -46.95, 0), plane_no=(0, 1, 0))
bm.to_mesh(strip.data); bm.free()
export(strip, "button-strip.stl")

# Native CAD hardware: four PCB screws and four flush lid screws.
reset()
hardware = []
for mount in PCB_MOUNTS["mounts"]:
    x, y = mount["x"], mount["y"]
    screw = prism("PCB-" + mount["name"], 5, 5, 2.5, .8, 3.3, x=x, y=y)
    add(screw, prism("PCB-shaft", 2.5, 2.5, 1.25, .8 - PCB_MOUNTS["screwLength"], .81, x=x, y=y))
    hardware.append(screw)
for idx, (x, y) in enumerate(LID_FASTENERS, 1):
    screw = cone("cover-screw-" + str(idx), 2.5, 5, 13.35, BACK_OUTER_Z, x, y)
    add(screw, prism("cover-shaft", 2.5, 2.5, 1.25, 8.6, 13.36, x=x, y=y))
    hardware.append(screw)
for idx, (x, y) in enumerate(LID_LOWER_FASTENERS, 1):
    screw = cone("lower-cover-screw-" + str(idx), 1.6, 3, 13.9, BACK_OUTER_Z, x, y)
    add(screw, prism("lower-cover-shaft", 1.6, 1.6, .8, 10.6, 13.91, x=x, y=y))
    hardware.append(screw)
for screw in hardware: screw.data.materials.append(display_flex.material("assembly-fastener", (.65, .67, .69)))
export_glb(hardware, "pcb-cover-fasteners.glb")

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
display = display_flex.SPEC["panel"]
panel = prism("ER-EPD3.97-1RY-nominal-outline", display["width"], display["height"], 1.0, display["frontZ"], display["backZ"], y=display["centerY"])
active = prism("480x800-active-area", 51.84, 86.4, .3, -4.71, -4.65, y=display["centerY"])
panel.data.materials.append(display_flex.material("EPD-black-perimeter", (.075, .075, .08)))
active.data.materials.append(display_flex.material("EPD-paper", (.86, .85, .77)))
flex_objects, length = display_flex.create_flex()
# Assembly.screen is anchored at J2's PCB surface, not at the PCB origin.
# Subtract both Y and Z to keep the panel in its measured enclosure rebate.
connector = display_flex.SPEC["connector"]
bpy.ops.object.select_all(action="DESELECT")
for obj in (panel, active, *flex_objects):
    obj.location.y -= connector["centerY"]
    obj.location.z -= connector["boardSurfaceZ"]
    obj.select_set(True)
bpy.context.view_layer.objects.active = panel
bpy.ops.export_scene.gltf(filepath=str(OUT.parent / "display-panel.glb"), export_format="GLB", export_yup=False, use_selection=True)
print(f"Nominal installed display flex length: {length:.6f} mm")

(OUT / "mesh-check.json").write_text(json.dumps(report, indent=2) + "\n")
# Print exports are oriented on the bed; CAD exports retain PCB coordinates.
from runpy import run_path
run_path(str(ROOT / "scripts/prepare-print-package.py"))
print(json.dumps(report, indent=2))
