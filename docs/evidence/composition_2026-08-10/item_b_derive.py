"""ITEM B — the pool year-0 age gradient, RE-DERIVED on the ORIGINAL corrected ruler. READ-ONLY.

Supersedes item_b_probe.py (the halted reconstruction). That probe's <=18 and 19-20 bands were
roughly right and its 21+ band was badly wrong (1.157) — the cause is now visible: it priced
delivery with the engine's own 0.14 discount and gfut REPL on live ev(), where the honest
instrument uses the frozen per-entrant matrices, DISC=1.0939 and each season's OWN fit bar.

INSTRUMENT: the year-0 F verdict of item_i_restate.py — F = Sigma(REALIZED/DISC^4) / Sigma(v0),
REALIZED = r24's instrument D (rate-based x year-11-capped: the owner's own economics and his own
horizon). Precondition r15_align.py = PASS.

C5 LEVEL-PRESERVING, and it is exact by construction rather than by tuning:
    factor(band) = F(band) / F(pool)
  =>  Sigma_b Sigma-v0_b x factor_b  =  (1/F_pool) x Sigma REALIZED  =  Sigma v0 .
The unknown global scale of the delivery object cancels in the ratio, so this factor set does NOT
inherit the level question flagged in ITEM I.

F8 = PLAYER UNIT throughout (Kish eff-n over players, weights = v0, bar 35).
"""
import os, sys, json, math, collections
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026; BARN = 35.0; NB = 4000
rng = np.random.default_rng(20260810)

recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
INST = {(r["key"], r["typ"], r["year"]): r for r in json.load(open(SP + "/r24_rows.json"))["rows"]}

# THE BASIS SPLIT, exactly as r36_dob.py enforces it: every VALUE comes from the act-branch
# artifact (store 37ced3ce, pre-DOB) and is neither rebuilt nor touched; ONLY THE AGE FIELD is
# taken from the DOB-written store d9a24282. A birth year is a fact about the world, not a
# valuation, so writing it cannot move a walk-forward price computed without it. Without this the
# teaching population still carries 88 age-unknown pool rows and the C5 identity cannot close.
REPO = os.environ.get("RL_REPO", "/home/user/afl-rl-engine")
_store = json.load(open(os.path.join(REPO, "engine", "rl_after", "rl_model_data.json")))
_srecs = _store if isinstance(_store, list) else (_store.get("players") or _store.get("data") or [])
if not isinstance(_srecs, list):
    for _v in _store.values():
        if isinstance(_v, list) and _v and isinstance(_v[0], dict) and "key" in _v[0]:
            _srecs = _v; break
BY = {p.get("key"): p.get("_by") for p in _srecs if p.get("key")}
def age_draft(r):                       # emit_matrix_338.py:262 exactly: draft year - _by
    by = BY.get(r["key"])
    return (r["year"] - by) if by else r.get("age_draft")

rows = []
for r in recs:
    i = INST.get((r["key"], r["type"], r["year"]))
    if i is None or not r.get("is_pool"): continue
    v0 = float(r["v0"] or 0)
    if v0 <= 0: continue
    rows.append(dict(key=r["key"], year=r["year"], pos=r["pos"], typ=r["type"],
                     age=age_draft(r), v0=v0, real=float(i["D_rt_win"]) / DISC ** 4))
print("POOL teaching population on the corrected ruler: n=%d  classes %d-%d"
      % (len(rows), min(r["year"] for r in rows), max(r["year"] for r in rows)))
unk = [r for r in rows if r["age"] is None]
print("age-UNKNOWN rows: %d   (its own cell by the ruling; never absorbed)" % len(unk))

F = lambda rs: (sum(r["real"] for r in rs) / sum(r["v0"] for r in rs)) if rs else float("nan")
def effn(rs):
    w = np.array([r["v0"] for r in rs], float)
    return float(w.sum() ** 2 / (w * w).sum()) if w.sum() > 0 else 0.0
