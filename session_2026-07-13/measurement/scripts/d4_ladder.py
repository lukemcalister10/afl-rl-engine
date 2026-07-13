"""D4.3 + D4.4 — the CAPTAINCY SENSITIVITY LADDER (report-only) on the tagged board 81e48293.
Per rung: Bont/Gawn/Daicos board values, top-19 total, A-PAIRS pair 3 (Bont vs Sanders), and G-COHORT
y4/y5/y6 on the July-8 binding construction (matrix baseline + re-priced capt-sensitive cohort cells).
Also G-PEAK/G-CONVEX/A-BONT/A-GAWN direction. NO rung chosen; NO tuning to catch a player."""
import json, time
import numpy as np
import harness as H
import cohort_repricer as CR
MA = H.MA; F = H.F
BASE = "/home/user/afl-rl-engine/session_2026-07-13/measurement"
MPATH = BASE + "/out/matrix_baseline_tagged.json"
by_key = {p.get("key"): p for p in MA.data}
cells = CR.cohort_cells(MPATH)   # (key,C,N,year,vp_matrix)
t0 = time.time()

# ---- fresh, unrounded capt-sensitive cohort-cell detection (threshold-crossing set is fixed vs GAIN/CAP/EXP) ----
H.capt_default()
dval = {(k, y): CR.price_asof(by_key[k], y) for (k, C, N, y, vp) in cells if k in by_key}
H.capt_off()
sens = set()
for (k, C, N, y, vp) in cells:
    if k not in by_key: continue
    o = CR.price_asof(by_key[k], y); d = dval.get((k, y))
    if d is not None and o is not None and abs(d - o) > 1e-6:
        sens.add((k, y))
H.capt_default()
print(f"[t={time.time()-t0:.0f}s] capt-sensitive cohort cells (unrounded): {len(sens)}")

# 19 over-line players (definitive present-capt-level list)
OVER19 = [d["player"] for d in json.load(open(BASE + "/out/d4_overline_clean.json"))["over_line"]]

def set_rung(gain, exp, cap):
    MA.CAPT_GAIN, MA.CAPT_EXP, MA.CAPT_CAP = gain, exp, cap

def board_vals(names):
    return {nm: (H.board_val(H.find(nm)) if H.find(nm) else None) for nm in names}

def cohort_ratios():
    triples = []
    for (k, C, N, y, vp) in cells:
        if (k, y) in sens and k in by_key:
            v = CR.price_asof(by_key[k], y)
        else:
            v = vp
        triples.append((C, N, v))
    figure, denom, ratios, co = CR.sums_from(triples)
    return round(ratios[4], 4), round(ratios[5], 4), round(ratios[6], 4), {n: round(figure[n], 1) for n in figure}

# ---- the ladder (stated; precedent = the RUC prior-cap ladder). vary one param at a time off baseline ----
RUNGS = [
    ("BASELINE",      0.35, 1.25, 18.0),
    ("GAIN 0.50",     0.50, 1.25, 18.0),
    ("GAIN 0.70",     0.70, 1.25, 18.0),
    ("GAIN 1.00",     1.00, 1.25, 18.0),
    ("CAP 24",        0.35, 1.25, 24.0),
    ("CAP 30",        0.35, 1.25, 30.0),
    ("CAP 40",        0.35, 1.25, 40.0),
    ("CAP ~inf(999)", 0.35, 1.25, 999.0),
    ("EXP 1.40",      0.35, 1.40, 18.0),
    ("EXP 1.60",      0.35, 1.60, 18.0),
    ("GAIN0.7+CAP30", 0.70, 1.25, 30.0),
]
SAN = 3960  # Ryley Sanders board (capt-invariant: 0 premium) — verified live below
results = []
for name, g, e, c in RUNGS:
    set_rung(g, e, c)
    bv = board_vals(["Marcus Bontempelli", "Max Gawn", "Nick Daicos", "Ryley Sanders", "Kieren Briggs"])
    top19 = sum(v for v in board_vals(OVER19).values() if v)
    y4, y5, y6, fig = cohort_ratios()
    bont = bv["Marcus Bontempelli"]; san = bv["Ryley Sanders"]
    pair3_gap = round(100 * (bont - san) / san, 2)   # + means bont above sanders
    results.append(dict(rung=name, gain=g, exp=e, cap=c,
                        bont=bont, gawn=bv["Max Gawn"], daicos=bv["Nick Daicos"],
                        sanders=san, briggs=bv["Kieren Briggs"], top19_total=top19,
                        pair3_gap_pct=pair3_gap, bont_passes_sanders=bont > san,
                        gcohort_y4=y4, gcohort_y5=y5, gcohort_y6=y6,
                        gcohort_margin_y4=round(1.30 - y4, 4), gcohort_breach=(max(y4, y5, y6) > 1.30),
                        figure=fig))
    print(f"[t={time.time()-t0:.0f}s] {name:14s} bont={bont} gawn={bv['Max Gawn']} daicos={bv['Nick Daicos']} "
          f"top19={top19} pair3={pair3_gap:+.2f}% pass={bont>san} | Gy4={y4} y5={y5} y6={y6} marg_y4={round(1.30-y4,4)} breach={max(y4,y5,y6)>1.30}")
set_rung(0.35, 1.25, 18.0)  # restore
json.dump(dict(board="81e48293 (tagged v2.9)", sanders_invariant=SAN, over19=OVER19,
               n_sensitive_cells=len(sens), rungs=results),
          open(BASE + "/out/d4_ladder.json", "w"), indent=1)
print(f"\n[done {time.time()-t0:.0f}s] wrote out/d4_ladder.json")
