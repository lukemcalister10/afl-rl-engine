"""Design-option magnitudes on the owner-basis FULL-COHORT YEAR-1 LEAD.
Basis = owner_basis.py exactly: classes 2004-2025, keys in both matrices, lead = sum(vpath[0]) / sum(v0),
concluded careers score 0 and stay in the denominator, unreached classes excluded, v0<=0 excluded.
Baseline (stage-5 landed) = 0.946050.  READ-ONLY arithmetic on committed matrices; no engine run.
"""
import json
SD = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
A = {(r["key"], r["type"], r["year"]): r for r in json.load(open(SD + "s4a1.json"))["recs"]}
B = {(r["key"], r["type"], r["year"]): r for r in json.load(open(SD + "s5.json"))["recs"]}
KS = sorted(set(A) & set(B)); END = 2026
LV = {"IRE": 133.4, "MSD": 286.8, "PDA": 194.3, "PDN": 123.0, "PDS": 145.0, "SSP": 252.8, "UNR": 103.7}
RDP = {"KPD": 300.3, "KPF": 216.0, "MID": 294.8, "RUCK": 282.5, "SD": 246.9, "SF": 231.5}
PLF = 1.0524; FLOOR1 = 0.45


def anchor(r):
    t = r["type"]
    lv = RDP[r["pos"]] if t == "RD" else (266.1 if t == "ND" else LV[t])
    return lv * PLF


