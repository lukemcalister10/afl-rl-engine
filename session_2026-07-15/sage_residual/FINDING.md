# FINDING — Is the S_AGE zero-at-30 real? · register 122a · L-SAGE-FADE · 2026-07-15

**Basis:** HEAD `62352729` · store `340a7a32` (Guard 5 PASS) · config gate `c2d233aec104`. Read-only.
**FINDINGS, NOT VERDICTS — no fix proposed, only the measured shape.**

## The question

`_S_AGE(age)` credits a proven player only `S_AGE·(Lc−Lo)` of a breakout (current level above baseline),
and the curve is **hard-zero from age 30 on** (`…29→0.027, 30→0.000, 31→0.000…`). Nobody had tested
whether a 30+ breakout truly carries none of itself forward. We measured the realised carry-forward
`s_real(age)` on the full historical panel, same population the engine's up-branch touches
(`n≥4`, `gap≥5`, `_radq`), realised = the following season's average.

## What the data says

**The zero at 30 survives.** The age-30-only realised slope is **−0.48 with zero inside its CI
[−1.10, +0.10]** (n=20 survivor player-years). Every unsmoothed pooled-30+ cut is negative (−0.36 to
−0.58): 30+ proven breakouts, as a group, land *below* baseline the next year — full reversion or worse.
Survivorship makes this generous, not harsh: the washout rate (breakout, then <10 games) rises 8%→17%→33%
across ages 29→30→31, and those non-persisters are *excluded* from the estimate. On its own terms, the
engine's zero-at-30 is **defensible — if anything slightly optimistic.**

**But the fade arrives one year too early.** At **age 29** the engine has already collapsed the curve to
0.027, while realised persistence is **+0.38 (smoothed) / +0.55 (raw), zero outside the CI both ways.**
Age 29 is the *only* age where the residual is significant. A 29-year-old proven breakout is ~40–55%
real; the engine prices it as ~3% real. The curve should still be carrying meaningful weight at 29 and
cross to zero around 30 — instead it zeroes 29 in all but name.

**31+ cannot be resolved.** n ≤ 12 and washout ≥ 33%. Point estimates trend negative but every CI spans
zero. The sample does not support any claim above 31.

## Zero-in-CI at each age (the direct answer)

| age | 29 | 30 | 31 | 32 | 33 | 34 | 35 | 36 |
|-----|----|----|----|----|----|----|----|----|
| smoothed | **NO** | NO¹ | YES | YES | YES | YES | YES | YES |
| raw age-only | **NO** | YES | YES | YES | YES | — | — | — |

¹ smoothed-30 excludes zero only by borrowing from the strong age-29 neighbour (h=1.5); the age-30-only
slope includes zero. **Age 29 is the only age where the zero fails on its own evidence.**

## The current players the near-zero touches (Y=2025, proven, gap≥5, up-branch)

Ranked by |implied − measured| level points; `implied` = engine (`Lo`, S_AGE≈0), `measured` = `Lo +
s_real(age)·gap`. **At 30+ the slope's CI includes zero → read these as exposure, not confident misprice.**

| player | pos | age '26 | Lo (implied) | Lc | gap | measured | Δ lvl |
|--------|-----|:--:|:--:|:--:|:--:|:--:|:--:|
| **Isaac Heeney** | MID | 30 | 101.4 | 109.5 | 8.1 | 104.5 | **+3.08** |
| **George Hewett** | MID | 31 | 95.2 | 107.8 | 12.6 | 98.2 | **+2.96** |
| **Darcy Cameron** | RUC | 31 | 98.8 | 108.2 | 9.4 | 101.0 | **+2.21** |
| Tom Atkins | MID | 31 | 85.9 | 95.1 | 9.2 | 88.1 | +2.17 |
| Bailey Dale | GFWD | 30 | 94.7 | 100.0 | 5.3 | 96.7 | +2.01 |
| Max Gawn | RUC | 35 | 120.8 | 125.9 | 5.2 | 118.9 | −1.86 |
| Marcus Bontempelli | MID | 31 | 122.6 | 128.9 | 6.3 | 124.1 | +1.48 |

**Robust subset:** only **Heeney** and **Dale** (both age 29 as of 2025, entering 30) sit on the one age
whose residual excludes zero — they are the two defensible under-prices (+3.08, +2.01 level pts). The 31+
names (Hewett, Cameron, Atkins, Bontempelli) sit on a slope statistically indistinguishable from the
engine's zero; Gawn's negative is n=1-class noise.

## Close (plain terms)

The engine's decision to stop trusting a 30-year-old's breakout is **basically right** — 30+ breakouts
really do wash out. The flaw is timing, not level: it stops trusting **29-year-olds** too, and there the
data plainly disagrees — their breakouts are about half-real. The zero is real; the *approach* to it is a
year premature. That is the measured shape; the disposition is the owner's.
