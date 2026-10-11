"""Inspect reference G-code bounds, layer coverage and spring toolpaths.

Run after check-printability.py. Draws actual extruded XY moves at selected
heights; it does not simulate deposited plastic or predict fatigue/fit.
"""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
import math
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "checks/printability"
ASSETS = ROOT / "assets/enclosure"
SPEC = json.loads((ASSETS / "display-connection.json").read_text())
CASE_Y = SPEC["case"]["centerY"]
COLORS = {"model": "#236a9e", "support": "#b27c26", "bridge": "#a63963"}

def read_moves(path):
    layers = defaultdict(list)
    xyz = [0., 0., 0.]
    e = 0.
    relative_e = False
    relative_xyz = False
    kind = ""
    for line in path.read_text().splitlines():
        if line.startswith(";TYPE:"):
            kind = line[6:].strip().lower()
        code = line.split(";")[0].strip()
        if not code:
            continue
        cmd = code.split()[0]
        words = {k: float(v) for k, v in re.findall(r"([XYZE])(-?(?:\d+(?:\.\d*)?|\.\d+))", code)}
        if cmd in ("M82", "M83"):
            relative_e = cmd == "M83"
        if cmd in ("G90", "G91"):
            relative_xyz = cmd == "G91"
        if cmd == "G92" and "E" in words:
            e = words["E"]
        if cmd not in ("G0", "G1", "G2", "G3"):
            continue
        previous = xyz[:]
        for i, axis in enumerate("XYZ"):
            if axis in words:
                xyz[i] = words[axis] + (xyz[i] if relative_xyz else 0)
        delta = 0.
        if "E" in words:
            delta = words["E"] if relative_e else words["E"] - e
            e = words["E"] if not relative_e else e + words["E"]
        if delta <= 0 or math.dist(previous[:2], xyz[:2]) < 1e-6 or not kind:
            continue
        assert cmd in ("G0", "G1"), "Arc toolpaths need a different inspector"
        layers[round(xyz[2], 3)].append((previous[:2], xyz[:2], kind))
    return dict(sorted(layers.items()))

def covers(moves, bounds):
    # Presence of an actual extrusion in a region; not a strength calculation.
    return any(bounds[0] <= (a[0] + b[0]) / 2 <= bounds[1]
               and bounds[2] <= (a[1] + b[1]) / 2 <= bounds[3]
               and "support" not in kind for a, b, kind in moves)

data = {}
for name in ("front-chassis", "rear-cover", "reader-print-plate"):
    path = OUT / (name + ".gcode")
    layers = read_moves(path)
    points = [p for moves in layers.values() for a, b, _ in moves for p in (a, b)]
    bounds = [[min(p[i] for p in points), max(p[i] for p in points)] for i in (0, 1)]
    assert all(0 <= low <= high <= 220 for low, high in bounds), (name, bounds)
    assert min(layers) == .2 and all(0 < z <= 250 for z in layers), name
    assert not any(b - a > .401 for a, b in zip(layers, list(layers)[1:])), name
    data[name] = {"gcode_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                  "extrusion_bounds_xy_mm": bounds, "extrusion_z_range_mm": [min(layers), max(layers)],
                  "extrusion_layers": len(layers), "extruded_xy_moves": sum(map(len, layers.values())),
                  "reference_bed_bounds_pass": True}
    if name == "front-chassis":
        spring_layers = {}
        # Centered STL: original world Y maps to print Y + (110 - CASE_Y).
        for x in SPEC["controls"]["navigationX"]:
            box = (110 + x - 4.5, 110 + x + 4.5, 110 - CASE_Y - 46.8, 110 - CASE_Y - 45.8)
            levels = [z for z, moves in layers.items() if 1.0 <= z <= 1.9 and covers(moves, box)]
            assert len(levels) >= 4, ("Key spring lost during slicing", x, levels)
            spring_layers[str(x)] = levels
        data[name]["key_leaf_toolpath_layers"] = spring_layers
        screen_leaves = {}
        for side in (-1, 1):
            for tip in SPEC['case']['screenClipTipY']:
                x, y = 110 + side * 29.3, 110 - CASE_Y + tip + 7
                levels = [z for z, moves in layers.items() if 2.7 <= z <= 3.9
                          and covers(moves, (x - .3, x + .3, y - 3, y + 3))]
                assert len(levels) >= 4, ("Screen leaf lost", side, tip, levels)
                screen_leaves[f"{side},{tip}"] = levels
        data[name]["six_screen_leaf_toolpath_layers"] = screen_leaves
    if name == "rear-cover":
        snaps = {}
        for side in (-1, 1):
            for tip in (-5., 24.):
                x, y = 110 + side * 32.6, 110 + CASE_Y - tip - 7.05
                levels = [z for z, moves in layers.items() if 3.0 <= z <= 6.3
                          and covers(moves, (x - .3, x + .3, y - 3, y + 3))]
                assert len(levels) >= 10, ("Cover snap leaf lost", side, tip, levels)
                snaps[f"{side},{tip}"] = levels
        data[name]["four_cover_snap_toolpath_layers"] = snaps
        supports = {}
        for x in (-12., 12.):
            levels = [z for z, moves in layers.items() if 12 <= z <= 14.2
                      and covers(moves, (110 + x - 3, 110 + x + 3, 110 + CASE_Y - SPEC["case"]["topSupportY"] - .4, 110 + CASE_Y - SPEC["case"]["topSupportY"] + .4))]
            assert len(levels) >= 8, ("Upper screen support lost", x, levels)
            supports[str(x)] = levels
        data[name]["two_upper_screen_support_toolpath_layers"] = supports
    if name == "reader-print-plate":
        continue
    selected = (.2, 1.4, 2.6, 3.6) if name == "front-chassis" else (.2, 5.8, 7.6, 10.2)
    canvas = Image.new("RGB", (1360, 690), "#f5f2ed")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 16)
    small = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 12)
    draw.text((22, 16), name + " — actual reference toolpaths", font=font, fill="#222222")
    draw.text((22, 44), "Blue: model   Gold: removable supports   Pink: bridges | 0.4 mm nozzle / 0.2 mm layers / PETG", font=small, fill="#444444")
    for column, target in enumerate(selected):
        z = min(layers, key=lambda level: abs(level - target))
        ox, oy = 22 + 335 * column, 110
        draw.text((ox, 76), f"Layer at Z {z:.2f} mm", font=font, fill="#222222")
        for a, b, kind in layers[z]:
            color = COLORS["support" if "support" in kind else "bridge" if "bridge" in kind else "model"]
            draw.line([(ox + (p[0] - 68) * 3.7, oy + (177 - p[1]) * 3.7) for p in (a, b)], fill=color, width=2)
    draw.text((22, 645), "Reference slice preview. Select and validate your own printer preset before printing.", font=small, fill="#444444")
    canvas.save(OUT / (name + "-toolpaths.png"))
report = {"status": "reference_toolpaths_inspected", "parts_and_plate": data,
          "scope": "Actual extrusion bounds, layer coverage, four key springs, six screen leaves, four cover snaps and two upper screen supports checked for toolpath presence. Selected layers rendered for visual review. Support removal, printed fit, snap force and fatigue need a prototype; this is not machine-ready G-code."}
(ASSETS / "stl/toolpath-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
