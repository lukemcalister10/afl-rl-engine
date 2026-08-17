#!/usr/bin/env python3
"""ORDER J — THE JOINT SWEEP OVER THE AXES THE CORRECTED GATE LEAVES OPEN.

Order I's calibrator (o36_calibrate.py) is reused whole: the same legs, the same corrected age-fair
hindsight surface, the same objective, the same ruled constraints. The ONE change is that the
counterweight's knobs are no longer pinned to a single point by a zero-tolerance mature test — under
PREREG_J §2.2 they are free to move and are gated afterwards by J-TOL, measured on the live board.

This file is arithmetic only. It runs no engine and it decides nothing: it navigates. The standing
extended-338 decides G2 and G3 (PREREG_J §3.3).

The maths is Order I's `p1_of`, re-expressed as numpy over the whole population at once so 408,240
grid points are reachable. The identity is asserted against Order I's own scalar implementation on a
random sample of grid points before the sweep starts.
"""
import os, sys, json, math, time, itertools, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OUT = os.environ.get('O37_OUT', SP + '/O37_SWEEP.json')

L = json.load(open(SP + '/O36_LEGS.json'))
DOSES = L['doses']; POP = L['pop']; PLF = L['PLF']
LEGS = {float(k): v for k, v in L['legs'].items()}
CONT = {float(k): v for k, v in L['cont'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
N = len(POP)
print('ORDER J sweep — legs %d rows x %d doses (Order I leg identity: %s)' % (N, len(DOSES), L['leg_identity']))

# ---------------- the grid, exactly as PREREG_J §3.1 declares it -----------------------------------
G_DOSE = list(DOSES)
G_KAP = [0.15, 0.18, 0.20, 0.22, 0.24, 0.26, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
G_GU = [8.0, 10.0, 11.0, 12.0, 14.0, 16.0]
G_ETA = [0.00, 0.10, 0.20, 0.30, 0.35, 0.40, 0.41, 0.45, 0.50]
G_GD = [4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
G_REL = [0.80, 0.90, 1.00, 1.08, 1.20, 1.30]
REPAIR = (0.24, 11.0, 0.41, 14.0, 1.08)
NGRID = len(G_DOSE) * len(G_KAP) * len(G_GU) * len(G_ETA) * len(G_GD) * len(G_REL)
print('grid: %d x %d x %d x %d x %d x %d = %d points'
      % (len(G_DOSE), len(G_KAP), len(G_GU), len(G_ETA), len(G_GD), len(G_REL), NGRID))

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


# ---------------- the corrected age-fair hindsight surface (Order I control 1, unchanged) ----------
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
print('\nCONTROL 1 — corrected age-fair surface vs REMIX_32R.json: W %.10f vs %.10f (dev %.2e) · '
      'cells %.2e · terciles %.2e  -> %s'
      % (W_HIND, CS['W_hind_age'], d1, d2, d3, 'EXACT' if max(d1, d2, d3) < 1e-9 else 'DEVIATION'))
assert max(d1, d2, d3) < 1e-9, 'ORDER J HALT: the instrument does not reproduce REMIX_32R'
print('   W 90%% CI [%.4f, %.4f]  ·  5-9g risers %.4f  ·  5-9g sub-expectation %.4f'
      % (W_LO, W_HI, REAL_TERC['5-9/riser'], REAL_TERC['5-9/poor']))

# ---------------- vectorised leg arrays -------------------------------------------------------------
KEYS = [q['key'] for q in POP]
IDX = {k: i for i, k in enumerate(KEYS)}
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

HMASK = np.array([1.0 if q['yr'] in CLASSES_H6 else 0.0 for q in POP])
HIDX = np.where(HMASK > 0)[0]
# rows_h order == [q for y in CLASSES_H6 for q in POP if q['yr']==y]; build the permutation
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
CLROW = MH.T @ np.arange(len(CLASSES_H6))          # class index of each rows_h entry

AH = np.column_stack([np.ones(len(ORD)), PRA, PD])
PINV = np.linalg.pinv(AH)                          # 3 x m — W's OLS solved once
Ybar = Yh.mean(); Yc = Yh - Ybar
CELLM = {}
for b in ('0', '1-4', '5-9', '10-15', '16+'):
    m = np.array([1.0 if bucket(r['g1']) == b else 0.0 for r in rows_h]); CELLM[b] = (m, m.sum())
TERCM = {}
for tk, ks in TERC_KEYS.items():
    m = np.array([1.0 if r['key'] in ks else 0.0 for r in rows_h]); TERCM[tk] = (m, m.sum())

MU = {gu: np.where(gv > 0, (gv / gu) * np.exp(1.0 - gv / gu), 0.0) for gu in G_GU}
MD = {gd: np.where(gv > 0, (gv / gd) * np.exp(1.0 - gv / gd), 0.0) for gd in G_GD}


def Dvec(lrel, fade):
    Df = Dft if fade == 'tall' else Dfp
    return np.where(Df < 1.0, np.minimum(1.0, Df * (1.0 + lrel * sig)), Df)


def p1_vec(dose, kap, gu, eta, gd, lrel, fade):
    D = Dvec(lrel, fade); mu = MU[gu]; md = MD[gd]
    r2 = rho + kap * mu * (1.0 - rho)
    ped = (D * (1.0 - r2) + Phi * bet * r2) * V0 * np.maximum(0.0, 1.0 - eta * md)
    return r2 * PHAT[dose] + ped + kap * mu * (1.0 - rho) * agp * 20.0 * PLF


def metrics(dose, kap, gu, eta, gd, lrel, fade='tall', full=False):
    p1 = p1_vec(dose, kap, gu, eta, gd, lrel, fade)
    Rc = (MC @ p1) / MCden
    bandR = (MB @ p1) / MBden
    ph = p1[ORD]
    x = ph / (MHn @ ph)[CLROW.astype(int)]
    b = PINV @ x
    W = float(b[1] / b[2])
    xb = x.mean(); xc = x - xb
    slope = float((xc @ Yc) / (xc @ xc))
    obj = 0.0; cells = {}; terc = {}
    for bnm, (m, n) in CELLM.items():
        pr = float((m @ x) / n); cells[bnm] = pr; obj += n * (REAL_CELLS[bnm] - pr) ** 2
    for tk, (m, n) in TERCM.items():
        pr = float((m @ x) / n); terc[tk] = pr
        if tk.startswith('5-9'):
            obj += n * (REAL_TERC[tk] - pr) ** 2
    o = dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, lam_rel=lrel, fade=fade,
             obj=float(obj), slope=slope, W=W,
             mean_0515=float(Rc[:11].mean()), max_class=float(Rc.max()),
             max_class_year=int(CLY[int(Rc.argmax())]), min_class=float(Rc.min()),
             band_R={b: float(v) for b, v in zip(BANDS5, bandR)})
    if full:
        o['per_class'] = {str(y): float(v) for y, v in zip(CLY, Rc)}
        o['cells'] = cells; o['terciles'] = terc
    return o


# ---------------- IDENTITY CONTROL: the vector form must equal Order I's scalar form ---------------
def p1_scalar(Lg, kap, gu, eta, gd, lrel, fade):
    g = Lg['g']
    Df = Lg['Dfade'] if fade == 'tall' else Lg['Dfade_pool']
    D = min(1.0, Df * (1.0 + lrel * Lg['sig'])) if Df < 1.0 else Df
    if g <= 0:
        return D * Lg['V0']
    mu = (g / gu) * math.exp(1.0 - g / gu)
    md = (g / gd) * math.exp(1.0 - g / gd)
    rb = Lg['rho']
    r2 = rb + kap * mu * (1.0 - rb)
    ped = (D * (1.0 - r2) + Lg['Phi'] * Lg['beta'] * r2) * Lg['V0'] * max(0.0, 1.0 - eta * md)
    return r2 * Lg['Phat'] + ped + kap * mu * (1.0 - rb) * Lg['agap'] * 20.0 * PLF


RS = np.random.default_rng(7)
worst = 0.0
for _ in range(12):
    pt = (float(RS.choice(G_DOSE)), float(RS.choice(G_KAP)), float(RS.choice(G_GU)),
          float(RS.choice(G_ETA)), float(RS.choice(G_GD)), float(RS.choice(G_REL)))
    fd = 'tall' if RS.random() < 0.5 else 'pool'
    vv = p1_vec(*pt, fd)
    sv = np.array([p1_scalar(LEGS[pt[0]][k], *pt[1:], fd) for k in KEYS])
    worst = max(worst, float(np.max(np.abs(vv - sv))))
print('\nCONTROL 2 — the vectorised price equals ORDER I\'s scalar `p1_of` on 12 random grid points '
      'x %d rows: worst absolute deviation %.3e  -> %s' % (N, worst, 'EXACT' if worst < 1e-9 else 'FAIL'))
assert worst < 1e-9, 'ORDER J HALT: the vectorised calibrator is not Order I\'s calibrator'

CANDPT = metrics(0.0, *REPAIR, fade='pool', full=True)
print('\nCONTROL 3 — the LANDING CANDIDATE on this instrument (dose 0, repair knobs, POOLED fade):')
print('   class mark mean_0515 = %.4f   (the Order-D wire\'s own W2 number of record: 1.0421)'
      % CANDPT['mean_0515'])
print('   max class %.4f on %s · slope %.4f · W %.4f · bands %s'
      % (CANDPT['max_class'], CANDPT['max_class_year'], CANDPT['slope'], CANDPT['W'],
         {k: '%+.2f%%' % (100 * (v - 1)) for k, v in CANDPT['band_R'].items()}))
assert abs(CANDPT['mean_0515'] - 1.0421) < 5e-4, 'ORDER J HALT: the landing-candidate control moved'
FADEONLY = metrics(0.0, *REPAIR, fade='tall', full=True)
print('\nCONTROL 4 — the RULED TALL FACTOR ALONE (dose 0, repair knobs, tall exponent):')
print('   class mark %.4f (%+.4f) · max class %.4f on %s · bands %s'
      % (FADEONLY['mean_0515'], FADEONLY['mean_0515'] - CANDPT['mean_0515'], FADEONLY['max_class'],
         FADEONLY['max_class_year'],
         {k: '%+.2f%%' % (100 * (v - 1)) for k, v in FADEONLY['band_R'].items()}))

# ---------------- the ruled continuity + monotonicity objects, precomputed -------------------------
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
print('\nruled at-bar continuity object: %d at-bar rows per dose' % len(CROWS[DOSES[0]]))

MU_G = {gu: np.where(GG > 0, (GG / gu) * np.exp(1.0 - GG / gu), 0.0) for gu in G_GU}
MD_G = {gd: np.where(GG > 0, (GG / gd) * np.exp(1.0 - GG / gd), 0.0) for gd in G_GD}


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
print('rho32 monotonicity: %d of %d (kappa, gamma_u) pairs pass'
      % (sum(MONO.values()), len(MONO)))

# ---------------- THE SWEEP ------------------------------------------------------------------------
FAIL = collections.Counter()
ALL = []
T0 = time.time()
for dose in G_DOSE:
    for lrel in G_REL:
        D = Dvec(lrel, 'tall')
        for gu in G_GU:
            mu = MU[gu]
            for kap in G_KAP:
                if not MONO[(kap, gu)]:
                    FAIL['mono'] += len(G_ETA) * len(G_GD); continue
                r2 = rho + kap * mu * (1.0 - rho)
                base_prod = r2 * PHAT[dose] + kap * mu * (1.0 - rho) * agp * 20.0 * PLF
                pedbase = (D * (1.0 - r2) + Phi * bet * r2) * V0
                for gd in G_GD:
                    md = MD[gd]
                    for eta in G_ETA:
                        p1 = base_prod + pedbase * np.maximum(0.0, 1.0 - eta * md)
                        Rc = (MC @ p1) / MCden
                        mx = float(Rc.max())
                        if mx > 1.139:
                            FAIL['1.14line'] += 1; continue
                        ph = p1[ORD]
                        x = ph / (MHn @ ph)[CLROW.astype(int)]
                        b = PINV @ x
                        W = float(b[1] / b[2])
                        if not (W_LO <= W <= W_HI):
                            FAIL['W'] += 1; continue
                        xb = x.mean(); xc = x - xb
                        slope = float((xc @ Yc) / (xc @ xc))
                        if not (0.885 <= slope <= 1.115):
                            FAIL['slope'] += 1; continue
                        if not continuity_ok(dose, kap, gu, eta, gd, lrel):
                            FAIL['continuity'] += 1; continue
                        bandR = (MB @ p1) / MBden
                        obj = 0.0
                        for bnm, (m, n) in CELLM.items():
                            obj += n * (REAL_CELLS[bnm] - float((m @ x) / n)) ** 2
                        for tk, (m, n) in TERCM.items():
                            if tk.startswith('5-9'):
                                obj += n * (REAL_TERC[tk] - float((m @ x) / n)) ** 2
                        ALL.append(dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd,
                                        lam_rel=lrel, obj=float(obj), slope=slope, W=W,
                                        mean_0515=float(Rc[:11].mean()), max_class=mx,
                                        max_class_year=int(CLY[int(Rc.argmax())]),
                                        band_R={bn: float(v) for bn, v in zip(BANDS5, bandR)}))
    print('  dose %.2f done — %d ruled-feasible so far  (%.0fs)' % (dose, len(ALL), time.time() - T0), flush=True)

print('\nswept %d grid points in %.0fs' % (NGRID, time.time() - T0))
print('ruled-constraint failures: %s' % dict(FAIL))
print('points feasible on the RULED constraints: %d of %d' % (len(ALL), NGRID))

# ---------------- the owner's laws, on the calibrator (navigation only) ----------------------------
def laws(M):
    f = []
    if not (M['mean_0515'] >= 1.03): f.append('G1floor')
    if not (M['mean_0515'] < 1.14): f.append('G1rail')
    if max(M['band_R'].values()) > 1.14: f.append('G3')
    if M['band_R']['31-40'] <= CANDPT['band_R']['31-40']: f.append('G2a-3140')
    if M['band_R']['41-64'] <= CANDPT['band_R']['41-64']: f.append('G2a-4164')
    return f


def laws_asp(M):
    f = []
    if M['band_R']['31-40'] < 1.0: f.append('G2asp-3140')
    if M['band_R']['41-64'] < 1.0: f.append('G2asp-4164')
    return f


LAWF = collections.Counter()
lawok = []
for M in ALL:
    M['law_fails'] = laws(M); M['asp_fails'] = laws_asp(M)
    for x in M['law_fails']: LAWF[x] += 1
    if not M['law_fails']:
        lawok.append(M)
print('\nowner-law failures over the ruled-feasible set: %s' % dict(LAWF))
print('points that ALSO satisfy G1 + G2-improve + G3 on the calibrator: %d' % len(lawok))
full = [M for M in lawok if not M['asp_fails']]
print('points that ALSO satisfy G2\'s NO-SELL-RED aspiration: %d' % len(full))

lawok.sort(key=lambda m: (m['obj'], m['dose'], abs(m['kappa'] - 0.24)))
full.sort(key=lambda m: (m['obj'], m['dose'], abs(m['kappa'] - 0.24)))

print('\n-- TOP 25 BY THE SELECTION LAW (min corrected-surface SSE), G1+G2-improve+G3 satisfied --')
print('  %5s %6s %5s %5s %5s %5s | %8s %7s %7s | %s' %
      ('dose', 'kappa', 'gu', 'eta', 'gd', 'rel', 'class', 'maxcls', 'SSE', 'five bands yr0->1'))
for M in (full or lawok)[:25]:
    print('  %5.2f %6.2f %5.0f %5.2f %5.0f %5.2f | %8.4f %7.4f %7.2f | %s'
          % (M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['lam_rel'],
             M['mean_0515'], M['max_class'], M['obj'],
             ' '.join('%+6.2f%%' % (100 * (M['band_R'][b] - 1)) for b in BANDS5)))

json.dump(dict(order='ORDER J — the joint sweep under the corrected gate',
               grid=dict(dose=G_DOSE, kappa=G_KAP, gamma_u=G_GU, eta=G_ETA, gamma_d=G_GD, lam_rel=G_REL),
               n_grid=NGRID, W_hind=W_HIND, W_ci=[W_LO, W_HI],
               real_cells=REAL_CELLS, real_terc=REAL_TERC,
               control_landing=CANDPT, control_tall_only=FADEONLY,
               fail_counts=dict(FAIL), law_fail_counts=dict(LAWF),
               n_ruled_feasible=len(ALL), n_law_ok=len(lawok), n_aspiration_ok=len(full),
               top_law_ok=lawok[:400], top_aspiration_ok=full[:400],
               ruled_feasible=ALL),
          open(OUT, 'w'), default=float)
print('\nwritten: %s' % OUT)
