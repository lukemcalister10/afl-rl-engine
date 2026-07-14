#!/usr/bin/env python3
"""IMPLEMENTATION-AGNOSTIC stage diff. Dump a hash of the full float64 state at each pipeline stage,
so we find the FIRST diverging stage regardless of WHICH numpy/BLAS op causes it (np.dot, the @
operator, np.linalg.solve, sklearn-internal gemm, ...). Run native + forced-Haswell, diff.
Usage: OPENBLAS_CORETYPE=<k> python3 stage_diff.py <outfile>"""
import os, sys, io, contextlib, hashlib, struct, json
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
OUT=sys.argv[1]
import numpy as np
def h(*vals):
    m=hashlib.sha1()
    for v in vals:
        m.update(np.ascontiguousarray(np.asarray(v,dtype=np.float64)).tobytes())
    return m.hexdigest()[:16]
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; PR=g['PR']; cp=g['cp']
stages={}
# STAGE A: PAR table (par_build @ / linalg.solve output). Enumerate a dense grid of par_at.
par=[]
with contextlib.redirect_stdout(io.StringIO()):
    for pos in ['MID','GEN_FWD','KEY_FWD','GEN_DEF','KEY_DEF','RUC']:
        for pk in range(1,int(cp.KMAX)+1):
            for T in range(1,7):
                par.append(PR.par_at(pos,pk,T))
stages['A_par_table']=h(par)
# STAGE B: ISO pick guard
ISO=g['ISO']
stages['B_iso_guard']=h([x for pos in sorted(ISO) for x in ISO[pos][1]])
# STAGE C: V0 curve (mature surfaces + age18) — the NW-smoother output
V0=g['_V0CURVE']
stages['C_v0curve']=h([V0[k] for k in sorted(V0.keys(), key=lambda t:str(t))])
# STAGE D: RUC ceiling grid
try:
    g['_build_ruc_ceiling']()
    xg,yg=g['_RUCCEIL']['grid']; stages['D_ruc_ceiling']=h(xg,yg)
except Exception as e:
    stages['D_ruc_ceiling']='ERR:%s'%e
# STAGE E: price6 raw for every player (2026)
pr6=[]; b6=g['b6']; price6=g['price6']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        try: pr6.append(price6(p,b6(p,2026),2026))
        except Exception: pr6.append(float('nan'))
stages['E_price6']=h(pr6)
# STAGE F: final ev (2026) per player
evs=[]
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        evs.append(ev(p,2026))
stages['F_ev']=h(evs)
with open(OUT,'w') as f:
    json.dump({'kernel':os.environ.get('OPENBLAS_CORETYPE','native'),'stages':stages}, f, indent=1)
for k in sorted(stages): print("  %-16s %s"%(k,stages[k]))
