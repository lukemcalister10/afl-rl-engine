#!/usr/bin/env python3
"""ORDER I — STEP 2: THE ONE JOINT CALIBRATION.

Plain words. There is one calibration, not three. It chooses the S1 dose, the two re-mix knobs and
their two shapes, and the selection relief TOGETHER, because they push on the same rows in opposite
directions: S1 lifts every young player who produces anything, and the counterweight decides who
keeps the lift. Choosing the dose first and the counterweight afterwards would be choosing twice.

Fixed before any number was looked at (PREREG_I.md §3):
  * the RULED feasibility constraints — rho32 monotone, the ruled at-bar continuity object, the
    hindsight weight W inside the corrected 90% CI, the calibration slope band, no class above 1.139;
  * the owner's acceptance gates G1-G5;
  * the selection rule: minimum corrected-surface SSE among the points that satisfy all of it, ties
    broken by the smaller dose;
  * and halt-and-report, with the tension quantified, if that set is empty.

The mature-row law G6 is enforced UPSTREAM, by o36_mature_gate.py, which measures on the live board
which knobs the law leaves free. This script reads that verdict and sweeps only what is left.

CONTROLS PRINTED FIRST, so the instrument is checked before it is trusted:
  * the corrected surface must reproduce REMIX_32R.json's own W, cells and terciles;
  * the LANDING CANDIDATE point (dose 0, repair knobs, pooled pick fade) must reproduce the Order-D
    wire's own class mark 1.0421.
"""
import os, sys, json, math, time, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

L = json.load(open(SP + '/O36_LEGS.json'))
DOSES = L['doses']; POP = L['pop']; PLF = L['PLF']
LEGS = {float(k): v for k, v in L['legs'].items()}
CONT = {float(k): v for k, v in L['cont'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
print('legs loaded: %d rows x %d doses (leg identity %s)' % (len(POP), len(DOSES), L['leg_identity']))
MG = json.load(open(os.path.join(HERE, 'MATURE_GATE_36.json')))
print('mature gate: knob moves that keep every mature row byte-identical: %s' % (MG['knob_axis_free'] or 'NONE'))
print('             relief values that do: %s' % (MG['relief_axis_free'] or 'NONE'))
print('             S1 doses that do:      %s' % (MG['dose_axis_free'] or 'NONE'))

O31_TAU_RHO = 29.194253560287144
O31_B_RHO = 0.8015424473253033
rho_base = lambda g: 0.0 if g <= 0.0 else 1.0 - math.exp(-((g / O31_TAU_RHO) ** O31_B_RHO))
CLASSES_H6 = list(range(2005, 2019))
BANDS5 = ['1-10', '11-20', '21-30', '31-40', '41-64']
REPAIR = (0.24, 11.0, 0.41, 14.0, 1.08)


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
assert [r['key'] for r in rows_h] == [q['key'] for y in CLASSES_H6 for q in POP if q['yr'] == y]

REF = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'REMIX_32R.json')))
CS = REF['corrected_surface']
print('\nCONTROL 1 — the corrected age-fair hindsight surface reproduces REMIX_32R.json:')
d1 = abs(W_HIND - CS['W_hind_age'])
d2 = max(abs(REAL_CELLS[b] - CS['cells_realized'][b]) for b in REAL_CELLS)
d3 = max(abs(REAL_TERC[t] - CS['terciles_realized'][t]) for t in REAL_TERC)
print('   W %.10f vs %.10f (dev %.2e) · cells max dev %.2e · terciles max dev %.2e  -> %s'
      % (W_HIND, CS['W_hind_age'], d1, d2, d3, 'EXACT' if max(d1, d2, d3) < 1e-9 else 'DEVIATION'))
print('   the W2 objects this order names: 5-9g risers %.4f · 5-9g sub-expectation %.4f (of entry)'
      % (REAL_TERC['5-9/riser'], REAL_TERC['5-9/poor']))
print('   W 90%% CI [%.4f, %.4f]' % (W_LO, W_HI))


def p1_of(Lg, kap, gu, eta, gd, lrel, fade):
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


