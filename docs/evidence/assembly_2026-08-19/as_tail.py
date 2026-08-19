#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE TAIL CALIBRATION ON THE CANDIDATE'S OWN CHARGE FORM.

THE ACCEPTANCE ITEM: "the tail calibration REPORTED against F5's expectation ~1.04". F5 computed
that expectation on the R-GRID CLIP — BETA_sat at its CI FLOOR (0.10416) with a HARD TMAX CLIP at
p20 — and read 1.04. THE CANDIDATE IS NOT THAT BOARD. It carries BETA_sat = 0.105 (the owner's
ruled value, above the floor) and the SMOOTH COMPRESSION T'(s) = C(1 - exp(-T_raw/C)) rather than a
clip. So the expectation cannot simply be quoted — it has to be recomputed on the form the candidate
actually charges with, and BOTH numbers printed side by side.

This file reuses os_f5.py's population and its charge algebra VERBATIM (imported, not
re-implemented) and changes ONE thing: the charge function f, which becomes the candidate's.

  calibration = ( realized(deep) / realized(at-bar) ) / ( charged(deep) / charged(at-bar) )

  = 1.00  the charge is exactly calibrated to outcomes
  > 1.00  the charge FRONT-LOADS — the deep cell delivers MORE than it was charged for
  < 1.00  the charge is GENEROUS to the deep cell

The deep cell is 10-22 games, surplus below -20, against the at-bar reference (surplus >= -10),
stages 1+2 pooled — F5's own cut, not a new one.

NO ENGINE RUN HERE. NO BOARD IS BUILT. NOTHING IS ADOPTED.
"""
import os, sys, json, math, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
F5DIR = os.path.join(REPO, 'docs/evidence/order_s_readonly_2026-08-19')
sys.path.insert(0, F5DIR)

import numpy as np

# Import os_f5's module-level population by executing it with its printing suppressed. It is a
# script, not a library, so this is the honest way to reuse it BYTE FOR BYTE rather than re-deriving
# a population that would then differ in some detail nobody would find.
_ns = {'__name__': '__as_tail__', '__file__': os.path.join(F5DIR, 'os_f5.py')}
_src = open(os.path.join(F5DIR, 'os_f5.py')).read()
_cwd = os.getcwd()
os.chdir(F5DIR)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src, os.path.join(F5DIR, 'os_f5.py'), 'exec'), _ns)
os.chdir(_cwd)

POOL12 = _ns['POOL12']
A_of = _ns['A_of']
LAMBDA = _ns['LAMBDA']
S0 = _ns['S0']
BETA_SAT_P = _ns['BETA_SAT']
S_PQ = {5: -33.06133449874688, 15: -22.148794633345666, 20: -19.024574086528315}

L = []


def P(s=''):
    print(s); L.append(str(s))


def T_raw(s, theta):
    return max(1.0 - theta * (s - S0), 0.0)


def T_clip(s, theta, tmax):
    return min(T_raw(s, theta), tmax)


def T_smooth(s, theta, C):
    """The candidate's cap. THE OWNER'S MONOTONE GAP-PRESERVING COMPRESSION, the engine's own form:
    T'(s) = C * (1 - exp(-T_raw(s)/C)). No flat segment anywhere, so worse play always costs strictly
    more; T' < C everywhere, so every row pays at most the hard-clip-at-Q charge."""
    return C * (1.0 - math.exp(-T_raw(s, theta) / C))


def f_clip(g, s, theta, tmax):
    return math.exp(-LAMBDA * A_of(g) * T_clip(s, theta, tmax))


def f_smooth(g, s, theta, C):
    return math.exp(-LAMBDA * A_of(g) * T_smooth(s, theta, C))


DEEP = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] < -20]
REF = [r for r in POOL12 if 10 <= r['g'] <= 22 and r['s'] >= -10]


def calib(fn, stat=np.mean):
    fa = float(np.mean([fn(r['g'], r['s']) for r in DEEP]))
    fb = float(np.mean([fn(r['g'], r['s']) for r in REF]))
    oa = float(stat([r['out'] for r in DEEP]))
    ob = float(stat([r['out'] for r in REF]))
    return (oa / ob) / (fa / fb), fa / fb, oa / ob


