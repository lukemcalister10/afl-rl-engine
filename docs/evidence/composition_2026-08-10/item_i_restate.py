"""ITEM I — THE RESTATEMENT, on the ORIGINAL corrected ruler (docs/evidence/ruler_act_2026-08-10),
with the F8 bar applied at PLAYER UNIT. READ-ONLY.

PRECONDITION: r15_align.py must print PASS. It does (re-verified this session: stage4a1 + stage5
both n=414 F1=1.1363, KPD 0.6680, RUCK 1.6959; Hurley spot exact).

THE TWO RULERS, same population, same estimator — this is what "restated" means.
  BENT (as filed):  F = Sigma( PROXY / DISC^d ) / Sigma( price_at_stage )
                    PROXY = vpath[3] = ev(p, C+4) — the engine's OWN year-4 price, which the ruler
                    act measured as standing 1.55-1.66x above realized delivery.
  CORRECTED:        F = Sigma( REALIZED / DISC^d ) / Sigma( price_at_stage )
                    REALIZED = the r24 instrument's realized delivery from career year 4 onward,
                    discounted back to year 4. Instrument D (rate-based x year-11-capped) is the
                    owner's own economics and his own horizon, and is the headline; A/B/C printed
                    beside it so the reading is not instrument-shopped.
  d = 4 for the year-0 verdict, 3 for the year-1 verdict (r15_align.py's own exponents).

F=1 is honest. F<1 = OVER-priced (the stage price does not grow into what the career delivered).
F>1 = UNDER-priced.

F8 = PLAYER UNIT: Kish effective n over PLAYERS, weights = the ratio's own denominator
(v0 for year 0, v1 for year 1). Never player-seasons. Bar 35, as the ruler act's own BARN.
"""
import os, sys, json, math
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026; BARN = 35.0; NB = 4000
rng = np.random.default_rng(20260810)

recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
R24 = json.load(open(SP + "/r24_rows.json"))
INST = {(r["key"], r["typ"], r["year"]): r for r in R24["rows"]}
print("corrected-ruler window: %d rows, classes %d-%d (career year 11 observable)"
      % (len(R24["rows"]), min(r["year"] for r in R24["rows"]), max(r["year"] for r in R24["rows"])))


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


KEYS = [("A", "A_av_full"), ("B", "B_rt_full"), ("C", "C_av_win"), ("D", "D_rt_win")]

# ---- build the two stage populations, each row carrying BOTH rulers ----
def build(stage):
    """stage 0 = the year-0 verdict, stage 1 = the year-1 verdict."""
    out = []
    for r in recs:
        i = INST.get((r["key"], r["type"], r["year"]))
        if i is None: continue                       # outside the corrected ruler's window
        den = v(r, stage)
        if not den or den <= 0: continue
        if stage == 1 and games_in(r, r["year"] + 1) < 6: continue   # r15's own year-1 rule
        d = 4 - stage
        row = dict(key=r["key"], year=r["year"], pos=r["pos"], typ=r["type"],
                   pick=r.get("pick"), pickless=r.get("pickless"), is_pool=r.get("is_pool"),
                   age=r.get("age_draft"), den=float(den),
                   bent=float(i["proxy"]) / DISC ** d)
        for k, f in KEYS: row[k] = float(i[f]) / DISC ** d
        out.append(row)
    return out


def ratio(rows, num):
    D_ = sum(r["den"] for r in rows)
    return (sum(r[num] for r in rows) / D_) if D_ > 0 else float("nan")


def effn_player(rows):
    w = np.array([r["den"] for r in rows], float)
    return float(w.sum() ** 2 / (w * w).sum()) if w.sum() > 0 else 0.0


def ci(rows, num):
    """player-resampled + draft-class-clustered bootstrap, union interval (r25's own scheme)."""
    n = len(rows)
    if n < 2: return (float("nan"), float("nan"))
    d = np.array([r["den"] for r in rows], float)
    x = np.array([r[num] for r in rows], float)
    idx = rng.integers(0, n, size=(NB, n))
    bp = x[idx].sum(1) / np.maximum(d[idx].sum(1), 1e-9)
    yrs = np.array([r["year"] for r in rows]); uy = np.unique(yrs)
    gs = [np.where(yrs == y)[0] for y in uy]
    gi = rng.integers(0, len(uy), size=(NB, len(uy)))
    gx = np.array([x[g].sum() for g in gs]); gd = np.array([d[g].sum() for g in gs])
    bc = gx[gi].sum(1) / np.maximum(gd[gi].sum(1), 1e-9)
    return (float(min(np.percentile(bp, 2.5), np.percentile(bc, 2.5))),
            float(max(np.percentile(bp, 97.5), np.percentile(bc, 97.5))))


