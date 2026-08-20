#!/usr/bin/env python3
"""ORDER S READ-ONLY — T1. THE PG *LEVEL* BY POSITION. NO BOARD IS BUILT. NOTHING IS ADOPTED.

ORDER R measured the SLOPE dPG/dln(v0) per position and found no pair separable. It never measured
the LEVEL. This is the level companion, preregistered in PREREG_SRO.md section 1.

THE OBJECT, per season row:

    resid = season avg  -  [ o32_gate_bar(pos, age)  +  PG_pooled(ln v0, class) ]

reported as the GAMES-WEIGHTED MEAN of resid PER POSITION. Positive = under-barred (the position
produces above the pooled bar). Negative = over-barred.

ESTIMATOR: ORDER P's own. Games-weighted local-linear kernel regression on ln(v0), tricube,
bandwidth 0.40 in log-v0 units, isotonised by pool-adjacent-violators, fitted PER CLASS. Nothing
about the estimator changes. Seed 32, B = 2000, ORDER P's and ORDER R's own.

THE PREMIUM IS REFITTED INSIDE EVERY BOOTSTRAP DRAW (prereg 1.2): PG is an estimated object and a
CI that held it fixed would understate the spread.

  usage: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
         VECLIB_MAXIMUM_THREADS=1 python3 os_level.py
"""
import json, math, os, sys, collections, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
POS_ALL = ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF')
CLS_OF = {p: ('TALL' if p in LB.TALLPOS else 'SMALL') for p in POS_ALL}
LAMBDA = 0.1743833036575403
BSAT = 0.11464630061141393
SURF = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_build_2026-08-18/PREMIUM_SURFACE.json')))
L = []


def P(s=''):
    print(s); L.append(str(s))


# ---- 0 · the population, asserted rather than assumed --------------------------------------------------
M = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(M)
NP_, NPL, NG = len(ROWS), len(set(r['key'] for r in ROWS)), sum(r['games'] for r in ROWS)
P('=' * 118)
P('ORDER S READ-ONLY — T1. THE PG *LEVEL* BY POSITION. THE COMPANION TO ORDER R\'s SLOPE TEST.')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. This file measures and reports.')
P('ruler     : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P('estimator : ORDER P\'s own op_lib.Premium — games-weighted local-linear kernel, tricube, h=%.2f in'
  % PB.H_PRIMARY)
P('            log-v0 units, isotonised, fitted PER CLASS. Refitted inside every bootstrap draw.')
P('population: %d season rows · %d players · %.0f games' % (NP_, NPL, NG))
assert (NP_, NPL) == (SURF['n_rows'], SURF['n_players']) and abs(NG - SURF['n_games']) < 1e-6, \
    'SRO-P1 FIRED: the population is not the one PG was fitted on (%d/%d/%.0f vs %d/%d/%.0f)' \
    % (NP_, NPL, NG, SURF['n_rows'], SURF['n_players'], SURF['n_games'])
P('            ASSERTED equal to PREMIUM_SURFACE.json::n_rows/n_players/n_games — the SAME population')
P('            the premium was fitted on. Falsifier SRO-P1 did not fire.')
P()

# ---- 1 · arrays, and the replicated fit asserted against op_lib.Premium bit for bit --------------------
X = np.array([r['x'] for r in ROWS])
Ydiff = np.array([r['d'] for r in ROWS])
W = np.array([r['games'] for r in ROWS])
V0 = np.array([r['v0'] for r in ROWS])
POSA = np.array([r['pos'] for r in ROWS])
CLSA = np.array([r['cls'] for r in ROWS])
KEYS = sorted(set(r['key'] for r in ROWS))
KIDX = {k: i for i, k in enumerate(KEYS)}
BYK = collections.defaultdict(list)
for i, r in enumerate(ROWS):
    BYK[KIDX[r['key']]].append(i)
