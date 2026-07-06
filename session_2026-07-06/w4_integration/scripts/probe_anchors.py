"""W4 calibration probe: load the candidate engine once, print owner anchors before/after context + diagnostics.
Run from /home/claude/rl_workspace/rl_after with the pinned env. Levers via env (default all ON)."""
import io, contextlib, os, sys, json
import numpy as np

g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']; cp = g['cp']; PR = g['PR']
_nqual = g['_nqual']; _lvlcurr = g['_lvlcurr']

def find(nm):
    c = [p for p in MA.data if nm.lower() == p['player'].lower() and MA.GRP.get(p.get('pos'))]
    if not c:
        c = [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None

BAKED = json.load(open('/home/user/afl-rl-engine/session_2026-07-06/w4_integration/out/baked_control.json'))  # v2.5 baked board (CONTROL)
names = list(BAKED.keys())
print(f"{'player':22s}{'pos':8s}{'age':>4s}{'nq':>3s}{'lcr':>7s}{'baked':>7s}{'now':>7s}{'d%':>7s}")
out = {}
for nm in names:
    p = find(nm)
    if p is None:
        print(f"{nm:22s} NOT FOUND"); continue
    with contextlib.redirect_stdout(io.StringIO()):
        v = ev(p)
    pos = MA.gfut(p); a = cp._age_asof(p, 2026); n = _nqual(p, 2026)
    lcr = _lvlcurr(p, 2026) - MA.REPL.get(pos, 0.0)
    b = BAKED[nm]
    d = f"{100*(v-b)/b:+.1f}%" if b else "  ?"
    out[nm] = v
    print(f"{p['player'][:22]:22s}{pos:8s}{a:4.0f}{n:3d}{lcr:7.1f}{str(b) if b else '—':>7s}{v:7d}{d:>7s}")
json.dump(out, open(os.environ.get('PROBE_OUT', '/tmp/probe_anchors.json'), 'w'), indent=1)
# targets
bo = out.get('Marcus Bontempelli'); ga = out.get('Max Gawn'); br = out.get('Kieren Briggs'); ca = out.get('Jeremy Cameron')
print()
if bo: print(f"TARGET Bont >= 3392 (+10%): {bo} {'OK' if bo>=3392 else 'MISS'}")
if ga and br: print(f"TARGET Gawn clearly above Briggs: {ga} vs {br} ({100*(ga-br)/br:+.1f}%) {'OK' if ga>1.05*br else 'MISS'}")
if ca: print(f"TARGET Cameron up: {ca} vs 1143 ({100*(ca-1143)/1143:+.1f}%) {'OK' if ca>1143 else 'MISS'}")
