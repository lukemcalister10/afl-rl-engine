"""SIDE-BY-SIDE DELIVERABLE — availability-in (landed) vs REALIZED-RATE (owner's economics).

CELL MEMBERSHIP IS HELD FIXED at the landed definitions -- including the dip classifier, which is
still computed on availability-based season prices.  A classifier is not a numerator: holding it
fixed is what makes the two columns comparable, so the ONLY thing that changes between them is how
a delivered season is priced.

Kish eff-n depends only on the denominator weights (PROXY), which are untouched -- asserted, not
assumed.  Same F8 bar (eff-n >= 35), same poolings, same caveats.
READ-ONLY.
"""
import json
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r20_rows.json"))
ROWS = [r for r in D["rows"] if 2004 <= r["year"] <= 2015]
LAND = {(x["key"], x["typ"], x["year"]): x for x in json.load(open(SP + "/r10_rows.json"))["rows"]}
NB = 20000; BARN = 35.0; T = "6"; BAND = ["10", "13"]
rng = np.random.default_rng(20260810)

nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")
era2 = lambda y: "pre-2012" if y <= 2011 else "2012-2015"
el = lambda r: r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
dipG = lambda r: el(r) and r["g4"] < 0.80 * min(r["g3"], r["g5"])

OV_AV = sum(r["realized"] for r in ROWS) / sum(r["proxy"] for r in ROWS)
OV_RT = sum(r["rate"][T] + r["stub"] for r in ROWS) / sum(r["proxy"] for r in ROWS)


def boot(w, num):
    n = len(w)
    idx = rng.integers(0, n, size=(NB, n))
    bp = num[idx].sum(1) / np.maximum(w[idx].sum(1), 1e-9)
    return float(np.percentile(bp, 2.5)), float(np.percentile(bp, 97.5))


def cell(rows):
    w = np.array([r["proxy"] for r in rows], float)
    P = w.sum()
    if P <= 0: return None
    effn = float(P ** 2 / (w ** 2).sum())
    nav = np.array([r["realized"] for r in rows], float)
    nrt = np.array([r["rate"][T] + r["stub"] for r in rows], float)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))

    def clus(num):
        gn = np.array([num[g].sum() for g in gs]); gd = np.array([w[g].sum() for g in gs])
        b = gn[gi].sum(1) / np.maximum(gd[gi].sum(1), 1e-9)
        return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
    lp, hp = boot(w, nrt); lc, hc = clus(nrt)
    return dict(n=len(rows), effn=effn,
                t_av=float(nav.sum() / P), t_rt=float(nrt.sum() / P),
                ci_rt=[min(lp, lc), max(hp, hc)],
                band={t: float(sum(r["rate"][t] + r["stub"] for r in rows) / P) for t in BAND},
                named=effn >= BARN)


CELLS = [
    ("OVERALL", ROWS),
    ("-- broad group --", None),
    ("talls (KPF/KPD/RUCK)", [r for r in ROWS if r["pos"] in TALL]),
    ("runners (MID/SD/SF)", [r for r in ROWS if r["pos"] in RUN]),
    ("-- position --", None),
    ("MID", [r for r in ROWS if r["pos"] == "MID"]),
    ("SD", [r for r in ROWS if r["pos"] == "SD"]),
    ("SF", [r for r in ROWS if r["pos"] == "SF"]),
    ("KPD", [r for r in ROWS if r["pos"] == "KPD"]),
    ("KPF  [below bar]", [r for r in ROWS if r["pos"] == "KPF"]),
    ("RUCK [below bar]", [r for r in ROWS if r["pos"] == "RUCK"]),
    ("-- era --", None),
    ("pre-2012 (2004-2011)", [r for r in ROWS if era2(r["year"]) == "pre-2012"]),
    ("2012-2015", [r for r in ROWS if era2(r["year"]) == "2012-2015"]),
    ("2004-2009", [r for r in ROWS if r["year"] <= 2009]),
    ("2010-2012", [r for r in ROWS if 2010 <= r["year"] <= 2012]),
    ("2013-2015", [r for r in ROWS if r["year"] >= 2013]),
    ("-- position x era (named) --", None),
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
    ("ND 21-40 x runners", [r for r in ROWS if nd(r) and 21 <= r["pick"] <= 40 and r["pos"] in RUN]),
    ("ND 1-10 x runners", [r for r in ROWS if nd(r) and r["pick"] <= 10 and r["pos"] in RUN]),
    ("ND 11-20 x runners", [r for r in ROWS if nd(r) and 11 <= r["pick"] <= 20 and r["pos"] in RUN]),
    ("ND 41-64 x runners", [r for r in ROWS if nd(r) and 41 <= r["pick"] <= 64 and r["pos"] in RUN]),
    ("ND 1-64 x talls (pooled)", [r for r in ROWS if nd(r) and r["pos"] in TALL]),
    ("-- route --", None),
    ("ND 1-64", [r for r in ROWS if nd(r)]),
    ("pool ALL", [r for r in ROWS if pool(r)]),
    ("pool RD", [r for r in ROWS if r["typ"] == "RD"]),
    ("poolRD x runners", [r for r in ROWS if r["typ"] == "RD" and r["pos"] in RUN]),
    ("-- the dip cut (membership FIXED at landed defs) --", None),
    ("dip-eligible base", [r for r in ROWS if el(r)]),
    ("no dip at all", [r for r in ROWS if el(r) and not dipB(r) and not dipG(r)]),
    ("FORM dip only (games held)", [r for r in ROWS if el(r) and dipB(r) and not dipG(r)]),
    ("AVAILABILITY dip g4<0.8*min", [r for r in ROWS if dipG(r)]),
    ("DIP-B broad", [r for r in ROWS if dipB(r)]),
    ("NO DIP-B", [r for r in ROWS if el(r) and not dipB(r)]),
    ("DIP-B x talls", [r for r in ROWS if dipB(r) and r["pos"] in TALL]),
    ("DIP-B x runners", [r for r in ROWS if dipB(r) and r["pos"] in RUN]),
]