BYK = {k: np.array(v, dtype=np.int64) for k, v in BYK.items()}
CMASK = {c: (CLSA == c) for c in ('TALL', 'SMALL')}
# the FIXED support grid, taken once from the full sample, so every draw's fit is evaluated on the
# same abscissa and the draws are comparable to each other and to the published surface.
GRID = {}
for c in ('TALL', 'SMALL'):
    xs = X[CMASK[c]]
    lo, hi = float(np.percentile(xs, 1)), float(np.percentile(xs, 99))
    GRID[c] = (lo, hi, np.linspace(lo, hi, PB.GRID_N))


def fit_class(xs, ys, ws, c, h=PB.H_PRIMARY):
    """op_lib.Premium's construction for ONE class, on a FIXED grid. Same loclin, same isotoniser."""
    gx = GRID[c][2]
    fit = np.array([PB.loclin(x0, xs, ys, ws, h)[0] for x0 in gx])
    if np.isnan(fit).any():
        fit = np.where(np.isnan(fit), np.nanmean(fit[~np.isnan(fit)]), fit)
    return PB.isotonize_up(fit)


PG_FULL = {c: fit_class(X[CMASK[c]], Ydiff[CMASK[c]], W[CMASK[c]], c) for c in ('TALL', 'SMALL')}
# FALSIFIER SRO-P2: the replicated fit must be op_lib.Premium's own, node for node.
PGOBJ = PB.Premium(ROWS)
for c in ('TALL', 'SMALL'):
    gxo, gyo = PGOBJ.grid[c]
    d = float(np.max(np.abs(gyo - PG_FULL[c])))
    dx = float(np.max(np.abs(gxo - GRID[c][2])))
    assert d < 1e-12 and dx < 1e-12, 'SRO-P2 FIRED: replicated fit differs from op_lib.Premium (%s: %g/%g)' % (c, d, dx)
    dpub = float(np.max(np.abs(np.array(SURF[c]['y']) - PG_FULL[c])))
    assert dpub < 1e-9, 'SRO-P2 FIRED: fit differs from the BUILT surface (%s: %g)' % (c, dpub)
P('1 · THE FIT IS THE ENGINE\'S OWN. Falsifier SRO-P2 did not fire: the replicated per-class surface')
P('    reproduces op_lib.Premium node for node (max |diff| < 1e-12) AND the BUILT engine surface in')
P('    PREMIUM_SURFACE.json (max |diff| < 1e-9). Nothing new is fitted in this file.')
P()


def pg_of(idx, pgs):
    """PG at each row's own ln(v0), per class, HELD FLAT outside support — Premium.at's own rule."""
    out = np.empty(len(idx))
    for c in ('TALL', 'SMALL'):
        m = CLSA[idx] == c
        if not m.any():
            continue
        lo, hi, gx = GRID[c]
        out[m] = np.interp(np.clip(X[idx][m], lo, hi), gx, pgs[c])
    return out


ALLIDX = np.arange(len(ROWS))
RESID_FULL = Ydiff - pg_of(ALLIDX, PG_FULL)

# ---- 2 · the price cuts, fixed in advance --------------------------------------------------------------
CUT = {}
for c in ('TALL', 'SMALL'):
    v = V0[CMASK[c]]
    CUT[c] = (float(np.median(v)), float(np.percentile(v, 90)))
CELLS = ('ALL', 'BELOW', 'ABOVE', 'TAIL')


def cell_mask(idx):
    med = np.array([CUT[c][0] for c in CLSA[idx]])
    p90 = np.array([CUT[c][1] for c in CLSA[idx]])
    v = V0[idx]
    return {'ALL': np.ones(len(idx), bool), 'BELOW': v <= med, 'ABOVE': v > med, 'TAIL': v > p90}


def wmean(vals, ws):
    s = ws.sum()
    return float((vals * ws).sum() / s) if s > 0 else float('nan')


