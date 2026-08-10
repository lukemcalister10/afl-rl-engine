"""THE TILT MAP — final cells on the PRIMARY window (draft classes 2004-2015).
CENSORING RULE (stated, and shown as a number in r12_censor.py): a class can contribute a LIVE career
only if it can reach 11 seasons of data by 2026, i.e. C+11 <= 2026 => C <= 2015.  For C >= 2016 the
owner's population rule admits ONLY completed careers -- i.e. only the failures -- and those classes
measure tilt 0.049 by construction.  They are DROPPED and disclosed, never named.
F8 BAR: Kish eff-n >= 35 on the cell's own denominator weights (w_i = the year-4 price) AND a
20,000-rep bootstrap CI in both the player-resampled and the draft-class-clustered variant.
READ-ONLY.
"""
import json
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json"))
CLO, CHI = 2004, 2015
ROWS = [r for r in D["rows"] if CLO <= r["year"] <= CHI]
CENS = [r for r in D["rows"] if r["year"] > CHI]
NB = 20000; BAR = 35.0
rng = np.random.default_rng(20260810)
OVERALL = sum(x["realized"] for x in ROWS) / sum(x["proxy"] for x in ROWS)

# ---- DIP CUT (mechanical, on the engine's OWN season price sp(k)) --------------------------------
# sp(k) = the engine season price of career year k (see r10_tilt.py).  A row is eligible for the dip
# cut only if the career reached career year 5 in calendar terms AND years 3 and 5 are both observed
# (games >= 1), so the year-4 season has two real neighbours to be judged against.
#   DIP-A (strict, "below BOTH neighbours"): sp4 < 0.80 * min(sp3, sp5)
#   DIP-B (broad, "below the better neighbour"): sp4 < 0.80 * max(sp3, sp5)
#   DIP-G (games only, the injury shape):       g4  < 0.60 * min(g3, g5)
def eligible_dip(r): return r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
def dipA(r): return eligible_dip(r) and r["sp4"] < 0.80 * min(r["sp3"], r["sp5"])
def dipB(r): return eligible_dip(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
def dipG(r): return eligible_dip(r) and r["g4"] < 0.60 * min(r["g3"], r["g5"])


def cell(rows):
    if not rows: return None
    w = np.array([r["proxy"] for r in rows], float)
    num = np.array([r["realized"] for r in rows], float)
    stub = np.array([r["stub"] for r in rows], float)
    P = w.sum()
    if P <= 0: return None
    effn = float((P ** 2) / (w ** 2).sum())
    tilt = float(num.sum() / P)
    n = len(rows)
    idx = rng.integers(0, n, size=(NB, n))
    bp = num[idx].sum(1) / np.maximum(w[idx].sum(1), 1e-9)
    lo_p, hi_p = np.percentile(bp, [2.5, 97.5])
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    groups = [np.where(yrs == y)[0] for y in uy]
    gnum = np.array([num[g].sum() for g in groups]); gden = np.array([w[g].sum() for g in groups])
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    bc = gnum[gi].sum(1) / np.maximum(gden[gi].sum(1), 1e-9)
    lo_c, hi_c = np.percentile(bc, [2.5, 97.5])
    return dict(n=n, n_wt=int((w > 0).sum()), effn=effn, tilt=tilt, corr=1.0 / tilt,
                rel=tilt / OVERALL, ci_player=[float(lo_p), float(hi_p)],
                ci_class=[float(lo_c), float(hi_c)],
                stub=float(stub.sum() / num.sum()) if num.sum() > 0 else 0.0,
                named=bool(effn >= BAR), sum_proxy=float(P), sum_real=float(num.sum()))


OUT = {}; NAMED = []


def run(axis, cells):
    res = [(nm, cell(rs)) for nm, rs in cells]
    print()
    print("=" * 120)
    print(axis)
    print("-" * 120)
    print("   %-33s %5s %5s %7s %8s %8s %6s  %-15s %-15s %5s" %
          ("cell", "n", "n_wt", "eff-n", "TILT", "1/tilt", "rel", "CI player", "CI class", "stub"))
    for nm, c in res:
        if c is None: print("   %-33s   (empty)" % nm); continue
        fl = " " if c["named"] else "*"
        sf = "!" if c["stub"] > 0.15 else " "
        print("  %s%-33s %5d %5d %7.1f %8.4f %8.4f %6.2f  [%5.3f,%5.3f] [%5.3f,%5.3f] %4.1f%%%s" %
              (fl, nm, c["n"], c["n_wt"], c["effn"], c["tilt"], c["corr"], c["rel"],
               c["ci_player"][0], c["ci_player"][1], c["ci_class"][0], c["ci_class"][1],
               100 * c["stub"], sf))
        if c["named"]: NAMED.append((axis, nm, c))
    OUT[axis] = {nm: c for nm, c in res}


nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")
era2 = lambda y: "pre-2012" if y <= 2011 else "2012-2015"
era3 = lambda y: "2004-2009" if y <= 2009 else ("2010-2012" if y <= 2012 else "2013-2015")

print("THE YEAR-4 RULER TILT MAP")
print("basis  : %s | store %s | engine %s | SCALE %.6f | hurdle %.4f"
      % (D["meta"]["matrix"], D["meta"]["store"], D["meta"]["engine_head"],
         D["meta"]["SCALE"], D["meta"]["DISC"]))
print("window : draft classes %d-%d (censoring rule); DROPPED as censored: %d rows, classes %d-2022"
      % (CLO, CHI, len(CENS), CHI + 1))
print("n      : %d rows (%d completed, %d live 11+)   sum PROXY=%.0f  sum REALIZED=%.0f"
      % (len(ROWS), sum(1 for r in ROWS if r["done"]), sum(1 for r in ROWS if not r["done"]),
         sum(r["proxy"] for r in ROWS), sum(r["realized"] for r in ROWS)))
print("OVERALL TILT = %.4f   correction 1/tilt = %.4f   terminal-stub share = %.2f%%"
      % (OVERALL, 1 / OVERALL, 100 * sum(r["stub"] for r in ROWS) / sum(r["realized"] for r in ROWS)))
print("zero-proxy rows (career over before year 4) = %d of %d -- kept, but they carry ZERO weight"
      % (sum(1 for r in ROWS if r["proxy"] <= 0), len(ROWS)))

run("AXIS 0 - OVERALL / BROAD GROUP / ROUTE (the coarse fallback)", [
    ("ALL", ROWS),
    ("talls (KPF/KPD/RUCK)", [r for r in ROWS if r["pos"] in TALL]),
    ("runners (MID/SD/SF)", [r for r in ROWS if r["pos"] in RUN]),
    ("ND 1-64", [r for r in ROWS if nd(r)]),
    ("pool (all routes)", [r for r in ROWS if pool(r)]),
])
run("AXIS 1a - POSITION",
    [(p, [r for r in ROWS if r["pos"] == p]) for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK")])
run("AXIS 1b - ERA (2-band) and ERA (3-band)",
    [(e, [r for r in ROWS if era2(r["year"]) == e]) for e in ("pre-2012", "2012-2015")] +
    [(e, [r for r in ROWS if era3(r["year"]) == e]) for e in ("2004-2009", "2010-2012", "2013-2015")])
run("AXIS 1c - POSITION x ERA (2-band)",
    [("%s x %s" % (p, e), [r for r in ROWS if r["pos"] == p and era2(r["year"]) == e])
     for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK") for e in ("pre-2012", "2012-2015")])
run("AXIS 1d - BROAD GROUP x ERA (2-band)  [the pooling target for failed position x era cells]",
    [("%s x %s" % (g, e), [r for r in ROWS if r["pos"] in (TALL if g == "talls" else RUN)
                           and era2(r["year"]) == e])
     for g in ("talls", "runners") for e in ("pre-2012", "2012-2015")])
run("AXIS 2 - ND PICK BANDS",
    [("ND %s" % nm, [r for r in ROWS if nd(r) and lo <= r["pick"] <= hi])
     for nm, lo, hi in (("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40), ("41-64", 41, 64))])
run("AXIS 2b - ND PICK BANDS x ERA (2-band)",
    [("ND %s x %s" % (nm, e), [r for r in ROWS if nd(r) and lo <= r["pick"] <= hi and era2(r["year"]) == e])
     for nm, lo, hi in (("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40), ("41-64", 41, 64))
     for e in ("pre-2012", "2012-2015")])
run("AXIS 2c - ND PICK BANDS x BROAD GROUP",
    [("ND %s x %s" % (nm, g), [r for r in ROWS if nd(r) and lo <= r["pick"] <= hi
                               and r["pos"] in (TALL if g == "talls" else RUN)])
     for nm, lo, hi in (("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40), ("41-64", 41, 64))
     for g in ("talls", "runners")])
run("AXIS 3 - ROUTE",
    [("ND 1-64", [r for r in ROWS if nd(r)]),
     ("pool ALL", [r for r in ROWS if pool(r)]),
     ("pool RD", [r for r in ROWS if r["typ"] == "RD"]),
     ("pool IRE", [r for r in ROWS if r["typ"] == "IRE"]),
     ("pool MSD", [r for r in ROWS if r["typ"] == "MSD"]),
     ("pool SSP", [r for r in ROWS if r["typ"] == "SSP"]),
     ("pool UNR", [r for r in ROWS if r["typ"] == "UNR"]),
     ("pool PDA/PDN/PDS", [r for r in ROWS if r["typ"] in ("PDA", "PDN", "PDS")]),
     ("pool ND (real pick>64)", [r for r in ROWS if r["typ"] == "ND" and r["is_pool"]]),
     ("pool non-RD (all others)", [r for r in ROWS if pool(r) and r["typ"] != "RD"]),
     ])
run("AXIS 3b - ROUTE x BROAD GROUP",
    [("%s x %s" % (t, g), [r for r in ROWS if (nd(r) if t == "ND1-64" else
                                               (r["typ"] == "RD" if t == "poolRD" else
                                                (pool(r) and r["typ"] != "RD")))
                           and r["pos"] in (TALL if g == "talls" else RUN)])
     for t in ("ND1-64", "poolRD", "pool-nonRD") for g in ("talls", "runners")])
run("AXIS 4 - DRAFT-AGE BANDS",
    [("young <=20 (all routes)", [r for r in ROWS if r["age"] is not None and r["age"] <= 20]),
     ("mature 21+ (all routes)", [r for r in ROWS if r["age"] is not None and r["age"] >= 21]),
     ("age UNKNOWN", [r for r in ROWS if r["age"] is None]),
     ("ND1-64 young <=20", [r for r in ROWS if nd(r) and r["age"] is not None and r["age"] <= 20]),
     ("ND1-64 mature 21+", [r for r in ROWS if nd(r) and r["age"] is not None and r["age"] >= 21]),
     ("pool young <=20", [r for r in ROWS if pool(r) and r["age"] is not None and r["age"] <= 20]),
     ("pool mature 21+", [r for r in ROWS if pool(r) and r["age"] is not None and r["age"] >= 21]),
     ("pool RD mature 21+", [r for r in ROWS if r["typ"] == "RD" and r["age"] is not None and r["age"] >= 21]),
     ("pool RD young <=20", [r for r in ROWS if r["typ"] == "RD" and r["age"] is not None and r["age"] <= 20]),
     ("pool non-RD mature 21+", [r for r in ROWS if pool(r) and r["typ"] != "RD" and r["age"] is not None and r["age"] >= 21]),
     ("mature 21+ x talls", [r for r in ROWS if r["age"] is not None and r["age"] >= 21 and r["pos"] in TALL]),
     ("mature 21+ x runners", [r for r in ROWS if r["age"] is not None and r["age"] >= 21 and r["pos"] in RUN]),
     ("young <=20 x talls", [r for r in ROWS if r["age"] is not None and r["age"] <= 20 and r["pos"] in TALL]),
     ("young <=20 x runners", [r for r in ROWS if r["age"] is not None and r["age"] <= 20 and r["pos"] in RUN]),
     ])
EL = [r for r in ROWS if eligible_dip(r)]
run("AXIS 5 - THE DIP CUT (did the year-4 price see through a year-4 dip?)",
    [("dip-eligible base (yrs 3&5 seen)", EL),
     ("DIP-A strict  sp4<0.8*min(sp3,sp5)", [r for r in EL if dipA(r)]),
     ("NO DIP-A (complement)", [r for r in EL if not dipA(r)]),
     ("DIP-B broad   sp4<0.8*max(sp3,sp5)", [r for r in EL if dipB(r)]),
     ("NO DIP-B (complement)", [r for r in EL if not dipB(r)]),
     ("DIP-G games   g4<0.6*min(g3,g5)", [r for r in EL if dipG(r)]),
     ("NO DIP-G (complement)", [r for r in EL if not dipG(r)]),
     ("DIP-G80 games g4<0.8*min(g3,g5)", [r for r in EL if r["g4"] < 0.80 * min(r["g3"], r["g5"])]),
     ("NO DIP-G80 (complement)", [r for r in EL if not r["g4"] < 0.80 * min(r["g3"], r["g5"])]),
     ("DIP-A x talls", [r for r in EL if dipA(r) and r["pos"] in TALL]),
     ("DIP-A x runners", [r for r in EL if dipA(r) and r["pos"] in RUN]),
     ("DIP-B x pre-2012", [r for r in EL if dipB(r) and era2(r["year"]) == "pre-2012"]),
     ("DIP-B x 2012-2015", [r for r in EL if dipB(r) and era2(r["year"]) == "2012-2015"]),
     ("DIP-B x talls", [r for r in EL if dipB(r) and r["pos"] in TALL]),
     ("DIP-B x runners", [r for r in EL if dipB(r) and r["pos"] in RUN]),
     ("DIP-B x ND1-64", [r for r in EL if dipB(r) and nd(r)]),
     ])

print()
print("=" * 120)
print("HEADLINE — NAMED CELLS RANKED BY |tilt - 1|  (where the ruler is least straight)")
print("-" * 120)
print("   %-52s %7s %8s %8s %6s" % ("cell", "eff-n", "TILT", "1/tilt", "rel"))
seen = set()
for axis, nm, c in sorted(NAMED, key=lambda t: -abs(t[2]["tilt"] - 1.0)):
    k = nm
    if k in seen: continue
    seen.add(k)
    print("   %-52s %7.1f %8.4f %8.4f %6.2f" % ("%s" % nm, c["effn"], c["tilt"], c["corr"], c["rel"]))

json.dump(dict(window=[CLO, CHI], overall=OVERALL, bar=BAR, nboot=NB, axes=OUT),
          open(SP + "/r13_map.json", "w"), indent=1)
print()
print("wrote", SP + "/r13_map.json")
