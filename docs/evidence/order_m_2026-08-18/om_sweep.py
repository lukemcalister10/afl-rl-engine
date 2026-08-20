#!/usr/bin/env python3
"""ORDER M — THE SWEEP WITH ETA PINNED TO ZERO.

ORDER J's o37_sweep.py, REUSED. Not rebuilt. Same legs (ORDER I's O36_LEGS.json), same corrected
age-fair hindsight surface, same ruled-constraint objects, same controls, same arithmetic. The
differences, all declared in PREREG_M.md:

  1. eta is PINNED to 0.0 by the owner's ruling. It is not an axis.
  2. gamma_d is INERT at eta = 0 (it multiplies a term that is multiplied by eta). It is held at 14
     and reported as inert, never swept.
  3. EVERY point is scored on EVERY constraint, instead of short-circuiting on the first failure.
     That is what makes a trade-off curve possible: the order asks what breaks FIRST and AT WHAT DOSE,
     and a short-circuiting sweep cannot answer that.
  4. The owner's laws and the inherited ruled constraints are recorded SEPARATELY, so "this breaks a
     law of yours" is never confused with "this leaves the calibrator's fitted band".

This file is arithmetic. It runs no build. It navigates and it decides nothing.
"""
import os, sys, json, math, time, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OUT = os.environ.get('OM_OUT', os.path.join(HERE, 'SWEEP_M.json'))
L = []


def P(s=''):
    print(s, flush=True); L.append(str(s))


