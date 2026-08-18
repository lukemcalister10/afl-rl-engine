#!/usr/bin/env python3
"""ORDER N — THE TRADE-OFF, PRICED. READ-ONLY. NO BOARD IS BUILT.

Two things this file settles.

(1) THE RETAINED-PRIOR DIAGNOSTIC. The order's requirement (c) says the charge should be monotone in
    evidence because a prior should decay as evidence accumulates, not recover. But the pedigree leg
    ALREADY decays on its own: pi(g) falls with games through rho and beta. So the right question is
    whether the RETAINED PRIOR pi_pre(g) * factor(g) is monotone, not whether the charge fraction is.
    This file measures both, on the engine's own published constants.

(2) THE LAMBDA LADDER. LAMBDA sets the level and THETA_R = BETA_sat/LAMBDA follows, so raising the
    level WEAKENS the tilt and lowering it strengthens the tilt. That is the trade-off, and it is
    walked here rather than asserted.

The band arithmetic is replicated from the pinned instrument's value_at() and CHECKED against
BANDS_N.json on two boards before any sweep number is printed.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_sweep.py
"""
import json, math, os, sys, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402
PL_F = 1.0524
L = []


def P(s=''):
    print(s); L.append(str(s))


M = json.load(open(os.path.join(HERE, 'MECH_N.json')))
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']
LAM_ANCHOR = M['LAMBDA']

# ---- the engine's published pedigree-leg constants ---------------------------------------------------
TAU_RHO, B_RHO = 29.194253560287144, 0.8015424473253033
BETA_ND = ((2.5, 0.2878886216033701), (10.5, 0.2878886216033701), (25.5, 0.21772876584106796),
           (53.0, 0.14155152291809878), (85.5, 0.023849021706229417))
KAP_K, GU_K = 0.20, 8.0


def loglin(pts, g):
    g = max(1e-9, float(g))
    if g <= pts[0][0]: return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]


def rho_base(g):
    return 0.0 if g <= 0 else 1.0 - math.exp(-((g / TAU_RHO) ** B_RHO))


def rho32(g):
    r = rho_base(g)
    return r if r <= 0 else r + KAP_K * ((g / GU_K) * math.exp(1.0 - g / GU_K)) * (1.0 - r)


def pi_pre(g):
    r = rho32(g)
    return (1.0 - r) + loglin(BETA_ND, g) * r


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def theta_r(lam):
    return BSAT / lam


def T_of(s, lam):
    tmax = 1.0 - theta_r(lam) * (S_P5 - S0)
    return min(max(1.0 - theta_r(lam) * (float(s) - S0), 0.0), tmax)


def F_new(g, s, lam):
    return 0.0 if g <= 0 else 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam))


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


P('=' * 118)
P('ORDER N — THE RETAINED-PRIOR DIAGNOSTIC AND THE LAMBDA LADDER. ESTIMATES PENDING A BUILD.')
P('=' * 118)
P()

# =====================================================================================================
P('-' * 118)
P('1 · IS THE RETAINED PRIOR ALREADY MONOTONE? — the question requirement (c) really asks')
P('-' * 118)
P('   pi_pre(g) is the pedigree-leg coefficient BEFORE any charge, on the engine\'s own constants at')
P('   D = 1 and Phi = 1. It already falls with games, because weight moves to the production leg.')
P('   The retained prior is pi_pre(g) x the charge factor. Both are printed.')
P()
P('   %-7s | %9s | %9s %11s | %9s %11s | %9s' % (
    'games', 'pi_pre', 'chg NOW', 'retained NOW', 'chg ORD N', 'retained N', 'A(g)'))
MONO = {}
prev_now = prev_new = None
bad_now = bad_new = 0
for g in list(range(0, 61)) + [70, 80, 100, 120, 141, 160, 200, 250, 300]:
    pp = pi_pre(g)
    rn = pp * (1.0 - F_old(g))
    rd = pp * (1.0 - F_new(g, S0, LAM_ANCHOR))
    if prev_now is not None and rn > prev_now + 1e-12:
        bad_now += 1
    if prev_new is not None and rd > prev_new + 1e-12:
        bad_new += 1
    prev_now, prev_new = rn, rd
    if g in (0, 1, 2, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50, 60, 80, 100, 141, 200, 300):
        P('   %-7d | %9.4f | %8.1f%% %11.4f | %8.1f%% %11.4f | %9.4f' % (
            g, pp, 100 * F_old(g), rn, 100 * F_new(g, S0, LAM_ANCHOR), rd, A_of(g)))
        MONO[g] = dict(pi_pre=pp, chg_now=F_old(g), ret_now=rn,
                       chg_new=F_new(g, S0, LAM_ANCHOR), ret_new=rd)
