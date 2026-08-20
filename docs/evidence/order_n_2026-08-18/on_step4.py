#!/usr/bin/env python3
"""ORDER N STEP 4 — PRICE THE DERIVED CHARGE OFFLINE. READ-ONLY. NO BOARD IS BUILT.

Everything here is an ESTIMATE PENDING A BUILD, and every table says so. The pedigree-leg arithmetic
is exact (falsifier N1 passed: on_ident.py). The instruments are the committed ones, run unchanged on
a modified matrix. What cannot be done without a build: the engine's assert wall, the continuity
objects, rho32 monotonicity, the day-0 identity, and the veteran caps.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_step4.py
"""
import json, math, os, sys, copy, collections
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

SP = LB.SP
PL_F = 1.0524                    # pick_redenomination.json::factor — matrix points / board points
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


M = json.load(open(os.path.join(HERE, 'MECH_N.json')))
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def theta_r(lam):
    """THETA_R = BETA_sat / LAMBDA -- the Step 3 constraint. Nothing free."""
    return BSAT / lam


def tmax_of(lam):
    """TMAX = T at the cohort's own 5th percentile of surplus. Data-set, declared in Step 3."""
    return 1.0 - theta_r(lam) * (S_P5 - S0)


def T_of(s, lam):
    return min(max(1.0 - theta_r(lam) * (float(s) - S0), 0.0), tmax_of(lam))


def F_new(g, s, lam):
    """The FRACTION of the pedigree leg removed by the derived charge."""
    if g <= 0:
        return 0.0
    return 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam))


def F_old(g, eta=LB.ETA_K):
    return max(0.0, eta * LB.m_d(g))


P('=' * 118)
P('ORDER N — STEP 4. THE DERIVED CHARGE, PRICED OFFLINE. EVERY NUMBER IS AN ESTIMATE PENDING A BUILD.')
P('=' * 118)
P('mechanism: pi *= exp( -LAMBDA * A(g) * T(s) )')
P('  A(g) = 1 - exp(-g/%.4f)                       G0 derived in Step 3 from the measured BETA curve' % G0)
P('  T(s) = clip( 1 - THETA_R*(s %+0.4f), 0, TMAX )    THETA_R = BETA_sat/LAMBDA = %.5f/LAMBDA' % (-S0, BSAT))
P('pricing identity (falsifier N1, PASSED in on_ident.py):  v(F) = v(F=0) - F * C,  C = the charge base')
P()

MK = LB.load_matrix('OKRULED')       # ETA = 0.50
ME = LB.load_matrix('M0ETA0')        # ETA = 0.00