LG = json.load(open(SP + '/O36_LEGS.json'))
DOSES = LG['doses']; POP = LG['pop']; PLF = LG['PLF']
LEGS = {float(k): v for k, v in LG['legs'].items()}
CONT = {float(k): v for k, v in LG['cont'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
N = len(POP)
P('ORDER M sweep — ORDER I legs, %d rows x %d doses (leg identity: %s)' % (N, len(DOSES), LG['leg_identity']))

# ---------------- the grid, exactly as PREREG_M §1.2 declares it -----------------------------------
G_DOSE = list(DOSES)
G_KAP = [0.15, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
G_GU = [8.0, 10.0, 11.0, 12.0, 14.0, 16.0]
G_ETA = [0.00]                      # PINNED by the owner's ruling
G_GD = [14.0]                       # INERT at eta = 0
G_REL = [0.80, 0.90, 1.00, 1.08, 1.20, 1.30]
REPAIR = (0.24, 11.0, 0.41, 14.0, 1.08)
ORDERK = (0.40, 0.20, 8.0, 0.50, 14.0, 1.08)
NGRID = len(G_DOSE) * len(G_KAP) * len(G_GU) * len(G_ETA) * len(G_GD) * len(G_REL)
P('grid: dose %d x kappa %d x gamma_u %d x lam_rel %d = %d points   (eta pinned 0, gamma_d inert)'
  % (len(G_DOSE), len(G_KAP), len(G_GU), len(G_REL), NGRID))

O31_TAU_RHO = 29.194253560287144
O31_B_RHO = 0.8015424473253033
rho_base = lambda g: 0.0 if g <= 0.0 else 1.0 - math.exp(-((g / O31_TAU_RHO) ** O31_B_RHO))
CLASSES_H6 = list(range(2005, 2019))
BANDS5 = ['1-10', '11-20', '21-30', '31-40', '41-64']


def nd_band(pk):
    if pk is None: return None
    for hi, nm in ((10, '1-10'), (20, '11-20'), (30, '21-30'), (40, '31-40'), (64, '41-64')):
        if pk <= hi: return nm
    return None


def bucket(g):
    if g == 0: return '0'
    if g <= 4: return '1-4'
    if g <= 9: return '5-9'
    if g <= 15: return '10-15'
    return '16+'


def ols(Xm, yv):
    A1 = np.column_stack([np.ones(len(yv))] + list(Xm))
    b, *_ = np.linalg.lstsq(A1, yv, rcond=None)
    return b


# ---------------- the corrected age-fair hindsight surface (ORDER I control 1, unchanged) ----------
rows_h = []
for y in CLASSES_H6:
    rows = [q for q in POP if q['yr'] == y]
    mdv = np.mean([q['dv1_h6'] for q in rows])
    mprodA = np.mean([q['sv1_age'] for q in rows]) or 1.0
    mped = np.mean([q['v0'] for q in rows])
    for q in rows:
        rows_h.append(dict(key=q['key'], yr=y, g1=q['g1'], y=q['dv1_h6'] / mdv,
                           prodA=q['sv1_age'] / mprodA, ped=q['v0'] / mped))
Yh = np.array([r['y'] for r in rows_h])
PRA = np.array([r['prodA'] for r in rows_h])
PD = np.array([r['ped'] for r in rows_h])
bh = ols([PRA, PD], Yh)
W_HIND = float(bh[1] / bh[2])
RNG = np.random.default_rng(33)
wb = []
for _ in range(1000):
    i = RNG.integers(0, len(rows_h), len(rows_h))
    t = ols([PRA[i], PD[i]], Yh[i])
    wb.append(t[1] / t[2])
W_LO, W_HI = float(np.percentile(wb, 5)), float(np.percentile(wb, 95))
REAL_CELLS = {b: float(np.mean([r['y'] for r in rows_h if bucket(r['g1']) == b]))
              for b in ('0', '1-4', '5-9', '10-15', '16+')}
TERC_KEYS = {}; REAL_TERC = {}
for b in ('1-4', '5-9'):
    rs = sorted([r for r in rows_h if bucket(r['g1']) == b], key=lambda r: r['prodA'])
    n3 = len(rs) // 3
    for nm, seg in (('poor', rs[:n3]), ('mid', rs[n3:2 * n3]), ('riser', rs[2 * n3:])):
        TERC_KEYS['%s/%s' % (b, nm)] = set(r['key'] for r in seg)
        REAL_TERC['%s/%s' % (b, nm)] = float(np.mean([r['y'] for r in seg]))

REF = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'REMIX_32R.json')))
CS = REF['corrected_surface']
d1 = abs(W_HIND - CS['W_hind_age'])
d2 = max(abs(REAL_CELLS[b] - CS['cells_realized'][b]) for b in REAL_CELLS)
d3 = max(abs(REAL_TERC[t] - CS['terciles_realized'][t]) for t in REAL_TERC)
P('\nCONTROL 1 (M6) — corrected age-fair surface vs REMIX_32R.json: W %.10f vs %.10f (dev %.2e) · '
  'cells %.2e · terciles %.2e  -> %s'
  % (W_HIND, CS['W_hind_age'], d1, d2, d3, 'EXACT' if max(d1, d2, d3) < 1e-9 else 'DEVIATION'))
assert max(d1, d2, d3) < 1e-9, 'ORDER M HALT (M6 FIRES): the instrument does not reproduce REMIX_32R'

# ---------------- vectorised leg arrays -------------------------------------------------------------
KEYS = [q['key'] for q in POP]
A0 = LEGS[DOSES[0]]
gv = np.array([A0[k]['g'] for k in KEYS])
rho = np.array([A0[k]['rho'] for k in KEYS])
Dft = np.array([A0[k]['Dfade'] for k in KEYS])
Dfp = np.array([A0[k]['Dfade_pool'] for k in KEYS])
sig = np.array([A0[k]['sig'] for k in KEYS])
Phi = np.array([A0[k]['Phi'] for k in KEYS])
bet = np.array([A0[k]['beta'] for k in KEYS])
V0 = np.array([A0[k]['V0'] for k in KEYS])
agp = np.array([A0[k]['agap'] for k in KEYS])
PHAT = {d: np.array([LEGS[d][k]['Phat'] for k in KEYS]) for d in DOSES}
v0p = np.array([q['v0'] for q in POP])
yrv = np.array([q['yr'] for q in POP])

CLY = list(range(2005, 2022))
MC = np.zeros((len(CLY), N))
for i, y in enumerate(CLY):
    MC[i] = (yrv == y)
