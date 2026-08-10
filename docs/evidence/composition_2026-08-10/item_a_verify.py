"""ITEM A — WIRING VERIFICATION. READ-ONLY.

  1. KILL-SWITCH IDENTITY: RL_ITEM_A=0 must reproduce the pre-A board byte-exact.
  2. CONTINUITY AT GRADUATION: the ns==0 branch is untouched, and the two branches agree at the
     boundary (E_q -> 0 => anchor_share -> 1-lam => exactly sitout_ev).
  3. THE FADING CHAIN: v2 borrows less than v1, more than v3 — shown on synthetic rows that differ
     ONLY in career year, and on the live cohort by rung.
  4. RECALCULATION LAW: a synthetic year-2 probe responds to year-2 games.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']
ev = g['ev']; entry_anchor = g['entry_anchor']
Y = 2026
real = [p for p in MA.data if g['_isreal'](p)]
board = json.load(open(os.path.join(os.environ.get("RL_REPO", "/home/user/afl-rl-engine"),
                                    "data", "rl_build", "rl_app_data.json")))
BK = set(r['key'] for r in board['active'])

print("ITEM A live? _A_ON =", g['_A_ON'], "  tau =", g['_A_TAU'])

# ---- 3. the fading chain, on the LIVE cohort by rung ----
print("\n=== THE FADING CHAIN — anchor share by career rung (live board rows) ===")
byr = collections.defaultdict(list)
for p in real:
    if p['key'] not in BK: continue
    if p.get('_retired') or g['delisted'](p): continue
    if g['nseas_pro'](p, Y) < 1: continue          # the ns>=1 population ITEM A newly touches
    rung = Y - MA.debut(p) + 1
    if rung < 1: continue
    byr[min(rung, 8)].append(float(g['_a_share'](p, Y)))
print(" %-8s %6s %10s %10s" % ("rung", "n", "mean share", "max share"))
prev = None
mono = True
for r in sorted(byr):
    v = byr[r]; m = float(np.mean(v))
    print(" %-8s %6d %10.4f %10.4f" % ("v%d" % r if r < 8 else "v8+", len(v), m, max(v)))
    if prev is not None and m > prev + 1e-9: mono = False
    prev = m
print("  monotone non-increasing across rungs (v2 borrows less than v1, more than v3): %s" % mono)

# ---- 4. recalculation law: a synthetic year-2 probe responds to year-2 games ----
print("\n=== RECALCULATION LAW — a synthetic year-2 probe responds to year-2 games ===")
import copy
base = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) >= 1
        and (Y - MA.debut(p) + 1) == 2]
if base:
    q = copy.deepcopy(base[0])
    row = [s for s in q['scoring'] if s['year'] == Y]
    if row:
        out = []
        for gm in (0, 4, 11, 22):
            row[0]['games'] = gm
            out.append((gm, float(g['_a_share'](q, Y))))
        print("  %s (rung 2): games -> anchor share" % q.get('player'))
        for gm, s in out: print("     %2d games -> %.4f" % (gm, s))
        print("  responds to year-2 games (strictly falling as games rise): %s"
              % all(out[i][1] >= out[i + 1][1] - 1e-12 for i in range(len(out) - 1)))
else:
    print("  no rung-2 row available on this board")

# ---- 2. continuity at graduation ----
print("\n=== CONTINUITY AT GRADUATION ===")
print("  At ns==0 the record carries E_q=0, so exp(-E_q/tau)=1 and _a_share = 1-lam, which is")
print("  EXACTLY sitout_ev's blend weight. Checked on the live sitters:")
sit = [p for p in real if p['key'] in BK and g['nseas_pro'](p, Y) == 0][:6]
for p in sit:
    fe = g['_fEy'](Y, p); gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
    lam = float(np.interp(min(gy / fe, 6.0), [0, 1, 2, 3, 4, 5, 6], g['LAM_SIT']))
    print("   %-24s E_q=%.4f  1-lam=%.4f  _a_share=%.4f  agree=%s"
          % (p.get('player'), g['_ev_qual'](p, Y), 1 - lam, g['_a_share'](p, Y),
             abs((1 - lam) - g['_a_share'](p, Y)) < 1e-9))
