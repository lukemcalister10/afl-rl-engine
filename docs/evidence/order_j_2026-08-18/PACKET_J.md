# PACKET J — THE GATE WAS WRONG. IT IS NOW RIGHT. THE ANSWER STILL CHANGED.

**Seat:** ORDER J. **Authority:** issue #334 comment **5320813582**. **Prereg:** `PREREG_J.md`, pushed
before this order read a single dose result. **Base:** the landing candidate **1f176444**.

**Nothing lands on this seat's word.**

---

## 0 · THE ANSWER IN TEN SHORT LINES

1. **Order I's headline finding was wrong, and this order overturns it.** Order I said the owner's own
   laws contradict each other. They do not.
2. **G1, G2 and G3 can all be satisfied at the same time.** 96 settings out of 408,240 do it. Another
   634 do it in the finer search. Order I's "factor of seven with no overlap" was caused by its own
   frozen counterweight, not by the laws.
3. **But a joint setting still does not exist**, because a fourth law blocks it: the mature-row law.
4. **The corrected gate did not rescue the counterweight.** Under the new, generous tolerance, 0 of 34
   single-knob moves pass and 0 of 16 joint settings pass.
5. **The reason is now a number instead of a wall.** The counterweight has real free play: eta may
   move ±0.004, kappa ±0.006, gamma_u ±0.28, gamma_d ±0.15, relief ±0.021. The owner's laws need
   moves **10 to 25 times larger**.
6. **The price is 2.2%.** The cheapest setting that satisfies the owner's laws needs some veterans
   repriced by **2.22% of their own value**. The gate allows 0.5%. That is the whole gap.
7. **"Rounding-level" was a size illusion.** Order I's worst-row numbers looked tiny because they were
   read as absolute points on a board where the big rows are worth thousands. The rows the
   counterweight actually moves are **not** the big rows. Billy Cootee is worth 257 board points. At
   the cheapest law-satisfying setting he moves 5.61 of them — **2.19% of him**. At the smallest knob
   step anyone has tested he still moves 1.24% of himself.
8. **The aggregate caps were never the problem.** At the reference setting the total churn is 106.5
   board points against a cap of 1,001.87, and the net is −106.3 against a cap of 667.91. It is
   entirely a per-row question.
9. **The owner-ruled tall factor is wired, verified and disclosed.** The redistribution identity
   residual is **−1.110e-16**, rebuilt from Order H's own 408 fitted sitters. Entry values are
   bit-identical on 89 of 89.
10. **HALT.** No candidate is carried. The trade-off curve is printed in §6 so the owner can choose.

---

## 1 · WHAT THIS ORDER WAS ASKED TO FIX

Order I used one test for two different mechanisms. The test was: **no row aged 24 or over may move at
all.**

For the age surface that test is right. The age surface is switched off from age 24 by construction.
A mature row cannot move unless something has leaked. Order I found three leaks that way and fixed
them. Those fixes are kept.

For the counterweight that test is wrong. The counterweight keys on **career games**, not on age. A
27-year-old with 141 games sits on the same reliability curve a 19-year-old with 141 games sits on.
Move the curve and the 27-year-old moves too. Zero was never achievable. Demanding it was demanding
that the mechanism not exist.

The owner named this himself when he commissioned this order. So this order wrote a new tolerance,
wrote down why, pushed it, and only then looked at any result.

---

## 2 · THE NEW TOLERANCE, AND WHY IT IS THE SIZE IT IS

Everything below is in **board points**. That is the unit the published board prints. The engine's
internal number is divided by 1.0524, the owner-ruled re-denomination scalar, to get it.

Facts about the base board, measured before the rule was written:

| object | number |
|---|---:|
| active priced rows | 804 |
| board total | 667,913.3 board points |
| rows aged 24 or over | **429** |
| what those 429 are worth together | 362,703.0 (54.30% of the board) |
| median value of one of them | 258.2 |
| how many are worth under 200 | **176 of 429** |

**The rule, called J-TOL.** A counterweight setting passes only if all three hold:

| clause | the test | the number |
|---|---|---:|
| **(a) per row** | every mature row moves by at most `min(25, max(1, 0.5% of his value))` | 0.5% |
| **(b) churn** | the sum of every mature row's movement, ignoring sign, stays under 0.15% of the board | **1,001.87** |
| **(c) net** | the mature pool's total, with sign, moves less than 0.10% of the board | **667.91** |

**Why 0.5% per row.** The owner states his own targets to the nearest hundred board points. He says
"dean around 2,600", "duff-tytler around 1,800", "smillie in the 700s". Half of one percent of a row
is a tenth of the grain he uses to say what a player is worth. It is also about sixty times inside the
instrument's own uncertainty: the hindsight weight has a 90% confidence band of [0.3117, 0.5560]
around 0.4127.

**Why a percentage and not a flat number of points.** Twenty points on a 4,500-point veteran is
invisible. Twenty points on a 30-point fringe veteran is a two-thirds repricing. 176 of the 429 rows
are worth under 200 points. Only a percentage is fair at both ends.

**Why the 1-point floor.** The published board prints whole numbers. One point is the smallest thing
it can show. Holding a 30-point veteran to 0.15 of a point holds him to a number the board cannot
display. **The floor makes the gate more generous, not less** — and the rows it protects still fail
the 0.5% clause anyway, so it changed no verdict.

