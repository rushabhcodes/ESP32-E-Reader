"""Check printable case surfaces against the tsci-exported component meshes.

Run: blender --background --python scripts/check-enclosure-clearance.py -- FILE.glb
The PCB and mating case pieces intentionally touch. Missing component models
and real-world tolerances remain outside the scope of this triangle check.
"""

import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

ROOT = Path(__file__).resolve().parents[1]
STL = ROOT / 'assets/enclosure/stl'
INPUT = Path(sys.argv[sys.argv.index('--') + 1])


def read_mesh(path):
    bpy.ops.wm.stl_import(filepath=str(path))
    return bpy.context.object


def tree(obj):
    mesh = bmesh.new()
    mesh.from_mesh(obj.data)
    mesh.transform(obj.matrix_world)
    result = BVHTree.FromBMesh(mesh)
    mesh.free()
    return result


def solid_intersection_volume(a, b):
    test = a.copy()
    test.data = a.data.copy()
    bpy.context.collection.objects.link(test)
    bpy.context.view_layer.objects.active = test
    modifier = test.modifiers.new('overlap', 'BOOLEAN')
    modifier.operation = 'INTERSECT'
    modifier.solver = 'EXACT'
    modifier.object = b
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh = bmesh.new()
    mesh.from_mesh(test.data)
    volume = abs(mesh.calc_volume(signed=True))
    mesh.free()
    bpy.data.objects.remove(test, do_unlink=True)
    return round(volume, 6)


def read_usb_body():
    """Place the checked-in GCT OBJ using J1's circuit-JSON CAD transform."""
    circuit = json.loads((ROOT / 'dist/index/circuit.json').read_text())
    source = next(item for item in circuit if item.get('type') == 'source_component' and item.get('name') == 'J1')
    cad = next(item for item in circuit if item.get('type') == 'cad_component' and item.get('source_component_id') == source['source_component_id'])
    path = ROOT / 'imports/USB4105_GF_A/USB4105_GF_A.obj'
    vertices, faces = [], []
    for line in path.read_text().splitlines():
        if line.startswith('v '):
            vertices.append(tuple(float(value) for value in line.split()[1:4]))
        elif line.startswith('f '):
            faces.append(tuple(int(token.split('/')[0]) - 1 for token in line.split()[1:]))
    mesh = bpy.data.meshes.new('J1 manufacturer OBJ')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new('J1 USB-C body', mesh)
    bpy.context.collection.objects.link(obj)
    pos, origin = cad['position'], cad['model_origin_position']
    obj.matrix_world = (
        Matrix.Translation(Vector((pos['x'], pos['y'], pos['z'])))
        @ Matrix.Rotation(math.radians(cad['rotation']['z']), 4, 'Z')
        @ Matrix.Translation(Vector((-origin['x'], -origin['y'], -origin['z'])))
    )
    return obj


shell = read_mesh(STL / 'front-shell.stl')
partition = read_mesh(STL / 'battery-partition.stl')
cover = read_mesh(STL / 'rear-cover.stl')
cell = read_mesh(STL / 'battery-envelope-DO-NOT-PRINT.stl')
buttons = [read_mesh(STL / f'button-{i}.stl') for i in range(1, 5)]
shell_tree = tree(shell)
partition_tree = tree(partition)
cover_tree = tree(cover)
cell_tree = tree(cell)
button_trees = [tree(button) for button in buttons]

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(INPUT))
# The tsci CLI GLB imports into Blender as (-PCB X, -PCB Y, PCB Z).
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
hits = []
partition_hits = []
button_hits = []
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH' or obj.name in ('Box0', 'MeshWithTextures0', 'EPD1'):
        continue
    obj.matrix_world = conversion @ obj.matrix_world
    component_tree = tree(obj)
    if component_tree.overlap(shell_tree):
        hits.append(obj.name)
    if component_tree.overlap(partition_tree):
        partition_hits.append(obj.name)
    if any(component_tree.overlap(button_tree) for button_tree in button_trees):
        button_hits.append(obj.name)

usb_body = read_usb_body()
usb_tree = tree(usb_body)
usb_hits = {
    'shell': bool(usb_tree.overlap(shell_tree)),
    'partition': bool(usb_tree.overlap(partition_tree)),
    'cover': bool(usb_tree.overlap(cover_tree)),
}

report = {
    'input_glb': str(INPUT),
    'modeled_component_shell_intersections': sorted(hits),
    'modeled_component_partition_intersections': sorted(partition_hits),
    'modeled_component_button_intersections': sorted(button_hits),
    'usb_c_body_intersections': usb_hits,
    'button_shell_solid_overlap_mm3': [solid_intersection_volume(button, shell) for button in buttons],
    'battery_shell_surface_intersections': len(cell_tree.overlap(shell_tree)),
    'battery_cover_surface_intersections': len(cell_tree.overlap(cover_tree)),
    'solid_overlap_mm3': {
        'shell_partition': solid_intersection_volume(shell, partition),
        'shell_cover': solid_intersection_volume(shell, cover),
        'shell_battery': solid_intersection_volume(shell, cell),
        'partition_battery': solid_intersection_volume(partition, cell),
        'cover_battery': solid_intersection_volume(cover, cell),
    },
    'expected_part_contacts': {
        'partition_on_shell_ledges': bool(partition_tree.overlap(shell_tree)),
        'battery_on_partition': bool(cell_tree.overlap(partition_tree)),
        'cover_on_shell': bool(cover_tree.overlap(shell_tree)),
    },
    'unmodeled': ['display FPC', 'antenna coax and plug',
                  'battery lead and plug',
                  'solder fillets', 'battery dimensional tolerance or swelling',
                  'printer material shrinkage'],
}
(STL / 'clearance-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if hits or partition_hits or button_hits or any(usb_hits.values()) or any(report['button_shell_solid_overlap_mm3']) or report['battery_shell_surface_intersections'] or report['battery_cover_surface_intersections'] or any(report['solid_overlap_mm3'].values()):
    raise RuntimeError('Case/model clearance check failed')
