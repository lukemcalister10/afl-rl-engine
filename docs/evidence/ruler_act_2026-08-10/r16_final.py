"""FINAL DELIVERABLE TABLES — correction factors for the NAMED cells, plus the variant sensitivity
band on every named cell, plus the age-axis fair base.  READ-ONLY."""
import json
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json"))
ROWS = [r for r in D["rows"] if 2004 <= r["year"] <= 2015]
NB = 20000; BARN = 35.0
rng = np.random.default_rng(20260810)
nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")
era2 = lambda y: "pre-2012" if y <= 2011 else "2012-2015"
el = lambda r: r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
dipG80 = lambda r: el(r) and r["g4"] < 0.80 * min(r["g3"], r["g5"])

VAR = [("headline", lambda x: x["real4"] + x["stub"]),
       ("ex-div(yr5+)", lambda x: x["real5"] + x["stub"]),
       ("eng disc 14%", lambda x: x["real4_eng"] + x["stub"]),
       ("no stub", lambda x: x["real4"]),
       ("KEY105", lambda x: x["real4_key"] + x["stub"]),
       ("ex-2026", lambda x: x["real4_no26"] + x["stub"])]


def stat(rows):
    w = np.array([r["proxy"] for r in rows], float)
    P = w.sum()
    if P <= 0: return None
    effn = float(P ** 2 / (w ** 2).sum())
    out = {}
    for nm, f in VAR:
        out[nm] = float(sum(f(r) for r in rows) / P)
    n = len(rows)
    num = np.array([r["real4"] + r["stub"] for r in rows], float)
    idx = rng.integers(0, n, size=(NB, n))
    bp = num[idx].sum(1) / np.maximum(w[idx].sum(1), 1e-9)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gn = np.array([num[g].sum() for g in gs]); gd = np.array([w[g].sum() for g in gs])
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    bc = gn[gi].sum(1) / np.maximum(gd[gi].sum(1), 1e-9)
    lo = min(np.percentile(bp, 2.5), np.percentile(bc, 2.5))
    hi = max(np.percentile(bp, 97.5), np.percentile(bc, 97.5))
    return dict(n=n, effn=effn, tilt=out["headline"], var=out,
                ci=[float(lo), float(hi)],
                stub=float(sum(r["stub"] for r in rows) / max(sum(r["real4"] + r["stub"] for r in rows), 1e-9)),
                named=effn >= BARN)


