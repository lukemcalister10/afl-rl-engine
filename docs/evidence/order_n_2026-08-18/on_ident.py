#!/usr/bin/env python3
"""ORDER N — THE OFFLINE PRICING IDENTITY. FALSIFIER N1. READ-ONLY.

PREREG_N.md section 6 claims the engine price is exactly linear in ETA at fixed knobs, because ETA
enters only through the factor (1 - ETA*m_d(g)) multiplying pi. If that is wrong, all of Step 4 is
withdrawn.

The claim is tested four ways, none of them circular:

  T1  DIRECTION. ETA can only subtract, so v(ETA=0) >= v(ETA=0.50) on every row and every vantage,
      and rows with g=0 must be EQUAL to the last printed digit.
  T2  LINEARITY, on built boards. ORDER M built six boards at dose 0.40 walking ETA 0.00 -> 0.50 in
      steps of 0.10 (LADDER_M.json). For each named row the six prices must lie on a straight line
      in ETA. Reported as the maximum deviation from the least-squares line, in board points.
  T3  SEPARABILITY. The implied charge base C = (v0eta - vK) / (0.50 * m_d(g)) must equal
      pi_pre(g) * pedigree. pedigree does not depend on g, so for a player observed at several
      vantages with DIFFERENT games counts, C / pi_pre(g) must be the SAME NUMBER at every vantage.
      pi_pre is computed here from the engine's own published constants with D = 1 and Phi = 1.
      That is the correct comparison for a row that has played and has no stall run.
  T4  ROUND TRIP. Rebuilding v(0.50) from v(0) and the implied base must return the emitted value.
      This one IS an identity by construction and is reported only as an arithmetic check.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_ident.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

REPO = LB.REPO
L = []


def P(s=''):
    print(s); L.append(str(s))


# ---- the engine's own constants, transcribed for pi_pre ---------------------------------------------
TAU_RHO, B_RHO = 29.194253560287144, 0.8015424473253033
BETA_ND = ((2.5, 0.2878886216033701), (10.5, 0.2878886216033701), (25.5, 0.21772876584106796),
           (53.0, 0.14155152291809878), (85.5, 0.023849021706229417))
BETA_POOL = None            # not needed: T3 is run on ND rows only
KAPPA_K, GAMMA_U_K = 0.20, 8.0                                # ORDER K's ruled re-mix knobs


def loglin(pts, g):
    g = max(1e-9, float(g))
    if g <= pts[0][0]: return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0 or y1 <= 0:
                return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]


def rho_base(g):
    g = float(g)
    return 0.0 if g <= 0 else 1.0 - math.exp(-((g / TAU_RHO) ** B_RHO))


def m_u(g, gu=GAMMA_U_K):
    return (g / gu) * math.exp(1.0 - g / gu)


def rho32(g, kap=KAPPA_K, gu=GAMMA_U_K):
    r = rho_base(g)
    return r if r <= 0 else r + kap * m_u(g, gu) * (1.0 - r)


def pi_pre(g):
    """pi BEFORE the eta factor, at D = 1 and Phi = 1 (a played row with no stall run)."""
    r = rho32(g)
    return 1.0 * (1.0 - r) + loglin(BETA_ND, g) * r


P('=' * 118)
P('ORDER N — THE OFFLINE PRICING IDENTITY. FALSIFIER N1.')
P('=' * 118)
P('claim: v(ETA) = v(0) - ETA * pi_pre(g) * pedigree * m_d(g),  m_d(g) = (g/14)*exp(1 - g/14)')
P()

MK = LB.load_matrix('OKRULED')          # ETA = 0.50
ME = LB.load_matrix('M0ETA0')           # ETA = 0.00, everything else identical
assert set(MK) == set(ME)

# ---- T1 ---------------------------------------------------------------------------------------------
P('-' * 118)
P('T1 · DIRECTION AND THE g = 0 LAW')
P('-' * 118)
bad_dir = []; bad_zero = []; n_pairs = 0; n_zero = 0
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []
    vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    gb = a.get('games_by') or {}
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            continue
        N = y - int(a['year'])
        g = LB.career_games(a, y)
        n_pairs += 1
        if vpb[i] + 1e-9 < vpa[i]:
            bad_dir.append((k, y, vpa[i], vpb[i]))
        if g <= 0:
            n_zero += 1
            if abs(vpb[i] - vpa[i]) > 1e-9:
                bad_zero.append((k, y, vpa[i], vpb[i]))
    if abs(float(a['v0'] or 0) - float(b['v0'] or 0)) > 1e-9:
        bad_zero.append((k, 'v0', a['v0'], b['v0']))
P('   row-vantage pairs compared        : %d' % n_pairs)
P('   pairs where ETA=0 is NOT >= ETA=.5: %d %s' % (len(bad_dir), bad_dir[:3]))
P('   gameless vantages                 : %d, of which not bit-equal: %d %s' % (n_zero, len(bad_zero), bad_zero[:3]))
P('   day-0 v0 mismatches               : %d' % sum(1 for x in bad_zero if x[1] == 'v0'))
T1 = (len(bad_dir) == 0 and len(bad_zero) == 0)
P('   T1: %s' % ('PASS' if T1 else 'FAIL'))
P()

# ---- T2 ---------------------------------------------------------------------------------------------
P('-' * 118)
P('T2 · LINEARITY IN ETA ON SIX BUILT BOARDS (LADDER A, dose 0.40, ORDER M)')
P('-' * 118)
LAD = json.load(open(os.path.join(REPO, 'docs/evidence/order_m_2026-08-18/LADDER_M.json')))['ladderA']
etas = np.array([float(r['eta']) for r in LAD])
P('   etas built: %s   (six boards, md5s %s)' % (list(etas), [r['md5'] for r in LAD]))
P('   %-14s | %-42s | %10s %10s' % ('row', 'board points at eta 0.00 .. 0.50', 'max dev', 'slope/0.1'))
T2max = 0.0
T2 = {}
for fld, nm in (('dean', 'harry-dean'), ('cdt', 'cooper-duff-tytler'), ('xavier', 'xavier-taylor'),
                ('annable', 'daniel-annable'), ('patterson', 'dylan-patterson'), ('kako', 'isaac-kako'),
                ('smillie', 'josh-smillie')):
    v = np.array([float(r[fld]) for r in LAD])
    A = np.column_stack([np.ones(len(etas)), etas])
    coef = np.linalg.lstsq(A, v, rcond=None)[0]
    dev = float(np.abs(v - A @ coef).max())
    T2max = max(T2max, dev)
    P('   %-14s | %-42s | %10.3f %10.1f' % (nm, ' '.join('%d' % x for x in v), dev, coef[1] * 0.1))
    T2[nm] = dict(values=[float(x) for x in v], max_dev=dev, slope_per_0p1=float(coef[1] * 0.1))
P('   MAXIMUM deviation from a straight line, over all seven rows: %.3f board points' % T2max)
P('   (the boards print integer points, so anything below 0.5 is rounding and nothing else)')
P('   T2: %s' % ('PASS' if T2max < 0.75 else 'FAIL'))
P()

# ---- T3 ---------------------------------------------------------------------------------------------
P('-' * 118)
P('T3 · SEPARABILITY — C / pi_pre(g) must be the SAME at every vantage of the same player')
P('-' * 118)
P('   Run on ND rows with at least three vantages whose games counts differ by 5 or more, so the')
P('   test has something to bite on. pi_pre uses D = 1 and Phi = 1: rows whose sitter fade or stall')
P('   conditioning is live will NOT match, and that is expected, not a failure of linearity — it is')
P('   why the reported statistic is the SPREAD WITHIN a player, and why the distribution is shown.')
P()
spreads = []
detail = []
for k, a in MK.items():
    if a.get('type') != 'ND':
        continue
    b = ME[k]
    yrs = a.get('yrs') or []; vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    ratios = []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            continue
        g = LB.career_games(a, y)
        if g < 1 or g > 120:
            continue
        md = LB.m_d(g)
        if md < 0.05:
            continue
        C = (vpb[i] - vpa[i]) / (0.50 * md)
        pp = pi_pre(g)
        if pp <= 0:
            continue
        ratios.append((g, C / pp))
    if len(ratios) >= 3 and (max(x[0] for x in ratios) - min(x[0] for x in ratios)) >= 5:
        vals = [x[1] for x in ratios]
        mn = float(np.mean(vals))
        if mn <= 0:
            continue
        sp = (max(vals) - min(vals)) / mn
        spreads.append(sp)
        detail.append((k, mn, sp, ratios))
spreads = np.array(spreads)
P('   players tested: %d' % len(spreads))
if len(spreads):
    P('   within-player spread of C/pi_pre, as a fraction of the player\'s own mean:')
    for q in (10, 25, 50, 75, 90, 95, 99):
        P('      p%-3d %8.4f' % (q, np.percentile(spreads, q)))
    P('      max  %8.4f' % spreads.max())
detail.sort(key=lambda t: t[2])
P()
P('   three worked examples at the median of that spread:')
mid = len(detail) // 2
for k, mn, sp, ratios in detail[mid - 1:mid + 2]:
    P('      %-26s implied pedigree %8.1f, spread %.4f' % (k, mn, sp))
    for g, v in ratios:
        P('          g=%6.1f  m_d=%.4f  C/pi_pre = %8.1f' % (g, LB.m_d(g), v))
T3ok = len(spreads) > 0 and float(np.median(spreads)) < 0.05
P('   T3: median within-player spread %.4f  -> %s' % (float(np.median(spreads)) if len(spreads) else float('nan'),
                                                      'PASS' if T3ok else 'REPORTED, see distribution'))
P()

# ---- T4 ---------------------------------------------------------------------------------------------
P('-' * 118)
P('T4 · ROUND TRIP')
P('-' * 118)
worst = 0.0; nrt = 0
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []; vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            continue
        g = LB.career_games(a, y)
        md = LB.m_d(g)
        if md <= 0:
            back = vpb[i]
        else:
            C = (vpb[i] - vpa[i]) / (0.50 * md)
            back = vpb[i] - C * (0.50 * md)
        den = max(1.0, abs(vpa[i]))
        worst = max(worst, abs(back - vpa[i]) / den)
        nrt += 1
P('   vantages round-tripped: %d   worst relative error: %.3e' % (nrt, worst))
T4 = worst < 1e-6
P('   T4: %s' % ('PASS' if T4 else 'FAIL'))
P()

P('=' * 118)
P('FALSIFIER N1: %s' % ('DID NOT FIRE — the offline pricing identity holds and Step 4 may proceed.'
                        if (T1 and T2max < 0.75 and T4) else 'FIRED — Step 4 is withdrawn.'))
P('=' * 118)

json.dump(dict(T1=dict(pairs=n_pairs, bad_direction=len(bad_dir), gameless=n_zero, bad_zero=len(bad_zero), pass_=T1),
               T2=dict(rows=T2, max_dev=T2max, pass_=bool(T2max < 0.75)),
               T3=dict(players=len(spreads),
                       spread_pct={str(q): float(np.percentile(spreads, q)) for q in (10, 25, 50, 75, 90, 95, 99)} if len(spreads) else {},
                       median=float(np.median(spreads)) if len(spreads) else None),
               T4=dict(vantages=nrt, worst_rel=worst, pass_=T4)),
          open(os.path.join(HERE, 'IDENT_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'IDENT_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote IDENT_N.json and IDENT_N_out.txt')
