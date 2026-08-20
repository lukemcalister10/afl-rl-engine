# PACKET P — THE BAR SHOULD SCALE WITH THE PRICE. IT DOES, IT IS MEASURABLE, AND IT ALMOST FIXES EVERYTHING.

**Seat:** ORDER P. **Date:** 2026-08-18. **Prereg:** `PREREG_P.md`, pushed at `5911796` before any
number in this packet existed.

**No board was built. No engine line was changed. Nothing is adopted and nothing lands on this seat's
word.** This is a measurement, a mechanism specification, and an offline estimate, for the owner to
rule on.

**No constant here was chosen to move any player to any value.** The named rows appear once, in §10,
wherever the derived rule puts them.

---

## 1 · THE ANSWER, IN TWELVE SENTENCES

You said the bar is the wrong object, because a top pick is priced with an expectation already inside
his price and a late pick is not.

**You were right, the effect is large, and it is measurable from outcomes.**

A player at the 90th percentile of entry price produces **16.7 points a game more above his age bar**
than a player at the 10th percentile, if he is a small. For talls it is 9.8. Those are measured on
5,041 seasons, and the confidence intervals do not come near zero.

**It holds where you need it to hold.** On rows with three career games or fewer behind them the gap
is still 11.0 points a game, 90% interval +8.3 to +13.6. So a separate bar at low games is justified
by the data, not assumed.

**When the bar scales with price, the pick axis falls out of the surplus.** The rank correlation
between draft pick and performance surplus goes from **−0.3303 against the age-only bar to +0.0249
against the pedigree-conditional bar**. That is the whole mechanism in one number.

**Your prediction is right in the primary window and wrong in the modern one.** Picks 1-10 read
**+8.62%** against your +14% rail, where ORDER N read +16.13% and ORDER K reads +8.22%. The inflation
collapses on its own, with no cap bolted on. In the modern window picks 1-10 read **+18.85%**, down
from ORDER N's +23.90% but still through the rail.

**And the late bands are now better than ORDER K, not worse.** Picks 31-40 go from −10.70% to
−8.88%; picks 41-64 from −6.89% to −5.03%. ORDER N made both of those worse.

**Every rail except that one modern cell holds.** Class mark 1.0613 on the registered basis, veteran
caps 951 / −595 inside 1,002 / 668, board −0.99% against ORDER N's −1.36%.

**The peaks are not restored.** They land 0.0% to 3.2% below ORDER K's at the same peak years —
about where ORDER N left them. The board still deflates: −0.99%, against ORDER N's −1.36%.

**The conflict is still there and it is now a hairline.** The modern rail needs LAMBDA at or above
0.596; the 1.03 class floor allows at most 0.584. ORDER N's gap was 1.20 to 1.80. This one is 0.012
wide. **I am not closing it for you.**

**On the forbidden set: this object runs the opposite way to par, and I could not find a channel that
puts pick value back on the board.** The argument, the three bounds, and the two channels I went
looking for are in §2 and §8, including the one place the honest answer is "it depends what you meant".

---

## 2 · STEP 1 — THE OLD PAR SYSTEM, HONESTLY, AND WHETHER THIS IS IT COMING BACK

You noticed this resembles the deleted par machinery. It does. Here is the comparison, plainly.

### 2.1 What `par_at(pos, pick, tenure)` actually computed

From `engine/forward_valuation/par_build.py`:

```
par(pos, pick, tenure)  =  level_pos(log-pick)  +  ramp_pos(tenure)
```

It was the median recency-weighted points per game among players **on the park** at that position and
that stage of career, fitted as a local-linear kernel regression over `log(pick)` with tricube weights
and bandwidth 0.40, on draft cohorts 2003-2018. A per-position tenure ramp was added, fitted by
additive backfitting and shrunk toward the global ramp where the position was thin.

In one sentence: **par said what a player of that draft position should be producing by now.**

### 2.2 How it entered price — and this is the part that matters

Four live sites, all on printed-price paths.

| # | site | what it did |
|---|---|---|
| 1 | `_par_prior`, blended into the level at `_merged_recover.py:339/741` | `(1 − pw)·production + pw·par`. **A high pick producing badly had his assessed LEVEL PULLED UP toward his par.** The engine comment calls it "the pedigree hump". |
| 2 | `par_pole(pos, pk, T)` | A synthetic player was created at that pick, producing exactly par, priced through the whole engine. Then: `raw_ev = pr + w·recover(perf,par)·max(0, po − pr)`. **The `max(0, ·)` makes it strictly non-negative.** It could lift a high pick toward what a pick of his number "should" be worth. It could never lower anyone. |
| 3 | the isotonic pick-tax `ISO` | Built by probing `raw_ev(synth(pk, par_at(pos,pk,4)))` across picks 1-70. A multiplicative pick-side correction on the production leg. |
| 4 | two denominators | the evidence weight `Q = clip(career avg / par, 0, 2)` and the mediocre-for-years decay gate `pr = bestlvl / par`. |

### 2.3 Why it was deleted

Your ruled forbidden set: *"pathway pedestals, par tables, prior poles (bars/aging/form legitimately
retained)."*

The seat that hit the boundary stopped rather than choosing, and priced it first
(`STOP_STEP3_FORBIDDEN_SET_BOUNDARY.md`): deleting the pole alone moved 271 rows and −19,273 board
points. Candidate 31 then executed the ruling. **The pole and the par-built ISO went. Sites 3 and 4
stayed, with their denominators re-referenced from pick-conditional par to pick-blind flat positional
bars.** ORDER C re-referenced those same two denominators again, from the flat mature bar to the AGE
bar, because S1 measured that the flat bars fail 86-100% of age-18/19 seasons even for players who
turn out fine.

**That age bar is the bar ORDER N's surplus is measured against today.** So the lineage runs
pick-conditional par → pick-blind flat bar → age bar. This order is asking whether the pedigree axis
comes back — and if so, in which direction.

### 2.4 How what is derived here DIFFERS

| | **the deleted par objects** | **this object** |
|---|---|---|
| where it sits | inside the value, as a level substitute and an additive pole | inside the CHARGE, as the bar the surplus is measured against |
| its sign on price | `max(0, po − pr)` — **strictly non-negative.** A high pick was paid for being a high pick | `T` is non-increasing in surplus. **Raising an expensive player's bar RAISES his charge and LOWERS his price** |
| what it does to a weak high pick | pulls his assessed level UP toward par | **charges him MORE, because he is further below a higher bar** |
| what it reads | the pick | the entry price, as a label for outcomes measured on players priced like him |
| the ceiling | none — the pole could add | **`v(F=0)`, the eta-zero board, which has no par object in it** |

**Measured, on the young board, the direction is exactly reversed.** Mean charge on the pedigree leg,
by pick band, over 4,143 young vantage rows:

| pick band | rows | ORDER K | ORDER N | **ORDER P** |
|---|---:|---:|---:|---:|
| 1-10 | 584 | 33.1% | 32.2% | **39.7%** |
| 11-20 | 572 | 33.3% | 43.0% | **35.2%** |
| 21-40 | 1015 | 33.1% | 49.7% | **33.0%** |
| 41-64 and pool | 1077 | 33.5% | 53.3% | **27.6%** |

