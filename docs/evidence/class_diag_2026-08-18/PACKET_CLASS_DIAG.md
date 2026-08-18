# PACKET CLASS DIAG — WAS 2015 JUST A STRONG DRAFT? MOSTLY YES. AND ORDER P READS CLASS STRENGTH BETTER THAN ORDER K.

**Seat:** CLASS DIAGNOSTIC. Read-only. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**This seat did not edit the engine, did not build a board, and did not change any candidate.**
Every number below is measured off the matrices ORDER P BUILD already produced and off the store
rows those matrices carry.

**Pins.** store `cb38ef11` · engine `7df6a923` · matrices `per_entrant_OKRULED.json` (ORDER K
`f3101883`), `per_entrant_PBUILT.json` (ORDER P `374d4e44`), `per_entrant_O35FINAL.json` (landing
candidate `1f176444`).

---

## THE ANSWER TO THE OWNER'S QUESTION, IN ONE PARAGRAPH

**Yes on 2015, and yes on Order P — with one exception the owner should see.** The 2015 draft class
really did have a strong first year. On nine measures of realised year-one production it is the
strongest of the eleven classes on the registered basis: first on surplus points per player, first
on the share of its players who beat the age bar for their position and age, first on points per
game above that bar, second on raw points per game, third on total production per player. Its top
ten picks played 12.4 games each at 65.6 points a game, which is +12.08 above the age bar — the next
best class is +8.81. So the mark going up is the board reading something real. And Order P reads
class strength **better** than Order K does: weight the realised measures the same way the class
mark weights them, and Order P's correlation with realised year-one production rises from +0.39 to
+0.66 and with realised surplus from +0.34 to +0.65, and that improvement survives deleting the 2015
class entirely. **The exception:** of the three classes now over the 1.14 line, 2015 and 2010 are
genuinely strong (they rank 1st and 2nd of eleven on price-weighted year-one surplus), but **2011 is
not** — it ranks 8th of eleven on that measure. 2011 sits over the rail because Order K already had
it at 1.1363, half a point below the line, and Order P adds an ordinary +0.0232. So "the three
classes in breach must have had strong first years" is true of two of them and not the third.

**n is 11 classes. That is small. Every confidence interval below is wide and most of them contain
zero. Nothing here should be read as proof; it is the best measurement eleven classes can support.**

---

## 1 · WHAT WAS MEASURED, AND WHAT WAS NOT

MEASURED: realised year-1 games, points per game, share above the age bar, production and surplus,
for every draft class 2005-2015, read straight off the season rows in the store. Class marks
reproduced from the same matrices `op_class.py` scored. Row-level decomposition of every class move.
Correlations with bootstrap intervals.

NOT MEASURED, and why: no out-of-sample prediction test exists here. A class's year-1 **price** is
built partly out of that class's year-1 **production**, so both boards must correlate with
production to some degree. That is why the only number that carries weight is the **difference**
between the two boards on the same eleven classes, and why the paired bootstrap is reported instead
of two separate intervals. This is a fidelity comparison, not a forecast test.

NOT MEASURED: nothing was skipped. No test in the brief was substituted for a weaker one.

---

## 2 · PART E FIRST — THE INSTRUMENT IS CLEAN

The 2015 number is not an artifact. `CD_REPRO_out.txt`, `CD_INST_out.txt`.

- My arithmetic reproduces all 22 published class marks. Worst disagreement **0.000049**. W2 mark
  1.0513 (Order K) and 1.0613 (Order P), both matching the published figures.
- Every one of the 2015 class's **110 rows is scored in both sums**. **Zero excluded**, **zero
  scored at a price of exactly zero**. The two classes that do lose rows to the pre-window rule are
  2018 (9 rows) and 2020 (20 rows), and neither is on the registered basis.
- The year-0 denominator is **bit-identical** between Order K and Order P for every class — worst
  difference 0.000000 — so a class's mark move is exactly the sum of its rows' year-1 price moves
  over one shared number. Every row's contribution is additive and exact.
- The year grid is identical row for row on the two boards. No row's year-1 cell is read from a
  different index.
