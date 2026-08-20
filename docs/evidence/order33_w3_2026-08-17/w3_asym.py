#!/usr/bin/env python
# ORDER 33 W3 — STEP 4 (POST-HOC, disclosed as such): the shrinkage probe.
# If the FIRST2 deficit is really TRACK-RECORD RELIABILITY (a short career's current avg is a
# noisier reading of true level, so it regresses harder toward the position mean in BOTH
# directions), then FIRST2 x (above-bar) should be strongly negative while FIRST2 x (below-bar)
# should be ~0 or positive. If it were a uniform level deficit ("first-years just decline"),
# both interactions would be equally negative. Cluster bootstrap B=1000 seed 33.
import json, os, collections
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(OUT, 'W3_TABLE.json')))
META = T['meta']; ROWS = T['rows']; BARS = META['bars']
BANDS = ['B0<-10', 'B1[-10,0)', 'B2[0,10)', 'B3>=10']

base = [dict(r) for r in ROWS if 2005 <= r['year'] <= 2025 and r['games'] >= 6.0 * r['u']
        and 18 <= r['age'] <= 30]
for r in base:
    x = r['avg'] - BARS[r['pos']]
    r['band'] = 0 if x < -10 else (1 if x < 0 else (2 if x < 10 else 3))
    r['first2'] = 1.0 if r['sidx'] <= 2 else 0.0
cond = [r for r in base if r['next_full6']]
for r in cond: r['d1'] = r['next_avg'] - r['avg']
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

POSL = ['KPD', 'KPF', 'RUCK', 'SD', 'SF']
def run(rows_, expo_cols, show, tag):
    n = len(rows_); cols = [np.ones(n)]; names = ['const']
    for a in sorted(set(r['age'] for r in rows_))[1:]:
        cols.append(np.array([1.0 if r['age'] == a else 0.0 for r in rows_])); names.append('age%d' % a)
    for p_ in POSL:
        cols.append(np.array([1.0 if r['pos'] == p_ else 0.0 for r in rows_])); names.append(p_)
    cols.append(np.array([r['avg'] - BARS[r['pos']] for r in rows_])); names.append('avg-bar')
    for b in (0, 1, 3):
        cols.append(np.array([1.0 if r['band'] == b else 0.0 for r in rows_])); names.append(BANDS[b])
    for nm, f in expo_cols:
        cols.append(np.array([f(r) for r in rows_], dtype=float)); names.append(nm)
    X = np.column_stack(cols); y = np.array([r['dA'] for r in rows_])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    groups = collections.defaultdict(list)
    for i, r in enumerate(rows_): groups[r['key']].append(i)
    garr = [np.array(v) for _, v in sorted(groups.items())]
    rng = np.random.default_rng(33)
    bs = np.empty((1000, len(names)))
    for b in range(1000):
        idx = np.concatenate([garr[i] for i in rng.integers(0, len(garr), len(garr))])
        bs[b] = np.linalg.lstsq(X[idx], y[idx], rcond=None)[0]
    lo = np.percentile(bs, 2.5, axis=0); hi = np.percentile(bs, 97.5, axis=0)
    P('%s (n=%d)' % (tag, n))
    for nm in show:
        i = names.index(nm)
        star = ' *' if (lo[i] > 0 or hi[i] < 0) else ''
        P('  %-16s %+7.3f  [%+7.3f, %+7.3f]%s' % (nm, beta[i], lo[i], hi[i], star))

L = []; P = L.append
P('ORDER 33 W3 ASYMMETRY PROBE (post-hoc, disclosed) — store %s — seed 33' % META['store_md5'][:8])
P('Mechanism test: reliability/shrinkage predicts FIRST2 hurts ABOVE bar, not below.')
run(cond, [('F2xBELOW', lambda r: r['first2'] * (1.0 if r['band'] <= 1 else 0.0)),
           ('F2xABOVE', lambda r: r['first2'] * (1.0 if r['band'] >= 2 else 0.0))],
    ['F2xBELOW', 'F2xABOVE'], 'ALL AGES 6u')
run([r for r in cond if r['age'] >= 23],
    [('F2xBELOW', lambda r: r['first2'] * (1.0 if r['band'] <= 1 else 0.0)),
     ('F2xABOVE', lambda r: r['first2'] * (1.0 if r['band'] >= 2 else 0.0))],
    ['F2xBELOW', 'F2xABOVE'], 'AGE 23+ 6u')
# same for career games
run(cond, [('cgBELOW', lambda r: (r['careergames'] / 50.0) * (1.0 if r['band'] <= 1 else 0.0)),
           ('cgABOVE', lambda r: (r['careergames'] / 50.0) * (1.0 if r['band'] >= 2 else 0.0))],
    ['cgBELOW', 'cgABOVE'], 'ALL AGES 6u career games split')
open(os.path.join(OUT, 'ASYM_W3_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
