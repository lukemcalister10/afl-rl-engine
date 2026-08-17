#!/usr/bin/env python3
"""ORDER I — STEP 2: THE ONE JOINT CALIBRATION.

Plain words. There is one calibration, not three. It chooses the S1 dose, the two re-mix knobs and
their two shapes, and the selection relief TOGETHER, because they push on the same rows in opposite
directions: S1 lifts every young player who produces anything, and the re-mix decides who keeps the
lift. Choosing the dose first and the counterweight afterwards would be choosing twice.

What is fixed before any number is looked at (PREREG_I.md §3):
  * the RULED feasibility constraints — rho32 monotone, the at-bar continuity object, the hindsight
    weight W inside the corrected 90% CI, the calibration slope band, no class above 1.139;
  * the MATURE-ROW IDENTITY, which is the owner's law G6 and which this seat measured to be BINDING
    on the re-mix knobs (see below);
  * the owner's acceptance gates G1-G5;
  * and the selection rule: minimum corrected-surface SSE among the points that satisfy all of it,
    ties broken by the smaller dose.

THE MATURE-ROW FINDING, stated here because it decides the shape of the answer: the re-mix is keyed
on CAREER GAMES, not on age. Any move in (kappa, gamma_u, eta, gamma_d) therefore re-prices mature
rows too. Measured on this tree: (kappa 0.24 -> 0.34, eta 0.41 -> 0.44) moved milan-murdock, 26, by
+5.67 board points. The owner's law says he cannot move at all. ORDER C hit the identical wall
(REMIX_34.json: the repaired knob point is the ONLY one of 3,960 the mature gate admits). So the
mature-row identity is carried as a HARD constraint and is TESTED here, knob point by knob point, on
the live board — not assumed. Whatever it leaves feasible is what the counterweight is allowed to be.
"""
import os, sys, json, math, io, contextlib, time, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

