#!/usr/bin/env python3
# LEG F3 — split raw_ev into its production leg pr=price6(b6) vs the pedigree-pole credit
# w*recover(perf,par)*(po-pr), at k=0 vs +1 (form-anchored). Pin whether the forward drop is the
# production map (pr / proj_from_peak territory) or the pole credit.
import os, io, contextlib
import numpy as np
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; effpk = G['effpk']
b6 = g['b6']; price6 = g['price6']; par_pole = g['par_pole']; PR = g['PR']; cp = g['cp']
eff_ten = g['eff_ten']; recover = g['recover']; _expgate = g['_expgate']; _uncomp_prod = g['_uncomp_prod']
fac = g.get('_form_anchor_clock')
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def legs(p, Y, form):
    MA._LENS_FORM = form; MA.AGE_REF = Y; MA.BASE_REF = form if form is not None else Y; MA._pe_clear()
    _bb = b6(p, Y); pr = price6(p, _bb, Y); pr = _uncomp_prod(pr, p, Y, _bb)
    pos = MA.gfut(p); pk = MA.effpk(p)
    ctx = contextlib.nullcontext() if fac is None else fac()
    with ctx:
        T = min(max(PR.tenure(p, Y), 1), 6); et = min(max(eff_ten(p, Y, PR.tenure(p, Y)), 1), 6)
        po, par = par_pole(pos, pk, T); a = MA.age(p)
        wage = 0.0 if pos == 'RUC' else float(np.clip(1 - ((a or 21) - 20) / 6, 0, 1))
        tfade = float(np.interp(et, [1, 2, 3, 4, 5, 6], [1.00, 0.76, 0.40, 0.16, 0.05, 0.05]))
        w = wage * tfade * _expgate(p, Y)
    perf = cp._lvl_wt(p, Y); pole = w * recover(perf, par) * max(0.0, po - pr)
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    return dict(pr=pr, pole=pole, po=po, w=w, T=T, et=et, evv=ev(p, Y) if form is None else None)

names = ['Jagga Smith', 'Xavier Lindsay', 'Taj Hotton', 'Sam Lalor', 'Jed Walter', 'Nate Caddy']
print("%-15s | %6s %6s %5s %5s | %6s %6s %5s %5s | %6s" % ("name", "pr26", "pole26", "po26", "w26", "pr27", "pole27", "po27", "w27", "Dpr%"))
for nm in names:
    p = next((pp for pp in players if nm.lower() in (pp.get('player') or '').lower()), None)
    if not p: continue
    L0 = legs(p, 2026, None); L1 = legs(p, 2027, 2026)
    dpr = 100 * (L1['pr'] / L0['pr'] - 1) if L0['pr'] else 0
    print("%-15s | %6.0f %6.0f %5.0f %5.2f | %6.0f %6.0f %5.0f %5.2f | %+5.1f" %
          (nm[:15], L0['pr'], L0['pole'], L0['po'], L0['w'], L1['pr'], L1['pole'], L1['po'], L1['w'], dpr))
print("\npr=production price (b6/price6 map); pole=pedigree-pole credit. Dpr%=production leg forward change.")
