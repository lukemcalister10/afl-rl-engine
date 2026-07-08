"""L1c TASK 1 — derive the TRAILING evidence-conditioned expected-rerating cell table + census.

INPUT: the CREDIT-OFF (RL_YOUNG=0) walk-forward as-of matrix (s4_matrix machinery: every value at year Y is
priced with scoring truncated <= Y, BASE_REF=Y, backtest path). The engine with the young lever OFF is the
"prices year-1 on delivered evidence only" engine of the investigation — the class re-rating measured on ITS
prices is exactly the gap the credit pays forward. One-shot derivation (declared): no fixed-point iteration.

MEASURE (per cell): one-year re-rating at the year-1 anchor, ATTRITION AND BUSTS INCLUDED —
    R = [kernel-weighted SUM of class values at career-year 2] / [same at career-year 1] - 1
computed as a SMOOTH function of log-pick (adaptive Gaussian bandwidth grown until local eff-n >= 35, the
D14 V0-curve convention — never wide bins as one number). A player whose path has ended contributes 0 to the
year-2 sum (attrition included). Cells: position-group (6) x played/sat-year-1 (sat = 0 games in calendar
year C+1). Pooling rungs, declared per cell, escalated only when min eff-n at max bandwidth < 35:
    rung 0 = (pos6, sat) -> rung 1 = (KPP/nonKPP/RUC, sat) -> rung 2 = (all positions, sat)
    -> rung 3 = (all positions, sat+played pooled)
TRAILING (leak-free): table_T uses only classes C with C+2 <= T (their year-2 values are as-of data <= T).
Tables built for T = 2007..2026 (min 2 classes; the applied credit at book years Y < 2007 is ZERO —
declared leak-free conservatism). The credit applied at year T reads table_T ONLY.
Ships: engine/rl_after/ycred_table.json (RAW measured R; the engine clips >= 0 at application per the
G-COHORT fix direction — negative cells are reported below as tension, never shipped as cuts).
"""
import json, os, sys
import numpy as np

HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
MAT = sys.argv[1] if len(sys.argv) > 1 else f'{OUT}/s4_matrix_youngoff.json'

# Guard 5 (boot-store) on entry
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('derive_ycred', store_path=f'{HERE}/engine/rl_after/rl_model_data.json')

mat = json.load(open(MAT))
store = json.load(open(f'{HERE}/engine/rl_after/rl_model_data.json'))
games_y1 = {}
for p in store:
    if p.get('key') and p.get('year'):
        games_y1[p['key']] = sum(x['games'] for x in p.get('scoring') or [] if x['year'] == p['year'] + 1)

CLS3 = {'KEY_FWD': 'KPP', 'KEY_DEF': 'KPP', 'GEN_FWD': 'nonKPP', 'GEN_DEF': 'nonKPP', 'MID': 'nonKPP', 'RUC': 'RUC'}
POS6 = ['MID', 'GEN_FWD', 'GEN_DEF', 'KEY_FWD', 'KEY_DEF', 'RUC']
rows = []   # (cls6, sat, C, logpick, v1, v2, v4, key, player, pick)
for v in mat.values():
    C = int(v['year']) if v['year'] is not None else None
    if C is None or not v['incurve'] or v.get('pickless') or not v.get('pick'):
        continue
    if not (2004 <= C <= 2024):
        continue
    cls = v['cpos']
    if cls not in POS6:
        continue
    Vp = v['Vpath']
    v1 = float(Vp[0] or 0.0) if len(Vp) >= 1 else 0.0
    v2 = float(Vp[1] or 0.0) if len(Vp) >= 2 else 0.0          # path ended -> 0 (attrition/bust included)
    v4 = float(Vp[3] or 0.0) if len(Vp) >= 4 else (0.0 if C + 4 <= 2026 else None)
    if v1 <= 0:
        continue
    sat = 1 if games_y1.get(v['key'], 0) == 0 else 0
    rows.append(dict(cls=cls, sat=sat, C=C, lp=float(np.log(min(max(v['pick'], 1), 90))),
                     v1=v1, v2=v2, v4=v4, key=v['key'], player=v['player'], pick=v['pick']))
print(f'derivation pool: {len(rows)} incurve picked players, classes 2004-2024 '
      f'(sat-y1: {sum(r["sat"] for r in rows)})')

GRIDPK = list(range(1, 91)); LGRID = np.log(GRIDPK)
EFFN, H0, HMAX = 35.0, 0.18, 2.6

def kernel_R(sub):
    """R(log-pick) on the grid as ratio of kernel-weighted sums; returns (grid, min_effn_at_hmax)."""
    lx = np.array([r['lp'] for r in sub]); a1 = np.array([r['v1'] for r in sub]); a2 = np.array([r['v2'] for r in sub])
    grid = []; mineff = 1e9
    for lg in LGRID:
        h = H0
        while True:
            w = np.exp(-0.5 * ((lx - lg) / h) ** 2); sw = w.sum()
            effn = (sw * sw) / float(np.sum(w * w)) if sw > 0 else 0.0
            if effn >= EFFN or h >= HMAX:
                break
            h *= 1.15
        mineff = min(mineff, effn)
        s1 = float(np.dot(w, a1)); s2 = float(np.dot(w, a2))
        grid.append(s2 / s1 - 1.0 if s1 > 0 else 0.0)
    return grid, mineff

