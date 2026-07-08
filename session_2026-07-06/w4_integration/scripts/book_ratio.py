"""G-COHORT — CONFORMING measure (owner-worded construction, CONSTRAINTS v1.5) + B1 shape, on a
walk-forward as-of matrix.  REPLACES the non-conforming avg(4-6)/avg(y1,y2) aggregation (obituary:
DECISIONS v84 SUPERSEDED list; the 124.6% it printed is STRUCK — audit 2026-07-08).

CONSTRUCTION (asserted here, in code, per the fitted-board-trap rule — code reading is the only basis test):
  * CLASS-YEAR SUMS: for each draft class C (incurve ND/RD, 2004..2020), SUM the class's players' values in
    career year N (calendar year C+N; a player out of the system contributes 0 — attrition/busts included).
  * AVERAGED ACROSS CLASSES: the per-class sums are AVERAGED across the sampled classes -> ONE figure per
    career year N (owner-worded 2026-07-08; per-capita reading OVERRULED, do not resurrect).
  * DENOMINATOR = min(year-1 figure, year-2 figure) (WD-1b, owner-picked; both figures printed).
  * EACH of years 4, 5, 6 is tested INDIVIDUALLY against the denominator: hard <=130%, guide 120-125%.
WALK-FORWARD BASIS (asserted): the input matrix is built by s4_matrix_M1v7.py, which prices every player at
year Y with scoring truncated to <=Y, BASE_REF=AGE_REF=Y, delist state as-of Y, on the BACKTEST path (board-
only laws off, Luke's D14 exemption) — the value scoring cohort year T sees only data <= T. Any L1c young
credit inside ev() reads its TRAILING re-rating table at table_T (classes with C+2 <= T only) — leak-free by
construction (see _merged_recover.py L1c block). A FITTED present-board reading is invalid here and is not
what this script consumes.
Usage: python3 book_ratio.py <matrix.json> [label]"""
import json, sys, os
import numpy as np

mpath = sys.argv[1]; label = sys.argv[2] if len(sys.argv) > 2 else mpath
mat = json.load(open(mpath))
S = {}                                  # S[(C,N)] = class-year SUM (attrition-inclusive: missing/ended = +0)
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
# one figure per career year = AVERAGE of the class-year sums across classes (every class 2004-2020 has
# calendar years C+1..C+7 <= 2027 capped at 2026 -> N=1..6 fully populated, N=7 missing only for 2020)
FIG = {N: float(np.mean([S[(C, N)] for C in cohorts if (C, N) in S])) for N in range(1, 8)}
den = min(FIG[1], FIG[2])               # WD-1b: the LOWER of year-1 / year-2
den_src = 'y1' if FIG[1] <= FIG[2] else 'y2'
ratios = {N: 100.0 * FIG[N] / den for N in (4, 5, 6)}
worst = max(ratios.values())
gc_pass = all(r <= 130.0 for r in ratios.values())
# B1 shape row (auxiliary diagnostic, unchanged semantics: per-class % of its own y1, averaged)
R = {C: {N: 100.0 * S[(C, N)] / max(S[(C, 1)], 1e-9) for N in range(1, 8) if (C, N) in S} for C in cohorts}
AVG = {N: float(np.mean([R[C][N] for C in cohorts if N in R[C]])) for N in range(1, 8)}
ppk = max(AVG, key=AVG.get)
path_ok = all(AVG[N + 1] >= 0.95 * AVG[N] for N in range(1, ppk) if N + 1 in AVG)
b1_ok = ppk in (4, 5, 6) and AVG[ppk] > 100.0 and path_ok
print(f'=== {label} ===  (classes {cohorts[0]}-{cohorts[-1]}, n={len(cohorts)})')
print('class-year figures (avg of class SUMS): ' + ' '.join(f'y{N}:{FIG[N]:,.1f}' for N in sorted(FIG)))
print(f'G-COHORT denominator = min(y1,y2) = {den:,.1f} ({den_src})')
for N in (4, 5, 6):
    print(f'  y{N}/den = {ratios[N]:6.1f}%   (hard <=130, guide 120-125)  {"PASS" if ratios[N] <= 130 else "BREACH"}')
print(f'G-COHORT (each of y4/y5/y6 individually): {"PASS" if gc_pass else "BREACH"}  worst {worst:.1f}%')
print('B1 avg row: ' + ' '.join(f'{N}:{AVG[N]:.0f}' for N in sorted(AVG)))
print(f'B1 gate: peak N={ppk} AVG={AVG[ppk]:.1f} path_ok={path_ok} -> {"PASS" if b1_ok else "FAIL"}')
_outdir = os.environ.get('RATIO_OUT', '/home/user/afl-rl-engine/session_2026-07-08/l1c_rectification/out')
json.dump({'label': label, 'figures': FIG, 'den': den, 'den_src': den_src,
           'ratios_y456': ratios, 'gcohort_pass': gc_pass, 'worst': worst,
           'b1_avg': AVG, 'b1_peak': ppk, 'b1_ok': b1_ok},
          open(os.path.join(_outdir, 'ratio_' + label.replace('/', '_').replace(' ', '_') + '.json'), 'w'),
          indent=1)
