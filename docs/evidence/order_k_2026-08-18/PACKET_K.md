# PACKET K — WHAT WAS BUILT, WHAT IT READS, AND WHAT IS STILL WRONG

**Seat:** ORDER K, the build seat. **Authority:** issue #334 comment 5321546243.
**Prereg:** PREREG_K.md, pushed at commit `cdc9042`, before the first engine edit.
**Decision board:** `f3101883a60b0a7b8cb50f9d8a5abfff`. **Base:** the landing candidate `1f176444`.

**Nothing here is adopted. Nothing lands on this seat's word.**

---

## 1 · THE HEADLINE, BEFORE ANY DETAIL

Three things you should read first.

**One. The floor fix worked, completely.** No small player is made lighter by the tall factor. Not at
any pick. Not on any row. Josh Smillie is back at **772**, which is the exact number the prereg
predicted before the board was built. All four talls you named keep their relief in full.

**Two. The built numbers are not the predicted numbers, and I am saying so up front.** You chose this
setting on a table that read class 1.0519, picks 1-10 +7.58%, 11-20 +13.82%, 31-40 −8.54%, 41-64
−6.50%. Those came off the fast navigation instrument, and they were computed on the fade curve with
the defective floor still in it. The real board, on the standing instrument, reads **1-10 +8.22% ·
11-20 +11.16% · 21-30 +5.26% · 31-40 −10.70% · 41-64 −6.89%**. Every one of those is better than the
landing candidate. None of them is the predicted number. Section 4 separates the two causes.

**Three. Two gates are breached, and I have not traded either of them away.** Daniel Annable rises
by 7 points when your law says he must not rise. And the veteran-movement cap is breached on its net
measure, by 27 board points. Both are in section 6, with their numbers.

---

## 2 · THE DEFECT, AND WHAT WAS DONE ABOUT IT

### 2.1 · What was wrong

A player who sits out a year gets a discount applied to his price. The size of that discount is set by
an exponent that depends on his draft pick.

The number the discount is raised to is below 1. That matters. It means a **higher** exponent is a
**heavier** discount, and a **lower** exponent is a **lighter** one. This is the whole defect in one
sentence, so read it twice.

Your tall/small factor gave talls a lighter discount and made smalls pay for it. That is what you
ruled and it is correct on the average. But the two curves involved were fitted separately and they
have different slopes. Below pick 19 the small curve fell **below** the pooled curve it replaced. So a
small drafted at pick 7 came out **lighter**, not heavier. He was being paid by a relief meant only
for talls.

There was a hard floor at 0.5 on that exponent. It did not cause the problem and it did not fix it.
It clipped the small curve part-way back toward where it should have been and then stopped, leaving
the inversion in place.

**Seven real players were affected, worth 126 board points between them.**

| player | position | pick | landing | Order J | gain |
|---|---|---:|---:|---:|---:|
| Josh Smillie | MID | 7 | 772 | 851 | **+79** |
| Will Brodie | MID | 9 | 791 | 812 | +21 |
| Oskar Taylor | SD | 15 | 596 | 611 | +15 |
| Campbell Chesser | MID | 14 | 332 | 338 | +6 |
| James Leake | SD | 17 | 457 | 459 | +2 |
| Tom Brown | SD | 17 | 507 | 509 | +2 |
| Sam Sturt | SF | 17 | 77 | 78 | +1 |

### 2.2 · The fix, in one sentence

**A small player's floor is no longer the number 0.5. It is his own pre-factor exponent — the value
the discount would have charged him if the tall factor did not exist.**

That makes your acceptance test structural. A small cannot be made lighter, because his floor is the
value he started from. There is no tolerance in it, no special case for picks 6 to 18, and no player's
name anywhere in the mechanism.

Talls keep the [0.5, 2.0] clip they were ruled with. `h_TALL` is unchanged at −0.6921227120657417.

### 2.3 · What the fix cost