def val(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    return 0.0 if n - 1 >= len(vp) else float(vp[n - 1] or 0.0)


BASE = []
for k in KS:
    r, b = A[k], B[k]
    if not (2004 <= r["year"] <= 2025): continue
    v1, v0 = val(b, 1), val(b, 0)
    if v1 is None or v0 is None or v0 <= 0: continue
    BASE.append((r, b, v1, v0))
SUM1 = sum(x[2] for x in BASE); SUM0 = sum(x[3] for x in BASE)
print("baseline lead %.6f   n=%d  sum v1=%.0f  sum v0=%.0f" % (SUM1 / SUM0, len(BASE), SUM1, SUM0))
print("  1 point of lead (+0.001) = %.0f units of year-1 value\n" % (0.001 * SUM0))

pool = lambda r: r["is_pool"]
age = lambda r: r.get("age_draft")
gy1 = lambda r: r.get("games_yr1") or 0
SIT = lambda r: gy1(r) == 0
RUN = lambda r: r["pos"] in ("MID", "SD", "SF")


def option(name, rule, floored=True, note=""):
    """rule(r) -> multiplier on the year-1 price (None = untouched)."""
    d = 0.0; moved = 0; clamped = 0
    for r, b, v1, v0 in BASE:
        if not pool(r): continue
        m = rule(r)
        if m is None: continue
        new = v1 * m
        if floored:
            fl = FLOOR1 * anchor(r)
            if new < fl: new = fl; clamped += 1
        if abs(new - v1) < 1e-9: continue
        d += new - v1; moved += 1
    print("%-58s dLead=%+.4f  rows moved=%4d  floor-clamped=%4d  %s"
          % (name, d / SUM0, moved, clamped, note))
    return d / SUM0


print("=== CUT-SIDE OPTIONS (year-1 over-pricing) ===")
option("A1  named union sitters (23+|IRE|MSD) x0.280, floored",
       lambda r: 0.280 if (SIT(r) and ((age(r) or 0) >= 23 or r["type"] in ("IRE", "MSD"))) else None,
       note="the stage-7 named cell, re-derived")
option("A1u A1 UNFLOORED (what #326 floor costs)",
       lambda r: 0.280 if (SIT(r) and ((age(r) or 0) >= 23 or r["type"] in ("IRE", "MSD"))) else None,
       floored=False)
option("A2  A1 + mature21+ non-RD (all states) x0.615, floored",
       lambda r: (0.280 if (SIT(r) and ((age(r) or 0) >= 23 or r["type"] in ("IRE", "MSD")))
                  else (0.615 if ((age(r) or 0) >= 21 and r["type"] != "RD") else None)))
option("A3  ALL pool sitters x0.804 (single named cell), floored",
       lambda r: 0.804 if SIT(r) else None, note="coarsest named cut; eff-n 636")
option("A4  BLANKET mature 21+ x0.944 (the forbidden shape)",
       lambda r: 0.944 if (age(r) or 0) >= 21 else None, note="CI straddles -> not a lawful cell")

print("\n=== LIFT-SIDE OPTIONS (year-1 under-pricing) ===")
option("B1  young<=20 x RUNNING x1.247, capped at entry anchor",
       lambda r: 1.247 if ((age(r) or 99) <= 20 and RUN(r)) else None, floored=False,
       note="uncapped; cap effect below")
option("B2  young<=20 x ND65+ x1.608, uncapped",
       lambda r: 1.608 if ((age(r) or 99) <= 20 and r["type"] == "ND") else None, floored=False)
option("B3  pool established 6+ young<=20 x1.497, uncapped",
       lambda r: 1.497 if ((age(r) or 99) <= 20 and gy1(r) >= 6) else None, floored=False)


def capped(name, rule):
    d = 0.0; moved = 0; hit = 0
    for r, b, v1, v0 in BASE:
        if not pool(r): continue
        m = rule(r)
        if m is None: continue
        new = v1 * m
        cap = anchor(r)
        if new > cap: new = cap; hit += 1
        if new <= v1: continue
        d += new - v1; moved += 1
    print("%-58s dLead=%+.4f  rows moved=%4d  cap-bound=%4d" % (name, d / SUM0, moved, hit))


capped("B1c B1 CAPPED at the entry anchor (the standing cap)",
       lambda r: 1.247 if ((age(r) or 99) <= 20 and RUN(r)) else None)
capped("B2c B2 CAPPED at the entry anchor",
       lambda r: 1.608 if ((age(r) or 99) <= 20 and r["type"] == "ND") else None)

print("\n=== YEAR-0 SIDE: flattening the engine age curve (moves the DENOMINATOR) ===")


def v0opt(name, rule, note=""):
    d = 0.0; moved = 0
    for r, b, v1, v0 in BASE:
        if not pool(r): continue
        m = rule(r)
        if m is None: continue
        d += v0 * m - v0; moved += 1
    L2 = SUM1 / (SUM0 + d)
    print("%-58s dLead=%+.4f  rows moved=%4d  d(sum v0)=%+8.0f  %s"
          % (name, L2 - SUM1 / SUM0, moved, d, note))


v0opt("C1  NAMED yr-0 cells only: <=18 x0.555, 21-22 x2.149",
      lambda r: 0.555 if (age(r) or 99) <= 18 else (2.149 if (age(r) or 0) in (21, 22) else None),
      note="23+ STRUCK by eff-n -> untouched")
v0opt("C2  C1 + 23+ riding the pooled mature 21+ cell x2.061",
      lambda r: 0.555 if (age(r) or 99) <= 18 else (2.061 if (age(r) or 0) >= 21 else None),
      note="POOLED, disclosed")
v0opt("C3  mature 21+ leg only x2.061 (leave young alone)",
      lambda r: 2.061 if (age(r) or 0) >= 21 else None)
v0opt("C4  whole pool x0.724 (the blanket the law forbids)",
      lambda r: 0.724, note="one blanket cell")

print("\n=== C5: LEVEL-PRESERVING year-0 age RESHAPE (pool leg total v0 held) ===")
tgt = lambda r: (0.555 if (age(r) or 99) <= 18 else (2.061 if (age(r) or 0) >= 21 else 1.0))
pv0 = sum(v0 for r, b, v1, v0 in BASE if pool(r))
raw = sum(v0 * tgt(r) for r, b, v1, v0 in BASE if pool(r))
s = pv0 / raw
up = sum(v0 * (tgt(r) * s - 1) for r, b, v1, v0 in BASE if pool(r) and tgt(r) * s > 1)
dn = sum(v0 * (1 - tgt(r) * s) for r, b, v1, v0 in BASE if pool(r) and tgt(r) * s < 1)
print("  renorm scale %.4f -> pool sum v0 unchanged; dLead = +0.0000 by construction" % s)
print("  value REDISTRIBUTED inside the pool year-0 leg: %.0f up / %.0f down (%.1f%% of the pool's own v0)"
      % (up, dn, 100 * up / pv0))
print("  per-row: age<=18 x%.3f   19-20 x%.3f   21+ x%.3f" % (0.555 * s, 1.0 * s, 2.061 * s))

print("\n=== D: SMOOTH YEAR-1 AGE TAPER on the anchor leg (no cliff; g(<=20)=1) ===")
def taper(name, g, note=""):
    d = 0.0; moved = 0; clamped = 0
    for r, b, v1, v0 in BASE:
        if not pool(r): continue
        a = age(r)
        if a is None: continue
        m = g(a)
        if m >= 1.0: continue
        new = v1 * m
        fl = FLOOR1 * anchor(r)
        if new < fl: new = fl; clamped += 1
        if abs(new - v1) < 1e-9: continue
        d += new - v1; moved += 1
    print("%-58s dLead=%+.4f  rows moved=%4d  floor-clamped=%4d  %s" % (name, d / SUM0, moved, clamped, note))

lin = lambda a, a0, a1, lo: 1.0 if a <= a0 else (lo if a >= a1 else 1.0 - (1.0 - lo) * (a - a0) / (a1 - a0))
taper("D1  linear 21->26, floor 0.33 (to the named 23+ level)", lambda a: lin(a, 20, 26, 0.33))
taper("D2  linear 21->26, floor 0.60 (to the mature non-RD level)", lambda a: lin(a, 20, 26, 0.60))
taper("D3  linear 21->26, floor 0.33, RUNNING ROUTES EXEMPT is not expressible on age alone", lambda a: lin(a, 20, 26, 0.33))
def taper2(name, g, keep):
    d = 0.0; moved = 0; clamped = 0
    for r, b, v1, v0 in BASE:
        if not pool(r): continue
        a = age(r)
        if a is None or keep(r): continue
        m = g(a)
        if m >= 1.0: continue
        new = v1 * m; fl = FLOOR1 * anchor(r)
        if new < fl: new = fl; clamped += 1
        if abs(new - v1) < 1e-9: continue
        d += new - v1; moved += 1
    print("%-58s dLead=%+.4f  rows moved=%4d  floor-clamped=%4d" % (name, d / SUM0, moved, clamped))
taper2("D4  D1 but RD route held at 1.0 (route-conditioned)", lambda a: lin(a, 20, 26, 0.33), lambda r: r["type"] == "RD")
taper2("D5  D1 restricted to SITTERS only (games_yr1==0)", lambda a: lin(a, 20, 26, 0.33), lambda r: gy1(r) > 0)
