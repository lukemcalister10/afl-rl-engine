"""THE AGE AXIS RE-CUT on the DOB-written store, four-instrument basis. READ-ONLY.

BASIS SPLIT (enforced): every numerator/denominator comes from the act-branch artifact
(store 37ced3ce); ONLY the age field comes from the DOB store d9a24282 (main@064abcae).
Instruments, identical to the landed 2x2:
  A full-horizon x availability-in   B full-horizon x rate T=6
  C year-11-capped x availability    D year-11-capped x rate T=6
PROXY (= vpath[3]) is the denominator in all four, so Kish eff-n is identical across them.
F8 bar: eff-n >= 35. Paired bootstrap: one 20,000-rep draw per cell reused across all four columns,
player-resampled and draft-class-clustered, CI = the union.
"""
import json
import numpy as np
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
ROWS = json.load(open(SP + "/r24_rows.json"))["rows"]
AG = {r["key"]: r["age_new"] for r in json.load(open(SP + "/r36_ages.json"))}
for r in ROWS: r["age"] = AG.get(r["key"])
assert all(r["age"] is not None for r in ROWS), "unknown age remains"
NB = 20000; BARN = 35.0
rng = np.random.default_rng(20260810)
KEYS = [("A", "A_av_full"), ("B", "B_rt_full"), ("C", "C_av_win"), ("D", "D_rt_win")]
OV = {k: sum(r[f] for r in ROWS) / sum(r["proxy"] for r in ROWS) for k, f in KEYS}
nd = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
pool = lambda r: r["is_pool"]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")


def cell(rows):
    if not rows: return None
    w = np.array([r["proxy"] for r in rows], float); P = w.sum()
    if P <= 0: return None
    effn = float(P ** 2 / (w ** 2).sum()); n = len(rows)
    idx = rng.integers(0, n, size=(NB, n)); wb = w[idx].sum(1)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    gd = np.array([w[g].sum() for g in gs]); gdb = gd[gi].sum(1)
    out = {}
    for k, f in KEYS:
        num = np.array([r[f] for r in rows], float); t = float(num.sum() / P)
        bp = num[idx].sum(1) / np.maximum(wb, 1e-9)
        gn = np.array([num[g].sum() for g in gs]); bc = gn[gi].sum(1) / np.maximum(gdb, 1e-9)
        lo = float(min(np.percentile(bp, 2.5), np.percentile(bc, 2.5)))
        hi = float(max(np.percentile(bp, 97.5), np.percentile(bc, 97.5)))
        out[k] = dict(tilt=t, corr=1.0 / t, ci=[lo, hi], bend=(1.0 / t) / (1.0 / OV[k]))
    return dict(n=n, effn=effn, named=effn >= BARN, inst=out)


A = lambda r: r["age"]
CELLS = [
    ("age-axis base (ALL, age known)", ROWS),
    ("-- the headline split --", None),
    ("young <=20", [r for r in ROWS if A(r) <= 20]),
    ("mature 21+", [r for r in ROWS if A(r) >= 21]),
    ("-- finer bins --", None),
    ("<=18", [r for r in ROWS if A(r) <= 18]),
    ("19-20", [r for r in ROWS if 19 <= A(r) <= 20]),
    ("21-22", [r for r in ROWS if 21 <= A(r) <= 22]),
    ("23+", [r for r in ROWS if A(r) >= 23]),
    ("-- route x age --", None),
    ("ND1-64 young <=20", [r for r in ROWS if nd(r) and A(r) <= 20]),
    ("ND1-64 mature 21+", [r for r in ROWS if nd(r) and A(r) >= 21]),
    ("pool young <=20", [r for r in ROWS if pool(r) and A(r) <= 20]),
    ("pool mature 21+", [r for r in ROWS if pool(r) and A(r) >= 21]),
    ("pool RD young <=20", [r for r in ROWS if r["typ"] == "RD" and A(r) <= 20]),
    ("pool RD mature 21+", [r for r in ROWS if r["typ"] == "RD" and A(r) >= 21]),
    ("pool non-RD mature 21+", [r for r in ROWS if pool(r) and r["typ"] != "RD" and A(r) >= 21]),
    ("pool mature 21-22", [r for r in ROWS if pool(r) and 21 <= A(r) <= 22]),
    ("pool mature 23+", [r for r in ROWS if pool(r) and A(r) >= 23]),
    ("-- group x age --", None),
    ("young <=20 x talls", [r for r in ROWS if A(r) <= 20 and r["pos"] in TALL]),
    ("young <=20 x runners", [r for r in ROWS if A(r) <= 20 and r["pos"] in RUN]),
    ("mature 21+ x talls", [r for r in ROWS if A(r) >= 21 and r["pos"] in TALL]),
    ("mature 21+ x runners", [r for r in ROWS if A(r) >= 21 and r["pos"] in RUN]),
    ("-- the relabelled cell --", None),
    ("classes 2004-05 (was 'UNKNOWN')", [r for r in ROWS if r["year"] <= 2005]),
    ("classes 2004-05 x young<=20", [r for r in ROWS if r["year"] <= 2005 and A(r) <= 20]),
    ("classes 2006-2015", [r for r in ROWS if r["year"] >= 2006]),
    ("classes 2006-2015 x young<=20", [r for r in ROWS if r["year"] >= 2006 and A(r) <= 20]),
]

