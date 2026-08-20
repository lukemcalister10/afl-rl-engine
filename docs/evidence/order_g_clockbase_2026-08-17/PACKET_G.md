# PACKET G — THE CLOCK RE-BASE: THE TABLES ON A CORRECTED BENCHMARK, AND THE MISSING SIX POINTS

**Order G. Issue #334. Branch `land/order-29`. Authority: your R-CLOCKBASE ruling (comment 5317457543)
and your correction of it (addendum G-1, registered before any number here was computed).**

> ### THIS SEAT CHANGES REPORTING, NOT PRICES.
> No board number moves. No price is proposed. Nothing is wired. I re-measured the *benchmark* the
> tables are judged against, and re-printed the tables.

Evidence: `PREREG_G.md` (the rule, pushed first) · `o_g_clockbase.py` · `CLOCKBASE_G_out.txt` (the full
console) · `CLOCKBASE_G.json` · `W2_TARGET_G.json` · `t338G_{D,C32R,C31}_console.txt`.

---

# PART ONE — THE TICK. YOU WERE RIGHT, AND ORDER F WAS WRONG.

You said: *"Each player's present season is 100%, and the next season is 86%, bar first year young
players who have one extra at 100%."*

Order F told you a mature-age entrant's fair first-year step was **+30%**. Your rule says **+14%**.

**I checked it against the code. Your rule is what the engine does. Order F made a measurement
mistake. There is no defect in the engine, and no entry price is wrong.**

### What Order F got wrong, in one sentence

Order F put the year-one board **one year too far forward**, which handed every season one extra
14% tick.

### The same thing, with the lines that decide it

The year-one price in the no-arb table is the board as at the entrant's **first season** — his debut
year. The emitter says so:

```
  328 |     MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
  332 |             ... ASOF[(id(p), Y)] = ev(p, Y)
  376 |     yrs = list(range(C + 1, yend + 1)) ...
  377 |     Vpath = [ASOF.get((id(p), y)) for y in yrs]
```
`C` is his draft year, so the year-one cell is the board priced at `AGE_REF = C + 1`. At that board
his first season is the **present** season — and the engine never discounts the present season:

```
 1009 |     if k<=0: return 1.0
```

Order F instead indexed that board as if it sat at `C + 2`:

```
  154 |     f1 = [(0.0 if j == 1 else 1.0 / disc_factor(a, 0.14, j - 2, 'bal', GE[lab])) ...
```

`j - 2`, and grace switched off, are both only true a year later. One year of clock, one factor of
1.14. That is the whole of the difference between 1.14 and 1.2996 (= 1.14²).

### Why nobody caught it

Because it is **invisible on young players**, who are 96% of the draft. At the correct board a young
entrant still has one grace season left, and that spare free step cancels the index slip exactly.
Both ladders give him 1.00. Here they are side by side, straight out of the engine's own
`disc_factor`:

| entry age ≤19 | season 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| weight in the ENTRY price | 1.00000 | 1.00000 | 0.87719 | 0.76947 | 0.67497 |
| weight in the YEAR-1 price — **correct** | *delivered* | 1.00000 | 0.87719 | 0.76947 | 0.67497 |
| weight in the YEAR-1 price — Order F | *delivered* | 1.00000 | 0.87719 | 0.76947 | 0.67497 |
| **fair step** | — | **1.00000** | **1.00000** | **1.00000** | **1.00000** |

| entry age ≥20 | season 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| weight in the ENTRY price | 0.87719 | 0.76947 | 0.67497 | 0.59208 | 0.51937 |
| weight in the YEAR-1 price — **correct** | *delivered* | 0.87719 | 0.76947 | 0.67497 | 0.59208 |
| weight in the YEAR-1 price — Order F | *delivered* | 1.00000 | 0.87719 | 0.76947 | 0.67497 |
| **fair step — correct** | — | **1.14000** | **1.14000** | **1.14000** | **1.14000** |
| fair step — Order F (superseded) | — | 1.29960 | 1.29960 | 1.29960 | 1.29960 |

Order F's own console even *says* the right answer in the line next to its wrong number: *"the step
accretes by 1.30, and Order C's fair = 1.14 × (1 − s1) is exactly right for him."* The prose was
right. The number was not.

### Two things I want to be plain about

