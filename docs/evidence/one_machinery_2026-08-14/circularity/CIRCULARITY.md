# THE CIRCULARITY DECOMPOSITION — IS THE STALLING PLAYER'S PEDIGREE PROPPED UP BY SOMEBODY ELSE'S CAREER?

**ORDER 30B-C · measurement seat · `land/order-29` · 2026-08-16 · READ-ONLY · NOTHING WIRES**
Prereg: `PREREG_30BC.md`, filed and pushed (`d4ec18b`) **before any quantity in this file existed.**
Harness `o30bc_circ.py` · raw readings `CIRCULARITY.json` / `CIRC_out.txt`.
No engine, board, store, curve or config file was touched. `git diff` for this order touches
`docs/evidence/one_machinery_2026-08-14/circularity/` and nothing else.

**The owner's suspicion, verbatim:**

> *"the raw or stalling players get to hold on to their pedigree much longer, a value propped up by the
> pedigree players of the past who went on to achieve something — and I suspect those players are the
> sharp tier guys who played early and well."*

---

## 0 · THE THREE ANSWERS IN ONE SCREEN

| | question | **answer** |
|---|---|---|
| **1** | is the bonus propped by the players who broke out? | **YES, and by almost all of it.** Across the low/mid bands, players who played a full at-or-above-bar season within two seasons of the state are **31.2% of the states** and deliver **79.5% of the coefficient's mass**. Players who never delivered a single such season in six years are **51.9% of the states** and deliver **1.9%**. In picks 1–20 the breakouts move **86%** of the coefficient at 6–15 games and **91%** at 16–35. **The owner named the mechanism correctly.** |
| **2** | does the continued staller ever collect it? | **NO — he underperforms his own pick-blind projection.** Picks 1–20 still stalling two seasons on beat their production/age/output projection by **−45 · −181 · −294** points across the three bands, against **+763 · +584 · +387** for the breakouts. Only **21%** of them (16–35 band) ever earn back even the pedigree top-up the law hands them; the top 10% of the cohort hold **57%** of everything the cohort delivers. |
| **3** | does the wired law self-correct along a stall path, or overpay? | **IT SELF-CORRECTS FAR TOO SLOWLY, AND IN THE PURE CASE IT MOVES THE WRONG WAY.** Along 352 real picks-1–20 stall paths the law pays **2.86× → 4.43×** what the stall cohort itself measured, at *every* step out to four seasons. For the players who barely play at all, career games barely move, so `β(g)` barely moves — and between the 2.5-game and 10.5-game knots of the committed curve **it rises**: in **57 of 352** paths the law paid a player **more** pedigree after a season he stalled. |

**One thing must be said first, because it protects the measurement from being over-read.**
**The bonus AT THE STATE is not wrong.** `β_b` is a legitimate *ex-ante* expectation: standing at the end
of a season, nobody knows which of these players is the breakout. Paying every player in the band the same
`β(g)·v0` is exactly what an expectation means, and the mass landing on the breakouts afterwards is what
"expectation over a skewed outcome" looks like — it is not, by itself, an error.

**What is wrong is what happens NEXT.** The law re-prices only through **career games**. A player who
stalls accumulates games slowly (or accumulates them while playing below his bar, which the law cannot
see at all), so his pedigree leg stays high while his measured conditional expectation collapses. **The
owner's word for it — "get to hold on to their pedigree much longer" — is the correct description of a
measured fact.**

---

## 1 · WHAT WAS MEASURED, ON WHAT, AND THE CONTROL

| | |
|---|---|
| panel | the **committed 30B-M panel**, re-derived by `exec`ing `o30bm_measure.py` verbatim to its `q1 = {}` line — harness md5 `e910fe6482ab7b05a92f18c173667073` **asserted at entry and exit** |
| control | **4,033 states over 767 careers**, and all five committed band coefficients and shares reproduce against `PERSISTENCE_TABLE.json` at **deviation 0.00e+00** (full stored precision, not the 5-dp print) |
| the object | `β_b` — the per-unit-`v0` slope of realized remaining 6-season delivered value, after position, age, output, current and 3-year production, games-at-Y and `log1p(games)` |
| the wired law | `price = P + β(g)·v0` (30B-R T1), `β(g)` read from `READING.json::beta_curve` and **asserted to 1e-12 against the four committed resolved rows** (kako `β(36) = 0.186935`) |
| a DELIVERED season | a store row with **`games ≥ 10` AND `avg ≥` the engine-read bar for the position played** (KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). Anything else — no row, under 10 games, or below the bar — is a **STALL season** |
| the classes | **BREAKOUT** = a delivered season at `Y+1` or `Y+2` · **SLOW-BLOOM** = none then, but one by `Y+6` · **BUST** = none in the whole six-season window. Exhaustive and disjoint |
| tiers | **T1 = picks 1–20 · T2 = picks 21–64** |
| thin cells | the preregistered `n < 8` collapse rule **was never triggered** — every reported cell cleared it. Disclosed as such rather than left unsaid |

