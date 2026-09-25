# PRE-REGISTRATION — ORDER 19, THE POOL SITTER LIFT

Written **before** any instrument in this directory was run. Committed in the same act as the results
so the two can be read against each other. Any figure landing outside a stated band is reported as a
**PREREG BREACH** in `POOL_SITTER_LIFT_SUMMARY.md`, named and unhidden. ORDER 18 breached 6 of 12 and
owned them; that is the standard this file is written to.

## THE OWNER'S RULING AND QUESTION, VERBATIM

> "For now, keep ND sitter and we can deal with it later. But given more pool players sit, if we keep
> it for them it will destroy their values"
>
> "For the pool players, I think we look at lifting the sitter penalty and rebuild it again if needed
> afterwards? How much would that change values of the pool and the v0 of them?"

**The ND sitter treatment stays untouched. This act measures only the size of a POOL lift.**

## THE TWO VARIANTS

- **VARIANT A — lift the H leg only.** `H_POOLSIT = H_UNION = 1.0`. Manifest dials, gate mode, guards
  armed. The R leg is untouched everywhere.
- **VARIANT B — lift the whole pool sitter penalty.** Variant A **plus** the R leg neutralised inside
  `sitout_ev` for pool rows only (`if p.get('_pool'): R = 1.0`), so a pool sitter carries his full
  entry anchor. **ND rows keep R exactly as they are.** No dial exists for the R leg, so this variant
  is a one-line code patch applied to a **STAGED SCRATCHPAD WORKTREE ONLY**; the checkout's shipped
  `engine/rl_after/_merged_recover.py` is never modified, and the variant's own `engine_head` md5 in
  the emitted matrix is the independent proof that it differs by code.

## WHAT IS ALREADY SETTLED FROM THE CODE (declared, NOT offered as prediction)

Read out of the source before any instrument was written. These are code facts, not forecasts.

- **F1.** `_h_cut` (`_merged_recover.py:2037-2049`) composes `H_POOLSIT`/`H_UNION` inside
  `if pool and sitter:`. `H_MATNONRD` is already 1.0 (ORDER 9). So with `H_POOLSIT=H_UNION=1.0`,
  `_h_cut` returns exactly 1.0 for **every** row on the board — variant A is equivalent to
  `RL_ITEM_H=0` at the shipped `H_MATNONRD`.
- **F2.** `sitout_ev` (`:1961-1969`) is reached from `ev()` only at `ns==0`. `_h_cut` is applied at
  the same site. So **both legs bite only on sit-out rows**; the two variants cannot move a pool row
  that played this season through these sites.
- **F3.** `_R_surf` clamps pick to the knot grid `[5,15,30,50]` in log-pick, so the constant pool index
  `effpk = 65` reads the **knot-50 column verbatim**: nonKPP `[.549,.388,.345,.239,.164,.164]`,
  RUCK `[.781,.594,.594,.594,.541,.470]`, KPP floored on the board path to the pointwise max with
  nonKPP `[.642,.407,.351,.334,.334,.329]`.
- **F4.** The year-zero **floor** (`ev()`, final wrapper) is `floor_frac(yis) * entry_anchor(p)` and
  covers pool entrants. At `yis=1` that is `0.45 x anchor`. A pool sitter whose cut price falls below
  the floor is **already floored today**, so part of the composed charge is not currently being paid
  on the board. This blunts the measured board effect relative to the pathway-mean charge and is the
  single biggest reason the two numbers will not agree.
- **F5.** `_v0_uncapped(p) = raw_ev(p, debutyr-1) * iso_eff(p, debutyr-1)`. `raw_ev` is a different
  function from `ev`; `_h_cut` and `sitout_ev` are both applied **inside `ev()`** and are not called
  from `raw_ev`. On the board path `v0_start` returns the frozen `_V0CURVE` value, built from
  `_v0_raw` = capped `_v0_uncapped`. Nothing in that chain reads `H_POOLSIT`, `H_UNION` or `_R_surf`.
  **The sign of the v0 answer is therefore deducible a priori; the act still PROVES it by execution
  rather than asserting it, because the order requires proof.**
