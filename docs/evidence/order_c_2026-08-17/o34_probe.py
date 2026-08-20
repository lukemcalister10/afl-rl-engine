#!/usr/bin/env python3
"""ORDER C — leg probe: load the engine with the env's dials and print the price legs for named rows.
Usage: RL_O34=1 python3 o34_probe.py  (or RL_O31=1 RL_O32=1 ...)"""
import os, sys, json, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
MA = NSE.get('MA', MA)
G = NSE
print('dials: O31 %s O32S %s O34 %s' % (G['_O31'], G['_O32S'], G.get('_O34')))
KEYS = ['josh-smillie', 'milan-murdock', 'harry-dean', 'nick-madden', 'harry-sheezel', 'ned-moyle']
BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), p)
for k in KEYS:
    p = BY[k]
    with contextlib.redirect_stdout(io.StringIO()):
        e_full = float(G['ev'](p, 2026))
    g = float(G['pv_games'](p, 2026))
    D = float(G['o31_D'](p, 2026))
    V0 = float(G['pv_pedigree'](p))
    r = float(G['rho31'](g))
    s = int(G['o31_stall_run'](p, 2026))
    pl = bool(p.get('_pool'))
    pi = float(G['o31_pi'](p, 2026, g))
    cr = float(G['o32_age_credit'](p, 2026, g)) if 'o32_age_credit' in G else 0.0
    Phat = (e_full - pi * V0 - cr) / r if g > 0 else 0.0
    print('%-16s g %5.1f  ev %9.2f  D %.4f  V0 %9.2f  rho %.4f  s %d  pi %.4f  credit %8.2f  Phat %9.2f'
          % (k, g, e_full, D, V0, r, s, pi, cr, Phat))