### 1.1 · The decomposition is an identity, not an approximation

By Frisch–Waugh–Lovell, the committed coefficient **is** a weighted sum of the realized outcomes:

```
β_b = Σ_i c_i ,   c_i = ṽ0_i · R_i / Σ_j ṽ0_j²      ( ṽ0 = v0 residualised on the band's own controls )
```

so `c_i` is *state i's delivery of the coefficient*, and the cell shares below **add to 100% exactly**.
**Checked against `band_fit`'s own output in all five bands: maximum deviation 5.79e-13.** This is not a
model of who delivered β. It is β, re-written.

---

## 2 · Q1 — THE DELIVERY DECOMPOSITION. WHO ACTUALLY PAYS THE PEDIGREE BONUS?

### 2.1 · The class mix first — how many of them were about to play well?

| games so far | n | BREAKOUT | SLOW-BLOOM | BUST |
|---|---:|---:|---:|---:|
| 0–5 | 382 | 56 (**14.7%**) | 85 (22.3%) | 241 (**63.1%**) |
| 6–15 | 591 | 160 (**27.1%**) | 109 (18.4%) | 322 (54.5%) |
| 16–35 | 834 | 348 (**41.7%**) | 112 (13.4%) | 374 (44.8%) |
| *36–70* | *887* | *502 (56.6%)* | *95 (10.7%)* | *290 (32.7%)* |
| *71+* | *1339* | *911 (68.0%)* | *50 (3.7%)* | *378 (28.2%)* |

Split by tier, the pedigree tier is more likely to move in every band — **17% vs 14%** at 0–5,
**40% vs 21%** at 6–15, **50% vs 36%** at 16–35 — which is itself the persistence effect, seen as an
event rate rather than as a coefficient.

### 2.2 · THE DECOMPOSITION — the coefficient's mass, by who delivered it

**Within-tier gross mass share** (each tier normalised to its own total |c|; this is the lens the prereg
scored C3 on):

| games so far | tier | n | **BREAKOUT** | SLOW-BLOOM | **BUST** |
|---|---|---:|---:|---:|---:|
| 0–5 | **T1 1–20** | 89 | **51.8%** | 46.0% | **2.2%** |
| 0–5 | T2 21–64 | 293 | 53.6% | 39.4% | 7.0% |
| 6–15 | **T1 1–20** | 187 | **86.0%** | 13.1% | **0.9%** |
| 6–15 | T2 21–64 | 404 | 69.5% | 27.7% | 2.9% |
| 16–35 | **T1 1–20** | 335 | **91.2%** | 8.3% | **0.5%** |
| 16–35 | T2 21–64 | 499 | 89.9% | 7.8% | 2.3% |
| *36–70* | *T1 1–20* | *389* | *97.7%* | *1.8%* | *0.4%* |
| *71+* | *T1 1–20* | *710* | *98.3%* | *1.5%* | *0.2%* |

**Pooled across the three low/mid bands (1,807 states), mass against population:**

| class | **share of the coefficient's gross mass** | share of the states |
|---|---:|---:|
| BREAKOUT | **79.5%** | 31.2% |
| SLOW-BLOOM | 18.6% | 16.9% |
| **BUST** | **1.9%** | **51.9%** |

**Read that last row twice. Half of the players sitting in these states carry one-fiftieth of the value
the pedigree coefficient is made of.**

### 2.3 · The same cells with their outcomes, so the mass has a face

Picks 1–20, the three low/mid bands, signed mass share of the band coefficient · realized `R_6`:

| band | class | n | signed mass share | pts of the band's pedigree contribution | mean `R_6` | p25 | **median** | p75 | zero |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0–5 | breakout | 15 | +55.0% | +97.9 | 1051.1 | 488.1 | 676.9 | 1127.9 | 0% |
| 0–5 | slow-bloom | 34 | +47.8% | +85.1 | 445.1 | 198.3 | 344.0 | 576.4 | 0% |
| 0–5 | **bust** | 40 | **+0.9%** | **+1.6** | **42.4** | 0.8 | **13.1** | 39.7 | 7.5% |
| 6–15 | breakout | 75 | +121.7% | +321.9 | 1251.8 | 628.0 | 961.3 | 1665.2 | 0% |
| 6–15 | slow-bloom | 45 | +17.9% | +47.3 | 507.0 | 182.7 | 446.1 | 674.3 | 0% |
| 6–15 | **bust** | 67 | **+1.2%** | **+3.3** | **24.8** | 0.2 | **4.0** | 24.4 | 6.0% |
| 16–35 | breakout | 169 | +188.3% | +356.2 | 1348.8 | 594.2 | 1069.5 | 1883.6 | 0% |
| 16–35 | slow-bloom | 57 | +14.7% | +27.8 | 473.8 | 155.1 | 304.6 | 719.5 | 0% |
| 16–35 | **bust** | 109 | **+1.1%** | **+2.1** | **17.6** | 0.0 | **0.3** | 13.2 | 22.9% |