**Under ORDER K the charge is flat in pick, because it only reads games. Under ORDER N it falls
hardest on the bottom of the draft. Under ORDER P it falls hardest on the top of it.** That is the
opposite of a pedestal.

### 2.5 The three bounds, asserted

- **P-F1.** `F = 1 − exp(−LAMBDA·A·T)` is in `[0, 1)` for every input, so `v = v(F=0) − F·C ≤ v(F=0)`.
  **The most any row can reach is its own uncharged price, and the uncharged board is ORDER K's own
  eta-zero board, which the forbidden set is already absent from. Asserted row by row: 0 of 9,746
  vantages price above it.**
- **P-F2.** `A(0) = 0` exactly. No day-0 print moves. The pick curve itself is untouched.
- **P-F3.** The bar reads outcomes, never prices. `v0` is the axis the outcomes are indexed by. No
  board price is added to anything.

### 2.6 The verdict, including the part where the honest answer is qualified

**I looked for two ways this could smuggle pick value back in. I named both before measuring.**

**Channel S1 — relief is proportional to the pedigree leg.** A charge that multiplies the pedigree
leg gives back more points to an expensive player than to a cheap one, for the same percentage of
relief. This is true of ORDER K's blind charge too. **Measured: it does not bind here, because ORDER P
does not give the top of the draft relief at all — it charges them more.** The rank correlation of
relief-per-unit-of-entry-price against pick is **+0.1617** (ORDER N: −0.1928). Positive means relief
flows toward LATER picks. Falsifier P10 did not fire.

**Channel S2 — an under-demanding bar.** If the production premium is shallower than the price
premium, the bar does not rise as fast as the price does and expensive players are let off. **On the
house ruler this does not fire**: at 20, a small at the 10th price percentile is expected at 59.6
points a game and one at the 90th at 76.3, and the ruler values those at 0.2 against 35.7 for a full
season — a far bigger ratio than the 9.0x price ratio. **But that ratio is unstable, because the
cheap end sits almost on the ruler's zero.** The empirical version is better behaved: the elasticity
of delivered value in the entry price, with surplus held fixed, is **+1.43**, so delivered value rises
more than proportionally with price, not less. Falsifier P11 did not fire on either reading.

**The one honest qualification.** The premium is measured on players who PLAY. A cheap player has to
be good to get a game; an expensive one plays anyway. So the measured premium is a **lower bound** on
the true talent gap, and the bar is therefore, if anything, **less demanding of expensive players than
it should be**. That cuts toward S2 rather than away from it. I have not corrected it, because
correcting it needs a construction choice this seat was not given, and #336 already fought that exact
fight over par's own survivor bias.

**So: this is not the forbidden set coming back.** It runs the other way, it cannot lift a row above a
board the forbidden set is already absent from, and measured on the board it charges the top of the
draft more, not less. **If your objection was to the pick axis existing at all anywhere on a price
path, rather than to the direction it pushed, then this object is inside your objection and you should
say so — because on that reading nothing conditional on pedigree can ever be built, including this.**

---

## 3 · THE BAR, AND HOW IT IS BUILT

One construction, used everywhere below.

```
BAR_P(v0, pos, age)  =  bar(pos, age)  +  PG(ln v0, class)
```

- `bar(pos, age)` is the engine's own `o32_gate_bar`, the S1 C3 surface, unchanged and asserted number
  by number against the engine's `O32_GATE_DELTA` literal.
- `PG` is the **pedigree premium**: how far above that age bar a player at that entry price actually
  produces. It is measured, not assumed.

**The premium, in points per game:**

| entry price v0 | SMALL (MID, SD, SF) | TALL (KPD, KPF, RUCK) |
|---:|---:|---:|
| 100 | −7.04 | −5.45 |
| 200 | −1.57 | +1.59 |
| 300 | −1.26 | +2.65 |
| 450 | −0.18 | +4.82 |
| 600 | +3.68 | +6.39 |
| 900 | +6.46 | +7.72 |
| 1200 | +7.15 | +9.41 |
| 1700 | +13.95 | +10.81 |
| 2400 | +17.77 | +12.26 |
| 3200 | +23.29 | +22.92 |

**Worked, and this is the owner's sentence written as a number.**

- A 19-year-old midfielder taken at pick 6 has an entry price near 1,660. His age bar is 57.0. His
  premium is +13.52. **His bar is 70.5 points a game.**
- A 19-year-old midfielder taken at pick 50 has an entry price near 285. His age bar is 57.0. His
  premium is −1.26. **His bar is 55.7 points a game.**
- Same age, same position, same league. **The expensive one has to produce 14.8 more points a game to
  be judged as being on track.**

**Then the surplus is the distance from that bar**, games-weighted over every season played:

```
s_P  =  SUM_s [ games_s * ( avg_s - BAR_P ) ]  /  SUM_s games_s
```

Because the premium does not depend on the season, this is exactly ORDER N's surplus minus one
per-player number:

```
s_P  =  s_N  -  PG
```

**The whole change is that the origin of the surplus scale moves, by an amount measured from
outcomes.** It is worth saying plainly so nobody reads it as more than it is.

---

## 4 · STEP 2 — THE MEASURED SURFACE

**Population.** Every season with games played, at age 18-23, by an entrant from 2005 on, in a season
up to 2025, with a position in the ruler's six groups. Force-majeure keys excluded.
**5,041 seasons over 1,575 players, 58,488 games.**

**Estimator.** Games-weighted local-linear kernel regression on `ln(v0)`, tricube, bandwidth 0.40 in
log-v0 units, fitted separately for TALL and SMALL. **This is the same estimator family `par_build.py`
used over log-pick at the same bandwidth. That was chosen deliberately, so the comparison with the
deleted object is like-for-like rather than flattering.**

### 4.1 The premium is real and it is large

| class | spread PG(v0 at p90) − PG(v0 at p10) | 90% CI | PG at the median v0 |
|---|---:|---|---:|
| **SMALL** | **+16.73** | [+13.53, +19.93] | +1.18 [−0.81, +2.96] |
| **TALL** | **+9.80** | [+5.50, +14.38] | +5.39 [+3.65, +7.07] |

v0 at p10 = 184, p50 = 485, p90 = 1,658 over the 5,041 seasons. Intervals are cluster-bootstrapped on
player, 2,000 resamples, seed 32 — ORDER N's own B and seed.

**Falsifier P4 did not fire: the premium is not zero. Falsifier P5 did not fire: it is positive.**

### 4.2 The null test that mattered — and it passes

Does pedigree still predict production when almost no games have been played? Career games counted
**before** the season being scored, so this is what was knowable at the time.

| career games before the season | rows | players | premium spread | 90% CI |
|---|---:|---:|---:|---|
| **0-3** | 1,996 | 1,574 | **+11.04** | **[+8.26, +13.62]** |
| 4-7 | 395 | 378 | +8.73 | [+0.63, +15.96] |
| 8-19 | 1,017 | 838 | +10.78 | [+7.07, +14.83] |
| 20-49 | 1,196 | 770 | +13.67 | [+10.05, +17.50] |
| 50+ | 437 | 310 | +21.88 | [+13.06, +28.59] |

