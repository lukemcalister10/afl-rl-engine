"""Cohort no-arbitrage ratio + B1 shape on a walk-forward matrix (aggregate across cohorts 2004-2020, incurve).
Usage: python3 book_ratio.py <matrix.json> [label]"""
import json, sys
import numpy as np

mpath = sys.argv[1]; label = sys.argv[2] if len(sys.argv) > 2 else mpath
mat = json.load(open(mpath))
S = {}
for v in mat.values():
    C = int(v['year'])
    if not v['incurve'] or not (2004 <= C <= 2020):
        continue
    for i, _y in enumerate(v['yrs']):
        N = i + 1
        if N > 7:
            break
        S[(C, N)] = S.get((C, N), 0.0) + float(v['Vpath'][i] or 0.0)
cohorts = sorted({c for c, _ in S})
tot = {N: sum(S[(C, N)] for C in cohorts if (C, N) in S) for N in range(1, 8)}
A46 = np.mean([tot[N] for N in (4, 5, 6)]); A12 = np.mean([tot[N] for N in (1, 2)])
ratio = 100 * A46 / A12
R = {C: {N: 100.0 * S[(C, N)] / max(S[(C, 1)], 1e-9) for N in range(1, 8) if (C, N) in S} for C in cohorts}
AVG = {N: float(np.mean([R[C][N] for C in cohorts if N in R[C]])) for N in range(1, 8)}
ppk = max(AVG, key=AVG.get)
path_ok = all(AVG[N + 1] >= 0.95 * AVG[N] for N in range(1, ppk) if N + 1 in AVG)
b1_ok = ppk in (4, 5, 6) and AVG[ppk] > 100.0 and path_ok
print(f'=== {label} ===')
print('aggregate totals: ' + ' '.join(f'N{N}:{tot[N]:,.0f}' for N in sorted(tot)))
print(f'NO-ARBITRAGE RATIO (agg avg y4-6 / agg avg y1-2) = {ratio:.1f}%   (HARD <=130, guide 120-125)')
print('B1 avg row: ' + ' '.join(f'{N}:{AVG[N]:.0f}' for N in sorted(AVG)))
print(f'B1 gate: peak N={ppk} AVG={AVG[ppk]:.1f} path_ok={path_ok} -> {"PASS" if b1_ok else "FAIL"}')
json.dump({'label': label, 'ratio': ratio, 'totals': tot, 'b1_avg': AVG, 'b1_peak': ppk, 'b1_ok': b1_ok},
          open('/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out/ratio_' +
               label.replace('/', '_').replace(' ', '_') + '.json', 'w'), indent=1)