1. **The mature entry print is NOT too cheap.** On draft day his first season has not started — it is
   *next* season, and 86% is exactly what your rule orders for next season. There is a second,
   independent proof that the code is right: if we "fixed" the entry print to give a mature entrant
   his first season at 100%, his first-year step would become **1.00, not 1.14** — which would
   contradict your own ruling. Your 1.14 is only producible by the code exactly as it stands. So
   **no defect is reported, and no counterfactual "corrected mature print" column is emitted.**
2. **What is withdrawn:** the "mature entrants ≈ +30%" implication carried to you with PACKET_F. The
   right number is +14%, which is what Order C had all along. **For a mature entrant Order C was
   never wrong.** The re-base bites on *young* entrants only.
3. **What survives, untouched:** Order F's central finding. A young entrant earns **no carry at all**
   over the draft-day → year-one step. The flat 1.14 benchmark was wrong for the 96% who are young,
   and that is the whole point of this re-base.

---

# PART TWO — HOW TO READ THE NEW TABLES

Every cell now carries **three readings**, and they answer different questions.

| reading | question | when it goes RED |
|---|---|---|
| **SELL rail** | Could someone sell at draft day, buy back a year later, and pocket the difference? | mark below 1.00 |
| **BUY rail** | Could someone buy at draft day, sell a year later, and beat the 14% cost of holding? | mark above 1.14 |
| **clock-fair gap** | Is the group marked where the board's *own* discount rule says it should be? | never — it is a signed number, not a verdict |

**The two rails are unchanged.** They are absolute money tests and the re-base does not touch them.
The clock-fair gap is the new, corrected *fairness* reading.

### The benchmark, in plain words

