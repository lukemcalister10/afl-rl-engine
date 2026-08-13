#!/usr/bin/env python3
"""ORDER 27 verification probe: the v502/v503 position-field invariant.

READ-ONLY. Measures, on the landed store and the shipped board, the population that
the ruled asserted-invariant would judge:
  "future_position == present_position for every player UNLESS he carries a declared
   blend (alternate_position + p_dual_stream) or appears on a declared-exception list"
"""
import json

STORE = 'engine/rl_after/rl_model_data.json'
BOARD = 'data/rl_build/rl_app_data.json'

d = json.load(open(STORE, encoding='utf-8'))
ks = set()
for p in d:
    ks |= set(p.keys())
print('store rows:', len(d))
print('position-ish fields present:', sorted(k for k in ks if 'pos' in k.lower() or 'dual' in k.lower()))

board = json.load(open(BOARD, encoding='utf-8'))
active = {p['key'] for p in board['active'] if 'key' in p}
back = {p['key'] for p in board['back'] if 'key' in p}

clash = [p for p in d
         if p.get('present_position') and p.get('future_position')
         and p['present_position'] != p['future_position']]
blend = [p for p in clash if p.get('alternate_position') or p.get('p_dual_stream')]
print('present!=future rows:', len(clash), '| declared blend among them:', len(blend))
print('  of which on the ACTIVE board:', sum(1 for p in clash if p.get('key') in active))
print('  of which on the BACK board  :', sum(1 for p in clash if p.get('key') in back))
print('  of which _retired           :', sum(1 for p in clash if p.get('_retired')))

allblend = [p for p in d if p.get('alternate_position') or p.get('p_dual_stream')]
print('rows carrying a declared blend at all:', len(allblend))
onboard = [p for p in clash if p.get('key') in active][:12]
for p in onboard:
    print('   ACTIVE clash:', p.get('key'), p.get('present_position'), '->', p.get('future_position'),
          'alt=', p.get('alternate_position'), 'pdual=', p.get('p_dual_stream'))
