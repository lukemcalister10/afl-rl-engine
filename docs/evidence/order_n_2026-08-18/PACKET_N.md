# PACKET N — THE BOARD DOES PAY FOR GOOD YOUNG PERFORMANCE. THE CHARGE DOES NOT.

**Seat:** ORDER N. **Date:** 2026-08-18. **Prereg:** `PREREG_N.md`, pushed at `602d40a` before any
number in this packet existed.

**No board was built. No engine line was changed. Nothing is adopted and nothing lands on this seat's
word.** This is a measurement and a mechanism specification, for the owner to rule on.

**No constant here was chosen to move any player to any value.** The named rows appear once, in §9,
wherever the derived rule puts them.

---

## 1 · THE ANSWER, IN TEN SENTENCES

You said young players who perform well are being punished as hard as those who do not.

**On the literal wording, the board is not guilty. On the substance, you are right, and I can show you
exactly where.**

The board's *price* does reward performing above your age bar. Hold games roughly constant and the
slope is positive and real: +0.039 on price-over-entry-price per point per game of surplus, 90%
confidence interval +0.023 to +0.060. That fired one of my own falsifiers, and I am reporting it as a
refutation rather than burying it.

**But the reward is almost absent where it matters most.** At 1 to 4 career games the board pays 7.8
board points for a point per game of surplus. At 16 to 24 games it pays 64.5. The rank correlation at
1 to 4 games is +0.14 with a confidence interval that straddles zero. The board barely distinguishes a
19-year-old flying from a 19-year-old drowning until he has played about ten games.

**And the charge itself reads nothing at all.** The counterweight's charge is a pure function of games
played. Its correlation with performance surplus is −0.05, confidence interval −0.18 to +0.08 —
indistinguishable from zero. **Measured in points, above-expectation rows actually pay MORE than
below-expectation rows: 172 points against 93.** They pay more because they have played more games.

**The outcome data says that is badly wrong.** A young player 10 points a game above his age bar
delivers 4.0 times what one 10 points below delivers, once he has ten games. At fifteen games it is
8.0 times. At thirty it is 9.3 times. Those are measured on the house delivered-value ruler with the
pedigree held fixed.

**I derived the replacement from that measurement and priced it offline. It works on the thing you
asked for and it breaks one rail I cannot fix.** All three sub-expectation rows fall — the first
mechanism this project has produced that can mark anyone down. Harry Dean and Cooper Duff-Tytler
clear your references. The year-1 class mark holds. The veteran caps hold. **Picks 1-10 goes through
the +14% buy rail in both windows, and no setting of the mechanism brings it back without pushing the
class mark below your 1.03 floor.** That conflict is quantified in §8 and it is yours to rule on.

---

## 2 · HOW "PERFORMING ABOVE YOUR AGE" IS MEASURED

One construction, used everywhere in this packet.

The engine already has an age-appropriate bar. It is `o32_gate_bar`, built from the S1 C3 surface. It
says what an average season looks like for a player of a given age in a given position class. For a
19-year-old key defender it is 44.8 points a game. For a 19-year-old midfielder it is 57.0. It goes
flat at age 24.

**Performance surplus** is a player's games-weighted average distance from that bar, in points per
game.

- Harry Dean: 17 games at 59.7 a game, as a 19-year-old key defender. His bar is 44.8. **Surplus
  +14.9.**
- Daniel Annable: 2 games, as a 19-year-old midfielder. His bar is 57.0. **Surplus −19.0.**
- Isaac Kako: 36 games as a small forward, ages 19 and 20. **Surplus +0.8** — almost exactly at his bar.

The surface was read out of `CONSTRUCTIONS_S1.json` and asserted, number by number, against the
engine's own `O32_GATE_DELTA` literal. Falsifier N2 did not fire.

---

## 3 · STEP 1 — THE PROPERTY, ON THE CURRENT BOARD

195 rows: on the ledger, aged 22 or under, between 1 and 60 career games. Price response is board
price divided by entry price.

### 3.1 · The board does reward it. That is a refutation of the literal claim.

| what was measured | ORDER K | landing candidate |
|---|---:|---:|
| slope of price response on surplus, unconditional | +0.0507 [+0.0278, +0.0798] | +0.0474 [+0.0257, +0.0751] |
| **the same with games-bin fixed effects** | **+0.0395 [+0.0228, +0.0596]** | **+0.0368 [+0.0209, +0.0561]** |
| the same, plus entry price controlled | +0.0564 [+0.0353, +0.0810] | +0.0534 [+0.0331, +0.0771] |
| Spearman(surplus, price response) | +0.4875 | +0.4712 |

**Falsifier N4 fired.** I preregistered that a positive, significant within-games slope would refute
the claim that good young performers are punished. It is positive and significant. I am not going to
restate it as a win.

### 3.2 · But look at where the reward lives.

| career games | n | rank correlation of price response with surplus | board points paid per point of surplus |
|---|---:|---|---:|
| 1-4 | 42 | +0.135 [−0.153, +0.394] — **not distinguishable from zero** | **+7.8** |
| 5-9 | 33 | +0.261 [−0.009, +0.500] — **not distinguishable from zero** | **+9.7** |
| 10-15 | 33 | +0.435 [+0.120, +0.693] | +35.4 |
| 16-24 | 36 | +0.707 [+0.508, +0.832] | +64.5 |
| 25-39 | 29 | +0.787 [+0.632, +0.870] | +40.5 |

