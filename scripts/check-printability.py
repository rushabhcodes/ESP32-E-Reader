"""Slice each oriented part and the 3MF plate with a reference FDM profile.

Usage: python3 scripts/check-printability.py [path-to-prusa-slicer]
G-code stays in ignored checks/printability; select a real printer preset for use.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, math, os, re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets/enclosure';OUT=ROOT/'checks/printability';OUT.mkdir(parents=True,exist_ok=True)
EXE=sys.argv[1] if len(sys.argv)>1 else shutil.which('prusa-slicer')
if not EXE:raise RuntimeError('PrusaSlicer CLI is required for toolpath validation')
version=subprocess.run([EXE,'--help'],capture_output=True,text=True,check=True).stdout.splitlines()[0]
parts=sorted((ASSETS/'print').glob('*.stl'));assert len(parts)==2

def slice_part(source):
    name=source.stem;gcode=OUT/(name+'.gcode')
    args=[EXE,'--load',str(ASSETS/'fdm-reference.ini'),'--export-gcode','--output',str(gcode)]
    args += ['--dont-arrange'] if source.suffix=='.3mf' else ['--center','110,110']
    result=subprocess.run([*args,str(source)],capture_output=True,text=True)
    log=result.stdout+result.stderr;(OUT/(name+'.log')).write_text(log)
    assert result.returncode==0,f'{name}: {log}'
    text=gcode.read_text();assert ';LAYER_CHANGE' in text and 'filament used [g]' in text,name
    support_mm=0;kind='';last_e=0;relative=False;xyz={'X':0,'Y':0,'Z':0}
    for line in text.splitlines():
        if line.startswith(';TYPE:'):kind=line[6:].strip().lower()
        if line.startswith('M83'):relative=True
        if line.startswith('M82'):relative=False
        words=dict(re.findall(r'([XYZE])(-?\d+(?:\.\d+)?)',line.split(';')[0]))
        if line.startswith('G92') and 'E' in words:last_e=float(words['E'])
        if not line.startswith(('G0 ','G1 ')):continue
        moving=any(axis in words and abs(float(words[axis])-xyz[axis])>1e-6 for axis in ('X','Y'))
        if 'E' in words:
            value=float(words['E']);delta=value if relative else value-last_e;last_e=value
            if moving and delta>0 and 'support material' in kind:support_mm+=delta
        for axis in xyz:
            if axis in words:xyz[axis]=float(words[axis])
    mass=re.search(r'; filament used \[g\] = ([\d.]+)',text)
    estimate=re.search(r'; estimated printing time \(normal mode\) = (.+)',text)
    warnings=[line for line in log.splitlines() if re.search(r'warning|repaired|error',line,re.I)]
    report={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'layer_change_events':text.count(';LAYER_CHANGE'),'filament_g':float(mass[1]),
            'support_filament_g':round(support_mm*math.pi*(1.75/2)**2*1.27/1000,3),
            'reference_time':estimate[1] if estimate else None,'warnings':warnings,'exit_code':0}
    print(name,report['layer_change_events'],'layer changes, supports',report['support_filament_g'],'g',flush=True)
    return report
with ThreadPoolExecutor(max_workers=2) as pool:reports=list(pool.map(slice_part,parts))
plate=slice_part(ASSETS/'reader-print-plate.3mf')
report={'slicer':version,'nozzle_mm':.4,'layer_mm':.2,'bed_mm':[220,220],
        'profile_sha256':hashlib.sha256((ASSETS/'fdm-reference.ini').read_bytes()).hexdigest(),
        'parts':reports,'plate':plate,'scope':'Toolpath generation only; printer-specific calibration, fit and fatigue remain unverified.'}
(ASSETS/'stl/printability-check.json').write_text(json.dumps(report,indent=2)+'\n')
