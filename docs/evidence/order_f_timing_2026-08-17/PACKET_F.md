# PACKET F — THE ENTRY TIMING-WEDGE: VERIFIED AND KILLED, AND WHAT THE V-SHAPE ACTUALLY IS

**Order F. Issue #334. Branch `land/order-29`. READ-ONLY — nothing is wired, no engine, board, law or
store file is touched. Rule fixed in `PREREG_F.md`, pushed before any number (commit `d20f71c`).**

Evidence: `PREREG_F.md` · `o_f_wedge.py` · `WEDGE_F_out.txt` (the full console) · `WEDGE_F.json`.

---

## THE SHORT VERSION

The owner asked why picks 21-64 trace a V: entry 1.00 → year 1 ≈ 0.92 → year 5 ≈ 1.48. The
supervisor's answer was a **timing wedge**: the entry surface was fitted to an *undiscounted* career
total, so it overstates the fair today-price, and overstates it most for bands whose value arrives
late. I was asked to verify or kill it.

**It is killed, at the first step, on the code.** The entry surface was **never** fitted to an
undiscounted total. Its target is the grace-A Layer-2 career score, and every season in that score is
divided by a 14%/yr discount factor. There is no undiscounted total anywhere in the lineage.

**But the seat did not come back empty.** Reading the two discount clocks against each other — the
curve's clock and the engine's clock — turns up something the timing hypothesis was groping toward
and got backwards. Under the board's own grace-A rule, **the entry→year-1 step earns no carry at all
for a normal-age draftee.** The no-arb table benchmarks that step at 1.14 for everyone. It should be
**1.00** for an entrant aged ≤19 and **1.30** for an entrant aged ≥20. Nearly the whole *level* of the
V's left arm is that benchmark, not a mispricing.

The *spread* between bands — the part that makes it a V rather than a step — is **not** explained by
timing (bands barely differ in when their value arrives) and **not** explained by the clock (the clock
correction is uniform in pick). It tracks **year-one sitting** at rank correlation **−0.80**. That is
the adversarial alternative, and on this evidence it is the one left standing.

---

## 1. P1 — WHAT THE ENTRY SURFACE WAS ACTUALLY FITTED TO

### VERDICT: FALSIFIED.

The v0 entry surface is derived in `docs/evidence/grace_adoption_2026-08-13/o28_derive.py`. Its fit
target is the argument `SC`:

```
   158 | def derive(SC, boundary='hybrid', monotone=True):
   159 |     nd = [dict(key=k, pick=ATTR[k]['pick'], value=SC[k]['total'], pos=E[k]['position_group'])
   160 |           for k in L2['fit_nd_keys']]
```

and the call site names it:

```
   311 | GA = L2['grace_a']
   312 | CAND = derive(GA, 'hybrid', True)                 # THE CANDIDATE LANDING CURVE
```

`L2['grace_a']` is built in `o26b_layer2.py`:

```
   636 | GA_O, _ = score_all('flat14', w_sqrt, True, grace=grace_O('A'))
```

and `score_all` sums an observed leg and a projected tail leg into `total`. **The line that decides
P1** is inside the observed leg:

```
   376 | def observed_value(e, D, wfn):
   377 |     """The observed leg of a career: every played season, valued at the position PLAYED, weighted by
   378 |     games, discounted to acquisition. Returns (board points, per-season detail, counters)."""
   ...
   389 |         k = (s['year'] - ey) if ey is not None else 0
   ...
   395 |         pts = MA.SCALE * raw * w / D.f(ea, k)
   396 |         tot += pts
```

Every season is **divided by a discount factor keyed on `k = season_year − entry_year`**. `D.f` is:

```
   350 |     def f(self, entry_age, k):
   351 |         if self.grace is not None:
   352 |             k = max(0, k - self.grace(entry_age))
   353 |         return MA.disc_factor(entry_age, MA.LENS['bal'], k, 'bal')
```

and the tail leg says so in its own docstring: *"the projected tail … **discounted to acquisition on
the SAME ladder as the observed leg**"* (`o26b_layer2.py:402-405`). The same target reappears when
Order 31-F reconstructs the fit population for the head fix (`o31f_headfix.py:83`,
`value=GA[k]['total']`).

