#!/usr/bin/env python3
"""ORDER I — THE OWNER'S GATES, SCORED ON THE BOARD, ROW BY NAMED ROW.

One engine load. Prices the named rows and the store-wide mature set on the landing candidate (dial
off) and on ORDER I at the chosen constants, and prints every acceptance gate that lives on the
2026 board with its number and a pass/fail. The band and class gates live on the walk-forward
instruments and are scored by bb_standing_tables36.py and o36_calibrate.py.
"""
import os, sys, json, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DOSE = os.environ.get('O36_DOSE', '0.35')
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
BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
ACT = [p for p in PB.values() if NSE['_isreal'](p) and not p.get('_retired')
       and not NSE['delisted'](p) and MA.GRP.get(p.get('pos'))]
MAT = sorted([p.get('key') for p in ACT if p.get('_by') and MA._age_at(p, 2026) >= 24])
ALL = sorted([p.get('key') for p in ACT])
print('active priced rows %d; aged 24+ %d' % (len(ALL), len(MAT)))

NAMED = [('harry-dean', 'UP', 'above his age bar by 14.9 a game'),
         ('cooper-duff-tytler', 'UP', 'above his age bar by 7.1 a game'),
         ('xavier-taylor', 'DOWN', 'sub-expectation WITH games (42.0 vs an age bar of 55.2)'),
         ('oskar-taylor', 'FLAT', 'zero games — S1 cannot reach him'),
         ('daniel-annable', 'DOWN', 'sub-expectation WITH games (38.0 vs 57.0)'),
         ('dylan-patterson', 'DOWN', 'sub-expectation WITH games (35.6 vs 55.2)'),
         ('josh-smillie', 'UP', 'a small at pick 7 falls onto the 0.5 clip'),
         ('chris-scerri', 'UP', 'pool row — production dominates a small pedigree'),
         ('thomas-burton', 'UP', 'same channel, weaker'),
         ('milan-murdock', 'EXACTLY FLAT', 'age 26 — the cap law'),
         ('will-green', 'UP', 'TALL at pick 16: exponent 0.793 -> 0.500'),
         ('toby-conway', 'UP', 'TALL at pick 24: exponent 0.899 -> 0.500'),
         ('steely-green', 'UP', 'high-rho row, fade clock spent'),
         ('isaac-kako', 'UP', 'S1 on a high-rho row'),
         ('alix-tauru', 'UP', 'S1, and tall gaps are the largest'),
         ('jedd-busslinger', 'UP', 'S1 + re-mix on an above-age-bar season')]
EXTRA = ['levi-ashcroft', 'connor-o-sullivan', 'logan-morris', 'finn-o-sullivan', 'sam-taylor',
         'tom-green', 'toby-greene', 'will-ashcroft', 'taylor-walker', 'keidean-coleman',
         'harry-morrison', 'taylor-goad', 'zac-taylor']


def price(keys, dose):
    MA.O36_LAM_S1 = float(dose)
    MA._pe_clear()
    o = {}
    for k in keys:
        with contextlib.redirect_stdout(io.StringIO()):
            o[k] = float(ev(PB[k], 2026))
    return o


KEYS = sorted(set(ALL))
A = price(KEYS, 0.0)
B = price(KEYS, DOSE)
A2 = price(KEYS, 0.0)
det = sum(1 for k in KEYS if A[k] != A2[k])
print('determinism control (same dial twice, same process): %d of %d rows differ -> %s'
      % (det, len(KEYS), 'PASS' if det == 0 else 'FAIL'))

matmoved = [(k, B[k] - A[k]) for k in MAT if A[k] != B[k]]
print('\nG6 (mature rows): %d of %d rows aged 24+ move.  %s'
      % (len(matmoved), len(MAT), 'PASS — byte-identical store-wide' if not matmoved
         else 'FAIL: ' + str(matmoved[:6])))
print('     murdock whole row: %r -> %r  %s'
      % (A['milan-murdock'], B['milan-murdock'],
         'IDENTICAL' if A['milan-murdock'] == B['milan-murdock'] else 'MOVED'))

print('\n-- THE NAMED ROWS (prereg scorecard) --')
print('%-22s %10s %10s %10s %8s  %-7s %-7s %s'
      % ('row', 'landing', 'ORDER I', 'delta', 'pct', 'pred', 'actual', 'hit?'))
SC = []
for k, pred, why in NAMED:
    a, b = A[k], B[k]
    d = b - a
    act = 'FLAT' if d == 0 else ('UP' if d > 0 else 'DOWN')
    hit = (act == 'FLAT') if pred in ('FLAT', 'EXACTLY FLAT') else (act == pred)
    if pred == 'FLAT' and act != 'FLAT' and abs(d) / max(1.0, a) < 0.01:
        hit = True; act += '<1%'
    SC.append(dict(key=k, pred=pred, actual=act, hit=bool(hit), landing=a, order_i=b, delta=d, why=why))
    print('%-22s %10.1f %10.1f %+10.1f %+7.2f%%  %-7s %-7s %s'
          % (k, a, b, d, 100 * d / max(1.0, a), pred, act, 'HIT' if hit else 'MISS'))
print('\nprereg scorecard: %d of %d named-row directions correct' % (sum(1 for s in SC if s['hit']), len(SC)))
print('\n-- controls and other rows of record --')
for k in EXTRA:
    if k in A:
        print('%-22s %10.1f %10.1f %+10.1f %+7.2f%%' % (k, A[k], B[k], B[k] - A[k], 100 * (B[k] - A[k]) / max(1.0, A[k])))

Y1 = [p for p in ACT if (p.get('year') == 2025) or (p.get('year') == 2026 and p.get('type') == 'MSD')]
Y1K = [p.get('key') for p in Y1]
t0 = sum(A[k] for k in Y1K); t1 = sum(B[k] for k in Y1K)
nd = [p for p in Y1 if p.get('type') == 'ND' and MA.effpk(p) and MA.effpk(p) <= 64]
ndk = [p.get('key') for p in nd]
print('\nyear-1 class on the 2026 board: %d rows, total %.0f -> %.0f (%+.2f%%);  ND 1-64 subset %d rows, '
      '%.0f -> %.0f (%+.2f%%)'
      % (len(Y1K), t0, t1, 100 * (t1 - t0) / t0, len(ndk), sum(A[k] for k in ndk), sum(B[k] for k in ndk),
         100 * (sum(B[k] for k in ndk) / sum(A[k] for k in ndk) - 1)))
up = sum(1 for k in Y1K if B[k] > A[k]); dn = sum(1 for k in Y1K if B[k] < A[k])
print('   %d up, %d down, %d unchanged' % (up, dn, len(Y1K) - up - dn))
json.dump(dict(dose=float(DOSE), n_active=len(ALL), n_mature=len(MAT),
               mature_moved=[{'key': k, 'delta': d} for k, d in matmoved],
               determinism_diffs=det, scorecard=SC,
               named_all={k: dict(landing=A[k], order_i=B[k]) for k, _, _ in NAMED},
               extra={k: dict(landing=A[k], order_i=B[k]) for k in EXTRA if k in A},
               year1=dict(n=len(Y1K), landing=t0, order_i=t1, up=up, down=dn)),
          open(os.path.join(HERE, 'GATES_I.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: GATES_I.json')
