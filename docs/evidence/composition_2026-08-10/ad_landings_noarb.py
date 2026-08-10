"""LANDINGS + NO-ARB, per age-discount variant. READ-ONLY.

  LANDINGS: the year-1 landing = mean(board price / entry_anchor) over the ruled cohort
  (ND in-curve, class 2025), played-only and all-rows. Ruled band [1.04, 1.13].

  NO-ARB (the yr1-to-peak frame): a changed discount structure changes the shape of the price
  path across career years. The arbitrage to look for is a rung whose EXPECTED appreciation to
  the next rung exceeds the discount rate the engine itself charges — if a player predictably
  appreciates faster than the discount, holding him is a free lunch. Measured cross-sectionally
  as the median board price per rung and the implied rung-to-rung appreciation.
"""
import os, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from engine_load import load

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
REPO = "/home/user/afl-rl-engine"
g = load(); MA = g['MA']; Y = 2026
entry_anchor = g['entry_anchor']
real = [p for p in MA.data if g['_isreal'](p)]
byk = {p['key']: p for p in real}
bd = lambda p: {r['key']: r for r in json.load(open(p))['active']}

COH = [p for p in real if p.get('type') == 'ND' and not MA.is_pool(p) and p.get('year') == 2025]
ANCH = {p['key']: float(entry_anchor(p)) for p in COH}
PLAYED = set(p['key'] for p in COH if sum(s['games'] for s in p['scoring']) > 0)
print("year-1 cohort (ND in-curve, class 2025): n=%d  played=%d  sitters=%d"
      % (len(COH), len(PLAYED), len(COH) - len(PLAYED)))

VARIANTS = [
    ("main (pre-act)",        REPO + "/data/rl_build/rl_app_data.json"),
    ("FULL (no AD)",          SP + "/bd_FULL.json"),
    ("V1 AD 13/15 (ordered)", SP + "/bd_FULL_AD.json"),
    ("V1 AD 12/16",           SP + "/bd_AD_12_16.json"),
    ("V2 four-band",          SP + "/bd_V2.json"),
    ("V3 corrected",          SP + "/bd_V3.json"),
    ("menu a: blend 30",      SP + "/bd_blend30.json"),
    ("menu a: blend 20",      SP + "/bd_blend20.json"),
    ("menu b: tail trim .35", SP + "/bd_tail35.json"),
    ("menu b: tail trim .65", SP + "/bd_tail65.json"),
]

print("\n=== THE TWO LANDINGS  (ruled band [1.04, 1.13]) ===")
print(" %-22s %14s %14s" % ("variant", "played-only", "all-rows"))
for lab, path in VARIANTS:
    if not os.path.exists(path): print(" %-22s (absent)" % lab); continue
    d = bd(path)
    po, ar = [], []
    for p in COH:
        k = p['key']
        if k not in d or ANCH.get(k, 0) <= 0: continue
        r = d[k]['v'] / ANCH[k]
        ar.append(r)
        if k in PLAYED: po.append(r)
    fp = float(np.mean(po)) if po else float('nan')
    fa = float(np.mean(ar)) if ar else float('nan')
    flag = "" if 1.04 <= fp <= 1.13 else "   <-- played-only OUTSIDE [1.04,1.13]"
    print(" %-22s %14.4f %14.4f%s" % (lab, fp, fa, flag))
print("  NOTE: if the played-only landing leaves the band, H may need re-reading from its ladder.")
print("  REPORTED, NOT RETUNED — the sizing word is the owner's.")

print("\n=== NO-ARB: THE YEAR-1-TO-PEAK TRAJECTORY ===")
print("  median board price by career rung, and the implied rung-to-rung appreciation.")
print("  An arbitrage opens if appreciation predictably EXCEEDS the discount rate charged")
print("  (holding a player would then be a free lunch). Discount band here: 12.0%-16.0%/yr.")
rung = {}
for p in real:
    try: r = Y - MA.debut(p) + 1
    except Exception: continue
    if 1 <= r <= 8: rung.setdefault(r, []).append(p['key'])
for lab, path in VARIANTS:
    if not os.path.exists(path): continue
    d = bd(path)
    med = {}
    for r, ks in sorted(rung.items()):
        v = [d[k]['v'] for k in ks if k in d and d[k]['v'] > 0]
        if v: med[r] = float(np.median(v))
    line = " %-22s " % lab
    worst = 0.0
    for r in sorted(med):
        if r + 1 in med and med[r] > 0:
            app = med[r + 1] / med[r] - 1.0
            worst = max(worst, app)
            line += "v%d->%d %+6.1f%%  " % (r, r + 1, 100 * app)
    print(line)
    print("   %-20s worst rung-to-rung appreciation %+.1f%%  %s"
          % ("", 100 * worst,
             "NO NEW ARBITRAGE (below the discount charged)" if worst < 0.12 else
             "** EXCEEDS the low end of the discount band — inspect"))
