"""DIP CROSS-TAB: form-dip vs availability-dip, disentangled. READ-ONLY."""
import json
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json"))
ROWS = [r for r in D["rows"] if 2004 <= r["year"] <= 2015]
rng = np.random.default_rng(20260810); NB = 20000
el = lambda r: r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
dipG = lambda r: el(r) and r["g4"] < 0.80 * min(r["g3"], r["g5"])
EL = [r for r in ROWS if el(r)]


def c(rows):
    w = np.array([r["proxy"] for r in rows], float); num = np.array([r["realized"] for r in rows], float)
    P = w.sum(); effn = P ** 2 / (w ** 2).sum(); t = num.sum() / P
    n = len(rows); idx = rng.integers(0, n, size=(NB, n))
    bp = num[idx].sum(1) / np.maximum(w[idx].sum(1), 1e-9)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gn = np.array([num[g].sum() for g in gs]); gd = np.array([w[g].sum() for g in gs])
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    bc = gn[gi].sum(1) / np.maximum(gd[gi].sum(1), 1e-9)
    return n, effn, t, min(np.percentile(bp, 2.5), np.percentile(bc, 2.5)), \
        max(np.percentile(bp, 97.5), np.percentile(bc, 97.5))


print("=" * 104)
print("DIP CROSS-TAB — a FORM dip and an AVAILABILITY dip are different objects")
print("  form dip     = sp4 < 0.80*max(sp3,sp5) but games held (NOT g4 < 0.80*min(g3,g5))")
print("  availability = g4 < 0.80*min(g3,g5)")
print("=" * 104)
print("  %-40s %5s %7s %8s %8s %-15s" % ("cell", "n", "eff-n", "TILT", "1/tilt", "95% CI"))
for nm, rs in (("dip-eligible base", EL),
               ("no dip at all", [r for r in EL if not dipB(r) and not dipG(r)]),
               ("FORM dip only (games held)", [r for r in EL if dipB(r) and not dipG(r)]),
               ("AVAILABILITY dip (g4<0.8*min)", [r for r in EL if dipG(r)]),
               ("  of which also a form dip", [r for r in EL if dipG(r) and dipB(r)]),
               ("  availability dip, form held", [r for r in EL if dipG(r) and not dipB(r)])):
    if not rs: print("  %-40s (empty)" % nm); continue
    n, e, t, lo, hi = c(rs)
    fl = " " if e >= 35 else "*"
    print("  %s%-39s %5d %7.1f %8.4f %8.4f [%5.3f,%5.3f]" % (fl, nm, n, e, t, 1 / t, lo, hi))
print("  (* below the eff-n 35 bar)")
