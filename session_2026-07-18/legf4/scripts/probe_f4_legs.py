#!/usr/bin/env python3
# LEG F4 — leg-level attribution of the MID forward decline (READ-ONLY).
# Splits ev's production price into raw_ev (proj_from_peak leg) vs iso_eff, and probes whether the
# forward change lives in peak_est(lp), level_now(cur/dev_advance), or the horizon frac/DELTAS.
import os, io, contextlib
from collections import defaultdict
import numpy as np
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; effpk = G['effpk']; GRP = G['GRP']
raw_ev = g['raw_ev']; iso_eff = g['iso_eff']; peak_est = G['peak_est']; level_now = G['level_now']
level_demo = G['level_demo']; prod_path = g['_prod_path']

def coh_of(a): return 'developing' if (a or 99) <= 23 else 'mid' if a <= 27 else 'veteran'

def setstate(Y, form):
    MA._LENS_FORM = form; MA.AGE_REF = Y; MA.BASE_REF = form if form is not None else Y; MA._pe_clear()
def clr():
    MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

# For each cohort accumulate leg totals now vs +1 (forward form-anchored) vs -1 (backward)
acc = defaultdict(lambda: defaultdict(float)); N = defaultdict(int)
for p in players:
    a0 = None
    clr(); a0 = age(p); c = coh_of(a0); N[c] += 1
    clr(); rn = raw_ev(p, 2026); iN = iso_eff(p, 2026); pn = prod_path(p, 2026); pen = peak_est(p); lnn = level_now(p); ldn = level_demo(p)
    setstate(2027, 2026); rf = raw_ev(p, 2027); iF = iso_eff(p, 2027); pf = prod_path(p, 2027); pef = peak_est(p); lnf = level_now(p)
    setstate(2025, None); rb = raw_ev(p, 2025); ib = iso_eff(p, 2025); pb = prod_path(p, 2025)
    clr()
    d = acc[c]
    d['raw_now'] += rn; d['raw_fwd'] += rf; d['raw_bak'] += rb
    d['iso_now'] += iN; d['iso_fwd'] += iF; d['iso_bak'] += ib
    d['pp_now'] += pn; d['pp_fwd'] += pf; d['pp_bak'] += pb
    d['pe_now'] += (pen or 0); d['pe_fwd'] += (pef or 0)
    d['ln_now'] += (lnn or 0); d['ln_fwd'] += (lnf or 0); d['ld_now'] += (ldn or 0)

print("%-11s %5s | %-22s | %-22s | %-22s" % ('cohort', 'n', 'raw_ev fwd/back %', 'iso fwd/back %', 'prod_path fwd/back %'))
for c in ('developing', 'mid', 'veteran'):
    d = acc[c]
    def pc(now, fwd, bak): return (100 * (fwd / now - 1), 100 * (now / bak - 1))
    rf, rb = pc(d['raw_now'], d['raw_fwd'], d['raw_bak'])
    iF, ib = pc(d['iso_now'], d['iso_fwd'], d['iso_bak'])
    pf, pb = pc(d['pp_now'], d['pp_fwd'], d['pp_bak'])
    print("%-11s %5d | fwd %+6.1f  back %+6.1f | fwd %+6.1f  back %+6.1f | fwd %+6.1f  back %+6.1f" %
          (c, N[c], rf, rb, iF, ib, pf, pb))
print()
print("%-11s | %-24s | %-24s" % ('cohort', 'peak_est(lp) fwd %', 'level_now(cur) fwd % vs demo'))
for c in ('developing', 'mid', 'veteran'):
    d = acc[c]
    pe = 100 * (d['pe_fwd'] / d['pe_now'] - 1) if d['pe_now'] else 0
    lnf = 100 * (d['ln_fwd'] / d['ln_now'] - 1) if d['ln_now'] else 0
    lnn_vs_demo = 100 * (d['ln_now'] / d['ld_now'] - 1) if d['ld_now'] else 0
    print("%-11s | peak_est fwd %+6.2f%%      | level_now fwd %+6.2f%%  (now vs demo %+.2f%%)" % (c, pe, lnf, lnn_vs_demo))
