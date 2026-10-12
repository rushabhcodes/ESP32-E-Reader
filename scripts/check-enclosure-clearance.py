"""Check printable case surfaces against the tsci-exported component meshes.

Run: blender --background --python scripts/check-enclosure-clearance.py -- FILE.glb
Tests enclosure geometry, independent integral keys, screen clips and assembly paths.
Forces, fatigue and manufacturing tolerances remain unverified.
"""

import json
import math
from pathlib import Path
import sys

import bpy
import bmesh
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree

ROOT = Path(__file__).resolve().parents[1]
DISPLAY_SPEC=json.loads((ROOT/'assets/enclosure/display-connection.json').read_text())
DISPLAY_ANCHOR=tuple(DISPLAY_SPEC['connector'][key] for key in ('centerX','centerY','boardSurfaceZ'))
STL = ROOT / 'assets/enclosure/stl'
INPUT = Path(sys.argv[sys.argv.index('--') + 1])
PCB_MOUNTS = json.loads((ROOT / 'assets/enclosure/pcb-mounts.json').read_text())


def read_mesh(path):
    bpy.ops.wm.stl_import(filepath=str(path))
    return bpy.context.object


def tree(obj):
    mesh = bmesh.new()
    mesh.from_mesh(obj.data)
    mesh.transform(obj.matrix_world)
    result = BVHTree.FromBMesh(mesh)
    mesh.free()
    return result


def solid_intersection_volume(a, b):
    test = a.copy()
    test.data = a.data.copy()
    bpy.context.collection.objects.link(test)
    bpy.context.view_layer.objects.active = test
    modifier = test.modifiers.new('overlap', 'BOOLEAN')
    modifier.operation = 'INTERSECT'
    modifier.solver = 'EXACT'
    modifier.object = b
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    mesh = bmesh.new()
    mesh.from_mesh(test.data)
    volume = abs(mesh.calc_volume(signed=True))
    mesh.free()
    if volume>1e-4:
        points=[test.matrix_world@v.co for v in test.data.vertices]
        print('Intersection region:',a.name,b.name,[(round(min(p[i] for p in points),5),round(max(p[i] for p in points),5)) for i in range(3)],flush=True)
    bpy.data.objects.remove(test, do_unlink=True)
    return round(volume, 6)


def cylinder(name, diameter, low, high, x, y):
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64, radius=diameter / 2, depth=high - low,
        location=(x, y, (low + high) / 2))
    obj = bpy.context.object
    obj.name = name
    return obj


EPS=1e-4
CONTACT_EPS_MM=1e-4  # Float32 CAD transforms at intentionally touching seats.
checks=[]
def bounds(o):
    pts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return [(min(p[i] for p in pts),max(p[i] for p in pts)) for i in range(3)]
def overlap(a,b):
    if any(min(x[1],y[1])-max(x[0],y[0])<=CONTACT_EPS_MM for x,y in zip(bounds(a),bounds(b))):return 0.
    ta,tb=tree(a),tree(b)
    if not ta.overlap(tb):
        ray=Vector((.912,.317,.257)).normalized()
        contained=False
        for inner,outer in ((a,tb),(b,ta)):
            center=sum((inner.matrix_world@Vector(v) for v in inner.bound_box),Vector())/8
            hit,normal,*_=outer.ray_cast(center,ray)
            if hit is not None and normal.dot(ray)>0:contained=True;break
        if not contained:return 0.
    return solid_intersection_volume(a,b)
def clear(label,a,b):
    value=overlap(a,b);assert value<=EPS,f'{label}: {a.name}/{b.name}: {value} mm3'
    return value
def local_glb(name):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/enclosure'/name))
    objects=[o for o in set(bpy.data.objects)-before if o.type=='MESH']
    for o in objects:o.matrix_world=Matrix.Rotation(-math.pi/2,4,'X')@o.matrix_world
    return objects

