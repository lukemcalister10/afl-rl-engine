#!/usr/bin/env python3
"""ORDER S — S5. THE PREMIUM'S DOMAIN AT 24+. FIX B1's WEAKNESS, MEASURED.

READ-ONLY. No engine import, no board build, no store write. PREREG_S.md section 5 fixes the rules.

PG was fitted on the YOUNG cohort's seasons (age 18-23). FIX B1 deletes the age-24 gate and so
applies PG at EVERY age. This file refits the IDENTICAL estimator on MATURE (24+) seasons and asks
whether the price-premium at a given v0 persists, shrinks or vanishes.

ESTIMATOR: ORDER P's own op_lib.Premium — games-weighted local-linear kernel on ln(v0), tricube,
bandwidth 0.40 in log-v0 units, isotonised, 121-point grid. NOTHING about the estimator changes.
Only the population it is fitted on changes. Seed 32, ORDER P's own.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_mature.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
MAT_LO, MAT_HI = 24, 40
L = []


def P(s=''):
    print(s); L.append(str(s))


M = LB.load_matrix('OKRULED')
YOUNG = PB.season_rows(M, 18, 23)
MATURE = PB.season_rows(M, MAT_LO, MAT_HI)

P('=' * 118)
P('ORDER S — S5. IS THE PEDIGREE PREMIUM THE SAME OBJECT AT 24+ AS IT IS AT 18-23?')
P('=' * 118)
P('READ-ONLY measurement. No board is built here. Nothing is adopted.')
P('ruler     : %s' % LB.check_s4_copy())
P('estimator : ORDER P\'s own op_lib.Premium, unchanged — tricube local-linear on ln(v0), h=%.2f,'
  % PB.H_PRIMARY)
P('            games-weighted, isotonised, %d-point grid. Only the POPULATION changes.' % PB.GRID_N)
P()
P('   %-10s %8s %9s %10s %10s %10s' % ('population', 'rows', 'players', 'games', 'med v0', 'mean d'))
for tag, R in (('YOUNG 18-23', YOUNG), ('MATURE %d+' % MAT_LO, MATURE)):
    gw = sum(r['games'] for r in R)
    md = sum(r['games'] * r['d'] for r in R) / gw
    P('   %-10s %8d %9d %10.0f %10.0f %10.3f'
      % (tag, len(R), len(set(r['key'] for r in R)), gw,
         float(np.median([r['v0'] for r in R])), md))
P()
P('   NOTE, and it matters: o32_gate_bar is FLAT at and above age 24, so the mature d is measured')
P('   against the position\'s flat bar with no development delta. That is the SAME bar FIX B1 makes')
P('   the charge read on those rows, so this refit is on exactly the object B1 uses.')
P()

PG_Y = PB.Premium(YOUNG)
PG_M = PB.Premium(MATURE)

# the young cohort's own v0 support, which is where B1's charge is actually read
allv_y = np.array([r['v0'] for r in YOUNG])
V_LO, V_HI = float(np.percentile(allv_y, 10)), float(np.percentile(allv_y, 90))
P('   the 10th-90th percentile of the YOUNG cohort\'s v0 — the materiality window fixed on the')
P('   prereg: %.0f to %.0f' % (V_LO, V_HI))
P()

# =====================================================================================================
P('-' * 118)
P('1 · THE TWO SURFACES, POINT BY POINT')
P('-' * 118)
VS = [100, 200, 400, 600, 800, 1000, 1500, 2000, 2500, 3000, 4000]


def ess_at(x0, sub, h=PB.H_PRIMARY):
    xs = np.array([r['x'] for r in sub]); ws = np.array([r['games'] for r in sub])
    k = PB.tricube((xs - x0) / h) * ws
    return float(k.sum() ** 2 / max(1e-12, (k ** 2).sum())) if k.sum() > 0 else 0.0


ROWS = dict(TALL=[], SMALL=[])
for cls in ('TALL', 'SMALL'):
    ys = [r for r in YOUNG if r['cls'] == cls]
    ms = [r for r in MATURE if r['cls'] == cls]
    P('   %s   (young rows %d, mature rows %d)' % (cls, len(ys), len(ms)))
    P('   %8s %10s %10s %10s | %9s %9s' %
      ('v0', 'PG_young', 'PG_mature', 'gap', 'ESS_young', 'ESS_mat'))
    for v in VS:
        x = math.log(v)
        a = PG_Y.at(x, cls); b = PG_M.at(x, cls)
        ey = ess_at(x, ys); em = ess_at(x, ms)
        ROWS[cls].append(dict(v0=v, young=a, mature=b, gap=b - a, ess_y=ey, ess_m=em))
        P('   %8d %10.3f %10.3f %+10.3f | %9.1f %9.1f' % (v, a, b, b - a, ey, em))
    P()

# =====================================================================================================
P('-' * 118)
P('2 · THE SLOPES — HOW MUCH PREMIUM PER LOG-UNIT OF ENTRY PRICE, YOUNG vs MATURE')
P('-' * 118)


def avg_slope(PG, cls):
    gx, gy = PG.grid[cls]
    return float((gy[-1] - gy[0]) / (gx[-1] - gx[0]))


def span(PG, cls):
    gx, gy = PG.grid[cls]
    return float(gy[-1] - gy[0]), float(math.exp(gx[0])), float(math.exp(gx[-1]))


P('   %-8s %12s %12s %12s' % ('class', 'slope young', 'slope mature', 'ratio'))
SLOPES = {}
for cls in ('TALL', 'SMALL'):
    a, b = avg_slope(PG_Y, cls), avg_slope(PG_M, cls)
    SLOPES[cls] = dict(young=a, mature=b, ratio=(b / a if a else float('nan')))
    P('   %-8s %12.4f %12.4f %12.3f' % (cls, a, b, b / a if a else float('nan')))
P()
P('   %-8s %14s %14s' % ('class', 'span young', 'span mature'))
for cls in ('TALL', 'SMALL'):
    sy = span(PG_Y, cls); sm = span(PG_M, cls)
    P('   %-8s %8.2f pts over %.0f-%.0f | %8.2f pts over %.0f-%.0f'
      % (cls, sy[0], sy[1], sy[2], sm[0], sm[1], sm[2]))
P('   ("span" is the total rise of the fitted premium across that fit\'s own 1-99 pct v0 support.)')
P()

# =====================================================================================================
P('-' * 118)
P('3 · PLAYER-CLUSTERED BOOTSTRAP ON THE GAP. IS THE DIFFERENCE SEPARABLE FROM NOISE?')
P('-' * 118)
P('   %d draws, seed %d, resampled over PLAYERS (not seasons) so a long career cannot narrow the'
  % (B_BOOT, SEED))
P('   interval by pretending to be many independent observations. ORDER R\'s own convention.')
P()
rng = np.random.RandomState(SEED)
keys_y = sorted(set(r['key'] for r in YOUNG))
keys_m = sorted(set(r['key'] for r in MATURE))
byk_y = collections.defaultdict(list); byk_m = collections.defaultdict(list)
for r in YOUNG: byk_y[r['key']].append(r)
for r in MATURE: byk_m[r['key']].append(r)
XQ = [math.log(v) for v in VS]
BOOT = {c: {v: [] for v in VS} for c in ('TALL', 'SMALL')}
for b in range(B_BOOT):
    iy = rng.randint(0, len(keys_y), len(keys_y))
    im = rng.randint(0, len(keys_m), len(keys_m))
    ry = [q for i in iy for q in byk_y[keys_y[i]]]
    rm = [q for i in im for q in byk_m[keys_m[i]]]
    try:
        py = PB.Premium(ry); pm = PB.Premium(rm)
    except Exception:
        continue
    for cls in ('TALL', 'SMALL'):
        for v, x in zip(VS, XQ):
            BOOT[cls][v].append(pm.at(x, cls) - py.at(x, cls))
CI = {c: {} for c in ('TALL', 'SMALL')}
for cls in ('TALL', 'SMALL'):
    P('   %s' % cls)
    P('   %8s %10s %12s %12s %8s' % ('v0', 'gap', 'CI90 lo', 'CI90 hi', 'excl 0?'))
    for v in VS:
        a = np.array(BOOT[cls][v], float)
        lo, hi = float(np.percentile(a, 5)), float(np.percentile(a, 95))
        pt = [r for r in ROWS[cls] if r['v0'] == v][0]['gap']
        CI[cls][v] = (lo, hi)
        P('   %8d %+10.3f %12.3f %12.3f %8s'
          % (v, pt, lo, hi, 'YES' if (lo > 0 or hi < 0) else 'no'))
    P()

# =====================================================================================================
P('-' * 118)
P('4 · IS IT AGE, OR IS IT CAREER STAGE? THE TWO ARE NOT THE SAME OBJECT.')
P('-' * 118)
P('   Career games BEFORE the season (cg_before) is the stage axis. Refitted on stage bands, ages')
P('   pooled, so an early-career 25-year-old and a late-career 25-year-old are separated.')
P()
STAGE = [('0-19 career g', 0, 20), ('20-59', 20, 60), ('60-119', 60, 120),
         ('120-199', 120, 200), ('200+', 200, 10 ** 9)]
ALLR = YOUNG + MATURE
STG = {}
P('   %-14s %7s %8s | %10s %10s %10s %10s' %
  ('stage', 'rows', 'players', 'PG@400', 'PG@1000', 'PG@2000', 'PG@3000'))
for tag, lo, hi in STAGE:
    sub = [r for r in ALLR if lo <= r['cg_before'] < hi]
    if len(sub) < 400:
        P('   %-14s %7d  TOO THIN — not fitted' % (tag, len(sub)))
        STG[tag] = None
        continue
    try:
        pg = PB.Premium(sub)
    except Exception as e:
        P('   %-14s %7d  fit failed: %s' % (tag, len(sub), e)); STG[tag] = None; continue
    vals = {}
    for cls in ('TALL', 'SMALL'):
        vals[cls] = [pg.at(math.log(v), cls) for v in (400, 1000, 2000, 3000)]
    STG[tag] = vals
    P('   %-14s %7d %8d | SMALL %8.3f %10.3f %10.3f %10.3f'
      % (tag, len(sub), len(set(r['key'] for r in sub)), *vals['SMALL']))
    P('   %-14s %7s %8s | TALL  %8.3f %10.3f %10.3f %10.3f'
      % ('', '', '', *vals['TALL']))
P()

# =====================================================================================================
P('-' * 118)
P('5 · WHAT IT MEANS FOR THE CHARGE — THE BAR MOVEMENT ON MATURE ROWS')
P('-' * 118)
P('   The charge reads BAR = o32_gate_bar(pos, age) + PG(ln v0, class). On a mature row FIX B1 makes')
P('   it read the YOUNG PG. Swapping in the mature PG moves the bar by exactly the gap above, and')
P('   the surplus by minus that. A LOWER mature premium => a LOWER bar => a HIGHER surplus =>')
P('   a SMALLER charge.')
P()
gaps = []
for cls in ('TALL', 'SMALL'):
    for r in ROWS[cls]:
        if V_LO <= r['v0'] <= V_HI:
            gaps.append(abs(r['gap']))
maxgap_win = max(gaps) if gaps else 0.0
P('   MAX |gap| inside the prereg materiality window (v0 %.0f-%.0f): %.3f points a game'
  % (V_LO, V_HI, maxgap_win))
P('   MAX |gap| anywhere on the printed grid                      : %.3f points a game'
  % max(abs(r['gap']) for c in ROWS for r in ROWS[c]))
P('   S5-F1 bar: <= 1.0 point a game everywhere in the window would make the domain concern a NULL.')
P('   S5-F1: %s' % ('*** FIRES — THE DOMAIN CONCERN IS A NULL, NO REFIT IS PRICED ***'
                    if maxgap_win <= 1.0 else 'does NOT fire — the surfaces differ materially'))
P()

# monotonicity check on the mature grid (S5-F2)
mono_ok = True
for cls in ('TALL', 'SMALL'):
    gx, gy = PG_M.grid[cls]
    for i in range(1, len(gy)):
        if gy[i] < gy[i - 1] - 1e-12:
            mono_ok = False
P('   S5-F2 (mature grid not monotone after isotonisation): %s'
  % ('*** FIRED ***' if not mono_ok else 'does not fire'))
P()

# the Setterfield-shaped population: above the AGE bar, below the PEDIGREE bar, 24+
sh = [r for r in MATURE if r['d'] > 0 and r['d'] < PG_Y.at(r['x'], r['cls'])]
shg = sum(r['games'] for r in sh)
P('   THE WATCHED SHAPE (never a target): mature rows ABOVE their age bar but BELOW the pedigree bar')
P('     rows %d of %d mature (%.1f%%), %.0f games, mean v0 %.0f'
  % (len(sh), len(MATURE), 100.0 * len(sh) / len(MATURE), shg,
     float(np.mean([r['v0'] for r in sh])) if sh else float('nan')))
P('     their mean shortfall against the YOUNG premium bar : %.3f pts a game'
  % (sum(r['games'] * (r['d'] - PG_Y.at(r['x'], r['cls'])) for r in sh) / shg))
P('     their mean shortfall against the MATURE premium bar: %.3f pts a game'
  % (sum(r['games'] * (r['d'] - PG_M.at(r['x'], r['cls'])) for r in sh) / shg))
P()

# =====================================================================================================
P('-' * 118)
P('6 · THE PREREG SCORED')
P('-' * 118)
gap3000 = {c: [r for r in ROWS[c] if r['v0'] == 3000][0]['gap'] for c in ('TALL', 'SMALL')}
p1 = all(gap3000[c] <= -2.0 for c in ('TALL', 'SMALL'))
p2 = all([r for r in ROWS[c] if r['v0'] == 3000][0]['ess_m'] >
         [r for r in ROWS[c] if r['v0'] == 3000][0]['ess_y'] for c in ('TALL', 'SMALL'))
P('   S5-P1  mature premium shallower at v0=3,000 by >= 2 pts/g : TALL %+.2f  SMALL %+.2f -> %s'
  % (gap3000['TALL'], gap3000['SMALL'], 'RIGHT' if p1 else 'WRONG'))
P('   S5-P2  mature ESS at v0=3,000 exceeds young ESS           : %s' % ('RIGHT' if p2 else 'WRONG'))
P()

OUT = dict(meta=dict(seed=SEED, boot=B_BOOT, h=PB.H_PRIMARY, grid_n=PB.GRID_N,
                     mat_lo=MAT_LO, v_window=[V_LO, V_HI],
                     n_young=len(YOUNG), n_mature=len(MATURE)),
           surface={c: ROWS[c] for c in ROWS}, slopes=SLOPES,
           ci={c: {str(k): v for k, v in CI[c].items()} for c in CI},
           stage=STG, max_gap_window=maxgap_win,
           falsifiers=dict(S5_F1=bool(maxgap_win <= 1.0), S5_F2=bool(not mono_ok)),
           predictions=dict(S5_P1=bool(p1), S5_P2=bool(p2)),
           mature_grid={c: [list(map(float, PG_M.grid[c][0])), list(map(float, PG_M.grid[c][1]))]
                        for c in ('TALL', 'SMALL')},
           young_grid={c: [list(map(float, PG_Y.grid[c][0])), list(map(float, PG_Y.grid[c][1]))]
                       for c in ('TALL', 'SMALL')})
json.dump(OUT, open(os.path.join(HERE, 'MATURE_S.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'MATURE_S_out.txt'), 'w').write('\n'.join(L) + '\n')
print('written: MATURE_S.json · MATURE_S_out.txt')
