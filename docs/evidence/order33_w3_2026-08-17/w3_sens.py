#!/usr/bin/env python
# ORDER 33 W3 — STEP 3: sensitivities.
#  S-A: FULL current season (games >= 10u) — the prereg'd threshold sensitivity. This is the
#       measurement-noise probe: a 6-9 game avg is a noisy reading, and at FIXED OBSERVED output a
#       noisy reading is more likely above true skill, biasing low-exposure next-season change DOWN.
#  S-B: POST-HOC (disclosed, not prereg'd): current-season games/22 added as a control.
#  S-C: age-23+ subsample regressions (the key population), 6u and 10u variants.
#  S-D: FIRST2 split by age band 18-22 vs 23+ (interaction read).
# Same frame, cluster bootstrap B=1000 seed 33.
import json, os, collections
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(OUT, 'W3_TABLE.json')))
META = T['meta']; ROWS = T['rows']; BARS = META['bars']
BANDS = ['B0<-10', 'B1[-10,0)', 'B2[0,10)', 'B3>=10']

def prep(ming):
    base = [dict(r) for r in ROWS if 2005 <= r['year'] <= 2025 and r['games'] >= ming * r['u']
            and 18 <= r['age'] <= 30]
    for r in base:
        x = r['avg'] - BARS[r['pos']]
        r['band'] = 0 if x < -10 else (1 if x < 0 else (2 if x < 10 else 3))
        r['first2'] = 1.0 if r['sidx'] <= 2 else 0.0
    cond = [r for r in base if r['next_full6']]
    for r in cond: r['d1'] = r['next_avg'] - r['avg']
    # age curve on THIS sample (pool to n>=20)
    curve = {}
    for tall in (False, True):
        sub = collections.defaultdict(list)
        for r in cond:
            if r['tall'] == tall: sub[min(r['age'], 27)].append(r['d1'])
        groups = []; cur = []; curn = []
        for a in sorted(sub):
            cur.extend(sub[a]); curn.append(a)
            if len(cur) >= 20: groups.append((tuple(curn), cur)); cur = []; curn = []
        if cur and groups:
            pa, pv = groups[-1]; groups[-1] = (pa + tuple(curn), pv + cur)
        elif cur:
            groups.append((tuple(curn), cur))
        for aa, vv in groups:
            for a in aa: curve[(tall, a)] = float(np.mean(vv))
    for r in cond: r['dA'] = r['d1'] - curve[(r['tall'], min(r['age'], 27))]
    return base, cond

POSL = ['KPD', 'KPF', 'RUCK', 'SD', 'SF']
def design(rows_, expo_cols, with_games=False):
    n = len(rows_); cols = [np.ones(n)]; names = ['const']
    ages = sorted(set(r['age'] for r in rows_))
    for a in ages[1:]:
        cols.append(np.array([1.0 if r['age'] == a else 0.0 for r in rows_])); names.append('age%d' % a)
    for p_ in POSL:
        cols.append(np.array([1.0 if r['pos'] == p_ else 0.0 for r in rows_])); names.append(p_)
    cols.append(np.array([r['avg'] - BARS[r['pos']] for r in rows_])); names.append('avg-bar')
    for b in (0, 1, 3):
        cols.append(np.array([1.0 if r['band'] == b else 0.0 for r in rows_])); names.append(BANDS[b])
    if with_games:
        cols.append(np.array([r['games'] / 22.0 for r in rows_])); names.append('games/22')
    for nm, f in expo_cols:
        cols.append(np.array([f(r) for r in rows_], dtype=float)); names.append(nm)
    return np.column_stack(cols), names

def boot(rows_, expo_cols, ykey='dA', B=1000, seed=33, with_games=False):
    X, names = design(rows_, expo_cols, with_games)
    y = np.array([r[ykey] for r in rows_], dtype=float)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    groups = collections.defaultdict(list)
    for i, r in enumerate(rows_): groups[r['key']].append(i)
    garr = [np.array(v) for _, v in sorted(groups.items())]
    rng = np.random.default_rng(seed)
    bs = np.empty((B, len(names)))
    for b in range(B):
        idx = np.concatenate([garr[i] for i in rng.integers(0, len(garr), len(garr))])
        bs[b] = np.linalg.lstsq(X[idx], y[idx], rcond=None)[0]
    return names, beta, np.percentile(bs, 2.5, axis=0), np.percentile(bs, 97.5, axis=0)

L = []; P = L.append
P('ORDER 33 W3 SENSITIVITIES — store %s — seed 33' % META['store_md5'][:8])