design=json.loads((ROOT/'assets/enclosure/enclosure-design.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
front,rear,rigid,cell=[read_mesh(STL/(n+'.stl')) for n in ('front-chassis','rear-cover','front-rigid-DO-NOT-PRINT','battery-envelope-DO-NOT-PRINT')]
front.name='front-chassis';rear.name='rear-cover';rigid.name='rigid-front';cell.name='cell'
rear_rigid=read_mesh(STL/'rear-rigid-DO-NOT-PRINT.stl')
cover_snaps=local_glb('cover-snaps-DO-NOT-PRINT.glb')
keys=[read_mesh(STL/f'button-moving-{i}-DO-NOT-PRINT.stl') for i in range(1,5)]
clips=local_glb('screen-clips-DO-NOT-PRINT.glb')
liner=local_glb('battery-liner-DO-NOT-PRINT.glb')
adhesive=local_glb('battery-adhesive-DO-NOT-PRINT.glb')
pads=local_glb('display-cushioning.glb')
hardware=local_glb('pcb-cover-fasteners.glb');pcb_screws=[o for o in hardware if o.name.startswith('PCB-')]
assert len(clips)==6 and len(keys)==4 and len(pcb_screws)==4
assert len(cover_snaps)==4 and len(hardware)==4,'Cover closure must have four integral tabs and zero cover screws'
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(INPUT))
conversion=Matrix(((-1,0,0,0),(0,-1,0,0),(0,0,1,0),(0,0,0,1)))
emitted={}
for o in set(bpy.data.objects)-before:
    if o.type=='MESH':o.matrix_world=conversion@o.matrix_world;emitted[o.name]=o
circuit=json.loads((ROOT/'dist/index/circuit.json').read_text())
board_spec=next(o for o in circuit if o['type']=='pcb_board')
# The viewer's PCB mesh has split/open edges around generated drilling. A
# conservative watertight outline is suitable for solid collision tests; fill
# drill holes here, and verify its bounds against the actual exported body.
points=board_spec['outline'];count=len(points);half=board_spec['thickness']/2
mesh=bpy.data.meshes.new('PCB-outline-solid')
mesh.from_pydata([(p['x'],p['y'],z) for z in (-half,half) for p in points],[],
    [tuple(reversed(range(count))),tuple(range(count,2*count))]+
    [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)])
mesh.update();pcb_solid=bpy.data.objects.new('PCB-outline-solid',mesh);bpy.context.collection.objects.link(pcb_solid)
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
native_pcb=next(o for name,o in emitted.items() if name in ('Box0','MeshWithTextures0'))
assert all(abs(a-b)<.001 for solid_axis,native_axis in zip(bounds(pcb_solid),bounds(native_pcb)) for a,b in zip(solid_axis,native_axis)), 'PCB solid differs from emitted board bounds'
sources={o['source_component_id']:o['name'] for o in circuit if o['type']=='source_component'}
cads={sources[o['source_component_id']]:o for o in circuit if o['type']=='cad_component'}
pcb_refs={sources[o['source_component_id']] for o in circuit if o['type']=='pcb_component'}
missing=sorted(set(cads)-set(emitted));assert not missing,f'Missing CAD: {missing}'
for name,spec in cads.items():
    if spec.get('model_obj_url') or spec.get('model_glb_url'):assert len(emitted[name].data.vertices)>8,f'Fallback CAD for {name}'
board_parts=[o for n,o in emitted.items() if n in pcb_refs]+[pcb_solid]
# Check the assembled model actually contains the current printable geometry.
for name,local in (('front_chassis',front),('rear_cover',rear),('battery_pack',cell),('battery_liner',liner[0])):
    # The printed ink plane is 0.002 mm above the nominal pouch envelope.
    tolerance=.01 if name=='battery_pack' else .001
    assert all(abs(a-b)<tolerance for local_axis,native_axis in zip(bounds(local),bounds(emitted[name])) for a,b in zip(local_axis,native_axis)),f'Stale or shifted native CAD: {name}'
