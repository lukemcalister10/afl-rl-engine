#!/usr/bin/env python3
"""ORDER P STEP 4 — PRICE THE DERIVED CHARGE OFFLINE. READ-ONLY. NO BOARD IS BUILT.

Every number here is an ESTIMATE PENDING A BUILD. The pedigree-leg arithmetic is exact and the
identity is ORDER N's, already proved (falsifier N1 / P1). What cannot be done without a build: the
engine's assert wall, the continuity objects, rho32 monotonicity, the day-0 identity.

The age gate at 24 is carried over from ORDER N variant B, for the reason ORDER N measured: A(g)
saturates, so an ungated charge breaks the veteran caps at every LAMBDA. The gate is re-checked here.

  usage: OPENBLAS_NUM_THREADS=1 ... python op_step4.py
"""
import json, math, os, sys, copy, statistics, collections
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

PL_F = 1.0524                    # pick_redenomination.json::factor — matrix points / board points
AGE_GATE = 24
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


M = json.load(open(os.path.join(HERE, 'MECH_P.json')))
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def theta_r(lam):
    return BSAT / lam


def tmax_of(lam):
    return 1.0 - theta_r(lam) * (S_P5 - S0)


def T_of(s, lam):
    return min(max(1.0 - theta_r(lam) * (float(s) - S0), 0.0), tmax_of(lam))


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_new(g, s, age, lam):
    """The FRACTION of the pedigree leg removed. Age-gated at 24, as ORDER N variant B."""
    if g <= 0:
        return 0.0
    if age is None or age >= AGE_GATE or s is None:
        return F_old(g)
    return 1.0 - math.exp(-lam * A_of(g) * T_of(s, lam))


P('=' * 118)
P('ORDER P — STEP 4. THE PEDIGREE-CONDITIONAL CHARGE, PRICED OFFLINE.')
P('EVERY NUMBER BELOW IS AN ESTIMATE PENDING A BUILD.')
P('=' * 118)
P('mechanism: pi *= exp( -LAMBDA * A(g) * T(s_P) )   below age 24;  the current charge at 24 and above')
P('  A(g)   = 1 - exp(-g/%.4f)' % G0)
P('  T(s)   = clip( 1 - THETA_R*(s %+0.4f), 0, TMAX ),  THETA_R = %.5f / LAMBDA' % (-S0, BSAT))
P('  s_P    = games-weighted mean of ( season avg - [ age bar + pedigree premium PG(ln v0, class) ] )')
P()

MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')

# ---- the pedigree premium surface, rebuilt from the same population ------------------------------------
ROWS = PB.season_rows(MK)
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)

# ---- the per-vantage charge base ------------------------------------------------------------------------
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
        row.append(dict(y=y, g=g, sP=PB.perf_surplus_P(a, y, PG), sN=LB.perf_surplus(a, y),
                        age=LB.age_at(a, y),
                        C=((vpb[i] - vpa[i]) / (0.50 * md)) if md > 1e-12 else 0.0,
                        v0eta=float(vpb[i]), vK=float(vpa[i])))
    VAN[k] = row

CURBASE = {}
for k, a in MK.items():
    ca, cb = a.get('cur'), ME[k].get('cur')
    if ca is None or cb is None:
        continue
    g = float(a.get('games_total') or 0.0)
    md = LB.m_d(g)
    CURBASE[k] = dict(g=g, sP=PB.perf_surplus_P(a, 2026, PG), sN=LB.perf_surplus(a, 2026),
                      age=LB.age_at(a, 2026),
                      C=((float(cb) - float(ca)) / (0.50 * md)) if md > 1e-12 else 0.0,
                      v0eta=float(cb), vK=float(ca))


def cur_new(k, lam):
    d = CURBASE.get(k)
    if d is None:
        return None
    if lam is None or d['C'] <= 0:
        return d['vK']
    return d['v0eta'] - d['C'] * F_new(d['g'], d['sP'], d['age'], lam)


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
        vp[i] = round(v['v0eta'] - v['C'] * F_new(v['g'], v['sP'], v['age'], lam), 1)
    return vp


# ---- 0 · the identity, re-asserted ------------------------------------------------------------------------
P('-' * 118)
P('0 · FALSIFIER P1 — THE OFFLINE PRICING IDENTITY, RE-ASSERTED ON THIS TREE')
P('-' * 118)
worst = 0.0; nchk = 0
for k, a in MK.items():
    for i, v in enumerate(VAN[k]):
        if v is None or v['C'] <= 0:
            continue
        back = v['v0eta'] - v['C'] * F_old(v['g'])
        den = max(1.0, abs(v['vK']))
        worst = max(worst, abs(back - v['vK']) / den); nchk += 1
