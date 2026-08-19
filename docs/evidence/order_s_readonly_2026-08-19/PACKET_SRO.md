# PACKET SRO — THE POSITION LEVEL, AND THE SELECTION HANDOFF

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Prereg:** `PREREG_SRO.md`, pushed at `09d5e3f` before any number in this packet existed.

**NO BOARD WAS BUILT. NO ENGINE FILE WAS EDITED. NO DIAL WAS ADDED. NO STORE WAS WRITTEN.
NOTHING IS ADOPTED. NOTHING LANDS. NO PULL REQUEST WAS OPENED. NOTHING WENT TO `main`.
NO FIX IS RECOMMENDED IN EITHER TASK.**

The engine was loaded in-process for reading, thread-pinned, one run at a time. Board totals
reproduce the built boards exactly: ORDER P **666,434** (`374d4e44`) and ORDER K **673,097**
(`f3101883`).

**No named player gated any number.** Named rows appear only where the derived rule puts them.

---

## 0 · THE TWO VERDICTS, ONE LINE EACH

**T1.** **NOT A NULL.** Three of the six positions differ from the pooled bar by more than sampling
noise — **SD is over-barred by 2.98 points a game, RUCK by 5.57, and SF is UNDER-barred by 2.71** —
so the pooled level is NOT vindicated, even though ORDER R's slope test found no position separable.

**T2.** **Non-selection is priced ONCE, by the sitter fade, and NOT AT ALL by the charge — but on
19 of 53 stale rows the fade is 1.000 and the missing season costs nothing anywhere; on 10 of them
neither mechanism moves the price by a single board point; and on 8 board rows it is priced TWICE,
once on the production leg and once on the pedigree leg.**

---

# PART ONE · T1 — THE PG LEVEL BY POSITION

## 1 · WHAT WAS MEASURED, AND WHAT WAS NOT

ORDER R measured the SLOPE `dPG/dln(v0)` per position, found every pairwise 90% CI overlapping, and
ruled the TALL/SMALL pooling defensible on that axis. **It did not test the level.** This is the
level companion.

The object, per season row:

```
resid  =  season avg  -  [ o32_gate_bar(pos, age)  +  PG_pooled(ln v0, class) ]
```

reported as the **games-weighted mean of `resid` per position**. Positive means the position produces
above the bar it is judged against — under-barred. Negative means over-barred.

**Everything about the estimator is ORDER P's own** and is asserted, not assumed:

- The population is ORDER P's: **5,041 season rows, 1,575 players, 58,488 games** — asserted equal to
  `PREMIUM_SURFACE.json`'s own counts. Falsifier SRO-P1 did not fire.
- The fit is ORDER P's `op_lib.Premium`, reproduced **node for node to under 1e-12**, and equal to
  the BUILT engine surface `O37_PG_GRID` to under 1e-9. Falsifier SRO-P2 did not fire.
- Intervals are player-level cluster bootstraps, **2,000 draws, seed 32**, and **the premium surface
  is refitted inside every draw**, so the interval carries the estimation noise in `PG` and not only
  the sampling noise in the residual. That was written into the prereg before the run.

## 2 · THE CONTROL FIRST — AND IT PASSES

The pooled surface is fitted on exactly these rows, so the games-weighted mean residual over a whole
CLASS has to sit on zero. If it did not, this seat would have misread the estimator.

| class | mean residual | 90% CI | verdict |
|---|---:|---|---|
| TALL | **−0.104** | [−0.263, +0.112] | PASS |
| SMALL | **+0.086** | [−0.023, +0.291] | PASS |

**Falsifier SRO-1 did not fire.**

**The consequence, stated before the table below is read.** Because the class mean is pinned at zero,
a position offset inside a class is a **redistribution between that class's three positions**. If one
is over-barred another must be under-barred. "Every position is over-barred" is not a result this
estimator can produce and nobody should read it out of the table.

## 3 · THE HEADLINE — THREE OF SIX POSITIONS ARE SEPARABLE ON LEVEL

Games-weighted mean residual, in AFL Fantasy points a game, pooled over price.

| position | rows | games | mean residual | 90% CI | CI excludes zero? |
|---|---:|---:|---:|---|---|
| KPD | 462 | 4,903 | +0.631 | [−0.332, +1.717] | no |
| KPF | 628 | 6,841 | +0.789 | [−0.064, +1.603] | no |
| **RUCK** | 206 | 1,778 | **−5.569** | **[−8.178, −2.900]** | **YES — over-barred** |
| MID | 1,380 | 16,841 | −0.348 | [−1.135, +0.556] | no |
| **SD** | 977 | 11,687 | **−2.978** | **[−4.329, −1.661]** | **YES — over-barred** |
| **SF** | 1,388 | 16,438 | **+2.709** | **[+1.834, +3.673]** | **YES — under-barred** |

**Falsifier SRO-2 did not fire on its main clause: this is not a null.** Three positions are
separable from zero and, pairwise inside SMALL, MID / SD / SF are all separable from each other.

**The DIRECTION this seat preregistered was half wrong, and that is reported as prominently as the
half that was right.** The prereg predicted MID positive and SF negative. **MID came out a null
(−0.35, interval covering zero) and SF came out POSITIVE (+2.71).** The prediction that "cheap
positions are over-barred" holds for SD and fails for SF, which is the cheaper of the two in median
entry price (441 against 664 for MID, and 367 for SD). **So the owner's Travaglia lead is confirmed
for SD and refuted for SF. It is not a "cheap position" effect. It is an SD effect and a RUCK
effect.**

### 3.1 Pairwise, inside each class

| pair | A | B | A − B | 90% CI of A − B | separable? |
|---|---:|---:|---:|---|---|
| MID vs SD | −0.348 | −2.978 | +2.630 | [+0.753, +4.596] | **SEPARABLE** |
| MID vs SF | −0.348 | +2.709 | −3.058 | [−4.489, −1.625] | **SEPARABLE** |
| SD vs SF | −2.978 | +2.709 | −5.688 | [−7.678, −3.804] | **SEPARABLE** |
| KPD vs KPF | +0.631 | +0.789 | −0.158 | [−1.789, +1.615] | no |
| KPD vs RUCK | +0.631 | −5.569 | +6.200 | [+3.241, +9.325] | **SEPARABLE** |
| KPF vs RUCK | +0.789 | −5.569 | +6.358 | [+3.120, +9.328] | **SEPARABLE** |

The differences are bootstrapped as differences INSIDE each draw. Both positions share one fitted
surface in a draw, so their errors are correlated and differencing two separately-computed intervals
would overstate the spread.

## 4 · WHERE IT BINDS BY PRICE — AND A PREREGISTERED PREDICTION THAT FIRED

