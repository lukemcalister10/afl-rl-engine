#!/usr/bin/env python3
"""READ-ONLY — one board pass for the MSD calibration-pool ripple (register v10 item 11, fork (a)).

argv[1] = 'baseline' | 'msd_excluded'
argv[2] = output JSON path (scratchpad)
argv[3] = shipped board JSON (parity assert, baseline only)

Isolation protocol mirrors the migration lane's ISOLATION_RESULTS method: ONE change alone,
in-memory, full board recompute, diff vs shipped. The change: MSD rows leave the q97m
quantile-GBM training pool (_merged_recover.py load-time fit) — nothing else touches.
"""
import json, io, os, sys, contextlib
from collections import Counter

MODE, OUT = sys.argv[1], sys.argv[2]
WS = '/home/claude/rl_workspace/rl_after'
os.chdir(WS)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
FILTER = "    if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')): continue"
assert src.count(FILTER) == 1, 'training-pool filter line not found exactly once'
if MODE == 'msd_excluded':
    src = src.replace(FILTER, FILTER.replace(': continue', " or p.get('type')=='MSD': continue"))

_ens = {'__name__': '_mr_ripple'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, _ens)
ev, MA, cp = _ens['ev'], _ens['MA'], _ens['cp']

# exact training-pool composition (replicate the loop's own conditions, pre-patch semantics)
pool_types, xrows = Counter(), Counter()
for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
    if cp.debutyr(p) > 2021 or not (p.get('pick') or p.get('_ft')):
        continue
    t = p.get('type')
    pool_types[t] += 1
    d0 = cp.debutyr(p) - 1
    last = max([x['year'] for x in p['scoring']] + [d0])
    xrows[t] += min(last, 2026) + 1 - d0

board = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        board[p.get('key') or p.get('player')] = ev(p, 2026)

res = {'mode': MODE,
       'pool_players_by_type': dict(pool_types),
       'pool_xrows_by_type': dict(xrows),
       'board': board}

if MODE == 'baseline':
    ship = json.load(open(sys.argv[3]))
    ship_v = {r['key']: r['v'] for r in ship['active']}
    mism = [k for k in ship_v if board.get(k) != ship_v[k]]
    res['parity'] = f'{len(ship_v)-len(mism)}/{len(ship_v)}'
    if mism:
        res['parity_fail_sample'] = mism[:10]
        json.dump(res, open(OUT, 'w'))
        raise SystemExit('BASELINE PARITY FAIL — results withheld: ' + res['parity'])

json.dump(res, open(OUT, 'w'))
print(MODE, 'pool by type:', dict(pool_types), '| parity:', res.get('parity', 'n/a'))