**A separate bar at low games is justified by the data.** The 4-7 cell is the noisy one; its interval
only just excludes zero and it holds 395 rows. That is reported, not smoothed.

### 4.3 Where it is thin, and where the guard bit

- The support runs `v0` 91 to 3,444 for SMALL and 96 to 2,947 for TALL. **Outside that range the
  premium is HELD FLAT at the end value. It is never extrapolated.**
- The effective sample size at the cheap tail is 97 (SMALL) and **19 (TALL, printed THIN)**. At the
  expensive tail it is 193 (SMALL) and **47 (TALL, thin and outside support)**. **The TALL surface at
  both extremes is thin and I am not pretending otherwise.**
- The raw fit was non-monotone at 22 of 120 grid steps in each class. The monotonicity guard
  (`increasing=True` isotonic, the house instrument) moved the surface by at most **1.85 points a
  game**. Both the raw and the guarded surfaces are printed in `STEP2_P_out.txt`, and §9 prices the
  whole board on the raw one so you can see it makes no difference to any headline.

### 4.4 The premium is NOT flat in age, and that is a real limitation

| age | rows | premium spread |
|---|---:|---:|
| 18 | 39 | thin — not scored |
| 19 | 808 | **+8.83** |
| 20 | 1,040 | +14.27 |
| 21 | 1,102 | +16.44 |
| 22 | 1,072 | +17.29 |
| 23 | 980 | **+19.60** |

**Pedigree buys about nine points a game of expected production at 19 and about twenty at 23.** The
primary bar pools ages, as preregistered, because the age-18 cell holds 39 rows in total and the
age-19 TALL cell holds 169. **So the pooled bar is harder on a 19-year-old high pick than his own age
slice says, and softer on a 23-year-old one.** §9 prices the age-carrying bar in full.

### 4.5 The slope did not change. Only the origin did.

`BETA` is the proportional change in subsequent delivered value per one point per game of surplus,
with the entry price held fixed, on the house S4 ruler over 4,143 vantage rows and 1,415 players —
ORDER N's exact population, so the two are comparable line by line.

| career games | rows | **BETA_P** (pedigree bar) | 90% CI | BETA_N (age bar), same rows |
|---|---:|---:|---|---:|
| 1-3 | 776 | +0.01574 | [+0.00513, +0.02641] | +0.01764 |
| 4-7 | 613 | +0.04451 | [+0.03031, +0.05831] | +0.04518 |
| 8-12 | 629 | +0.06731 | [+0.05083, +0.08463] | +0.06962 |
| 13-17 | 465 | +0.10378 | [+0.08535, +0.12088] | +0.10419 |
| 18-24 | 517 | +0.10424 | [+0.08811, +0.11997] | +0.10414 |
| 25-39 | 625 | +0.11166 | [+0.09612, +0.12744] | +0.11146 |
| 40-60 | 518 | +0.10704 | [+0.09120, +0.12187] | +0.10817 |

**The two columns are nearly identical, and the prereg predicted that before the run.** At a fixed
entry price the two surpluses differ by a constant, so a regression that already controls the entry
price sees the same slope. **The honest reading is that ORDER N measured the slope correctly and your
correction is about where zero sits on the scale, not about how steep it is.** Falsifier P6 did not
fire: the slope is positive and significant at every games level, including two games.

### 4.6 The one number the whole order turns on

Spearman(draft pick, performance surplus) over 3,248 ND vantage rows:

| | |
|---|---:|
| ORDER N, surplus against the AGE bar | **−0.3303** |
| **ORDER P, surplus against the PEDIGREE bar** | **+0.0249** |

| pick band | rows | median s_N | **median s_P** |
|---|---:|---:|---:|
| 1-10 | 584 | +6.12 | **−7.34** |
| 11-20 | 572 | +0.63 | **−6.79** |
| 21-40 | 1,015 | −4.78 | **−7.73** |
| 41-64 and pool | 1,077 | −8.01 | **−6.19** |

**The pick axis is gone from the surplus.** That is the whole of the owner's insight, measured, before
a single price is computed.

---

## 5 · STEP 3 — THE DERIVED CHARGE

### 5.1 The form

```
pi  *=  exp( -LAMBDA * A(g) * T(s_P) )      below age 24
        the current charge                  at 24 and above

A(g) = 1 - exp(-g / G0)                            how much evidence g games is
T(s) = clip( 1 - THETA_R * (s - s0), 0, TMAX )     what the evidence says
```

**The FORM is ORDER N's.** It was derived there and it is not re-litigated here. What this order
changes is `s`.

**The age gate at 24 is ORDER N's too**, and for the reason ORDER N measured: `A(g)` saturates at 1,
so an ungated charge makes a 141-game row pay about half his pedigree leg where today he pays 0.1%,
and that breaks the veteran caps at every level of LAMBDA. The engine's own cap law says the age bar
is flat from 24, so "performance against expectation" has content below 24 and none at or above it.

### 5.2 Every constant, and where it comes from

| constant | value | 90% CI | derived from | ORDER N |
|---|---:|---|---|---:|
| **G0** | **9.89 games** | [7.60, 12.98] | the BETA_P curve of §4.5, fitted as `BETA_sat·(1 − exp(−g/G0))`, weighted by each bin's own inverse variance | 9.72 |
| **BETA_sat** | **0.11465** | [0.10416, 0.12718] | the same fit | 0.11521 |
| **LAMBDA × THETA_R** | **= BETA_sat** | — | so the delivered slope `d ln(retained pedigree)/ds = LAMBDA·A(g)·THETA_R` **equals the measured slope**, at every level of surplus | same rule |
| **s0** | **−2.4527** | — | the games-weighted mean of the new surplus. `T(s0) = 1` | +2.3163 |
| **TMAX** | **21.12** | — | `T` at the cohort's own 5th percentile of the new surplus, −33.06 | 5.998 |
| **LAMBDA** | **0.17438** | — | **solved**, not chosen: bisection, so the derived charge removes exactly the same total points from the year-1 class-mark population as the current charge does (101,402.7 matrix points, matched to the last decimal) | 0.82131 |
| **THETA_R** | **0.65744** | — | `= BETA_sat / LAMBDA`. Not free | 0.14028 |

**There is no free parameter.** Weighted SSE of the `A(g)` fit is 3.33 over seven bins with two
parameters.

### 5.3 What the charge does

Percentage of the pedigree leg removed, at age 19.

| career games | **current, blind** | s_P = −25 | s_P = −10 | s_P = 0 | s_P = +10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 16.8% | 39.7% | 17.3% | 0.0% | 0.0% |
| 5 | 34.0% | 66.5% | 33.8% | 0.0% | 0.0% |
| 10 | 47.5% | 82.7% | 48.4% | 0.0% | 0.0% |
| 14 | 50.0% | 87.6% | 54.5% | 0.0% | 0.0% |
| **17** | **49.0%** | 89.6% | 57.4% | 0.0% | 0.0% |
| 20 | 46.5% | 90.9% | 59.4% | 0.0% | 0.0% |
| 30 | 34.2% | 92.8% | 62.8% | 0.0% | 0.0% |
| **36** | **26.7%** | 93.2% | 63.7% | 0.0% | 0.0% |
| 50 | 13.6% | 93.6% | 64.4% | 0.0% | 0.0% |