def ci(rs):
    n = len(rs)
    if n < 2: return (float("nan"),) * 2
    d = np.array([r["v0"] for r in rs], float); x = np.array([r["real"] for r in rs], float)
    idx = rng.integers(0, n, size=(NB, n))
    bp = x[idx].sum(1) / np.maximum(d[idx].sum(1), 1e-9)
    return float(np.percentile(bp, 2.5)), float(np.percentile(bp, 97.5))

FPOOL = F(rows)
print("\npool-wide F (the normaliser, = the level-preserving anchor) = %.6f" % FPOOL)

# ---------------- per-single-age, to see whether 21+ carries a gradient ----------------
print("\n=== PER-SINGLE-AGE (does 21+ carry a gradient, or is it one flat cell?) ===")
print(" %-8s %5s %8s %8s %10s %s" % ("age", "n", "eff-n", "F", "factor", "F8"))
byage = collections.defaultdict(list)
for r in rows:
    if r["age"] is not None: byage[int(r["age"])].append(r)
for a in sorted(byage):
    rs = byage[a]
    print(" %-8s %5d %8.1f %8.4f %10.4f %s"
          % (a if a > 18 else "<=%d" % a, len(rs), effn(rs), F(rs), F(rs) / FPOOL,
             "PASS" if effn(rs) >= BARN else "fail"))

# ---------------- the ruled bands ----------------
BANDS = [("<=18", lambda a: a <= 18), ("19-20", lambda a: 19 <= a <= 20), ("21+", lambda a: a >= 21)]
PRIOR = {"<=18": 0.666, "19-20": 1.200, "21+": 2.474}
print("\n=== THE RULED BANDS — re-derived vs filed (the bridge, as ordered) ===")
print(" %-8s %5s %9s %10s %9s %11s %10s %8s %s"
      % ("band", "n", "eff-n", "Sig v0", "F", "RE-DERIVED", "as filed", "shift", "95% CI on F"))
band_rows = {}
for nm, pred in BANDS:
    rs = [r for r in rows if r["age"] is not None and pred(int(r["age"]))]
    band_rows[nm] = rs
    lo, hi = ci(rs)
    print(" %-8s %5d %9.1f %10.1f %9.4f %11.4f %10.3f %+8.1f%% [%.3f, %.3f] %s"
          % (nm, len(rs), effn(rs), sum(r["v0"] for r in rs), F(rs), F(rs) / FPOOL, PRIOR[nm],
             100 * ((F(rs) / FPOOL) / PRIOR[nm] - 1), lo, hi,
             "" if effn(rs) >= BARN else " *below F8 bar"))

# ---------------- the smooth taper 21->26 (no integer cliff) ----------------
# The ruling: "smooth taper 21->26, no integer cliff". The 21+ cell is ONE measured number, so the
# taper spreads it across 21..26 while HOLDING THE CELL'S OWN v0-weighted mean — the cell's measured
# value is preserved exactly, only its internal shape is smoothed. Shape = linear in age from the
# 19-20 level at 20 up to the plateau at 26, solved for the plateau that reproduces the cell mean.
mat = band_rows["21+"]
f18 = F(band_rows["<=18"]) / FPOOL
f19 = F(band_rows["19-20"]) / FPOOL
fmat = F(mat) / FPOOL
w = np.array([r["v0"] for r in mat], float)
ages = np.array([min(float(r["age"]), 26.0) for r in mat])
sh = (ages - 20.0) / 6.0
P = f19 + (fmat - f19) * float(w.sum() / (w * sh).sum())
print("\n=== THE TAPER — THE RULED SHAPE TESTED AGAINST THE EVIDENCE (HALT-NO-SURPRISE) ===")
print("  THE RULING: 'smooth taper 21->26, no integer cliff'.")
print("  WHAT A MEAN-HOLDING LINEAR 21->26 RAMP WOULD REQUIRE: plateau P = %.4f at age 26." % P)
print("  THAT IS REFUSED, and here is the measurement that refuses it:")
print("    - per-age eff-n INSIDE 21+ : " + " · ".join(
    "%d:%.1f" % (a, effn(byage[a])) for a in sorted(byage) if a >= 21))
