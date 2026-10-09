"""Preserve original STEP sources in standard ZIPs below registry request limits."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
from io import BytesIO
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/components'
LIMIT=2*1024*1024
sources=[*sorted(OUT.glob('*.step')),ROOT/'imports/USB4105_GF_A/USB4105_GF_A.step']
manifest=OUT/'sources.json'
def archive(paths):
    data=BytesIO()
    with ZipFile(data,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in [*paths,manifest]:
            info=ZipInfo(p.relative_to(ROOT).as_posix(),date_time=(1980,1,1,0,0,0))
            info.compress_type=ZIP_DEFLATED
            z.writestr(info,p.read_bytes(),compresslevel=9)
    return data.getvalue()
groups=[];current=[]
for p in sources:
    if current and len(archive([*current,p]))>LIMIT:groups.append(current);current=[]
    current.append(p)
if current:groups.append(current)
records=[]
for i,group in enumerate(groups,1):
    data=archive(group);assert len(data)<=LIMIT
    name=f'supplier-step-models-{i}.zip';(OUT/name).write_bytes(data)
    records.append({'path':'assets/components/'+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'step_files':[p.relative_to(ROOT).as_posix() for p in group]})
(OUT/'supplier-step-archives.json').write_text(json.dumps(records,indent=2)+'\n')
(OUT/'supplier-step-models.zip').unlink(missing_ok=True)
subprocess.run(['bun',str(ROOT/'scripts/prepare-preview-archives.mjs'),'--supplier'],cwd=ROOT,check=True)
print('Packaged',len(sources),'original STEP models in',len(records),'standard ZIPs within registry request limits')
