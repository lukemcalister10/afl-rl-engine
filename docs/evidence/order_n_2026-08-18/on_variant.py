#!/usr/bin/env python3
"""ORDER N — VARIANT B: THE DERIVED CHARGE WHERE THE AGE BAR HAS CONTENT, THE CURRENT CHARGE WHERE IT
DOES NOT. READ-ONLY. NO BOARD IS BUILT.

Why this variant exists, stated before its numbers. on_sweep.py found that the derived charge breaks
the veteran caps at EVERY level of LAMBDA, and that the breach is structural: A(g) saturates at 1, so
a 141-game row pays about 54% of his pedigree leg where today he pays 0.1%. The veteran identity is
not something this seat may trade away on its own word.

The engine's own cap law says the age bar is FLAT from age 24. So "performance against age
expectation" is a statement with content below 24 and no content at or above it. Variant B applies
the derived charge exactly where that statement has content, and leaves the existing charge in place
where it does not.

  F(g, s, age) = 1 - exp(-LAMBDA * A(g) * T(s))     if age at the vantage < 24
               = 0.50 * m_d(g)                      otherwise

LAMBDA is re-solved by the same anchoring identity. Nothing else changes.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_variant.py
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


def T_of(s, lam):
    tmax = 1.0 - theta_r(lam) * (S_P5 - S0)
    return min(max(1.0 - theta_r(lam) * (float(s) - S0), 0.0), tmax)


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_var(g, s, age, lam):
    if g <= 0:
        return 0.0
    if age is None or age >= AGE_GATE or s is None:
        return F_old(g)
    return 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam))


P('=' * 118)
P('ORDER N — VARIANT B. THE DERIVED CHARGE BELOW 24, THE CURRENT CHARGE AT 24 AND ABOVE.')
P('ESTIMATES PENDING A BUILD.')
P('=' * 118)
P()

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
        row.append(dict(y=y, g=g, s=LB.perf_surplus(a, y), age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i])))
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
    """The CURRENT (2026) price, priced through the same identity. `cur` is a separate field from
    vpath for rows whose career ended before 2026, so it must be priced in its own right."""
    d = CURBASE.get(k)
    if d is None:
        return None
    if lam is None or d['C'] <= 0:
        return d['vK']
    return d['v0eta'] - d['C'] * F_var(d['g'], d['s'], d['age'], lam)


def vp_new(r, lam):
    vp = list(r.get('vpath') or [])
    if lam is None:
        return vp
    van = VAN.get(r['key']) or []
    for i in range(len(vp)):
        if i >= len(van) or van[i] is None or vp[i] is None:
            continue
        v = van[i]
        if v['C'] <= 0:
            continue
        vp[i] = round(v['v0eta'] - v['C'] * F_var(v['g'], v['s'], v['age'], lam), 1)
    return vp


# ---- anchoring solve --------------------------------------------------------------------------------
CLASSES_MARK = list(range(2005, 2016))
anchor = []
for k, a in MK.items():
    c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
    if c not in CLASSES_MARK or not (float(a.get('v0') or 0) > 0):
        continue
    yrs = a.get('yrs') or []
    if c not in yrs:
        continue
    v = VAN[k][yrs.index(c)]
    if v is None or v['C'] <= 0:
        continue
    anchor.append(v)
tot_old = sum(v['C'] * F_old(v['g']) for v in anchor)
lo, hi = 1e-6, 20.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if sum(v['C'] * F_var(v['g'], v['s'], v['age'], mid) for v in anchor) < tot_old:
        lo = mid
    else:
        hi = mid
LAM = 0.5 * (lo + hi)
P('-' * 118)
P('1 · THE ANCHORING SOLVE, RE-RUN UNDER THE GATE')
P('-' * 118)
P('   anchor population %d year-1 rows, cohort classes 2005-2015. Current charge removes %.1f points.'
  % (len(anchor), tot_old))
P('   SOLVED:  LAMBDA  = %.5f      THETA_R = %.5f      zero point s = %+.2f points per game'
  % (LAM, theta_r(LAM), S0 + 1.0 / theta_r(LAM)))
P('   rows in the anchor population already at or past the zero point: %d of %d (%.1f%%)'
  % (sum(1 for v in anchor if v['s'] is not None and v['s'] >= S0 + 1.0 / theta_r(LAM)),
     len(anchor), 100.0 * sum(1 for v in anchor if v['s'] is not None and v['s'] >= S0 + 1.0 / theta_r(LAM)) / len(anchor)))
P()

# ---- band and class instruments (checked in on_sweep.py) ---------------------------------------------
SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
ND = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
      and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
BANDS = [('ALL picks 1-64', lambda p: True), ('picks 1-20', lambda p: p <= 20),
         ('picks 21-64', lambda p: p >= 21), ('picks 1-10', lambda p: p <= 10),
         ('picks 11-20', lambda p: 11 <= p <= 20), ('picks 21-30', lambda p: 21 <= p <= 30),
         ('picks 31-40', lambda p: 31 <= p <= 40), ('picks 41-64', lambda p: 41 <= p <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]


def apprec01(lam):
    out = {}
    cache = {r['key']: vp_new(r, lam) for r in ND}
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


def classmark(lam, lo_y=2005, hi_y=2015):
    per = []
    for y in range(lo_y, hi_y + 1):
        num = den = 0.0; n = 0
        for k, a in MK.items():
            c = (a['year'] if a.get('type') == 'MSD' else a['year'] + 1)
            if c != y or not (float(a.get('v0') or 0) > 0):
                continue
            yrs = a.get('yrs') or []
            vp = vp_new(a, lam)
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


def board_points(lam):
    out = {}
    for k in MK:
        c = cur_new(k, lam)
        if c is not None:
            out[k] = round(c / PL_F)
    return out


LED = LB.load_ledger()
MAT = [r for r in LED['rows'] if int(r['age']) >= 24]
BOARD_TOTAL = sum(float(r['landing']) for r in LED['rows'])
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie']

P('-' * 118)
P('2 · THE LADDER UNDER THE GATE')
P('-' * 118)
P('   The W2 mark is the REGISTERED BASIS for the owner\'s 1.03 floor and the 1.14 buy rail: draft')
P('   classes 2005-2015, which are cohort classes 2006-2016 (ORDER L settled this).')
P('   %-7s %8s %8s | %8s %8s %9s %9s %9s %9s | %7s %7s | %6s %6s %6s %6s %6s %6s' % (
    'LAMBDA', 'THETA_R', 'zero s', 'coh mark', 'W2 mark', 'p1-10 PRI', 'p1-10 MOD', 'ALL PRI', 'ALL MOD',
    'vetchurn', 'vet net', 'dean', 'cdt', 'xav', 'ann', 'pat', 'kako'))
LAD = []
CANDS = sorted(set([round(x, 3) for x in np.arange(0.30, 3.01, 0.10)] + [round(LAM, 5)]))
for lam in CANDS:
    ap = apprec01(lam); bp = board_points(lam)
    mv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
    mv = [(k, d) for k, d in mv if d != 0]
    churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    cm = classmark(lam); w2 = classmark(lam, 2006, 2016)
    row = dict(lam=lam, theta_r=theta_r(lam), zero_at=S0 + 1.0 / theta_r(lam), cohort_mark=cm, w2_mark=w2,
               p110_pri=ap['PRIMARY|picks 1-10'], p110_mod=ap['MODERN|picks 1-10'],
               all_mod=ap['MODERN|ALL picks 1-64'], all_pri=ap['PRIMARY|ALL picks 1-64'],
               vet_churn=churn, vet_net=net, named={k: bp.get(k) for k in NAMED},
               bands={k: v for k, v in ap.items()})
    LAD.append(row)
    tag = ' <- anchoring solve' if abs(lam - round(LAM, 5)) < 1e-9 else ''
    P('   %-7.3f %8.5f %+8.2f | %8.4f %8.4f %+8.2f%% %+8.2f%% %+8.2f%% %+8.2f%% | %7.0f %+7.0f | %6d %6d %6d %6d %6d %6d%s' % (
        lam, theta_r(lam), row['zero_at'], cm, w2, 100 * row['p110_pri'], 100 * row['p110_mod'],
        100 * row['all_pri'], 100 * row['all_mod'], churn, net, *[bp.get(k, 0) for k in NAMED[:6]], tag))
P()
P('   RAILS: picks 1-10 under +14.00%% in BOTH windows · veteran churn <= %.0f · |veteran net| <= %.0f'
  % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
P('   ORDER K: cohort mark 1.0324 · picks 1-10 +8.22%% / +13.65%% · ALL MOD -0.96%% · churn 947 · net -601')
P('            dean 2403 · cdt 1505 · xavier 1162 · annable 1537 · patterson 1440 · kako 832')
P()

def ok_rail(r):
    return r['p110_pri'] < 0.14 and r['p110_mod'] < 0.14
def ok_floor(r):
    return r['w2_mark'] >= 1.03
def ok_vet(r):
    return r['vet_churn'] <= 0.0015 * BOARD_TOTAL and abs(r['vet_net']) <= 0.0010 * BOARD_TOTAL
P('   THE TWO RAILS AND WHICH WAY EACH ONE PUSHES:')
rail_ok = [r['lam'] for r in LAD if ok_rail(r)]
floor_ok = [r['lam'] for r in LAD if ok_floor(r)]
vet_ok = [r['lam'] for r in LAD if ok_vet(r)]
P('     picks 1-10 under +14%% in BOTH windows  needs LAMBDA >= %s' % (
    ('%.2f' % min(rail_ok)) if rail_ok else 'nothing on this ladder'))
P('     the G1 floor, W2 mark >= 1.03           needs LAMBDA <= %s' % (
    ('%.2f' % max(floor_ok)) if floor_ok else 'nothing on this ladder'))
P('     the veteran caps                        hold at EVERY LAMBDA on this ladder (%d of %d)' % (
    len(vet_ok), len(LAD)))
legal = [r for r in LAD if ok_rail(r) and ok_floor(r) and ok_vet(r)]
P()
if legal:
    best = min(legal, key=lambda r: r['lam'])
    P('   %d rungs clear all three. The SMALLEST is LAMBDA = %.3f, and smallest is best here because'
      % (len(legal), best['lam']))
    P('   THETA_R = BETA_sat/LAMBDA — the smallest legal LAMBDA is the STRONGEST legal tilt.')
else:
    P('   *** NO RUNG CLEARS ALL THREE. THE TWO RAILS DO NOT OVERLAP. ***')
    P('   The band rail pushes LAMBDA up. The class floor pushes it down. Between them there is nothing.')
    if rail_ok and floor_ok:
        P('   The gap is LAMBDA %.2f to %.2f — the band rail wants at least %.2f, the floor allows at most %.2f.'
          % (max(floor_ok), min(rail_ok), min(rail_ok), max(floor_ok)))
P()

# ---- the frontier point, in full ---------------------------------------------------------------------
BL = min(legal, key=lambda r: r['lam'])['lam'] if legal else round(LAM, 5)
P('-' * 118)
P('3 · THE FRONTIER POINT IN FULL — LAMBDA = %.3f, THETA_R = %.5f' % (BL, theta_r(BL)))
P('-' * 118)
ap = apprec01(BL); bp = board_points(BL)
P('   BAND TABLES, BOTH WINDOWS. B = over the +14%% buy rail. S = below 0%%, sell side.')
P('   %-16s | %-22s | %-22s' % ('band', 'PRIMARY  N / K', 'MODERN  N / K'))
BREF = json.load(open(os.path.join(HERE, 'BANDS_N.json')))
for bname, _ in BANDS:
    cells = []
    for w in ('PRIMARY', 'MODERN'):
        a = ap['%s|%s' % (w, bname)]
        k = BREF['nd']['OKRULED']['%s|ALLCOH|%s' % (w, bname)]['apprec01']
        tg = 'B' if a > 0.14 else ('S' if a < 0 else ' ')
        tk = 'B' if k > 0.14 else ('S' if k < 0 else ' ')
        cells.append('%+8.2f%%%s / %+7.2f%%%s' % (100 * a, tg, 100 * k, tk))
    P('   %-16s | %-22s | %-22s' % (bname, cells[0], cells[1]))
P()
mv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
mv = [(k, d) for k, d in mv if d != 0]
P('   veteran pool: %d move · churn %.0f (rail %.0f) · net %+.0f (rail %.0f) · %s'
  % (len(mv), sum(abs(d) for _, d in mv), 0.0015 * BOARD_TOTAL, sum(d for _, d in mv),
     0.0010 * BOARD_TOTAL,
     'INSIDE BOTH' if (sum(abs(d) for _, d in mv) <= 0.0015 * BOARD_TOTAL
                       and abs(sum(d for _, d in mv)) <= 0.0010 * BOARD_TOTAL) else 'BREACH'))
P('   cohort class mark %.4f (ORDER K 1.0324)' % classmark(BL))
tot_k = sum(float(r['orderk']) for r in LED['rows'])
tot_n = sum(bp.get(r['key'], float(r['orderk'])) for r in LED['rows'])
P('   board total %d -> %d  (%+d, %+.2f%%)' % (round(tot_k), round(tot_n), round(tot_n - tot_k),
                                               100 * (tot_n - tot_k) / tot_k))
P()

# ---- property test at the frontier point -------------------------------------------------------------
S1 = json.load(open(os.path.join(HERE, 'STEP1_N.json')))
rows = S1['rows']
P('   THE PROPERTY TEST at LAMBDA = %.3f. Spearman of the price response and of the CHARGE against' % BL)
P('   performance surplus, within games bins.')
P('   %-10s %5s | %11s %11s | %11s %11s' % ('games bin', 'n', 'rho R ORDER K', 'rho R ORDER N',
                                            'rho chg K', 'rho chg N'))
for lo_, hi_ in LB.G_BINS_1:
    b = '%d-%d' % (lo_, hi_)
    sub = [r for r in rows if r['gbin'] == b]
    if len(sub) < 8:
        continue
    ps = np.array([r['ps'] for r in sub])
    rk = np.array([r['R_k'] for r in sub])
    rn = np.array([bp.get(r['key'], r['orderk']) / r['v0'] for r in sub])
    ck = np.array([r['charge_pct'] for r in sub])
    cn = np.array([F_var(r['g'], r['ps'], r['age'], BL) for r in sub])
    P('   %-10s %5d | %+11.4f %+11.4f | %+11.4f %+11.4f' % (b, len(sub), spear(ps, rk), spear(ps, rn),
                                                            spear(ps, ck), spear(ps, cn)))
P()
P('   NAMED ROWS AT THE FRONTIER POINT — ILLUSTRATIONS OF THE DERIVED RULE, NEVER TARGETS.')
byk = {r['key']: r for r in LED['rows']}
P('   %-22s %3s %5s %5s %9s | %8s %8s %8s' % ('row', 'age', 'pick', 'g', 'surplus', 'landing', 'ORDER K', 'ORDER N'))
NAMEDOUT = {}
for k in NAMED + ['milan-murdock']:
    r = byk.get(k)
    if r is None:
        P('   %-22s  not on the 804-row board' % k); continue
    m = MK.get(k)
    Y = max((s['year'] for s in m['seasons']), default=None)
    s = LB.perf_surplus(m, Y) if Y else None
    P('   %-22s %3d %5s %5.0f %9s | %8d %8d %8d' % (
        r['name'][:22], r['age'], r['pick'], float(r['g'] or 0),
        ('%+.2f' % s) if s is not None else 'n/a', round(r['landing']), round(r['orderk']),
        bp.get(k, round(r['orderk']))))
    NAMEDOUT[k] = dict(age=r['age'], pick=r['pick'], g=float(r['g'] or 0), ps=s,
                       landing=r['landing'], orderk=r['orderk'], order_n=bp.get(k))
P()

# ---- write the frontier matrix so the committed instruments can be run on it --------------------------
out = copy.deepcopy(json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json'))))
for r in out['recs']:
    vp = vp_new(r, BL)
    r['vpath'] = vp
    c = cur_new(r['key'], BL)
    if c is not None:
        r['cur'] = round(c, 1)
    live = [x for x in vp if x is not None] + ([r['cur']] if r.get('cur') is not None else [])
    if live:
        r['peak'] = max(live + [float(r['v0'] or 0)])
out['meta']['ORDER_N'] = dict(note='ESTIMATE, NOT A BUILD. ORDER N variant B at the frontier point.',
                              LAMBDA=BL, THETA_R=theta_r(BL), G0=G0, s0=S0, age_gate=AGE_GATE)
json.dump(out, open(os.path.join(LB.SP, 'per_entrant_NVARB.json'), 'w'))
P('   wrote per_entrant_NVARB.json — the frontier-point matrix, for the committed instruments.')

M['variantB'] = dict(age_gate=AGE_GATE, LAMBDA_anchor=LAM, LAMBDA_frontier=BL,
                     THETA_R_frontier=theta_r(BL), zero_at=S0 + 1.0 / theta_r(BL))
json.dump(M, open(os.path.join(HERE, 'MECH_N.json'), 'w'), indent=1)
json.dump(dict(ladder=LAD, frontier=BL, named=NAMEDOUT,
               rails=dict(churn=0.0015 * BOARD_TOTAL, net=0.0010 * BOARD_TOTAL)),
          open(os.path.join(HERE, 'VARIANT_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'VARIANT_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote VARIANT_N.json / VARIANT_N_out.txt')
