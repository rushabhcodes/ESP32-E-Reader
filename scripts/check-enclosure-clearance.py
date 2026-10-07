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
PCB_MOUNTS = json.loads((ROOT / 'assets/enclosure/pcb-mounts.json').read_text())


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


def cylinder(name, diameter, low, high, x, y):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=diameter / 2, depth=high - low,
        location=(x, y, (low + high) / 2))
    obj = bpy.context.object
    obj.name = name
    return obj


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

# Check real exported surfaces at both ends of the nominal switch stroke.
pressed_cap_shell_overlap = []
for button in buttons:
    button.location.z += PCB_MOUNTS['buttonTravel']
    bpy.context.view_layer.update()
    pressed_cap_shell_overlap.append(solid_intersection_volume(button, shell))
    button.location.z -= PCB_MOUNTS['buttonTravel']
bpy.context.view_layer.update()

mount_supports = []
for mount in PCB_MOUNTS['mounts']:
    x, y = mount['x'], mount['y']
    origin = Vector((x, y, .5))
    floor, _, _, _ = shell_tree.ray_cast(origin, Vector((0, 0, -1)))
    support_heights = []
    for dx, dy in ((1.7, 0), (-1.7, 0), (0, 1.7), (0, -1.7)):
        hit, _, _, _ = shell_tree.ray_cast(
            Vector((x + dx, y + dy, .5)), Vector((0, 0, -1)))
        support_heights.append(round(hit.z, 5) if hit is not None else None)
    correct = (
        floor is not None and floor.z <= mount['pilotBaseZ'] + .01
        and all(z is not None and abs(z - PCB_MOUNTS['supportZ']) < .001
                for z in support_heights))
    mount_supports.append({'name': mount['name'], 'pilot_floor_z':
                           round(floor.z, 5) if floor is not None else None,
                           'support_heights_z': support_heights, 'passed': correct})

before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=str(INPUT))
# The tsci CLI GLB imports into Blender as (-PCB X, -PCB Y, PCB Z).
conversion = Matrix(((-1, 0, 0, 0), (0, -1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)))
hits = []
partition_hits = []
button_hits = []
component_objects = []
# Case parts are checked from the exported STLs above. CLI GLB assembly
# nodes can contain fallback cubes when a preview asset cannot be fetched.
assembly_nodes = {'EPD1', 'battery_envelope', 'wifi_antenna_envelope',
                  'front_shell', 'battery_partition', 'rear_cover',
                  'button_1', 'button_2', 'button_3', 'button_4'}
for obj in set(bpy.data.objects) - before:
    if obj.type != 'MESH' or obj.name in {'Box0', 'MeshWithTextures0', *assembly_nodes}:
        continue
    obj.matrix_world = conversion @ obj.matrix_world
    component_objects.append(obj)
    component_tree = tree(obj)
    if component_tree.overlap(shell_tree):
        hits.append(obj.name)
    if component_tree.overlap(partition_tree):
        partition_hits.append(obj.name)
    if any(component_tree.overlap(button_tree) for button_tree in button_trees):
        button_hits.append(obj.name)

usb_body = read_usb_body()
component_objects.append(usb_body)
usb_tree = tree(usb_body)
usb_hits = {
    'shell': bool(usb_tree.overlap(shell_tree)),
    'partition': bool(usb_tree.overlap(partition_tree)),
    'cover': bool(usb_tree.overlap(cover_tree)),
}

screw_checks = []
for mount in PCB_MOUNTS['mounts']:
    x, y = mount['x'], mount['y']
    head = cylinder(mount['name'] + '-head-envelope',
                    PCB_MOUNTS['screwHeadDiameter'], .8,
                    .8 + PCB_MOUNTS['screwHeadHeight'], x, y)
    shaft = cylinder(mount['name'] + '-shaft-envelope', 2.5,
                     .8 - PCB_MOUNTS['screwLength'], .8, x, y)
    head_tree = tree(head)
    head_hits = [obj.name for obj in [shell, partition, cover, cell, *component_objects]
                 if head_tree.overlap(tree(obj))]
    # PCB screws are installed before the partition, battery and cover.
    # Check the full tool approach through fixed shell posts and ledges.
    driver = cylinder(mount['name'] + '-driver-access-envelope',
                      PCB_MOUNTS['driverDiameter'],
                      .8 + PCB_MOUNTS['screwHeadHeight'], 20.0, x, y)
    driver_tree = tree(driver)
    driver_hits = [obj.name for obj in [shell, *component_objects]
                   if driver_tree.overlap(tree(obj))]
    cap_overlaps = []
    for button in buttons:
        button.location.z += PCB_MOUNTS['buttonTravel']
        bpy.context.view_layer.update()
        cap_overlaps.append(solid_intersection_volume(shaft, button))
        button.location.z -= PCB_MOUNTS['buttonTravel']
    bpy.context.view_layer.update()
    screw_checks.append({'name': mount['name'], 'head_intersections': head_hits,
                         'driver_access_intersections': driver_hits,
                         'shaft_pressed_cap_overlap_mm3': cap_overlaps})
    bpy.data.objects.remove(head, do_unlink=True)
    bpy.data.objects.remove(shaft, do_unlink=True)
    bpy.data.objects.remove(driver, do_unlink=True)

report = {
    'input_glb': str(INPUT),
    'modeled_component_mesh_count': len(component_objects),
    'modeled_component_shell_intersections': sorted(hits),
    'modeled_component_partition_intersections': sorted(partition_hits),
    'modeled_component_button_intersections': sorted(button_hits),
    'usb_c_body_intersections': usb_hits,
    'button_shell_solid_overlap_mm3': [solid_intersection_volume(button, shell) for button in buttons],
    'pressed_button_shell_solid_overlap_mm3': pressed_cap_shell_overlap,
    'pcb_mount_supports': mount_supports,
    'pcb_screw_clearance': screw_checks,
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
if (hits or partition_hits or button_hits or any(usb_hits.values())
    or any(report['button_shell_solid_overlap_mm3']) or any(pressed_cap_shell_overlap)
    or not all(mount['passed'] for mount in mount_supports)
    or any(check['head_intersections'] or check['driver_access_intersections']
           or any(check['shaft_pressed_cap_overlap_mm3'])
           for check in screw_checks)
    or report['battery_shell_surface_intersections']
    or report['battery_cover_surface_intersections']
    or any(report['solid_overlap_mm3'].values())):
    raise RuntimeError('Case/model clearance check failed')