**Read the 17-game row against the 36-game row in the current column.** The blind charge falls from
49.0% to 26.7% — a 36-game player keeps more unearned pedigree than a 17-game player. The derived
charge does not fall anywhere. That defect, which ORDER N found and you agreed with, is fixed here
too, because `A(g)` never falls.

**The zero point.** `T` hits zero at `s_P = −0.93`. **A young player producing within about one point
a game of what a player at his price normally produces, at his age, pays nothing on his pedigree
leg.** He keeps the whole prior. **32.0% of the young cohort is at or past that point**, against
18.5% under ORDER N.

**One consequence of that, stated because it is a design fact and not a detail.** LAMBDA came out low
and THETA_R came out high, so the charge is more like a switch than a dial: 32.0% pay nothing, 1.9%
pay more than 90%, and the median row pays 28.5%. Under ORDER N those numbers were 18.5%, 6.0% and
53.6%; under ORDER K, 0.0%, 0.0% and 35.5%.

### 5.4 The structural properties

| property | result |
|---|---|
| **P-S1** `A(0) = 0` exactly, so `pi(0) = D` and no day-0 print moves | PASS |
| **P-S2** `A` non-decreasing in `g` over [0, 400] | PASS |
| **P-S3** `T` non-increasing in `s` | PASS — structural, a clipped decreasing line |
| **P-S4** the factor is in (0, 1] for every input | PASS — structural, it is an exponential |
| **P-S5** no row prices above its own uncharged price | **PASS — 0 of 9,746 vantages** |

---

## 6 · STEP 4 — WHAT IT DOES. ESTIMATES PENDING A BUILD.

The pricing identity is ORDER N's, re-asserted here on this tree: rebuilding ORDER K from the
eta-zero board through the identity at eta 0.50 reproduces it with **worst relative error 1.88e-16
over 9,746 vantages**, and **0 charge bases have the wrong sign**. Falsifier P1 did not fire.

### 6.1 The owner's prediction, tested

**Share of each pick band earning FULL relief — the number your insight was about:**

| pick band | rows | ORDER N | **ORDER P** |
|---|---:|---:|---:|
| **1-10** | 584 | **41.3%** | **28.8%** |
| 11-20 | 572 | 26.4% | 31.8% |
| 21-40 | 1,015 | 15.7% | 30.5% |
| **41-64 and pool** | 1,077 | **12.6%** | **33.2%** |

*(The bottom band here is pick 41-64 **and pool rows together**, which is why the ORDER N column reads
12.6% where `PACKET_N` §8.3 reads 12.5% on picks 41-64 alone. Same rows, one wider bucket.)*

**Under ORDER N a top-ten row was 3.3 times as likely to earn full relief as a pick 41-64 row. Under
ORDER P it is slightly LESS likely.** The spread across bands is 28.8 to 33.2, which is flat within
sampling noise.

**And the relief itself:**

| pick band | mean relief per unit of entry price, ORDER N | **ORDER P** |
|---|---:|---:|
| 1-10 | **+0.0137** | **−0.0202** |
| 11-20 | −0.0372 | −0.0007 |
| 21-40 | −0.0675 | +0.0090 |
| 41-64 and pool | −0.0740 | **+0.0431** |

Negative means the row pays MORE than under ORDER K. **ORDER N gave the top of the draft money and
took it from the bottom. ORDER P does the reverse.** Spearman(pick, relief) goes from −0.1928 to
**+0.1617**. Falsifier P10 did not fire.

### 6.2 The property test, re-run

Rank correlation within games bins, each order read against the surplus it actually uses.

| games bin | n | price response ORDER K | **price response ORDER P** | charge ORDER K | **charge ORDER P** |
|---|---:|---:|---:|---:|---:|
| 1-4 | 42 | +0.135 | **+0.459** | +0.099 | **−0.840** |
| 5-9 | 33 | +0.261 | **+0.677** | +0.442 | **−0.971** |
| 10-15 | 33 | +0.435 | **+0.650** | +0.226 | **−0.989** |
| 16-24 | 36 | +0.707 | **+0.900** | +0.120 | **−0.990** |
| 25-39 | 29 | +0.787 | **+0.871** | −0.156 | **−0.992** |
| 40-60 | 22 | +0.538 | **+0.891** | −0.436 | **−0.936** |

**The charge is now monotone in surplus at every games level, and the price response is strongest
exactly where ORDER K was weakest.** At 1-4 games it goes from +0.135, an interval that straddled
zero, to +0.459.

Charge paid by surplus tercile over the 195-row young board:

| group | n | mean s_P | mean games | ORDER K | **ORDER P** |
|---|---:|---:|---:|---:|---:|
| below expectation | 65 | −24.65 | 11.2 | 34.5% | **67.5%** |
| middle | 65 | −9.81 | 17.6 | 37.8% | 47.1% |
| **above expectation** | 65 | **+4.78** | 23.7 | 31.5% | **4.4%** |

### 6.3 The band tables. BOTH WINDOWS.

Year-0 to year-1 appreciation. **B** = over the +14% buy rail. **S** = below 0%, sell side. All three
boards through the same committed instrument, `t338_extended_DISCLOSED.py`, md5-asserted.

#### PRIMARY window — cohorts 2005-2023

| band | n | ORDER K | ORDER N | **ORDER P** | P − K |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 1200 | +4.23% | +5.94% | **+5.33%** | +1.10 |
| picks 1-20 | 380 | +9.22% | +13.85% | **+9.79%** | +0.57 |
| picks 21-64 | 820 | −3.67% **S** | −6.58% **S** | **−1.73% S** | +1.94 |
| **picks 1-10** | 190 | +8.22% | **+16.13% B** | **+8.62%** | +0.40 |
| picks 11-20 | 190 | +11.16% | +9.44% | **+12.07%** | +0.91 |
| picks 21-30 | 190 | +5.26% | +2.17% | **+7.38%** | +2.12 |
| **picks 31-40** | 190 | −10.70% **S** | −13.17% **S** | **−8.88% S** | **+1.82** |
| **picks 41-64** | 440 | −6.89% **S** | −9.99% **S** | **−5.03% S** | **+1.86** |

#### MODERN window — cohorts 2019-2023

| band | n | ORDER K | ORDER N | **ORDER P** | P − K |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 311 | −0.96% **S** | +1.33% | **+1.45%** | +2.41 |
| picks 1-20 | 100 | +9.58% | +15.37% **B** | **+12.88%** | +3.30 |
| picks 21-64 | 211 | −17.97% **S** | −21.33% **S** | **−17.01% S** | +0.96 |
| **picks 1-10** | 50 | +13.65% | **+23.90% B** | **+18.85% B** | +5.20 |
| picks 11-20 | 50 | +2.11% | −0.26% **S** | **+1.94%** | −0.17 |
| picks 21-30 | 50 | −14.26% **S** | −18.09% **S** | **−13.84% S** | +0.42 |
| picks 31-40 | 50 | −14.27% **S** | −15.44% **S** | **−11.73% S** | +2.54 |
| picks 41-64 | 111 | −25.06% **S** | −29.81% **S** | **−24.88% S** | +0.18 |

