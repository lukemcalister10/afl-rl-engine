#!/usr/bin/env python3
"""ORDER N — VARIANT C: THE SAME DERIVED CHARGE WITH A FLOOR UNDER THE RELIEF. READ-ONLY.

on_variant.py found the conflict: the band rail on picks 1-10 needs LAMBDA at or above 1.80, the G1
class floor allows at most 1.20, and there is nothing in between. The reason is one specific thing —
at the derived tilt a young row far enough above his age bar pays NOTHING, and top-of-draft rows have
the largest pedigree legs on the board, so the modern picks 1-10 band goes straight through the rail.

Variant C changes exactly one thing. The relief is floored:

    T(s) = clip( 1 - THETA_R*(s - s0), TMIN, TMAX )        TMIN >= 0

TMIN is the ONE number this file solves for, and it is solved against a rail, not chosen: the
smallest floor that holds picks 1-10 under +14% in BOTH windows at the anchoring LAMBDA. Everything
else — G0, BETA_sat, THETA_R, s0, TMAX, the age gate, the anchoring identity — is unchanged.

The cost is stated plainly rather than buried: a floor means an over-performing young player pays
SOMETHING rather than nothing, so he is charged less than an under-performer but not zero.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_floor.py
"""
import json, math, os, sys, copy, statistics
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402
PL_F = 1.0524
AGE_GATE = 24
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
    return BSAT / lam


def T_of(s, lam, tmin):
    tmax = 1.0 - theta_r(lam) * (S_P5 - S0)
    return min(max(1.0 - theta_r(lam) * (float(s) - S0), tmin), tmax)


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_var(g, s, age, lam, tmin):
    if g <= 0:
        return 0.0
    if age is None or age >= AGE_GATE or s is None:
        return F_old(g)
    return 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam, tmin))


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
        g = LB.career_games(a, y); md = LB.m_d(g)
        row.append(dict(y=y, g=g, s=LB.perf_surplus(a, y), age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i])))
    VAN[k] = row
CURBASE = {}
for k, a in MK.items():
    ca, cb = a.get('cur'), ME[k].get('cur')
    if ca is None or cb is None:
        continue
    g = float(a.get('games_total') or 0.0); md = LB.m_d(g)
    CURBASE[k] = dict(g=g, s=LB.perf_surplus(a, 2026), age=LB.age_at(a, 2026),
                      C=((float(cb) - float(ca)) / (0.50 * md)) if md > 1e-12 else 0.0,
                      v0eta=float(cb), vK=float(ca))


def vp_new(r, lam, tmin):
    vp = list(r.get('vpath') or [])
    van = VAN.get(r['key']) or []
    for i in range(len(vp)):
        if i >= len(van) or van[i] is None or vp[i] is None:
            continue
        v = van[i]
        if v['C'] <= 0:
            continue
        vp[i] = round(v['v0eta'] - v['C'] * F_var(v['g'], v['s'], v['age'], lam, tmin), 1)
    return vp


def board_points(lam, tmin):
    out = {}
    for k, d in CURBASE.items():
        if d['C'] <= 0:
            out[k] = round(d['vK'] / PL_F)
        else:
            out[k] = round((d['v0eta'] - d['C'] * F_var(d['g'], d['s'], d['age'], lam, tmin)) / PL_F)
    return out


SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
ND = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
      and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
