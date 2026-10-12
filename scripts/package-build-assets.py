"""Keep lossless text backups of CAD/print binaries omitted by Git imports."""
from pathlib import Path
import base64
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/enclosure/binary-sources'
OUT.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted((ROOT / 'assets/enclosure').rglob('*')):
    if path.suffix not in ('.glb', '.stl') or not path.is_file():
        continue
    data = path.read_bytes()
    relative = path.relative_to(ROOT).as_posix()
    filename = hashlib.sha256(relative.encode()).hexdigest()[:16] + '.json'
    source = 'assets/enclosure/binary-sources/' + filename
    encoded = {'path': relative, 'bytes': len(data),
               'sha256': hashlib.sha256(data).hexdigest(),
               'gzip_base64': base64.b64encode(gzip.compress(data, compresslevel=9, mtime=0)).decode()}
    (OUT / filename).write_text(json.dumps(encoded, separators=(',', ':')) + '\n')
    records.append({'path': relative, 'source': source, 'bytes': len(data), 'sha256': encoded['sha256']})
(OUT / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
print(f'Backed up {len(records)} CAD/print binaries; original hashes preserved')
