"""Render the STL stack with the tsci PCB model from front, rear, and exploded views.

Run after `tsci export dist/index/circuit.json --format glb --output /tmp/esp-reader-current.glb`.
"""

from pathlib import Path
import json
from math import pi
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
STL = ROOT / 'assets/enclosure/stl'
OUT = ROOT / 'assets/enclosure'
PCB_MOUNTS = json.loads((OUT / 'pcb-mounts.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)


def read_stl(filename, color):
    bpy.ops.wm.stl_import(filepath=str(STL / filename))
    obj = bpy.context.object
    obj.color = (*color, 1)
    return obj


shell = read_stl('front-bezel.stl', (.09, .105, .12))
retainers = [read_stl('main-body.stl', (.09, .105, .12))]
partition = read_stl('battery-partition.stl', (.26, .28, .31))
cover = read_stl('rear-cover.stl', (.11, .12, .14))
cell = read_stl('battery-envelope-DO-NOT-PRINT.stl', (.32, .54, .75))
buttons = [read_stl('button-strip.stl', (.25, .26, .28))]

# CLI GLB imports into Blender with axes (-PCB X, -PCB Y, PCB Z).
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath='/tmp/esp-reader-current.glb')
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
board = []
assembly_nodes = {'EPD1', 'battery_envelope', 'wifi_antenna_envelope',
                  'pcb_cover_fasteners', 'front_bezel', 'main_body', 'button_strip', 'battery_partition', 'rear_cover',
                  'display_retainer_lower_left', 'display_retainer_lower_right',
                  'display_retainer_upper_left', 'display_retainer_upper_right',
                  'display_cushioning', 'display_retainer_fasteners',
                  'button_1', 'button_2', 'button_3', 'button_4'}
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH':
        continue
    if obj.name in assembly_nodes:
        obj.hide_render = True
        continue
    obj.matrix_world = conversion @ obj.matrix_world
    obj.color = (.62, .64, .67, 1)
    if obj.name in ('Box0', 'MeshWithTextures0'):
        obj.color = (.04, .25, .16, 1)
    board.append(obj)

# Nominal fastener envelopes use the same specification as the clearance check.
for mount in PCB_MOUNTS['mounts']:
    for name, radius, low, high in (
        ('head', PCB_MOUNTS['screwHeadDiameter'] / 2, .8, .8 + PCB_MOUNTS['screwHeadHeight']),
        ('shaft', 1.25, .8 - PCB_MOUNTS['screwLength'], .8),
    ):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64, radius=radius, depth=high - low,
            location=(mount['x'], mount['y'], (low + high) / 2))
        obj = bpy.context.object
        obj.name = mount['name'] + '-' + name
        obj.color = (.68, .7, .73, 1)
        board.append(obj)

# Use the same panel and installed flex shown by assembly.screen.
connection = json.loads((OUT / 'display-connection.json').read_text())
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(OUT / 'display-panel.glb'))
display_objects = []
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH':
        continue
    # Our local GLB is deliberately Z-up for tscircuit. Blender's importer
    # assumes glTF Y-up, so undo its X-axis conversion before placing it.
    obj.matrix_world = Matrix.Translation(Vector((0, connection['connector']['centerY'], connection['connector']['boardSurfaceZ']))) @ Matrix.Rotation(-pi / 2, 4, 'X') @ obj.matrix_world
    obj.color = tuple(obj.data.materials[0].diffuse_color)
    display_objects.append(obj)
panel = next(obj for obj in display_objects if 'nominal-outline' in obj.name)
active = next(obj for obj in display_objects if 'active-area' in obj.name)
flex_objects = [obj for obj in display_objects if obj not in (panel, active)]

retention_supplies = []
for filename in ('display-cushioning.glb', 'display-retainer-fasteners.glb'):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(OUT / filename))
    for obj in set(bpy.data.objects) - before:
        if obj.type != 'MESH':
            continue
        obj.matrix_world = Matrix.Rotation(-pi / 2, 4, 'X') @ obj.matrix_world
        obj.color = tuple(obj.data.materials[0].diffuse_color) if obj.data.materials else (.65, .67, .69, 1)
        retention_supplies.append(obj)

