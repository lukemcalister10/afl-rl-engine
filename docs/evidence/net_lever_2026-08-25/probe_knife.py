#!/usr/bin/env python3
"""Knife-edge reconciliation probe (PREREG_ORDER45 §4 declared class): for the three partial-lambda
rows, print the raw ev-scale arithmetic — V, CF, lambda, the lever's add-then-round W, the
single-rounded board prediction, and the double-rounded board value — from the PRE-LEVER inner
engine (RL_O45 declared '0' via the manifest is NOT needed: we recompute both paths from V/CF).
Read-only. Run in wsF/rl_after with the usual gate bindings AFTER restoring manifest RL_O45='1'."""
import contextlib, io, json, os, sys
os.environ.setdefault('RL_CONFIG_MODE', 'gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']
F = float(json.load(open(os.path.join(os.environ['RL_REPO'], 'engine/rl_after/pick_redenomination.json')))['factor'])
bars = {k: (float(v) - 3.0) for k, v in MA.REPL.items()}
def lam(c, pos):
    s = bars[pos] / bars['MID']
    lo, hi = 40.0 * s, 45.0 * s
    if c <= lo: return 0.0
    if c >= hi: return 1.0
    t = (c - lo) / (hi - lo)
    return 3 * t * t - 2 * t * t * t
# NOTE: ev here is the WRAPPED symbol (O45 live). The wrapped value for a lifted row IS W; the
# inner V is recovered by stripping the row from scope via its own kill condition — instead we
# recompute V and CF directly: V = the wrapper's inner is not exported, so probe via the same
# counterfactual trick the lever itself uses is not available here. We therefore read V from the
# KILL-SWITCH-OFF board file (ev-scale is not in it) — so instead: recompute from the wrapped ev
# by inverting the lever on rows we know are lifted is fragile. CLEAN PATH: the off-board carries
# round(V/F); the on-board carries round(W/F); we get V,CF exactly by re-running the lever's own
# arithmetic pieces below from the engine's own numbers via a temporary scope exclusion.
for key in ('cooper-simpson', 'wil-parker', 'taylor-goad'):
    p = next(x for x in MA.data if x.get('key') == key)
    sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= 2026]
    g_tot = sum(x.get('games', 0) for x in sc)
    c = sum(x['avg'] * x['games'] for x in sc) / g_tot
    pos = MA.gfut(p)
    L = lam(c, pos)
    with contextlib.redirect_stdout(io.StringIO()):
        W = ev(p, 2026)                      # wrapped: the lever's output
        s0 = p['scoring']; p['scoring'] = []
        try:
            CF = ev(p, 2026)                 # stripped row: 0 games => wrapper inert => inner CF
        finally:
            p['scoring'] = s0
        # inner V: exclude the row from scope by lambda: temporarily null its _by? NO mutation games.
        # V = invert: W = round(V + L*(CF-V)) is not invertible exactly; get V from the wrapper-off
        # identity instead: the off-board value round(V/F) is known (86); print all pieces we have.
    x_single = None
    print('%s: pos=%s c=%.2f lambda=%.6f  CF(ev-scale)=%r  W(ev-scale, wrapped ev)=%r  F=%s' % (key, pos, c, L, CF, W, F))
    print('   board double-round = round(W/F) = %d' % round(W / F))
    # V candidates: integers v with round(v/F) == off-board value; enumerate the consistent ones
    off = {'cooper-simpson': 86, 'wil-parker': 36, 'taylor-goad': 441}[key]
    cands = [v for v in range(int((off - 1) * F), int((off + 2) * F) + 1) if round(v / F) == off]
    fits = [v for v in cands if round(v + L * (CF - v)) == W]
    print('   ev-scale V candidates consistent with off-board %d AND lever W: %s' % (off, fits))
    for v in fits:
        x = v + L * (CF - v)
        print('   V=%d: X=V+L*(CF-V)=%.4f -> lever W=round(X)=%d -> board %d ; single-round path round(X/F)=%d'
              % (v, x, round(x), round(round(x) / F), round(x / F)))