P('   round trip: rebuild ORDER K from the eta-zero board through the identity at eta 0.50.')
P('   vantages checked %d   worst relative error %.3g   -> P1 %s' % (
    nchk, worst, 'DID NOT FIRE' if worst < 1e-6 else 'FIRED'))
assert worst < 1e-6, 'P1 FIRED'
neg = sum(1 for k in MK for v in VAN[k] if v is not None and v['C'] < -1e-9)
P('   charge bases with the wrong sign (the charge must only ever subtract): %d' % neg)
P()

# ---- 1 · the anchoring solve -------------------------------------------------------------------------------
P('-' * 118)
P('1 · THE ANCHORING SOLVE — LAMBDA IS NOT TUNED, IT IS SOLVED')
P('-' * 118)
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
    if sum(v['C'] * F_new(v['g'], v['sP'], v['age'], mid) for v in anchor) < tot_old:
        lo = mid
    else:
        hi = mid
LAM = 0.5 * (lo + hi)
ZERO = S0 + 1.0 / theta_r(LAM)
P('   The LEVEL of the charge is a no-arbitrage calibration, not an outcome question (ORDER M proved')
P('   the charge is load-bearing for the whole board\'s year-1 anchoring). So LAMBDA is solved so the')
P('   derived charge removes THE SAME TOTAL POINTS from the year-1 class-mark population as the')
P('   current charge does. The tilt then redistributes those points. It does not add any.')
P()
P('   anchor population %d year-1 rows, cohort classes 2005-2015. Current charge removes %.1f points.'
  % (len(anchor), tot_old))
P('   SOLVED:  LAMBDA = %.5f   THETA_R = %.5f   TMAX = %.4f   zero point s_P = %+.2f points/game'
  % (LAM, theta_r(LAM), tmax_of(LAM), ZERO))
P('            (ORDER N, on the age-only surplus: LAMBDA 0.82131, THETA_R 0.14028, zero at +9.44.)')
P('   removes %.1f points against the target %.1f.' % (
    sum(v['C'] * F_new(v['g'], v['sP'], v['age'], LAM) for v in anchor), tot_old))
P()

# ---- 2 · the charge, side by side ---------------------------------------------------------------------------
P('-' * 118)
P('2 · THE CHARGE, SIDE BY SIDE. Percentage of the pedigree leg removed.')
P('-' * 118)
P('   %-6s | %-12s | %-46s' % ('games', 'CURRENT', 'ORDER P, by pedigree-conditional surplus s_P'))
P('   %-6s | %-12s | %10s %10s %10s %10s' % ('', 'blind', 's_P=-25', 's_P=-10', 's_P=0', 's_P=+10'))
CHG = {}
for g in (1, 2, 3, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50):
    cells = [100 * F_new(g, s, 19, LAM) for s in (-25, -10, 0, 10)]
    P('   %-6d | %11.1f%% | %9.1f%% %9.1f%% %9.1f%% %9.1f%%' % (g, 100 * F_old(g), *cells))
    CHG[g] = dict(old=100 * F_old(g), new=cells)
P()
P('   THE ZERO POINT. T hits zero at s_P = %+.2f. A young player producing more than %.2f points a' % (ZERO, ZERO))
P('   game above his PEDIGREE-CONDITIONAL bar pays nothing on his pedigree leg.')
S2J = json.load(open(os.path.join(HERE, 'STEP2_P.json')))
vr = S2J['rows']
P('   Share of the young cohort at or past it: %.1f%%   (ORDER N, on its own zero point: 18.5%%)'
  % (100.0 * np.mean([1.0 if r['sP'] >= ZERO else 0.0 for r in vr])))
P()

# ---- 3 · THE OWNER'S PREDICTION, TESTED --------------------------------------------------------------------
P('-' * 118)
P('3 · THE OWNER\'S PREDICTION, TESTED. Does relief still flow to the top of the draft?')
P('-' * 118)
ZN = 9.13                       # ORDER N's own zero point on its own surplus (PACKET_N sec 8.3)
nd = [r for r in vr if r['pick'] is not None]
P('   %-10s %6s | %10s %10s | %12s %12s' % ('pick band', 'rows', 'med s_N', 'med s_P',
                                            'share full N', 'share full P'))
