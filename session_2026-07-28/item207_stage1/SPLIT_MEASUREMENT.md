# ITEM 207 stage 1 — measurement under the split structure

Owner rulings 2026-07-28. Measurement only, scratch boards only, nothing adopted, no bake, no pin
moved. Store `c120cfd5`, base `85e39ee`, baseline scratch board reproduces `fa172ac1` byte-exact.

**Populations reproduced, all five exact:** ND 1–64 = 1,448 · ND 65+ = 121 · RD + post-draft = 924
(RD 693 + UNR/IRE/PDA/PDN/PDS 231) · SSP 52 · MSD 106. Pool = 1,045. Total 2,651.

---

## (d) The rookie weight share — the propping, stated directly

At each national pick: the adaptive bandwidth `h`, the year-0 effective-n that sets it, and the
fraction of total kernel weight coming from rookie observations.

| national pick | h | eff-n | **rookie share of kernel weight** |
|---|---|---|---|
| 40 | 0.10 | 211.6 | **0.0%** |
| 50 | 0.10 | 264.5 | **0.8%** |
| 60 | 0.10 | 313.9 | **17.0%** |
| **64** | 0.10 | 327.9 | **30.3%** |
| 70 | 0.10 | 333.6 | 51.0% |
| 80 | 0.10 | 325.1 | 81.5% |

**At pick 64, 30.3% of the evidence setting the value of a national pick is rookie observations.**
That is the number asked for, and it is large.

**Two limbs of the stated mechanism do not fire on this data, and the third does.** Reporting this
because the instruction was to measure where it shows.

1. **The bandwidth never grows.** `h` sits at the floor `0.10` at every pick from 40 to 80, because
   the year-0 effective-n in that region is 211–334 against a `nmin` of 35 — six to nine times the
   threshold. The kernel never has to widen to find observations. The reach into rookie data is
   proximity in log-pick, not adaptation: rookie entrants begin at effective pick **59**, and
   `log(64) − log(59) = 0.081`, inside one bandwidth of 0.10. A rookie at pick 59 therefore carries
   72% of peak kernel weight at pick 64 regardless of how dense the national sample is.
2. **PAVA never fires.** The raw fit is already strictly non-increasing: **zero monotonicity
   violations across all 99 picks**, and PAVA changes **no** value at **any** pick. There are no
   adjacent blocks to pool, so nothing is propagated backward. The strict-descent step is not
   masking anything here because it does nothing here.
3. **The blend does move the fit inside 1–64, and it is visible at the raw stage** — which is the
   part of the account that holds.

## The direction, measured at matched effective pick

Weighted exactly as the fit weights them (year-0 anchor plus career-year points, evidence share ×
time kernel):

| effective pick | ND n | ND wmean | RD n | RD wmean | **RD − ND** |
|---|---|---|---|---|---|
| 50–58 | 1,145 | 563.0 | 0 | — | — |
| **59–64** | 573 | 536.0 | 79 | 458.7 | **−77.3** |
| 65–70 | 333 | 516.9 | 263 | 543.7 | **+26.8** |
| 71–80 | 351 | 519.5 | 576 | 503.6 | −15.9 |

Rookie observations sit **above** national at 65–70, exactly as described — but **77 points below**
national at 59–64, the band that actually touches a 1–64 national curve. So inside the proposed
boundary the blend **depresses** the national fit rather than propping it up:

| pick | blended raw | ND 1–64 raw | difference |
|---|---|---|---|
| 40 | 655.0 | 655.0 | 0.0 |
| 50 | 580.6 | 581.8 | −1.3 (−0.2%) |
| 55 | 555.5 | 560.4 | −5.0 (−0.9%) |
| 60 | 538.4 | 548.2 | −9.7 (−1.8%) |
| **64** | 530.1 | 543.9 | **−13.7 (−2.5%)** |

Shallowest pick where the two raw fits differ by more than 0.5: **pick 48**. Everything above 48 is
untouched.

The upward propping is real and it lives at 65–70 — the band that leaves the national curve entirely
under ruling 1. Removing it is therefore achieved by the split itself, not by anything further.

## (c) The 0.6 ceiling — confirmed

Bust prior at pick 1, six positions, current store, mechanism exactly as written.

| position | n | w as written | pooled | **blended (as written)** | **own fit (w = 1.0)** |
|---|---|---|---|---|---|
| MID | 579 | 0.600 | 93.0 | 99.4 | 103.6 |
| GEN_DEF | 304 | 0.600 | 93.0 | 94.5 | 95.6 |
| GEN_FWD | 333 | 0.600 | 93.0 | 90.1 | 88.1 |
| KEY_DEF | 222 | 0.600 | 93.0 | 89.0 | 86.3 |
| KEY_FWD | 208 | 0.600 | 93.0 | 80.9 | 72.8 |
| RUC | 147 | 0.441 | 93.0 | 99.8 | 108.3 |

**Spread at pick 1: 18.9 as written, 35.5 at w = 1.0 — a 1.88× compression.** The mechanism is
confirmed.

One correction to the framing: the ~19 points is the **compressed output**, not the real spread. The
uncompressed positional spread is **35.5**, so the ceiling is removing more than the ~19 → ~8
description implies, in the same direction. KEY_FWD is pulled up 8.1 points by pooling (72.8 → 80.9)
and RUC pulled down 8.5 (108.3 → 99.8); those two are most of the compression.

