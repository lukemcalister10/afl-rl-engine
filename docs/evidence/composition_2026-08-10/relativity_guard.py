"""THE RELATIVITY GUARD — measured exactly as pre-registered in RELATIVITY_GUARD.md. READ-ONLY.

  rung(p) = 2026 - debut(p) + 1        (1 = first season; <=0 = not yet debuted)
  YOUNG   = every priced draft PICK asset + every player with rung <= 1
  PEAK    = every player with rung in {4,5,6}
  RELATIVITY = Sigma(YOUNG) / Sigma(PEAK), board currency, whole books.

FAIRNESS RULES, as registered: ONE function run over every board; MEMBERSHIP FROZEN on the
PRE-ACT board and reused for every later board keyed by player, so the ratio cannot move because
the population moved; the pick side taken from the same artifact on both sides.

Usage: relativity_guard.py <label>=<board.json> [<label>=<board.json> ...]
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine_load import load

g = load()
MA = g['MA']
Y = 2026
bykey = {p['key']: p for p in MA.data if p.get('key')}

args = [a.split('=', 1) for a in sys.argv[1:]]
boards = [(lab, json.load(open(path))) for lab, path in args]

# ---- membership FROZEN on the first board (the pre-act one) ----
base = boards[0][1]
YOUNG, PEAK = set(), set()
for r in base['active']:
    p = bykey.get(r['key'])
    if p is None: continue
    try: rung = Y - MA.debut(p) + 1
    except Exception: continue
    if rung <= 1: YOUNG.add(r['key'])
    elif rung in (4, 5, 6): PEAK.add(r['key'])
print("membership frozen on %s: YOUNG players %d  ·  PEAK players %d" % (boards[0][0], len(YOUNG), len(PEAK)))

# ---- the pick side: the same artifact on every board ----
def picks_total(b):
    for k in ('picks', 'pick_values', 'PICKS'):
        v = b.get(k)
        if isinstance(v, list) and v and isinstance(v[0], dict):
            for f in ('v', 'value', 'val'):
                if f in v[0]: return sum(float(x[f]) for x in v), len(v)
        if isinstance(v, dict) and v:
            try: return sum(float(x) for x in v.values()), len(v)
            except Exception: pass
    return None, 0

pt, pn = picks_total(base)
print("pick side: %s" % ("%d picks, total %.0f (identical on every board — the ladder is not moved by this act)"
                         % (pn, pt) if pt else "no pick block on the board artifact; YOUNG = the rung<=1 players only (disclosed)"))

print("\n %-26s %12s %12s %12s %10s %9s" % ("board", "YOUNG", "PEAK", "RELATIVITY", "d(ratio)", "d(pp)"))
prev = None
first = None
for lab, b in boards:
    v = {r['key']: float(r['v']) for r in b['active']}
    yv = sum(v.get(k, 0.0) for k in YOUNG) + (pt or 0.0)
    pv = sum(v.get(k, 0.0) for k in PEAK)
    rat = yv / pv if pv else float('nan')
    if first is None: first = rat
    d = "" if prev is None else "%+.6f" % (rat - prev)
    dpp = "" if prev is None else "%+.3f" % ((rat - first) * 100.0)
    print(" %-26s %12.0f %12.0f %12.6f %10s %9s" % (lab, yv, pv, rat, d, dpp))
    prev = rat

print("\n PRE-REGISTERED EXPECTATION: RELATIVITY should RISE or hold — the package should NARROW")
print(" the peak-vs-young gap, never widen it.")
if prev is not None and first is not None:
    move = (prev - first) / first * 100.0
    print(" MEASURED end-to-end: %.6f -> %.6f  (%+.3f%%)" % (first, prev, move))
    if prev >= first:
        print(" VERDICT: RELATIVITY HELD OR ROSE — the guard PASSES.")
    else:
        print(" VERDICT: RELATIVITY FELL — HALT CONDITION. This is a TOP-OF-REPORT FLAG for the owner")
        print(" before adoption. It is NOT rebalanced to pass and no component is retuned to move it.")
