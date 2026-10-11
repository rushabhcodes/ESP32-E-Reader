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


def flex_sections():
    """Fold at the OEM positioning line and wrap outside the PCB bottom edge.

    The material coordinate follows the drawing's 33.66 mm flat projection.
    A physical sample must establish the allowable installed bend radius.
    """
    from math import acos
    panel, connector, flex = (SPEC[key] for key in ("panel", "connector", "flex"))
    root_y = panel["centerY"] - panel["height"] / 2
    r, root_z, route_z = flex["bendRadius"], flex["rootZ"], flex["routingZ"]
    flat = flex["flatRootLength"]
    bend_y = root_y - flat
    outside_y = bend_y - r
    assert abs(outside_y - SPEC["route"]["bendCenterY"]) < 1e-6
    arc = r * pi / 2
    vertical = route_z - root_z - 2 * r
    assert vertical > 0
    return_s = flat + 2 * arc + vertical
    angle = acos(1 - (route_z - flex["entryZ"]) / (2 * r))
    settle_end = flex["settleAtLength"]
    settle_start = settle_end - 2 * r * angle
    assert settle_start > return_s
    def point(s):
        if s <= flat:
            return (s, root_y - s, root_z)
        if s <= flat + arc:
            a = (s - flat) / r
            return (s, bend_y - r * sin(a), root_z + r * (1 - cos(a)))
        if s <= flat + arc + vertical:
            return (s, outside_y, root_z + r + s - flat - arc)
        if s <= return_s:
            a = (s - flat - arc - vertical) / r
            return (s, outside_y + r * (1 - cos(a)), route_z - r + r * sin(a))
        if s <= settle_start:
            return (s, bend_y + s - return_s, route_z)
        start_y = bend_y + settle_start - return_s
        if s <= settle_start + r * angle:
            a = (s - settle_start) / r
            return (s, start_y + r * sin(a), route_z - r * (1 - cos(a)))
        if s <= settle_end:
            a = (s - settle_start - r * angle) / r
            return (s, start_y + r * (2 * sin(angle) - sin(angle - a)), route_z - r * (1 - cos(angle)) - r * (cos(angle - a) - cos(angle)))
        return (s, start_y + 2 * r * sin(angle) + s - settle_end, flex["entryZ"])
    samples = {0., 3.95, 8., flat, flat + arc, flat + arc + vertical,
               return_s, settle_start, settle_end,
               flex["nominalTailLength"] - flex["stiffenerLength"], flex["nominalTailLength"]}
    for boundary in (flex["wingStartLength"], flex["wingEndLength"]):
        samples.update((boundary - 1e-5, boundary, boundary + 1e-5))
    for low, high in ((flat, flat + arc), (flat + arc + vertical, return_s), (settle_start, settle_end)):
        samples.update(low + (high - low) * i / 64 for i in range(65))
    sections = [point(s) for s in sorted(samples)]
    tip_y = connector["centerY"] - connector["modelOriginY"] + connector["tipModelY"]
    assert abs(sections[-1][1] - tip_y) < 1e-6
    return sections


def flex_path():
    return [(y, z) for _, y, z in flex_sections()]


def flex_edges(s):
    flex = SPEC["flex"]
    # Envelope of the dimensioned L outline; undimensioned taper corners are nominal.
    if s <= 3.95:
        return (-flex["rootWidth"] / 2, flex["rootWidth"] / 2)
    if s < 8.0:
        half = flex["rootWidth"] / 2 + (flex["width"] / 2 - flex["rootWidth"] / 2) * (s - 3.95) / 4.05
        return (-half, half)
    if s < flex["wingStartLength"]:
        return (flex["wingMinX"], flex["wingMinX"] + flex["neckWidth"])
    if s <= flex["wingEndLength"]:
        return (flex["wingMinX"], flex["wingMaxX"])
    x = SPEC["connector"]["centerX"]
    return (x - flex["width"] / 2, x + flex["width"] / 2)


def material(name, color, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = .45
    return mat


def strip(name, points, width, thickness, color, offset=0, x=0, metallic=0, edges=None):
    vertices, faces = [], []
    for i, (y, z) in enumerate(points):
        a, b = points[max(0, i - 1)], points[min(len(points) - 1, i + 1)]
        dy, dz = b[0] - a[0], b[1] - a[1]
        length = hypot(dy, dz)
        # +Z on the straight mating section. Bottom contacts use -normal.
        ny, nz = -dz / length, dy / length
        left, right = edges[i] if edges else (-width / 2, width / 2)
        for edge_x, edge_t in ((left, -.5), (right, -.5), (right, .5), (left, .5)):
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
    sections = flex_sections()
    path = [(y, z) for _, y, z in sections]
    length = sum(hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:]))
    assert abs(length - flex["nominalTailLength"]) <= flex["tailLengthTolerance"]
    objects = [strip("EPD-flex-polyimide-nominal", path, flex["width"], flex["thickness"], (.72, .36, .045), edges=[flex_edges(s) for s, _, _ in sections])]
    tip_y, tip_z = path[-1]
    objects.append(strip("EPD-flex-tip-stiffener-nominal", [(tip_y - flex["stiffenerLength"], tip_z), (tip_y, tip_z)], flex["width"], flex["stiffenerThickness"], (.12, .26, .46), offset=(flex["thickness"] + flex["stiffenerThickness"]) / 2, x=SPEC["connector"]["centerX"]))
    for i in range(flex["contacts"]):
        # The exact supplier socket has pin 1 on +X. Raw panel pin numbering
        # remains a separate, unresolved supplier/sample check.
        x = SPEC["connector"]["centerX"] + ((flex["contacts"] - 1) / 2 - i) * flex["contactPitch"]
        objects.append(strip(f"EPD-contact-{i + 1:02}", [(tip_y - flex["contactLength"], tip_z), (tip_y, tip_z)], flex["contactWidth"], .01, (.75, .57, .16), offset=-flex["thickness"] / 2 - .005, x=x, metallic=.7))
    return objects, length
