"""Render the reader using the current native assembly and transparent source GLBs.

Run after `bun run export:assembly`. Rendering preserves source CAD alpha;
it illustrates a transparent CAD material, not the optical finish of FDM PETG.
"""
from pathlib import Path
from math import pi
import subprocess
import bpy
from mathutils import Matrix, Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/enclosure'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)

def local(name,offset=(0,0,0)):
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(OUT/name))
    objects=[o for o in set(bpy.data.objects)-before if o.type=='MESH']
    for o in objects:o.matrix_world=Matrix.Translation(Vector(offset))@Matrix.Rotation(-pi/2,4,'X')@o.matrix_world
    return objects

front=local('front-chassis.glb');rear=local('rear-cover.glb')
cell=local('battery-envelope-DO-NOT-PRINT.glb')
liner=local('battery-liner-DO-NOT-PRINT.glb');adhesive=local('battery-adhesive-DO-NOT-PRINT.glb')
antenna=local('antenna-envelope-DO-NOT-PRINT.glb')
keys=front # Key caps/leaves are part of the same connected chassis mesh.
display=local('display-panel.glb',(0,-32.34,.8))
pads=local('display-cushioning.glb');hardware=local('pcb-cover-fasteners.glb')
pcb_screws=[o for o in hardware if o.name.startswith('PCB-')]
cover_screws=[o for o in hardware if o not in pcb_screws]
before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(ROOT/'dist/index/assembly.glb'))
conversion=Matrix(((-1,0,0,0),(0,-1,0,0),(0,0,1,0),(0,0,0,1)))
assembly={'EPD1','battery_envelope','wifi_antenna_envelope','front_chassis','rear_cover','battery_liner','battery_adhesive','display_cushioning','pcb_cover_fasteners'}
board=[]
for o in set(bpy.data.objects)-before:
    if o.type!='MESH':continue
    if o.name.split('.')[0] in assembly:bpy.data.objects.remove(o,do_unlink=True);continue
    o.matrix_world=conversion@o.matrix_world;board.append(o)
# Work in metre-sized Blender coordinates, keeping millimetre source files.
for o in bpy.data.objects:
    if o.type=='MESH':o.matrix_world=Matrix.Scale(.01,4)@o.matrix_world
objects=[o for o in bpy.data.objects if o.type=='MESH'];original={o:o.matrix_world.copy() for o in objects}
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
scene.cycles.use_denoising=True;scene.render.resolution_x=1100;scene.render.resolution_y=1000
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.82,.87,.91,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.6
scene.view_settings.view_transform='AgX';scene.view_settings.exposure=-1.2
for pos,power,size in [((1.3,-1.6,2.6),500,2),((-1.8,1,1.6),350,2),((1.2,1.8,-2),450,2)]:
    bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size
    o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()

def hide(group):
    for o in group:o.hide_render=True

def reset():
    for o,m in original.items():o.hide_render=False;o.matrix_world=m

def shift(group,z):
    for o in group:o.matrix_world=Matrix.Translation(Vector((0,0,z*.01)))@o.matrix_world

def render(name,pos,scale=145,target=(0,5,3)):
    bpy.ops.object.camera_add(location=Vector(pos)*.01);cam=bpy.context.object
    cam.rotation_euler=(Vector(target)*.01-cam.location).to_track_quat('-Z','Y').to_euler()
    cam.data.type='ORTHO';cam.data.ortho_scale=scale*.01;cam.data.clip_start=.001
    scene.camera=cam;scene.render.filepath=str(OUT/name);bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam,do_unlink=True);print('Rendered',name,flush=True)

render('printable-front.png',(80,110,-125))
render('printable-side.png',(170,-55,65),142)
hide(rear+cell+liner+adhesive+antenna+cover_screws)
render('printable-open-back.png',(-85,-110,135))
hide(display+pads)
render('printable-pcb-mounts.png',(0,5,220),133)
reset();hide(rear+cell+liner+adhesive+antenna+hardware+board)
render('display-retainer-installed.png',(70,-110,150),132,(0,9,-3))
reset();hide(front+rear+cell+liner+adhesive+antenna+hardware+pads)
render('display-ribbon-connection.png',(30,-80,28),43,(0,-34,0))
reset();shift(display,8);shift(pads,8);shift(board+pcb_screws,25)
shift(cell+liner+adhesive,44);shift(rear+antenna+cover_screws,60)
render('printable-exploded.png',(130,-135,130),185,(0,5,33))
# Print plate: show the actual two oriented exports with opaque material so
# the support features remain legible. Assembly previews above retain alpha.
hide(objects)
for name,x,y in [('front-chassis',65,110),('rear-cover',150,110)]:
    bpy.ops.wm.stl_import(filepath=str(OUT/'print'/(name+'.stl')));o=bpy.context.object
    o.matrix_world=Matrix.Scale(.01,4)@Matrix.Translation(Vector((x,y,0)))@o.matrix_world
    mat=bpy.data.materials.new(name+'-print-preview');mat.diffuse_color=(.16,.37,.43,1);mat.use_nodes=True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=mat.diffuse_color
    o.data.materials.clear();o.data.materials.append(mat)
    bpy.ops.object.text_add(location=((x-34)*.01,48*.01,.001));label=bpy.context.object
    label.data.body=name.replace('-',' ');label.data.size=.032
    ink=bpy.data.materials.new('label-ink');ink.diffuse_color=(.025,.04,.05,1);ink.use_nodes=True
    ink.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=ink.diffuse_color
    label.data.materials.append(ink)
bpy.ops.mesh.primitive_cube_add(size=1,location=(1.1,1.1,-.015));bed=bpy.context.object;bed.dimensions=(2.2,2.2,.02)
render('reader-print-plate.png',(210,-135,360),295,(110,110,0))
subprocess.run(['python3',str(ROOT/'scripts/package-preview-images.py')],cwd=ROOT,check=True)