**The board pays about eight times less for a point of surplus at two games than at twenty.** Below ten
games it does not reliably pay for it at all. That is precisely the region where your two named rows
live and precisely where the pedigree leg — the thing the charge attacks — dominates the price.

### 3.3 · Worked, from the binned means at 1-4 games

| surplus tercile | n | mean surplus | mean games | mean price / entry price |
|---|---:|---:|---:|---:|
| low | 14 | −28.66 | 2.3 | 0.8799 |
| mid | 14 | −12.68 | 2.7 | 1.0052 |
| high | 14 | **+7.09** | 2.6 | **1.1402** |

A 35.75-point gap in surplus buys 0.26 of price ratio. At 25-39 games a 21.4-point gap buys 1.92.

### 3.4 · The charge in isolation. This is the part that is indefensible.

The charge is `0.50 × (g/14) × exp(1 − g/14)`. Games played is its only input.

| statistic | value | 90% CI |
|---|---:|---|
| Spearman(surplus, charge as a percentage) | **−0.0495** | [−0.1750, +0.0833] |
| Spearman(surplus, charge **in board points**) | **+0.1931** | [+0.0661, +0.3106] |
| Spearman(surplus, charge as a share of the uncharged price) | −0.3731 | [−0.4811, −0.2533] |

Pooled over the whole young window:

| group | n | mean surplus | mean games | mean charge | **mean charge in points** |
|---|---:|---:|---:|---:|---:|
| below expectation | 65 | −21.40 | 10.1 | 34.1% | **93.5** |
| middle | 65 | −6.87 | 17.0 | 38.5% | 113.4 |
| **above expectation** | 65 | **+10.99** | 25.4 | 31.2% | **172.0** |

**In money, the young players who are producing above their age bar pay nearly twice the charge of the
ones who are not.** Not because of how they played. Because they played more.

### 3.5 · Two rows, two games apart

Every pair below is held to within two career games.

| above the bar | below the bar | games | surplus | charge each pays |
|---|---|---|---|---|
| Noah Mraz | Matt Hill | 4 vs 2 | +35.2 vs −44.5 | 29.2% vs 16.8% |
| Oscar Ryan | Jakob Ryan | 2 vs 1 | +24.0 vs −43.2 | 16.8% vs **9.0%** |
| Noah Mraz | Balyn O'Brien | 4 vs 4 | +35.2 vs −28.5 | **29.2% vs 29.2%** |

1,217 such pairs exist on the board. Read the third row: same games, a 63-point gap in production
against age, identical charge to the last decimal.

**That is the defect, and it is a property of the rule, not of any player.**

---

## 4 · STEP 2 — WHAT PERFORMING ABOVE YOUR AGE ACTUALLY PREDICTS

This is the derivation input and it comes from outcomes, never from board prices.

**Population.** Every entrant from 2005 on, looked at 1 to 6 years after entry, aged 22 or under at
that moment, with between 1 and 60 career games and at least one observable season afterwards.
**4,143 vantage rows over 1,415 players.**

**Ruler.** The house delivered-value ruler, lifted whole out of `s4_shootout.py` and md5-asserted.
Falsifier N3 did not fire. Delivered value is the discounted sum of every later season a player
actually produced, at your own 1.14 rate. A player who never plays again scores zero.

**A player contributes up to six rows, so every confidence interval below resamples PLAYERS, not
rows.**

### 4.1 · The headline surface

`BETA` is the proportional change in subsequent delivered value per one point per game of surplus,
with the entry price held fixed.

| career games | rows | BETA | 90% CI | **what +10 above the bar is worth against −10 below** |
|---|---:|---:|---|---:|
| **2** | 776 | +0.0176 | [+0.0072, +0.0281] | **1.42×** |
| **5** | 613 | +0.0452 | [+0.0313, +0.0584] | **2.47×** |
| **10** | 629 | +0.0696 | [+0.0532, +0.0865] | **4.02×** |
| **15** | 465 | +0.1042 | [+0.0857, +0.1218] | **8.04×** |
| **20** | 517 | +0.1041 | [+0.0887, +0.1195] | **8.03×** |
| **30** | 625 | +0.1115 | [+0.0960, +0.1269] | **9.29×** |
| 50 | 518 | +0.1082 | [+0.0914, +0.1247] | 8.70× |

**Three things fall out and all three matter.**

**One. It is real everywhere, including at two games.** The interval at two games excludes zero. Small,
but there. Falsifier N5 did not fire. Falsifier N6 did not fire — the sign is positive at every level.

**Two. It gets stronger with evidence, and then it stops.** It roughly sextuples between two games and
fifteen, and is flat after that. That is an evidence-accumulation curve and it is the whole
justification for a charge that grows with games and then holds, rather than one that peaks and falls
back.

**Three. It is very large.** Nine times is not a nudge. The board is currently paying a small fraction
of it below ten games.

### 4.2 · The plain read

Mean subsequent delivered value, by surplus tercile, within games bins.

