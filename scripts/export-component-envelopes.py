"""Extract modeled assembly component AABBs from tsci-exported GLB.

Run: blender --background --python scripts/export-component-envelopes.py -- FILE.glb
The dimensions are tessellated CAD/model bounds, not component datasheet tolerances.
"""

import csv
import json
from pathlib import Path
import sys

import bpy

ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(sys.argv[sys.argv.index('--') + 1])
OUTPUT = ROOT / 'assets/enclosure/component-envelopes.csv'
data = json.loads((ROOT / 'dist/index/circuit.json').read_text())
source_names = {x['source_component_id']: x['name'] for x in data if x['type'] == 'source_component'}
pcb_refs = {source_names[x['source_component_id']] for x in data if x['type'] == 'pcb_component'}
bpy.ops.import_scene.gltf(filepath=str(INPUT))
rows = []
for obj in bpy.data.objects:
    if obj.type != 'MESH' or not obj.data.vertices or obj.name not in pcb_refs:
        continue
    pts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    # tsci GLB axes: X=-PCB X, Y=-PCB Y, Z=PCB Z.
    xyz = [(-p.x, -p.y, p.z) for p in pts]
    lows = [min(p[i] for p in xyz) for i in range(3)]
    highs = [max(p[i] for p in xyz) for i in range(3)]
    rows.append([obj.name] + [round(v, 3) for pair in zip(lows, highs) for v in pair])
rows.sort(key=lambda row: row[0])
with OUTPUT.open('w', newline='') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(['model_name', 'x_min_mm', 'x_max_mm', 'y_min_mm', 'y_max_mm', 'z_min_mm', 'z_max_mm'])
    writer.writerows(rows)
print(f'{len(rows)} model mesh envelopes -> {OUTPUT}')