**Why the 25-point ceiling.** The owner has already told us where "acceptable" sits. He ruled the tall
factor in knowing its largest single mature move is about 39 board points. This gate caps the gated
mechanism at 25. **The gate this seat set is tighter, per row, than a movement the owner has already
accepted on the exempt lever.**

**Why two aggregate caps.** A per-row cap alone can be beaten by nudging every row a little in the
same direction. That is exactly what "silently repricing veterans" means. The net cap catches a
systematic drift. The churn cap catches movement that cancels out. Both are measured against the board
total, because the harm is a shift in the board's balance between old and young.

**They are not decorative.** If every mature row moved its full allowance under (a), the churn would
come to roughly 2,100 points. The churn cap is 1,001.87 — about half of that. Both clauses bite.

---

## 3 · THE FIRST RESULT: THE OWNER'S LAWS DO NOT FIGHT EACH OTHER

Order I searched one axis, because its gate had frozen the other five. This order searched all six.

408,240 grid points. After the ruled constraints — the reliability curve must stay monotone, the price
must not jump at the bar, the hindsight weight must stay inside its confidence band, the calibration
slope must stay inside its band, and no single draft class may pass the ruled 1.139 no-arbitrage line
— **216 points survive**.

Of those 216:

- **96 satisfy G1, G2's "materially improve" and G3 at the same time.**
- 0 satisfy G2's *aspiration* that no sell-red band remains.

A finer search around that region, 119,700 points, found **634** that satisfy the same three laws.

**So Order I's central claim is overturned.** There is no contradiction between G1, G2 and G3. Order
I's "G1 needs 0.25, G3 caps at 0.08, G2 needs 0.58 to 0.80" was an artifact of a counterweight its own
gate had frozen. Unfreeze the counterweight and the three laws sit together comfortably.

**What is genuinely out of reach, and why.** G1's *ideal* class mark of 1.08 cannot be reached at any
tolerance. The blocker is not the mature law. It is the **ruled 1.139 single-class no-arbitrage line**,
which kills 331,170 of the 408,240 grid points on its own. The best class mark anywhere inside the
ruled constraints is **1.0519**. Reaching 1.08 needs a setting whose worst single class is 1.1687 —
**0.030 over the ruled line**.

---

## 4 · THE SECOND RESULT: THE MATURE-ROW LAW IS WHAT BLOCKS THE BUILD

Measured on the live board, at stage 6, store-wide, on all 429 rows aged 24 or over, with the
owner-ruled tall factor switched **off** so every movement here belongs to S1 and the counterweight
alone.

### 4.1 · S1 passes the zero test, at every dose

| dose | mature rows that move | worst |
|---:|---:|---:|
| 0.10 / 0.15 / 0.25 / 0.35 / 0.45 / 0.70 / 1.00 | **0 of 429, every one** | **0.0000** |

Seven doses, zero rows, zero movement. Falsifier F1 does not fire. The age lever is clean.

### 4.2 · The counterweight fails, at every setting the laws need

**0 of 34 single-knob moves pass. 0 of 16 joint settings pass.** Every one fails on clause (a), the
per-row cap. Almost none fail on churn or net.

The smallest steps, with the rows that break:

| move | rows moved | over cap | churn (cap 1,001.87) | net (cap 667.91) | needs |
|---|---:|---:|---:|---:|---:|
| eta 0.41 → 0.42 | 426 | 12 | 63.4 ok | −63.4 ok | **1.56%** |
| kappa 0.24 → 0.26 | 423 | 17 | 87.5 ok | +16.9 ok | **2.03%** |
| gamma_u 11 → 12 | 425 | 16 | 113.1 ok | +20.3 ok | **1.79%** |
| gamma_d 14 → 13 | 426 | 54 | 221.3 ok | +177.9 ok | **3.32%** |
| relief 1.08 → 1.00 | 19 | 10 | 38.1 ok | −38.1 ok | **3.38%** |

### 4.3 · Why "3.35 points is rounding-level" was wrong

This is the correction that matters most, and it is a correction to what the owner was told.

At eta 0.41 → 0.42 — the smallest step anyone tested — the worst-moving veterans are these:

| veteran | age | what he is worth | how far he moves | as a share of himself |
|---|---:|---:|---:|---:|
| Billy Cootee | 24 | 256.6 | −3.18 | **−1.24%** |
| Mani Liddy | 24 | 153.0 | −2.39 | **−1.56%** |
| Conor Stone | 24 | 224.2 | −2.33 | −1.04% |
| Saad El-Hawli | 25 | 89.0 | −1.39 | **−1.56%** |
| Jack Watkins | 26 | 80.7 | −1.20 | **−1.49%** |

The counterweight does not land on the thousand-point players. It lands on veterans worth 80 to 260
points, and on those men a "rounding-level" 3-point move is one and a half percent of everything they
are worth. Twelve rows are over the cap at the smallest step tested.

### 4.4 · The free play, measured

The counterweight is **not pinned**, as Order I concluded. It moves. Here is how far. These are
**derived by linearity** from the measured ladder — mature movement is very nearly proportional to the
distance from the wired point, so the admissible step is the tested step divided by how many times its
worst row exceeded its cap. They are estimates of the edge, not measured points on it, and they are
labelled as such:

| knob | wired at | may move by (derived) | the laws need |
|---|---:|---:|---|
| kappa | 0.24 | **±0.0059** | ±0.04 to ±0.06 |
| eta | 0.41 | **±0.0040** | +0.015 to +0.09 |
| gamma_u | 11.0 | **±0.279** | −1.0 to −3.0 |
| gamma_d | 14.0 | **±0.153** | −0.5 to −2.0 |
| relief | 1.08 | **±0.021** | (invisible to the instrument — see §7) |