P('=' * 118)
P('ASSEMBLY BUILD — THE TAIL CALIBRATION, ON THE CANDIDATE\'S OWN CHARGE FORM')
P('=' * 118)
P('NO BOARD IS BUILT HERE. The population and the charge algebra are os_f5.py\'s, imported and not')
P('re-implemented. The ONE thing this file changes is the charge function f.')
P()
P('population : stages 1+2 pooled — deep cell n = %d (10-22 games, surplus < -20)' % len(DEEP))
P('             at-bar reference n = %d (10-22 games, surplus >= -10)' % len(REF))
P('reading    : > 1 the charge FRONT-LOADS (the deep cell delivers more than it was charged for)')
P('             < 1 the charge is GENEROUS to the deep cell')
P('basis      : the MEAN, which the owner accepted at v747 ("a lot of this engine prices on mean")')
P()

ROWS = []
# ORDER P as wired — the 1.90 headline
th_p = BETA_SAT_P / LAMBDA
c_p, ch_p, ou_p = calib(lambda g, s: f_clip(g, s, th_p, 1.0 - th_p * (S_PQ[5] - S0)))
ROWS.append(('ORDER P as wired (BETA_sat %.5f, hard clip p5)' % BETA_SAT_P, c_p, ch_p))

# F5's own convergence point — the CI floor + hard clip p20
th_f = 0.10416359711151935 / LAMBDA
c_f, ch_f, _ = calib(lambda g, s: f_clip(g, s, th_f, 1.0 - th_f * (S_PQ[20] - S0)))
ROWS.append(("F5's convergence point (BETA_sat CI FLOOR 0.10416, hard clip p20)", c_f, ch_f))

# the candidate: BETA_sat 0.105, SMOOTH compression anchored p20
BSAT_C = 0.105
th_c = BSAT_C / LAMBDA
C_c = 1.0 - th_c * (S_PQ[20] - S0)
c_c, ch_c, ou_c = calib(lambda g, s: f_smooth(g, s, th_c, C_c))
ROWS.append(('*** THE CANDIDATE (BETA_sat 0.105, SMOOTH compression p20) ***', c_c, ch_c))

# the two halves of the candidate's softening, separated
c_s1, ch_s1, _ = calib(lambda g, s: f_clip(g, s, th_c, 1.0 - th_c * (S_PQ[5] - S0)))
ROWS.append(('  the slope 0.105 alone (hard clip p5)', c_s1, ch_s1))
c_s2, ch_s2, _ = calib(lambda g, s: f_smooth(g, s, th_p, 1.0 - th_p * (S_PQ[20] - S0)))
ROWS.append(('  the compression p20 alone (BETA_sat as ORDER P)', c_s2, ch_s2))

P('  %-62s %10s %12s' % ('charge form', 'CALIB', 'charged ratio'))
for nm, c, ch in ROWS:
    P('  %-62s %10.4f %12.4f' % (nm, c, ch))
P()
P('  realized ratio (deep / at-bar), the same on every row above: %.4f' % ou_p)
P()
P('THE ANSWER TO THE ACCEPTANCE ITEM, IN ONE LINE:')
P('  F5 published ~1.04 for the FLOOR + CLIP combination. THE CANDIDATE READS %.4f.' % c_c)
P('  BUILT vs EXPECTED: %+.4f against F5\'s ~1.04.' % (c_c - 1.04))
P()
P('WHY THEY DIFFER — AND IT IS NOT THE SLOPE. THE CAP FORM IS DOING ALL OF IT.')
P()
P('  %-30s %14s %14s %14s' % ('BETA_sat', 'HARD CLIP p5', 'HARD CLIP p20', 'SMOOTH p20'))
GRID = {}
for bname, bs in (('ORDER P  0.11465', BETA_SAT_P), ('CI floor 0.10416', 0.10416359711151935),
                  ('RULED    0.105', 0.105)):
    th = bs / LAMBDA
    r5 = calib(lambda g, s, th=th, tm=1.0 - th * (S_PQ[5] - S0): f_clip(g, s, th, tm))[0]
    r20 = calib(lambda g, s, th=th, tm=1.0 - th * (S_PQ[20] - S0): f_clip(g, s, th, tm))[0]
    Cq = 1.0 - th * (S_PQ[20] - S0)
    rs = calib(lambda g, s, th=th, Cq=Cq: f_smooth(g, s, th, Cq))[0]
    GRID[bname.split()[0]] = dict(clip5=r5, clip20=r20, smooth20=rs)
    P('  %-30s %14.4f %14.4f %14.4f' % (bname, r5, r20, rs))
