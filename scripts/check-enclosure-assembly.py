"""Verify native CAD meshes and sampled PCB, tray and cover installation paths.

Run: blender --background --python-exit-code 1 --python
scripts/check-enclosure-assembly.py -- /tmp/esp-reader-current.glb
This is rigid nominal geometry; it does not predict assembly forces or tolerances.
"""
from pathlib import Path
import bpy,bmesh,json,math,sys
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];STL=ROOT/'assets/enclosure/stl'
INPUT=Path(sys.argv[sys.argv.index('--')+1])
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def stl(name):
    bpy.ops.wm.stl_import(filepath=str(STL/(name+'.stl')))
    obj=bpy.context.object;obj.name=name;return obj

def tree(obj):
    bm=bmesh.new();bm.from_mesh(obj.data);bm.transform(obj.matrix_world)
    result=BVHTree.FromBMesh(bm);bm.free();return result

def overlap(a,b):
    def bounds(o):
        p=[o.matrix_world@Vector(v) for v in o.bound_box]
        return [(min(q[i] for q in p),max(q[i] for q in p)) for i in range(3)]
    if any(min(x[1],y[1])-max(x[0],y[0])<=1e-5 for x,y in zip(bounds(a),bounds(b))):return 0
    ta,tb=tree(a),tree(b)
    if not ta.overlap(tb):
        center=sum((a.matrix_world@Vector(v) for v in a.bound_box),Vector())/8
        point,normal,*_=tb.ray_cast(center,Vector((.912,.317,.257)).normalized())
        if point is None or normal.dot(Vector((.912,.317,.257)))<=0:return 0
    test=a.copy();test.data=a.data.copy();bpy.context.collection.objects.link(test)
    bpy.context.view_layer.objects.active=test
    mod=test.modifiers.new('nominal-overlap','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=b
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bm=bmesh.new();bm.from_mesh(test.data);volume=round(abs(bm.calc_volume(signed=True)),6);bm.free()
    bpy.data.objects.remove(test,do_unlink=True);return volume

def local_glb(name):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets/enclosure'/name))
    objects=[o for o in set(bpy.data.objects)-before if o.type=='MESH']
    for o in objects:o.matrix_world=Matrix.Rotation(-math.pi/2,4,'X')@o.matrix_world
    return objects

body,bezel,strip,tray,cover,cell=[stl(n) for n in ('main-body','front-bezel','button-strip','battery-partition','rear-cover','battery-envelope-DO-NOT-PRINT')]
screws=local_glb('pcb-cover-fasteners.glb');pcb_screws=[o for o in screws if o.name.startswith('PCB-')]
bezel_screws=local_glb('display-retainer-fasteners.glb');assert len(pcb_screws)==4 and len(bezel_screws)==6
circuit=json.loads((ROOT/'dist/index/circuit.json').read_text())
sources={o['source_component_id']:o['name'] for o in circuit if o['type']=='source_component'}
cad={sources[o['source_component_id']]:o for o in circuit if o['type']=='cad_component'}
pcb_refs={sources[o['source_component_id']] for o in circuit if o['type']=='pcb_component'}
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(INPUT))
conversion=Matrix(((-1,0,0,0),(0,-1,0,0),(0,0,1,0),(0,0,0,1)))
emitted={}
for obj in set(bpy.data.objects)-before:
    if obj.type=='MESH':obj.matrix_world=conversion@obj.matrix_world;emitted[obj.name]=obj
missing=sorted(set(cad)-set(emitted));assert not missing,f'Missing native CAD models: {missing}'
for name,spec in cad.items():
    if spec.get('model_obj_url') or spec.get('model_glb_url'):
        assert len(emitted[name].data.vertices)>8,f'Fallback model for {name}'
board_parts=[o for name,o in emitted.items() if name in pcb_refs or name in ('Box0','MeshWithTextures0')]
assert any(o.name in ('Box0','MeshWithTextures0') for o in board_parts),'Missing PCB mesh'

paths=[]
def vertical_path(name,moving,obstacles):
    original={o:o.matrix_world.copy() for o in moving};maximum=0;samples=0
    for step in range(49):
        dz=24-step*.5
        for o in moving:o.matrix_world=Matrix.Translation((0,0,dz))@original[o]
        bpy.context.view_layer.update()
        for o in moving:
            for target in obstacles:
                value=overlap(o,target);maximum=max(maximum,value)
                assert value<=1e-4,f'{name}: {o.name} intersects {target.name} at +Z {dz}: {value} mm3'
        samples+=1
    for o,m in original.items():o.matrix_world=m
    bpy.context.view_layer.update()
    paths.append({'assembly':name,'direction':'straight -Z from open rear','samples':samples,'step_mm':.5,'max_solid_overlap_mm3':maximum})
vertical_path('PCB',board_parts,[body,bezel,strip,*bezel_screws])
vertical_path('battery-tray',[tray],[body,bezel,strip,*board_parts,*pcb_screws,*bezel_screws])
vertical_path('rear-cover',[cover],[body,bezel,strip,tray,cell,*board_parts,*pcb_screws,*bezel_screws])
# The four tray sleeves must seat on FR-4, not on components or screw heads.
mounts=json.loads((ROOT/'assets/enclosure/pcb-mounts.json').read_text())['mounts']
pcb_trees=[tree(o) for o in board_parts if o.name in ('Box0','MeshWithTextures0')]
seats=[]
for m in mounts:
    hits=[]
    for dx,dy in ((3,0),(-3,0),(0,3),(0,-3)):
        x,y=m['x']+dx,m['y']+dy
        point,*_=tree(tray).ray_cast(Vector((x,y,.7)),Vector((0,0,1)))
        assert point is not None and abs(point.z-.8)<1e-4,'Missing tray-foot seating face'
        supported=any((hit:=t.ray_cast(Vector((x,y,1)),Vector((0,0,-1)))[0]) is not None and abs(hit.z-.8)<1e-4 for t in pcb_trees)
        hits.append(supported)
    assert sum(hits)>=3,f'Insufficient FR-4 seating: {m}, {hits}'
    seats.append({'mount':m['name'],'foot_base_z':.8,'fr4_samples_supported':sum(hits),'samples':4})
report={'native_cad_models':len(cad),'missing_native_models':missing,'pcb_meshes':len(board_parts),'installation_paths':paths,'tray_seats':seats,
        'scope':'Sampled rigid nominal geometry. Physical tolerances, cable handling, thread fit, pad force and fatigue remain unverified.'}
(STL/'assembly-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
