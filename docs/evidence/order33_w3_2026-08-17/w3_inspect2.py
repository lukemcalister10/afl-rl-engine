#!/usr/bin/env python
# ORDER 33 W3 — field coverage inspection (read-only)
import json, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
d = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')))
ny = sum(1 for p in d if p.get('year') is None)
print('players with year=None:', ny)
# year vs first played season
diffs = collections.Counter()
bad = 0
for p in d:
    sc = [x for x in (p.get('scoring') or []) if (x.get('games') or 0) > 0]
    if not sc or p.get('year') is None: continue
    fy = min(x['year'] for x in sc)
    dd = fy - p['year']
    diffs[max(min(dd, 5), -3)] += 1
    if dd < 0: bad += 1
print('first_played_year - entry_year distribution (clamped -3..5):', dict(sorted(diffs.items())))
print('players who played BEFORE entry year:', bad)
# entry year range
yrs = [p['year'] for p in d if p.get('year')]
print('entry year range:', min(yrs), max(yrs))
# how many players have a played season at age>=23 that is their 1st or 2nd played season
n = 0
for p in d:
    sc = sorted([x for x in (p.get('scoring') or []) if (x.get('games') or 0) > 0], key=lambda r: r['year'])
    by = p.get('_by')
    if by is None: continue
    for i, x in enumerate(sc):
        if x['year'] - by >= 23 and i <= 1 and (x.get('games') or 0) >= 6:
            n += 1
print('played seasons (g>=6) at age>=23 that are 1st/2nd played season:', n)
import numpy
print('numpy', numpy.__version__)
