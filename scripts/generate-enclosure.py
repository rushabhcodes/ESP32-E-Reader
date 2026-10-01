"""Generate a visual enclosure reconstruction for the Rev. B board.

Run with: blender --background --python scripts/generate-enclosure.py

The source project's enclosure CAD is unpublished. These meshes use the board
outline and part locations in this repository plus the source project's photos.
They are visual reference models, not validated printable or snap-fit parts.
"""

from math import cos, pi, sin
from pathlib import Path

import bpy


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "enclosure"
OUTPUT.mkdir(parents=True, exist_ok=True)


def reset_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def material(name, color, alpha=1.0):
    result = bpy.data.materials.new(name)
    result.diffuse_color = (*color, alpha)
    result.use_nodes = True
    shader = result.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, alpha)
    shader.inputs["Roughness"].default_value = 0.78
    if alpha < 1:
        shader.inputs["Alpha"].default_value = alpha
        result.surface_render_method = "BLENDED"
    return result


def rounded_prism(name, width, height, radius, z_low, z_high, x=0, y=0):
    radius = min(radius, width / 2, height / 2)
    corners = [
        (x + width / 2 - radius, y - height / 2 + radius, -pi / 2),
        (x + width / 2 - radius, y + height / 2 - radius, 0),
        (x - width / 2 + radius, y + height / 2 - radius, pi / 2),
        (x - width / 2 + radius, y - height / 2 + radius, pi),
    ]
    outline = []
    for cx, cy, start in corners:
        for step in range(9):
            angle = start + step * pi / 16
            outline.append((cx + radius * cos(angle), cy + radius * sin(angle)))
    count = len(outline)
    vertices = [(px, py, z_low) for px, py in outline]
    vertices += [(px, py, z_high) for px, py in outline]
    faces = [tuple(reversed(range(count))), tuple(range(count, count * 2))]
    for i in range(count):
        next_i = (i + 1) % count
        faces.append((i, next_i, count + next_i, count + i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def box(name, size, position):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def subtract(target, cutter):
    bpy.context.view_layer.objects.active = target
    modifier = target.modifiers.new("opening", "BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.solver = "EXACT"
    modifier.object = cutter
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


def unite(target, part):
    bpy.context.view_layer.objects.active = target
    modifier = target.modifiers.new("join-shell-sections", "BOOLEAN")
    modifier.operation = "UNION"
    modifier.solver = "EXACT"
    modifier.object = part
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(part, do_unlink=True)


def export(name, parts):
    bpy.ops.object.select_all(action="DESELECT")
    for part in parts:
        part.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.export_scene.gltf(
        filepath=str(OUTPUT / name),
        export_format="GLB",
        export_yup=False,
        use_selection=True,
    )


# The 62.5 mm board now has the same width through its tactile-button chin.
# Front = bottom-layer/button side (-Z), back = component/battery side (+Z).
# A straight-sided shell gives the larger screen an X3-like pocket-reader
# silhouette. The selected cell sits behind the upper PCB, clear of the
# tactile switches in plan view.
# This is a visual concept, not a validated mechanical design.
reset_scene()
black = material("textured-black-plastic", (0.033, 0.038, 0.042))
bezel = rounded_prism("front-bezel", 68, 109.5, 5.0, -8.0, -5.6, y=5.75)
bezel.data.materials.append(black)
subtract(bezel, rounded_prism("display-window", 52.8, 87.2, 1.8, -8.2, -5.4, y=10.5))
# Four independent pill openings match the source reader's front controls.
# The small caps below are separate from the shell, with nominal free play.
for x in (-21, -7, 7, 21):
    subtract(bezel, rounded_prism("button-opening", 10.8, 5.2, 2.5, -8.2, -5.4, x=x, y=-42.5))

# The inner lip is narrower than the rear cavity. It is a visual mating rim;
# no snap tab, tolerance, or load path has been validated for fabrication.
lip = rounded_prism("front-mating-rim", 63.2, 94, 3.4, -5.6, -1.1, y=12.7)
lip.data.materials.append(black)
subtract(lip, rounded_prism("lip-interior", 61.5, 92.6, 2.6, -5.8, -0.9, y=12.7))
subtract(lip, box("usb-relief", (6, 11, 6), (32.5, 36.3, -2.3)))
subtract(lip, box("sd-relief", (6, 15, 6), (-32.5, -18.5, -2.3)))
chin_lip = rounded_prism("chin-mating-rim", 63.2, 11.5, 3.4, -5.6, -1.1, y=-42.25)
chin_lip.data.materials.append(black)
subtract(chin_lip, rounded_prism("chin-lip-interior", 61.5, 9.8, 2.6, -5.8, -0.9, y=-42.25))
export("front-bezel.glb", [bezel, lip, chin_lip])

reset_scene()
caps = []
for x in (-21, -7, 7, 21):
    cap = rounded_prism("button-cap", 9.6, 4.0, 1.8, -8.25, -6.9, x=x, y=-42.5)
    cap.data.materials.append(material("button-graphite", (0.15, 0.16, 0.17)))
    stem = rounded_prism("button-plunger", 2.2, 2.2, 0.7, -6.9, -3.45, x=x, y=-42.5)
    stem.data.materials.append(material("button-stem", (0.12, 0.13, 0.14)))
    caps.extend([cap, stem])
export("button-caps.glb", caps)

# assembly.screen anchors to J2 at (-0.75, -29.5, +0.8) with zero
# rotation. Keep model geometry relative to that anchor so the panel lies
# behind the front window, on the other side of the PCB from J2.
reset_scene()
panel_x = 0.75
panel_y = 10.5 + 29.5
panel = rounded_prism("ER-EPD3.97-1RY-outline", 56.24, 96.62, 1.0, -6.15, -5.25, x=panel_x, y=panel_y)
panel.data.materials.append(material("e-paper-edge", (0.04, 0.045, 0.05)))
active = rounded_prism("480x800-active-area", 51.84, 86.4, 0.3, -6.21, -6.15, x=panel_x, y=panel_y)
active.data.materials.append(material("e-paper-white", (0.89, 0.88, 0.80)))
export("display-panel.glb", [panel, active])

reset_scene()
rear = rounded_prism("rear-tray", 68, 109.5, 5.0, -1.0, 10.2, y=5.75)
rear.data.materials.append(material("graphite-rear-shell", (0.055, 0.06, 0.065)))
subtract(rear, rounded_prism("pcb-cavity", 64.0, 98.5, 3.4, -1.2, 10.3, y=9.25))
subtract(rear, rounded_prism("chin-cavity", 64, 11.5, 3.4, -1.2, 10.3, y=-42.25))
# Each cutter reaches past the outer wall at x=+/-34. The earlier shallow
# pockets left these ports sealed by several millimetres of plastic.
subtract(rear, box("usb-c-opening", (10, 11, 6), (34, 36.3, 1.8)))
subtract(rear, box("micro-sd-opening", (10, 15, 6), (-34, -18.5, 1.8)))
subtract(rear, box("power-switch-opening", (11, 9, 6), (33.5, 14.1, 1.8)))
shelf = rounded_prism("battery-shelf", 31, 38, 2, 3.9, 4.2, x=16, y=-10)
shelf.data.materials.append(material("battery-shelf-plastic", (0.075, 0.08, 0.085)))
# The notch faces BT1, below the pack. The lead, strain relief, and shelf
# support are not modeled; all vertical clearances need physical validation.
subtract(shelf, box("battery-lead-passage", (9, 5, 1), (23, -29, 4.05)))
back = rounded_prism("translucent-back-preview", 68, 109.5, 5.0, 10.2, 12.4, y=5.75)
back.data.materials.append(material("graphite-back-preview", (0.055, 0.06, 0.065), 0.23))
export("rear-tray.glb", [rear, shelf])
export("rear-cover.glb", [back])

# A separate, static visualization of a side-access thumb slider for SW7.
# Its inner bar reaches the switch and the outer tab moves along Y through
# the side slot. Guide rails, switch coupling, travel, and tolerances remain
# to be validated before this can be fabricated as a working mechanism.
reset_scene()
slider_material = material("power-slider-plastic", (0.14, 0.15, 0.16))
slider_bar = box("power-slider-bar", (8.4, 1.8, 2.0), (31.0, 14.1, 2.4))
slider_bar.data.materials.append(slider_material)
slider_tab = box("power-slider-thumb", (2.2, 5.0, 3.2), (34.4, 14.1, 2.4))
slider_tab.data.materials.append(slider_material)
export("power-slider.glb", [slider_bar, slider_tab])

# Nominal body size of Adafruit 1578, not a validated fit or swelling envelope.
reset_scene()
cell = rounded_prism("Adafruit-1578-nominal-envelope", 29, 36, 1.4, 4.2, 8.95, x=16, y=-10)
cell.data.materials.append(material("battery-envelope", (0.45, 0.49, 0.53), 0.65))
export("battery-envelope.glb", [cell])
