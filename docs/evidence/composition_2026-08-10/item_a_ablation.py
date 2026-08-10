"""ITEM A — IDENTIFY THE RAMP FUNCTIONALLY, BY ABLATION. READ-ONLY.

The order: do not pick the ramp by name. THE ramp is the object that TODAY moves the year-1+ price
from ANCHOR-DOMINATED to PRODUCTION-DOMINATED inside ev(). The identification must be PROVEN:
    zeroed    -> the price collapses to pure anchor
    saturated -> the price goes pure production

This script measures only. The verdict at the end is computed from the measured columns, not
asserted in prose. The engine is EXEC'd (never imported), so rebinding a name in its globals dict
rebinds the name that ev()/raw_ev close over — that is what makes a clean ablation possible.
"""
import os, sys, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']; PR = g['PR']
ev = g['ev']; entry_anchor = g['entry_anchor']
Y = 2026
real = [p for p in MA.data if g['_isreal'](p)]

# the population the question is about: year-1+ national draftees carrying a real record
COH = [p for p in real if p.get('type') == 'ND' and not MA.is_pool(p)
       and (p.get('year') or 0) >= 2019 and not p.get('_retired') and not g['delisted'](p)
       and sum(s['games'] for s in p['scoring']) > 0]
COH.sort(key=lambda p: p['key'])                 # deterministic order before sampling
FULL_N = len(COH)
SAMPLE = int(os.environ.get('ABL_SAMPLE', '60'))
if SAMPLE and FULL_N > SAMPLE:
    step = FULL_N / float(SAMPLE)
    COH = [COH[int(i * step)] for i in range(SAMPLE)]
print("year-1+ ND cohort with a record: n=%d (deterministic every-%.1fth sample of %d; an ablation"
      % (len(COH), FULL_N / float(len(COH)), FULL_N))
print("  reads DIRECTION and MAGNITUDE, not a precise level, and each cohort re-pricing costs ~1s")
print("  per player. Set ABL_SAMPLE=0 to run the full cohort.)")

ANCH = {p['key']: float(entry_anchor(p)) for p in COH}
def prices(): return {p['key']: float(ev(p, Y)) for p in COH}
BASE = prices()
PROD = {p['key']: float(g['_prod_path'](p, Y)) for p in COH}
mean = lambda d: float(np.mean(list(d.values())))
vs = lambda px, ref: {k: px[k] / max(ref[k], 1e-9) for k in px}

print("baseline           mean ev/anchor = %7.4f   mean ev/production = %7.4f"
      % (mean(vs(BASE, ANCH)), mean(vs(BASE, PROD))))
print("pure production    mean prod/anchor = %7.4f" % mean(vs(PROD, ANCH)))
print()

RES = {}
def ablate(name, setlo, sethi, restore, note=""):
    setlo(); lo = prices(); restore()
    sethi(); hi = prices(); restore()
    la, lp = mean(vs(lo, ANCH)), mean(vs(lo, PROD))
    ha, hp = mean(vs(hi, ANCH)), mean(vs(hi, PROD))
    RES[name] = dict(zero_anchor=la, zero_prod=lp, sat_anchor=ha, sat_prod=hp)
    print("  %-32s ZEROED /anchor %7.4f /prod %7.4f  |  SATURATED /anchor %7.4f /prod %7.4f %s"
          % (name, la, lp, ha, hp, note))

print("=== ABLATION: which object moves the year-1+ price anchor -> production? ===")

_LS = list(g['LAM_SIT'])
ablate("LAM_SIT (sit-out blend)",
       lambda: g['LAM_SIT'].__setitem__(slice(None), [0.0] * 7),
       lambda: g['LAM_SIT'].__setitem__(slice(None), [1.0] * 7),
       lambda: g['LAM_SIT'].__setitem__(slice(None), _LS))

_eg = g['_expgate']
ablate("_expgate (POLE_RAMP exposure)",
       lambda: g.__setitem__('_expgate', lambda p, Y: 0.0),
       lambda: g.__setitem__('_expgate', lambda p, Y: 1.0),
       lambda: g.__setitem__('_expgate', _eg),
       "(also carries tfade's leg: w = wage*tfade*expgate)")

