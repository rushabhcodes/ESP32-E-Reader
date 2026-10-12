"""Build the selected battery and its installed two-wire JST-PH connection.

Run with Blender. Published pack dimensions and JST PH drawings define the
envelopes. Cable routing is our installation design, not a supplier drawing.
"""
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/enclosure'
SPEC = json.loads((OUT / 'battery-connection.json').read_text())
DESIGN = json.loads((OUT / 'enclosure-design.json').read_text())

def material(name, color, metallic=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = m.diffuse_color
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = .38
    return m

foil = material('aluminium-polymer-pouch', (.68,.70,.73), .65)
tape = material('amber-protection-tape', (.75,.43,.035))
ink = material('battery-label-ink', (.025,.03,.035))
white = material('JST-PHR-2-natural-nylon', (.88,.86,.79))
red = material('positive-red-insulation', (.65,.014,.018))
black = material('negative-black-insulation', (.018,.022,.026))

def box(name, size, center, mat, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    o = bpy.context.object; o.name = name; o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        m=o.modifiers.new('soft-edges','BEVEL');m.width=bevel;m.segments=3
        bpy.ops.object.modifier_apply(modifier=m.name)
    o.data.materials.append(mat)
    return o

def subtract(o, cutter):
    bpy.context.view_layer.objects.active=o
    m=o.modifiers.new('cavity','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter
    bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.data.objects.remove(cutter,do_unlink=True)

def export(objects, name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.export_scene.gltf(filepath=str(OUT/name),export_format='GLB',export_yup=False,use_selection=True)

def rounded_path(points, radius):
    points=[Vector(p) for p in points]; result=[points[0]]
    for i in range(1,len(points)-1):
        p=points[i];u=(points[i-1]-p).normalized();v=(points[i+1]-p).normalized()
        angle=math.acos(max(-1,min(1,u.dot(v))))
        tangent=radius/math.tan(angle/2)
        # Endpoint segments have one bend; interior segments share two bends.
        tangent=min(tangent,(points[i-1]-p).length*(.9 if i==1 else .45),
                    (points[i+1]-p).length*(.9 if i==len(points)-2 else .45))
        actual_radius=tangent*math.tan(angle/2)
        assert actual_radius>=radius-1e-5,'Waypoints force a smaller cable bend'
        center=p+(u+v).normalized()*actual_radius/math.sin(angle/2)
        a=p+u*tangent;b=p+v*tangent
        va=(a-center).normalized();vb=(b-center).normalized()
        sweep=math.acos(max(-1,min(1,va.dot(vb))))
        axis=va.cross(vb).normalized()
        from mathutils import Quaternion
        for j in range(33):result.append(center+Quaternion(axis,sweep*j/32)@va*actual_radius)
    result.append(points[-1]);return result

def wire(name, points, mat):
    curve=bpy.data.curves.new(name,'CURVE');curve.dimensions='3D'
    curve.bevel_depth=SPEC['leads']['insulationDiameterMm']/2
    curve.bevel_resolution=4;curve.use_fill_caps=True
    spline=curve.splines.new('POLY');spline.points.add(len(points)-1)
    for p,q in zip(spline.points,points):p.co=(*q,1)
    o=bpy.data.objects.new(name,curve);bpy.context.collection.objects.link(o)
    o.data.materials.append(mat);bpy.context.view_layer.objects.active=o
    o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
    return o

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
b=DESIGN['battery'];x,y,z=b['centerX'],b['centerY'],b['baseZ'];w,h,d=SPEC['part']['sizeMm']
assert b['sizeMm']==SPEC['part']['sizeMm'], 'Selected battery does not fit the designed envelope'
# Pouch and tape stay inside the published total pack dimensions.
pouch=box('PRT-13855-foil-pouch',(w,h,d),(x,y,z+d/2),foil,.8)
body=[pouch]
for sx in (-1,1):body.append(box('pouch-edge-tape',(.9,h-1,.025),(x+sx*(w/2-1),y,z+d-.04),tape,.008))
body.append(box('protected-end-tape',(w-1,4,.025),(x,y+h/2-2.3,z+d-.04),tape,.008))
# Flat printed ink sits 0.002 mm above the pouch and needs no external texture.
bpy.ops.object.text_add(location=(x-17,y+8,z+d+.002))
label=bpy.context.object;label.name='PRT-13855-specification-label'
label.data.body='1S LiPo  2000 mAh\n3.7 V / 4.2 V max\nSparkFun PRT-13855'
label.data.size=2.15;label.data.space_line=1.15;label.data.extrude=0
label.data.materials.append(ink);bpy.ops.object.convert(target='MESH');body.append(label)
export(body,'battery-pack.glb')

lengths={};paths={};wires=[]
for key,mat in [('positive',red),('negative',black)]:
    points=rounded_path(SPEC['leads'][key+'Waypoints'],SPEC['leads']['bendRadiusMm'])
    paths[key]=[list(p) for p in points]
    lengths[key]=round(sum((b-a).length for a,b in zip(points,points[1:])),3)
    wires.append(wire('battery-'+key+'-lead',points,mat))
export(wires,'battery-leads.glb')

c=SPEC['connector'];cx=c['centerX'];exit_y=c['wireExitY'];cz=c['contactZ']
# PHR-2: 5.8 mm flange, 4.5 mm thickness, 8 mm total length, 2 mm pitch.
# The smaller inserted body and polarization relief follow the PH drawing.
plug=box('PHR-2-inserted-housing',(4.8,7.0,3.4),(cx,exit_y+4.5,3.55),white,.04)
flange=box('PHR-2-wire-end-flange',(5.8,1.0,4.5),(cx,exit_y+.5,3.3),white,.04)
latch=box('PHR-2-polarizing-latch',(.5,1.4,.3),(cx,-8.85,5.4),white,.03)
plug_parts=[plug,flange,latch]
for px in (c['positiveX'],c['negativeX']):
    for o in plug_parts:subtract(o,box('contact-and-wire-bore',(1.05,9.0,1.15),(px,exit_y+4,cz),white))
export(plug_parts,'battery-plug.glb')
report={'part_number':SPEC['part']['partNumber'],'size_mm':SPEC['part']['sizeMm'],
        'wire_centerline_length_mm':lengths,'wire_paths_mm':paths,
        'required_free_lead_length_mm':2*math.ceil((max(lengths.values())+8)/2),
        'free_length_allowance_mm':8,'scope':SPEC['modelScope']+' '+SPEC['leads']['scope']}
(OUT/'battery-model.json').write_text(json.dumps(report,indent=2)+'\n')
print('Battery model:',lengths,'minimum usable lead length',report['required_free_lead_length_mm'],flush=True)
