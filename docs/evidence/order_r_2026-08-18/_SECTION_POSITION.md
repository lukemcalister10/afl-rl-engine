## 1 · THE READ-ONLY POSITION TEST — THE POOLING IS DEFENSIBLE, AND A SPLIT WOULD MAKE THE REVERSAL WORSE

**No board was built for this. It is a measurement on ORDER P's own estimator and it rules on nothing.**

The owner asked whether pooling `PG` into TALL (KPD/KPF/RUCK) and SMALL (MID/SD/SF) is defensible,
given that SD/SF and MID price and perform very differently.

### 1.1 First, what is ALREADY separate — and the two bar objects reconciled

**The position-specific S1 age bar already carries the level difference. `PG` is only the pedigree
INCREMENT above each position's own bar.** That is the whole of what is pooled.

There are TWO age-bar objects in this engine and they must not be confused:

| object | what it is | MID at 21 | SF at 21 | gap |
|---|---|---:|---:|---:|
| `o36_bar(pos, 21)` | the S1 bar in the PRODUCTION path, dose-scaled by `RL_O36_LAM_S1` 0.40 | **75.59** | **66.39** | **9.20** |
| `o32_gate_bar(pos, 21)` | **the bar the CHARGE reads** — `MA.REPL - REPL_DROP` minus the full class delta | **65.83** | **56.63** | **9.20** |

**The order quotes the first. The charge uses the second. THE GAP IS IDENTICAL — 9.20 points a game
on either object** — because the development delta is class-pooled and cancels in the difference.
So nothing turns on which one is quoted, and both are printed rather than one being silently
substituted for the other.

### 1.2 The slopes DO differ numerically. Not one difference is statistically material.

`dPG/dln(v0)`, averaged across each fit's own support, refitted per position on ORDER P's own
estimator (local-linear tricube, bandwidth 0.40 in log-v0 units, games-weighted, isotonised):

| group | players | avg slope | 90% CI (player-level cluster bootstrap, 2,000 draws, seed 32) |
|---|---:|---:|---|
| TALL pool | 442 | **8.2896** | [+6.39, +10.33] |
| SMALL pool | 1,146 | **8.9432** | [+7.73, +10.66] |
| KPD | 191 | **3.0467** | [+0.99, +7.95] |
| KPF | 257 | **8.6718** | [+5.74, +10.81] |
| RUCK | 96 | **8.9213** | **[+4.97, +918.83]** |
| MID | 583 | **9.9129** | [+8.34, +12.68] |
| SD | 420 | **9.0224** | [+6.78, +12.48] |
| SF | 602 | **9.9502** | [+8.03, +11.99] |

**The pooled slopes reproduce the engine's own published grid to the last decimal — TALL 8.2896 and
SMALL 8.9432 — so the refit is the same object, not a lookalike.**

**PAIRWISE, NOT ONE DIFFERENCE IS MATERIAL. Every pair's 90% CIs overlap:**

| pair | slope A | slope B | difference | CIs |
|---|---:|---:|---:|---|
| MID vs SD | 9.9129 | 9.0224 | +0.89 | **OVERLAP** |
| MID vs SF | 9.9129 | 9.9502 | −0.04 | **OVERLAP** |
| SD vs SF | 9.0224 | 9.9502 | −0.93 | **OVERLAP** |
| KPD vs KPF | 3.0467 | 8.6718 | **−5.63** | **OVERLAP** |
| KPD vs RUCK | 3.0467 | 8.9213 | **−5.87** | **OVERLAP** |
| KPF vs RUCK | 8.6718 | 8.9213 | −0.25 | **OVERLAP** |

**KPD's point estimate is 5.6 points a game per log-unit below KPF's and it STILL cannot be
separated from it.** That is how wide these intervals are.

**RUCK's bootstrap upper limit is +918.83.** On resampled draws of 96 players the estimator produces
a near-vertical fit. That is not a wide interval, it is a **degenerate one**, and it is the single
strongest piece of evidence in this test: a per-position RUCK premium is not estimable at all on this
sample. It is printed at full precision rather than trimmed.

### 1.3 The effective sample, and where it runs out

ESS is the kernel's own effective sample at that price: `(Σk)² / Σk²` with `k` the tricube weight
times games. It is what the fit actually leans on, not the raw row count. `ESS_THIN` in ORDER P's own
library is **30**.