- 2015 is unremarkable in shape: 110 rows (classes run 100 to 145), 67 national-draft and 43 pool,
  10 picks in the top ten like every class, top-5 price share 21.4% against a range of 19.5% to
  22.8%, Gini of entry price 0.468 against a range of 0.439 to 0.502.
- No data artifact. No row missing an age. No row missing an entry price. Entry-age mix ordinary:
  80.3% of the class's price weight is aged 19 at the year priced, against 73% to 96% elsewhere.

**One thing to read carefully.** The charge is one factor inside the price, not the price. On the
2015 class the Order P / Order K **charge** ratio spans 0.731 to 2.000 while the **price** ratio
spans only 0.833 to 1.248. Across all 844 rows on the matrix that carry the new charge the two move
in the same direction every time — **0 sign disagreements** — but not proportionally. Read the
charge column in section 4 as the input and the price move as the output.

---

## 3 · PART A — IS THE 2015 CLASS ACTUALLY STRONG? YES.

Realised year-1 outcomes, draft classes 2005-2015. Year 1 of draft class C is season C+1. No board
price is used anywhere in this table. `CD_OUTCOMES_out.txt`.

| draft class | played % | games/row | ppg | ppg above bar | above bar % | production/row | surplus/row |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2005 | 41.3% | 2.71 | 54.05 | −0.78 | 31.1% | 146.3 | −2.1 |
| 2006 | 46.7% | 3.02 | 54.17 | +0.69 | 36.8% | 163.4 | +2.1 |
| 2007 | 43.4% | 3.22 | 58.40 | +3.88 | 34.0% | 188.1 | +12.5 |
| 2008 | 35.8% | 3.26 | 60.11 | +3.44 | 50.0% | 196.0 | +11.2 |
| 2009 | 42.9% | 4.29 | 62.88 | +3.88 | 46.3% | 270.0 | +16.6 |
| 2010 | 46.4% | 4.46 | 59.31 | +2.68 | 45.3% | 264.3 | +12.0 |
| 2011 | 53.1% | 4.12 | 58.38 | −0.26 | 33.8% | 240.7 | −1.1 |
| 2012 | 54.6% | 4.55 | 56.18 | −2.70 | 30.5% | 255.4 | −12.3 |
| 2013 | 46.0% | 4.26 | 56.73 | +1.78 | 41.3% | 241.7 | +7.6 |
| 2014 | 46.3% | 3.76 | 53.31 | −2.08 | 39.3% | 200.5 | −7.8 |
| **2015** | **50.0%** | **4.20** | **62.13** | **+6.40** | **56.4%** | **260.9** | **+26.9** |

**2015 ranks 1st of eleven** on surplus per row, on points per game above the bar, and on the share
of its year-1 players who beat the bar. **2nd** on points per game. **3rd** on production per row and
on the share of the class that played at all. Mean rank across nine measures: **3.0**, the best of
the eleven.

**Where the other two breach classes rank.** 2010 is **4.3** (2nd best overall; 2nd on year-1 games
per row and production per row). 2011 is **6.1** — middling. Full mean-rank order, best to worst:
2015 (3.0), 2010 (4.3), 2009 (4.7), 2013 (4.8), 2008 (5.1), 2011 (6.1), 2006 (6.6), 2007 (6.6),
2012 (7.6), 2014 (8.0), 2005 (9.3).

**A caveat the owner should have.** 2015's strength is a **first-year** strength. On career length it
is ordinary: 8th of eleven on career games per player, 3rd on the share reaching 100 games. That is
not a contradiction — the mark being diagnosed is a year-0-to-1 mark and first-year production is
the right thing for it to read — but "2015 was a great draft" is a claim about first years, not
careers, on this evidence.

**The apples-to-apples version.** The class mark is a ratio of sums, so an expensive row counts more
than a cheap one. Weight the outcomes the same way (`CD_WCORR_out.txt`):

