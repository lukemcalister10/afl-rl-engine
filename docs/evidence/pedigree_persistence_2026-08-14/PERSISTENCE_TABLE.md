# PERSISTENCE TABLE — ORDER 30B-M

Machine-readable twin: `PERSISTENCE_TABLE.json` (every cell, including the ones too thin to print).
Harness: `o30bm_measure.py` · derivation: `o30bm_derive.py` · prereg: `PREREG_30BM.md`.
**READ-ONLY. NOTHING WIRES.**

## 0 · Population, window, censoring

| | |
|---|---|
| population | ND effective_pick 1-64, entry_year>=2005, state year <= 2019 (H=6 fully observed) |
| panel | **4033 states** over **767 careers**; state years 2006–2019, entry years 2005–2018 |
| left censoring | entry years 2003-2004 excluded: store season rows begin 2005 |
| right censoring | 2026 in progress: contributes no future value, supplies no fitting state |
| survivorship | zeros stay in; a season with no row contributes 0 |
| scorer | 26B Layer 2 pricing core (Ruling 1 bars, Ruling 3 season callable, sqrt games weight, no era normalisation), discount re-anchored at the state year |
| bars (engine-read, Ruling 1 asserted) | KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9 |
| discount | flat 14%/yr, re-anchored at the state year |
| horizon | H = 6 observed seasons (H=4 / H=10 as declared sensitivities) |
| force majeure | paddy-mccartin, thomas-boyd (excluded entirely; the pick slide is carried in `effective_pick`) |
| pool band | 1706 states, descriptive only — never fitted (no v0 ladder position) |
| pins | layer1 `ad1229ea` · v0 artifact `dc324ad9` · board `36d5dfc7` · store `cb38ef11` · rl_model `14000af2` |

## 1 · The shape of the target — remaining 6-season delivered value, by games-so-far

| games so far | n | mean | p25 | median | p75 | zero share |
|---|---:|---:|---:|---:|---:|---:|
| 0-5 | 382 | 254.1 | 0.0 | 14.9 | 311.9 | 15.4% |
| 6-15 | 591 | 398.4 | 0.3 | 51.3 | 559.9 | 10.2% |
| 16-35 | 834 | 571.2 | 2.2 | 161.6 | 827.1 | 10.3% |
| 36-70 | 887 | 857.0 | 26.7 | 349.5 | 1284.5 | 6.2% |
| 71+ | 1339 | 1018.2 | 39.4 | 593.1 | 1644.5 | 6.3% |

Delivered value is star-dominated at every depth — the median is a fraction of the mean throughout.
Every table below reports n and dispersion for this reason; no bare mean stands alone.

## 2 · The entry anchor — the pick spread with NO output information

| pick band | n | mean R6 | p25 | median | p75 | zero share | mean v0 | **R6 / v0** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A 1-6 | 88 | 883.0 | 171.8 | 663.6 | 1374.5 | 0.0% | 2291.8 | **0.3853** |
| B 7-12 | 90 | 568.9 | 57.6 | 321.4 | 763.4 | 1.1% | 1324.6 | **0.4295** |
| C 13-20 | 120 | 394.8 | 6.4 | 154.6 | 537.2 | 0.8% | 895.3 | **0.4410** |
| D 21-40 | 300 | 255.0 | 0.4 | 18.3 | 255.6 | 7.3% | 605.1 | **0.4214** |
| E 41-64 | 355 | 112.5 | 0.0 | 1.0 | 81.0 | 20.8% | 280.8 | **0.4005** |

**The Step-1 v0 ladder survives its own outcome check.** Realized six-season delivered value is a
near-constant fraction of v0 across all five pick bands (0.3853–0.4410, max/min 1.145). The ladder's
PICK SHAPE is confirmed by outcomes; what the rest of this table measures is how long that shape
keeps mattering once games arrive.

## 3 · Q1 — THE PERSISTENCE CURVE

Within each games band: `R6 ~ position dummies + age + age² + output + output² + current production
+ 3-season production + games this season + log1p(games so far) + v0`. `σ` is the pedigree share —
`β_v0 · mean(v0) / mean(R6)` — the fraction of expected remaining value carried by the pick term
after production, age and position have taken everything they can. Standard errors are
cluster-robust on player; the CI is a 300-replicate player-cluster bootstrap.

| games so far | n | clusters | β_v0 | cluster t | **σ (pedigree share)** | σ 90% CI | ruled blend `1−w` at midpoint | old anchor carry |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0-5 | 382 | 332 | 0.29683 | 3.76 | **70.1%** | 42.9% … 99.6% | 78.9% | ~40% |
| 6-15 | 591 | 467 | 0.36226 | 5.95 | **66.4%** | 47.7% … 83.0% | 40.4% | ~40% |
| 16-35 | 834 | 571 | 0.22330 | 4.25 | **33.1%** | 20.8% … 45.6% | 12.4% | ~40% |
| 36-70 | 887 | 436 | 0.15315 | 2.39 | **16.5%** | 5.9% … 28.0% | 1.6% | ~40% |
| 71+ | 1339 | 297 | 0.02007 | 0.49 | **2.2%** | -4.6% … 10.5% | 0.2% | ~40% |

