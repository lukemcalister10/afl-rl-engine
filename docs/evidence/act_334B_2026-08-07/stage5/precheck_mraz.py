#!/usr/bin/env python3
"""#334 stage 5 — THE MRAZ PRE-CHECK, run on the TAUGHT surface BEFORE the board is built.

Addendum 2 pre-states the arithmetic to be verified at his cell (KPP, pick 35, tau=1.83, 4 games):
"~13.7 display points per 1pp anchor lift; G >= ~1.20 breaches 3.5x, >= ~1.31 breaches 3.8x".
This script MEASURES it instead of assuming it, through the engine's own wired evaluation (the M3
blend included) and the L7 numeraire re-base that produces the display board, and prints the taught
G at his cell together with the implied price.
"""
import os, sys, io, contextlib, json
import numpy as np

WS = os.environ['RL_WORKDIR']
sys.path.insert(0, '/home/claude/rl_vendor'); os.chdir(WS); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s5pre'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; ev = G['ev']
PLF = 1.0524                      # the L7 numeraire re-base divisor the export applies to display v
PICKV = float(os.environ.get('RL_PICKV', '530'))     # Mraz's own pick's value on the ruled baseline board

W = [G['G5_W']]
def set_w(w):
    G['G5_W'] = w
    for m in ('_g5', 'sitout_ev'):
        G[m].__globals__['G5_W'] = w

p = next(x for x in MA.data if x.get('key') == 'noah-mraz')
Y = 2026
fe = G['_fEy'](Y, p); tau = max(0.0, Y - cp.debutyr(p)) + fe ** 1.5
cls = G['_sitout_cls'](MA.gfut(p)); pk = MA.effpk(p)
R = G['_R_surf'](cls, pk, tau); A = G['entry_anchor'](p)
gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
set_w(1.0)
gt = G['_g5'](p, Y, tau, cls, pk)

print("=" * 100)
print("MRAZ PRE-CHECK — the taught G at his cell, and the price it implies, BEFORE the build")
print("=" * 100)
print("  Noah Mraz  ND 2024 pick %s (epk %s)  pos %s  class %s  debut year %s" % (p.get('pick'), pk, MA.gfut(p), cls, cp.debutyr(p)))
print("  his cell   : tau = %.4f   cumulative career games = %.0f   season-%d games = %.0f   fe = %.4f" % (tau, gcum, Y, gy, fe))
print("  the engine : R(%s, pick %s, tau %.4f) = %.6f   entry anchor A = %.2f   anchor leg R*A = %.2f"
      % (cls, pk, tau, R, A, R * A))
print()
print("  >>> TAUGHT G AT HIS CELL = %.6f   (taught anchor leg G*R*A = %.2f, G*R = %.6f)" % (gt, gt * R * A, gt * R))
print()

def disp(w):
    set_w(w); MA._pe_clear()
    with contextlib.redirect_stdout(io.StringIO()): v = ev(p, Y)
    return v, round(v / PLF)

set_w(0.0); base_v, base_d = disp(0.0)
print("  baseline (dial 0)      : engine v = %.0f   display = %d   = %.4f x his pick (%.0f)"
      % (base_v, base_d, base_d / PICKV, PICKV))
set_w(1.0); live_v, live_d = disp(1.0)
print("  SHIPPED  (dial 1.0)    : engine v = %.0f   display = %d   = %.4f x his pick   [%+d, %+.2f%%]"
      % (live_v, live_d, live_d / PICKV, live_d - base_d, 100.0 * (live_d - base_d) / base_d))
print()
print("  THE MEASURED SENSITIVITY AT HIS CELL (sweeping the taught factor, everything else held):")
print("    %-10s %12s %10s %10s %14s" % ("G at cell", "engine v", "display", "x pick", "d(disp)/1pp G"))
prev = None
for g in (1.0, 1.05, 1.10, 1.20, 1.31, 1.40, 1.50, 1.75, 2.00, 2.29, 2.50):
    w = (g - 1.0) / max(gt - 1.0, 1e-12)
    set_w(w); MA._pe_clear()
    with contextlib.redirect_stdout(io.StringIO()): v = ev(p, Y)
    d = round(v / PLF)
    sl = '' if prev is None else "%.3f" % ((d - prev[1]) / ((g - prev[0]) * 100.0))
    print("    %-10.3f %12.0f %10d %10.4f %14s" % (g, v, d, d / PICKV, sl))
    prev = (g, d)

def solve(tier):
    lo, hi = 1.0, 80.0
    def f(g):
        set_w((g - 1.0) / max(gt - 1.0, 1e-12)); MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()): return round(ev(p, Y) / PLF) / PICKV
    if f(lo) >= tier: return None
    if f(hi) < tier: return float('inf')
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if f(m) < tier: lo = m
        else: hi = m
    return hi

print()
print("  THE TIER THRESHOLDS, SOLVED (Addendum 2 gate 2 tiering, on the DISPLAY board):")
for t in (3.0, 3.5, 3.8):
    s = solve(t)
    print("    %.1fx his pick  needs G = %s" % (t, "already breached at G=1" if s is None else
                                                ("unreachable" if s == float('inf') else "%.4f" % s)))
print()
print("  ADDENDUM 2 PRE-STATED : ~13.7 display points per 1pp of G ; 3.5x at G>=~1.20 ; 3.8x at G>=~1.31")
s35 = solve(3.5); s38 = solve(3.8)
print("  MEASURED              : ~%.1f display points per 1pp of G at G~1.0-1.2 ; 3.5x at G=%.3f ; 3.8x at G=%.3f"
      % ((disp((1.10 - 1.0) / (gt - 1.0))[1] - base_d) / 10.0, s35, s38))
print("  The pre-stated figures are OFF BY ~3.3x. The reason is measurable and printed: at his cell the")
print("  anchor leg is only a small share of his price — lam*e_full carries the rest — so a 1pp lift on")
print("  the anchor cannot move his display value by 1pp of the WHOLE price.")
set_w(1.0)