The tall/small factor is pinned: it moves fade between groups, it does not change the total fade the
board charges. So charging smalls at picks 6 to 18 properly means giving something back elsewhere.

The normalising constant rises from 1.4284052407 to **1.4340996146**, a move of 0.40%. That was
re-solved on Order H's own 408 fitted sitters, with the new floor inside the constraint. The
redistribution identity still holds exactly: residual **−1.1e-16** against the ruled depth-2 fade
0.5582775.

The effect of that 0.40% is that late talls end up with slightly **more** relief, not less. At pick 64
a tall goes from +11.40% to +11.65%. Talls at picks 1 to 25 are on the 0.5 floor either way and do not
move at all.

### 2.4 · Two other routes were considered and rejected, and here is why

**Re-solving the normalisation with the clip inside the constraint set.** This is a no-op, and I
proved it rather than assumed it. Order H's solve already carried the clip. Re-solving it in this seat
reproduces 1.4284052406915069 to the last bit. The small curve's problem is its slope, not its level,
and no level change can fix a slope.

**Applying the factor after the clip.** This throws away Order H's fitted small slope and carries your
ruled `h_TALL` onto a curve it was never fitted against. That would change what `h_TALL` means. It is
a re-optimisation of something you ruled, and this seat is not permitted to make one.

### 2.5 · Where the floor still binds, and for whom

- **Talls sit on the 0.5 hard floor over picks 1 to 25.** That is 117 rows on the 2026 board. Under
  Order J it was picks 1 to 24. The extra pick is the 0.40% normalisation move.
- **Smalls sit on the re-sited floor over picks 1 to 18.** That is 241 rows. These are exactly the
  rows the fit wanted to make lighter; the floor holds them at neutral instead.
- **Of those, picks 1 to 5 also sit on the 0.5 hard floor**, because Order D's pooled curve is itself
  clipped there. At those five picks nothing in the tall/small factor can move a small either way.

### 2.6 · The acceptance test, scored

| clause | test | result |
|---|---|---|
| **(a)** | no small made lighter, at any pick, structurally | **PASS** — none. Order J had picks 6-18 |
| **(b)** | no small made lighter, on the board | **PASS** — 127 smalls move on the factor, 0 of them up |
| **(c)** | Smillie returns to the ~700s | **PASS** — **772**, the exact preregistered number |
| **(d)** | the four talls keep their relief | **PASS** — Green +141, Conway +86, McCabe +70, Dodson +16 |
| **(e)** | the redistribution identity holds | **PASS** — residual −1.1e-16, build-failing above 1e-9 |

The engine carries (a), (d) and (e) as **build-failing asserts**. They are proven able to fail: (a)
fired the instant the fix was removed, and that firing run is kept at `K1_NONVACUITY_PROOF.txt`.

### 2.7 · The proof that the fix is the only thing this order changed

The engine carries a declared measurement dial, `RL_O36_FLOORFIX`, default on. Set it to 0 and the
floor fix is removed. That board is `d1058fe02cbf59f70441dd3a1b4001ff` — **byte-identical to Order J's
ruled tall board**. Nothing else in the fade moved.

---

## 3 · THE INSTRUMENT QUESTION YOU ASKED

**Which fade were the REGION_J frontier rows scored on — the pooled one or the tall one?**

**The tall one.** Not read off a comment. Proved by reproduction.

`o37_sweep.py` line 322 sets `D = Dvec(lrel, 'tall')` inside the grid loop, so every swept point is
scored on the tall exponent. Only the two named controls carry a `fade` label; the frontier rows do
not. Re-scoring your ruled point on Order J's own legs reproduces the published row exactly on the
tall fade and not on the pooled one:

| fade | class | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 | max class |
|---|---:|---:|---:|---:|---:|---:|---:|
| pooled (Order D) | 1.0520 | +7.38% | +12.72% | +7.43% | −10.09% | −5.58% | 1.1441 |
| **tall, wired floor** | **1.0519** | **+7.58%** | **+13.82%** | **+8.26%** | **−8.54%** | **−6.50%** | **1.1385** |
| tall, floor fixed | 1.0515 | +7.47% | +13.62% | +8.30% | −8.47% | −6.41% | 1.1386 |

