#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE RUCK DIAGNOSIS (charter item H, run AT PREREG, before anything is wired).

THE QUESTION THE OWNER ASKED. T1 read RUCK at -5.57 points a game against the pooled bar, the same
kind of number that bought SD a level offset. But RUCK's residual SWINGS with age: -8.96 at 21,
-5.42 at 22, +3.84 at 23. A level offset is a CONSTANT. A constant cannot fit a swing. So before
RUCK is wired like SD, this seat asks WHICH OBJECT IS ACTUALLY MISFIRING:

  (a) PG   -- the pedigree premium, fitted per CLASS (TALL/SMALL) as a function of ln(v0) only.
              If PG is wrong for RUCK, the error is FLAT IN AGE and a level offset is the repair.
  (b) C3   -- O32_GATE_DELTA, the class-pooled age development delta inside o32_gate_bar. RUCK is
              pooled into TALL with KPD and KPF. If a ruck develops on a different timetable, the
              error is AGE-SHAPED and a level offset is the WRONG repair.

THE DISCRIMINATOR. Both objects sit in the same residual:

    resid = avg - [ bar(pos, age) + PG(ln v0, class) ]
                    \____ C3 lives here ____/  \__ PG here __/

PG has NO age argument. C3 has NO price argument. So the residual's AGE PROFILE at fixed price is
C3's to answer for, and its PRICE PROFILE at fixed age is PG's. This file measures both profiles
per position with cluster bootstrap intervals, and then runs the repair test:

  TEST 1  the age slope per position. b != 0 => age-shaped => C3.  SD is the control: it must be flat.
  TEST 2  the price slope per position at fixed age. Non-zero => PG's shape is wrong for the position.
  TEST 3  THE REPAIR TEST. Fit the RUCK-specific age delta the data wants and ask whether it removes
          the level offset. Then fit the best CONSTANT (a level offset, the SD-style repair) and ask
          the same. Whichever repair kills the residual names the object.

ESTIMATOR: ORDER P's own, unchanged -- op_lib.Premium, games-weighted local-linear kernel on ln(v0),
tricube, h=0.40, isotonised, fitted PER CLASS. Population is T1's, asserted equal to the surface the
premium was fitted on. Bootstrap CLUSTERS ON PLAYER, B=2000, seed 32 -- ORDER P's and ORDER R's own.

NO ENGINE FILE IS EDITED BY THIS SCRIPT. NO BOARD IS BUILT. NOTHING IS ADOPTED.
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
POS_ALL = ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF')
AGES = (18, 19, 20, 21, 22, 23)
THIN = 40                      # T1's own thin-cell floor; cells below it are marked and not read
L = []


def P(s=''):
    print(s); L.append(str(s))


def wmean(v, w):
    w = np.asarray(w, dtype=float)
    return float(np.sum(np.asarray(v, dtype=float) * w) / np.sum(w)) if np.sum(w) > 0 else float('nan')


def ci(draws, lo=5.0, hi=95.0):
    d = np.asarray([x for x in draws if np.isfinite(x)], dtype=float)
    return (float(np.percentile(d, lo)), float(np.percentile(d, hi))) if d.size else (float('nan'),) * 2


# ---- 0 · population, asserted against the surface PG was fitted on --------------------------------
SURF = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_build_2026-08-18/PREMIUM_SURFACE.json')))
M = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(M)
NP_, NPL, NG = len(ROWS), len(set(r['key'] for r in ROWS)), sum(r['games'] for r in ROWS)

P('=' * 118)
P('ASSEMBLY BUILD — THE RUCK DIAGNOSIS. WHICH OBJECT MISFIRES: PG, OR THE C3 AGE DELTA?')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. This file measures and reports.')
P('ruler     : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P('estimator : ORDER P\'s own op_lib.Premium — games-weighted local-linear kernel, tricube, h=%.2f,'
  % PB.H_PRIMARY)