def build_table(pool):
    """One (cls6 x sat) -> R-grid table from a class pool, with declared pooling rungs."""
    tab = {}; rungs = {}
    for cls in POS6:
        for sat in (0, 1):
            cands = [
                (0, [r for r in pool if r['cls'] == cls and r['sat'] == sat]),
                (1, [r for r in pool if CLS3[r['cls']] == CLS3[cls] and r['sat'] == sat]),
                (2, [r for r in pool if r['sat'] == sat]),
                (3, pool),
            ]
            for rung, sub in cands:
                if len(sub) < EFFN:
                    continue
                grid, mineff = kernel_R(sub)
                if mineff >= EFFN or rung == 3:
                    tab.setdefault(cls, {})[str(sat)] = [round(x, 4) for x in grid]
                    rungs[(cls, sat)] = (rung, len(sub), mineff)
                    break
            else:
                grid, mineff = kernel_R(pool)
                tab.setdefault(cls, {})[str(sat)] = [round(x, 4) for x in grid]
                rungs[(cls, sat)] = (3, len(pool), mineff)
    return tab, rungs

# ---- trailing tables per T ----
TABLE = {}; RUNGS = {}
for T in range(2007, 2027):
    pool = [r for r in rows if r['C'] + 2 <= T]
    if len({r['C'] for r in pool}) < 2:
        continue
    TABLE[str(T)], RUNGS[T] = build_table(pool)
FULL, FULL_RUNGS = build_table(rows)     # leaky full-window comparator (EVIDENCE ONLY — trailing ships)

# ---- census (full window, rung-0 grouping wherever the data lives) ----
def decile_share(sub, hkey):
    d = [ (r[hkey] - r['v1']) for r in sub if r[hkey] is not None ]
    if len(d) < 10 or sum(d) <= 0:
        return None
    d = sorted(d, reverse=True); k = max(1, int(round(len(d) * 0.10)))
    return round(sum(d[:k]) / sum(d), 3)

census = []
for cls in POS6:
    for sat in (0, 1):
        sub = [r for r in rows if r['cls'] == cls and r['sat'] == sat]
        rung, n_used, mineff = RUNGS[2026].get((cls, sat), (None, 0, 0.0))
        g = TABLE['2026'][cls][str(sat)]
        reps = {pk: round(g[pk - 1], 3) for pk in (1, 3, 8, 15, 30, 50, 70)}
        census.append(dict(cell=f'{cls}/{"sat" if sat else "played"}', n_cell=len(sub),
                           pool_rung=rung, n_pooled=n_used, min_effn=round(mineff, 1),
                           R_at_pick=reps,
                           topdecile_share_y2=decile_share(sub, 'v2'),
                           topdecile_share_y4=decile_share(sub, 'v4')))
json.dump(dict(doc=__doc__, G0=46, G0_basis='median cum games end-y3=37 / end-y4=54 (674 normal developers, '
               '>=10g in >=2 of first 4 seasons, classes 2004-2020); G0=46=midpoint',
               grid_picks=GRIDPK, table=TABLE), open(f'{OUT}/ycred_table.json', 'w'))
json.dump(census, open(f'{OUT}/ycred_census.json', 'w'), indent=1)

print('\n=== CENSUS (full window 2004-2024; R printed at picks 1/3/8/15/30/50/70) ===')
print(f'{"cell":18s}{"n":>5s}{"rung":>5s}{"n_pool":>7s}{"effn":>6s}  R@1    R@3    R@8    R@15   R@30   R@50   R@70   top10%y2  top10%y4')
for c in census:
    r = c['R_at_pick']
    print(f'{c["cell"]:18s}{c["n_cell"]:5d}{str(c["pool_rung"]):>5s}{c["n_pooled"]:7d}{c["min_effn"]:6.0f}  '
          + '  '.join(f'{r[k]:+.2f}' for k in (1, 3, 8, 15, 30, 50, 70))
          + f'   {c["topdecile_share_y2"]}     {c["topdecile_share_y4"]}')

print('\n=== TRAILING vs FULL (evidence line; TRAILING ships) — R at pick 8, sat cells ===')
for T in (2010, 2016, 2021, 2026):
    if str(T) not in TABLE:
        continue
    line = f'  T={T} (classes<={T-2}): '
    for cls in POS6:
        tr = TABLE[str(T)][cls]['1'][7]; fu = FULL[cls]['1'][7]
        line += f'{cls} {tr:+.2f}/{fu:+.2f}  '
    print(line)
print('  (pairs = trailing/full; full uses classes the credit-year could not yet see -> leaky, NOT shipped)')

neg = [c['cell'] for c in census if min(c['R_at_pick'].values()) < 0]
print(f'\nTENSION REPORT — cells with measured-NEGATIVE re-rating somewhere on the pick axis: {neg or "none"}')
print('  (engine clips R>=0 at application: fix direction = raise year-1, never cut young)')
print(f'\nwrote {OUT}/ycred_table.json + ycred_census.json')
