"""ITEM I — reconstruct the four-instrument ruler. READ-ONLY probe.

The target (directive §5): levels A 1.6621 (avail-in x full horizon) · B 1.5883 (avail-in x yr11)
· C 1.6028 (rate x full) · D 1.5468 (rate x yr11) — "the year-4 price stands at 1.55x realized".
"""
import os, sys, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
from engine_load import load
import numpy as np
g = load()
MA = g['MA']; cp = g['cp']; PR = g['PR']
ev = g['ev']

D = MA.LENS['bal']            # 0.14 production discount per year
REPL = MA.REPL
posval = MA.posval
capt_prem = MA.capt_prem

real = [p for p in MA.data if g['_isreal'](p)]
print('real rows', len(real))

def career_seasons(p):
    """(career_year k starting 1 at debut, games, avg, year) for every scored season."""
    d = MA.debut(p)
    out = []
    for s in p['scoring']:
        if s['games'] <= 0: continue
        k = s['year'] - d + 1
        if k < 1: continue
        out.append((k, s['games'], s['avg'], s['year']))
    return sorted(out)

def delivered(p, from_k, avail, horizon):
    """Realized delivery from career year from_k onward, discounted back to from_k."""
    pos = MA.gfut(p)
    rp = REPL.get(pos, 70.0)
    tot = 0.0
    for k, gm, av, yr in career_seasons(p):
        if k < from_k: continue
        if horizon == 11 and k > 11: continue
        G = gm if avail == 'in' else 21.0
        lev = av
        tot += posval(lev + capt_prem(lev) - rp) * G / ((1 + D) ** (k - from_k))
    return tot

# ---- the year-4 price: evaluate the engine at the season that WAS the player's career year 4
def price_at_k(p, k):
    d = MA.debut(p)
    Y = d + k - 1
    try:
        return float(ev(p, Y))
    except Exception:
        return None

# cohort: players whose career year 4 exists in the record and who have subsequent record
rows = []
for p in real:
    cs = career_seasons(p)
    if not cs: continue
    ks = [c[0] for c in cs]
    if 4 not in ks: continue
    if max(ks) < 5: continue          # need delivery after year 4
    rows.append(p)
print('year-4 cohort n =', len(rows))

for avail in ('in', 'rate'):
    for hor in ('full', 11):
        num = den = 0.0; n = 0
        for p in rows:
            pr = price_at_k(p, 4)
            dl = delivered(p, 4, avail, hor)
            if pr is None or dl <= 0: continue
            num += pr; den += dl; n += 1
        print('avail=%-4s horizon=%-4s  n=%d  Sigma price / Sigma realized = %.4f'
              % (avail, str(hor), n, num / den if den else float('nan')))
