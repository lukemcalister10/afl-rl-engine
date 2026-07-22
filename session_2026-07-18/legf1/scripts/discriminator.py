#!/usr/bin/env python3
# LEG F1 DISCRIMINATOR (supervisor item 347, before any phantom work).
# Question: is the board-md5 gap vs the filed hashes ULP-scale *weather* (zero rank moves, integer v
# untouched) or a real defect? The filed 06d8af60/d85901af BYTES are not in-repo (they are the very
# artifacts that do not reproduce here), so the filed reference is the repo's frozen panel gate — 10
# pinned `v` values (numeraire, round(ev/1.0524)) cross-checked against the shipped board — plus the
# board-wide integer-v stability of THIS container's balanced build.
# HARD HALT if: any panel `v` != filed pin (a real value move), or any panel rank inversion.
import io, contextlib, os, json
WS = '/home/claude/rl_ws_legf/rl_after'
os.chdir(WS)
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']; ev = g['ev']
_F = 1.0524
def find(nm):
    c = [p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
# The frozen filed panel (run_panel.sh, LEG D ACT-2 RE-PIN; == shipped board v, cross-checked).
PANEL = [('Nick Daicos',8017),('Marcus Bontempelli',3897),('Harry Sheezel',7964),('Max Gawn',3416),
         ('Harley Reid',3348),('Josh Ward',2003),('Darcy Moore',257),('Taylor Goad',914),
         ('Josh Smillie',1324),('Will Green',651)]
rows = []; ok = True
for nm, exp in PANEL:
    p = find(nm); v = int(round(ev(p)/_F)) if p else None
    d = (v-exp) if v is not None else None
    ok = ok and (v == exp)
    rows.append((nm, v, exp, d))
# rank check among the panel (filed order vs mine)
filed_order = [nm for nm,_ in sorted(PANEL, key=lambda x:-x[1])]
mine_order  = [nm for nm,v,_,_ in sorted(rows, key=lambda r:-(r[1] if r[1] is not None else -1))]
rank_ok = filed_order == mine_order

print("LEG F1 DISCRIMINATOR — filed panel (10 pinned v) vs this container")
print("%-22s %8s %8s %6s" % ('player','mine_v','filed','delta'))
for nm, v, exp, d in rows:
    flag = '' if d == 0 else '   <-- MOVE'
    print("  %-20s %8s %8d %6s%s" % (nm[:20], v, exp, d, flag))
maxabs = max(abs(d) for _,_,_,d in rows if d is not None)
print()
print("max |delta_v| on filed anchors : %d   (expect 0 — integer v is BLAS-weather-immune here)" % maxabs)
print("changed anchor rows            : %d / %d" % (sum(1 for _,_,_,d in rows if d), len(rows)))
print("panel rank order preserved     : %s (filed==mine)" % rank_ok)
print("VERDICT:", "PASS — 0 value moves, 0 rank moves => gap is 6dp-float weather, not a defect"
      if (ok and rank_ok) else "HARD HALT — a filed value or rank moved (defect, not weather)")
import sys; sys.exit(0 if (ok and rank_ok) else 3)