| position | below the class median v0 | above it | the expensive tail (v0 > class p90) |
|---|---:|---:|---:|
| KPD | +1.123 | +0.003 | −0.910 THIN |
| KPF | +0.518 | +0.945 | +0.363 |
| RUCK | **−8.237** [−11.23, −5.50] | **−4.098** [−7.71, −0.40] | −1.814 THIN |
| MID | −0.896 | −0.108 | −1.113 |
| SD | **−2.760** [−4.85, −0.93] | **−3.210** [−4.97, −1.52] | −1.486 |
| SF | **+3.252** [+1.95, +4.70] | **+2.156** [+0.97, +3.37] | +0.213 |

**Falsifier SRO-3 FIRED. The prereg predicted the offsets would be LARGER in the expensive tail. They
are SMALLER — every one of the six tail intervals covers zero.** The offsets bind hardest at and
below the class median and fade out at the top. The tail cells hold 18 to 212 rows and two of them
are printed THIN, so part of that is width rather than a real collapse; but the point estimates fall
too, not only the confidence, so this seat reports the prediction as fired rather than as
inconclusive.

**Falsifier SRO-4 half fired.** RUCK does carry the widest pooled interval of the six (5.278 points a
game against KPF's 1.666), which is what was predicted. **But it is rulable anyway — its interval
excludes zero.** ORDER R found RUCK's SLOPE not estimable at all (bootstrap upper limit +918.83).
**Its LEVEL is estimable and materially negative.** That is a genuine difference between the two
tests and it is the clearest single illustration of why the level test was worth running.

## 5 · WHERE THE OFFSET COMES FROM

| position | vs the AGE bar alone | mean premium its prices earn it | vs the POOLED bar |
|---|---:|---:|---:|
| KPD | +5.878 | +5.248 | +0.631 |
| KPF | +7.739 | +6.950 | +0.789 |
| **RUCK** | **+2.448** | **+8.017** | **−5.569** |
| MID | +6.846 | +7.195 | −0.348 |
| **SD** | **−0.027** | **+2.952** | **−2.978** |
| **SF** | +6.142 | +3.433 | **+2.709** |

Read RUCK's row. A young ruck produces **2.4 points a game above his own age bar** — the weakest of
the six. His entry prices are high enough that the pooled TALL premium hands him **+8.0 points a game
of extra bar**. The gap between those two numbers IS the −5.57.

Read SD's row. A young small defender produces **0.0** above his age bar — he sits ON it — and his
prices earn him **+3.0** of extra bar. The gap is the −2.98.

Read SF's row. He produces **+6.1** above his age bar and his cheap prices earn him only **+3.4**, so
he is left **+2.7** to the good.

### 5.1 Is it flat in age? For SD yes. For RUCK no.

Mean residual by position and age. Cells under 40 rows are marked and are not read.

| position | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---:|---:|---:|---:|---:|---:|
| KPD | −21.42* | +0.87 | +2.34 | +0.32 | +0.55 | +0.26 |
| KPF | −12.66* | −3.18 | −0.18 | +0.63 | +1.99 | +2.34 |
| **RUCK** | — | −15.18* | −17.60* | **−8.96** | **−5.42** | **+3.84** |
| MID | −8.59* | −6.86 | −3.35 | −0.15 | +2.41 | +3.87 |
| **SD** | +1.35* | **−2.99** | **−5.57** | **−2.14** | **−3.48** | **−1.53** |
| **SF** | −0.81* | +0.07 | +2.05 | +3.13 | +4.62 | +2.38 |
| rows | 39 | 808 | 1,040 | 1,102 | 1,072 | 980 |

**These are two different findings and they should not be merged.**

- **SD's offset is flat in age** — between −1.5 and −5.6 at every age with rows, no trend. That is a
  LEVEL problem: either SD's own flat bar or the pooled premium puts him in the wrong place, and it
  is `PG`'s to answer for.
- **RUCK's offset runs from −9.0 at 21 to +3.8 at 23** and the age-19 and age-20 cells are thin. That
  is a DEVELOPMENT-CURVE shape, and the object that carries development is the **class-pooled C3 age
  delta in `o32_gate_bar`, not `PG`**. A ruck develops later than a key forward and the TALL class
  delta averages the two. **Splitting `PG` by position would not fix RUCK's problem, because RUCK's
  problem is in a different object.** This seat says so plainly rather than letting the −5.57 be read
  as an argument for a per-position premium.
- **MID, KPD and KPF have a clear age slope too** (MID −6.9 at 19 to +3.9 at 23), which is the same
  class-pooled development delta showing up. ORDER P §4.4 already measured that the premium is not
  flat in age and priced the age-carrying variant as worse on every rail. This table is the
  per-position version of that finding and it points at the same object.

## 6 · THE OWNER'S SENTENCE, CHECKED ARITHMETICALLY

*"An SD is priced ~18% below a MID at the same pick but barred only ~2-7% lower."*

**That is the separate question of how much the bar moves when the price moves, and the residual
table above does not answer it. Here it is answered on the engine's own positional day-0 curve
(`pvc_curve_v2.json::nd_v0.posv`), at age 19, in engine currency.**

How far BELOW MID is each position priced, and how far below MID is it barred?

| pick | KPD price / bar | KPF price / bar | RUCK price / bar | SD price / bar | SF price / bar |
|---:|---|---|---|---|---|
| 1 | −16.7% / −19.7% | −27.5% / −30.5% | −14.4% / −5.6% | **−17.6% / −7.3%** | −21.3% / −17.4% |
| 3 | −15.1% / −26.3% | −25.4% / −31.1% | +2.6% / −0.8% | **−16.4% / −7.0%** | −14.6% / −15.9% |
| 5 | −29.6% / −25.1% | −27.9% / −27.3% | +0.6% / −11.5% | **−22.6% / −7.2%** | −23.2% / −17.4% |
| 10 | −42.1% / −25.1% | −29.4% / −25.9% | −22.6% / −6.8% | **−18.2% / −8.6%** | −37.6% / −22.9% |
| 20 | −30.2% / −18.4% | −21.4% / −20.1% | +16.0% / −0.1% | **−15.1% / −3.9%** | −40.9% / −19.6% |
| 30 | −35.5% / −19.4% | −25.2% / −20.9% | +40.7% / +1.2% | **−45.5% / −13.2%** | −44.0% / −24.3% |
| 40 | −35.1% / −20.0% | −39.8% / −23.5% | +20.9% / +1.6% | **−50.4% / −12.4%** | −37.8% / −24.4% |

**The owner's arithmetic is right about SD and his estimate of the gap is if anything conservative.**
At pick 10 an SD is priced 18.2% below a MID and barred 8.6% below him. At pick 30 he is priced
45.5% below and barred 13.2% below. **The bar moves about a third to a quarter as far as the price
does.**

**But it is right about every other position too, and about SF most of all** — at pick 20 an SF is
priced 40.9% below MID and barred 19.6% below. **The bar under-tracking the price is a general
property of the construction, not an SD special case.** Its cause is arithmetic and simple: the
premium is ADDITIVE in points a game on a bar of 50 to 80, and its slope is about 9 points a game per
log-unit of price, so an 18% price cut moves the bar by `9.0 × ln(0.82) = −1.77` points a game — about
3% of a 60-point bar. **A proportional price cut cannot produce a proportional bar cut inside an
additive premium. That is a fact about the shape, and it is the same fact for every position.**

**And it is NOT the same thing as the residual test.** SF's bar under-tracks his price by more than
SD's and SF is nonetheless UNDER-barred. **Under-tracking says nothing about whether the resulting
bar is right. Only the residual does.** The two are printed together because the order asked the
question in the first language and the answer lives in the second.

## 7 · WHAT IT IS WORTH — IN BOARD POINTS, ON THE ACTUAL BOARD

The offsets above are in points a game. Here is what they are worth in the owner's units.

**This is a counterfactual READ and NOT a proposal.** Hold everything else fixed and move each row's
`s_P` by his own position's measured offset — exactly what the bar would have done if it carried that
position's level instead of the pooled one. **Falsifier SRO-B1 did not fire: the charge factor
recomputed here reproduces the engine's own `f` to under 1e-9, and at offset zero it moves nothing.**

The charge can only reach **289 of the 804 board rows**: under 24, with career games, with a readable
`s_P`.

| position | rows | total board points | median row | worst row | below median v0 | above it | the tail |
|---|---:|---:|---:|---:|---:|---:|---:|
| KPD | 24 | −98 | −1.6 | −18 | −32 | −66 | +0 |
| KPF | 42 | −214 | −2.8 | −56 | −45 | −92 | −77 |
| **RUCK** | 13 | **+204** | 0.0 | +68 | +102 | +102 | +0 |
| MID | 81 | +321 | +1.7 | +41 | +15 | +182 | +124 |
| **SD** | 60 | **+726** | **+5.5** | +89 | **+264** | **+397** | +64 |
| **SF** | 69 | **−684** | **−5.8** | −72 | **−393** | **−291** | +0 |
| ALL | 289 | +255 | | | | | |

Positive means the row is currently charged too much and would gain that many points if the bar
carried his own position's level.

**In one sentence: the over-charge on SD is about 726 board points spread over 60 rows, a median of
5.5 points a row and a worst row of 89; the matching under-charge on SF is 684 points over 69 rows.
On a 666,434-point board that is one tenth of one per cent in each direction.**

**The price ranges it binds in.** For SD it is spread across the whole range and is slightly larger
ABOVE the class median (397 points on 20 rows) than below (264 on 39). For SF it is largest BELOW the
median (−393 on 50 rows). **The expensive tail carries almost none of it** — consistent with §4.

**Six numbers, and they do not net to zero.** They net to zero within each class on the FITTED
population, but the board is a different population: one as-of year, one age window, one set of
prices, and each row moves in proportion to his own pedigree leg and his own `A(g)`.

The rows the offset moves most, printed wherever the rule puts them and chosen by nothing else:

| row | pos | age | games | v0 | f now | f counterfactual | board | move |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Koltyn Tholstrup | SD | 21 | 40 | 1,243 | 0.818 | 1.000 | 1,655 | +89 |
| Leo Lombard | SF | 20 | 25 | 1,005 | 0.560 | 0.421 | 1,540 | −72 |
| Mitchell Edwards | RUCK | 21 | 16 | 1,060 | 0.189 | 0.315 | 1,237 | +68 |
| Zeke Uwland | SD | 19 | 17 | 2,454 | 0.153 | 0.203 | 1,486 | +64 |
| Harry Kyle | SD | 19 | 7 | 1,040 | 0.464 | 0.552 | 841 | +60 |
| Cooper Duff-Tytler | KPF | 19 | 13 | 1,765 | 0.789 | 0.739 | 1,824 | −56 |

**The share of the young charged board each position carries**, because a large offset on a small
population is a small problem:

| position | rows | share of rows | board points | share of points |
|---|---:|---:|---:|---:|
| KPD | 24 | 8.3% | 20,564 | 7.1% |
| KPF | 42 | 14.5% | 34,543 | 11.9% |
| **RUCK** | **13** | **4.5%** | **7,879** | **2.7%** |
| MID | 81 | 28.0% | 148,265 | 51.1% |
| SD | 60 | 20.8% | 43,594 | 15.0% |
| SF | 69 | 23.9% | 35,503 | 12.2% |

**RUCK carries the biggest offset per point of production and the smallest share of the board: 13
rows and 2.7% of the value.**

## 8 · RECONCILING WITH ORDER R's SLOPE NULL

**They do not contradict each other, and neither substitutes for the other.**

A pooled fit `PG(x)` can have the right SLOPE for every position and still put a given position at
the wrong ORIGIN. ORDER R measured `dPG/dln(v0)` — how fast the bar rises with price — and found no
pair separable. This seat measured `E[avg − bar]` — where the bar SITS for that position — and found
three of six separable.

Concretely, if SD's true premium curve is the SMALL pooled curve shifted DOWN by 3 points a game,
then the two positions have identical slopes at every price (R's finding) and SD is charged against a
bar 3 points too high at every price (this finding). **Both measurements are correct and they are
measuring different coefficients of the same line.**

**Three things follow, and this seat rules on none of them.**

1. ORDER R's conclusion that a per-position SPLIT is not statistically supportable stands untouched.
   Nothing here re-opens it; a level offset does not need a per-position slope to be described.
2. The level offsets are, on the fitted population, a zero-sum redistribution INSIDE each class. They
   move SD and SF against each other and RUCK against KPD and KPF. **They do not change the pooled
   level and they cannot be used to argue the whole premium is too high or too low.**
3. **RUCK's offset is very likely not `PG`'s to answer for at all** (§5.1). It runs strongly with age
   and the object that carries age is the class-pooled C3 delta.

## 9 · T1's LIMITATIONS, ALL OF THEM

- **In-sample.** The residuals are measured against a surface fitted on the same rows. There is no
  hold-out. ORDER P owed this already and it is still owed.
- **Survivor bias, inherited.** The premium is estimated on players who PLAY. A cheap player must be
  good to be selected; an expensive one plays anyway. That biases the premium DOWN at the cheap end,
  which biases the residual at the cheap end UP. **SF's positive residual is exactly where that bias
  would put it, and this seat cannot separate the two.** SD's is not, since SD sits at a similar
  price to SF.
- **Thin cells, named.** The age-18 row holds 39 rows in total and is marked in every table. The
  expensive-tail cells for KPD (19 rows) and RUCK (18) are marked THIN. RUCK holds 206 rows and 96
  players in total, the smallest of the six.
- **RUCK's interval is the widest of the six** (5.278 points a game pooled over price).
- **One as-of year for the board translation.** §7 is measured at `Y = 2026` on 289 charged rows. It
  is not a claim about any other year.
- **The class-level control is not exactly zero** (−0.104 / +0.086); it is inside the declared 0.5
  band but it is not identically zero, because the isotonic guard and the 1-99 percentile support
  boundary both bite slightly.
- **The price cuts are unweighted row percentiles of `v0` within class,** not games-weighted.
- **The age table is point estimates only.** No intervals were computed on the position-by-age cells
  and they should not be read as separable from each other.

---

# PART TWO · T2 — THE SELECTION HANDOFF AUDIT

## 10 · THE FOUR MECHANISMS, AND HOW THEY WERE READ

Every number below is READ out of the engine's own functions at the exact call site where the price
is formed, using ORDER Q's read-and-delegate pattern. **No arithmetic was changed anywhere.**

```
price   = rho31(g)*e  +  pi*ped  +  o32_age_credit
pi      = pi_base * f
pi_base = D_final*(1 - rho)  +  Phi(g,s)*beta(g)*rho
D_raw   = the fade schedule at the UNPLAYED depth c_u = clock - played units
D_kap   = D_raw ** kappa(effective pick, TALL/SMALL)
D_final = min(1, D_kap * (1 + 1.08*sigma_sel))                        == the engine's own o31_D
f       = exp(-LAMBDA*A(g)*T(s_P))  below 24, the ORDER K blind charge otherwise
```

| assert | result |
|---|---|
| the reassembled price against the engine's own `ev()` | **worst error 9.09e-13 on 804 of 804 rows** |
| the recomputed fade chain against the engine's own `o31_D()` | **worst error 0, exactly** |
| board total, ORDER P dial line | **666,434 — the built board `374d4e44`** |
| board total, ORDER K dial line | **673,097 — the built board `f3101883`** |

Falsifiers SRO-T1 and SRO-T2 did not fire. The tolerance was declared at 1e-6 in the prereg.

Two counterfactuals wrap a function **in the loaded namespace only** and both are inert at their
identity setting: `_staleness_grade → 1.0` (which makes the D8 arm `min(e, e) = e` identically), and
the tall exponent replaced by ORDER D's pooled exponent (which is exactly what `RL_O36_TALL=0` falls
back to). **No repository file was touched.**

## 11 · (a) THE BOARD POPULATION BY STALENESS

804 priced rows carry a pedigree leg at `Y = 2026`.

| window | career games > 0 and ZERO in window | 1-2 games in window |
|---|---:|---:|
| the last 1 season | **53** | 52 |
| the last 2 seasons | **12** | 30 |
| the last 3 seasons | **3** | 29 |

89 further rows have never played at all. `A(0) = 0` exactly, so the charge cannot reach them; they
are not this task's population and are listed for completeness.

**The stale(1) population by age band and class:**

| age band | TALL | SMALL | total | median career games | median board price |
|---|---:|---:|---:|---:|---:|
| 20 and under | 3 | 4 | 7 | 4.0 | 591 |
| 21-23 | 6 | 13 | 19 | 15.0 | 141 |
| 24-26 | 6 | 10 | 16 | 34.2 | 102 |
| 27+ | 2 | 9 | 11 | 109.0 | 180 |

**By career games, because that is the only games axis the charge reads:**

| career games | stale(1) | stale(2) | stale(3) | A(g) at the band midpoint |
|---|---:|---:|---:|---:|
| 1-3 | 9 | 4 | 1 | 0.141 |
| 3-10 | 8 | 1 | 0 | 0.482 |
| 10-25 | 10 | 1 | 0 | 0.830 |
| 25-60 | 11 | 4 | 2 | 0.986 |
| 60-150 | 11 | 2 | 0 | 1.000 |
| 150+ | 4 | 0 | 0 | 1.000 |

**The stale(2) and stale(3) cells hold 12 and 3 rows. They are thin and every number computed on them
in this packet is printed as thin.**

## 12 · (b) THE LEGS — HOW MUCH OF EACH ROW'S PRICE EACH MECHANISM MOVED

Board points. Positive = the mechanism removed that many points from the row.

| group | n | med g | med c_u | med D | med f | med rho | CHARGE total | FADE total | med chg | med fade |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FRESH (played in 2026) | 662 | 76.0 | 0.00 | 1.000 | 0.993 | 0.884 | 32,504 | 4,278 | 0.2 | 0.0 |
| **STALE(1)** | 53 | 23.0 | 2.00 | 0.633 | 0.741 | 0.601 | 3,796 | 2,536 | 18.9 | 20.4 |
| STALE(2) *thin* | 12 | 26.0 | 3.92 | 0.566 | 0.714 | 0.625 | 613 | 1,208 | 22.3 | 85.1 |
| STALE(3) *thin* | 3 | 31.5 | 3.92 | 0.566 | 0.702 | 0.669 | 90 | 225 | 20.6 | 31.7 |
| stale(1), age ≤20 | 7 | 4.0 | 1.92 | 0.597 | 0.661 | 0.318 | 1,795 | 425 | 37.0 | 66.3 |
| stale(1), age 21-23 | 19 | 15.0 | 2.50 | 0.630 | 0.649 | 0.531 | 1,489 | 1,232 | 35.0 | 6.9 |
| stale(1), age 24-26 | 16 | 34.2 | 2.96 | 0.566 | 0.755 | 0.689 | 485 | 727 | 18.3 | 29.4 |
| **stale(1), age 27+** | 11 | 109.0 | **1.00** | **1.000** | **0.996** | 0.944 | **27** | **153** | **0.2** | **0.0** |
| stale(1), TALL | 17 | 7.0 | 3.92 | 0.630 | 0.744 | 0.417 | 881 | 1,189 | 20.6 | 48.6 |
| stale(1), SMALL | 36 | 30.5 | 1.92 | 0.840 | 0.734 | 0.661 | 2,915 | 1,347 | 16.4 | 1.8 |

**Read the fresh row against the stale row.** The fresh row's median `c_u` is 0.00 and its median `D`
is 1.000: the sitter fade does not reach a player who played this year, by construction. The stale
row's median `c_u` is 2.00 and its median `D` is 0.633.

**The same table on the ORDER K dial line**, so it is clear which of this is ORDER P's doing:

| group | ORDER P charge | ORDER K charge | ORDER P fade | ORDER K fade |
|---|---:|---:|---:|---:|
| FRESH | 32,504 | 26,973 | 4,278 | 4,968 |
| STALE(1) | 3,796 | 2,673 | 2,536 | 2,774 |
| stale(1), TALL | 881 | 874 | 1,189 | 1,256 |
| stale(1), SMALL | 2,915 | 1,799 | 1,347 | 1,518 |

**The fade totals barely move between the two boards** — the sitter machinery is the same object in
both, and the small differences come from the charge multiplying it. **The charge total rises under
ORDER P on both fresh and stale rows, and it rises by the same kind of proportion on each.** ORDER P
did not make the charge any more aware of staleness than ORDER K's blind charge was.

## 13 · IS THE CHARGE READING STALENESS AT ALL? — NO. (prereg SRO-5)

The charge is `exp(-LAMBDA*A(g)*T(s_P))`. `A(g)` reads **career** games. `s_P` is the games-weighted
mean over **played** seasons. **Neither carries a date.**

| career games | n fresh | med f | med A | med s_P | n stale | med f | med A | med s_P |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1-3 | 15 | 0.7541 | 0.1831 | −22.45 | 9 | 0.7261 | 0.0962 | −29.96 |
| 3-10 | 59 | 0.5878 | 0.4548 | −16.82 | 8 | 0.6546 | 0.4258 | −15.97 |
| 10-25 | 97 | 0.5133 | 0.8017 | −9.85 | 10 | 0.4883 | 0.8066 | −23.27 |
| 25-60 | 118 | **0.7444** | 0.9815 | −10.50 | 11 | **0.7444** | 0.9737 | −3.68 |
| 60-150 | 207 | 0.9959 | 0.9999 | −1.00 | 11 | 0.9785 | 0.9998 | −2.83 |
| 150+ | 166 | 1.0000 | 1.0000 | +6.16 | 4 | 1.0000 | 1.0000 | +3.04 |

**At the same career games the stale row and the fresh row pay the same charge**, and where they
differ it is because their surplus differs, not their recency. **Falsifier SRO-5 did not fire.**

**How old is the evidence the charge reads?** The games-weighted mean age, in seasons, of the seasons
entering `s_P`. The charge weights every one of them exactly the same.

| group | n | median evidence age | 90th percentile |
|---|---:|---:|---:|
| FRESH | 662 | **2.03 seasons** | 5.35 |
| STALE(1) | 53 | **2.25 seasons** | 5.23 |
| STALE(2) *thin* | 12 | 3.19 | 4.92 |
| STALE(3) *thin* | 3 | 3.38 | 4.63 |
| stale(1) with 25 career games or fewer | 27 | 1.19 | 2.54 |

**The median board row is charged against evidence two seasons old, at full weight, whether he played
this year or not.** That is a fact about the construction, not a defect this seat is ruling on — the
recency fix is the other seat's S1 and this packet states no fix.

## 14 · (c) THE MATCHED PAIRS

Match rule, written into the prereg before it ran: same class, career games within 3, age within 1,
same pathway. 38 of the 53 stale(1) rows found a match.

**A declared addition, not in the prereg.** The prereg rule does NOT match on entry price, so a stale
row could be paired with a fresh row ten times his price and the retention comparison would then be
about the price, not the staleness. A second, price-matched set was therefore also run: the same rule
plus `|ln(v0 ratio)| ≤ 0.35`. It found 28 pairs. Both are printed and the prereg rule stays primary.

Median difference, stale MINUS fresh:

| quantity | prereg rule (n = 38) | price-matched (n = 28) |
|---|---:|---:|
| charge factor `f` | **−0.0025** | **−0.0006** |
| fade `D_final` | **+0.0000** | **+0.0000** |
| unplayed clock `c_u` | **+0.94** | **+0.92** |
| `rho31(g)` | +0.0000 | −0.0000 |
| `sigma_sel` selection relief | **+0.0000** | **+0.0000** |
| charge attribution, board points | +0.0 | +0.0 |
| fade attribution, board points | **+0.0** | **+0.0** |
| price / entry price, retention | **−0.160** | **−0.314** |

**This is the single most important table in T2 and it says three things.**

1. **The charge does not know.** The median difference in `f` is −0.0025 on the prereg rule and
   −0.0006 price-matched. **A stale row and a fresh row of the same age and games pay the same
   charge.**
2. **The clock does know.** The median stale row carries **0.94 more seasons of unplayed clock** than
   his fresh match. That is the whole of the staleness signal in the price.
3. **But the fade does not act on it at the median.** The median difference in `D_final` is **exactly
   zero**, and so is the median fade attribution. **Because the fade schedule is 1.0 at every depth
   `c_u ≤ 1`, an extra 0.94 seasons of sitting buys nothing at the median row.** The median retention
   still falls by 16 points (31 price-matched), and that comes from `rho`, from the production
   estimate and from the D8 cap — not from the two mechanisms this order named.

The ten largest price-matched pairs:

| STALE row | age | g | v0 | f | D | c_u | board | FRESH match | age | g | v0 | f | D | c_u | board |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| Nicholas Martin | 25 | 83 | 360 | 0.979 | 1.000 | 1.00 | 3,196 | Matt Cottrell | 26 | 84 | 360 | 0.980 | 0.886 | 2.00 | 95 |
| Darcy Jones | 22 | 37 | 538 | 1.000 | 1.000 | 1.00 | 1,095 | Toby McMullin | 22 | 34 | 419 | 0.162 | 1.000 | 1.00 | 42 |
| Thomas Sims | 20 | 11 | 590 | 0.470 | 1.000 | 1.92 | 702 | Harry Armstrong | 20 | 11 | 682 | 0.177 | 1.000 | 1.00 | 454 |
| Cody Angove | 20 | 4 | 843 | 0.538 | 0.597 | 1.92 | 622 | Harrison Oliver | 20 | 5 | 813 | 0.291 | 0.668 | 2.00 | 314 |
| Harry O'Farrell | 20 | 6 | 407 | 1.000 | 0.794 | 2.00 | 591 | Noah Mraz | 20 | 4 | 454 | 1.000 | 0.678 | 2.00 | 2,089 |
| **Harry Barnett** | 22 | 2 | 1,069 | 0.509 | 0.621 | 3.92 | 557 | **Taylor Goad** | 21 | 2 | 1,072 | 0.555 | 0.524 | 3.00 | 590 |
| Joshua Kelly | 31 | 230 | 2,869 | 1.000 | 1.000 | 1.00 | 427 | Christian Petracca | 30 | 231 | 2,869 | 1.000 | 1.000 | 0.00 | 1,977 |
| Clay Hall | 21 | 16 | 629 | 0.649 | 1.000 | 0.92 | 391 | Hugh Boxshall | 20 | 19 | 500 | 0.674 | 1.000 | 0.00 | 674 |

**Read the Barnett / Goad pair.** Two rucks, two games each, entry prices 1,069 and 1,072 — within a
third of a per cent. Barnett has sat a season longer (`c_u` 3.92 against 3.00). His charge factor is
0.509 against Goad's 0.555, and that gap is about their SURPLUS, not their recency. His fade is 0.621
against 0.524 — **the row who has sat LONGER carries the LIGHTER fade**, because Goad is at a
different pick and carries a different `kappa`. **The extra year of sitting is worth 557 against 590,
33 board points, and the sign of the difference is set by the pick exponent rather than by the
sitting.** That is the handoff working as built, and it is not obviously what anyone intended.

**Read the Nicholas Martin row.** 83 career games, no games this year, `c_u` 1.00, `D` 1.000, `f`
0.979. **Nothing in either mechanism prices his missing season, and he is the second most expensive
stale row on the board at 3,196.**

## 15 · (d) THE TALL/SMALL INTERACTION — THE EVIDENCE WEIGHT WINS, EVERYWHERE

Both columns are **board points KEPT ON the row**.

| group | n | med g | med A | EVIDENCE WEIGHT kept | TALL FACTOR kept | which is bigger |
|---|---:|---:|---:|---:|---:|---|
| stale(1) TALL, g ≤ 5 | 5 | 1.0 | 0.096 | **+119.2** | +38.5 | **EVIDENCE, 3.1×** |
| stale(1) TALL, g 6-20 | 5 | 6.0 | 0.455 | +34.8 | +31.5 | EVIDENCE, 1.1× |
| stale(1) TALL, all | 17 | 7.0 | 0.507 | +34.8 | +12.6 | EVIDENCE, 2.8× |
| stale(1) SMALL, g ≤ 5 | 8 | 2.0 | 0.179 | +55.0 | **−9.7** | EVIDENCE |
| stale(1) SMALL, all | 36 | 30.5 | 0.954 | +3.9 | 0.0 | EVIDENCE |

**Falsifier SRO-8 did not fire: the evidence weight is the larger of the two on the median row in
every cell.**

The two rows the order used to illustrate the shape, printed wherever the mechanism puts them:

| | Harry Barnett | Toby Conway |
|---|---:|---:|
| position, age, games | RUCK, 22, 2 | RUCK, 23, 6 |
| `s_P` | **−44.7** | **+2.4** |
| charge factor `f` | 0.509 | **1.000** |
| fade `D_final` | 0.621 | 0.630 |
| the charge REMOVED | 279.0 | **0.0** |
| the sitter fade REMOVED | 164.2 | **240.6** |
| the evidence weight A(g) KEPT | **275.5** | 0.0 |
| the tall/small factor KEPT | 83.1 | 126.3 |
| board price | **557** | **1,066** |

**Barnett, in plain words.** He is 44.7 points a game below the bar a player at his price is measured
against, which at full evidence would take almost his whole pedigree leg. He has two games, so
`A(2) = 0.183`, and only 18.3% of that verdict can reach him: he pays 49.1% instead. **The evidence
weight keeps 275.5 board points on him; the owner-ruled tall sitter factor keeps 83.1. The evidence
weight is 3.3 times the tall factor on this row.** The order's question — how much of what Barnett
keeps is the evidence weight and how much is the gentler tall fade — has the answer **roughly
three-quarters evidence weight, one-quarter tall factor.**

**Conway is the mirror image and he is why the handoff matters.** Six games, produced ABOVE his bar
(`s_P` +2.4), so **he pays nothing at all on the charge.** He has sat 4.50 seasons of unplayed clock,
and the ONLY thing pricing that is the fade: 240.6 board points. **His entire staleness bill is paid
by one mechanism and the other is silent by construction, because his played games went well.**

The negative number for SMALL rows at 5 games or fewer (−9.7) is ORDER I's own disclosed side effect:
the redistribution identity is pinned, so late small sitters pay for the talls' relief.

## 16 · THE CHANNELS OUTSIDE THE FOUR NAMED LEGS (prereg SRO-9)

Reading `ev()` finds three further objects that react to a season not played. They are not the charge
and not the fade, and they sit on the PRODUCTION leg or on the whole row.

- **A. The D8 graded staleness cap.** `el ≥ onset and ns ≤ 1` caps the production leg at
  `v0_start * frac`, with a graded release. `onset` is 4 for KPD/KPF/RUCK and 3 otherwise.
- **B. The mediocre-for-years decay gate.** `el ≥ onset+2 and bestlvl/par < 0.55` caps it at
  `v0_start * frac`. A hard min, no grading.
- **C. The ITEM H sitter cuts.** A POOL row with no games this year takes `H_POOLSIT`, and the named
  union subset takes `H_UNION` on top. **This one reads "did not play this year" directly.**

| channel | rows on the ORDER P board |
|---|---:|
| A · D8 predicate TRUE | 32 |
| B · mediocre-for-years predicate TRUE | **0** |
| C · ITEM H sitter cut below 1.0 | **0** (ITEM H is live; no board row is in a cut cell) |
| the `ns == 0` sit-out arm, a different price path entirely | 160 |
| A/B/C predicate TRUE **and** the sitter fade below 1 | 18 |

**A predicate being true is not the same as a cap binding.** The counterfactual settles it. Wrapping
the engine's own `_staleness_grade` to return 1.0 makes the D8 arm `min(e, e) = e` identically, so it
removes that arm and nothing else.

| | ORDER P | ORDER K |
|---|---:|---:|
| rows the D8 arm actually moves | **15** | 16 |
| board points it removes in total | **808** | 811 |
| worst single row | **367** | 368 |

The five it costs most on the ORDER P board:

| row | pick | age | games | c_u | fade D | board | without the D8 arm | it costs him |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Clay Hall | 38 | 21 | 16 | 0.92 | 1.000 | 391 | 758 | **367** |
| Billy Dowling | 43 | 22 | 13 | 2.50 | 0.310 | 162 | 387 | **225** |
| Will Lorenz | 57 | 21 | 11 | 1.00 | 1.000 | 272 | 350 | 78 |
| Riley Hardeman | 23 | 21 | 25 | 1.00 | 1.000 | 183 | 234 | 51 |
| Ashton Moir | 29 | 21 | 13 | 1.00 | 1.000 | 219 | 251 | 32 |

**PRICED TWICE: 8 of those 15 rows also carry a sitter fade below 1.** Both legs are reduced by the
same fact — a season not played — and the two legs are added together in the price identity. That is
the definition fixed in the prereg.

| row | games | c_u | fade D (removes) | D8 cap (removes) | board |
|---|---:|---:|---|---|---:|
| Liam McMahon | 7 | 5.92 | 0.796 (35.6 bp) | 3 bp | 213 |
| **Billy Dowling** | 13 | 2.50 | **0.310 (107.1 bp)** | **225 bp** | 162 |
| Tom Hanily | 12 | 2.00 | 0.702 (10.3 bp) | 3 bp | 131 |
| Isaac Keeler | 13 | 3.00 | 0.761 (10.5 bp) | 10 bp | 128 |
| Will McLachlan | 7 | 2.46 | 0.518 (11.5 bp) | 6 bp | 114 |
| Shadeau Brain | 11 | 3.00 | 0.426 (66.7 bp) | 5 bp | 99 |
| Kaleb Smith | 12 | 2.92 | 0.325 (8.7 bp) | 6 bp | 37 |
| Harvey Gallagher | 28 | 2.00 | 0.496 (10.9 bp) | 1 bp | 21 |

**Billy Dowling is the one that matters.** His production leg is capped for not playing (225 board
points) AND his pedigree leg is faded to 0.310 for not playing (107 board points). **332 board points
on one 162-point row, charged twice for one fact.** On the other seven the D8 side is 1 to 10 points
and the double-pricing is real but small.

## 17 · WHERE STALENESS GOES UNPRICED

### 17.1 The fade is 1.000 on 19 of 53 stale rows (prereg SRO-6, did not fire)

The fade schedule is 1.0 at every unplayed depth `c_u ≤ 1`, and `c_u` is the clock MINUS the time
actually played. A row who played last season and nothing this one sits below depth 1 and carries no
fade at all — **while the charge is silent on the unplayed season, because `s_P` reads played seasons
only. For that row the missing season costs nothing anywhere in the price.**

| row | age | games | c_u | clock | played units | board |
|---|---:|---:|---:|---:|---:|---:|
| **Tom Green** | 25 | 115 | 1.00 | 8.00 | 6.00 | **4,339** |
| **Nicholas Martin** | 25 | 83 | 1.00 | 6.00 | 4.00 | **3,196** |
| Darcy Jones | 22 | 37 | 1.00 | 5.00 | 2.00 | 1,095 |
| Thomas Sims | 20 | 11 | 1.92 | 2.92 | 1.00 | 702 |
| Sid Draper | 20 | 10 | 1.92 | 2.92 | 1.00 | 623 |
| Joshua Kelly | 31 | 230 | 1.00 | 14.00 | 12.00 | 427 |
| Clay Hall | 21 | 16 | 0.92 | 3.92 | 2.00 | 391 |
| Josh Draper | 22 | 31 | 0.92 | 4.92 | 2.00 | 264 |
| Jack Viney | 32 | 237 | 1.00 | 15.00 | 13.00 | 254 |
| Tyson Stengle | 28 | 109 | 0.92 | 10.92 | 7.00 | 181 |

**The two most expensive stale rows on the whole board are in this table.** Tom Green at 4,339 and
Nicholas Martin at 3,196 have not played a game in 2026 and neither mechanism has moved either price by more
than 3.4 board points — Green pays 0.3 on the charge and 0.0 on the fade, Martin 3.4 and 0.0.

**On 10 of the 53 stale rows NEITHER the charge NOR the fade moves the price by as much as one board
point:** Tom Green, Darcy Jones, Joshua Kelly, Jack Viney, Sam Powell-Pepper, Josh Draper, Tyson
Stengle, Bobby Hill, Lachlan Sholl, Bailey Banfield.

### 17.2 A two-game season cancels a full season of sitter clock (prereg SRO-7, did not fire)

`o31_played_units` credits `min(1, games/2)` per season. **A two-game season buys the same full unit
of clock credit that a twenty-two-game season buys.** A one-game season buys 0.50.

- **217 board rows** have at least one season of 1-2 games.
- **120 of them** have that season inside the last four, where the credit is still holding the sitter
  clock down.
- **15 of those are stale(1).**

| row | token games | year | clock | played units | c_u | D | board |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ryan Gardner | 1.0 | 2026 | 11.92 | 5.96 | 5.96 | 0.429 | 34 |
| Tom Doedee | 1.0 | 2025 | 11.92 | 6.00 | 2.42 | 0.490 | 233 |
| Henry Smith | 2.0 | 2025 | 6.92 | 2.00 | 4.92 | 0.460 | 93 |
| Lewis Hayes | 1.0 | 2025 | 5.00 | 0.50 | 4.50 | 0.630 | 338 |
| **Toby Conway** | 1.0 | 2023 | 6.00 | 1.50 | 4.50 | 0.630 | 1,066 |
| Mitchell Hinge | 1.0 | 2026 | 10.92 | 6.46 | 0.46 | 1.000 | 305 |

Read the units column against the clock. **Two games and a full season are the same object to the
sitter fade.**

### 17.3 The age-24 gate closes the charge on 11 stale rows

The stale(1) rows aged 27 and over — 11 of them, median 109 career games — carry median `c_u` 1.00,
median `D` 1.000 and a median charge of 0.2 board points. **For a mature stale row both mechanisms
are silent: the age gate hands the charge back at 24 and the depth-1 floor holds the fade at 1.0.**
The gate is ORDER P's own design and ORDER Q priced its repair; nothing here re-opens that.

## 18 · (e) THE VERDICT, IN PLAIN WORDS, WITH POPULATION SIZES

**Non-selection is priced ONCE on most stale rows, by the sitter fade, and NOT AT ALL by the charge.
It goes entirely unpriced on a third of them, and it is priced TWICE on eight board rows.**

| how the row is treated | mechanism | rows |
|---|---|---:|
| **priced once** — the fade bites, nothing else does | `D(c_u)` inside `pi` | **32 of 53 stale(1)** |
| **priced twice** — the production leg is capped AND the pedigree leg faded | D8 cap + `D(c_u)` | **8 board rows**, of which **2 are stale(1)** (Liam McMahon, Kaleb Smith) |
| **not priced at all** — no fade, and the charge is structurally silent | neither | **19 of 53 stale(1)**, of which **10** move under one board point |
| **structurally unreachable** — no games at all, `A(0) = 0` | none | 89 board rows |

**And the treatment is INCOHERENT in three specific ways. This seat names them and stops.**

1. **The charge weights three-year-old evidence exactly as heavily as this season's.** `A(g)` reads
   career games and `s_P` reads played seasons with no date. The median board row is charged against
   evidence 2.03 seasons old at full weight. **Falsifier SRO-10's prediction is confirmed. The fix is
   the other seat's S1 and this packet proposes nothing.**
2. **The fade's floor and the charge's silence overlap exactly.** A row one season out sits at
   `c_u ≤ 1` where the schedule is 1.0, and the charge cannot see the unplayed season at all. **The
   first season of non-selection is free in both mechanisms simultaneously.** 19 of 53 stale rows are
   in that state and they include the two most expensive stale rows on the board.
3. **The clock credit is a step, not a rate.** Two games buy a whole season of clock. So a row who
   plays two games a year forever never accrues sitter fade at all, while a row who plays none accrues
   it in full. **Non-selection is priced as a binary at a threshold of two games**, and the charge —
   which could carry the gradation, since it reads production per game — does not, because a two-game
   season enters `s_P` at a games weight of two and vanishes into the mean.

**What their fix has to be checked against.** Any recency change to `s_P` acts on mechanism 1 only. It
does NOT reach the 19 rows in the second failure mode, because those rows have no unplayed season in
`s_P` to reweight — the season is absent, not stale. **A recency weighting makes the charge read
recent evidence more heavily; it does not make the charge read the ABSENCE of evidence at all.** Any
claim that a recency fix prices non-selection should be tested against those 19 rows and against the
10 that move under one board point.

## 19 · T2's LIMITATIONS, ALL OF THEM

- **One as-of year.** Everything is measured at `Y = 2026`. Nothing here is a longitudinal claim, and
  the in-progress-season fraction (0.58) sits inside every clock figure.
- **The stale(2) and stale(3) cells hold 12 and 3 rows.** Every number computed on them is thin and
  is marked thin. The stale(1) cell holds 53.
- **The matched pairs are 38 and 28.** Medians over 28 pairs are not precise; no interval was computed
  on them, and none should be read into them.
- **The mediocre-for-years arm (B) was not counterfactually priced.** Its predicate is FALSE on every
  board row at this as-of year, so there was nothing to price; but the read-only counterfactual for
  that arm would have needed `bestlvl` wrapped, and `bestlvl` also feeds the RUCK production ceiling,
  so it was not attempted. **If that arm ever binds, this packet has not measured its size.**
- **ITEM H reaches no board row at this as-of year.** `H_ON` is live and the cut cells are simply
  empty. That is a fact about this board, not about the mechanism.
- **The 160 rows on the `ns == 0` sit-out arm take a different price path** (`sitout_ev` /
  `_pv_apply` at `ns == 0`) which this packet enumerates but does not decompose leg by leg. They are
  rows with evidence who have not yet banked a six-game season.
- **The board attribution is a counterfactual on one object at a time**, not a decomposition into
  orthogonal parts. The legs interact — the charge multiplies the faded `pi_base` — so the individual
  attributions do not sum to the whole gap against an uncharged, unfaded price. That is stated rather
  than hidden.
- **The tall/small counterfactual is against ORDER D's POOLED exponent**, which is what
  `RL_O36_TALL=0` falls back to. It is not against "no fade at all".
- **No delisted or retired row is in the population**, and rows without a birth year or without a
  day-0 `v0` object fall out of the charge by the engine's own fallback.

---

## 20 · THE FALSIFIER SCORECARD

| # | falsifier | fired? |
|---|---|---|
| **SRO-P1** | the population is not the one PG was fitted on | **no** — 5,041 / 1,575 / 58,488 asserted equal |
| **SRO-P2** | the replicated fit is not `op_lib.Premium` / the built surface | **no** — under 1e-12 and 1e-9 |
| **SRO-1** | the class-level mean residual exceeds 0.5 points a game | **no** — TALL −0.104, SMALL +0.086 |
| **SRO-2** | all six position intervals contain zero (a NULL) | **no — three exclude zero.** The DIRECTION half of the prediction is **FALSIFIED**: MID is a null, not positive, and SF is positive, not negative |
| **SRO-3** | the tail offsets are no larger than the cheap-end offsets | **FIRED.** They are SMALLER, and every tail interval covers zero |
| **SRO-4** | RUCK's interval is narrower than the median position's | **no** — it is the widest of the six. But the "not rulable" half is **FALSIFIED**: RUCK's level interval excludes zero where ORDER R's slope interval was degenerate |
| **SRO-B1** | the recomputed charge factor is not the engine's own | **no** — under 1e-9 on every row checked |
| **SRO-T1** | the price identity does not reassemble | **no** — worst 9.09e-13 on 804 of 804 |
| **SRO-T2** | the recomputed fade chain is not `o31_D` | **no** — worst error exactly 0 |
| **SRO-5** | the charge factor differs systematically between matched stale and fresh rows | **no** — median difference −0.0025, and −0.0006 price-matched |
| **SRO-6** | every stale row carries `D_final < 1` | **no** — 19 of 53 carry `D_final = 1.000` |
| **SRO-7** | no board row's played-unit credit exceeds its share of a season | **no** — 217 rows have a 1-2 game season, 120 of them inside the last four |
| **SRO-8** | the tall factor beats the evidence weight on the median stale tall row | **no** — the evidence weight is larger in every cell, 3.3× on Barnett |
| **SRO-9** | no row has a production-leg staleness cap AND a sitter fade below 1 | **no** — 8 rows do |
| **SRO-10** | the combined treatment is coherent | the prediction of incoherence is **confirmed** — three named ways, §18 |

**Prereg deviations, declared.** Nothing was removed. Three additions: the board-points translation of
the T1 offsets (`os_bind.py`, §7), which the prereg promised only as a formula; the price-matched pair
set in §14, declared in the output before its numbers were read and printed alongside the prereg rule
rather than instead of it; and the ORDER K comparison column in §12, which the prereg did not name.

---

## 21 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_SRO.md` | the prereg, pushed at `09d5e3f` before any number existed |
| `os_level.py` · `LEVEL_SRO.json` · `LEVEL_SRO_out.txt` | T1 — the level test, the bootstrap, the age profile, the same-pick table |
| `os_bind.py` · `BIND_SRO.json` · `BIND_SRO_out.txt` | T1b — what the offsets are worth in board points |
| `os_lib.py` | the wide recorder and the leg attributions. ORDER Q's `oq_lib.load` is imported and used unchanged |
| `os_handoff.py` · `HANDOFF_P.json` · `HANDOFF_P_out.txt` | T2 on the ORDER P dial line |
| `HANDOFF_K.json` · `HANDOFF_K_out.txt` | T2 on the ORDER K dial line, the comparison column |
| `os_level_run.txt` · `os_bind_run.txt` · `os_handoff_run.txt` · `os_handoff_K_run.txt` | the raw console of every run, engine banners included |

**Nothing in this directory is adopted, nothing lands, and neither task recommends a fix.**
