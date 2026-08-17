#!/usr/bin/env python
# ORDER 33 W3 — STEP 1: exposure season table (read-only; writes W3_TABLE.json + BUILD_W3_out.txt).
# Definitions per PREREG_W3.md (committed & pushed before this ran). Season-table construction
# follows ORDER 32 S1's s1_build.py precedent.
import json, os, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STORE = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')
OUT = os.path.dirname(os.path.abspath(__file__))

BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
TALL = {'KPD', 'KPF', 'RUCK'}
MIDSEASON_TYPES = {'MSD', 'SSP', 'UNR', 'PDA', 'PDN', 'PDS'}   # first season = entry year
SS = json.load(open(os.path.join(ROOT, 'data', 'season_state.json')))
FE26 = float(SS['calendar_progress']); INPROG = int(SS['inprog_year'])

def u(y): return FE26 if y == INPROG else 1.0

d = json.load(open(STORE))
md5 = hashlib.md5(open(STORE, 'rb').read()).hexdigest()

rows = []
for p in d:
    pos = p.get('future_position')
    if pos not in BARS: continue
    by = p.get('_by')
    if by is None: continue
    sc = sorted([x for x in (p.get('scoring') or []) if (x.get('games') or 0) > 0],
                key=lambda r: r['year'])
    if not sc: continue
    ey = p.get('year')
    typ = p.get('type')
    byyear = {x['year']: x for x in sc}
    cum = 0.0
    for i, x in enumerate(sc):
        Y = x['year']; g = float(x['games']); a = float(x['avg'] or 0.0)
        cum += g
        sidx = i + 1                                   # X2 played-season index
        lt = (Y - ey + 1) if typ in MIDSEASON_TYPES else (Y - ey)   # X3 listed tenure
        lt = max(lt, 1)
        nxt = byyear.get(Y + 1)
        n_g = float(nxt['games']) if nxt else 0.0
        n_a = float(nxt['avg'] or 0.0) if nxt else None
        # 3-year horizon: best avg among Y+1..Y+3 with games >= 6u
        best3 = None
        for k in (1, 2, 3):
            z = byyear.get(Y + k)
            if z and float(z['games']) >= 6.0 * u(Y + k):
                av = float(z['avg'] or 0.0)
                if best3 is None or av > best3: best3 = av
        rows.append(dict(
            key=p['key'], year=Y, age=Y - by, pos=pos, tall=pos in TALL,
            games=g, avg=a, u=u(Y), typ=typ, entry_year=ey, pick=p.get('pick'),
            careergames=cum, sidx=sidx, ltenure=lt,
            next_games=n_g, next_avg=n_a,
            next_full6=bool(nxt and n_g >= 6.0 * u(Y + 1)),
            exit1=(nxt is None), exitever=(sc[-1]['year'] <= Y),
            best3=best3,
            retired=bool(p.get('_retired'))))

json.dump(dict(meta=dict(store_md5=md5, n_players=len(d), n_rows=len(rows), fe26=FE26,
                         bars=BARS, built='2026-08-17 ORDER33 W3 step1'),
               rows=rows), open(os.path.join(OUT, 'W3_TABLE.json'), 'w'))

L = []
P = L.append
P('ORDER 33 W3 BUILD — store %s, %d players, %d played season rows' % (md5[:8], len(d), len(rows)))
base = [r for r in rows if 2005 <= r['year'] <= 2025 and r['games'] >= 6.0 * r['u']
        and 18 <= r['age'] <= 30]
cond = [r for r in base if r['next_full6']]
P('base sample (Y 2005-2025, games>=6u, age 18-30): %d rows, %d players'
  % (len(base), len(set(r['key'] for r in base))))
P('conditional sample (next season games>=6u): %d rows (%.1f%%)'
  % (len(cond), 100.0 * len(cond) / len(base)))
P('exit1 (no Y+1 played season at all): %d (%.1f%%); thin next season (played but <6u): %d'
  % (sum(r['exit1'] for r in base), 100.0 * sum(r['exit1'] for r in base) / len(base),
     len(base) - len(cond) - sum(r['exit1'] for r in base)))
c = collections.Counter((min(r['sidx'], 5)) for r in base)
P('season-index (X2, 5=5+) over base: %s' % dict(sorted(c.items())))
c = collections.Counter((min(r['age'], 27)) for r in base if r['sidx'] <= 2)
P('ages of first/second-season rows (27=27+): %s' % dict(sorted(c.items())))
key23 = [r for r in base if r['age'] >= 23 and r['sidx'] <= 2]
P('KEY CELL raw: age>=23 & first/second played season: n=%d rows, %d players; exit1 %.1f%%'
  % (len(key23), len(set(r['key'] for r in key23)),
     100.0 * sum(r['exit1'] for r in key23) / max(len(key23), 1)))
c = collections.Counter(r['typ'] for r in key23)
P('  entry types in key cell: %s' % dict(c.most_common()))
open(os.path.join(OUT, 'BUILD_W3_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