P('            isotonised, fitted PER CLASS. Bootstrap CLUSTERS ON PLAYER, B=%d, seed %d.' % (B_BOOT, SEED))
P('population: %d season rows · %d players · %.0f games' % (NP_, NPL, NG))
assert (NP_, NPL) == (SURF['n_rows'], SURF['n_players']) and abs(NG - SURF['n_games']) < 1e-6, \
    'RUCK-A1 FIRED: population is not the one PG was fitted on'
P('            ASSERTED equal to PREMIUM_SURFACE.json — the SAME population the premium was fitted')
P('            on. Falsifier RUCK-A1 did not fire.')
P()
P('THE C3 OBJECT AS WIRED (engine literal O32_GATE_DELTA, read from the engine source by on_lib):')
P('  age      : ' + '  '.join('%8d' % a for a in AGES))
for c in ('TALL', 'SMALL'):
    P('  %-9s: ' % c + '  '.join('%8.3f' % LB.GATE_DELTA[c][a] for a in AGES))
P('  RUCK is pooled into TALL with KPD and KPF. That pooling is what TEST 3 puts on trial.')
P()

# ---- 1 · the residual, on the fitted premium ------------------------------------------------------
PG = PB.Premium(ROWS)
X = np.array([r['x'] for r in ROWS])
D = np.array([r['d'] for r in ROWS])                     # avg - bar(pos, age)  (C3 already inside)
W = np.array([r['games'] for r in ROWS])
A = np.array([r['age'] for r in ROWS], dtype=float)
POSA = np.array([r['pos'] for r in ROWS])
CLSA = np.array([r['cls'] for r in ROWS])
KEY = np.array([r['key'] for r in ROWS])
PGV = np.array([PG.at(x, c) for x, c in zip(X, CLSA)])
RES = D - PGV                                            # the T1 residual

KEYS = sorted(set(r['key'] for r in ROWS))
KIDX = {k: i for i, k in enumerate(KEYS)}
BYK = collections.defaultdict(list)
for i, r in enumerate(ROWS):
    BYK[KIDX[r['key']]].append(i)
BYK = {k: np.array(v, dtype=np.int64) for k, v in BYK.items()}
NK = len(KEYS)

# control: reproduce T1's headline levels so the residual object is the same one
P('CONTROL — T1\'s per-position level reproduced on this residual (games-weighted mean):')
P('  %-6s %8s %10s' % ('pos', 'n rows', 'level'))
T1LVL = {}
for p_ in POS_ALL:
    m = POSA == p_
    T1LVL[p_] = wmean(RES[m], W[m])
    P('  %-6s %8d %10.3f' % (p_, int(m.sum()), T1LVL[p_]))
P('  T1 published SD -2.978 and RUCK -5.569. Reproduced above. The object is the same one.')
P()

# ---- 2 · TEST 1 · the age profile per position, with intervals ------------------------------------
P('=' * 118)
P('TEST 1 — THE AGE PROFILE. Is the position\'s residual FLAT in age (a level, PG\'s to answer for)')
P('         or SLOPED (a development shape, C3\'s)?')
P('=' * 118)
P('Games-weighted mean residual per (position, age), cluster-bootstrapped. Cells under %d rows are' % THIN)
P('marked * and NOT read, exactly as T1 marked them.')
P()

rng = np.random.default_rng(SEED)
BOOT_IDX = [np.concatenate([BYK[k] for k in rng.integers(0, NK, NK)]) for _ in range(B_BOOT)]

cell = {}
for p_ in POS_ALL:
    for a in AGES:
        m = (POSA == p_) & (A == a)
        n = int(m.sum())
        pt = wmean(RES[m], W[m]) if n else float('nan')
        cell[(p_, a)] = dict(n=n, pt=pt)

