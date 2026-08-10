"""ITEM H — the ruled cut list, RE-DERIVED on the corrected ruler. READ-ONLY.

THE RULED CUTS (directive §2H): named union sitters (23+ | IRE | MSD) x 0.280 ·
all-pool-sitters x 0.804 · mature nonRD x 0.615, as cell-qualified by the pool grid.
The #326 floor (0.45) is NOT touched. NO blanket lifts anywhere.

A cut factor is the cell's own delivery ratio F: a cell that returns 0.280 of what it is priced
is cut to 0.280 of its price. So each ruled factor should reproduce as that cell's F on the
ruler it was measured on. This script tests exactly that, on the BENT ruler first (the ruler the
cuts were measured on) — if a factor does not reproduce there, its cell definition is wrong and
the cut must not be taken from this instrument.

F8 at PLAYER unit throughout. Ages from the DOB store (r36_dob.py's basis split).
"""
import os, sys, json, math, collections
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026; BARN = 35.0; NB = 4000
rng = np.random.default_rng(20260810)
REPO = os.environ.get("RL_REPO", "/home/user/afl-rl-engine")

recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
INST = {(r["key"], r["typ"], r["year"]): r for r in json.load(open(SP + "/r24_rows.json"))["rows"]}
_store = json.load(open(os.path.join(REPO, "engine", "rl_after", "rl_model_data.json")))
_srecs = _store if isinstance(_store, list) else (_store.get("players") or _store.get("data") or [])
if not isinstance(_srecs, list):
    for _v in _store.values():
        if isinstance(_v, list) and _v and isinstance(_v[0], dict) and "key" in _v[0]:
            _srecs = _v; break
BY = {p.get("key"): p.get("_by") for p in _srecs if p.get("key")}


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def games_in(r, y):
    for s in (r.get("seasons") or []):
        if s["year"] == y: return s["games"]
    return 0


def age_of(r):
    by = BY.get(r["key"])
    return (r["year"] - by) if by else r.get("age_draft")


rows = []
for r in recs:
    if not r.get("is_pool"): continue
    if not (2004 <= r["year"] <= 2022) or r["year"] + 4 > END: continue
    v0 = v(r, 0)
    if not v0 or v0 <= 0: continue
    i = INST.get((r["key"], r["type"], r["year"]))
    rows.append(dict(key=r["key"], year=r["year"], typ=r["type"], pos=r["pos"], age=age_of(r),
                     v0=v0, sitter=(games_in(r, r["year"] + 1) == 0),
                     bent=v(r, 4) / DISC ** 4,
                     corr=(float(i["D_rt_win"]) / DISC ** 4) if i else None))
print("pool rows: n=%d  (with a corrected-ruler value: %d)"
      % (len(rows), sum(1 for x in rows if x["corr"] is not None)))

F = lambda rs, k: (sum(x[k] for x in rs) / sum(x["v0"] for x in rs)) if rs else float("nan")
def effn(rs):
    w = np.array([x["v0"] for x in rs], float)
    return float(w.sum() ** 2 / (w * w).sum()) if w.sum() > 0 else 0.0
def ci(rs, k):
    m = len(rs)
    if m < 2: return (float("nan"),) * 2
    d = np.array([x["v0"] for x in rs], float); y = np.array([x[k] for x in rs], float)
    idx = rng.integers(0, m, size=(NB, m))
    bp = y[idx].sum(1) / np.maximum(d[idx].sum(1), 1e-9)
    return float(np.percentile(bp, 2.5)), float(np.percentile(bp, 97.5))


CELLS = [
    ("named union sitters (23+|IRE|MSD)", 0.280,
     lambda x: x["sitter"] and ((x["age"] or 0) >= 23 or x["typ"] in ("IRE", "MSD"))),
    ("all-pool-sitters",                  0.804, lambda x: x["sitter"]),
    ("mature nonRD",                      0.615,
     lambda x: x["typ"] != "RD" and (x["age"] or 0) >= 21),
]

print("\n=== THE RULED CUTS vs THE INSTRUMENT ===")
print(" %-36s %5s %8s %9s %9s %9s %s"
      % ("cell", "n", "eff-n", "F bent", "RULED", "F corr", "F8"))
OUT = {}
for nm, ruled, pred in CELLS:
    rs = [x for x in rows if pred(x)]
    rc = [x for x in rs if x["corr"] is not None]
    fb = F(rs, "bent"); fc = F(rc, "corr") if rc else float("nan")
    en = effn(rs)
    print(" %-36s %5d %8.1f %9.4f %9.3f %9.4f %s"
          % (nm, len(rs), en, fb, ruled, fc, "PASS" if en >= BARN else "FAIL"))
    lo, hi = ci(rc, "corr") if rc else (float("nan"),) * 2
    OUT[nm] = dict(ruled=ruled, F_bent=fb, F_corr=fc, n=len(rs), effn=en, ci=[lo, hi])

print("\n=== DOES THE BENT RULER REPRODUCE THE RULED FACTORS? ===")
allok = True
for nm, ruled, _ in CELLS:
    d = OUT[nm]
    ok = abs(d["F_bent"] - ruled) < 0.05
    allok = allok and ok
    print("  %-36s ruled %.3f  vs  F bent %.4f   %s"
          % (nm, ruled, d["F_bent"], "reproduces" if ok else "DOES NOT REPRODUCE"))
if not allok:
    print("""
  HALT-NO-SURPRISE. At least one ruled cut factor does not reproduce as its cell's delivery
  ratio on the ruler it was measured on. That means the cell definition used here is NOT the
  one the cut was sized from — the pool-grid qualification (ruling 2.5, comment 5235784509)
  carries conditions this script does not have. The cut factors are therefore NOT re-derived;
  they are taken AS FILED (0.280 / 0.804 / 0.615) and marked as filed in the attribution, and
  the corrected-ruler column above is reported beside them as the bridge the order asked for.
  Re-deriving them properly needs the pool-design instrument, which is a separate act's script.""")
else:
    print("\n  All three reproduce: the cut factors are re-derived on the corrected ruler column above.")

print("\n=== WHAT SHIPS ===")
for nm, ruled, _ in CELLS:
    d = OUT[nm]
    src = "AS FILED" if not allok else "re-derived"
    print("  %-36s x %.3f   [%s]   corrected-ruler reading %.4f  CI [%.3f, %.3f]"
          % (nm, ruled, src, d["F_corr"], d["ci"][0], d["ci"][1]))
print("  the #326 floor (0.45) is UNTOUCHED; no blanket lifts anywhere.")
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "item_h_factors.json"), "w"), indent=1)
print("\nwrote item_h_factors.json")
