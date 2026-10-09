"""Write five bed-oriented STLs, a geometry-only 220 mm 3MF, and a print ZIP.

Binary STL input stays in assembly coordinates. No printer-specific G-code is
shipped; select a printer/PETG profile after importing the 3MF.
"""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
import struct
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/enclosure'
PARTS = [('front-bezel', False, 38, 61), ('main-body', False, 111, 61),
         ('rear-cover', True, 184, 61), ('battery-partition', True, 38, 167),
         ('button-strip', False, 112, 145)]
NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)
def tag(name): return '{'+NS+'}'+name
model = ET.Element(tag('model'), unit='millimeter', **{'xml:lang':'en-US'})
ET.SubElement(model, tag('metadata'), name='Title').text = 'ESP32 Reader Rev. C: five parts, 220 x 220 mm plate'
ET.SubElement(model, tag('metadata'), name='Description').text = 'Geometry only. Select your printer and PETG preset. See PRINTING.md for supports and pilot-hole preparation.'
resources = ET.SubElement(model, tag('resources'))
build = ET.SubElement(model, tag('build'))
(ASSETS/'print').mkdir(exist_ok=True)
for object_id, (name, flip, x, y) in enumerate(PARTS, 1):
    data = (ASSETS/'stl'/f'{name}.stl').read_bytes()
    count = struct.unpack_from('<I',data,80)[0]
    assert len(data)==84+count*50, 'Expected binary STL'
    triangles=[]; normals=[]
    for i in range(count):
        values=struct.unpack_from('<12fH',data,84+i*50)
        transform=lambda p: (p[0],-p[1],-p[2]) if flip else p
        normals.append(transform(values[:3]))
        triangles.append([transform(values[j:j+3]) for j in (3,6,9)])
    points=[p for tri in triangles for p in tri]
    low=[min(p[i] for p in points) for i in range(3)]
    high=[max(p[i] for p in points) for i in range(3)]
    offset=[-(low[0]+high[0])/2, -(low[1]+high[1])/2, -low[2]]
    oriented=[[(p[0]+offset[0],p[1]+offset[1],p[2]+offset[2]) for p in tri] for tri in triangles]
    out=bytearray(b'ESP32 reader bed-oriented STL'.ljust(80,b'\0'))+struct.pack('<I',count)
    for normal,tri in zip(normals,oriented):out.extend(struct.pack('<12fH',*normal,*[c for p in tri for c in p],0))
    (ASSETS/'print'/f'{name}.stl').write_bytes(out)
    obj=ET.SubElement(resources,tag('object'),id=str(object_id),type='model',name=name)
    mesh=ET.SubElement(obj,tag('mesh'));verts=ET.SubElement(mesh,tag('vertices'));tris=ET.SubElement(mesh,tag('triangles'))
    index={}
    for tri in oriented:
        ids=[]
        for p in tri:
            key=tuple(round(v,6) for v in p)
            if key not in index:
                index[key]=len(index)
                ET.SubElement(verts,tag('vertex'),x=str(key[0]),y=str(key[1]),z=str(key[2]))
            ids.append(index[key])
        ET.SubElement(tris,tag('triangle'),v1=str(ids[0]),v2=str(ids[1]),v3=str(ids[2]))
    assert x+low[0]+offset[0]>=0 and x+high[0]+offset[0]<=220
    assert y+low[1]+offset[1]>=0 and y+high[1]+offset[1]<=220
    ET.SubElement(build,tag('item'),objectid=str(object_id),transform=f'1 0 0 0 1 0 0 0 1 {x} {y} 0')
with ZipFile(ASSETS/'reader-print-plate.3mf','w',ZIP_DEFLATED) as package:
    def write_model_file(name, content):
        info=ZipInfo(name, date_time=(1980,1,1,0,0,0));info.compress_type=ZIP_DEFLATED
        package.writestr(info,content)
    write_model_file('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    write_model_file('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    write_model_file('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
with ZipFile(ASSETS/'esp32-reader-printable-stls.zip','w',ZIP_DEFLATED,compresslevel=9) as package:
    for name, *_ in PARTS:
        package.write(ASSETS/'print'/f'{name}.stl',f'{name}.stl')
    for name in ('reader-print-plate.3mf','PRINTING.md','fdm-reference.ini','pcb-mounts.json','display-connection.json','display-retainer.json'):
        package.write(ASSETS/name,name)
print('Packaged five bed-oriented parts and a geometry-only 220 x 220 mm plate')
