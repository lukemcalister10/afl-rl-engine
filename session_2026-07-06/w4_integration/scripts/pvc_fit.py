"""W4 PVC FIT (downstream lever, per the re-stamped PVC Derivation Spec v1 / PR #41):
PVC(k) = end-of-calendar-year-1 as-of value of the TYPICAL player at pick k, fitted from the CANDIDATE
walk-forward book anchors (ND, recorded pick, 2004-2024 — the "2004 window": every cohort from the 2004
draft forward). The anchors carry the lifted young values and the LIVE ruck values (nothing hardcoded).
Method: adaptive-bandwidth Nadaraya-Watson MEDIAN over log-pick (eff-n>=35, the house kernel convention) ->
parametric power-decay top (a*k^-b fit on picks 1-8, blended out by pick 12 — the spec's loclin-at-pick-1
top treatment) -> isotonic non-increasing -> re-anchor pick1 = 3000 (RL_PICK1).
Usage: python3 pvc_fit.py <candidate_matrix.json> <out_curve.json>"""
import json, sys, hashlib, os
import numpy as np

mpath, outp = sys.argv[1], sys.argv[2]
mat = json.load(open(mpath))
pts = []
for v in mat.values():
    if v.get('type') != 'ND' or v.get('pickless') or not v.get('incurve'):
        continue
    C = int(v['year'])
    if not (2004 <= C <= 2024):
        continue
    a = v.get('anchor')
    pk = v.get('pick')
    if a is None or pk is None or pk < 1:
        continue
    pts.append((float(pk), float(a)))
print(f'anchor pool: {len(pts)} ND year-1 anchors (2004-2024)')
lx = np.log(np.array([p for p, _ in pts])); vy = np.array([a for _, a in pts])
GRID = list(range(1, 100)); LG = np.log(GRID)

def ksm_median(lg, h0=0.10, hmax=1.6, effn_min=35.0):
    h = h0
    while True:
        w = np.exp(-0.5 * ((lx - lg) / h) ** 2); sw = w.sum()
        effn = (sw * sw) / float(np.sum(w * w)) if sw > 0 else 0.0
        if effn >= effn_min or h >= hmax:
            break
        h *= 1.15
    idx = np.argsort(vy); cw = np.cumsum(w[idx]); cw /= cw[-1]
    return float(vy[idx][np.searchsorted(cw, 0.5)])

raw = [ksm_median(lg) for lg in LG]
# parametric power top from picks 1-8 of the smoothed medians (the spec's trend-extrapolated top)
kf = np.arange(1, 9); yf = np.array([max(raw[i], 1e-6) for i in range(8)])
B, lA = np.polyfit(np.log(kf), np.log(yf), 1); A = float(np.exp(lA))
cur = []
for i, k in enumerate(GRID):
    par = A * k ** B
    if k <= 6:
        cur.append(par)
    elif k >= 12:
        cur.append(raw[i])
    else:
        w = (12 - k) / 6.0
        cur.append(w * par + (1 - w) * raw[i])
for i in range(1, len(cur)):          # isotonic non-increasing
    cur[i] = min(cur[i], cur[i - 1])
f = 3000.0 / cur[0]                    # pick-1 anchor (RL_PICK1)
curve = {k: max(210, int(round(cur[i] * f))) for i, k in enumerate(GRID)}
store_md5 = hashlib.md5(open('/home/claude/rl_workspace/rl_after/rl_model_data.json', 'rb').read()).hexdigest()[:8]
json.dump({'curve': curve, 'fitted_from': os.path.basename(mpath), 'store_md5': store_md5,
           'n_anchors': len(pts), 'window': '2004-2024 ND year-1 anchors (candidate walk-forward book)',
           'anchor_scale_factor': f, 'power_top': {'A': A, 'B': float(B)}},
          open(outp, 'w'), indent=1)
print('curve at key picks:', {k: curve[k] for k in [1, 3, 5, 8, 10, 15, 20, 30, 45, 60, 80]})
print(f'pick-1 anchor factor {f:.3f}; wrote {outp}')