def verdict(lo, hi):
    if lo != lo: return "n/a"
    if lo <= 1.0 <= hi: return "HONEST"
    return "UNDER-priced" if lo > 1.0 else "OVER-priced"


NDC = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
POS = ["MID", "SD", "SF", "KPF", "KPD", "RUCK"]


def cells(stage):
    out = [("ALL rows", lambda r: True), ("ND in-curve (1-64)", NDC)]
    for p in POS:
        out.append(("  ND in-curve x " + p, lambda r, p=p: NDC(r) and r["pos"] == p))
    if stage == 0:
        out += [("pool ALL", lambda r: r["is_pool"]),
                ("  pool RD", lambda r: r["is_pool"] and r["typ"] == "RD"),
                ("  pool non-RD", lambda r: r["is_pool"] and r["typ"] != "RD"),
                ("  pool age <=18", lambda r: r["is_pool"] and (r["age"] or 99) <= 18),
                ("  pool age 19-20", lambda r: r["is_pool"] and 19 <= (r["age"] or 0) <= 20),
                ("  pool age 21+", lambda r: r["is_pool"] and (r["age"] or 0) >= 21)]
        for p in POS:
            out.append(("  pool x " + p, lambda r, p=p: r["is_pool"] and r["pos"] == p))
    else:
        out += [("pool ALL (played yr1)", lambda r: r["is_pool"])]
    out += [("ND 1-10", lambda r: NDC(r) and r["pick"] <= 10),
            ("ND 11-20", lambda r: NDC(r) and 11 <= r["pick"] <= 20),
            ("ND 21-40", lambda r: NDC(r) and 21 <= r["pick"] <= 40),
            ("ND 41-64", lambda r: NDC(r) and 41 <= r["pick"] <= 64)]
    return out


FLIPS = []
for stage in (0, 1):
    rows = build(stage)
    print("\n" + "=" * 118)
    print("ITEM I — THE %s VERDICTS, RESTATED.  population n=%d  (denominator = %s)"
          % ("YEAR-0" if stage == 0 else "YEAR-1", len(rows), "v0" if stage == 0 else "v1 = ev(p,C+1)"))
    print("=" * 118)
    print(" %-26s %5s %7s %8s | %8s %8s | %-13s %-13s %s"
          % ("cell", "n", "eff-n", "F8", "F BENT", "F CORR", "verdict BENT", "verdict CORR", "95% CI (corrected D)"))
    print(" " + "-" * 116)
    for name, pred in cells(stage):
        sub = [r for r in rows if pred(r)]
        if len(sub) < 2: continue
        en = effn_player(sub)
        fb, fc = ratio(sub, "bent"), ratio(sub, "D")
        lb, hb = ci(sub, "bent"); lc, hc = ci(sub, "D")
        vb, vc = verdict(lb, hb), verdict(lc, hc)
        flag = "" if en >= BARN else "  *below F8 bar"
        if vb != vc and en >= BARN:
            FLIPS.append((stage, name, fb, vb, fc, vc, en))
            flag += "   <<< VERDICT FLIPS"
        print(" %-26s %5d %7.1f %8s | %8.4f %8.4f | %-13s %-13s [%.3f, %.3f]%s"
              % (name, len(sub), en, "PASS" if en >= BARN else "FAIL", fb, fc, vb, vc, lc, hc, flag))
    # the four instruments side by side on the headline cells
    print("\n  the four instruments (no instrument-shopping) — F on each:")
    print("  %-26s %8s %8s %8s %8s %8s" % ("cell", "BENT", "A", "B", "C", "D"))
    for name, pred in [("ALL rows", lambda r: True), ("ND in-curve (1-64)", NDC)] + \
                      [("  ND in-curve x " + p, (lambda r, p=p: NDC(r) and r["pos"] == p)) for p in POS]:
        sub = [r for r in rows if pred(r)]
        if len(sub) < 2: continue
        print("  %-26s %8.4f %8.4f %8.4f %8.4f %8.4f"
              % (name, ratio(sub, "bent"), ratio(sub, "A"), ratio(sub, "B"), ratio(sub, "C"), ratio(sub, "D")))

