"""ITEM I — THE RESTATEMENT, on the ORIGINAL corrected ruler (docs/evidence/ruler_act_2026-08-10),
with the F8 bar applied at PLAYER UNIT. READ-ONLY.

PRESENTED UNDER THE LEVEL LAW (register v633 / CURRENT_STATE v120, owner words 5240550781).

  THE LEVEL of a delivery-based ruler is NOT evidence and is never presented as a finding. The
  same ruler reads year-4/5 prices ~1.5x hot exactly as it reads year-0: a belief/option market
  always reads hot against AVERAGE delivery, at every rung, by construction. Only CONTRASTS
  WITHIN THE SAME RULER are evidence. Asymmetric level changes (one rung, not all) are BARRED.

So this script states the common level ONCE, as a numeraire property, with its year-4 equivalence
beside it — and then reports only RELATIVE position, which is the evidence. There are no
per-group "over-priced" verdicts anywhere in the output, and the absolute reading of the ITEM A
precondition is closed by law rather than argued.

PRECONDITION: r15_align.py must print PASS. It does (re-verified this session: stage4a1 + stage5
both n=414 F1=1.1363, KPD 0.6680, RUCK 1.6959; Hurley spot exact).

THE TWO RULERS, same population, same estimator — this is what "restated" means.
  BENT (as filed):  F = Sigma( PROXY / DISC^d ) / Sigma( price_at_stage ), PROXY = vpath[3]
  CORRECTED:        F = Sigma( REALIZED / DISC^d ) / Sigma( price_at_stage )
  d = 4 for the year-0 rung, 3 for the year-1 rung (r15_align.py's own exponents).
Instrument D (rate-based x year-11-capped) is the headline; A/B/C printed beside it so no
reading is instrument-shopped.

F8 = PLAYER UNIT: Kish effective n over PLAYERS, weights = the ratio's own denominator. Bar 35.
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


def build(stage):
    out = []
    for r in recs:
        i = INST.get((r["key"], r["type"], r["year"]))
        if i is None: continue
        den = v(r, stage)
        if not den or den <= 0: continue
        if stage == 1 and games_in(r, r["year"] + 1) < 6: continue
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


def ci_rel(all_rows, mask, num):
    """Bootstrap the CONTRAST (cell F / population F) — the quantity that IS evidence.
    One resample of the whole population per replicate; the cell is read off the same draw, so
    numerator and denominator move together and the ratio's interval is honest."""
    n = len(all_rows)
    x = np.array([r[num] for r in all_rows], float)
    d = np.array([r["den"] for r in all_rows], float)
    m = np.array(mask, bool)
    idx = rng.integers(0, n, size=(NB, n))
    xs, ds = x[idx], d[idx]; ms = m[idx]
    pop = xs.sum(1) / np.maximum(ds.sum(1), 1e-9)
    cell = (xs * ms).sum(1) / np.maximum((ds * ms).sum(1), 1e-9)
    rel = cell / np.maximum(pop, 1e-9)
    return float(np.percentile(rel, 2.5)), float(np.percentile(rel, 97.5))


def contrast_verdict(lo, hi):
    """The ONLY verdict this script issues. Material = the ruler act's own |bend-1| >= 0.10 rule."""
    if lo != lo: return "n/a"
    if lo > 1.10: return "ABOVE population"
    if hi < 0.90: return "BELOW population"
    return "at population"


NDC = lambda r: r["typ"] == "ND" and not r["pickless"] and r["pick"] and 1 <= r["pick"] <= 64
POS = ["MID", "SD", "SF", "KPF", "KPD", "RUCK"]


def cells(stage):
    out = [("ND in-curve (1-64)", NDC)]
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


# ==================== THE LEVEL, STATED ONCE, AS A NUMERAIRE PROPERTY ====================
r0, r1 = build(0), build(1)
L0b, L0c = ratio(r0, "bent"), ratio(r0, "D")
L1b, L1c = ratio(r1, "bent"), ratio(r1, "D")
YR4 = 1.0 / 1.5468        # the same ruler read at the year-4 rung (r25_2x2: 1/tilt D = 1.5468)
print("""
======================================================================================================
THE COMMON RULER LEVEL — stated once, as a NUMERAIRE PROPERTY, and never again as a finding
======================================================================================================
  On the corrected ruler the WHOLE population reads:
        year-0 rung   F = %.4f        year-1 rung   F = %.4f
  and the SAME ruler read at the year-4 rung gives F = 1/1.5468 = %.4f.

  Those three numbers are the same number. A belief/option market is priced against the FULL
  distribution of outcomes it might buy, and it is measured here against the AVERAGE career that
  was actually delivered; it therefore reads hot at EVERY rung, by construction. That is a
  property of the numeraire, not a fact about year 0, about young players, or about picks.

  THE LEVEL LAW (owner words 5240550781): the level is not evidence and is never presented as a
  finding; only CONTRASTS within one ruler are evidence; and an asymmetric level change — moving
  one rung and not the others — is BARRED, because it manufactures a pick-hoarding arbitrage.

  Everything below is therefore reported RELATIVE to the common level of its own rung.
  (For the record, the bent ruler's common level was year-0 %.4f / year-1 %.4f — the restatement
  moves the LEVEL by ~1.55x at every rung alike, which is exactly why the level carries no
  information about any group.)
""" % (L0c, L1c, YR4, L0b, L1b))

