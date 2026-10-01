"""Render the display side of the current 3D assembly with Blender.

Run `tsci build index.circuit.tsx` first, then:
blender --background --python scripts/render-front-preview.py
"""

import json
import math
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
circuits = json.loads((ROOT / "dist" / "index" / "circuit.json").read_text())
names = {
    item["source_component_id"]: item.get("name")
    for item in circuits
    if item["type"] == "source_component"
}
visible = ("front_bezel", "button_caps_preview", "EPD1")
models = {
    names.get(item.get("source_component_id")): item
    for item in circuits
    if item["type"] == "cad_component"
}

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for name in visible:
    item = models[name]
    url = item.get("model_glb_url")
    if not url:
        continue
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(ROOT / url))
    position = item["position"]
    # These exported GLBs use the board's Z-up frame. Blender's GLB importer
    # maps board (x, y, z) to Blender (x, -z, y).
    shift = Vector((position["x"], -position["z"], position["y"]))
    for obj in set(bpy.data.objects) - before:
        obj.location += shift
        if obj.type != "MESH":
            continue
        if "active-area" in obj.name:
            obj.color = (0.88, 0.85, 0.75, 1)
        elif "button-cap" in obj.name:
            obj.color = (0.32, 0.34, 0.37, 1)
        elif "bezel" in obj.name or "chin" in obj.name or "rim" in obj.name:
            obj.color = (0.04, 0.04, 0.05, 1)
        else:
            obj.color = (0.14, 0.14, 0.15, 1)

bpy.ops.object.camera_add(location=(0, 170, 0))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, -0.5)) - camera.location).to_track_quat(
    "-Z", "Z"
).to_euler()
camera.rotation_euler.rotate_axis("Z", math.pi)
camera.data.type = "ORTHO"
camera.data.ortho_scale = 140

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.color_type = "OBJECT"
scene.display.shading.light = "STUDIO"
scene.display.shading.show_cavity = True
scene.render.resolution_x = 800
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.filepath = str(ROOT / "assets" / "enclosure" / "front-preview.png")
bpy.ops.render.render(write_still=True)
