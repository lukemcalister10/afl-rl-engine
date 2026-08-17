#!/usr/bin/env python3
"""ORDER I — THE MATURE-ROW IDENTITY GATE, MEASURED KNOB POINT BY KNOB POINT ON THE LIVE BOARD.

The owner's law G6: every row aged 24 or over is BYTE-IDENTICAL to the landing candidate. Not "within
rounding" — identical. This script decides, before any calibration, which of the counterweight's knobs
the law actually leaves free. It must run at STAGE 6, because the re-mix is inert below it and a
stage-5 probe would report every knob as harmless when it is not.

The re-mix is keyed on CAREER GAMES, not on age. A 27-year-old with 141 career games sits on the same
rho curve as a 19-year-old with 141 games would; move the curve and you move him. So this is not a
subtle interaction — it is the mechanism working as designed, colliding with a law that says mature
rows cannot move.

Store-wide, tolerance ZERO, every active row aged 24+.
"""
import os, sys, json, io, contextlib, time

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
MA = NSE.get('MA', MA)
assert NSE['_O32S'] == 6, 'the mature gate MUST be probed at stage 6 — the re-mix is inert below it'
ev = NSE['ev']
BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
MAT = sorted([p.get('key') for p in PB.values()
              if NSE['_isreal'](p) and not p.get('_retired') and not NSE['delisted'](p)
              and MA.GRP.get(p.get('pos')) and p.get('_by') and MA._age_at(p, 2026) >= 24])
YOUNG = sorted([p.get('key') for p in PB.values()
                if NSE['_isreal'](p) and not p.get('_retired') and not NSE['delisted'](p)
                and MA.GRP.get(p.get('pos')) and p.get('_by') and MA._age_at(p, 2026) < 24])
print('stage %d; active rows aged 24+ under the store-wide identity assert: %d (young: %d)'
      % (NSE['_O32S'], len(MAT), len(YOUNG)))
REPAIR = dict(kappa=0.24, gamma_u=11.0, eta=0.41, gamma_d=14.0, lam_rel=1.08)


def price(keys, dose, **kn):
    NSE['O32_KAPPA'] = kn['kappa']; NSE['O32_GAMMA'] = kn['gamma_u']; NSE['O32_ETA'] = kn['eta']
    NSE['O32_GAMMA_D'] = kn['gamma_d']; NSE['O32_LAMBDA'] = kn['lam_rel']
    MA.O36_LAM_S1 = dose
    MA._pe_clear()
    out = {}
    for k in keys:
        with contextlib.redirect_stdout(io.StringIO()):
            out[k] = float(ev(PB[k], 2026))
    return out


BASE = price(MAT, 0.0, **REPAIR)          # == the landing candidate 1f176444 on these rows
CTRL = price(MAT, 0.0, **REPAIR)
assert all(BASE[k] == CTRL[k] for k in MAT), 'the harness is not repeatable — HALT'
print('harness repeatability control: PASS (identical on all %d rows)' % len(MAT))


def gate(dose, **kn):
    cur = price(MAT, dose, **kn)
    bad = sorted([(abs(cur[k] - BASE[k]), k) for k in MAT if cur[k] != BASE[k]], reverse=True)
    return len(bad), (bad[0][0] if bad else 0.0), (bad[0][1] if bad else None)


R = {}
print('\n%-46s %8s %10s  %s' % ('point', 'moved', 'worst', 'row'))


def row(nm, dose, **kn):
    n, w, k = gate(dose, **kn)
    R[nm] = dict(n_moved=n, worst=w, worst_row=k, passes=(n == 0), dose=dose, **kn)
    print('%-46s %8d %10.4f  %s' % (nm, n, w, k or ''))
    return n == 0


T0 = time.time()
print('-- THE S1 DOSE AXIS (knobs and relief at the repair point) --')
for d in (0.15, 0.35, 0.70, 1.00):
    row('lambda_S1 = %.2f' % d, d, **REPAIR)
print('-- THE RE-MIX KNOB AXIS (dose 0.35) --')
for nm, kn in (('kappa 0.24 -> 0.25', dict(REPAIR, kappa=0.25)),
               ('kappa 0.24 -> 0.30', dict(REPAIR, kappa=0.30)),
               ('kappa 0.24 -> 0.34', dict(REPAIR, kappa=0.34)),
               ('kappa 0.24 -> 0.20', dict(REPAIR, kappa=0.20)),
               ('gamma_u 11 -> 12', dict(REPAIR, gamma_u=12.0)),
               ('gamma_u 11 -> 10', dict(REPAIR, gamma_u=10.0)),
               ('eta 0.41 -> 0.42', dict(REPAIR, eta=0.42)),
               ('eta 0.41 -> 0.50', dict(REPAIR, eta=0.50)),
               ('eta 0.41 -> 0.30', dict(REPAIR, eta=0.30)),
               ('gamma_d 14 -> 13', dict(REPAIR, gamma_d=13.0)),
               ('gamma_d 14 -> 12', dict(REPAIR, gamma_d=12.0))):
    row(nm, 0.35, **kn)
print('-- THE RELIEF AXIS (dose 0.35, knobs at the repair point) --')
for lr in (0.80, 1.00, 1.08, 1.20, 1.30):
    row('lambda_rel = %.2f' % lr, 0.35, **dict(REPAIR, lam_rel=lr))
print('-- THE TALL/SMALL FADE (it is inside RL_O36 and cannot be switched off here; the dose-0 row '
      'above with the repair knobs IS the fade-only board) --')

free = [nm for nm, d in R.items() if d['passes']]
knobfree = [nm for nm in free if nm.startswith(('kappa', 'gamma', 'eta'))]
relfree = [nm for nm in free if nm.startswith('lambda_rel')]
dosefree = [nm for nm in free if nm.startswith('lambda_S1')]
print('\nVERDICT (%.0fs):' % (time.time() - T0))
print('  S1 dose axis      : %d of 4 doses leave every mature row byte-identical' % len(dosefree))
print('  re-mix knob axis  : %d of 11 knob moves leave every mature row byte-identical' % len(knobfree))
print('  relief axis       : %d of 5 relief values leave every mature row byte-identical' % len(relfree))
print('  tall/small fade   : carried in every row above (it is the dial, not an axis)')
if not knobfree:
    print('  => THE COUNTERWEIGHT\'S RE-MIX KNOBS ARE PINNED AT THE REPAIR POINT BY THE OWNER\'S OWN')
    print('     MATURE-ROW LAW. Not a choice this seat made — a law this seat obeyed.')
json.dump(dict(order='ORDER I — the mature-row identity gate, stage 6, store-wide, tolerance zero',
               n_mature=len(MAT), n_young=len(YOUNG), repair_point=REPAIR, results=R,
               knob_axis_free=knobfree, relief_axis_free=relfree, dose_axis_free=dosefree),
          open(os.path.join(HERE, 'MATURE_GATE_36.json'), 'w'), indent=1, sort_keys=True, default=float)
print('written: MATURE_GATE_36.json')