BANDS = [('ALL picks 1-64', lambda p: True), ('picks 1-20', lambda p: p <= 20),
         ('picks 21-64', lambda p: p >= 21), ('picks 1-10', lambda p: p <= 10),
         ('picks 11-20', lambda p: 11 <= p <= 20), ('picks 21-30', lambda p: 21 <= p <= 30),
         ('picks 31-40', lambda p: 31 <= p <= 40), ('picks 41-64', lambda p: 41 <= p <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]


def apprec01(lam, tmin):
    out = {}
    cache = {r['key']: vp_new(r, lam, tmin) for r in ND}
    for wname, lo_, hi_ in WINDOWS:
        pop_w = [r for r in ND if lo_ <= r['year'] + 1 <= hi_]
        for bname, bf in BANDS:
            incl = [r for r in pop_w if bf(int(r['pick'])) and r['year'] + 1 <= WEND]
            if len(incl) < 5:
                out['%s|%s' % (wname, bname)] = None; continue
            vals = [(0.0 if (not cache[r['key']] or cache[r['key']][0] is None) else float(cache[r['key']][0]))
                    for r in incl]
            out['%s|%s' % (wname, bname)] = statistics.mean(vals) / statistics.mean(
                [float(r['v0']) for r in incl]) - 1.0
    return out


def classmark(lam, tmin, lo_y=2005, hi_y=2015):
    per = []
    for y in range(lo_y, hi_y + 1):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0):
                continue
            yrs = a.get('yrs') or []
            vp = vp_new(a, lam, tmin)
            if not yrs:
                v1 = 0.0
            elif y < yrs[0]:
                continue
            elif y > yrs[-1]:
                v1 = 0.0
            else:
                i = yrs.index(y)
                v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(a['v0']); n += 1
        if den > 0 and n >= 5:
            per.append(num / den)
    return sum(per) / len(per)


P('=' * 118)
P('ORDER N — VARIANT C. THE DERIVED CHARGE WITH A FLOOR UNDER THE RELIEF. ESTIMATES PENDING A BUILD.')
P('=' * 118)
P()
LAM = M['variantB']['LAMBDA_anchor']
P('   LAMBDA is held at the anchoring solve, %.5f, and THETA_R at %.5f. The only new number is TMIN.' % (
    LAM, theta_r(LAM)))
P('   TMIN = 0 IS variant B. TMIN = 1 would switch the tilt off above the centre entirely.')
P()

LED = LB.load_ledger()
MAT = [r for r in LED['rows'] if int(r['age']) >= 24]
BOARD_TOTAL = sum(float(r['landing']) for r in LED['rows'])
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako']
P('-' * 118)
P('THE TMIN LADDER, at LAMBDA = %.5f' % LAM)
P('-' * 118)
P('   %-6s | %8s %8s %9s %9s %9s %9s | %7s %7s | %6s %6s %6s %6s %6s %6s' % (
    'TMIN', 'coh mark', 'W2 mark', 'p1-10 PRI', 'p1-10 MOD', 'ALL PRI', 'ALL MOD',
    'vetchurn', 'vet net', 'dean', 'cdt', 'xav', 'ann', 'pat', 'kako'))
LADC = []
for tmin in [round(x, 3) for x in np.arange(0.0, 1.001, 0.05)]:
    ap = apprec01(LAM, tmin); bp = board_points(LAM, tmin)
    mv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
    mv = [(k, d) for k, d in mv if d != 0]
    churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    row = dict(tmin=tmin, coh=classmark(LAM, tmin), w2=classmark(LAM, tmin, 2006, 2016),
               p110_pri=ap['PRIMARY|picks 1-10'], p110_mod=ap['MODERN|picks 1-10'],
               all_pri=ap['PRIMARY|ALL picks 1-64'], all_mod=ap['MODERN|ALL picks 1-64'],
               churn=churn, net=net, named={k: bp.get(k) for k in NAMED}, bands=ap)
    LADC.append(row)
    P('   %-6.2f | %8.4f %8.4f %+8.2f%% %+8.2f%% %+8.2f%% %+8.2f%% | %7.0f %+7.0f | %6d %6d %6d %6d %6d %6d' % (
        tmin, row['coh'], row['w2'], 100 * row['p110_pri'], 100 * row['p110_mod'],
        100 * row['all_pri'], 100 * row['all_mod'], churn, net, *[bp.get(k, 0) for k in NAMED]))
P()
ok = [r for r in LADC if r['p110_pri'] < 0.14 and r['p110_mod'] < 0.14 and r['w2'] >= 1.03
      and r['churn'] <= 0.0015 * BOARD_TOTAL and abs(r['net']) <= 0.0010 * BOARD_TOTAL]
