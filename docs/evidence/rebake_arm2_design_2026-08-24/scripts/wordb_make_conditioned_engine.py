#!/usr/bin/env python3
"""WORD B — build the CONDITIONED-INFERENCE engine workspace. SCRATCH ONLY, never committed.

The conditioned bust prior has to be applied at INFERENCE as well as at training, or the board would
price a model trained on one feature with another feature's values — train/serve skew, which is the
exact defect the frozen pvc_snapshot exists to prevent.

The inference site is `rl_model.py:1235`:

    def _v4_bp(po,pk): return _BUSTPT[po][str(min(max(int(round(pk)),1),70))]

consumed by `_v4_feats(p,Y)` (:1245, the last element) and `_v4_draft_feat(p)` (:1247, likewise).
`_v4_bp` is a pure function of (position, pick) and has no access to the player, so the swap cannot be
made inside it — the CALL SITES have to pass the player and the as-of year. This script rewrites
exactly those two call sites in a SCRATCH copy of rl_model.py and appends the conditioned resolver.

WHY THIS IS NOT AN ENGINE EDIT. Owner word B asks for a MEASUREMENT ("Fit both and show me"), and the
coordinator's brief is explicit that neither version is adopted by this task. So the conditioning lives
in a scratch workspace exactly as the must-move proof's restored ratchet does, and the committed engine
is untouched. If the owner rules for the conditioned version, THAT is when it becomes an engine edit
with its own prereg.

DAY-0: `_v4_draft_feat` passes no seasons, so A == 0 and mu == B identically — the draft row is
byte-exact by construction, and wordb_fit_both.py asserts it on the training side over 2,650 rows.
"""
import argparse, os, sys

APPEND = '''

# ==== WORD B (SCRATCH, NEVER COMMITTED) — the evidence-conditioned bust prior at INFERENCE ==========
# seam-lever CAND-B, constants from CONSTRUCTION.md section 2 (the repricing refit). Applied at the two
# _v4 feature sites so the board prices with the same feature the peak model was trained on.
import math as _wb_math
_WB = {'M1': 149.7064, 'tauM': 2.1061, 'c0': 45.8848, 'w_c': 13.6587,
       'kappa0': 4.6810, 'tauK': 0.4333, 'beta': 0.0, 'r': 0.11, 'damp': 5.8, 'tmax': 4}


def _wb_mu(pos, ep, p, Y):
    """mu = (1-A)*B + A*T. Zero evidence => A == 0 => exactly the static table value."""
    B = _v4_bp(pos, ep)
    t = Y - debut(p) + 1
    if t > _WB['tmax'] or t < 1:
        return B                                  # declared scope clamp: static B outside tenure 1-4
    sub = [x for x in p['scoring'] if x['year'] <= Y and x.get('games', 0) > 0]
    if not sub:
        return B
    W = sum((float(x['games']) ** 2) / (float(x['games']) + _WB['damp']) for x in sub)
    if W <= 0.0:
        return B
    kap = _WB['kappa0'] * _wb_math.exp(-(t - 1) / _WB['tauK'])
    A = (1.0 - _WB['r']) * W / (W + kap)
    den = sum(float(x['games']) for x in sub)
    c = sum(float(x['games']) * float(x['avg']) for x in sub) / den
    M = _WB['M1'] * _wb_math.exp(-(t - 1) / _WB['tauM'])
    c50 = _WB['c0'] + _WB['beta'] * (t - 1)
    z = (c - c50) / _WB['w_c']
    T = 0.0 if z < -700 else M / (1.0 + _wb_math.exp(-z))
    return (1.0 - A) * B + A * T
'''


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='the workspace rl_model.py to rewrite IN PLACE')
    a = ap.parse_args(argv[1:])
    s = open(a.src).read()

    old_feats = "np.log(_V4PVC[str(ep)]),ep,_POSI[pos],b2 or 0,b1 or 0,recent,la,lg,gg,nss,maxg,early,slope,ysb,_v4_age(p,Y),T,_v4_bp(pos,ep)]"
    new_feats = "np.log(_V4PVC[str(ep)]),ep,_POSI[pos],b2 or 0,b1 or 0,recent,la,lg,gg,nss,maxg,early,slope,ysb,_v4_age(p,Y),T,_wb_mu(pos,ep,p,Y)]"
    if s.count(old_feats) != 1:
        raise SystemExit('wordb HALT: _v4_feats bust_prior element not found exactly once')
    s = s.replace(old_feats, new_feats)

    # _v4_draft_feat: the draft row. mu with no seasons == B, so this is byte-exact — but it is
    # rewritten anyway so the two sites cannot drift apart, and the exactness is a PROPERTY rather
    # than an omission.
    old_draft = "0,0,0,0,0,0,0,0,0,0,0,_v4_age(p,debut(p)-1),0,_v4_bp(pos,ep)]"
    new_draft = "0,0,0,0,0,0,0,0,0,0,0,_v4_age(p,debut(p)-1),0,_wb_mu(pos,ep,p,debut(p)-1)]"
    if s.count(old_draft) != 1:
        raise SystemExit('wordb HALT: _v4_draft_feat bust_prior element not found exactly once')
    s = s.replace(old_draft, new_draft)

    # INSERTED IMMEDIATELY BEFORE _v4_bp, NOT APPENDED AT THE END. This seat appended it first and the
    # board build died with `NameError: _wb_mu is not defined`: rl_model.py CALLS _v4_feats during its
    # OWN module-level execution, which is reached long before the end of the file. Definition order is
    # load-bearing in a module that does work at import time.
    anchor = 'def _v4_bp(po,pk):'
    if s.count(anchor) != 1:
        raise SystemExit('wordb HALT: _v4_bp definition not found exactly once')
    s = s.replace(anchor, APPEND.strip() + '\n\n\n' + anchor)
    open(a.src, 'w').write(s)
    import hashlib
    print('conditioned-inference rl_model.py -> %s  md5=%s'
          % (a.src, hashlib.md5(s.encode()).hexdigest()))
    print('  two call sites rewritten; _wb_mu appended; SCRATCH ONLY.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
