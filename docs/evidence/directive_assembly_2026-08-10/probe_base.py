"""Baseline probe: identities, cohorts, book sums. READ-ONLY."""
import sys, json, collections
sys.path.insert(0, '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad')
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']; PR = g['PR']
ev = g['ev']; entry_anchor = g['entry_anchor']; v0_start = g['v0_start']

real = [p for p in MA.data if g['_isreal'](p)]
print('REAL rows:', len(real))
print('v0surf sig:', g['_v0surf_sig'](real))

board = json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))
print('board keys:', list(board.keys())[:12])
act = board.get('active') or []
print('n active:', len(act), 'sum v:', sum(x['v'] for x in act))
print('sample row:', json.dumps(act[0], sort_keys=True)[:400])
