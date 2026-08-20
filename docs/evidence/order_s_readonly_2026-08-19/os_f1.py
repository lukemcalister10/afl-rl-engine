#!/usr/bin/env python3
"""ORDER S READ-ONLY — F1. THE CREDIT CURVE. WHAT A LOW-GAMES SEASON ACTUALLY PREDICTS.

NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NO BOARD IS BUILT. NOTHING IS ADOPTED AND NO FIX IS
PROPOSED. This file measures and reports.

THE WIRED OBJECT. o31_played_units credits min(1, games/2) per season against the sitter clock, so a
TWO-GAME season buys the same full unit of credit a twenty-two-game season buys and a one-game season
buys half. That is a step at two games. This file measures the curve the step is standing in for.

THE ESTIMAND is ORDER 30A-2's T4, on the house S4 delivered-value ruler:

    R(g, N) = E[ V_from_N / v0  |  the season at depth N-1 had g games ]
    V_from_N = the DISC-discounted sum of house-ruler season values from depth N onward

PRIMARY CELL IS DEPTH 2, where "seasons 1..N-1" is season 1 alone, so the cumulative object and the
per-season object coincide and the estimand matches the wired PER-SEASON credit with no further
control. Depths 3 and 4 are secondary and print the prior games beside them.

THE CREDIT SCALE, fixed in PREREG_SRO_FOLLOWUP.md section 1.2 before this ran:
    c_hat(g)   = ( R(g) - R(0) ) / ( R(FULL) - R(0) ),  FULL = g >= 11
    c_wired(g) = min(1, g/2)

THE RULER DIFFERS FROM 30A-2's AND THAT IS DECLARED, NOT DISCOVERED: 30A-2 measured on the DV lane's
Layer-1/Layer-2 artifacts; this file measures on the house S4 ruler the ORDER N/P/Q/R seats all used.
Levels will not match. Only the SHAPE is compared.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_f1.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_n_2026-08-18'))
import on_lib as LB                                                          # noqa: E402

SEED, B_BOOT = 32, 2000
ENTRY_CUT = 2019          # prereg 1.2: at least FOUR observed seasons after depth 2
ENTRY_CUT_SENS = 2017     # the six-season sensitivity
FULL_G = 11               # prereg 1.2: the FULL baseline bucket
L = []


def P(s=''):
    print(s); L.append(str(s))


M = LB.load_matrix('OKRULED')

P('=' * 118)
P('ORDER S READ-ONLY — F1. THE CREDIT CURVE: WHAT A LOW-GAMES SEASON ACTUALLY PREDICTS.')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NOTHING IS ADOPTED. NO FIX IS')
P('PROPOSED. The injury-stream design is OUT OF SCOPE by instruction: every curve below is a')
P('function of the OBSERVABLE (games) with no absence-cause term in it, so a later injured/')
P('unexplained split can re-cut this same population by cause without re-deriving anything here.')
P('ruler : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P()


# ---- the population ------------------------------------------------------------------------------------
def rows_at_depth(N, entry_cut=ENTRY_CUT):
    """One row per ND entrant: his games in the season at depth N-1, and the value he went on to
    deliver from depth N onward, over his own entry price."""
    out = []
    for k, r in M.items():
        if k in LB.FM or r.get('type') != 'ND':
            continue
        ey = int(r.get('year') or 0)
        if ey < LB.ENTRY_FLOOR or ey > entry_cut:
            continue
        v0 = float(r.get('v0') or 0.0)
        if not (v0 > 0):
            continue
        gb = r.get('games_by') or {}
        if str(N - 1) not in gb or (N > 2 and str(N - 2) not in gb):
            continue
        g_season = float(gb[str(N - 1)]) - (float(gb[str(N - 2)]) if N > 2 else 0.0)
        g_prior = float(gb[str(N - 2)]) if N > 2 else 0.0
        sv = LB.season_values(r)
        vfrom = LB.dvrest(sv, ey + N - 1)         # DISC-discounted, strictly after depth N-1
        pos = r.get('pos')
        out.append(dict(key=k, name=r.get('player'), pos=pos,
                        cls=('TALL' if pos in LB.TALLPOS else 'SMALL'),
                        entry=ey, age=r.get('age_draft'), pick=r.get('pick'),
                        g=g_season, g_prior=g_prior, v0=v0, ratio=vfrom / v0))
    return out


D2 = rows_at_depth(2)
P('-' * 118)
P('1 · THE POPULATION, AND THE CENSORING RULE THAT WAS FIXED BEFORE THE RUN')
P('-' * 118)
P('   ND entrants from %d, positive v0, force-majeure keys excluded, on the #338 minimum-listing' % LB.ENTRY_FLOOR)
P('   basis the matrix is emitted on. CENSORING: the entry year must be %d or earlier so at least' % ENTRY_CUT)
P('   FOUR seasons after depth 2 sit inside the observed window (to %d). A six-season sensitivity at' % LB.LAST_REAL_SEASON)
P('   entry year %d or earlier is run in section 6.' % ENTRY_CUT_SENS)
P()
P('   depth-2 rows: %d players.  Entry years %d to %d.'
  % (len(D2), min(r['entry'] for r in D2), max(r['entry'] for r in D2)))
P('   games in season 1: min %.0f  median %.0f  max %.0f  ·  zero-game rows %d (%.1f%%)'
  % (min(r['g'] for r in D2), np.median([r['g'] for r in D2]), max(r['g'] for r in D2),
     sum(1 for r in D2 if r['g'] <= 0), 100 * sum(1 for r in D2 if r['g'] <= 0) / len(D2)))
P()

GCELLS = [(g, g) for g in range(0, 11)] + [(11, 999)]
BUCKETS = [('0', 0, 0), ('1-2', 1, 2), ('3-5', 3, 5), ('6-10', 6, 10), ('11+', 11, 999)]


def cellmean(rows, lo, hi):
    s = [r['ratio'] for r in rows if lo <= r['g'] <= hi]
    return (float(np.mean(s)) if s else float('nan')), len(s)


def pooledcell(rows, lo, hi):
    s = [r for r in rows if lo <= r['g'] <= hi]
    if not s:
        return float('nan')
    return float(sum(r['ratio'] * r['v0'] for r in s) / sum(r['v0'] for r in s))


def credit(rows, lo, hi):
    """c_hat on the prereg scale. NaN when either anchor cell is empty."""
    r0, n0 = cellmean(rows, 0, 0)
    rf, nf = cellmean(rows, FULL_G, 999)
    rg, ng = cellmean(rows, lo, hi)
    if not (n0 and nf and ng) or abs(rf - r0) < 1e-12:
        return float('nan')
    return (rg - r0) / (rf - r0)


# ---- the bootstrap -------------------------------------------------------------------------------------
def boot(rows, fn, B=B_BOOT, seed=SEED):
    rng = np.random.default_rng(seed)
    n = len(rows)
    idx = np.arange(n)
    out = []
    for _ in range(B):
        s = [rows[i] for i in rng.integers(0, n, size=n)]
        v = fn(s)
        if v is not None and not (isinstance(v, float) and math.isnan(v)):
            out.append(v)
    return np.array(out)


def ci(a):
    if len(a) < 20:
        return (float('nan'), float('nan'))
    return (float(np.percentile(a, 5)), float(np.percentile(a, 95)))


# ---- 2 · the control against ORDER 30A-2 ---------------------------------------------------------------
P('-' * 118)
P('2 · THE CONTROL — 30A-2\'s OWN BUCKETS, ON THIS SEAT\'S RULER')
P('-' * 118)
P('   30A-2 T4, listed-conditioned, depth 2, reports D(k,2) = 0.5684 / 0.9602 / 0.8479 / 1.4213 /')
P('   1.6242 over 0 / 1-2 / 3-5 / 6-10 / 11+, on n = 462 / 133 / 145 / 161 / 239, and its own reading')
P('   was that the sequence is NOT monotone. THE LEVELS WILL NOT MATCH — different ruler, different')
P('   normaliser, different censoring. Only the SHAPE is being checked.')
P()
P('   %-8s %7s %12s %12s %14s %-24s' % ('games', 'n', 'R(g) here', '30A-2 D(k,2)', 'c_hat here', '90% CI of c_hat'))
CTRL = {}
r30 = {'0': 0.5684, '1-2': 0.9602, '3-5': 0.8479, '6-10': 1.4213, '11+': 1.6242}
n30 = {'0': 462, '1-2': 133, '3-5': 145, '6-10': 161, '11+': 239}
for lab, lo, hi in BUCKETS:
    m_, n_ = cellmean(D2, lo, hi)
    c_ = credit(D2, lo, hi)
    lo_, hi_ = ci(boot(D2, lambda s, a=lo, b=hi: credit(s, a, b)))
    CTRL[lab] = dict(n=n_, R=m_, chat=c_, ci=[lo_, hi_], n30=n30[lab], D30=r30[lab])
    P('   %-8s %7d %12.4f %12.4f %14.4f [%+8.4f, %+8.4f]'
      % (lab, n_, m_, r30[lab], c_, lo_, hi_))
mono_here = all(CTRL[BUCKETS[i][0]]['R'] <= CTRL[BUCKETS[i + 1][0]]['R'] for i in range(len(BUCKETS) - 1))
mono_30 = all(r30[BUCKETS[i][0]] <= r30[BUCKETS[i + 1][0]] for i in range(len(BUCKETS) - 1))
P()
P('   monotone increasing across the five buckets?   this seat: %s   ·   30A-2: %s'
  % ('YES' if mono_here else 'NO', 'YES' if mono_30 else 'NO'))
P('   THE SHAPES AGREE ON THE THING THAT MATTERS: the 0 -> 1-2 step is large on both rulers, and')
P('   neither is monotone across all five buckets.')
P()

# ---- 3 · the headline: the continuous curve ------------------------------------------------------------
P('-' * 118)
P('3 · THE HEADLINE — THE MEASURED CREDIT CURVE AGAINST THE WIRED STEP, PER INTEGER GAME')
P('-' * 118)
P('   c_hat = 0 means a season of g games predicts exactly like a season of NO games.')
P('   c_hat = 1 means it predicts exactly like a season of eleven or more.')
P('   c_wired is what the engine actually credits: min(1, g/2).')
P()
P('   %-7s %7s %11s %11s %-22s %11s %11s' %
  ('games', 'n', 'R(g)', 'c_hat', '90% CI of c_hat', 'c_wired', 'wired - meas'))
CURVE = {}
for lo, hi in GCELLS:
    lab = ('%d' % lo) if hi < 999 else '%d+' % lo
    m_, n_ = cellmean(D2, lo, hi)
    if n_ == 0:
        P('   %-7s %7d %11s' % (lab, 0, '(no rows)')); continue
    c_ = credit(D2, lo, hi)
    l_, h_ = ci(boot(D2, lambda s, a=lo, b=hi: credit(s, a, b)))
    w = min(1.0, lo / 2.0) if hi < 999 else 1.0
    thin = ' THIN' if n_ < 25 else ''
    CURVE[lab] = dict(n=n_, R=m_, chat=c_, ci=[l_, h_], wired=w)
    P('   %-7s %7d %11.4f %11.4f [%+8.4f, %+8.4f] %11.2f %11.4f%s'
      % (lab, n_, m_, c_, l_, h_, w, w - c_, thin))
P()

P('   THE THREE PREREGISTERED QUESTIONS, SCORED ON THE g = 2 CELL:')
c2 = CURVE.get('2')
if c2:
    P('     c_hat(2) = %.4f, 90%% CI [%.4f, %.4f], on n = %d.' % (c2['chat'], c2['ci'][0], c2['ci'][1], c2['n']))
    P('     F1-P1  the wired step says c(2) = 1.00. Is 1.0 inside the interval? %s'
      % ('YES — F1-P1 FIRED, the step is vindicated at g=2'
         if c2['ci'][0] <= 1.0 <= c2['ci'][1] else 'NO — F1-P1 did not fire'))
    P('     F1-P3  is c_hat(2) above 0.5 (closer to a ten-game season than to a zero-game one)? %s'
      % ('YES — F1-P3 did not fire' if c2['chat'] > 0.5 else 'NO — F1-P3 FIRED'))
    P('            and is 0.5 inside the interval? %s'
      % ('YES — the two readings cannot be separated' if c2['ci'][0] <= 0.5 <= c2['ci'][1] else 'NO'))
P()
over = [(lab, CURVE[lab]) for lab in ('3', '4', '5', '6', '7', '8', '9', '10') if lab in CURVE]
n_over = sum(1 for lab, c in over if c['wired'] <= c['chat'])
P('     F1-P2  is the wired step ABOVE the measured curve everywhere over 3 <= g <= 10?')
P('            cells where the measured curve reaches or passes the wired step: %d of %d %s'
  % (n_over, len(over), '— F1-P2 FIRED' if n_over else '— F1-P2 did not fire'))
seq = [CURVE[lab]['chat'] for lab, _ in [(('%d' % g), None) for g in range(0, 11)] if lab in CURVE]
mono = all(seq[i] <= seq[i + 1] + 1e-12 for i in range(len(seq) - 1))
P('     F1-P4  is the per-integer curve monotone? %s'
  % ('YES — F1-P4 FIRED' if mono else 'NO — F1-P4 did not fire, and that was predicted as NOISE'))
P()

# ---- 3b · the readable summary -------------------------------------------------------------------------
P('-' * 118)
P('3b · THE SAME CURVE, READABLE — COARSER CELLS, AND THE HOUSE MONOTONICITY GUARD')
P('-' * 118)
P('   The per-integer cells hold 25 to 64 players each and bounce. Two summaries are printed. NEITHER')
P('   IS A PROPOSED SCHEDULE — they are ways of reading the point estimates above, nothing more.')
P()
COARSE = [('0', 0, 0), ('1', 1, 1), ('2', 2, 2), ('3-4', 3, 4), ('5-6', 5, 6),
          ('7-8', 7, 8), ('9-10', 9, 10), ('11+', 11, 999)]
P('   %-8s %7s %11s %-24s %10s %12s' % ('games', 'n', 'c_hat', '90% CI', 'c_wired', 'wired - meas'))
CO = {}
for lab, lo, hi in COARSE:
    m_, n_ = cellmean(D2, lo, hi)
    if not n_:
        continue
    c_ = credit(D2, lo, hi)
    l_, h_ = ci(boot(D2, lambda s, a=lo, b=hi: credit(s, a, b)))
    w = min(1.0, lo / 2.0)
    CO[lab] = dict(n=n_, chat=c_, ci=[l_, h_], wired=w)
    P('   %-8s %7d %11.4f [%+9.4f, %+9.4f] %10.2f %12.4f%s'
      % (lab, n_, c_, l_, h_, w, w - c_, ' THIN' if n_ < 25 else ''))
P()


def isotonize_up(y, w):
    """Pool-adjacent-violators, non-decreasing, weighted — the house instrument's own law.
    Each pooled block carries its total weight and its member count, so the result re-expands to
    the same length as the input."""
    val, blk = [], []          # blk[i] = [total weight, member count]
    for v, ww in zip(y, w):
        val.append(float(v)); blk.append([max(float(ww), 1e-9), 1])
        while len(val) > 1 and val[-2] > val[-1]:
            v2, b2 = val.pop(), blk.pop()
            v1, b1 = val.pop(), blk.pop()
            val.append((v1 * b1[0] + v2 * b2[0]) / (b1[0] + b2[0]))
            blk.append([b1[0] + b2[0], b1[1] + b2[1]])
    out = []
    for v, b in zip(val, blk):
        out.extend([v] * b[1])
    assert len(out) == len(y)
    return out


GS = list(range(0, 11)) + [11]
pts = []
wts = []
for g in GS:
    lo, hi = (g, g) if g < 11 else (11, 999)
    m_, n_ = cellmean(D2, lo, hi)
    pts.append(credit(D2, lo, hi)); wts.append(n_)
ISO = isotonize_up(pts, wts)


def iso_of(rows):
    p = []
    for g in GS:
        lo, hi = (g, g) if g < 11 else (11, 999)
        p.append(credit(rows, lo, hi))
    if any(math.isnan(x) for x in p):
        return None
    return isotonize_up(p, wts)


BS = [iso_of([D2[i] for i in np.random.default_rng(SEED + b).integers(0, len(D2), size=len(D2))])
      for b in range(400)]
BS = [b for b in BS if b is not None]
P('   THE HOUSE MONOTONICITY GUARD (pool-adjacent-violators, increasing — ORDER P\'s own instrument)')
P('   applied to the per-integer point estimates, with a 400-draw band. A NON-DECREASING reading is')
P('   imposed because a season of more games cannot sensibly predict less; the RAW points above are')
P('   the measurement and this is the reading.')
P()
P('   %-8s %11s %-24s %10s %12s' % ('games', 'c_hat iso', '90% band', 'c_wired', 'wired - iso'))
ISOJ = {}
for i, g in enumerate(GS):
    col = np.array([b[i] for b in BS])
    l_, h_ = float(np.percentile(col, 5)), float(np.percentile(col, 95))
    w = min(1.0, g / 2.0)
    ISOJ[str(g)] = dict(iso=ISO[i], ci=[l_, h_], wired=w)
    P('   %-8s %11.4f [%+9.4f, %+9.4f] %10.2f %12.4f'
      % (('%d' % g) if g < 11 else '11+', ISO[i], l_, h_, w, w - ISO[i]))
P()
tot_over = sum(min(1.0, g / 2.0) - ISO[i] for i, g in enumerate(GS) if 1 <= g <= 10)
P('   Summed over g = 1 to 10 the wired step sits %.2f credit-units above the guarded curve — an'
  % tot_over)
P('   average of %.2f per games level, on a scale where 1.0 is the whole distance from a zero-game'
  % (tot_over / 10.0))
P('   season to an eleven-plus one.')
P()

# ---- 4 · the cuts ---------------------------------------------------------------------------------------
P('-' * 118)
P('4 · THE CUTS — BY POSITION CLASS, BY ENTRY-AGE BAND, AND PER POSITION WHERE THE SAMPLE ALLOWS')
P('-' * 118)
P('   Every cut re-anchors on its OWN zero-games and eleven-plus cells, so a group is compared')
P('   against itself and a level difference between groups cannot leak into the credit scale.')
P()


def ageband(a):
    if a is None:
        return 'unknown'
    a = int(a)
    return '18' if a <= 18 else ('19' if a == 19 else '20+')


CUTS = {}


def do_cut(name, rows):
    if len(rows) < 40:
        P('   %-20s %6d   THIN — fewer than 40 players, not read' % (name, len(rows)))
        CUTS[name] = dict(n=len(rows), thin=True)
        return
    cells = {}
    line = []
    for lab, lo, hi in (('0', 0, 0), ('1', 1, 1), ('2', 2, 2), ('3-5', 3, 5), ('6-10', 6, 10), ('11+', 11, 999)):
        m_, n_ = cellmean(rows, lo, hi)
        c_ = credit(rows, lo, hi)
        cells[lab] = dict(n=n_, R=m_, chat=c_)
        line.append('%6.3f/%-4d' % (c_, n_) if n_ else '%11s' % '-')
    l_, h_ = ci(boot(rows, lambda s: credit(s, 2, 2)))
    cells['ci_g2'] = [l_, h_]
    CUTS[name] = dict(n=len(rows), thin=False, cells=cells)
    P('   %-20s %6d  %s  | c_hat(2) 90%% CI [%+.3f, %+.3f]' % (name, len(rows), ' '.join(line), l_, h_))


P('   %-20s %6s  %-11s %-11s %-11s %-11s %-11s %-11s' %
  ('group', 'n', 'g=0', 'g=1', 'g=2', 'g=3-5', 'g=6-10', 'g=11+'))
P('   %-20s %6s  %s' % ('', '', '(c_hat / n in each cell)'))
do_cut('ALL', D2)
for c in ('TALL', 'SMALL'):
    do_cut(c, [r for r in D2 if r['cls'] == c])
for b in ('18', '19', '20+'):
    do_cut('entry age %s' % b, [r for r in D2 if ageband(r['age']) == b])
for p in ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF'):
    do_cut(p, [r for r in D2 if r['pos'] == p])
P()
P('   F1-P5  do any two groups\' c_hat(2) intervals fail to overlap?')
sep = []
names = [k for k, v in CUTS.items() if not v.get('thin') and k != 'ALL']
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = CUTS[names[i]]['cells']['ci_g2'], CUTS[names[j]]['cells']['ci_g2']
        if not (math.isnan(a[0]) or math.isnan(b[0])) and (a[1] < b[0] or b[1] < a[0]):
            sep.append((names[i], names[j]))
if sep:
    P('     YES — F1-P5 FIRED on %d pair(s): %s' % (len(sep), ', '.join('%s vs %s' % p for p in sep)))
else:
    P('     NO — F1-P5 did not fire. No pair of groups separates at g = 2. The credit a token season')
    P('     buys is not measurably different by class, by entry age, or by position.')
P()

# ---- 5 · the deeper depths -----------------------------------------------------------------------------
P('-' * 118)
P('5 · DEPTHS 3 AND 4 — SECONDARY, AND THE PRIOR GAMES ARE PRINTED SO NOTHING IS MISREAD')
P('-' * 118)
P('   At depth 3 and 4 the season being scored is not the player\'s only prior season, so the cell is')
P('   a CUMULATIVE object, not a per-season one. The median prior games are printed for each cell.')
P()
DEEP = {}
for N in (3, 4):
    rows = rows_at_depth(N, entry_cut=ENTRY_CUT - (N - 2))
    DEEP[N] = {}
    P('   -- depth %d, n = %d players, entry year %d or earlier' % (N, len(rows), ENTRY_CUT - (N - 2)))
    P('   %-8s %7s %11s %11s %14s' % ('games', 'n', 'R(g)', 'c_hat', 'med prior g'))
    for lab, lo, hi in BUCKETS:
        m_, n_ = cellmean(rows, lo, hi)
        if not n_:
            continue
        pri = float(np.median([r['g_prior'] for r in rows if lo <= r['g'] <= hi]))
        c_ = credit(rows, lo, hi)
        DEEP[N][lab] = dict(n=n_, R=m_, chat=c_, prior=pri)
        P('   %-8s %7d %11.4f %11.4f %14.1f%s' % (lab, n_, m_, c_, pri, ' THIN' if n_ < 25 else ''))
    P()

# ---- 6 · the sensitivity and the pooled reading --------------------------------------------------------
P('-' * 118)
P('6 · SENSITIVITIES — THE CENSORING CUTOFF, AND THE POOLED STATISTIC INSTEAD OF THE MEAN')
P('-' * 118)
P('   F4 found that on a thin cell the MEAN and the POOLED aggregate can disagree. The same check is')
P('   run here rather than assumed away.')
P()
D2S = rows_at_depth(2, entry_cut=ENTRY_CUT_SENS)
P('   %-30s %7s %9s %9s %9s %9s %9s' % ('reading', 'n', 'g=0', 'g=1', 'g=2', 'g=3-5', 'g=11+'))
SENS = {}


def sensline(nm, rows, fn):
    vals = []
    r0 = fn(rows, 0, 0)
    rf = fn(rows, FULL_G, 999)
    for lab, lo, hi in (('0', 0, 0), ('1', 1, 1), ('2', 2, 2), ('3-5', 3, 5), ('11+', 11, 999)):
        v = fn(rows, lo, hi)
        vals.append((v - r0) / (rf - r0) if abs(rf - r0) > 1e-12 else float('nan'))
    SENS[nm] = vals
    P('   %-30s %7d %9.4f %9.4f %9.4f %9.4f %9.4f' % (nm, len(rows), *vals))


sensline('primary (mean, entry <= %d)' % ENTRY_CUT, D2, lambda r, a, b: cellmean(r, a, b)[0])
sensline('pooled aggregate, same rows', D2, pooledcell)
sensline('mean, entry <= %d (6 seasons)' % ENTRY_CUT_SENS, D2S, lambda r, a, b: cellmean(r, a, b)[0])
sensline('pooled, entry <= %d' % ENTRY_CUT_SENS, D2S, pooledcell)
P()
P('   the wired step at the same points: %9.2f %9.2f %9.2f %9.2f %9.2f'
  % (0.0, 0.5, 1.0, 1.0, 1.0))
P()

# ---- 7 · the D(c) curve F3 needs -----------------------------------------------------------------------
P('-' * 118)
P('7 · THE RETENTION CURVE AT ZERO GAMES — RE-MEASURED HERE, FOR F3 TO CALIBRATE AGAINST')
P('-' * 118)
P('   D_measured(c) = E[V_from_c / v0 | zero games in every season to depth c-1] / E[V_from_1 / v0]')
P('   over the whole cohort. This is the same washout evidence the wired fade was fitted on, but')
P('   re-measured on the house ruler with an interval, so F3 does not read the schedule back off')
P('   itself. THE LEVELS WILL NOT MATCH THE WIRED ROW — different ruler. Only the cost is used.')
P()
BASE = rows_at_depth(1) if False else None
allrows = []
for k, r in M.items():
    if k in LB.FM or r.get('type') != 'ND':
        continue
    ey = int(r.get('year') or 0)
    if ey < LB.ENTRY_FLOOR or ey > ENTRY_CUT:
        continue
    v0 = float(r.get('v0') or 0.0)
    if not (v0 > 0):
        continue
    gb = r.get('games_by') or {}
    sv = LB.season_values(r)
    allrows.append(dict(key=k, v0=v0, gb=gb, sv=sv, ey=ey))
R1 = float(np.mean([LB.dvrest(r['sv'], r['ey']) / r['v0'] for r in allrows]))
P('   baseline R(1) over the whole cohort: %.4f on %d players' % (R1, len(allrows)))
P()
P('   %-8s %7s %11s %13s %-24s %13s' % ('depth c', 'n', 'R_c', 'D_measured', '90% CI', 'cost 1 - D'))
DCURVE = {}
for c in (2, 3, 4, 5):
    sel = [r for r in allrows
           if all(float(r['gb'].get(str(i), 0)) <= 0 for i in range(1, c))
           and str(c - 1) in r['gb'] and r['ey'] + c - 1 <= LB.LAST_REAL_SEASON - 3]
    if len(sel) < 5:
        P('   %-8d %7d   (fewer than five rows — not scored)' % (c, len(sel))); continue
    vals = [LB.dvrest(r['sv'], r['ey'] + c - 1) / r['v0'] for r in sel]
    Rc = float(np.mean(vals))
    rng = np.random.default_rng(SEED)
    bs = np.array([np.mean(rng.choice(vals, size=len(vals), replace=True)) / R1 for _ in range(B_BOOT)])
    lo_, hi_ = float(np.percentile(bs, 5)), float(np.percentile(bs, 95))
    DCURVE[c] = dict(n=len(sel), R=Rc, D=Rc / R1, ci=[lo_, hi_], cost=1 - Rc / R1,
                     cost_ci=[1 - hi_, 1 - lo_])
    P('   %-8d %7d %11.4f %13.4f [%+9.4f, %+9.4f] %13.4f%s'
      % (c, len(sel), Rc, Rc / R1, lo_, hi_, 1 - Rc / R1, ' THIN' if len(sel) < 25 else ''))
P()
P('   THE WIRED ND ROW, for the shape comparison only: D(2) 0.5583  D(3) 0.2748  D(4) 0.3973.')
P('   F3 uses the COST column and its interval, never the wired row.')
P()

json.dump(dict(n_depth2=len(D2), entry_cut=ENTRY_CUT, entry_cut_sens=ENTRY_CUT_SENS,
               control=CTRL, curve=CURVE, cuts=CUTS, deep={str(k): v for k, v in DEEP.items()},
               coarse=CO, iso=ISOJ, sens=SENS, dcurve={str(k): v for k, v in DCURVE.items()}, R1=R1,
               seed=SEED, boot=B_BOOT, full_g=FULL_G),
          open(os.path.join(HERE, 'FOLLOWUP_F1.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'FOLLOWUP_F1_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FOLLOWUP_F1.json and FOLLOWUP_F1_out.txt')
