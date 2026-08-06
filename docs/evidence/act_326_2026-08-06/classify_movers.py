#!/usr/bin/env python3
"""#326 second rehearsal — classify every board mover by the ENGINE's own pool classification.

Run inside the workspace with the engine importable. Reads the two boards, joins on key, and asks the
engine (not the board) whether each mover is a pool entrant and which signed division he is in. Also
separates the ruck-cap-basis route from the entry-anchor route by re-evaluating with the cap basis pinned
back to the ladder's pool slot.
"""
import contextlib, io, json, os, sys

EV = sys.argv[1]
base = json.load(open(os.path.join(EV, 'baseline_rl_app_data.json')))
cand = json.load(open(os.path.join(EV, 'rehearsed_rl_app_data.json')))

G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA = G['MA']
ev = G['ev']; prefloor = G['ev_prefloor']; nspro = G['nseas_pro']
by_key = {p['key']: p for p in MA.data}


def route(p):
    with contextlib.redirect_stdout(io.StringIO()):
        pre = prefloor(p, 2026); post = ev(p, 2026); ns = nspro(p, 2026)
    if post != pre:
        return 'floor'
    if ns == 0:
        return 'blend'
    return 'ruck cap / other'


def career_games(p):
    return sum(r.get('games', 0) for r in p.get('scoring', []))

rows = {}
for sec in ('active', 'back'):
    A = {r['key']: r for r in base.get(sec, [])}
    B = {r['key']: r for r in cand.get(sec, [])}
    for k in A:
        rows[(sec, k)] = (A[k], B.get(k))

movers, still = [], []
for (sec, k), (a, b) in rows.items():
    p = by_key.get(k)
    pool = bool(p and p.get('_pool'))
    div = (MA.pool_division(p) if pool else None)
    changed_fields = sorted(f for f in set(a) | set(b or {}) if a.get(f) != (b or {}).get(f))
    rec = dict(sec=sec, key=k, name=a.get('player') or (p or {}).get('player'), pool=pool, div=div,
               v0=a.get('v'), v1=(b or {}).get('v'), fields=changed_fields,
               type=(p or {}).get('type'), gfut=(MA.gfut(p) if p else None),
               route=(route(p) if (p and changed_fields) else None),
               games=(career_games(p) if p else None),
               yrs=(2026 - int((p or {}).get('year') or 0)) if p else None)
    (movers if changed_fields else still).append(rec)

nonpool_movers = [m for m in movers if not m['pool']]
print('BOARD ROWS %d · movers (any field) %d · non-pool movers %d'
      % (len(rows), len(movers), len(nonpool_movers)))
print('every mover is engine-pool-classified: %s' % (not nonpool_movers))
if nonpool_movers:
    for m in nonpool_movers[:40]:
        print('   NON-POOL MOVER %-26s type=%-4s v %s -> %s  fields=%s'
              % (m['name'], m['type'], m['v0'], m['v1'], m['fields']))

# per-division direction table
byd = {}
for m in movers:
    d = m['div'] or 'NON-POOL'
    e = byd.setdefault(d, dict(n=0, up=0, down=0, same_v=0, dv=[]))
    e['n'] += 1
    if m['v1'] is None or m['v0'] is None:
        continue
    if m['v1'] > m['v0']:
        e['up'] += 1
    elif m['v1'] < m['v0']:
        e['down'] += 1
    else:
        e['same_v'] += 1
    e['dv'].append(m['v1'] - m['v0'])
print('\n| division | movers | up | down | v unchanged | median dv | min dv | max dv |')
print('|---|---|---|---|---|---|---|---|')
for d in sorted(byd):
    e = byd[d]
    dv = sorted(e['dv'])
    med = dv[len(dv) // 2] if dv else 0
    print('| %s | %d | %d | %d | %d | %+d | %+d | %+d |'
          % (d, e['n'], e['up'], e['down'], e['same_v'], med, dv[0] if dv else 0, dv[-1] if dv else 0))

# population that did NOT move, by division — the honest denominator
pop = {}
for p in MA.data:
    if p.get('_pool'):
        pop.setdefault(MA.pool_division(p), [0, 0])[0] += 1
for m in movers:
    if m['pool']:
        pop.setdefault(m['div'], [0, 0])[1] += 1
print('\npool population (store rows) vs movers by division:')
for d in sorted(pop):
    print('   %-9s store rows %4d   board movers %3d' % (d, pop[d][0], pop[d][1]))

# route x career-depth cross-tab: which movers are thin records and which have real careers
import collections as _c
rt = _c.Counter((m['route'], 'thin(<20g)' if (m['games'] or 0) < 20 else 'career(>=20g)') for m in movers if m['v0'] != m['v1'])
print('\nV-MOVERS by route x career depth (senior games in the store):')
for (r, d), n in sorted(rt.items()):
    print('   %-18s %-12s %3d' % (r, d, n))
deep = sorted([m for m in movers if m['v0'] != m['v1'] and (m['games'] or 0) >= 20],
              key=lambda m: -abs((m['v1'] or 0) - (m['v0'] or 0)))
print('\nmovers WITH a real career (>=20 senior games), biggest first:')
for m in deep[:20]:
    print('   %-24s %-8s %-8s games=%-4d yrs=%-3s v %5s -> %5s (%+d)'
          % (m['name'], m['div'], m['route'], m['games'], m['yrs'], m['v0'], m['v1'], (m['v1'] or 0) - (m['v0'] or 0)))
print('   ... %d such rows in total' % len(deep))

json.dump([dict(m, fields=m['fields']) for m in movers],
          open(os.path.join(EV, 'gate6_movers.json'), 'w'), indent=1, sort_keys=True)
print('\nwrote gate6_movers.json')
