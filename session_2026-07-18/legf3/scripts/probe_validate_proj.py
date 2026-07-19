#!/usr/bin/env python3
# LEG F3 — VALIDATE the _proj_w4 (proj_from_peak) forward pedigree-carry (READ-ONLY monkeypatch).
# v_at_peak -> proj_from_peak(g,L,a,cur,...); the forward pr collapse is the horizon+runway keying on the
# advancing age a. Reid fix: form-anchor the young/pedigree age to BASE_REF (offset=AGE_REF-BASE_REF => a_fa=a-off),
# so the pedigree-driven credit decays with projected EVIDENCE, not the lens clock. k=0 (off=0) identical.
# Variants:  V1 = runway/elite age anchored only.  V2 = whole horizon age anchored (a_fa) + runway.
import os, io, contextlib
import numpy as np
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']
VAR = os.environ.get('PROJVAR', 'V1')
_W4CTX = g['_W4CTX']; _w4_W = g['_w4_W']; _proj0 = g['_proj_w4_0']
_BOARD = g.get('_BOARD_PATH', True)

def _proj_fix(gg, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0):
    ctx = _W4CTX['on']
    if ctx is None:
        return _proj0(gg, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc)
    off = MA.AGE_REF - MA.BASE_REF          # >0 forward lens; 0 at k=0/balanced/backward => identical
    a_fa = a - off if off > 0 else a        # form-anchored (now) age for the pedigree-driven credit
    pa = MA.PEAK_AGE[gg]; d = MA.LENS[lens]; cl = cur if cur else lp * MA.frac(a, pa); prod = 0.0
    if g0 is None: g0 = gg
    if fut is None: fut = [(gg, 1.0)]
    a_h = a_fa if VAR == 'V2' else a         # V2 anchors the horizon age-shape; V1 keeps it advancing
    for k in range(18):
        ag = a_h + k
        if ag > 38 or MA.frac(ag, pa) < 0.42: break
        lev = lp * MA.frac(ag, pa)
        if ag <= pa: lev = max(lev, cl)
        if k == 0: lev = max(lev, cl)
        if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026: lev *= (1 - pre_hc)
        if _BOARD and k == ctx.get('ret_k', -1) and ctx.get('ret_hc', 0.0) > 0: lev *= (1 - ctx['ret_hc'])
        base = lev + MA.capt_prem(lev)
        Wk = _w4_W(k, ctx)
        if k == 0: prod += Wk * MA.posval(base - MA.REPL[g0]) * 21 / ((1 + d) ** k)
        else: prod += Wk * sum(w * MA.posval(base - MA.REPL[gh]) for gh, w in fut) * 21 / ((1 + d) ** k)
    if gg in ('KEY_FWD', 'KEY_DEF'): prod *= 1.05
    runway = MA.clamp((25 - a_fa) / 6.0, 0, 1); elite = MA.clamp((lp / MA.PEAK[gg] - 0.97) / 0.30, 0, 1)
    prod *= (1 + runway * elite * MA.PMAX)
    return prod

MA.proj_from_peak = _proj_fix

def totals(label):
    Sv = SvP1 = 0.0; coh = defaultdict(lambda: [0, 0.0, 0.0])
    for p in players:
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear(); v = ev(p, 2026)
        MA._LENS_FORM = 2026; MA.BASE_REF = 2026; MA.AGE_REF = 2027; MA._pe_clear(); vP1 = ev(p, 2027)
        MA._LENS_FORM = None; MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
        Sv += v; SvP1 += vP1
        a = age(p); c = 'dev(<=23)' if (a or 99) <= 23 else 'mid(24-27)' if a <= 27 else 'vet(>=28)'
        coh[c][0] += 1; coh[c][1] += v; coh[c][2] += vP1
    print("[%s]  Sv=%.0f  SvP1=%.0f  (%+.1f%%)" % (label, Sv, SvP1, 100 * (SvP1 / Sv - 1)))
    for c in ('dev(<=23)', 'mid(24-27)', 'vet(>=28)'):
        n, now, fwd = coh[c]; print("   %-11s n=%3d  d=%+9.0f  %+6.1f%%" % (c, n, fwd - now, 100 * (fwd - now) / now))

totals("PROJ-" + VAR)