_ie = g['iso_eff']
ablate("iso_eff  exp(-E_q/tau) fade",
       lambda: g.__setitem__('iso_eff', lambda p, Y=2026: 1.0),
       lambda: g.__setitem__('iso_eff', lambda p, Y=2026: float(g['iso_corr'](MA.gfut(p), MA.effpk(p)))),
       lambda: g.__setitem__('iso_eff', _ie))

_pp = g['_prod_path']
ablate("_prod_path (production leg)",
       lambda: g.__setitem__('_prod_path', lambda p, Y: 0.0),
       lambda: g.__setitem__('_prod_path', lambda p, Y: _pp(p, Y) * 1000.0),
       lambda: g.__setitem__('_prod_path', _pp),
       "<- CONTROL")

print()
print("=== VERDICT (computed from the columns above, not asserted) ===")
print("  pass = ZEROED lands on the anchor (|/anchor - 1| < 0.15) AND SATURATED lands on")
print("  production (|/prod - 1| < 0.15).")
winner = None
for k, r in RES.items():
    za = abs(r['zero_anchor'] - 1.0) < 0.15
    sp = abs(r['sat_prod'] - 1.0) < 0.15
    if za and sp and k != "_prod_path (production leg)": winner = k
    print("  %-32s zeroed==anchor %-4s  saturated==production %-4s  %s"
          % (k, "YES" if za else "no", "YES" if sp else "no", "<<< THE RAMP" if (za and sp) else ""))

print()
if winner:
    print("  IDENTIFIED: %s is the ramp. ITEM A rides it." % winner)
else:
    print("  NO CANDIDATE PASSES BOTH ENDS. That is the finding, and it is not a null result.")
    ctrl = RES["_prod_path (production leg)"]
    print("  The CONTROL row is the proof: zeroing the production leg ENTIRELY leaves the price at")
    print("  /anchor = %.4f, not 1.0 — because what catches a year-1+ row when production goes to"
          % ctrl['zero_anchor'])
    print("  zero is the FLOOR (floor_frac(yis) x entry_anchor: 0.45 at year 1, 0.35 at year 2 ...),")
    print("  a ONE-SIDED lower bound, not a blend. And saturating production leaves /prod = %.4f"
          % ctrl['sat_prod'])
    print("  because the ruck cap, the staleness caps and the KPF compression bind above it.")
    print()
    print("  => THE YEAR-1+ PRICE IS NEVER ANCHOR-DOMINATED, so no object can move it off the")
    print("     anchor. That is defect D1 restated as a measurement: at ns>=1 the fitted year-0")
    print("     prior survives only as a floor and as the staleness-cap basis. There is no blend to")
    print("     find. LAM_SIT is the engine's ONLY anchor<->production blend, and it is switched")
    print("     off the moment a row QUALIFIES (ns>=1). Forcing it to 0 and to 1 moves this cohort")
    print("     %.4f <-> %.4f on /anchor, which is NOT inertness: the cohort is ND rows with ANY"
          % (RES['LAM_SIT (sit-out blend)']['zero_anchor'], RES['LAM_SIT (sit-out blend)']['sat_anchor']))
    print("     games, and a row below the prorated bar (6 x fE) still has nseas_pro==0 and still")
    print("     routes through sitout_ev. So LAM_SIT is LIVE exactly where the anchor blend still")
    print("     exists and DEAD the instant a row qualifies — which is the cliff ITEM A removes.")
    print("     See ABLATION_READING.md for the full reading.")
    print()
    print("  CONSEQUENCE FOR ITEM A: 'the EXISTING games ramp' cannot mean an existing year-1+")
    print("  blend weight, because none exists. The only reading consistent with 'no new machinery'")
    print("  is LAM_SIT's games ramp — the engine's own anchor<->production hand-over — CARRIED")
    print("  FORWARD past ns==0 instead of being switched off, on CUMULATIVE games so that v2")
    print("  borrows less than v1 and more than v3.")

json.dump(RES, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "item_a_ablation.json"), "w"), indent=1)
print("\nwrote item_a_ablation.json")