| games | tercile | rows | mean surplus | mean entry price | **mean delivered value** |
|---|---|---:|---:|---:|---:|
| 1-3 | low | 258 | −36.07 | 395 | 81.0 |
| 1-3 | mid | 259 | −17.28 | 477 | 199.9 |
| 1-3 | **high** | 259 | **+1.92** | 479 | **175.9** |
| 8-12 | low | 209 | −18.26 | 505 | 134.4 |
| 8-12 | mid | 210 | −6.55 | 468 | 158.4 |
| 8-12 | **high** | 210 | **+6.44** | 717 | **474.0** |
| 13-17 | low | 155 | −15.50 | 567 | 94.6 |
| 13-17 | mid | 155 | −3.17 | 612 | 247.8 |
| 13-17 | **high** | 155 | **+11.02** | 912 | **801.5** |
| 25-39 | low | 208 | −8.85 | 618 | 206.8 |
| 25-39 | mid | 208 | +2.37 | 756 | 450.8 |
| 25-39 | **high** | 209 | **+15.54** | 1124 | **1125.0** |

**One row of that table does not behave, and it is the honest one to point at.** At 1-3 games the top
tercile delivers 175.9 against the middle tercile's 199.9. The ordering fails. At every other games
level it holds and the spread widens. That is the same story the confidence interval at two games
tells: the signal is there, it is small, and it is noisy.

*(full table with dispersion, medians and zero-shares in `STEP2_N_out.txt`)*

### 4.3 · Pedigree's own decay — the other half of requirement (c)

The partial rank correlation of the entry price with delivered value, once you already know how the
player has performed:

| career games | partial rho(entry price, delivered value \| surplus) |
|---|---:|
| 1-3 | +0.186 [+0.107, +0.267] |
| 4-7 | +0.347 [+0.271, +0.415] |
| 8-12 | +0.278 [+0.194, +0.355] |
| 13-17 | +0.361 [+0.285, +0.435] |
| **18-24** | **+0.167** [+0.075, +0.254] |
| 25-39 | +0.178 [+0.100, +0.254] |
| 40-60 | +0.188 [+0.093, +0.277] |

**Falsifier N7 did not fire — pedigree's incremental power does not rise with games.** But it does not
decay smoothly either. It is noisy up to seventeen games and then drops to about half and stays there.
I am reporting it as it is rather than smoothing it into a story.

### 4.4 · Splits. One of them is a real finding.

| position class | 1-3 games | 8-12 games | 18-24 games | 40-60 games |
|---|---:|---:|---:|---:|
| **TALL** (KPD, KPF, RUCK) | +0.011 [−0.007, +0.032] **not distinguishable from zero** | +0.040 [+0.011, +0.069] | +0.066 [+0.028, +0.102] | +0.124 [+0.084, +0.168] |
| **SMALL** (MID, SD, SF) | stronger at every level | | | |

**For a tall, early production against the age bar carries little or no information.** That is
consistent with everything this project already believes about talls developing late, and it means the
mechanism below is doing less work on a Cooper Duff-Tytler than on a small of the same age. It is
reported, not corrected: the derived charge is pooled, because splitting it would add a construction
choice the sample sizes do not support at 1-3 games (n = 273 for talls).

By pick band the effect is present in every band and is not a top-of-draft artefact. Full table in
`STEP2_N_out.txt`.

### 4.5 · The censoring check

Later vantages have fewer observable future seasons. Every regression above carries vantage-year
effects to absorb that. As a separate check the whole surface was recomputed on a **fixed five-year
forward window** (3,295 rows with five full observable seasons). The numbers barely move: 0.0172 at
two games, 0.0818 at ten, 0.1043 at fifteen, 0.1119 at thirty. The shape is not a censoring artefact.

---

## 5 · STEP 3 — THE DERIVED CHARGE

### 5.1 · The form

```
pi  *=  exp( -LAMBDA * A(g) * T(s) )

A(g) = 1 - exp(-g / G0)                            how much evidence g games is
T(s) = clip( 1 - THETA_R * (s - s0), TMIN, TMAX )  what the evidence says
```

`g` is career games. `s` is performance surplus (§2).

### 5.2 · Two changes from what I preregistered, both disclosed

I preregistered `max(0, 1 - ETA * A(g) * exp(-THETA*(s-s0)))`. Two things changed and neither is
cosmetic.

**D1 — `exp(-X)` instead of `(1 - X)`.** `exp(-X)` is between 0 and 1 for every non-negative X. A row
can never be charged past its whole pedigree leg, and the `max(0, ·)` clamp the current mechanism
needs disappears from the law entirely. It stops being a thing to check.

**D2 — the tilt is linear in surplus inside the exponent, not exponential.** At the measured tilt
strength, an exponential multiplier spans this population from 0.031 to 175.8 — four orders of
magnitude. Worse, it would make the delivered tilt depend on where a row sits, leaning 350 times
harder on the bottom of the spread than the top. Step 2 measured **one** slope. With the linear form
the delivered slope is exactly constant:

```
d ln(retained pedigree) / ds  =  LAMBDA * A(g) * THETA_R
```

### 5.3 · Every constant, and where it comes from

| constant | value | 90% CI | derived from |
|---|---:|---|---|
| **G0** | **9.72 games** | [7.39, 12.84] | the BETA curve of §4.1, fitted as `BETA(g) = BETA_sat·(1 − exp(−g/G0))`, weighted by each bin's own inverse variance |
| **BETA_sat** | **0.11521** | [0.10434, 0.12828] | the same fit |
| **LAMBDA × THETA_R** | **= BETA_sat** | — | so the pedigree leg responds to surplus at exactly the rate the outcome data says it should, at every level of surplus, scaled by A(g), which reproduces the measured BETA(g) |
| **s0** | **+2.3163** | — | the games-weighted mean surplus of the young cohort. T(s0) = 1: a row at the centre pays the base charge |
| **TMAX** | 5.998 at the anchoring LAMBDA | — | T at the cohort's own 5th percentile of surplus (−31.72). The worst 5% all pay the same top rate rather than an unbounded one |
| **LAMBDA** | **0.82131** | — | **solved**, not chosen: bisection, so the derived charge removes exactly the same total number of points from the year-1 class-mark population as the current charge does |
| **age gate** | 24 | — | see §7 |