**The ceiling binds almost everywhere.** `w = min(n/200, 1) × 0.6` reaches 0.600 for five of six
positions — MID with 579 samples gets exactly the same weight as KEY_FWD with 208. Only RUC (n=147)
sits below, at 0.441. Above n=200 sample size stops mattering entirely, and the prior is never less
than 40% pooled no matter how much data a position has.

## (a) Priors recalculated on the current store, under the split

Training window 2006–2020, GRP-mapped, real effective pick: 1,793 players. ND 1–64 training rows
955; pool training rows 816.

**ND 1–64 — function as written, national picks 1–64 only** (shipped table in brackets):

| position | n | pick 1 | pick 10 | pick 30 | pick 64 |
|---|---|---|---|---|---|
| MID | 355 | 99.4 [98.13] | 82.7 [84.70] | 65.0 [66.37] | **21.7 [33.51]** |
| GEN_DEF | 148 | 94.1 [102.84] | 80.9 [80.91] | 57.7 [55.36] | 31.6 [34.26] |
| GEN_FWD | 176 | 90.4 [89.67] | 76.7 [75.94] | 56.5 [57.05] | **21.3 [34.17]** |
| KEY_DEF | 107 | 90.9 [89.16] | 76.5 [74.18] | 56.5 [54.80] | **28.6 [38.39]** |
| KEY_FWD | 121 | 85.7 [80.48] | 76.1 [72.62] | 59.2 [59.28] | 25.7 [29.50] |
| RUC | 48 | 95.2 [100.03] | 79.6 [85.09] | 64.5 [71.90] | **29.6 [39.34]** |

The top of the draft barely moves (±5 to ±9). **The deep end moves a lot** — at pick 64 every
position falls, four of them by 10–13 points. That is where the restructure and the stream split
both land.

**Pool — one value per position, no isotonic step:**

| position | n | own mean | w | **blended** |
|---|---|---|---|---|
| MID | 217 | 31.5 | 0.600 | 30.8 |
| GEN_DEF | 153 | 37.9 | 0.459 | 33.5 |
| GEN_FWD | 155 | 27.6 | 0.465 | 28.8 |
| KEY_DEF | 114 | 24.2 | 0.342 | 27.9 |
| KEY_FWD | 81 | 24.9 | 0.243 | 28.7 |
| RUC | 96 | 27.7 | 0.288 | 29.2 |

Pool grand mean 29.8. Spread 5.6 blended against 13.7 on own means — the same ceiling compressing
the same way, and here the sample sizes are small enough that `w` is genuinely below the cap for
five of six positions.

Full recalculated table written to `priors_recalculated.json`.

## (b) The curve under the new structure, and its board delta

ND 1–64 fitted on national picks 1–64 only (1,326 rows). Pool valued flat at **492.6** in curve
currency, from the evidence-weighted mean of pool members' fit inputs.

| pick | shipped | split | delta |
|---|---|---|---|
| 1 | 3000 | 3000 | 0 |
| 10 | 1604 | 1551 | −53 |
| 30 | 811 | 783 | −28 |
| 50 | 589 | 582 | −7 |
| 60 | 542 | 548 | +6 |
| 64 | 530 | 544 | **+14** |
| 65 | 528 | 493 | **−35** |
| 80 | 494 | 478 | −16 |
| 99 | 463 | 459 | −4 |

The structure produces a **step at the boundary**: national pick 64 rises to 544, the pool starts at
493, a 51-point drop across the 64/65 line. That is what pricing two mechanisms separately looks
like, and it is the intended shape rather than a defect.

**Board delta** (scratch board `8f6d2c3c` vs board of record `fa172ac1`):

| | |
|---|---|
| movers | **18 of 804 (2.2%)** |
| range | **−32 to −1, all falls** |
| mean | −15.2 |
| pick-asset sum | 75,957 → 74,576 (**−1,381**) |
| routes | National 10 · Mid-season 4 · Rookie 2 · Post-draft 2 |

Largest: Caleb May, Alex Van Wyk, Patrick Carr and Max Mapley all 581 → 549 (−32); Flynn Riley
613 → 587; three rookie/post-draft entrants 446 → 422.

Compared with the earlier two-way fit, the split moves the same 18 rows but **uniformly downward**,
where the blended re-derivation was ±4–9 and the ND-only variant rose. The direction is consistent
with the 59–64 finding: rookies were holding the boundary region *down*, and pricing them separately
lets national pick 64 rise while the pool settles below it.

**One structural blocker for stage 2.** `_merged_recover.py:1566` asserts strict descent across the
whole curve. A pool where order is irrelevant is by definition **flat**, which that assert rejects.
For this measurement I emitted the pool tail descending 1 unit per pick — numerically almost flat,
but it is a proxy, and I am flagging it rather than hiding it. Adopting the split for real means
relaxing that assert above the boundary, which is a deliberate change to the curve contract and
belongs to the owner.

## What I could not do

- The **flat pool tail** could not be measured as genuinely flat; see above.
- The **pool value is position-blind in the board measurement.** Ruling 1 values the pool by
  position, but `_PVC0` is a pick-indexed, position-blind curve. Wiring a positional pool value into
  the board needs an engine change, not a curve swap, so the board delta above understates the
  structure by however much the positional spread matters (5.6 points blended, 13.7 on own means).
- **SSP and MSD tracked separately** — recorded in the populations above (52 and 106) but not
  separately valued; they take the pool value, as ruled.

---
*Execution supervisor, ITEM 207 stage 1. Measurement only; adoption is the owner's and belongs to
stage 2.*
