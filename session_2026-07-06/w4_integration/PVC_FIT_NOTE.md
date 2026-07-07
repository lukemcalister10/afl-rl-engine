# W4 PVC FIT — derivation note (candidate; owner rules on the curve)
**2026-07-06 · fitted per the re-stamped PVC Derivation Spec v1 (PR #41) · generated artifact:
`engine/rl_after/pvc_fit_candidate.json` (stamped with source + book id) · lever `RL_PVCFIT` (default ON).**

## Definition (the spec's, executed on the candidate)
`PVC(k)` = **end-of-calendar-year-1 as-of value of the TYPICAL player at pick k** — the book's `anchor` column
(the D10 curve anchor: end of calendar year 1, whether or not the player debuted, so a sat-out year-1 carries its
sit-out value R·V0 — the TYPICAL player at a slot includes the sitters).

- **Pool:** 1,448 ND year-1 anchors, drafts **2004–2024** (the "2004 window": every cohort from 2004 forward),
  recorded picks, pickless mechanisms excluded — from the CANDIDATE walk-forward book
  (`out/s4_matrix_prefit.json`), so the anchors carry the **lifted young values** and the **LIVE ruck values**
  (#44 ceiling + smooth young headroom — nothing hardcoded, no 1.4 anywhere in the fit).
- **Smoother:** adaptive-bandwidth Nadaraya–Watson **median** over log-pick (bandwidth grown until eff-n ≥ 35 —
  the house kernel convention), then a parametric power-decay top (a·k^b fit on the smoothed picks 1-8) blended
  out by pick 12 — the spec's trend-extrapolated top (loclin-at-pick-1 treatment), then **isotonic
  non-increasing**, then re-anchored **pick 1 = 3000** (`RL_PICK1`).
- **Monotone:** verified non-increasing across 1..99; two 1-pick interior plateaus (21-22, 31-32 — plateaus
  allowed under the house isotonic convention); floor 210 from ~pick 55 (the board's existing pick floor).

## The curve (v3.4 → fitted)
| pick | v3.4 (baked) | fitted | Δ |
|---|---|---|---|
| 1 | 3000 | 3000 | anchor |
| 3 | 2249 | 1853 | −17.6% |
| 5 | 1967 | 1481 | −24.7% |
| 8 | 1706 | 1167 | −31.6% |
| 15 | 1074 | 735 | −31.6% |
| 30 | 606 | 395 | −34.8% |
| 45 | 452 | 264 | −41.6% |
| 60+ | 308 | 210 | −31.8% |

**Why it is steeper than v3.4:** v3.4 measures realized CAREER value per pick (best-2 posval, busts→0) — a
backward long-horizon measure. The spec's year-1-anchor basis prices the slot at the one-year mark, where the
engine has already charged sit-out retention, thin-evidence shrink and bust risk — so the typical deep pick is
worth far less than its realized-career survivors suggest. This is the same direction as the #43 finding
(deep-pick cohorts over-priced, band-centre over-optimism) and prices the survivor reward AT THE TOP of the
draft rather than spreading it down the tail.

## Scope fence (deliberate, no circularity)
The fitted curve re-prices the **pick side** (the board's trade currency, the `picks` section, A13/A14 advisory,
the book's `draftval` display column). **Player pricing does NOT read it back:** the head freezes `draftval` (the
RUC prior-cap / scaffold basis) on the pre-fit v3.4 curve (`_PVC0`), honouring the PR #44 V0-scaffold scope. The
fit therefore cannot feed back into the anchors it was fitted from; the one-iteration drift is nil by
construction on the player side. Kill-switch `RL_PVCFIT=0` (or absent artifact) → v3.4 curve verbatim.

## For the owner
The pick curve is the piece with the largest owner-facing move in this candidate (picks 3-60 down 18-42% against
players). It is exactly what the re-stamped spec defines, fitted on your ruled window, and it is separable: the
player board stands with or without it (`RL_PVCFIT` dial). A13/A14 (Wardlaw/Ashcroft ~pick-1; Rivers/Reid/
Burgoyne ~pick-8) move from PENDING to measurable against this curve — read them on the board.
