# THE ONE COMBINED GATE — reconciled G-COHORT re-measure · PASS · 2026-07-13 (directive item 2)

Run ONCE on the fully-combined candidate (L1 + L4 + L2@14 + L3), on the reconciled official harness
(`s4_matrix_M1v7` gate-mode matrix → `_b1_rows` verbatim; HARNESS_RECONCILIATION.md). L7 and L5 are
proven neutral to this measure below, so the combined candidate for the gate is exactly L1+L4+L2+L3.

## The verdict
| construction | y1 | y2 | y3 | **y4** | **y5** | **y6** | y7 | verdict |
|---|---|---|---|---|---|---|---|---|
| BASE (b0c39d78, engine 7a07e369) | 100 | 115.3 | 120.0 | **128.6** | **127.1** | **119.0** | 105.8 | PASS |
| **COMBINED (L1+L4+L2+L3, engine 16e97c3a)** | 100 | 113.9 | 118.1 | **126.8** | **125.2** | **116.1** | 101.9 | **PASS** |
| Δ (combined − base) | — | −1.4 | −1.9 | **−1.8** | **−1.9** | **−2.9** | −3.9 | margin WIDENS |

- **GATE: PASS.** y4/y5/y6 = **126.8 / 125.2 / 116.1**, each ≤ hard 130 (margins **3.2 / 4.8 / 13.9**
  pt). Peak at N=4, path monotone to peak (path_ok). Same population as base (n=17 cohorts 2004–2020,
  2649 players, store b0c39d78 unchanged); engine md5 16e97c3a = the four levers applied.
- **A breach would HALT the candidate; there is none.** The candidate proceeds to the refit.

## Why it holds (the one-candidate law, vindicated on the reconciled harness)
The combined candidate LOWERS the cohort ratios (widens the margin) by ~1.8 pt at y4. On the ad-hoc
harness the retiring seat measured L3 as a +2.3 pt y4 SPEND and projected dial-14 to add ~2.4 pt, net
≈ −0.1 (≈128.5 hold). On the reconciled harness the net is a cleaner **−1.8 pt**: dial-14's
margin-widening (a lower discount lifts the young y1/y2 denominator faster than the survivor-year
numerators — SWEEP_DISCOUNT's own finding) plus the L1/L4 repricing OUTWEIGH L3's young-riser spend.
Either way the levers were ALWAYS meant to be judged together, and together they PASS with room.

## L7 and L5 are neutral to this gate — proven, not assumed
- **L7 (numéraire ÷1.0524) is ratio-invariant.** `_b1_rows` indexes each cohort to its own Yr1:
  `R[C][N] = 100·S[C,N]/S[C,1]`. A uniform scalar k on every value gives `S→kS`, so
  `kS[C,N]/kS[C,1] = S[C,N]/S[C,1]` — the indexed curves and the AVG row are unchanged. L7 cannot
  move the gate. (It applies LAST in the refit for the numéraire quotation, not for the ratio.)
- **L5 (trio → pickless) is cohort-neutral.** The gate population is `incurve` (type ∈ {ND, RD}) ∧
  cohort 2004–2020. The trio (perez/mcandrew/keane) are type SSP — not in the population — and are
  already out of the calibration training pool via the debut-window leg; nulling their `pick` changes
  neither the population nor the ND/RD calibration. The base matrix already carries their SSP override,
  so the gate is identical with or without the L5 completion.

## Butters (the flagged narrow margin) — holds
Independently confirmed at L3a: butters 6060 → 5997 = −1.04%, inside the G-PEAK ≤2% tolerance (board
pass reproduced it exactly, `out/lever_validation.md`). The G-PEAK guard is not breached by the age curve.

## Reproduction
`out/gate_base.json`, `out/gate_combined.json` (summary + per-cohort). Matrices built by
`scripts/run_levers.sh <levers> matrix` (patch pristine → `s4_matrix_M1v7` gate mode → restore,
md5-verified); gate by `scripts/cohort_gate_official.py` (`_b1_rows` verbatim). All-levers-off
reproduces the base matrix (the base run IS all-off). The verdict feeds the ladder (owner-word gate).