# ============================================================================================
# LEVEL vs BEND — the ruler act's OWN decomposition, applied to the restatement.
#
# Every cell above flips in the SAME direction by roughly the SAME factor (~1.55x), which is the
# ruler act's own headline: the year-4 price stands 1.55x above realized delivery. That is a LEVEL
# re-basing of the whole board, not a property of any cell. r25_2x2.py draws exactly this line for
# the tilt cells -- "bend = the cell's 1/tilt divided by the OVERALL 1/tilt on the SAME instrument
# (level divides out)" -- and the sitting acted only on bends.
#
# So the restatement is read the same way: a cell is DIRTY when its position RELATIVE to the
# population changes ruler-to-ruler. A uniform level shift that moves every cell identically is the
# ROOT ACT's business (the directive stages it AFTER composition, precisely because correcting the
# forward projection "re-derives year 0/1/2+ consistently").
# ============================================================================================
print("\n" + "=" * 118)
print("LEVEL vs BEND — is the flip a CELL property or the GLOBAL re-basing?")
print("=" * 118)
BENDFLIPS = []
for stage in (0, 1):
    rows = build(stage)
    ovb, ovc = ratio(rows, "bent"), ratio(rows, "D")
    print("\n  stage year-%d   OVERALL F: bent %.4f -> corrected %.4f   (level factor %.3fx)"
          % (stage, ovb, ovc, ovb / ovc))
    print("  %-26s %7s | %8s %8s | %8s %8s | %s"
          % ("cell", "eff-n", "relBENT", "relCORR", "d(rel)", "ratio", "relative verdict"))
    print("  " + "-" * 108)
    for name, pred in cells(stage):
        sub = [r for r in rows if pred(r)]
        if len(sub) < 2: continue
        en = effn_player(sub)
        if en < BARN: continue
        rb, rc = ratio(sub, "bent") / ovb, ratio(sub, "D") / ovc
        # relative-position flip = crosses 1.0 materially (the ruler act's own |bend-1|>=0.10 rule)
        mb = "above" if rb >= 1.10 else ("below" if rb <= 0.90 else "at population")
        mc = "above" if rc >= 1.10 else ("below" if rc <= 0.90 else "at population")
        fl = ""
        if mb != mc and "at population" not in (mb, mc):
            BENDFLIPS.append((stage, name, rb, rc, en)); fl = "   <<< RELATIVE FLIP"
        print("  %-26s %7.1f | %8.4f %8.4f | %+8.4f %8.3f | %s -> %s%s"
              % (name, en, rb, rc, rc - rb, (ratio(sub, "bent") / ratio(sub, "D")), mb, mc, fl))

print("\n" + "=" * 118)
print("THE ITEM A PRECONDITION — are the restated ND YEAR-0 verdicts CLEAN?")
print("=" * 118)
nd0 = [f for f in FLIPS if f[0] == 0 and f[1].strip().startswith("ND")]
ndb0 = [f for f in BENDFLIPS if f[0] == 0 and f[1].strip().startswith("ND")]
print("  READING 1 — ABSOLUTE honesty verdict (level included):")
if not nd0:
    print("    CLEAN — no ND year-0 cell flips.")
else:
    print("    DIRTY — %d ND year-0 cell(s) flip, ALL of them HONEST -> OVER-priced:" % len(nd0))
    for _s, nm, fb, vb, fc, vc, en in nd0:
        print("      %-28s eff-n %6.1f   %s (F %.4f) -> %s (F %.4f)   [level factor %.3fx]"
              % (nm, en, vb, fb, vc, fc, fb / fc))
print("\n  READING 2 — RELATIVE position (the ruler act's own bend rule, level divided out):")
if not ndb0:
    print("    CLEAN — no ND year-0 cell changes its position relative to the population.")
    print("    Every flip in reading 1 is the SAME ~1.55x level re-basing hitting every cell alike,")
    print("    which is the ruler act's already-ruled headline finding, not new cell-level dirt.")
else:
    print("    DIRTY — %d ND year-0 cell(s) move relative to the population:" % len(ndb0))
    for _s, nm, rb, rc, en in ndb0:
        print("      %-28s eff-n %6.1f   rel %.4f -> %.4f" % (nm, en, rb, rc))
print("\n  >>> OWNER DECISION (recorded, not decided by the seat): which reading governs")
print("      'a dirty ND year-0 cell' for ITEM A's precondition.")
print("      Seat's reading: READING 2. The uniform level shift is the ROOT ACT's object — the")
print("      directive stages it AFTER composition precisely because correcting the forward")
print("      projection 're-derives year 0/1/2+ consistently' — and re-teaching every ND year-0")
print("      cell down by 1.55x inside this act would BE the root act, unruled and unfunded.")
print("      Under reading 1, ITEM A cannot ship at all this act and the package stops here.")
print("\nALL FLIPS (both stages, above the bar):")
for s, nm, fb, vb, fc, vc, en in FLIPS:
    print("  year-%d  %-28s eff-n %6.1f  %s %.4f -> %s %.4f" % (s, nm, en, vb, fb, vc, fc))
if not FLIPS: print("  none")