**So the fit target is a time-of-delivery *discounted* career value**: flat 14%/yr
(`LENS['bal'] = 0.14`, `AGE_DISC` off), with the grace-A exponent shift `max(0, k − G)` the owner
ruled at Order 28 (G = 2 for entry age ≤19, 0 otherwise, reading O).

P1 predicted "undiscounted". The code says "discounted". **The hypothesis dies here**, and per
`PREREG_F.md` §5 the wedge computation as specified stops and is reported below only as a
counterfactual bound.

### The residual, checked before moving on

The grace shift does leave the target *under*-discounted relative to a strict 14% ladder — by exactly
`1.14^G`. But that residual is a **level set by the entrant's age**, not a **gradient in delivery
timing**: from season `G+1` onward the two ladders differ by a constant, so a cell that delivers later
gets no deeper residual than one that delivers early. Measured (Part 4 of the console):

| cell | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 | RD | SSP | UNR | IRE | PDA | PDN | PDS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `W_resid` | 0.748 | 0.760 | 0.763 | 0.785 | 0.770 | 0.858 | 0.849 | 0.956 | 0.784 | 0.766 | 0.909 | 0.770 |

The five ND bands span **0.037**. The drops they are supposed to explain span **0.175**. Structurally
and numerically, this residual cannot make a V.

---

## 2. THE TWO CLOCKS — THE FINDING THAT REPLACES THE HYPOTHESIS

The engine's `disc_factor` was **lifted by source text and exec'd verbatim** (md5
`93a198a86f7c832dba79e41de5146d8c`); the live config is `AGE_DISC` off, `LENS['bal'] = 0.14`; control
`disc_factor(18, 0.14, 3, grace=0) == 1.14³` PASS. Grace-A is **on by default** on the board since
Order 29's landing (`rl_model.py:234`, `RL_GRACE` defaults to `'1'`).

Order 28 reconciled two clocks with one rule (`rl_model.py:205-211`): curve side `k_c = season_year −
entry_year` with seasons 1 and 2 free; engine side `k_e` = seasons ahead of the pricing year, `k_e = 0`
always free, so **one** extra free step. Put the two vantages side by side for an entrant drafted in
year *e*, his season *e+j* carrying delivered value *v_j*:

**Entry age ≤ 19** (curve `G_O = 2`; engine grace 0 at the year-1 vantage)

| season j | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| weight in ENTRY price | 1.00000 | 1.00000 | 0.87719 | 0.76947 | 0.67497 | 0.59208 | 0.51937 |
| weight in YEAR-1 price | *delivered* | 1.00000 | 0.87719 | 0.76947 | 0.67497 | 0.59208 | 0.51937 |
| **accretion yr1/entry** | — | **1.00000** | **1.00000** | **1.00000** | **1.00000** | **1.00000** | **1.00000** |

**Entry age ≥ 20** (curve `G_O = 0`; engine grace 0)

| season j | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| weight in ENTRY price | 0.87719 | 0.76947 | 0.67497 | 0.59208 | 0.51937 | 0.45559 | 0.39964 |
| weight in YEAR-1 price | *delivered* | 1.00000 | 0.87719 | 0.76947 | 0.67497 | 0.59208 | 0.51937 |
| **accretion yr1/entry** | — | **1.29960** | **1.29960** | **1.29960** | **1.29960** | **1.29960** | **1.29960** |

Every surviving season accretes by the same factor, so the whole price does.

> **For a normal-age draftee the entry price and the year-1 price weight every surviving season
> identically. The entry→year-1 step earns NO CARRY.** Grace-A gives seasons 1 and 2 full weight on the
> curve clock and exactly one extra free step on the engine clock, and the two were *designed* to line
> up. The consequence appears not to have been carried into the no-arb benchmark.
>
> **For a mature-age entrant the same step accretes 1.30, not 1.14** — he has no grace on either
> clock, *and* the curve clock sits one index step ahead of the engine clock at the corresponding
> vantage (the curve prices his first played season at `1.14⁻¹` while the engine, one year later,
> prices the then-present season at 1.00).

So the board-consistent fair year-1 mark is

    fair_board = accretion(entry age) x (1 - s1),   accretion = 1.00 (age <= 19) or 1.30 (age >= 20)

