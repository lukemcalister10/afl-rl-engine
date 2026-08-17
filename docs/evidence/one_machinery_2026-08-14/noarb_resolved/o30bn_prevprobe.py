#!/usr/bin/env python3
"""ORDER 30B-N -- dump the PREVIEW lane's UNROUNDED ev() per row, in BOARD currency.

Why this exists. The derived resolved board recovers its production column by inverting the weight
blend on the PRINTED INTEGER preview price, so that column carries the board's print rounding (+-0.5)
ON TOP of the blend site's own round() in engine currency. Reading ev() directly removes the print
rounding, which yields a strictly better production leg and lets the row control show that the
remaining disagreement really is rounding and not law.

The engine must be loaded IN THE PREVIEW LANE, so this is a separate process from the resolved-lane
row control by construction.

env:   RL_O30B_PREVIEW=1  STAGE=<preview-staged rl_after>  RL_REPO=<worktree>
usage: o30bn_prevprobe.py <out.json>
"""
import os, sys, io, json, contextlib

OUT = sys.argv[1]
assert os.environ.get('RL_O30B_PREVIEW') == '1', 'this probe must run IN the preview lane'
assert os.environ.get('RL_O30B_RESOLVED') in (None, '', '0'), 'the resolved dial must be OFF here'
STAGE = os.environ['STAGE']
ROOT = os.environ['RL_REPO']
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']
ev = G['ev']
_PL_F = G['_PL_F']
sigma30bp = G['sigma30bp']
pv_games = G['pv_games']
day0_v0 = G['day0_v0']
Y = 2026

AR = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resolution',
                                 'RESOLVED_ALLROWS.json')))
keys = {r['key'] for r in AR['rows']}
BYK = {p['key']: p for p in MA.data if p.get('key')}
out = {}
for k in keys:
    p = BYK.get(k)
    if p is None:
        continue
    out[k] = dict(ev_board=float(ev(p, Y)) / _PL_F, sigma=sigma30bp(pv_games(p, Y)),
                  v0=float(day0_v0(p) or 0.0), games=pv_games(p, Y))
json.dump(out, open(OUT, 'w'), indent=1, sort_keys=True)
print('PREVIEW-lane unrounded ev() dumped for %d rows -> %s' % (len(out), OUT))