*(Signed shares exceed 100% in T1 and go negative in T2 because `ṽ0` is positive for high picks and
negative for low picks — a low-pick player who delivers a big `R_6` pulls the coefficient DOWN. Both tiers
are in `CIRCULARITY.json`; the gross-share column is the one to read for "who moves it".)*

### 2.4 · So how much of the staller's bonus is other people's careers?

**At the state, ex ante: 86–91% of it in picks 1–20 (6–15 and 16–35 games), 52% at 0–5 games** — where
the missing mass is not busts but slow-blooms (46.0%), i.e. players who *did* arrive, three to six years
later. Put the two together and **97.8% of the pedigree coefficient at 0–5 games, and 99.5% at 16–35
games, is delivered by players who eventually produced a full season at or above their bar. The ones who
never did contribute essentially nothing to the number they are being paid out of.**

---

## 3 · Q2 — THE STALL-PERSISTENCE QUESTION. DOES THE BONUS EVAPORATE, OR IS IT HELD?

### 3.1 · The continued staller's measured forward value against what the law hands him

"Continued staller" = **no delivered season at `Y+1` or `Y+2`**. "Ped excess" is the mean residual against
the band's own **pick-blind** fit — the same instrument 30B-M §2.1 used — with a 300-replicate
player-cluster bootstrap.

| band | tier | group | n | clusters | mean `R_6` | median | p75 | zero | **law pays `β(g)·v0`** | **measured ped excess (90% CI)** |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0–5 | T1 | breakout | 15 | 15 | 1051.1 | 676.9 | 1127.9 | 0% | 355.4 | **+762.6** (+419…+1140) |
| 0–5 | T1 | **cont. staller** | 74 | 67 | 227.4 | 108.8 | 319.3 | 4.1% | **335.0** | **−45.0** (−108…**+20**) |
| 0–5 | T1 | of which bust | 40 | 34 | 42.4 | 13.1 | 39.7 | 7.5% | 319.9 | −237.4 (−268…−207) |
| 6–15 | T1 | breakout | 75 | 70 | 1251.8 | 961.3 | 1665.2 | 0% | 492.8 | **+584.0** (+444…+752) |
| 6–15 | T1 | **cont. staller** | 112 | 92 | 218.6 | 39.4 | 262.9 | 3.6% | **410.0** | **−181.1** (−242…−119) |
| 6–15 | T1 | of which bust | 67 | 51 | 24.8 | 4.0 | 24.4 | 6.0% | 399.9 | −300.1 (−345…−255) |
| 16–35 | T1 | breakout | 169 | 148 | 1348.8 | 1069.5 | 1883.6 | 0% | 368.0 | **+386.6** (+257…+502) |
| 16–35 | T1 | **cont. staller** | 166 | 102 | 174.3 | 19.9 | 189.4 | 15.1% | **297.4** | **−293.6** (−362…−226) |
| 16–35 | T1 | of which bust | 109 | 56 | 17.6 | 0.3 | 13.2 | 22.9% | 284.7 | −283.7 (−345…−215) |

*(T2 is in the JSON and moves the same way: −136.5 · −203.2 · −233.4 for its continued stallers.)*

**The continued staller does not merely fail to collect a pedigree premium — he finishes BELOW what his
own production, age, position and output predicted, in every band, and the interval clears zero in two of
the three.** The law is paying him 297–410 points of pedigree at the same moment.

### 3.2 · The coefficient re-fitted on the stalling population itself

The committed `band_fit`, unchanged, run on the states whose next two seasons are both stall seasons:

| band | n | clusters | **`β` stall cohort** | t | vs the wired band `β` | `β` breakout cohort (contrast) |
|---|---:|---:|---:|---:|---:|---:|
| 0–5 | 326 | 283 | **0.17319** | 3.64 | **58% of 0.29683** | 0.70241 (t 2.32) |
| 6–15 | 431 | 326 | **0.08549** | 2.15 | **24% of 0.36226** | 0.31338 (t 3.34) |
| 16–35 | 486 | 298 | **0.07959** | 2.65 | **36% of 0.22330** | 0.16790 (t 2.03) |
| *36–70* | *385* | *198* | *−0.00623* | *−0.29* | **NO SIGNAL** (CI spans zero) | *0.13815 (t 1.76)* |
| *71+* | *428* | *164* | *−0.01276* | *−0.90* | **NO SIGNAL** (CI spans zero) | *0.05016 (t 0.99)* |

**Pedigree does not vanish inside the stalling population — at 0–5 games it is still `t = 3.6`.** A high
pick who is not yet playing is still a better bet than a low pick who is not yet playing. **But it is a
quarter to a half of the pooled number the wired law hands him**, and past 36 games it is measured at
zero. *This is the single number that answers "is it propped up": at 6–15 games the wired law pays
**4.2×** the coefficient the stalling population itself earns.*