| draft class | price-weighted year-1 surplus | rank |
|---:|---:|---:|
| **2015** | **+83.8** | **1** |
| 2009 | +58.3 | 2 |
| 2010 | +58.3 | 2 |
| 2013 | +48.0 | 4 |
| 2008 | +45.2 | 5 |
| 2007 | +38.8 | 6 |
| 2012 | +28.8 | 7 |
| **2011** | **+26.2** | **8** |
| 2006 | +5.7 | 9 |
| 2005 | +3.5 | 10 |
| 2014 | −0.4 | 11 |

2015 is clear of the field by 44%. **2011 is 8th.**

---

## 4 · PART B — THE DECISIVE TEST. ORDER P TRACKS REALISED STRENGTH BETTER.

`CD_CORR_out.txt`, `CD_WCORR_out.txt`, `CD_LOO_out.txt`.

### 4.1 The headline, on the price-weighted measures

These are the like-for-like ones: the outcome is weighted the same way the mark is.

| realised measure | ORDER K | **ORDER P** | landing cand | P − K, Pearson, 95% CI |
|---|---:|---:|---:|---|
| price-weighted year-1 **production** | +0.391 | **+0.655** | +0.518 | +0.130 [+0.012, +0.467] |
| price-weighted year-1 **surplus** | +0.336 | **+0.645** | +0.436 | +0.199 [+0.029, +0.495] |
| price-weighted year-1 **games** | +0.282 | **+0.555** | +0.418 | +0.114 [+0.001, +0.456] |
| price-weighted **share who played** | +0.818 | +0.836 | +0.864 | +0.018 [−0.201, +0.186] |

Correlations shown are Spearman. On the three production measures Order P is more strongly
correlated in **91% to 94%** of bootstrap resamples on Spearman and **98% to 99%** on Pearson. On
"share who played" the two boards are indistinguishable, which makes sense: whether a player got a
game is not what the new charge reads.

### 4.2 It is not 2015 doing the work

Drop the 2015 class and redo it on ten classes:

| price-weighted measure | ORDER K | ORDER P | difference |
|---|---:|---:|---:|
| production | +0.345 | +0.624 | **+0.279** |
| surplus | +0.224 | +0.527 | **+0.303** |
| games | +0.261 | +0.539 | **+0.279** |

Leave-one-class-out against unweighted year-1 production per row: Order P beats Order K on **all
eleven** leave-one-out samples, by +0.194 to +0.448. There is no single class holding the result up.

### 4.3 The move itself is informative

The change Order P makes to each class mark, correlated with that class's realised year-1
production per row: **Spearman +0.827, 95% CI [+0.389, +0.971]**; Pearson +0.787 [+0.573, +0.967].
Against year-1 games per row: Spearman +0.727 [+0.143, +0.923]. **The dispersion Order P adds is
pointed at realised production, not scattered.** That is the sharpest single number in this packet.

### 4.4 Where Order P does not help, reported as a null

On the unweighted per-row measures Order P is better on 7 of 9 (Spearman and Pearson alike). With
2015 dropped that falls to **4 of 9 (Spearman), 6 of 9 (Pearson)**. The two measures where Order P
is consistently *worse*: **share of the class that played in year 1** (−0.127) and **career games
per row** (−0.182). Neither difference is distinguishable from zero. **Order P is not better at
reading long-run career outcomes, and this seat found no evidence that it is.**

### 4.5 Rank agreement

Sum of |rank on the board − rank on realised year-1 production| over eleven classes:
**Order K 28, Order P 16**. Against realised surplus: Order K 34, Order P 32 — essentially unchanged.

The single largest rank error on both boards is the **2011 class**: Order K ranks it **1st** of
eleven, Order P **2nd**, realised production ranks it **6th** and realised surplus **8th**.

---

## 5 · PART C — DECOMPOSING THE +0.0987

`CD_DECOMP_out.txt`, `CD_WHY_out.txt`.

### 5.1 It is broad-based, not one or two rows