The measured points either side of those edges are in `JTOL_J.json`: every tested step fails, and the
repair point itself passes at zero movement.

### 4.5 · The cheapest law-satisfying setting, priced exactly

Point: `lambda_S1 = 0.10, kappa = 0.240, gamma_u = 10.5, eta = 0.425, gamma_d = 14.0, relief = 1.08`.

| clause | reading | cap | verdict |
|---|---:|---:|---|
| (a) per row | 21 of 429 rows over their cap; worst row needs **2.22%** | 0.5% | **FAIL** |
| (b) churn | **106.5** | 1,001.87 | ok |
| (c) net | **−106.3** | 667.91 | ok |

And the control that proves the gate is not simply impossible: **the repair point itself passes J-TOL
exactly** — 0 of 429 rows move, 0.0000 worst. A frozen counterweight passes. A useful one does not.

---

## 5 · THE OWNER-RULED TALL FACTOR — WIRED, VERIFIED, DISCLOSED

R-TALLFACTOR is adopted. It is exempt from every gate. Exempt does not mean unexamined.

**Verified.**

- `h_TALL` on the wire is −0.6921227120657417. Order H's file says −0.6921227120657417. Deviation
  **exactly zero**.
- `s_norm'` on the wire is 1.4284052406915069. Order H's file says the same. Deviation **exactly zero**.
- The curve reproduces Order H's published exponent table at all eleven picks. Worst deviation
  **0.0e+00**.
- **The redistribution identity, rebuilt from Order H's own 408 fitted sitters** — the same count H
  itself prints — gives a residual of **−1.110e-16** against H's published −1.11e-16. **The total fade
  the board charges is unchanged.** This factor only moves fade between talls and smalls.
- `m_TALL` is **0.645** on the wire over picks 1-64 and **0.677** on Order H's own averaging. Both are
  printed. Neither is a constant the engine uses.

**Its two declared side effects, with numbers.**

1. The 0.5 clip binds for talls over picks **1 to 24** and for smalls over picks **1 to 9**. Over that
   range the clip, not the fit, sets the price. The flat spot ends abruptly at pick 25.
2. The identity is pinned, so **late small sitters pay for the talls' relief**. A small at pick 64
   goes from Order D's exponent 1.1533 to 1.4527.

**Its movement, disclosed in full.** 54 of 429 mature rows move. Total movement 453.6 board points —
0.068% of the board. Net +110.8. 23 up, 31 down. Largest up **Nick Bryan +41.5**. Largest down **Luke
Beecken −32.2**. Every one of the 54 is named with age, pick, value and move in `TALL_J_out.txt` §6
and in `TALL_J.json`.

**One line the owner needs to see, and it is not comfortable.** Measured on the same ruler J-TOL
applies to the gated mechanism, **44 of those 54 rows would exceed the cap**. Reef McInnes moves 42.5%
of his own value. Joel Hamling 40.5%. Callum Coleman-Jones 33.0%. Liam McMahon 21.6%.

The two mechanisms have different shapes, and both facts are true at once:

- The ruled factor touches **54** veterans, hard, and they are almost all **sitters** — men who have
  never played, whose price *is* the sitting discount. That is the mechanism doing precisely what it
  was ruled in to do.
- The counterweight touches **426 of 429** veterans, gently, including men who play every week and
  have nothing to do with sitting.

This seat does not say which is worse. It puts them on one ruler and hands the owner both numbers.

**Day-0.** `derived_v0`, the raw entry object the walk-forward matrix writes as year-0, is
**bit-identical on 89 of 89 at tolerance zero**. Entry values do not move. Falsifier F4 does not fire.
The **printed** day-0 price moves on 89 of 89, 32 up and 57 down, largest up **Mitchell Marsh 429 →
524**, largest down **Ben Camporeale 149 → 116**. That is because a day-0 price for a man who has
never played *is* his entry value multiplied by the sitting discount, and this factor changes that
discount for talls. The stored reference is regenerated per board and the regeneration is disclosed
here, exactly as Order D disclosed the same thing when its own pick-curve fade landed.

---

## 6 · THE TRADE-OFF CURVE — SO THE OWNER CAN CHOOSE, NOT BE TOLD "IMPOSSIBLE"

### 6.1 · What each level of veteran movement buys

The admissible counterweight move scales with the tolerance. Best laws reachable at each level:

| allow veterans to move up to | best class mark | picks 31-40 | picks 41-64 |
|---|---:|---:|---:|
| **0.5% (the gate)** | **nothing satisfies the laws** | — | — |
| 1.0% | **nothing satisfies the laws** | — | — |
| 1.5% | **nothing satisfies the laws** | — | — |
| **2.0%** | 1.0510 | −8.33% | −7.26% |
| 3.0% | 1.0495 | −8.27% | −7.26% |
| 4.0% | 1.0492 | −8.14% | −7.01% |
| 5.0% | 1.0484 | −8.13% | −6.76% |
| 7.5% | 1.0468 | −8.08% | −6.47% |
| 10.0% | 1.0468 | −8.03% | −6.32% |
| *the landing candidate today* | *1.0421* | *−10.46%* | *−7.30%* |

**Read the bottom half of that table carefully. The returns are almost flat.** Going from 2% veteran
movement to 10% — five times the disturbance — buys 0.30 points on picks 31-40 and 0.94 points on
picks 41-64. **Relaxing the gate does not unlock the aspiration.** Nothing anywhere inside the ruled
constraints gets picks 41-64 above −5.31% or picks 31-40 above −8.07%. Neither reaches zero.

