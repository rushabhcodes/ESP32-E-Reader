"""Generate dimensioned prototype STLs (millimetres) for the Rev. E reader.

Run: blender --background --python scripts/generate-printable-enclosure.py
The cell dimensions are the published *nominal* SparkFun PRT-13855 pack dimensions.
See assets/enclosure/PRINTING.md before fitting a real cell or powering a board.
"""

from math import cos, pi, sin
from pathlib import Path
import json
import sys

import bpy
import bmesh


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from importlib import import_module
display_flex = import_module("display-flex")
PCB_MOUNTS = json.loads((ROOT / "assets/enclosure/pcb-mounts.json").read_text())
OUT = ROOT / "assets" / "enclosure" / "stl"
OUT.mkdir(parents=True, exist_ok=True)

# PCB coordinates: +Z is the component/battery side; front display faces -Z.
CASE_W, CASE_H, CASE_Y, CORNER_R = 68.0, 111.0, 5.0, 5.0


def reset():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def prism(name, width, height, radius, low, high, x=0, y=0):
    radius = min(radius, width / 2, height / 2)
    corners = [
        (x + width / 2 - radius, y - height / 2 + radius, -pi / 2),
        (x + width / 2 - radius, y + height / 2 - radius, 0),
        (x - width / 2 + radius, y + height / 2 - radius, pi / 2),
        (x - width / 2 + radius, y - height / 2 + radius, pi),
    ]
    outline = []
    for cx, cy, start in corners:
        for step in range(17):
            angle = start + step * pi / 32
            outline.append((cx + radius * cos(angle), cy + radius * sin(angle)))
    count = len(outline)
    verts = [(px, py, low) for px, py in outline]
    verts += [(px, py, high) for px, py in outline]
    faces = [tuple(reversed(range(count))), tuple(range(count, count * 2))]
    for i in range(count):
        j = (i + 1) % count
        faces.append((i, j, count + j, count + i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def box(name, dims, center):
    bpy.ops.mesh.primitive_cube_add(size=1, location=center)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return obj


def boolean(target, other, operation):
    bpy.context.view_layer.objects.active = target
    mod = target.modifiers.new(operation.lower(), "BOOLEAN")
    mod.operation = operation
    mod.solver = "MANIFOLD"
    mod.object = other
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other, do_unlink=True)


def cut(target, other):
    boolean(target, other, "DIFFERENCE")


def add(target, other):
    boolean(target, other, "UNION")


def wedge(name, profile, low, high, along_x=False):
    n = len(profile)
    vertices = [(t, q, z) if along_x else (q, t, z) for t in (low, high) for q, z in profile]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    bm = bmesh.new(); bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh); bpy.context.collection.objects.link(obj)
    return obj


def cone(name, bottom_diameter, top_diameter, low, high, x, y):
    bpy.ops.mesh.primitive_cone_add(
        vertices=64, radius1=bottom_diameter / 2,
        radius2=top_diameter / 2, depth=high - low,
        location=(x, y, (low + high) / 2))
    obj = bpy.context.object
    obj.name = name
    return obj


def export_glb(objects, filename):
    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=str(OUT.parent / filename),
                              export_format="GLB", export_yup=False,
                              use_selection=True)


report = {}


