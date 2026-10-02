"""Render the STL stack with the tsci PCB model from front, rear, and exploded views.

Run after `tsci export dist/index/circuit.json --format glb --output /tmp/esp-reader-current.glb`.
"""

from pathlib import Path
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
STL = ROOT / 'assets/enclosure/stl'
OUT = ROOT / 'assets/enclosure'
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


def read_stl(filename, color):
    bpy.ops.wm.stl_import(filepath=str(STL / filename))
    obj = bpy.context.object
    obj.color = (*color, 1)
    return obj


shell = read_stl('front-shell.stl', (.09, .105, .12))
partition = read_stl('battery-partition.stl', (.26, .28, .31))
cover = read_stl('rear-cover.stl', (.11, .12, .14))
cell = read_stl('battery-envelope-DO-NOT-PRINT.stl', (.32, .54, .75))
buttons = [read_stl(f'button-{i}.stl', (.25, .26, .28)) for i in range(1, 5)]

# CLI GLB imports into Blender with axes (-PCB X, -PCB Y, PCB Z).
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath='/tmp/esp-reader-current.glb')
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
board = []
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH':
        continue
    obj.matrix_world = conversion @ obj.matrix_world
    obj.color = (.62, .64, .67, 1)
    if obj.name in ('Box0', 'MeshWithTextures0'):
        obj.color = (.04, .25, .16, 1)
    if obj.name == 'EPD1':
        obj.hide_render = True
    board.append(obj)

# Nominal panel envelope, including front visible area; FPC is unmodeled.
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 10.5, -4.2))
panel = bpy.context.object
panel.dimensions = (56.24, 96.62, .9)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
panel.color = (.1, .1, .11, 1)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 10.5, -4.66))
active = bpy.context.object
active.dimensions = (51.84, 86.4, .05)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
active.color = (.86, .85, .77, 1)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.color_type = 'OBJECT'
scene.display.shading.light = 'STUDIO'
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.render.resolution_x = 1100
scene.render.resolution_y = 1000
scene.render.resolution_percentage = 100
scene.world.color = (.025, .027, .032)


def render(name, pos, scale=145, target=(0, 5, 5)):
    bpy.ops.object.camera_add(location=pos)
    cam = bpy.context.object
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = scale
    scene.camera = cam
    scene.render.filepath = str(OUT / name)
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam, do_unlink=True)


cover.hide_render = True
render('printable-front.png', (100, 130, -110))
render('printable-open-back.png', (-100, -110, 120))
render('printable-side.png', (190, -25, 35), 140)

# Local view of the changed battery connector and the lifted cable notch.
shell.hide_render = True
cell.hide_render = True
panel.hide_render = True
active.hide_render = True
partition.location.z += 10
render('printable-battery-connector.png', (75, -125, 125), 80, (12, -29, 8))
partition.location.z -= 10
shell.hide_render = False
cell.hide_render = False
panel.hide_render = False
active.hide_render = False

# Exploded illustration preserves X/Y positions and shifts Z only.
for obj in board:
    obj.location.z += 24
partition.location.z += 35
cell.location.z += 44
cover.location.z += 53
cover.hide_render = False
render('printable-exploded.png', (165, -145, 125), 185, (0, 5, 38))
