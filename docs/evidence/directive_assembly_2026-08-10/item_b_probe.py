"""ITEM B — re-derive the pool year-0 age gradient on the DOB-written store. READ-ONLY.

Level-preserving (C5): the factors are a RELATIVE gradient inside the pool, so the unknown global
scale of the delivery instrument cancels — this measurement does NOT depend on the four-instrument
ruler's absolute level (which ITEM I could not reproduce).

  band factor = mean_band( delivered / entry_anchor )  normalised so the anchor-weighted
  mean factor over the whole pool = 1.0  ->  pool Sigma v0 held EXACTLY by construction.

F8 = PLAYER UNIT: effective n counts PLAYERS, never player-seasons.
Prior measurement (directive SS2B): <=18 x0.666 / 19-20 x1.200 / 21+ x2.474.
"""
import sys, math, collections
sys.path.insert(0, '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad')
from engine_load import load
import numpy as np
g_ = load()
MA = g_['MA']; cp = g_['cp']
entry_anchor = g_['entry_anchor']
D = MA.LENS['bal']; REPL = MA.REPL; posval = MA.posval; capt_prem = MA.capt_prem
real = [p for p in MA.data if g_['_isreal'](p)]

def deliv(p, avail='in', hor=11):
    d = MA.debut(p); rp = REPL.get(MA.gfut(p), 70.0); t = 0.0
    for s in p['scoring']:
        if s['games'] <= 0: continue
        k = s['year'] - d + 1
        if k < 1 or (hor and k > hor): continue
        G = s['games'] if avail == 'in' else 21.0
        t += posval(s['avg'] + capt_prem(s['avg']) - rp) * G / ((1 + D) ** (k - 1))
    return t

def draft_age(p):
    """the DOB-derived draft age; None where the store carries no birthdate (own cell, never absorbed)."""
    if p.get('_by') is None: return None
    return g_['_ageR'](p)

def band(a):
    if a is None: return 'age-unknown'
    if a <= 18: return '<=18'
    if a <= 20: return '19-20'
    return '21+'

pool = [p for p in real if p.get('_pool')]
print('POOL POPULATION (engine classification): n = %d' % len(pool))

# only rows with a record can teach the gradient; rows without one still CARRY it.
rows = []
for p in pool:
    a = entry_anchor(p)
    dl = deliv(p)
    if a <= 0: continue
    rows.append((p, band(draft_age(p)), a, dl, dl / a))
print('  with a scored record (teaching rows): %d' % len([r for r in rows if r[3] > 0]))

print('\n=== THE RE-DERIVED POOL YEAR-0 AGE GRADIENT (F8 at PLAYER unit) ===')
order = ['<=18', '19-20', '21+', 'age-unknown']
by = collections.defaultdict(list)
for p, b, a, dl, r in rows: by[b].append((p, a, dl, r))

# raw band means, then the level-preserving normalisation
raw = {}
for b in order:
    v = by.get(b) or []
    if not v: continue
    raw[b] = float(np.mean([x[3] for x in v]))
tot_anchor = sum(a for _p, _b, a, _d, _r in rows)
wmean = sum(a * raw.get(b, 1.0) for _p, b, a, _d, _r in rows) / tot_anchor
print(' anchor-weighted mean raw ratio (the normaliser) = %.6f' % wmean)
print('\n %-13s %-6s %-9s %-9s %-11s %-11s %-9s' % ('band', 'n', 'Sig anchor', 'raw ratio', 'FACTOR', 'prior', 'shift'))
PRIOR = {'<=18': 0.666, '19-20': 1.200, '21+': 2.474}
newsum = 0.0
for b in order:
    v = by.get(b) or []
    if not v: continue
    sa = sum(x[1] for x in v)
    f = raw[b] / wmean
    newsum += sa * f
    pr = PRIOR.get(b)
    print(' %-13s %-6d %-9.1f %-9.4f %-11.4f %-11s %-9s'
          % (b, len(v), sa, raw[b], f, ('%.3f' % pr) if pr else '-- (own cell)',
             ('%+.1f%%' % (100 * (f / pr - 1))) if pr else '--'))
print('\n CONSERVATION: Sigma anchor before = %.1f   after (x factor) = %.1f   delta = %.6f'
      % (tot_anchor, newsum, newsum - tot_anchor))

# ---- F8 player-unit evidence bar per cell
print('\n=== F8 PLAYER-UNIT EVIDENCE BAR PER CELL ===')
print(' effective n = (Sig w)^2 / Sig w^2 over PLAYERS (w = anchor), never player-seasons.')
print(' %-13s %-8s %-10s %-12s %-10s' % ('band', 'players', 'eff-n', 'player-seasons', 'F8 (>=35?)'))
for b in order:
    v = by.get(b) or []
    if not v: continue
    w = np.array([x[1] for x in v], dtype=float)
    effn = (w.sum() ** 2) / (w * w).sum() if w.sum() > 0 else 0.0
    pseas = sum(len([s for s in x[0]['scoring'] if s['games'] > 0]) for x in v)
    print(' %-13s %-8d %-10.1f %-12d %-10s' % (b, len(v), effn, pseas, 'PASS' if effn >= 35 else 'FAIL'))
