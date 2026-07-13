# HARNESS RECONCILIATION — the G-COHORT gate · RESOLVED · 2026-07-13 (directive item 1, blocking)

## The disagreement
The retiring seat's L3b gate (`l3_cohort_gate.py`, ad-hoc) read baseline **y4 = 137.8%**. The audited
lineage reads **~128.6**: the discount sweep's 15% shipped book (`SWEEP_DISCOUNT.md`) =
`100 / 115.3 / 120.0 / 128.6 / 127.1 / 119.0 / 99.6`, and the v2.6 bake-guard = 128.8 / 127.3 / 119.6.
A ~9 pt gap. The retiring seat flagged it (L3_FINDINGS §L3b) and STOPPED short of a PASS/BREACH verdict,
tasking this seat to reconcile.

## The official gate, by code reading (NOT re-derived)
The project's G-COHORT gate is **`ship_gates_check.py` gate B1** (owner ruling D5, in writing
02/07/2026). Its construction is coded in `_b1_rows()` (ship_gates_check.py:278–295) on a matrix
**regenerated in a clean subprocess by `s4_matrix_M1v7.py` in gate mode** (config pinned; the matrix's
embedded engine/store/config hashes must equal the candidate under test or B1 FAILs). Asserted basis:

- **population**: `incurve` (type ∈ {ND, RD}) ∧ draft cohort **2004 ≤ C ≤ 2020** (17 cohorts).
- **per-cohort curve**: class-year **SUM** of the walk-forward `Vpath` at each depth N (N=1 is the
  anchor = **end of calendar Yr1 = C+1**, regardless of games — D10 sit-out anchor; retired players
  stop at last played year; `Vpath[i] or 0` folds inactive→0).
- **combine**: **index each cohort to its OWN Yr1 (=100), THEN take the UNWEIGHTED cross-cohort simple
  mean** at each depth over cohorts observed at that depth.
- **law (CONSTRAINTS / directive)**: y4/y5/y6 EACH ≤ **130** (hard; guide 120–125). Since each cohort
  is indexed to its own Yr1, the denominator = min(y1, y2) = y1 = 100 by construction (values rise
  y1→y2), so the AVG-row values ARE the ratios-vs-130.

## The convention gap — WHY the ad-hoc read 137.8
| convention | official `_b1_rows` (ADOPTED) | ad-hoc `l3_cohort_gate.py` (SUPERSEDED) |
|---|---|---|
| population | incurve **ND+RD**, cohorts **2004–2020** | **ND only**, cohorts **2014–2020** |
| combine order | **index per cohort → then average (unweighted)** | **average raw sums → then ÷ min(avg₁,avg₂)** |
| pricer | `s4_matrix_M1v7` ASOF (calendar-yr anchor, D10 sit-out, retired-stop) | `value_asof` (career-yr, `cum_games==0∧t≥3→0`) |

The **dominant driver is the combine order.** Averaging raw class-sums lets big/rich cohorts and the
ragged-panel column composition (different cohort sets contribute to y1 vs y4) inflate the deep depths;
indexing each cohort to its own Yr1 first removes cohort-size and cohort-richness heterogeneity. The
short recent window (2014–2020, ND-only) compounds it (recent draftees priced richer, thin tails).

## Reproduction — the audited baseline, on the current candidate base (store b0c39d78)
`scripts/cohort_gate_official.py` reuses `_b1_rows` **verbatim** (byte-for-byte; marked do-not-edit)
on a matrix from `s4_matrix_M1v7.py` (gate mode). On the base engine 7a07e369 / store b0c39d78 /
config 69ead79b:

```
AVG row (indexed yr1=100): 100.0 / 115.3 / 120.0 / 128.6 / 127.1 / 119.0 / 105.8
y4 = 128.6   y5 = 127.1   y6 = 119.0     GATE: PASS   (margins vs 130: 1.4 / 2.9 / 11.0)
cohorts n=17 (2004..2020)   n_players=2649   peak N=4   path_ok=True
```

- **y1..y6 reproduce the SWEEP_DISCOUNT 15% shipped book to 0.0 pt** (`100/115.3/120.0/128.6/127.1/119.0`).
  y7 = 105.8 vs the sweep's 99.6 — the deepest, thinnest, UNGATED depth (differs on cohort-observation
  and the b0c39d78 store vs the sweep's levered board); immaterial to the y4/y5/y6 verdict.
- Matches the v2.6 bake-guard 128.8/127.3/119.6 within store drift (~0.2–0.3 pt).
- The matrix `__meta__` engine/store/config hashes equal the candidate base → this IS the audited
  harness, reproduced. Well inside the directive's ~0.2% tolerance on the gated years.

**Verdict: harness reconciled. The official baseline is y4=128.6 (PASS), NOT 137.8. The ad-hoc
class-sum construction is superseded.** The retiring seat's Δ (L3 spends ~+2.3 pt of y4) was measured
on the ad-hoc harness and must be RE-MEASURED as an absolute on this reconciled harness — that is the
one combined gate (item 2), run once on the fully-combined candidate.
