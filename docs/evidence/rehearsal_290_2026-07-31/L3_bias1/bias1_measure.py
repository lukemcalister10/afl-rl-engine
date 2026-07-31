#!/usr/bin/env python3
"""L3 BIAS-1 — BOTH LIMBS MEASURED. #290, seam word 2026-07-31: nothing chosen silently.

Window A keeps the 2003 class, so both limbs are live.

  LIMB 1  the PHANTOM ROWS. The store's scoring begins in 2005. A 2003 draftee (debut 2004)
          emits a training row at Y=2004 carrying games=0 / exposure=0 / level=0 -- not because
          he did not play, but because the store cannot see 2004. Measured: 64 such rows.
          (The 214 rows at Y==d0 are DRAFT-YEAR rows and are zero BY DESIGN -- not this limb.)

  LIMB 2  the TENURE OFFSET. _feat uses ten = Y-(debutyr-1). A 2003 draftee at Y=2005 reads
          tenure 2 carrying ONE observed season; a 2004 draftee at Y=2005 reads tenure 1 carrying
          one. Same evidence, one tenure-year older. Touches all 641 of the class's rows.

Four treatments, each a full independent prior build:
  T0  as-is (baseline)
  T1  limb 1 only  -- drop rows for seasons the store cannot observe
  T2  limb 2 only  -- tenure re-anchored to the first OBSERVABLE season
  T3  both

NOTHING IS CHOSEN HERE. Every treatment is measured and reported.
"""
import os, sys, io, json, time, contextlib, collections
import numpy as np

OUT = os.environ['L3_OUT']; os.makedirs(OUT, exist_ok=True)
NTREES = int(os.environ.get('RL_PRIOR_TREES', '400'))
ONLY = os.environ.get('L3_ONLY')          # optional: run one treatment

sys.path.insert(0, os.environ['RL_FV'])
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    import conditional_prior as CP
from sklearn.ensemble import GradientBoostingRegressor

FIRST_OBS = min(x['year'] for p in MA.data for x in (p.get('scoring') or []))
RESOLVED_CUT, CAP = 2021, 2026
Q = CP.Q

def eff_debut(p, limb2):
    """Limb 2: anchor tenure to the first OBSERVABLE season, not the nominal debut."""
    d = CP.debutyr(p)
    return max(d, FIRST_OBS) if limb2 else d

def feat(p, Y, limb2):
    """CP._feat, verbatim, except that tenure uses eff_debut under limb 2."""
    oh = [0.0]*len(CP.GROUPS); oh[CP.GIDX[MA.gfut(p)]] = 1.0
    ep = min(MA.effpk(p), CP.KMAX)
    ten = max(0, Y - (eff_debut(p, limb2) - 1))
    return oh + [np.log(ep), CP._exposure(p, Y), ten, CP._lvl_eff(p, Y), CP._age_asof(p, Y)]

def emit_rows(limb1, limb2):
    """build_cond_prior's row loop, verbatim, with the limb switches applied."""
    pool = [p for p in MA.data if MA.GRP.get(p['pos'])]
    X, y, prov = [], [], collections.Counter()
    for p in pool:
        if CP.debutyr(p) > RESOLVED_CUT: continue
        if not (p.get('pick') or p.get('_ft')): continue
        d0 = CP.debutyr(p) - 1
        last = max([x['year'] for x in p['scoring']] + [d0])
        for Y in range(d0, min(last, CAP) + 1):
            if limb1 and Y > d0 and Y < FIRST_OBS:
                prov['dropped_unobservable'] += 1          # the phantom rows
                continue
            X.append(feat(p, Y, limb2)); y.append(CP.fwd_best3_from(p, Y, CAP))
            prov['kept'] += 1
    return np.array(X), np.array(y), prov

def build(limb1, limb2):
    X, y, prov = emit_rows(limb1, limb2)
    t = time.time()
    models = {q: GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=NTREES,
              max_depth=4, learning_rate=0.05, min_samples_leaf=25, random_state=0).fit(X, y)
              for q in Q}
    return models, prov, len(y), round(time.time() - t, 1)

def band(p, models, limb2, Y=None):
    if Y is None: Y = MA.BASE_REF
    f = np.array([feat(p, Y, limb2)])
    return np.sort(np.array([float(models[q].predict(f)[0]) for q in Q]))

TREATMENTS = [('T0_baseline', False, False), ('T1_limb1_drop_phantom', True, False),
              ('T2_limb2_tenure_reanchor', False, True), ('T3_both', True, True)]
if ONLY: TREATMENTS = [t for t in TREATMENTS if t[0] == ONLY]

ens = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], ens)
board = ens['MA'].__dict__['players']
c2003 = [p for p in board if CP.debutyr(p) - 1 == 2003]

R = {'first_observable_season': FIRST_OBS, 'n_trees': NTREES,
     'board_population': len(board), 'board_2003_class': len(c2003), 'treatments': {}}
print('L3 BIAS-1 — first observable season %d | board %d | 2003 class on board %d | trees %d'
      % (FIRST_OBS, len(board), len(c2003), NTREES))

for name, l1, l2 in TREATMENTS:
    models, prov, n, secs = build(l1, l2)
    bands = {p['key']: [round(v, 4) for v in band(p, models, l2)] for p in board}
    R['treatments'][name] = {'limb1_drop_phantom': l1, 'limb2_tenure_reanchor': l2,
                             'training_rows': n, 'provenance': dict(prov),
                             'fit_seconds': secs, 'bands': bands}
    print('  %-26s rows %5d  dropped %3d  fit %5.1fs' % (name, n, prov.get('dropped_unobservable', 0), secs))
    json.dump(R, open(os.path.join(OUT, 'bias1_treatments.json'), 'w'))

json.dump(R, open(os.path.join(OUT, 'bias1_treatments.json'), 'w'))
print('wrote', os.path.join(OUT, 'bias1_treatments.json'))