def stat(idx, pgs):
    """Games-weighted mean residual for every (group, cell). Groups: the six positions + both classes."""
    res = Ydiff[idx] - pg_of(idx, pgs)
    cm = cell_mask(idx)
    out = {}
    for g in POS_ALL:
        gm = POSA[idx] == g
        for cl in CELLS:
            m = gm & cm[cl]
            out[(g, cl)] = wmean(res[m], W[idx][m]) if m.any() else float('nan')
    for c in ('TALL', 'SMALL'):
        gm = CLSA[idx] == c
        for cl in CELLS:
            m = gm & cm[cl]
            out[(c, cl)] = wmean(res[m], W[idx][m]) if m.any() else float('nan')
    return out


PT = stat(ALLIDX, PG_FULL)

# ---- 3 · the sample, per position and per cell ---------------------------------------------------------
P('-' * 118)
P('2 · THE SAMPLE, PER POSITION AND PER PRICE CELL')
P('-' * 118)
P('   price cuts are the row\'s OWN CLASS percentiles of v0, fixed before any residual was computed:')
for c in ('TALL', 'SMALL'):
    P('     %-6s median v0 %7.0f   p90 v0 %7.0f' % (c, CUT[c][0], CUT[c][1]))
P()
P('   %-6s %6s %8s %9s | %8s %8s %8s %8s | %9s' %
  ('group', 'rows', 'players', 'games', 'ALL n', 'BELOW n', 'ABOVE n', 'TAIL n', 'med v0'))
POPJ = {}
for g in POS_ALL + ('TALL', 'SMALL'):
    gm = (POSA == g) if g in POS_ALL else (CLSA == g)
    cm = cell_mask(ALLIDX)
    ns = [int((gm & cm[cl]).sum()) for cl in CELLS]
    gg = [float(W[gm & cm[cl]].sum()) for cl in CELLS]
    POPJ[g] = dict(rows=int(gm.sum()), players=len(set(np.array([r['key'] for r in ROWS])[gm])),
                   games=float(W[gm].sum()), n=ns, g=gg, medv0=float(np.median(V0[gm])))
    P('   %-6s %6d %8d %9.0f | %8d %8d %8d %8d | %9.0f'
      % (g, POPJ[g]['rows'], POPJ[g]['players'], POPJ[g]['games'], ns[0], ns[1], ns[2], ns[3],
         POPJ[g]['medv0']))
P()
P('   THIN-CELL RULE, stated before the numbers: a cell with fewer than 30 games-weighted effective')
P('   rows, or fewer than 40 players, is printed THIN and is not read as a result.')
P()
P('   THE ESTIMATOR\'S OWN EFFECTIVE SAMPLE at the two cut prices, read straight off the BUILT')
P('   surface\'s per-node ESS (PREMIUM_SURFACE.json). ORDER P\'s ESS_THIN is %.0f.' % PB.ESS_THIN)
ESSJ = {}
for c in ('TALL', 'SMALL'):
    lo, hi = SURF[c]['lo'], SURF[c]['hi']
    ess = np.array(SURF[c]['ess'])
    gx = np.linspace(lo, hi, len(ess))
    e_med = float(np.interp(np.clip(math.log(CUT[c][0]), lo, hi), gx, ess))
    e_p90 = float(np.interp(np.clip(math.log(CUT[c][1]), lo, hi), gx, ess))
    ESSJ[c] = dict(median=e_med, p90=e_p90, min=float(ess.min()), max=float(ess.max()))
    P('     %-6s ESS at the class median v0 %7.1f · at the class p90 %7.1f · min over the grid %6.1f'
      % (c, e_med, e_p90, ess.min()))
P()

