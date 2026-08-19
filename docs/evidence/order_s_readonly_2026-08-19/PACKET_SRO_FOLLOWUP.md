# PACKET SRO FOLLOW-UP — THE CREDIT CURVE, THE GRADED RESET, THE COMBINED TAKE, THE INVERSION

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Prereg:** `PREREG_SRO_FOLLOWUP.md`, pushed at `6fab2f8` before any number here existed.
**Extends:** `PACKET_SRO.md` (`6625d53`).

**NO ENGINE FILE WAS EDITED. NO DIAL WAS ADDED. NO BOARD WAS BUILT. NO STORE WAS WRITTEN.
NO PULL REQUEST. NOTHING ON `main`. NOTHING IS ADOPTED. NO FIX IS PROPOSED IN ANY OF THE FOUR.**

Board totals reproduce the built boards exactly: ORDER P **666,434**. Every counterfactual wraps a
function in the loaded namespace only and every one is proved inert at its identity setting.

**Out of scope by instruction: the injury-stream design.** The logged-injured exemption via the
owner-authored LTI register is a live-board wiring question the owner has not ruled on and this seat
does not touch it. **F1 and F2 are reported cause-free** — every curve is a function of the
observable (games, avg-vs-bar) with no absence-cause term — **so a later injured/unexplained split can
re-cut these same populations by cause without re-deriving anything here.**

**Madden, Conway, Barnett and Dowling are exhibits. They gate nothing.**

---

## 0 · THE FOUR VERDICTS, ONE LINE EACH

**F1.** **The wired `min(1, games/2)` credit is too generous and "a 2-game season is a 0-game season"
is too harsh — the measured credit at two games is 0.47 raw and 0.24 guarded, and BOTH 1.00 and 0.00
sit outside the interval.**

**F2.** **A returning season never restores a never-sat comparable — the best-measured return cell
reaches 0.60 of the way back and the neighbourhood of the wired threshold reaches 0.10 — so a FULL
wipe over-credits it; but the step at ten games is NOT separable from a smooth curve on this sample
and the preregistered NULL stands.**

**F3.** **The owner's reframe is confirmed and it runs against this seat's own earlier framing: the
combined take does not overshoot anywhere — it UNDERSHOOTS the measured cost in every depth band, and
in three of four bands even the structural CEILING of both collectors sits below the measured cost.**

**F4.** **The inversion is a thin-cell survivorship artifact of the listed conditioning: the
unconditional row is strictly monotone down on 154 rows at depth 4, the conditioning that creates the
"still listed after four sat years" population is the same operation that cuts that cell to 11, and
on essentially those same 11 rows a change of `v0` basis moves `D(4)` by +29.3% and flips the
ordering.**

---

# F1 · THE CREDIT CURVE

## 1 · WHAT WAS ALREADY MEASURED, AND WHAT IS NEW

**ORDER 30A-2 already ran a games transition** (`sitter_fade_2026-08-14`, T4). It reports `D(k, N)` at
five buckets, at depths 2/3/4, under two listing readings, and its own conclusion was that *"the
0 → 1-2 boundary is a LARGE step but not the largest, and the sequence is NOT monotone, so the
measurement supports neither a clean cliff nor a smooth curve at this resolution."*

**What this seat adds:** a continuous curve in games instead of five buckets, cut by age band and
position class, and put on the same [0,1] scale as the wired credit so the two can be laid side by
side. **Where the buckets overlap, 30A-2 is the control.**

**The ruler differs and that was declared in the prereg, not discovered.** 30A-2 measured on the DV
lane's Layer-1/Layer-2 artifacts; this seat measures on the house S4 ruler (md5 `241842f6…`) that
ORDER N, P, Q and R all used. **Levels do not match. Only the shape is compared.**

**Population.** ND entrants 2005-2019, positive `v0`, force-majeure excluded, on the #338 listing
basis. **Censoring, fixed in advance: entry year 2019 or earlier**, so at least four seasons after
depth 2 sit inside the observed window. **1,068 players.** Depth 2 is the primary cell because there
"seasons 1..N−1" is season 1 alone, so the estimand matches the wired PER-SEASON credit with no
further control.

## 2 · THE CONTROL AGAINST 30A-2 — THE SHAPES AGREE

| games | n here | R(g) here | 30A-2 D(k,2) | n in 30A-2 |
|---|---:|---:|---:|---:|
| 0 | 463 | 0.3290 | 0.5684 | 462 |
| 1-2 | 123 | 0.5601 | 0.9602 | 133 |
| 3-5 | 130 | 0.4241 | 0.8479 | 145 |
| 6-10 | 143 | 0.7788 | 1.4213 | 161 |
| 11+ | 209 | 1.0828 | 1.6242 | 239 |

Monotone across the five buckets? **This seat: NO. 30A-2: NO.** The levels differ by construction; the
0 → 1-2 step is large on both and neither is monotone. **The two rulers agree on the shape.**

## 3 · THE HEADLINE — THE MEASURED CREDIT AGAINST THE WIRED STEP

`c_hat = 0` means a season of `g` games predicts exactly like a season of none. `c_hat = 1` means it
predicts exactly like a season of eleven or more. `c_wired = min(1, g/2)` is what the engine credits.