def export(obj, filename):
    # Triangulate and check that every edge has exactly two adjacent faces.
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    # Exact booleans can leave coincident vertices on an intersected ledge.
    # Weld only numerical seams (0.00001 mm), then validate the actual mesh.
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-5)
    bmesh.ops.dissolve_degenerate(bm, edges=list(bm.edges), dist=1e-7)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    obj.data.update()
    bad = sum(not edge.is_manifold for edge in bm.edges)
    bad_edges = [[[round(c, 7) for c in v.co] for v in edge.verts]
                 for edge in bm.edges if not edge.is_manifold]
    volume = bm.calc_volume(signed=True)
    unseen = set(bm.verts)
    islands = 0
    regions = []
    while unseen:
        islands += 1
        todo = [unseen.pop()]
        region = []
        while todo:
            v = todo.pop()
            region.append(obj.matrix_world @ v.co)
            for edge in v.link_edges:
                other = edge.other_vert(v)
                if other in unseen:
                    unseen.remove(other)
                    todo.append(other)
        regions.append([[round(min(p[i] for p in region),4), round(max(p[i] for p in region),4)] for i in range(3)])
    bm.free()
    coords = [obj.matrix_world @ v.co for v in obj.data.vertices]
    bounds = [[min(v[i] for v in coords), max(v[i] for v in coords)] for i in range(3)]
    report[filename] = {"nonmanifold_edges": bad, "connected_shells": islands, "signed_volume_mm3": round(volume, 3), "bounds_mm": [[round(q, 3) for q in pair] for pair in bounds]}
    if bad or volume <= 0 or islands != 1:
        print("Connected region bounds:", regions)
        print("Non-manifold edge coordinates:", bad_edges)
        raise RuntimeError(f"{filename}: {bad} non-manifold edges, {islands} islands, volume {volume}")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.wm.stl_export(filepath=str(OUT / filename), export_selected_objects=True, apply_modifiers=True)
    if filename in {"rear-cover.stl", "front-chassis.stl", "battery-envelope-DO-NOT-PRINT.stl", "antenna-envelope-DO-NOT-PRINT.stl"}:
        bpy.ops.export_scene.gltf(
            filepath=str(OUT.parent / filename.replace(".stl", ".glb")),
            export_format="GLB", export_yup=False, use_selection=True,
        )


# Fresh two-piece enclosure: front chassis/keys and transparent rear battery cradle.
FRONT_Z, SEAM_Z = -5.8, 5.4
# Move the existing pack below U4 in XY, then lower it over the shorter parts.
# The insulating liner remains above the 3.25 mm PCB cantilever bosses.
CELL_X, CELL_Y, CELL_BASE = -6.0, -8.5, 3.7
CELL_THICKNESS, LINER_THICKNESS, ADHESIVE_THICKNESS = 5.6, .2, .5
CELL_LOADING_STANDOFF = .1
REAR_THICKNESS = 1.2
LID_INNER = CELL_BASE + CELL_THICKNESS + ADHESIVE_THICKNESS
LID_OUTER = LID_INNER + REAR_THICKNESS
GUIDE_BASE = CELL_BASE - .4
CLIP_TIPS = (-27.0, 3.0, 27.0)
CLIP_PAD_Z = -3.4
SNAP_TIPS = (-5.0, 24.0)
SNAP_LENGTH, SNAP_RELEASE = 14.0, .6

def paint(obj, mat):
    # Booleans may leave empty material slots. Assign every polygon explicitly.
    obj.data.materials.clear();obj.data.materials.append(mat)
    for poly in obj.data.polygons:poly.material_index=0
    obj.color=mat.diffuse_color

def transparent_material(name, color, alpha):
    mat=display_flex.material(name,color)
    mat.diffuse_color=(*color,alpha)
    shader=mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value=(*color,alpha)
    shader.inputs['Alpha'].default_value=alpha
    mat.surface_render_method='DITHERED'
    return mat

def save_gauge(obj, filename):
    export(obj,filename)

reset()
front=prism('front-chassis',68,111,5,FRONT_Z,-3.25,y=5)
cut(front,prism('screen-window',52.8,87.2,1.8,FRONT_Z-.1,5.5,y=10.5))
cut(front,prism('screen-drop-in-rebate',56.8,97.2,1.3,-4.8,5.5,y=10.5))
wall=prism('front-sidewalls',68,111,5,-3.3,SEAM_Z,y=5)
cut(wall,prism('rear-opening',64,107,3.1,-3.4,SEAM_Z+.1,y=5))
# The display extends beyond the upper PCB edge. Preserve its full rebate.
cut(wall,prism('top-panel-pocket',56.8,97.2,1.3,-4.8,SEAM_Z+.1,y=10.5))
add(front,wall)
# Keep the installed display tail clear between the glass exit and PCB slot.
cut(front,box('ribbon-service-opening',(15,7,3),(0,-37.5,-2.5)))
for x,y,w,low in ((34,36.3,11.,-1.7),(-34,-18.5,16.,-1.7),(34,14.1,11.,-1.5)):
    cut(front,box('open-assembly-port',(10,w,SEAM_Z+.2-low),(x,y,(SEAM_Z+.2+low)/2)))
