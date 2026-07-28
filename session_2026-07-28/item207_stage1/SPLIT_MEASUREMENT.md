# ITEM 207 stage 1 — measurement under the split structure

Owner rulings 2026-07-28. Measurement only, scratch boards only, nothing adopted, no bake, no pin
moved. Store `c120cfd5`, base commit `85e39ee`.

**Populations reproduced, all five exact:** ND 1–64 = 1,448 · ND 65+ = 121 · RD + post-draft = 924
(RD 693 + UNR/IRE/PDA/PDN/PDS 231) · SSP 52 · MSD 106. Pool = 1,045. Total 2,651.

> **Retraction, owner-corrected 2026-07-28.** An earlier version of this document expressed the pool
> as curve entries for picks 65–99 and reported a scratch-board delta from it — 18 movers, mean
> −15.2, pick-asset sum −1,381. **Those figures are withdrawn.** Under the ruled structure there is
> no price for pick 70: the pool is not a pick curve and selection order within it is irrelevant, so
> a descending 493→459 tail is a structure that was never ruled. Nothing measured on it is carried
> forward. The pool's board effect waits for the engine change.
>
> Two blockers claimed in that version were also wrong, in opposite directions:
> - **Strict descent is not an engine blocker.** The write-path assert at `rl_export.py:137` is `>=`
>   and says so in its own message ("monotone non-increasing"). The strict rule is
>   `docs/RULEBOOK.md:12` §4 G-MONO — "the pick curve is strictly decreasing; pick 1 = 3000 exactly"
>   — which is law, not code. It does not bite: under the ruling the pick curve is 1–64, it descends,
>   and the pool is not a pick curve.
> - **Positional pricing already exists.** `iso_corr(pos, pk)` (`_merged_recover.py:493`) takes
>   position and pick, and `_v0_curve_assert` (`:1361`) asserts V0\* is a function of
>   (pos, ageR, pick). Only `_PVC0`/draftval — the raw ladder underneath — is position-blind, and
>   that is not the layer that prices players. The pool needs one index, not a new capability.
>   (`iso_corr` already clamps at `min(pk, 70)`, so a single pool index sits inside existing
>   behaviour rather than extending it.)

---

## 1 · The rookie weight share in the blended fit

**Measured on:** store `c120cfd5`; `per_entrant.json` regenerated against that store; the shipped
`derive_pvc2` fit configuration (tau 0.12, nmin 35, pick-bandwidth floor 0.10). This measures the
*existing blended fit*, which is what the split replaces.

| national pick | h | eff-n | **rookie share of kernel weight** |
|---|---|---|---|
| 40 | 0.10 | 211.6 | **0.0%** |
| 50 | 0.10 | 264.5 | **0.8%** |
| 60 | 0.10 | 313.9 | **17.0%** |
| **64** | 0.10 | 327.9 | **30.3%** |
| 70 | 0.10 | 333.6 | 51.0% |
| 80 | 0.10 | 325.1 | 81.5% |

**At national pick 64, 30.3% of the evidence setting the value is rookie observations.**

**Two limbs of the stated mechanism do not fire; the third does.**

1. **The bandwidth never grows.** `h` sits at the floor `0.10` at every pick from 40 to 80, because
   the year-0 effective-n there is 211–334 against an `nmin` of 35 — six to nine times the threshold.
   The kernel never widens to find observations. The reach into rookie data is proximity in log-pick:
   rookie entrants begin at effective pick **59**, and `log(64) − log(59) = 0.081`, inside one
   bandwidth of 0.10. A rookie at pick 59 carries 72% of peak kernel weight at pick 64 however dense
   the national sample is.
2. **PAVA never fires.** The raw fit is already strictly non-increasing — **zero monotonicity
   violations across all 99 picks**, and PAVA changes **no** value at **any** pick. There are no
   adjacent blocks to pool, so nothing propagates backward.
3. **The blend does move the raw fit inside 1–64.** This limb holds, and is measured below.

### Direction, at matched effective pick

Weighted exactly as the fit weights them — year-0 anchor plus career-year points, evidence share ×
time kernel.

| effective pick | ND n | ND wmean | RD n | RD wmean | **RD − ND** |
|---|---|---|---|---|---|
| 50–58 | 1,145 | 563.0 | 0 | — | — |
| **59–64** | 573 | 536.0 | 79 | 458.7 | **−77.3** |
| 65–70 | 333 | 516.9 | 263 | 543.7 | **+26.8** |
| 71–80 | 351 | 519.5 | 576 | 503.6 | −15.9 |

Rookie observations sit **above** national at 65–70 — the described mechanism — but **77 points
below** at 59–64, the band that touches a 1–64 national curve. Inside the boundary the blend
therefore **depresses** the national fit:

| pick | blended raw | ND 1–64 raw | difference |
|---|---|---|---|
| 40 | 655.0 | 655.0 | 0.0 |
| 50 | 580.6 | 581.8 | −1.3 (−0.2%) |
| 55 | 555.5 | 560.4 | −5.0 (−0.9%) |
| 60 | 538.4 | 548.2 | −9.7 (−1.8%) |
| **64** | 530.1 | 543.9 | **−13.7 (−2.5%)** |

Shallowest pick where the two raw fits differ by more than 0.5: **pick 48**. Everything above 48 is
untouched. The upward propping is real and lives at 65–70 — the band that leaves the national curve
entirely under ruling 1, so the split removes it by construction.

## 2 · The national curve, picks 1–64

**Measured on:** store `c120cfd5`; `per_entrant.json` regenerated against it; national-draft rows
only, picks 1–64; **1,326 fit rows**; `derive_pvc2` machinery unchanged (tau 0.12, nmin 35);
numeraire pin 1 = 3000. Artifact: `curve_nd_1_64.json`, 64 entries, **no pool entries**.