### 6.2 · What the class mark can reach

| class mark floor | best late band reachable | the setting |
|---|---:|---|
| 1.030 | −8.07% | dose 0.00, kappa 0.30, gu 8, eta 0.50, gd 12 |
| 1.045 | −8.18% | dose 0.10, kappa 0.28, gu 8, eta 0.50, gd 12 |
| 1.050 | −8.45% | dose 0.15, kappa 0.24, gu 11, eta 0.45, gd 14 |
| **1.055 and above** | **unreachable inside the ruled constraints** | — |

### 6.3 · With the counterweight frozen, the dose alone reaches nothing

| dose | class mark | worst single class | against the ruled 1.139 line |
|---:|---:|---:|---|
| 0.00 | 1.0420 | 1.1279 | ok |
| 0.10 | 1.0551 | 1.1428 | **over** |
| 0.25 | 1.0788 | 1.1687 | **over** |
| 0.55 | 1.1369 | 1.2398 | **over** |

**With the counterweight frozen at the repair point, the ruled 1.139 line permits no S1 dose at all.**
Order I's carried dose of 0.25 was itself outside that ruled line, at 1.1687.

---

## 7 · A MEASURED FACT ABOUT THE RELIEF KNOB THAT WAS NOT KNOWN BEFORE

The selection relief `lambda_rel` is **invisible to the calibration instrument**. It reaches only
**5 of the 1,986** rows in the walk-forward population, because the relief only applies where the fade
is under 1 and the selection signal is non-zero, and those two conditions almost never coincide in the
historical classes. Every relief value from 0.80 to 1.30 gives the identical class mark to four
decimal places.

So the relief cannot be calibrated on history at all. It acts on today's board sitters. It has to be
decided on board evidence. Under J-TOL it may move by ±0.021, because it moves 19 to 40 mature rows
directly.

---

## 8 · EVERY GATE, PRINTED WITH ITS NUMBER

Two columns, never mixed:

- **ORDER J RULED** = the owner-ruled tall/small sitter factor alone. Board **d1058fe0**.
- **ORDER J REFERENCE** = the cheapest law-satisfying setting. Board **73bb064c**. **It fails J-TOL. It
  is NOT carried. Nothing lands.**

| gate | what it asks | RULED | REFERENCE | verdict |
|---|---|---|---|---|
| **G1** | class cohort grows; floor 1.03, ideal ~1.08, under the 1.14 rail | 1.0421 → **1.0420** | 1.0421 → **1.0510** | RULED **FAILS** "grows" by 0.0001. REFERENCE **PASSES the floor**, is well under the rail, and **does not reach the ideal** |
| **G2** | picks 31-40 and 41-64 materially improve | 31-40 −12.84% → **−11.11%** (+1.73) · 41-64 −7.88% → **−8.62%** (**−0.74**) | 31-40 → **−10.59%** (+2.25) · 41-64 → **−7.68%** (**+0.20**) | RULED **FAILS on 41-64** — it gets worse. REFERENCE improves 31-40 materially; **+0.20 on 41-64 is not material** |
| **G2** | aspiration: no sell-red band | picks 21-64, 31-40, 41-64 all still red | same three still red | **FAIL** on both, and unreachable anywhere in the searched space |
| **G3** | no band or arm over +14% | worst band **+10.37%** (11-20) | worst band **+11.34%** (11-20) | **PASS on the bands, both columns** |
| **G3** | the inherited SSP breach | SSP **+50.40%** | SSP **+52.35%** | **INHERITED**, declared in the prereg, reported separately, not created here and not cured here |
| **G4** | dean ≈ 2,600 | 2400 → **2400** | 2400 → **2412** | **BOTH FAIL** — short by 200 and 188 |
| **G4** | duff-tytler ≈ 1,800 | 1572 → **1572** | 1572 → **1569** | **BOTH FAIL** — short by 228 and 231 |
| **G5** | xavier-taylor must not rise | 1176 → **1176** | → **1175** (−1) | **HOLDS** |
| **G5** | daniel-annable must not rise | 1530 → **1530** | → **1536** (**+6**) | **FAIL on the reference** |
| **G5** | dylan-patterson must not rise | 1467 → **1467** | → **1469** (**+2**) | **FAIL on the reference** |
| **side** | josh-smillie holds the ~700s | 772 → **851** | → **851** | **LEAVES the 700s**, and the entire move is the owner-ruled factor. Disclosed, not gated. Pre-declared in the prereg |
| **J-TOL** | the counterweight | exempt lever, not gated | 21 of 429 over cap; needs **2.22%** | **FAIL — the reference is not carried** |
| **S1 zero** | mature rows byte-identical | 0 of 429 at seven doses | 0 of 429 | **PASS** |
| **F1** | any mature row moves under S1 alone | — | 0 rows, 0.0000 | **does not fire** |
| **F3** | dial-off reproduces 1f176444 | `1f17644445f074d11e631b5cbae98a9a` | same | **PASS** |
| **F4** | derived_v0 bit-identical 89/89 | 89 of 89 | 89 of 89 | **PASS — does not fire** |
| **F5** | tall identity residual under 1e-9 | **−1.110e-16** | same | **PASS** |
| **F6** | continuity in age, games, pick | monotone and continuous at every searched point | same | **PASS** |
| **F7** | no point satisfies everything jointly | — | — | **FIRES — this is the halt** |
| **F8** | a sub-expectation row rises | none on the ruled board | annable +6, patterson +2 | **FIRES on the reference**, reported by name |
| **F9** | determinism ×2 | d1058fe0 twice | — | **PASS** |

