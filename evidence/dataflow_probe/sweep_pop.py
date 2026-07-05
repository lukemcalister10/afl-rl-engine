#!/usr/bin/env python3
# Board-vs-engine sweep (reproduce cold-review 537/805) + population counts.
# TRUE engine = single-namespace ev() (layers applied). Board = shipped rl_app_data.json 'v'.
import os, io, contextlib, json, statistics
RA = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../engine/rl_after')
os.chdir(RA)
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA, ev, delisted = g['MA'], g['ev'], g['delisted']
bykey = {p['key']: p for p in MA.data}
B = json.load(open('../../data/rl_build/rl_app_data.json'))
active = B['active']
byk = {r['key']: r for r in active}

# ---- SWEEP: board 'v' vs TRUE ev ----
diffs = []; divergent = 0; n = 0; capped_rucks = []
for r in active:
    p = bykey.get(r['key']); bv = r.get('v')
    if p is None or bv in (None, 0):
        continue
    with contextlib.redirect_stdout(io.StringIO()):
        e = ev(p, 2026)
    n += 1
    if abs(bv - e) > 0.5:
        divergent += 1
        if e != 0:
            diffs.append((bv - e) / abs(e) * 100.0)
    if MA.gfut(p) == 'RUC' and abs(bv - e) > 0.5:
        capped_rucks.append((r['key'], e, bv))
print("=== SWEEP: board v vs TRUE engine ev (single-namespace) ===")
print("compared              :", n)
print("divergent (|d|>0.5)   :", divergent, "(%d%% of %d)" % (round(100*divergent/n), n))
print("median board-vs-eng %%:", round(statistics.median(diffs), 2), "%")
print("mean   board-vs-eng %%:", round(statistics.mean(diffs), 2), "%")
print("rucks diverging       :", len(capped_rucks), "e.g.", capped_rucks[:5])

# ---- POPULATION ----
print("\n=== POPULATION ===")
print("board active rows     :", len(active))
print("engine store total    :", len(MA.data))
elig = [p for p in MA.data if MA.GRP.get(p.get('pos'))]
print("engine GRP-eligible    :", len(elig))
ret = [p for p in MA.data if p.get('_retired')]
print("store _retired=True   :", len(ret))
retk = {p['key'] for p in ret}
ret_board = [(r['key'], r['v']) for r in active if r['key'] in retk]
ret_nonzero = [x for x in ret_board if x[1] not in (0, None)]
print("retired appearing on board:", len(ret_board), "| with non-zero v:", len(ret_nonzero), ret_nonzero[:5])
for nm in ['toby-conway', 'max-king-syd', 'louis-emmett']:
    p = bykey.get(nm); r = byk.get(nm)
    print("  %-14s store _retired=%s games=%s board_v=%s" %
          (nm, p.get('_retired') if p else 'NA', p.get('games') if p else 'NA', r.get('v') if r else 'NA'))