**There is no free parameter.** The product `LAMBDA × THETA_R` is pinned by the measurement, and
`LAMBDA` is pinned by the anchoring identity. `THETA_R` follows as 0.14028.

Weighted SSE of the A(g) fit is 2.56 over seven bins with two parameters. Fit against observation:

| games | BETA observed | BETA fitted | A(g) |
|---:|---:|---:|---:|
| 1.91 | +0.0176 | +0.0206 | 0.179 |
| 5.38 | +0.0452 | +0.0490 | 0.425 |
| 9.86 | +0.0696 | +0.0734 | 0.637 |
| 15.00 | +0.1042 | +0.0906 | 0.786 |
| 20.84 | +0.1041 | +0.1017 | 0.883 |
| 31.60 | +0.1115 | +0.1108 | 0.961 |
| 48.63 | +0.1082 | +0.1144 | 0.993 |

### 5.4 · What it does, side by side

Percentage of the pedigree leg removed.

| career games | **current, blind** | derived, s = −25 | derived, s = −10 | derived, s = 0 | derived, s = +15 |
|---:|---:|---:|---:|---:|---:|
| 2 | 16.8% | 52.2% | 34.1% | 18.3% | **0.0%** |
| 5 | 34.0% | 79.7% | 59.4% | 35.4% | **0.0%** |
| 10 | 47.5% | 92.2% | 76.3% | 50.3% | **0.0%** |
| 14 | 50.0% | 95.2% | 81.9% | 56.4% | **0.0%** |
| **17** | **49.0%** | 96.2% | 84.3% | 59.3% | **0.0%** |
| 20 | 46.5% | 96.9% | 85.8% | 61.3% | **0.0%** |
| 30 | 34.2% | 97.7% | 88.2% | 64.6% | **0.0%** |
| **36** | **26.7%** | 97.9% | 88.8% | 65.4% | **0.0%** |

**Read the 17-game row against the 36-game row in the current column.** The charge falls from 49.0% to
26.7%. The derived charge does not fall anywhere.

**The zero point.** T hits zero at surplus +9.44 points a game. **A young player producing more than
9.44 points a game above his age bar pays nothing on his pedigree leg. He keeps the whole prior.**
That is 18.5% of the young cohort, and it is the mechanism doing the thing you asked for.

### 5.5 · Requirement (c), checked properly — and the answer is not the one the order assumed

The order says the charge should be monotone in evidence because a prior should decay, not recover. I
checked whether the **retained prior** — the pedigree coefficient after the charge — is monotone,
because that is what the argument is actually about. The pedigree leg already decays on its own as
weight moves to production.

| career games | pi before any charge | **retained NOW** | **retained ORDER N** |
|---:|---:|---:|---:|
| 14 | 0.6162 | 0.3081 | 0.3386 |
| **17** | 0.5867 | **0.2992** | 0.3069 |
| 20 | 0.5598 | 0.2993 | 0.2824 |
| 25 | 0.5179 | 0.3071 | 0.2509 |
| **30** | 0.4727 | **0.3112** | 0.2236 |
| 36 | 0.4228 | 0.3099 | 0.1967 |

**The retained prior under the current mechanism rises 14 times over g = 0 to 300.** It bottoms out at
17 games and then recovers. A 30-game player holds 0.3112 of unearned prior; a 17-game player holds
0.2992. **You were right and the number is 4%.** Under the derived charge it never rises: 0 rises over
the same range.

### 5.6 · The structural properties

| property | result |
|---|---|
| **N-S1** A(0) = 0 exactly, so pi(0) = D and no day-0 print can move | PASS |
| **N-S2** A is non-decreasing in g over [0, 400] | PASS |
| **N-S3** T is non-increasing in s | PASS — structural, a clipped decreasing line |
| **N-S4** the factor is in (0, 1] for every input | PASS — structural, it is an exponential |

---

## 6 · HOW THE OFFLINE PRICING WORKS, AND WHY IT IS EXACT

The charge enters the engine as one multiplier on the pedigree leg. So the price is exactly linear in
the charge:

```
price(F)  =  price(F = 0)  -  F × C          C = the pedigree leg before any charge
```

Two boards ORDER M already built give both ends: `f3101883` (charge on) and `73bf9617` (charge off,
everything else identical). Every row's `C` falls straight out.

**Falsifier N1 did not fire.** Four tests, in `IDENT_N_out.txt`:

| test | result |
|---|---|
| **T1** the charge can only subtract, and gameless rows must be bit-equal | PASS — 0 of 14,420 wrong-signed, 0 of 2,514 gameless rows moved, 0 day-0 mismatches |
| **T2** linearity, on six built boards at eta 0.00 to 0.50 | PASS — largest deviation from a straight line **0.467 board points** across seven rows, on boards that print integers |
| **T3** separability diagnostic | reported — this checks my analytic pi formula, not the identity, and the identity needs only T2 |
| **T4** round trip | PASS — worst relative error 1.9e-16 over 14,420 vantages |

