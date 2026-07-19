#!/usr/bin/env python3
# LEG F3 — what PINS the forward value of a young pedigree row? el/staleness vs floor_frac*v0 vs pr.
import os, io, contextlib
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; PR = g['PR']; nseas_pro = g['nseas_pro']; v0_start = g['v0_start']
prod_path = g['_prod_path']; floor_frac = g['floor_frac']; ev_prefloor = g['ev_prefloor']
sitout_ev = g.get('sitout_ev'); delisted = g['delisted']

def diag(nm):
    p = next((pp for pp in players if nm.lower() in (pp.get('player') or '').lower()), None)
    if not p: return
    for (Y, form) in [(2026, None), (2027, 2026)]:
        MA._LENS_FORM = form; MA.AGE_REF = Y; MA.BASE_REF = form if form is not None else Y; MA._pe_clear()
        el = PR.tenure(p, Y); ns = nseas_pro(p, Y); v0 = v0_start(p)
        e = prod_path(p, Y); pre = ev_prefloor(p, Y); fin = ev(p, Y)
        yis = Y - int(p.get('year') or 0); fl = floor_frac(yis) * v0
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        tag = 'FLOOR' if abs(fin - fl) < 2 else ('prefloor' if abs(fin - pre) < 2 else '?')
        print("  %s Y=%d form=%s | el=%.1f ns=%d v0=%.0f | prod_path=%.0f prefloor=%.0f floor(%.2f)=%.0f | ev=%.0f [%s]" %
              (nm[:12], Y, form, el, ns, v0, e, pre, floor_frac(yis), fl, fin, tag))

for nm in ['Jagga Smith', 'Xavier Lindsay', 'Jed Walter', 'Sam Lalor', 'Nate Caddy', 'Nick Daicos']:
    diag(nm); print()