print("=" * 134)
print("AVAILABILITY-IN (landed) vs REALIZED-RATE (owner's economics), headline threshold T=%s games" % T)
print("overall: availability-in tilt %.4f (1/tilt %.4f)  |  rate-based tilt %.4f (1/tilt %.4f)"
      % (OV_AV, 1 / OV_AV, OV_RT, 1 / OV_RT))
print("=" * 134)
hd = ("  %-34s %5s %7s | %7s %7s | %7s %7s %-15s | %6s %6s | %6s" %
      ("cell", "n", "eff-n", "tilt_av", "1/t_av", "tilt_rt", "1/t_rt", "95% CI (rate)",
       "T=10", "T=13", "d(1/t)"))
print(hd); print("  " + "-" * (len(hd) - 2))
OUT = {}
effn_moves = 0
for nm, rs in CELLS:
    if rs is None:
        print("  %s" % nm); continue
    c = cell(rs)
    if c is None: continue
    OUT[nm] = c
    # eff-n identity check against the landed row file
    wl = np.array([LAND[(r["key"], r["typ"], r["year"])]["proxy"] for r in rs], float)
    e_land = float(wl.sum() ** 2 / (wl ** 2).sum())
    if abs(e_land - c["effn"]) > 1e-9: effn_moves += 1
    fl = " " if c["named"] else "*"
    d = 1 / c["t_rt"] - 1 / c["t_av"]
    print("  %s%-33s %5d %7.1f | %7.4f %7.4f | %7.4f %7.4f [%5.3f,%5.3f] | %6.3f %6.3f | %+6.3f" %
          (fl, nm, c["n"], c["effn"], c["t_av"], 1 / c["t_av"], c["t_rt"], 1 / c["t_rt"],
           c["ci_rt"][0], c["ci_rt"][1],
           1 / c["band"]["10"], 1 / c["band"]["13"], d))
print()
print("  * = below the F8 bar (Kish eff-n < 35). eff-n cells that MOVED vs the landed weights: %d "
      "(expected 0; PROXY is untouched)." % effn_moves)

print()
print("=" * 134)
print("BEND SURVIVAL — named cells ranked by |1/tilt - overall 1/tilt| on the RATE basis")
print("  'bend' = the cell's factor divided by the overall factor on the SAME basis (the level")
print("  divides out, so this is the pure ruler-bend).  A cell whose bend collapses toward 1.00 on")
print("  the rate basis was an AVAILABILITY ARTEFACT; one that holds is a real bend.")
print("=" * 134)
print("  %-34s %7s | %8s %8s | %8s %8s | %s" %
      ("named cell", "eff-n", "bend_av", "bend_rt", "1/t_av", "1/t_rt", "verdict"))
print("  " + "-" * 122)
rank = [(nm, c) for nm, c in OUT.items() if c["named"] and not nm.startswith("--") and nm != "OVERALL"]
for nm, c in sorted(rank, key=lambda t: -abs((1 / t[1]["t_rt"]) / (1 / OV_RT) - 1.0)):
    b_av = (1 / c["t_av"]) / (1 / OV_AV); b_rt = (1 / c["t_rt"]) / (1 / OV_RT)
    shrink = (abs(b_rt - 1) - abs(b_av - 1)) / max(abs(b_av - 1), 1e-9)
    # A cell must HAVE a bend on the landed basis before "survives"/"collapsed" mean anything.
    if abs(b_av - 1) < 0.10 and abs(b_rt - 1) < 0.10: verd = "no material bend on either basis"
    elif abs(b_av - 1) < 0.10: verd = "EMERGES under rate (was masked by availability)"
    elif abs(b_rt - 1) < 0.05: verd = "COLLAPSED -> availability artefact"
    elif shrink < -0.30: verd = "shrank %.0f%% -> largely availability" % (-100 * shrink)
    elif shrink > 0.15: verd = "GREW %.0f%% -> masked by availability" % (100 * shrink)
    else: verd = "SURVIVES (bend held)"
    print("  %-34s %7.1f | %8.3f %8.3f | %8.3f %8.3f | %s"
          % (nm, c["effn"], b_av, b_rt, 1 / c["t_av"], 1 / c["t_rt"], verd))

json.dump(dict(T=T, band=BAND, overall_av=OV_AV, overall_rt=OV_RT, cells=OUT),
          open(SP + "/r21_sidebyside.json", "w"), indent=1)
print()
print("wrote", SP + "/r21_sidebyside.json")