**Everything in §7, §8 and §9 is an estimate pending a build.** The arithmetic is exact and the
instruments are the committed ones run unchanged. What cannot be done without a build: the engine's
assert wall, the continuity objects, rho32 monotonicity, and the day-0 identity.

---

## 7 · STEP 4 — WHAT THE DERIVED CHARGE DOES. ESTIMATES PENDING A BUILD.

### 7.1 · The age gate, and why it is there

Priced without a gate, the derived charge breaks the veteran caps at **every** level of LAMBDA: churn
9,778 against a 1,002 rail, net −8,196 against 668. The cause is structural — A(g) saturates at 1, so a
141-game row pays about 54% of his pedigree leg where today he pays 0.1%.

The engine's own cap law says the age bar is flat from 24. "Performance against age expectation" has
content below 24 and none at or above it. So the derived charge is applied where that statement has
content, and the existing charge is left in place where it does not:

```
F(g, s, age)  =  1 - exp(-LAMBDA * A(g) * T(s))     if age at the vantage < 24
              =  0.50 * (g/14) * exp(1 - g/14)      otherwise
```

With the gate the veteran pool reads **churn 951 against a 1,002 rail and net −595 against 668 — inside
both, and identical to ORDER K's own 947 / −601.**

### 7.2 · The property test, re-run

Rank correlation with performance surplus, within games bins.

| games bin | n | price response, ORDER K | price response, ORDER N | **charge, ORDER K** | **charge, ORDER N** |
|---|---:|---:|---:|---:|---:|
| 1-4 | 42 | +0.135 | **+0.360** | +0.099 | **−0.747** |
| 5-9 | 33 | +0.261 | **+0.487** | +0.442 | **−0.903** |
| 10-15 | 33 | +0.435 | **+0.524** | +0.226 | **−0.982** |
| 16-24 | 36 | +0.707 | **+0.812** | +0.120 | **−0.995** |
| 25-39 | 29 | +0.787 | **+0.831** | −0.156 | **−1.000** |
| 40-60 | 22 | +0.538 | **+0.569** | −0.436 | **−0.916** |

**The charge is now monotone in performance surplus at every games level.** And the price response
rises most where it was weakest: at 1-4 games from +0.135 to +0.360, at 5-9 games from +0.261 to
+0.487.

Charge paid, by surplus tercile, over the whole young window:

| group | mean surplus | mean games | current | **ORDER N** |
|---|---:|---:|---:|---:|
| below expectation | −21.40 | 10.1 | 34.1% | **75.2%** |
| middle | −6.87 | 17.0 | 38.5% | 69.3% |
| **above expectation** | **+10.99** | 25.4 | 31.2% | **15.1%** |

### 7.3 · The year-1 class

| board | W2 scorer, draft classes 2005-2015 (the registered basis) | vs the 1.03 floor | vs the 1.14 buy rail | cohort clock 2005-2015 |
|---|---:|---:|---:|---:|
| **ORDER N** | **1.0604** | +0.0304 | −0.0796 **PASS** | 1.0324 |
| ORDER K | 1.0513 | +0.0213 | −0.0887 PASS | 1.0324 |
| landing candidate | 1.0421 | +0.0121 | −0.0979 PASS | 1.0232 |
| eta = 0 | 1.2046 | +0.1746 | **+0.0646 FAIL** | 1.1829 |

The cohort mark is identical to ORDER K's to four decimals, which is the anchoring identity doing
exactly what it was solved to do.

### 7.4 · The band tables. BOTH WINDOWS.

Year-0 to year-1 appreciation. **B** = over the +14% buy rail. **S** = below 0%, sell side.

#### PRIMARY window — cohorts 2005-2023

| band | n | **ORDER N** | ORDER K | landing | eta = 0 |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 1200 | +5.94% | +4.23% | +2.98% | +21.72% **B** |
| picks 1-20 | 380 | +13.85% | +9.22% | +8.36% | +30.90% **B** |
| picks 21-64 | 820 | −6.58% **S** | −3.67% **S** | −5.54% **S** | +7.21% |
| **picks 1-10** | 190 | **+16.13% B** | +8.22% | +7.93% | +31.58% **B** |
| picks 11-20 | 190 | +9.44% | +11.16% | +9.20% | +29.58% **B** |
| picks 21-30 | 190 | +2.17% | +5.26% | +2.76% | +19.81% **B** |
| picks 31-40 | 190 | −13.17% **S** | −10.70% **S** | −12.84% **S** | −1.57% **S** |
| picks 41-64 | 440 | −9.99% **S** | −6.89% **S** | −7.88% **S** | +1.71% |

#### MODERN window — cohorts 2019-2023

| band | n | **ORDER N** | ORDER K | landing | eta = 0 |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 311 | **+1.33%** | −0.96% **S** | −1.69% **S** | +15.72% **B** |
| picks 1-20 | 100 | +15.37% **B** | +9.58% | +8.92% | +31.27% **B** |
| picks 21-64 | 211 | −21.33% **S** | −17.97% **S** | −18.83% **S** | −9.39% **S** |
| **picks 1-10** | 50 | **+23.90% B** | +13.65% | +13.24% | +37.46% **B** |
| picks 11-20 | 50 | −0.26% **S** | +2.11% | +1.00% | +19.94% **B** |
| picks 21-30 | 50 | −18.09% **S** | −14.26% **S** | −16.34% **S** | −4.40% **S** |
| picks 31-40 | 50 | −15.44% **S** | −14.27% **S** | −15.92% **S** | −5.46% **S** |
| picks 41-64 | 111 | −29.81% **S** | −25.06% **S** | −23.94% **S** | −18.00% **S** |

