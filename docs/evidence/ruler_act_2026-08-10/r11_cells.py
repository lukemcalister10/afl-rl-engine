"""TILT MAP CELLS — F8 discipline: Kish eff-n >= 35 on the cell's own denominator weights,
plus 20,000-rep bootstrap CI in two variants (player-resampled and draft-class-clustered).
READ-ONLY.  Reads r10_rows.json, writes r11_cells.json + prints every table.
"""
import json, math
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json"))
ROWS = D["rows"]
NB = 20000
BAR = 35.0
rng = np.random.default_rng(20260810)

OVERALL = sum(x["realized"] for x in ROWS) / sum(x["proxy"] for x in ROWS)


def cell(rows):
    if not rows: return None
    w = np.array([r["proxy"] for r in rows], float)
    num = np.array([r["realized"] for r in rows], float)
    stub = np.array([r["stub"] for r in rows], float)
    P = w.sum()
    if P <= 0: return None
    effn = (w.sum() ** 2) / (w ** 2).sum()
    tilt = num.sum() / P
    # player-resampled bootstrap
    n = len(rows)
    idx = rng.integers(0, n, size=(NB, n))
    bp = num[idx].sum(1) / np.maximum(w[idx].sum(1), 1e-9)
    lo_p, hi_p = np.percentile(bp, [2.5, 97.5])
    # class-clustered bootstrap
    yrs = np.array([r["year"] for r in rows])
    uy = np.unique(yrs)
    groups = [np.where(yrs == y)[0] for y in uy]
    gnum = np.array([num[g].sum() for g in groups])
    gden = np.array([w[g].sum() for g in groups])
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    bc = gnum[gi].sum(1) / np.maximum(gden[gi].sum(1), 1e-9)
    lo_c, hi_c = np.percentile(bc, [2.5, 97.5])
    return dict(n=n, n_weighted=int((w > 0).sum()), effn=float(effn), tilt=float(tilt),
                corr=float(1.0 / tilt) if tilt > 0 else None,
                rel=float(tilt / OVERALL),
                ci_player=[float(lo_p), float(hi_p)], ci_class=[float(lo_c), float(hi_c)],
                stub_share=float(stub.sum() / num.sum()) if num.sum() > 0 else 0.0,
                sum_proxy=float(P), sum_real=float(num.sum()),
                named=bool(effn >= BAR))


def show(title, cells):
    print()
    print("=" * 118)
    print(title)
    print("-" * 118)
    print("  %-34s %5s %6s %7s %8s %8s   %-17s %-17s %6s" %
          ("cell", "n", "n_wt", "eff-n", "TILT", "1/tilt", "CI player", "CI class-clust", "stub%"))
    for name, c in cells:
        if c is None:
            print("  %-34s   (empty)" % name); continue
        flag = " " if c["named"] else "*"
        print("  %s%-33s %5d %6d %7.1f %8.4f %8.4f   [%6.3f,%6.3f] [%6.3f,%6.3f] %5.1f%%" %
              (flag, name, c["n"], c["n_weighted"], c["effn"], c["tilt"], c["corr"],
               c["ci_player"][0], c["ci_player"][1], c["ci_class"][0], c["ci_class"][1],
               100 * c["stub_share"]))
    print("  (* = BELOW BAR: Kish eff-n < 35 -- not a named cell)")


OUT = {}


def run(axis, cells):
    res = [(nm, cell(rs)) for nm, rs in cells]
    show(axis, res)
    OUT[axis] = {nm: c for nm, c in res}
    return res


ALL = ROWS
nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")


def era(y): return "pre-2012" if y <= 2011 else ("2012-2017" if y <= 2017 else "2018+")


print("BASIS: stage5 walk-forward matrix %s | store %s | engine %s" %
      (D["meta"]["matrix"], D["meta"]["store"], D["meta"]["engine_head"]))
print("population n=%d  (classes %d-%d)  OVERALL TILT = %.4f  correction 1/tilt = %.4f"
      % (len(ROWS), D["meta"]["window"][0], D["meta"]["window"][1], OVERALL, 1 / OVERALL))

run("AXIS 0 - OVERALL and broad group", [
    ("ALL", ALL),
    ("talls (KPF/KPD/RUCK)", [r for r in ALL if r["pos"] in TALL]),
    ("runners (MID/SD/SF)", [r for r in ALL if r["pos"] in RUN]),
    ("ND 1-64", [r for r in ALL if nd(r)]),
    ("pool (all routes)", [r for r in ALL if pool(r)]),
])

