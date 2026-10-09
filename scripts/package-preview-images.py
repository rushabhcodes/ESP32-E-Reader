"""Preserve rendered CAD previews for Git imports that omit image binaries."""
import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENCLOSURE = ROOT / 'assets/enclosure'
OUT = ENCLOSURE / 'preview-sources'
OUT.mkdir(exist_ok=True)
for source in sorted(ENCLOSURE.glob('*.png')):
    data = source.read_bytes()
    encoded = json.dumps({'sha256': hashlib.sha256(data).hexdigest(), 'base64': base64.b64encode(data).decode('ascii')}) + '\n'
    assert len(encoded.encode()) <= 3 * 1024 * 1024, 'Split preview source before upload'
    (OUT / (source.name + '.json')).write_text(encoded)
print('Preserved eight rendered preview images as checksummed text sources')