**Three things to read.**

**One. Picks 1-10 primary reads +8.62%, forty basis points above ORDER K, with the whole property fix
in place.** ORDER N read +16.13%. **The inflation collapses on its own, exactly as you predicted, with
no cap bolted on.**

**Two. Falsifier P12 did not fire. Every late band is BETTER than ORDER K, in both windows.** That was
the other half of your complaint about ORDER N, and it is fixed. Picks 31-40 primary −10.70% →
−8.88%. Picks 41-64 primary −6.89% → −5.03%.

**Three. Modern picks 1-10 reads +18.85% and that is still through your rail.** It is 5.05 points
better than ORDER N and 5.20 points worse than ORDER K. That cell carries **50 rows**. §8 is about it.

### 6.4 The peaks, which you asked for specifically

The maximum of each band's year-0-to-7 path and the year it falls in.

#### PRIMARY

| band | ORDER K | ORDER N | **ORDER P** | **P vs K** | N vs K |
|---|---|---|---|---:|---:|
| ALL picks 1-64 | 1.532 at yr5 | 1.492 at yr5 | **1.501 at yr5** | **−2.01%** | −2.59% |
| picks 1-20 | 1.566 at yr5 | 1.530 at yr5 | **1.527 at yr5** | **−2.47%** | −2.27% |
| picks 21-64 | 1.510 at yr6 | 1.507 at yr6 | **1.509 at yr6** | **−0.01%** | −0.14% |
| picks 1-10 | 1.552 at yr4 | 1.524 at yr4 | **1.502 at yr4** | **−3.22%** | −1.82% |
| picks 11-20 | 1.660 at yr5 | 1.607 at yr5 | **1.620 at yr5** | **−2.43%** | −3.21% |
| picks 21-30 | 1.686 at yr6 | 1.684 at yr6 | **1.686 at yr6** | **+0.01%** | −0.08% |
| picks 31-40 | 1.403 at yr5 | 1.355 at yr5 | **1.384 at yr5** | **−1.31%** | −3.37% |
| picks 41-64 | 1.512 at yr6 | 1.511 at yr6 | **1.513 at yr6** | **+0.07%** | −0.07% |

#### MODERN

| band | ORDER K | ORDER N | **ORDER P** | **P vs K** | N vs K |
|---|---|---|---|---:|---:|
| ALL picks 1-64 | 1.376 at yr5 | 1.327 at yr5 | **1.335 at yr5** | **−2.97%** | −3.54% |
| picks 1-20 | 1.578 at yr5 | 1.548 at yr7 | **1.548 at yr7** | **−1.90%** | −1.90% |
| picks 1-10 | 1.667 at yr5 | 1.644 at yr5 | **1.639 at yr5** | **−1.65%** | −1.35% |
| picks 11-20 | 1.442 at yr7 | 1.442 at yr7 | **1.442 at yr7** | **0.00%** | 0.00% |
| picks 21-30 | 1.361 at yr6 | 1.361 at yr6 | **1.361 at yr6** | **0.00%** | 0.00% |
| picks 31-40 | 1.539 at yr5 | 1.491 at yr5 | **1.507 at yr5** | **−2.08%** | −3.15% |
| picks 41-64 | 1.000 at yr0 | 1.000 at yr0 | **1.000 at yr0** | **0.00%** | 0.00% |

**The honest answer to your question: no, this construction does not restore the peaks.** They land
0.0% to 3.2% below ORDER K's, at exactly the same peak years, which is the same band ORDER N landed
in. It is better than ORDER N in five of the eight primary bands and worse in three, and the worst
single cell is picks 1-10 primary at −3.22% against ORDER N's −1.82%.

**The board still deflates, and by less than ORDER N: −0.99% against −1.36%.** Board total
**673,097 → 666,450**. 288 of 804 rows move: 133 up, 155 down.

**Why the peaks do not come back, stated plainly.** The anchoring identity pins the total points the
charge removes from the year-1 population. It does not pin what happens at year 4 or 5. `A(g)` never
falls, so a row with 30 or 50 games keeps paying where the blind charge had already let him off, and
the peak years are exactly where those rows sit. **Restoring the peaks would need the charge to fall
back with games — which is the defect you asked ORDER N to remove.** The two cannot both be had from
this family of shapes, and I am not going to pretend otherwise.

### 6.5 The class mark

| board | W2 scorer, draft classes 2005-2015 (the registered basis) | vs the 1.03 floor | vs the 1.14 buy rail | cohort clock |
|---|---:|---:|---:|---:|
| **ORDER P** | **1.0613** | +0.0313 | −0.0787 **PASS** | 1.0322 |
| ORDER N | 1.0604 | +0.0304 | −0.0796 PASS | 1.0324 |
| ORDER K | 1.0513 | +0.0213 | −0.0887 PASS | 1.0324 |
| landing candidate | 1.0421 | +0.0121 | −0.0979 PASS | 1.0232 |
| eta = 0 | 1.2046 | +0.1746 | **+0.0646 FAIL** | 1.1829 |

The cohort mark comes in at 1.0322 against ORDER K's 1.0324. The two-ten-thousandths gap is the
rounding of the value path to one decimal; the anchoring identity itself matched to the last decimal
(101,402.7 points against 101,402.7).

### 6.6 The veteran caps, and where the money moves

| | rows | churn | rail | net | rail | verdict |
|---|---:|---:|---:|---:|---:|---|
| **ORDER P** | 130 | **951** | 1,002 | **−595** | ±668 | **INSIDE BOTH** |
| ORDER N | 130 | 951 | 1,002 | −595 | ±668 | inside both |
| ORDER K | — | 947 | 1,002 | −601 | ±668 | inside both |

| age in 2026 | rows | total points |
|---|---:|---:|
| 20 and under | 158 | −887 |
| **21-23** | 217 | **−5,759** |
| **24 and over** | 429 | **−1** |

The 24-and-over line is the age gate holding: 429 mature rows move one point between them.

| career games | rows | total points | per row |
|---|---:|---:|---:|
| 0 | 89 | −7 | −0.1 |
| 1-4 | 46 | −1,108 | −24.1 |
| 5-9 | 45 | −862 | −19.2 |
| 10-15 | 51 | +867 | +17.0 |
| 16-29 | 81 | −1,385 | −17.1 |
| 30-59 | 103 | −3,035 | −29.5 |
| 60+ | 388 | −1,124 | −2.9 |

*(The 0-games line reads −7 rather than exactly 0 because the offline arithmetic rounds each value to
one decimal and then converts to board points. `A(0) = 0` holds exactly in the mechanism and no
gameless row is charged anything; the seven points are rounding, and they are disclosed rather than
hidden.)*

### 6.7 The pool arms, which ORDER N left owed

Year-0 to year-1, through the committed pool-arm instrument, both windows.