# Rear-cover support columns nest in sidewall grooves; the front chassis
# has no PCB bosses projecting across the display insertion path.
for m in PCB_MOUNTS['mounts']:
    cut(front,prism('PCB-head-clearance',5.4,5.4,2.7,-3.45,-3.1,x=m['x'],y=m['y']))
    cut(front,box('rear-PCB-column-clearance',(1.4,6.2,4.9),(31.8 if m['x']>0 else -31.8,m['y'],3.05)))
# Open receiving channels leave 0.8 mm outer retaining ledges. Each hook
# snaps into a recessed side window, also accessible for service with a pick.
for side in (-1,1):
    for tip in SNAP_TIPS:
        cut(front,box('snap-stem-channel',(1.7,18.2,2.6),(side*32.35,tip+5.9,4.3)))
        cut(front,box('snap-release-window',(3.0,6.0,1.5),(side*33.2,tip,3.75)))
# Free printed key faces, rear flanges and spring leaves. Through slots prevent
# bridges from fusing to a floor beneath them; roots remain joined to the shell.
for x in (-21.,-7.,7.,21.):
    cut(front,prism('key-face-opening',10.8,5.2,2.5,FRONT_Z-.1,-3.1,x=x,y=-42.5))
    cut(front,prism('key-flange-pocket',12.2,6.6,2.5,-4.3,-3.1,x=x,y=-42.5))
    cut(front,box('leaf-free-slot',(12.4,1.8,3.0),(x,-46.3,-4.45)))
    cut(front,box('leaf-tip-free-slot',(1.4,3.4,3.0),(x+5.2,-45.3,-4.45)))
# Clearance below each cam lip lets the clip move outwards without striking
# the back of the display rebate. The front support ledge stays intact.
for side in (-1,1):
    for tip in CLIP_TIPS:
        cut(front,box('clip-release-pocket',(3.4,20,1.8),(side*29.95,tip+6,-2.9)))
# Inspection gauge is the rigid portion; it is excluded from the print package.
rigid=front.copy();rigid.data=front.data.copy();bpy.context.collection.objects.link(rigid)
save_gauge(rigid,'front-rigid-DO-NOT-PRINT.stl');bpy.data.objects.remove(rigid,do_unlink=True)
clips=[]
for side in (-1,1):
    for tip in CLIP_TIPS:
        leaf=box('screen-leaf',(0.8,14.0,1.2),(side*29.3,tip+7,-2.8))
        lip=wedge('screen-cam-lip',[(side*27.5,-3.4),(side*29.7,-3.4),(side*29.7,-2.2)],tip-2.5,tip+2.5)
        add(leaf,lip)
        # Root alone joins the case. The rest has lateral deflection clearance.
        add(front,box('screen-leaf-root',(3.4,1.2,1.2),(side*30.6,tip+14,-2.8)))
        gauge=leaf.copy();gauge.data=leaf.data.copy();bpy.context.collection.objects.link(gauge);clips.append(gauge)
        add(front,leaf)
export_glb(clips,'screen-clips-DO-NOT-PRINT.glb')
for o in clips:bpy.data.objects.remove(o,do_unlink=True)
strip=box('integral-key-rail',(54,.8,.8),(0,-47.55,-3.65))
for idx,x in enumerate((-21.,-7.,7.,21.),1):
    cap=prism('key-'+str(idx),9.6,4,1.7,FRONT_Z,-4.05,x=x,y=-42.5)
    flange=prism('key-flange',11.6,6,2.2,-4.06,-3.65,x=x,y=-42.5)
    for m in PCB_MOUNTS['mounts']:
        if m['buttonFlangeRelief'] and abs(x-m['x'])<9:
            cut(flange,prism('PCB-boss-relief',6.4,6.4,3.2,-4.2,-3.4,x=m['x'],y=m['y']))
    add(cap,flange);add(cap,prism('key-plunger',2.2,2.2,.6,-3.7,-3.35,x=x,y=-42.5))
    save_gauge(cap,'button-'+str(idx)+'-DO-NOT-PRINT.stl')
    add(strip,cap)
    add(strip,box('key-spring-leaf',(11.2,.8,.8),(x,-46.3,-3.65)))
    add(strip,box('key-root',(.8,1.7,.8),(x-5.2,-47.,-3.65)))
    add(strip,box('key-tip',(.8,2.8,.8),(x+5.2,-45.3,-3.65)))
