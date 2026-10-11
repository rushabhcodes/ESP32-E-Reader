"""Compare panel tolerances and installed geometry with primary drawings.

A nominal fit is not sufficient to clear PCB ordering. Keep unresolved supplier
acceptance, panel pin numbering and physical bends visible as a failing gate.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / 'assets/enclosure/display-connection.json'
spec = json.loads(SPEC_PATH.read_text())
f = spec['flex']
assert spec['connector']['partNumber'] == 'FH34SRJ-24S-0.5SH(50)', 'Refresh the drawing comparison for a different connector'
assert f['contacts'] == 24 and f['contactPitch'] == .5 and f['width'] == 12.5
findings = []
if f['flatRootLength'] < 15.0:
    findings.append({'id':'bend_position','reason':'First bend must not precede the OEM line 17.40 minus 2.40 = 15.00 mm from glass.'})
# Hirose FH34 catalogs: recommended single-sided FPC dimensions.
# Compare full tolerance ranges, not just matching nominal values.
comparisons = [
    ('reinforced_thickness', [.25,.35], [.27,.33]),
    ('exposed_contact_length', [1.4,2.0], [1.2,1.8]),
    ('stiffener_length', [2.7,3.3], [2.2,2.8]),
]
for name, panel, recommended in comparisons:
    if panel[0] < recommended[0] or panel[1] > recommended[1]:
        findings.append({'id':name,'panel_range_mm':panel,'hirose_recommended_range_mm':recommended,
                         'reason':'Panel tolerance is not fully contained in the recommended FPC drawing. A longer exposed area/stiffener is not automatically a mechanical failure, but requires supplier acceptance or a sample mating test; the published recommendation alone cannot clear it.'})
findings.append({'id':'panel_contact_width','cad_width_mm':f['contactWidth'],'hirose_recommended_range_mm':[.27,.33],
                 'reason':'The panel drawing does not dimension individual finger width. The 0.35 mm CAD fingers are illustrative, not a supplier width/tolerance; actual contact overlap must be checked.'})
if not spec['route']['panelPin1Verified']:
    findings.append({'id':'panel_pin_1','reason':'The panel mechanical drawing labels a white oil line, not pin 1. CAD finger numbers follow the canonical supplier socket (+X pin 1); panel direction must be established independently before ordering/powering.'})
findings.append({'id':'installed_bend_radius','modeled_radius_mm':f['bendRadius'],
                 'reason':'The OEM marks the bend line but does not specify a minimum installed radius. The modeled 0.6 mm radius and full insertion need physical validation.'})
report = {
    'status':'requires_supplier_or_sample_confirmation' if findings else 'drawing_checks_pass_sample_required',
    'pcb_order_ready':False,
    'selected_connector':spec['connector']['partNumber'],
    'supplier_part':spec['connector']['supplierPartNumber'],
    'model_spec_sha256':hashlib.sha256(SPEC_PATH.read_bytes()).hexdigest(),
    'nominal_matches':{'positions':24,'pitch_mm':.5,'tip_width_mm':12.5,'reinforced_thickness_mm':.3,
                       'panel_contact_length_mm':1.7,'recommended_contact_range_mm':[1.2,1.8],
                       'panel_stiffener_mm':3.0,'older_catalog_stiffener_minimum_mm':2.5,
                       'flat_root_mm':f['flatRootLength'],'drawing_bend_line_mm':15.0,
                       'contact_face':'BACK on flat panel, -Z after edge wrap; dual-contact socket'},
    'findings':findings,
    'sources':[
        {'url':spec['sources']['panel'],'revision':'1.0','printed_page':4,'pdf_page':7},
        {'url':'https://www.hirose.com/en/product/series/FH34SRJ/documents?path=%2Fapi%2Fv1%2Fseries%2FFH34SRJ%2Fdocuments%2Fproduct_series_catalog%2Fcontent%3Flang%3DEN','revision':'March 2025','section':'FH34SRJ Recommended FPC Dimensions'},
        {'url':'https://www.hirose.com/en/product/document?clcode=CL0580-1255-6-99&documentid=en_FH34_CAT&documenttype=Catalog&lang=en&productname=FH34SRJ-24S-0.5SH%2899%29&series=FH34SRJ','section':'Recommended FPC/FFC Dimensions'},
        {'url':'https://static.chipdip.ru/lib/240/DOC041240712.pdf','author':'HIROSE ELECTRIC CO., LTD.','date':'2021-02-01','printed_page':5},
        {'url':'https://www.mouser.com/datasheet/2/185/FH34SRJ_catalog-939325.pdf','author':'HIROSE ELECTRIC CO., LTD.','section':'older catalog: stiffener 2.5 mm min'},
    ],
    'scope':'The gross FH12 short-tip mismatch and early fold were corrected. FH34SRJ is a nominally compatible candidate, not manufacturer-approved for every panel tolerance. This gate intentionally fails until the remaining acceptance/pin-1/physical-fit evidence is recorded. No physical sample has been tested.'
}
(ROOT/'assets/enclosure/stl/display-interface-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
sys.exit(1 if findings else 0)
