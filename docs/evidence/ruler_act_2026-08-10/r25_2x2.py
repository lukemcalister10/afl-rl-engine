"""THE 2x2 ACROSS THE NAMED CELLS + the four-instrument bend-survival ledger.

PAIRED BOOTSTRAP: one resample draw per cell, reused across all four instruments, so the four
columns' intervals are directly comparable (the same players/classes are in or out of every rep).
20,000 reps, player-resampled and draft-class-clustered; CI reported as the union.
PROXY is identical in all four -> Kish eff-n is identical in all four (asserted).
Cell membership frozen at the landed definitions.  READ-ONLY.
"""
import json
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r24_rows.json"))
ROWS = D["rows"]
NB = 20000; BARN = 35.0
rng = np.random.default_rng(20260810)
KEYS = [("A", "A_av_full", "full x avail"), ("B", "B_rt_full", "full x rate"),
        ("C", "C_av_win", "yr11 x avail"), ("D", "D_rt_win", "yr11 x rate")]

nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")
era2 = lambda y: "pre-2012" if y <= 2011 else "2012-2015"
el = lambda r: r["g3"] >= 1 and r["g5"] >= 1
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
dipG = lambda r: el(r) and r["g4"] < 0.80 * min(r["g3"], r["g5"])
OV = {k: sum(r[f] for r in ROWS) / sum(r["proxy"] for r in ROWS) for k, f, _ in KEYS}


def cell(rows):
    w = np.array([r["proxy"] for r in rows], float)
    P = w.sum()
    if P <= 0: return None
    effn = float(P ** 2 / (w ** 2).sum())
    n = len(rows)
    idx = rng.integers(0, n, size=(NB, n))              # ONE draw, reused by all four
    wb = w[idx].sum(1)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    gd = np.array([w[g].sum() for g in gs]); gdb = gd[gi].sum(1)
    out = {}
    for k, f, _ in KEYS:
        num = np.array([r[f] for r in rows], float)
        t = float(num.sum() / P)
        bp = num[idx].sum(1) / np.maximum(wb, 1e-9)
        gn = np.array([num[g].sum() for g in gs])
        bc = gn[gi].sum(1) / np.maximum(gdb, 1e-9)
        lo = float(min(np.percentile(bp, 2.5), np.percentile(bc, 2.5)))
        hi = float(max(np.percentile(bp, 97.5), np.percentile(bc, 97.5)))
        out[k] = dict(tilt=t, corr=1.0 / t, ci=[lo, hi], bend=(1.0 / t) / (1.0 / OV[k]))
    return dict(n=n, effn=effn, named=effn >= BARN, inst=out)


CELLS = [
    ("OVERALL", ROWS),
    ("talls (KPF/KPD/RUCK)", [r for r in ROWS if r["pos"] in TALL]),
    ("runners (MID/SD/SF)", [r for r in ROWS if r["pos"] in RUN]),
    ("MID", [r for r in ROWS if r["pos"] == "MID"]),
    ("SD", [r for r in ROWS if r["pos"] == "SD"]),
    ("SF", [r for r in ROWS if r["pos"] == "SF"]),
    ("KPD", [r for r in ROWS if r["pos"] == "KPD"]),
    ("KPF  [below bar]", [r for r in ROWS if r["pos"] == "KPF"]),
    ("RUCK [below bar]", [r for r in ROWS if r["pos"] == "RUCK"]),
    ("pre-2012 (2004-2011)", [r for r in ROWS if era2(r["year"]) == "pre-2012"]),
    ("2012-2015", [r for r in ROWS if era2(r["year"]) == "2012-2015"]),
    ("2004-2009", [r for r in ROWS if r["year"] <= 2009]),
    ("2010-2012", [r for r in ROWS if 2010 <= r["year"] <= 2012]),
    ("2013-2015", [r for r in ROWS if r["year"] >= 2013]),
    ("MID x pre-2012", [r for r in ROWS if r["pos"] == "MID" and era2(r["year"]) == "pre-2012"]),
    ("SD x pre-2012", [r for r in ROWS if r["pos"] == "SD" and era2(r["year"]) == "pre-2012"]),
    ("SF x pre-2012", [r for r in ROWS if r["pos"] == "SF" and era2(r["year"]) == "pre-2012"]),
    ("KPD x pre-2012", [r for r in ROWS if r["pos"] == "KPD" and era2(r["year"]) == "pre-2012"]),
    ("talls x pre-2012", [r for r in ROWS if r["pos"] in TALL and era2(r["year"]) == "pre-2012"]),
    ("runners x pre-2012", [r for r in ROWS if r["pos"] in RUN and era2(r["year"]) == "pre-2012"]),
    ("runners x 2012-2015", [r for r in ROWS if r["pos"] in RUN and era2(r["year"]) == "2012-2015"]),
    ("ND 1-10", [r for r in ROWS if nd(r) and r["pick"] <= 10]),
    ("ND 11-20", [r for r in ROWS if nd(r) and 11 <= r["pick"] <= 20]),
    ("ND 21-40", [r for r in ROWS if nd(r) and 21 <= r["pick"] <= 40]),
    ("ND 41-64", [r for r in ROWS if nd(r) and 41 <= r["pick"] <= 64]),
    ("ND 21-40 x runners", [r for r in ROWS if nd(r) and 21 <= r["pick"] <= 40 and r["pos"] in RUN]),
    ("ND 1-10 x runners", [r for r in ROWS if nd(r) and r["pick"] <= 10 and r["pos"] in RUN]),
    ("ND 11-20 x runners", [r for r in ROWS if nd(r) and 11 <= r["pick"] <= 20 and r["pos"] in RUN]),
    ("ND 41-64 x runners", [r for r in ROWS if nd(r) and 41 <= r["pick"] <= 64 and r["pos"] in RUN]),
    ("ND 1-64 x talls (pooled)", [r for r in ROWS if nd(r) and r["pos"] in TALL]),
    ("ND 1-64", [r for r in ROWS if nd(r)]),
    ("pool ALL", [r for r in ROWS if pool(r)]),
    ("pool RD", [r for r in ROWS if r["typ"] == "RD"]),
    ("poolRD x runners", [r for r in ROWS if r["typ"] == "RD" and r["pos"] in RUN]),
    ("dip-eligible base", [r for r in ROWS if el(r)]),
    ("no dip at all", [r for r in ROWS if el(r) and not dipB(r) and not dipG(r)]),
    ("FORM dip only (games held)", [r for r in ROWS if el(r) and dipB(r) and not dipG(r)]),
    ("AVAILABILITY dip", [r for r in ROWS if dipG(r)]),
    ("DIP-B broad", [r for r in ROWS if dipB(r)]),
    ("NO DIP-B", [r for r in ROWS if el(r) and not dipB(r)]),
    ("DIP-B x talls", [r for r in ROWS if dipB(r) and r["pos"] in TALL]),
    ("DIP-B x runners", [r for r in ROWS if dipB(r) and r["pos"] in RUN]),
]