bm=bmesh.new();bm.from_mesh(strip.data)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=1e-6,plane_co=(0,-46.95,0),plane_no=(0,1,0))
bm.to_mesh(strip.data);bm.free()
save_gauge(strip,'button-flexures-DO-NOT-PRINT.stl')
for idx,x in enumerate((-21.,-7.,7.,21.),1):
    moving=strip.copy();moving.data=strip.data.copy();bpy.context.collection.objects.link(moving)
    boolean(moving,box('free-key-gauge',(13.6,10,4),(x,-41.95,-4.2)),'INTERSECT')
    save_gauge(moving,'button-moving-'+str(idx)+'-DO-NOT-PRINT.stl')
    bpy.data.objects.remove(moving,do_unlink=True)
add(front,strip)
paint(front,transparent_material('smoke-PETG-front',(.14,.24,.28),.38))
export(front,'front-chassis.stl')
export_glb([front],'front-chassis.glb')

reset()
rear=prism('rear-cover',68,111,5,LID_INNER,LID_OUTER,y=5)
wall=prism('rear-sidewalls',68,111,5,SEAM_Z,LID_INNER+.05,y=5)
cut(wall,prism('rear-interior',64,107,3.1,SEAM_Z-.1,LID_INNER+.15,y=5));add(rear,wall)
tongue=prism('seam-tongue',63.6,106.4,2.8,SEAM_Z-1.2,SEAM_Z+.05,y=5)
cut(tongue,prism('tongue-interior',62.0,104.8,2.0,SEAM_Z-1.3,SEAM_Z+.15,y=5))
collar=prism('seam-connecting-collar',68,111,5,SEAM_Z,SEAM_Z+.8,y=5)
cut(collar,prism('collar-interior',62.0,104.8,2.0,SEAM_Z-.1,SEAM_Z+.9,y=5))
add(rear,collar);add(rear,tongue)
# PCB clamps to the underside of cantilever bosses in the rear cover.
# Columns stay outside the board outline; bridges stay below the battery.
for m in PCB_MOUNTS['mounts']:
    x,y=m['x'],m['y'];side=1 if x>0 else -1
    add(rear,box('PCB-support-column',(.9,5.6,LID_INNER+.05-.8),(side*31.8,y,(LID_INNER+.05+.8)/2)))
    add(rear,box('PCB-cantilever',(abs(side*31.8-x)+.6,5.6,2.45),((side*31.8+x)/2,y,2.025)))
    add(rear,prism('PCB-boss',5.6,5.6,2.8,.8,3.25,x=x,y=y))
    cut(rear,prism('PCB-pilot',2,2,1,.7,3.35,x=x,y=y))
# The cell enters straight through the open front of the removed cover.
# Nonconductive pouch-compatible foam adhesive holds it against the lid;
# a thin liner shields its PCB-facing surface. Four guides locate its edges.
for x in (CELL_X-25.2,CELL_X+25.2):add(rear,box('cell-side-guide',(.8,70.4,LID_INNER+.05-GUIDE_BASE),(x,CELL_Y,(LID_INNER+.05+GUIDE_BASE)/2)))
# Leave the upper end open: insert the pack at Y -2, above the lower PCB
# bosses, then slide it 6.5 mm towards the single lower stop before fitting PCB.
add(rear,box('cell-lower-stop',(50.2,.8,LID_INNER+.05-GUIDE_BASE),(CELL_X,CELL_Y-35,(LID_INNER+.05+GUIDE_BASE)/2)))
cut(rear,box('BT1-and-lead-notch',(1.,14,8),(CELL_X+25.2,-32.4,7.0)))
# Two upper-border columns pass completely above the PCB outline. Their pads
# support the long display end without a loose retainer or pressure on pixels.
for x in (-12.,12.):add(rear,box('upper-screen-support',(10,1.4,LID_INNER+.05-CLIP_PAD_Z),(x,55.4,(LID_INNER+.05+CLIP_PAD_Z)/2)))
# Four long side leaves flex inward without crossing PCB or battery envelopes.
# The rail above the free slots stays joined to the flat rear wall.
for side in (-1,1):
    for tip in SNAP_TIPS:
        cut(rear,box('cover-snap-free-slot',(3.0,17.2,6.2),(side*33.0,tip+5.6,6.1)))