| group | v0=200 | 500 | 1,000 | 1,500 | 2,000 | 2,500 | **3,000** | verdict at the expensive end |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| KPD | 57.6 | 130.4 | 46.3 | 17.7 | 9.1 | 8.1 | **4.9** | **NOT SUPPORTABLE past ~1,000** |
| KPF | 79.0 | 106.4 | 114.5 | 83.9 | 60.0 | 51.2 | **29.5** | supportable to ~2,000, not beyond |
| RUCK | 14.7 | 37.7 | 48.5 | 25.4 | 4.9 | 12.7 | **9.7** | **NOT SUPPORTABLE past ~1,000** |
| **MID** | 182.6 | 145.5 | 209.1 | 163.4 | 174.8 | 136.4 | **134.9** | **SUPPORTABLE to 3,000** |
| SD | 180.0 | 99.1 | 149.1 | 102.8 | 41.4 | 29.3 | **26.0** | supportable to ~2,000, not beyond |
| **SF** | 213.1 | 270.8 | 179.4 | 100.5 | 92.1 | 67.8 | **55.0** | **SUPPORTABLE to 3,000** |
| TALL pool | 145.7 | 267.0 | 209.0 | 125.8 | 73.6 | 71.9 | **43.6** | *(the object a split would replace)* |
| SMALL pool | 570.0 | 515.1 | 537.1 | 365.3 | 307.9 | 233.3 | **215.7** | *(the object a split would replace)* |

**The order's own figure is confirmed: TALL POOLED reads 43.6 effective at v0 3,000 for all three
positions combined**, against the ~47 the order quoted. It is already thin before anything is split.

### 1.4 THE VERDICT, and it REFINES the answer the order suggested

The order said: *"If the answer is 'only MID has the sample', say exactly that."*

**The measured answer is not quite that, and this seat reports what it measured rather than the
answer it was offered. TWO positions have the sample at the expensive end, not one: MID (134.9) and
SF (55.0).** SD (26.0) and KPF (29.5) sit just under the line. **KPD (4.9) and RUCK (9.7) have
essentially nothing above the median price.**

**But the sample is not the binding constraint. The CONFIDENCE INTERVALS are.** Even MID and SF,
which have the rows, cannot be told apart from each other or from the pool: MID 9.91 and SF 9.95
against SMALL pooled 8.94, with intervals more than 3.5 points a game wide.

**So: a per-position fit is statistically supportable for NO position.** Not one of the six can be
distinguished from the class it sits in, and two of the six cannot be estimated at all.

### 1.5 Would a per-position premium reduce or worsen the pick reversal? IT WOULD WORSEN IT.

The reversal is `dPG/dln(v0) > 1/(BETA_sat·A)`. At saturation the threshold is `1/0.11465 = 8.723`.
Pooling AVERAGES slopes. Splitting replaces the pooled slope with each position's own.

| position | own slope | pool slope | own − pool | effect of splitting |
|---|---:|---:|---:|---|
| KPD | 3.0467 | 8.2896 | **−5.24** | better — its own slope is shallower |
| KPF | 8.6718 | 8.2896 | +0.38 | **worse** |
| RUCK | 8.9213 | 8.2896 | +0.63 | **worse** |
| MID | 9.9129 | 8.9432 | +0.97 | **worse** |
| SD | 9.0224 | 8.9432 | +0.08 | no material change |
| SF | 9.9502 | 8.9432 | **+1.01** | **worse** |

**Four of the six positions get a STEEPER slope under a split, and they are the four that carry the
games.** Only KPD improves, and KPD is precisely the position whose fit collapses at the expensive
end — so the improvement is bought with the least reliable number in the table.

**The local slope matters more than the average, because the reversal is a LOCAL condition.**

| group | avg slope | **max local slope** | v0 at the max | reverses at A=1? |
|---|---:|---:|---:|---|
| TALL pool | 8.2896 | 57.07 | 2,864 | YES |
| SMALL pool | 8.9432 | 35.99 | 3,342 | YES |
| KPD | 3.0467 | 24.94 | 1,120 | YES |
| **KPF** | 8.6718 | **82.33** | 2,636 | YES |
| RUCK | 8.9213 | 64.05 | 1,327 | YES |
| MID | 9.9129 | 50.43 | 1,476 | YES |
| SD | 9.0224 | 47.77 | 153 | YES |
| SF | 9.9502 | 56.25 | 94 | YES |

**Every group already reverses locally, pooled or split.** And splitting makes the worst local slope
WORSE for the TALL class: KPF alone peaks at **82.33** against the TALL pool's 57.07. **A split does
not repair the reversal. It sharpens it, in the class that has the least data to justify the change.**

### 1.6 One more measured fact worth stating, because it changes where the reversal lives

The reversal threshold at saturation is `1/BETA_sat`. **On the AVERAGE slope the reversal is a SMALL-
class fact, not a board-wide one:**

- SMALL average slope **8.9432** > threshold **8.7225** → the SMALL class reverses on average.
- TALL average slope **8.2896** < threshold **8.7225** → the TALL class does NOT reverse on average.

TALL reverses only in its locally steep segments. This matters for the ORDER R grid: **lowering
`BETA_sat` raises the threshold, and at `BETA_sat` 0.111 the threshold becomes 9.0090, which clears
the SMALL average slope of 8.9432 as well.** That is the whole reason 0.111 was chosen, and it was
chosen from this measurement, not from a board.