cell_bounds=bounds(cell);liner_bounds=bounds(liner[0]);module_bounds=bounds(emitted['U4'])
under_battery=[o for o in board_parts if all(min(a[1],b[1])-max(a[0],b[0])>1e-5 for a,b in zip(bounds(o)[:2],liner_bounds[:2]))]
highest=max(under_battery,key=lambda o:bounds(o)[2][1])
electronics_gap=liner_bounds[2][0]-bounds(highest)[2][1]
boss_gap=liner_bounds[2][0]-3.25
module_gap=module_bounds[1][0]-liner_bounds[1][1]
assert electronics_gap>=.5-1e-5,'Less than 0.5 mm nominal insulation/electronics clearance'
assert boss_gap>=.25-1e-5,'Less than 0.25 mm nominal insulation/PCB boss clearance'
assert module_gap>=1.-1e-5,'Battery overlaps the ESP32 module margin'
height=bounds(rear)[2][1]-bounds(front)[2][0]
assert abs(height-design['outsideMm'][2])<.001,'Outside thickness does not match actual meshes'
battery_margins={'highest_underlying_component':highest.name,'insulation_to_component_mm':round(electronics_gap,4),'insulation_to_pcb_boss_mm':round(boss_gap,4),'battery_liner_to_esp32_xy_mm':round(module_gap,4),'scope':'Nominal CAD clearances; actual pack thickness, swelling, wires and printed tolerances need a prototype check.'}
# Closed assembly: every actual electronic body, the PCB and battery remain clear.
for o in board_parts:
    for shell in (front,rear):clear('electronics/case',o,shell)
    clear('battery/electronics',cell,o)
    for item in liner:clear('insulator/electronics',item,o)
clear('case seam',front,rear);clear('battery/front',cell,front);clear('battery/rear',cell,rear)
for o in liner+adhesive:clear('battery supplies/front',o,front);clear('battery supplies/rear',o,rear)
for screw in pcb_screws:
    for o in (front,cell,*liner):clear('PCB screw/front-battery',screw,o)
    # The shaft intentionally engages the smaller rear-cover tap pilot.
    b=bounds(screw);head=cylinder('PCB-head-envelope',5,-3.3,-.8,(b[0][0]+b[0][1])/2,(b[1][0]+b[1][1])/2)
    clear('PCB screw head/rear',head,rear);bpy.data.objects.remove(head,do_unlink=True)
# Probe rear-cover cantilever seats, pilot floors and underside driver access.
seats=[];seat_tree=tree(rear)
for m in PCB_MOUNTS['mounts']:
    hits=[]
    for dx,dy in ((1.7,0),(-1.7,0),(0,1.7),(0,-1.7)):
        hit=seat_tree.ray_cast(Vector((m['x']+dx,m['y']+dy,0)),Vector((0,0,1)))[0]
        assert hit is not None and abs(hit.z-.8)<1e-4,'PCB seating face incorrect'
        hits.append(round(hit.z,5))
    floor=seat_tree.ray_cast(Vector((m['x'],m['y'],0)),Vector((0,0,1)))[0]
    assert floor is not None and floor.z-3.2>=.1,'PCB pilot has insufficient screw-tip clearance'
    driver=cylinder('driver',5,-24,-3.3,m['x'],m['y']);clear('PCB driver access before fitting front',driver,rear);bpy.data.objects.remove(driver,do_unlink=True)
    seats.append({'name':m['name'],'seat_samples_z':hits,'pilot_floor_z':round(floor.z,5),'screw_tip_clearance_mm':round(floor.z-3.2,5)})
snap_spec=design['coverSnaps']
assert snap_spec['count']==4 and snap_spec['coverScrews']==0
snap_seats=[]
for side in snap_spec['sides']:
    for tip in snap_spec['tipY']:
        probe=Vector((side*(snap_spec['retainingFaceX']+.2),tip,4.4))
        roof=tree(front).ray_cast(probe,Vector((0,0,1)))[0]
        hook=tree(rear).ray_cast(probe,Vector((0,0,-1)))[0]
        assert roof is not None and abs(roof.z-4.5)<1e-4,'Missing cover retaining ledge'
        assert hook is not None and abs(hook.z-4.3)<1e-4,'Missing cover hook shoulder'
        snap_seats.append({'side':side,'tip_y_mm':tip,'hook_engagement_mm':round(snap_spec['hookOuterX']-snap_spec['retainingFaceX'],4),'vertical_play_mm':round(roof.z-hook.z,4)})