# ---- 4 · the bootstrap ---------------------------------------------------------------------------------
P('-' * 118)
P('3 · PLAYER-LEVEL CLUSTER BOOTSTRAP — %d DRAWS, SEED %d, THE PREMIUM REFITTED IN EVERY DRAW' % (B_BOOT, SEED))
P('-' * 118)
P('   Players are the cluster: one player contributes up to six correlated season rows. Each draw')
P('   resamples PLAYERS with replacement, REFITS both class surfaces on the resampled rows over the')
P('   SAME support grid, and recomputes every games-weighted mean residual. So the interval carries')
P('   both the sampling noise in the residual AND the estimation noise in the premium itself.')
P()
rng = np.random.default_rng(SEED)
t0 = time.time()
BS = collections.defaultdict(list)
NK = len(KEYS)
for b in range(B_BOOT):
    pick = rng.integers(0, NK, size=NK)
    idx = np.concatenate([BYK[int(i)] for i in pick])
    pgs = {}
    ok = True
    for c in ('TALL', 'SMALL'):
        m = CLSA[idx] == c
        if m.sum() < 50:
            ok = False
            break
        pgs[c] = fit_class(X[idx][m], Ydiff[idx][m], W[idx][m], c)
    if not ok:
        continue
    s = stat(idx, pgs)
    for k, v in s.items():
        BS[k].append(v)
P('   %d draws completed in %.1fs.' % (len(BS[('MID', 'ALL')]), time.time() - t0))
P()

CI = {}
for k, v in BS.items():
    a = np.array([z for z in v if not math.isnan(z)])
    CI[k] = (float(np.percentile(a, 5)), float(np.percentile(a, 95)), len(a)) if len(a) > 10 else (float('nan'),) * 2 + (len(a),)

# ---- 5 · the control ------------------------------------------------------------------------------------
P('-' * 118)
P('4 · THE STRUCTURAL CONTROL (prereg SRO-1) — THE CLASS-LEVEL MEAN RESIDUAL MUST BE ~ZERO')
P('-' * 118)
P('   The pooled surface is fitted on exactly these rows, so the games-weighted mean residual over a')
P('   whole class has to sit on zero. If it does not, this seat has misread the estimator and says so.')
P()
P('   %-8s %14s %-26s %-12s' % ('class', 'mean resid', '90% CI', 'verdict'))
CTRL = {}
for c in ('TALL', 'SMALL'):
    m, (lo, hi, nb) = PT[(c, 'ALL')], CI[(c, 'ALL')]
    v = 'PASS — |mean| < 0.5' if abs(m) < 0.5 else 'SRO-1 FIRED'
    CTRL[c] = v
    P('   %-8s %+14.4f [%+10.4f,%+10.4f] %-12s' % (c, m, lo, hi, v))
P()
P('   SRO-1b, the zero-sum note, stated in the prereg: because the class mean is pinned at zero, a')
P('   position-level offset inside a class is a REDISTRIBUTION between that class\'s three positions.')
P('   If one is over-barred another must be under-barred. "Everyone is over-barred" is not a result')
P('   this estimator can produce, and nobody should read it out of the table below.')
P()

# ---- 6 · the headline -----------------------------------------------------------------------------------
P('-' * 118)
P('5 · THE LEVEL, PER POSITION — GAMES-WEIGHTED MEAN RESIDUAL AGAINST THE POOLED BAR')
P('-' * 118)
P('   POSITIVE = the position produces ABOVE the pooled bar = UNDER-barred = charged too little.')
P('   NEGATIVE = the position produces BELOW the pooled bar = OVER-barred = charged too much.')
P('   Every number is in AFL Fantasy points a game. Intervals are the bootstrap of section 3.')
P()
for cl in CELLS:
    lab = {'ALL': 'POOLED OVER PRICE', 'BELOW': 'BELOW the class median v0',
           'ABOVE': 'ABOVE the class median v0', 'TAIL': 'THE EXPENSIVE TAIL (v0 > class p90)'}[cl]
    P('   -- %s' % lab)
    P('   %-6s %6s %9s %13s %-26s %10s %-10s' %
      ('pos', 'rows', 'games', 'mean resid', '90% CI', 'CI width', 'excl 0?'))
    for g in POS_ALL:
        n = POPJ[g]['n'][CELLS.index(cl)]
        gg = POPJ[g]['g'][CELLS.index(cl)]
        m = PT[(g, cl)]
        lo, hi, nb = CI[(g, cl)]
        if n == 0 or math.isnan(m):
            P('   %-6s %6d %9s %13s %-26s %10s %-10s' % (g, n, '-', 'no rows', '', '', ''))
            continue
        thin = ' THIN' if (n < 40 or POPJ[g]['players'] < 40) else ''
        exc = ('YES %s' % ('+' if lo > 0 else '-')) if (lo > 0 or hi < 0) else 'no'
        P('   %-6s %6d %9.0f %+13.3f [%+10.3f,%+10.3f] %10.3f %-10s%s'
          % (g, n, gg, m, lo, hi, hi - lo, exc, thin))
    P()