print("=" * 132)
print("THE 2x2 ACROSS THE NAMED CELLS -- correction factor 1/tilt under each instrument")
print("  A = full-horizon x availability-in (LANDED)   B = full-horizon x rate T=6")
print("  C = year-11-capped x availability-in          D = year-11-capped x rate T=6")
for k, f, lab in KEYS:
    print("  overall %s (%-13s): tilt %.4f  1/tilt %.4f" % (k, lab, OV[k], 1 / OV[k]))
print("=" * 132)
hd = ("  %-32s %5s %7s | %7s %7s %7s %7s | %-15s" %
      ("cell", "n", "eff-n", "A", "B", "C", "D", "95% CI on D (tilt)"))
print(hd); print("  " + "-" * (len(hd) - 2))
OUT = {}
for nm, rs in CELLS:
    c = cell(rs)
    if c is None: continue
    OUT[nm] = c
    fl = " " if c["named"] else "*"
    print("  %s%-31s %5d %7.1f | %7.4f %7.4f %7.4f %7.4f | [%5.3f,%5.3f]" %
          (fl, nm, c["n"], c["effn"], c["inst"]["A"]["corr"], c["inst"]["B"]["corr"],
           c["inst"]["C"]["corr"], c["inst"]["D"]["corr"],
           c["inst"]["D"]["ci"][0], c["inst"]["D"]["ci"][1]))
print("  * = below the F8 bar (eff-n < 35); eff-n identical across all four (PROXY untouched).")

print()
print("=" * 132)
print("BEND-SURVIVAL LEDGER ACROSS ALL FOUR INSTRUMENTS")
print("  bend = the cell's 1/tilt divided by the OVERALL 1/tilt on the SAME instrument (level")
print("  divides out).  A cell the sitting can act on is one whose bend holds on ALL FOUR.")
print("  RULE: 'material' = |bend-1| >= 0.10 ; 'holds' = material on all four with the same sign.")
print("=" * 132)
print("  %-32s %7s | %7s %7s %7s %7s | %s" % ("named cell", "eff-n", "bendA", "bendB", "bendC", "bendD", "verdict"))
print("  " + "-" * 118)
rank = [(nm, c) for nm, c in OUT.items() if c["named"] and nm != "OVERALL"]
survivors = []
for nm, c in sorted(rank, key=lambda t: -abs(t[1]["inst"]["D"]["bend"] - 1.0)):
    b = [c["inst"][k]["bend"] for k, _, _ in KEYS]
    mats = [abs(x - 1) >= 0.10 for x in b]
    signs = {(x > 1) for x in b}
    if all(mats) and len(signs) == 1:
        verd = "HOLDS ON ALL FOUR"; survivors.append((nm, c))
    elif not any(mats): verd = "no material bend on any"
    elif mats[0] and not mats[3]: verd = "fades out (gone by D)"
    elif not mats[0] and mats[3]: verd = "EMERGES only under D"
    else: verd = "partial (%s)" % "".join("X" if m else "." for m in mats)
    print("  %-32s %7.1f | %7.3f %7.3f %7.3f %7.3f | %s" % (nm, c["effn"], b[0], b[1], b[2], b[3], verd))
print()
print("  CELLS THE SITTING CAN ACT ON (bend material and same-signed on all four instruments):")
for nm, c in survivors:
    print("     %-32s  1/tilt A %.3f -> D %.3f   bend D %.3f  eff-n %.1f" %
          (nm, c["inst"]["A"]["corr"], c["inst"]["D"]["corr"], c["inst"]["D"]["bend"], c["effn"]))
if not survivors: print("     (none)")

json.dump(dict(overall=OV, cells=OUT), open(SP + "/r25_2x2.json", "w"), indent=1)
print()
print("wrote", SP + "/r25_2x2.json")
