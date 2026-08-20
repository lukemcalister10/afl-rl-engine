#!/usr/bin/env python
# ORDER 33 W3 — store inspection (read-only)
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
d = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')))
print('players:', len(d))
p0 = d[0]
print('fields:', sorted(p0.keys()))
for k in ['milan-murdock', 'hugo-hall-kahan', 'lachlan-mcandrew']:
    p = next((x for x in d if x['key'] == k), None)
    if p is None:
        print(k, 'NOT FOUND'); continue
    print('---', k)
    print({kk: vv for kk, vv in p.items() if kk != 'scoring'})
    print('  scoring:', p.get('scoring'))
# type field values
import collections
print(collections.Counter(p.get('type') for p in d))
# do scoring arrays include 0-game years?
nz = sum(1 for p in d for x in (p.get('scoring') or []) if not (x.get('games') or 0))
print('zero-game scoring rows:', nz)