| draft class | move | top 1 row | top 3 | top 5 | top 10 |
|---:|---:|---:|---:|---:|---:|
| 2010 | +0.0211 | 37.0% | 39.4% | 93.4% | 62.2% |
| 2011 | +0.0232 | 50.6% | 115.2% | 78.8% | 114.1% |
| 2013 | +0.0226 | 63.4% | 68.1% | 63.0% | 86.1% |
| **2015** | **+0.0987** | **13.2%** | **31.0%** | **44.3%** | **56.2%** |

**No single row carries more than 13% of the 2015 move.** The 102 rows outside the top eight
contribute 51.4% of it. Compare 2013, where one row (Marcus Bontempelli) carries 63% of a much
smaller move. **2015 is the least concentrated of the four.**

### 5.2 The eight biggest movers in the 2015 class

`surpAGE` is games-weighted production above the S1 age bar to the year priced. `surpPED` is the
same against the age bar plus the measured pedigree premium. `chg` is the retained fraction after
the charge — higher means charged less.

| player | pick | pos | v0 | yr-1 games | ppg | surpAGE | surpPED | v1 ORDER K | v1 ORDER P | move | share | chgK | chgP |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jacob Weitering | 1 | KPD | 2869.9 | 20 | 67.7 | +22.86 | +1.44 | 3762.3 | 4509.8 | +747.5 | 13.2% | 0.535 | 1.000 |
| Callum Mills | 3 | SD | 2400.5 | 22 | 74.7 | +17.68 | −0.10 | 3438.8 | 4016.9 | +578.1 | 10.2% | 0.556 | 1.000 |
| Josh Schache | 2 | KPF | 2294.3 | 17 | 51.3 | +8.06 | −2.86 | 1936.2 | 2372.5 | +436.3 | 7.7% | 0.510 | 0.834 |
| Darcy Parish | 5 | MID | 2170.0 | 20 | 72.2 | +15.18 | −2.11 | 3639.2 | 4070.6 | +431.4 | 7.6% | 0.535 | 0.890 |
| Callum Ah Chee | 8 | SF | 1101.9 | 16 | 59.7 | +11.88 | +5.35 | 1780.3 | 2105.6 | +325.3 | 5.7% | 0.505 | 1.000 |
| Josh Dunkley | 25 | MID | 886.3 | 17 | 74.3 | +17.28 | +10.93 | 2331.5 | 2586.3 | +254.8 | 4.5% | 0.510 | 1.000 |
| Matthew Kennedy | 13 | MID | 1520.5 | 3 | 48.0 | −9.02 | −20.30 | 1485.7 | 1238.3 | **−247.4** | −4.4% | 0.765 | 0.559 |
| Clayton Oliver | 4 | MID | 2609.3 | 13 | 70.3 | +13.28 | −6.16 | 3483.9 | 3719.2 | +235.3 | 4.1% | 0.501 | 0.645 |

Read Weitering. He played 20 games in 2016 at 67.7 points, which is 22.86 above the age bar for a
19-year-old key defender. Under Order K the blind charge stripped him to 0.535 of his pedigree,
because 20 career games sits close to the old charge's worst point of exactly 14 games. Under Order P
he cleared his own pedigree bar by +1.44, so the charge on him goes to zero. That is the mechanism
doing exactly what it was built to do.

Read Matthew Kennedy for the other side. He played 3 games at 48.0, which is 20.30 **below** the bar
his pick-13 entry price implies. Order K charged him **less** than Weitering (0.765 retained, because
3 games is far from the 14-game worst point). Order P charges him **more** (0.559). His price falls
247 points. **That is the defect being fixed, visible on one row.**

### 5.3 Class composition is not the explanation

2015 has 110 rows, 67 national-draft, 43 pool, ten top-ten picks, 20 top-twenty picks — the same as
every other class in the window by construction. Its price concentration is mid-range. Its
entry-age mix is ordinary. Nothing about the class's *shape* explains the move.

---

## 6 · PART D — WHY 2015 AND NOT 2010, 2011 OR 2013

### 6.1 The real distinction: 2015 has almost no downside

Split each class's move into the rises and the falls:

| draft class | net move | gross up | gross down | ratio | n up | n down |
|---:|---:|---:|---:|---:|---:|---:|
| 2010 | +0.0211 | +0.0645 | **−0.0434** | 1.49 | 31 | 26 |
| 2011 | +0.0232 | +0.0625 | **−0.0393** | 1.59 | 34 | 32 |
| 2012 | +0.0228 | +0.0584 | −0.0356 | 1.64 | 27 | 25 |
| 2013 | +0.0226 | +0.0740 | **−0.0514** | 1.44 | 22 | 19 |
| **2015** | **+0.0987** | **+0.1085** | **−0.0099** | **11.01** | **41** | **11** |

**2015 does not have the biggest rise.** +0.1085 against 2013's +0.0740 is 47% bigger, not four times
bigger. What makes 2015 four times bigger on the net is that **its fall is almost absent**: −0.0099
against −0.0356 to −0.0826 for every other class in the window. Eleven rows fall where the other
classes drop 19 to 33.

That is the answer to "why 2015". In every other class the rows that beat their pedigree bar and the
rows that miss it roughly offset. In 2015 hardly anyone misses.

### 6.2 The measurement behind that

v0-weighted, over the rows carrying the new charge:

| draft class | mean surplus vs AGE bar | mean surplus vs PEDIGREE bar | share above PED bar | share above AGE bar | retained under K | retained under P |
|---:|---:|---:|---:|---:|---:|---:|
| 2008 | +3.71 | −6.86 | 24.2% | 64.4% | 0.590 | 0.652 |
| 2009 | +4.70 | −7.08 | 17.8% | 58.7% | 0.588 | 0.645 |
| 2010 | +2.64 | −7.38 | 27.4% | 56.5% | 0.601 | 0.664 |
| 2011 | −2.82 | −10.24 | 17.5% | 46.5% | 0.629 | 0.699 |
| 2013 | +0.05 | −9.87 | 28.3% | 58.7% | 0.602 | 0.677 |
| **2015** | **+7.01** | **−2.39** | **33.4%** | **72.7%** | **0.618** | **0.856** |

**Order K charged the 2015 class an utterly ordinary amount — 0.618 retained, mid-pack.** Order P
retains **0.856**, the highest of the eleven by a wide margin; the next highest is 0.709. The class's
price-weighted production sits **+7.01** above the age bar, best of the eleven, and only **−2.39**
below its own pedigree bar, again best of the eleven by more than four points.

Coverage is not the explanation. The share of each class's denominator that carries the new charge
(the rest were 24 or over, or have no readable production, and keep the old charge unchanged) is
69% for 2015 against 56% to 66% elsewhere — slightly high, not extreme.

### 6.3 The four specific tests the brief named

**(i) Low games but high production — the rows the new charge most relieves.** The old charge is at
its worst at exactly 14 career games. The v0-weighted share of each class sitting in 8-24 career
games **and** above its pedigree bar: 2015 **15.0%**, 2013 17.4%, 2010 13.7%, 2011 7.4%. **2015 is
high but 2013 is higher.** This is not on its own the explanation. The corresponding
low-games-but-**below**-the-bar share, which is charged harder: 2015 26.6%, 2013 24.6%, 2010 28.1%,
2011 24.3% — ordinary. The distinguishing quantity is not the count in the cell; it is how far above
or below the bar those rows sit, which is section 6.2.

**(ii) Expensive rows above the pedigree bar.** Rows with v0 ≥ 1000 carry 35% to 47% of each class's
denominator. Their price-weighted surplus against the pedigree bar: **2015 −3.52**, against −8.57 to
−19.97 for every other class in the window. Their mean year-1 games: 2015 **10.85**, second highest.
These rows carry **57%** of the 2015 move. And the top ten picks alone:

| draft class | top-10 picks who played yr 1 | mean yr-1 games | mean ppg | mean surplus vs AGE bar | mean vs PED bar | share of class move |
|---:|---:|---:|---:|---:|---:|---:|
| 2010 | 100% | 12.80 | 65.1 | +4.44 | −10.81 | −0.0017 |
| 2011 | 80% | 8.40 | 56.6 | +1.11 | −11.80 | +0.0085 |
| 2013 | 80% | 13.40 | 63.5 | +5.51 | −8.85 | +0.0219 |
| **2015** | **90%** | **12.40** | **65.6** | **+12.08** | **−1.73** | **+0.0542** |

