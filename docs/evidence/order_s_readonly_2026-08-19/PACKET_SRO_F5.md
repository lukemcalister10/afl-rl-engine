# PACKET F5 — THE SEVERITY CALIBRATION

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Prereg:** `PREREG_SRO_F5.md`, pushed at `7b114e9` before any number here existed.

**NO ENGINE FILE WAS EDITED. NO DIAL WAS ADDED. NO BOARD WAS BUILT. NO STORE WAS WRITTEN.
NO PULL REQUEST. NOTHING ON `main`. NOTHING IS ADOPTED. NO REPAIR IS PROPOSED.**

Every constant used is asserted against the engine block (`F5-A1` did not fire) and the premium
surface is asserted node-for-node against the built engine grid (`F5-A2` did not fire).

**Named rows illustrate. They gate nothing.**

---

## 0 · THE ANSWER, IN SIX SENTENCES

**The owner's objection is supported, and the mechanism's own conviction constant is the place it
shows up.**

At every games level measured, the empirical strength of conviction sits **below** what `A(g)` assumes
— **7 of 7 games bins, without exception.** Pooled over the tail the owner named, a deep
underperformer with 10-22 games goes on to deliver **1.90 times** what the charge marks him at
relative to a near-bar peer, 90% CI **[1.21, 2.79]**. The fitted conviction constant is
**`G0_hat = 21.5`, 90% CI [12.98, 28.99]**, against a wired 9.89 and a published interval of
[7.60, 12.98] — **the two intervals fail to overlap by three thousandths, which is a hairline and is
reported as one.** The tail flattens exactly where `TMAX` assumes it does, so that part of the design
is vindicated. **And there is one caveat large enough to sit in this paragraph: on the MEDIAN row the
charge is not too harsh at all — the front-loading is a statement about the average, and the average
is carried by a minority who recover.**

---

## 1 · THE OWNER'S PREMISE, CHECKED BEFORE ANYTHING ELSE

The shape: a first-year row, 15 games, about 19 points a game below his pedigree bar. From the wired
constants, not assumed:

```
A(15)  = 1 - exp(-15/9.89)                      = 0.7806
T(-19) = clip(1 - 0.65744*(-19 - (-2.4527)))    = 11.8788
f      = exp(-0.174383 * 0.7806 * 11.8788)      = 0.1985
```

**The mechanism retains 19.9% of that row's pedigree leg and charges away 80.1%. On the pedigree leg
the owner is right and is understating it — that is a 5.0x cut, not 4x.**

**But the PRICE is not the pedigree leg.** It is `rho*production + pi*pedigree + age credit`, and the
charge touches only the middle term. The twelve actual ORDER P board rows closest to the shape (age
under 24, 10-20 career games, `s_P` between −14 and −24), with their real price over entry price:

| row | pick | games | s_P | f | v0 | price | price/v0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Zeke Uwland | 2 | 17 | −20.86 | 0.1534 | 2,583 | 1,564 | 0.606 |
| Samuel Grlj | 8 | 19 | −15.16 | 0.2485 | 1,659 | 1,463 | 0.882 |
| Mitchell Edwards | 32 | 16 | −19.05 | 0.1891 | 1,115 | 1,301 | 1.167 |
| Sam Marshall | 25 | 13 | −22.50 | 0.1639 | 886 | 418 | 0.471 |
| Jordan Croft | 15 | 18 | −16.95 | 0.2146 | 799 | 449 | 0.562 |
| Harry Armstrong | 23 | 11 | −23.45 | 0.1768 | 718 | 478 | 0.666 |
| Wil Dawson | 22 | 16 | −19.43 | 0.1826 | 667 | 240 | 0.359 |
| **Miller Bergman** | 38 | 15 | −16.74 | 0.2430 | 344 | 9 | **0.026** |
| Isaac Keeler | 44 | 13 | −15.84 | 0.2864 | 328 | 135 | 0.411 |
| **Alwyn Davey** | 45 | 20 | −17.19 | 0.1984 | 297 | 6 | **0.020** |

**The premise is PARTLY confirmed and the packet says so rather than rounding it either way.** The
price ratio runs 0.020 to 1.167, median **0.52**. **Two of the twelve sit at or below 0.25x.** The
0.24x figure is at the harsh end of what the board actually does, not the middle of it. **The
difference between a row at 0.52x and one at 0.02x is the production leg, which the charge does not
touch at all.**

**So the object to test is the pedigree mark `f`, not the price ratio, and that is what F5 tests.**

