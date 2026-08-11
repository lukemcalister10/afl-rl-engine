"""WHY THE LEVEL BARELY MOVES — the mechanics of the availability correction, as numbers.
Also: the two-sided nature of the 21-game normalization (it CUTS finals-heavy seasons as well as
lifting short ones).  READ-ONLY."""
import json, math
from collections import Counter
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939; END = 2026; FULL = 21.0; T = 6


def _s(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt(l):
    c = LG * LW * (_s((l - LM) / LW) - _s((LB - LM) / LW)); return c if c > 0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def kern(a, b): return SCALE * posval(a + capt(a) - REPL[b]) if b in REPL else 0.0


recs = {(r["key"], r["type"], r["year"]): r for r in
        json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]}
ROWS = [r for r in json.load(open(SP + "/r20_rows.json"))["rows"] if 2004 <= r["year"] <= 2015]

vw_num = vw_den = 0.0; uw = []; up = 0.0; dn = 0.0; nlong = 0; nshort = 0; nfull = 0
seasons = 0; delivered_by_row = []
for r in ROWS:
    rec = recs[(r["key"], r["typ"], r["year"])]
    Cy = r["year"]; nd_ = 0
    for s in (rec.get("seasons") or []):
        k = s["year"] - Cy
        if k < 4 or s["year"] > END or s["games"] < 1: continue
        u = kern(s["avg"], s["bar"]); g = s["games"]
        seasons += 1; nd_ += 1; uw.append(g)
        vw_num += u * g; vw_den += u
        if g >= T:
            d = DISC ** (k - 4)
            if g < FULL: up += u * (FULL - g) / d; nshort += 1
            elif g > FULL: dn += u * (g - FULL) / d; nlong += 1
            else: nfull += 1
    delivered_by_row.append((r["proxy"], nd_))

print("=" * 108)
print("A. WHY THE AVAILABILITY CORRECTION IS SMALL: value sits in seasons that were already near-full")
print("=" * 108)
print("  delivered seasons from career year 4 on (primary window) : %d" % seasons)
print("  UNWEIGHTED mean games per delivered season               : %.2f" % (sum(uw) / len(uw)))
print("  VALUE-WEIGHTED mean games (weight = the season's kernel)  : %.2f" % (vw_num / vw_den))
print("  -> the gap the rate convention can close is only %.2f games per value-unit, not %.2f."
      % (FULL - vw_num / vw_den, FULL - sum(uw) / len(uw)))
print("  games distribution of delivered seasons (bucketed):")
b = Counter(("0-5" if g <= 5 else "6-9" if g <= 9 else "10-12" if g <= 12 else
             "13-17" if g <= 17 else "18-21" if g <= 21 else "22+") for g in uw)
for k in ("0-5", "6-9", "10-12", "13-17", "18-21", "22+"):
    print("     %-6s %5d seasons (%4.1f%%)" % (k, b[k], 100 * b[k] / len(uw)))

print()
print("=" * 108)
print("B. THE 21-GAME NORMALIZATION IS TWO-SIDED (it cuts as well as lifts)")
print("=" * 108)
print("  seasons at/above T=%d priced at FULL: %d short of 21 (lifted) | %d exactly 21 | %d above 21 (CUT)"
      % (T, nshort, nfull, nlong))
print("  discounted value ADDED by lifting short seasons  : %+10.0f" % up)
print("  discounted value REMOVED by capping 22+ seasons  : %+10.0f" % -dn)
print("  NET availability add-back                        : %+10.0f" % (up - dn))
P = sum(r["proxy"] for r in ROWS)
Rav = sum(r["realized"] for r in ROWS); Rrt = sum(r["rate"]["6"] + r["stub"] for r in ROWS)
print("  check: REALIZED_rate - REALIZED_av = %+.0f  (matches: %s)"
      % (Rrt - Rav, "yes" if abs((Rrt - Rav) - (up - dn)) < 1.0 else "NO"))
print("  the add-back is %.1f%% of availability-in REALIZED and %.1f%% of the PROXY."
      % (100 * (up - dn) / Rav, 100 * (up - dn) / P))

print()
print("=" * 108)
print("C. WHAT REMAINS AFTER THE OWNER'S CORRECTION")
print("=" * 108)
print("  sum PROXY                    %10.0f" % P)
print("  sum REALIZED-RATE (T=6)      %10.0f   tilt %.4f  ->  1/tilt %.4f" % (Rrt, Rrt / P, P / Rrt))
print("  residual gap                 %10.0f   = %.1f%% of the year-4 price" % (P - Rrt, 100 * (P - Rrt) / P))
print("  of the ORIGINAL gap (%.0f), attendance explained %.0f = %.1f%%; %.1f%% is NOT attendance."
      % (P - Rav, Rrt - Rav, 100 * (Rrt - Rav) / (P - Rav), 100 * (1 - (Rrt - Rav) / (P - Rav))))
wsum = sum(p for p, _ in delivered_by_row)
vwd = sum(p * n for p, n in delivered_by_row) / wsum
print("  value-weighted mean DELIVERED seasons from year 4 on : %.2f" % vwd)
print("  (the engine's own forward loop runs up to 18 years subject to age/decay, rl_model.py:806-808)")
print("  -> the residual is dominated by CAREERS ENDING, which the owner's principle keeps on the")
print("     realized side by design ('career end = no seasons = delivers nothing').")