### 3.3 · Does the law re-price him? Only if he plays.

**Continued stallers who played again at `Y+2`** (so career games advanced and a state exists there):

| band | tier | n | g at `Y` | g at `Y+2` | `β(Y)` | `β(Y+2)` | ratio | law `Y` | law `Y+2` | median \|Δβ\|/β | β **ROSE** for |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0–5 | T1 | 66 | 3.1 | 20.2 | 0.3083 | 0.2700 | 0.876 | 334.7 | 292.4 | 18.6% | **20 of 66** |
| 6–15 | T1 | 96 | 9.9 | 31.0 | 0.3394 | 0.2134 | 0.629 | 413.2 | 257.7 | 38.3% | 1 of 96 |
| 16–35 | T1 | 110 | 23.4 | 45.0 | 0.2395 | 0.1589 | 0.664 | 313.1 | 206.2 | 31.2% | 0 of 110 |

**THE PURE CASE — the players the owner actually described.** Continued stallers who accumulated **fewer
than 10 games in total** across `Y+1` and `Y+2` — the ones who genuinely could not get on the park:

| band | tier | n | g at `Y` | g at `Y+2` | `β(Y)` | `β(Y+2)` | **ratio** | **law `Y`** | **law `Y+2`** | **mean `R_6`** | **median `R_6`** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0–5 | **T1** | 20 | 2.8 | 6.9 | 0.3055 | 0.3355 | **1.098** | 326.2 | **354.0** | 133.4 | 79.1 |
| 6–15 | **T1** | 26 | 10.2 | 15.2 | 0.3409 | 0.3008 | 0.882 | 405.9 | 350.0 | 47.8 | **0.6** |
| 16–35 | **T1** | 69 | 24.5 | 27.5 | 0.2347 | 0.2196 | 0.936 | 281.6 | **264.3** | 23.9 | **0.0** |
| 0–5 | T2 | 145 | 2.8 | 5.3 | 0.3062 | 0.3220 | **1.052** | 129.7 | 137.6 | 36.4 | 0.0 |
| 6–15 | T2 | 167 | 10.6 | 13.6 | 0.3340 | 0.3113 | 0.932 | 138.9 | 129.2 | 20.9 | 0.0 |
| 16–35 | T2 | 137 | 23.2 | 25.7 | 0.2405 | 0.2280 | 0.948 | 97.8 | 92.4 | 27.2 | 0.0 |

> **At 16–35 games, a picks-1–20 player who has managed under 10 games in two seasons is still being paid
> 264 points of pedigree by the wired law. The median such player's entire measured six-season forward
> value is ZERO.** At 0–5 games the law's pedigree leg **goes UP** while he sits: mean 326.2 → **354.0
> (+8.5%)**, mean per-row `β` ratio **1.098**.

### 3.4 · Who inside the stalling cohort ever collects?

Picks 1–20 continued stallers:

| band | n | top 10% of the cohort hold | **`R_6` > the law's pedigree leg** | `R_6` > 2× it |
|---|---:|---:|---:|---:|
| 0–5 | 74 | **36.9%** of the cohort's value | **33.8%** | 6.8% |
| 6–15 | 112 | **48.6%** | **17.9%** | 9.8% |
| 16–35 | 166 | **57.3%** | **21.1%** | 9.6% |

**Four out of five of them never deliver, over six seasons, even the size of the pedigree top-up they are
carrying — and more than half of what the cohort does deliver belongs to one player in ten.** The owner's
"propped up" is measured, inside the stalling cohort as well as across it.

---

## 4 · Q3 — THE WIRED LAW ALONG HISTORICAL STALL PATHS

352 real picks-1–20 low/mid states, over **159 careers**, with **two or more consecutive stall seasons**.
At each successive year: what the wired law pays (`β_wired(g_t)·v0`) against what the stall cohort
measured from a state at that depth (`β_stall(band(g_t))·v0`).

| step | n | mean g | `β_wired` | `β` stall cohort | **LAW PAYS** | **COHORT SAYS** | **GAP** | **law / cohort** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (the state) | 352 | 15.1 | 0.2847 | 0.1011 | **341.1** | 119.4 | **+221.7** | **2.86×** |
| 1 | 352 | 23.5 | 0.2486 | 0.0728 | **295.0** | 84.8 | **+210.2** | **3.48×** |
| 2 | 352 | 31.6 | 0.2137 | 0.0513 | **252.7** | 58.6 | **+194.1** | **4.31×** |
| 3 | 285 | 36.7 | 0.1917 | 0.0436 | **221.5** | 49.1 | **+172.4** | **4.51×** |
| 4 | 254 | 39.6 | 0.1814 | 0.0419 | **208.3** | 47.0 | **+161.3** | **4.43×** |

