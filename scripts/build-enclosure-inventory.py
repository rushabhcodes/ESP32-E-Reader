"""Join tsci PCB placements with modeled component envelopes for case review."""

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'dist/index/circuit.json').read_text())
SOURCE = {x['source_component_id']: x['name'] for x in DATA if x['type'] == 'source_component'}
MODELS = {x['model_name']: x for x in csv.DictReader((ROOT / 'assets/enclosure/component-envelopes.csv').open())}
OUTPUT = ROOT / 'assets/enclosure/component-inventory.csv'


def usb_obj_bounds():
    cad = next(x for x in DATA if x['type'] == 'cad_component' and x.get('source_component_id') == next(
        source_id for source_id, name in SOURCE.items() if name == 'J1'))
    pos, origin = cad['position'], cad['model_origin_position']
    angle = math.radians(cad['rotation']['z'])
    cosine, sine = math.cos(angle), math.sin(angle)
    coords = []
    for line in (ROOT / 'imports/USB4105_GF_A/USB4105_GF_A.obj').read_text().splitlines():
        if line.startswith('v '):
            x, y, z = (float(value) for value in line.split()[1:4])
            x, y, z = x - origin['x'], y - origin['y'], z - origin['z']
            coords.append((pos['x'] + cosine*x - sine*y,
                           pos['y'] + sine*x + cosine*y,
                           pos['z'] + z))
    return [round(max(p[i] for p in coords) - min(p[i] for p in coords), 3) for i in (0, 1)] + [
        round(min(p[2] for p in coords), 3), round(max(p[2] for p in coords), 3)]


J1_BOUNDS = usb_obj_bounds()

with OUTPUT.open('w', newline='') as file:
    w = csv.writer(file, lineterminator='\n')
    w.writerow(['refdes', 'pcb_x_mm', 'pcb_y_mm', 'side', 'pcb_footprint_width_mm', 'pcb_footprint_height_mm',
                'model_width_mm', 'model_length_mm', 'model_z_min_mm', 'model_z_max_mm', 'source'])
    for p in sorted((x for x in DATA if x['type'] == 'pcb_component'), key=lambda x: SOURCE[x['source_component_id']]):
        name = SOURCE[p['source_component_id']]
        model = MODELS.get(name)
        dims = ['', '', '', ''] if model is None else [
            round(float(model['x_max_mm'])-float(model['x_min_mm']), 3),
            round(float(model['y_max_mm'])-float(model['y_min_mm']), 3),
            model['z_min_mm'], model['z_max_mm'],
        ]
        if name == 'J1':
            dims = J1_BOUNDS
        w.writerow([name, round(p['center']['x'], 3), round(p['center']['y'], 3), p['layer'],
                    round(p['width'], 3), round(p['height'], 3), *dims,
                    'GCT manufacturer OBJ, nominal' if name == 'J1' else
                    'tsci tessellated model, nominal' if model else 'PCB footprint only; no 3D body model'])
print(OUTPUT)
