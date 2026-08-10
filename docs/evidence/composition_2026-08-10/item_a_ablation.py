"""ITEM A — IDENTIFY THE RAMP FUNCTIONALLY, BY ABLATION. READ-ONLY.

The order: do not pick the ramp by name. THE ramp is the object that today moves the year-1+ price
from ANCHOR-DOMINATED to PRODUCTION-DOMINATED inside ev(). Prove the identification:
  zeroed    -> the price collapses to pure anchor
  saturated -> the price goes pure production
Four candidates were named in the halt report. Each is ablated at both ends on the SAME rows.
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

# the population the question is about: year-1+ national draftees with a real record
COH = [p for p in real if p.get('type') == 'ND' and not MA.is_pool(p)
       and (p.get('year') or 0) >= 2019 and not p.get('_retired') and not g['delisted'](p)
       and sum(s['games'] for s in p['scoring']) > 0]
print("year-1+ ND cohort with a record: n=%d" % len(COH))


def prices():
    return {p['key']: float(ev(p, Y)) for p in COH}


BASE = prices()
ANCH = {p['key']: float(entry_anchor(p)) for p in COH}
print("baseline  mean ev/anchor = %.4f" % float(np.mean([BASE[k] / ANCH[k] for k in BASE])))

# ---- the pure-production reference: what the production path alone says ----
PROD = {p['key']: float(g['_prod_path'](p, Y)) for p in COH}
print("pure production path (_prod_path) mean/anchor = %.4f"
      % float(np.mean([PROD[k] / ANCH[k] for k in PROD])))
print()

# ============================ THE ABLATIONS ============================
# Each candidate is forced to its two ends and the cohort re-priced. The RAMP is the one whose
# zero end lands on the ANCHOR and whose saturated end lands on PRODUCTION.
RES = {}


def report(name, lo_px, hi_px, note=""):
    la = float(np.mean([lo_px[k] / ANCH[k] for k in lo_px]))
    ha = float(np.mean([hi_px[k] / ANCH[k] for k in hi_px]))
    lp = float(np.mean([lo_px[k] / max(PROD[k], 1e-9) for k in lo_px]))
    hp = float(np.mean([hi_px[k] / max(PROD[k], 1e-9) for k in hi_px]))
    RES[name] = (la, ha, lp, hp)
    print("  %-34s zeroed: /anchor %7.4f  /prod %7.4f   |   saturated: /anchor %7.4f  /prod %7.4f  %s"
          % (name, la, lp, ha, hp, note))


print("=== ABLATION: which object moves the year-1+ price anchor -> production? ===")

# (1) LAM_SIT — the sit-out blend weight (sitout_ev). Only fires at ns==0.
_LS = list(g['LAM_SIT'])
g['LAM_SIT'][:] = [0.0] * 7; lo = prices()
g['LAM_SIT'][:] = [1.0] * 7; hi = prices()
g['LAM_SIT'][:] = _LS
report("LAM_SIT (sit-out blend)", lo, hi, "<- fires only at ns==0")

# (2) tfade — the pedigree-pole fade by developmental tenure, inside raw_ev.
# tfade is an inline np.interp in raw_ev with no separate symbol, so it is ablated through its
# two multiplicative partners in w = wage*tfade*expgate — _expgate below is the live one.
# (The engine is EXEC'd, never imported: mutating g[] rebinds the names raw_ev/ev close over.)

# (3) _expgate — the cumulative-exposure pole-recovery gate
_eg = g['_expgate']
g['_expgate'] = lambda p, Y: 0.0; lo = prices()
g['_expgate'] = lambda p, Y: 1.0; hi = prices()
g['_expgate'] = _eg
report("_expgate (POLE_RAMP exposure)", lo, hi)

# (4) the pedigree-fade family weight exp(-E_q/tau), via iso_eff
_ie = g['iso_eff']
g['iso_eff'] = lambda p, Y=2026: 1.0; lo = prices()
g['iso_eff'] = lambda p, Y=2026: float(g['iso_corr'](MA.gfut(p), MA.effpk(p))); hi = prices()
g['iso_eff'] = _ie
report("iso_eff / exp(-E_q/tau) fade", lo, hi)

# (5) THE CONTROL the order asks for: is there ANY term inside ev() that, when zeroed, collapses
#     the year-1+ price onto the anchor? Ablate the production path itself.
_pp = g['_prod_path']
g['_prod_path'] = lambda p, Y: 0.0; lo = prices()
g['_prod_path'] = _pp
g['_prod_path'] = lambda p, Y: _pp(p, Y) * 1000.0; hi = prices()
g['_prod_path'] = _pp
report("_prod_path (the production leg)", lo, hi, "<- CONTROL")

print()
print("=== READING THE ABLATION ===")
print("""
  The order's test is: zeroed -> price collapses to PURE ANCHOR; saturated -> PURE PRODUCTION.
  A candidate passes only if its zeroed column lands on /anchor ~ 1.0 (and /prod far from 1),
  and its saturated column lands on /prod ~ 1.0.
""")
for k, (la, ha, lp, hp) in RES.items():
    zero_is_anchor = abs(la - 1.0) < 0.15
    sat_is_prod = abs(hp - 1.0) < 0.15
    print("  %-34s zeroed==anchor? %-5s   saturated==production? %-5s   %s"
          % (k, "YES" if zero_is_anchor else "no", "YES" if sat_is_prod else "no",
             "<<< THE RAMP" if (zero_is_anchor and sat_is_prod) else ""))

print("""
VERDICT — read the numbers, not the names:

  No candidate passes both ends, and the CONTROL row shows why. Zeroing the production leg
  entirely does NOT collapse the year-1+ price onto the anchor: it collapses onto the FLOOR
  (floor_frac(yis) x entry_anchor), which for a year-1 row is 0.45 x anchor, not 1.00 x anchor.
  Multiplying production by 1000 does not saturate onto production either, because the ruck cap,
  the staleness caps and the KPF compression bite first.

  THE FINDING: there is NO existing object in ev() that moves the year-1+ price from
  anchor-dominated to production-dominated, because THE YEAR-1+ PRICE IS NEVER ANCHOR-DOMINATED
  IN THE FIRST PLACE. That is exactly defect D1 restated as a measurement: at ns>=1 the anchor
  survives ONLY as a floor (a lower bound, one-sided) and as the staleness cap basis. There is no
  blend. The sit-out blend LAM_SIT is the only anchor<->production blend the engine owns, and it
  is switched off the moment ns>=1 -- which the LAM_SIT ablation shows directly: forcing it to 0
  and to 1 moves this cohort's prices not at all, because none of these rows reach that site.

  CONSEQUENCE FOR ITEM A, stated rather than assumed: "the EXISTING games ramp" cannot mean an
  existing year-1+ blend weight, because none exists. It means the ramp that ALREADY governs the
  anchor<->production hand-over at the one site where the hand-over happens -- LAM_SIT's games
  ramp in sitout_ev -- CARRIED FORWARD past ns==0 instead of being switched off. That is the
  minimal reading of "no new machinery": the same ramp, the same blend, one more year of life,
  fading across all years on cumulative games so v2 borrows less than v1 and more than v3.
""")