# ---- 6b · where the offset comes from: the age bar alone, and the age profile --------------------------
P('-' * 118)
P('5b · WHERE THE OFFSET COMES FROM — THE AGE BAR ALONE, AND WHETHER IT IS FLAT IN AGE')
P('-' * 118)
P('   Column 1 is the games-weighted mean of (avg - o32_gate_bar(pos, age)) with NO premium at all —')
P('   ORDER N\'s own surplus. Column 2 is the same after the pooled premium is subtracted. The')
P('   DIFFERENCE between them is exactly the games-weighted mean premium the position\'s own price')
P('   distribution earns it. This separates "the position\'s own bar is wrong" from "the pooled')
P('   premium puts this position in the wrong place".')
P()
P('   %-6s %14s %14s %14s' % ('pos', 'vs AGE bar', 'mean PG earned', 'vs POOLED bar'))
AGEONLY = {}
for g in POS_ALL:
    gm = POSA == g
    a = wmean(Ydiff[gm], W[gm])
    b = wmean(pg_of(ALLIDX, PG_FULL)[gm], W[gm])
    AGEONLY[g] = dict(vs_age=a, pg=b, vs_pooled=a - b)
    P('   %-6s %+14.3f %+14.3f %+14.3f' % (g, a, b, a - b))
P()
P('   THE AGE PROFILE. If the offset is flat in age it is a LEVEL problem — the position\'s flat bar')
P('   or the pooled premium. If it grows with age it is the CLASS-POOLED age development delta, which')
P('   is a different object (the S1 C3 surface) and not PG\'s to answer for. Point estimates only;')
P('   cells under 40 rows are printed THIN and are not read.')
P()
P('   %-6s %s' % ('pos', ' '.join('%14s' % ('age %d' % a) for a in range(18, 24))))
AGEPROF = {}
AGEN = {}
for g in POS_ALL:
    cells = []
    AGEPROF[g] = {}
    AGEN[g] = {}
    for a in range(18, 24):
        m = (POSA == g) & np.array([r['age'] == a for r in ROWS])
        n = int(m.sum())
        AGEN[g][a] = n
        if n == 0:
            cells.append('%14s' % '-'); AGEPROF[g][a] = None; continue
        v = wmean(Ydiff[m] - pg_of(ALLIDX, PG_FULL)[m], W[m])
        AGEPROF[g][a] = v
        cells.append('%14s' % ('%+.2f%s' % (v, '*' if n < 40 else '')))
    P('   %-6s %s' % (g, ' '.join(cells)))
P('   %-6s %s' % ('n', ' '.join('%14d' % sum(AGEN[g][a] for g in POS_ALL) for a in range(18, 24))))
P('   (* = fewer than 40 rows in that position-age cell — THIN, not read.)')
P()