CELLS = [
    ("OVERALL (the whole population)", ROWS),
    ("-- broad group --", None),
    ("talls (KPF/KPD/RUCK)", [r for r in ROWS if r["pos"] in TALL]),
    ("runners (MID/SD/SF)", [r for r in ROWS if r["pos"] in RUN]),
    ("-- position --", None),
    ("MID", [r for r in ROWS if r["pos"] == "MID"]),
    ("SD", [r for r in ROWS if r["pos"] == "SD"]),
    ("SF", [r for r in ROWS if r["pos"] == "SF"]),
    ("KPD", [r for r in ROWS if r["pos"] == "KPD"]),
    ("KPF  [BELOW BAR eff-n 33.8]", [r for r in ROWS if r["pos"] == "KPF"]),
    ("RUCK [BELOW BAR eff-n 24.7]", [r for r in ROWS if r["pos"] == "RUCK"]),
    ("-- era --", None),
    ("pre-2012 (classes 2004-2011)", [r for r in ROWS if era2(r["year"]) == "pre-2012"]),
    ("2012-2015", [r for r in ROWS if era2(r["year"]) == "2012-2015"]),
    ("-- position x era, named only --", None),
    ("MID x pre-2012", [r for r in ROWS if r["pos"] == "MID" and era2(r["year"]) == "pre-2012"]),
    ("SD x pre-2012", [r for r in ROWS if r["pos"] == "SD" and era2(r["year"]) == "pre-2012"]),
    ("SF x pre-2012", [r for r in ROWS if r["pos"] == "SF" and era2(r["year"]) == "pre-2012"]),
    ("KPD x pre-2012", [r for r in ROWS if r["pos"] == "KPD" and era2(r["year"]) == "pre-2012"]),
    ("talls x pre-2012", [r for r in ROWS if r["pos"] in TALL and era2(r["year"]) == "pre-2012"]),
    ("runners x pre-2012", [r for r in ROWS if r["pos"] in RUN and era2(r["year"]) == "pre-2012"]),
    ("runners x 2012-2015", [r for r in ROWS if r["pos"] in RUN and era2(r["year"]) == "2012-2015"]),
    ("-- ND pick bands --", None),
    ("ND 1-10", [r for r in ROWS if nd(r) and r["pick"] <= 10]),
    ("ND 11-20", [r for r in ROWS if nd(r) and 11 <= r["pick"] <= 20]),
    ("ND 21-40", [r for r in ROWS if nd(r) and 21 <= r["pick"] <= 40]),
    ("ND 41-64", [r for r in ROWS if nd(r) and 41 <= r["pick"] <= 64]),
    ("-- route --", None),
    ("ND 1-64", [r for r in ROWS if nd(r)]),
    ("pool ALL", [r for r in ROWS if pool(r)]),
    ("pool RD", [r for r in ROWS if r["typ"] == "RD"]),
    ("-- draft age (classes 2006-2015 only: 2004-05 carry no DOB) --", None),
    ("age-axis base (age known)", [r for r in ROWS if r["age"] is not None]),
    ("young <=20", [r for r in ROWS if r["age"] is not None and r["age"] <= 20]),
    ("mature 21+  [BELOW BAR eff-n 30.8]", [r for r in ROWS if r["age"] is not None and r["age"] >= 21]),
    ("pool young <=20", [r for r in ROWS if pool(r) and r["age"] is not None and r["age"] <= 20]),
    ("pool mature 21+ [BELOW BAR 21.9]", [r for r in ROWS if pool(r) and r["age"] is not None and r["age"] >= 21]),
    ("age UNKNOWN (classes 2004-05)", [r for r in ROWS if r["age"] is None]),
    ("-- the dip cut --", None),
    ("dip-eligible base", [r for r in ROWS if el(r)]),
    ("DIP-B (sp4 < 0.8*max(sp3,sp5))", [r for r in ROWS if dipB(r)]),
    ("NO DIP-B", [r for r in ROWS if el(r) and not dipB(r)]),
    ("DIP-G80 (g4 < 0.8*min(g3,g5))", [r for r in ROWS if dipG80(r)]),
    ("NO DIP-G80", [r for r in ROWS if el(r) and not dipG80(r)]),
]

print("=" * 132)
print("PER-CELL CORRECTION FACTORS (1/tilt) AND THE VARIANT SENSITIVITY BAND")
print("The factor is what the composition sitting would MULTIPLY an F-based magnitude by to restate it")
print("in realized-career terms.  '95% CI' is the union of the player-resampled and class-clustered")
print("bootstrap intervals on TILT (20,000 reps each).  Variant columns are 1/tilt under each")
print("alternative numerator convention -- the band, not the point, is the honest object.")
print("=" * 132)
hdr = ("  %-38s %5s %7s %7s %8s %-15s | %s" %
       ("cell", "n", "eff-n", "TILT", "1/tilt", "95% CI (tilt)",
        "  ".join("%-12s" % v[0] for v in VAR[1:])))
print(hdr); print("  " + "-" * (len(hdr) - 2))
OUT = {}
for nm, rs in CELLS:
    if rs is None:
        print("  %s" % nm); continue
    s = stat(rs)
    if s is None: continue
    OUT[nm] = s
    fl = " " if s["named"] else "*"
    print("  %s%-37s %5d %7.1f %8.4f %8.4f [%5.3f,%5.3f] | %s" %
          (fl, nm, s["n"], s["effn"], s["tilt"], 1 / s["tilt"], s["ci"][0], s["ci"][1],
           "  ".join("%-12.3f" % (1 / s["var"][v[0]]) for v in VAR[1:])))
print()
print("  * = BELOW THE F8 BAR (Kish eff-n < 35 on the cell's own denominator weights) -- NOT a named cell.")
json.dump(OUT, open(SP + "/r16_final.json", "w"), indent=1)
print("wrote", SP + "/r16_final.json")