def metrics(dose, kap, gu, eta, gd, lrel, fade):
    Ld = LEGS[dose]
    p1 = {q['key']: p1_of(Ld[q['key']], kap, gu, eta, gd, lrel, fade) for q in POP}
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
    return dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, lam_rel=lrel, fade=fade,
                obj=obj, slope=slope, W=W, mean_0515=mean_0515, max_class=max(Rc.values()),
                max_class_year=max(Rc, key=Rc.get), min_class=min(Rc.values()), per_class=Rc,
                band_R=bandR, min_band=min(bandR.values()),
                band_spread=max(bandR.values()) - min(bandR.values()), cells=cells, terciles=terc)


CANDPT = metrics(0.0, *REPAIR, 'pool')
print('\nCONTROL 2 — the LANDING CANDIDATE on this instrument (dose 0, repair knobs, POOLED pick fade):')
print('   class mark mean_0515 = %.4f   (the Order-D wire\'s own W2 scorecard number of record: 1.0421)'
      % CANDPT['mean_0515'])
print('   max class %.4f on %s  ·  min class %.4f  ·  slope %.4f  ·  W %.4f'
      % (CANDPT['max_class'], CANDPT['max_class_year'], CANDPT['min_class'], CANDPT['slope'], CANDPT['W']))
print('   five-band yr0->1: %s' % {k: '%+.2f%%' % (100 * (v - 1)) for k, v in CANDPT['band_R'].items()})
FADEONLY = metrics(0.0, *REPAIR, 'tall')
print('\nCONTROL 3 — the TALL/SMALL FADE ALONE (dose 0, repair knobs, tall exponent):')
print('   class mark %.4f (%+.4f) · max class %.4f on %s · bands %s'
      % (FADEONLY['mean_0515'], FADEONLY['mean_0515'] - CANDPT['mean_0515'], FADEONLY['max_class'],
         FADEONLY['max_class_year'],
         {k: '%+.2f%%' % (100 * (v - 1)) for k, v in FADEONLY['band_R'].items()}))


def rho32_monotone(kap, gu):
    prev = -1.0; g = 0.0
    while g <= 300.0:
        r = rho_base(g)
        r = r + kap * ((g / gu) * math.exp(1.0 - g / gu)) * (1.0 - r)
        if r < prev - 1e-12 or not (r < 1.0 + 1e-12):
            return False
        prev = r; g += 0.25
    return True


ENGF = {}