| arm | n (primary) | ORDER K | ORDER N | **ORDER P** |
|---|---:|---:|---:|---:|
| RD | 623 | −3.39% | −5.55% | **−1.86%** |
| UNR | 49 | −42.91% | −43.67% | **−43.12%** |
| IRE | 47 | +13.34% | +10.76% | **+13.62%** |
| PDA | 43 | −20.70% | −23.11% | **−20.25%** |
| PDN | 33 | −40.32% | −41.51% | **−40.78%** |
| **SSP** | 31 | **+52.71%** | +53.91% | **+58.17%** |
| PDS | 21 | −27.70% | −27.56% | **−26.15%** |
| **ALLPOOL** | 1016 | −4.93% | −6.91% | **−3.60%** |

**ORDER P is closer to ORDER K than ORDER N is on every arm, and better on most.** The whole pool
book reads −3.60% against ORDER K's −4.93%, so the sell-side pressure on the pool eases.

**One arm to watch: SSP.** It is already BUY-RED under ORDER K at +52.71% and ORDER P pushes it to
+58.17%, the largest single arm move in the order. Those 31 rows are cheap mid-season signings whose
entry prices are low, so their pedigree bar is low and they clear it easily. **That is the mechanism
working as designed, on an arm that was already over the rail before this order touched it.** It is
flagged, not fixed, because fixing it is a separate ruling.

---

## 7 · THE SENSITIVITIES. THE HEADLINE IS NOT A SMOOTHING CHOICE.

Each row below **re-estimates the surface from scratch, re-solves LAMBDA by the anchoring identity,
and re-prices the whole board.** Nothing is carried across.

| surface | LAMBDA | picks 1-10 PRI | picks 1-10 MOD | picks 31-40 | picks 41-64 | W2 mark | rho(pick, surplus) |
|---|---:|---:|---:|---:|---:|---:|---:|
| ln(v0), H = 0.25, guarded | 0.1523 | +8.80% | +18.98% | −8.86% | −5.06% | 1.0613 | +0.053 |
| **ln(v0), H = 0.40, guarded (primary)** | **0.1600** | **+8.57%** | **+18.80%** | **−8.87%** | **−5.03%** | **1.0611** | **+0.056** |
| ln(v0), H = 0.60, guarded | 0.1585 | +8.51% | +18.88% | −8.88% | −5.04% | 1.0608 | +0.051 |
| ln(v0), H = 0.40, **monotonicity guard OFF** | 0.1667 | +8.64% | +18.82% | −8.84% | −5.01% | 1.0612 | +0.058 |
| **pick band instead of v0** | 0.3405 | +9.07% | +17.92% | −10.09% | −5.44% | 1.0604 | +0.026 |
| **no premium at all (= ORDER N)** | 0.8092 | **+16.01%** | **+23.72%** | −13.15% | −9.96% | 1.0602 | **−0.309** |

**Read the last row first.** It is a control: set the premium to zero and the whole pipeline
reproduces ORDER N — LAMBDA 0.809 against ORDER N's 0.821, picks 1-10 +16.01% against +16.13%,
rho −0.309 against −0.330. **The machinery is doing what it is supposed to be doing.**

**Then read the first five.** Every variation of the surface — bandwidth up, bandwidth down, guard
off, and the pick axis this order deliberately did not choose — lands picks 1-10 primary between
+8.5% and +9.1% and the class mark between 1.0604 and 1.0613. **The result is a property of the data,
not of a smoothing choice.**

*(This file re-implements the anchoring solve independently and lands LAMBDA 0.1600 where `op_step4.py`
lands 0.17438, because it recomputes `s0` over the vantage rows whose year is on the value path rather
than over all Step 2 rows. The headline moves by 0.05 percentage points. Both are printed and neither
is hidden.)*

### 7.1 The age-carrying bar, priced in full

§4.4 measured that the premium is not flat in age. This variant carries the age axis, pools ages 18
and 19 because the 18 cell holds 39 rows, and re-solves LAMBDA from scratch.

| | pooled bar (the proposal) | age-carrying bar | ORDER K |
|---|---:|---:|---:|
| LAMBDA | 0.174 | **0.523** | — |
| picks 1-10 PRIMARY | **+8.62%** | +11.36% | +8.22% |
| picks 1-10 MODERN | **+18.85%** | +21.51% | +13.65% |
| picks 31-40 PRIMARY | **−8.88%** | −10.33% | −10.70% |
| picks 41-64 PRIMARY | **−5.03%** | −6.25% | −6.89% |
| W2 class mark | **1.0613** | 1.0617 | 1.0513 |

**The age-carrying bar is worse on every rail.** It reads the true 19-year-old premium of about nine
points rather than the pooled sixteen, so young high picks are measured against a lower bar and get
more relief, and picks 1-10 rises. **The pooled bar was fixed as primary in the prereg before any of
these numbers existed, and it happens to be the better of the two. I am printing both so you can see
that I did not pick it after the fact.**

---

## 8 · THE CONFLICT, QUANTIFIED. I AM NOT PICKING FOR YOU.

### 8.1 The gap is now a hairline, and it is still a gap

`LAMBDA` is the level. `THETA_R = BETA_sat / LAMBDA` is the tilt. Raising the level cools the board
and weakens the tilt.

| LAMBDA | THETA_R | zero point | W2 class mark | picks 1-10 PRI | picks 1-10 MOD | ALL PRI | ALL MOD |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **0.174** | 0.6574 | −0.93 | **1.0613** | **+8.62%** | **+18.85%** | +5.33% | +1.45% |
| 0.300 | 0.3822 | +0.16 | 1.0516 | +6.98% | +17.38% | +4.19% | +0.40% |
| 0.400 | 0.2866 | +1.04 | 1.0439 | +5.71% | +16.24% | +3.29% | −0.45% |
| 0.500 | 0.2293 | +1.91 | 1.0364 | +4.48% | +15.10% | +2.40% | −1.30% |
| **0.600** | 0.1911 | +2.78 | **1.0288 — floor broken** | +3.21% | **+13.96% — rail met** | +1.50% | −2.15% |
| 0.700 | 0.1638 | +3.65 | 1.0214 | +1.99% | +12.88% | +0.62% | −2.97% |

| what needs to be true | the LAMBDA it needs |
|---|---|
| picks 1-10 under +14% in the **PRIMARY** window | **every LAMBDA on the ladder, including the solved one** |
| picks 1-10 under +14% in the **MODERN** window | **LAMBDA at or above 0.596** |
| the G1 floor, W2 class mark at or above 1.03 | **LAMBDA at or below 0.584** |
| the veteran caps | **every LAMBDA on the ladder** |

**The gap is LAMBDA 0.584 to 0.596. It is 0.012 wide.**

**ORDER N's gap was 1.20 to 1.80 — fifty times wider.** The pedigree-conditional bar did not close the
conflict, but it nearly did, and it closed the primary window outright.

### 8.2 What the gap is actually made of

It is one cell with fifty rows in it. The modern picks 1-10 band had almost no headroom before this
order: ORDER K sits at +13.65% against a +14% rail, which is 0.35 of a point of slack. ORDER M wrote
it down in its own words: *"anything that lifts the top of the draft has less headroom than the
primary table suggests."*

