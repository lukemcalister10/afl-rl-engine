#!/usr/bin/env python3
# LEG F4 — split raw_ev into pr(=price6(b6) production price) vs pole(pedigree), per cohort, fwd/back.
# And measure b6 (the 6-band demonstrated-level block) forward change. READ-ONLY.
import os, io, contextlib
from collections import defaultdict
import numpy as np
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; effpk = G['effpk']
b6 = g['b6']; price6 = g['price6']; par_pole = g['par_pole']; PR = g['PR']; cp = g['cp']
eff_ten = g['eff_ten']; recover = g['recover']; _expgate = g['_expgate']; _uncomp_prod = g['_uncomp_prod']
fac = g.get('_form_anchor_clock')

def coh_of(a): return 'developing' if (a or 99) <= 23 else 'mid' if a <= 27 else 'veteran'

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
    bmean = float(np.mean(_bb))
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    return pr, pole, bmean

acc = defaultdict(lambda: defaultdict(float)); N = defaultdict(int)
for p in players:
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    c = coh_of(age(p)); N[c] += 1
    prn, pon, bn = legs(p, 2026, None)
    prf, pof, bf = legs(p, 2027, 2026)
    prb, pob, bb = legs(p, 2025, None)
    d = acc[c]
    d['pr_now'] += prn; d['pr_fwd'] += prf; d['pr_bak'] += prb
    d['po_now'] += pon; d['po_fwd'] += pof; d['po_bak'] += pob
    d['b_now'] += bn; d['b_fwd'] += bf; d['b_bak'] += bb

print("%-11s %5s | %-24s | %-20s | %-22s" % ('cohort', 'n', 'pr (price6/b6) fwd/back', 'pole fwd/back', 'b6 mean fwd/back'))
for c in ('developing', 'mid', 'veteran'):
    d = acc[c]
    def pcs(now, fwd, bak): return (100 * (fwd / now - 1) if now else 0, 100 * (now / bak - 1) if bak else 0)
    prf, prb = pcs(d['pr_now'], d['pr_fwd'], d['pr_bak'])
    pof, pob = pcs(d['po_now'], d['po_fwd'], d['po_bak'])
    bf, bb = pcs(d['b_now'], d['b_fwd'], d['b_bak'])
    print("%-11s %5d | fwd %+6.1f  back %+6.1f  | fwd %+6.1f back %+6.1f | fwd %+6.2f back %+6.2f  (pr share now=%.0f pole=%.0f)" %
          (c, N[c], prf, prb, pof, pob, bf, bb, d['pr_now'], d['po_now']))
