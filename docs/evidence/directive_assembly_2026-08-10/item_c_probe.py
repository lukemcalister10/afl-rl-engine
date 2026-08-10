"""ITEM C — reproduce the directive's worked rows exactly, then run the C-Q3 demonstration.

w = G x Q x gate ;  G = g/(g+8) ;  Q = clip(sa/par, 0, 2) with the engine's own par_at + eff_ten
draft-age bridge ;  gate = min(e/entry_anchor, 1).
"""
import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad')
from engine_load import load
import numpy as np
g_ = load()
MA = g_['MA']; cp = g_['cp']; PR = g_['PR']
ev = g_['ev']; entry_anchor = g_['entry_anchor']; eff_ten = g_['eff_ten']
G0 = 8.0; QMAX = 2.0
Y = 2026

byname = {}
for p in MA.data:
    if g_['_isreal'](p): byname.setdefault(p.get('player'), p)

def career(p):
    """g = CAREER games total; sa = CAREER games-weighted average (the directive's main-table
    convention; the latest-season variant is its declared robustness alternative)."""
    gt = 0.0; num = 0.0
    for s in p['scoring']:
        if s['games'] <= 0: continue
        gt += s['games']; num += s['games'] * s['avg']
    return gt, (num / gt if gt else 0.0)

def par_of(p, Y=Y):
    """par_at(pos, pick, T) on the engine's own eff_ten DRAFT-AGE bridge: eff_ten's thin-career
    branch is max(base, age-18), so the draft-age reading is T = clip(draft_age - 18, 1, 6)
    — 'quality judged against WHO HE IS' (directive §2C), resolving §6 discrepancy 2."""
    pos = MA.gfut(p); pk = min(MA.effpk(p), cp.KMAX)
    T = int(min(max(g_['_ageR'](p) - 18, 1), 6))
    return float(PR.par_at(pos, pk, T)), T

def wparts(p, Y=Y):
    gm, sa = career(p)
    par, T = par_of(p, Y)
    G = gm / (gm + G0) if gm > 0 else 0.0
    Q = float(np.clip(sa / par, 0.0, QMAX)) if par > 0 else 0.0
    a = float(entry_anchor(p))
    e = float(ev(p, Y))
    gate = min(e / a, 1.0) if a > 0 else 0.0
    return dict(g=gm, sa=sa, par=par, T=T, G=G, Q=Q, gate=gate, w=G * Q * gate, anchor=a, e=e)

print('=== THE DIRECTIVE WORKED ROWS (target vs reproduced) ===')
TARGET = [
    ('Noah Mraz',       4, 84.25, 57.55, 0.333, 1.464, 1.000, 0.488, 487.5),
    ('Archie Ludowyke', 2, 40.00, 49.03, 0.200, 0.816, 1.000, 0.163, 260.3),
    ('Luke Beecken',    1,  7.00, 77.94, 0.111, 0.090, 0.349, 0.0035, 301.0),
    ('Gerrick Weedon',  1,  5.00, 55.71, 0.111, 0.090, 0.020, 0.0002, 695.3),
    ('Zeke Uwland',    17, 53.58, 69.04, 0.680, 0.776, 1.000, 0.528, 2375.9),
    ('Toby Conway',     6, 74.00, 53.80, 0.429, 1.375, 0.533, 0.314, 992.0),
]
hdr = '%-18s %-5s %-8s %-8s %-7s %-7s %-7s %-8s %-9s'
print(hdr % ('player', 'g', 'sa', 'par', 'G', 'Q', 'gate', 'w', 'anchor'))
for nm, tg, tsa, tpar, tG, tQ, tgate, tw, tanc in TARGET:
    p = byname.get(nm)
    if p is None:
        print('%-18s NOT FOUND IN STORE' % nm); continue
    d = wparts(p)
    print(hdr % (nm, '%d/%d' % (d['g'], tg), '%.2f/%.2f' % (d['sa'], tsa),
                 '%.2f/%.2f' % (d['par'], tpar), '%.3f/%.3f' % (d['G'], tG),
                 '%.3f/%.3f' % (d['Q'], tQ), '%.3f/%.3f' % (d['gate'], tgate),
                 '%.4f/%.4f' % (d['w'], tw), '%.1f/%.1f' % (d['anchor'], tanc)))
    print('%-18s   e=%.1f  e/anchor=%.3f  T=%d' % ('', d['e'], d['e'] / d['anchor'] if d['anchor'] else 0, d['T']))