L = json.load(open(SP + '/O36_LEGS.json'))
DOSES = L['doses']; POP = L['pop']; PLF = L['PLF']
LEGS = {float(k): v for k, v in L['legs'].items()}
CONT = {float(k): v for k, v in L['cont'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
print('legs loaded: %d rows x %d doses (identity %s)' % (len(POP), len(DOSES), L['leg_identity']))

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


# ---- the CORRECTED (age-fair) hindsight surface — rebuilt here, dose-independent ------------------
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
print('corrected hindsight W: %.4f  90%% CI [%.4f, %.4f]' % (W_HIND, W_LO, W_HI))

REAL_CELLS = {b: float(np.mean([r['y'] for r in rows_h if bucket(r['g1']) == b]))
              for b in ('0', '1-4', '5-9', '10-15', '16+')}
TERC_KEYS = {}; REAL_TERC = {}
for b in ('1-4', '5-9'):
    rs = sorted([r for r in rows_h if bucket(r['g1']) == b], key=lambda r: r['prodA'])
    n3 = len(rs) // 3
    for nm, seg in (('poor', rs[:n3]), ('mid', rs[n3:2 * n3]), ('riser', rs[2 * n3:])):
        TERC_KEYS['%s/%s' % (b, nm)] = set(r['key'] for r in seg)
        REAL_TERC['%s/%s' % (b, nm)] = float(np.mean([r['y'] for r in seg]))
print('corrected tercile targets (the W2 5-9g objects the order names):',
      {k: round(v, 3) for k, v in REAL_TERC.items() if k.startswith('5-9')})
assert [r['key'] for r in rows_h] == [q['key'] for y in CLASSES_H6 for q in POP if q['yr'] == y]


def p1_of(Lg, kap, gu, eta, gd, lrel):
    g = Lg['g']
    if g <= 0:
        D = min(1.0, Lg['Dfade'] * (1.0 + lrel * Lg['sig'])) if Lg['Dfade'] < 1.0 else Lg['Dfade']
        return D * Lg['V0']
    mu = (g / gu) * math.exp(1.0 - g / gu)
    md = (g / gd) * math.exp(1.0 - g / gd)
    rb = Lg['rho']
    r2 = rb + kap * mu * (1.0 - rb)
    D = min(1.0, Lg['Dfade'] * (1.0 + lrel * Lg['sig'])) if Lg['Dfade'] < 1.0 else Lg['Dfade']
    ped = (D * (1.0 - r2) + Lg['Phi'] * Lg['beta'] * r2) * Lg['V0'] * max(0.0, 1.0 - eta * md)
    acr = kap * mu * (1.0 - rb) * Lg['agap'] * 20.0 * PLF
    return r2 * Lg['Phat'] + ped + acr


def metrics(dose, kap, gu, eta, gd, lrel):
    Ld = LEGS[dose]
    p1 = {q['key']: p1_of(Ld[q['key']], kap, gu, eta, gd, lrel) for q in POP}
    Rc = {}
    for y in range(2005, 2022):
        rows = [q for q in POP if q['yr'] == y]
        Rc[y] = sum(p1[q['key']] for q in rows) / sum(q['v0'] for q in rows)
    mean_0515 = float(np.mean([Rc[y] for y in range(2005, 2016)]))
    bandR = {}
    for bnm in BANDS5:
        rows = [q for q in POP if q['arm'] == 'ND' and nd_band(q['pick']) == bnm]
        bandR[bnm] = sum(p1[q['key']] for q in rows) / sum(q['v0'] for q in rows)
    rows_s = []
    for y in CLASSES_H6:
        rows = [q for q in POP if q['yr'] == y]
        mp1 = np.mean([p1[q['key']] for q in rows])
        mprodA = np.mean([q['sv1_age'] for q in rows]) or 1.0
        mped = np.mean([q['v0'] for q in rows])
        for q in rows:
            rows_s.append(dict(key=q['key'], g1=q['g1'], x=p1[q['key']] / mp1,
                               prodA=q['sv1_age'] / mprodA, ped=q['v0'] / mped))
    X = np.array([r['x'] for r in rows_s])
    slope = float(ols([X], Yh)[1])
    bc = ols([np.array([r['prodA'] for r in rows_s]), np.array([r['ped'] for r in rows_s])], X)
    W = float(bc[1] / bc[2])
    cells = {}; obj = 0.0
    for b in ('0', '1-4', '5-9', '10-15', '16+'):
        rs = [r for r in rows_s if bucket(r['g1']) == b]
        pr = float(np.mean([r['x'] for r in rs]))
        cells[b] = dict(n=len(rs), price=pr, real=REAL_CELLS[b], gap=REAL_CELLS[b] - pr)
        obj += len(rs) * (REAL_CELLS[b] - pr) ** 2
    terc = {}
    for tk, keys in TERC_KEYS.items():
        seg = [r for r in rows_s if r['key'] in keys]
        pr = float(np.mean([r['x'] for r in seg]))
        terc[tk] = dict(n=len(seg), price=pr, real=REAL_TERC[tk], gap=REAL_TERC[tk] - pr)
        if tk.startswith('5-9'):
            obj += len(seg) * (REAL_TERC[tk] - pr) ** 2
    return dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, lam_rel=lrel, obj=obj,
                slope=slope, W=W, mean_0515=mean_0515, max_class=max(Rc.values()),
                min_class=min(Rc.values()), per_class=Rc, band_R=bandR,
                min_band=min(bandR.values()), band_spread=max(bandR.values()) - min(bandR.values()),
                cells=cells, terciles=terc)


def rho32_monotone(kap, gu):
    prev = -1.0; g = 0.0
    while g <= 300.0:
        r = rho_base(g)
        r = r + kap * ((g / gu) * math.exp(1.0 - g / gu)) * (1.0 - r)
        if r < prev - 1e-12 or not (r < 1.0 + 1e-12):
            return False
        prev = r; g += 0.25
    return True


def continuity_ok(dose, kap, gu, eta, gd, lrel):
    """The ledger's ruled at-bar object: integer game steps 0..20, tolerance 1e-9, at-bar rows only,
    the age credit included. A price that DIPS as a game is added is the cliff this forbids."""
    for c in CONT[dose]:
        if not c['atbar']:
            continue
        D = min(1.0, c['Dfade'] * (1.0 + lrel * c['sig'])) if c['Dfade'] < 1.0 else c['Dfade']
        prev = None
        for gg in range(0, 21):
            rb = rho_base(gg)
            mu = ((gg / gu) * math.exp(1.0 - gg / gu)) if gg > 0 else 0.0
            r2 = rb + kap * mu * (1.0 - rb)
            mix = max(0.0, 1.0 - eta * ((gg / gd) * math.exp(1.0 - gg / gd))) if gg > 0 else 1.0
            pi = (D * (1.0 - r2) + PHI(gg, c['s'], c['pool']) * BETA(gg, c['pool']) * r2) * mix
            pu = r2 * c['Phat'] + pi * c['V0'] + kap * mu * (1.0 - rb) * c['agap'] * 20.0 * PLF
            if prev is not None and pu < prev - 1e-9:
                return False
            prev = pu
    return True


# phi31/beta31 are pure functions of (g, pool); lift them off the engine once
_ENG = {}


def _load_engine_funcs():
    os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O32_STAGE='5', RL_O36_LAM_S1='0.0',
                      PYTHONHASHSEED='0', RL_REPO=ROOT,
                      OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                      NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                      RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                      RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                      RL_PRIOR_TREES='400', PAR_RAMPS='22',
                      RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
    sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
    cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
    NSE = {}
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
    os.chdir(cwd)
    _ENG['MA'] = NSE.get('MA', MA); _ENG['NSE'] = NSE
    return _ENG


_load_engine_funcs()
PHI = lambda g, s, pl: float(_ENG['NSE']['phi31'](g, s, pl))
BETA = lambda g, pl: float(_ENG['NSE']['beta31'](g, pl))

# ================= THE MATURE-ROW IDENTITY TEST, ON THE LIVE BOARD ==================================
MA = _ENG['MA']; NSE = _ENG['NSE']; ev = NSE['ev']
BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
MATURE = [p for p in PB.values()
          if NSE['_isreal'](p) and not p.get('_retired') and not NSE['delisted'](p)
          and MA.GRP.get(p.get('pos')) and p.get('_by') and (2026 - int(p['_by'])) >= 24]
print('mature (age 24+) active rows under the store-wide identity assert: %d' % len(MATURE))


MATURE.sort(key=lambda p: p.get('key') or '')
PROBE_MAT = [p.get('key') for p in MATURE[::5]]     # deterministic 1-in-5 probe; the CHOSEN point is
print('  (the knob probe uses a deterministic 1-in-5 mature sample, n=%d; the CHOSEN point is asserted '
      'store-wide on all %d)' % (len(PROBE_MAT), len(MATURE)))


def price_all(keys, dose, kap, gu, eta, gd, lrel):
    NSE['O32_KAPPA'] = kap; NSE['O32_GAMMA'] = gu; NSE['O32_ETA'] = eta
    NSE['O32_GAMMA_D'] = gd; NSE['O32_LAMBDA'] = lrel
    MA.O36_LAM_S1 = dose
    MA._pe_clear()
    out = {}
    for k in keys:
        p = PB.get(k)
        if p is None: continue
        with contextlib.redirect_stdout(io.StringIO()):
            out[k] = float(ev(p, 2026))
    return out


REPAIR = (0.24, 11.0, 0.41, 14.0, 1.08)
MKEYS = [p.get('key') for p in MATURE]
BASE_MAT = price_all(MKEYS, 0.0, *REPAIR)     # the landing candidate's own mature prices


def mature_identity(dose, kap, gu, eta, gd, lrel, keys=None):
    """Every active row aged 24+, tolerance ZERO. Returns (n_moved, worst_abs, worst_key)."""
    keys = MKEYS if keys is None else keys
    cur = price_all(keys, dose, kap, gu, eta, gd, lrel)
    bad = [(abs(cur[k] - BASE_MAT[k]), k) for k in keys if cur.get(k) != BASE_MAT.get(k)]
    if not bad:
        return 0, 0.0, None
    bad.sort(reverse=True)
    return len(bad), bad[0][0], bad[0][1]


# The knob axes are tested against the mature law FIRST, because if a knob point cannot pass it,
# nothing else about that point matters. The dose and the relief are tested with it.
print('\n--- THE MATURE-ROW IDENTITY, TESTED KNOB POINT BY KNOB POINT (owner law G6) ---')
KNOB_PROBE = [(0.24, 11.0, 0.41, 14.0), (0.25, 11.0, 0.41, 14.0), (0.24, 11.0, 0.42, 14.0),
              (0.24, 12.0, 0.41, 14.0), (0.24, 11.0, 0.41, 13.0), (0.30, 11.0, 0.41, 14.0),
              (0.24, 11.0, 0.50, 14.0), (0.20, 11.0, 0.41, 14.0), (0.24, 11.0, 0.30, 14.0)]
KNOB_OK = {}
for kp in KNOB_PROBE:
    n, w, k = mature_identity(0.35, *kp, 1.08, PROBE_MAT)
    KNOB_OK[kp] = (n == 0)
    print('  kappa %.2f gu %4.1f eta %.2f gd %4.1f -> mature rows moved: %-5d worst %8.3f  %s'
          % (kp[0], kp[1], kp[2], kp[3], n, w, ('' if n == 0 else 'on ' + str(k))))
print('  RELIEF axis (knobs at the repair point):')
REL_OK = {}
for lr in (0.80, 1.08, 1.30, 1.50):
    n, w, k = mature_identity(0.35, *REPAIR[:4], lr, PROBE_MAT)
    REL_OK[lr] = (n == 0)
    print('    lambda_rel %.2f -> mature rows moved: %-5d worst %8.3f  %s'
          % (lr, n, w, ('' if n == 0 else 'on ' + str(k))))
print('  DOSE axis (knobs and relief at the repair point):')
DOSE_OK = {}
for dz in (0.15, 0.35, 0.70, 1.00):
    n, w, k = mature_identity(dz, *REPAIR, PROBE_MAT)
    DOSE_OK[dz] = (n == 0)
    print('    lambda_S1 %.2f -> mature rows moved: %-5d worst %8.3f  %s'
          % (dz, n, w, ('' if n == 0 else 'on ' + str(k))))

MAT_FREE_KNOBS = [kp for kp, ok in KNOB_OK.items() if ok]
MAT_FREE_REL = [lr for lr, ok in REL_OK.items() if ok]
json.dump(dict(knob_probe={('%.2f/%.1f/%.2f/%.1f' % kp): ok for kp, ok in KNOB_OK.items()},
               relief_probe=REL_OK, dose_probe=DOSE_OK, n_mature=len(MATURE)),
          open(os.path.join(HERE, 'MATURE_GATE_36.json'), 'w'), indent=1, sort_keys=True, default=float)
print('  -> knob points that pass the mature law: %d of %d;  relief values that pass: %s'
      % (len(MAT_FREE_KNOBS), len(KNOB_PROBE), MAT_FREE_REL))

# ================= THE JOINT SWEEP =================================================================
# The knob axes are the ones the MATURE LAW leaves open, and no others. If the law admits only the
# repair point, the honest joint grid is (dose x relief) and the packet says so — it does not pretend
# to have swept knobs the owner's own law forbids. The FULL prereg'd knob grid is swept anyway with
# the mature law switched off, and reported as the UNCONSTRAINED diagnostic that is NEVER CHOSEN
# (exactly the discipline ORDER C used for its alpha=0 optimum).
if len(MAT_FREE_KNOBS) <= 1:
    GRID_K = [REPAIR[0]]; GRID_GU = [REPAIR[1]]; GRID_E = [REPAIR[2]]; GRID_GD = [REPAIR[3]]
    print('  -> THE MATURE LAW PINS THE RE-MIX KNOBS. The joint grid is (dose x relief).')
else:
    GRID_K = sorted(set(k[0] for k in MAT_FREE_KNOBS))
    GRID_GU = sorted(set(k[1] for k in MAT_FREE_KNOBS))
    GRID_E = sorted(set(k[2] for k in MAT_FREE_KNOBS))
    GRID_GD = sorted(set(k[3] for k in MAT_FREE_KNOBS))
GRID_REL = sorted(set([0.80, 1.08, 1.30] + MAT_FREE_REL))
MONO = {(k, gu): rho32_monotone(k, gu) for k in GRID_K for gu in GRID_GU}

import collections
FAIL = collections.Counter()
feas = []
allpts = []
T0 = time.time()
for dose in DOSES:
    for kap in GRID_K:
        for gu in GRID_GU:
            if not MONO[(kap, gu)]:
                FAIL['mono'] += len(GRID_E) * len(GRID_GD) * len(GRID_REL); continue
            for eta in GRID_E:
                for gd in GRID_GD:
                    for lrel in GRID_REL:
                        M = metrics(dose, kap, gu, eta, gd, lrel)
                        f = []
                        if not (0.885 <= M['slope'] <= 1.115): f.append('slope')
                        if not (W_LO <= M['W'] <= W_HI): f.append('W')
                        if not (M['max_class'] <= 1.139): f.append('1.14line')
                        if not continuity_ok(dose, kap, gu, eta, gd, lrel): f.append('continuity')
                        for x in f: FAIL[x] += 1
                        M['ruled_fails'] = f
                        allpts.append(M)
                        if not f:
                            feas.append(M)
print('\nruled-constraint failure counts over the joint grid (%d points, %.0fs): %s'
      % (len(allpts), time.time() - T0, dict(FAIL)))
print('points feasible on the RULED constraints alone: %d' % len(feas))
json.dump(dict(W_hind=W_HIND, W_ci=[W_LO, W_HI], real_cells=REAL_CELLS, real_terc=REAL_TERC,
               n_grid=len(allpts), n_ruled_feasible=len(feas), fail_counts=dict(FAIL),
               doses=DOSES, grid=dict(kappa=GRID_K, gamma_u=GRID_GU, eta=GRID_E, gamma_d=GRID_GD,
                                      lam_rel=GRID_REL),
               feasible=sorted(feas, key=lambda m: m['obj'])[:400]),
          open(SP + '/O36_SWEEP.json', 'w'), default=float)
for M in sorted(feas, key=lambda m: (m['obj'], m['dose']))[:12]:
    print('  dose %.2f k=%.2f gu=%.0f e=%.2f gd=%.0f lrel=%.2f | obj %5.1f W %.3f sl %.3f class %.4f '
          'max %.4f | bands %s'
          % (M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['lam_rel'], M['obj'],
             M['W'], M['slope'], M['mean_0515'], M['max_class'],
             {k: round(100 * (v - 1), 2) for k, v in M['band_R'].items()}))

# ---- THE UNCONSTRAINED DIAGNOSTIC — the full prereg'd knob grid with the mature law SWITCHED OFF.
# REPORTED, NEVER CHOSEN. Its only job is to put a number on what the owner's mature-row law costs.
DK = [round(0.15 + 0.05 * i, 2) for i in range(10)]
DGU = [8.0, 10.0, 11.0, 12.0, 14.0, 16.0]
DE = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.41, 0.45, 0.5]
DGD = [4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
DDOSE = [d for d in DOSES if d in (0.15, 0.25, 0.35, 0.50, 0.70)]
DMONO = {(k, gu): rho32_monotone(k, gu) for k in DK for gu in DGU}
unc = []
T1 = time.time()
for dose in DDOSE:
    for kap in DK:
        for gu in DGU:
            if not DMONO[(kap, gu)]: continue
            for eta in DE:
                for gd in DGD:
                    M = metrics(dose, kap, gu, eta, gd, 1.08)
                    if not (0.885 <= M['slope'] <= 1.115): continue
                    if not (W_LO <= M['W'] <= W_HI): continue
                    if M['max_class'] > 1.139: continue
                    if not continuity_ok(dose, kap, gu, eta, gd, 1.08): continue
                    unc.append(M)
print('\nUNCONSTRAINED DIAGNOSTIC (mature law OFF, %d ruled-feasible of the full knob grid, %.0fs):'
      % (len(unc), time.time() - T1))
for M in sorted(unc, key=lambda m: m['obj'])[:6]:
    print('  dose %.2f k=%.2f gu=%.0f e=%.2f gd=%.0f | obj %5.1f class %.4f bands %s   [NEVER CHOSEN]'
          % (M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['obj'], M['mean_0515'],
             {k: round(100 * (v - 1), 2) for k, v in M['band_R'].items()}))
json.dump(dict(unconstrained_best=sorted(unc, key=lambda m: m['obj'])[:20],
               n_unconstrained_feasible=len(unc), doses=DDOSE),
          open(SP + '/O36_UNCONSTRAINED.json', 'w'), default=float)
print('written: %s/O36_SWEEP.json  %s/O36_UNCONSTRAINED.json' % (SP, SP))