**The instrument overturn, declared in advance and now reported.** PREREG_J §3.3 registered that the
calibrator navigates and the standing extended-338 decides. It decided differently. On the calibrator
the reference improved both late bands. On the standing instrument picks 41-64 improved by only 0.20
points. **The standing instrument wins and the overturn is printed here.**

---

## 9 · THE PREREG SCORECARD — 11 OF 16

Scored on the reference board, the only one with all three levers live.

**One correction to the automated scorer, made against this seat's own favour.** `o37_gates.py` scores
milan-murdock a HIT because the prereg predicted he would move and he moved. But the prereg made a
second claim about him — that he would move **inside J-TOL** — and that claim is **wrong**. He is worth
169.8 board points, so his cap is 1.00, and he moves **1.64**. The prediction is scored a **MISS** here
and the scorecard reads **11 of 16**, not the 12 the script prints.

| row | predicted | actual | landing | RULED | REFERENCE | hit? | why |
|---|---|---|---:|---:|---:|---|---|
| harry-dean | UP | UP | 2400 | 2400 | 2412 | HIT | above his own age bar by 14.9 a game |
| cooper-duff-tytler | UP | DOWN | 1572 | 1572 | 1569 | **MISS** | his S1 gain is smaller than the counterweight's charge at this dose |
| xavier-taylor | DOWN | DOWN | 1176 | 1176 | 1175 | HIT | below his age bar with games |
| daniel-annable | DOWN | UP | 1530 | 1530 | 1536 | **MISS** | the counterweight cannot move far enough to charge him |
| dylan-patterson | DOWN | UP | 1467 | 1467 | 1469 | **MISS** | same reason |
| oskar-taylor | UP | UP | 596 | 611 | 611 | HIT | zero games — only the ruled fade reaches him |
| josh-smillie | UP | UP | 772 | 851 | 851 | HIT | the 0.5 clip at small picks 1-9 |
| chris-scerri | UP | UP | 313 | 313 | 319 | HIT | pool row, small pedigree, production dominates |
| thomas-burton | UP | UP | 309 | 309 | 316 | HIT | same channel, weaker |
| milan-murdock | moves, **inside J-TOL** | moves −2, and **outside** J-TOL (1.64 against a cap of 1.00) | 170 | 170 | 168 | **MISS** | he does sit inside the re-mix's zone, but 17 games at a value of 170 puts him over the per-row cap |
| will-green | UP | UP | 483 | 624 | 624 | HIT | the ruled factor at pick 16 |
| toby-conway | UP | UP | 855 | 941 | 940 | HIT | the ruled factor at pick 24 |
| steely-green | DOWN | DOWN | 80 | 76 | 76 | HIT | a late small pays for the talls' relief |
| isaac-kako | UP | UP | 788 | 788 | 799 | HIT | S1 on a high-reliability row |
| alix-tauru | UP | DOWN | 920 | 920 | 918 | **MISS** | the counterweight's charge outweighs a small S1 gain at dose 0.10 |
| jedd-busslinger | UP | UP | 579 | 632 | 631 | HIT | S1 plus the ruled fade |

**Four of the five misses share one cause.** duff-tytler, annable, patterson and tauru are all
settings-level, not mechanism-level: at a dose of 0.10 the S1 lift is small, and the counterweight's
charge — which the prereg predicted would fall on sub-expectation rows — is capped so tightly by J-TOL
that it cannot separate them. Annable and Patterson rise for the same reason Order I found: there is
not enough counterweight to charge them. The prereg said so in advance and marked it "FLAT-to-UP if
J-TOL pins it".

**The fifth miss is a miss about the gate itself, and it is the more useful one.** This seat predicted
murdock would move inside J-TOL. He does not. That is a small, direct demonstration of §4.3: a
26-year-old worth 170 board points is exactly the size of row the counterweight lands on hardest in
relative terms, and exactly the size the "rounding-level" reading overlooked.

---

## 10 · THE STANDARD TABLES

Instruments run whole and unmodified: the **extended-338** five-band table, committed md5
`d59ad550116ebbe3d90ed82becd2c4d5`, and the **all-arm** cohort instrument in both windows. Verified at
run: `0f8220351c64c56ccfa90c60edcdfa5f`, `d59ad550116ebbe3d90ed82becd2c4d5`, `02dcf28c…`.

Full output is in `STANDING_TABLES_J_out.txt`. The band table:

```
-- ND BANDS (extended-338 disclosed instrument; years 0..7 as mean-ratio vs the same-set yr0) --

[O35FINAL  LANDING CANDIDATE 1f176444 (Order D) — the base]
  band                  n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
  ALL picks 1-64     1200   1.000   1.030   1.143   1.325   1.468   1.517   1.494   1.321     +2.98%   +11.02%        ok
  picks 1-20          380   1.000   1.084   1.187   1.355   1.527   1.550   1.482   1.317     +8.36%    +5.64%        ok
  picks 21-64         820   1.000   0.945   1.073   1.277   1.376   1.465   1.513   1.326     -5.54%   +19.54%  SELL-RED
  ----------------------------------------------------------------------------------------------------------------
  picks 1-10          190   1.000   1.079   1.179   1.360   1.521   1.503   1.424   1.247     +7.93%    +6.07%        ok
  picks 11-20         190   1.000   1.092   1.203   1.345   1.538   1.642   1.593   1.456     +9.20%    +4.80%        ok
  picks 21-30         190   1.000   1.028   1.182   1.418   1.599   1.610   1.687   1.459     +2.76%   +11.24%        ok
  picks 31-40         190   1.000   0.872   0.941   1.255   1.249   1.394   1.298   1.162    -12.84%   +26.84%  SELL-RED
  picks 41-64         440   1.000   0.921   1.073   1.152   1.256   1.375   1.518   1.329     -7.88%   +21.88%  SELL-RED

[O37TALL  ORDER J / R-TALLFACTOR — the OWNER-RULED tall/small factor ALONE (lambda_S1 = 0)]
  band                  n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
  ALL picks 1-64     1200   1.000   1.036   1.149   1.330   1.471   1.518   1.495   1.321     +3.57%   +10.43%        ok
  picks 1-20          380   1.000   1.089   1.192   1.358   1.529   1.551   1.482   1.318     +8.91%    +5.09%        ok
  picks 21-64         820   1.000   0.951   1.082   1.285   1.380   1.467   1.514   1.327     -4.87%   +18.87%  SELL-RED
  ----------------------------------------------------------------------------------------------------------------
  picks 1-10          190   1.000   1.081   1.181   1.361   1.522   1.503   1.425   1.247     +8.15%    +5.85%        ok
  picks 11-20         190   1.000   1.104   1.214   1.352   1.544   1.644   1.594   1.458    +10.37%    +3.63%        ok
  picks 21-30         190   1.000   1.039   1.193   1.427   1.601   1.611   1.688   1.459     +3.91%   +10.09%        ok
  picks 31-40         190   1.000   0.889   0.959   1.268   1.256   1.399   1.301   1.163    -11.11%   +25.11%  SELL-RED
  picks 41-64         440   1.000   0.914   1.071   1.153   1.258   1.377   1.519   1.330     -8.62%   +22.62%  SELL-RED

[O37REF  ORDER J DISCLOSED REFERENCE — FAILS J-TOL, NOT CARRIED (d0.10 k0.240 gu10.5 e0.425 gd14.0)]
  band                  n     yr0     yr1     yr2     yr3     yr4     yr5     yr6     yr7     apr0-1   buy-mgn   verdict
  ALL picks 1-64     1200   1.000   1.044   1.161   1.341   1.479   1.522   1.494   1.321     +4.40%    +9.60%        ok
  picks 1-20          380   1.000   1.098   1.204   1.369   1.537   1.555   1.482   1.318     +9.76%    +4.24%        ok
  picks 21-64         820   1.000   0.959   1.094   1.297   1.388   1.471   1.514   1.326     -4.07%   +18.07%  SELL-RED
  ----------------------------------------------------------------------------------------------------------------
  picks 1-10          190   1.000   1.089   1.192   1.372   1.530   1.507   1.424   1.247     +8.94%    +5.06%        ok
  picks 11-20         190   1.000   1.113   1.226   1.364   1.552   1.649   1.594   1.458    +11.34%    +2.66%        ok
  picks 21-30         190   1.000   1.048   1.206   1.440   1.610   1.616   1.687   1.459     +4.82%    +9.18%        ok
  picks 31-40         190   1.000   0.894   0.969   1.279   1.262   1.401   1.300   1.163    -10.59%   +24.59%  SELL-RED
  picks 41-64         440   1.000   0.923   1.085   1.166   1.266   1.381   1.518   1.329     -7.68%   +21.68%  SELL-RED

-- THE MOVE, BAND BY BAND (O37TALL minus the landing candidate) --
  band                candidate      O37TALL         move   verdict move
  ALL picks 1-64         +2.98%       +3.57%       +0.59   ok -> ok
  picks 1-20             +8.36%       +8.91%       +0.54   ok -> ok
  picks 21-64            -5.54%       -4.87%       +0.66   SELL-RED -> SELL-RED
  picks 1-10             +7.93%       +8.15%       +0.22   ok -> ok
  picks 11-20            +9.20%      +10.37%       +1.17   ok -> ok
  picks 21-30            +2.76%       +3.91%       +1.15   ok -> ok
  picks 31-40           -12.84%      -11.11%       +1.73   SELL-RED -> SELL-RED
  picks 41-64            -7.88%       -8.62%       -0.74   SELL-RED -> SELL-RED

-- THE MOVE, BAND BY BAND (O37REF minus the landing candidate) --
  band                candidate       O37REF         move   verdict move
  ALL picks 1-64         +2.98%       +4.40%       +1.42   ok -> ok
  picks 1-20             +8.36%       +9.76%       +1.40   ok -> ok
  picks 21-64            -5.54%       -4.07%       +1.47   SELL-RED -> SELL-RED
  picks 1-10             +7.93%       +8.94%       +1.01   ok -> ok
  picks 11-20            +9.20%      +11.34%       +2.14   ok -> ok
  picks 21-30            +2.76%       +4.82%       +2.06   ok -> ok
  picks 31-40           -12.84%      -10.59%       +2.25   SELL-RED -> SELL-RED
  picks 41-64            -7.88%       -7.68%       +0.20   SELL-RED -> SELL-RED
```

**The pool arms, both windows, all eight arms plus ALLPOOL, are printed in full in
`STANDING_TABLES_J_out.txt`.** The primary-window summary:

