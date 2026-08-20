#!/usr/bin/env python3
"""ORDER J — J-TOL measured on the EXACT reference point, with the exempt lever removed.

The reference point comes from the declared refinement pass, so it was not one of the sixteen coarse
shortlist points the first gate run measured. This file closes that hole: it applies PREREG_J §2.2 to
the carried-shape setting itself, with RL_O36_TALL=0 so the owner-ruled factor is out of the
measurement and every delta is attributable to S1 + the counterweight alone.

It also prints the same reading for the two runner-up refinement points, so the verdict is not resting
on one setting.
"""
import os, sys, json, io, contextlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_TALL='0', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
os.environ.pop('RL_O32_STAGE', None)
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(cwd)
MA = NSE.get('MA', MA); ev = NSE['ev']
assert NSE['_O32S'] == 6
F = 1.0524
BJ = json.load(open(os.path.join(HERE, 'BASELINE_J.json')))
BOARD = BJ['board_total'] / F
CAP_CHURN, CAP_NET = 0.0015 * BOARD, 0.0010 * BOARD

BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
ACT = [p for p in PB.values() if NSE['_isreal'](p) and not p.get('_retired')
       and not NSE['delisted'](p) and MA.GRP.get(p.get('pos'))]
MAT = sorted([p.get('key') for p in ACT if p.get('_by') and MA._age_at(p, 2026) >= 24])
NAME = {p.get('key'): p.get('player') for p in ACT}
AGEOF = {p.get('key'): MA._age_at(p, 2026) for p in ACT}


def price(dose, kap, gu, eta, gd, rel, dial=True):
    NSE['O32_KAPPA'] = kap; NSE['O32_GAMMA'] = gu; NSE['O32_ETA'] = eta
    NSE['O32_GAMMA_D'] = gd; NSE['O32_LAMBDA'] = rel
    MA._O36 = bool(dial); NSE['_O36'] = bool(dial)
    MA.O36_LAM_S1 = float(dose)
    MA._pe_clear()
    o = {}
    for k in MAT:
        with contextlib.redirect_stdout(io.StringIO()):
            o[k] = float(ev(PB[k], 2026)) / F
    return o


BASE = price(0.0, 0.24, 11.0, 0.41, 14.0, 1.08, dial=False)
assert all(BASE[k] == BJ['mature_values'][k] / F for k in MAT), 'baseline is not the landing candidate'
CAP = {k: min(25.0, max(1.0, 0.005 * BASE[k])) for k in MAT}
print('ORDER J — J-TOL ON THE REFERENCE POINT AND ITS RUNNERS-UP (board points, tall factor OFF)')
print('  caps: per row min(25, max(1, 0.5%% of value)) · churn <= %.2f · net <= %.2f' % (CAP_CHURN, CAP_NET))

PTS = [('REFERENCE   d0.10 k0.240 gu10.5 e0.425 gd14.0', 0.10, 0.240, 10.5, 0.425, 14.0, 1.08),
       ('runner-up 1 d0.15 k0.230 gu10.0 e0.425 gd13.5', 0.15, 0.230, 10.0, 0.425, 13.5, 1.08),
       ('runner-up 2 d0.10 k0.240 gu10.0 e0.425 gd13.5', 0.10, 0.240, 10.0, 0.425, 13.5, 1.08),
       ('the repair point itself (counterweight frozen)', 0.10, 0.240, 11.0, 0.410, 14.0, 1.08)]
OUT = {}
print('\n%-48s %6s %6s %9s %9s %9s %9s  %s'
      % ('point', 'moved', 'over', 'worst', 'its cap', 'churn', 'net', 'J-TOL'))
for nm, dose, kap, gu, eta, gd, rel in PTS:
    cur = price(dose, kap, gu, eta, gd, rel)
    d = {k: cur[k] - BASE[k] for k in MAT}
    over = sorted([(abs(d[k]) / CAP[k], k) for k in MAT if abs(d[k]) > CAP[k]], reverse=True)
    churn = sum(abs(v) for v in d.values()); net = sum(d.values())
    w = max(MAT, key=lambda k: abs(d[k]))
    need = max((abs(d[k]) / BASE[k]) for k in MAT if abs(d[k]) > 1.0) if any(abs(v) > 1.0 for v in d.values()) else 0.0
    ok = (not over) and churn <= CAP_CHURN and abs(net) <= CAP_NET
    OUT[nm] = dict(dose=dose, kappa=kap, gamma_u=gu, eta=eta, gamma_d=gd, lam_rel=rel,
                   n_moved=sum(1 for v in d.values() if v != 0), n_over=len(over),
                   worst=abs(d[w]), worst_row=w, churn=churn, net=net, passes=bool(ok),
                   needs_pct=100 * need,
                   top_over=[dict(key=k, name=NAME.get(k), age=AGEOF[k], value=BASE[k],
                                  move=d[k], pct=100 * d[k] / BASE[k], cap=CAP[k])
                             for _, k in over[:12]])
    print('%-48s %6d %6d %9.3f %9.3f %9.1f %+9.1f  %s'
          % (nm, OUT[nm]['n_moved'], len(over), abs(d[w]), CAP[w], churn, net,
             'PASS' if ok else 'FAIL (needs %.2f%% per row)' % (100 * need)))

print('\n-- THE REFERENCE POINT: WHO BREAKS, AND BY HOW MUCH OF HIS OWN VALUE --')
print('   %-24s %4s %10s %10s %9s %9s' % ('row', 'age', 'value', 'move', 'as %', 'its cap'))
for r in OUT[PTS[0][0]]['top_over']:
    print('   %-24s %4d %10.1f %+10.2f %+8.2f%% %9.2f'
          % ((r['name'] or r['key'])[:24], r['age'], r['value'], r['move'], r['pct'], r['cap']))
json.dump(OUT, open(os.path.join(HERE, 'JTOL_REF_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: JTOL_REF_J.json')