against Order C's `fair_C = 1.14 × (1 − s1)` for everyone. `s1` is the year-one delivered share, rebuilt
with **Order C's own construction** (`o34_attribution.py::cell_line`) so the two are comparable — the
reproduction control is tight: my `fair_C` reads 1.122 / 1.110 / 1.124 / 1.101 / 1.107 against Order C's
published 1.120 / 1.111 / 1.124 / 1.103 / 1.107.

---

## 3. THE DELIVERY TIMING PROFILES

Built on the **house delivered-value ruler**, lifted by source text out of
`docs/evidence/order32_s4_2026-08-17/s4_shootout.py` (md5 `ce730ab0c5fa62da8f920c2c9ec8672c`), with the
`SV` assembly lifted verbatim too. Classes 2005-2019, right censor 2025, force-majeure keys excluded.
Value-weighted share of career delivered value arriving in year *k* after entry:

| cell | n | U=0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | yr8 | mean yr |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ND 1-10 | 150 | 0 | 0.007 | 0.039 | 0.069 | 0.098 | 0.111 | 0.131 | 0.110 | 0.099 | 6.22 |
| ND 11-20 | 150 | 2 | 0.012 | 0.028 | 0.050 | 0.098 | 0.114 | 0.134 | 0.127 | 0.100 | 6.49 |
| ND 21-30 | 150 | 6 | 0.007 | 0.032 | 0.071 | 0.113 | 0.094 | 0.134 | 0.134 | 0.106 | 6.35 |
| ND 31-40 | 150 | 16 | 0.015 | 0.023 | 0.062 | 0.078 | 0.104 | 0.118 | 0.100 | 0.078 | 6.21 |
| ND 41-64 | 354 | 72 | 0.013 | 0.025 | 0.044 | 0.079 | 0.093 | 0.127 | 0.119 | 0.121 | 6.68 |
| RD | 543 | 230 | 0.031 | 0.040 | 0.077 | 0.100 | 0.103 | 0.111 | 0.128 | 0.116 | 6.38 |
| MSD *(thin)* | 9 | 6 | 0.014 | 0.017 | 0.069 | 0.160 | 0.117 | 0.624 | 0.000 | 0.000 | 5.22 |
| SSP *(thin)* | 13 | 5 | 0.097 | 0.151 | 0.270 | 0.055 | 0.223 | 0.080 | 0.125 | 0.000 | **3.89** |
| UNR | 44 | 24 | 0.004 | 0.034 | 0.057 | 0.154 | 0.183 | 0.087 | 0.008 | 0.047 | 6.55 |
| IRE | 43 | 23 | 0.004 | 0.023 | 0.007 | 0.051 | 0.111 | 0.140 | 0.243 | 0.127 | 6.53 |
| PDA | 32 | 13 | 0.002 | 0.001 | 0.149 | 0.184 | 0.162 | 0.058 | 0.220 | 0.117 | 5.71 |
| PDN *(thin)* | 17 | 9 | 0.000 | 0.002 | 0.008 | 0.209 | 0.071 | 0.278 | 0.252 | 0.180 | 6.09 |
| PDS | 21 | 14 | 0.000 | 0.000 | 0.000 | 0.116 | 0.131 | 0.116 | 0.039 | 0.122 | **7.54** |

Cross-player dispersion of each player's own wedge (p25 / p50 / p75) is in the console; it is wide
(e.g. ND 41-64 0.450 / 0.593 / 0.755) — the cohort means below are not tight objects.

**The single most important number in this table: the five ND bands' mean delivery year spans 6.21 to
6.68 — 0.47 of a year.** Draft bands do not differ in *when* their value arrives. They differ in *how
much* of it there is (the `U = 0` column: 0 washouts in 1-10, 72 of 354 in 41-64). A story that needs
timing to separate the bands has almost no timing to work with.

**P3 (SSP) is confirmed as a fact and fails as an explanation.** SSP's value genuinely arrives early —
mean year 3.89 against ~6.4 for everything else, 51.8% of its value in the first three years. Its wedge
is correspondingly the largest of any pool arm (**sign test S1: PASS**). But the wedge is 0.618 and the
inversion needs 1.536. Right delivery-timing signal, wrong order of magnitude, on n = 13. **Sign test
S2 FAILS**: PDN (0.458) and PDA (0.478) sit *above* RD (0.434), not below.

