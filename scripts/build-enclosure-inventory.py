"""Join tsci PCB placements with modeled component envelopes for case review."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'dist/index/circuit.json').read_text())
SOURCE = {x['source_component_id']: x['name'] for x in DATA if x['type'] == 'source_component'}
MODELS = {x['model_name']: x for x in csv.DictReader((ROOT / 'assets/enclosure/component-envelopes.csv').open())}
OUTPUT = ROOT / 'assets/enclosure/component-inventory.csv'

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
        w.writerow([name, round(p['center']['x'], 3), round(p['center']['y'], 3), p['layer'],
                    round(p['width'], 3), round(p['height'], 3), *dims,
                    'tsci tessellated model, nominal' if model else 'PCB footprint only; no 3D body model'])
print(OUTPUT)