**ALL picks 1-64 in the modern window turns positive for the first time** — from ORDER K's −0.96%
sell-red to +1.33%. **And picks 1-10 goes through the buy rail in both windows.** That is the problem
and §8 is about it.

### 7.5 · Where the money moves, whole board

Board total 673,097 → 663,931, **down 9,166 points, −1.36%.** The board gets cooler, not hotter.
291 of 804 rows move: 80 up, 211 down.

| career games | rows | total points | per row |
|---|---:|---:|---:|
| 0 | 89 | 0 | 0.0 |
| 1-4 | 46 | −2,054 | −44.7 |
| 5-9 | 45 | −2,175 | −48.3 |
| 10-15 | 51 | +190 | +3.7 |
| 16-29 | 81 | −983 | −12.1 |
| 30-59 | 103 | −3,050 | −29.6 |
| 60+ | 388 | −1,065 | −2.7 |

| age in 2026 | rows | total points |
|---|---:|---:|
| 20 and under | 158 | −534 |
| **21-23** | 217 | **−8,638** |
| **24 and over** | 429 | **+6** |

The 24-and-over line is the age gate: 429 mature rows move a net six points between them, and that
six points is rounding on rows whose current prices are untouched.

**The ten largest rises and the ten largest falls:**

| move | row | age | games | pick | ORDER K → ORDER N |
|---:|---|---:|---:|---:|---|
| **+883** | Willem Duursma | 19 | 19 | 1 | 3703 → 4586 |
| +788 | Sam Lalor | 20 | 22 | 1 | 3456 → 4244 |
| +711 | Jagga Smith | 20 | 20 | 3 | 3637 → 4348 |
| +666 | Harry Dean | 19 | 17 | 3 | 2403 → 3069 |
| +485 | Sullivan Robey | 19 | 14 | 9 | 2379 → 2864 |
| +452 | Dyson Sharp | 19 | 13 | 13 | 2427 → 2879 |
| +360 | Jacob Farrow | 19 | 18 | 10 | 2155 → 2515 |
| +349 | Cooper Duff-Tytler | 19 | 13 | 4 | 1505 → 1854 |
| +295 | Phoenix Gothard | 21 | 15 | 12 | 1319 → 1614 |
| +254 | Josh Lindsay | 19 | 13 | 19 | 1796 → 2050 |
| −344 | Jhye Clark | 22 | 33 | 8 | 921 → 577 |
| −384 | Daniel Annable | 19 | 2 | 6 | 1537 → 1153 |
| −419 | Zane Duursma | 21 | 38 | 4 | 629 → 210 |
| −453 | Dylan Patterson | 19 | 5 | 5 | 1440 → 987 |
| **−667** | Sid Draper | 20 | 10 | 4 | 1267 → 600 |

**Look at the two ends together.** Every large rise is a 19- or 20-year-old high pick who is well above
his age bar. Every large fall is a high pick who is well below it. That is the mechanism, and none of
those rows was aimed at.

Gameless rows move by exactly zero, which is the `A(0) = 0` law holding. 60-plus rows move by exactly
zero, which is the age gate.

---

## 8 · THE CONFLICT, QUANTIFIED. I AM NOT PICKING FOR YOU.

### 8.1 · The two rails push opposite ways and do not meet

`LAMBDA` is the level. `THETA_R = BETA_sat / LAMBDA` is the tilt. Raising the level cools the board and
weakens the tilt. The full ladder is in `VARIANT_N_out.txt`; the ends of it:

| LAMBDA | THETA_R | zero point | W2 class mark | picks 1-10 PRIMARY | picks 1-10 MODERN | dean | duff-tytler |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.80 | 0.1440 | +9.26 | 1.0618 | +16.34% | +24.16% | 3069 | 1868 |
| **0.821** | 0.1403 | +9.44 | **1.0604** | +16.13% | +23.90% | 3069 | 1854 |
| 1.20 | 0.0960 | +12.73 | **1.0351** | +12.15% | +19.48% | 3069 | 1634 |
| **1.30** | 0.0886 | +13.60 | **1.0280 — floor broken** | +10.91% | +18.40% | 3069 | 1585 |
| 1.80 | 0.0640 | +17.94 | 0.9902 | +4.58% | **+13.25% — rail met** | 2723 | 1389 |

| what needs to be true | the LAMBDA it needs |
|---|---|
| picks 1-10 under +14% in **both** windows | **LAMBDA at or above 1.80** |
| the G1 floor, W2 class mark at or above 1.03 | **LAMBDA at or below 1.20** |
| the veteran caps | every LAMBDA on the ladder |

**The gap is 1.20 to 1.80 and there is nothing in it.**

### 8.2 · A floor under the relief does not close it either

I tried the obvious repair: stop the relief at a floor, so an over-performer pays something rather
than nothing. Twenty-one settings, `FLOOR_N_out.txt`.

| what needs to be true | the floor it needs |
|---|---|
| picks 1-10 under +14% in both windows | TMIN at or above **0.65** |
| the G1 floor | TMIN at or below **0.40** |

