"""Render the open right-side power-switch access concept.

Run after generating the enclosure GLBs:
blender --background --python scripts/render-power-access-preview.py
"""

from pathlib import Path

import bpy
from mathutils import Vector


root = Path(__file__).resolve().parents[1]
assets = root / "assets" / "enclosure"

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for filename, color in (
    ("front-bezel.glb", (0.08, 0.08, 0.09, 1)),
    ("rear-tray.glb", (0.11, 0.11, 0.12, 1)),
    ("power-slider.glb", (0.52, 0.53, 0.55, 1)),
):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(assets / filename))
    for obj in set(bpy.data.objects) - before:
        if obj.type == "MESH":
            obj.color = color

# The GLB import maps board (x, y, z) to Blender (x, -z, y). Looking from
# positive X and negative Y exposes the case's right wall and open back.
target = Vector((32, -2, 14))
bpy.ops.object.camera_add(location=(145, -55, 22))
camera = bpy.context.object
camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Z").to_euler()
camera.data.type = "ORTHO"
camera.data.ortho_scale = 70

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.color_type = "OBJECT"
scene.display.shading.light = "STUDIO"
scene.display.shading.show_cavity = True
scene.render.resolution_x = 900
scene.render.resolution_y = 650
scene.render.resolution_percentage = 100
scene.render.filepath = str(assets / "power-access-preview.png")
bpy.ops.render.render(write_still=True)