---

## 4. THE MATCH TEST, AT THE PREREGISTERED TOLERANCE

`W_implied = observed mark / fair_C`. `W_pure = Σ s_k · 1.14⁻ᵏ` — the counterfactual bound, i.e. what
the wedge *would* be if P1 had been true. Tolerance fixed in advance: MATCH ≤ 0.05, NEAR ≤ 0.10,
MISS > 0.10; cells with n < 15 are printed THIN and carry no verdict.

| cell | n | s1 | obs mark | fair_C | W_implied | W_pure | diff | verdict |
|---|---|---|---|---|---|---|---|---|
| ND 1-10 | 150 | 0.016 | 1.048 | 1.122 | 0.934 | 0.404 | −0.529 | **MISS** |
| ND 11-20 | 150 | 0.026 | 1.087 | 1.110 | 0.979 | 0.402 | −0.577 | **MISS** |
| ND 21-30 | 150 | 0.014 | 1.037 | 1.124 | 0.923 | 0.412 | −0.511 | **MISS** |
| ND 31-40 | 150 | 0.034 | 0.885 | 1.101 | 0.804 | 0.374 | −0.429 | **MISS** |
| ND 41-64 | 354 | 0.029 | 0.929 | 1.107 | 0.839 | 0.385 | −0.454 | **MISS** |
| RD | 543 | 0.061 | 0.980 | 1.070 | 0.916 | 0.434 | −0.482 | **MISS** |
| SSP | 13 | 0.138 | 1.510 | 0.983 | 1.536 | 0.618 | −0.918 | THIN |
| UNR | 44 | 0.009 | 0.620 | 1.130 | 0.549 | 0.414 | −0.134 | **MISS** |
| IRE | 43 | 0.008 | 1.090 | 1.130 | 0.964 | 0.374 | −0.590 | **MISS** |
| PDA | 32 | 0.003 | 0.810 | 1.137 | 0.712 | 0.478 | −0.235 | **MISS** |
| PDN | 17 | 0.000 | 0.640 | 1.140 | 0.561 | 0.458 | −0.103 | **MISS** |
| PDS | 21 | 0.001 | 0.760 | 1.139 | 0.667 | 0.387 | −0.280 | **MISS** |

**Scored cells: 11. MATCH 0. NEAR 0. MISS 11.** The prereg's support bar (≥7 MATCH, ≤2 MISS, both sign
tests) fails on every clause. Band rank correlation is +0.600 — the right *direction*, on five points,
and worthless against a level error of −0.5.

The failure is not marginal and it is not a tolerance quibble: **the wedge is roughly half of what the
match would need, everywhere.** The reason is in Part 3 — these cohorts deliver their value around year
6, so a 14% ladder halves it, while the observed marks sit within ~20% of their benchmark.

And the shape fails independently of the level: **band `W_pure` spread 0.038 against a band `W_implied`
spread of 0.175.** Even taken entirely on trust, the timing story could supply at most **22%** of the
V's spread. Its premise is false as well.

---

## 5. THE ADVERSARIAL ALTERNATIVES

### ALT-2 — the benchmark, not the price (this is Part 2's prediction, tested)

Re-basing the fair mark onto the board's own clock, `fair_board = accretion(age) × (1 − s1)`, mixed by
entry points inside each cell:

| cell | n | share ≤19 | obs | fair_C | gap_C | **fair_board** | **gap_board** | better? |
|---|---|---|---|---|---|---|---|---|
| ND 1-10 | 150 | 1.00 | 1.048 | 1.122 | −0.074 | 0.984 | **+0.064** | yes |
| ND 11-20 | 150 | 0.98 | 1.087 | 1.110 | −0.023 | 0.981 | **+0.106** | no |
| ND 21-30 | 150 | 0.97 | 1.037 | 1.124 | −0.087 | 0.994 | **+0.043** | yes |
| ND 31-40 | 150 | 0.95 | 0.885 | 1.101 | −0.216 | 0.980 | **−0.095** | yes |
| ND 41-64 | 354 | 0.91 | 0.929 | 1.107 | −0.178 | 0.998 | **−0.069** | yes |
| RD | 543 | 0.73 | 0.980 | 1.070 | −0.090 | 1.015 | **−0.035** | yes |
| SSP | 13 | 0.56 | 1.510 | 0.983 | +0.527 | 0.975 | **+0.535** | no |
| UNR | 44 | 0.27 | 0.620 | 1.130 | −0.510 | 1.209 | **−0.589** | no |
| IRE | 43 | 0.57 | 1.090 | 1.130 | −0.040 | 1.118 | **−0.028** | yes |
| PDA | 32 | 0.90 | 0.810 | 1.137 | −0.327 | 1.028 | **−0.218** | yes |
| PDN | 17 | 0.76 | 0.640 | 1.140 | −0.500 | 1.071 | **−0.431** | yes |
| PDS | 21 | 1.00 | 0.760 | 1.139 | −0.379 | 0.999 | **−0.239** | yes |