The middle row is your published prediction, bit for bit.

**So the numbers you chose on were computed on the defective fade.** That is not a small point and it
is why the row below it is in the table.

---

## 4 · BUILT AGAINST PREDICTED — THE TWO CAUSES, SEPARATED

There are two different reasons the built numbers differ from the predicted ones, and they should not
be blurred together.

**Cause one: the floor fix moved the prediction.** On the same navigation instrument, fixing the floor
costs picks 1-10 about 0.11 points and picks 11-20 about 0.20 points, because part of what was lifting
those bands was smalls at picks 6-18 being paid by the defect. It slightly improves 31-40 and 41-64.
The class mark barely moves.

**Cause two: the navigation instrument and the standing instrument disagree, and they always have.**
Order J registered this in advance. The calibrator runs hotter on the young bands. On the landing
candidate it reads picks 11-20 at +11.52% where the standing instrument reads +9.20%. The standing
instrument is the one that decides.

### The table

| quantity | predicted (navigation, defective fade) | same instrument, floor fixed | **BUILT (standing instrument)** | landing candidate (standing) | move |
|---|---:|---:|---:|---:|---:|
| picks 1-10 | +7.58% | +7.47% | **+8.22%** | +7.93% | +0.29 |
| picks 11-20 | +13.82% | +13.62% | **+11.16%** | +9.20% | +1.96 |
| picks 21-30 | +8.26% | +8.30% | **+5.26%** | +2.76% | +2.50 |
| picks 31-40 | −8.54% | −8.47% | **−10.70%** | −12.84% | +2.14 |
| picks 41-64 | −6.50% | −6.41% | **−6.89%** | −7.88% | +0.99 |
| year-1 class | 1.0519 | 1.0515 | **1.0324** (built matrix) | 1.0232 | +0.0092 |
| max single class | 1.1385 | 1.1386 | **1.1363** | 1.1311 | inside the 1.139 line |
| slope | 0.976 | — | not re-read on the board | — | navigation object |
| hindsight weight W | 0.327 | — | not re-read on the board | — | navigation object |

**Read the built column, not the predicted one.** Every band is better than the landing candidate.
Picks 11-20 and 21-30 come in materially cooler than predicted, and picks 31-40 materially warmer —
that is the instrument, not the build.

**Slope and W** are properties of the navigation instrument's own fitted surface. They are not
re-derivable on a built board and are not restated here as if they were.

### The class mark, on three readings of the same boards

| reading | landing | candidate 31 | ORDER K | move |
|---|---:|---:|---:|---:|
| built matrix, every eligible row | 1.0232 | 1.0360 | **1.0324** | +0.0092 |
| built matrix, the calibrator's 1,986 teaching rows | 1.0367 | 1.0471 | **1.0458** | +0.0091 |
| the navigation instrument (the number you were quoted) | 1.0421 | — | **1.0515** | +0.0094 |

All three move the same way, by very nearly the same amount. The **levels** differ because they are
different objects: the built matrix scores every eligible row with the engine's own walk-forward
value, the navigation instrument scores a teaching subset with an analytic year-1 price.

---

## 5 · EVERY GATE, WITH ITS NUMBER