| games | n | c_hat | 90% CI | c_wired | wired − measured |
|---:|---:|---:|---|---:|---:|
| 0 | 463 | 0.0000 | — | 0.00 | 0.00 |
| 1 | 59 | 0.1287 | [−0.123, +0.405] | 0.50 | +0.37 |
| **2** | **64** | **0.4706** | **[+0.148, +0.877]** | **1.00** | **+0.53** |
| 3 | 52 | 0.0724 | [−0.167, +0.353] | 1.00 | +0.93 |
| 4 | 38 | 0.0743 | [−0.203, +0.410] | 1.00 | +0.93 |
| 5 | 40 | 0.2455 | [−0.133, +0.756] | 1.00 | +0.75 |
| 6 | 26 | 0.5711 | [+0.145, +1.086] | 1.00 | +0.43 |
| 7 | 30 | 0.2250 | [−0.106, +0.634] | 1.00 | +0.78 |
| 8 | 31 | 0.4519 | [+0.082, +0.888] | 1.00 | +0.55 |
| 9 | 25 | 1.0320 | [+0.439, +1.796] | 1.00 | −0.03 |
| 10 | 31 | 0.7716 | [+0.186, +1.552] | 1.00 | +0.23 |
| 11+ | 209 | 1.0000 | — | 1.00 | 0.00 |

**THE PREREGISTERED SQUEEZE, AND BOTH ENDS ARE REJECTED.**

- **`c_hat(2) = 0.4706`, 90% CI [0.148, 0.877], on 64 players.**
- **The wired step says 1.00. It is OUTSIDE the interval. F1-P1 did not fire — the step is not
  vindicated.**
- **"A two-game season is a zero-game season" says 0.00. It is also OUTSIDE the interval.**
- F1-P3, which predicted `c_hat(2) > 0.5`, **FIRED**: 0.4706 is just below. But 0.5 is inside the
  interval, so the two readings cannot be separated. **The measurement says the answer is in between
  and cannot say exactly where.**

**F1-P2 FIRED**: the measured curve reaches or passes the wired step in 1 of the 8 cells over
3 ≤ g ≤ 10 — the g = 9 cell, at 1.032 on 25 players. Everywhere else the step is above the curve.

**F1-P4 did not fire**: the per-integer curve is not monotone, which was preregistered as NOISE and is
reported as noise. The cells hold 25 to 64 players each.

## 4 · THE SAME CURVE, GUARDED — THE READABLE VERSION

