#!/usr/bin/env python3
# LEG F3 — FIX-HYPOTHESIS VALIDATION (READ-ONLY monkeypatch; nothing written to engine files).
# Hypothesis: in the FORWARD lens (AGE_REF>BASE_REF) the EVIDENCE clock (tenure, produced-seasons)
# must stay at BASE_REF (the form anchor), while only AGE advances. This carries the pedigree/evidence
# blend forward (Reid-compliant: same map, projected evidence state; no new multiplier/growth term).
# Test: floor the eval-year seen by the evidence gates at BASE_REF and re-measure the cohort gradient.
import os, io, contextlib
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; GRP = G['GRP']

def totals(label):
    Sv = SvP1 = 0.0; coh = defaultdict(lambda: [0, 0.0, 0.0])
    MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    for p in players:
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear(); v = ev(p, 2026)
        MA._LENS_FORM = 2026; MA.BASE_REF = 2026; MA.AGE_REF = 2027; MA._pe_clear(); vP1 = ev(p, 2027)
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        Sv += v; SvP1 += vP1
        a = age(p); c = 'dev(<=23)' if (a or 99) <= 23 else 'mid(24-27)' if a <= 27 else 'vet(>=28)'
        coh[c][0] += 1; coh[c][1] += v; coh[c][2] += vP1
    print("\n[%s]  Sv=%.0f  SvP1=%.0f  (%+.1f%%)" % (label, Sv, SvP1, 100 * (SvP1 / Sv - 1)))
    for c in ('dev(<=23)', 'mid(24-27)', 'vet(>=28)'):
        n, now, fwd = coh[c]; print("   %-11s n=%3d  d=%+9.0f  %+6.1f%%" % (c, n, fwd - now, 100 * (fwd - now) / now))
    return Sv, SvP1

# ---- baseline (unpatched) ----
totals("BASELINE (unpatched)")

# ---- patch: evidence gates see min(Y, BASE_REF) in the forward lens ----
_tenure0 = g['PR'].tenure; _nseas0 = g['nseas_pro']
def _clk(Y):
    b = getattr(MA, 'BASE_REF', Y)
    return min(Y, b) if b is not None else Y
g['PR'].tenure = lambda p, Y=2026: _tenure0(p, _clk(Y))
_ns_name = 'nseas_pro'
g[_ns_name] = lambda p, Y=2026, _f=_nseas0: _f(p, _clk(Y))
# ev closed over the ORIGINAL nseas_pro name at def-time; rebind via globals of the exec namespace:
import types
ev.__globals__['nseas_pro'] = g[_ns_name]
ev.__globals__['PR'].tenure = g['PR'].tenure

totals("PATCHED (evidence clock anchored at BASE_REF)")