**At `g = 36` exactly** (isaac-kako's games count), log-linear interpolation between the measured
band midpoints 25.5 and 53.0 — *an interpolation, labelled as one*:

| | pedigree share at 36 games |
|---|---:|
| **MEASURED (this order)** | **23.8%** |
| the ruled blend, `1 − w(36)` | 5.62% |
| the old machinery's anchor carry | ~40% |

### 3.1 · The same claim without a model — matched contrasts

Stratum = position × age band × output band; a cell needs n ≥ 8 to be used; the preregistered
collapse ladder is quintile → tercile → stratum dropped, and both rungs are printed.

| games so far | quintile lens: strata | Δ (top − bottom pick band) | tercile lens: strata | Δ | weight |
|---|---:|---:|---:|---:|---:|
| 0-5 | 2 | 159.5 | 2 | 159.5 | 23 |
| 6-15 | 1 | 90.5 | 2 | 848.7 | 19 |
| 16-35 | 0 | — | 7 | 272.6 | 63 |
| 36-70 | 3 | -4.2 | 8 | 127.1 | 79 |
| 71+ | 13 | 239.6 | 17 | 200.6 | 212 |

The quintile lens leaves **0 usable strata at 16–35 games** — that is the thin-cell case the
preregistered ladder exists for, and it is disclosed rather than quietly collapsed. Cells collapsed
out: 486 on the quintile lens, 311 on the tercile lens.

**Residual contrast** — the same claim with the whole panel behind it. The pick-blind production
model is fitted within each games band; the mean residual by pick class is the pick information the
production features could not carry. 90% CI is a player-cluster bootstrap.

| games so far | n picks 1–12 | mean residual | n picks 21–64 | mean residual | gap | gap 90% CI |
|---|---:|---:|---:|---:|---:|---:|
| 0-5 | 37 | 133.0 | 293 | -28.2 | **161.2** | 30.2 … 313.9 |
| 6-15 | 109 | 129.3 | 404 | -57.2 | **186.5** | 54.9 … 324.1 |
| 16-35 | 196 | 44.9 | 499 | -22.9 | **67.8** | -51.8 … 199.0 |
| 36-70 | 238 | 52.0 | 498 | -16.1 | **68.1** | -80.7 … 237.4 |
| 71+ | 479 | 27.7 | 629 | -0.8 | **28.5** | -90.9 … 146.1 |

The gap is positive at every depth and its sign never turns; the confidence interval crosses zero
from 16–35 games onward, which is the honest statement of the power available at these n.

### 3.2 · The pool band (never fitted, carried for the record)

| games so far | n pool | mean R6 pool | n band A | mean R6 A | n band E | mean R6 E |
|---|---:|---:|---:|---:|---:|---:|
| 0-5 | 279 | 142.3 | 12 | 272.1 | 145 | 212.9 |
| 6-15 | 305 | 235.8 | 43 | 1084.3 | 206 | 253.4 |
| 16-35 | 368 | 362.3 | 95 | 1086.3 | 230 | 329.2 |
| 36-70 | 323 | 589.6 | 128 | 1457.2 | 219 | 558.6 |
| 71+ | 431 | 599.0 | 263 | 1311.0 | 253 | 710.9 |

## 4 · Q2 — THE FORM

Same target, same panel, same folds. `P` = production only · `L` = `P` + `v0` + `v0·log1p(g)` (the
blend's shape, generalised) · `T` = `L` + pick-class × development-axis interactions (the owner's
hypothesis: the growth curve itself is pick-conditional). Criterion and decision rule preregistered:
**≥ 2.0% held-out RMS reduction AND ≥ 4 of 5 folds**, folds grouped by player, no RNG.

| form | parameters | held-out RMS | held-out MAE | held-out Spearman |
|---|---:|---:|---:|---:|
| P | 16 | **715.76** | 478.29 | 0.7166 |
| L | 18 | **709.42** | 471.74 | 0.7277 |
| T | 30 | **709.53** | 473.27 | 0.7175 |

| comparison | RMS reduction | folds won | bar | adopted? |
|---|---:|---:|---:|---|
| P → L | 0.89% | 5 / 5 | 2.0% + 4/5 | **NO** |
| L → T | -0.02% | 2 / 5 | 2.0% + 4/5 | **NO** |

**Q2 VERDICT, by the preregistered rule: PRODUCTION-ONLY.**

Time-block hold-out (fit on state years ≤ 2012, test on ≥ 2013 — 1,219 train / 2,814 test):

| form | RMS | MAE | Spearman |
|---|---:|---:|---:|
| P | 725.33 | 489.49 | 0.7159 |
| L | 718.92 | 477.41 | 0.7321 |
| T | 724.94 | 486.54 | 0.7213 |

### 4.1 · The pick terms themselves (full panel, cluster-robust on player)

| term | β | cluster SE | t |
|---|---:|---:|---:|
| `v0` | 0.490757 | 0.100950 | **4.86** |
| `v0_lg` | -0.090950 | 0.023405 | **-3.89** |

The level form's two pick terms are individually strong (t = 4.86 and t = -3.89) and say exactly what
the persistence curve says: a positive pick effect that decays in log games. What they do NOT do is
move held-out squared error by 2% — because squared error in this target is dominated by which
handful of players become stars, and the pedigree term moves the whole distribution modestly rather
than calling the tail. Both facts are the measurement.

Form `T`'s interaction terms (reference class = picks 13–30):

| term | β | cluster SE | t |
|---|---:|---:|---:|
| `age2_x_hi` | 7.6581 | 4.8180 | 1.59 |
| `age2_x_lo` | -5.7224 | 3.2195 | -1.78 |
| `age_x_hi` | -425.5147 | 243.5826 | -1.75 |
| `age_x_lo` | 309.5984 | 162.2505 | 1.91 |
| `cur_x_hi` | 0.6925 | 0.2232 | 3.10 |
| `cur_x_lo` | 1.0261 | 0.2573 | 3.99 |
| `d_hi` | 4795.8873 | 2833.5982 | 1.69 |
| `d_lo` | -3298.7929 | 1903.0341 | -1.73 |
| `lg_x_hi` | 360.4586 | 93.5786 | 3.85 |
| `lg_x_lo` | -59.2397 | 63.7512 | -0.93 |
| `o_x_hi` | -11.0277 | 4.7565 | -2.32 |
| `o_x_lo` | -9.6762 | 3.5018 | -2.76 |

### 4.2 · Where each form is right and wrong (held-out RMS by cell; same predictions, sliced)

**by games band**

| cell | n | RMS P | RMS L | RMS T | best |
|---|---:|---:|---:|---:|---|
| 0-5 | 382 | 526.7 | 512.9 | 514.7 | L |
| 16-35 | 834 | 730.7 | 720.4 | 720.8 | L |
| 36-70 | 887 | 797.1 | 791.9 | 791.3 | T |
| 6-15 | 591 | 620.9 | 595.8 | 594.2 | T |
| 71+ | 1339 | 735.1 | 738.6 | 739.3 | P |

**by pick class**

| cell | n | RMS P | RMS L | RMS T | best |
|---|---:|---:|---:|---:|---|
| hi | 1059 | 848.0 | 844.5 | 848.6 | L |
| lo | 1646 | 632.2 | 622.2 | 619.8 | T |
| mid | 1328 | 697.9 | 692.8 | 691.7 | T |

**by young thin**

| cell | n | RMS P | RMS L | RMS T | best |
|---|---:|---:|---:|---:|---|
| g<=40 & age<=21 | 1437 | 708.6 | 689.6 | 691.1 | L |
| other | 2596 | 719.7 | 720.2 | 719.5 | T |

## 5 · Q3 — POSITION CLOCKS

| model | parameters | held-out RMS | MAE | Spearman |
|---|---:|---:|---:|---:|
| P1 | 16 | 715.76 | 478.29 | 0.7166 |
| P6 | 66 | 719.68 | 479.47 | 0.7110 |

P1 → P6: -0.55% RMS reduction, 0/5 folds. **Q3 VERDICT, by the same rule: ONE TABLE.**

**The preregistered peak-age lens carries NO SIGNAL, and the prereg is breached on it.** NO SIGNAL -- degenerate: remaining value falls with age at a fixed state for horizon reasons, so the fitted age part has no interior peak and pins to the 18 boundary in every group. P7 is breached on this lens and the breach is owned.

**Supplementary (post-hoc, descriptive, does NOT re-decide Q3):** the raw development clock —
median change in season average from one season to the next, players with ≥ 5 games in both.

| position | age 18 | age 19 | age 20 | age 21 | age 22 | age 23 | age 24 | age 25 | age 26 | age 27 | age 28 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **KPD** | · | +4.0 | +1.4 | +3.2 | -1.5 | +1.3 | +3.1 | -1.5 | +1.9 | -4.2 | -1.5 |
| **KPF** | · | +8.1 | +2.9 | +3.1 | +0.8 | +2.5 | +0.7 | +0.4 | +1.1 | -3.3 | +2.4 |
| **MID** | +7.3 | +8.1 | +5.5 | +3.8 | +1.7 | +1.7 | -2.0 | +1.1 | -2.6 | +0.4 | -3.9 |
| **RUCK** | · | · | +9.4 | +4.9 | +5.5 | +4.6 | -2.2 | -5.1 | -2.4 | +3.7 | -3.4 |
| **SD** | · | +5.4 | +3.6 | +3.2 | +1.8 | +2.5 | +1.1 | +1.1 | -2.6 | -1.1 | -3.6 |
| **SF** | · | +8.1 | +3.0 | +4.3 | -0.6 | +0.8 | +0.7 | -0.1 | -1.9 | -1.4 | -4.0 |
| *n (all groups)* | 9 | 373 | 564 | 669 | 688 | 652 | 598 | 536 | 462 | 391 | 335 |

Last age with a positive median growth step: **KPD** 26 · **KPF** 28 · **MID** 27 · **RUCK** 27 · **SD** 25 · **SF** 24.
Tall mean 27.00 vs small/mid mean 25.33 — a gap of **1.67 years**.

## 6 · Named rows

| player | pick | pos | games | age | output | board price | v0 | pred P | pred L | pred T |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `isaac-kako` | 13 | SF | 36 | 20 | 50.7 | 1320 | 759.8 | 483.0 | 449.0 | 481.2 |
| `willem-duursma` | 1 | MID | 19 | 19 | 77.0 | 4223 | 3879.3 | 1475.7 | 2010.5 | 2171.1 |
| `dyson-sharp` | 13 | SF | 13 | 19 | 68.2 | 3269 | 1551.0 | 1102.0 | 1251.0 | 1442.4 |
| `jacob-farrow` | 10 | SD | 18 | 19 | 71.7 | 2765 | 1284.5 | 1072.6 | 1115.2 | 1060.9 |

*Prediction states are 2026 — in progress. `cur` for these rows is a part-season at full-season
weight (≥10 games caps the weight at 1), which is disclosed, not corrected.*

## 7 · Historical validation cohorts

Selection rule, fixed in the prereg: **a state at 30–40 games whose output is below the median of
its own position group.** The names fall out of the rule.

**picks 1 10** — n 26 · mean R6 691.5 · p25 3.4 · median 102.4 · p75 1155.5 · zero 12%

| player | pick | pos | year | age | games | output | **realized R6** | career games |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `andrew-brayshaw` | 2 | MID | 2019 | 20 | 39 | 66.1 | **3751.8** | 191 |
| `nicholas-naitanui` | 2 | RUCK | 2010 | 20 | 32 | 66.9 | **3040.0** | 213 |
| `dion-prestia` | 9 | MID | 2012 | 20 | 31 | 69.0 | **2086.7** | 253 |
| `ben-mcevoy` | 9 | RUCK | 2010 | 21 | 31 | 53.0 | **1954.3** | 252 |
| `travis-boak` | 6 | MID | 2008 | 20 | 31 | 72.5 | **1832.5** | 387 |
| `paddy-ryder` | 7 | KPD | 2007 | 19 | 30 | 57.3 | **1672.1** | 277 |
| `ben-cunnington` | 5 | MID | 2011 | 20 | 34 | 53.2 | **1302.5** | 238 |
| `tom-scully` | 1 | MID | 2011 | 20 | 31 | 73.3 | **714.4** | 182 |
| `luke-mcdonald` | 8 | SD | 2015 | 20 | 37 | 61.0 | **495.5** | 235 |
| `will-hoskin-elliott` | 6 | MID | 2014 | 21 | 39 | 61.5 | **297.9** | 242 |
| `lachlan-plowman` | 4 | KPD | 2016 | 22 | 39 | 57.5 | **260.9** | 145 |
| `rhys-palmer` | 7 | MID | 2010 | 21 | 38 | 71.1 | **207.7** | 123 |
| `cale-morton` | 4 | MID | 2009 | 20 | 40 | 73.1 | **105.5** | 76 |
| `callum-ah-chee` | 8 | SF | 2017 | 20 | 30 | 56.7 | **99.4** | 175 |
| `bradley-sheppard` | 7 | SD | 2012 | 21 | 32 | 55.9 | **71.5** | 216 |
| `james-aish` | 7 | MID | 2015 | 19 | 32 | 64.4 | **35.8** | 186 |
| `jake-melksham` | 10 | MID | 2011 | 20 | 37 | 60.0 | **30.5** | 254 |
| `sam-weideman` | 9 | KPF | 2019 | 22 | 31 | 58.0 | **9.2** | 76 |
| `josh-schache` | 2 | KPF | 2018 | 21 | 40 | 48.1 | **8.8** | 76 |
| `lochie-o-brien` | 10 | MID | 2019 | 20 | 35 | 46.1 | **1.5** | 66 |
| `paddy-dow` | 3 | SF | 2019 | 20 | 39 | 57.1 | **0.6** | 83 |
| `matthew-buntine` | 7 | SD | 2016 | 23 | 39 | 56.5 | **0.1** | 67 |
| `jimmy-toumpas` | 6 | MID | 2016 | 22 | 35 | 57.7 | **0.0** | 37 |
| `jimmy-toumpas` | 6 | MID | 2017 | 23 | 37 | 60.6 | **0.0** | 37 |
| `john-butcher` | 8 | KPF | 2016 | 25 | 31 | 53.5 | **0.0** | 31 |
| `scott-gumbleton` | 3 | KPF | 2013 | 25 | 35 | 58.0 | **0.0** | 35 |

**picks 40 plus** — n 49 · mean R6 407.8 · p25 7.7 · median 29.2 · p75 304.1 · zero 12%

| player | pick | pos | year | age | games | output | **realized R6** | career games |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| `andrew-swallow` | 43 | MID | 2008 | 21 | 37 | 70.5 | **3006.7** | 213 |
| `luke-parker` | 42 | MID | 2012 | 20 | 32 | 56.7 | **2821.9** | 336 |
| `jarryd-lyons` | 61 | SF | 2015 | 23 | 35 | 50.7 | **2585.6** | 194 |
| `andrew-swallow` | 43 | MID | 2007 | 20 | 34 | 68.1 | **2456.7** | 213 |
| `taylor-walker` | 64 | KPF | 2010 | 20 | 32 | 56.0 | **1651.2** | 316 |
| `bailey-dale` | 45 | MID | 2018 | 22 | 40 | 63.6 | **1442.2** | 195 |
| `rhys-stanley` | 47 | KPF | 2013 | 23 | 39 | 59.6 | **1143.3** | 230 |
| `jack-graham` | 53 | MID | 2019 | 21 | 39 | 68.6 | **770.6** | 160 |
| `robert-warnock` | 42 | RUCK | 2010 | 23 | 32 | 55.9 | **720.1** | 83 |
| `dylan-roberton` | 48 | SD | 2012 | 21 | 37 | 45.9 | **641.0** | 129 |
| `craig-bird` | 56 | MID | 2010 | 21 | 40 | 66.7 | **554.0** | 157 |
| `craig-bird` | 56 | MID | 2009 | 20 | 36 | 65.0 | **345.8** | 157 |
| `joel-patfull` | 51 | KPD | 2007 | 23 | 36 | 56.7 | **304.1** | 216 |
| `charlie-ballard` | 42 | KPD | 2019 | 20 | 32 | 54.7 | **280.8** | 143 |
| `will-schofield` | 50 | KPD | 2010 | 22 | 35 | 50.3 | **173.2** | 194 |
| `lindsay-thomas` | 53 | SF | 2008 | 20 | 35 | 54.6 | **167.7** | 212 |
| `dean-kent` | 51 | SF | 2015 | 21 | 32 | 51.0 | **141.4** | 100 |
| `alipate-carlile` | 44 | KPD | 2008 | 21 | 31 | 56.7 | **134.2** | 161 |
| `david-mackay` | 48 | MID | 2009 | 21 | 39 | 66.0 | **113.1** | 248 |
| `nicholas-holman` | 49 | MID | 2018 | 23 | 31 | 67.2 | **97.5** | 153 |
| `matthew-dea` | 43 | SD | 2014 | 23 | 31 | 53.8 | **57.3** | 70 |
| `jack-lonie` | 41 | SF | 2017 | 21 | 39 | 58.4 | **48.3** | 87 |
| `riley-knight` | 46 | SF | 2017 | 22 | 31 | 58.9 | **30.1** | 55 |
| `martin-gleeson` | 57 | MID | 2015 | 21 | 31 | 54.1 | **29.3** | 97 |
| `james-polkinghorne` | 41 | SF | 2010 | 21 | 39 | 52.4 | **29.2** | 101 |
| `kaiden-brand` | 64 | KPD | 2018 | 24 | 38 | 61.6 | **26.7** | 48 |
| `brendon-ah-chee` | 54 | SF | 2018 | 24 | 35 | 61.8 | **26.3** | 58 |
| `jake-neade` | 56 | SF | 2015 | 21 | 31 | 60.5 | **24.2** | 62 |
| `billy-stretch` | 42 | MID | 2017 | 21 | 36 | 69.4 | **22.6** | 47 |
| `kyle-cheney` | 52 | SD | 2013 | 24 | 32 | 48.5 | **22.2** | 85 |
| `shane-kersten` | 43 | KPF | 2016 | 23 | 37 | 56.9 | **21.8** | 66 |
| `jackson-nelson` | 51 | SD | 2017 | 21 | 32 | 45.7 | **18.1** | 102 |
| `zaine-cordy` | 61 | KPF | 2017 | 21 | 30 | 59.1 | **18.0** | 141 |
| `riley-knight` | 46 | SF | 2018 | 23 | 39 | 61.2 | **15.0** | 55 |
| `sam-lonergan` | 47 | MID | 2009 | 22 | 37 | 72.9 | **14.3** | 81 |
| `billy-stretch` | 42 | MID | 2018 | 22 | 38 | 72.1 | **10.5** | 47 |
| `neville-jetta` | 51 | MID | 2012 | 22 | 36 | 57.5 | **7.7** | 159 |
| `neville-jetta` | 51 | MID | 2011 | 21 | 30 | 64.3 | **6.6** | 159 |
| `ben-sinclair` | 59 | SF | 2013 | 22 | 39 | 51.4 | **2.3** | 63 |
| `rohan-bail` | 63 | MID | 2012 | 24 | 36 | 67.1 | **1.8** | 71 |
| `mitchell-hannan` | 46 | SF | 2018 | 24 | 35 | 56.5 | **1.1** | 80 |
| `jay-kennedy-harris` | 40 | MID | 2018 | 23 | 34 | 58.4 | **0.4** | 39 |
| `tony-armstrong` | 55 | SD | 2014 | 25 | 34 | 58.1 | **0.0** | 35 |
| `cory-gregson` | 47 | SF | 2018 | 22 | 39 | 51.1 | **0.0** | 39 |
| `ahmed-saad` | 40 | SF | 2015 | 26 | 33 | 45.5 | **0.0** | 33 |
| `jay-kennedy-harris` | 40 | MID | 2019 | 24 | 39 | 62.2 | **0.0** | 39 |
| `mitch-honeychurch` | 55 | SF | 2018 | 23 | 35 | 61.9 | **0.0** | 35 |
| `mitchell-farmer` | 48 | SD | 2011 | 22 | 31 | 53.4 | **0.0** | 31 |
| `ryan-gamble` | 45 | SF | 2011 | 24 | 35 | 54.5 | **0.0** | 35 |

## 8 · Declared sensitivities

| variant | panel n | P→L RMS | folds | L→T RMS | folds | verdict | σ(36–70) |
|---|---:|---:|---:|---:|---:|---|---:|
| H=10 | 2294 | 0.88% | 4/5 | 0.31% | 2/5 | PRODUCTION-ONLY | 8.5% |
| H=4 | 4969 | 0.72% | 4/5 | 0.23% | 3/5 | PRODUCTION-ONLY | 16.8% |
| core window entry<=2014 | 3593 | 0.53% | 4/5 | 0.52% | 4/5 | PRODUCTION-ONLY | 12.3% |
| discount 0% | 4033 | 0.97% | 5/5 | 0.03% | 2/5 | PRODUCTION-ONLY | 16.4% |
| games weight linear | 4033 | 0.87% | 5/5 | 0.02% | 2/5 | PRODUCTION-ONLY | 16.5% |
| grace 2 seasons | 4033 | 0.90% | 5/5 | -0.01% | 2/5 | PRODUCTION-ONLY | 16.4% |
| output = state season only | 4033 | 1.01% | 5/5 | 0.01% | 2/5 | PRODUCTION-ONLY | 17.6% |
| primary (H=6, 14%, sqrt) | 4033 | 0.89% | 5/5 | -0.02% | 2/5 | PRODUCTION-ONLY | 16.5% |

Every declared sensitivity agrees with the primary reading on both verdicts. The pedigree share is
stable across horizon, discount, grace, games-weight and output-axis choices; it falls to 8.5% at
H = 10 (a 10-season window is only observable for state years ≤ 2015, so that reading is thinner
and older) and to 12.3% on the core window alone.

## 9 · Prereg scored by number

| # | verdict | claim | measured |
|---|---|---|---|
| **P1** | HELD | panel 2,500-6,000 states over 700-1,050 careers | 4033 states, 767 careers |
| **P2** | **BREACH** | median R6 < 25% of mean in 16-35 band; >=30% zeros in <=35-game bands | median/mean 0.283 ; zero share 0.113 |
| **P3** | HELD | pick still predicts at 16-35 games: matched delta > 0 and v0 coefficient > 0 | matched delta quintile lens None (0 usable strata -> the preregistered collapse applies); tercile lens 272.6 over 7 strata; residual contrast gap 67.8 (90% CI [-51.776875152270065, 199.00198856634177]); beta_v0(16-35) 0.22329587551741345 (cluster t 4.251750729187223); beta_v0 full panel 0.49075691269015215 |
| **P4** | HELD | pedigree share at 36-70 games strictly between 5.6% and 40%, specifically 8-25% | 0.165 |
| **P5** | HELD | pedigree share non-increasing across games bands (one blip <=2pp allowed) | sequence [0.7011, 0.6641, 0.3313, 0.1645, 0.0221] ; up-steps 0 ; worst up-step 0.0000 |
| **P6** | HELD | TRAJECTORY does not clear the 2.0%/4-of-5 bar over LEVEL (seat predicts against the owner) | RMS reduction -0.0002, folds 2/5, adopt=False |
| **P7** | **BREACH** | per-position clocks clear the bar AND tall peak age >= small peak age + 1.0y | adopt=False (-0.55% RMS, 0/5 folds) ; preregistered peak-age lens DEGENERATE (pins to the age-18 boundary in all six groups: the target is REMAINING value, which declines with age for horizon reasons) -> NO SIGNAL on that lens ; supplementary raw growth clock (post-hoc, non-deciding): last positive-growth age tall 27.00 vs small/mid 25.33, gap 1.67 |
| **P8** | HELD | kako: every form predicts remaining 6-season value below his board price 1320; L and T differ by <2x | P 483.0 L 449.0 T 481.2 ; board 1320 |
| **P9** | HELD | pool band mean R6 below band A at comparable states | pool means [142.3, 235.8, 362.3, 589.6, 599.0] vs band A means [272.1, 1084.3, 1086.3, 1457.2, 1311.0] |
| **P10** | HELD | one pass, nothing tuned after a reading, breaches owned by number | single execution of this harness; no quantity re-fitted after being read |

## 10 · All cells

Every cell with n ≥ 8 (position × age band × games band × output quintile × pick band). The full
1378-cell table, including the 1284 cells too thin to print, is in `PERSISTENCE_TABLE.json` under
`cells_all_states`; the thin-cell collapse is disclosed there cell by cell.

| position | age | games | output | pick band | n | mean | p25 | median | p75 | zero |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|
| KPD | 24-26 | 71+ | Q4 | D 21-40 | 8 | 181.0 | 136.3 | 180.7 | 248.9 | 0% |
| KPD | 24-26 | 71+ | Q5 | E 41-64 | 9 | 1401.2 | 1356.4 | 1495.8 | 2059.9 | 0% |
| KPD | 27+ | 71+ | Q2 | E 41-64 | 8 | 90.2 | 0.0 | 0.6 | 96.5 | 12% |
| KPD | 27+ | 71+ | Q4 | D 21-40 | 16 | 172.8 | 46.8 | 144.3 | 234.2 | 6% |
| KPD | 27+ | 71+ | Q5 | C 13-20 | 13 | 645.5 | 366.6 | 574.3 | 959.7 | 8% |
| KPF | 20 | 0-5 | Q1 | E 41-64 | 9 | 186.0 | 0.0 | 0.0 | 12.6 | 33% |
| KPF | 20 | 6-15 | Q1 | D 21-40 | 8 | 273.2 | 0.1 | 1.7 | 255.5 | 25% |
| KPF | 24-26 | 71+ | Q4 | D 21-40 | 10 | 991.7 | 411.4 | 799.9 | 1683.1 | 0% |
| KPF | 24-26 | 71+ | Q5 | A 1-6 | 11 | 1711.6 | 1001.3 | 2220.1 | 2373.3 | 0% |
| KPF | 24-26 | 71+ | Q5 | B 7-12 | 14 | 1086.9 | 479.5 | 964.2 | 1880.4 | 0% |
| KPF | 24-26 | 71+ | Q5 | D 21-40 | 11 | 1424.3 | 1097.8 | 1308.0 | 1730.0 | 0% |
| KPF | 27+ | 71+ | Q5 | A 1-6 | 10 | 2066.6 | 1276.8 | 2384.0 | 2937.2 | 0% |
| KPF | 27+ | 71+ | Q5 | D 21-40 | 9 | 868.8 | 670.2 | 909.9 | 1033.5 | 0% |
| KPF | <=19 | 0-5 | Q1 | D 21-40 | 11 | 122.9 | 1.6 | 14.9 | 193.9 | 0% |
| MID | 20 | 0-5 | Q1 | E 41-64 | 10 | 261.0 | 0.0 | 0.0 | 2.5 | 30% |
| MID | 20 | 6-15 | Q1 | D 21-40 | 14 | 222.2 | 0.0 | 3.6 | 268.0 | 7% |
| MID | 20 | 6-15 | Q1 | E 41-64 | 8 | 131.7 | 4.3 | 106.8 | 243.8 | 0% |
| MID | 21 | 16-35 | Q1 | D 21-40 | 8 | 94.3 | 0.5 | 11.4 | 68.2 | 0% |
| MID | 21 | 16-35 | Q2 | D 21-40 | 8 | 694.8 | 18.3 | 447.0 | 1249.3 | 0% |
| MID | 21 | 6-15 | Q1 | E 41-64 | 8 | 26.8 | 0.0 | 0.0 | 0.2 | 50% |
| MID | 21 | 6-15 | Q2 | E 41-64 | 8 | 272.0 | 1.5 | 4.4 | 48.2 | 12% |
| MID | 22-23 | 16-35 | Q1 | D 21-40 | 9 | 38.2 | 0.0 | 0.0 | 2.2 | 44% |
| MID | 22-23 | 36-70 | Q2 | D 21-40 | 8 | 589.5 | 23.9 | 585.3 | 790.1 | 12% |
| MID | 22-23 | 36-70 | Q3 | D 21-40 | 15 | 342.9 | 28.4 | 224.3 | 615.8 | 7% |
| MID | 22-23 | 71+ | Q3 | A 1-6 | 9 | 702.8 | 21.4 | 798.3 | 865.8 | 0% |
| MID | 22-23 | 71+ | Q4 | A 1-6 | 8 | 1615.0 | 1055.0 | 1665.6 | 2281.1 | 0% |
| MID | 22-23 | 71+ | Q4 | D 21-40 | 12 | 1704.8 | 818.9 | 1083.2 | 2618.9 | 0% |
| MID | 22-23 | 71+ | Q5 | A 1-6 | 15 | 3701.9 | 2412.0 | 3612.6 | 5207.8 | 0% |
| MID | 22-23 | 71+ | Q5 | B 7-12 | 12 | 3298.6 | 1779.0 | 2692.9 | 4821.3 | 0% |
| MID | 22-23 | 71+ | Q5 | D 21-40 | 10 | 2230.6 | 1211.0 | 2274.5 | 2731.0 | 0% |
| MID | 24-26 | 36-70 | Q2 | E 41-64 | 8 | 24.2 | 1.4 | 5.7 | 13.7 | 12% |
| MID | 24-26 | 71+ | Q3 | D 21-40 | 11 | 932.6 | 154.7 | 732.3 | 1492.4 | 0% |
| MID | 24-26 | 71+ | Q4 | A 1-6 | 24 | 913.8 | 314.5 | 824.6 | 1251.3 | 0% |
| MID | 24-26 | 71+ | Q4 | B 7-12 | 13 | 1482.6 | 1231.9 | 1394.1 | 1689.6 | 0% |
| MID | 24-26 | 71+ | Q4 | C 13-20 | 11 | 1127.6 | 880.7 | 1018.0 | 1398.9 | 0% |
| MID | 24-26 | 71+ | Q4 | D 21-40 | 19 | 1107.0 | 436.6 | 818.1 | 1264.3 | 0% |
| MID | 24-26 | 71+ | Q5 | A 1-6 | 27 | 2407.6 | 1673.0 | 2282.6 | 2792.7 | 0% |
| MID | 24-26 | 71+ | Q5 | B 7-12 | 16 | 3101.7 | 1572.8 | 2539.1 | 4489.2 | 0% |
| MID | 24-26 | 71+ | Q5 | C 13-20 | 20 | 2462.5 | 1830.3 | 2397.9 | 3058.4 | 0% |
| MID | 24-26 | 71+ | Q5 | D 21-40 | 17 | 1523.6 | 898.8 | 1246.2 | 1935.5 | 0% |
| MID | 24-26 | 71+ | Q5 | E 41-64 | 16 | 2392.7 | 1699.8 | 2486.9 | 3064.0 | 0% |
| MID | 27+ | 71+ | Q3 | A 1-6 | 9 | 131.3 | 0.0 | 4.7 | 21.2 | 22% |
| MID | 27+ | 71+ | Q4 | A 1-6 | 9 | 581.4 | 21.3 | 151.6 | 293.8 | 0% |
| MID | 27+ | 71+ | Q4 | C 13-20 | 13 | 578.9 | 368.3 | 459.2 | 948.2 | 8% |
| MID | 27+ | 71+ | Q4 | D 21-40 | 14 | 536.0 | 103.7 | 440.4 | 887.1 | 0% |
| MID | 27+ | 71+ | Q5 | A 1-6 | 23 | 1602.1 | 922.5 | 1480.1 | 2402.4 | 0% |
| MID | 27+ | 71+ | Q5 | B 7-12 | 17 | 1423.2 | 849.9 | 1090.9 | 1825.3 | 0% |
| MID | 27+ | 71+ | Q5 | C 13-20 | 10 | 1263.3 | 734.5 | 1229.9 | 1539.6 | 0% |
| MID | 27+ | 71+ | Q5 | D 21-40 | 10 | 1352.1 | 187.3 | 1359.2 | 2395.5 | 10% |
| MID | 27+ | 71+ | Q5 | E 41-64 | 16 | 1462.4 | 802.9 | 1558.3 | 1980.0 | 0% |
| MID | <=19 | 0-5 | Q1 | C 13-20 | 9 | 691.6 | 139.6 | 444.1 | 570.7 | 0% |
| MID | <=19 | 0-5 | Q1 | D 21-40 | 21 | 112.9 | 0.0 | 4.8 | 52.7 | 10% |
| MID | <=19 | 0-5 | Q1 | E 41-64 | 17 | 84.0 | 0.0 | 0.1 | 31.4 | 12% |
| MID | <=19 | 16-35 | Q2 | A 1-6 | 10 | 1045.2 | 145.1 | 1001.6 | 1388.7 | 0% |
| MID | <=19 | 16-35 | Q3 | A 1-6 | 12 | 1927.3 | 814.8 | 1596.3 | 2861.1 | 0% |
| MID | <=19 | 6-15 | Q1 | E 41-64 | 9 | 400.0 | 0.0 | 13.8 | 105.8 | 11% |
| MID | <=19 | 6-15 | Q2 | D 21-40 | 9 | 840.7 | 70.6 | 816.2 | 1203.1 | 0% |
| SD | 20 | 6-15 | Q1 | D 21-40 | 10 | 107.8 | 0.0 | 0.0 | 3.8 | 20% |
| SD | 22-23 | 16-35 | Q2 | E 41-64 | 8 | 37.7 | 1.2 | 11.7 | 29.0 | 12% |
| SD | 22-23 | 36-70 | Q3 | D 21-40 | 13 | 136.0 | 0.4 | 6.6 | 168.6 | 8% |
| SD | 22-23 | 36-70 | Q3 | E 41-64 | 10 | 225.5 | 31.9 | 202.6 | 267.7 | 0% |
| SD | 22-23 | 36-70 | Q4 | D 21-40 | 9 | 394.7 | 14.2 | 51.5 | 196.8 | 0% |
| SD | 22-23 | 36-70 | Q4 | E 41-64 | 8 | 330.4 | 11.0 | 214.4 | 675.3 | 0% |
| SD | 24-26 | 71+ | Q5 | C 13-20 | 14 | 889.3 | 524.6 | 886.6 | 1201.9 | 0% |
| SD | 24-26 | 71+ | Q5 | D 21-40 | 13 | 590.4 | 141.7 | 346.2 | 837.0 | 0% |
| SD | 24-26 | 71+ | Q5 | E 41-64 | 12 | 682.9 | 6.7 | 231.2 | 749.4 | 8% |
| SD | 27+ | 71+ | Q5 | C 13-20 | 11 | 1104.4 | 159.8 | 1412.9 | 1886.2 | 9% |
| SD | <=19 | 0-5 | Q1 | D 21-40 | 11 | 137.4 | 0.5 | 14.7 | 184.7 | 0% |
| SF | 20 | 0-5 | Q1 | E 41-64 | 11 | 258.5 | 0.0 | 0.0 | 2.4 | 45% |
| SF | 20 | 6-15 | Q1 | E 41-64 | 11 | 113.5 | 0.0 | 0.2 | 27.1 | 9% |
| SF | 22-23 | 16-35 | Q3 | E 41-64 | 8 | 246.5 | 0.0 | 16.1 | 65.3 | 38% |
| SF | 22-23 | 36-70 | Q3 | D 21-40 | 8 | 341.8 | 9.8 | 133.8 | 493.8 | 12% |
| SF | 22-23 | 36-70 | Q3 | E 41-64 | 12 | 307.9 | 15.0 | 86.4 | 275.3 | 0% |
| SF | 22-23 | 36-70 | Q4 | D 21-40 | 9 | 664.3 | 148.0 | 543.5 | 1139.9 | 0% |
| SF | 22-23 | 36-70 | Q5 | D 21-40 | 9 | 1481.7 | 443.5 | 1053.9 | 1797.6 | 0% |
| SF | 22-23 | 71+ | Q5 | A 1-6 | 12 | 2303.9 | 1366.4 | 2220.5 | 3198.8 | 0% |
| SF | 24-26 | 36-70 | Q3 | E 41-64 | 10 | 156.3 | 0.1 | 38.1 | 232.0 | 20% |
| SF | 24-26 | 36-70 | Q4 | D 21-40 | 10 | 168.4 | 14.1 | 114.9 | 313.3 | 10% |
| SF | 24-26 | 71+ | Q4 | D 21-40 | 12 | 366.6 | 123.6 | 154.9 | 715.4 | 0% |
| SF | 24-26 | 71+ | Q4 | E 41-64 | 13 | 244.6 | 15.2 | 60.2 | 363.7 | 0% |
| SF | 24-26 | 71+ | Q5 | B 7-12 | 12 | 1618.3 | 852.2 | 1283.6 | 1608.2 | 0% |
| SF | 24-26 | 71+ | Q5 | C 13-20 | 10 | 1111.1 | 560.0 | 1056.8 | 1613.1 | 0% |
| SF | 24-26 | 71+ | Q5 | D 21-40 | 17 | 1203.1 | 318.0 | 1452.9 | 1877.0 | 0% |
| SF | 27+ | 71+ | Q2 | D 21-40 | 8 | 0.8 | 0.0 | 0.1 | 0.5 | 38% |
| SF | 27+ | 71+ | Q3 | D 21-40 | 8 | 1.3 | 0.0 | 0.8 | 1.6 | 25% |
| SF | 27+ | 71+ | Q3 | E 41-64 | 11 | 36.0 | 0.0 | 0.8 | 14.1 | 27% |
| SF | 27+ | 71+ | Q4 | D 21-40 | 11 | 179.7 | 6.4 | 45.0 | 379.6 | 9% |
| SF | 27+ | 71+ | Q5 | B 7-12 | 8 | 1089.7 | 14.6 | 1321.8 | 1818.4 | 0% |
| SF | 27+ | 71+ | Q5 | D 21-40 | 12 | 843.1 | 341.9 | 715.7 | 1178.2 | 8% |
| SF | 27+ | 71+ | Q5 | E 41-64 | 9 | 1070.4 | 826.0 | 1045.4 | 1192.0 | 0% |
| SF | <=19 | 0-5 | Q1 | D 21-40 | 14 | 143.4 | 0.5 | 4.2 | 202.3 | 21% |
| SF | <=19 | 0-5 | Q1 | E 41-64 | 16 | 272.1 | 0.6 | 44.2 | 371.6 | 6% |
| SF | <=19 | 6-15 | Q1 | E 41-64 | 8 | 93.7 | 0.1 | 50.6 | 131.6 | 0% |
| SF | <=19 | 6-15 | Q2 | D 21-40 | 8 | 325.8 | 9.4 | 155.5 | 514.2 | 0% |

