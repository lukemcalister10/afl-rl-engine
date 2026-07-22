"""Engine-level verification of the RL_PVC2 wire + the REAL (post-swap) G-Y0 gate.
Run inside the workspace rl_after with the pinned env. RL_PVC2 taken from the ambient env.
Emits a per-gate verdict dict; exit 0 iff every hard gate passes."""
import os, io, contextlib, json, sys
import numpy as np
from collections import defaultdict

G = {'__name__': '_legd_verify'}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; v0_start = G['v0_start']; _PVC0 = G['_PVC0']; delisted = G['delisted']

PVC2 = os.environ.get('RL_PVC2', '1')
L1b = {int(k): int(v) for k, v in json.load(open('pvc_curve_L1b.json'))['curve'].items()}
V2  = {int(k): int(v) for k, v in json.load(open('pvc_curve_v2.json'))['curve'].items()}

# which curve is _PVC0 now?
p0 = {k: int(round(_PVC0[k])) for k in range(1, 100)}
is_l1b = all(p0[k] == L1b[k] for k in range(1, 100))
is_v2  = all(p0[k] == V2[k] for k in range(1, 100))

# --- build the in-curve derivation pool (emit_matrix.py filter, verbatim spirit) ---
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
        v = v0_start(p)
    byp[MA.effpk(p)].append(v)

cur = {k: p0[min(k, 99)] for k in byp}
picks = sorted(byp)
num = sum(len(byp[k]) * (np.mean(byp[k]) - cur[k]) for k in picks)
den = sum(len(byp[k]) * cur[k] for k in picks)
pooled_net = 100.0 * num / den
mean_rel = 100.0 * np.mean([(v - cur[k]) / cur[k] for k in picks for v in byp[k]])

strict = all(p0[k] > p0[k + 1] for k in range(1, 99))
pin1 = (p0[1] == 3000)

res = dict(RL_PVC2=PVC2, PVC0_is_L1b=is_l1b, PVC0_is_v2=is_v2,
           curve1=p0[1], strict_descent=strict, pin1_3000=pin1,
           pool_n=len(pool), n_picks=len(picks),
           gy0_pooled_abs_pct=round(abs(pooled_net), 3), gy0_mean_rel_pct=round(mean_rel, 3),
           PVC0_sample={k: p0[k] for k in (1, 2, 3, 10, 50, 80, 99)})
print(json.dumps(res, indent=1))

# hard-gate verdict only meaningful when the v2 curve is loaded
ok = True
if PVC2 != '0':
    ok = is_v2 and strict and pin1 and abs(pooled_net) <= 2.0
    print("HARD GATES (RL_PVC2 on): _PVC0==v2 %s | strict %s | pin1 %s | G-Y0 pooled |%.3f%%|<=2%% %s"
          % (is_v2, strict, pin1, abs(pooled_net), abs(pooled_net) <= 2.0))
else:
    ok = is_l1b
    print("KILL-SWITCH (RL_PVC2=0): _PVC0==L1b %s" % is_l1b)
sys.exit(0 if ok else 1)
