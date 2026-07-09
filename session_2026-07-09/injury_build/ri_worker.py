#!/usr/bin/env python3
"""R-i worker: exec the engine once under the ambient RL_LTI_CLOCK (pause|advance) and dump, for every
register name, the board ev + the L1c young-credit multiplier + career-games clock. Driver diffs two runs.
Run from the bootstrapped workspace rl_after under the panel env. argv[1] = output json path."""
import io, contextlib, json, os, sys
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g['MA']; ev = g['ev']; state = g['_AVAIL_STATE']
ycred_mult = g['_ycred_mult']; ycred_games = g['_ycred_games']
out = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        k = p.get('key')
        if k in state:
            out[k] = {'player': p.get('player'), 'section': state[k]['section'],
                      'ev': ev(p, 2026), 'ycred': round(ycred_mult(p, 2026), 4),
                      'games': round(ycred_games(p, 2026), 1),
                      'avail_nerf': p.get('_avail_nerf', 0)}
json.dump({'clock': os.environ.get('RL_LTI_CLOCK', 'pause'), 'names': out}, open(sys.argv[1], 'w'), indent=1)
print("wrote %s (clock=%s, %d register names)" % (sys.argv[1], os.environ.get('RL_LTI_CLOCK', 'pause'), len(out)))