BAL = {}
for b in ('1-10', '11-20', '21-40', '41+/pool'):
    sub = [r for r in nd if r['band'] == b]
    if not sub: continue
    sN = np.array([r['sN'] for r in sub]); sP = np.array([r['sP'] for r in sub])
    fN = 100.0 * float(np.mean(sN >= ZN)); fP = 100.0 * float(np.mean(sP >= ZERO))
    P('   %-10s %6d | %+10.2f %+10.2f | %11.1f%% %11.1f%%' % (b, len(sub), np.median(sN), np.median(sP), fN, fP))
    BAL[b] = dict(n=len(sub), med_N=float(np.median(sN)), med_P=float(np.median(sP)),
                  share_N=fN, share_P=fP)
pk = np.array([float(r['pick']) for r in nd])
rN = spear(pk, np.array([r['sN'] for r in nd])); rP = spear(pk, np.array([r['sP'] for r in nd]))
P('   Spearman(pick, surplus):  ORDER N %+.4f   ORDER P %+.4f' % (rN, rP))
P()
P('   FALSIFIER P10 — does the RELIEF itself still flow to the top? Relief is what the row keeps that')
P('   the current charge would have taken, as a share of its own entry price.')
relN = []; relP = []; pks = []
for r in nd:
    k = r['key']
    yrs = MK[k].get('yrs') or []
    if r['Y'] not in yrs:
        continue
    v = VAN[k][yrs.index(r['Y'])]
    if v is None or v['C'] <= 0:
        continue
    rp = v['C'] * (F_old(v['g']) - F_new(v['g'], v['sP'], v['age'], LAM)) / r['v0']
    rn = v['C'] * (F_old(v['g']) - (0.0 if v['sN'] is None else
                                    (1.0 - math.exp(-0.82131 * (1 - math.exp(-v['g'] / 9.72))
                                                    * min(max(1 - 0.14028 * (v['sN'] - 2.3163), 0.0), 5.998)))
                                    if (v['age'] is not None and v['age'] < 24) else F_old(v['g']))) / r['v0']
    relP.append(rp); relN.append(rn); pks.append(float(r['pick']))
sr_p = spear(np.array(pks), np.array(relP)); sr_n = spear(np.array(pks), np.array(relN))
P('   Spearman(pick, relief / v0):  ORDER N %+.4f   ORDER P %+.4f   over %d ND vantages'
  % (sr_n, sr_p, len(pks)))
P('   P10 threshold was |rho| > 0.20 under the derived charge  ->  P10 %s'
  % ('FIRED' if abs(sr_p) > 0.20 else 'did not fire'))
P('   %-10s %6s | %14s %14s' % ('pick band', 'rows', 'mean relief N', 'mean relief P'))
for b in ('1-10', '11-20', '21-40', '41+/pool'):
    ix = [i for i, r in enumerate([x for x in nd if x['pick'] is not None]) if r['band'] == b]
    ix = [i for i in range(len(pks)) if LB.band_of(pks[i]) == b]
    if not ix: continue
    P('   %-10s %6d | %+13.4f %+13.4f' % (b, len(ix), np.mean([relN[i] for i in ix]),
                                          np.mean([relP[i] for i in ix])))
P()

# ---- 4 · the ladder ------------------------------------------------------------------------------------------
SRC = json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json')))['recs']
NDR = [r for r in SRC if (not r.get('is_pool')) and r.get('teaches_curve') and r.get('type') == 'ND'
       and r.get('pick') and 1 <= int(r['pick']) <= 64]