P()
P('   RISES IN THE RETAINED PRIOR as games increase, over g = 0..300 at the grid above:')
P('       CURRENT mechanism : %d rises  %s' % (bad_now, 'MONOTONE' if bad_now == 0 else '<- NOT MONOTONE'))
P('       ORDER N mechanism : %d rises  %s' % (bad_new, 'MONOTONE' if bad_new == 0 else '<- NOT MONOTONE'))
P()
P('   THIS IS THE ANSWER TO REQUIREMENT (c), AND IT IS NOT THE ONE THE ORDER ASSUMED.')
if bad_now == 0:
    P('   The retained prior under the CURRENT mechanism is already monotone. pi_pre falls fast enough')
    P('   that the bump in the charge never lets a high-games row hold MORE prior than a low-games row.')
    P('   The charge FRACTION is backwards; the prior it leaves behind is not.')
else:
    P('   The retained prior under the CURRENT mechanism is NOT monotone: it recovers as games rise.')
P()
P('   That does NOT make the current mechanism fine. It makes the complaint precise. A 36-game player')
P('   does not end up holding more prior than a 17-game player. What he does is pay a SMALLER SHARE of')
P('   it, at exactly the point where the evidence about him is strongest. That is the defect.')
P()

# =====================================================================================================
# 2 · the fast band instrument, checked against the committed one
# =====================================================================================================
BANDS_REF = json.load(open(os.path.join(HERE, 'BANDS_N.json')))
MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')

VAN = {}
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
        row.append(dict(g=g, s=LB.perf_surplus(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i])))
    VAN[k] = row

SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
ND = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
      and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
BANDS = [('ALL picks 1-64', lambda p: True), ('picks 1-20', lambda p: p <= 20),
         ('picks 21-64', lambda p: p >= 21), ('picks 1-10', lambda p: p <= 10),
         ('picks 11-20', lambda p: 11 <= p <= 20), ('picks 21-30', lambda p: 21 <= p <= 30),
         ('picks 31-40', lambda p: 31 <= p <= 40), ('picks 41-64', lambda p: 41 <= p <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]


def vp_new(r, lam):
    """the row's re-priced vpath under LAMBDA, or its ORDER K vpath when lam is None."""
    vp = list(r.get('vpath') or [])
    if lam is None:
        return vp
    van = VAN.get(r['key']) or []
    for i in range(len(vp)):
        if i >= len(van) or van[i] is None or vp[i] is None:
            continue
        v = van[i]
        if v['C'] <= 0 or v['s'] is None:
            continue
        vp[i] = round(v['v0eta'] - v['C'] * F_new(v['g'], v['s'], lam), 1)
    return vp


def apprec01(lam):
    """year-0 -> year-1 appreciation per band per window, on the pinned value_at semantics."""
    out = {}
    cache = {r['key']: vp_new(r, lam) for r in ND}
    for wname, lo, hi in WINDOWS:
        pop_w = [r for r in ND if lo <= r['year'] + 1 <= hi]
        for bname, bf in BANDS:
            pop = [r for r in pop_w if bf(int(r['pick']))]
            incl = [r for r in pop if r['year'] + 1 <= WEND]
            if len(incl) < 5:
                out['%s|%s' % (wname, bname)] = None; continue
            vals = []
            for r in incl:
                vp = cache[r['key']]
                if len(vp) < 1:
                    vals.append(0.0)
                else:
                    vals.append(0.0 if vp[0] is None else float(vp[0]))
            m1 = statistics.mean(vals); m0 = statistics.mean([float(r['v0']) for r in incl])
            out['%s|%s' % (wname, bname)] = m1 / m0 - 1.0
    return out


ref_k = apprec01(None)
ref_n = apprec01(LAM_ANCHOR)
P('-' * 118)
P('2 · THE FAST BAND INSTRUMENT, CHECKED AGAINST THE COMMITTED ONE BEFORE USE')
P('-' * 118)
worst = 0.0
for w, _, _ in WINDOWS:
    for bn, _ in BANDS:
        for tag, mine in (('OKRULED', ref_k), ('NDERIV', ref_n)):
            a = BANDS_REF['nd'][tag]['%s|ALLCOH|%s' % (w, bn)]['apprec01']
            if a is None or mine['%s|%s' % (w, bn)] is None:
                continue
            worst = max(worst, abs(a - mine['%s|%s' % (w, bn)]))
P('   worst disagreement with BANDS_N.json over 32 cells on two boards: %.2e' % worst)
P('   %s' % ('MATCHES — the fast instrument may be used for the ladder.' if worst < 1e-9
              else 'DOES NOT MATCH — the ladder is not reported.'))
P()
assert worst < 1e-9, 'fast band instrument does not reproduce the committed one'

# =====================================================================================================
# 3 · the ladder
# =====================================================================================================
LED = LB.load_ledger()
byk = {r['key']: r for r in LED['rows']}
MATK = [r for r in LED['rows'] if int(r['age']) >= 24]
BOARD_TOTAL = sum(float(r['landing']) for r in LED['rows'])
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako']


CURBASE = {}
for k, a in MK.items():
    ca, cb = a.get('cur'), ME[k].get('cur')
    if ca is None or cb is None:
        continue
    g = float(a.get('games_total') or 0.0)
    md = LB.m_d(g)
    CURBASE[k] = dict(g=g, s=LB.perf_surplus(a, 2026),
                      C=((float(cb) - float(ca)) / (0.50 * md)) if md > 1e-12 else 0.0,
                      v0eta=float(cb), vK=float(ca))


def board_points(lam):
    out = {}
    for k, d in CURBASE.items():
        if d['C'] <= 0 or d['s'] is None:
            out[k] = round(d['vK'] / PL_F)
        else:
            out[k] = round((d['v0eta'] - d['C'] * F_new(d['g'], d['s'], lam)) / PL_F)
    return out


def classmark(lam):
    """ok_class.py's cohort-clock mark over classes 2005-2015, recomputed on the re-priced vpath."""
    per = []
    for y in range(2005, 2016):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0):
                continue
            yrs = a.get('yrs') or []
            Y = c
            vp = vp_new(a, lam)
            if not yrs:
                v1 = 0.0
            elif Y < yrs[0]:
                continue
            elif Y > yrs[-1]:
                v1 = 0.0
            else:
                i = yrs.index(Y)
                v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(a['v0']); n += 1
        if den > 0 and n >= 5:
            per.append(num / den)
    return sum(per) / len(per)


