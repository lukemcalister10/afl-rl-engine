#!/usr/bin/env python3
# =====================================================================================================
# ORDER 32 SEAT S4 -- THE OLD-LAW SHOOTOUT. READ-ONLY.
# Everything here executes the rule fixed in PREREG_S4.md (committed and pushed FIRST, bf39901).
# No engine import, no board build, no store write. Inputs: the two per-entrant matrices.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np
from scipy.stats import rankdata

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'
OLD_P = SP + '/per_entrant_O29CFINAL.json'

B_BOOT = 2000
SEED = 32
FM = {'paddy-mccartin', 'thomas-boyd'}
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
LAST_REAL_SEASON = 2025   # 2026 in progress -- right censor (prereg SS2)
ENTRY_FLOOR = 2005        # left censor (prereg SS2)


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


A = json.load(open(CAND_P))
B = json.load(open(OLD_P))
print('inputs: CAND %s md5 %s  |  OLD %s md5 %s' % (
    os.path.basename(CAND_P), md5f(CAND_P)[:8], os.path.basename(OLD_P), md5f(OLD_P)[:8]))
Arecs = {r['key']: r for r in A['recs']}
Brecs = {r['key']: r for r in B['recs']}
assert len(Arecs) == len(A['recs']) == 2648, 'dup or missing keys in candidate matrix'
assert set(Arecs) == set(Brecs), 'key sets differ'
for k in Arecs:
    assert Arecs[k]['yrs'] == Brecs[k]['yrs'] and Arecs[k]['seasons'] == Brecs[k]['seasons']

# ---- per-player season values (identical between matrices; computed once) ---------------------------
SV = {}       # key -> {year: season value}
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


def dv1(k, Y):
    return SV[k].get(Y + 1, 0.0)