**But ORDER P is not lifting the top of the draft.** It charges picks 1-10 more than ORDER K does
(39.7% against 33.1% of the pedigree leg, §2.4), and their primary-window band reads +0.40 of a point
above ORDER K. **The modern cell moves +5.20 points anyway, and the reason is not the tilt — it is the
level.** LAMBDA solved to 0.174 rather than ORDER K's effective 0.50, because the derived charge with
a saturating `A(g)` collects the same total from the class-mark population at a much lower LAMBDA. The
modern top-ten rows are young, high-games and near their bars, so they sit in the part of the curve
where the lower level shows up most.

**Two readings, both yours to make, neither of them mine:**

- **The modern window is 50 rows and the primary window is 190.** If the modern cell is not binding,
  every rail in this order holds at the solved LAMBDA and there is nothing left to decide.
- **If the modern cell is binding**, then LAMBDA between 0.584 and 0.596 is what the rails jointly
  require and nothing sits there. Moving 0.012 of a point in either direction breaks one of them by a
  little: at 0.584 the modern cell reads about +14.1%; at 0.596 the class mark reads about 1.029.
  **Both breaches are inside a tenth of a point of the rail they break. I will not decide which
  tenth of a point matters more.**

### 8.3 The other conflicts, named

- **The peaks are not restored (§6.4).** They cannot be, inside a charge that is monotone in evidence.
  Monotonicity in evidence was the thing ORDER N fixed and you agreed with. **You cannot have both
  from this shape family, and this is the trade, priced.**
- **The premium is not flat in age (§4.4, §7.1), and the primary bar pools it.** The pooled bar is
  harder on 19-year-old high picks than their own age slice justifies. The age-carrying bar is worse
  on every rail. **Both are printed. Neither is chosen for you.**
- **The measured premium is a lower bound.** It is estimated on players who play. That means the bar
  is, if anything, less demanding of expensive players than the truth. It is the same survivor-bias
  problem #336 fought over par, and it is not repaired here.
- **The TALL surface is thin at both ends.** ESS 19 at the cheap tail and 47 at the expensive one. The
  premium there is held flat at the end of support. **Talls are also where §4.4 of ORDER N found early
  production carries the least information, so this order is doing the least work exactly where it is
  least sure. That is reported, not corrected.**

---

## 9 · WHAT THE THREE COLUMNS LOOK LIKE, SIDE BY SIDE

| | ORDER K `f3101883` | ORDER N derived | **ORDER P derived** |
|---|---:|---:|---:|
| the bar the surplus is measured against | — | age only | **age + pedigree premium** |
| Spearman(pick, surplus) | — | −0.3303 | **+0.0249** |
| share of picks 1-10 earning full relief | — | 41.3% | **28.8%** |
| share of picks 41-64 earning full relief | — | 12.6% | **33.2%** |
| mean charge, picks 1-10 | 33.1% | 32.2% | **39.7%** |
| mean charge, picks 41-64 and pool | 33.5% | 53.3% | **27.6%** |
| picks 1-10 PRIMARY | +8.22% | +16.13% **B** | **+8.62%** |
| picks 1-10 MODERN | +13.65% | +23.90% **B** | **+18.85% B** |
| picks 31-40 PRIMARY | −10.70% | −13.17% | **−8.88%** |
| picks 41-64 PRIMARY | −6.89% | −9.99% | **−5.03%** |
| ALL 1-64 MODERN | −0.96% **S** | +1.33% | **+1.45%** |
| W2 class mark | 1.0513 | 1.0604 | **1.0613** |
| cohort class mark | 1.0324 | 1.0324 | **1.0322** |
| veteran churn / net | 947 / −601 | 951 / −595 | **951 / −595** |
| board total | 673,097 | 663,917 (−1.36%) | **666,450 (−0.99%)** |
| ALLPOOL PRIMARY | −4.93% | −6.91% | **−3.60%** |

---

## 10 · THE ILLUSTRATION ROWS — CONSEQUENCES, NEVER TARGETS

**Not one constant in this mechanism was chosen with any of these rows in view.** They are printed
last because you asked to see them, and they are printed wherever the derived rule puts them. If one
of them is in the wrong place, that is a finding about the rule.

| row | age | pick | games | v0 | s vs AGE bar | premium | **s vs PEDIGREE bar** | chg K | chg N | **chg P** | ORDER K | ORDER N | **ORDER P** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Harry Dean | 19 | 3 | 17 | 2438 | +14.86 | +12.95 | **+1.91** | 49.0% | 0.0% | **0.0%** | 2403 | 3069 | **3069** |
| Cooper Duff-Tytler | 19 | 4 | 13 | 1858 | +7.06 | +10.81 | **−3.75** | 49.9% | 18.4% | **21.1%** | 1505 | 1854 | **1824** |
| Xavier Taylor | 19 | 11 | 2 | 1355 | −13.22 | +9.23 | **−22.45** | 16.8% | 38.5% | **36.3%** | 1162 | 927 | **950** |
| Daniel Annable | 19 | 6 | 2 | 1661 | −19.02 | +13.54 | **−32.56** | 16.8% | 45.7% | **48.5%** | 1537 | 1153 | **1115** |
| Dylan Patterson | 19 | 5 | 5 | 1679 | −19.62 | +13.73 | **−33.35** | 34.0% | 74.0% | **76.8%** | 1440 | 987 | **955** |
| Isaac Kako | 20 | 13 | 36 | 938 | +0.84 | +6.53 | **−5.70** | 26.7% | 62.0% | **41.3%** | 832 | 716 | **784** |
| Josh Smillie | 20 | 7 | 0 | 1660 | n/a | n/a | **n/a** | 0.0% | 0.0% | **0.0%** | 772 | 772 | **772** |
| Milan Murdock | 26 | pool | 17 | 131 | +2.17 | −7.04 | **+9.21** | 49.0% | 49.0% | **49.0% — age gated** | 156 | 156 | **156** |

**What the rule did, row by row, and none of it was aimed.**

- **Dean** is 14.9 points a game above his age bar. His entry price is 2,438, so 13.0 of those points
  are what a player at his price is expected to produce anyway. **He is still +1.9 past his own bar,
  which is past the zero point, so he pays nothing and keeps his whole pedigree leg.** He lands on
  exactly the same number as ORDER N, by a different route.
- **Duff-Tytler** is +7.1 above his age bar, but his price expects +10.8, so against his own bar he is
  −3.8. He pays 21.1% rather than ORDER K's 49.9%. **The pedigree bar costs him 30 points against
  ORDER N and he still rises 319 against ORDER K.**
- **Taylor, Annable and Patterson** are 13 to 20 points a game below their age bars and 22 to 33 below
  their pedigree bars, because all three are expensive. They pay 36.3%, 48.5% and 76.8%. **All three
  fall.**
- **Kako** is the one worth reading. He is at his age bar with 36 games — the most evidence here. His
  price is 938, which expects +6.5, so he is −5.7 against his own bar. He pays 41.3%. **Under ORDER N
  he paid 62.0%, because ORDER N judged him against a bar that ignored his being pick 13 rather than
  pick 3.** Under ORDER K he pays 26.7% — less than Dean's 49.0% — because 36 games sits on the far
  side of the blind bump. That inversion is the defect both orders remove.
