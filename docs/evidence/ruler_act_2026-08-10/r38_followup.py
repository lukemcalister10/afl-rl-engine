"""FOLLOW-UPS: (1) exact relabel of the OLD 207-row UNKNOWN cell; (2) bend-survival across all four
instruments for the named age cells; (3) is the 19-20 band a real age effect or a route effect?
(4) why mature-21+ still fails the bar. READ-ONLY."""
import json
from collections import Counter
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
ROWS = json.load(open(SP + "/r24_rows.json"))["rows"]
AGN = {r["key"]: r["age_new"] for r in json.load(open(SP + "/r36_ages.json"))}
AGO = {r["key"]: r["age_old"] for r in json.load(open(SP + "/r36_ages.json"))}
for r in ROWS: r["age"] = AGN.get(r["key"]); r["age_old"] = AGO.get(r["key"])
NB = 20000; rng = np.random.default_rng(20260810)
KEYS = [("A", "A_av_full"), ("B", "B_rt_full"), ("C", "C_av_win"), ("D", "D_rt_win")]
OV = {k: sum(r[f] for r in ROWS) / sum(r["proxy"] for r in ROWS) for k, f in KEYS}
nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")


def stat(rows):
    w = np.array([r["proxy"] for r in rows], float); P = w.sum()
    effn = float(P ** 2 / (w ** 2).sum())
    return effn, {k: float(sum(r[f] for r in rows) / P) for k, f in KEYS}


print("=" * 100)
print("1. THE OLD 'age UNKNOWN' CELL, RE-MEASURED EXACTLY (the same 207 rows the landed map named)")
print("=" * 100)
old = [r for r in ROWS if r["age_old"] is None]
e, t = stat(old)
print("  n=%d  eff-n %.1f" % (len(old), e))
for k, _ in KEYS:
    print("     %s  tilt %.4f  1/tilt %.4f   [landed A was 2.1393]" % (k, t[k], 1 / t[k]))
print("  its TRUE age composition: %s" % sorted(Counter(r["age"] for r in old).items()))
w = sum(r["proxy"] for r in old)
print("  weight by band: <=18 %.1f%% | 19-20 %.1f%% | 21-22 %.1f%% | 23+ %.1f%%"
      % tuple(100 * sum(r["proxy"] for r in old if lo <= r["age"] <= hi) / w
              for lo, hi in ((0, 18), (19, 20), (21, 22), (23, 99))))
print("  classes: %s" % sorted(Counter(r["year"] for r in old).items()))
# is 2.139 an era effect? compare same-age cells inside vs outside 2004-05
y_in = [r for r in ROWS if r["year"] <= 2005 and r["age"] <= 18]
y_out = [r for r in ROWS if r["year"] >= 2006 and r["age"] <= 18]
ei, ti = stat(y_in); eo, to = stat(y_out)
print("\n  CONTROLLED COMPARISON — age<=18 only, inside vs outside classes 2004-05:")
print("     2004-05  n=%3d eff-n %5.1f  1/tilt A %.4f  D %.4f" % (len(y_in), ei, 1 / ti["A"], 1 / ti["D"]))
print("     2006-15  n=%3d eff-n %5.1f  1/tilt A %.4f  D %.4f" % (len(y_out), eo, 1 / to["A"], 1 / to["D"]))
print("     -> holding AGE fixed at <=18, the 2004-05 cell is still %.0f%% (A) / %.0f%% (D) worse,"
      % (100 * (ti["A"] and (1 / ti["A"]) / (1 / to["A"]) - 1), 100 * ((1 / ti["D"]) / (1 / to["D"]) - 1)))
print("        so the old cell's factor is an ERA/CLASS reading, not an age one.")

print()
print("=" * 100)
print("2. BEND SURVIVAL ACROSS ALL FOUR — named age cells only (bar 35)")
print("=" * 100)
CAND = [("young <=20", [r for r in ROWS if r["age"] <= 20]),
        ("mature 21+", [r for r in ROWS if r["age"] >= 21]),
        ("<=18", [r for r in ROWS if r["age"] <= 18]),
        ("19-20", [r for r in ROWS if 19 <= r["age"] <= 20]),
        ("21-22", [r for r in ROWS if 21 <= r["age"] <= 22]),
        ("23+", [r for r in ROWS if r["age"] >= 23]),
        ("ND1-64 young <=20", [r for r in ROWS if nd(r) and r["age"] <= 20]),
        ("pool young <=20", [r for r in ROWS if r["is_pool"] and r["age"] <= 20]),
        ("pool RD young <=20", [r for r in ROWS if r["typ"] == "RD" and r["age"] <= 20]),
        ("young <=20 x talls", [r for r in ROWS if r["age"] <= 20 and r["pos"] in TALL]),
        ("young <=20 x runners", [r for r in ROWS if r["age"] <= 20 and r["pos"] in RUN]),
        ("classes 2004-05", [r for r in ROWS if r["year"] <= 2005])]
