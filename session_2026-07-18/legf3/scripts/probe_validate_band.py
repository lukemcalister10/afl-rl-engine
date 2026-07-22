#!/usr/bin/env python3
# LEG F3 — VALIDATE the band-level pedigree carry (READ-ONLY monkeypatch; nothing written to engine files).
# The dominant forward drop is pr=price6(b6); b6=cp.cond_prior_band + q97m(cp._feat), which de-pedigree on the
# AGE clock. Hypothesis: in the forward lens, hold the band's pedigree at the FORM ANCHOR (BASE_REF), carrying
# it forward and decaying only with projected evidence. Two variants measured:
#   FULL   : band computed fully at BASE_REF (upper bound of the pedigree carry; no age-growth in the band).
#   DECAY  : band = fwd + phi(games)*max(0, now_anchored - fwd); phi=(1-g/46)^2 (evidence-decayed carry, Reid).
import os, io, contextlib
import numpy as np
from collections import defaultdict
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; G = MA.__dict__
players = G['players']; age = G['age']; cp = g['cp']
MODE = os.environ.get('BANDMODE', 'FULL')
G0 = 46.0

def _games(p, Y):
    d0 = cp.debutyr(p) - 1
    return float(sum(x.get('games', 0) for x in p['scoring'] if d0 < x['year'] <= Y))

_cpb0 = cp.cond_prior_band; _feat0 = cp._feat
def _anchor(fn, *a):
    sv = MA.AGE_REF
    if getattr(MA, '_LENS_FORM', None) is not None and MA.AGE_REF != MA.BASE_REF:
        MA.AGE_REF = MA.BASE_REF
    try:
        return fn(*a)
    finally:
        MA.AGE_REF = sv

if MODE == 'FULL':
    cp.cond_prior_band = lambda p, cm, Y=2026: _anchor(_cpb0, p, cm, Y)
    cp._feat = lambda p, Y=2026: _anchor(_feat0, p, Y)
else:  # DECAY
    def _cpb_decay(p, cm, Y=2026):
        fwd = np.asarray(_cpb0(p, cm, Y))
        if getattr(MA, '_LENS_FORM', None) is None or MA.AGE_REF == MA.BASE_REF:
            return fwd
        now = np.asarray(_anchor(_cpb0, p, cm, Y))
        phi = max(0.0, (1.0 - _games(p, MA.BASE_REF) / G0)) ** 2
        return fwd + phi * np.maximum(0.0, now - fwd)
    cp.cond_prior_band = _cpb_decay
    def _feat_decay(p, Y=2026):
        return _feat0(p, Y)  # q97 ceiling left as-is in DECAY (band carry dominates)
    cp._feat = _feat_decay

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
    print("[%s]  Sv=%.0f  SvP1=%.0f  (%+.1f%%)" % (label, Sv, SvP1, 100 * (SvP1 / Sv - 1)))
    for c in ('dev(<=23)', 'mid(24-27)', 'vet(>=28)'):
        n, now, fwd = coh[c]; print("   %-11s n=%3d  d=%+9.0f  %+6.1f%%" % (c, n, fwd - now, 100 * (fwd - now) / now))

totals("BAND-CARRY " + MODE)