**The honest reading, both halves of it:**
- **It IS partially self-correcting** — in board points the gap falls from +222 to +161 over four seasons,
  because a player who plays badly still accumulates games and the curve does come down.
- **It is nowhere near correcting enough** — as a ratio the overpay **widens** from 2.86× to 4.5×, and it
  never converges. Past 36 games the stall cohort's own coefficient is **statistically zero** while the
  law is still paying **0.18 × v0**.
- *(Disclosure: where the stall-cohort `β` is measured slightly negative — the deep bands, `t = −0.29` and
  `−0.90`, both indistinguishable from zero — flooring it at zero is reported beside the primary and moves
  the gap by ≤ 4 points at every step: +221.7 / +208.9 / +191.1 / +168.6 / +157.0. Nothing turns on it.)*

### 4.1 · The named paths — the overpaid

Year by year: games played, career games, the law's `β(g)`, the pedigree points the law pays him, what the
stall cohort measured from that depth, the gap, and what he **actually** delivered over the next six
seasons from that year. *(Selection rule fixed in the harness: the ten longest / highest-pedigree BUST
paths, then the six with the largest realized `R_6` — no hand-picking.)*

**`jonathan-o-rourke` · pick 2 · MID · v0 3036.8 · state 2013 (age 19, 1 game) · stalled 6 straight**

| year | games | cum g | β(g) | **LAW PAYS** | cohort says | GAP | realized `R_6` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2013 | 1 | 1 | 0.2968 | **901.4** | 525.9 | +375.5 | 0.2 |
| 2014 | 8 | 9 | 0.3546 | **1076.8** ↑ | 259.6 | +817.2 | 0.2 |
| 2015 | 2 | 11 | 0.3532 | 1072.5 | 259.6 | +812.9 | 0.0 |
| 2016 | 7 | 18 | 0.2700 | 819.9 | 241.7 | +578.2 | 0.0 |
| 2017 | 0 | 18 | 0.2700 | 819.9 | 241.7 | +578.2 | 0.0 |
| 2018 | 3 | 21 | 0.2482 | 753.8 | 241.7 | +512.1 | 0.0 |
| 2019 | 0 | 21 | 0.2482 | **753.8** | 241.7 | +512.1 | **0.0** |

**Seven years of stalling. The law's pedigree leg went 901 → 1077 → 754. He delivered nothing at all.**

**`anthony-morabito` · pick 4 · MID · v0 2631.5 · state 2010 (age 19, 23 games) · stalled 6 straight**

| year | games | cum g | β(g) | **LAW PAYS** | cohort says | GAP | realized `R_6` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2010 | 23 | 23 | 0.2362 | 621.6 | 209.4 | +412.2 | 0.0 |
| 2011–13 | 0 | 23 | 0.2362 | **621.6 · 621.6 · 621.6** | 209.4 | +412.2 | 0.0 |
| 2014 | 3 | 26 | 0.2211 | 581.7 | 209.4 | +372.3 | 0.0 |
| 2015–16 | 0 | 26 | 0.2211 | **581.7 · 581.7** | 209.4 | +372.3 | **0.0** |

**Six seasons in which he played three games in total, and the pedigree leg falls by 6.4%.** This is the mechanism in one row: the
law re-prices only through games, and a player who does not play does not re-price. *(The wired sitter law
handles a `cg == 0` row separately; Morabito is not gameless — he is a 23-game player who stopped, which
is exactly the population that falls between the two lanes.)*

**`jarrod-pickett` · pick 5 · SF · v0 2196.3 · state 2017 (age 21, 10 games)**

| year | games | cum g | β(g) | **LAW PAYS** | cohort says | GAP | realized `R_6` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2017 | 10 | 10 | 0.3598 | **790.3** | 187.8 | +602.5 | 0.0 |
| 2018 | 7 | 17 | 0.2786 | 611.8 | 174.8 | +437.0 | 0.0 |
| 2019–23 | 0 | 17 | 0.2786 | **611.8** each year | 174.8 | +437.0 | 0.0 (2019) |

**`xavier-ellis` · pick 3 · SD · v0 2830.9 · state 2007 (age 19, 13 games)** — the "plays a bit, never
kicks on" case the owner had in mind:

| year | games | cum g | β(g) | **LAW PAYS** | cohort says | GAP | realized `R_6` | law / `R_6` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2007 | 13 | 13 | 0.3224 | 912.8 | 242.0 | +670.8 | 167.4 | **5.5×** |
| 2008 | 21 | 34 | 0.1925 | 545.0 | 225.3 | +319.7 | 159.0 | 3.4× |
| 2009 | 11 | 45 | 0.1666 | 471.7 | −17.6 † | +489.3 | 141.4 | 3.3× |
| 2010 | 22 | 67 | 0.0566 | 160.1 | −17.6 † | +177.7 | 115.4 | 1.4× |
| 2011 | 8 | 75 | 0.0350 | 99.1 | −36.1 † | +135.3 | 2.6 | 37.5× |