print("  %-24s %7s | %7s %7s %7s %7s | %s" % ("cell", "eff-n", "bendA", "bendB", "bendC", "bendD", "verdict"))
for nm, rs in CAND:
    e, t = stat(rs)
    if e < 35: print("  %-24s %7.1f | %s" % (nm, e, "BELOW BAR - not named")); continue
    b = [(1 / t[k]) / (1 / OV[k]) for k, _ in KEYS]
    mats = [abs(x - 1) >= 0.10 for x in b]; signs = {(x > 1) for x in b}
    v = ("HOLDS ON ALL FOUR" if (all(mats) and len(signs) == 1) else
         ("no material bend on any" if not any(mats) else "partial (%s)" %
          "".join("X" if m else "." for m in mats)))
    print("  %-24s %7.1f | %7.3f %7.3f %7.3f %7.3f | %s" % (nm, e, b[0], b[1], b[2], b[3], v))

print()
print("=" * 100)
print("3. IS THE 19-20 BAND A REAL AGE EFFECT, OR A ROUTE EFFECT IN DISGUISE?")
print("=" * 100)
b1920 = [r for r in ROWS if 19 <= r["age"] <= 20]
print("  n=%d  route: %s" % (len(b1920), Counter(r["typ"] for r in b1920).most_common()))
print("  pool share by weight: %.1f%%  (population pool share %.1f%%)"
      % (100 * sum(r["proxy"] for r in b1920 if r["is_pool"]) / sum(r["proxy"] for r in b1920),
         100 * sum(r["proxy"] for r in ROWS if r["is_pool"]) / sum(r["proxy"] for r in ROWS)))
print("  position: %s" % Counter(r["pos"] for r in b1920).most_common())
print("  class span: %s" % sorted(Counter(r["year"] for r in b1920).items()))
for nm, rs in (("19-20 x ND1-64", [r for r in b1920 if nd(r)]),
               ("19-20 x pool", [r for r in b1920 if r["is_pool"]]),
               ("<=18 x ND1-64", [r for r in ROWS if r["age"] <= 18 and nd(r)]),
               ("<=18 x pool", [r for r in ROWS if r["age"] <= 18 and r["is_pool"]])):
    if not rs: continue
    e, t = stat(rs)
    fl = " " if e >= 35 else "*"
    print("  %s%-18s n=%4d eff-n %6.1f  1/tilt A %.4f  D %.4f" % (fl, nm, len(rs), e, 1 / t["A"], 1 / t["D"]))
print("  (* below bar) -- if 19-20 is straighter WITHIN each route, it is an age effect.")

print()
print("=" * 100)
print("4. WHY MATURE-21+ STILL FAILS THE BAR (n=167 but eff-n 32.8)")
print("=" * 100)
mat = [r for r in ROWS if r["age"] >= 21]
w = np.array([r["proxy"] for r in mat], float)
print("  n=%d  sum proxy %.0f  eff-n %.1f" % (len(mat), w.sum(), w.sum() ** 2 / (w ** 2).sum()))
print("  rows with proxy == 0 (bust before yr 4, zero weight): %d" % int((w == 0).sum()))
print("  top 8 by weight (share of the cell):")
for r in sorted(mat, key=lambda x: -x["proxy"])[:8]:
    print("     %-26s %-4s %d age %-3d proxy %7.0f  %4.1f%%"
          % (r["player"], r["typ"], r["year"], r["age"], r["proxy"], 100 * r["proxy"] / w.sum()))
print("  top-5 weight share: %.1f%%  -> the cell is dominated by a handful of priced matures,"
      % (100 * sum(sorted(w)[-5:]) / w.sum()))
print("     which is what holds eff-n down; the birthdates added 0 mature rows (2004-05 were 96.6%% young).")
print("  mature rows gained from the DOB write: %d"
      % len([r for r in mat if r["age_old"] is None]))