---

## 2 · THE VANTAGE, THE POPULATION, AND THE CENSORING

Stage `N` is the moment immediately after the player's `N`th season — exactly the state the engine
charges from:

- `g` = cumulative career games through depth `N` — the axis `A(g)` reads
- `s_P` = ORDER P's surplus over seasons 1..`N` — the axis `T(s)` reads
- `OUT` = the discounted house-ruler delivered value from depth `N+1` onward, over `v0`

| stage | rows | entry years | median games | median s_P | delisted share |
|---:|---:|---|---:|---:|---:|
| 1 | 644 | 2005-2020 | 7.0 | −7.86 | **65.4%** |
| 2 | 826 | 2005-2019 | 14.0 | −6.30 | **70.2%** |
| 3 | 849 | 2005-2018 | 23.0 | −5.01 | **73.9%** |

**Censoring, fixed before the run: at least four observed seasons after the vantage.** The last
several draft classes are absent from F5 entirely and **no claim here reaches them**.

**The direction of the censoring bias was written down before the result and it matters.** `OUT` sums
observed seasons to 2025 with **no projected tail**, unlike ORDER 30A-2's estimand. That biases `OUT`
downward for later cohorts, **which cuts AGAINST finding that the charge front-loads.** The finding
below survives that bias rather than being produced by it, and the six-season sensitivity moves it by
four hundredths.

**Rows with zero career games are excluded because `A(0) = 0` exactly — the charge cannot reach them.
Nothing else is excluded.**

---

## 3 · THE COMPARISON, AND WHY IT IS A RATIO

**The charged mark `f` and the realized outcome `OUT` are in different units and a level comparison
between them is meaningless.** The house ruler is not board currency and no constant converts one to
the other without a board build. Both are therefore taken relative to a reference cell at the **same
stage and the same games bin**, which makes both sides unit-free:

```
CALIBRATION = ( OUT(cell)/OUT(ref) ) / ( f(cell)/f(ref) )
```

**Above 1: the row delivers more than the charge marks him at, relative to his peer — front-loading.
Below 1: the charge is generous.** The reference cell is surplus 0 to −10, fixed in the prereg.

---

## 4 · THE CALIBRATION CURVE, PER CAREER STAGE

Delisted rows are in every cell as outcomes. `n` and the delisted share are printed for all of them.

### STAGE 1 — after the first season, 644 rows

| games | surplus | n | delisted | mean f | mean OUT | charged | realized | **CALIB** | 90% CI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1-9 | 0 to −10 *(ref)* | 168 | 67% | 0.9286 | 0.7217 | 1.000 | 1.000 | 1.000 | — |
| 1-9 | −10 to −20 | 96 | 70% | 0.6020 | 0.3639 | 0.648 | 0.504 | 0.778 | [0.515, 1.134] |
| 1-9 | −20 to −35 | 91 | 78% | 0.4866 | 0.4508 | 0.524 | 0.625 | 1.192 | [0.813, 1.680] |
| 1-9 | worse than −35 | 32 | 78% | 0.5261 | 0.3423 | 0.567 | 0.474 | 0.837 | [0.365, 1.519] |
| 10-22 | 0 to −10 *(ref)* | 178 | 52% | 0.8674 | 1.1977 | 1.000 | 1.000 | 1.000 | — |
| 10-22 | −10 to −20 | 56 | 68% | 0.3342 | 0.5475 | 0.385 | 0.457 | 1.187 | [0.800, 1.751] |
| **10-22** | **−20 to −35** | **11** | 73% | 0.1324 | 0.2611 | 0.153 | 0.218 | **1.428** *THIN* | [0.630, 2.372] |
| 23+ | 0 to −10 *(ref)* | 10 | 40% | 1.0000 | 1.2485 | 1.000 | 1.000 | 1.000 | — |

### STAGE 2 — after the second season, 826 rows

