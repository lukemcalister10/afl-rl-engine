#!/usr/bin/env python3
"""ORDER J — J-TOL, THE CORRECTED MATURE-ROW GATE, MEASURED STORE-WIDE ON THE LIVE BOARD.

The rule is PREREG_J.md §2.2, pushed before this file produced a number. Restated so the code and the
prereg can be read against each other:

    board points = ev / 1.0524                    (the engine's own re-denomination scalar)
    (a) per row   |d_i| <= min(25.0, max(1.0, 0.005 * v_i))
    (b) churn     sum|d_i| <= 0.15% of the board total  = 1001.87
    (c) net       |sum d_i| <= 0.10% of the board total =  667.91

Measured on every active row aged 24+ (429 of them) against the landing candidate 1f176444.

THE EXEMPT LEVER IS OUT OF THE MEASUREMENT. This runs with RL_O36_TALL=0, so Order H's owner-ruled
tall/small factor is not live and every delta here is attributable to S1 + the counterweight alone.
The ruled factor's own mature movement is DISCLOSED separately by o37_tall_disclose.py.

S1 keeps the zero-tolerance test (PREREG_J §2.1) and it is measured here too, on its own.
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
assert NSE['_O32S'] == 6, 'J-TOL MUST be measured at stage 6 — the re-mix is inert below it'

F = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'pick_redenomination.json')))['factor']
assert abs(F - 1.0524) < 1e-12
BASE_J = json.load(open(os.path.join(HERE, 'BASELINE_J.json')))
BOARD_TOTAL_BP = BASE_J['board_total'] / F
CAP_CHURN = 0.0015 * BOARD_TOTAL_BP
CAP_NET = 0.0010 * BOARD_TOTAL_BP
print('J-TOL caps from PREREG_J §2.2 — board total %.1f bp · churn cap %.2f · net cap %.2f'
      % (BOARD_TOTAL_BP, CAP_CHURN, CAP_NET))

BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
ACT = [p for p in PB.values() if NSE['_isreal'](p) and not p.get('_retired')
       and not NSE['delisted'](p) and MA.GRP.get(p.get('pos'))]
MAT = sorted([p.get('key') for p in ACT if p.get('_by') and MA._age_at(p, 2026) >= 24])
AGE = {p.get('key'): MA._age_at(p, 2026) for p in ACT}
print('active rows under the store-wide gate, aged 24+: %d' % len(MAT))
REPAIR = dict(kappa=0.24, gamma_u=11.0, eta=0.41, gamma_d=14.0, lam_rel=1.08)


def price(keys, dose, dial=True, **kn):
    NSE['O32_KAPPA'] = kn['kappa']; NSE['O32_GAMMA'] = kn['gamma_u']; NSE['O32_ETA'] = kn['eta']
    NSE['O32_GAMMA_D'] = kn['gamma_d']; NSE['O32_LAMBDA'] = kn['lam_rel']
    MA._O36 = bool(dial); NSE['_O36'] = bool(dial)
    MA.O36_LAM_S1 = float(dose)
    MA._pe_clear()
    out = {}
    for k in keys:
        with contextlib.redirect_stdout(io.StringIO()):
            out[k] = float(ev(PB[k], 2026)) / F
    return out


T0 = time.time()
BASE = price(MAT, 0.0, dial=False, **REPAIR)
print('baseline priced in %.0fs' % (time.time() - T0))
CTRL = price(MAT, 0.0, dial=False, **REPAIR)
assert all(BASE[k] == CTRL[k] for k in MAT), 'the harness is not repeatable — HALT'
bad = [k for k in MAT if abs(BASE[k] - BASE_J['mature_values'][k] / F) > 0]
print('harness repeatability: PASS on all %d rows · identity vs BASELINE_J: %s'
      % (len(MAT), 'EXACT on 429 of 429' if not bad else 'DEVIATION on %d rows' % len(bad)))
assert not bad, 'the in-process dial-off baseline is not the landing candidate — HALT'
CAP = {k: min(25.0, max(1.0, 0.005 * BASE[k])) for k in MAT}
print('per-row caps: min %.2f · median %.2f · max %.2f board points'
      % (min(CAP.values()), sorted(CAP.values())[len(CAP) // 2], max(CAP.values())))


def jtol(dose, **kn):
    cur = price(MAT, dose, dial=True, **kn)
    d = {k: cur[k] - BASE[k] for k in MAT}
    over = sorted([(abs(d[k]) / CAP[k], k, d[k], CAP[k]) for k in MAT if abs(d[k]) > CAP[k]], reverse=True)
    churn = sum(abs(v) for v in d.values()); net = sum(d.values())
    nmov = sum(1 for v in d.values() if v != 0.0)
    worst = max((abs(v), k) for k, v in d.items()) if d else (0.0, None)
    return dict(n_moved=nmov, n_over_row_cap=len(over), worst=worst[0], worst_row=worst[1],
                worst_over=(over[0][1] if over else None),
                worst_over_ratio=(over[0][0] if over else 0.0),
                worst_over_delta=(over[0][2] if over else 0.0),
                worst_over_cap=(over[0][3] if over else 0.0),
                churn=churn, net=net,
                pass_a=(not over), pass_b=(churn <= CAP_CHURN), pass_c=(abs(net) <= CAP_NET),
                passes=(not over) and (churn <= CAP_CHURN) and (abs(net) <= CAP_NET),
                deltas={k: d[k] for k in MAT if d[k] != 0.0}, dose=dose, **kn)


R = {}
HDR = ('%-40s %6s %6s %9s %9s %10s %9s  %-5s%-5s%-5s %s'
       % ('point', 'moved', 'over', 'worst', 'its cap', 'churn', 'net', '(a)', '(b)', '(c)', 'J-TOL'))


def row(nm, dose, quiet=False, **kn):
    g = jtol(dose, **kn)
    R[nm] = {x: y for x, y in g.items() if x != 'deltas'}
    R[nm]['deltas'] = g['deltas']
    if not quiet:
        print('%-40s %6d %6d %9.3f %9.3f %10.1f %+9.1f  %-5s%-5s%-5s %s'
              % (nm, g['n_moved'], g['n_over_row_cap'], g['worst'], CAP.get(g['worst_row'], 0.0),
                 g['churn'], g['net'], 'ok' if g['pass_a'] else 'FAIL',
                 'ok' if g['pass_b'] else 'FAIL', 'ok' if g['pass_c'] else 'FAIL',
                 'PASS' if g['passes'] else 'FAIL'))
    return g['passes']


print('\n=== 1 · S1 ALONE — THE ZERO-TOLERANCE TEST (PREREG_J §2.1), COUNTERWEIGHT AT THE REPAIR POINT ===')
print('%-40s %8s %10s  %s' % ('point', 'moved', 'worst', 'verdict'))
S1R = {}
for d in (0.10, 0.15, 0.25, 0.35, 0.45, 0.70, 1.00):
    g = jtol(d, **REPAIR)
    S1R['lambda_S1 = %.2f' % d] = dict(n_moved=g['n_moved'], worst=g['worst'], worst_row=g['worst_row'],
                                       passes=(g['n_moved'] == 0))
    print('%-40s %8d %10.4f  %s' % ('lambda_S1 = %.2f' % d, g['n_moved'], g['worst'],
                                    'PASS — zero' if g['n_moved'] == 0 else 'FAIL — F1 FIRES'))
F1 = [k for k, v in S1R.items() if not v['passes']]
print('S1 zero-tolerance verdict: %d of %d doses leave every mature row byte-identical  -> %s'
      % (sum(1 for v in S1R.values() if v['passes']), len(S1R),
         'PASS' if not F1 else 'F1 FIRES on ' + ', '.join(F1)))

print('\n=== 2 · THE COUNTERWEIGHT KNOB LADDER UNDER J-TOL (dose 0.35, Order I\'s own comparison dose) ===')
print(HDR)
LADDER = [('kappa 0.24 -> %.2f' % k, dict(REPAIR, kappa=k)) for k in
          (0.15, 0.18, 0.20, 0.22, 0.26, 0.28, 0.30, 0.35, 0.40, 0.50, 0.60)]
LADDER += [('eta 0.41 -> %.2f' % e, dict(REPAIR, eta=e)) for e in (0.00, 0.10, 0.20, 0.30, 0.42, 0.45, 0.50)]
LADDER += [('gamma_u 11 -> %.0f' % u, dict(REPAIR, gamma_u=u)) for u in (8.0, 10.0, 12.0, 14.0, 16.0)]
LADDER += [('gamma_d 14 -> %.0f' % v, dict(REPAIR, gamma_d=v)) for v in (4.0, 6.0, 8.0, 10.0, 12.0, 13.0)]
LADDER += [('lambda_rel 1.08 -> %.2f' % r, dict(REPAIR, lam_rel=r)) for r in (0.80, 0.90, 1.00, 1.20, 1.30)]
for nm, kn in LADDER:
    row(nm, 0.35, **kn)

print('\n=== 3 · THE SEARCH SHORTLIST — THE JOINT SETTINGS, IN SELECTION ORDER ===')
SH = json.load(open(os.path.join(HERE, 'REGION_J.json')))['shortlist']
print(HDR)
CAND = []
for i, M in enumerate(SH, 1):
    kn = dict(kappa=M['kappa'], gamma_u=M['gamma_u'], eta=M['eta'], gamma_d=M['gamma_d'],
              lam_rel=M['lam_rel'])
    nm = '#%d  d%.2f k%.2f gu%.0f e%.2f gd%.0f r%.2f' % (i, M['dose'], M['kappa'], M['gamma_u'],
                                                         M['eta'], M['gamma_d'], M['lam_rel'])
    ok = row(nm, M['dose'], **kn)
    CAND.append(dict(rank=i, point=M, name=nm, jtol=R[nm]['passes'],
                     churn=R[nm]['churn'], net=R[nm]['net'], n_over=R[nm]['n_over_row_cap'],
                     worst=R[nm]['worst'], worst_row=R[nm]['worst_row']))

surv = [c for c in CAND if c['jtol']]
print('\nJ-TOL VERDICT ON THE SHORTLIST: %d of %d joint settings PASS the corrected mature gate'
      % (len(surv), len(CAND)))
if surv:
    b = surv[0]
    print('  the selection law\'s choice (min corrected-surface SSE among J-TOL survivors): %s' % b['name'])

lad_pass = [nm for nm, kn in LADDER if R[nm]['passes']]
print('\nknob ladder: %d of %d single-axis moves pass J-TOL (Order I\'s zero-tolerance test passed 0 of 11)'
      % (len(lad_pass), len(LADDER)))

json.dump(dict(order='ORDER J — J-TOL, the corrected mature-row gate, stage 6, store-wide',
               rule=dict(per_row='min(25.0, max(1.0, 0.005*v))', churn_cap=CAP_CHURN, net_cap=CAP_NET,
                         board_total_bp=BOARD_TOTAL_BP, currency='board points = ev / 1.0524',
                         tall_factor='EXCLUDED from the measurement (RL_O36_TALL=0) — it is exempt'),
               n_mature=len(MAT), s1_zero_tolerance=S1R, s1_pass=(not F1),
               ladder={nm: {x: y for x, y in R[nm].items() if x != 'deltas'} for nm, _ in LADDER},
               shortlist=CAND, n_shortlist_pass=len(surv),
               ages={k: AGE[k] for k in MAT}, base={k: BASE[k] for k in MAT},
               caps=CAP),
          open(os.path.join(HERE, 'JTOL_J.json'), 'w'), indent=1, sort_keys=True, default=float)
json.dump({nm: R[nm]['deltas'] for nm in R}, open(os.path.join(HERE, 'JTOL_RAW.json'), 'w'),
          sort_keys=True, default=float)
print('\nwritten: JTOL_J.json + JTOL_RAW.json  (%.0fs total)' % (time.time() - T0))