| # | gate | rail | result | number |
|---|---|---|---|---|
| **G1** | year-1 class grows | — | **PASS** | 1.0232 → **1.0324** (+0.0092) |
| **G1a** | floor 1.03 | ≥ 1.03 | **PASS** | 1.0324 |
| **G1b** | strictly under the buy rail | < 1.14 | **PASS** | 1.0324 |
| **G1c** | your ~1.08 ideal | reported, never chased | **NOT REACHED** | short by 0.0476 |
| **G1d** | worst single class | ≤ 1.139 | **PASS** | 1.1363 (class of 2012) |
| **G2a** | picks 31-40 materially improve | > 0 points | **PASS** | −12.84% → **−10.70%** (+2.14) |
| **G2b** | picks 41-64 materially improve | > 0 points | **PASS** | −7.88% → **−6.89%** (+0.99) |
| **G2c** | both remain negative | expected | **BOTH STILL NEGATIVE** | known limitation, not a failure |
| **G3** | no ND band above +14% | +14% | **PASS** | highest is 11-20 at +11.16% |
| **G3a** | no reachable pool arm above +14% | +14% | **PASS** | highest reachable is IRE +13.34% |
| **G3-SSP** | SSP's inherited buy-red | reported, separate | **REPORTED** | +50.52% → **+52.71%**, worse by 2.19 |
| **G4** | picks 1-10 stay near +7.93% | your stated concern | **PASS** | **+8.22%**, up 0.29 |
| **G5** | xavier-taylor must not rise | ≤ 0 | **PASS** | 1,176 → 1,162 (−14) |
| **G5** | daniel-annable must not rise | ≤ 0 | **FAIL — K13 FIRES** | 1,530 → **1,537 (+7)** |
| **G5** | dylan-patterson must not rise | ≤ 0 | **PASS** | 1,467 → 1,440 (−27) |
| **G6a** | day-0 entry values bit-identical | 89/89 | **PASS** | **89 of 89** on `derived_v0` |
| **G6b** | the sitter PRINT reference | regenerates, disclosed | **DISCLOSED** | 87 of 89 printed day-0 move (30 up, 57 down) |
| **G7a** | determinism ×2 | byte equality | **PASS** | f3101883 = f3101883 |
| **G7b** | dial-off = 1f176444 | byte-exact | **PASS** | 1f17644445f074d11e631b5cbae98a9a |
| **G7c** | the floor-fix removal lane = Order J | byte-exact | **PASS** | d1058fe0 |
| **G8a** | continuity in age | monotone, capped at 24 | **PASS** | bar rises, never above flat, exact from 24 |
| **G8b** | continuity in games | ≥ 0 at 1e-9 | **PASS** | 8 at-bar rows, 0 falling steps |
| **G8c** | continuity in pick | no cliff | **PASS** | largest 0.01-pick step 5.0e-4 |
| **G8d** | rho32 monotone and < 1 | — | **PASS** | 0 violations over g = 0 to 300 |
| **G9a** | S1's zero-tolerance mature law | exactly 0 | **PASS** | **0 of 429** mature rows move |
| **G9b** | J-TOL per-row cap, gated levers | min(25, 0.5%) | **59 rows over** | worst −77 (Ned Moyle) |
| **G9c** | J-TOL churn cap, gated levers | ≤ 1,001.87 | **PASS** | 695 |
| **G9d** | J-TOL net cap, gated levers | ≤ 667.92 | **FAIL** | **−695**, over by 27 |
| **G10** | dean / duff-tytler vs candidate 31 | reported | **BOTH BELOW** | 2,403 vs 2,670 · 1,505 vs 1,832 |
| **K-FLOOR** | the fix's acceptance test | five clauses | **ALL FIVE PASS** | §2.6 |

---

## 6 · THE TWO BREACHES, IN FULL

### 6.1 · Daniel Annable rises

Your law: a player who is below expectation but has played games must not go up.

He goes from **1,530 to 1,537**. Up 7.

Here is why. The age bar lifts him by **+40**, because a 19-year-old midfielder is now judged against
what 19-year-old midfielders actually produce instead of against a flat league bar. He has played 2
games at an average of 38.0, against an age bar of 57.0, so he is well below expectation. The
counterweight is meant to charge him for that. At this setting it charges him **−33**. That is 7 short
of cancelling the lift.

The other two hold. Xavier Taylor: +15 then −29, net **−14**. Dylan Patterson: +48 then −75, net
**−27**. Annable's own production leg is thinner than theirs (2 games, and his pedigree is a pick 6),
so the counterweight bites less on him.