| games | surplus | n | delisted | mean f | mean OUT | charged | realized | **CALIB** | 90% CI |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1-9 | 0 to −10 *(ref)* | 121 | 79% | 0.8887 | 0.6097 | 1.000 | 1.000 | 1.000 | — |
| 1-9 | −10 to −20 | 72 | 82% | 0.6087 | 0.4004 | 0.685 | 0.657 | 0.959 | [0.409, 1.921] |
| 1-9 | −20 to −35 | 86 | 84% | 0.4883 | 0.2620 | 0.549 | 0.430 | 0.782 | [0.327, 1.623] |
| 1-9 | worse than −35 | 28 | 89% | 0.5205 | 0.3379 | 0.586 | 0.554 | 0.946 | [0.314, 2.013] |
| 10-22 | 0 to −10 *(ref)* | 164 | 68% | 0.8555 | 0.8269 | 1.000 | 1.000 | 1.000 | — |
| 10-22 | −10 to −20 | 71 | 73% | 0.3346 | 0.3995 | 0.391 | 0.483 | 1.235 | [0.806, 1.825] |
| **10-22** | **−20 to −35** | **27** | **93%** | 0.1412 | 0.3381 | 0.165 | 0.409 | **2.476** | **[1.286, 4.113]** |
| 23+ | 0 to −10 *(ref)* | 224 | 51% | 0.8674 | 1.3904 | 1.000 | 1.000 | 1.000 | — |
| 23+ | −10 to −20 | 25 | 68% | 0.2534 | 0.3857 | 0.292 | 0.277 | 0.949 | [0.681, 1.300] |
| 23+ | −20 to −35 | 7 | 100% | 0.0963 | 0.1716 | 0.111 | 0.123 | 1.111 *THIN* | [0.029, 2.659] |

### STAGE 3 — after the third season, 849 rows

| games | surplus | n | delisted | charged | realized | **CALIB** | 90% CI |
|---|---|---:|---:|---:|---:|---:|---|
| 1-9 | −10 to −20 | 52 | 90% | 0.638 | 0.752 | 1.179 | [0.475, 3.328] |
| 1-9 | −20 to −35 | 63 | 92% | 0.570 | 0.338 | 0.593 | [0.193, 1.759] |
| 1-9 | worse than −35 | 21 | 95% | 0.616 | 1.202 | 1.952 *THIN* | [0.246, 6.143] |
| 10-22 | −10 to −20 | 57 | 88% | 0.394 | 0.163 | **0.413** | **[0.245, 0.702]** |
| 10-22 | −20 to −35 | 32 | 97% | 0.158 | 0.245 | 1.555 | [0.326, 3.864] |
| 23+ | −10 to −20 | 59 | 80% | 0.300 | 0.239 | 0.798 | [0.542, 1.109] |
| 23+ | −20 to −35 | 14 | 86% | 0.105 | 0.116 | 1.097 *THIN* | [0.111, 2.678] |

**One cell runs the other way and it is not buried: stage 3, 10-22 games, −10 to −20 reads 0.413 with
an interval of [0.245, 0.702] that excludes 1 — there the charge is measurably GENEROUS.** That is a
third-year row with only 10-22 career games, i.e. a player who has barely played in three years, and
the charge lets him off relative to his peers. **It is the only separable cell in the whole table
pointing that way and it is stated as prominently as the ones pointing the other way.**

---

## 5 · VERDICT (1) — THE TAIL THE OWNER NAMED

| cell | n | delisted | charged | realized | **CALIB** | 90% CI | verdict |
|---|---:|---:|---:|---:|---:|---|---|
| stage 1, −20 to −35, 10-22 games | 11 | 73% | 0.153 | 0.218 | 1.428 *THIN* | [0.630, 2.372] | ON IT (CI covers 1) |
| stage 2, −20 to −35, 10-22 games | 27 | 93% | 0.165 | 0.409 | **2.476** | **[1.286, 4.113]** | **FRONT-LOADS** |
| worse than −35, 10-22 games | 1 each | — | — | — | — | — | too few to score |
| **POOLED stages 1+2, 10-22 games, all below −20 vs all at-or-above −10** | **40** | — | — | — | **1.9025** | **[1.2058, 2.7921]** | **FRONT-LOADS** |

**THE RATIO WITH ITS CI, WHICH IS WHAT THE ORDER ASKED FOR: 1.90, 90% CI [1.21, 2.79].**

**The realized value sits ABOVE the charged mark. The charge front-loads at the tail the owner
named.** **F5-P1 is confirmed on the pooled cell.** The reference cell holds 342 rows; the deep cell
holds 40.

**Both individual stage cells are thin — 11 and 27 rows — and F5-P5's prediction that a required cell
would come in under 25 players held. The pooled cell is where the sample is and it is the number to
quote.**

### 5.1 THE CAVEAT THAT MUST BE READ WITH IT — THE MEAN AND THE MEDIAN DISAGREE

The deep cell's outcomes are **option-shaped: 21 of 40 deliver essentially nothing (under 0.05 of
entry), and the cell mean is carried by 3 rows above 1.0.**