lid_hardware = []
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(OUT / 'pcb-cover-fasteners.glb'))
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH': continue
    obj.matrix_world = Matrix.Rotation(-pi / 2, 4, 'X') @ obj.matrix_world
    obj.color = (.65, .67, .69, 1)
    if 'cover-screw-' in obj.name:
        obj.hide_render = True; lid_hardware.append(obj)
    else: obj.hide_render = True

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
partition.hide_render = True
cell.hide_render = True
panel.hide_render = True
active.hide_render = True
for obj in flex_objects:
    obj.hide_render = True
render('printable-pcb-mounts.png', (0, 3, 220), 132, (0, 3, 0))
partition.hide_render = False
cell.hide_render = False
panel.hide_render = False
active.hide_render = False
for obj in flex_objects:
    obj.hide_render = False
cover.hide_render = False
for obj in lid_hardware: obj.hide_render = False
render('printable-front.png', (100, 130, -110))
cover.hide_render = True
for obj in lid_hardware: obj.hide_render = True
render('printable-open-back.png', (-100, -110, 120))
cover.hide_render = False
for obj in lid_hardware: obj.hide_render = False
render('printable-side.png', (190, -25, 35), 140)
cover.hide_render = True
for obj in lid_hardware: obj.hide_render = True

# Installed connection close-up with the shell removed so the locking socket
# and the flex crossing through the actual PCB slot remain visible.
shell.hide_render = True
for obj in retainers: obj.hide_render = True
partition.hide_render = True
cell.hide_render = True
render('display-ribbon-connection.png', (35, -83, 30), 44, (0, -34, 0))
shell.hide_render = False
for obj in retainers: obj.hide_render = False

# Show the integral display retainer with the PCB lifted out:
# flush fasteners, and the central ribbon opening remain visible.
for obj in board:
    obj.hide_render = True
render('display-retainer-installed.png', (95, -115, 140), 137, (0, 8, -3))
for obj in board:
    obj.hide_render = False
partition.hide_render = False
cell.hide_render = False

# Local view of the changed battery connector and the lifted cable notch.
shell.hide_render = True
for obj in retainers: obj.hide_render = True
cell.hide_render = True
panel.hide_render = True
active.hide_render = True
partition.location.z += 10
render('printable-battery-connector.png', (75, -125, 125), 80, (12, -29, 8))
partition.location.z -= 10
shell.hide_render = False
for obj in retainers: obj.hide_render = False
cell.hide_render = False
panel.hide_render = False
active.hide_render = False

# Exploded illustration preserves X/Y positions and shifts Z only.
for obj in display_objects:
    obj.location.z += 8
for obj in retainers:
    obj.location.z += 16
for obj in retention_supplies:
    obj.location.z += 12 if 'pad' in obj.name else 16
for obj in board:
    obj.location.z += 24
partition.location.z += 35
cell.location.z += 44
cover.location.z += 53
cover.hide_render = False
for obj in lid_hardware:
    obj.location.z += 53; obj.hide_render = False
render('printable-exploded.png', (165, -145, 125), 185, (0, 5, 38))

# The actual five bed-oriented exports, at their 3MF plate positions.
for obj in list(bpy.data.objects): obj.hide_render = True
for name, x, y, color in (
    ('front-bezel', 38, 61, (.10, .13, .16)),
    ('main-body', 111, 61, (.15, .30, .38)),
    ('rear-cover', 184, 61, (.10, .13, .16)),
    ('battery-partition', 38, 167, (.30, .34, .38)),
    ('button-strip', 112, 145, (.19, .42, .54))):
    bpy.ops.wm.stl_import(filepath=str(OUT/'print'/(name+'.stl')))
    obj = bpy.context.object; obj.location.x += x; obj.location.y += y
    obj.color = (*color, 1)
    if name == 'button-strip':
        label_pos = (x, y - 8, .3)
    else:
        label_pos = (x - (32 if name == 'battery-partition' else 34.5), y - 23, .3)
    bpy.ops.object.text_add(location=label_pos)
    label = bpy.context.object; label.data.body = name.replace('-', ' ')
    label.data.size = 3.3; label.data.align_x = 'CENTER' if name == 'button-strip' else 'LEFT'
    if name != 'button-strip': label.rotation_euler.z = pi / 2
    label.color = (.15,.18,.20,1)
bpy.ops.mesh.primitive_cube_add(size=1, location=(110,110,-.65))
bed = bpy.context.object; bed.dimensions = (220,220,1.2); bed.color = (.78,.80,.81,1)
render('reader-print-plate.png', (230,-170,390), 325, (110,110,0))