def snap_shift(world,deflection):
    side=1 if world.x>0 else -1
    tip=next((y for y in snap_spec['tipY'] if y-2.001<=world.y<=y+snap_spec['beamLength']+.101),None)
    if tip is None or not 32.199<=abs(world.x)<=snap_spec['hookOuterX']+.001 or not 3.199<=world.z<=8.301:return world
    t=max(0,min(1,(world.y-tip)/snap_spec['beamLength']))
    return world+Vector((-side*deflection*(1-t)*(1-t)*(1+2*t),0,0))
for snap in cover_snaps:
    vertices=[v.co.copy() for v in snap.data.vertices]
    original_matrix=snap.matrix_world.copy()
    snap.matrix_world=Matrix.Translation(Vector((0,0,.3)))@original_matrix
    assert overlap(snap,front)>EPS,'Cover hook does not retain the uncompressed cover'
    snap.matrix_world=original_matrix
    for v,p in zip(snap.data.vertices,vertices):v.co=snap.matrix_world.inverted()@snap_shift(snap.matrix_world@p,snap_spec['releaseDeflectionMm'])
    snap.data.update()
    for obstacle in (front,rear_rigid,cell,*liner,*board_parts):clear('cover tab release',snap,obstacle)
    for v,p in zip(snap.data.vertices,vertices):v.co=p
    snap.data.update()

# Four integral key leaves have independent full actuation stroke plus a rest gap.
display=local_glb('display-panel.glb')
for o in display:o.matrix_world=Matrix.Translation(Vector(DISPLAY_ANCHOR))@Matrix.Rotation(math.radians(cads['EPD1']['rotation']['z']),4,'Z')@o.matrix_world
source_display_bounds=[(min(bounds(o)[axis][0] for o in display),max(bounds(o)[axis][1] for o in display)) for axis in range(3)]
assert all(abs(a-b)<.001 for source_axis,native_axis in zip(source_display_bounds,bounds(emitted['EPD1'])) for a,b in zip(source_axis,native_axis)), 'Native display differs from anchored source solids'
source_points=[o.matrix_world@v.co for o in display for v in o.data.vertices]
native_points=[emitted['EPD1'].matrix_world@v.co for v in emitted['EPD1'].data.vertices]
display_deviation=0.
for reference,compared in ((source_points,native_points),(native_points,source_points)):
    kd=KDTree(len(reference))
    for i,point in enumerate(reference):kd.insert(point,i)
    kd.balance()
    display_deviation=max(display_deviation,max(kd.find(point)[2] for point in compared))
assert display_deviation<1e-4, 'Native export changed display solid geometry'

# The battery harness is an external connection, not extra PCB BOM components.
# Check source/native equality, real clearance and the actual netlist endpoints.
battery_spec=json.loads((ROOT/'assets/enclosure/battery-connection.json').read_text())
battery_model=json.loads((ROOT/'assets/enclosure/battery-model.json').read_text())
leads=local_glb('battery-leads.glb');plug=local_glb('battery-plug.glb')
assert len(leads)==2
for name,parts in (('battery_leads',leads),('battery_plug',plug)):
    points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
    actual=[emitted[name].matrix_world@v.co for v in emitted[name].data.vertices]
    maximum=0.
    for reference,compared in ((points,actual),(actual,points)):
        kd=KDTree(len(reference))
        for i,p in enumerate(reference):kd.insert(p,i)
        kd.balance();maximum=max(maximum,max(kd.find(p)[2] for p in compared))
    assert maximum<1e-4,f'Native export changed {name}: {maximum}'
for part in leads+plug:
    for obstacle in (front,rear,*hardware,*liner,*adhesive,*display):clear('battery harness/case-display-hardware',part,obstacle)
    for obstacle in board_parts:clear('battery harness/electronics',part,obstacle)
for part in plug:clear('battery plug/pouch',part,cell)
# A contact blade can lie entirely inside a solid housing without its surfaces
# crossing the housing boundary. Test the socket directly, including containment.
for part in plug:
    assert solid_intersection_volume(part,emitted['BT1'])<=EPS,'Plug plastic covers the header contacts or latch'