MCden = MC @ v0p
MB = np.zeros((5, N))
for i, bnm in enumerate(BANDS5):
    MB[i] = np.array([1.0 if (q['arm'] == 'ND' and nd_band(q['pick']) == bnm) else 0.0 for q in POP])
MBden = MB @ v0p

ORD = []
for y in CLASSES_H6:
    for j, q in enumerate(POP):
        if q['yr'] == y:
            ORD.append(j)
ORD = np.array(ORD)
assert [KEYS[j] for j in ORD] == [r['key'] for r in rows_h]
MH = np.zeros((len(CLASSES_H6), len(ORD)))
for i, y in enumerate(CLASSES_H6):
    MH[i] = np.array([1.0 if rows_h[j]['yr'] == y else 0.0 for j in range(len(ORD))])
MHn = MH / MH.sum(axis=1, keepdims=True)
CLROW = (MH.T @ np.arange(len(CLASSES_H6))).astype(int)
AH = np.column_stack([np.ones(len(ORD)), PRA, PD])
PINV = np.linalg.pinv(AH)
Ybar = Yh.mean(); Yc = Yh - Ybar
CELLM = {}
for b in ('0', '1-4', '5-9', '10-15', '16+'):
    m = np.array([1.0 if bucket(r['g1']) == b else 0.0 for r in rows_h]); CELLM[b] = (m, m.sum())
TERCM = {}
for tk, ks in TERC_KEYS.items():
    m = np.array([1.0 if r['key'] in ks else 0.0 for r in rows_h]); TERCM[tk] = (m, m.sum())

ALLGU = sorted(set(G_GU) | {11.0, 8.0})
ALLGD = sorted(set(G_GD) | {14.0})
MU = {gu: np.where(gv > 0, (gv / gu) * np.exp(1.0 - gv / gu), 0.0) for gu in ALLGU}
MD = {gd: np.where(gv > 0, (gv / gd) * np.exp(1.0 - gv / gd), 0.0) for gd in ALLGD}


def Dvec(lrel, fade):
    Df = Dft if fade == 'tall' else Dfp
    return np.where(Df < 1.0, np.minimum(1.0, Df * (1.0 + lrel * sig)), Df)


def p1_vec(dose, kap, gu, eta, gd, lrel, fade):
    D = Dvec(lrel, fade); mu = MU[gu]; md = MD[gd]
    r2 = rho + kap * mu * (1.0 - rho)
    ped = (D * (1.0 - r2) + Phi * bet * r2) * V0 * np.maximum(0.0, 1.0 - eta * md)
    return r2 * PHAT[dose] + ped + kap * mu * (1.0 - rho) * agp * 20.0 * PLF


def metrics(dose, kap, gu, eta, gd, lrel, fade='tall'):
    p1 = p1_vec(dose, kap, gu, eta, gd, lrel, fade)
    Rc = (MC @ p1) / MCden
    bandR = (MB @ p1) / MBden
    ph = p1[ORD]
    x = ph / (MHn @ ph)[CLROW]
    b = PINV @ x
    W = float(b[1] / b[2])
    xb = x.mean(); xc = x - xb
    slope = float((xc @ Yc) / (xc @ xc))
    obj = 0.0
    for bnm, (m, n) in CELLM.items():
        obj += n * (REAL_CELLS[bnm] - float((m @ x) / n)) ** 2
    for tk, (m, n) in TERCM.items():
        if tk.startswith('5-9'):
            obj += n * (REAL_TERC[tk] - float((m @ x) / n)) ** 2
    return dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, lam_rel=lrel,
                obj=float(obj), slope=slope, W=W,
                mean_0515=float(Rc[:11].mean()), max_class=float(Rc.max()),
                max_class_year=int(CLY[int(Rc.argmax())]),
                band_R={b: float(v) for b, v in zip(BANDS5, bandR)})