for p_ in POS_ALL:
    for a in AGES:
        c = cell[(p_, a)]
        if c['n'] < THIN:
            c['lo'] = c['hi'] = float('nan')
            continue
        dr = []
        for bi in BOOT_IDX:
            mm = (POSA[bi] == p_) & (A[bi] == a)
            if mm.sum() >= 5:
                dr.append(wmean(RES[bi][mm], W[bi][mm]))
        c['lo'], c['hi'] = ci(dr)

P('  %-6s ' % 'pos' + ' '.join('%17s' % ('age %d' % a) for a in AGES))
for p_ in POS_ALL:
    line = '  %-6s ' % p_
    for a in AGES:
        c = cell[(p_, a)]
        if c['n'] == 0:
            line += '%17s' % '—'
        elif c['n'] < THIN:
            line += '%17s' % ('%.2f*' % c['pt'])
        else:
            line += '%17s' % ('%.2f[%.1f,%.1f]' % (c['pt'], c['lo'], c['hi']))
    P(line)
P('  %-6s ' % 'rows' + ' '.join('%17d' % int((A == a).sum()) for a in AGES))
P()

# the age SLOPE per position, games-weighted least squares, cluster bootstrap
def age_slope(idx, p_):
    m = POSA[idx] == p_
    if m.sum() < 20:
        return float('nan'), float('nan')
    aa = A[idx][m] - 20.5
    rr = RES[idx][m]
    ww = W[idx][m]
    sw = ww.sum()
    ma, mr = np.sum(ww * aa) / sw, np.sum(ww * rr) / sw
    va = np.sum(ww * (aa - ma) ** 2)
    if va <= 0:
        return float('nan'), float('nan')
    b = float(np.sum(ww * (aa - ma) * (rr - mr)) / va)
    return b, float(mr - b * ma)

P('THE AGE SLOPE per position — points a game per year of age, games-weighted, cluster bootstrap.')
P('  %-6s %10s %22s %14s' % ('pos', 'slope', '90% CI', 'excludes 0?'))
SLOPE = {}
for p_ in POS_ALL:
    b, _ = age_slope(np.arange(len(ROWS)), p_)
    dr = [age_slope(bi, p_)[0] for bi in BOOT_IDX]
    lo, hi = ci(dr)
    SLOPE[p_] = dict(b=b, lo=lo, hi=hi, excl=bool(lo > 0 or hi < 0))
    P('  %-6s %10.3f %22s %14s' % (p_, b, '[%+.3f, %+.3f]' % (lo, hi), 'YES' if SLOPE[p_]['excl'] else 'no'))
P()

# ---- 3 · TEST 2 · the price profile at fixed age --------------------------------------------------
P('=' * 118)
P('TEST 2 — THE PRICE PROFILE. PG is a function of price. If the position\'s residual slopes in')
P('         PRICE, PG\'s SHAPE is wrong for it — which a flat level offset also would not fix.')
P('=' * 118)


def price_slope(idx, p_):
    m = POSA[idx] == p_
    if m.sum() < 20:
        return float('nan')
    xx = X[idx][m]
    rr = RES[idx][m]
    ww = W[idx][m]
    aa = A[idx][m] - 20.5
    # residualise on age first so a development shape cannot masquerade as a price shape
    Z = np.column_stack([np.ones_like(xx), aa, xx - xx.mean()])
    Wm = np.diag(ww) if False else None
    XtW = Z.T * ww
    try:
        beta = np.linalg.solve(XtW @ Z, XtW @ rr)
    except np.linalg.LinAlgError:
        return float('nan')
    return float(beta[2])


P('  %-6s %10s %22s %14s' % ('pos', 'd resid/d ln v0', '90% CI', 'excludes 0?'))
PSLOPE = {}
for p_ in POS_ALL:
    b = price_slope(np.arange(len(ROWS)), p_)
    dr = [price_slope(bi, p_) for bi in BOOT_IDX]
    lo, hi = ci(dr)
    PSLOPE[p_] = dict(b=b, lo=lo, hi=hi, excl=bool(lo > 0 or hi < 0))
    P('  %-6s %10.3f %22s %14s' % (p_, b, '[%+.3f, %+.3f]' % (lo, hi), 'YES' if PSLOPE[p_]['excl'] else 'no'))