rigid=rear.copy();rigid.data=rear.data.copy();bpy.context.collection.objects.link(rigid)
save_gauge(rigid,'rear-rigid-DO-NOT-PRINT.stl');bpy.data.objects.remove(rigid,do_unlink=True)
snaps=[]
for side in (-1,1):
    for tip in SNAP_TIPS:
        leaf=box('cover-snap-leaf',(.8,14.1,3.6),(side*32.6,tip+7.05,6.5))
        profile=[(32.2,3.2),(33.6,3.9),(33.6,4.3),(33.0,4.3),(33.0,4.8),(32.2,4.8)]
        add(leaf,wedge('cover-snap-hook',[(side*x,z) for x,z in profile],tip-2.,tip+2.))
        gauge=leaf.copy();gauge.data=leaf.data.copy();bpy.context.collection.objects.link(gauge);snaps.append(gauge)
        add(rear,box('cover-snap-root',(1.6,1.2,2.7),(side*33.,tip+14.6,6.95)))
        add(rear,leaf)
export_glb(snaps,'cover-snaps-DO-NOT-PRINT.glb')
for o in snaps:bpy.data.objects.remove(o,do_unlink=True)
paint(rear,transparent_material('clear-PETG-rear',(.66,.88,.93),.22))
export(rear,'rear-cover.stl')

# Hardware, cushioning and liner are inspection models, never printable parts.
reset();hardware=[]
for m in PCB_MOUNTS['mounts']:
    o=prism('PCB-'+m['name'],5,5,2.5,-3.3,-.8,x=m['x'],y=m['y'])
    add(o,prism('PCB-shaft',2.5,2.5,1.25,-.81,3.2,x=m['x'],y=m['y']));hardware.append(o)
for o in hardware:paint(o,display_flex.material('fastener',(.65,.67,.69)))
export_glb(hardware,'pcb-cover-fasteners.glb')
reset();pads=[]
front_pads=[(side*27.1,y,1.4,10) for side in (-1,1) for y in (-22,8,32)]+[(x,y,10,1.4) for x in (-16,16) for y in (-34.4,55.4)]
for idx,(x,y,w,h) in enumerate(front_pads):pads.append(box('front-screen-pad-'+str(idx),(w,h,.15),(x,y,-4.725)))
for side in (-1,1):
    for tip in CLIP_TIPS:pads.append(box('clip-pad',(0.55,4,.35),(side*27.82,tip,-3.575)))