# ---------------- CONTROLS ---------------------------------------------------------------------------
CANDPT = metrics(0.0, *REPAIR, fade='pool')
P('\nCONTROL 2 (M6) — THE LANDING CANDIDATE on this instrument (dose 0, repair knobs, POOLED fade):')
P('   class mark %.4f  (the W2 number of record: 1.0421) · max class %.4f · bands %s'
  % (CANDPT['mean_0515'], CANDPT['max_class'],
     ' '.join('%s %+.2f%%' % (b, 100 * (CANDPT['band_R'][b] - 1)) for b in BANDS5)))
assert abs(CANDPT['mean_0515'] - 1.0421) < 5e-4, 'ORDER M HALT (M6 FIRES): the landing control moved'
KPT = metrics(*ORDERK, fade='tall')
P('\nCONTROL 3 — ORDER K\'s RULED SETTING on this instrument (dose .40 k .20 gu 8 eta .50 gd 14 rel 1.08):')
P('   class %.4f · max class %.4f on %d · slope %.3f · W %.3f · bands %s'
  % (KPT['mean_0515'], KPT['max_class'], KPT['max_class_year'], KPT['slope'], KPT['W'],
     ' '.join('%s %+.2f%%' % (b, 100 * (KPT['band_R'][b] - 1)) for b in BANDS5)))
P('   (ORDER K published 1.0519 / 1.1385 here; the built board reads class 1.0513 on the registered')
P('    W2 basis and picks 1-10 +8.22%. The calibrator runs hot on the young bands — ORDER J said so')
P('    in advance and ORDER K measured it. NOTHING below is a decision.)')
K_ETA0 = metrics(0.40, 0.20, 8.0, 0.0, 14.0, 1.08, fade='tall')
P('\nCONTROL 4 — ORDER K\'s SETTING WITH ETA SET TO ZERO AND NOTHING ELSE CHANGED:')
P('   class %.4f (%+.4f) · max class %.4f (%+.4f) · bands %s'
  % (K_ETA0['mean_0515'], K_ETA0['mean_0515'] - KPT['mean_0515'],
     K_ETA0['max_class'], K_ETA0['max_class'] - KPT['max_class'],
     ' '.join('%s %+.2f%%' % (b, 100 * (K_ETA0['band_R'][b] - 1)) for b in BANDS5)))