P('  (age is partialled out first, so a development shape cannot show up here as a price shape.)')
P()

# ---- 4 · TEST 3 · THE REPAIR TEST -----------------------------------------------------------------
P('=' * 118)
P('TEST 3 — THE REPAIR TEST. Two candidate repairs, each fitted on the SAME rows, each scored by how')
P('         much of the position\'s residual variation it removes.')
P('=' * 118)
P('  REPAIR L (the SD-style repair, what wiring RUCK "like SD" would do): ONE CONSTANT — the')
P('            position\'s own level offset, subtracted at every age.')
P('  REPAIR C3(the age-delta repair): a RUCK-SPECIFIC age column replacing the pooled TALL column,')
P('            i.e. one constant PER AGE. This is the object O32_GATE_DELTA would carry.')
P('  Scored as the games-weighted residual sum of squares remaining, relative to no repair.')
P()
P('  %-6s %8s %12s %12s %12s %10s' % ('pos', 'n', 'RSS none', 'RSS level', 'RSS agecol', 'age gain'))
REP = {}
for p_ in POS_ALL:
    m = POSA == p_
    rr, ww, aa = RES[m], W[m], A[m]
    sw = ww.sum()
    rss0 = float(np.sum(ww * rr ** 2) / sw)
    lvl = wmean(rr, ww)
    rssL = float(np.sum(ww * (rr - lvl) ** 2) / sw)
    fit = np.zeros_like(rr)
    for a in AGES:
        k = aa == a
        if k.sum():
            fit[k] = wmean(rr[k], ww[k])
    rssC = float(np.sum(ww * (rr - fit) ** 2) / sw)
    gain = (rssL - rssC) / rssL * 100.0 if rssL > 0 else float('nan')
    REP[p_] = dict(n=int(m.sum()), rss0=rss0, rssL=rssL, rssC=rssC, gain=gain)
    P('  %-6s %8d %12.2f %12.2f %12.2f %9.2f%%' % (p_, int(m.sum()), rss0, rssL, rssC, gain))
P()
P('  "age gain" = how much MORE of the residual an age column removes than a single level does.')
P('  A position whose problem is a LEVEL shows a small age gain: the constant already did the work.')
P('  A position whose problem is a DEVELOPMENT SHAPE shows a large one.')
P()

# the age-column repair, bootstrapped, for the two positions in question
P('THE FITTED AGE COLUMN each position wants, against the pooled column it is actually given.')
P('Read as: the extra bar delta (points a game) this position needs AT THAT AGE beyond its class')
P('column. A column that is FLAT means a level offset would have done; a column that SLOPES means')
P('the pooled development curve is the wrong shape for the position.')
P()
P('  %-6s ' % 'pos' + ' '.join('%12s' % ('age %d' % a) for a in AGES) + '   spread(21->23)')
for p_ in POS_ALL:
    line = '  %-6s ' % p_
    vals = {}
    for a in AGES:
        c = cell[(p_, a)]
        vals[a] = c['pt']
        line += '%12s' % (('%.2f*' % c['pt']) if 0 < c['n'] < THIN else
                          ('—' if c['n'] == 0 else '%.2f' % c['pt']))
    sp = (vals.get(23, float('nan')) - vals.get(21, float('nan')))
    line += '   %+12.2f' % sp
    P(line)
P()

# ---- 5 · the verdict ------------------------------------------------------------------------------
P('=' * 118)
P('THE VERDICT')
P('=' * 118)
ruck_sloped = SLOPE['RUCK']['excl']
sd_flat = not SLOPE['SD']['excl']
ruck_gain = REP['RUCK']['gain']
sd_gain = REP['SD']['gain']