It is 7 board points on a 1,530-point row, which is under half a percent. It is still a breach and it
is still your law, so it is printed here rather than rounded away.

### 6.2 · The veteran-movement cap is breached on the net measure

Order J preregistered a three-part rule (J-TOL) limiting how far the young-player levers may move the
veteran pool. On the two gated levers together:

- **per-row cap** — 59 of 429 mature rows exceed their own cap. Worst is Ned Moyle at −77.
- **churn cap** (total absolute movement, limit 1,001.87) — **695. Inside.**
- **net cap** (net movement, limit 667.92) — **−695. Over by 27.**

Two things matter about this.

**First, the age bar is not the cause.** The age bar alone moves **zero** mature rows out of 429. Its
own law is exact and it holds exactly. The whole of the movement is the counterweight, which keys on
career games rather than age. A 27-year-old with 141 games sits on the same reliability curve as a
19-year-old with 141 games; move the curve and both move. That was known and stated when the gate was
written.

**Second, this rule was written by Order J, before you ruled the setting.** You then chose these knobs
knowing the counterweight moves veterans. So this is a report, not a veto. The number is −695 against
a 668 line, on a veteran pool worth 362,703 points. It is 0.19% of that pool.

---

## 7 · WHERE THE PRICES ACTUALLY WENT

**The board total** goes from 667,916 to **673,097**, up 5,181 points. **493 of 804 rows move**, 124 of
them aged 24 or over.

**The legs, each one a real board rather than an arithmetic split:**

| leg | what it is | total |
|---|---|---:|
| the age bar at dose 0.40 | young players judged against their own age | **+12,857** |
| the counterweight | weight off pedigree, onto shown production, charged down with games | **−8,875** |
| the tall/small factor | talls' sitting relief, smalls paying for it | **+1,255** |
| the fade floor fix | inside the factor: the seven smalls released | **−60** |
| interaction | what the legs do not account for | −56 |

Read the first two together. **The counterweight takes back about 70% of what the age bar gives.**
That is the mechanism working as designed — the lift is paid to players who are performing and charged
to players who are not. But it is also why the two rows you care about most do not move the way you
would expect.

**Harry Dean.** Age bar **+221**. Counterweight **−218**. Net **+3**. He reads 2,403, against 2,670 on
candidate 31 and your stated ~2,600.

**Cooper Duff-Tytler.** Age bar **+85**. Counterweight **−152**. Net **−67**. He reads 1,505, which is
**below** the landing candidate's 1,572 and 327 short of candidate 31.

Both are 19, both are key-position talls, both have a high pick and few games. That combination is
exactly what this setting's `eta` of 0.50 charges hardest.

**The twenty largest rises** are dominated by the age bar on young players with real games behind them:
Murphy Reid +236, Noah Mraz +224, Logan Morris +207, Levi Ashcroft +192, Colby McKercher +190.

**The twenty largest falls** are the counterweight on rows with high pedigree and thin production:
Ned Moyle −77, Sid Draper −72, Cooper Duff-Tytler −67, Lachlan McAndrew −56, Marcus Herbert −56.

**The year-1 class on the 2026 board** goes from 58,060 to 57,823, down 237 points across 120 rows.
That is not the same object as the year-1 class growth rate in section 4 — this is the current class's
prices on today's board, that is how historical classes appreciated in their first year.

---

## 8 · THE DAY-0 DISCLOSURE, IN THE SAME WORDS ORDER D USED

There are two objects here and they must not be confused.

**`derived_v0` is the raw entry value.** What the pick itself was worth on draft day, before the player
had done anything. The walk-forward matrix writes it as year 0. It is **bit-identical on 89 of 89**.
Entry values do not move in this order.

**The printed day-0 price is entry value multiplied by the sitting discount.** For a player who has
already sat, that is not an entry value — it is an entry value with a year of sitting charged against
it. The tall/small factor IS a change to that discount. So the printed day-0 of a sitter moves by
construction, and the reference file regenerates.

