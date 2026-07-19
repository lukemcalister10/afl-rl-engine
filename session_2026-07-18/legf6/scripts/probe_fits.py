# LEG F6 job-1 probe: hash each candidate import-time/board-time fit's OUTPUT, so we can see which one
# moves under a forced BLAS coretype (the residual-weather source). Read-only; no engine edits.
import io, contextlib, hashlib, json, sys, os
import numpy as np
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
def h(obj):
    return hashlib.md5(json.dumps(obj, sort_keys=True, separators=(',',':')).encode()).hexdigest()[:12]
out={}
# (1) ISO pick-tax table (lines 461-471): {pos: fs list}
ISO=g['ISO']
out['ISO_table']=h({pos:[round(float(x),9) for x in ISO[pos][1]] for pos in ISO})
# (2) V0 curve per-player dict _V0CURVE
V0=g['_V0CURVE']
out['V0CURVE']=h({'|'.join(map(str,k)):round(float(v),9) for k,v in V0.items()})
# (3) V0 surfaces (the _iso_dec outputs directly)
META=g['_V0CURVE_META']
out['V0_c18']=h({p:[round(float(x),9) for x in META['_c18'][p]] for p in META['_c18']})
out['V0_surfN']=h({str(a):[round(float(x),9) for x in META['_surfN'][a]] for a in META['_surfN']})
out['V0_surfR']=h({str(a):[round(float(x),9) for x in META['_surfR'][a]] for a in META['_surfR']})
# (4) board Σv (ultimate signal) over priced players
ev=g['ev']; MA=g['MA']; GRP=MA.GRP
sv=0.0
for p in MA.data:
    if GRP.get(p.get('pos')):
        try: sv+=float(ev(p))
        except Exception: pass
out['board_sumEV_raw']=round(sv,3)
# (5) q97m sanity (should be frozen/identical always)
print(json.dumps(out, sort_keys=True))