- **F6.** `_a_blend` (`:2176-2179`) reads `_R_surf` a **second** time, on the year-1+ arm. Variant B as
  specified by the order touches only `sitout_ev`, so that site is left alone. It is measured
  separately as a disclosed sensitivity, not folded into variant B.
- **F7.** `noarb_table_338.py`'s population is `teaches_curve and 1 <= pick <= 64`, and
  `_teaches_curve(p) = _in_pvc(p) and not is_pool(p)` (`rl_model.py:313`). **No pool row is in the
  legacy picks 1-64 instrument at all.** Its movement under either variant is therefore predicted to
  be exactly zero, and that is a declared code fact, not a prediction.

## THE PREDICTIONS (genuine, made before running anything)

### Board effect (live board `94f1fec5`, 804 active rows, `v = round(ev(p,2026)/F)`)

| # | quantity | predicted band |
|---|---|---|
| P1 | live-board rows moved by VARIANT A | **12 – 45** |
| P2 | VARIANT A board total change | **+0.20% – +1.20%** |
| P3 | VARIANT B moves EXACTLY the same row set as A (no row moves under B that is still at today's value under A) | **TRUE** |
| P4 | VARIANT B board total change | **+0.80% – +4.00%**, and **at least 2.5x** variant A's |
| P5 | largest single named mover under B, as a percentage of his own value today | **+90% – +250%** |

### Per-pathway mean-preserving figure

| # | quantity | predicted band |
|---|---|---|
| P6 | VARIANT A per-pathway figure reproduces ORDER 18's published **"R leg only"** column on all nine pathways | max abs delta **< 1e-6** |
| P7 | VARIANT B per-pathway figure | **exactly 1.000000** on all nine pathways (the law holds by construction once the whole pool differential is lifted) |

### v0

| # | quantity | predicted band |
|---|---|---|
| P8 | v0 (`v0_start`, and `entry_anchor` for pool rows) under both variants vs today | **identical to at least 12 significant figures on every row**; max abs relative delta **< 1e-12** |

### Derived-level interaction (Phase 1)

| # | quantity | predicted band |
|---|---|---|
| P9 | the phase-1 profile measure `realised_full / v0` **DOES** read the sitter penalty, because `realised_full` averages `vpath` = walk-forward `ev()` and a sit-out season's `ev()` carries `R x H`. So **derived levels DO change.** | **TRUE — levels change** |
| P10 | `nd_profile` (the calibration target, ND 1-64) is **UNCHANGED** under both variants to < 1e-9 relative, because no ND row reaches either leg | **TRUE** |
| P11 | the worst-hit pathway's Layer-1 `lam` (PDN or PDS or IRE) rises under VARIANT B by | **+10% – +80% relative** |

### Cohort instruments

| # | quantity | predicted band |
|---|---|---|
| P12 | legacy picks 1-64 (`noarb_table_338`) tables under BOTH variants | **byte-identical to SHIP** (F7) |
| P13 | all-arm PRIMARY (cohorts 2005-2023) yr1 ratio, SHIP 0.8850 → VARIANT B | **+0.005 – +0.060 absolute** |
| P14 | all-arm no-arbitrage margin against the 14% charge stays **POSITIVE (no arbitrage)** under both variants | **TRUE** |

### The owner's own premise, tested

| # | quantity | predicted band |
|---|---|---|
| P15 | every one of the nine pool pathways has an entry-weighted sit-out share ABOVE ND 1-64's 0.1394 | **TRUE on all nine** |
| P16 | the pooled pool sit-out share (entry-weighted) vs ND 1-64's 0.1394 | **2.0x – 4.5x** |

## CONSTRAINTS ASSERTED AT WRITE TIME

    board       data/rl_build/rl_app_data.json                             94f1fec59f99c59d5890d5975c79fa9b
    store       engine/rl_after/rl_model_data.json                         d9a24282357cf3083b1640466e3ecd83
    instrument  docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py  0f8220351c64c56ccfa90c60edcdfa5f

MEASURE AND REPORT ONLY. No wiring, no shipped-default change, no board move. Every variant is built in
a scratchpad worktree. The repo tree is never written outside this evidence directory.
Branch `build/pool-sitter-lift`, cut from `origin/main` (`d3d5f55`). `build/pool-repricing-phase1` and
`build/nd-sitter-redistribution` are not touched.