**87 of the 89 wired entrants move on the printed number: 30 up, 57 down.** Largest up: Mitchell Marsh
+100.8, James Barrat +77.7, Blake Thredgold +77.6. Largest down: Ben Camporeale −34.3, Zac Walker
−28.9, Koby Coulson −28.4.

This is the same regeneration Order D disclosed when the pick-curve fade landed, and Order J after it.
It is disclosed, not buried.

---

## 9 · THE PREREG SCORECARD

Scored exactly as written, including the misses.

### The named rows

| row | predicted | actual | result |
|---|---|---|---|
| josh-smillie | **772 exactly** | 772 | **HIT** |
| oskar-taylor | **596 exactly** | 596 | **HIT** |
| will-brodie | leg tall → 0 | 0 | **HIT** on the leg; row direction MISS (−3 from the counterweight) |
| campbell-chesser | leg tall → 0 | 0 | **HIT** on the leg; row direction MISS (+1) |
| james-leake / tom-brown / sam-sturt | leg tall → 0 | all 0 | **HIT** |
| will-green | **+141 retained** | +141 | **HIT** |
| toby-conway | **+86 retained** | +86 | **HIT** |
| william-mccabe | **+70 retained** | +70 | **HIT** |
| alex-dodson | +16 or +17 | +16 | **HIT** |
| steely-green | down, slightly less than −4 | −4 | **MISS** — integer rounding absorbed the difference |
| harry-dean | UP, below C31 | +3, below C31 | **HIT** |
| cooper-duff-tytler | UP, below C31 | **−67**, below C31 | **MISS** |
| xavier-taylor | DOWN | −14 | **HIT** |
| daniel-annable | DOWN | **+7** | **MISS** |
| dylan-patterson | DOWN | −27 | **HIT** |
| milan-murdock | moves, small | −14 | **HIT** |
| isaac-kako | UP | +44 | **HIT** |
| alix-tauru | UP | **−39** | **MISS** |
| jedd-busslinger | UP | +26 | **HIT** |

**15 of 20 directions correct** on the gate scoring.

**The three misses that matter, and what caused them.** Duff-Tytler, Annable and Tauru all sit in the
same place: a high pick, few games, a young age. The prereg reasoned about the age bar and
under-weighted how hard this setting's `eta` of 0.50 charges the pedigree leg down. For Duff-Tytler and
Tauru the counterweight overwhelms the lift and they fall. For Annable it undershoots and he rises. The
seat got the direction of the counterweight right and its **size** wrong on exactly this class of row.

### The bands

| prediction | range | built | result |
|---|---|---:|---|
| picks 1-10 stay near +7.93% | +8.0 to +8.6 | +8.22% | **HIT** |
| picks 11-20 up, under the rail | +10.5 to +12.0 | +11.16% | **HIT** |
| picks 21-30 up | +4 to +6 | +5.26% | **HIT** |
| picks 31-40 improved, still negative | −11.5 to −9.0 | −10.70% | **HIT** |
| picks 41-64 improved, still negative | −9.0 to −7.0 | −6.89% | **MISS by 0.11** — outside the range, on the good side |
| year-1 class in [1.03, 1.14), ideal not reached | — | 1.0324 | **HIT** |

**5 of 6 band predictions correct**, and the miss is better than predicted, stated as a miss anyway.

### The falsifiers

| # | fired? | note |
|---|---|---|
| K1 no small made lighter | **no** — and proven able to fire | fired when the fix was removed |
| K2 smillie leaves the 700s | no | 772 |
| K3 a tall loses relief | no | all four retained |
| K4 identity misses 0.5582775 | no | −1.1e-16 |
| K5 dial-off ≠ 1f176444 | no | byte-exact |
| K6 derived_v0 not 89/89 | no | 89/89 |
| K7 determinism differs | no | identical |
| K8 continuity fires | no | all four objects pass |
| K9 class outside [1.03, 1.14) | no | 1.0324 |
| K10 a band or reachable arm over +14% | no | SSP is the inherited, separate case |
| K11 picks 1-10 fall materially | no | up 0.29 |
| K12 late bands fail to improve | no | +2.14 and +0.99 |
| **K13 a sub-expectation row rises** | **YES** | daniel-annable +7 |
| **K14 built differs materially from predicted** | **YES — as registered** | §4 |