Mean |gap|: all 12 cells **0.246 → 0.204**; the five ND bands **0.116 → 0.075**. 9 of 12 cells improve.
The three that do not (11-20, SSP, UNR) are the two cells that were already *above* their benchmark and
the arm with the deepest red on the board.

**The natural experiment.** Grace-A cuts at entry age ≤19 — a ruled, discrete boundary. A
delivery-timing story predicts marks vary smoothly with age. The clock story predicts a discontinuity
exactly there. Classes 2005-2021, Order C's own window:

| age at draft | n | mark | fair_C | gap_C | **fair_board** | **gap_board** |
|---|---|---|---|---|---|---|
| 17 | 93 | 0.861 | 1.134 | −0.273 | 0.995 | **−0.133** |
| 18 | 1401 | 1.014 | 1.122 | −0.107 | 0.984 | **+0.030** |
| 19 | 167 | 0.954 | 1.129 | −0.176 | 0.990 | **−0.037** |
| 20 | 80 | 1.282 | 1.074 | +0.208 | 1.225 | **+0.058** |
| 21+ | 245 | 1.110 | 0.991 | +0.120 | 1.129 | **−0.019** |

Mean |gap| across the five buckets: **0.177 → 0.056**. Under `fair_C` the gap **jumps 0.384 across the
single-year step from 19 to 20** — precisely the ruled boundary, and a jump no smooth story about
delivery timing can produce. Under the board's own clock the same step is 0.095.

**This is the strongest evidence in the packet, and it is evidence for the clock, not the wedge.**

### ALT-1 — the year-one marks are simply too low

Its preregistered discriminator: the deficit should track *who sat*, and should *not* track how late a
cell delivers.

| band | mean delivery yr | sat(0g) share | gap_board |
|---|---|---|---|
| ND 1-10 | 6.22 | 0.107 | +0.064 |
| ND 11-20 | 6.49 | 0.240 | +0.106 |
| ND 21-30 | 6.35 | 0.300 | +0.043 |
| ND 31-40 | 6.21 | 0.520 | −0.095 |
| ND 41-64 | 6.68 | 0.596 | −0.069 |

- rank corr(**sat share**, gap) = **−0.800** — strongly negative, as ALT-1 predicts.
- rank corr(**mean delivery year**, gap) = **+0.300** — the *wrong sign*; the timing story needs this
  strongly negative.

### The scoreboard on the V's two features

| | the LEVEL of the yr0→1 dip | the SPREAD between bands (0.19 pts) |
|---|---|---|
| **timing wedge** (the hypothesis) | premise false (P1); bound is 2× too deep anyway | supplies ≤ 22%, wrong sign vs delivery lateness |
| **clock / benchmark** (ALT-2) | **explains most of it**; age-boundary discontinuity is decisive | uniform in pick — explains **none** |
| **year-1 marks too low** (ALT-1) | can't be separated from the clock on this evidence | **the only candidate standing**, ρ = −0.80 on sit share |

**P4, cited not recomputed** (Order C, `NOARB_34_out.txt`): forward growth from the year-1 vantage is
1.616 for picks 31-40 and 1.489 for 41-64 against carry 1.689. From year 1 onward the grace is
exhausted and the clocks agree, so that leg is benchmarked correctly and remains genuinely short —
about 4 and 12 points. That is the V's *right* arm, and nothing in this packet moves it.

---

## 6. WHERE THE EVIDENCE CANNOT TELL

