#!/usr/bin/env python3
"""Load the engine and dump the PICK CURVE machinery for picks 1,2,3,5,10,20,30,50,70:
   V0 curve (fitted, from _iso_dec->_fit_pick_curve), pick-currency _PVC0/draftval (loaded, pick1=3000),
   RUC ceiling grid endpoints, and the numeraire (pick 1). Run under different CPU env to compare."""
import os, sys, io, contextlib, json
WS=os.environ.get('RL_WS','/home/claude/rl_workspace/rl_after')
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
try:
    import config_manifest as _cm; _cm.enforce()
except Exception: pass
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(WS,'_merged_recover.py')).read().split('print("=== AFTER')[0], g)
PICKS=[1,2,3,5,10,20,30,50,70]
out={'env':{k:os.environ.get(k) for k in ('OPENBLAS_CORETYPE','NPY_DISABLE_CPU_FEATURES','RL_PRIOR_TREES')}}
# pick-currency (loaded, pick1=3000)
draftval=g.get('draftval'); PVC0=g.get('_PVC0')
star=g.get('_V0CURVE_META',{}).get('_star')
cp=g.get('cp')
# build a synthetic MID player at each pick to get the pick-currency + V0
def pv(pk):
    row={'v0':None,'pvc':None}
    try:
        if star is not None: row['v0']=round(star('MID',18,pk),3)
    except Exception as e: row['v0']='ERR:%s'%e
    try:
        if PVC0 is not None: row['pvc']=PVC0.get(min(pk, g['cp'].KMAX)) if hasattr(PVC0,'get') else PVC0[min(pk,g['cp'].KMAX)]
    except Exception as e: row['pvc']='ERR:%s'%e
    return row
out['picks']={pk:pv(pk) for pk in PICKS}
# RUC ceiling grid
rc=g.get('_RUCCEIL',{})
if 'grid' not in rc and '_build_ruc_ceiling' in g:
    with contextlib.redirect_stdout(io.StringIO()): g['_build_ruc_ceiling']()
    rc=g.get('_RUCCEIL',{})
if 'grid' in rc:
    xg,yg=rc['grid']; out['ruc_ceiling']={'grid_lo':round(float(yg[0]),4),'grid_hi':round(float(yg[-1]),4),'n':len(yg),'y_mid':round(float(yg[len(yg)//2]),4)}
# numeraire: pick-1 pick-currency
out['pick1_pvc']= (PVC0.get(1) if hasattr(PVC0,'get') else None)
# V0 curve full grid checksum (all 6 age18 positions) — sensitive residual detector
meta=g.get('_V0CURVE_META',{})
import hashlib
c18=meta.get('_c18',{})
h=hashlib.sha256()
for pos in sorted(c18): h.update(pos.encode()); h.update(json.dumps([round(x,6) for x in c18[pos]]).encode())
out['v0_c18_sha']=h.hexdigest()[:16]
print(json.dumps(out,indent=1,default=str))