P()
P('READ THE LAST TWO COLUMNS. At EVERY slope the hard clip at p20 lands near 1.04-1.17 and the')
P('SMOOTH COMPRESSION at the SAME ANCHOR lands near 0.73-0.80. The slope barely moves the answer;')
P('THE CAP FORM MOVES IT BY ABOUT 0.35 OF CALIBRATION.')
P()
P('*** THIS CORRECTS A STATEMENT ON THE REGISTER, AND THE CORRECTION IS THE POINT OF THIS TABLE. ***')
P('v746 recorded: "the compression at the same anchor behaves ~identically at the parked tail; the')
P('assembly build verifies on real boards." THIS BUILD VERIFIED IT AND IT DOES NOT HOLD. The')
P('compression and the clip differ at the tail by roughly a third of a calibration unit, because the')
P('compression is STRICTLY BELOW the clip ceiling everywhere (T\' < C by construction, which is the')
P('very property that makes it monotone and gap-preserving) and the deep cell is exactly where the')
P('clip was binding. The ~1.04 figure on the register belongs to the CLIP. THE CANDIDATE USES THE')
P('COMPRESSION, AND ITS NUMBER IS %.4f.' % c_c)
P()
P('WHAT THAT MEANS IN PLAIN WORDS. On the mean, the candidate no longer over-charges the deep')
P('underperformer — it now UNDER-charges him by about a quarter. The direction is the one the owner')
P('asked for (his objection was that the charge was too harsh) but the ruled pair of softenings')
P('travels PAST the calibration point rather than landing on it. THIS SEAT IS NOT PROPOSING A FIX')
P('AND HAS NOT APPLIED ONE: the dials are ruled and the charter does not authorise re-opening them.')
P('It is reported here, loudly, because the acceptance item asked for exactly this comparison and')
P('because a number that misses its expectation by -0.30 must not be quietly filed as agreement.')
P()
P('THE OWNER\'S CHOICE, LAID OUT WITHOUT A RECOMMENDATION. If he wants the tail AT the calibration')
P('point, the hard clip at p20 with his ruled slope 0.105 reads %.4f — and that is a board this seat'
  % GRID['RULED']['clip20'])
P('can build on request. If he prefers the compression for the reason he chose it — no flat segment,')
P('worse play always costs strictly more — then %.4f is the price of that property at the tail.' % c_c)
P()

# the median reading, printed because F5 printed it
c_med, _, _ = calib(lambda g, s: f_smooth(g, s, th_c, C_c), np.median)
P('THE MEDIAN READING, PRINTED BECAUSE F5 PRINTED IT AND BURYING IT WOULD BE DISHONEST:')
P('  On the MEDIAN the candidate\'s deep cell calibrates at %.4f.' % c_med)
P('  F5\'s caveat stands unchanged and is repeated here rather than left behind: the deep cell is')
P('  OPTION-SHAPED. %d of %d deep rows deliver under 0.05 of entry and %d rows above 1.0 carry the'
  % (sum(1 for r in DEEP if r['out'] < 0.05), len(DEEP), sum(1 for r in DEEP if r['out'] > 1.0)))
P('  mean. The mean is primary because a multiplicative mark on a prior is a price and a price is an')
P('  expectation — the owner ruled on that at v747 — but on the typical deep row the charge is')
P('  GENEROUS, not harsh, and that is the reading his Pickett objection was about.')
P()
P('WHAT THIS DOES NOT SAY. It does not re-derive G0. v746\'s disposition holds: speed and strength')
P('are not separable in this data, a G0 move breaks the anchoring identity LAMBDA was solved by, and')
P('the interval gap was a hairline. The named open finding — the charge convicts somewhat fast at low')
P('games — is carried forward, not closed.')

json.dump(dict(n_deep=len(DEEP), n_ref=len(REF), realized_ratio=ou_p,
               rows=[dict(form=nm, calib=c, charged=ch) for nm, c, ch in ROWS],
               candidate_calib=c_c, candidate_calib_median=c_med,
               f5_expectation=1.04, built_minus_expected=c_c - 1.04,
               beta_sat_candidate=BSAT_C, C_candidate=C_c),
          open(os.path.join(HERE, 'TAIL_ASM.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'TAIL_ASM_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: TAIL_ASM.json · TAIL_ASM_out.txt')
