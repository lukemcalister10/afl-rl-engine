"""ITEM I calibration round 2 — variant sweep against the filed levels A1.6621 B1.5883 C1.6028 D1.5468."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
from engine_load import load
import numpy as np
g = load()
MA = g['MA']; ev = g['ev']
D = MA.LENS['bal']; REPL = MA.REPL; posval = MA.posval; capt_prem = MA.capt_prem
real = [p for p in MA.data if g['_isreal'](p)]

def cs(p):
    d = MA.debut(p); out = []
    for s in p['scoring']:
        if s['games'] <= 0: continue
        k = s['year'] - d + 1
        if k >= 1: out.append((k, s['games'], s['avg']))
    return sorted(out)

def deliv(p, from_k, avail, hor):
    rp = REPL.get(MA.gfut(p), 70.0); t = 0.0
    for k, gm, av in cs(p):
        if k < from_k: continue
        if hor and k > hor: continue
        G = gm if avail == 'in' else 21.0
        t += posval(av + capt_prem(av) - rp) * G / ((1 + D) ** (k - from_k))
    return t

CACHE = {}
def price4(p):
    k = p['key']
    if k not in CACHE:
        try: CACHE[k] = float(ev(p, MA.debut(p) + 3))
        except Exception: CACHE[k] = None
    return CACHE[k]

def cohort(name):
    out = []
    for p in real:
        c = cs(p)
        if not c: continue
        ks = [x[0] for x in c]
        if 4 not in ks or max(ks) < 5: continue
        if name == 'nd' and (p.get('type') != 'ND' or MA.is_pool(p)): continue
        if name == 'done' and not (p.get('_retired') or g['delisted'](p)): continue
        if name == 'nd_done' and ((p.get('type') != 'ND' or MA.is_pool(p)) or not (p.get('_retired') or g['delisted'](p))): continue
        if name == 'k11' and max(ks) < 11: continue
        out.append(p)
    return out

TARGET = {('in','full'):1.6621, ('in',11):1.5883, ('rate','full'):1.6028, ('rate',11):1.5468}
for cname in ('all','nd','done','nd_done','k11'):
    rows = cohort(cname)
    line = []
    for avail in ('in','rate'):
        for hor in (None, 11):
            ss = sr = 0.0; per = []
            for p in rows:
                pr = price4(p); dl = deliv(p, 4, avail, hor)
                if pr is None or dl <= 0: continue
                ss += pr; sr += dl; per.append(pr/dl)
            tgt = TARGET[(avail, 'full' if hor is None else 11)]
            line.append('%s/%s SS=%.4f med=%.4f (tgt %.4f)' % (avail, hor or 'full', ss/sr if sr else 0,
                                                               float(np.median(per)) if per else 0, tgt))
    print('%-8s n=%-5d %s' % (cname, len(rows), ' | '.join(line)))
