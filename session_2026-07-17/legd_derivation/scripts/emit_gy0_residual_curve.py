"""LEG-D ACT-2 — the G-Y0 DIAGNOSTIC: the residual PER EXACT PICK, kernel-smoothed across picks, committed
as a CURVE artifact for the owner's viewing (R2). NO decile/band tables as gated or headline numbers
(CORE rule 7). Runs the REAL engine (RL_PVC2 from env) so v0_start is the POST-SWAP day-after value.
Writes out/gy0_residual_curve_v2.json. Report-only diagnostic; the HARD gate is the pooled number."""
import os, io, contextlib, json, sys
import numpy as np
from collections import defaultdict

G = {'__name__': '_legd_resid'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA = G['MA']; v0_start = G['v0_start']; _PVC0 = G['_PVC0']
INCURVE = {'ND', 'RD'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p)]
best = {}
for p in players:
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())
pool = [p for p in players if p.get('type') in INCURVE and MA.effpk(p) and 2004 <= (p.get('year') or 0) <= 2024]

byp = defaultdict(list)
for p in pool:
    with contextlib.redirect_stdout(io.StringIO()):
        byp[MA.effpk(p)].append(v0_start(p))
picks = sorted(byp)
cur = {k: int(round(_PVC0[min(k, 99)])) for k in picks}
meanv0 = {k: float(np.mean(byp[k])) for k in picks}
n = {k: len(byp[k]) for k in picks}

# kernel-smooth the per-exact-pick residual across picks (log-pick Gaussian, entrant-weighted) — the owner curve
lp = np.log(np.array(picks)); resid = np.array([meanv0[k] - cur[k] for k in picks])
wn = np.array([n[k] for k in picks], float)
def smooth(target, h=0.20):
    w = np.exp(-0.5 * ((lp - np.log(target)) / h) ** 2) * wn
    return float(np.sum(w * resid) / np.sum(w))
smoothed = {k: round(smooth(k), 1) for k in range(1, 100)}
rel_smoothed = {k: round(100 * smoothed[k] / cur.get(k, _PVC0[min(k, 99)]), 2) for k in range(1, 100)}

# pooled HARD gate number (the composition-weighted mean day-after V0 vs curve, aggregate)
num = sum(n[k] * (meanv0[k] - cur[k]) for k in picks); den = sum(n[k] * cur[k] for k in picks)
pooled = round(abs(100 * num / den), 3)

out = dict(
    _doc="G-Y0 residual PER EXACT PICK, kernel-smoothed across picks (owner-viewing diagnostic; REPORT-ONLY). "
         "The HARD gate is the single POOLED number below (composition-weighted mean day-after V0 - curve). "
         "NO decile/band table is a gated or headline number (CORE rule 7 / owner ruling R2).",
    RL_PVC2=os.environ.get('RL_PVC2', '1'),
    gate_pooled_abs_pct=pooled, gate_hard_bound_pct=2.0, gate_pass=bool(pooled <= 2.0),
    curve='pvc_curve_v2.json (== _PVC0 post-swap)',
    smoothed_residual_per_pick=smoothed,            # SCAR, day-after V0 minus curve, smoothed over exact pick
    smoothed_residual_rel_pct=rel_smoothed,
    raw_per_pick={str(k): dict(n=n[k], meanV0=round(meanv0[k], 1), curve=cur[k],
                               resid=round(meanv0[k] - cur[k], 1)) for k in picks},
)
json.dump(out, open('/home/user/afl-rl-engine/session_2026-07-17/legd_derivation/out/gy0_residual_curve_v2.json', 'w'), indent=1)
print("G-Y0 owner-viewing residual curve written. pooled |%.3f%%| <= 2%% : %s" % (pooled, pooled <= 2.0))
print("smoothed rel residual at picks 1,3,10,30,50,80,99:",
      {k: rel_smoothed[k] for k in (1, 3, 10, 30, 50, 80, 99)})
sys.exit(0 if pooled <= 2.0 else 1)