# ---------------- the ruled continuity + monotonicity objects --------------------------------------
import io, contextlib
os.environ.update(RL_O31='1', RL_O32='1', RL_O32_STAGE='5', RL_O36='1', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as _MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
PHIF, BETF = NSE['phi31'], NSE['beta31']
GG = np.arange(0, 21, dtype=float)
RHO_G = np.array([rho_base(g) for g in GG])
CROWS = {}
for dose in DOSES:
    lst = []
    for c in CONT[dose]:
        if not c['atbar']:
            continue
        pb = np.array([float(PHIF(int(g), c['s'], c['pool'])) * float(BETF(int(g), c['pool'])) for g in GG])
        lst.append((c['Dfade'], c['Dfade_pool'], c['sig'], c['Phat'], c['V0'], c['agap'], pb))
    CROWS[dose] = lst
P('\nruled at-bar continuity object: %d at-bar rows per dose' % len(CROWS[DOSES[0]]))
MU_G = {gu: np.where(GG > 0, (GG / gu) * np.exp(1.0 - GG / gu), 0.0) for gu in ALLGU}
MD_G = {gd: np.where(GG > 0, (GG / gd) * np.exp(1.0 - GG / gd), 0.0) for gd in ALLGD}


def continuity_ok(dose, kap, gu, eta, gd, lrel, fade='tall'):
    mu = MU_G[gu]; md = MD_G[gd]
    r2 = RHO_G + kap * mu * (1.0 - RHO_G)
    mix = np.maximum(0.0, 1.0 - eta * md)
    for (Dt, Dp, sg, Ph, v0, ag, pb) in CROWS[dose]:
        Df = Dt if fade == 'tall' else Dp
        D = min(1.0, Df * (1.0 + lrel * sg)) if Df < 1.0 else Df
        pu = r2 * Ph + (D * (1.0 - r2) + pb * r2) * v0 * mix + kap * mu * (1.0 - RHO_G) * ag * 20.0 * PLF
        if np.any(np.diff(pu) < -1e-9):
            return False
    return True


GGM = np.arange(0.0, 300.25, 0.25)
RHO_M = np.array([rho_base(g) for g in GGM])
MONO = {}
for kap in G_KAP:
    for gu in G_GU:
        mm = np.where(GGM > 0, (GGM / gu) * np.exp(1.0 - GGM / gu), 0.0)
        r = RHO_M + kap * mm * (1.0 - RHO_M)
        MONO[(kap, gu)] = bool(np.all(np.diff(r) >= -1e-12) and np.all(r < 1.0 + 1e-12))
P('rho32 monotonicity: %d of %d (kappa, gamma_u) pairs pass' % (sum(MONO.values()), len(MONO)))

# ---------------- THE SWEEP — every point scored on every constraint --------------------------------
KBAND = KPT['band_R']
ALL = []
T0 = time.time()
for dose in G_DOSE:
    for lrel in G_REL:
        for gu in G_GU:
            for kap in G_KAP:
                for eta in G_ETA:
                    for gd in G_GD:
                        M = metrics(dose, kap, gu, eta, gd, lrel, fade='tall')
                        rf = []
                        if not MONO[(kap, gu)]: rf.append('rho32-mono')
                        if M['max_class'] > 1.139: rf.append('maxclass-1.139')
                        if not (W_LO <= M['W'] <= W_HI): rf.append('W-band')
                        if not (0.885 <= M['slope'] <= 1.115): rf.append('slope-band')
                        if not continuity_ok(dose, kap, gu, eta, gd, lrel): rf.append('at-bar-continuity')
                        lf = []
                        if M['mean_0515'] < 1.03: lf.append('G1-floor')
                        if M['mean_0515'] >= 1.14: lf.append('G1-rail')
                        if max(M['band_R'].values()) > 1.14: lf.append('G3-band')
                        if M['band_R']['31-40'] <= KBAND['31-40']: lf.append('G2-3140-vsK')
                        if M['band_R']['41-64'] <= KBAND['41-64']: lf.append('G2-4164-vsK')
                        if M['band_R']['1-10'] < KBAND['1-10'] - 0.01: lf.append('G4-110')
                        M['ruled_fails'] = rf; M['law_fails'] = lf
                        ALL.append(M)
    P('  dose %.2f done (%.0fs)' % (dose, time.time() - T0))
P('\nswept %d points in %.0fs' % (len(ALL), time.time() - T0))

RC = collections.Counter()
LC = collections.Counter()
for M in ALL:
    for x in M['ruled_fails']: RC[x] += 1
    for x in M['law_fails']: LC[x] += 1
P('\nRULED-CONSTRAINT failure counts over the whole eta=0 grid (%d points): %s' % (len(ALL), dict(RC)))
P('OWNER-LAW      failure counts over the whole eta=0 grid (%d points): %s' % (len(ALL), dict(LC)))
RULED = [M for M in ALL if not M['ruled_fails']]
LAWOK = [M for M in ALL if not M['law_fails']]
BOTH = [M for M in ALL if not M['ruled_fails'] and not M['law_fails']]
P('\npoints feasible on the INHERITED RULED CONSTRAINTS : %d of %d' % (len(RULED), len(ALL)))
P('points feasible on the OWNER\'S LAWS                : %d of %d' % (len(LAWOK), len(ALL)))
P('points feasible on BOTH                            : %d of %d' % (len(BOTH), len(ALL)))

P('\n-- WHAT BREAKS FIRST, AS THE DOSE RISES (best point at each dose) --')
P('  %5s | %6s %6s %6s %6s | %8s %8s | %s' %
  ('dose', 'ruled', 'lawok', 'both', 'n', 'bestcls', 'minmaxcl', 'first breach seen at this dose'))
DOSECURVE = []
for dose in G_DOSE:
    sub = [M for M in ALL if M['dose'] == dose]
    r = [M for M in sub if not M['ruled_fails']]
    l = [M for M in sub if not M['law_fails']]
    b = [M for M in sub if not M['ruled_fails'] and not M['law_fails']]
    bestcls = max(M['mean_0515'] for M in sub)
    minmax = min(M['max_class'] for M in sub)
    fc = collections.Counter()
    for M in sub:
        for x in M['ruled_fails'] + M['law_fails']: fc[x] += 1
    DOSECURVE.append(dict(dose=dose, n=len(sub), n_ruled=len(r), n_law=len(l), n_both=len(b),
                          best_class=bestcls, min_maxclass=minmax, fails=dict(fc)))
    P('  %5.2f | %6d %6d %6d %6d | %8.4f %8.4f | %s'
      % (dose, len(r), len(l), len(b), len(sub), bestcls, minmax,
         ', '.join('%s %d' % (k, v) for k, v in fc.most_common(4))))

if BOTH:
    BOTH.sort(key=lambda m: (m['obj'], -m['dose']))
    P('\n-- TOP 30 POINTS LEGAL ON BOTH, ordered by the inherited selection law (min corrected SSE) --')
    P('  %5s %6s %5s %5s | %8s %7s %6s %6s | %s'
      % ('dose', 'kappa', 'gu', 'rel', 'class', 'maxcls', 'slope', 'W', 'five bands yr0->1'))
    for M in BOTH[:30]:
        P('  %5.2f %6.2f %5.0f %5.2f | %8.4f %7.4f %6.3f %6.3f | %s'
          % (M['dose'], M['kappa'], M['gamma_u'], M['lam_rel'], M['mean_0515'], M['max_class'],
             M['slope'], M['W'], ' '.join('%+6.2f%%' % (100 * (M['band_R'][b] - 1)) for b in BANDS5)))
else:
    P('\n-- NO POINT IN THE DECLARED GRID IS LEGAL ON BOTH SETS. --')

if LAWOK:
    LAWOK.sort(key=lambda m: (-m['dose'], m['obj']))
    P('\n-- TOP 30 POINTS LEGAL ON THE OWNER\'S LAWS (ruled constraints shown, not required) --')
    P('  %5s %6s %5s %5s | %8s %7s %6s %6s | %-34s | %s'
      % ('dose', 'kappa', 'gu', 'rel', 'class', 'maxcls', 'slope', 'W', 'five bands yr0->1', 'ruled fails'))
    for M in LAWOK[:30]:
        P('  %5.2f %6.2f %5.0f %5.2f | %8.4f %7.4f %6.3f %6.3f | %-34s | %s'
          % (M['dose'], M['kappa'], M['gamma_u'], M['lam_rel'], M['mean_0515'], M['max_class'],
             M['slope'], M['W'], ' '.join('%+6.2f%%' % (100 * (M['band_R'][b] - 1)) for b in BANDS5),
             ','.join(M['ruled_fails']) or '-'))

json.dump(dict(order='ORDER M — the eta=0 sweep',
               grid=dict(dose=G_DOSE, kappa=G_KAP, gamma_u=G_GU, eta=G_ETA, gamma_d=G_GD, lam_rel=G_REL),
               n_grid=len(ALL), W_hind=W_HIND, W_ci=[W_LO, W_HI],
               control_landing=CANDPT, control_orderK=KPT, control_orderK_eta0=K_ETA0,
               ruled_fail_counts=dict(RC), law_fail_counts=dict(LC),
               n_ruled_ok=len(RULED), n_law_ok=len(LAWOK), n_both=len(BOTH),
               dose_curve=DOSECURVE, top_both=BOTH[:200], top_lawok=LAWOK[:200], points=ALL),
          open(OUT, 'w'), default=float)
open(os.path.join(HERE, 'SWEEP_M_out.txt'), 'w').write('\n'.join(L) + '\n')
P('\nwritten: %s and SWEEP_M_out.txt' % OUT)