Strictly decreasing across its whole domain, pick 1 = 3000 exactly — G-MONO satisfied as written.

| pick | shipped (blended, 1–99) | **ND 1–64** | difference |
|---|---|---|---|
| 1 | 3000 | 3000 | 0 |
| 10 | 1604 | 1551 | −53 |
| 30 | 811 | 783 | −28 |
| 50 | 589 | 582 | −7 |
| 60 | 542 | 548 | +6 |
| **64** | 530 | **544** | **+14** |

The comparison is against the shipped curve because that is the incumbent; it is not a like-for-like
comparison of two curves over the same domain, since the shipped curve runs to 99 and this one stops
at 64 by construction.

**No board effect is reported for this curve.** Scoring a board requires a price for the pool as
well, and the pool is not expressible as curve entries. That measurement waits for the engine change.

## 3 · Bust priors recalculated

**Measured on:** store `c120cfd5`; the derivation exactly as supplied; training window 2006–2020,
GRP-mapped, real effective pick — **1,793 players**. ND 1–64 training rows 955; pool training rows
816. Full table: `priors_recalculated.json`.

### ND 1–64 — the function as written, national picks 1–64 only

Shipped table in brackets.

| position | n | pick 1 | pick 10 | pick 30 | pick 64 |
|---|---|---|---|---|---|
| MID | 355 | 99.4 [98.13] | 82.7 [84.70] | 65.0 [66.37] | **21.7 [33.51]** |
| GEN_DEF | 148 | 94.1 [102.84] | 80.9 [80.91] | 57.7 [55.36] | 31.6 [34.26] |
| GEN_FWD | 176 | 90.4 [89.67] | 76.7 [75.94] | 56.5 [57.05] | **21.3 [34.17]** |
| KEY_DEF | 107 | 90.9 [89.16] | 76.5 [74.18] | 56.5 [54.80] | **28.6 [38.39]** |
| KEY_FWD | 121 | 85.7 [80.48] | 76.1 [72.62] | 59.2 [59.28] | 25.7 [29.50] |
| RUC | 48 | 95.2 [100.03] | 79.6 [85.09] | 64.5 [71.90] | **29.6 [39.34]** |

The top of the draft barely moves (±5 to ±9). **The deep end moves a lot** — at pick 64 every
position falls, four of them by 10–13 points. That is where the restructure and the stream split both
land.

### Pool — one value per position, no isotonic step

Order of selection is irrelevant within the pool, so there is no pick to regress on. Same target,
same credibility blend.

| position | n | own mean | w | **blended** |
|---|---|---|---|---|
| MID | 217 | 31.5 | 0.600 | 30.8 |
| GEN_DEF | 153 | 37.9 | 0.459 | 33.5 |
| GEN_FWD | 155 | 27.6 | 0.465 | 28.8 |
| KEY_DEF | 114 | 24.2 | 0.342 | 27.9 |
| KEY_FWD | 81 | 24.9 | 0.243 | 28.7 |
| RUC | 96 | 27.7 | 0.288 | 29.2 |

Pool grand mean 29.8. Spread 5.6 blended against 13.7 on own means. These are **positional values**,
not curve entries, and are not expressible as a price for any pick.

SSP (52) and MSD (106) take the pool value as ruled, and are tracked separately so they can become
their own pools as data accumulates.

## 4 · The 0.6 ceiling

**Measured on:** store `c120cfd5`, same 1,793-player training window, bust prior at pick 1.

| position | n | w as written | pooled | **blended (as written)** | **own fit (w = 1.0)** |
|---|---|---|---|---|---|
| MID | 579 | 0.600 | 93.0 | 99.4 | 103.6 |
| GEN_DEF | 304 | 0.600 | 93.0 | 94.5 | 95.6 |
| GEN_FWD | 333 | 0.600 | 93.0 | 90.1 | 88.1 |
| KEY_DEF | 222 | 0.600 | 93.0 | 89.0 | 86.3 |
| KEY_FWD | 208 | 0.600 | 93.0 | 80.9 | 72.8 |
| RUC | 147 | 0.441 | 93.0 | 99.8 | 108.3 |

**Spread at pick 1: 18.9 as written, 35.5 at w = 1.0 — a 1.88× compression. The mechanism is
confirmed.**

The ~19 points is the **compressed output**, not the real spread; the uncompressed positional spread
is **35.5**. The ceiling is removing more than the ~19 → ~8 description implies, in the same
direction. KEY_FWD is pulled up 8.1 points by pooling (72.8 → 80.9) and RUC pulled down 8.5
(108.3 → 99.8); those two are most of it.

**The ceiling binds almost everywhere.** `w = min(n/200, 1) × 0.6` reaches 0.600 for five of six
positions — MID with 579 samples gets exactly what KEY_FWD gets with 208. Only RUC (n = 147) sits
below, at 0.441. Above n = 200 sample size stops mattering, and the prior is never less than 40%
pooled however much data a position has.

Two properties of the derivation, neither flagged when it was written: the `0.6` is a chosen constant
with no stated basis, and `increasing=False` on raw pick makes the output a step function whose
plateau widths are set by noise rather than by anything derived.

## 5 · What is not measured

- **The pool's board effect.** Requires the engine to carry a pool index; it is not a curve swap.
  This is now the priority ahead of further measurement.
- **The 1–64 curve's board effect.** Same reason — a board needs both sides priced.
- **SSP and MSD as their own pools.** Populations recorded (52, 106); they take the pool value as
  ruled.

---
*Execution supervisor, ITEM 207 stage 1. Measurement only; adoption is the owner's and belongs to
stage 2.*
