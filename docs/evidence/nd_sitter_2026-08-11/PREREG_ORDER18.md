# PRE-REGISTRATION — ORDER 18, THE NATIONAL-DRAFT SITTER REDISTRIBUTION TEST

Written **before** `nd_sitter.py` was run. Committed in the same act as the result so the two can be
read against each other. Any figure that lands outside a stated band is reported as a **PREREG BREACH**
in `ND_SITTER_SUMMARY.md`, named and unhidden. This project's standard is that breaches are owned.

## THE OWNER'S QUESTION, VERBATIM

> "Does the ND sitter penalty redistribute? As if we are penalising 5x for some sitters, that would be
> a huge redistribution to those who don't."

## THE LAW BEING TESTED (owner's D8 amendment, the MEAN-PRESERVING PRINCIPLE)

Once a group's entry price is calibrated to that group's own realized returns — **sitters included** —
any within-group sitter differential must be a **REDISTRIBUTION** (value moved from sitters to
non-sitters of the same group), **never a net charge**. If it is a net charge, the group stops
averaging to its own calibrated return and the calibration is undone.

The test statistic is the entry-weighted mean of the applied sitter multiplier over the group:

    mean = ( SUM_sitters e*R  +  SUM_non-sitters e*1 ) / SUM_all e

`mean < 1.0` is a **NET CHARGE** and a breach of the law. `mean == 1.0` is redistribution-neutral.
The uplift the non-sitters would have to carry for the law to hold is

    U = ( SUM_all e  -  SUM_sitters e*R ) / SUM_non-sitters e

## WHAT IS ALREADY SETTLED FROM THE CODE (declared, NOT offered as a prediction)

These were read out of the source before the measurement was written and are stated here so the
prediction section below is not credited with them. They are code facts, not forecasts.

- **F1.** `_h_cut` (`engine/rl_after/_merged_recover.py:2037-2049`) is gated on `p['_pool']` — the
  `H_POOLSIT` / `H_UNION` multipliers are inside `if pool and sitter:`. **No ND row ever reaches them.**
  On the ND arm the retention surface `R` is therefore the ENTIRE sitter differential.
- **F2.** `sitout_ev` (`:1961`) builds `anch = R * entry_anchor(p)` with
  `R = _R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)`, applied to **every** player including
  national draftees. For a true sitter `lam = 0`, so the finished price IS `R * entry_anchor(p)`.
- **F3.** `entry_anchor(p)` (`:1852-1857`) returns `v0_start(p)` for any non-pool row. So on the ND
  arm the two denominators phase-1 kept separate for the pool (`entry_anchor` vs `v0_start`)
  **coincide identically**, and the denominator ambiguity phase 1 had to disclose does not arise here.
- **F4.** `R_SURF` (`:1121-1124`) carries no entry above 1.0 at any depth >= 1. Every `R` a sitter can
  draw is therefore `<= 1`, and strictly `< 1` everywhere except RUCK at knot pick 5, depth 1 (1.000).
  **Consequence: the ND headline mean is below 1.0 by arithmetic whenever the arm carries any sitter.**
  The SIGN of the answer is deducible a priori; only its MAGNITUDE is genuinely measured. This is
  declared rather than presented as a discovered result.
- **F5.** There is no uplift term anywhere on the ND arm. Nothing in `sitout_ev`, `_h_cut`, or the
  year-1+ leg multiplies a non-sitter's price by anything above 1.0 on account of another row sitting.

## THE PREDICTIONS (genuine, made before running anything)

Population: the phase-1 cell construction, national arm, `stream == 'ND 1-64'`, complete-window
(`Y <= 2021`). Weight `e = entry_anchor`. Sitter multiplier `R = _R_surf(cls, effpk, float(d))` at the
row's OWN pick — not clamped to the pool index 65.

| # | quantity | predicted band |
|---|---|---|
| P1 | headline entry-weighted mean, ND 1-64 | **0.87 – 0.93** |
| P2 | net charge (mean − 1) | **−7% – −13%** |
| P3 | entry-weighted sitter share | **0.15 – 0.25** |
| P4 | mean R among sitters (entry-weighted) | **0.45 – 0.60** |
| P5 | required uplift U | **1.10 – 1.18** |
| P6 | direction vs the pool arm | **same direction (net charge, mean < 1) on ND as on all nine pool pathways** |
| P7 | ND net charge vs RD's −8.07% | **ND is the LARGER charge in magnitude** — R is far harsher than H_POOLSIT=0.804 even though ND's sitter share is lower |
| P8 | class ordering of severity | **RUCK mildest, KPP harshest**; nonKPP between |
| P9 | pick-band ordering | **later picks charged harder than early picks** (both a higher sitter rate and a lower R at pick 50 than at pick 5) |
| P10 | who is uplifted | **NOBODY.** The measured uplift actually applied to ND non-sitters is exactly 1.0000 at every pick band and every class. The owner's "huge redistribution to those who don't" does not occur; the value is removed from the arm, not moved within it. |

## THE CALIBRATION QUESTION (item 3) — the pre-registered decision rule

The law only bites if the ND entry prices are already calibrated to ND returns **including sitters**.
The rule is fixed here, before the code is quoted in the summary, so the verdict cannot be fitted to
the answer:

- **IF** never-established players (no season of `QUAL_GAMES = 6` games) sit INSIDE the curve-teaching
  population carrying value `0.0`, and stay in the aggregator's denominator, **THEN** the ND entry
  price already prices sit-out risk in, and applying `R` on top is a **SECOND CHARGE FOR THE SAME
  THING — a double charge**, and the mean-preserving law bites on the ND arm exactly as it does on
  the pool.
- **IF** they are EXCLUDED from the teaching population, **THEN** the curve is calibrated on survivors
  only, the entry price is a survivor price, and `R` may be a necessary correction rather than a
  double charge — in which case the headline net charge, though real, is not by itself a breach.

Instruments: `structural_values()` at
`docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py:339`,
`realised_full()` at `:313`, `never_established()` at `:277`, `load_matrix()` at `:325`.

**Prediction: INSIDE at 0.0 — the double-charge branch.** (Low confidence is not claimed; the
`realised_full` early-return `return 0.0` was visible when this file was written. What was NOT
established before running is how MANY teaching rows are never-established and what share of the
teaching weight they carry. Those two counts are the genuine measurement here.)

| # | quantity | predicted band |
|---|---|---|
| P11 | never-established share of the 1197-row ND teaching population | **18% – 25%** |
| P12 | rows that teach exactly 0.0 | **all never-established rows except those taking a prior fallback** |

## CONSTRAINTS ASSERTED AT WRITE TIME

    board       data/rl_build/rl_app_data.json                             94f1fec59f99c59d5890d5975c79fa9b
    store       engine/rl_after/rl_model_data.json                         d9a24282357cf3083b1640466e3ecd83
    instrument  docs/evidence/.../noarb/noarb_table_338.py                 0f8220351c64c56ccfa90c60edcdfa5f

MEASURE AND REPORT ONLY. No wiring, no engine configuration change, no board touch. The engine is
loaded READ-ONLY from a staged copy exactly as phase 1 does; the repo tree is never written by the
measurement script outside this evidence directory.