| statistic | deep cell | reference | ratio |
|---|---:|---:|---:|
| mean | 0.3039 | 1.0199 | 0.298 |
| median | 0.0386 | 0.3938 | 0.098 |
| share delivering above 0.5 of entry | 30.0% | 44.4% | 0.675 |

**On the MEAN the charge front-loads (CALIB 1.90). On the MEDIAN it does not (CALIB 0.63).**

**Both are true and they are not in conflict. The typical deep underperformer really is worth about
what the charge says. The AVERAGE one is worth about twice it, because a minority recover hard.**

**Which is the right comparison?** A multiplicative mark on a prior is a mean-like object — **it is a
price, and a price is an expectation, not a median** — so the mean is the like-for-like reading and it
is primary. **The same statistic choice already sits inside the wired mechanism: ORDER P fitted `BETA`
on cell means, and the sitter fade is a cell mean normalised by the depth-1 mean (F4 §2).** **The
median is printed because it disagrees, not despite it.** Anyone who prefers a median-based severity
should know that on that basis the current charge is not too harsh.

---

## 6 · VERDICT (2) — THE CONVICTION-SPEED ASSUMPTION

`G0 = 9.89` was measured from where the PRODUCTION slope `BETA(g)` saturates. Putting it inside the
charge assumes pedigree-conviction should firm at the same speed. **That assumption is tested here
directly, from outcomes alone.**

The mechanism implies `ln f(at-bar) − ln f(deep) = BETA_sat · A(g) · Δs`. Inverting it recovers an
**empirical A**:

```
A_hat(g) = -ln( OUT(deep,g) / OUT(at-bar,g) ) / ( BETA_sat * Δs(g) )
```

Stages 1-3 pooled, because `A(g)` is a pure function of `g` in the mechanism. `A_hat` is not bounded
to [0,1] by construction and is printed raw.

| games | n deep | n ref | OUT deep | OUT ref | Δs | **A_hat** | **A(g) wired** |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1-4 | 240 | 166 | 0.3317 | 0.4751 | 31.94 | **0.098** | 0.202 |
| 5-9 | 81 | 199 | 0.2383 | 0.7062 | 27.27 | **0.348** | 0.500 |
| 10-14 | 43 | 188 | 0.1830 | 0.9890 | 26.14 | **0.563** | 0.699 |
| 15-19 *thin* | 23 | 165 | 0.2990 | 0.9394 | 27.22 | **0.367** | 0.820 |
| 20-24 *thin* | 13 | 165 | 0.2821 | 0.9630 | 24.99 | **0.429** | 0.891 |
| 25-34 *thin* | 8 | 193 | 0.3307 | 1.2863 | 25.11 | **0.472** | 0.948 |
| 35+ *thin* | 8 | 339 | 0.0855 | 1.4461 | 28.89 | **0.854** | 0.991 |

**THE RAWEST FORM OF THE RESULT, before any curve is fitted: the empirical A sits BELOW the wired
`A(g)` in 7 of the 7 scored games bins.** Four of the seven bins hold fewer than 25 deep rows and are
marked thin.

### 6.1 The fit

| fit | G0_hat | 90% CI | amplitude C |
|---|---:|---|---:|
| `A_hat = 1 − exp(−g/G0)` — amplitude pinned at 1, **as the mechanism has it** | **21.53** | **[12.98, 28.99]** | 1 (fixed) |
| `A_hat = C·(1 − exp(−g/G0))` — amplitude free | 9.36 | [4.79, 400.0] | **0.620** [0.484, 11.60] |
| **the wired value** | **9.89** | **[7.60, 12.98] published** | 1 |
| stage-1 only, sensitivity | 20.90 | — | 1 |

**`G0_hat = 21.53` — more than twice the wired 9.89 — and its 90% CI [12.983, 28.993] fails to
overlap the published [7.60, 12.98] by three thousandths.**

**THAT SEPARATION IS A HAIRLINE AND IS REPORTED AS ONE. Nobody should read a 0.003-wide gap as
decisive.** **F5-P2 did not fire** — the point estimate is above the published interval, as predicted —
but the interval barely clears it and the honest statement is "the two are on the edge of separable",
not "the published interval is refuted".

### 6.2 Two readings, and the data cannot separate them