# ---- 7 · pairwise inside each class ---------------------------------------------------------------------
P('-' * 118)
P('6 · PAIRWISE, INSIDE EACH CLASS — IS ONE POSITION SEPARABLE FROM ANOTHER ON LEVEL?')
P('-' * 118)
P('   The difference is bootstrapped as a DIFFERENCE inside each draw, which is the right object:')
P('   the two positions share the same fitted surface in a draw, so their errors are correlated and')
P('   differencing the two CIs separately would overstate the spread.')
P()
PAIRS = [('MID', 'SD'), ('MID', 'SF'), ('SD', 'SF'), ('KPD', 'KPF'), ('KPD', 'RUCK'), ('KPF', 'RUCK')]
PAIRJ = {}
for cl in CELLS:
    P('   -- %s' % cl)
    P('   %-14s %11s %11s %11s %-26s %-14s' % ('pair', 'A', 'B', 'A-B', '90% CI of A-B', 'separable?'))
    for a, b in PAIRS:
        da = np.array(BS[(a, cl)]); db = np.array(BS[(b, cl)])
        n = min(len(da), len(db))
        if n < 10:
            P('   %-14s %11s' % ('%s vs %s' % (a, b), 'thin')); continue
        d = da[:n] - db[:n]
        d = d[~np.isnan(d)]
        lo, hi = float(np.percentile(d, 5)), float(np.percentile(d, 95))
        sep = 'SEPARABLE' if (lo > 0 or hi < 0) else 'no — CI covers 0'
        PAIRJ['%s|%s|%s' % (a, b, cl)] = (float(PT[(a, cl)] - PT[(b, cl)]), lo, hi, sep)
        P('   %-14s %+11.3f %+11.3f %+11.3f [%+10.3f,%+10.3f] %-14s'
          % ('%s vs %s' % (a, b), PT[(a, cl)], PT[(b, cl)], PT[(a, cl)] - PT[(b, cl)], lo, hi, sep))
    P()

# ---- 8 · translation into price -------------------------------------------------------------------------
P('-' * 118)
P('7 · WHAT A LEVEL OFFSET IS WORTH — THE TRANSLATION WRITTEN DOWN IN THE PREREG')
P('-' * 118)
P('   In the unclipped region  d ln(retained pedigree)/ds = LAMBDA*A(g)*THETA_R = BETA_sat*A(g).')
P('   So a level offset of x points a game moves the RETAINED pedigree leg by exp(BETA_sat*A(g)*x)-1.')
G0 = 9.890000000000008
P('   BETA_sat = %.6f. A(g) = 1 - exp(-g/%.3f).' % (BSAT, G0))
P()
P('   %-8s %8s | %s' % ('games g', 'A(g)', 'change in the RETAINED pedigree leg, per level offset'))
P('   %-8s %8s | %10s %10s %10s %10s %10s' % ('', '', '-3.0 ppg', '-2.0 ppg', '-1.0 ppg', '+1.0 ppg', '+2.0 ppg'))
TRJ = {}
for g in (2, 5, 10, 17, 25, 40, 60):
    A = 1.0 - math.exp(-g / 9.890000000000008)
    row = [math.exp(BSAT * A * x) - 1.0 for x in (-3.0, -2.0, -1.0, 1.0, 2.0)]
    TRJ[g] = dict(A=A, chg=row)
    P('   %-8d %8.4f | %+9.2f%% %+9.2f%% %+9.2f%% %+9.2f%% %+9.2f%%'
      % (g, A, *[100 * z for z in row]))
P()
P('   Read it as: a position over-barred by 2 points a game has its retained pedigree leg cut by')
P('   %.1f%% at 17 games and by %.1f%% at 2 games, for no reason connected to how he played.'
  % (-100 * (math.exp(BSAT * (1 - math.exp(-17 / 9.89)) * -2.0) - 1),
     -100 * (math.exp(BSAT * (1 - math.exp(-2 / 9.89)) * -2.0) - 1)))
P()