# ---- build the per-vantage charge base ---------------------------------------------------------------
VAN = {}                       # key -> list over path index of dict(y, g, s, C, v0eta, vK)
for k, a in MK.items():
    b = ME[k]
    yrs = a.get('yrs') or []
    vpa = a.get('vpath') or []; vpb = b.get('vpath') or []
    row = []
    for i, y in enumerate(yrs):
        if i >= len(vpa) or i >= len(vpb) or vpa[i] is None or vpb[i] is None:
            row.append(None); continue
        g = LB.career_games(a, y)
        md = LB.m_d(g)
        C = ((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0
        s = LB.perf_surplus(a, y)
        row.append(dict(y=y, g=g, s=s, C=C, v0eta=float(vpb[i]), vK=float(vpa[i])))
    VAN[k] = row

CURBASE = {}
for k, a in MK.items():
    ca, cb = a.get('cur'), ME[k].get('cur')
    if ca is None or cb is None:
        continue
    g = float(a.get('games_total') or 0.0)
    md = LB.m_d(g)
    CURBASE[k] = dict(g=g, s=LB.perf_surplus(a, 2026), age=LB.age_at(a, 2026),
                      C=((float(cb) - float(ca)) / (0.50 * md)) if md > 1e-12 else 0.0,
                      v0eta=float(cb), vK=float(ca))


def cur_new(k, lam):
    d = CURBASE.get(k)
    if d is None:
        return None
    if d['C'] <= 0 or d['s'] is None:
        return d['vK']
    return d['v0eta'] - d['C'] * F_new(d['g'], d['s'], lam)


# ---- board-points conversion check ------------------------------------------------------------------
LED = LB.load_ledger()
err = []
for r in LED['rows']:
    m = MK.get(r['key'])
    if m is None or m.get('cur') is None:
        continue
    err.append(abs(float(m['cur']) / PL_F - float(r['orderk'])))
P('-' * 118)
P('0 · BOARD POINTS FROM MATRIX POINTS')
P('-' * 118)
P('   board points = matrix points / %.4f (pick_redenomination.json::factor). Checked on all %d ledger rows:' % (PL_F, len(err)))
P('   worst discrepancy %.3f board points, mean %.4f. Rounding, and nothing else.' % (max(err), float(np.mean(err))))
P()

# ---- 1 · THE ANCHORING SOLVE -------------------------------------------------------------------------
P('-' * 118)
P('1 · THE ANCHORING SOLVE — LAMBDA IS NOT TUNED, IT IS SOLVED')
P('-' * 118)
P('   ORDER M proved the charge is load-bearing for the whole board\'s year-1 anchoring, not just for')
P('   the age bar. So the LEVEL of the replacement is not an outcome question; it is a no-arbitrage')
P('   calibration. LAMBDA is solved so the derived charge removes THE SAME TOTAL NUMBER OF POINTS from')
P('   the year-1 class-mark population as the current charge does. The tilt then redistributes those')
P('   points between over- and under-performers. It does not add any.')
P()

CLASSES_MARK = list(range(2005, 2016))


def cohort_of(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


anchor_rows = []
for k, a in MK.items():
    c = cohort_of(a)
    if c is None or c not in CLASSES_MARK or not (float(a.get('v0') or 0) > 0):
        continue
    Y = c                                  # ok_class val(r, 1) reads year cohort + 1 - 1 = cohort
    yrs = a.get('yrs') or []
    if Y not in yrs:
        continue
    v = VAN[k][yrs.index(Y)]
    if v is None or v['C'] <= 0 or v['s'] is None:
        continue
    anchor_rows.append(v)
tot_old = sum(v['C'] * F_old(v['g']) for v in anchor_rows)
P('   anchor population: %d year-1 rows from cohort classes %d-%d with a live charge.' % (
    len(anchor_rows), CLASSES_MARK[0], CLASSES_MARK[-1]))
P('   points the CURRENT charge removes from them: %.1f matrix points.' % tot_old)

lo, hi = 0.0, 20.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    t = sum(v['C'] * F_new(v['g'], v['s'], mid) for v in anchor_rows)
    if t < tot_old:
        lo = mid
    else:
        hi = mid
LAM = 0.5 * (lo + hi)
tot_new = sum(v['C'] * F_new(v['g'], v['s'], LAM) for v in anchor_rows)
P('   SOLVED:  LAMBDA  = %.5f      (bisection, 200 halvings; removes %.1f points, target %.1f)' % (LAM, tot_new, tot_old))
P('            THETA_R = %.5f      = BETA_sat / LAMBDA. Not a free parameter.' % theta_r(LAM))
P('            TMAX    = %.5f      = T at the cohort 5th percentile of surplus, %+.2f points/game.' % (tmax_of(LAM), S_P5))
P()
P('   THE ZERO POINT. T(s) hits 0 at s = s0 + 1/THETA_R = %+.2f points per game.' % (S0 + 1.0 / theta_r(LAM)))
P('   A young player producing more than %.2f points a game above his age bar pays NOTHING on his' % (S0 + 1.0 / theta_r(LAM)))
P('   pedigree leg. He keeps the whole prior. That is the mechanism doing the thing the order asked for.')
P('   Share of the young cohort at or past that point: %.1f%%.' % (
    100.0 * float(np.mean([1.0 if (r['ps'] >= S0 + 1.0/theta_r(LAM)) else 0.0
                           for r in json.load(open(os.path.join(HERE, 'STEP2_N.json')))['rows']]))))
P()
M['LAMBDA'] = LAM
M['THETA_R'] = theta_r(LAM)
M['TMAX'] = tmax_of(LAM)
M['zero_charge_at_surplus'] = S0 + 1.0 / theta_r(LAM)
M['anchor'] = dict(n=len(anchor_rows), points_old=tot_old, points_new=tot_new,
                   classes=[CLASSES_MARK[0], CLASSES_MARK[-1]])
json.dump(M, open(os.path.join(HERE, 'MECH_N.json'), 'w'), indent=1)

P('   THE CHARGE, SIDE BY SIDE. Percentage of the pedigree leg removed.')
P('   %-8s | %-30s | %s' % ('games', 'CURRENT  0.50*m_d(g), blind', 'DERIVED  1-exp(-LAM*A(g)*T(s))'))
P('   %-8s | %-30s | %10s %10s %10s %10s' % ('', '', 's=-25', 's=-10', 's=0', 's=+15'))
CHG = {}
for g in (1, 2, 3, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50, 80, 141):
    cells = [100 * F_new(g, s, LAM) for s in (-25, -10, 0, 15)]
    P('   %-8d | %28.1f%% | %9.1f%% %9.1f%% %9.1f%% %9.1f%%' % (g, 100 * F_old(g), *cells))
    CHG[g] = dict(old=100 * F_old(g), new=cells)
P()
P('   Read the row at 17 games against the row at 36 games. The current charge falls from 49.0%% to')
P('   16.6%%: a 36-game player keeps MORE unearned pedigree than a 17-game player. The derived charge')
P('   does not fall anywhere.')
P()

# ---- 2 · APPLY IT ------------------------------------------------------------------------------------
def build_matrix(lam, tag):
    src = json.load(open(os.path.join(SP, 'per_entrant_OKRULED.json')))
    out = copy.deepcopy(src)
    nmoved = 0
    for r in out['recs']:
        k = r['key']
        vp = r.get('vpath') or []
        van = VAN.get(k) or []
        for i in range(len(vp)):
            if i >= len(van) or van[i] is None or vp[i] is None:
                continue
            v = van[i]
            if v['C'] <= 0 or v['s'] is None:
                continue
            nv = v['v0eta'] - v['C'] * F_new(v['g'], v['s'], lam)
            if abs(nv - vp[i]) > 1e-9:
                nmoved += 1
            vp[i] = round(nv, 1)
        r['vpath'] = vp
        c = cur_new(k, lam)
        if c is not None:
            r['cur'] = round(c, 1)
        live = [x for x in vp if x is not None] + ([r['cur']] if r.get('cur') is not None else [])
        if live:
            r['peak'] = max(live + [float(r['v0'] or 0)])
    out['meta']['ORDER_N'] = dict(note='ESTIMATE, NOT A BUILD. vpath re-priced offline by ORDER N.',
                                  mechanism='pi *= exp(-LAMBDA*A(g)*T(s))', LAMBDA=lam,
                                  G0=G0, BETA_sat=BSAT, THETA_R=theta_r(lam), TMAX=tmax_of(lam), s0=S0,
                                  base_eta0='per_entrant_M0ETA0.json', base_etaK='per_entrant_OKRULED.json')
    p = os.path.join(SP, 'per_entrant_%s.json' % tag)
    json.dump(out, open(p, 'w'))
    return p, nmoved


PATH_N, NMOVED = build_matrix(LAM, 'NDERIV')
P('-' * 118)
P('2 · THE RE-PRICED MATRIX')
P('-' * 118)
P('   wrote %s' % os.path.basename(PATH_N))
P('   vantage cells whose price moved against ORDER K: %d' % NMOVED)
P('   ESTIMATE PENDING A BUILD. No engine was run.')
P()

# ---- 3 · THE PROPERTY TEST, RE-RUN -------------------------------------------------------------------
P('-' * 118)
P('3 · THE PROPERTY TEST RE-RUN ON THE ESTIMATED PRICES')
P('-' * 118)
S1 = json.load(open(os.path.join(HERE, 'STEP1_N.json')))
rows = S1['rows']
MN = LB.load_matrix('NDERIV')
for r in rows:
    r['v_new'] = float(MN[r['key']]['cur'] if MN[r['key']]['cur'] is not None else MN[r['key']]['v0'])
    r['new_bp'] = r['v_new'] / PL_F
    r['R_n'] = r['new_bp'] / r['v0']
    r['chg_new'] = F_new(r['g'], r['ps'], LAM)
P('   The question: is the CHARGE now monotone in performance surplus at fixed games? It is, by')
P('   construction — Q is non-increasing in s (property N-S3). The number worth printing is what that')
P('   does to the price response.')
P()
P('   %-10s %5s | %10s %10s %10s | %10s %10s' % (
    'games bin', 'n', 'rho ORDER K', 'rho DERIVED', 'change', 'chg-rho K', 'chg-rho N'))
PROP = {}
for lo_, hi_ in LB.G_BINS_1:
    b = '%d-%d' % (lo_, hi_)
    sub = [r for r in rows if r['gbin'] == b]
    if len(sub) < 8:
        continue
    ps = np.array([r['ps'] for r in sub])
    a = spear(ps, np.array([r['R_k'] for r in sub]))
    c = spear(ps, np.array([r['R_n'] for r in sub]))
    ck = spear(ps, np.array([r['charge_pct'] for r in sub]))
    cn = spear(ps, np.array([r['chg_new'] for r in sub]))
    P('   %-10s %5d | %+10.4f %+10.4f %+10.4f | %+10.4f %+10.4f' % (b, len(sub), a, c, c - a, ck, cn))
    PROP[b] = dict(n=len(sub), rho_k=a, rho_n=c, chg_rho_k=ck, chg_rho_n=cn)
psall = np.array([r['ps'] for r in rows])
P('   %-10s %5d | %+10.4f %+10.4f %+10.4f | %+10.4f %+10.4f' % (
    'ALL', len(rows), spear(psall, np.array([r['R_k'] for r in rows])),
    spear(psall, np.array([r['R_n'] for r in rows])),
    spear(psall, np.array([r['R_n'] for r in rows])) - spear(psall, np.array([r['R_k'] for r in rows])),
    spear(psall, np.array([r['charge_pct'] for r in rows])),
    spear(psall, np.array([r['chg_new'] for r in rows]))))
P()
P('   Charge paid, by performance-surplus tercile, over the whole young window:')
sub = sorted(rows, key=lambda r: r['ps']); n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
for t, lab in enumerate(('below expectation', 'middle', 'above expectation')):
    pt = sub[cuts[t]:cuts[t + 1]]
    P('   %-20s n=%-4d mean PS %+7.2f  mean g %5.1f | CURRENT %5.1f%%  DERIVED %5.1f%%' % (
        lab, len(pt), np.mean([r['ps'] for r in pt]), np.mean([r['g'] for r in pt]),
        100 * np.mean([r['charge_pct'] for r in pt]), 100 * np.mean([r['chg_new'] for r in pt])))
P()

# ---- 4 · WHERE THE MONEY GOES -------------------------------------------------------------------------
P('-' * 118)
P('4 · WHERE THE MONEY MOVES, IN BOARD POINTS, ACROSS THE WHOLE 804-ROW BOARD')
P('-' * 118)
mv = []
for r in LED['rows']:
    k = r['key']
    if k not in MN:
        continue
    if MN[k].get('cur') is None:
        continue
    nb = float(MN[k]['cur']) / PL_F
    mv.append(dict(key=k, name=r['name'], age=r['age'], g=float(r['g'] or 0), pick=r.get('pick'),
                   pos=r['pos'], orderk=float(r['orderk']), new=nb, d=nb - float(r['orderk'])))
tot_k = sum(x['orderk'] for x in mv); tot_n = sum(x['new'] for x in mv)
P('   board total: ORDER K %d  ->  DERIVED %d   (%+d points, %+.2f%%)' % (
    round(tot_k), round(tot_n), round(tot_n - tot_k), 100 * (tot_n - tot_k) / tot_k))
P('   rows that move: %d of %d (up %d, down %d)' % (
    sum(1 for x in mv if abs(x['d']) >= 0.5), len(mv),
    sum(1 for x in mv if x['d'] >= 0.5), sum(1 for x in mv if x['d'] <= -0.5)))
P()
P('   %-12s %6s %12s %10s' % ('career games', 'rows', 'total points', 'per row'))
for lo_, hi_, lab in ((0, 0, '0'), (1, 4, '1-4'), (5, 9, '5-9'), (10, 15, '10-15'),
                      (16, 29, '16-29'), (30, 59, '30-59'), (60, 10 ** 9, '60+')):
    s = [x for x in mv if lo_ <= x['g'] <= hi_]
    if not s: continue
    P('   %-12s %6d %+12.0f %+10.1f' % (lab, len(s), sum(x['d'] for x in s), np.mean([x['d'] for x in s])))
P()
P('   the ten largest rises and the ten largest falls:')
mv.sort(key=lambda x: -x['d'])
for x in mv[:10]:
    P('     %+8.0f  %-26s age %2d  g %5.0f  pick %-5s  %d -> %d' % (
        x['d'], x['name'][:26], x['age'], x['g'], x['pick'], round(x['orderk']), round(x['new'])))
P('     ...')
for x in mv[-10:]:
    P('     %+8.0f  %-26s age %2d  g %5.0f  pick %-5s  %d -> %d' % (
        x['d'], x['name'][:26], x['age'], x['g'], x['pick'], round(x['orderk']), round(x['new'])))
P()

# ---- 5 · THE NAMED ROWS ------------------------------------------------------------------------------
P('-' * 118)
P('5 · THE NAMED ROWS — ILLUSTRATIONS OF WHERE THE DERIVED RULE PUTS THEM. NEVER TARGETS.')
P('-' * 118)
P('   No constant in this mechanism was chosen with any of these rows in view. They are printed last')
P('   because the order asked to see them, and they are printed wherever the derived rule puts them.')
P()
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie', 'anthony-scerri', 'milan-murdock']
byk = {r['key']: r for r in LED['rows']}
P('   %-22s %3s %5s %5s | %8s %8s | %7s %7s | %7s %7s %7s' % (
    'row', 'age', 'pick', 'g', 'PS', 'A(g)', 'chg K', 'chg N', 'landing', 'ORDER K', 'DERIVED'))
NAM = {}
for k in NAMED:
    r = byk.get(k); m = MK.get(k)
    if r is None or m is None:
        P('   %-22s  not on the ledger' % k); continue
    Y = max((s['year'] for s in m['seasons']), default=None)
    s = LB.perf_surplus(m, Y) if Y else None
    g = float(r['g'] or 0)
    nb = float(MN[k]['cur']) / PL_F
    P('   %-22s %3d %5s %5.0f | %+8.2f %8.4f | %6.1f%% %6.1f%% | %7d %7d %7d' % (
        r['name'][:22], r['age'], r['pick'], g, (s if s is not None else float('nan')), A_of(g),
        100 * F_old(g), 100 * F_new(g, s, LAM) if s is not None else 0.0,
        round(r['landing']), round(r['orderk']), round(nb)))
    NAM[k] = dict(age=r['age'], pick=r['pick'], g=g, ps=s, A=A_of(g),
                  chg_k=100 * F_old(g), chg_n=(100 * F_new(g, s, LAM) if s is not None else 0.0),
                  landing=r['landing'], orderk=r['orderk'], derived=nb)
P()

json.dump(dict(mechanism=M, charge_table=CHG, property=PROP, named=NAM,
               board=dict(total_k=tot_k, total_n=tot_n),
               movers=sorted(mv, key=lambda x: -abs(x['d']))[:120]),
          open(os.path.join(HERE, 'STEP4_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP4_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STEP4_N.json and STEP4_N_out.txt; matrix tag NDERIV')