- **(a) Conviction firms about twice as slowly as assumed.** `G0 ≈ 21.5`, amplitude 1.
- **(b) Conviction firms at about the assumed speed but only ever reaches 62% of the assumed
  strength.** `G0 ≈ 9.4`, amplitude 0.62.

Reading (b)'s amplitude CI is [0.484, 11.60] and its `G0` CI runs to the search bound. **The data
cannot tell speed from strength here.**

**WHAT BOTH READINGS AGREE ON — and this is the finding — is that the charge convicts HARDER than
outcomes support at every games level measured.** Whether the repair belongs in `G0`, in `BETA_sat`,
or in `LAMBDA` is a construction choice, and **this seat does not make it.**

---

## 7 · F5-P3 — THE TAIL FLATTENS, EXACTLY WHERE `TMAX` ASSUMES IT DOES

| cell (stages 1+2 pooled) | n | mean OUT | 90% CI |
|---|---:|---:|---|
| −10 to −20 | 320 | 0.4139 | [0.337, 0.491] |
| −20 to −35 | 223 | 0.3442 | [0.263, 0.437] |
| worse than −35 | 62 | 0.3318 | [0.184, 0.515] |

**Not separable. F5-P3 did not fire.** Beyond about −20 points a game, being worse tells you nothing
more about the outcome. **That is the empirical question `TMAX` exists to answer, and the answer
vindicates having a cap.** It says nothing about where the cap should sit.

---

## 8 · F5-P4 — SURVIVAL, HANDLED AS OUTCOMES

**Delisted rows are outcomes, not exclusions. Dropping them is the survivor bias this seat
preregistered against, and the last column shows exactly how much it would have flattered the
charge.**

| surplus band (stage 1) | n | delisted | mean OUT | mean OUT *if survivors only* |
|---|---:|---:|---:|---:|
| 0 to −10 | 356 | 59% | 0.9745 | 1.3857 |
| −10 to −20 | 152 | 69% | 0.4315 | 0.5421 |
| −20 to −35 | 103 | 78% | 0.4262 | 0.6938 |
| worse than −35 | 33 | 79% | 0.3330 | **1.0218** |

**The delisted share rises monotonically with the depth of underperformance. F5-P4 did not fire.**

**Read the last row.** A survivor-only reading would have said the very worst underperformers deliver
1.02 of entry — more than a near-bar player on the same reading — because the four-fifths who were
delisted would have vanished from the average. **That column is printed once, is used nowhere, and is
the reason the whole measurement keeps delisted rows in.**

---

## 9 · SENSITIVITIES

| reading | n deep | CALIB | 90% CI lower |
|---|---:|---:|---:|
| **primary (mean, ND, ≥4 future seasons)** | **40** | **1.9025** | **1.199** |
| ≥ 6 future seasons | 36 | 1.8643 | 1.190 |
| every pathway, not ND only | 50 | 2.3207 | 1.141 |
| median instead of mean | 40 | **0.6263** | — |
| pooled aggregate, v0-weighted | 40 | 2.4559 | — |

**Three of the four ratio readings sit above 1 and the interval clears 1 on all three that carry one.
The median is the exception and it is §5.1's caveat, not a sensitivity failure.**

### 9.1 The already-priced softenings, for reference only

**ORDER R priced these. NONE IS RECOMMENDED HERE and no new constant is derived.** This is only so the
owner can see whether anything already on the record lands where the measurement points.

| variant | f at the owner's shape | charged ratio | CALIB |
|---|---:|---:|---:|
| **ORDER P as wired** | 0.1985 | 0.157 | **1.903** |
| TMAX at p15 | 0.1985 | 0.201 | 1.479 |
| TMAX at p20 | 0.1985 | 0.254 | 1.174 |
| BETA_sat at its CI floor | 0.2273 | 0.184 | 1.622 |
| **BETA_sat floor + TMAX p20** | 0.2273 | 0.286 | **1.041** |

**Read the last row as arithmetic and nothing more: the combination of two softenings the owner
already ruled on, both already priced by ORDER R, lands the tail calibration at 1.04 against the
wired 1.90.** **This seat is not recommending it.** It is recording that the measurement points inside
the range of variants already on the record rather than outside it, which is a fact the owner should
have when he rules.

**Note what the `f at the owner's shape` column does and does not do.** Neither `TMAX` variant moves
that row at all (0.1985 either way) — the cap only reaches rows parked at it, which is exactly what
ORDER R measured. **The `TMAX` lever fixes the calibration at the tail without touching the owner's
own illustrative shape.** That is a real distinction and it should not be blurred.

---

