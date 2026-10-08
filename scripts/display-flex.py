"""Nominal installed ribbon in PCB millimetres, shared by CAD and fit checks.

The supplier listing defines the 0.5 mm contact pitch; this is installation
geometry, not an OEM model or a verified minimum bend-radius specification.
"""

from math import cos, sin, pi, hypot
from pathlib import Path
import json
import bpy

ROOT = Path(__file__).resolve().parents[1]
SPEC = json.loads((ROOT / "assets/enclosure/display-connection.json").read_text())


def flex_path():
    panel, connector, slot, flex = (SPEC[key] for key in ("panel", "connector", "slot", "flex"))
    root_y = panel["centerY"] - panel["height"] / 2
    root_z, radius, entry_z = flex["rootZ"], flex["bendRadius"], flex["entryZ"]
    assert abs(root_y - radius - slot["centerY"]) < 1e-6
    points = []
    # The tail exits the glass toward -Y, bends up through the slot, then
    # turns toward +Y into the connector; the panel and tip share X=0.
    for step in range(33):
        angle = -pi / 2 - step * pi / 64
        points.append((root_y + radius * cos(angle), root_z + radius + radius * sin(angle)))
    points.append((slot["centerY"], entry_z - radius))
    for step in range(1, 33):
        angle = pi - step * pi / 64
        points.append((slot["centerY"] + radius + radius * cos(angle), entry_z - radius + radius * sin(angle)))
    tip_y = connector["centerY"] - connector["modelOriginY"] + connector["tipModelY"]
    points.append((tip_y, entry_z))
    return points


def material(name, color, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = .45
    return mat


def strip(name, points, width, thickness, color, offset=0, x=0, metallic=0):
    vertices, faces = [], []
    for i, (y, z) in enumerate(points):
        a, b = points[max(0, i - 1)], points[min(len(points) - 1, i + 1)]
        dy, dz = b[0] - a[0], b[1] - a[1]
        length = hypot(dy, dz)
        # +Z on the straight mating section. Bottom contacts use -normal.
        ny, nz = -dz / length, dy / length
        for edge_x, edge_t in ((-width / 2, -.5), (width / 2, -.5), (width / 2, .5), (-width / 2, .5)):
            t = offset + edge_t * thickness
            vertices.append((x + edge_x, y + ny * t, z + nz * t))
        if i:
            previous, current = (i - 1) * 4, i * 4
            for j in range(4):
                k = (j + 1) % 4
                faces.append((previous + j, previous + k, current + k, current + j))
    faces += [(3, 2, 1, 0), tuple(range(len(vertices) - 4, len(vertices)))]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material(name, color, metallic))
    obj.color = (*color, 1)
    return obj


def create_flex():
    flex = SPEC["flex"]
    path = flex_path()
    length = sum(hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))
    assert abs(length - flex["nominalTailLength"]) <= flex["tailLengthTolerance"]
    objects = [strip("EPD-flex-polyimide-nominal", path, flex["width"], flex["thickness"], (.72, .36, .045))]
    tip_y, tip_z = path[-1]
    objects.append(strip("EPD-flex-tip-stiffener-nominal", [(tip_y - flex["stiffenerLength"], tip_z), (tip_y, tip_z)], flex["width"], flex["stiffenerThickness"], (.12, .26, .46), offset=(flex["thickness"] + flex["stiffenerThickness"]) / 2))
    for i in range(flex["contacts"]):
        # J2 pin 1 lies at +X in the imported footprint's orientation.
        x = ((flex["contacts"] - 1) / 2 - i) * flex["contactPitch"]
        objects.append(strip(f"EPD-contact-{i + 1:02}", [(tip_y - flex["contactLength"], tip_z), (tip_y, tip_z)], flex["contactWidth"], .01, (.75, .57, .16), offset=-flex["thickness"] / 2 - .005, x=x, metallic=.7))
    return objects, length