clear('battery wires separated',leads[0],leads[1])
plug_original={o:o.matrix_world.copy() for o in plug}
for step in range(1,14):
    for part in plug:
        part.matrix_world=Matrix.Translation(Vector((0,-step*.5,0)))@plug_original[part]
        for obstacle in (front,rear,cell,*board_parts):clear('battery plug removal with case open',part,obstacle)
for part,transform in plug_original.items():part.matrix_world=transform
connector=battery_spec['connector']
bt_id=next(k for k,v in sources.items() if v=='BT1')
bt_ports={p['pin_number']:p for p in circuit if p['type']=='source_port' and p['source_component_id']==bt_id}
pad_records=[p for p in circuit if p['type']=='pcb_plated_hole' and p.get('pcb_component_id')==cads['BT1']['pcb_component_id']]
for key,pin,color in (('positive',1,'red'),('negative',2,'black')):
    port=bt_ports[pin]
    net_id=next(o['source_net_id'] for o in circuit if o['type']=='source_net' and o['name']==connector[key+'Net'])
    assert any(port['source_port_id'] in o.get('connected_source_port_ids',[]) and net_id in o.get('connected_source_net_ids',[]) for o in circuit if o['type']=='source_trace'),f'BT1 pin {pin} net mismatch'
    pad=next(p for p in pad_records if p.get('pcb_port_id')==next(p['pcb_port_id'] for p in circuit if p['type']=='pcb_port' and p['source_port_id']==port['source_port_id']))
    assert abs(pad['x']-connector[key+'X'])<.001,'Harness does not align with the actual board pin'
    end=battery_model['wire_paths_mm'][key][-1]
    assert abs(end[0]-pad['x'])<.001 and abs(end[1]-connector['wireExitY'])<.001 and abs(end[2]-connector['contactZ'])<.001
battery_report={'part':battery_spec['part']['partNumber'],'nominal_geometry_passed':True,
    'native_models_match_source':True,'wire_case_component_collisions':0,
    'connection':{'red':'BT1.1 / BATT_P','black':'BT1.2 / BATT_N_RAW (protected return)'},
    'wire_centerline_length_mm':battery_model['wire_centerline_length_mm'],
    'required_free_lead_length_mm':battery_model['required_free_lead_length_mm'],
    'plug_axial_removal_travel_mm':6.5,
    'removal_scope':'Rigid plug path, with the case open and flexible cable repositioned; strain and disconnect force require a physical sample.',
    'charge_current_ma':battery_spec['charging']['nominalChargeCurrentMa'],
    'physical_battery_qualified':False,
    'remaining_checks':['Delivered dimensions and swelling allowance','Actual keyed plug polarity','Usable lead length and wire diameter','Supplier charge/discharge ratings and allowed temperature'],
    'scope':battery_spec['modelScope']}
(STL/'battery-connection-check.json').write_text(json.dumps(battery_report,indent=2)+'\n')
print('Battery harness nominal geometry and netlist verified',flush=True)
key_strokes=[];key_refs=['SW6','SW3','SW2','SW4']
for key,x,ref in zip(keys,DISPLAY_SPEC['controls']['navigationX'],key_refs):
    original=[v.co.copy() for v in key.data.vertices]
    # Front-side ribbon must also clear the moving key's XY projection, rather
    # than relying on a shallow Z gap or notching its retaining flange.
    kb=bounds(key);root_y=DISPLAY_SPEC['panel']['centerY']-DISPLAY_SPEC['panel']['height']/2
    sl=max(0.,root_y-kb[1][1]);sh=min(DISPLAY_SPEC['flex']['flatRootLength'],root_y-kb[1][0])
    assert sl<sh,'Expected key row beside the flat tail region'
    # Use the widest root throughout this region, independent of taper corners.
    left=-DISPLAY_SPEC['flex']['rootWidth']/2;right=-left
    projection_gap=left-kb[0][1] if x<0 else kb[0][0]-right
    assert projection_gap>=.5,f'Moving {ref} overlaps full front ribbon corridor: {projection_gap}'
    switch=emitted[ref];hit=tree(switch).ray_cast(Vector((x,-42.5,-10)),Vector((0,0,1)))[0]
    assert hit is not None,'No switch actuator surface'
    plunger=-3.35;gap=hit.z-plunger
    assert 0<=gap<=.08,f'Incorrect rest gap {gap}'
    for stroke in (0,.1,.25):
        for v,p in zip(key.data.vertices,original):
            v.co=p;wx,wy,wz=key.matrix_world@p
            direction=1
            t=max(0,min(1,(direction*(wx-x)+4.5)/9.0))
            v.co.z+=stroke*(1 if wy>=-45.9 else t*t*(3-2*t))
        key.data.update();bpy.context.view_layer.update()
        clear('key stroke/static shell',key,rigid)
        for part in display:clear('key stroke/display ribbon',key,part)
        for other in keys:
            if other!=key:clear('independent key stroke',key,other)
        for o in board_parts:
            if o.name!=ref:clear('key stroke/other electronics',key,o)
    key_strokes.append({'switch':ref,'key_travel_mm':.25,'rest_actuator_gap_mm':round(gap,4),'switch_compression_at_full_stroke_mm':round(.25-gap,4),'other_part_collisions':0,'front_ribbon_projection_gap_mm':round(projection_gap,4)})
    for v,p in zip(key.data.vertices,original):v.co=p
    key.data.update()