for x in (-12,12):pads.append(box('upper-display-pad',(10,1.4,.35),(x,55.4,-3.575)))
for o in pads:paint(o,display_flex.material('display-compatible-foam',(.32,.34,.36)))
export_glb(pads,'display-cushioning.glb')
reset();liner=prism('battery-insulating-adhesive-liner',49.4,69,1.0,CELL_BASE-LINER_THICKNESS,CELL_BASE,x=CELL_X,y=CELL_Y)
paint(liner,transparent_material('PET-insulating-liner',(.93,.93,.93),.65))
export_glb([liner],'battery-liner-DO-NOT-PRINT.glb')
reset();adhesive=[box('battery-mount-adhesive',(10,50,ADHESIVE_THICKNESS),(x,CELL_Y,LID_INNER-ADHESIVE_THICKNESS/2)) for x in (CELL_X-15,CELL_X+15)]
for o in adhesive:paint(o,display_flex.material('nonconductive-foam-adhesive',(.65,.65,.65)))
export_glb(adhesive,'battery-adhesive-DO-NOT-PRINT.glb')
reset();cell=prism('protected-cell-nominal',49.2,68.8,1.4,CELL_BASE,CELL_BASE+CELL_THICKNESS,x=CELL_X,y=CELL_Y)
paint(cell,display_flex.material('protected-pouch-envelope',(.3,.52,.72)))
export(cell,'battery-envelope-DO-NOT-PRINT.stl')
reset();antenna=prism('Taoglas-film',5.9,4.1,.2,LID_INNER-.24,LID_INNER,x=25,y=44)
export(antenna,'antenna-envelope-DO-NOT-PRINT.stl')
reset();display=display_flex.SPEC['panel']
panel=prism('ER-EPD3.97-1RY-nominal-outline',display['width'],display['height'],1,display['frontZ'],display['backZ'],y=display['centerY'])
active=prism('480x800-active-area',51.84,86.4,.3,-4.71,-4.65,y=10.5)
paint(panel,display_flex.material('EPD-black-perimeter',(.075,.075,.08)))
paint(active,display_flex.material('EPD-paper',(.86,.85,.77)))
flex,length=display_flex.create_flex();connector=display_flex.SPEC['connector']
for o in (panel,active,*flex):o.location.y-=connector['centerY'];o.location.z-=connector['boardSurfaceZ']
export_glb([panel,active,*flex],'display-panel.glb')
(OUT/'mesh-check.json').write_text(json.dumps(report,indent=2)+'\n')
spec={'revision':'E','printedParts':['front-chassis','rear-cover'],'outsideMm':[CASE_W,CASE_H,round(LID_OUTER-FRONT_Z,3)],'frontZ':FRONT_Z,'seamZ':SEAM_Z,'rearInnerZ':LID_INNER,'rearOuterZ':LID_OUTER,'battery':{'centerX':CELL_X,'centerY':CELL_Y,'baseZ':CELL_BASE,'sizeMm':[49.2,68.8,CELL_THICKNESS],'linerThickness':LINER_THICKNESS,'linerZ':[CELL_BASE-LINER_THICKNESS,CELL_BASE],'mountAdhesiveThickness':ADHESIVE_THICKNESS,'guideBaseZ':GUIDE_BASE,'lowerStopY':CELL_Y-35,'loadingOffsetY':6.5,'loadingStandOffZ':CELL_LOADING_STANDOFF,'loadingDirection':'insert +Z at Y -2, slide -Y 6.5 mm with 0.1 mm lid stand-off, then seat adhesive before fitting PCB'},'screen':{'rebateFloorZ':-4.8,'frontPadThickness':.15,'clipFaceZ':CLIP_PAD_Z,'rearPadThickness':.35,'clipSides':[-1,1],'clipTipY':list(CLIP_TIPS),'beamLength':14.,'beamWidth':.8,'beamZ':[-3.4,-2.2],'releaseDeflectionMm':1.0,'topSupportX':[-12.,12.]},'coverSnaps':{'count':4,'sides':[-1,1],'tipY':list(SNAP_TIPS),'beamLength':SNAP_LENGTH,'beamWidth':.8,'beamZ':[4.7,8.3],'hookOuterX':33.6,'retainingFaceX':33.2,'retainingWallThicknessMm':.8,'hookEngagementMm':.4,'releaseDeflectionMm':SNAP_RELEASE,'windowZ':[3.,4.5],'printedClosureParts':0,'coverScrews':0},'cadAlpha':{'front':.38,'rear':.22},'scope':'Nominal CAD and toolpaths. Clear PETG is translucent; CAD transparency does not predict optical clarity. Physical fit, flexure force/fatigue and battery lead routing need prototype testing.'}
(OUT.parent/'enclosure-design.json').write_text(json.dumps(spec,indent=2)+'\n')
from runpy import run_path
run_path(str(ROOT/'scripts/prepare-print-package.py'))
print(json.dumps(report,indent=2))