WEND = max(y for r in SRC for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
BANDS = [('ALL picks 1-64', lambda p: True), ('picks 1-20', lambda p: p <= 20),
         ('picks 21-64', lambda p: p >= 21), ('picks 1-10', lambda p: p <= 10),
         ('picks 11-20', lambda p: 11 <= p <= 20), ('picks 21-30', lambda p: 21 <= p <= 30),
         ('picks 31-40', lambda p: 31 <= p <= 40), ('picks 41-64', lambda p: 41 <= p <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]


def apprec01(lam):
    out = {}
    cache = {r['key']: vp_new(r, lam) for r in NDR}
    for wname, lo_, hi_ in WINDOWS:
        pop_w = [r for r in NDR if lo_ <= r['year'] + 1 <= hi_]
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
P('4 · THE LADDER. LAMBDA is SOLVED at %.3f; the ladder shows what the rails do around it.' % LAM)
P('-' * 118)
P('   %-7s %8s %8s | %8s %8s %9s %9s %9s %9s | %7s %7s' % (
    'LAMBDA', 'THETA_R', 'zero s', 'coh mark', 'W2 mark', 'p1-10 PRI', 'p1-10 MOD', 'ALL PRI', 'ALL MOD',
    'vetchurn', 'vet net'))
LAD = []
for lam in sorted(set([round(x, 3) for x in np.arange(0.30, 2.01, 0.10)] + [round(LAM, 5)])):
    ap = apprec01(lam); bp = board_points(lam)
    mv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
    mv = [(k, d) for k, d in mv if d != 0]
    churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    cm = classmark(lam); w2 = classmark(lam, 2006, 2016)
    row = dict(lam=lam, theta_r=theta_r(lam), zero_at=S0 + 1.0 / theta_r(lam), cohort_mark=cm, w2_mark=w2,
               p110_pri=ap['PRIMARY|picks 1-10'], p110_mod=ap['MODERN|picks 1-10'],
               all_pri=ap['PRIMARY|ALL picks 1-64'], all_mod=ap['MODERN|ALL picks 1-64'],
               vet_churn=churn, vet_net=net, bands=dict(ap))
    LAD.append(row)
    tag = '  <- the anchoring solve' if abs(lam - round(LAM, 5)) < 1e-9 else ''
    P('   %-7.3f %8.5f %+8.2f | %8.4f %8.4f %+8.2f%% %+8.2f%% %+8.2f%% %+8.2f%% | %7.0f %+7.0f%s' % (
        lam, theta_r(lam), row['zero_at'], cm, w2, 100 * row['p110_pri'], 100 * row['p110_mod'],
        100 * row['all_pri'], 100 * row['all_mod'], churn, net, tag))
P()
P('   RAILS: picks 1-10 under +14.00%% in BOTH windows · W2 class mark >= 1.03 · veteran churn <= %.0f'
  % (0.0015 * BOARD_TOTAL))
P('          · |veteran net| <= %.0f' % (0.0010 * BOARD_TOTAL))
P('   ORDER K: cohort mark 1.0324 · W2 1.0513 · picks 1-10 +8.22%% / +13.65%% · churn 947 · net -601')
P('   ORDER N: cohort mark 1.0324 · W2 1.0604 · picks 1-10 +16.13%% / +23.90%% · churn 951 · net -595')
rail_ok = [r['lam'] for r in LAD if r['p110_pri'] < 0.14 and r['p110_mod'] < 0.14]
floor_ok = [r['lam'] for r in LAD if r['w2_mark'] >= 1.03]
vet_ok = [r['lam'] for r in LAD if r['vet_churn'] <= 0.0015 * BOARD_TOTAL
          and abs(r['vet_net']) <= 0.0010 * BOARD_TOTAL]
legal = [r for r in LAD if r['lam'] in rail_ok and r['lam'] in floor_ok and r['lam'] in vet_ok]
P()
P('     picks 1-10 under +14%% in BOTH windows  : %s' % (
    'LAMBDA >= %.2f' % min(rail_ok) if rail_ok else 'nothing on this ladder'))
P('     the G1 floor, W2 mark >= 1.03          : %s' % (
    'LAMBDA <= %.2f' % max(floor_ok) if floor_ok else 'nothing on this ladder'))
P('     the veteran caps                       : hold at %d of %d rungs' % (len(vet_ok), len(LAD)))
P('     rungs legal on all three               : %d' % len(legal))
if legal:
    P('     the anchoring solve LAMBDA = %.5f is %s' % (
        LAM, 'INSIDE the legal set' if any(abs(r['lam'] - round(LAM, 5)) < 1e-9 for r in legal)
        else 'OUTSIDE the legal set'))
P()

# ---- 5 · the priced matrix -----------------------------------------------------------------------------------
out = copy.deepcopy(json.load(open(os.path.join(LB.SP, 'per_entrant_OKRULED.json'))))
nabove = 0
for r in out['recs']:
    vp = vp_new(r, LAM)
    van = VAN.get(r['key']) or []
    for i in range(len(vp)):
        if i < len(van) and van[i] is not None and vp[i] is not None:
            if vp[i] > van[i]['v0eta'] + 1e-6:
                nabove += 1
    r['vpath'] = vp
    c = cur_new(r['key'], LAM)
    if c is not None:
        r['cur'] = round(c, 1)
    live = [x for x in vp if x is not None] + ([r['cur']] if r.get('cur') is not None else [])
    if live:
        r['peak'] = max(live + [float(r['v0'] or 0)])
out['meta']['ORDER_P'] = dict(note='ESTIMATE, NOT A BUILD. vpath re-priced offline by ORDER P.',
                              mechanism='pi *= exp(-LAMBDA*A(g)*T(s_P)), age gate 24',
                              LAMBDA=LAM, G0=G0, BETA_sat=BSAT, THETA_R=theta_r(LAM),
                              TMAX=tmax_of(LAM), s0=S0, age_gate=AGE_GATE,
                              base_eta0='per_entrant_M0ETA0.json', base_etaK='per_entrant_OKRULED.json')
json.dump(out, open(os.path.join(LB.SP, 'per_entrant_PDERIV.json'), 'w'))
P('-' * 118)
P('5 · THE RE-PRICED MATRIX AND THE STRUCTURAL ASSERTS')
P('-' * 118)
P('   wrote per_entrant_PDERIV.json')
P('   P-S5, asserted row by row: vantages priced ABOVE their own uncharged (eta-zero) price: %d' % nabove)
P('   P-S1, gameless rows: A(0)=0, so every row with 0 career games at a vantage is bit-identical.')
assert nabove == 0, 'P-S5 FIRED'
P()

# ---- 6 · where the money moves ---------------------------------------------------------------------------------
MN = LB.load_matrix('PDERIV')
MNN = LB.load_matrix('NVARB')
P('-' * 118)
P('6 · WHERE THE MONEY MOVES, IN BOARD POINTS, ACROSS THE WHOLE 804-ROW BOARD')
P('-' * 118)
mv = []
for r in LED['rows']:
    k = r['key']
    if k not in MN or MN[k].get('cur') is None:
        continue
    nb = float(MN[k]['cur']) / PL_F
    nn = float(MNN[k]['cur']) / PL_F if (k in MNN and MNN[k].get('cur') is not None) else None
    mv.append(dict(key=k, name=r['name'], age=r['age'], g=float(r['g'] or 0), pick=r.get('pick'),
                   pos=r['pos'], orderk=float(r['orderk']), ordern=nn, new=nb, d=nb - float(r['orderk'])))
tot_k = sum(x['orderk'] for x in mv)
tot_n = sum((x['ordern'] if x['ordern'] is not None else x['orderk']) for x in mv)
tot_p = sum(x['new'] for x in mv)
P('   board total: ORDER K %d  ·  ORDER N %d (%+.2f%%)  ·  ORDER P %d (%+.2f%%)' % (
    round(tot_k), round(tot_n), 100 * (tot_n - tot_k) / tot_k, round(tot_p), 100 * (tot_p - tot_k) / tot_k))
P('   rows that move against ORDER K: %d of %d (up %d, down %d)' % (
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
P('   %-14s %6s %12s' % ('age in 2026', 'rows', 'total points'))
for lo_, hi_, lab in ((0, 20, '20 and under'), (21, 23, '21-23'), (24, 99, '24 and over')):
    s = [x for x in mv if lo_ <= int(x['age']) <= hi_]
    P('   %-14s %6d %+12.0f' % (lab, len(s), sum(x['d'] for x in s)))
P()
bp = board_points(LAM)
mvv = [(r['key'], bp.get(r['key'], float(r['landing'])) - float(r['landing'])) for r in MAT]
mvv = [(k, d) for k, d in mvv if d != 0]
P('   VETERAN POOL (age 24+): %d move · churn %.0f (rail %.0f) · net %+.0f (rail %.0f) · %s' % (
    len(mvv), sum(abs(d) for _, d in mvv), 0.0015 * BOARD_TOTAL, sum(d for _, d in mvv),
    0.0010 * BOARD_TOTAL,
    'INSIDE BOTH' if (sum(abs(d) for _, d in mvv) <= 0.0015 * BOARD_TOTAL
                      and abs(sum(d for _, d in mvv)) <= 0.0010 * BOARD_TOTAL) else 'BREACH'))
P('   (ORDER K 947 / -601 · ORDER N 951 / -595)')
P()
P('   the ten largest rises and the ten largest falls against ORDER K:')
mv.sort(key=lambda x: -x['d'])
for x in mv[:10] + [None] + mv[-10:]:
    if x is None:
        P('     ...'); continue
    P('     %+8.0f  %-26s age %2d  g %5.0f  pick %-5s  K %5d -> P %5d   (N %s)' % (
        x['d'], x['name'][:26], x['age'], x['g'], x['pick'], round(x['orderk']), round(x['new']),
        ('%5d' % round(x['ordern'])) if x['ordern'] is not None else '   - '))
P()

# ---- 7 · the class mark ------------------------------------------------------------------------------------------
P('-' * 118)
P('7 · THE YEAR-1 CLASS MARK')
P('-' * 118)
w2 = classmark(LAM, 2006, 2016); cm = classmark(LAM)
P('   ORDER P : W2 registered basis %.4f   ·   cohort clock %.4f' % (w2, cm))
P('   ORDER N : W2 1.0604 · cohort 1.0324    ORDER K : W2 1.0513 · cohort 1.0324')
P('   the 1.03 floor: %+.4f    the 1.14 buy rail: %+.4f  %s' % (
    w2 - 1.03, w2 - 1.14, 'PASS' if w2 < 1.14 else 'FAIL'))
P()

# ---- 8 · the property test ---------------------------------------------------------------------------------------
P('-' * 118)
P('8 · THE PROPERTY TEST, RE-RUN ON THE ESTIMATED PRICES')
P('-' * 118)
S1 = json.load(open(os.path.join(os.path.dirname(HERE), 'order_n_2026-08-18', 'STEP1_N.json')))
rows = S1['rows']
for r in rows:
    m = MK[r['key']]
    r['sP'] = PB.perf_surplus_P(m, 2026, PG)
    r['R_p'] = (float(MN[r['key']]['cur']) / PL_F) / r['v0']
    r['chg_p'] = F_new(r['g'], r['sP'], LB.age_at(m, 2026), LAM)
P('   Rank correlation with surplus, within games bins. ORDER K reads its own age surplus; ORDER P')
P('   reads its own pedigree-conditional surplus. Both are the surplus that order actually uses.')
P('   %-10s %5s | %11s %11s | %11s %11s' % ('games bin', 'n', 'rho R  K', 'rho R  P', 'rho chg K', 'rho chg P'))
PROP = {}
for lo_, hi_ in LB.G_BINS_1:
    b = '%d-%d' % (lo_, hi_)
    sub = [r for r in rows if r['gbin'] == b and r['sP'] is not None]
    if len(sub) < 8: continue
    sp = np.array([r['sP'] for r in sub]); sn = np.array([r['ps'] for r in sub])
    P('   %-10s %5d | %+11.4f %+11.4f | %+11.4f %+11.4f' % (
        b, len(sub), spear(sn, np.array([r['R_k'] for r in sub])),
        spear(sp, np.array([r['R_p'] for r in sub])),
        spear(sn, np.array([r['charge_pct'] for r in sub])),
        spear(sp, np.array([r['chg_p'] for r in sub]))))
    PROP[b] = dict(n=len(sub))
P()
sub = sorted([r for r in rows if r['sP'] is not None], key=lambda r: r['sP'])
n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
P('   Charge paid, by PEDIGREE-CONDITIONAL surplus tercile, over the young window:')
for t, lab in enumerate(('below expectation', 'middle', 'above expectation')):
    pt = sub[cuts[t]:cuts[t + 1]]
    P('   %-20s n=%-4d mean s_P %+7.2f  mean g %5.1f | CURRENT %5.1f%%  ORDER P %5.1f%%' % (
        lab, len(pt), np.mean([r['sP'] for r in pt]), np.mean([r['g'] for r in pt]),
        100 * np.mean([r['charge_pct'] for r in pt]), 100 * np.mean([r['chg_p'] for r in pt])))
P()

json.dump(dict(mechanism=dict(M, LAMBDA=LAM, THETA_R=theta_r(LAM), TMAX=tmax_of(LAM), zero_at=ZERO,
                              age_gate=AGE_GATE),
               charge=CHG, ladder=LAD, balance=BAL, spear_pick_sN=rN, spear_pick_sP=rP,
               spear_pick_relief_N=sr_n, spear_pick_relief_P=sr_p,
               class_w2=w2, class_cohort=cm,
               board=dict(k=tot_k, n=tot_n, p=tot_p),
               vet=dict(n=len(mvv), churn=sum(abs(d) for _, d in mvv), net=sum(d for _, d in mvv)),
               movers=sorted(mv, key=lambda x: -abs(x['d']))[:150]),
          open(os.path.join(HERE, 'STEP4_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'STEP4_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STEP4_P.json and STEP4_P_out.txt; matrix tag PDERIV')