# ---- 9 · the owner's arithmetic, checked ----------------------------------------------------------------
P('-' * 118)
P('8 · THE OWNER\'S SENTENCE, CHECKED ARITHMETICALLY — "priced 18% below, barred only 2-7% lower"')
P('-' * 118)
P('   This is NOT the residual test. It is the separate question of how much the bar moves when the')
P('   price moves, and it is printed because the residual table only answers half of what was asked.')
P()
P('   The bar has two position-carrying parts: the position\'s OWN o32_gate_bar, and PG at the')
P('   position\'s OWN entry price. A cheaper position gets a lower bar through BOTH.')
P()
PLF = float(json.load(open(os.path.join(REPO, 'engine/rl_after/pick_redenomination.json')))['factor'])
POSV = {g: {int(k): float(v) for k, v in d.items()}
        for g, d in json.load(open(os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')))['nd_v0']['posv'].items()}


def bar_at(pos, pick, age):
    """The FULL bar the charge reads for a row of this position taken at this pick, at this age:
    the position's own o32_gate_bar plus the pooled premium at that position's own entry price."""
    v0 = POSV[pos][pick] * PLF
    c = CLS_OF[pos]
    lo, hi, gx = GRID[c]
    return LB.bar(pos, age) + float(np.interp(np.clip(math.log(v0), lo, hi), gx, PG_FULL[c])), v0


P('   THE SAME-PICK COMPARISON, on the engine\'s own positional day-0 curve (pvc_curve_v2.json::')
P('   nd_v0.posv) in engine currency (x %.4f), at age 19.' % PLF)
P()
P('   %-6s | %s' % ('pick', '   '.join('%-16s' % g for g in POS_ALL)))
P('   %-6s | %s' % ('', '   '.join('%8s %7s' % ('v0', 'bar19') for g in POS_ALL)))
SAMEPICK = {}
for pk in (1, 3, 5, 10, 15, 20, 30, 40, 50, 60):
    cells = []
    for g in POS_ALL:
        b, v0 = bar_at(g, pk, 19)
        cells.append('%8.0f %7.2f' % (v0, b))
        SAMEPICK.setdefault(str(pk), {})[g] = dict(v0=v0, bar19=b)
    P('   %-6d | %s' % (pk, '   '.join(cells)))
P()
P('   THE OWNER\'S TWO NUMBERS, READ OFF THAT TABLE. For each pick: how far BELOW MID is each')
P('   position PRICED, and how far below MID is it BARRED?')
P()
P('   %-6s | %s' % ('pick', '  '.join('%-17s' % g for g in POS_ALL if g != 'MID')))
P('   %-6s | %s' % ('', '  '.join('%8s %8s' % ('price', 'bar') for g in POS_ALL if g != 'MID')))
GAPJ = {}
for pk in (1, 3, 5, 10, 15, 20, 30, 40, 50, 60):
    bm, vm = bar_at('MID', pk, 19)
    cells = []
    for g in POS_ALL:
        if g == 'MID':
            continue
        b, v0 = bar_at(g, pk, 19)
        cells.append('%7.1f%% %7.1f%%' % (100 * (v0 / vm - 1), 100 * (b / bm - 1)))
        GAPJ.setdefault(str(pk), {})[g] = dict(price=100 * (v0 / vm - 1), bar=100 * (b / bm - 1))
    P('   %-6d | %s' % (pk, '  '.join(cells)))
P()
P('   The step in the premium\'s own axis: an 18%% lower entry price is ln(0.82) = %.4f log-units.'
  % math.log(0.82))
P('   At the SMALL average slope ORDER R measured (%.4f points a game per log-unit) that is %.2f'
  % (8.9432, 8.9432 * math.log(0.82)))
P('   points a game of BAR — before the position\'s own gate bar moves at all.')
P()

json.dump(dict(pop={g: POPJ[g] for g in POPJ}, cuts={c: list(CUT[c]) for c in CUT},
               point={'%s|%s' % k: (None if math.isnan(v) else v) for k, v in PT.items()},
               ci={'%s|%s' % k: list(v) for k, v in CI.items()},
               ess=ESSJ, ageonly=AGEONLY, ageprof=AGEPROF, agen=AGEN, pairs=PAIRJ, control=CTRL, translate={str(k): v for k, v in TRJ.items()},
               samepick=SAMEPICK, gap_vs_mid=GAPJ,
               seed=SEED, boot=B_BOOT, n_rows=NP_, n_players=NPL, n_games=NG),
          open(os.path.join(HERE, 'LEVEL_SRO.json'), 'w'), indent=1)
open(os.path.join(HERE, 'LEVEL_SRO_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote LEVEL_SRO.json and LEVEL_SRO_out.txt')
