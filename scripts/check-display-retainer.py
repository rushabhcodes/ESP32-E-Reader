"""Compatibility entry point: screen supports and clip insertion are checked together.

Run: blender --background --python-exit-code 1 --python scripts/check-display-retainer.py -- dist/index/assembly.glb
"""
from pathlib import Path
from runpy import run_path
run_path(str(Path(__file__).with_name("check-enclosure-clearance.py")),run_name="__main__")