The fair first-year step is **0% for a young entrant** and **+14% for a mature one**. A group's
benchmark is just the blend of those two, weighted by how much of the group's entry value was bought
young — then trimmed slightly for whatever value the group already delivered in that first season.

    clock-fair benchmark = (blended fair step) x (1 - the group's own year-1 delivered share)

Because the draft is ~97% young, the ND bands' benchmarks land near **0.98**, not near **1.11**.

### The two worked examples you asked for

**(1) A cell that was reading RED-and-short, and is now exactly fair — while the rail stays red.**

> **Rookie Draft (RD), 2005–2023, n = 623, landing candidate.**
> Its mark is **0.978** — it *depreciates* 2.2% over the first year.
> - Old flat ruler: fair was **1.073**. It read **9.6 points short of fair.**
> - Clock ruler: 74% of its entry value is young, so its fair step blends to 1.037; after its 5.8%
>   year-one delivery the benchmark is **0.976**. Its gap is **+0.002.**
> - **It is sitting dead on its clock-fair mark.** Nine and a half points of apparent unfairness were
>   ruler, not price.
> - **But its SELL rail is still RED**, and correctly so: a group that ends the year worth less than
>   it cost still offers a sell-and-rebuy. Fairness and arbitrage are different questions, and this
>   row is the cleanest example of why the table now prints both.

**(2) A cell that stays red on every reading.**

> **Picks 31–40, n = 190, landing candidate.**
> Its mark is **0.872** — it loses 12.8%.
> - Old flat ruler: fair 1.104, gap **−0.233**.
> - Clock ruler: 96% young, benchmark **0.975**, gap **−0.103**.
> - **SELL rail RED. Clock-fair gap still short by 10.3 points.** The re-base cuts the apparent
>   problem by more than half, and **does not make it go away.** This is the V's real left arm.

---

# PART THREE — THE RE-BASED STANDING TABLES

Marks are the standing instruments, re-run unchanged. Controls, all halting: the five-band re-run
reproduces `NOARB_D.json` and `NOARB_32R.json` exactly; the delivered-value stream is byte-identical
across the three boards; `fair_C` is the old flat ruler; `fair_F` is Order F's superseded reading,
printed so you can see what moved.

## T1 — the five bands and the two pick windows

### THE LANDING CANDIDATE — board `1f176444`

| cell | n | mark | share ≤19 | fair step | **clock-fair** | **gap** | old fair | old gap | F (sup.) | SELL | BUY |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ALL picks 1-64 | 1200 | **+2.98%** | 0.974 | 1.0036 | 0.980 | **+0.050** | 1.113 | −0.083 | 0.984 | ok | ok |
| picks 1-20 | 380 | **+8.36%** | 0.993 | 1.0010 | 0.979 | **+0.105** | 1.114 | −0.031 | 0.980 | ok | ok |
| picks 21-64 | 820 | **−5.54%** | 0.945 | 1.0077 | 0.982 | **−0.038** | 1.111 | −0.167 | 0.991 | **RED** | ok |
| picks 1-10 | 190 | **+7.93%** | 1.000 | 1.0000 | 0.979 | **+0.101** | 1.116 | −0.037 | 0.979 | ok | ok |
| picks 11-20 | 190 | **+9.20%** | 0.979 | 1.0030 | 0.978 | **+0.114** | 1.112 | −0.020 | 0.982 | ok | ok |
| picks 21-30 | 190 | **+2.76%** | 0.977 | 1.0032 | 0.990 | **+0.038** | 1.125 | −0.097 | 0.993 | ok | ok |
| picks 31-40 | 190 | **−12.84%** | 0.958 | 1.0059 | 0.975 | **−0.103** | 1.104 | −0.233 | 0.981 | **RED** | ok |
| picks 41-64 | 440 | **−7.88%** | 0.900 | 1.0140 | 0.981 | **−0.060** | 1.103 | −0.181 | 0.996 | **RED** | ok |

### C32R — board `7802ee97` (comparison column)

| cell | n | mark | fair step | **clock-fair** | **gap** | old gap | SELL | BUY |
|---|---|---|---|---|---|---|---|---|
| ALL picks 1-64 | 1200 | +1.95% | 1.0036 | 0.980 | **+0.040** | −0.094 | ok | ok |
| picks 1-20 | 380 | +6.56% | 1.0010 | 0.979 | **+0.087** | −0.049 | ok | ok |
| picks 21-64 | 820 | −5.34% | 1.0077 | 0.982 | **−0.036** | −0.165 | **RED** | ok |
| picks 1-10 | 190 | +6.13% | 1.0000 | 0.979 | **+0.083** | −0.055 | ok | ok |
| picks 11-20 | 190 | +7.40% | 1.0030 | 0.978 | **+0.096** | −0.038 | ok | ok |
| picks 21-30 | 190 | +1.62% | 1.0032 | 0.990 | **+0.026** | −0.109 | ok | ok |
| picks 31-40 | 190 | −12.88% | 1.0059 | 0.975 | **−0.103** | −0.233 | **RED** | ok |
| picks 41-64 | 440 | −6.14% | 1.0140 | 0.981 | **−0.042** | −0.164 | **RED** | ok |

### Candidate 31 — board `fe6be9d6` (comparison column)

| cell | n | mark | fair step | **clock-fair** | **gap** | old gap | SELL | BUY |
|---|---|---|---|---|---|---|---|---|
| ALL picks 1-64 | 1200 | +6.62% | 1.0036 | 0.980 | **+0.086** | −0.047 | ok | ok |
| picks 1-20 | 380 | +14.78% | 1.0010 | 0.979 | **+0.169** | +0.033 | ok | **RED** |
| picks 21-64 | 820 | −6.28% | 1.0077 | 0.982 | **−0.045** | −0.174 | **RED** | ok |
| picks 1-10 | 190 | +16.19% | 1.0000 | 0.979 | **+0.183** | +0.046 | ok | **RED** |
| picks 11-20 | 190 | +12.04% | 1.0030 | 0.978 | **+0.142** | +0.009 | ok | ok |
| picks 21-30 | 190 | +3.68% | 1.0032 | 0.990 | **+0.047** | −0.088 | ok | ok |
| picks 31-40 | 190 | −12.38% | 1.0059 | 0.975 | **−0.098** | −0.228 | **RED** | ok |
| picks 41-64 | 440 | −11.36% | 1.0140 | 0.981 | **−0.094** | −0.216 | **RED** | ok |

**Reading it:** the head of the draft (1–30) was reading as *under*-marked on the old ruler and is now
reading as **over** its clock-fair mark by 4 to 11 points. The tail (31–64) was reading 18–23 points
short and is now 6–10 short. **The re-base moves the level. It does not move the spread** — the gap
between the best and worst band is essentially unchanged, because the correction is nearly uniform in
pick. That is exactly what Order F predicted, and it is why the band spread remains a question for the
year-one machinery, not for the entry curve.

## T2 — every pool arm, both windows, all three boards

`fair step` and `clock-fair` are common to all three boards (same store, same delivered stream, same
age mix); only the mark and therefore the gap move between boards.

### PRIMARY window, 2005–2023

| arm | n | share ≤19 | fair step | **clock-fair** | mark D | **gap D** | mark C32R | **gap C32R** | mark C31 | **gap C31** | SELL/BUY (D) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RD | 623 | 0.737 | 1.0369 | 0.976 | 0.978 | **+0.002** | 1.012 | **+0.035** | 0.930 | **−0.046** | **SELL RED** / ok |
| MSD | 55 | — | — | — | *(window has no year-1 cell — every row is n_pre, excluded and counted, never zeroed)* ||||||
| SSP *(thin, n=31)* | 31 | 0.424 | 1.0806 | 0.881 | 1.505 | **+0.625** | 1.532 | **+0.651** | 1.382 | **+0.501** | ok / **BUY RED** |
| UNR | 49 | 0.274 | 1.1016 | 1.092 | 0.579 | **−0.513** | 0.622 | **−0.470** | 0.634 | **−0.458** | **SELL RED** / ok |
| IRE | 47 | 0.571 | 1.0601 | 1.051 | 1.135 | **+0.084** | 1.174 | **+0.123** | 0.947 | **−0.104** | ok / ok |
| PDA | 43 | 0.933 | 1.0094 | 1.007 | 0.817 | **−0.190** | 0.857 | **−0.150** | 0.772 | **−0.235** | **SELL RED** / ok |
| PDN | 33 | 0.870 | 1.0183 | 1.018 | 0.622 | **−0.396** | 0.666 | **−0.352** | 0.628 | **−0.390** | **SELL RED** / ok |
| PDS | 21 | 1.000 | 1.0000 | 1.000 | 0.745 | **−0.254** | 0.791 | **−0.209** | 0.712 | **−0.288** | **SELL RED** / ok |
| **ALLPOOL** | 961 | 0.734 | 1.0373 | 0.981 | 0.961 | **−0.020** | 0.995 | **+0.015** | 0.915 | **−0.066** | **SELL RED** / ok |

### MODERN window, 2019–2023

| arm | n | share ≤19 | fair step | **clock-fair** | mark D | **gap D** | mark C32R | **gap C32R** | mark C31 | **gap C31** | SELL/BUY (D) | thin? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RD | 66 | 0.722 | 1.0389 | 1.010 | 0.814 | **−0.196** | 0.851 | **−0.159** | 0.815 | **−0.195** | **SELL RED** / ok | |
| MSD | 55 | — | — | — | *(no year-1 cell)* ||||||| |
| SSP | 31 | 0.424 | 1.0806 | 0.881 | 1.505 | **+0.625** | 1.532 | **+0.651** | 1.382 | **+0.501** | ok / **BUY RED** | |
| UNR | 13 | 0.286 | 1.1000 | 1.099 | 0.672 | **−0.427** | 0.717 | **−0.383** | 0.674 | **−0.425** | **SELL RED** / ok | **THIN** |
| IRE | 12 | 0.467 | 1.0746 | 1.075 | 0.507 | **−0.568** | 0.555 | **−0.520** | 0.555 | **−0.520** | **SELL RED** / ok | **THIN** |
| PDA | 13 | 1.000 | 1.0000 | 1.000 | 0.589 | **−0.412** | 0.631 | **−0.369** | 0.619 | **−0.381** | **SELL RED** / ok | **THIN** |
| PDN | 25 | 1.000 | 1.0000 | 1.000 | 0.651 | **−0.349** | 0.696 | **−0.304** | 0.638 | **−0.362** | **SELL RED** / ok | |
| PDS | 0 | — | — | — | *(no year-1 cell)* ||||||| |
| **ALLPOOL** | 174 | 0.683 | 1.0444 | 0.955 | 0.909 | **−0.047** | 0.945 | **−0.010** | 0.884 | **−0.071** | **SELL RED** / ok | |

**Thin-n bounds stand.** SSP (n = 31, and a recent mechanism that is right-censored), UNR, IRE and PDA
in the modern window all sit under 15 rows in at least one cut and carry no clock-fair verdict — only
their rails. **SSP's +50% inversion is untouched by this seat and remains unexplained**, exactly as
Order C and Order F both said. Its buy-side rail is RED on all three boards.

**UNR, registered in advance and answered:** the prereg predicted UNR would get worse under a 1.30
mature accretion. Under your ruled 1.14 it does **not** — it lands back at Order C's own reading
(−0.513 against −0.551). The prediction was withdrawn before the run and this is the outcome.

## T3 — the vantage matrix, refreshed (landing candidate, diagnostic only)

**The carry columns are unchanged.** From the year-one board onward the grace is spent and the two
clocks agree, so those legs were already benchmarked correctly. Only the caption is re-based.

| picks 1-10 — mark 1.079, clock-fair 0.979, gap **+0.101** (old ruler: fair 1.116, gap −0.036) |
|---|

| vantage | k=1 | k=2 | k=3 | k=4 | carry |
|---|---|---|---|---|---|
| yr 0 | 1.079 | 1.179 | 1.360 | 1.521 | 1.14 / 1.30 / 1.48 / 1.69 |
| yr 1 | 1.093 | 1.260 | 1.409 | 1.392 | |
| yr 2 | 1.153 | 1.290 | 1.274 | 1.208 | |

| picks 11-20 — mark 1.092, clock-fair 0.978, gap **+0.114** (old: 1.112, −0.020) |
|---|

| vantage | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| yr 0 | 1.092 | 1.203 | 1.345 | 1.538 |
| yr 1 | 1.101 | 1.232 | 1.409 | 1.504 |
| yr 2 | 1.118 | 1.279 | 1.365 | 1.324 |

| picks 21-30 — mark 1.028, clock-fair 0.990, gap **+0.038** (old: 1.125, −0.097) |
|---|

| vantage | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| yr 0 | 1.028 | 1.182 | 1.418 | 1.599 |
| yr 1 | 1.150 | 1.380 | 1.556 | 1.567 |
| yr 2 | 1.200 | 1.352 | 1.362 | 1.428 |

| picks 31-40 — mark 0.872, clock-fair 0.975, gap **−0.103** (old: 1.104, −0.233) |
|---|

| vantage | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| yr 0 | **0.872\*** | **0.941\*** | 1.255 | 1.249 |
| yr 1 | 1.080 | **1.440\*** | 1.433 | 1.600 |
| yr 2 | **1.333\*** | 1.327 | 1.482 | 1.379 |

| picks 41-64 — mark 0.921, clock-fair 0.981, gap **−0.060** (old: 1.103, −0.181) |
|---|

| vantage | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|
| yr 0 | **0.921\*** | 1.073 | 1.152 | 1.256 |
| yr 1 | 1.164 | 1.251 | 1.363 | 1.493 |
| yr 2 | 1.074 | 1.171 | 1.282 | 1.415 |

Band-vs-band spread of forward growth is unchanged by the re-base: yr-0 vantage 0.220 / 0.262 / 0.266
/ 0.350 at k = 1..4.

## T4 — where each band's inconsistency lives, re-based

| band | year-1 leg (clock) | was, on the flat ruler | later-years leg (yr1→5 growth vs carry 1.689) |
|---|---|---|---|
| picks 1-10 | **+0.101** | −0.036 | 1.392 → **−0.297** |
| picks 11-20 | **+0.114** | −0.020 | 1.504 → **−0.185** |
| picks 21-30 | **+0.038** | −0.097 | 1.567 → **−0.122** |
| picks 31-40 | **−0.103** | −0.233 | 1.600 → **−0.089** |
| picks 41-64 | **−0.060** | −0.181 | 1.493 → **−0.196** |

The later-years leg is untouched by this seat — it never depended on the entry clock.

## T5 — the entry-age natural experiment, and the one live finding it produces

Your grace rule cuts at entry age ≤19, which is a hard, ruled boundary. Order C's own window,
2005–2021:

| age at entry | n | mark | **clock-fair** | **gap** | old flat fair | old gap | F (sup.) gap | SELL | BUY |
|---|---|---|---|---|---|---|---|---|---|
| 17 and under | 93 | 0.900 | 0.995 | **−0.094** | 1.134 | −0.233 | −0.094 | **RED** | ok |
| 18 | 1401 | 1.026 | 0.984 | **+0.042** | 1.122 | −0.096 | +0.042 | ok | ok |
| 19 | 167 | 0.945 | 0.991 | **−0.045** | 1.129 | −0.184 | −0.045 | **RED** | ok |
| **20** | 80 | **1.273** | 1.074 | **+0.199** | 1.074 | +0.199 | +0.049 | ok | **RED** |
| **21+** | 245 | 1.100 | 0.991 | **+0.110** | 0.991 | +0.110 | −0.029 | ok | ok |

Mean absolute gap across the five buckets: old flat ruler **0.164** → your clock **0.098**.

**THE ONE LIVE FINDING, and I am not smoothing it.** Under your ruled 1.14, mature-age entrants sit
**above** their fair mark — age 20 by 20 points, age 21+ by 11 — and the age-20 bucket also **breaches
the buy-side exploit rail** (1.273 against the 1.14 cap). In plain words: **mature-age entrants look
cheap at entry relative to what the board pays them a year later.**

I want to be honest about the tension. Order F's superseded 1.2996 fits those two rows *better*
(+0.049 and −0.029). But **fit is not law.** The code and your ruling both say 1.14, so 1.14 governs
the benchmark, and the excess gets reported as a finding rather than absorbed into the ruler where you
would never see it. This is an **entry-side, age-targeted** question — 325 rows out of 2,648 — and it
is yours to rule on, not mine to price.

---

# PART FOUR — THE W2 CLASS TARGET, RE-DERIVED. THE MISSING SIX POINTS.

## What the old band was

Seat W2 measured the hindsight-fair year-one class appreciation and proposed a class-level acceptance
band of **[1.100, 1.117]**. It was built on the flat identity `fair = 1.14 × (1 − year-1 delivered
share)` — the ruler you have now corrected. That identity is where the "the candidate is ~6 points too
low" reading came from.

## How I rebuilt it

Same matrix (the registered W2 object), same 17 classes, same all-arm population, same delivered-value
ruler, same estimator (2005–2015 class mean, class bootstrap B = 2000, seed 33). **The only thing that
changed is the benchmark**, from `1.14 × (1 − share)` to `(blended fair step) × (1 − share)`.

Halting controls, both passed: my flat column reproduces PACKET_W2's published `R*full` **exactly on
all 17 classes**, and my recomputation of the landing candidate's own class marks reproduces the Order-D
wire's `mean_0515` of **1.0421** exactly.

| class | n | candidate | old fair | delivered share | share ≤19 | fair step | **NEW fair** |
|---|---|---|---|---|---|---|---|
| 2005 | 109 | 0.9011 | 1.1161 | 0.0210 | 0.946 | 1.0076 | **0.9865** |
| 2006 | 122 | 1.0313 | 1.1198 | 0.0177 | 0.969 | 1.0043 | **0.9865** |
| 2007 | 122 | 1.0626 | 1.1086 | 0.0276 | 0.952 | 1.0068 | **0.9790** |
| 2008 | 134 | 1.0084 | 1.1020 | 0.0333 | 0.935 | 1.0091 | **0.9755** |
| 2009 | 126 | 1.0574 | 1.0692 | 0.0621 | 0.881 | 1.0167 | **0.9535** |
| 2010 | 138 | 1.1410 | 1.0998 | 0.0353 | 0.918 | 1.0114 | **0.9757** |
| 2011 | 145 | 1.1197 | 1.0978 | 0.0370 | 0.884 | 1.0163 | **0.9786** |
| 2012 | 108 | 1.0606 | 1.1165 | 0.0206 | 0.896 | 1.0146 | **0.9936** |
| 2013 | 100 | 1.0720 | 1.1329 | 0.0063 | 0.950 | 1.0071 | **1.0008** |
| 2014 | 121 | 1.0167 | 1.1288 | 0.0098 | 0.912 | 1.0123 | **1.0024** |
| 2015 | 110 | 1.1069 | 1.1038 | 0.0317 | 0.910 | 1.0126 | **0.9805** |
| 2016 | 125 | 1.0429 | 1.1130 | 0.0237 | 0.905 | 1.0132 | **0.9892** |
| 2017 | 106 | 1.0883 | 1.1014 | 0.0339 | 0.937 | 1.0089 | **0.9747** |
| 2018 | 124 | 1.0140 | 1.1012 | 0.0341 | 0.903 | 1.0136 | **0.9791** |
| 2019 | 100 | 0.9821 | 1.0968 | 0.0379 | 0.928 | 1.0101 | **0.9719** |
| 2020 | 88 | 0.9767 | 1.1214 | 0.0163 | 0.957 | 1.0060 | **0.9896** |
| 2021 | 108 | 1.0168 | 1.0532 | 0.0761 | 0.870 | 1.0182 | **0.9407** |

2019–2021 are right-truncated and are printed but excluded from the band, exactly as W2 did.

## The corrected band, with its uncertainty

| ruler | 2005–2015 class mean | median | per-class range | **90% band** |
|---|---|---|---|---|
| OLD, flat 1.14 | 1.1087 | 1.1086 | [1.0692, 1.1329] | **[1.100, 1.117]** |
| **NEW, your clock (primary)** | **0.9830** | 0.9805 | [0.9535, 1.0024] | **[0.976, 0.989]** |
| control — exact clock ratio | 0.9909 | 0.9931 | [0.9696, 1.0053] | [0.985, 0.996] |
| control — head-count age mix | 0.9936 | 0.9929 | [0.9734, 1.0131] | [0.988, 1.000] |
| superseded — Order F's 1.2996 | 0.9949 | 0.9944 | [0.9713, 1.0163] | [0.989, 1.001] |

The corrected band is identical on all three boards to four decimals — the age mix barely differs
between them. My two disclosed construction choices (the exact-clock variant and head-count weighting)
move the band by at most **+0.011**; every variant sits between 0.976 and 1.000, and **none of them
comes within four points of 1.100.**

## THE VERDICT ON THE MISSING SIX POINTS — one sentence

> **The "missing 6 points" was entirely a ruler artifact — and more than entirely: under your own
> grace clock the corrected class target is [0.976, 0.989], and the landing candidate's 1.042 does not
> fall 5.8 points short of it but sits 5.3 points ABOVE it.**

Two things follow, and both matter:

1. **No points are owed to the year-one class.** The W2 recommendation to add +6 to +7 points of
   class-level appreciation was built on the flat ruler and **must not be used as an acceptance gate
   in that form again.** The band `[1.100, 1.117]` is retired by this measurement.
2. **Nothing is broken by the overshoot.** 1.042 is comfortably inside the buy-side exploit rail
   (1.042 < 1.14), so no arbitrage is created by the class sitting a little rich. It is a fairness
   reading, not a money leak.

**Note also what does NOT change:** W2's *spread* findings — the calibration slope, the two-leg
production/pedigree re-mix, the 5–9-game cells — are all **within-class share** objects. A class-level
benchmark cancels out of them entirely. **Acceptance bands 2, 3 and 4 of PACKET_W2 §(3) are untouched
by this seat and stand as written. Only band 1, the LEVEL band, is retired and replaced.**

---

# PART FIVE — HONESTY LEDGER

1. **Every table says it: this seat changes reporting, not prices.** No board number moved. No price
   was proposed. Nothing was wired.
2. **The tick verdict was read off the code, not off the fit.** Order F's superseded 1.2996 fits the
   mature-entrant rows better than your ruled 1.14 does. I did not let that choose the benchmark, and
   I printed the losing column in every table so you can see the cost of the choice.
3. **Choice points in the age mix, all disclosed at the point of use.** *Which age:* the matrix's
   `age_draft`, Order F's field, complete on all three boards (zero nulls, asserted). *The boundary:*
   ≤19 vs ≥20, your ruled grace-A cut, not a fitted one. *The weight:* entry board points, because the
   mark being judged is itself value-weighted; the head-count alternative is printed and moves the
   class band by +0.011. *Mid-year entrants:* MSD keeps `age_draft` as stored, and has no year-one
   cell in either window in any case — its rows are excluded and counted (`n_pre = 55`), never zeroed
   and never blank.
4. **One approximation, named in the prereg before the run.** The benchmark uses the flat-clock
   delivered share so the new and old columns stay directly comparable; the exactly-clock-consistent
   object is printed as a control throughout and differs by about 0.008 at class level and 0.003–0.025
   at cell level.
5. **Right-censoring.** Later classes are truncated on the delivered ruler, which overstates the
   delivered share and therefore understates the clock-fair benchmark. Order F's own 2005–2019 window
   is printed beside the primary for every ND cell; the two differ by at most 0.006.
6. **Thin-n bounds stand** on SSP, UNR, IRE, PDA, PDN, PDS wherever n < 15 in a window — rails only,
   no clock-fair verdict. SSP additionally keeps its right-censoring caveat and remains unexplained.
7. **The prereg's UNR prediction was withdrawn before the run** (it was conditional on the 1.30 that
   the tick verdict killed) and re-registered as a question; the answer is that UNR returns to Order
   C's own number rather than deepening.
8. **What I did not do.** I did not re-fit anything, propose a price, or touch the exploit rails. The
   band spread, the SSP inversion, the mature-entrant richness and the year-one machinery are all
   left exactly where they were, named, for you.

---

*Order G, clock re-base instrument seat. Measured and reported; nothing wired.*