# ==================== THE RESTATEMENT: CONTRASTS ONLY ====================
MOVES = []
for stage, rows, Lb, Lc in ((0, r0, L0b, L0c), (1, r1, L1b, L1c)):
    print("=" * 118)
    print("ITEM I — THE %s RUNG, RESTATED AS CONTRASTS.  n=%d  (denominator = %s)"
          % ("YEAR-0" if stage == 0 else "YEAR-1", len(rows), "v0" if stage == 0 else "v1 = ev(p,C+1)"))
    print("  rel = the cell's F divided by its OWN rung's common level. rel > 1 = the cell delivered")
    print("  MORE per point of price than the population; rel < 1 = less. The level divides out.")
    print("=" * 118)
    print(" %-26s %5s %7s %6s | %8s %8s %9s | %-20s %s"
          % ("cell", "n", "eff-n", "F8", "rel BENT", "rel CORR", "d(rel)", "95% CI (rel, corr)", "contrast"))
    print(" " + "-" * 116)
    for name, pred in cells(stage):
        sub = [r for r in rows if pred(r)]
        if len(sub) < 2: continue
        en = effn_player(sub)
        rb, rc = ratio(sub, "bent") / Lb, ratio(sub, "D") / Lc
        lo, hi = ci_rel(rows, [pred(r) for r in rows], "D")
        vb = contrast_verdict(*ci_rel(rows, [pred(r) for r in rows], "bent"))
        vc = contrast_verdict(lo, hi)
        flag = "" if en >= BARN else "  *below F8 bar"
        if vb != vc and en >= BARN:
            MOVES.append((stage, name, rb, vb, rc, vc, en)); flag += "   <<< CONTRAST MOVES"
        print(" %-26s %5d %7.1f %6s | %8.4f %8.4f %+9.4f | [%.3f, %.3f]%s %-16s%s"
              % (name, len(sub), en, "PASS" if en >= BARN else "fail", rb, rc, rc - rb, lo, hi,
                 " " * 5, vc, flag))
    print("\n  the four instruments, as CONTRASTS (rel to each instrument's own level):")
    print("  %-26s %8s %8s %8s %8s" % ("cell", "relA", "relB", "relC", "relD"))
    LV = {k: ratio(rows, k) for k, _f in KEYS}
    for name, pred in [("ND in-curve (1-64)", NDC)] + \
                      [("  ND in-curve x " + p, (lambda r, p=p: NDC(r) and r["pos"] == p)) for p in POS]:
        sub = [r for r in rows if pred(r)]
        if len(sub) < 2: continue
        print("  %-26s %8.4f %8.4f %8.4f %8.4f"
              % (name, ratio(sub, "A") / LV["A"], ratio(sub, "B") / LV["B"],
                 ratio(sub, "C") / LV["C"], ratio(sub, "D") / LV["D"]))
    print()

# ==================== THE ITEM A PRECONDITION ====================
print("=" * 118)
print("THE ITEM A PRECONDITION — are the restated ND YEAR-0 CONTRASTS CLEAN?")
print("=" * 118)
nd0 = [m for m in MOVES if m[0] == 0 and m[1].strip().startswith("ND")]
print("""  Under the LEVEL LAW the question can only be asked of CONTRASTS. A cell is dirty when its
  position RELATIVE to its own rung changes between the two rulers. The absolute reading — every
  ND year-0 cell 'flipping' because the common level moved ~1.55x at every rung alike — is closed
  by law: it is the numeraire moving, it moves every rung together, and acting on one rung alone
  is the barred asymmetric change.
""")
if not nd0:
    print("  CLEAN. No ND year-0 cell above the F8 player-unit bar changes its contrast between the")
    print("  bent ruler and the corrected ruler. ITEM A's precondition is MET on the shape reading;")
    print("  no year-0 cell is re-taught. (The owner's confirming word is still awaited before the")
    print("  ITEM A wiring fires.)")
else:
    print("  DIRTY — %d ND year-0 cell(s) move their contrast. These re-teach BEFORE ITEM A:" % len(nd0))
    for _s, nm, rb, vb, rc, vc, en in nd0:
        print("    %-28s eff-n %6.1f   rel %.4f (%s) -> %.4f (%s)" % (nm, en, rb, vb, rc, vc))

print("\nALL CONTRAST MOVES (both rungs, above the bar) — THIS is the evidence the act reads:")
for s, nm, rb, vb, rc, vc, en in MOVES:
    print("  rung-%d  %-28s eff-n %6.1f  rel %.4f %s -> %.4f %s" % (s, nm, en, rb, vb, rc, vc))
if not MOVES: print("  none")