- **Smillie** has never played. `A(0) = 0`, so he cannot move. 772 on every board in this order.
- **Murdock** is 26. The age gate leaves him on the existing charge and he does not move.

### 10.1 The matched pair, which is your point on two real rows

Chosen on two conditions only: within 1.5 points a game of each other against the **same age bar**,
and within 4 career games of each other. Nothing else.

| row | age | pick | games | v0 | s vs AGE bar | premium | **s vs PEDIGREE bar** | charge ORDER K | **charge ORDER P** | ORDER K | **ORDER P** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Zeke Uwland** | 19 | 2 | 17 | 2583 | **−1.64** | +19.22 | **−20.86** | **49.0%** | **84.7%** | 1949 | **1486** |
| **Cooper Harvey** | 22 | 56 | 17 | 265 | **−1.80** | −1.26 | **−0.54** | **49.0%** | **0.0%** | 331 | **373** |

**Read it slowly.** Both have played 17 games. Both are producing about 1.7 points a game below what
is normal for their age in their position. **Under ORDER K they pay the identical charge, 49.0%, to
the last decimal, because the charge only reads games.**

Uwland was pick 2 and costs 2,583. A player at that price is expected to be 19.2 points a game clear
of the age bar. He is 1.6 below it. **Against what is priced into him he is 20.9 points a game short,
and he pays 84.7%.**

Harvey was pick 56 and costs 265. A player at that price is expected to be 1.3 points a game below the
age bar. He is 1.8 below it. **Against what is priced into him he is half a point short, and he pays
nothing.**

**Same production for their age. Same games. Opposite verdicts, because they were priced
differently to begin with.** That is your sentence, on two rows nobody chose.

Two more pairs, same rule, in `NAMED_P_out.txt`: Jhye Clark (pick 8, 33 games, −16.9 vs his age bar,
96.2% under ORDER P) against Arthur Jones (pick 43, 34 games, −17.1, 80.8%); and Samuel Grlj (pick 8,
19 games) against Harvey again.

---

## 11 · THE FALSIFIER SCORECARD

| # | falsifier | fired? |
|---|---|---|
| **P1** | the offline pricing identity fails | **no** — worst relative error 1.88e-16 over 9,746 vantages, 0 wrong-signed charge bases |
| **P2** | the age bar does not reproduce the engine's own | **no** — asserted number by number against `O32_GATE_DELTA` |
| **P3** | the delivered-value ruler moved | **no** — md5 `241842f6…` on both copies |
| **P4** | the pedigree premium is not distinguishable from zero, overall or at low games | **no** — +16.73 [+13.53, +19.93] SMALL, +9.80 [+5.50, +14.38] TALL, and +11.04 [+8.26, +13.62] on rows with three games or fewer behind them |
| **P5** | the premium is negative | **no** — positive at every level of price |
| **P6** | BETA on the new surplus is not distinguishable from zero | **no** — positive and significant at every games level, including 1-3 games |
| **P7** | no LAMBDA reproduces the current aggregate charge | **no** — 0.17438, matched to the last decimal |
| **P8** | a structural property fails | **no** — P-S1 to P-S5 all hold; P-S5 asserted on all 9,746 vantages |
| **P9** | **picks 1-10 still breaks the +14% rail in the PRIMARY window** | **no — +8.62%.** The owner's prediction is confirmed in the window it was preregistered on. **In the MODERN window it reads +18.85% and does break the rail, and that is reported here as prominently as the pass.** |
| **P10** | relief still flows to the top of the draft, rho beyond ±0.20 | **no** — +0.1617, and the sign is now toward LATER picks |
| **P11** | the production premium is shallower than the price premium | **no** on both readings — but the measured premium is a lower bound because it is estimated on players who play, and that is disclosed in §2.6 |
| **P12** | the late bands come out worse than ORDER K | **no** — every late band is better than ORDER K in both windows |

**Prereg deviations, declared.** None of the constructions changed. Three additions, nothing removed:
the sensitivity file `op_sens.py` re-solves the whole mechanism under each declared surface variation
(the prereg promised the variations, not the re-solve); the age-carrying bar in §7.1 was declared as a
sensitivity and is priced in full; and the matched pair in §10.1 was selected by the two stated
conditions with the selection rule written into `op_named.py` before it was run.

---

## 12 · WHAT IS OWED, AND WHAT THIS SEAT COULD NOT DO

- **No board was built.** Every number in §6 to §10 is an estimate. The engine's assert wall, the
  continuity objects in age, games and pick, rho32 monotonicity, and the day-0 identity cannot be run
  without a build. A build is the next step and it is not this seat's to take.
- **The mature-row path identity will move**, exactly as ORDER I recorded and ORDER N disclosed. The
  age gate holds the current prices of 24-plus rows to within one point across 429 rows, but rows now
  over 24 had younger vantages and their paths move.
- **The survivor bias in the premium is not repaired.** §2.6 and §8.3.
- **The TALL surface is thin at both ends** and the premium there is held flat rather than fitted.
- **The SSP arm moves +5.5 points and was already over the rail.** Flagged in §6.7, not fixed.
- **The premium is estimated on the same board's `v0` that the charge is applied to.** There is no
  hold-out. A future order could re-estimate it on pre-2015 entrants and price the post-2015 ones, and
  that would be a stronger test than anything in this packet.
- **Nothing here rules on the modern picks 1-10 cell.** §8.2 gives both readings and the numbers under
  each. It is a ruling, not a calculation.

---

## 13 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_P.md` | the prereg, pushed at `5911796` before any number existed |
| `op_lib.py` | the one new object — the pedigree premium, the bar, the new surplus. ORDER N's `on_lib.py` is imported whole and not re-implemented |
| `s4_shootout_COPY.py` | the house delivered-value ruler, copied and md5-asserted |
| `op_step2.py` · `STEP2_P.json` · `STEP2_P_out.txt` | the measured surface, the null tests, the new BETA curve |
| `op_step3.py` · `MECH_P.json` · `STEP3_P_out.txt` | the derivation |
| `op_step4.py` · `STEP4_P.json` · `STEP4_P_out.txt` | the anchoring solve, the identity, the ladder, the property test, the movers |
| `op_bands.py` · `BANDS_P.json` · `BANDS_P_out.txt` | ORDER L/M/N's band machinery, only the board list changed |
| `op_arms.py` · `ARMS_P.json` · `ARMS_P_out.txt` | ORDER L/M's pool-arm machinery, only the board list changed |
| `op_class.py` · `CLASS_P.json` · `CLASS_P_out.txt` | ORDER L/N's class machinery, only the board list changed |
| `op_named.py` · `NAMED_P.json` · `NAMED_P_out.txt` | the bar printed, the illustration rows, the matched pairs, the age-carrying variant |
| `op_sens.py` · `SENS_P.json` · `SENS_P_out.txt` | every declared sensitivity, each re-solved from scratch |

Matrix written: `per_entrant_PDERIV.json` in the scratchpad, for the committed instruments. It is an
**estimate, not a build**, and its own metadata says so.