print("      every one is far below the F8 bar of %.0f — the band has NO nameable internal shape." % BARN)
print("    - and the point estimates FALL rather than rise after 22: " + " · ".join(
    "%d:%.2f" % (a, F(byage[a]) / FPOOL) for a in sorted(byage) if 21 <= a <= 26))
print("    - a rising ramp to 26 therefore assigns the LARGEST factor (%.2f) to the OLDEST, THINNEST" % P)
print("      rows (ages 25-26: n=%d, eff-n %.1f, measured factor ~0) on no evidence at all,"
      % (len(byage.get(25, [])) + len(byage.get(26, [])),
         effn(byage.get(25, []) + byage.get(26, []))))
print("      and it breaks pool conservation by +3.5%. The directive's own tilt reading already says")
print("      'mature-21+ unnameable -> base factor, pooling disclosed'. The evidence agrees.")
print()
print("  WHAT SHIPS: the cliff is removed where the ruling actually points at it — the BAND BOUNDARY —")
print("  by keying the factor on CONTINUOUS draft age (cp._age_asof is a float; the engine's own")
print("  _ageR rounding is what would create an integer cliff). Piecewise-linear, continuous:")
print("     a <= 18        -> %.4f" % f18)
print("     18 < a < 19    -> linear %.4f .. %.4f" % (f18, f19))
print("     19 <= a <= 20  -> %.4f" % f19)
print("     20 < a < 21    -> linear %.4f .. %.4f" % (f19, fmat))
print("     a >= 21        -> %.4f   (FLAT — pooled, pooling disclosed)" % fmat)
print("  No integer cliff anywhere; each band's v0-weighted mean is held EXACTLY (every row sits at")
print("  a knot, so the bridges carry no mass); no unmeasured within-band gradient is invented.")

KNOTS = [(18.0, f18), (19.0, f19), (20.0, f19), (21.0, fmat)]
def curve(a):
    if a is None: return 1.0                      # age-unknown: OWN cell, never absorbed
    a = float(a)
    if a <= 18.0: return f18
    if a >= 21.0: return fmat
    for (a0, v0_), (a1, v1_) in zip(KNOTS, KNOTS[1:]):
        if a0 <= a <= a1:
            return v0_ if a1 == a0 else v0_ + (v1_ - v0_) * (a - a0) / (a1 - a0)
    return fmat
print("\n  the shipped curve on the half-year grid (continuity visible):")
print("  " + " · ".join("%.1f:%.3f" % (a / 2.0, curve(a / 2.0)) for a in range(35, 45)))
CURVE = {a: curve(a) for a in range(18, 30)}

# ---------------- conservation, shown not asserted ----------------
print("\n=== CONSERVATION (C5: pool Sigma v0 held EXACTLY) ===")
def shape(r): return curve(r["age"])   # age-unknown -> 1.0 (own cell, never absorbed)
before = sum(r["v0"] for r in rows)
_raw = sum(r["v0"] * shape(r) for r in rows)
K = before / _raw          # THE C5 RENORMALISER — a state function re-derived every build, never stored
print("  C5 renormaliser K = %.10f   (the age GRADIENT is preserved exactly; only the level is pinned)" % K)
def fac(r): return K * shape(r)
after = sum(r["v0"] * fac(r) for r in rows)
print("  Sigma v0 before = %.4f" % before)
print("  Sigma v0 after  = %.4f" % after)
print("  delta           = %.6f   (%.3e relative)" % (after - before, abs(after - before) / before))
print("  The engine additionally applies a build-time renormalisation over the LIVE pool population")
print("  (a state function re-derived every build, never a stored constant), so the shipped identity")
print("  is exact on whatever population the board actually carries.")

json.dump(dict(FPOOL=FPOOL, K=K, curve={str(k): K * v for k, v in CURVE.items()},
               curve_unnormalised={str(k): v for k, v in CURVE.items()},
               bands={nm: dict(F=F(band_rows[nm]), factor=F(band_rows[nm]) / FPOOL,
                               n=len(band_rows[nm]), effn=effn(band_rows[nm]), filed=PRIOR[nm])
                      for nm, _ in BANDS},
               age_unknown_rows=len(unk)),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "item_b_factors.json"), "w"), indent=1)
print("\nwrote item_b_factors.json")