P('   RAILS: picks 1-10 under +14%% in BOTH windows · W2 mark >= 1.03 · veteran churn <= %.0f · |net| <= %.0f'
  % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
P('   Rungs clearing all four: %d of %d.' % (len(ok), len(LADC)))
BEST = None
if ok:
    BEST = min(ok, key=lambda r: r['tmin'])
    P('   The SMALLEST floor that clears them is TMIN = %.2f. Smallest is best: a smaller floor means'
      % BEST['tmin'])
    P('   more relief for the young player who is ahead of his age bar. It is a frontier point.')
else:
    P('   *** NO FLOOR CLEARS ALL FOUR. The conflict survives variant C. ***')
P()

if BEST is not None:
    tmin = BEST['tmin']
    P('-' * 118)
    P('THE FRONTIER POINT IN FULL — LAMBDA %.5f, THETA_R %.5f, TMIN %.2f, age gate 24' % (LAM, theta_r(LAM), tmin))
    P('-' * 118)
    P('   THE CHARGE, PER CENT OF THE PEDIGREE LEG REMOVED:')
    P('   %-8s | %-14s | %10s %10s %10s %10s %10s' % (
        'games', 'CURRENT blind', 's=-25', 's=-10', 's=0', 's=+10', 's=+20'))
    for g in (1, 2, 3, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50):
        P('   %-8d | %13.1f%% | %9.1f%% %9.1f%% %9.1f%% %9.1f%% %9.1f%%' % (
            g, 100 * F_old(g), *[100 * F_var(g, s, 19, LAM, tmin) for s in (-25, -10, 0, 10, 20)]))
    P()
    ap = apprec01(LAM, tmin); bp = board_points(LAM, tmin)
    BREF = json.load(open(os.path.join(HERE, 'BANDS_N.json')))
    P('   BAND TABLES, BOTH WINDOWS.  B = over the +14%% buy rail.  S = below 0%%.')
    P('   %-16s | %-24s | %-24s' % ('band', 'PRIMARY   N  /  ORDER K', 'MODERN    N  /  ORDER K'))
    for bname, _ in BANDS:
        cells = []
        for w in ('PRIMARY', 'MODERN'):
            a = ap['%s|%s' % (w, bname)]
            kk = BREF['nd']['OKRULED']['%s|ALLCOH|%s' % (w, bname)]['apprec01']
            cells.append('%+8.2f%%%s / %+8.2f%%%s' % (100 * a, 'B' if a > 0.14 else ('S' if a < 0 else ' '),
                                                      100 * kk, 'B' if kk > 0.14 else ('S' if kk < 0 else ' ')))
        P('   %-16s | %-24s | %-24s' % (bname, cells[0], cells[1]))
    P()
    P('   class mark  cohort 2005-2015 %.4f (ORDER K 1.0324) · W2 draft 2005-2015 %.4f (ORDER K 1.0513, floor 1.03, rail 1.14)'
      % (classmark(LAM, tmin), classmark(LAM, tmin, 2006, 2016)))
    mv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
    mv = [(k, d) for k, d in mv if d != 0]
    P('   veteran pool %d move · churn %.0f (rail %.0f) · net %+.0f (rail %.0f) · INSIDE BOTH'
      % (len(mv), sum(abs(d) for _, d in mv), 0.0015 * BOARD_TOTAL, sum(d for _, d in mv), 0.0010 * BOARD_TOTAL))
    tot_k = sum(float(r['orderk']) for r in LED['rows'])
    tot_n = sum(bp.get(r['key'], float(r['orderk'])) for r in LED['rows'])
    P('   board total %d -> %d  (%+d, %+.2f%%)' % (round(tot_k), round(tot_n), round(tot_n - tot_k),
                                                   100 * (tot_n - tot_k) / tot_k))
    P()
    S1 = json.load(open(os.path.join(HERE, 'STEP1_N.json')))
    rows = S1['rows']
    P('   THE PROPERTY TEST. Spearman against performance surplus, within games bins.')
    P('   %-10s %5s | %13s %13s | %11s %11s' % ('games bin', 'n', 'rho price K', 'rho price N',
                                                'rho chg K', 'rho chg N'))
    for lo_, hi_ in LB.G_BINS_1:
        b = '%d-%d' % (lo_, hi_)
        sub = [r for r in rows if r['gbin'] == b]
        if len(sub) < 8:
            continue
        ps = np.array([r['ps'] for r in sub])
        P('   %-10s %5d | %+13.4f %+13.4f | %+11.4f %+11.4f' % (
            b, len(sub), spear(ps, np.array([r['R_k'] for r in sub])),
            spear(ps, np.array([bp.get(r['key'], r['orderk']) / r['v0'] for r in sub])),
            spear(ps, np.array([r['charge_pct'] for r in sub])),
            spear(ps, np.array([F_var(r['g'], r['ps'], r['age'], LAM, tmin) for r in sub]))))
    P()
    P('   THE NAMED ROWS — ILLUSTRATIONS OF WHERE THE DERIVED RULE PUTS THEM. NEVER TARGETS.')
    byk = {r['key']: r for r in LED['rows']}
    P('   %-22s %3s %5s %5s %9s | %7s %7s %7s %7s | %8s' % (
        'row', 'age', 'pick', 'g', 'surplus', 'landing', 'ORD K', 'eta=0', 'ORD N', 'chg N'))
    ME_ = LB.load_matrix('M0ETA0')
    for k in NAMED + ['josh-smillie', 'milan-murdock']:
        r = byk.get(k)
        if r is None:
            P('   %-22s  not on the 804-row board' % k); continue
        a = MK[k]
        Y = max((s['year'] for s in a['seasons']), default=None)
        s = LB.perf_surplus(a, Y) if Y else None
        e0 = round(float(ME_[k]['cur']) / PL_F) if ME_[k].get('cur') else None
        P('   %-22s %3d %5s %5.0f %9s | %7d %7d %7s %7d | %7.1f%%' % (
            r['name'][:22], r['age'], r['pick'], float(r['g'] or 0),
            ('%+.2f' % s) if s is not None else 'n/a', round(r['landing']), round(r['orderk']),
            ('%d' % e0) if e0 is not None else '-', bp.get(k, round(r['orderk'])),
            100 * F_var(float(r['g'] or 0), s, int(r['age']), LAM, tmin)))
    P()
    out = copy.deepcopy(json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json'))))
    for r in out['recs']:
        r['vpath'] = vp_new(r, LAM, tmin)
        d = CURBASE.get(r['key'])
        if d is not None:
            r['cur'] = round(d['vK'] if d['C'] <= 0 else
                             d['v0eta'] - d['C'] * F_var(d['g'], d['s'], d['age'], LAM, tmin), 1)
        live = [x for x in r['vpath'] if x is not None] + ([r['cur']] if r.get('cur') is not None else [])
        if live:
            r['peak'] = max(live + [float(r['v0'] or 0)])
    out['meta']['ORDER_N'] = dict(note='ESTIMATE, NOT A BUILD. ORDER N variant C frontier point.',
                                  LAMBDA=LAM, THETA_R=theta_r(LAM), TMIN=tmin, G0=G0, s0=S0, age_gate=24)
    json.dump(out, open(os.path.join(LB.SP, 'per_entrant_NVARC.json'), 'w'))
    P('   wrote per_entrant_NVARC.json')
    M['variantC'] = dict(LAMBDA=LAM, THETA_R=theta_r(LAM), TMIN=tmin, age_gate=24,
                         w2_mark=classmark(LAM, tmin, 2006, 2016), cohort_mark=classmark(LAM, tmin))
    json.dump(M, open(os.path.join(HERE, 'MECH_N.json'), 'w'), indent=1)

json.dump(dict(ladder=LADC, best=BEST), open(os.path.join(HERE, 'FLOOR_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'FLOOR_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FLOOR_N.json / FLOOR_N_out.txt')
