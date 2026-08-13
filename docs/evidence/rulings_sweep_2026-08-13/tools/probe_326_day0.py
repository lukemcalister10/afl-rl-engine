#!/usr/bin/env python3
"""ORDER 27 verification probe: the #326 ruled sentence, measured on the LIVE board.

RULED (register v574, owner words "Keep as ruled. Land it."): "the N43 signed levels price
pool entrants AT ENTRY the way the pick curve prices national draftees."

This probe reads the shipped board and the signed pool levels and reports, for fresh
(zero-game, entry-year) pool entrants, printed day-0 price vs the signed level x _PL_F.
READ-ONLY.
"""
import json
import os

BOARD = 'data/rl_build/rl_app_data.json'
CURVE = 'engine/rl_after/pvc_curve_v2.json'
STORE = 'engine/rl_after/rl_model_data.json'
REDEN = 'engine/rl_after/pick_redenomination.json'

b = json.load(open(BOARD, encoding='utf-8'))
cur = json.load(open(CURVE, encoding='utf-8'))
store = {p.get('key'): p for p in json.load(open(STORE, encoding='utf-8'))}
plf = float(json.load(open(REDEN, encoding='utf-8'))['factor'])

pl = cur.get('pool_levels', {})
print('pool_levels keys:', list(pl.keys()))
flat = pl.get('signed_flat', {})
rdpos = pl.get('signed_rd_positional', {})
print('signed_flat:', flat)
print('signed_rd_positional:', rdpos)
print('_PL_F (pick_redenomination.factor):', plf)
print('curve[1]:', cur.get('curve', {}).get('1') or (cur.get('curve') or [None])[0])

rows = b['active'] + b['back']
def sig(p):
    t = p.get('type')
    if t == 'RD':
        g = p.get('present_position') or p.get('drafted_position')
        return rdpos.get(g)
    return flat.get(t)

fresh = []
for r in rows:
    p = store.get(r.get('key'))
    if not p:
        continue
    if not p.get('type') or p.get('type') == 'ND':
        continue
    lvl = sig(p)
    if lvl is None:
        continue
    # "fresh entrant": no scoring history at all
    seasons = p.get('seasons') or p.get('rows') or []
    games = 0
    try:
        games = sum(int(s.get('games') or 0) for s in seasons) if isinstance(seasons, list) else 0
    except Exception:
        games = -1
    if games == 0:
        fresh.append((r.get('key'), p.get('type'), p.get('present_position'), r.get('v'),
                      lvl, lvl * plf, (r.get('v') / (lvl * plf)) if lvl else None))

fresh.sort(key=lambda x: -(x[6] or 0))
print('\nFRESH (zero recorded games) POOL ENTRANTS ON THE BOARD: %d' % len(fresh))
print('%-28s %-5s %-5s %7s %8s %10s %8s' % ('key', 'type', 'pos', 'printed', 'signed', 'signed*PLF', 'ratio'))
for k, t, pos, v, lvl, anchor, ratio in fresh[:25]:
    print('%-28s %-5s %-5s %7s %8.1f %10.1f %8.3f' % (k, t, pos or '', v, lvl, anchor, ratio or 0))
if fresh:
    rs = [f[6] for f in fresh if f[6]]
    print('\nmedian ratio printed/anchor: %.4f   mean: %.4f   n=%d'
          % (sorted(rs)[len(rs) // 2], sum(rs) / len(rs), len(rs)))