def _phi_beta():
    import io, contextlib
    os.environ.update(RL_O31='1', RL_O32='1', RL_O32_STAGE='5', RL_O36='1', RL_O36_LAM_S1='0.0',
                      PYTHONHASHSEED='0', RL_REPO=ROOT,
                      RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                      RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                      RL_PRIOR_TREES='400', PAR_RAMPS='22',
                      RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
    sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
    cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
    NSE = {}
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as _MA
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
    os.chdir(cwd)
    ENGF['phi'] = NSE['phi31']; ENGF['beta'] = NSE['beta31']


_phi_beta()


def continuity_ok(dose, kap, gu, eta, gd, lrel, fade):
    for c in CONT[dose]:
        if not c['atbar']:
            continue
        Df = c['Dfade'] if fade == 'tall' else c['Dfade_pool']
        D = min(1.0, Df * (1.0 + lrel * c['sig'])) if Df < 1.0 else Df
        prev = None
        for gg in range(0, 21):
            rb = rho_base(gg)
            mu = ((gg / gu) * math.exp(1.0 - gg / gu)) if gg > 0 else 0.0
            r2 = rb + kap * mu * (1.0 - rb)
            mix = max(0.0, 1.0 - eta * ((gg / gd) * math.exp(1.0 - gg / gd))) if gg > 0 else 1.0
            pi = (D * (1.0 - r2) + float(ENGF['phi'](gg, c['s'], c['pool'])) *
                  float(ENGF['beta'](gg, c['pool'])) * r2) * mix
            pu = r2 * c['Phat'] + pi * c['V0'] + kap * mu * (1.0 - rb) * c['agap'] * 20.0 * PLF
            if prev is not None and pu < prev - 1e-9:
                return False
            prev = pu
    return True


# ============ THE SWEEP: the axes the mature law leaves open ========================================
KNOBS_PINNED = not MG['knob_axis_free']
REL_PINNED = (MG['relief_axis_free'] == ['lambda_rel = 1.08'] or not MG['relief_axis_free'])
GRID_K = [REPAIR[0]] if KNOBS_PINNED else [round(0.15 + 0.05 * i, 2) for i in range(10)]
GRID_GU = [REPAIR[1]] if KNOBS_PINNED else [8.0, 10.0, 11.0, 12.0, 14.0, 16.0]
GRID_E = [REPAIR[2]] if KNOBS_PINNED else [0.0, 0.1, 0.2, 0.3, 0.4, 0.41, 0.5]
GRID_GD = [REPAIR[3]] if KNOBS_PINNED else [4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
GRID_REL = [REPAIR[4]] if REL_PINNED else [0.80, 1.08, 1.30]
print('\nTHE JOINT GRID THE OWNER\'S LAWS LEAVE OPEN: dose %d values x kappa %d x gamma_u %d x eta %d '
      'x gamma_d %d x relief %d = %d points'
      % (len(DOSES), len(GRID_K), len(GRID_GU), len(GRID_E), len(GRID_GD), len(GRID_REL),
         len(DOSES) * len(GRID_K) * len(GRID_GU) * len(GRID_E) * len(GRID_GD) * len(GRID_REL)))

FAIL = collections.Counter()
feas = []; allpts = []
for dose in DOSES:
    for kap in GRID_K:
        for gu in GRID_GU:
            if not rho32_monotone(kap, gu):
                FAIL['mono'] += 1; continue
            for eta in GRID_E:
                for gd in GRID_GD:
                    for lrel in GRID_REL:
                        M = metrics(dose, kap, gu, eta, gd, lrel, 'tall')
                        f = []
                        if not (0.885 <= M['slope'] <= 1.115): f.append('slope')
                        if not (W_LO <= M['W'] <= W_HI): f.append('W')
                        if not (M['max_class'] <= 1.139): f.append('1.14line')
                        if not continuity_ok(dose, kap, gu, eta, gd, lrel, 'tall'): f.append('continuity')
                        for x in f: FAIL[x] += 1
                        M['ruled_fails'] = f
                        allpts.append(M)
                        if not f: feas.append(M)
print('\nruled-constraint failures over that grid: %s' % dict(FAIL))
print('points feasible on the RULED constraints: %d of %d' % (len(feas), len(allpts)))

print('\n-- THE DOSE RESPONSE (knobs and relief where the mature law pins them, tall fade live) --')
print('  %6s %10s %10s %10s %8s %8s | %s' % ('dose', 'class', 'max class', 'yr', 'slope', 'W', 'five bands yr0->1'))
for M in sorted([m for m in allpts if (m['kappa'], m['gamma_u'], m['eta'], m['gamma_d'], m['lam_rel']) == REPAIR],
                key=lambda m: m['dose']):
    print('  %6.2f %10.4f %10.4f %10s %8.4f %8.4f | %s   %s'
          % (M['dose'], M['mean_0515'], M['max_class'], M['max_class_year'], M['slope'], M['W'],
             ' '.join('%+6.2f%%' % (100 * (M['band_R'][b] - 1)) for b in BANDS5),
             ('FEASIBLE' if not M['ruled_fails'] else 'fails ' + ','.join(M['ruled_fails']))))

json.dump(dict(W_hind=W_HIND, W_ci=[W_LO, W_HI], real_cells=REAL_CELLS, real_terc=REAL_TERC,
               control_landing=CANDPT, control_fade_only=FADEONLY,
               knobs_pinned=KNOBS_PINNED, relief_pinned=REL_PINNED,
               n_grid=len(allpts), n_ruled_feasible=len(feas), fail_counts=dict(FAIL),
               doses=DOSES, points=allpts, feasible=sorted(feas, key=lambda m: m['obj'])[:200]),
          open(SP + '/O36_SWEEP.json', 'w'), default=float)
print('\nwritten: %s/O36_SWEEP.json' % SP)
