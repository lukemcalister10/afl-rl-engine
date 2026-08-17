#!/usr/bin/env python3
"""ORDER A REPAIR — R1: THE CORRECTED (AGE-RELATIVE) HINDSIGHT SURFACE AND THE RE-MIX
RE-CALIBRATION (PREREG_32R.md, pushed first).

Plain-language summary of what this does:
 1. Re-cuts W2's "poor starter / mid / riser" buckets using AGE-APPROPRIATE expectations — a
    19-year-old's season is scored against the bar a 19-year-old should clear (the S1 measured
    development gap), not the mature bar. The outcome ruler (what careers actually delivered)
    does not move; only how a young season is CLASSIFIED.
 2. Re-measures the hindsight production-vs-pedigree weight ratio (W) with the same age-fair
    classifier, with a bootstrap band.
 3. Re-fits the re-mix knobs (kappa, gamma_u, eta, gamma_d) — now WITH the R1 age credit live in
    the price — against the corrected surface, under the same hard gates as the build:
    slope band, W inside the corrected band, no class above 1.139 (the 1.14 no-arb line),
    rho monotone, and the ruled at-bar continuity object (now including the age credit).
 4. Reports the five ND pick bands' year-0 -> year-1 appreciation at every grid point, and
    prefers feasible points where NO band depreciates (the R3 gate), reporting exactly what is
    and is not reachable.

Control: with kappa=0 the reconstructed year-1 price equals ev(p, yr+1) exactly on every row.
"""
import os, sys, json, math, io, contextlib, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

