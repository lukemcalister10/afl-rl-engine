"""Explore: locate the year-1+ ND cap, the par surface, the entry anchor. READ-ONLY."""
import engine_load, json, collections
g = engine_load.load()
MA = g['MA']; ev = g['ev']; cp = g['cp']; PR = g['PR']
v0_start = g['v0_start']; entry_anchor = g['entry_anchor']
BF = g.get('_PL_F')
print('board factor _PL_F =', BF)

data = MA.data
def get(k): return next((p for p in data if p.get('key') == k), None)

for k in ('noah-mraz', 'archie-ludowyke', 'zeke-uwland', 'bodhi-uwland'):
    p = get(k)
    if not p: print(k, 'MISSING'); continue
    print(k, 'type', p.get('type'), 'pick', p.get('pick'), 'effpk', MA.effpk(p),
          'pos', p.get('pos'), 'gfut', MA.gfut(p), 'year', p.get('year'),
          'debutyr', cp.debutyr(p), 'age_asof26', cp._age_asof(p, 2026),
          'ageR', g['_ageR'](p),
          'scoring', p.get('scoring'))
    print('   v0_start', v0_start(p), 'entry_anchor', entry_anchor(p), 'ev2026', ev(p, 2026))

# ---- year-1 ND cohort: is ev capped at v0_start? ----
print('\n=== year-1 ND cohort (drafted 2025, debut 2026) ratio ev/v0 ===')
rows = []
for p in data:
    if p.get('type') != 'ND' or p.get('pick') is None: continue
    if MA.is_pool(p): continue
    if p.get('year') != 2025: continue
    v0 = v0_start(p); e = ev(p, 2026)
    cg = sum(x['games'] for x in p['scoring'])
    rows.append((p['key'], MA.effpk(p), MA.gfut(p), cg, v0, e, (e / v0 if v0 else 0)))
rows.sort(key=lambda r: r[1])
for r in rows[:40]:
    print('  %-28s pk%-3d %-5s g%-3d v0 %8.1f ev %6d  ratio %.4f' % r)
import numpy as np
rr = [r[6] for r in rows]
print('n', len(rows), 'mean ratio', np.mean(rr), 'max', max(rr), 'n_at_1.000', sum(1 for x in rr if abs(x - 1) < 1e-3))
print('Sum ev / Sum v0 =', sum(r[5] for r in rows) / sum(r[4] for r in rows))