---

## 10 · WHAT IS STILL BROKEN

None of this was in scope. All of it is carried on all three documents.

1. **Picks 31-40 and 41-64 still lose money in year one.** −10.70% and −6.89%. Both improved. Neither
   reaches zero, and no setting inside your rules does.
2. **Harry Dean and Cooper Duff-Tytler are still below their candidate-31 levels.** 2,403 against
   2,670, and 1,505 against 1,832. Duff-Tytler is also below the landing candidate.
3. **SSP still appreciates about 50% in its first year** — +52.71% here, against +50.52% on the landing
   candidate. It got 2.19 points worse. SSP enters at pick 65, outside the 1-64 curve, so no lever in
   this order reaches it.
4. **The development arms still lose money.** PDA −20.70%, PDN −40.32%, PDS −27.70%, UNR −42.91%.
5. **Veteran key-position talls aged 28-30 are over-priced by roughly 30%,** because the veteran board
   is parked. Read them about a third lighter than the number shown.
6. **The engine leans too hard on the most recent season.** One-breakout players are probably rich:
   Xerri, Callaghan, Ash, Thilthorpe. One-bad-year veterans are probably cheap: Coniglio, De Goey,
   Langford.
7. **The ceiling column on the dial page prints roughly the 87th percentile, not the 97th, for players
   aged 22 and up.** It reads too low for them.

---

## 11 · ONE THING FOUND ALONG THE WAY, NOT ASKED FOR

The repository tracks `engine/rl_after/rl_app_data.json`. The build script copies the engine directory
into a staging area, so a board file is already sitting there before the export runs. Order J's script
never removed it. That means **a failed export left the stale file in place and the suite printed its
md5 as though a board had been built.**

This seat hit it: the first attempt at the floor-fix removal lane halted on the K1 assert, and the
suite still printed a board hash for it. The fix is one line — the staged board is deleted before the
export — and it is in `bbK.sh`. Flagged because the same shape is in the inherited script.

---

## 12 · THE FILES

| what | where |
|---|---|
| the prereg | `docs/evidence/order_k_2026-08-18/PREREG_K.md` |
| **the player list** | `docs/evidence/order_k_2026-08-18/ORDER_K_PLAYERS.html` |
| **the year-1 class** | `docs/evidence/order_k_2026-08-18/ORDER_K_YEAR1.html` |
| **the no-arb tables** | `docs/evidence/order_k_2026-08-18/ORDER_K_NOARB.html` |
| the movers ledger | `docs/ledgers/ORDER_K_MOVERS.json` |
| the gates | `GATES_K.json` / `GATES_K_out.txt` |
| the fade table | `FADE_K.json` / `FADE_K_out.txt` |
| the class mark | `CLASS_K.json` / `CLASS_K_out.txt` |
| the standing tables | `STANDING_TABLES_K.json` / `STANDING_TABLES_K_out.txt` |
| the day-0 identity | `DAY0_IDENTITY_K.json` / `DAY0_IDENTITY_K_out.txt` |
| continuity | `CONTINUITY_K.json` / `CONTINUITY_K_out.txt` |
| the K1 non-vacuity proof | `K1_NONVACUITY_PROOF.txt` |
| the floor design and the calibrator bridge | `ok_floor_design.py` / `ok_bridge.py` / `FLOOR_DESIGN.json` / `BRIDGE_K.json` |

**Boards:** dial off `1f176444` · the factor with Order J's wired floor `d1058fe0` · the factor with
the fixed floor `eb4b8f04` · the age bar alone `0423c8b2` · the gated levers alone `a7d149d1` ·
**the decision board `f3101883`**.

*— ORDER K. Nothing lands on this seat's word.*