run("AXIS 1a - POSITION (whole population)",
    [(p, [r for r in ALL if r["pos"] == p]) for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK")])

run("AXIS 1b - ERA (draft class)",
    [(e, [r for r in ALL if era(r["year"]) == e]) for e in ("pre-2012", "2012-2017", "2018+")])

run("AXIS 1c - POSITION x ERA",
    [("%s x %s" % (p, e), [r for r in ALL if r["pos"] == p and era(r["year"]) == e])
     for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK") for e in ("pre-2012", "2012-2017", "2018+")])

run("AXIS 1d - BROAD GROUP x ERA",
    [("%s x %s" % (g, e), [r for r in ALL if (r["pos"] in (TALL if g == "talls" else RUN))
                           and era(r["year"]) == e])
     for g in ("talls", "runners") for e in ("pre-2012", "2012-2017", "2018+")])

run("AXIS 2 - ND PICK BANDS",
    [("ND %s" % nm, [r for r in ALL if nd(r) and lo <= r["pick"] <= hi])
     for nm, lo, hi in (("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40), ("41-64", 41, 64))])

run("AXIS 2b - ND PICK BANDS x ERA",
    [("ND %s x %s" % (nm, e), [r for r in ALL if nd(r) and lo <= r["pick"] <= hi and era(r["year"]) == e])
     for nm, lo, hi in (("1-10", 1, 10), ("11-20", 11, 20), ("21-40", 21, 40), ("41-64", 41, 64))
     for e in ("pre-2012", "2012-2017", "2018+")])

run("AXIS 3 - ROUTE",
    [("ND 1-64", [r for r in ALL if nd(r)]),
     ("pool ALL", [r for r in ALL if pool(r)]),
     ("pool RD", [r for r in ALL if r["typ"] == "RD"]),
     ("pool IRE", [r for r in ALL if r["typ"] == "IRE"]),
     ("pool MSD", [r for r in ALL if r["typ"] == "MSD"]),
     ("pool SSP", [r for r in ALL if r["typ"] == "SSP"]),
     ("pool UNR", [r for r in ALL if r["typ"] == "UNR"]),
     ("pool PDA/PDN/PDS", [r for r in ALL if r["typ"] in ("PDA", "PDN", "PDS")]),
     ("pool ND (pick>64)", [r for r in ALL if r["typ"] == "ND" and r["is_pool"]]),
     ])

run("AXIS 4 - DRAFT-AGE BANDS",
    [("young <=20 (all)", [r for r in ALL if r["age"] is not None and r["age"] <= 20]),
     ("mature 21+ (all)", [r for r in ALL if r["age"] is not None and r["age"] >= 21]),
     ("age unknown", [r for r in ALL if r["age"] is None]),
     ("ND1-64 young <=20", [r for r in ALL if nd(r) and r["age"] is not None and r["age"] <= 20]),
     ("ND1-64 mature 21+", [r for r in ALL if nd(r) and r["age"] is not None and r["age"] >= 21]),
     ("pool young <=20", [r for r in ALL if pool(r) and r["age"] is not None and r["age"] <= 20]),
     ("pool mature 21+", [r for r in ALL if pool(r) and r["age"] is not None and r["age"] >= 21]),
     ("pool RD mature 21+", [r for r in ALL if r["typ"] == "RD" and r["age"] is not None and r["age"] >= 21]),
     ("pool RD young <=20", [r for r in ALL if r["typ"] == "RD" and r["age"] is not None and r["age"] <= 20]),
     ("pool non-RD mature 21+", [r for r in ALL if pool(r) and r["typ"] != "RD"
                                 and r["age"] is not None and r["age"] >= 21]),
     ])

run("AXIS 4b - DRAFT-AGE x BROAD GROUP",
    [("%s x %s" % (a, g), [r for r in ALL if r["age"] is not None
                           and ((r["age"] <= 20) if a == "young<=20" else (r["age"] >= 21))
                           and r["pos"] in (TALL if g == "talls" else RUN)])
     for a in ("young<=20", "mature21+") for g in ("talls", "runners")])

json.dump(dict(overall=OVERALL, bar=BAR, nboot=NB, axes=OUT), open(SP + "/r11_cells.json", "w"), indent=1)
print()
print("wrote", SP + "/r11_cells.json")