**Nothing clears both. Zero rungs of 21.**

### 8.3 · Why, and it is one fact about the population

**The young players above their age bar are the young players taken at the top of the draft.** So
relieving over-performers relieves the top of the draft, and the top of the draft is where the buy rail
has almost no room.

Spearman(pick, surplus) on 3,248 vantage rows: **−0.3303.**

| pick band | rows | median surplus | share at or past the zero point (+9.13) |
|---|---:|---:|---:|
| **1-10** | 584 | **+6.12** | **41.3%** |
| 11-20 | 572 | +0.63 | 26.4% |
| 21-40 | 1015 | −4.78 | 15.7% |
| 41-64 | 888 | −7.60 | 12.5% |

**A pick 1-10 row is 3.3 times as likely to earn full relief as a pick 41-64 row.** That is not the
mechanism being unfair. It is the mechanism being right about who is playing well, landing on the one
cell of the board that had no slack.

And it had no slack before this order:

| board | picks 1-10 PRIMARY, headroom to +14% | picks 1-10 MODERN, headroom |
|---|---:|---:|
| ORDER K | +5.78 | **+0.35** |
| landing candidate | +6.07 | +0.76 |
| candidate 31 | −2.19 | −8.25 |
| dose 0, eta 0.31 | +4.16 | −1.11 |

ORDER M wrote it down in its own words: *"Anything that lifts the top of the draft has less headroom
than the primary table suggests."* This order is the thing that lifts the top of the draft.

The modern picks 1-10 cell carries **50 rows**.

### 8.4 · The three ways out, priced, so you can choose knowingly

**This seat does not recommend one. Each is a ruling, not a calculation.**

**Way 1 — take the mechanism as derived and accept the top-of-draft reading.** LAMBDA 0.821. The
property is fixed at every games level, the class mark holds at 1.0604, the veteran caps hold, all
three sub-expectation rows fall, Dean and Duff-Tytler clear your references. Picks 1-10 reads +16.13%
primary and +23.90% modern. **The cost is explicit: a team buying a top-ten pick and carrying it a
season keeps about 2 points of free money in the primary reading and about 10 in the modern one.**

**Way 2 — hold the primary window and rule that the 50-row modern cell is not binding.** With a relief
floor of TMIN = 0.20 at LAMBDA 0.821: picks 1-10 primary **+13.33%, inside the rail**; W2 class mark
**1.0468**, above the floor; veteran caps inside; ALL 1-64 primary +4.36%. The modern cell still reads
+21.14%. Dean 2,897, Duff-Tytler 1,854, Taylor 927, Annable 1,153, Patterson 987. **This is the only
setting found anywhere in this order that is legal on every standing rail in the primary window.**

**Way 3 — keep ORDER K and accept that below ten games the board barely pays for performance.** Every
rail holds. The property in §3 stays exactly as measured: 7.8 board points per point of surplus at 1-4
games, a charge that reads nothing, and above-bar rows paying nearly twice the charge of below-bar ones
in money.

**What I will not do is present Way 1 as "the ruling delivered".** It delivers the property fix. It
also hands a top-ten pick holder a free 24% in the modern reading.

---

## 9 · THE NAMED ROWS — ILLUSTRATIONS, NEVER TARGETS

**Not one constant in this mechanism was chosen with any of these rows in view.** They are printed last
because you asked to see them, and they are printed wherever the derived rule puts them. If one of them
is in the wrong place, that is a finding about the rule.

At the derived mechanism, LAMBDA 0.821, age gate 24:

| row | age | pick | games | **surplus** | charge now | **charge ORDER N** | landing | ORDER K | **ORDER N** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Harry Dean | 19 | 3 | 17 | **+14.86** | 49.0% | **0.0%** | 2400 | 2403 | **3069** |
| Cooper Duff-Tytler | 19 | 4 | 13 | **+7.06** | 49.9% | 18.4% | 1572 | 1505 | **1854** |
| Xavier Taylor | 19 | 11 | 2 | −13.22 | 16.8% | 38.5% | 1176 | 1162 | **927** |
| Daniel Annable | 19 | 6 | 2 | −19.02 | 16.8% | 45.7% | 1530 | 1537 | **1153** |
| Dylan Patterson | 19 | 5 | 5 | −19.62 | 34.0% | 74.0% | 1467 | 1440 | **987** |
| Isaac Kako | 20 | 13 | 36 | +0.84 | 26.7% | 62.0% | 788 | 832 | **716** |
| Josh Smillie | 20 | 7 | 0 | n/a — no games | 0.0% | **0.0%** | 772 | 772 | **772** |
| Milan Murdock | 26 | pool | 17 | +2.17 | 49.0% | 49.0% — age gated | 170 | 156 | **156** |
| Anthony Scerri | — | — | — | — | — | — | **not on the 804-row board** |

**What the rule did, row by row, and none of it was aimed.**

- **Dean** is 14.9 points a game clear of what a 19-year-old key defender normally produces, with 17
  games of evidence. He is past the zero point, so he pays nothing and keeps his whole pedigree leg.
- **Duff-Tytler** is +7.1, short of the +9.44 zero point, so he pays a reduced 18.4% rather than 49.9%.
- **Taylor, Annable and Patterson** are 13 to 20 points a game *below* their bars. They pay 38.5%, 45.7%
  and 74.0%. **All three fall. This is the first mechanism this project has built that can mark a row
  down** — ORDER M proved kappa cannot, and that eta at zero pushes all three up.
