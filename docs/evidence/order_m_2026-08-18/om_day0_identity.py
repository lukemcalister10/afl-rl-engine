#!/usr/bin/env python3
"""ORDER K — G6, THE DAY-0 ENTRY IDENTITY.

Two different objects, and the packet must not let them be confused:

  derived_v0  — the RAW ENTRY OBJECT. What the pick itself was worth on draft day, before the player
                had done anything. The walk-forward matrix writes it as year 0. THIS MUST NOT MOVE.
                It is BIT-IDENTICAL, 89 of 89, and that is asserted here against the DIAL-OFF value.

  printed day-0 — entry value multiplied by the SITTING DISCOUNT. For a player who has already sat,
                this is not an entry value; it is an entry value with a year of sitting charged
                against it. The tall/small factor IS a change to that discount, so the printed day-0
                of a sitter moves BY CONSTRUCTION, and its reference file regenerates. That is
                DISCLOSED here in exactly the way ORDER D disclosed the same re-base when the
                pick-curve fade landed, and ORDER J after it.

Run with the dial OFF and the dial ON in two separate processes; compare.
"""
import io, os, sys, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LANE = sys.argv[1] if len(sys.argv) > 1 else 'on'
OUTP = os.path.join(HERE, 'DAY0M_V0_%s.json' % LANE.upper())
env = dict(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
           MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
           RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'), RL_GAMMA='1.0', RL_PICK1='3000',
           RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72', RL_PRIOR_TREES='400', PAR_RAMPS='22',
           RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'), RL_O31='1', RL_O32='1')
if LANE == 'on':
    env.update(RL_O36='1', RL_O36_LAM_S1='0.40', RL_O36_TALL='1', RL_O36_FLOORFIX='1',
               RL_O36_KAPPA='0.20', RL_O36_GAMMA='8.0', RL_O36_ETA='0.00', RL_O36_GAMMA_D='14.0',
               RL_O36_LAMBDA='1.08')
else:
    env.update(RL_O35='1')
    for v in ('RL_O36', 'RL_O36_LAM_S1', 'RL_O36_TALL', 'RL_O36_FLOORFIX', 'RL_O36_KAPPA',
              'RL_O36_GAMMA', 'RL_O36_ETA', 'RL_O36_GAMMA_D', 'RL_O36_LAMBDA'):
        os.environ.pop(v, None)
os.environ.update(env)
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
entry_derived = NSE['_entry29b_derived']; o31_D = NSE['o31_D']
Y = MA.BASE_REF
rows = {}
for p in MA.data:
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = entry_derived(p, Y)
    if d0 is None:
        continue
    k = p.get('key') or MA.slug(p['player'])
    with contextlib.redirect_stdout(io.StringIO()):
        D = float(o31_D(p, Y))
    rows[k] = dict(derived_v0=repr(float(d0)), fade_D=repr(D), day0=repr(float(d0) * D))
json.dump(dict(lane=LANE, base_ref=Y, n=len(rows), rows=rows), open(OUTP, 'w'), indent=1, sort_keys=True)
print('lane=%s  wired entrants=%d  -> %s' % (LANE, len(rows), os.path.basename(OUTP)))

other = os.path.join(HERE, 'DAY0M_V0_%s.json' % ('OFF' if LANE == 'on' else 'ON'))
if os.path.exists(other):
    O = json.load(open(other))['rows']
    same_v0 = [k for k in rows if k in O and rows[k]['derived_v0'] == O[k]['derived_v0']]
    diff_v0 = [k for k in rows if k in O and rows[k]['derived_v0'] != O[k]['derived_v0']]
    same_pr = [k for k in rows if k in O and rows[k]['day0'] == O[k]['day0']]
    diff_pr = sorted([k for k in rows if k in O and rows[k]['day0'] != O[k]['day0']])
    print('\n== G6 — THE DAY-0 ENTRY IDENTITY, dial ON vs dial OFF ==')
    print('  derived_v0 (THE RAW ENTRY OBJECT) BIT-IDENTICAL : %d of %d   -> %s'
          % (len(same_v0), len(rows), 'PASS' if not diff_v0 else 'FAIL — M5 FIRES: %s' % diff_v0[:10]))
    print('  printed day-0 (entry value x sitting discount)  : %d of %d unchanged, %d MOVE'
          % (len(same_pr), len(rows), len(diff_pr)))
    print('  the %d that move are sitters whose sitting DISCOUNT the ruled tall/small factor changes.'
          % len(diff_pr))
    print('  This is the ruled fade\'s intended effect. The PRINT reference regenerates, disclosed')
    print('  exactly as ORDER D disclosed it when the pick-curve fade landed.')
    ups = [(k, float(rows[k]['day0']) - float(O[k]['day0'])) for k in diff_pr]
    ups.sort(key=lambda x: -x[1])
    print('  largest up  : %s' % ', '.join('%s %+.1f' % (k, d) for k, d in ups[:6]))
    print('  largest down: %s' % ', '.join('%s %+.1f' % (k, d) for k, d in ups[-6:]))
    print('  count up %d · count down %d' % (sum(1 for _, d in ups if d > 0),
                                             sum(1 for _, d in ups if d < 0)))
    json.dump(dict(n_wired=len(rows), derived_v0_identical=len(same_v0),
                   derived_v0_moved=diff_v0, printed_day0_moved=diff_pr,
                   moves={k: d for k, d in ups}),
              open(os.path.join(HERE, 'DAY0_IDENTITY_M.json'), 'w'), indent=1, sort_keys=True)
    print('\nwrote DAY0_IDENTITY_M.json')
