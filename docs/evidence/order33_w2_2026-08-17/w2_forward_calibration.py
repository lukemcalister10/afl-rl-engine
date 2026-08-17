#!/usr/bin/env python3
# =====================================================================================================
# ORDER 33 SEAT W2 -- THE FORWARD CALIBRATION. READ-ONLY.
# Executes exactly the rule fixed in PREREG_W2.md (pushed first, commit 792d979 on land/order-29).
# No engine import, no board build, no store write. Input: the O31FFINAL walk-forward matrix.
# Ruler: the Order 32 S4 delivered-value construction, constants lifted verbatim from s4_shootout.py.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'

B_BOOT = 2000
SEED = 33
FM = {'paddy-mccartin', 'thomas-boyd'}
# ---- S4 ruler constants, lifted verbatim (docs/evidence/order32_s4_2026-08-17/s4_shootout.py) -------
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
CARRY = 1.14
# ---- candidate rho (engine/rl_after/_merged_recover.py:3181,3286; LAW31F.json) ----------------------
O31_TAU_RHO = 29.194253560287144
O31_B_RHO = 0.8015424473253033


def rho(g):
    return 0.0 if g <= 0.0 else 1.0 - math.exp(-((g / O31_TAU_RHO) ** O31_B_RHO))


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(lev):
    c = LCAPT_G * LCAPT_W * (softplus((lev - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0.0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def season_raw(X, g):
    return posval(X + capt_prem(X) - BARS[g]) * 21.0


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        if t == 'RD':
            return 'RD'
        if t == 'MSD':
            return 'MSD'
        return 'OTHERPOOL'
    return None


# ---- identity assertions (prereg SS1) ---------------------------------------------------------------
assert md5f(CAND_P) == 'd97f1aee4161ebcf785cd635ed095038', 'matrix md5 mismatch'
A = json.load(open(CAND_P))
assert A['meta']['store_md5'] == 'cb38ef11', 'store identity mismatch'
assert A['meta']['engine_head'] == '71d9949a', 'engine head mismatch'
assert A['meta']['n_records'] == 2648 and len(A['recs']) == 2648, 'record count mismatch'
Arecs = {r['key']: r for r in A['recs']}
assert len(Arecs) == 2648, 'duplicate keys'
print('identity OK: matrix md5 d97f1aee store cb38ef11 head 71d9949a n=2648')

# ---- season values (the S4 ruler) -------------------------------------------------------------------
SV = {}
for k, r in Arecs.items():
    d = {}
    for s in r['seasons']:
        if s['year'] > LAST_REAL_SEASON:
            continue
        g = s.get('bar')
        if g not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * season_raw(s['avg'], g)
    SV[k] = d


def dv_full(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


def dv_h6(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if Y < t <= Y + 6)


# ---- population -------------------------------------------------------------------------------------
POP = []   # dicts per player, classes 2005-2021
for k, r in Arecs.items():
    if k in FM:
        continue
    arm = arm_of(r)
    if arm is None:
        continue
    yr = r['year']
    if yr < ENTRY_FLOOR or yr > 2021:
        continue
    assert len(r['vpath']) >= 1 and r['vpath'][0] is not None, 'missing year-1 vantage: ' + k
    sv1 = SV[k].get(yr + 1, 0.0)
    POP.append(dict(key=k, yr=yr, arm=arm, v0=float(r['v0']), p1=float(r['vpath'][0]),
                    g1=int(r.get('games_yr1') or 0), sv1=sv1,
                    dv0_full=dv_full(k, yr), dv1_full=dv_full(k, yr + 1),
                    dv0_h6=dv_h6(k, yr), dv1_h6=dv_h6(k, yr + 1),
                    last=int(r.get('last_game_year') or 0)))
print('population: %d players in classes 2005-2021 (all-arm)' % len(POP))

CLASSES_FULL = list(range(2005, 2022))
CLASSES_H6 = list(range(2005, 2019))


def class_rows(y, nd_only=False):
    return [p for p in POP if p['yr'] == y and (not nd_only or p['arm'] == 'ND')]


# ---- (a) LEVEL --------------------------------------------------------------------------------------
def level_table(nd_only=False):
    out = []
    for y in CLASSES_FULL:
        rows = class_rows(y, nd_only)
        n = len(rows)
        P0 = sum(p['v0'] for p in rows); P1 = sum(p['p1'] for p in rows)
        DV0f = sum(p['dv0_full'] for p in rows); DV1f = sum(p['dv1_full'] for p in rows)
        DV0h = sum(p['dv0_h6'] for p in rows); DV1h = sum(p['dv1_h6'] for p in rows)
        SV1 = sum(p['sv1'] for p in rows)
        # right-truncation share on FULL: value beyond 2025 unobserved; proxy = 1 - DV_full(H<=2025)
        # disclosed as the share of the H6 window that is beyond 2025 (structurally 0 for <=2018)
        yrs_obs = LAST_REAL_SEASON - (y + 1)          # observable future seasons at yr-1 vantage
        rec = dict(cls=y, n=n, P0=P0, P1=P1,
                   R_cand=P1 / P0 if P0 > 0 else float('nan'),
                   Rstar_full=DV1f / DV0f if DV0f > 0 else float('nan'),
                   Rstar_h6=DV1h / DV0h if (y in CLASSES_H6 and DV0h > 0) else None,
                   K0_full=DV0f / P0, K1_full=DV1f / P1,
                   K0_h6=DV0h / P0 if y in CLASSES_H6 else None,
                   K1_h6=DV1h / P1 if y in CLASSES_H6 else None,
                   DV1_over_P0_h6=DV1h / P0 if y in CLASSES_H6 else None,
                   SV1_share_full=SV1 / (SV1 + DV1f) if (SV1 + DV1f) > 0 else float('nan'),
                   yrs_observable=yrs_obs)
        out.append(rec)
    return out


LVL_ALL = level_table(False)
LVL_ND = level_table(True)


def summ(vals):
    v = np.array([x for x in vals if x is not None and not math.isnan(x)])
    return dict(n=len(v), mean=float(v.mean()), median=float(np.median(v)),
                p25=float(np.percentile(v, 25)), p75=float(np.percentile(v, 75)),
                lo=float(v.min()), hi=float(v.max()))


RNG = np.random.default_rng(SEED)


def cls_boot(vals):
    v = np.array([x for x in vals if x is not None and not math.isnan(x)])
    idx = RNG.integers(0, len(v), size=(B_BOOT, len(v)))
    m = v[idx].mean(axis=1)
    return [float(np.percentile(m, 5)), float(np.percentile(m, 95))]


LEVEL = dict(
    all_full=summ([r['Rstar_full'] for r in LVL_ALL]),
    all_h6=summ([r['Rstar_h6'] for r in LVL_ALL]),
    all_h6_ci90=cls_boot([r['Rstar_h6'] for r in LVL_ALL]),
    all_full_ci90=cls_boot([r['Rstar_full'] for r in LVL_ALL if r['cls'] <= 2015]),
    era1_h6=summ([r['Rstar_h6'] for r in LVL_ALL if r['cls'] <= 2014]),
    era2_h6=summ([r['Rstar_h6'] for r in LVL_ALL if r['cls'] >= 2015]),
    era1_full=summ([r['Rstar_full'] for r in LVL_ALL if r['cls'] <= 2014]),
    cand_mean_R=summ([r['R_cand'] for r in LVL_ALL]),
    nd_h6=summ([r['Rstar_h6'] for r in LVL_ND]),
    K0_h6=summ([r['K0_h6'] for r in LVL_ALL]),
    K1_h6=summ([r['K1_h6'] for r in LVL_ALL]),
)

# ---- (b) SPREAD -------------------------------------------------------------------------------------
# shares within class, pooled 2005-2018, H6
rows_s = []
for y in CLASSES_H6:
    rows = class_rows(y)
    mp1 = np.mean([p['p1'] for p in rows]); mdv = np.mean([p['dv1_h6'] for p in rows])
    mprod = np.mean([p['sv1'] for p in rows]); mped = np.mean([p['v0'] for p in rows])
    for p in rows:
        rows_s.append(dict(yr=y, key=p['key'], arm=p['arm'], g1=p['g1'],
                           x=p['p1'] / mp1, y=p['dv1_h6'] / mdv,
                           prod=p['sv1'] / mprod if mprod > 0 else 0.0,
                           ped=p['v0'] / mped))
X = np.array([r['x'] for r in rows_s]); Y = np.array([r['y'] for r in rows_s])
PR = np.array([r['prod'] for r in rows_s]); PD = np.array([r['ped'] for r in rows_s])
n_s = len(rows_s)
print('spread pool: %d players, classes 2005-2018' % n_s)


def ols(Xm, yv):
    A1 = np.column_stack([np.ones(len(yv))] + list(Xm))
    b, *_ = np.linalg.lstsq(A1, yv, rcond=None)
    return b


def slope_xy(x, y):
    return ols([x], y)[1]


b_point = float(slope_xy(X, Y))
idx = RNG.integers(0, n_s, size=(B_BOOT, n_s))
b_boot = np.array([slope_xy(X[i], Y[i]) for i in idx])
b_ci = [float(np.percentile(b_boot, 5)), float(np.percentile(b_boot, 95))]

# winsorized + spearman robustness
w99x = np.minimum(X, np.percentile(X, 99)); w99y = np.minimum(Y, np.percentile(Y, 99))
b_wins = float(slope_xy(w99x, w99y))
from scipy.stats import rankdata


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


sp_xy = spear(X, Y)

# per-class and per-era slopes
per_cls_b = {}
for y in CLASSES_H6:
    m = np.array([r['yr'] == y for r in rows_s])
    per_cls_b[y] = float(slope_xy(X[m], Y[m]))
era_b = {}
for nm, lo, hi in (('2005-2014', 2005, 2014), ('2015-2018', 2015, 2018)):
    m = np.array([lo <= r['yr'] <= hi for r in rows_s])
    era_b[nm] = float(slope_xy(X[m], Y[m]))

# S2 two-leg
bh = ols([PR, PD], Y)     # hindsight: [a, b_prod, b_ped]
bc = ols([PR, PD], X)     # candidate: [a, c_prod, c_ped]
W_hind = float(bh[1] / bh[2]); W_cand = float(bc[1] / bc[2])
wh_boot, wc_boot = [], []
for i in idx[:1000]:
    t = ols([PR[i], PD[i]], Y[i]); u = ols([PR[i], PD[i]], X[i])
    wh_boot.append(t[1] / t[2]); wc_boot.append(u[1] / u[2])
W_hind_ci = [float(np.percentile(wh_boot, 5)), float(np.percentile(wh_boot, 95))]
W_cand_ci = [float(np.percentile(wc_boot, 5)), float(np.percentile(wc_boot, 95))]
dW = np.array(wh_boot) - np.array(wc_boot)
dW_ci = [float(np.percentile(dW, 5)), float(np.percentile(dW, 95))]

# S3 low-g cells
def bucket(g):
    if g == 0: return '0'
    if g <= 4: return '1-4'
    if g <= 9: return '5-9'
    if g <= 15: return '10-15'
    return '16+'


cells = collections.defaultdict(list)
for r in rows_s:
    cells[bucket(r['g1'])].append(r)
S3 = {}
for b in ('0', '1-4', '5-9', '10-15', '16+'):
    rs = cells[b]
    S3[b] = dict(n=len(rs), mean_price_share=float(np.mean([r['x'] for r in rs])),
                 mean_real_share=float(np.mean([r['y'] for r in rs])),
                 gap=float(np.mean([r['y'] for r in rs]) - np.mean([r['x'] for r in rs])))
# riser/poor-starter terciles inside 1-4 and 5-9 (g>=1); tercile by prod share
S3T = {}
for b in ('1-4', '5-9'):
    rs = sorted(cells[b], key=lambda r: r['prod'])
    n3 = len(rs) // 3
    for nm, seg in (('poor', rs[:n3]), ('mid', rs[n3:2 * n3]), ('riser', rs[2 * n3:])):
        S3T['%s/%s' % (b, nm)] = dict(n=len(seg),
                                      mean_price_share=float(np.mean([r['x'] for r in seg])),
                                      mean_real_share=float(np.mean([r['y'] for r in seg])),
                                      gap=float(np.mean([r['y'] for r in seg]) - np.mean([r['x'] for r in seg])))

# ---- (c) translation: rho steepness ----------------------------------------------------------------
g_med = float(np.median([r['g1'] for r in rows_s if r['g1'] > 0]))
rho_med = rho(g_med)
target_rho = min(0.95, b_point * rho_med)
# solve tau' with same B: rho'(g_med)=target => tau' = g_med / (-ln(1-target))^(1/B)
tau_p = g_med / ((-math.log(1.0 - target_rho)) ** (1.0 / O31_B_RHO))

OUT = dict(meta=dict(prereg='PREREG_W2.md pushed first (792d979)', matrix_md5=md5f(CAND_P),
                     store='cb38ef11', seed=SEED, B_boot=B_BOOT, n_pop=len(POP), n_spread=n_s,
                     ruler='Order 32 S4 delivered-value construction, verbatim constants'),
           level=dict(per_class_all=LVL_ALL, per_class_nd=LVL_ND, summary=LEVEL),
           spread=dict(S1=dict(b=b_point, ci90=b_ci, b_winsor99=b_wins, spearman=sp_xy,
                               per_class=per_cls_b, per_era=era_b),
                       S2=dict(b_prod=float(bh[1]), b_ped=float(bh[2]), c_prod=float(bc[1]),
                               c_ped=float(bc[2]), W_hind=W_hind, W_cand=W_cand,
                               W_hind_ci90=W_hind_ci, W_cand_ci90=W_cand_ci, dW_ci90=dW_ci),
                       S3=dict(buckets=S3, terciles=S3T)),
           rho_translation=dict(g_med=g_med, rho_g_med=rho_med, b=b_point,
                                target_rho=target_rho, tau_prime=tau_p,
                                tau_current=O31_TAU_RHO, B=O31_B_RHO))
with open(os.path.join(HERE, 'RESULTS_W2.json'), 'w') as f:
    json.dump(OUT, f, indent=1)

# ---- console ---------------------------------------------------------------------------------------
print()
print('=== LEVEL (a): hindsight-fair yr0->1 class appreciation R* = DV1/DV0 ===')
print('%-5s %-3s %8s %8s %8s %8s %8s %8s %6s' % ('cls', 'n', 'R_cand', 'R*full', 'R*h6', 'K0h6', 'K1h6', 'SV1shF', 'yrsObs'))
for r in LVL_ALL:
    print('%-5d %-3d %8.4f %8.4f %8s %8s %8s %8.4f %6d' % (
        r['cls'], r['n'], r['R_cand'], r['Rstar_full'],
        '%.4f' % r['Rstar_h6'] if r['Rstar_h6'] else '--',
        '%.3f' % r['K0_h6'] if r['K0_h6'] else '--',
        '%.3f' % r['K1_h6'] if r['K1_h6'] else '--',
        r['SV1_share_full'], r['yrs_observable']))
print('summary:', json.dumps({k: v for k, v in LEVEL.items()}, indent=1))
print()
print('=== SPREAD (b) ===')
print('S1 slope b=%.4f ci90=[%.4f,%.4f] winsor99=%.4f spearman=%.4f' % (b_point, b_ci[0], b_ci[1], b_wins, sp_xy))
print('per-era:', era_b)
print('per-class:', {k: round(v, 3) for k, v in per_cls_b.items()})
print('S2 W_hind=%.4f ci=%s  W_cand=%.4f ci=%s  d(W) ci=%s' % (W_hind, W_hind_ci, W_cand, W_cand_ci, dW_ci))
print('S3 buckets:', json.dumps(S3, indent=1))
print('S3 terciles:', json.dumps(S3T, indent=1))
print()
print('rho translation: g_med=%.1f rho=%.4f -> target %.4f, tau %.2f -> %.2f' % (
    g_med, rho_med, target_rho, O31_TAU_RHO, tau_p))
print('wrote RESULTS_W2.json')