# An integral floor shields the front-side tail from fingers between the keys.
ribbon_guard=[]
for x,y in ((-10.65,-42.5),(0.,-42.5),(10.65,-42.5),(0.,-47.5),(0.,-36.5)):
    exterior=tree(front).ray_cast(Vector((x,y,-10)),Vector((0,0,1)))[0]
    interior=tree(front).ray_cast(Vector((x,y,-3.8)),Vector((0,0,-1)))[0]
    assert exterior is not None and interior is not None,'Missing central ribbon guard'
    thickness=interior.z-exterior.z
    assert thickness>=1.8,'Ribbon channel exposes the tail to the key face'
    ribbon_guard.append({'x':x,'y':y,'floor_thickness_mm':round(thickness,4)})
# Ten front pads land on a continuous perimeter ledge, outside the active area.
front_pad_positions=[(side*27.1,y) for side in (-1,1) for y in (-22,8,32)]+[(x,y) for x in (-16,16) for y in (DISPLAY_SPEC['case']['bottomSupportY'],DISPLAY_SPEC['case']['topSupportY'])]
for x,y in front_pad_positions:
    hit=tree(front).ray_cast(Vector((x,y,-4.6)),Vector((0,0,-1)))[0]
    assert hit is not None and abs(hit.z+4.8)<1e-4,'Missing screen ledge'
for side in (-1,1):
    for y in design['screen']['clipTipY']:
        hit=tree(front).ray_cast(Vector((side*27.82,y,-3.7)),Vector((0,0,1)))[0]
        assert hit is not None and abs(hit.z-DISPLAY_SPEC['case']['clipFaceZ'])<1e-4,'Missing screen clip seating face'
for x in (-12,12):
    hit=tree(rear).ray_cast(Vector((x,DISPLAY_SPEC['case']['topSupportY'],-3.7)),Vector((0,0,1)))[0]
    assert hit is not None and abs(hit.z-DISPLAY_SPEC['case']['clipFaceZ'])<1e-4,'Missing upper screen support'
# Release six PETG leaf clips before dropping the padded glass. This rigid
# insertion model checks geometric freedom; no actuation force is predicted.
panel=next(o for o in display if 'nominal-outline' in o.name)
clip_original={o:[v.co.copy() for v in o.data.vertices] for o in clips}
for o,vertices in clip_original.items():
    world=[o.matrix_world@p for p in vertices];side=1 if sum(p.x for p in world)>0 else -1
    tip=min(p.y for p in world)+2.5
    for v,p,w in zip(o.data.vertices,vertices,world):
        t=max(0,min(1,(w.y-tip)/14.))
        shifted=w+Vector((side*(1-t)*(1-t)*(1+2*t),0,0))
        v.co=o.matrix_world.inverted()@shifted
    o.data.update();clear('released screen clip/case',o,rigid)