1. **Clock versus year-1 marks, on the level.** Both stories predict a class-wide shortfall against
   `fair_C`. The age-boundary discontinuity discriminates them *at the boundary*; it does not prove the
   clock accounts for the whole level among ≤19s, where 96% of the population sits and the two stories
   overlap almost completely.
2. **Every thin arm.** SSP (n = 13 in the observable window), PDN (17), PDS (21), MSD (9). SSP is
   additionally a recent mechanism and right-censored, so its career-lens numbers cannot judge it —
   Order C said the same. Its +51% inversion survives *both* re-basings (gap +0.527 → +0.535) and is
   **not explained by anything in this packet.**
3. **UNR gets worse under the correction** (−0.510 → −0.589) because it is a mature-age arm and the
   correction raises its benchmark. Either the correction is wrong for that arm or UNR's entry cell is
   worse than Order C's table suggests. This seat cannot separate those.
4. **My profiles are observed-leg only.** The fit target's `total` = observed leg + projected tail; a
   live career's future seasons are absent from my profile. As stated in the prereg, this biases the
   wedge **upward, toward 1 — i.e. against the hypothesis.** The hypothesis fails by ~0.5, so the bias
   cannot be what killed it, but the exact `W_pure` values are soft.
5. **Right censoring.** The 2019 class has six visible years. The fixed-6-year-horizon column
   (`W_pure_h`, Part 4) reads 0.560-0.568 across all five bands — an even *flatter* band profile than
   the full window, so the conclusion on the spread is if anything stronger under the control.
6. **The `s1` reconstruction** matches Order C's published `fair_C` to ~0.002, but my class window is
   2005-2019 (prereg) against its 2005-2021; the age table is run on Order C's window for
   comparability.

---

## 7. RECOMMENDATION

**No entry-discount curve is proposed.** The prereg conditioned that output on support, and the
hypothesis is not supported: its premise is false on the fit code, its magnitude is off by a factor of
two, and its shape can supply at most a fifth of the spread it was meant to explain. Building a smooth
per-pick entry-discount curve now would be fitting a correction to a mechanism this seat has shown is
not there, and it would double-discount a target that is already discounted.

**Rulings-material, for the owner, in priority order:**

1. **Re-base the yr0→1 no-arb benchmark onto the board's own clock.** This is a *benchmark* change, not
   a price change — no entry cell and no board number moves. `fair = accretion(entry age) × (1 − s1)`
   with accretion 1.00 for ≤19 and 1.30 for ≥20, both read off the engine's own `disc_factor` and
   `grace_years`. Consequence, stated plainly: **most of the yr0→1 sell-side reds close by
   construction**, because they were being judged against a carry step that grace-A deliberately
   suspends. What remains after re-basing: **31-40 at −0.095 and 41-64 at −0.069** (still short, the
   V's real left arm, now about a third the size), **PDA −0.218, PDN −0.431, PDS −0.239** (the
   development-arm entry cells, which Order C already sent to the refit as an own-arm re-anchor),
   **UNR −0.589** (deepened by the correction — a live question), and **SSP +0.535** (untouched, and
   still unexplained).
2. **Settle the mature-age clock offset as a question of law, not of fit.** The 1.30 accretion for a
   ≥20 entrant is `1.14²` — one factor of no-grace and one factor of the curve clock sitting an index
   step ahead of the engine clock. The board is internally consistent either way, but a reader is
   entitled to know whether a mature-age entry cell is *meant* to sit one discount step below the
   engine's own valuation of the same seasons. If it is not, that is a genuine entry-side correction —
   **age-targeted, not pick-targeted**, and the opposite sign to the hypothesis this seat was given.
3. **Send the band spread to the year-1 machinery, not to the entry surface.** The V's spread tracks
   year-one sitting at ρ = −0.80 and delivery timing at +0.30. Order D's finding — that the ruled
   pick-curve sitter fade points the wrong way on its own evidence base — sits directly on top of this
   and should be read with it.
4. **Interaction with the entry refit, noted:** if the S5 head re-fit and the development-arm own-arm
   re-anchor both land at the next v0 refit, the re-based yr0→1 table must be regenerated after them,
   not before — the two changes move `s1` and the entry cells respectively, and the re-basing is a
   function of both.

---

*Order F, entry timing-wedge verification seat. Measured and reported; nothing wired.*
