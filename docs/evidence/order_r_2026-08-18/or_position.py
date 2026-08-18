#!/usr/bin/env python3
"""ORDER R — THE READ-ONLY POSITION TEST. NO BOARD IS BUILT. NOTHING IS ADOPTED.

The question the owner asked: PG, the pedigree premium, is pooled into TALL (KPD/KPF/RUCK) and
SMALL (MID/SD/SF). Is that pooling defensible, given that SD/SF and MID price and perform very
differently?

WHAT IS ALREADY SEPARATE, AND MUST BE SAID FIRST. The position-specific S1 AGE BAR already separates
the positions. PG is only the pedigree INCREMENT above each position's OWN bar. So the question is
not "do MIDs and SFs differ" -- they plainly do, and the bar carries it -- but "does the INCREMENT
above each position's own bar differ".

ESTIMATOR: ORDER P's own. op_lib.Premium -- games-weighted local-linear kernel regression on ln(v0),
tricube, bandwidth 0.40 in log-v0 units, isotonised by pool-adjacent-violators. Refitted per POSITION
instead of per CLASS. Nothing about the estimator changes. Seed 32, ORDER P's own.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 or_position.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
LAMBDA = 0.1743833036575403
BSAT_P = 0.11464630061141393
BSAT_CI = (0.10416359711151935, 0.1271777523096214)
POS_ALL = ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF')
CLS_OF = {p: ('TALL' if p in LB.TALLPOS else 'SMALL') for p in POS_ALL}
L = []


def P(s=''):
    print(s); L.append(str(s))


M = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(M)
P('=' * 118)
P('ORDER R — THE READ-ONLY POSITION TEST. IS THE TALL/SMALL POOLING OF PG DEFENSIBLE?')
P('=' * 118)
P('NO BOARD IS BUILT. NOTHING IS ADOPTED. This file measures and reports; it does not rule.')
P('ruler  : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P('estimator : ORDER P\'s own op_lib.Premium — games-weighted local-linear kernel, tricube, h=0.40 in')
P('            log-v0 units, isotonised. Refitted PER POSITION instead of per CLASS. Seed %d.' % SEED)
P('population: %d season rows, games>0, age 18-23, entrant from %d on, up to %d.'
  % (len(ROWS), LB.ENTRY_FLOOR, LB.LAST_REAL_SEASON))
P()
P('WHAT IS ALREADY SEPARATE. The S1 AGE BAR is position-specific and carries the level difference.')
P('   %-6s %10s' % ('pos', 'bar(21)'))
for p in POS_ALL:
    P('   %-6s %10.2f' % (p, LB.bar(p, 21)))
P('   PG is the pedigree INCREMENT ABOVE each position\'s own bar. It is the only pooled object.')
P()

# ---- 1 · the population, per position -----------------------------------------------------------------
P('-' * 118)
P('1 · THE SAMPLE, PER POSITION — AND WHERE IT RUNS OUT')
P('-' * 118)
by = collections.defaultdict(list)
for r in ROWS:
    by[r['pos']].append(r)
allv = np.array([r['v0'] for r in ROWS])
QCUT = [float(np.percentile(allv, q)) for q in (50, 75, 90, 95)]
P('   price cuts on the WHOLE population: median %.0f · p75 %.0f · p90 %.0f · p95 %.0f'
  % tuple(QCUT))
P()
P('   %-6s %7s %8s %9s | %9s %9s %9s %9s | %10s' %
  ('pos', 'rows', 'players', 'games', '>median', '>p75', '>p90', '>p95', 'med v0'))
POP = {}
for p in POS_ALL:
    sub = by[p]
    ks = len(set(r['key'] for r in sub))
    gsum = sum(r['games'] for r in sub)
    cnt = [sum(1 for r in sub if r['v0'] > c) for c in QCUT]
    POP[p] = dict(rows=len(sub), players=ks, games=gsum, above=cnt,
                  medv0=float(np.median([r['v0'] for r in sub])) if sub else float('nan'))
    P('   %-6s %7d %8d %9.0f | %9d %9d %9d %9d | %10.0f' %
      (p, len(sub), ks, gsum, cnt[0], cnt[1], cnt[2], cnt[3], POP[p]['medv0']))
tot = dict(rows=len(ROWS))
P('   %-6s %7d %8d %9.0f |' % ('ALL', len(ROWS), len(set(r['key'] for r in ROWS)),
                               sum(r['games'] for r in ROWS)))
P()

# ---- 2 · the effective sample of the ESTIMATOR at each price ------------------------------------------
P('-' * 118)
P('2 · THE EFFECTIVE SAMPLE OF THE ESTIMATOR ITSELF (ESS), AT EACH PRICE')
P('-' * 118)
P('   ESS is the kernel\'s own effective sample: (sum k)^2 / sum(k^2) with k the tricube weight times')
P('   games. It is what the fit actually leans on at that price, not the raw row count.')
P('   Reference: the packet records TALL POOLED at about 47 effective at the top for all three')
P('   positions COMBINED. Anything materially under that is thinner than an already-thin object.')
P()
XP = [math.log(v) for v in (200.0, 500.0, 1000.0, 1500.0, 2000.0, 2500.0, 3000.0)]
ESS = {}


def ess_at(x0, sub, h=PB.H_PRIMARY):
    xs = np.array([r['x'] for r in sub]); ws = np.array([r['games'] for r in sub])
    k = PB.tricube((xs - x0) / h) * ws
    if k.sum() <= 0:
        return 0.0
    return float(k.sum() ** 2 / max(1e-12, (k ** 2).sum()))


P('   %-8s %8s %8s %8s %8s %8s %8s %8s' % ('group', 'v0=200', '500', '1000', '1500', '2000', '2500', '3000'))
for p in POS_ALL:
    ESS[p] = [ess_at(x, by[p]) for x in XP]
    P('   %-8s %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f' % (p, *ESS[p]))
for c in ('TALL', 'SMALL'):
    sub = [r for r in ROWS if r['cls'] == c]
    ESS[c] = [ess_at(x, sub) for x in XP]
    P('   %-8s %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f %8.1f' % (c + ' pool', *ESS[c]))
P()

# ---- 3 · the per-position fits and their slopes -------------------------------------------------------
P('-' * 118)
P('3 · dPG/dln(v0) — THE SLOPE, POOLED AND PER POSITION')
P('-' * 118)
P('   The slope is what drives the pick reversal. The charged pedigree leg FALLS with entry price')
P('   wherever  dPG/dln(v0) > 1/(BETA_sat*A(g)).  At saturation A=1 the threshold is 1/BETA_sat.')
P('       ORDER P BETA_sat %.5f  =>  threshold %.4f' % (BSAT_P, 1.0 / BSAT_P))
P('       CI floor %.5f          =>  threshold %.4f' % (BSAT_CI[0], 1.0 / BSAT_CI[0]))
P()


def fit_one(sub, grid_lo=None, grid_hi=None, n=121, h=PB.H_PRIMARY, iso=True):
    xs = np.array([r['x'] for r in sub]); ys = np.array([r['d'] for r in sub])
    ws = np.array([r['games'] for r in sub])
    lo = float(np.percentile(xs, 1)) if grid_lo is None else grid_lo
    hi = float(np.percentile(xs, 99)) if grid_hi is None else grid_hi
    gx = np.linspace(lo, hi, n)
    fit = np.array([PB.loclin(x0, xs, ys, ws, h)[0] for x0 in gx])
    if np.isnan(fit).any():
        fit = np.where(np.isnan(fit), np.nanmean(fit), fit)
    gy = PB.isotonize_up(fit) if iso else fit
    return gx, gy


def avg_slope(gx, gy):
    return float((gy[-1] - gy[0]) / (gx[-1] - gx[0]))


POOL = {}
for c in ('TALL', 'SMALL'):
    sub = [r for r in ROWS if r['cls'] == c]
    POOL[c] = fit_one(sub)
FIT = {}
for p in POS_ALL:
    FIT[p] = fit_one(by[p])

P('   AVERAGE SLOPE ACROSS EACH FIT\'S OWN SUPPORT (the reversal condition is read on this):')
P('   %-10s %10s %10s %12s %12s %10s' % ('group', 'support lo', 'support hi', 'PG at lo', 'PG at hi', 'avg slope'))
SL = {}
for c in ('TALL', 'SMALL'):
    gx, gy = POOL[c]; SL[c] = avg_slope(gx, gy)
    P('   %-10s %10.0f %10.0f %12.3f %12.3f %10.4f'
      % (c + ' pool', math.exp(gx[0]), math.exp(gx[-1]), gy[0], gy[-1], SL[c]))
for p in POS_ALL:
    gx, gy = FIT[p]; SL[p] = avg_slope(gx, gy)
    P('   %-10s %10.0f %10.0f %12.3f %12.3f %10.4f'
      % (p, math.exp(gx[0]), math.exp(gx[-1]), gy[0], gy[-1], SL[p]))
P()

# ---- 4 · CIs by player-level cluster bootstrap ---------------------------------------------------------
P('-' * 118)
P('4 · CONFIDENCE INTERVALS — PLAYER-LEVEL CLUSTER BOOTSTRAP, %d DRAWS, SEED %d' % (B_BOOT, SEED))
P('-' * 118)
P('   Players are the cluster, not seasons: one player contributes up to six correlated season rows.')
P('   Resampling seasons would understate the spread. Each draw resamples PLAYERS with replacement')
P('   and refits the whole surface on the SAME support grid, so the slopes are comparable draw to draw.')
P()
rng = np.random.default_rng(SEED)


def boot_slopes(sub, B=B_BOOT):
    keys = sorted(set(r['key'] for r in sub))
    idx = collections.defaultdict(list)
    for r in sub:
        idx[r['key']].append(r)
    xs0 = np.array([r['x'] for r in sub])
    lo = float(np.percentile(xs0, 1)); hi = float(np.percentile(xs0, 99))
    out = []
    for _ in range(B):
        pick = rng.choice(len(keys), size=len(keys), replace=True)
        rs = []
        for i in pick:
            rs.extend(idx[keys[i]])
        try:
            gx, gy = fit_one(rs, grid_lo=lo, grid_hi=hi)
            out.append(avg_slope(gx, gy))
        except Exception:
            continue
    return np.array(out)


P('   %-10s %8s %10s %-24s %12s %14s' %
  ('group', 'players', 'slope', '90% CI', 'CI width', 'crosses 8.723?'))
CI = {}
for g, sub in ([(c + ' pool', [r for r in ROWS if r['cls'] == c]) for c in ('TALL', 'SMALL')] +
               [(p, by[p]) for p in POS_ALL]):
    bs = boot_slopes(sub)
    lo, hi = float(np.percentile(bs, 5)), float(np.percentile(bs, 95))
    key = g.replace(' pool', '')
    CI[g] = (lo, hi)
    thr = 1.0 / BSAT_P
    cross = 'YES — both sides' if (lo <= thr <= hi) else ('no, ABOVE' if lo > thr else 'no, BELOW')
    P('   %-10s %8d %10.4f [%+9.4f,%+9.4f] %12.4f %14s'
      % (g, len(set(r['key'] for r in sub)), SL[key], lo, hi, hi - lo, cross))
P()

# ---- 5 · is a per-position fit supportable? -----------------------------------------------------------
P('-' * 118)
P('5 · IS A PER-POSITION FIT STATISTICALLY SUPPORTABLE? AND FOR WHICH POSITIONS?')
P('-' * 118)
P('   The test written down in advance: a per-position fit is supportable at a price only if the')
P('   estimator\'s own effective sample there is comparable to the pooled object it would replace.')
P('   ESS_THIN in ORDER P\'s own library is %.0f. Below that the fit is a handful of players.' % PB.ESS_THIN)
P()
P('   %-8s %10s %10s %10s | %-46s' % ('pos', 'ESS@1000', 'ESS@2000', 'ESS@3000', 'verdict at the expensive end'))
VERD = {}
for p in POS_ALL:
    e1, e2, e3 = ESS[p][2], ESS[p][4], ESS[p][6]
    if e3 >= PB.ESS_THIN:
        v = 'SUPPORTABLE to 3,000'
    elif e2 >= PB.ESS_THIN:
        v = 'supportable to ~2,000, NOT beyond'
    elif e1 >= PB.ESS_THIN:
        v = 'supportable to ~1,000, NOT beyond'
    else:
        v = 'NOT SUPPORTABLE — thin from the median up'
    VERD[p] = v
    P('   %-8s %10.1f %10.1f %10.1f | %-46s' % (p, e1, e2, e3, v))
for c in ('TALL', 'SMALL'):
    P('   %-8s %10.1f %10.1f %10.1f | %-46s'
      % (c + ' pool', ESS[c][2], ESS[c][4], ESS[c][6], '(the object a split would replace)'))
P()
P('   DO THE SLOPES DIFFER MATERIALLY? Pairwise, with the bootstrap spread as the yardstick.')
P('   Two positions differ materially only if their 90% CIs do not overlap.')
P()
P('   %-14s %10s %10s %10s | %-28s' % ('pair', 'slope A', 'slope B', 'diff', 'CIs overlap?'))
PAIRS = [('MID', 'SD'), ('MID', 'SF'), ('SD', 'SF'), ('KPD', 'KPF'), ('KPD', 'RUCK'), ('KPF', 'RUCK')]
OVER = {}
for a, b in PAIRS:
    la, ha = CI[a]; lb, hb = CI[b]
    ov = not (ha < lb or hb < la)
    OVER[(a, b)] = ov
    P('   %-14s %10.4f %10.4f %10.4f | %-28s'
      % ('%s vs %s' % (a, b), SL[a], SL[b], SL[a] - SL[b],
         'OVERLAP — no material difference' if ov else 'DISJOINT — materially different'))
P()

# ---- 6 · would a per-position premium reduce or worsen the reversal? -----------------------------------
P('-' * 118)
P('6 · WOULD A PER-POSITION PREMIUM REDUCE OR WORSEN THE PICK REVERSAL?')
P('-' * 118)
P('   The reversal is dPG/dln(v0) > 1/(BETA_sat*A). Pooling AVERAGES slopes. A split replaces the')
P('   pooled slope with each position\'s own. Where a position\'s own slope is STEEPER than the pool,')
P('   splitting makes its reversal WORSE; where it is shallower, splitting makes it better.')
P()
P('   %-8s %10s %10s %10s | %-40s' % ('pos', 'own slope', 'pool slope', 'own-pool', 'effect of splitting on the reversal'))
for p in POS_ALL:
    c = CLS_OF[p]; d = SL[p] - SL[c]
    eff = ('WORSE — its own slope is steeper than the pool' if d > 0.25 else
           ('better — its own slope is shallower' if d < -0.25 else
            'no material change — its slope is the pool\'s'))
    P('   %-8s %10.4f %10.4f %+10.4f | %-40s' % (p, SL[p], SL[c], d, eff))
P()
P('   THE MAXIMUM LOCAL SLOPE MATTERS MORE THAN THE AVERAGE, because the reversal is a LOCAL')
P('   condition: it bites wherever the fit is locally steep, not where it is steep on average.')
P()
P('   %-10s %12s %12s %14s %14s' % ('group', 'avg slope', 'max local', 'v0 at max', 'reverses at A=1?'))
for g, (gx, gy) in ([(c + ' pool', POOL[c]) for c in ('TALL', 'SMALL')] + [(p, FIT[p]) for p in POS_ALL]):
    d = np.diff(gy) / np.diff(gx)
    i = int(np.argmax(d))
    key = g.replace(' pool', '')
    P('   %-10s %12.4f %12.4f %14.0f %14s'
      % (g, SL[key], float(d[i]), math.exp(gx[i]), 'YES' if d[i] > 1.0 / BSAT_P else 'no'))
P()

json.dump(dict(pop={p: POP[p] for p in POS_ALL}, ess={k: list(map(float, v)) for k, v in ESS.items()},
               slope={k: float(v) for k, v in SL.items()}, ci={k: list(v) for k, v in CI.items()},
               verdict=VERD, overlap={('%s|%s' % k): v for k, v in OVER.items()},
               xp=[float(math.exp(x)) for x in XP], seed=SEED, boot=B_BOOT),
          open(os.path.join(HERE, 'POSITION_R.json'), 'w'), indent=1)
open(os.path.join(HERE, 'POSITION_R_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote POSITION_R.json and POSITION_R_out.txt')