† *past 36 games the stall cohort's own coefficient is measured at `−0.006` (t = −0.29) and `−0.013`
(t = −0.90) — **statistically zero**, not negative. Read those cells as ≈ 0; the floored variant is in §4.*

Ellis is the clean picture of partial self-correction: **by 67 games the law has come most of the way
down** — but it took him four seasons and 54 extra games to get there, and it was still paying 3.3× his
measured forward value in year three.

Others on the same list, each with the full path in `CIRC_out.txt`: `paddy-dow` (pk 3, 722 → 508 → 489
while delivering 1.3), `jimmy-toumpas` (pk 6, 523 → 312), `jarrad-oakley-nicholls` (pk 8, **535 → 578 →
599** across three stalled seasons — the law paying *more* each year), `chayce-jones` (pk 9),
`paul-ahern` (pk 9, 596 → 455 → 389 then **four gameless seasons frozen at 389.3**), `andrew-moore` (pk 9),
`lochie-o-brien` (pk 10), `nathan-freeman` (pk 10, **500.4 every year for seven years on 2 career games**),
`jake-melksham` (pk 10), `aiden-bonar` (pk 11).

### 4.2 · The named paths — the vindicated, because the answer is not one-sided

The same rule, applied to the largest realized `R_6`: players who stalled two or more seasons from a
low/mid state **and delivered anyway**. For these the law **underpays** — `law / R_6` of 0.03–0.49.

| player | pick | pos | state | `v0` | law pays at the state | cohort says | **realized `R_6`** | law / `R_6` |
|---|---:|---|---|---:|---:|---:|---:|---:|
| **`callum-mills`** | 3 | MID | 2016, 22 g | 2830.9 | 685.1 | 225.3 | **1839.1** | 0.37× |
| **`luke-davies-uniacke`** | 4 | MID | 2018, 7 g | 2631.5 | 901.1 | 225.0 | **1839.0** | 0.49× |
| **`taylor-adams`** | 19 | SF | 2012, 15 g | 959.4 | 286.1 | 82.0 | **1729.0** | 0.17× |
| **`callan-ward`** | 19 | SD | 2008, 6 g | 959.4 | 321.6 | 82.0 | **1535.4** | 0.21× |
| **`ben-mcevoy`** | 9 | KPF | 2008, 1 g | 1382.4 | 410.3 | 239.4 | **1426.8** | 0.29× |
| **`bradley-ebert`** | 13 | MID | 2009, 32 g | 1551.0 | 308.1 | 123.4 | **1300.2** | 0.24× |

**This is why the coefficient is real and why the seat will not call the bonus "wrong".** Mills at the end
of 2016 looked exactly like the population in §3 — and he delivered 1,839 points. The pedigree bonus is
optionality on precisely these careers. **The measurement's complaint is not that the option is priced;
it is that the option keeps being priced at full value for years after the market has told you it expired.**

### 4.3 · The law paying MORE for stalling — 57 of 352 paths

The committed `β(g)` curve **rises** between its 2.5-game knot (0.2968) and its 10.5-game knot (0.3623),
because 30B-M measured `σ` slightly higher at 6–15 games than at 0–5. Wired as a per-game law this means a
young high pick who plays a handful of poor games **gains** pedigree:

| player | pick | career games | law pedigree | move |
|---|---:|---|---:|---:|
| `jye-caldwell` | 11 | 2 → 11 | 500.1 → **595.1** | **+95.0** |
| `jarrod-brander` | 13 | 3 → 11 | 293.3 → **340.3** | **+47.0** |
| `callum-coleman-jones` | 20 | 1 → 9 | 206.8 → **247.1** | **+40.2** |
| `aiden-bonar` | 11 | 4 → 6 | 533.8 → **564.7** | **+30.9** |
| `jed-anderson` | 16 | 5 → 9 | 328.5 → **356.5** | **+27.9** |
| `jarrad-oakley-nicholls` | 8 | 4 → 7 → 9 (two consecutive stalled seasons) | 534.8 → 578.0 → **598.5** | +43.2 then +20.5 (**+63.7**) |

**This is not a measurement error — it is a faithful wiring of a measured non-monotonicity.** 30B-M's own
band curve had it (70.1% → 66.4% is monotone in σ, but `β` itself rises 0.2968 → 0.3623 because mean `v0`
and mean `R` differ across the two bands). The additive law reads `β`, not `σ`, so the law inherits the
rise. **It was invisible until somebody walked a stall path along it.**

---

## 5 · THE OWNER'S QUESTION, ANSWERED IN HIS OWN WORDS

> *"the raw or stalling players get to hold on to their pedigree much longer"*

**TRUE, and it is the games clock that does it.** The wired law re-prices pedigree only through career
games. A player who cannot get a game cannot re-price: `nathan-freeman` holds 500.4 points of pedigree for
seven consecutive years on two career games. A player who plays badly re-prices at the *same rate as a
player who plays brilliantly* — the law cannot see the difference, because form lives entirely in the
production leg. Measured: the stall cohort's own coefficient is **24–58%** of the pooled one in the
low/mid bands and **statistically zero** past 36 games, while the law keeps paying the pooled number.

