"""#334 stage B / STAGE 4 — THE BOUNDARY DiD, done properly.

The integer 5g -> 6g step in probes.py is a RAW-GAMES step that STRADDLES the bar: at a season 88% elapsed
the prorated establishment bar is 6*fE = 5.28 raw games, so 5 raw games (5.68 AT PACE) is still BELOW the bar
and 6 raw games (6.82 at pace) is ABOVE it. That step therefore contains three things at once -- the last of
the lam ramp, the bar crossing itself, and the ordinary growth of e_full with an extra game -- and it is not
a cliff test.

THE CLIFF TEST is the one-sided limit AT the bar: price at games-at-pace 6-eps versus 6+eps. lam(6)=1 and
1**e == 1 for every exponent, so the pedigree conditioning is INERT exactly at the bar and the jump must be
unchanged. That is the SEAM RATIO reported here: (jump on this build) / (jump on the base build) ~= 1.

The placebo, in the seam_boundary pattern: the SAME eps-step taken well away from the bar (at pace 3), where
the mechanism IS live. A cliff-free change shows seam ratio ~= 1 at the bar and a ratio away from 1 at the
placebo -- the effect is in the ramp, not at the seam.

RL_TAG names the build. READ-ONLY.
"""
import os, sys, io, json, copy, contextlib
import numpy as np

REPO = os.environ.get('RL_REPO'); OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
TAG = os.environ.get('RL_TAG', 'untagged')
sys.path.insert(0, REPO + '/vendor'); os.chdir('/home/claude/rl_workspace/rl_after'); sys.path.insert(0, '.')
G = {'__name__': '_s4_bd'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA = G['MA']; cp = G['cp']; Y = 2026
star = G['_V0CURVE_META']['_star']; _V0CURVE = G['_V0CURVE']; _v0key = G['_v0key']; _ageR = G['_ageR']
HELD = []; L = []
def say(s=''): L.append(s); print(s)

def price_g(base, g, avg=84.25):
    p = copy.deepcopy(base); HELD.append(p)
    p['scoring'] = [dict(year=Y, games=float(g), avg=avg)]
    MA._pe_clear()
    _V0CURVE[_v0key(p)] = star(MA.gfut(p), _ageR(p), min(max(MA.effpk(p), 1), 90))
    G['_V0C'].clear(); G['_V0U'].clear()
    return G['ev'](p, Y)

PROBES = ['noah-mraz', 'josh-smillie', 'charlie-west', 'samuel-swadling']
res = {}
say('=' * 104)
say('#334 stage B / STAGE 4 — BOUNDARY DiD (the establishment bar).  build tag: %s   PED_BAR=%s'
    % (TAG, G.get('PED_BAR', 'n/a (base engine)')))
say('=' * 104)
for k in PROBES:
    b = next((x for x in MA.data if x.get('key') == k), None)
    if b is None: continue
    fe = G['_fEy'](Y, b); bar = 6.0 * fe            # raw games at which games-at-pace == 6 (the establishment bar)
    eps = 1e-4
    below = price_g(b, bar - eps); above = price_g(b, bar + eps)
    pl_lo = price_g(b, 3.0 * fe - eps); pl_hi = price_g(b, 3.0 * fe + eps)
    g5, g6 = price_g(b, 5.0), price_g(b, 6.0)
    res[k] = dict(player=b.get('player'), pos=MA.gfut(b), pick=MA.effpk(b), fe=fe, bar_raw_games=bar,
                  at_bar_below=below, at_bar_above=above, jump_at_bar=above - below,
                  placebo_below=pl_lo, placebo_above=pl_hi, jump_placebo=pl_hi - pl_lo,
                  g5=g5, g6=g6, step_5_to_6=g6 - g5,
                  ns_below=G['nseas_pro'](HELD[-4], Y) if False else None)
    say('')
    say('  %-20s %-5s pick %-3d   fE=%.2f   establishment bar = %.4f raw games (= 6.00 at pace)'
        % (b.get('player')[:20], MA.gfut(b), MA.effpk(b), fe, bar))
    say('    AT THE BAR   : %.4fg -> %d   |   %.4fg -> %d   |   JUMP %+d  (%+.4f%%)'
        % (bar - eps, below, bar + eps, above, above - below, 100.0 * (above - below) / max(below, 1)))
    say('    PLACEBO (3 at pace, mechanism live): %d -> %d   JUMP %+d  (%+.4f%%)'
        % (pl_lo, pl_hi, pl_hi - pl_lo, 100.0 * (pl_hi - pl_lo) / max(pl_lo, 1)))
    say('    integer 5g -> 6g (STRADDLES the bar): %d -> %d   step %+d' % (g5, g6, g6 - g5))
json.dump(dict(tag=TAG, ped_bar=G.get('PED_BAR'), probes=res), open(os.path.join(OUT, 'boundary_%s.json' % TAG), 'w'), indent=1)
open(os.path.join(OUT, 'boundary_%s.txt' % TAG), 'w').write('\n'.join(L) + '\n')
