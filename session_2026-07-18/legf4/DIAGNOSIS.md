# LEG F4 — DIAGNOSIS (read-only; board-verified, single-thread) · seat 13 · 2026-07-19
The mid/veteran (φ=0) forward-vs-backward asymmetry, decomposed per mechanism with `_merged_recover.py`
addresses. All numbers from the faithfully-rebuilt F3 board (`bccc231` engine tree; entry proof in PLAN §1).

## A. THE RESIDUAL, RE-MEASURED (probe_f4_decomp.py — replicates rl_export's exact lens construction)
Composition-controlled, same 804 roster, per cohort. fwd = vP1/v−1 ; back = v/vM1−1.

| cohort | n | now | fwd% | back% | fwd/back |
|---|--:|--:|--:|--:|--:|
| developing ≤23 | 375 | 365,451 | −26.3%¹ | −2.4% | 10.9× |
| **mid 24–27** | 210 | 246,466 | **−18.2%** | **−10.2%** | **1.79×** |
| **veteran ≥28** | 219 | 177,559 | **−24.8%** | **−19.0%** | **1.30×** |
| **MID+VET** | 429 | 424,025 | **−20.9%** | **−14.1%** | **1.48×** |

¹ developing's −26.3% is the *un-floored* probe value; on the shipped board F3's φ pedigree-carry FLOOR
(rl_export:111-120) lifts it to −18.2% (board build). Mid/veteran are φ=0 → NO floor available → the probe ==
the board exactly (this is the item-354 residual: F3's cure cannot reach φ=0). Board comp-controlled: fwd
−19.6% / back −9.1% — the ~11pt gap of record.

## B. WHERE IT LIVES — one leg (probe_f4_legs.py + probe_f4_pr.py)
- **iso_eff is FLAT** forward and backward (all cohorts +0.0%). The band-isotonic layer is not implicated.
- The ENTIRE decline is `raw_ev`, and within `raw_ev` the **production price `pr = price6(b6)`** — the
  pedigree `pole` is ≈0 for φ=0 (mid pole 1,478 vs pr 233,777; veteran pole 0). Confirms production-anchored.
- `pr` forward: mid −23.2% / veteran −28.4%; backward mid −12.6% / veteran −21.0%.
- Upstream, **the demonstrated-level block `b6` declines forward** (mid −5.9%, vet −7.1%) vs a much shallower
  real backward (mid −1.8%, vet −4.2%). `price6`→`dp.v_at_peak`'s `posval(level−REPL)` nonlinearity LEVERS
  that ~6–7% level drop into the ~23–28% `pr` drop (≈4× — the small above-replacement margin of a settled
  producer is elastic; GAMMA=0.85 SCAR convexity compounds it).

## C. TWO AGE-REF-DRIVEN TERMS FEED `pr` FORWARD — NEITHER REACHED BY F3's FORM-ANCHOR
F3's `_off`/`_LENS_FORM` form-anchor lives ONLY in `_proj_w4` (the age SHAPE `ah=a-_off`) and the pedigree/
tenure clocks. It never touches the demonstrated-level age reads. Measured:

1. **VETERAN driver — the `_dev_advance` level roll** (`rl_model.py:361`, consumed via `level_now` at
   `_merged_recover.py:821`/`:851` and inside the M1 band). The forward lens (BASE_REF=2026, AGE_REF=2027,
   a1≠a0) rolls the demonstrated level DOWN the empirical AGE_CURVE ratio `c1/c0`; backward
   (`_LENS_FORM=None` ⇒ BASE_REF=AGE_REF=2025 ⇒ a1==a0) returns the level UNCHANGED and re-values on real
   evidence. Neutralizing `_dev_advance`→identity (probe_f4_decomp MECH 1): **veteran fwd −24.8% → −10.6%**
   (−14pt) and **MID+VET fwd −20.9% → −14.5% ≈ backward −14.4% (1.01× — SYMMETRY RESTORED)**. Dominant
   board-wide driver. Levered by the same `v_at_peak` nonlinearity (veteran level_now moves only −3.69%
   forward → −14pt of value).

2. **MID driver — the demonstrated-level band `b6`** (`_merged_recover.py:287-288`:
   `cp.cond_prior_band(p,cm,Y)` + the q97 ceiling `q97m.predict(cp._feat(p,Y))`). Both read the ADVANCING
   AGE_REF (2027). Neutralizing `_dev_advance` moved mid only −18.2%→−17.2% (1pt) — so the mid decline is a
   SEPARATE age term, NOT the level roll. Decisive test: `b6` forward decline is **identical with vs without
   F3's form-anchor** (mid −5.93% anchored vs −5.86% AGE-only; vet −7.14% vs −7.13%) ⇒ the band's
   age-dependence keys on AGE_REF and is FULLY asymmetric (real backward: mid −1.8%, vet −4.2%). F3's `_off`
   construction cannot reach it by design.

## D. THE UNIFYING MECHANISM (the L-SYMMETRY breach)
The forward lens advances the AGE clock through the production-price chain — the `_dev_advance` roll
(`rl_model.py:361`) AND the `b6` demonstrated-level band (`_merged_recover.py:287-288`) — applying the
engine's MODELED empirical age-decline (AGE_CURVE / DELTAS / M1 band), then LEVERING it ~4× through
`price6`→`dp.v_at_peak` (`distribution_pricing.py`, `posval(level−REPL)`). The BACKWARD lens re-values on
REAL evidence (`_dev_advance` inert, band at the real prior year). **Result: the modeled forward decline is
~2× the realized backward decline of the SAME players** — a direct L-SYMMETRY breach (R103.3 / MEMO_LEGE §2:
"projected improvement and decline face the same evidentiary bar"). It is NOT a pedigree strip (§2.vi, F3)
and NOT the band-iso or the v0 floor (measured inert).

## E. THE ADDRESSES
- `_merged_recover.py:820-821` — `_proj_w4` `_off`/`ah`: F3 form-anchored the SHAPE, DELIBERATELY left
  `cur=level_now` advancing (line-821 comment). The veteran roll enters here + at `:851`.
- `_merged_recover.py:287-288` — `b6` = `cp.cond_prior_band` + q97 ceiling; both read AGE_REF (mid driver),
  form-anchor never reaches them.
- `rl_model.py:361` — `_dev_advance` (the AGE_CURVE `c1/c0` roll). **HARD-OUT** (rl_model.py fenced).
- `distribution_pricing.py::v_at_peak` (via `price6@289`) — the `posval(level−REPL)` ~4× leverage.
  **OUTSIDE any fence** (F3 flagged this exact term OUT of scope in CHECKPOINT2).

## F. WHAT THIS SESSION DID NOT DO
No engine edit. No board write to the repo (built in a scratch copy of the F3 tree). No k=0 movement (proven
dormant). Store/curve/rl_model/ui/docs untouched. The ±5% number is NOT bent — reproduced OUT as F3 filed it.