```
-- THE MOVE, ARM BY ARM (primary window; O37TALL minus the landing candidate) --
  arm           candidate      O37TALL         move   verdict move
  RD               -2.21%       -4.39%       -2.18   SELL-RED -> SELL-RED
  UNR             -42.06%      -42.31%       -0.25   SELL-RED -> SELL-RED
  IRE             +13.51%       +9.29%       -4.22   ok -> ok
  PDA             -18.33%      -22.20%       -3.87   SELL-RED -> SELL-RED
  PDN             -37.81%      -41.47%       -3.66   SELL-RED -> SELL-RED
  SSP             +50.52%      +50.40%       -0.12   BUY-RED -> BUY-RED
  PDS             -25.47%      -28.87%       -3.41   SELL-RED -> SELL-RED
  ALLPOOL          -3.91%       -6.06%       -2.15   SELL-RED -> SELL-RED

-- THE MOVE, ARM BY ARM (primary window; O37REF minus the landing candidate) --
  arm           candidate       O37REF         move   verdict move
  RD               -2.21%       -3.56%       -1.35   SELL-RED -> SELL-RED
  UNR             -42.06%      -42.34%       -0.28   SELL-RED -> SELL-RED
  IRE             +13.51%      +10.88%       -2.63   ok -> ok
  PDA             -18.33%      -21.44%       -3.11   SELL-RED -> SELL-RED
  PDN             -37.81%      -41.14%       -3.33   SELL-RED -> SELL-RED
  SSP             +50.52%      +52.35%       +1.83   BUY-RED -> BUY-RED
  PDS             -25.47%      -28.20%       -2.73   SELL-RED -> SELL-RED
  ALLPOOL          -3.91%       -5.22%       -1.32   SELL-RED -> SELL-RED
```

**A cost worth naming.** The ruled tall factor makes the **RD** pool arm worse by 2.18 points and the
**IRE** arm worse by 4.22. Those arms are not on the 1-64 pick curve, and the movement reaches them
through the shared sitter fade. It is a real cost of the ruled change and it is reported here rather
than left in the appendix.

**The entry-year control passes on both columns** — every year-0 band cell is inside ±0.1% of the
landing candidate. Year-1 moves by design.

---

## 11 · THE MOVERS LEDGER AND THE PREVIEW PAGES

**Boards:** live `88ce647f` · Candidate 31 `fe6be9d6` · landing candidate `1f176444` · **ORDER J RULED
`d1058fe0`** · ORDER J REFERENCE `73bb064c` · leg S1 `69bf858e`.

**Board totals:** live 752,429 · C31 666,913 · landing 667,916 · **RULED 669,231** · REFERENCE 671,186.

The ruled factor moves **216 of 804** rows, 50 of them aged 24 or over. The reference moves **449 of
804**, 90 of them aged 24 or over.

| row | age | pick | g | live | C31 | landing | RULED | REFERENCE | leg tall | leg S1 | leg re-mix |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Harry Dean | 19 | 3 | 17 | 2577 | 2670 | 2400 | 2400 | 2412 | +0 | +38 | −26 |
| Cooper Duff-Tytler | 19 | 4 | 13 | 1561 | 1832 | 1572 | 1572 | 1569 | +0 | +15 | −18 |
| Xavier Taylor | 19 | 11 | 2 | 802 | 1288 | 1176 | 1176 | 1175 | +0 | +3 | −4 |
| Oskar Taylor | 19 | 15 | 0 | 629 | 529 | 596 | 611 | 611 | +15 | +0 | +0 |
| Daniel Annable | 19 | 6 | 2 | 1395 | 1633 | 1530 | 1530 | 1536 | +0 | +9 | −3 |
| Dylan Patterson | 19 | 5 | 5 | 1628 | 1675 | 1467 | 1467 | 1469 | +0 | +9 | −7 |
| Josh Smillie | 20 | 7 | 0 | 953 | 459 | 772 | 851 | 851 | +79 | +0 | +0 |
| Chris Scerri | 20 | — | 7 | 459 | 232 | 313 | 313 | 319 | +0 | +5 | +1 |
| Thomas Burton | 19 | — | 5 | 439 | 213 | 309 | 309 | 316 | +0 | +5 | +2 |
| Milan Murdock | 26 | — | 17 | 208 | 187 | 170 | 170 | 168 | +0 | +0 | −2 |
| Will Green | 21 | 16 | 1 | 604 | 338 | 483 | 624 | 624 | +141 | +1 | −1 |
| Toby Conway | 23 | 24 | 6 | 503 | 729 | 855 | 941 | 940 | +86 | +1 | −2 |
| Steely Green | 22 | 55 | 43 | 150 | 60 | 80 | 76 | 76 | −4 | +0 | +0 |
| Isaac Kako | 20 | 13 | 36 | 1413 | 806 | 788 | 788 | 799 | +0 | +14 | −3 |
| Alix Tauru | 20 | 10 | 18 | 1684 | 1005 | 920 | 920 | 918 | +0 | +8 | −10 |
| Jedd Busslinger | 22 | 13 | 15 | 916 | 469 | 579 | 632 | 631 | +53 | +5 | −6 |

The legs are **real boards**, each built on its own. They do not sum to the total. The residual carries
the interaction and is shown rather than hidden. The full 804-row ledger, the top movers up and down
for both columns, and the age profiles are in `docs/ledgers/ORDER_J_MOVERS.json` and
`LEDGER_J_out.txt`.