## 10 · THE FALSIFIER SCORECARD

| # | falsifier | fired? |
|---|---|---|
| **F5-A1** | the constants do not match the engine block | **no** — asserted to 1e-15 |
| **F5-A2** | the premium surface is not the built one | **no** — asserted to 1e-9 |
| **F5-P1** | the CI on CALIBRATION contains or sits below 1 | **no** — 1.90 [1.21, 2.79] on the pooled tail |
| **F5-P2** | `G0_hat` sits inside the published [7.60, 12.98] | **no** — 21.53 [12.98, 28.99], but the separation is a hairline of 0.003 |
| **F5-P3** | the two deepest surplus cells separate | **no** — they overlap; the tail flattens |
| **F5-P4** | the delisted share does not rise with depth | **no** — it rises monotonically |
| **F5-P5** | every required cell clears 25 players | **FIRED** — the stage-1 tail cell holds 11 |

**Prereg deviations, declared.** Nothing removed. Three additions: the mean/median caveat block in
§5.1, which the prereg promised as "both are reported" but did not promise as its own section and
which materially qualifies the headline; the split of the owner's premise into its pedigree-leg and
price halves in §1; and the note in §9.1 that the `TMAX` lever does not move the owner's own
illustrative shape.

---

## 11 · EVERY LIMITATION

- **The mean/median disagreement is the largest one and it is in the body, not here.** On a
  median-based reading of severity the current charge is not too harsh.
- **Thin cells.** The stage-1 tail cell holds 11 rows; the stage-2 tail cell 27. Four of the seven
  games bins in the speed test hold fewer than 25 deep rows. The pooled tail cell holds 40. **Every
  one of those is marked in place.**
- **The `G0` separation is 0.003 wide.** It is at the edge of significance, not past it.
- **Speed and strength cannot be separated.** Readings (a) and (b) in §6.2 fit the same data.
- **Censoring.** Entry year ≤ 2021 − stage; the last several draft classes are absent. The outcome
  carries no projected tail, which biases it down for later cohorts. **That bias runs against the
  finding, so the finding is conservative — but it also means the levels of `OUT` are not comparable
  to ORDER 30A-2's, which does carry a tail.**
- **Selection, not causation.** `OUT` compares players who produced below their bar with players who
  did not. It does not isolate the effect of underperforming from the effect of being the sort of
  player who underperforms. **The wired mechanism was derived on exactly the same kind of comparison,
  so the two are like-for-like — but neither is causal and this seat is not claiming otherwise.**
- **One reference cell.** Everything is relative to the 0-to-−10 surplus cell at the same stage and
  games. A different reference moves every ratio.
- **`s_P` at the historical vantage is computed offline** from `op_lib`, not from an engine run, so it
  carries the offline/engine differences ORDER Q measured (board rounding, the M3 double call). Those
  are small relative to the cell widths here but they are not zero.
- **The `A_hat` inversion assumes the mechanism's own algebra holds.** If the true relationship
  between surplus and outcome is not log-linear in `Δs`, `A_hat` absorbs that misspecification into
  what looks like a speed result. **The free-amplitude fit is the partial check on that and it is
  reported.**
- **Nothing here tests `LAMBDA`, the anchoring identity, or any rail.** F5 is one measurement of one
  assumption.

---

## 12 · WHAT IS OWED, AND WHAT THIS SEAT DID NOT DO

- **No repair is proposed.** The measurement says the charge convicts harder than outcomes support and
  gives the fitted values with their intervals. **Choosing where the repair belongs — `G0`,
  `BETA_sat`, `TMAX`, `LAMBDA`, or none of them — is the owner's and the supervisor's.**
- **No board was built**, so nothing here says what any repair would do to the rails, the class mark,
  the veteran caps, or the band tables. **A variant that changes `G0` changes `A(g)` on every young
  row, and `LAMBDA` was solved by an anchoring identity that a `G0` move would break.** That is the
  next step and it is not this seat's.
- **The out-of-sample test is still owed**, on this and on every premium object: everything here is
  fitted and evaluated on overlapping populations.

---

## 13 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_SRO_F5.md` | the prereg addition, pushed at `7b114e9` before any number existed |
| `os_f5.py` · `F5_CALIB.json` · `F5_CALIB_out.txt` | the measurement, the calibration curve, the speed test, the sensitivities |
| `os_f5_run.txt` | the raw console of the run |

**Nothing in this directory is adopted, nothing lands, and F5 proposes no repair.**