clip_pads=[o for o in pads if o.name.startswith('clip-pad')]
front_pads=[o for o in pads if o.name.startswith('front-screen-pad')]
assert len(clip_pads)==6 and len(front_pads)==10
pad_original={o:[v.co.copy() for v in o.data.vertices] for o in clip_pads}
for o,vertices in pad_original.items():
    world=[o.matrix_world@p for p in vertices];center=sum(world,Vector())/len(world)
    side=1 if center.x>0 else -1;tip=min(design['screen']['clipTipY'],key=lambda y:abs(y-center.y))
    for v,p,w in zip(o.data.vertices,vertices,world):
        t=max(0,min(1,(w.y-tip)/14.))
        v.co=o.matrix_world.inverted()@(w+Vector((side*(1-t)*(1-t)*(1+2*t),0,0)))
    o.data.update();clear('released clip foam/case',o,rigid)
paths=[]
def path(label,moving,obstacles,axis,start,step=.5,deform=None):
    print('Checking insertion:',label,flush=True)
    original={o:o.matrix_world.copy() for o in moving};maximum=0;samples=0
    offsets=[start-i*step*(1 if start>0 else -1) for i in range(round(abs(start)/step)+1)]
    if deform:offsets=sorted(set(offsets+[i*.1 for i in range(26)]),reverse=True)
    for offset in offsets:
        if deform:deform(offset)
        shift=Vector((0,0,0));shift[axis]=offset
        for o in moving:o.matrix_world=Matrix.Translation(shift)@original[o]
        bpy.context.view_layer.update()
        for o in moving:
            for b in obstacles:maximum=max(maximum,clear(label,o,b))
        samples+=1
    for o,m in original.items():o.matrix_world=m
    bpy.context.view_layer.update()
    paths.append({'assembly':label,'axis':axis,'start_offset_mm':start,'samples':samples,'step_mm':step,'max_overlap_mm3':maximum})
path('screen with clips manually released',[panel],[rigid,*clips,*clip_pads,*front_pads],2,12)
for o,vertices in clip_original.items():
    for v,p in zip(o.data.vertices,vertices):v.co=p
    o.data.update()
path('PCB straight into removed rear cover',board_parts,[rear,cell,*liner,*adhesive],2,-24)
pack=[cell,*liner,*adhesive];pack_original={o:o.matrix_world.copy() for o in pack}
stand_off=design['battery']['loadingStandOffZ']
for o in pack:o.matrix_world=Matrix.Translation(Vector((0,design['battery']['loadingOffsetY'],-stand_off)))@pack_original[o]
path('battery insertion clear of lower PCB bosses',pack,[rear],2,-24)
for o,m in pack_original.items():o.matrix_world=Matrix.Translation(Vector((0,0,-stand_off)))@m
path('battery slide to lower stop before fitting PCB',pack,[rear],1,design['battery']['loadingOffsetY'])
for o,m in pack_original.items():o.matrix_world=m
path('battery seating against adhesive',pack,[rear],2,-stand_off,step=.05)
rear_vertices=[v.co.copy() for v in rear.data.vertices]
def deform_cover(offset):
    # Kinematic ramp compression and release; contact forces are not predicted.
    if offset>=2.5:amount=0.
    elif offset>=1.5:amount=snap_spec['releaseDeflectionMm']*(2.5-offset)
    elif offset>=.2:amount=snap_spec['releaseDeflectionMm']
    else:amount=snap_spec['releaseDeflectionMm']*offset/.2
    # Geometry stays in unshifted assembly coordinates while its object moves.
    for v,p in zip(rear.data.vertices,rear_vertices):v.co=snap_shift(p,amount)
    rear.data.update()
