# RESIDUAL — the measured S_AGE 30+ breakout-persistence curve · register 122a · 2026-07-15

Basis: HEAD `62352729` · store `340a7a32` (Guard 5 PASS) · engine `_merged_recover.py` under the
config gate (47 vars = manifest defaults, hash `c2d233aec104`). Read-only; harness =
`measure_sage_residual.py`. FINDINGS, NOT VERDICTS.

## What was measured

`_S_AGE(age)` is the fraction of a proven player's current-over-baseline elevation `(Lc−Lo)` that the
engine keeps in the up-branch of `_coreM1` (fires only when `n≥4`, `Lc−Lo≥5.0`, `_radq`). Curve:
`age 28→0.151, 29→0.027, **30→0.000, 31+→0.000**`.

Realised analogue `s_real(age)` = the fraction of that same elevation actually realised in the
FOLLOWING season, over the identical population (proven, up-branch, `gap≥5`, `_radq`), on the full
historical panel. `x = Lc−Lo`, `y = L_next − Lo`, slope = ratio-of-means through the origin, Gaussian
age kernel `h=1.5`, 95% CI by player-cluster bootstrap (5000). Raw = same estimator at the integer age
only (no borrowing). n = up-branch player-years with a qualifying (`≥10g`) next season.

Total up-branch proven player-years with a realised Y+1: **590** — overwhelmingly young (breakouts are a
young-player event). The 30+ tail is thin, and thins fast.

## The curve

| age | n (obs) | players | s_real **smoothed** [95% CI] | s_real **raw age-only** [95% CI] | `_S_AGE` | 0 in CI? |
|----:|--------:|--------:|:-----------------------------|:---------------------------------|:--------:|:--------:|
| 29  | 33 | 74 | **+0.379** [+0.208, +0.534] | +0.551 [+0.150, +0.970] | 0.027 | **NO (both)** |
| 30  | 20 | 51 | **+0.236** [+0.014, +0.439] | −0.476 [−1.095, +0.101] | 0.000 | smoothed NO¹ · raw **YES** |
| 31  | 12 | 32 | +0.061 [−0.281, +0.392] | −0.396 [−1.410, +0.621] | 0.000 | YES |
| 32  |  4 | 16 | −0.061 [−0.559, +0.410] | +0.829 [−0.103, +1.971] | 0.000 | YES |
| 33  |  2 |  6 | −0.147 [−0.787, +0.460] | −0.047 [−2.167, +1.667] | 0.000 | YES |
| 34  |  1 |  3 | −0.359 [−0.978, +0.442] | (degenerate n=1) | 0.000 | YES |
| 35  |  1 |  2 | −0.743 [−1.334, +0.454] | (degenerate n=1) | 0.000 | YES |
| 36  |  0 |  1 | −1.046 [−1.810, +0.471] | (no obs) | 0.000 | YES |

¹ The smoothed age-30 estimate excludes zero **only by borrowing from age 29** (h=1.5 puts ~0.80 weight
on the strongly-positive 29 obs). The age-30-**only** slope is −0.48 with **zero inside** the CI. Declared
per CORE rule 7 (thin slices pooled deliberately and declared).

## Survivorship (declared caveat — biases s_real UP)

A breakout Y+1 only enters `s_real` if the player plays ≥10 games again. Washout rate rises with age:

| age | breakouts | washed out (no qual Y+1) | rate |
|----:|----------:|-------------------------:|-----:|
| 29 | 36 | 3 | 0.08 |
| 30 | 24 | 4 | 0.17 |
| 31 | 18 | 6 | 0.33 |
| 32 |  6 | 2 | 0.33 |
| 33 |  4 | 2 | 0.50 |

Washouts are excluded, so the true (washout-inclusive) 30+ persistence is **lower** than the survivor
numbers above — pushing the 30+ curve further toward / below zero.

## Sensitivity (pooled 30+, no kernel)

| next-games ≥ | gap ≥ | n(30+) | players | slope (ratio) | slope (mean y/x) |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 10 | 5 | 40 | 34 | −0.355 | −0.350 |
|  6 | 5 | 46 | 37 | −0.417 | −0.431 |
| 10 | 3 | 83 | 60 | −0.485 | −0.608 |
|  6 | 3 | 90 | 63 | −0.575 | −0.723 |

Every unsmoothed pooled-30+ cut is **negative**: 30+ proven breakouts, on the whole, fall *below*
baseline the next year — reversion to `Lo` or worse.

## Reading

1. **Zero-at-30 is NOT rejected at age 30.** Raw age-30 slope −0.48, 0 inside [−1.10, +0.10]; pooled
   30+ is negative; survivorship pushes it lower still. On the strict question, the zero is defensible —
   if anything slightly *generous*.
2. **The one robust misprice is age 29**, where the curve has already faded to 0.027 but realised
   persistence is +0.38–0.55 (0 outside CI, raw and smoothed). **The fade to zero arrives ~a year early:**
   a 29-year-old proven breakout is ~40–55% real; the engine treats it as ~3% real.
3. **31+ is unresolvable** (n ≤ 12, washout ≥ 33%). Point estimates trend negative but every CI spans
   zero. The sample does not support a claim either way; do not read the negative tail as signal.
