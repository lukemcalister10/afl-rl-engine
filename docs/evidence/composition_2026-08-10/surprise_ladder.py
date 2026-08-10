"""SALVAGE 3 — THE SURPRISE DIAL LADDER + THE INTERACTION GUARDS. READ-ONLY.

The branch shipped RL_SUR_W=5.0, calibrated on the OLD currency and board. It is NOT shipped blind.
This re-calibrates on the CURRENT board against the owner's ruled tolerance — a 4-game player lands
~2-3x his pick — and prints:
  1. THE LADDER: RL_SUR_W in {0,1,2,3.5,5} vs Mraz's ratio to pick-35's ladder value;
  2. THE NEAR-PROJECTION NO-REBALANCE PROOF: rows within +/-25% of projection must not move
     materially (the ruled condition: no broad young hit, no rebalance);
  3. THE INTERACTION GUARDS with ITEM A, which shares this site:
       (a) a QUALIFYING row must be untouched by the surprise term (it never reaches sitout_ev);
       (b) a sub-bar NEAR-PROJECTION row must be untouched by BOTH.
Run once per dial value, in-process, by re-binding SUR_W in the engine's globals — the same
technique the ITEM A ablation used, and the reason the engine is exec'd rather than imported.
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']
ev = g['ev']; entry_anchor = g['entry_anchor']
Y = 2026
REPO = os.environ.get("RL_REPO", "/home/user/afl-rl-engine")
real = [p for p in MA.data if g['_isreal'](p)]
board = json.load(open(os.path.join(REPO, "data", "rl_build", "rl_app_data.json")))
BK = set(r['key'] for r in board['active'])
CURVE = g['_PVC0']; PL_F = g['_PL_F']
MRAZ = [p for p in real if p['key'] == 'noah-mraz'][0]
curve35 = float(CURVE[35])

DIALS = [0.0, 1.0, 2.0, 3.5, 5.0]

def set_dial(v):
    g['SUR_W'] = v

# the sit-out population is the only one the surprise term can reach
SIT = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) == 0
       and not p.get('_retired') and not g['delisted'](p)]
QUAL = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) >= 1
        and not p.get('_retired') and not g['delisted'](p)]
print("sit-out rows on the board (the term's whole reach): %d   qualifying rows: %d"
      % (len(SIT), len(QUAL)))

def price_all(rows):
    return {p['key']: float(ev(p, Y)) for p in rows}

set_dial(0.0)
BASE_SIT = price_all(SIT); BASE_QUAL = price_all(QUAL)
base_mraz = float(ev(MRAZ, Y))

# ---- the projection ratio: how far a thin record's production sits from its own anchor ----
def surprise_ratio(p):
    fe = g['_fEy'](Y, p)
    tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
    R = g['_R_surf'](g['_sitout_cls'](MA.gfut(p)), MA.effpk(p), tau)
    anch = R * float(entry_anchor(p))
    e = float(g['_prod_path'](p, Y))
    return (e / anch) if anch > 0 else float('nan')

NEAR = [p for p in SIT if 0.75 <= surprise_ratio(p) <= 1.25]
print("sit-out rows NEAR projection (production within +/-25%% of their own anchor leg): %d" % len(NEAR))

print("\n=== 1. THE DIAL LADDER — Mraz against his ruled ~2-3x tolerance ===")
print(" %-8s %10s %10s %10s   %s" % ("RL_SUR_W", "ev", "board", "x pick-35", "verdict"))
lad = []
for d in DIALS:
    set_dial(d)
    e = float(ev(MRAZ, Y)); b = e / PL_F
    r = b / curve35
    lad.append((d, e, b, r))
    v = "INSIDE 2-3x" if 2.0 <= r <= 3.0 else ("above 3x" if r > 3.0 else "below 2x")
    print(" %-8.1f %10.1f %10.1f %10.3f   %s" % (d, e, b, r, v))
inside = [d for d, _e, _b, r in lad if 2.0 <= r <= 3.0]
print("\n  SMALLEST rung landing him inside 2-3x: %s"
      % ("%.1f" % min(inside) if inside else "NONE ON THIS LADDER — halt and report"))

print("\n=== 2. THE NEAR-PROJECTION NO-REBALANCE PROOF ===")
print("  the ruled condition: rows performing near their projection must NOT move materially.")
print(" %-8s %8s %10s %10s %10s" % ("RL_SUR_W", "n near", "max |d%|", "mean |d%|", "n > 2%"))
for d in DIALS:
    set_dial(d)
    ds = []
    for p in NEAR:
        b0 = BASE_SIT[p['key']]
        if b0 <= 0: continue
        ds.append(abs(float(ev(p, Y)) - b0) / b0 * 100.0)
    if not ds: print(" %-8.1f    (none)" % d); continue
    print(" %-8.1f %8d %10.2f %10.2f %10d" % (d, len(ds), max(ds), float(np.mean(ds)),
                                              sum(1 for x in ds if x > 2.0)))

print("\n=== 3. INTERACTION GUARDS WITH ITEM A (they share the sit-out/anchor site) ===")
set_dial(5.0)
moved = [k for k, v in price_all(QUAL).items() if v != BASE_QUAL[k]]
print("  (a) QUALIFYING rows (ns>=1, ITEM A's population) moved by the surprise dial: %d of %d"
      % (len(moved), len(QUAL)))
print("      expected 0 — a qualifying row returns before sitout_ev, so the surprise term")
print("      cannot reach it. ITEM A and the surprise law therefore never both act on one row.")
if moved: print("      ** NOT ZERO — double-shrink risk, names:", moved[:6])
nm = []
for p in NEAR:
    b0 = BASE_SIT[p['key']]
    if b0 <= 0: continue
    if abs(float(ev(p, Y)) - b0) / b0 > 0.02: nm.append(p.get('player'))
print("  (b) sub-bar NEAR-PROJECTION rows moving >2%% at the maximum dial: %d of %d %s"
      % (len(nm), len(NEAR), ("names: " + ", ".join(nm[:6])) if nm else "— untouched by both, as ruled"))
set_dial(0.0)