> *"a value propped up by the pedigree players of the past who went on to achieve something"*

**TRUE, and quantified: 79.5% of the coefficient's mass across the low/mid bands, 86% and 91% inside picks
1–20 at 6–15 and 16–35 games.** Players who never produced a single at-or-above-bar season in six years
are **51.9% of the population and 1.9% of the mass.**

> *"and I suspect those players are the sharp tier guys who played early and well"*

**TRUE as stated — and one refinement the measurement insists on.** The mass is delivered by the ones who
played early and well (breakouts: within two seasons). But at the very start of a career — the 0–5 games
band — the breakouts carry only **51.8%** of the tier's mass and the **slow-blooms carry 46.0%**. At one
or two games played, "he hasn't done it yet" is genuinely uninformative: `ben-mcevoy` after one game
delivered 1,427. **The propping is by the players who eventually arrive, and by 6–15 games "eventually"
has collapsed into "within two seasons".**

**AND THE FAIRNESS ANSWER, WHICH IS THE ONE HE ASKED FOR:**

> **The stalling player's held value does not track his true conditional expectation. It lags it, and the
> lag grows.** Ex ante at the state the price is defensible. One season later the law is paying 3.5× the
> stall cohort's measured value, two seasons later 4.3×, three seasons later 4.5×. **The dynamic is
> self-correcting in the right direction and at roughly a quarter of the required speed** — and for the
> sub-population that cannot get on the park at all, the correction is zero or negative.

---

## 6 · WHAT THIS ORDER DOES **NOT** SAY

1. **It does not say β is wrong.** `β_b` reproduces byte-identically here and is the right ex-ante
   expectation at a state. This order re-writes it; it does not re-fit it.
2. **It does not recommend a dial, a re-calibration, or a form-conditional β.** The measurement shows the
   wired law's only re-pricing channel (career games) is too slow and, in one segment, has the wrong sign.
   **What to do about that is a ruling, not a fit, and the seat does not take it.**
3. **It does not re-open the 30B-R T1 verdict.** The additive form is assumed exactly as ruled; the gap
   measured here is a property of `β(g)`'s *argument*, not of the additive form.
4. **It does not touch the sitter lane.** A `cg == 0` row is priced by the wired sitter law; every state
   in this order has at least one game. The population this order exposes — a 23-game player who stops —
   sits between the two lanes and is priced by neither's assumptions.

---

## 7 · PREREG SCORED BY NUMBER — BREACHES OWNED

| # | verdict | claimed | measured |
|---|---|---|---|
| **C1** | **HELD** | panel 4,033/767, band coefficients to 1e-9, FWL identity to 1e-9 | 4,033 / 767; β and σ reproduce at **deviation 0.00e+00** against `PERSISTENCE_TABLE.json`'s stored precision; FWL max deviation **5.79e-13** |
| **C2** | **BREACH** (both magnitude legs) | breakout share 20–55% at 0–5 and 45–80% at 16–35; rising; T1 > T2 | **14.7%** and **41.7%** — **both below the floor**. Rising ✓ (14.7 → 27.1 → 41.7) and T1 > T2 in all three ✓. **The seat over-estimated how many young players produce a full at-or-above-bar season within two years. The breach strengthens the finding: fewer breakouts carry even more of the mass.** |
| **C3** | **BREACH at 0–5; HELD at 6–15 and 16–35** | T1 breakouts ≥ 60% of the tier's gross mass in every low/mid band; busts ≤ 15% | **51.8% / 86.0% / 91.2%** — the 0–5 band misses by 8.2 points. Busts **2.2% / 0.9% / 0.5%**, held with room. **Owned: at 0–5 games the mass the seat assigned to breakouts sits in slow-blooms (46.0%), not busts — the claim's spirit survives, its number does not.** |
| **C4** | **HELD** (widely) | pooled low/mid busts < 8% of gross mass while > 15% of states | **1.9% of mass, 51.9% of states** |
| **C5** | **HELD** | T1 staller ped excess < ⅓ of breakouts' in all three bands; ≥ 1 band's CI contains zero | staller **−45.0 / −181.1 / −293.6** vs breakout **+762.6 / +584.0 / +386.6** (negative, so satisfied); 0–5 CI **(−108, +20)** contains zero |
| **C6** | **BREACH on leg 1 at 6–15; HELD at 0–5; leg 2 HELD** | median 2-season \|Δβ\|/β ≤ 25% at 0–5 and 6–15; ≥ 1 named path where the law pays more after a stall | **18.6%** at 0–5 ✓, **38.3%** at 6–15 ✗. **57 of 352 paths** rose ✓. **Owned, with the reason: the re-price sample is conditional on playing again, and those players added a mean 17–21 games. In the pure sub-lens (<10 games over two seasons) the ratios are 1.098 / 0.882 / 0.936 — the prediction was right about the mechanism and wrong about the sample it would show up in.** |
| **C7** | **BREACH on the widening leg; HELD on the sign leg** | gap positive at k = 1, 2, 3 and wider at k = 3 than k = 1 | positive at every step (**+221.7 / +210.2 / +194.1 / +172.4 / +161.3**) ✓; but the absolute gap **NARROWS**. **The ratio widens (2.86× → 4.51×) — which the seat did not predict and which is the more honest statement of the pathology.** |
| **C8** | **HELD** (in all three bands, not just the predicted one) | at 0–5, mean law pedigree leg > mean realized `R_6` for T1 continued stallers | **1.47× / 1.88× / 1.71×** |
| **C9** | **HELD** | ≥ 6 T1 careers with k ≥ 2; ≥ 1 genuine slow-bloom who delivered large value | **159 careers**; `callum-mills` 1839.1, `luke-davies-uniacke` 1839.0, `taylor-adams` 1729.0, `callan-ward` 1535.4, `ben-mcevoy` 1426.8, `bradley-ebert` 1300.2 |
| **C10** | **HELD** | one pass, no tuning, thin cells collapsed and disclosed | one execution; **the n < 8 rule never triggered** — every reported cell cleared it, disclosed rather than left unsaid. Four lenses were added after the first output and are labelled where they appear (§3.3 pure case, §3.4 who-collects, §4's ratio column, §2.1's band totals); **none re-decides a verdict** |