def dvrest(k, Y):
    return sum((1.14 ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


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


def band_of(pick):
    if pick <= 10: return '1-10'
    if pick <= 20: return '11-20'
    if pick <= 30: return '21-30'
    if pick <= 40: return '31-40'
    return '41-64'


def era_of(y):
    return '2005-2014' if y <= 2014 else '2015+'


# ---- vantage cohorts --------------------------------------------------------------------------------
# rows: dict key -> per-N dict of (cand, old, pedA, pedB, pick, dv1, dvrest, arm, band, era)
cohorts = {}       # N -> list of row dicts
excl = collections.Counter()
for N in range(0, 7):
    rows = []
    for k, r in Arecs.items():
        if k in FM:
            excl[(N, 'force_majeure')] += 1; continue
        arm = arm_of(r)
        if arm is None:
            excl[(N, 'no_arm')] += 1; continue
        yr = r['year']
        if yr < ENTRY_FLOOR:
            excl[(N, 'left_censor')] += 1; continue
        if yr + N + 1 > LAST_REAL_SEASON:
            excl[(N, 'future_unobservable')] += 1; continue
        Y = yr + N
        if N == 0:
            cand, old = float(r['v0']), float(Brecs[k]['v0'])
        else:
            vp, vpB = r['vpath'], Brecs[k]['vpath']
            if len(vp) < N or vp[N - 1] is None or vpB[N - 1] is None:
                excl[(N, 'window_closed_before_N')] += 1; continue
            cand, old = float(vp[N - 1]), float(vpB[N - 1])
        rows.append(dict(key=k, cand=cand, old=old,
                         pedA=float(r['v0']), pedB=float(Brecs[k]['v0']),
                         negpick=-float(r['pick']) if arm == 'ND' else None,
                         dv1=dv1(k, Y), dvrest=dvrest(k, Y),
                         arm=arm, band=band_of(r['pick']) if arm == 'ND' else None,
                         era=era_of(yr)))
    cohorts[N] = rows
    nd = sum(1 for x in rows if x['arm'] == 'ND')
    print('vantage N=%d: cohort %d (ND %d, pool %d); excluded window_closed=%d future_unobs=%d' % (
        N, len(rows), nd, len(rows) - nd,
        excl[(N, 'window_closed_before_N')], excl[(N, 'future_unobservable')]))


# ---- metrics ----------------------------------------------------------------------------------------
def ranks(m):
    return rankdata(m, axis=-1)


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


def spear_mat(X, Y):
    """row-wise spearman for (B,n) matrices."""
    rx = rankdata(X, axis=1); ry = rankdata(Y, axis=1)
    rx = rx - rx.mean(axis=1, keepdims=True); ry = ry - ry.mean(axis=1, keepdims=True)
    den = np.sqrt((rx ** 2).sum(axis=1) * (ry ** 2).sum(axis=1))
    with np.errstate(invalid='ignore', divide='ignore'):
        return (rx * ry).sum(axis=1) / den


def nmae(p, t):
    mp, mt = p.mean(), t.mean()
    if mp <= 0 or mt <= 0:
        return float('nan')
    return float(np.abs(p / mp - t / mt).mean())


def nmae_mat(P, T):
    mp = P.mean(axis=1, keepdims=True); mt = T.mean(axis=1, keepdims=True)
    with np.errstate(invalid='ignore', divide='ignore'):
        out = np.abs(P / mp - T / mt).mean(axis=1)
    out[(mp[:, 0] <= 0) | (mt[:, 0] <= 0)] = np.nan
    return out


RNG = np.random.default_rng(SEED)
RESULTS = []


def score_cell(label, N, horizon, rows, pop_name):
    """One cell: both machines + pedigree baselines, point + bootstrap, verdicts per prereg SS5."""
    n = len(rows)
    tgt = np.array([r[horizon] for r in rows])
    cell = dict(pop=pop_name, N=N, horizon=horizon, n=n, label=label)
    if n < 20 or len(set(np.round(tgt, 9))) < 5:
        cell['status'] = 'n<20 unscored' if n < 20 else 'target<5 distinct unscored'
        RESULTS.append(cell); return cell
    cell['status'] = 'scored'
    cand = np.array([r['cand'] for r in rows])
    old = np.array([r['old'] for r in rows])
    pedA = np.array([r['pedA'] for r in rows])
    pedB = np.array([r['pedB'] for r in rows])
    haspick = all(r['negpick'] is not None for r in rows)
    npick = np.array([r['negpick'] for r in rows]) if haspick else None
    cell['zero_target_share'] = float((tgt == 0).mean())

    idx = RNG.integers(0, n, size=(B_BOOT, n))
    Tm = tgt[idx]; Cm = cand[idx]; Om = old[idx]

    # M1
    rc, ro = spear(cand, tgt), spear(old, tgt)
    rcB, roB = spear_mat(Cm, Tm), spear_mat(Om, Tm)
    d = rcB - roB
    lo, hi = np.nanpercentile(d, [5, 95])
    point = rc - ro
    verdict = ('candidate' if (point > 0 and lo > 0) else
               'oldlaw' if (point < 0 and hi < 0) else 'tie')
    cell['M1'] = dict(rho_cand=round(rc, 4), rho_old=round(ro, 4),
                      rho_cand_ci=[round(float(np.nanpercentile(rcB, 5)), 4), round(float(np.nanpercentile(rcB, 95)), 4)],
                      rho_old_ci=[round(float(np.nanpercentile(roB, 5)), 4), round(float(np.nanpercentile(roB, 95)), 4)],
                      delta=round(point, 4), delta_ci=[round(float(lo), 4), round(float(hi), 4)],
                      verdict=verdict)
    # M2
    ec, eo = nmae(cand, tgt), nmae(old, tgt)
    if not (math.isnan(ec) or math.isnan(eo)):
        ecB, eoB = nmae_mat(Cm, Tm), nmae_mat(Om, Tm)
        d2 = eoB - ecB          # >0 favours candidate
        lo2, hi2 = np.nanpercentile(d2, [5, 95])
        point2 = eo - ec
        verdict2 = ('candidate' if (point2 > 0 and lo2 > 0) else
                    'oldlaw' if (point2 < 0 and hi2 < 0) else 'tie')
        cell['M2'] = dict(nmae_cand=round(ec, 4), nmae_old=round(eo, 4),
                          nmae_cand_ci=[round(float(np.nanpercentile(ecB, 5)), 4), round(float(np.nanpercentile(ecB, 95)), 4)],
                          nmae_old_ci=[round(float(np.nanpercentile(eoB, 5)), 4), round(float(np.nanpercentile(eoB, 95)), 4)],
                          delta=round(point2, 4), delta_ci=[round(float(lo2), 4), round(float(hi2), 4)],
                          verdict=verdict2)
    else:
        cell['M2'] = dict(status='unscored (nonpositive mean)')
    # pedigree baselines: own rho + CI on the SAME resamples
    ped = {}
    for nm, arr in (('pick', npick), ('v0_cand', pedA), ('v0_old', pedB)):
        if arr is None:
            continue
        r0 = spear(arr, tgt)
        rB = spear_mat(arr[idx], Tm)
        plo, phi = np.nanpercentile(rB, [5, 95])
        ped[nm] = dict(rho=round(r0, 4), ci=[round(float(plo), 4), round(float(phi), 4)],
                       effective=bool(plo > 0 or phi < 0))
    cell['pedigree'] = ped
    RESULTS.append(cell)
    return cell


# ---- enumerate cells in FIXED order (rng determinism) ----------------------------------------------
for N in range(1, 7):
    rows = cohorts[N]
    for hz in ('dv1', 'dvrest'):
        nd = [r for r in rows if r['arm'] == 'ND']
        score_cell('PRIMARY ND', N, hz, nd, 'ND')
        for b in ('1-10', '11-20', '21-30', '31-40', '41-64'):
            score_cell('band ' + b, N, hz, [r for r in nd if r['band'] == b], 'ND band ' + b)
        for e in ('2005-2014', '2015+'):
            score_cell('era ' + e, N, hz, [r for r in nd if r['era'] == e], 'ND era ' + e)
        for arm in ('RD', 'MSD', 'OTHERPOOL'):
            score_cell('arm ' + arm, N, hz, [r for r in rows if r['arm'] == arm], arm)
        score_cell('POOL-ALL', N, hz, [r for r in rows if r['arm'] != 'ND'], 'POOL-ALL')

# supplementary N=0 (day-0)
for hz in ('dv1', 'dvrest'):
    rows = cohorts[0]
    nd = [r for r in rows if r['arm'] == 'ND']
    score_cell('DAY0 ND', 0, hz, nd, 'ND day0')
    score_cell('DAY0 POOL-ALL', 0, hz, [r for r in rows if r['arm'] != 'ND'], 'POOL-ALL day0')

out = dict(meta=dict(prereg='PREREG_S4.md (pushed before any comparison number: commit bf39901)',
                     cand=dict(path=CAND_P, md5=md5f(CAND_P)),
                     old=dict(path=OLD_P, md5=md5f(OLD_P)),
                     B_boot=B_BOOT, seed=SEED, bars=BARS,
                     exclusions={('N%d:%s' % k): v for k, v in sorted(excl.items())}),
           cells=RESULTS)
with open(os.path.join(HERE, 'RESULTS_S4.json'), 'w') as f:
    json.dump(out, f, indent=1)

# ---- console verdict summary ------------------------------------------------------------------------
def tally(pred):
    t = collections.Counter()
    for c in RESULTS:
        if c['status'] != 'scored' or not pred(c):
            continue
        for m in ('M1', 'M2'):
            v = c.get(m, {}).get('verdict')
            if v:
                t[v] += 1
    return t


print()
print('PRIMARY ND (N=1..6 x 2 horizons x 2 metrics):', dict(tally(lambda c: c['pop'] == 'ND' and c['N'] >= 1)))
print('ALL SCORED CELLS:', dict(tally(lambda c: True)))
print('wrote RESULTS_S4.json  cells=%d' % len(RESULTS))
