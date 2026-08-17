#!/usr/bin/env python3
# =====================================================================================================
# ORDER 33 SEAT W5 -- VETERAN MARK VALIDATION (ages 27-31). READ-ONLY.
# Executes the rules fixed in PREREG_W5.md (pushed first, commit dd5cd25). Ruler reused verbatim from
# Order 32 S4 (docs/evidence/order32_s4_2026-08-17/s4_shootout.py). No engine import, no store write.
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np
from scipy.stats import rankdata

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
import sys
LABEL = sys.argv[1]
CAND_P = SP + '/per_entrant_%s.json' % LABEL
BOARD_P = SP + '/cand31.json'

B_BOOT = 2000
SEED = 33
FM = {'paddy-mccartin', 'thomas-boyd'}
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
VANTAGE_LAST = 2021
AGES = list(range(23, 32))
TEST_AGES = [27, 28, 29, 30, 31]
ANCHOR_AGES = {23, 24, 25, 26}
POSG = {'KPD': 'TALL', 'KPF': 'TALL', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL', 'RUCK': 'RUCK'}


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


A = json.load(open(CAND_P))
recs = A['recs']
print('input: %s md5 %s recs %d' % (os.path.basename(CAND_P), md5f(CAND_P)[:8], len(recs)))

# ---- per-player season values (S4 ruler) ------------------------------------------------------------
SV = {}
SBAR = {}   # key -> {year: bar}
for r in recs:
    d, bb = {}, {}
    for s in r['seasons']:
        if s['year'] > LAST_REAL_SEASON:
            continue
        g = s.get('bar')
        if g not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * season_raw(s['avg'], g)
        bb[s['year']] = g
    SV[r['key']] = d
    SBAR[r['key']] = bb


def dvrest(k, Y):
    return sum((1.14 ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


# ---- extract vantage rows ---------------------------------------------------------------------------
rows = []          # PRIMARY (career-complete)
rows_cens = []     # SECONDARY (censored)
excl = collections.Counter()
for r in recs:
    k = r['key']
    if k in FM:
        excl['force_majeure'] += 1; continue
    arm = arm_of(r)
    if arm is None:
        excl['no_arm'] += 1; continue
    if r['year'] < ENTRY_FLOOR:
        excl['left_censor'] += 1; continue
    lg = r.get('last_game_year')
    complete = (r['retired_now'] or r['delisted']) and (lg is not None and lg <= LAST_REAL_SEASON) \
        and not any(s['year'] > LAST_REAL_SEASON for s in r['seasons'])
    for i, Y in enumerate(r['yrs']):
        if Y > VANTAGE_LAST:
            continue
        a = r['age_draft'] + (Y - r['year'])
        if a not in AGES:
            continue
        m = r['vpath'][i]
        if m is None:
            excl['vpath_none'] += 1; continue
        bar = SBAR[k].get(Y)
        pg = POSG.get(bar if bar is not None else r.get('pos'), None)
        has_future = any(t > Y for t in SV[k])
        row = dict(key=k, age=a, Y=Y, mark=float(m), R=dvrest(k, Y),
                   t2=SV[k].get(Y, 0.0) + SV[k].get(Y - 1, 0.0),
                   pos=pg, era=('<=2015' if Y <= 2015 else '2016+'),
                   surv=has_future, arm=arm)
        (rows if complete else rows_cens).append(row)

print('primary rows %d  censored rows %d  excl %s' % (len(rows), len(rows_cens), dict(excl)))

# tier terciles within age cell (primary cohort)
for a in AGES:
    cell = [r for r in rows if r['age'] == a]
    if not cell:
        continue
    t2 = np.array([r['t2'] for r in cell])
    q1, q2 = np.percentile(t2, [100 / 3, 200 / 3])
    for r in cell:
        r['tier'] = 'role' if r['t2'] <= q1 else ('mid' if r['t2'] <= q2 else 'star')
for r in rows_cens:
    r['tier'] = None

players = sorted({r['key'] for r in rows})
by_player = collections.defaultdict(list)
for r in rows:
    by_player[r['key']].append(r)

# survivor-linked pairs for M-RATE: same player at a and a+1 (consecutive vantage years)
pairs = []
for k, rl in by_player.items():
    d = {r['age']: r for r in rl}
    for a in range(23, 31):
        if a in d and (a + 1) in d and d[a + 1]['Y'] == d[a]['Y'] + 1:
            pairs.append(dict(key=k, a=a, m0=d[a]['mark'], m1=d[a + 1]['mark'],
                              r0=d[a]['R'], r1=d[a + 1]['R']))

RNG = np.random.default_rng(SEED)


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


def view_rows(view, base):
    return base if view == 'full' else [r for r in base if r['surv']]


def cell_stats(sel, anchor_ratio):
    """ratio of means and anchored profile for a list of rows."""
    if len(sel) < 20:
        return None
    M = float(np.mean([r['mark'] for r in sel]))
    R = float(np.mean([r['R'] for r in sel]))
    if R <= 0:
        return None
    ratio = M / R
    return dict(n=len(sel), mean_mark=round(M, 1), mean_R=round(R, 1), ratio=round(ratio, 4),
                B=round(ratio / anchor_ratio, 4) if anchor_ratio else None)


def anchor_of(sel_rows):
    anc = [r for r in sel_rows if r['age'] in ANCHOR_AGES]
    if len(anc) < 20:
        return None
    M = np.mean([r['mark'] for r in anc]); R = np.mean([r['R'] for r in anc])
    return float(M / R) if R > 0 else None


# ---- bootstrap machinery: cluster by player ---------------------------------------------------------
pl_index = {k: i for i, k in enumerate(players)}
boot_draws = [RNG.integers(0, len(players), size=len(players)) for _ in range(B_BOOT)]

R_ALL = np.array([r['mark'] for r in rows]), np.array([r['R'] for r in rows]), \
    np.array([r['age'] for r in rows]), np.array([r['surv'] for r in rows])
ROW_PL = np.array([pl_index[r['key']] for r in rows])
ROW_IDX_BY_PL = [np.where(ROW_PL == i)[0] for i in range(len(players))]


def boot_profiles(subset_fn, view):
    """dict age -> B_BOOT bootstrap values of anchored B(a), cluster-resampled by player."""
    mark_a, R_a, age_a, surv_a = R_ALL
    inview = np.array([bool(subset_fn(r)) and (view == 'full' or r['surv']) for r in rows])
    # per-player row indices restricted to subset+view
    per_pl = [ix[inview[ix]] for ix in ROW_IDX_BY_PL]
    is_anchor = np.isin(age_a, list(ANCHOR_AGES))
    out = {a: [] for a in TEST_AGES}
    for bp in boot_draws:
        ix = np.concatenate([per_pl[i] for i in bp if per_pl[i].size]) if len(bp) else np.array([], int)
        if ix.size == 0:
            for a in TEST_AGES:
                out[a].append(np.nan)
            continue
        anc_m = is_anchor[ix]
        if anc_m.sum() < 20:
            for a in TEST_AGES:
                out[a].append(np.nan)
            continue
        Ranc = R_a[ix][anc_m].mean()
        anc = mark_a[ix][anc_m].mean() / Ranc if Ranc > 0 else np.nan
        for a in TEST_AGES:
            am = age_a[ix] == a
            if am.sum() < 20 or not np.isfinite(anc):
                out[a].append(np.nan); continue
            Rc = R_a[ix][am].mean()
            out[a].append((mark_a[ix][am].mean() / Rc) / anc if Rc > 0 else np.nan)
    return out


RESULTS = dict(meta=dict(prereg='PREREG_W5.md pushed first (commit dd5cd25)',
                         input=dict(path=CAND_P, md5=md5f(CAND_P)),
                         board=dict(path=BOARD_P, md5=md5f(BOARD_P)),
                         B_boot=B_BOOT, seed=SEED, vantage=[ENTRY_FLOOR, VANTAGE_LAST],
                         primary_rows=len(rows), censored_rows=len(rows_cens),
                         exclusions=dict(excl)),
               bias={}, rate={}, rank={}, exit={}, censored={}, tiers={}, positions={}, eras={})


def run_bias(name, subset_fn, store):
    for view in ('full', 'survivor'):
        base = [r for r in rows if subset_fn(r)]
        sv = view_rows(view, base)
        anc = anchor_of(sv)
        prof = {}
        boots = boot_profiles(subset_fn, view)
        for a in TEST_AGES:
            cs = cell_stats([r for r in sv if r['age'] == a], anc)
            if cs is None:
                prof[a] = dict(status='unscored (n<20 or R<=0)')
                continue
            bs = np.array(boots[a], dtype=float)
            lo, hi = np.nanpercentile(bs, [5, 95])
            called = (cs['B'] is not None) and (lo > 1.0 or hi < 1.0)
            cs.update(B_ci=[round(float(lo), 4), round(float(hi), 4)],
                      called=('over-mark' if (called and cs['B'] > 1) else
                              'under-mark' if called else 'no'))
            prof[a] = cs
        store['%s|%s' % (name, view)] = dict(anchor_ratio=round(anc, 4) if anc else None, cells=prof)
        print('  bias[%s|%s] anchor=%.3f  ' % (name, view, anc or float('nan')) +
              ' '.join('%d:B=%s%s' % (a, prof[a].get('B'), '*' if prof[a].get('called') not in (None, 'no') else '')
                       for a in TEST_AGES))


print('\n== M-BIAS ==')
run_bias('ALL', lambda r: True, RESULTS['bias'])
for pg in ('TALL', 'SMALL', 'RUCK'):
    run_bias('pos:' + pg, lambda r, p=pg: r['pos'] == p, RESULTS['positions'])
for tr in ('star', 'mid', 'role'):
    run_bias('tier:' + tr, lambda r, t=tr: r.get('tier') == t, RESULTS['tiers'])
for e in ('<=2015', '2016+'):
    run_bias('era:' + e, lambda r, e0=e: r['era'] == e0, RESULTS['eras'])

# ---- exit shares ------------------------------------------------------------------------------------
print('\n== EXIT SHARE (primary, full) ==')
for a in AGES:
    cell = [r for r in rows if r['age'] == a]
    if not cell:
        continue
    ex = np.mean([0.0 if r['surv'] else 1.0 for r in cell])
    z = np.mean([1.0 if r['R'] == 0 else 0.0 for r in cell])
    RESULTS['exit'][a] = dict(n=len(cell), exit_share=round(float(ex), 4), zero_R_share=round(float(z), 4))
    print('  age %d n=%d exit(no season after Y)=%.3f  R==0 share=%.3f' % (a, len(cell), ex, z))

# ---- M-RATE -----------------------------------------------------------------------------------------
print('\n== M-RATE (survivor-linked pairs) ==')
by_step = collections.defaultdict(list)
for p in pairs:
    by_step[p['a']].append(p)
for a in range(26, 31):
    P = by_step[a]
    if len(P) < 20:
        RESULTS['rate'][a] = dict(status='n<20'); continue
    em = np.mean([p['m1'] for p in P]) / np.mean([p['m0'] for p in P])
    rm = np.mean([p['r1'] for p in P]) / np.mean([p['r0'] for p in P])
    # cluster bootstrap: one pair per player at this step, so resample pairs directly
    M0 = np.array([p['m0'] for p in P]); M1 = np.array([p['m1'] for p in P])
    R0 = np.array([p['r0'] for p in P]); R1 = np.array([p['r1'] for p in P])
    bE, bR = [], []
    for _ in range(B_BOOT):
        ix = RNG.integers(0, len(P), size=len(P))
        bE.append(M1[ix].mean() / M0[ix].mean())
        m0 = R0[ix].mean()
        bR.append(R1[ix].mean() / m0 if m0 > 0 else np.nan)
    d = np.array(bE) - np.array(bR)
    lo, hi = np.nanpercentile(d, [5, 95])
    RESULTS['rate'][a] = dict(n=len(P), step='%d->%d' % (a, a + 1),
                              engine_decline=round(float(em), 4), realized_decline=round(float(rm), 4),
                              engine_ci=[round(float(x), 4) for x in np.nanpercentile(bE, [5, 95])],
                              realized_ci=[round(float(x), 4) for x in np.nanpercentile(bR, [5, 95])],
                              delta=round(float(em - rm), 4), delta_ci=[round(float(lo), 4), round(float(hi), 4)],
                              verdict=('engine_shallower' if (em > rm and lo > 0) else
                                       'engine_steeper' if (em < rm and hi < 0) else 'match'))
    print('  %d->%d n=%d engine %.3f realized %.3f delta %.3f [%.3f,%.3f] %s' % (
        a, a + 1, len(P), em, rm, em - rm, lo, hi, RESULTS['rate'][a]['verdict']))

# ---- M-RANK -----------------------------------------------------------------------------------------
print('\n== M-RANK (Spearman mark vs R, full primary) ==')
for label, fn in (('ALL', lambda r: True),
                  ('era<=2015', lambda r: r['era'] == '<=2015'),
                  ('era2016+', lambda r: r['era'] == '2016+')):
    for a in TEST_AGES:
        cell = [r for r in rows if fn(r) and r['age'] == a]
        if len(cell) < 20:
            RESULTS['rank']['%s|%d' % (label, a)] = dict(status='n<20'); continue
        x = np.array([r['mark'] for r in cell]); y = np.array([r['R'] for r in cell])
        rho = spear(x, y)
        bs = []
        for _ in range(B_BOOT):
            ix = RNG.integers(0, len(cell), size=len(cell))
            bs.append(spear(x[ix], y[ix]))
        lo, hi = np.nanpercentile(bs, [5, 95])
        RESULTS['rank']['%s|%d' % (label, a)] = dict(n=len(cell), rho=round(rho, 4),
                                                     ci=[round(float(lo), 4), round(float(hi), 4)])
        print('  %s age %d n=%d rho=%.3f [%.3f,%.3f]' % (label, a, len(cell), rho, lo, hi))

# ---- censored secondary (disclosed) -----------------------------------------------------------------
anc_c = anchor_of(rows)   # anchor from primary (censored anchor cells are tiny) -- disclosed
for a in TEST_AGES:
    cell = [r for r in rows_cens if r['age'] == a]
    cs = cell_stats(cell, anc_c)
    RESULTS['censored'][a] = cs if cs else dict(status='n<20', n=len(cell))
RESULTS['censored']['note'] = 'censored rows use PRIMARY anchor; R right-censored at 2025 -> ratios biased up; never pooled'

with open(os.path.join(HERE, 'RESULTS_W5_%s.json' % LABEL), 'w') as f:
    json.dump(RESULTS, f, indent=1)
print('\nwrote RESULTS_W5_%s.json' % LABEL)