print("=" * 128)
print("AGE AXIS RE-CUT — DOB store d9a24282 (main@064abcae) for AGE ONLY; all values from the")
print("act-branch artifact (store 37ced3ce).  n=%d, age-UNKNOWN = 0." % len(ROWS))
for k, f in KEYS:
    print("  overall %s: tilt %.4f  1/tilt %.4f" % (k, OV[k], 1 / OV[k]))
print("=" * 128)
hd = ("  %-33s %5s %7s | %7s %7s %7s %7s | %-15s" %
      ("cell", "n", "eff-n", "1/t A", "1/t B", "1/t C", "1/t D", "95% CI on D (tilt)"))
print(hd); print("  " + "-" * (len(hd) - 2))
OUT = {}
for nm, rs in CELLS:
    if rs is None: print("  %s" % nm); continue
    c = cell(rs)
    if c is None: continue
    OUT[nm] = c
    fl = " " if c["named"] else "*"
    print("  %s%-32s %5d %7.1f | %7.4f %7.4f %7.4f %7.4f | [%5.3f,%5.3f]" %
          (fl, nm, c["n"], c["effn"], c["inst"]["A"]["corr"], c["inst"]["B"]["corr"],
           c["inst"]["C"]["corr"], c["inst"]["D"]["corr"],
           c["inst"]["D"]["ci"][0], c["inst"]["D"]["ci"][1]))
print("  * = below the F8 bar (Kish eff-n < 35).")

print()
print("=" * 128)
print("THE QUESTION THE POOL FINDINGS NEED: does mature-21+ clear the bar, and does it differ from young?")
print("=" * 128)
for nm in ("young <=20", "mature 21+", "pool young <=20", "pool mature 21+",
           "pool RD mature 21+", "pool non-RD mature 21+", "ND1-64 mature 21+"):
    c = OUT.get(nm)
    if not c: continue
    print("  %-24s eff-n %6.1f  %s" % (nm, c["effn"], "NAMED" if c["named"] else "below bar"))
    for k, _ in KEYS:
        i = c["inst"][k]
        print("      %s  tilt %.4f  1/tilt %.4f  bend %.3f  CI [%.3f,%.3f]"
              % (k, i["tilt"], i["corr"], i["bend"], i["ci"][0], i["ci"][1]))
# overlap test young vs mature on each instrument
y, m = OUT.get("young <=20"), OUT.get("mature 21+")
if y and m:
    print()
    print("  young vs mature, per instrument (do the CIs on TILT overlap?):")
    for k, _ in KEYS:
        yi, mi = y["inst"][k], m["inst"][k]
        ov = not (yi["ci"][1] < mi["ci"][0] or mi["ci"][1] < yi["ci"][0])
        print("      %s  young %.4f [%.3f,%.3f]  mature %.4f [%.3f,%.3f]  -> %s"
              % (k, yi["tilt"], yi["ci"][0], yi["ci"][1], mi["tilt"], mi["ci"][0], mi["ci"][1],
                 "OVERLAP (no separation)" if ov else "SEPARATED"))
yp, mp = OUT.get("pool young <=20"), OUT.get("pool mature 21+")
if yp and mp:
    print("  pool young vs pool mature:")
    for k, _ in KEYS:
        yi, mi = yp["inst"][k], mp["inst"][k]
        ov = not (yi["ci"][1] < mi["ci"][0] or mi["ci"][1] < yi["ci"][0])
        print("      %s  young %.4f [%.3f,%.3f]  mature %.4f [%.3f,%.3f]  -> %s"
              % (k, yi["tilt"], yi["ci"][0], yi["ci"][1], mi["tilt"], mi["ci"][0], mi["ci"][1],
                 "OVERLAP (no separation)" if ov else "SEPARATED"))
json.dump(dict(overall=OV, cells=OUT), open(SP + "/r37_ageaxis.json", "w"), indent=1)
print()
print("wrote", SP + "/r37_ageaxis.json")