**The year-1 class on the 2026 board:** 120 rows. Under the ruled factor, 58,060 → **57,897**
(−0.28%), 18 up and 37 down. Under the reference, 58,060 → **58,257** (+0.34%), 55 up and 60 down.

**Both preview pages are in the standing formats:** `PREVIEW_J_PLAYERS.html` (all 804 rows, five board
columns and the three legs) and `PREVIEW_J_YEAR1.html` (the year-1 class in draft order with v0). The
reference column is labelled **NOT CARRIED** on the pages themselves.

---

## 11a · WHERE THIS ORDER DEPARTED FROM ITS OWN PREREG, DECLARED

Three departures. None of them loosened anything.

1. **PREREG_J §3.4 step 5 said the gate would be run on the top 40 points by the selection law.** It
   was run on **all 16**, because the 96 law-satisfying coarse points collapse to 16 distinct
   `(dose, kappa, gamma_u, eta, gamma_d)` settings once the relief axis is removed — and the relief
   axis is inert on that instrument (§7). So the whole law-satisfying set was gated, not a top slice.
   The refinement pass's cheapest point and its two runners-up were gated as well
   (`o37_jtol_ref.py`).
2. **PREREG_J §4 predicted xavier-taylor, annable and patterson DOWN, with the caveat "FLAT-to-UP if
   J-TOL pins it".** J-TOL did pin it. Two of the three rose. Both readings are on the scorecard and
   the prediction is scored as written, not as caveated.
3. **A board was built at a setting that fails the gate.** That is deliberate and it is labelled on
   every artifact that carries it — the packet, the ledger, both preview pages and the standing
   tables all say **FAILS J-TOL, NOT CARRIED**. It exists because the owner cannot price a trade-off
   he can only see on the calibrator, and because the calibrator turned out to be wrong about picks
   41-64 (§8). It is not a candidate and nothing about it is proposed for landing.

---

## 12 · WHAT THIS SEAT DOES NOT SAY

- It does not carry a setting. The region is empty under the preregistered gate and nothing is landed.
- It does not amend J-TOL. The rule was pushed before the first result and it stands as written, and
  it stands whether or not that is convenient.
- It does not recommend relaxing the gate. It prints the exchange rate — 2.22% per veteran for the
  cheapest law-satisfying setting — and shows that going further buys almost nothing.
- It does not say the tall factor should or should not have been ruled in. It is ruled in. This seat
  wires it, verifies it, and discloses every row it touches, including the 44 rows that would have
  failed the gate the other lever must pass.
- It does not decide whether the day-0 regeneration is acceptable. That is the owner's ruling. It is
  disclosed with its numbers.
- It does not propose relaxing G3's +14% line or the ruled 1.139 line. Those are the owner's.
- It does not re-open smillie's fade. His rise to 851 is reported with its mechanism named.

---

## 13 · REPRODUCTION

Lane on every run: `PATH=/root/rl_venv312/bin:$PATH`, `PYTHONHASHSEED=0`,
`OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_NUM_THREADS=1`, `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25
RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22`, `RL_V0SURF_PKL=data/v0surf.pkl`. Engine runs
strictly sequential; one tag, one directory, one run.

| step | script | output |
|---|---|---|
| the base-board facts | `o37_baseline.py` | `BASELINE_J.json` |
| **the prereg, pushed first** | `PREREG_J.md` | — |
| the joint sweep, 408,240 points | `o37_sweep.py` | `SWEEP_J_out.txt` |
| the feasible region and trade-off | `o37_region.py` | `REGION_J.json` |
| **J-TOL, store-wide, stage 6** | `o37_mature_gate.py` | `JTOL_J.json`, `JTOL_RAW.json` |
| why it fails, row by row | `o37_whyfail.py` | `WHYFAIL_J_out.txt` |
| the declared refinement pass | `o37_refine.py` | `REFINE_J.json` |
| J-TOL on the reference point | `o37_jtol_ref.py` | `JTOL_REF_J.json` |
| the ruled tall factor, disclosed | `o37_tall_disclose.py` | `TALL_J.json` |
| the five boards | `build_all37.sh` (wraps `bb37.sh`) | `BUILD_J_out.txt` |
| the day-0 guards | `o37_day0.py` | `DAY0_J_TALL.json`, `DAY0_J_REF.json` |
| the walk-forward matrices | `run_emit_o37.sh` | `EMIT_O37TALL_out.txt`, `EMIT_O37REF_out.txt` |
| the standing instruments | `bb_noarb37.sh` → `bb_standing_tables37.py` | `STANDING_TABLES_J_out.txt` |
| the board gates | `o37_gates.py` | `GATES_J.json` |
| the movers ledger | `o37_ledger.py` | `docs/ledgers/ORDER_J_MOVERS.json` |
| both preview pages | `o37_pages.py` | `PREVIEW_J_*.html` |

**Instrument controls, all exact and re-run in every script that uses them:**

- the rebuilt corrected age-fair surface reproduces `REMIX_32R.json` at deviation **0.00e+00** on W, on
  every game cell and on every tercile;
- the vectorised calibrator equals Order I's own scalar implementation to **9.1e-13** over 12 random
  grid points × 1,986 rows;
- the landing candidate reproduces the Order-D class mark of record **1.0421**;
- the in-process dial-off baseline is **exact on 429 of 429** mature rows and on all 804 rows against
  the independently measured `BASELINE_J.json`.

---

*— ORDER J. The gate was corrected. The counterweight is still blocked, but now by a number the owner
can price rather than a wall. Nothing lands on this seat's word.*