def rep(tag, rows_, expo_cols, show, **kw):
    names, beta, lo, hi = boot(rows_, expo_cols, **kw)
    P('%s (n=%d)' % (tag, len(rows_)))
    for nm in show:
        i = names.index(nm)
        star = ' *' if (lo[i] > 0 or hi[i] < 0) else ''
        P('  %-14s %+7.3f  [%+7.3f, %+7.3f]%s' % (nm, beta[i], lo[i], hi[i], star))

base6, cond6 = prep(6.0)
base10, cond10 = prep(10.0)
P('')
P('S-A FULL current season (games>=10u), prereg sensitivity — main-run values in brackets for compare')
rep('  S-A cg/50', cond10, [('cg/50', lambda r: r['careergames'] / 50.0)], ['cg/50'])
P('    [main 6u: +2.343 (+1.833,+2.848)*]')
rep('  S-A FIRST2', cond10, [('FIRST2', lambda r: r['first2'])], ['FIRST2'])
P('    [main 6u: -2.142 (-3.173,-1.122)*]')
rep('  S-A sidx dummies', cond10,
    [('sidx=%d' % k, (lambda kk: (lambda r: 1.0 if r['sidx'] == kk else 0.0))(k)) for k in (1, 2, 3, 4)],
    ['sidx=1', 'sidx=2', 'sidx=3', 'sidx=4'])
P('    [main 6u: -3.842*, -1.985*, -0.239, -1.547*]')
P('')
P('S-B POST-HOC: current games/22 added as control (games known at valuation time; NOT prereg-d)')
rep('  S-B 6u FIRST2 + games ctrl', cond6, [('FIRST2', lambda r: r['first2'])], ['games/22', 'FIRST2'], with_games=True)
rep('  S-B 10u FIRST2 + games ctrl', cond10, [('FIRST2', lambda r: r['first2'])], ['games/22', 'FIRST2'], with_games=True)
rep('  S-B 6u cg/50 + games ctrl', cond6, [('cg/50', lambda r: r['careergames'] / 50.0)], ['games/22', 'cg/50'], with_games=True)
P('')
P('S-C AGE 23+ SUBSAMPLE (the population the owner is talking about), full controls')
c23_6 = [r for r in cond6 if r['age'] >= 23]
c23_10 = [r for r in cond10 if r['age'] >= 23]
rep('  S-C 23+ 6u FIRST2', c23_6, [('FIRST2', lambda r: r['first2'])], ['FIRST2'])
rep('  S-C 23+ 10u FIRST2', c23_10, [('FIRST2', lambda r: r['first2'])], ['FIRST2'])
rep('  S-C 23+ 6u FIRST2 + games ctrl', c23_6, [('FIRST2', lambda r: r['first2'])], ['games/22', 'FIRST2'], with_games=True)
rep('  S-C 23+ 6u cg/50', c23_6, [('cg/50', lambda r: r['careergames'] / 50.0)], ['cg/50'])
rep('  S-C 23+ 6u sidx dummies', c23_6,
    [('sidx=%d' % k, (lambda kk: (lambda r: 1.0 if r['sidx'] == kk else 0.0))(k)) for k in (1, 2, 3, 4)],
    ['sidx=1', 'sidx=2', 'sidx=3', 'sidx=4'])
P('')
P('S-D FIRST2 by age band (separate columns, one regression)')
rep('  S-D 6u', cond6,
    [('F2xU23', lambda r: r['first2'] * (1.0 if r['age'] < 23 else 0.0)),
     ('F2x23+', lambda r: r['first2'] * (1.0 if r['age'] >= 23 else 0.0))],
    ['F2xU23', 'F2x23+'])
rep('  S-D 10u', cond10,
    [('F2xU23', lambda r: r['first2'] * (1.0 if r['age'] < 23 else 0.0)),
     ('F2x23+', lambda r: r['first2'] * (1.0 if r['age'] >= 23 else 0.0))],
    ['F2xU23', 'F2x23+'])
P('')
P('Context ns: 6u cond=%d (23+ %d), 10u cond=%d (23+ %d)' %
  (len(cond6), len(c23_6), len(cond10), len(c23_10)))
# how many first2 rows in the 23+ conditional samples
P('FIRST2 rows in 23+ cond: 6u %d, 10u %d' %
  (sum(1 for r in c23_6 if r['first2']), sum(1 for r in c23_10 if r['first2'])))
open(os.path.join(OUT, 'SENS_W3_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