os.environ.update(RL_O31='1', RL_O32='1', RL_O32_STAGE='5', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
G = {k: NSE[k] for k in ('rho31', 'beta31', 'phi31', 'o31_D', 'o31_stall_run', 'pv_games',
                         'pv_pedigree', 'ev', '_O32S', '_PL_F', '_O30BP_BARS')}
assert G['_O32S'] == 5, 'engine must load at stage 5 (no re-mix) for the legs'
ev = G['ev']; PLF = float(G['_PL_F'])

# ---- constants: ruler + age gaps (S1 C3, same transcription the engine asserts) -------------------
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
TALL = {'KPD', 'KPF', 'RUCK'}
D_TALL = {18: 22.334475609756097, 19: 20.55500752464971, 20: 16.306362402208926,
          21: 11.588672690048071, 22: 7.826894964594814, 23: 6.439783302063788}
D_SMALL = {18: 20.080511089352214, 19: 20.080511089352214, 20: 14.306977484301457,
           21: 11.265167414136857, 22: 6.761247284555768, 23: 4.584052475875439}


def age_gap(pos, age):
    if age is None or age >= 24:
        return 0.0
    return (D_TALL if pos in TALL else D_SMALL)[max(18, min(23, int(age)))]


S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
CARRY = 1.14


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(l):
    c = LCAPT_G * LCAPT_W * (softplus((l - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


def season_val(avg, pos, bar):
    return w_sqrt_g * 0  # placeholder, unused


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        return 'RD' if t == 'RD' else ('MSD' if t == 'MSD' else 'OTHERPOOL')
    return None


CAND_P = SP + '/per_entrant_O31FFINAL.json'
A = json.load(open(CAND_P))
Arecs = {r['key']: r for r in A['recs']}
FM = {'paddy-mccartin', 'thomas-boyd'}

SV = {}      # flat-bar season values (the OUTCOME ruler — unchanged)
SVA1 = {}    # the year-1 season's AGE-ADJUSTED value (the classifier — R1)
for k, r in Arecs.items():
    d = {}
    yr = r['year']; aged = r.get('age_draft')
    for s in r['seasons']:
        if s['year'] > 2025:
            continue
        gp = s.get('bar')
        if gp not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - BARS[gp]) * 21.0
        if s['year'] == yr + 1:
            a1 = (aged + 1) if aged is not None else None
            bar_age = BARS[gp] - age_gap(gp, a1)
            SVA1[k] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - bar_age) * 21.0
    SV[k] = d


def dv_h6(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if Y < t <= Y + 6)


def dv_full(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


POP = []
for k, r in Arecs.items():
    if k in FM:
        continue
    arm = arm_of(r)
    if arm is None:
        continue
    yr = r['year']
    if yr < 2005 or yr > 2021:
        continue
    aged = r.get('age_draft')
    POP.append(dict(key=k, yr=yr, arm=arm, v0=float(r['v0']), g1=int(r.get('games_yr1') or 0),
                    pick=r.get('pick'), pos=r.get('pos'),
                    age1=(aged + 1) if aged is not None else None,
                    sv1=SV[k].get(yr + 1, 0.0), sv1_age=SVA1.get(k, 0.0),
                    dv1_h6=dv_h6(k, yr + 1), dv0_full=dv_full(k, yr), dv1_full=dv_full(k, yr + 1)))
print('population: %d players (classes 2005-2021, all-arm)' % len(POP))

# ---- the year-1 legs (stage 5) — same as the build calibrator, with the leg-identity control ------
BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key'), []).append(p)
players = [max(v, key=lambda q: len(q['scoring'])) for v in BYKEY.values()]
PBYK = {p.get('key'): p for p in players}


def _min_tenure(p):
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2


def _debut_year(p):
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)


def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)


NEED = {}
for q in POP:
    NEED.setdefault(q['yr'] + 1, []).append(q)
LEGS = {}
CTRL_FAIL = []
for Y in sorted(NEED):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y:
            continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for q in NEED[Y]:
        p = PBYK.get(q['key'])
        if p is None:
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                e = float(ev(p, Y))
        except Exception:
            continue
        g = float(G['pv_games'](p, Y))
        r = float(G['rho31'](g))
        D = float(G['o31_D'](p, Y))
        s = int(G['o31_stall_run'](p, Y))
        pl = bool(p.get('_pool'))
        ph = float(G['phi31'](g, s, pl))
        be = float(G['beta31'](g, pl))
        V0 = float(G['pv_pedigree'](p))
        pi = D * (1.0 - r) + ph * be * r
        Phat = (e - pi * V0) / r if g > 0 else 0.0
        rec = (r * Phat + pi * V0) if g > 0 else D * V0
        if abs(rec - e) > 1e-6 * max(1.0, abs(e)):
            CTRL_FAIL.append((q['key'], Y))
        agp = age_gap(MA.gfut(p), (Y - p['_by']) if p.get('_by') else None)
        LEGS[q['key']] = dict(g=g, rho=r, D=D, s=s, Phi=ph, beta=be, V0=V0, Phat=Phat, p1_s5=e,
                              agap=agp)
    for p in players:
        if id(p) in saved:
            p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
if CTRL_FAIL:
    sys.exit('REPAIR HALT: leg identity failed on %d rows' % len(CTRL_FAIL))
print('leg-identity control PASS on %d rows' % len(LEGS))
POP = [q for q in POP if q['key'] in LEGS]

# ---- the corrected hindsight surface --------------------------------------------------------------
CLASSES_H6 = list(range(2005, 2019))
rows_h = []
for y in CLASSES_H6:
    rows = [q for q in POP if q['yr'] == y]
    mdv = np.mean([q['dv1_h6'] for q in rows])
    mprod = np.mean([q['sv1'] for q in rows])
    mprodA = np.mean([q['sv1_age'] for q in rows]) or 1.0
    mped = np.mean([q['v0'] for q in rows])
    for q in rows:
        rows_h.append(dict(key=q['key'], yr=y, g1=q['g1'],
                           y=q['dv1_h6'] / mdv, prod=q['sv1'] / mprod,
                           prodA=q['sv1_age'] / mprodA, ped=q['v0'] / mped))
Yh = np.array([r['y'] for r in rows_h])
PRA = np.array([r['prodA'] for r in rows_h])
PD = np.array([r['ped'] for r in rows_h])


def ols(Xm, yv):
    A1 = np.column_stack([np.ones(len(yv))] + list(Xm))
    b, *_ = np.linalg.lstsq(A1, yv, rcond=None)
    return b


bh = ols([PRA, PD], Yh)
W_HIND_AGE = float(bh[1] / bh[2])
RNG = np.random.default_rng(33)
wb = []
n_h = len(rows_h)
for _ in range(1000):
    i = RNG.integers(0, n_h, n_h)
    t = ols([PRA[i], PD[i]], Yh[i])
    wb.append(t[1] / t[2])
W_CI = [float(np.percentile(wb, 5)), float(np.percentile(wb, 95))]
print('corrected hindsight W (age-adjusted prod leg): %.4f  90%% CI [%.4f, %.4f]' % (W_HIND_AGE, W_CI[0], W_CI[1]))


def bucket(g):
    if g == 0: return '0'
    if g <= 4: return '1-4'
    if g <= 9: return '5-9'
    if g <= 15: return '10-15'
    return '16+'


REAL_CELLS = {}
for b in ('0', '1-4', '5-9', '10-15', '16+'):
    rs = [r for r in rows_h if bucket(r['g1']) == b]
    REAL_CELLS[b] = float(np.mean([r['y'] for r in rs]))
TERC_KEYS = {}
REAL_TERC = {}
for b in ('1-4', '5-9'):
    rs = sorted([r for r in rows_h if bucket(r['g1']) == b], key=lambda r: r['prodA'])
    n3 = len(rs) // 3
    for nm, seg in (('poor', rs[:n3]), ('mid', rs[n3:2 * n3]), ('riser', rs[2 * n3:])):
        TERC_KEYS['%s/%s' % (b, nm)] = set(r['key'] for r in seg)
        REAL_TERC['%s/%s' % (b, nm)] = float(np.mean([r['y'] for r in seg]))
print('corrected tercile targets:', {k: round(v, 3) for k, v in REAL_TERC.items()})

# who moved bucket? count the composition poisoning the owner named
old_poor = set()
rs59 = sorted([r for r in rows_h if bucket(r['g1']) == '5-9'], key=lambda r: r['prod'])
n3 = len(rs59) // 3
old_poor = set(r['key'] for r in rs59[:n3])
moved = old_poor.symmetric_difference(TERC_KEYS['5-9/poor'])
print('5-9 "poor" bucket membership changed on %d of %d rows under the age-fair classifier'
      % (len(moved) // 1, len(rs59[:n3])))

# ---- price model under (kappa, gu, eta, gd) with the R1 age credit --------------------------------
O31_TAU_RHO = 29.194253560287144
O31_B_RHO = 0.8015424473253033


def rho_base(g):
    return 0.0 if g <= 0.0 else 1.0 - math.exp(-((g / O31_TAU_RHO) ** O31_B_RHO))


def p1_of(q, kap, gu, eta, gd):
    L = LEGS[q['key']]
    g = L['g']
    if g <= 0:
        return L['p1_s5']
    mu = (g / gu) * math.exp(1.0 - g / gu)
    md = (g / gd) * math.exp(1.0 - g / gd)
    rb = L['rho']
    r2 = rb + kap * mu * (1.0 - rb)
    ped = (L['D'] * (1.0 - r2) + L['Phi'] * L['beta'] * r2) * L['V0'] * max(0.0, 1.0 - eta * md)
    acr = kap * mu * (1.0 - rb) * L['agap'] * 20.0 * PLF
    return r2 * L['Phat'] + ped + acr


def nd_band(pk):
    if pk is None: return None
    if pk <= 10: return '1-10'
    if pk <= 20: return '11-20'
    if pk <= 30: return '21-30'
    if pk <= 40: return '31-40'
    if pk <= 64: return '41-64'
    return None


def metrics(kap, gu, eta, gd):
    p1 = {q['key']: p1_of(q, kap, gu, eta, gd) for q in POP}
    Rc = {}
    for y in range(2005, 2022):
        rows = [q for q in POP if q['yr'] == y]
        Rc[y] = sum(p1[q['key']] for q in rows) / sum(q['v0'] for q in rows)
    mean_0515 = float(np.mean([Rc[y] for y in range(2005, 2016)]))
    # ND five-band year-0 -> year-1 appreciation (the R3 object, walk-forward all classes)
    bandR = {}
    for bnm in ('1-10', '11-20', '21-30', '31-40', '41-64'):
        rows = [q for q in POP if q['arm'] == 'ND' and nd_band(q['pick']) == bnm]
        bandR[bnm] = sum(p1[q['key']] for q in rows) / sum(q['v0'] for q in rows)
    rows_s = []
    for y in CLASSES_H6:
        rows = [q for q in POP if q['yr'] == y]
        mp1 = np.mean([p1[q['key']] for q in rows])
        mprodA = np.mean([q['sv1_age'] for q in rows]) or 1.0
        mped = np.mean([q['v0'] for q in rows])
        for q in rows:
            rows_s.append(dict(key=q['key'], yr=y, g1=q['g1'], x=p1[q['key']] / mp1,
                               prodA=q['sv1_age'] / mprodA, ped=q['v0'] / mped))
    X = np.array([r['x'] for r in rows_s])
    PRa = np.array([r['prodA'] for r in rows_s])
    PDa = np.array([r['ped'] for r in rows_s])
    Ya = np.array([next(rr['y'] for rr in rows_h if rr['key'] == r['key']) for r in rows_s]) if False else None
    slope = float(ols([X], Yh)[1])          # rows_s and rows_h are same-ordered populations
    bc = ols([PRa, PDa], X)
    W = float(bc[1] / bc[2])
    cells = {}
    obj = 0.0
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
    return dict(kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, obj=obj, slope=slope, W=W,
                mean_0515=mean_0515, max_class=max(Rc.values()), min_class=min(Rc.values()),
                per_class=Rc, band_R=bandR, min_band=min(bandR.values()),
                band_spread=max(bandR.values()) - min(bandR.values()), cells=cells, terciles=terc)


# rows_s must align with rows_h ordering for the slope: verify once
assert [r['key'] for r in rows_h] == [q['key'] for y in CLASSES_H6 for q in POP if q['yr'] == y], 'ordering broke'

# ---- feasibility: F5 monotonicity + the at-bar continuity object (WITH the age credit) ------------
def rho32_monotone(kap, gu):
    prev = -1.0
    g = 0.0
    while g <= 300.0:
        r = rho_base(g)
        r = r + kap * ((g / gu) * math.exp(1.0 - g / gu)) * (1.0 - r)
        if r < prev - 1e-12 or not (r < 1.0 + 1e-12):
            return False
        prev = r; g += 0.25
    return True


CONT_KEYS = ['lachlan-carmichael', 'josh-smillie', 'harry-demattia', 'max-knobel', 'dyson-sharp',
             'isaac-kako', 'noah-mraz', 'willem-duursma', 'toby-conway', 'luke-beecken', 'chris-scerri']
CONT_LEGS = []
for ck in CONT_KEYS:
    p = PBYK.get(ck)
    if p is None:
        continue
    with contextlib.redirect_stdout(io.StringIO()):
        e = float(ev(p, 2026))
    g = float(G['pv_games'](p, 2026))
    r = float(G['rho31'](g))
    D = float(G['o31_D'](p, 2026))
    s = int(G['o31_stall_run'](p, 2026))
    pl = bool(p.get('_pool'))
    V0 = float(G['pv_pedigree'](p))
    pi = D * (1.0 - r) + float(G['phi31'](g, s, pl)) * float(G['beta31'](g, pl)) * r
    Phat = (e - pi * V0) / r if g > 0 else float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0 * PLF
    atbar = Phat >= float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0 * PLF
    agp = age_gap(MA.gfut(p), (2026 - p['_by']) if p.get('_by') else None)
    CONT_LEGS.append(dict(key=ck, Phat=Phat, V0=V0, D=D, s=s, pool=pl, atbar=atbar, agap=agp))
phi31_f = G['phi31']; beta31_f = G['beta31']


def continuity_ok(kap, gu, eta, gd):
    """EXACTLY the ledger's ruled gate: integer game steps 0..20, tolerance 1e-9, at-bar rows only.
    (The first diagnosis run used 0.25-game steps — STRICTER than the ruled object; the gate the
    build must pass is the ledger's own integer-step curve, so that is what feasibility tests.)"""
    for c in CONT_LEGS:
        if not c['atbar']:
            continue
        prev = None
        for gg in range(0, 21):
            rb = rho_base(gg)
            mu = ((gg / gu) * math.exp(1.0 - gg / gu)) if gg > 0 else 0.0
            r2 = rb + kap * mu * (1.0 - rb)
            mix = max(0.0, 1.0 - eta * ((gg / gd) * math.exp(1.0 - gg / gd))) if gg > 0 else 1.0
            pi = (c['D'] * (1.0 - r2) + float(phi31_f(gg, c['s'], c['pool'])) * float(beta31_f(gg, c['pool'])) * r2) * mix
            pu = r2 * c['Phat'] + pi * c['V0'] + kap * mu * (1.0 - rb) * c['agap'] * 20.0 * PLF
            if prev is not None and pu < prev - 1e-9:
                return False
            prev = pu
    return True


# ---- the sweep ------------------------------------------------------------------------------------
BASE = metrics(0.0, 14.0, 0.0, 12.0)
print('\nSTAGE-5 baseline (no re-mix): mean %.4f  W(age) %.4f  slope %.4f  bands %s  spread %.3f'
      % (BASE['mean_0515'], BASE['W'], BASE['slope'],
         {k: round(v, 3) for k, v in BASE['band_R'].items()}, BASE['band_spread']))
SHIPPED = metrics(0.25, 14.0, 0.30, 12.0)
print('shipped C32 point (k.25/14, e.30/12) WITH the age credit: mean %.4f  W(age) %.4f  bands %s'
      % (SHIPPED['mean_0515'], SHIPPED['W'], {k: round(v, 3) for k, v in SHIPPED['band_R'].items()}))

GRID_K = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
GRID_GU = [8.0, 10.0, 12.0, 14.0, 16.0]
GRID_E = [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
GRID_GD = [4.0, 6.0, 8.0, 10.0, 12.0]
W_LO, W_HI = W_CI
MONO = {(k, gu): rho32_monotone(k, gu) for k in GRID_K for gu in GRID_GU}
feas = []
best = None
import collections as _c
FAILCOUNT = _c.Counter()
NEAR = []
for kap in GRID_K:
    for gu in GRID_GU:
        if not MONO[(kap, gu)]:
            FAILCOUNT['mono'] += len(GRID_E) * len(GRID_GD)
            continue
        for eta in GRID_E:
            for gd in GRID_GD:
                M = metrics(kap, gu, eta, gd)
                fails = []
                if not (0.885 <= M['slope'] <= 1.115): fails.append('slope')
                if not (W_LO <= M['W'] <= W_HI): fails.append('W')
                if not (M['max_class'] <= 1.139): fails.append('1.14line')
                if not continuity_ok(kap, gu, eta, gd): fails.append('continuity')
                for f in fails: FAILCOUNT[f] += 1
                if not fails:
                    feas.append(M)
                elif len(fails) == 1:
                    NEAR.append((fails[0], M))
print('\nconstraint failure counts over the grid:', dict(FAILCOUNT))
for f, M in sorted(NEAR, key=lambda t: t[1]['obj'])[:8]:
    print('  NEAR (only %s fails): k=%.2f gu=%.0f e=%.2f gd=%.0f  W %.3f sl %.3f mx %.4f mean %.4f'
          % (f, M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['W'], M['slope'], M['max_class'], M['mean_0515']))
# AMENDMENT A2 (PREREG_32R): selection = min corrected-surface SSE among the ruled-gate-feasible
# set, FULL STOP. The vantage matrix and the band spread are DIAGNOSTIC-ONLY — no parameter
# choice is justified by them; band figures are computed for the report only.
print('feasible points: %d' % len(feas))
if not feas:
    import sys as _s
    json.dump(dict(order='ORDER A REPAIR R1 — DIAGNOSIS RUN, no feasible point',
                   corrected_surface=dict(W_hind_age=W_HIND_AGE, W_ci90=W_CI,
                                          cells_realized=REAL_CELLS, terciles_realized=REAL_TERC,
                                          poor_bucket_moved_rows=len(moved)),
                   baseline_stage5=BASE, shipped_c32_point=SHIPPED,
                   fail_counts=dict(FAILCOUNT)),
              open(os.path.join(HERE, 'REMIX_32R_DIAG.json'), 'w'), indent=1, sort_keys=True, default=float)
    _s.exit('NO FEASIBLE POINT — diagnosis written to REMIX_32R_DIAG.json')
pool = feas
for M in sorted(pool, key=lambda m: m['obj'])[:10]:
    print('  k=%.2f gu=%.0f e=%.2f gd=%.0f | obj %5.1f W %.3f sl %.3f mean %.4f mx %.4f | bands %s spread %.3f'
          % (M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['obj'], M['W'], M['slope'],
             M['mean_0515'], M['max_class'], {k: round(v, 3) for k, v in M['band_R'].items()},
             M['band_spread']))
best = min(pool, key=lambda m: m['obj'])
print('\nCHOSEN: kappa=%.2f gamma_u=%.1f eta=%.2f gamma_d=%.1f' % (best['kappa'], best['gamma_u'], best['eta'], best['gamma_d']))
print('  mean %.4f  W %.4f  slope %.4f  max class %.4f  min band %.4f  band spread %.4f'
      % (best['mean_0515'], best['W'], best['slope'], best['max_class'], best['min_band'], best['band_spread']))
print('  cells:', {b: (round(c['price'], 3), round(c['real'], 3)) for b, c in best['cells'].items()})
print('  terciles:', {t: (round(c['price'], 3), round(c['real'], 3)) for t, c in best['terciles'].items()})
print('  per-class:', {y: round(v, 4) for y, v in best['per_class'].items()})

json.dump(dict(order='ORDER A REPAIR R1 — corrected surface + re-calibration',
               corrected_surface=dict(W_hind_age=W_HIND_AGE, W_ci90=W_CI,
                                      cells_realized=REAL_CELLS, terciles_realized=REAL_TERC,
                                      poor_bucket_moved_rows=len(moved)),
               baseline_stage5=BASE, shipped_c32_point=SHIPPED, chosen=best,
               n_feasible=len(feas),
               grid=dict(kappa=GRID_K, gamma_u=GRID_GU, eta=GRID_E, gamma_d=GRID_GD),
               constraints=dict(slope=[0.885, 1.115], W='corrected hindsight 90% CI',
                                max_class='<=1.139', mono='rho32 monotone',
                                continuity='at-bar object incl. the age credit'),
               age_credit='kappa*m_u(g)*(1-rho_base)*(S1 gap)*20*PL_F, zero at g=0 and age>=24'),
          open(os.path.join(HERE, 'REMIX_32R.json'), 'w'), indent=1, sort_keys=True, default=float)
print('written: REMIX_32R.json')