- **Kako** is the one to read carefully, because he shows the rule is not a reward scheme. He is
  producing almost exactly at his age bar, with 36 games — the most evidence of anyone here. The rule
  says: the evidence is in, and it says average. He pays 62.0% and drops from 832 to 716. **Under the
  current rule he pays 26.7% — less than Dean's 49.0% — because 36 games sits on the far side of the
  bump.** That inversion is the defect, and this is what removing it costs him.
- **Smillie** has never played. `A(0) = 0`, so he cannot move. 772 on every board in this order.
- **Murdock** is 26. The age gate leaves him on the existing charge and he does not move.
- **Scerri** is not on the 804-row board and no number is invented for him.

---

## 10 · THE FALSIFIER SCORECARD, INCLUDING THE ONE THAT FIRED

| # | falsifier | fired? |
|---|---|---|
| **N1** | the offline pricing identity fails | **no** — 0.467 board points across six built boards, round trip 1.9e-16 |
| **N2** | the age bar does not reproduce the engine's own | **no** — asserted number by number |
| **N3** | the delivered-value ruler moved | **no** — md5 `241842f6…` on both copies |
| **N4** | the board rewards over-performance, refuting the owner's claim | **FIRED.** The slope is +0.0395, 90% CI [+0.0228, +0.0596], games controlled. Restated in §1 and §3: the claim is wrong as worded and right in substance. |
| **N5** | performance surplus predicts nothing | **no** — positive and significant at every games level, including two games |
| **N6** | performance surplus predicts negatively | **no** — positive everywhere |
| **N7** | pedigree's power rises with evidence | **no** — it falls after 17 games, though not smoothly |
| **N8** | no LAMBDA reproduces the current aggregate charge | **no** — 0.82131 |
| **N9** | the derived charge breaks a structural property | **no** — N-S1 to N-S4 all hold |

**Prereg deviations, declared:** D1 and D2 in §5.2. One addition: a fixed five-year forward window
alongside the preregistered uncapped one (§4.5) — an addition, nothing was removed. One construction
choice named at the time it was made: vantage-year effects in the E2 regression, because censoring is
not constant across the panel.

---

## 11 · WHAT IS OWED, AND WHAT THIS SEAT COULD NOT DO

- **No board was built.** Every number in §7, §8 and §9 is an estimate. The engine's assert wall, the
  continuity objects in age, games and pick, rho32 monotonicity, and the day-0 identity cannot be run
  without a build. A build is the next step and it is not this seat's to take.
- **The mature-row byte-identity gate will break.** ORDER I recorded that any move in the counterweight
  knobs re-prices mature rows. The age gate in §7.1 holds the *current* prices of 24-plus rows exactly,
  and the veteran caps come in inside — but rows now over 24 had younger vantages, and their **paths**
  move. That is disclosed, not hidden, and it is what the J-TOL numbers in §7.1 are measuring.
- **The tall finding in §4.4 is not acted on.** For talls, early production against the age bar carries
  little information at 1-3 games. The derived charge is pooled anyway, because splitting it needs a
  construction choice the sample does not support. A future order could split it; this one names it.
- **The pool arms were not re-tabled.** The age gate leaves most pool rows on the existing charge and
  the ones it touches are young, but the arm tables were not recomputed and should be before anything
  lands.
- **Step 1's sample is 195 rows.** The current-board property test is small. Step 2's 4,143 rows carry
  the derivation; Step 1 carries the diagnosis only.

---

## 12 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_N.md` | the prereg, pushed at `602d40a` before any number existed |
| `on_lib.py` | the shared constructions — the age bar, performance surplus, the house ruler |
| `s4_shootout_COPY.py` | the delivered-value ruler, copied and md5-asserted |
| `on_step1.py` · `STEP1_N.json` · `STEP1_N_out.txt` | the property test on the current board |
| `on_step2.py` · `STEP2_N.json` · `STEP2_N_out.txt` | what performance-vs-age predicts |
| `on_step3.py` · `MECH_N.json` · `STEP3_N_out.txt` | the derivation |
| `on_ident.py` · `IDENT_N.json` · `IDENT_N_out.txt` | the offline pricing identity, falsifier N1 |
| `on_step4.py` · `STEP4_N.json` · `STEP4_N_out.txt` | the ungated pricing |
| `on_sweep.py` · `SWEEP_N.json` · `SWEEP_N_out.txt` | the retained-prior diagnostic and the first ladder |
| `on_variant.py` · `VARIANT_N.json` · `VARIANT_N_out.txt` | the age gate, the LAMBDA ladder, the conflict |
| `on_floor.py` · `FLOOR_N.json` · `FLOOR_N_out.txt` | the relief floor, and why it does not close the gap |
| `on_why.py` · `WHY_N_out.txt` | why the rails do not overlap |
| `on_check.py` · `CHECK_N_out.txt` | every packet table recomputed at the one quoted setting, so nothing is carried across runs |
| `on_class.py` · `CLASS_N.json` · `CLASS_N_out.txt` | ORDER L's class machinery, only the board list changed |
| `on_bands.py` · `BANDS_N.json` · `BANDS_N_out.txt` | ORDER M's band machinery, only the board list changed |
| `on_tables.py` · `TABLES_N.json` · `TABLES_N_out.txt` | the comparison tables |