**2015's top ten picks beat the age bar by +12.08 points a game. The next best class in the window is
+8.81. That single fact carries 55% of the +0.0987 move.** This is the strongest confirmation of the
owner's reading in the packet.

**(iii) Do one or two extreme rows dominate?** No. Section 5.1. 2015 is the *least* concentrated of
the four classes examined.

**(iv) Data artifacts.** None found. Section 2.

### 6.4 2011, the breach the owner's hypothesis does not cover

2011 moves +0.0232, which is the fifth largest move in the window and completely ordinary. Its top
ten picks played 80% of the time for 8.40 games at 56.6 points, +1.11 above the age bar — 8th of
eleven. Its price-weighted year-1 surplus is +26.2, 8th of eleven. **The 2011 class is not a strong
class on realised outcomes.** It breaches because Order K already had it at 1.1363, 0.0037 under the
line, and Order P adds a routine amount on top. Order K ranks 2011 **1st of eleven** on the class
mark against **6th** on realised production and **8th** on realised surplus, and Order P inherits
most of that error.

**This is the part of the finding that contradicts the owner's read, and it is stated here as
prominently as the part that confirms it.** "The three classes now in breach must have just had
strong first years" is true of 2015 and true of 2010. It is not true of 2011.

---

## 7 · WHAT THIS SEAT DOES NOT CLAIM

- **It does not claim Order P is well calibrated in magnitude.** 2015's mark move is 4× the next
  largest. Its lead on price-weighted realised surplus is 1.44× the next largest. The ordering is
  right; the *size* of the 2015 move is larger than the outcome gap alone would suggest. This seat
  measured no way to say by how much, and did not try to fit one.
- **It does not rule on the rail.** Whether a single-class breach at 1.2047 is tradeable, and
  whether the engine's own internal "max class ≤ 1.139" condition should hold, are rulings.
- **It does not claim significance.** With eleven classes, every Spearman interval in this packet is
  roughly a unit wide. The paired-difference Pearson intervals on the three price-weighted
  production measures are the only ones that exclude zero, and they only just do.
- **It found no test it could not run.** Every measurement in the brief was executed.

---

## 8 · FILES

| file | what |
|---|---|
| `cd_lib.py` | shared loaders; the class-mark arithmetic restated from `op_class.py`; the S1 age bar and the wired pedigree premium |
| `cd_repro.py` / `CD_REPRO_out.txt` / `CD_REPRO.json` | part E: reproduction, denominators, class composition |
| `cd_outcomes.py` / `CD_OUTCOMES_out.txt` / `CD_OUTCOMES.json` | part A: realised year-1 outcomes and ranks |
| `cd_corr.py` / `CD_CORR_out.txt` / `CD_CORR.json` | part B: nine measures, Spearman and Pearson, bootstrap CIs |
| `cd_wcorr.py` / `CD_WCORR_out.txt` | part B: the price-weighted, like-for-like version |
| `cd_loo.py` / `CD_LOO_out.txt` | part B: leave-one-class-out and rank agreement |
| `cd_decomp.py` / `CD_DECOMP_out.txt` / `CD_DECOMP.json` | parts C and D: row-level decomposition and named movers |
| `cd_why.py` / `CD_WHY_out.txt` / `CD_WHY.json` | part D: up/down split, the two bars, the top of the draft, artifact sweep |
| `cd_inst.py` / `CD_INST_out.txt` | part E: artifact checks and the charge-versus-price caution |

The scripts read the built matrices from the build seat's scratch directory
(`per_entrant_OKRULED.json`, `per_entrant_PBUILT.json`, `per_entrant_O35FINAL.json`) and two files
that live in the repo (`docs/evidence/order32_s1_2026-08-17/CONSTRUCTIONS_S1.json` and
`docs/evidence/order_p_build_2026-08-18/PREMIUM_SURFACE.json`). Nothing else is read and nothing is
written outside this directory.