The house monotonicity guard (pool-adjacent-violators, increasing — ORDER P's own instrument) applied
to the point estimates above, with a 400-draw band. **This is a way of reading the measurement, not a
proposed schedule.**

| games | c_hat guarded | 90% band | c_wired | wired − guarded |
|---:|---:|---|---:|---:|
| 0 | 0.0000 | [−0.017, +0.000] | 0.00 | 0.00 |
| 1 | 0.1287 | [−0.017, +0.307] | 0.50 | +0.37 |
| **2** | **0.2383** | **[+0.030, +0.418]** | **1.00** | **+0.76** |
| 3 | 0.2383 | [+0.033, +0.418] | 1.00 | +0.76 |
| 4 | 0.2383 | [+0.045, +0.424] | 1.00 | +0.76 |
| 5 | 0.2455 | [+0.082, +0.554] | 1.00 | +0.75 |
| 6 | 0.3857 | [+0.192, +0.648] | 1.00 | +0.61 |
| 7 | 0.3857 | [+0.195, +0.652] | 1.00 | +0.61 |
| 8 | 0.4519 | [+0.230, +0.861] | 1.00 | +0.55 |
| 9 | 0.8879 | [+0.465, +1.117] | 1.00 | +0.11 |
| 10 | 0.8879 | [+0.518, +1.124] | 1.00 | +0.11 |
| 11+ | 1.0000 | — | 1.00 | 0.00 |

**Summed over g = 1 to 10 the wired step sits 5.41 credit-units above the guarded curve — an average
of 0.54 per games level, on a scale where 1.0 is the whole distance from a zero-game season to an
eleven-plus one.** **On the guarded reading 1.00 is outside the band at every g from 1 to 8.**

**The answer to the owner's question in one sentence: a two-game season genuinely clears about a
quarter to a half of the non-selection signal that a ten-game season clears — not all of it, which the
current step assumes, and not none of it either.**

## 5 · THE CUTS — NOTHING SEPARATES

`c_hat` in each cell, with the cell's own n. Every cut re-anchors on its OWN zero-games and
eleven-plus cells, so a level difference between groups cannot leak into the credit scale.

| group | n | g=0 | g=1 | g=2 | g=3-5 | g=6-10 | g=11+ | c_hat(2) 90% CI |
|---|---:|---|---|---|---|---|---|---|
| ALL | 1,068 | 0.000/463 | 0.129/59 | 0.471/64 | 0.126/130 | 0.597/143 | 1.000/209 | [+0.148, +0.877] |
| TALL | 299 | 0.000/159 | −0.083/19 | 0.590/21 | −0.199/30 | 0.478/45 | 1.000/25 | [+0.037, +1.649] |
| SMALL | 769 | 0.000/304 | 0.233/40 | 0.377/43 | 0.246/100 | 0.620/98 | 1.000/184 | [+0.013, +0.823] |
| entry age 18 | 933 | 0.000/421 | 0.222/54 | 0.351/57 | 0.212/112 | 0.676/120 | 1.000/169 | [−0.056, +0.807] |
| entry age 19 | 58 | — | −0.600/1 | 2.038/4 | −0.340/10 | 0.803/10 | 1.000/5 | [−3.862, +10.161] |
| entry age 20+ | 77 | 0.000/14 | −0.119/4 | 0.936/3 | 0.025/8 | 0.442/13 | 1.000/35 | [+0.167, +2.229] |
| KPD | 118 | 0.000/54 | −0.031/7 | 1.151/10 | −0.094/14 | 0.803/19 | 1.000/14 | [+0.068, +3.734] |
| KPF | 121 | 0.000/65 | −0.114/10 | 0.184/8 | −0.103/11 | 0.231/17 | 1.000/10 | [−0.514, +1.526] |
| RUCK | 60 | −0.000/40 | −2.543/2 | −1.664/3 | 2.057/5 | −1.681/9 | 1.000/1 | [−17.16, +9.75] |
| MID | 316 | 0.000/124 | 0.137/20 | 0.048/20 | 0.114/36 | 0.722/39 | 1.000/77 | [−0.296, +0.327] |
| SD | 228 | 0.000/98 | 0.234/9 | 0.670/13 | 0.127/32 | 0.689/28 | 1.000/48 | [−0.025, +2.038] |
| SF | 225 | 0.000/82 | 0.493/11 | 0.645/10 | 0.664/32 | 0.296/31 | 1.000/59 | [−0.879, +2.675] |

**F1-P5 did not fire. No pair of groups separates at g = 2.** The credit a token season buys is not
measurably different by class, by entry age, or by position. **The entry-age-19, entry-age-20+ and
RUCK rows are useless — RUCK's g=1 cell holds 2 players and its g=11+ anchor holds 1 — and they are
printed only so nobody has to wonder whether they were looked at.**

## 6 · DEPTHS 3 AND 4, AND THE SENSITIVITIES

At depths 3 and 4 the scored season is not the player's only prior one, so the cell is CUMULATIVE.
Median prior games are printed so it is not misread as a per-season object.

| depth | games | n | c_hat | median prior games |
|---:|---|---:|---:|---:|
| 3 | 0 | 289 | 0.000 | 0 |
| 3 | 1-2 | 101 | 0.216 | 0 |
| 3 | 3-5 | 119 | 0.424 | 2 |
| 3 | 6-10 | 159 | 0.446 | 3 |
| 3 | 11+ | 336 | 1.000 | 9 |
| 4 | 0 | 255 | 0.000 | 0 |
| 4 | 1-2 | 84 | 0.106 | 6 |
| 4 | 3-5 | 79 | 0.620 | 8 |
| 4 | 6-10 | 142 | 0.352 | 10 |
| 4 | 11+ | 366 | 1.000 | 23 |

**The sensitivities, because F4 shows the mean and the pooled aggregate can disagree on thin cells:**

| reading | n | g=0 | g=1 | g=2 | g=3-5 | g=11+ |
|---|---:|---:|---:|---:|---:|---:|
| primary (mean, entry ≤ 2019) | 1,068 | 0.000 | 0.129 | **0.471** | 0.126 | 1.000 |
| pooled aggregate, same rows | 1,068 | 0.000 | 0.114 | **0.605** | 0.094 | 1.000 |
| mean, entry ≤ 2017 (six seasons) | 926 | 0.000 | 0.081 | **0.480** | 0.105 | 1.000 |
| pooled, entry ≤ 2017 | 926 | 0.000 | 0.042 | **0.662** | 0.013 | 1.000 |
| **the wired step** | | 0.00 | **0.50** | **1.00** | **1.00** | 1.00 |

**`c_hat(2)` runs 0.47 to 0.66 across all four readings. Not one of them reaches 1.00, and not one
falls to 0.00.** The g=1 cell runs 0.04 to 0.13 against a wired 0.50, so **the one-game credit is the
one that is furthest out of line in proportional terms.**

---

# F2 · THE GRADED RESET

## 7 · THE EXHIBIT, CHECKED

The owner's exhibit: 7 games at 78.4 this season counts as delivered and four sat seasons cost zero;
the same row at 5 games does not deliver and sits at depth 3.0 with `D = 0.263`.

**The arithmetic checks out and the reason is the proration.** `o32_delivered` requires
`games >= 10*f`, and `f` for the in-progress season is the calendar fraction. **Measured on the loaded
engine: `f = 0.9200`, so the effective threshold in the current season is 9.20 games, not 10.**
A 7-game season therefore does NOT clear it at this cut — the exhibit holds at an earlier point in the
season, when `f` was under 0.70. **That is a fact about the exhibit, not about the mechanism, and it
is stated so nobody quotes the exhibit at the wrong `f`.** The mechanism the exhibit is about — an
all-or-nothing wipe at a proration-dependent threshold — is exactly as described.

## 8 · THE REVERSAL CURVE ON HISTORY

**Population.** 1,068 ND entrants 2005-2019 with at least three observed depths. A **RETURNER** at
depth N had zero games at depths N−1 and N−2 and then played. A **KEPT-SITTING** row played zero at
N as well. A **NEVER-SAT** row has no zero-game season at any depth up to N. The outcome in all three
is the discounted house-ruler value from depth N+1 onward over `v0` — **so the return season's own
output is not inside the outcome it is scored against.**

| group | rows | mean outcome |
|---|---:|---:|
| RETURNERS | 134 | 0.2339 |
| KEPT SITTING | 760 | 0.0279 |
| NEVER SAT | 1,704 | 0.9626 |

`reversal = 0` at the kept-sitting mean, `reversal = 1` at the never-sat mean. The scale between them
is 0.9347.

### 8.1 Against the games leg — no separable step at ten

| return games | n | reversal | 90% CI | the wired reset credits |
|---|---:|---:|---|---:|
| 1-2 | 38 | 0.1760 | [+0.053, +0.333] | 0.0 |
| 3-5 | 29 | 0.1690 | [+0.030, +0.353] | 0.0 |
| 6-9 | 27 | 0.0944 | [+0.004, +0.214] | 0.0 |
| 10-14 *thin* | 22 | 0.2125 | [+0.054, +0.449] | **1.0** |
| 15+ *thin* | 18 | 0.5959 | [+0.321, +0.886] | **1.0** |

**The cells straddling the threshold overlap:** 6-9 games [0.004, 0.214] against 10-14 games
[0.054, 0.449]. **F2-P4's preregistered NULL is the result. F2-P1 is NOT established: this sample
cannot separate a step at ten from a smooth curve, and this seat does not claim it can.**

**But two things the sample CAN say:**

1. **No cell reaches 1.0.** The best-measured return — 15 or more games — recovers **0.596** of the
   way back to a never-sat comparable, with an interval topping out at 0.886. **A returning season
   does not restore a player who never sat, however convincing it is.**
2. **The whole 10-14 cell reads 0.2125 with an interval of [0.054, 0.449], which excludes 1.0 on 22
   players.** That is the better-powered version of the next test.

### 8.2 The wired threshold point itself

Returners at 10-14 games with a margin inside ±5 points a game of their own bar — the closest
measurable neighbourhood of the wired point (`g = 10, m = 0`):

**n = 5. reversal 0.1049, 90% CI [0.007, 0.217]. The wired reset credits 1.0.**

**F2-P2 did not fire — the interval excludes 1.0. But n = 5 and this seat will not hang a verdict on
five players.** The honest statement is the one from §8.1: the 22-row 10-14 cell also excludes 1.0,
and so does every other cell. **On every reading available, a bare delivered season is measured to buy
far less than a full wipe.**

### 8.3 Against the margin leg — flat at this sample

| margin `m` (points a game vs the row's own bar) | n | reversal | 90% CI |
|---|---:|---:|---|
| below −10 | 70 | 0.1216 | [+0.042, +0.218] |
| −10 to 0 | 32 | 0.3230 | [+0.133, +0.529] |
| 0 to +10 *thin* | 22 | 0.2741 | [+0.067, +0.483] |
| +10 and up *thin* | 10 | 0.4656 | [+0.223, +0.672] |

Below the bar [0.098, 0.276] against at-or-above the bar [0.177, 0.510]: **OVERLAP. F2-P3 FIRED — the
outcome is not separable in `m` at this sample**, though the point estimates rise monotonically from
0.12 to 0.47 across the four bands. **A monotone point sequence with overlapping intervals is a
suggestion, not a result, and it is reported as a suggestion.**

## 9 · THE THRESHOLD CENSUS — EXACT, ON THE BOARD

No estimation in this section. `Y = 2026`, ORDER P dial line, in-progress fraction `f = 0.9200`, so
the current-season threshold is **9.20 games**.

| cell | rows |
|---|---:|
| board rows with a season inside ±2 games of their own threshold | **371** |
| of those, the season delivers today | 120 |
| of those, it does not | 310 |
| rows a −2-game move would flip OUT of delivered | **83** |
| rows a +2-game move would flip INTO delivered | **69** |

**F2-P5 did not fire: the census holds 371 rows, far above the 20 predicted.**

**What the flip is actually worth.** The engine's own `o32_delivered` was wrapped in the loaded
namespace to return the opposite verdict for one row and one season at a time. **Falsifier F2-A1 did
not fire: at the identity setting all 804 board rows reprice bit-identically.**

**132 rows tested. Six move. 201 board points at stake in total, worst single row 107.**

| row | year | games | threshold | flip | board | flipped | delta |
|---|---:|---:|---:|---|---:|---:|---:|
| **Billy Dowling** | 2024 | 9.0 | 10.00 | gains delivered | 162 | 269 | **+107** |
| Callum Coleman-Jones | 2021 | 8.0 | 10.00 | gains delivered | 120 | 169 | +49 |
| Jedd Busslinger | 2026 | 8.0 | 9.20 | gains delivered | 671 | 687 | +16 |
| Jy Farrar | 2025 | 8.0 | 10.00 | gains delivered | 34 | 47 | +13 |
| Matt Carroll | 2026 | 10.0 | 10.00 | loses delivered | 609 | 601 | −8 |
| Elliott Himmelberg | 2020 | 11.0 | 10.00 | loses delivered | 61 | 53 | −8 |

**The cliff is a large population and a small price.** 371 rows sit at it, but only 6 have anything
riding on it, because for the rest the accumulated clock was already zero for another reason or the
fade was not reaching them. **One row — Billy Dowling — carries more than half the total, and he is
the same row F3 finds is the only one of the eight double-priced rows getting close to the right
total. That is a coincidence of one row being at the extreme of two mechanisms at once, and it is
flagged rather than built on.**

---

# F3 · THE COMBINED-TAKE CALIBRATION

## 10 · THE OWNER'S REFRAME, AND THAT IT SUPERSEDES THIS SEAT

**The owner's words, recorded as his:** split collection across mechanisms is NOT a defect; the defect
is an uncalibrated TOTAL.

**`PACKET_SRO.md` §16 and §18 treated the double-pricing as a defect in itself. That framing is
superseded by the owner's, and the supersession is recorded here rather than quietly applied.**
Whether one collector or two collect the absence cost is irrelevant if the total is right.

## 11 · THE MEASURED COST — NOT THE WIRED SCHEDULE

`D_measured(c)` is this seat's own re-measurement of the washout evidence on the house ruler, from F1
§7. **Reading the wired schedule back would be circular and it is not done anywhere in F3.**
Depth `c = 2` means ONE unplayed season.

| depth c | n | D_measured | cost 1 − D | 90% CI of the cost |
|---:|---:|---:|---:|---|
| 2 | 463 | 0.6328 | **0.3672** | [+0.201, +0.513] |
| 3 | 242 | 0.2371 | 0.7629 | [+0.680, +0.836] |
| 4 | 161 | 0.1117 | 0.8883 | [+0.822, +0.947] |
| 5 | 132 | 0.0549 | 0.9451 | [+0.872, +0.994] |

**The first unplayed season already costs 36.7% of delivered value and zero is well outside its
interval. F3-P4's prediction holds on the "materially above zero from depth 2" half.** The other half
cannot be tested: **at depth 1 the cost is zero BY CONSTRUCTION, because depth 1 is the normaliser.
The measurement cannot speak about depth 1 and this seat does not pretend it can.**

## 12 · POPULATION A — THE DOUBLE-PRICED ROWS

`absence_take = (fade + D8 cap) / the row's absence-free price`. **The ORDER P charge is not in the
numerator: it prices production against a bar, not absence.** It is printed beside for visibility.

| row | games | c_u | fade | D8 | charge | board | absence take | measured cost 90% CI | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Liam McMahon | 7 | 5.92 | 35.6 | 3 | 112.6 | 213 | 0.153 | [+0.872, +0.994] | **UNDERSHOOTS** |
| **Billy Dowling** | 13 | 2.50 | 107.1 | 225 | 0.0 | 162 | **0.672** | [+0.495, +0.717] | **APPROXIMATES** |
| Tom Hanily | 12 | 2.00 | 10.3 | 3 | 49.7 | 131 | 0.092 | [+0.201, +0.513] | UNDERSHOOTS |
| Isaac Keeler | 13 | 3.00 | 10.5 | 10 | 87.5 | 128 | 0.138 | [+0.680, +0.836] | UNDERSHOOTS |
| Will McLachlan | 7 | 2.46 | 11.5 | 6 | 51.9 | 114 | 0.133 | [+0.476, +0.705] | UNDERSHOOTS |
| Shadeau Brain | 11 | 3.00 | 66.7 | 5 | 31.5 | 99 | 0.420 | [+0.680, +0.836] | UNDERSHOOTS |
| Kaleb Smith | 12 | 2.92 | 8.7 | 6 | 27.0 | 37 | 0.285 | [+0.656, +0.821] | UNDERSHOOTS |
| Harvey Gallagher | 28 | 2.00 | 10.9 | 1 | 49.6 | 21 | 0.363 | [+0.201, +0.513] | **APPROXIMATES** |

**POPULATION A: UNDERSHOOTS 6, APPROXIMATES 2, OVERSHOOTS 0.**

**F3-P2 did not fire — the population does not overshoot.** And the finding runs directly against
`PACKET_SRO.md`'s own framing: **the one row this seat previously called the worst case of
double-pricing, Billy Dowling, is the ONLY row of the eight that gets close to the measured cost.**
332 board points of absence take on an absence-free price of 494 is 0.672, against a measured cost of
0.613 [0.495, 0.717]. **F3-P3's prediction that he was the one row that could overshoot is refuted:
he approximates.**

## 13 · POPULATION B — THE ZERO-PRICED ROWS

These rows have played no games this season and carry a fade of exactly 1.000. **Two yardsticks are
printed because they answer different questions and merging them would be dishonest.**

- **(i) the cost at the row's OWN unplayed depth.** For every one of these rows `c_u ≤ 1`, and the
  measured curve, like the wired schedule, says **zero**. **On its own clock the row is not being
  under-charged.**
- **(ii) the cost of ONE unplayed season, 0.3672 [0.201, 0.513].** That is what the missed season
  would cost **if the clock counted it**. It does not, because the row's earlier played seasons and
  his last delivered season have already reset and credited it away.

Against yardstick (ii): **UNDERSHOOTS 18, APPROXIMATES 1.**

**F3-P1 FIRED**, and on a detail worth having: **Clay Hall is the one exception, at an absence take of
0.484, because although his sitter fade is 1.000 the D8 production cap takes 367 board points off him.
A different mechanism picks the absence up on exactly one of the nineteen.** Lance Collard is a
partial second, at 0.109 from the same source.

**The size of the gap, on yardstick (ii): if the missed season were charged at the measured cost of
one unplayed season, these 19 rows would carry about 7,139 board points less between them, against a
board of 666,434.** **That is an arithmetic consequence of the measurement and NOT a proposal. This
seat is not saying the clock should count that season. It is saying what the number is.**

## 14 · THE MIDDLE — EVERY ROW THE FADE ACTUALLY REACHES

| c_u band | rows | median absence take | measured cost | 90% CI | verdict on the median |
|---|---:|---:|---:|---|---|
| 1-2 | 18 | 0.167 | 0.613 | [+0.495, +0.717] | **UNDERSHOOTS** |
| 2-3 | 59 | 0.111 | 0.613 | [+0.495, +0.717] | **UNDERSHOOTS** |
| 3-4 | 39 | 0.276 | 0.837 | [+0.761, +0.907] | **UNDERSHOOTS** |
| 4+ | 15 | 0.319 | 0.922 | [+0.849, +0.982] | **UNDERSHOOTS** |

**Nowhere does the combined take overshoot.**

## 15 · THE DENOMINATOR PROBLEM, AND THE STRUCTURAL CEILING

**This section must be read before §14 is quoted.** The two numbers compared there have different
denominators. **The measured cost is a fraction of DELIVERED VALUE. The absence take is a fraction of
BOARD PRICE.** A row's price already carries a production leg that is low for its own reasons, so the
gap in §14 is not simply "the dial is set too low".

**The question that makes it meaningful: what is the MOST the absence mechanisms could take on this
row, at any setting?** The sitter fade multiplies only the `(1 − rho)` share of the pedigree leg. Drive
`D` to zero and that whole share goes; nothing more can. Add the D8 cap at its measured size and that
is the ceiling.

| c_u band | rows | median take | **median CEILING** | measured cost | 90% CI |
|---|---:|---:|---:|---:|---|
| 1-2 | 18 | 0.167 | **0.545** | 0.613 | [+0.495, +0.717] |
| 2-3 | 59 | 0.111 | **0.422** | 0.613 | [+0.495, +0.717] |
| 3-4 | 39 | 0.276 | **0.542** | 0.837 | [+0.761, +0.907] |
| 4+ | 15 | 0.319 | **0.704** | 0.922 | [+0.849, +0.982] |

**In three of four bands the CEILING sits below the lower limit of the measured cost.**

**That is a structural finding, not a dial finding.** In those bands no setting of the sitter fade and
no size of the D8 cap can collect the measured cost of the absence, **because the collectors act on a
share of the price that is smaller than the cost is.** Scaling the split — the remedy the owner's
reframe points at when a total overshoots — cannot close a gap of this kind. **This seat proposes
nothing. It reports that the lever and the gap are different sizes.**

**And the limitation that cuts the other way, stated as plainly.** A row whose absence has already
depressed his PRODUCTION leg has paid for it somewhere these attributions do not count, because `rho`
and the production estimate are not absence mechanisms and were not read as such. **The §14 gap is
therefore an UPPER bound on the shortfall, not a point estimate.**

---

# F4 · THE SCHEDULE INVERSION

## 16 · THE ROW, IN THREE VINTAGES

The engine literal `O31_FADE_D` is asserted equal to `FADE_31F.json::wired` at every depth.
**Falsifier F4-A1 did not fire.**

| vintage | D(1) | D(2) | D(3) | D(4) | depth 3 → depth 4 |
|---|---:|---:|---:|---:|---|
| ORDER A / R1, the previously ruled row | 1.0000 | 0.5502 | 0.2628 | 0.3460 | **INVERTS (+0.0832)** |
| **ORDER 31-F re-derived — LIVE AND WIRED** | 1.0000 | 0.5583 | 0.2748 | 0.3973 | **INVERTS (+0.1225)** |
| ORDER 30A-2 L-B as filed | 1.0000 | 0.5684 | 0.3600 | 0.3073 | monotone down (−0.0527) |

**The order quoted the R1 row. The live row is the 31-F one. Both invert, so nothing here turns on
which vintage is quoted — but the third row is the same conditioning on the same population under a
different `v0` basis, and it does NOT invert.**

## 17 · n PER DEPTH CELL

`FADE_31F.json::cells`, as filed:

| depth | n | n_ever | n_zero | mean | median | p25 | p75 | POOLED | tail share |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,142 | 1,021 | 121 | 0.9955 | 0.1411 | 0.0006 | 1.1954 | 1.0583 | 0.0999 |
| 2 | 464 | 343 | 121 | 0.5558 | 0.0028 | 0.0000 | 0.2993 | 0.5812 | 0.0807 |
| 3 | 100 | 67 | 33 | 0.2735 | 0.0013 | 0.0000 | 0.1293 | 0.2438 | 0.1019 |
| **4** | **11** | **9** | **2** | **0.3955** | **0.0807** | **0.0273** | **0.3588** | **0.2468** | **0.3262** |
| 5 | 2 | 2 | 0 | 0.6991 | 0.6991 | 0.4338 | 0.9644 | 0.7820 | 0.5458 |
| 6 | 1 | 1 | 0 | 1.4018 | 1.4018 | 1.4018 | 1.4018 | 1.4018 | 0.0923 |

**The wired value is the cell MEAN normalised by the depth-1 mean, verified rather than assumed:
0.2735/0.9955 = 0.274786 = the wired D(3), and 0.3955/0.9955 = 0.397271 = the wired D(4), both to
1e-16.**

**F4-P1 did not fire: the depth-4 cell holds 11 observations, of which 2 are exact zeros.**

**F4-P4 FIRED — every published statistic on the cell inverts in the same direction**, but the sizes
say something the direction alone hides:

| statistic | depth 3 | depth 4 | difference |
|---|---:|---:|---:|
| mean | 0.2735 | 0.3955 | **+0.1219** |
| median | 0.0013 | 0.0807 | +0.0794 |
| p25 | 0.0000 | 0.0273 | +0.0273 |
| p75 | 0.1293 | 0.3588 | +0.2295 |
| **POOLED aggregate** | **0.2438** | **0.2468** | **+0.0030** |

**On the pooled aggregate — the sum of delivered value over the sum of `v0` on the same rows — the
inversion is 2.5% of the mean-based inversion. The two summaries of the same eleven rows disagree by a
factor of forty.**

## 18 · THE COMPARISON THAT DECIDES IT

| reading | D(1) | D(2) | D(3) | D(4) | depth 3 → 4 | n at 2 / 3 / 4 |
|---|---:|---:|---:|---:|---|---|
| **UNCONDITIONAL (ORDER 30A)** | 1.0000 | 0.5684 | 0.2143 | 0.1052 | **monotone down (−0.1091)** | 462 / 234 / **154** |
| L-A reconstruction as filed | 1.0000 | 0.5684 | 0.3435 | 0.4630 | **INVERTS (+0.1195)** | 462 / 146 / **35** |
| L-B outcome-blind floor | 1.0000 | 0.5684 | 0.3600 | 0.3073 | monotone down (−0.0527) | 462 / 100 / **11** |

**The unconditional row is strictly monotone down at every depth and has no inversion anywhere, on
154 rows at depth 4.** **The conditioning that creates the "still listed after four sat years"
population is the SAME operation that empties the cell: 154 → 35 → 11.**

**F4-P2 is confirmed in direction and refined in mechanism.** The inversion is absent unconditioned
and present under conditioning — but it is not present under BOTH conditioned readings as filed.
**It takes the conditioning AND the 31-F `v0` re-basis together to produce the row the engine
carries.**

**F4-P3 is confirmed: "real survivorship feature" and "thin cell" are not alternatives here. They are
the same operation.** The 11 players at depth 4 under L-B genuinely are a special population — that is
what "still listed after four sat years" means — and there are 11 of them.

## 19 · THE STABILITY CHECK THAT SETTLES IT

| `v0` basis | D(3) | D(4) | depth 3 → depth 4 |
|---|---:|---:|---|
| 30A-2, as filed | 0.3600 | 0.3073 | monotone down (−0.0527) |
| **31-F, head-fixed `v0` — THIS IS THE LIVE ROW** | 0.2748 | 0.3973 | **INVERTS (+0.1225)** |

**On essentially the same eleven rows, changing the `v0` basis moves `D(4)` by +29.3% and flips the
ordering against depth 3.** `FADE_31F.json`'s own drift column records the pattern: **0.0513 at depth
4, 0.0120 at depth 3, 0.0081 at depth 2 — the drift grows as the cell empties.**

**And where it ends:** depth 5 holds 2 rows and depth 6 holds 1, and their re-derived values are
0.7023 and **1.4081** — a player who sat six years measured as delivering 40% MORE than his entry
price. **The schedule is held flat from depth 4 precisely so those two rows never price anything, and
that is the engine's own `O31_FADE_FLAT_FROM = 4`.**

## 20 · IS A CI RECOVERABLE? NO, AND NONE IS INVENTED

**The per-observation ratios behind each depth cell are not published.** `FADE_31F.json` files summary
statistics only, and `SITTER_DISCOUNT_TABLE_2.json`'s per-player block carries career aggregates but
not the per-depth `V_from_N` share. **A bootstrap CI on the depth-4 cell cannot be recomputed from the
artifacts and this seat is not inventing one.**

**What IS recoverable, distribution-free:** n = 11, of which 2 are exact zeros; IQR [0.0273, 0.3588];
median 0.0807; **mean 0.3955, which is 4.9 times the median, so the cell is carried by its upper
tail**; and a tail share of 0.3262 against 0.1019 at depth 3 and 0.0807 at depth 2, **so the depth-4
estimate also leans hardest of the three on PROJECTED rather than observed value.** With eleven
observations the published p25 and p75 are the 3rd and 9th ordered values; **any interval printed here
would be a statement about three data points.**

**ORDER 30A-2 scored this itself, in its own prereg, and it is quoted rather than re-discovered:**

- **Q6 BREACHED** — `n_LB(3) = 100 ; n_LB(4) = 11` (30A unconditional 234 / 154)
- Q5 HELD — `n_LB(5) = 2 ; n_LB(6) = 1` (expected 0)
- Q10 HELD — `extrapolated_L-B = True` (deepest resolved depth 4)

**NO SMOOTHING IS PROPOSED AND NO REPLACEMENT ROW IS DERIVED.**

---

## 21 · THE FALSIFIER SCORECARD

| # | falsifier | fired? |
|---|---|---|
| **F1-P1** | 1.0 lies inside the `c_hat(2)` interval (the wired step vindicated) | **no** — [+0.148, +0.877] raw, [+0.030, +0.418] guarded; 1.0 outside both |
| **F1-P2** | the measured curve reaches or passes the wired step over 3 ≤ g ≤ 10 | **FIRED** — 1 of 8 cells (g = 9, n = 25) |
| **F1-P3** | `c_hat(2) < 0.5` | **FIRED** — 0.4706, though 0.5 is inside the interval |
| **F1-P4** | the per-integer curve is monotone | **no** — it is not, and that was preregistered as noise |
| **F1-P5** | some pair of cuts separates at g = 2 | **no** — no pair separates |
| **F2-P1** | a step at ten fits better than a smooth curve | **not established** — the straddling cells overlap |
| **F2-P2** | the interval at the wired threshold contains or exceeds 1.0 | **no** — [0.007, 0.217] on n = 5, and [0.054, 0.449] on the 22-row cell |
| **F2-P3** | the outcome is flat in `m` at fixed `g` | **FIRED** — the intervals overlap |
| **F2-P4** | any cell comparison across the threshold is separable | **no** — **the preregistered NULL is the result** |
| **F2-P5** | the ±2-game census holds fewer than 20 board rows | **no** — 371 rows |
| **F2-A1** | the `o32_delivered` wrapper is not inert at identity | **no** — all 804 rows bit-identical |
| **F3-P1** | all 19 zero-priced rows undershoot | **FIRED** — 18 undershoot, 1 approximates (Clay Hall, via the D8 cap) |
| **F3-P2** | population A overshoots | **no** — 6 undershoot, 2 approximate, 0 overshoot |
| **F3-P3** | Billy Dowling overshoots | **refuted** — he APPROXIMATES, and is the closest of the eight |
| **F3-P4** | the measured cost is indistinguishable from zero at depth 2 | **no** — 0.3672 [0.201, 0.513] |
| **F4-P1** | the depth-4 cell holds 30 or more observations | **no** — 11 |
| **F4-P2** | the unconditional row inverts too | **no** — it is strictly monotone down |
| **F4-P3** | the depth-4 cell is thin under both conditionings, or large under both | **no** — 154 unconditioned against 11 conditioned |
| **F4-P4** | every published statistic on the depth-4 cell inverts in the same direction | **FIRED** — they all do, but the pooled one by 2.5% of the mean's gap |
| **F4-A1** | the engine literal is not the artifact's row | **no** — equal at every depth |

**Prereg deviations, declared.** Nothing was removed. Three additions: the guarded (isotonic) reading
of the F1 curve in §4, printed beside the raw points and labelled as a reading rather than a schedule;
the structural-ceiling section of F3 (§15), which the prereg did not name and which materially changes
how §14 must be read; and the exhibit's proration check in §7.

---

## 22 · EVERY LIMITATION

**F1.** In-sample against a censoring cutoff of entry year 2019, so the most recent six draft classes
are excluded entirely and nothing here speaks to them. Per-integer cells hold 25 to 64 players. The
entry-age-19, entry-age-20+ and RUCK cuts are useless and are printed only for completeness. The
credit scale is anchored on a `g ≥ 11` cell that itself holds 209 players. The estimand compares
players who played `g` games with players who played none — **it is a selection comparison, not a
causal one, and the same objection applies to the wired schedule it is being compared against.** The
ruler differs from 30A-2's and only the shape is comparable.

**F2.** The returner population is 134 rows across four depths and every threshold cell is thin; the
`g = 10-14, |m| ≤ 5` neighbourhood holds five players. The step-versus-curve question is **NOT
answered** and the null is reported as a null. The outcome window requires two observed seasons after
the return, which censors recent returns. The reversal scale is anchored on two group means, so a
composition difference between returners and never-sat rows enters it. The board census is exact but
is one as-of year at one in-progress fraction — **at a different `f` the current-season threshold
moves and so does the population at the cliff.**

**F3.** **The denominator asymmetry in §15 is the central limitation and it is stated in the packet
body, not here.** The measured cost is a fraction of delivered value; the take is a fraction of board
price. The §14 gap is an upper bound. `D_measured` at depth 1 is zero by construction, so the
zero-priced pocket cannot be scored on its own clock. The two populations are 8 and 19 rows. Yardstick
(ii) for population B assumes the missed season would be counted as one unplayed season, which is a
counterfactual about the clock, not a measurement of it.

**F4.** Everything is read from published artifacts; nothing was re-derived. **No CI is recoverable
and none is given.** The depth-4 comparison rests on 11 rows under one conditioning and 154 under
another, and the two conditionings are not nested populations of the same thing — L-B is an
outcome-blind listing floor and the unconditional row makes no listing assumption at all. **Whether
the listing conditioning is the right one is a ruled question this seat does not reopen.**

---

## 23 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_SRO_FOLLOWUP.md` | the prereg addition, pushed at `6fab2f8` before any number existed |
| `os_f1.py` · `FOLLOWUP_F1.json` · `FOLLOWUP_F1_out.txt` | F1 — the credit curve, the cuts, the deeper depths, the sensitivities, and the retention curve F3 calibrates against |
| `os_f2.py` · `FOLLOWUP_F2.json` · `FOLLOWUP_F2_out.txt` | F2 — the reversal curve and the threshold census |
| `os_f3.py` · `FOLLOWUP_F3.json` · `FOLLOWUP_F3_out.txt` | F3 — the combined-take calibration and the structural ceiling |
| `os_f4.py` · `FOLLOWUP_F4.json` · `FOLLOWUP_F4_out.txt` | F4 — the inversion, provenance and sample |
| `os_f1_run.txt` · `os_f2_run.txt` · `os_f3_run.txt` · `os_f4_run.txt` | the raw console of every run, engine banners included |

`os_lib.py` (the wide recorder) is carried over unchanged from the first packet.

**Nothing in this directory is adopted, nothing lands, and none of the four proposes a fix.**
