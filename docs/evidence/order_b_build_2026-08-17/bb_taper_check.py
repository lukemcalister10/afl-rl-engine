#!/usr/bin/env python3
"""ORDER B — B-3 verification: the ceiling band under taper retirement.
Loads the engine twice IN ONE PROCESS is not possible (module state), so this runs as:
    python3 bb_taper_check.py off   -> writes TAPER_BANDS_off.json  (RL_O33 unset)
    python3 bb_taper_check.py on    -> writes TAPER_BANDS_on.json   (RL_O33=1 stage 3)
    python3 bb_taper_check.py judge -> compares the two files, counts inversions, sums the ceiling leg
Bands are b6(p, 2026) for the 804 board rows (the S6 page's own object); band[5] is the ceiling
(q97) the price6 WQ6 weight 0.10 consumes."""
import os, sys, json, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33'
MODE = sys.argv[1]

if MODE == 'judge':
    A = json.load(open(os.path.join(HERE, 'TAPER_BANDS_off.json')))
    B = json.load(open(os.path.join(HERE, 'TAPER_BANDS_on.json')))
    inv_off = sum(1 for k in A if A[k][5] < A[k][4] - 1e-9)
    inv_on = sum(1 for k in B if B[k][5] < B[k][4] - 1e-9)
    d5 = {k: B[k][5] - A[k][5] for k in A}
    moved = {k: v for k, v in d5.items() if abs(v) > 1e-6}
    tot = sum(d5.values())
    lower = {k: round(json.dumps([round(B[k][i] - A[k][i], 2) for i in range(5)]) != json.dumps([0.0] * 5))
             for k in A}
    n_lower_moved = sum(lower.values())
    top = sorted(moved.items(), key=lambda t: -t[1])[:12]
    print('CEILING BAND (b6 band[5], the S6 sixth-scenario level object), 804 board rows:')
    print('  v-inversions (band5 < band4): dial-off %d  ->  dial-on %d' % (inv_off, inv_on))
    print('  rows with band[5] moved: %d;  total ceiling-band points restored: %+.0f' % (len(moved), tot))
    print('  rows with ANY band[0..4] moved (must be 0 — retirement touches only band 5): %d' % n_lower_moved)
    print('  top ceiling risers:')
    for k, v in top:
        print('    %-24s %+8.1f' % (k, v))
    json.dump(dict(inversions_off=inv_off, inversions_on=inv_on, n_moved=len(moved),
                   total_band5_delta=round(tot, 1), lower_bands_moved=n_lower_moved,
                   top=[[k, round(v, 1)] for k, v in top]),
              open(os.path.join(HERE, 'TAPER_CHECK.json'), 'w'), indent=1)
    print('wrote TAPER_CHECK.json')
    sys.exit(0)

os.environ.update(RL_O31='1', RL_O32='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
if MODE == 'on':
    os.environ['RL_O33'] = '1'
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
b6 = NSE['b6']
BOARD = json.load(open(SP + '/bb_off_o32/rl_after/rl_app_data.json'))
KEYS = {r['key'] for r in BOARD['active']}
out = {}
for p in MA.data:
    k = p.get('key')
    if k in KEYS and k not in out:
        try:
            out[k] = [float(x) for x in b6(p, 2026)]
        except Exception:
            pass
json.dump(out, open(os.path.join(HERE, 'TAPER_BANDS_%s.json' % MODE), 'w'))
print('wrote TAPER_BANDS_%s.json rows=%d' % (MODE, len(out)))
