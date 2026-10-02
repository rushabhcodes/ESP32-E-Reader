"""Check printable case surfaces against the tsci-exported component meshes.

Run: blender --background --python scripts/check-enclosure-clearance.py -- FILE.glb
The PCB and mating case pieces intentionally touch. Missing component models
and real-world tolerances remain outside the scope of this triangle check.
"""

import json
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Matrix
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

report = {
    'input_glb': str(INPUT),
    'modeled_component_shell_intersections': sorted(hits),
    'modeled_component_partition_intersections': sorted(partition_hits),
    'modeled_component_button_intersections': sorted(button_hits),
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
    'unmodeled': ['USB-C J1 body placement', 'display FPC', 'battery lead and plug',
                  'solder fillets', 'battery dimensional tolerance or swelling',
                  'printer material shrinkage'],
}
(STL / 'clearance-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
if hits or partition_hits or button_hits or any(report['button_shell_solid_overlap_mm3']) or report['battery_shell_surface_intersections'] or report['battery_cover_surface_intersections'] or any(report['solid_overlap_mm3'].values()):
    raise RuntimeError('Case/model clearance check failed')