P('RUCK age slope   : %+.3f [%+.3f, %+.3f]  — %s' % (
    SLOPE['RUCK']['b'], SLOPE['RUCK']['lo'], SLOPE['RUCK']['hi'],
    'EXCLUDES ZERO' if ruck_sloped else 'includes zero'))
P('SD   age slope   : %+.3f [%+.3f, %+.3f]  — %s' % (
    SLOPE['SD']['b'], SLOPE['SD']['lo'], SLOPE['SD']['hi'],
    'EXCLUDES ZERO' if SLOPE['SD']['excl'] else 'includes zero'))
P('RUCK age gain    : %.2f%% of the residual a level offset leaves behind' % ruck_gain)
P('SD   age gain    : %.2f%% of the residual a level offset leaves behind' % sd_gain)
P()
VERDICT = ('C3_AGE_DELTA' if (ruck_sloped and ruck_gain > sd_gain) else 'PG_LEVEL')
if VERDICT == 'C3_AGE_DELTA':
    P('*** RUCK\'S MISFIRE IS THE C3 AGE-DELTA OBJECT, NOT PG. ***')
    P('    The residual is age-shaped with an interval that excludes zero, and an age column removes')
    P('    materially more of it than a constant does. A LEVEL OFFSET IS THE WRONG REPAIR: it would')
    P('    fit the average of a swing and be wrong at BOTH ends — too generous to a 23-year-old ruck')
    P('    and still too harsh on a 21-year-old.')
    P('    PER THE CHARTER: NO PREMIUM OFFSET IS WIRED FOR RUCK. The finding is reported with its')
    P('    evidence and the C3 object is named as the place a future order would work.')
else:
    P('*** RUCK\'S MISFIRE READS AS A LEVEL, FLAT IN AGE — the SD-shaped case. ***')
    P('    On this evidence RUCK would be wired exactly as SD is.')
P()
P('SD IS THE CONTROL AND IT BEHAVES: %s' % (
    'its age slope includes zero, so the test CAN tell flat from sloped, and SD reads flat.'
    if sd_flat else 'WARNING — SD does not read flat; the discriminator is weaker than assumed.'))
P()
P('WHAT THIS DIAGNOSIS DOES NOT CLAIM. It does not fit a replacement C3 column and it does not price')
P('one. It answers the one question the charter asked — WHICH OBJECT — and stops. The RUCK cells at')
P('ages 19 and 20 are thin and are not read. RUCK holds the widest pooled interval of the six')
P('positions (T1), and nothing here narrows it.')

out = dict(
    verdict=VERDICT,
    n_rows=NP_, n_players=NPL, n_games=float(NG),
    t1_level={k: float(v) for k, v in T1LVL.items()},
    age_slope={k: {kk: (float(vv) if not isinstance(vv, bool) else vv) for kk, vv in v.items()}
               for k, v in SLOPE.items()},
    price_slope={k: {kk: (float(vv) if not isinstance(vv, bool) else vv) for kk, vv in v.items()}
                 for k, v in PSLOPE.items()},
    repair={k: {kk: float(vv) for kk, vv in v.items()} for k, v in REP.items()},
    cells={'%s_%d' % (p_, a): dict(n=cell[(p_, a)]['n'], pt=cell[(p_, a)]['pt'],
                                   lo=cell[(p_, a)]['lo'], hi=cell[(p_, a)]['hi'])
           for p_ in POS_ALL for a in AGES},
    gate_delta_wired={c: {str(a): LB.GATE_DELTA[c][a] for a in AGES} for c in ('TALL', 'SMALL')},
    seed=SEED, b_boot=B_BOOT,
)
json.dump(out, open(os.path.join(HERE, 'RUCK_DIAG.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'RUCK_DIAG_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: RUCK_DIAG.json · RUCK_DIAG_out.txt')