**6 HELD (C1, C4, C5, C8, C9, C10) · 4 BREACHED (C2, C3, C6, C7).** No breach reverses an answer: C2's and
C3's misses make the concentration *sharper* than predicted, and C6's and C7's make the self-correction
story more nuanced rather than less — the gap narrows in points while widening as a ratio, which the seat
did not foresee and which is the more useful fact.

---

## 8 · ANOMALIES AND LIMITATIONS, STATED

1. **"DELIVERED" IS A BAR TEST, AND THE MID BAR IS HIGH.** `callum-mills` is classed slow-bloom because
   2017 was 24 games at **73.3** as an SD against a **75.3** bar, and 2018 was 9 games (under the
   10-game floor) at 79.0. He was playing senior football throughout. **The classes measure "produced at
   or above replacement", not "was in the team"** — which is the right test for a *value* decomposition
   and the wrong word for a selection story. Read "stall" as "did not clear his own position's bar",
   never as "was dropped".
2. **THE STALL COHORT IS TWO POPULATIONS.** Under-10-games men and below-bar regulars are pooled by the
   class definition. §3.3's pure sub-lens separates them and the separation matters: the overpay is
   sharpest, and the self-correction is worst, for the ones who cannot get a game.
3. **THE `Y+2` RE-PRICE IS CONDITIONAL ON SURVIVING.** A continued staller who never played again has no
   `Y+2` state, so the re-price table is computed on those who did (66 of 74 · 96 of 112 · 110 of 166 in
   T1). Those who vanished re-price **not at all** — the table therefore *understates* the stickiness.
4. **RIGHT CENSORING ON THE PATHS.** A stall path from a 2018 state runs past 2019, so its later `R_6`
   values are censored and printed as `censored`, never imputed. The gap-path columns (law vs cohort) are
   uncensored — they need only games and `v0`.
5. **`β_stall` PAST 36 GAMES IS NOT A NEGATIVE NUMBER, IT IS A ZERO.** `t = −0.29` and `−0.90`; the CI
   spans zero in both bands. The primary tables carry the measured value; the zero-floored variant is
   printed beside it and changes the gap path by ≤ 4 points.
6. **SIX SEASONS IS NOT A CAREER** (30B-M's own caveat, inherited). The shares transfer; the levels do
   not. A staller who breaks out in year 7 is a bust here.
7. **THE PATH ARITHMETIC IS A SIMULATION OF THE LAW, NOT A REBUILD OF THE BOARD.** `β_wired(g_t)·v0` is
   the law's pedigree leg only; the production leg and the fade/join lanes are not re-derived. No price is
   claimed for any of these players. **DERIVED, NOT BUILT.**
8. **`β` RISES BETWEEN THE FIRST TWO KNOTS** (§4.3). It is faithful to 30B-M and it was never wrong as a
   *band* statement; it becomes a live problem only when read as a per-game law along a path.

---

## 9 · THE LINE

**NOTHING WIRES.** No board, store, engine, curve or config file was touched. The committed 30B-M panel is
reproduced at deviation zero and its coefficient is re-written, not re-fitted. **The owner's suspicion is
measured TRUE on all three of its clauses, with one refinement at the very start of a career — and the
fairness question he asked underneath it has a number: the wired law pays a continued staller 2.9× to 4.5×
what his own cohort measured, and the gap does not close.**