P('-' * 118)
P('3 · THE LAMBDA LADDER — level against tilt. THETA_R = BETA_sat/LAMBDA, so they move opposite ways.')
P('-' * 118)
P('   %-7s %8s %9s | %8s %9s %9s | %8s %8s | %6s %6s %6s %6s %6s %6s' % (
    'LAMBDA', 'THETA_R', 'zero at s', 'coh mark', 'p1-10 PRI', 'p1-10 MOD', 'vet churn', 'vet net',
    'dean', 'cdt', 'xav', 'ann', 'pat', 'kako'))
LAD = []
for lam in (0.30, 0.45, 0.60, LAM_ANCHOR, 0.95, 1.20, 1.60, 2.20, 3.00):
    ap = apprec01(lam)
    bp = board_points(lam)
    mv = [(r['key'], bp.get(r['key'], r['landing']) - float(r['landing'])) for r in MATK]
    mv = [(k, d) for k, d in mv if d != 0]
    churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    cm = classmark(lam)
    row = dict(lam=lam, theta_r=theta_r(lam), zero_at=S0 + 1.0 / theta_r(lam),
               cohort_mark=cm, p110_pri=ap['PRIMARY|picks 1-10'], p110_mod=ap['MODERN|picks 1-10'],
               all_pri=ap['PRIMARY|ALL picks 1-64'], all_mod=ap['MODERN|ALL picks 1-64'],
               vet_churn=churn, vet_net=net,
               named={k: bp.get(k) for k in NAMED})
    LAD.append(row)
    tag = ' <- anchoring solve' if abs(lam - LAM_ANCHOR) < 1e-9 else ''
    P('   %-7.3f %8.5f %+9.2f | %8.4f %+8.2f%% %+8.2f%% | %8.0f %+8.0f | %6d %6d %6d %6d %6d %6d%s' % (
        lam, theta_r(lam), S0 + 1.0 / theta_r(lam), cm, 100 * row['p110_pri'], 100 * row['p110_mod'],
        churn, net, *[bp.get(k, 0) for k in NAMED], tag))
P()
P('   rails for the last four column groups: cohort mark under ~1.05 keeps the W2 basis under 1.14;')
P('   picks 1-10 must stay under +14.00%% in BOTH windows; veteran churn <= %.0f and |net| <= %.0f.'
  % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
P('   ORDER K reads: cohort mark 1.0324, picks 1-10 +8.22%% / +13.65%%, vet churn 947, vet net -601,')
P('   dean 2403, cdt 1505, xavier 1162, annable 1537, patterson 1440, kako 832.')
P()

json.dump(dict(monotone=MONO, mono_rises=dict(now=bad_now, order_n=bad_new),
               ladder=LAD, band_check=worst,
               rails=dict(churn=0.0015 * BOARD_TOTAL, net=0.0010 * BOARD_TOTAL)),
          open(os.path.join(HERE, 'SWEEP_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'SWEEP_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote SWEEP_N.json / SWEEP_N_out.txt')
