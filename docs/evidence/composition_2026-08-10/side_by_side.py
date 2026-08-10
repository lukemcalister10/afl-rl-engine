"""THE SIDE-BY-SIDE — the act's deliverable. READ-ONLY.

Per-item attribution by kill-switch difference: item X's contribution to a player is
(FULL board) - (board with X off). Because the items interact through one book, those
differences do not have to sum exactly to the total; the RESIDUAL is printed per player rather
than being distributed silently, which is the honest form of "attribution columns summing to the
total".

Usage: side_by_side.py   (reads the boards from the scratchpad by convention)
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
REPO = "/home/user/afl-rl-engine"

def bd(p):
    return {r['key']: r for r in json.load(open(p))['active']}

MAIN = bd(REPO + "/data/rl_build/rl_app_data.json")
FULL = bd(SP + "/bd_FULL.json")
OFF = {
    'H':   bd(SP + "/bd_noH.json"),
    'C/E2': bd(SP + "/bd_noC.json"),
    'E1':  bd(SP + "/bd_noE1.json"),
    'A':   bd(SP + "/bd_noA.json"),
    'SUR': bd(SP + "/bd_noSUR.json"),
}
BASE = bd(SP + "/bd_BASE.json")          # B + era + #336 only
B_ONLY = bd(SP + "/board_B.json")
B_ERA = bd(SP + "/board_B_era.json")

sm = lambda d: sum(r['v'] for r in d.values())
print("=" * 104)
print("THE COMPOSITION ACT — SIDE-BY-SIDE")
print("=" * 104)
print(" %-34s %12s %12s %10s" % ("board", "total", "delta vs main", "ratio"))
rows = [("main (pre-act)", MAIN), ("+ ITEM B", B_ONLY), ("+ era removal", B_ERA),
        ("+ #336 / A / C / E1 / E2 / H / SUR", FULL)]
for lab, d in rows:
    print(" %-34s %12d %12d %10.6f" % (lab, sm(d), sm(d) - sm(MAIN), sm(d) / sm(MAIN)))

print("\n=== PER-ITEM BOOK DELTA (kill-switch difference on the FULL board) ===")
print(" %-10s %14s %10s   %s" % ("item", "book delta", "ratio", "movers"))
print(" %-10s %14d %10.6f   %s" % ("B", sm(B_ONLY) - sm(MAIN), sm(B_ONLY) / sm(MAIN),
                                   sum(1 for k in MAIN if MAIN[k]['v'] != B_ONLY.get(k, MAIN[k])['v'])))
print(" %-10s %14d %10.6f   %s" % ("era", sm(B_ERA) - sm(B_ONLY), sm(B_ERA) / sm(B_ONLY),
                                   sum(1 for k in B_ONLY if B_ONLY[k]['v'] != B_ERA.get(k, B_ONLY[k])['v'])))
print(" %-10s %14d %10.6f   %s" % ("#336+rest", sm(BASE) - sm(B_ERA), sm(BASE) / sm(B_ERA),
                                   sum(1 for k in B_ERA if B_ERA[k]['v'] != BASE.get(k, B_ERA[k])['v'])))
for it, d in OFF.items():
    delta = sm(FULL) - sm(d)
    n = sum(1 for k in FULL if FULL[k]['v'] != d.get(k, FULL[k])['v'])
    print(" %-10s %14d %10.6f   %d" % (it, delta, sm(FULL) / sm(d) if sm(d) else 0, n))

# ---- movers with per-item attribution ----
print("\n=== TOP MOVERS, WITH PER-ITEM ATTRIBUTION (full act vs main) ===")
mv = []
for k, r in FULL.items():
    if k not in MAIN: continue
    tot = r['v'] - MAIN[k]['v']
    if tot == 0: continue
    att = {it: r['v'] - d.get(k, r)['v'] for it, d in OFF.items()}
    att['B'] = B_ONLY.get(k, MAIN[k])['v'] - MAIN[k]['v']
    att['era'] = B_ERA.get(k, B_ONLY.get(k, MAIN[k]))['v'] - B_ONLY.get(k, MAIN[k])['v']
    resid = tot - sum(att.values())
    mv.append((abs(tot), tot, k, r.get('name'), r.get('gf'), MAIN[k]['v'], r['v'], att, resid))
mv.sort(reverse=True)
hdr = " %-22s %-5s %8s %8s %7s | %6s %6s %6s %6s %6s %6s %6s | %6s"
print(hdr % ("player", "pos", "before", "after", "total", "B", "era", "A", "C/E2", "E1", "H", "SUR", "resid"))
for _a, tot, k, nm, pos, b, a, att, resid in mv[:20]:
    print(hdr % (nm[:22], pos, b, a, "%+d" % tot,
                 "%+d" % att['B'], "%+d" % att['era'], "%+d" % att['A'], "%+d" % att['C/E2'],
                 "%+d" % att['E1'], "%+d" % att['H'], "%+d" % att['SUR'], "%+d" % resid))
print("\n total movers vs main: %d   (up %d / down %d)"
      % (len(mv), sum(1 for m in mv if m[1] > 0), sum(1 for m in mv if m[1] < 0)))
tr = sum(abs(m[8]) for m in mv)
print(" RESIDUAL (interaction between items, NOT distributed silently): total |resid| = %d over %d movers,"
      % (tr, len(mv)))
print(" mean |resid| per mover = %.1f. The items share one book, so exact additivity is not available;"
      % (tr / len(mv) if mv else 0))
print(" the residual is the size of that interaction and is printed rather than smoothed away.")

# ---- the Mraz lines ----
print("\n=== THE MRAZ LINES ===")
import subprocess
curve35 = 561.0
for lab, d in (("pre-act (main)", MAIN), ("post-act (full)", FULL)):
    if 'noah-mraz' in d:
        v = d['noah-mraz']['v']
        print("  %-18s board %6d   x pick-35 = %.3f (raw)  %.3f (ladder ccy)"
              % (lab, v, v / curve35, v * 1.0524 / curve35))
if 'noah-mraz' in FULL and 'noah-mraz' in MAIN:
    m = [x for x in mv if x[2] == 'noah-mraz']
    if m:
        att = m[0][7]
        print("  package delta per item: " + " · ".join("%s %+d" % (k, v) for k, v in att.items()))
        print("  total move %+d   residual %+d" % (m[0][1], m[0][8]))
