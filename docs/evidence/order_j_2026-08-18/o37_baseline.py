#!/usr/bin/env python3
"""ORDER J — STEP 0: THE BASELINE FACTS THE PREREG'S PERCENTAGES ARE MEASURED AGAINST.

This runs BEFORE the prereg is written, and it looks at NOTHING that depends on a dose or a knob. It
prices the LANDING CANDIDATE 1f176444 only (dial off) and reports:
  * the board total and the active row count;
  * the mature pool (age 24+) total, count, and its value distribution;
  * the same for the young pool.

Those are properties of the base board, not results of any setting, so reading them cannot bias the
choice of tolerance. Every number the prereg quotes as "x% of y" is y from this file.
"""
import os, sys, json, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
os.environ.pop('RL_O32_STAGE', None)
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(cwd)
MA = NSE.get('MA', MA); ev = NSE['ev']
assert NSE['_O32S'] == 6, 'baseline must be read at stage 6'

BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
ACT = [p for p in PB.values() if NSE['_isreal'](p) and not p.get('_retired')
       and not NSE['delisted'](p) and MA.GRP.get(p.get('pos'))]
MAT = sorted([p.get('key') for p in ACT if p.get('_by') and MA._age_at(p, 2026) >= 24])
YNG = sorted([p.get('key') for p in ACT if not (p.get('_by') and MA._age_at(p, 2026) >= 24)])
ALL = sorted([p.get('key') for p in ACT])

# dial OFF == the landing candidate 1f176444 (the ORDER I in-process identity, re-verified downstream)
MA._O36 = False; NSE['_O36'] = False
MA.O36_LAM_S1 = 0.0
MA._pe_clear()
V = {}
for k in ALL:
    with contextlib.redirect_stdout(io.StringIO()):
        V[k] = float(ev(PB[k], 2026))

tot = sum(V.values()); mt = sum(V[k] for k in MAT); yt = sum(V[k] for k in YNG)
vm = sorted(V[k] for k in MAT)
q = lambda a: vm[min(len(vm) - 1, int(a * len(vm)))]
print('ORDER J BASELINE — the landing candidate 1f176444, dial off, stage 6')
print('  active priced rows        : %d' % len(ALL))
print('  BOARD TOTAL               : %.4f' % tot)
print('  mature rows (age 24+)     : %d' % len(MAT))
print('  MATURE POOL TOTAL         : %.4f  (%.2f%% of the board)' % (mt, 100 * mt / tot))
print('  young rows (under 24)     : %d' % len(YNG))
print('  young pool total          : %.4f  (%.2f%% of the board)' % (yt, 100 * yt / tot))
print('  mature row value: min %.2f  p10 %.2f  median %.2f  p90 %.2f  max %.2f  mean %.2f'
      % (vm[0], q(0.10), q(0.50), q(0.90), vm[-1], mt / len(vm)))
print('  mature rows worth under 200 board points: %d' % sum(1 for v in vm if v < 200))
json.dump(dict(order='ORDER J baseline — landing candidate 1f176444, dial off',
               n_active=len(ALL), board_total=tot, n_mature=len(MAT), mature_total=mt,
               n_young=len(YNG), young_total=yt,
               mature_min=vm[0], mature_p10=q(0.10), mature_median=q(0.50), mature_p90=q(0.90),
               mature_max=vm[-1], mature_mean=mt / len(vm),
               mature_values={k: V[k] for k in MAT}, all_values=V),
          open(os.path.join(HERE, 'BASELINE_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('written: BASELINE_J.json')