path('loaded rear cover snaps into front chassis',[rear,cell,*liner,*adhesive,*board_parts,*pcb_screws],[front,panel],2,24,deform=deform_cover)
path('cover opening with four tabs held released',[rear,cell,*liner,*adhesive,*board_parts,*pcb_screws],[front,panel],2,3,step=.2,deform=lambda offset:deform_cover(1.))
for v,p in zip(rear.data.vertices,rear_vertices):v.co=p
rear.data.update()
# Transparency must be in the actual source GLBs; STL is geometry only.
import struct
materials=[]
for name in ('front-chassis','rear-cover'):
    raw=(ROOT/'assets/enclosure'/f'{name}.glb').read_bytes();n=struct.unpack_from('<I',raw,12)[0];gltf=json.loads(raw[20:20+n])
    mats=gltf.get('materials',[]);assert mats and all(m.get('alphaMode')=='BLEND' and 0<m['pbrMetallicRoughness']['baseColorFactor'][3]<1 for m in mats),'Opaque enclosure CAD'
    materials.append({'part':name,'alpha':mats[0]['pbrMetallicRoughness']['baseColorFactor'][3],'alphaMode':'BLEND'})
raw=INPUT.read_bytes();n=struct.unpack_from('<I',raw,12)[0];native=json.loads(raw[20:20+n])
native_transparency=[]
for name,source_alpha in (('front_chassis',.38),('rear_cover',.22)):
    # The tscircuit viewer/exporter applies 0.5 alpha for this explicit flag.
    expected=.5 if cads[name].get('show_as_translucent_model') else source_alpha
    node=next(node for node in native['nodes'] if node.get('name')==name)
    mats=[native['materials'][p['material']] for p in native['meshes'][node['mesh']]['primitives']]
    assert mats and all(m.get('alphaMode')=='BLEND' and abs(m['pbrMetallicRoughness']['baseColorFactor'][3]-expected)<1e-5 for m in mats),'Native export lost enclosure transparency'
    native_transparency.append({'part':name,'effective_alpha':expected,'alphaMode':'BLEND'})
import hashlib
switch_source=next(item for item in circuit if item['type']=='source_component' and item['name']=='SW7')
power_switch={'reference':'SW7','supplier_part_number':switch_source['supplier_part_numbers']['jlcpcb'][0],
              'model_bounds_mm':[[round(value,4) for value in axis] for axis in bounds(emitted['SW7'])],
              'component_case_collisions':0}
report={'revision':design['revision'],'power_switch':power_switch,'native_assembly_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'printed_parts':2,'outside_mm':design['outsideMm'],'measured_mesh_thickness_mm':round(height,4),'battery_clearances':battery_margins,'cover_snaps':{'seats':snap_seats,'release_deflection_mm':snap_spec['releaseDeflectionMm'],'cover_screws':0,'nominal_beam_surface_strain':round(3*snap_spec['beamWidth']*snap_spec['releaseDeflectionMm']/(2*snap_spec['beamLength']**2),6)},'native_cad_models':len(cads),'missing_native_models':missing,'pcb_meshes':len(board_parts),'component_case_collisions':0,'pcb_mounts':seats,'key_strokes':key_strokes,'ribbon_guard_floor':ribbon_guard,'screen_front_pad_seats':10,'screen_rear_clip_seats':6,'upper_screen_supports':2,'installation_paths':paths,'cad_transparency':materials,'native_assembly_transparency':native_transparency,'native_assembly_transparency_verified':True,'volume_epsilon_mm3':EPS,'scope':'Nominal geometry, sampled insertion and flexure deformation only. Fit, force, fatigue, optical clarity and adhesive retention need physical testing.'}
report['pcb_collision_model']='Watertight emitted outline with drills filled conservatively; bounds match native PCB export.'
report['native_display_geometry_max_vertex_deviation_mm']=round(display_deviation,8)
report['key_display_collision_model']='Separate source glass, flex, stiffener and contact solids; vertices match native export.'
report['numerical_contact_epsilon_mm']=CONTACT_EPS_MM
(STL/'clearance-check.json').write_text(json.dumps(report,indent=2)+'\n')
(STL/'assembly-check.json').write_text(json.dumps({'revision':design['revision'],'native_cad_models':len(cads),'missing_native_models':missing,'installation_paths':paths,'scope':report['scope']},indent=2)+'\n')
(STL/'display-retainer-check.json').write_text(json.dumps({'revision':design['revision'],'front_pad_seats':10,'side_clip_seats':6,'upper_cover_supports':2,'screen_insertion':paths[0],'scope':report['scope']},indent=2)+'\n')
print(json.dumps(report,indent=2))
