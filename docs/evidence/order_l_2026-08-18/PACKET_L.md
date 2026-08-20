# PACKET — ORDER L: THE NO-ARB TABLES RE-ISSUED

Read-only seat. No price moved. No board was built. No engine, board or law file was touched.
Prereg: `PREREG_L.md`, pushed before any number (commit 5e1d6e3).
Document: `ORDER_L_NOARB.html` (this directory).
Published copy: https://claude.ai/code/artifact/f1273981-1688-4b9c-9ec9-4432d7af159d (private until shared).

The owner raised two gaps in Order K's no-arb document. Both are closed here.

---

## 1. WHAT WAS ASKED, AND WHAT WAS DONE

**Gap 1.** The band tables had no window split. Only the pool-arm tables were split into primary and
modern. Every band table is now shown in both windows, on all three boards.

**Gap 2.** The owner asked for the tables again with the 2005 and 2006 classes excluded from the
numerator and the denominator. Every table is now also shown with those two cohorts removed. It is
labelled a sensitivity check on the page, and it is never the headline.

Nothing was rebuilt. The three boards are the three walk-forward matrices Order K already built. The
value rules, the population filter and the window definitions came from the instruments that were
already pinned and disclosed. Order L added one thing: a filter on which cohorts are counted.

Instrument pins, computed at run:

| file | md5 | status |
|---|---|---|
| `t338_extended_DISCLOSED.py` | `d59ad550116ebbe3d90ed82becd2c4d5` | pinned, asserted |
| `noarb_table_338.py` | `0f8220351c64c56ccfa90c60edcdfa5f` | pinned, asserted |
| `harness_pvc_REPINNED_pass3.py` | `02dcf28c7bd0d39b3526e24c5cc0a87a` | printed |
| `noarb_table_allarm.py` | `8673d7e33a6267ff51ff6331cc13b171` | printed |
| `w2_forward_calibration.py` | `106c6880d3fd4d1e9c948df38f2fdfc6` | read only |

The `value_at` function in `ol_bands.py` is asserted byte-identical to the disclosed instrument's at
run time. If it is ever edited, the run halts.

## 2. WHAT THE TWO WINDOWS ARE

A cohort is every player eligible to debut in the same year. A national draft pick taken in November
2018 first plays in 2019, so he is in the 2019 cohort. That is the pool-arm tables' own rule. Order L
applies the same rule to the band tables so the two sets can be read together.

- **Primary window = cohorts 2005-2023 = the national drafts of 2004-2022.** 1,200 players.
- **Modern window = cohorts 2019-2023 = the national drafts of 2018-2022.** 311 players.

The primary window is the whole national-draft population. So the primary tables are Order K's
published tables. That was checked cell by cell.

## 3. THE BAND TABLES, BOTH WINDOWS — THE CURRENT CANDIDATE (ORDER K f3101883)

Year-1 appreciation, and the verdict against the 14% carry rail.

| band | n primary | primary | verdict | n modern | modern | verdict | modern minus primary |
|---|---|---|---|---|---|---|---|
| ALL picks 1-64 | 1200 | **+4.23%** | ok | 311 | **-0.96%** | **SELL-RED** | -5.19 |
| picks 1-20 | 380 | +9.22% | ok | 100 | +9.58% | ok | +0.36 |
| picks 21-64 | 820 | -3.67% | SELL-RED | 211 | **-17.97%** | SELL-RED | -14.30 |
| picks 1-10 | 190 | +8.22% | ok | 50 | **+13.65%** | ok | +5.43 |
| picks 11-20 | 190 | +11.16% | ok | 50 | +2.11% | ok | -9.05 |
| picks 21-30 | 190 | +5.26% | ok | 50 | **-14.26%** | **SELL-RED** | -19.52 |
| picks 31-40 | 190 | -10.70% | SELL-RED | 50 | -14.27% | SELL-RED | -3.57 |
| picks 41-64 | 440 | -6.89% | SELL-RED | 111 | **-25.06%** | SELL-RED | -18.17 |

Full year paths, current candidate, primary window (yr0 to yr7):

| band | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 |
|---|---|---|---|---|---|---|---|---|
| ALL 1-64 | 1.000 | 1.042 | 1.176 | 1.364 | 1.498 | 1.532 | 1.492 | 1.320 |
| 1-20 | 1.000 | 1.092 | 1.220 | 1.396 | 1.559 | 1.566 | 1.480 | 1.317 |
| 21-64 | 1.000 | 0.963 | 1.106 | 1.314 | 1.401 | 1.478 | 1.510 | 1.324 |
| 1-10 | 1.000 | 1.082 | 1.209 | 1.400 | 1.552 | 1.518 | 1.423 | 1.247 |
| 11-20 | 1.000 | 1.112 | 1.241 | 1.388 | 1.571 | 1.660 | 1.591 | 1.456 |
| 21-30 | 1.000 | 1.053 | 1.223 | 1.467 | 1.632 | 1.629 | 1.686 | 1.458 |
| 31-40 | 1.000 | 0.893 | 0.974 | 1.288 | 1.268 | 1.403 | 1.294 | 1.161 |
| 41-64 | 1.000 | 0.931 | 1.096 | 1.180 | 1.277 | 1.386 | 1.512 | 1.325 |

Full year paths, current candidate, modern window:

| band | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 |
|---|---|---|---|---|---|---|---|---|
| ALL 1-64 | 1.000 | 0.990 | 1.071 | 1.180 | 1.241 | 1.376 | 1.238 | 1.193 |
| 1-20 | 1.000 | 1.096 | 1.194 | 1.336 | 1.480 | 1.578 | 1.356 | 1.548 |
| 21-64 | 1.000 | 0.820 | 0.873 | 0.929 | 0.854 | 1.062 | 1.058 | 0.647 |
| 1-10 | 1.000 | 1.137 | 1.257 | 1.450 | 1.621 | 1.667 | 1.426 | 1.604\* |
| 11-20 | 1.000 | 1.021 | 1.077 | 1.127 | 1.223 | 1.420 | 1.233 | 1.442\* |
| 21-30 | 1.000 | 0.857 | 1.006 | 0.917 | 0.810 | 1.093 | 1.361 | 0.485\* |
| 31-40 | 1.000 | 0.857 | 0.920 | 1.283 | 1.264 | 1.539 | 1.349 | 1.018\* |
| 41-64 | 1.000 | 0.749 | 0.694 | 0.636 | 0.548 | 0.627 | 0.482 | 0.487 |

**Two verdicts change when you look at the modern window instead of the total.** ALL picks 1-64 goes
from ok to SELL-RED. Picks 21-30 goes from ok to SELL-RED. Picks 1-10 gets better in the modern
window, not worse.

Comparison boards, year-1 appreciation, both windows:

| band | landing primary | landing modern | cand 31 primary | cand 31 modern |
|---|---|---|---|---|
| ALL 1-64 | +2.98% ok | -1.69% SELL-RED | +6.62% ok | +3.00% ok |
| 1-20 | +8.36% ok | +8.92% ok | +14.78% BUY-RED | +16.12% BUY-RED |
| 21-64 | -5.54% SELL-RED | -18.83% SELL-RED | -6.28% SELL-RED | -18.17% SELL-RED |
| 1-10 | +7.93% ok | +13.24% ok | +16.19% BUY-RED | +22.25% BUY-RED |
| 11-20 | +9.20% ok | +1.00% ok | +12.04% ok | +4.89% ok |
| 21-30 | +2.76% ok | -16.34% SELL-RED | +3.68% ok | -14.76% SELL-RED |
| 31-40 | -12.84% SELL-RED | -15.92% SELL-RED | -12.38% SELL-RED | -16.55% SELL-RED |
| 41-64 | -7.88% SELL-RED | -23.94% SELL-RED | -11.36% SELL-RED | -23.12% SELL-RED |

## 4. THIN CELLS — DISCLOSED, NOT SMOOTHED

The rule was fixed in writing before any number was computed. A cell built on fewer than 30 players
is flagged. Fewer than 10 gets a second flag. Fewer than 5 is not printed at all.

What is actually flagged on this page:

- **Only the year-7 column of the four ten-pick bands in the modern window.** Each of those four
  cells rests on 20 players. They are marked with an asterisk above and coloured on the page.
- Nothing is very thin. Nothing was suppressed. No cell has fewer than 5 players.
- **Every year-1 cell on every band table rests on 50 players or more.** The year-1 cell is the one
  the verdict is about, so no verdict on this page rests on a thin sample.

Why the modern counts fall in later years: a player drafted in 2022 has not had a seventh season
yet. At year 5 the modern window holds 4 of its 5 cohorts, at year 6 it holds 3, and at year 7 it
holds 2 (the 2019 and 2020 cohorts). Every count is printed on the page in the "n by year" table.

On the pool arms in the modern window the samples are genuinely small: UNR 13, IRE 12, PDA 13,
PDN 25, SSP 31. The southern academy has no players in the modern window at all, so it does not
appear there. The mid-season draft has no year-1 cell in any window, because an MSD player debuts in
his own draft year; those rows are excluded from that year and counted, never scored zero.

## 5. THE 2005/06 EXCLUSION — WHAT IT DOES

**The interpretation used, stated plainly on the page so it can be corrected:** the 2005 and 2006
cohorts are removed from the population entirely. Not their first two seasons. The players
themselves, out of the year-1 average and out of the entry average alike, everywhere they would
otherwise appear.

On the cohort clock those two classes are the **national drafts of 2004 and 2005**. That is 125 of
the 1,200 national-draft players. The identification was made against the numbers the owner read:
those are the two classes that mark 0.899 and 0.856 on the year-1 class measure for this board.

### Effect on the bands, current candidate, primary window

| band | all cohorts | excl 05/06 | move | verdict change |
|---|---|---|---|---|
| ALL 1-64 | +4.23% | +6.42% | +2.19 | none |
| 1-20 | +9.22% | +11.31% | +2.09 | none |
| 21-64 | -3.67% | -1.30% | +2.37 | none, still SELL-RED |
| 1-10 | +8.22% | +10.20% | +1.98 | none |
| 11-20 | +11.16% | +13.48% | +2.32 | none |
| 21-30 | +5.26% | +8.61% | +3.35 | none |
| 31-40 | -10.70% | -8.03% | +2.67 | none, still SELL-RED |
| 41-64 | -6.89% | -5.84% | +1.05 | none, still SELL-RED |

Every band improves by between 1.0 and 3.4 points. **No verdict changes on any band, on any board.**
The two negative bands stay negative. Picks 21-64 stays negative.

### Effect in the modern window

**None at all.** The modern window starts at the 2019 cohort, so it never contained a 2005 or 2006
player. This was stated in writing before the run and then checked: every modern cell is identical
with and without the exclusion, to exactly zero difference. That is registered self-check L-SC3 and
it passed.

### Effect on the pool arms, primary window, current candidate

Only three lines move, because only three have any players in those two cohorts.

| arm | all cohorts | excl 05/06 | n falls |
|---|---|---|---|
| RD (rookie draft) | -3.39% | -3.10% | 623 to 531 |
| IRE (Irish) | +13.34% | +11.62% | 47 to 45 |
| ALLPOOL | -4.93% | -4.97% | 1016 to 922 |

Every other arm is unchanged to the last decimal. Note that the pooled all-pool line moves the wrong
way by 0.04 points — the exclusion does not help the pool. SSP stays at +52.71% BUY-RED either way.

## 6. THE YEAR-1 CLASS MARK

Order K's `ok_class.py` machinery, unchanged. Cohort clock. Each class gets one number: the total
year-1 price of the class divided by its total entry price. The published mark averages eleven
classes, 2005 to 2015. The exclusion leaves nine classes, 2007 to 2015.

| board | standing (11 classes) | excl 05/06 (9 classes) | move |
|---|---|---|---|
| **ORDER K f3101883 — the current candidate** | **1.0324** | **1.0669** | +0.0344 |
| the landing candidate 1f176444 | 1.0232 | 1.0564 | +0.0332 |
| candidate 31 fe6be9d6 | 1.0360 | 1.0633 | +0.0273 |

**The supervisor's 1.0669 for the current candidate reproduces.** This run reads 1.06685. The
difference from the supervisor's figure is 0.00005, which is the rounding of the published
four-decimal class rows. Registered check L-SC4 passed.

Every class, printed:

| class | national draft | ORDER K | landing | cand 31 | n | in the mark? |
|---|---|---|---|---|---|---|
| 2005 | 2004 | **0.8985** | 0.8880 | 0.9251 | 110 | removed by the sensitivity |
| 2006 | 2005 | **0.8562** | 0.8599 | 0.9011 | 109 | removed by the sensitivity |
| 2007 | 2006 | 1.0579 | 1.0351 | 1.0313 | 122 | in the mark |
| 2008 | 2007 | 1.0713 | 1.0480 | 1.0626 | 122 | in the mark |
| 2009 | 2008 | 1.0063 | 1.0007 | 1.0084 | 134 | in the mark |
| 2010 | 2009 | 1.0432 | 1.0391 | 1.0574 | 126 | in the mark |
| 2011 | 2010 | 1.1359 | 1.1308 | 1.1410 | 138 | in the mark |
| 2012 | 2011 | 1.1363 | 1.1311 | 1.1197 | 145 | in the mark |
| 2013 | 2012 | 1.0673 | 1.0536 | 1.0606 | 108 | in the mark |
| 2014 | 2013 | 1.0535 | 1.0461 | 1.0720 | 100 | in the mark |
| 2015 | 2014 | 1.0300 | 1.0230 | 1.0167 | 121 | in the mark |
| 2016 | 2015 | 1.1060 | 1.0955 | 1.1069 | 110 | — |
| 2017 | 2016 | 1.0289 | 1.0145 | 1.0429 | 125 | — |
| 2018 | 2017 | 1.0562 | 1.0518 | 1.0883 | 106 | — |
| 2019 | 2018 | 1.0147 | 1.0086 | 1.0140 | 124 | — |
| 2020 | 2019 | 0.9810 | 0.9735 | 1.0024 | 91 | — |
| 2021 | 2020 | 0.9170 | 0.9159 | 0.9767 | 88 | — |

The two removed classes are the only two in the mark window that sit below 1.00. Every other class
in the window reads between 1.006 and 1.136.

## 7. THE W2 INSTRUMENT QUESTION — ANSWERED

The question: was the class target of 1.03 floor and ~1.08 ideal computed on the fast navigation
calibrator or on the full built matrix? The answer decides whether the board clears the floor
comfortably or barely.

### 7a. The floor was not computed on either instrument. It is the owner's own prior.

`docs/evidence/order33_w2_2026-08-17/PREREG_W2.md`, section 0, line 9, registered and pushed before
any result number:

> Ruling R-CAL (2026-08-17): the year-1 entry class should in aggregate appreciate over its entry
> values with **floor 1.03, ideally ~1.08**. This is registered as a **LOOSE PRIOR, not a target**.

`PACKET_W2.md`, honesty ledger: *"The owner's prior (floor 1.03 / ideal 1.08) was registered before
computation."*

### 7b. The instrument the board is measured against is the FULL BUILT MATRIX.

`PREREG_W2.md` section 1: *"Primary object: the walk-forward per-entrant matrix
`per_entrant_O31FFINAL.json`"*, with its md5, store, engine head and record count all asserted before
the run.

The deciding code, `w2_forward_calibration.py`. Population, lines 117-121:

```python
    yr = r['year']
    if yr < ENTRY_FLOOR or yr > 2021:
        continue
    assert len(r['vpath']) >= 1 and r['vpath'][0] is not None, 'missing year-1 vantage: ' + k
```

with `ENTRY_FLOOR = 2005` (line 23) and, line 121:

```python
    POP.append(dict(key=k, yr=yr, arm=arm, v0=float(r['v0']), p1=float(r['vpath'][0]), ...
```

The class mark, lines 142-150:

```python
        P0 = sum(p['v0'] for p in rows); P1 = sum(p['p1'] for p in rows)
        ...
        rec = dict(cls=y, n=n, P0=P0, P1=P1,
                   R_cand=P1 / P0 if P0 > 0 else float('nan'),
```

`p1` is `r['vpath'][0]` — the engine's own walk-forward year-1 valuation out of the built matrix.
There is no analytic formula anywhere in that path.

The gate was registered on that scorer. `docs/evidence/order_i_2026-08-18/PREREG_I.md` line 139:

> | **G1** | year-1 class cohort mark (W2 estimator, `mean_0515`) | **>= 1.03**, ideal ~1.08,
> **strictly < 1.14** | **1.0421** |

and 1.0421 is that scorer's output on a built matrix. `docs/evidence/order_d_2026-08-17/o35_w2_score.py`
runs `w2_forward_calibration.py` whole against `per_entrant_O35FINAL.json` and then, lines 44-45:

```python
per = {r['cls']: r['R_cand'] for r in R['level']['per_class_all']}
mean_0515 = float(np.mean([per[y] for y in range(2005, 2016)]))
```

Its console output, `docs/evidence/order_d_2026-08-17/W2_D_out.txt` line 2:
`mean 2005-15 1.0421`.

**Verdict: the built matrix, read by the W2 scorer. Not the navigation calibrator.**

### 7c. So why does the current candidate read 1.0324 in Order K?

Because that is a different set of draft classes, not a different instrument.

- `ok_class.py` labels a class by the year it could first debut and averages classes 2005-2015. Those
  are the national drafts of **2004-2014**.
- `w2_forward_calibration.py` labels a class by its draft year and averages 2005-2015. Those are the
  national drafts of **2005-2015**.

The two windows are shifted by one year at both ends. Order K's cohort class 2005 is the 2004 draft,
which the W2 population excludes outright at `ENTRY_FLOOR = 2005`. Order K's window also stops one
class earlier.

Demonstration rather than assertion: on candidate 31, `ok_class.py`'s cohort class 2006 reads 0.9011,
and the filed W2 packet's draft class 2005 reads 0.9011. Same players, same number, different label.

Take Order K's own class rows and average them over the same draft classes the W2 scorer uses:

| board | Order K cohort 2005-2015 | same rows, draft 2005-2015 | W2 scorer, draft 2005-2015 | difference |
|---|---|---|---|---|
| ORDER K f3101883 | 1.0324 | **1.0513** | **1.0513** | -0.00000 |
| landing candidate | 1.0232 | **1.0421** | **1.0421** | -0.00000 |
| candidate 31 | 1.0360 | **1.0525** | **1.0525** | +0.00000 |

The whole gap is the class window. There is no instrument disagreement to reconcile. Order K's own
note attributed the gap to the analytic-versus-built distinction and to the population size; that
note is superseded — the cause is the class window, and aligning it closes the gap to five decimal
places on all three boards.

### 7d. What this means for the floor

| reading | current candidate | floor 1.03 | margin |
|---|---|---|---|
| **W2 scorer, built matrix, draft classes 2005-2015 (the registered gate basis)** | **1.0513** | CLEARS | **+0.0213** |
| navigation calibrator (Order I record) | 1.0515 | CLEARS | +0.0215 |
| `ok_class.py`, cohort classes 2005-2015 | 1.0324 | CLEARS | +0.0024 |
| `ok_class.py`, 2005/06 excluded — SENSITIVITY | 1.0669 | CLEARS | +0.0369 |
| W2 scorer, 2005/06 removed (draft 2006-2015) — SENSITIVITY | 1.0708 | CLEARS | +0.0408 |

**On the basis the gate was actually registered on, the board clears the floor comfortably at 1.0513,
by 0.0213.** It does not clear it barely.

The navigation calibrator reads 1.0515 on this board against the built matrix's 1.0513. The two agree
to 0.0002. The navigation instrument is an accurate stand-in for the built matrix, not a rival to it.
The 1.0324 figure is not wrong, but it is a different class window and it should not be read against
the W2 floor.

The ideal of ~1.08 is still not reached on any basis except the two sensitivity rows, and the
sensitivity rows are not the headline. Reported, not chased.

## 8. THE REGISTERED CHECKS

| check | what it tests | result |
|---|---|---|
| L-SC1a | the primary tables match Order K's stored record to 1e-9 | **FAILS on rounding only.** Order K's JSON stores ratios at 4 decimals and means at 2. Worst difference 4.9e-05, which is under half a published digit. Disclosed, not worked around. |
| L-SC1b | Order L's unrounded values, put through Order K's own rounding, compared for exact equality | **PASS.** 816 comparisons across 3 boards, 8 bands, 8 ratios, all sample counts and both means per year. Zero mismatches. |
| L-SC2 | the draft clock and the cohort clock agree on every ND row | **PASS**, asserted at run |
| L-SC3 | the exclusion moves nothing in the modern window | **PASS**, worst difference exactly 0.000e+00 |
| L-SC4 | the class arithmetic reproduces the supervisor's 1.0669 | **PASS**, this run reads 1.06685 |
| L-SC5 | the arm tables reproduce Order K's arm cells | **PASS**, 459 comparisons, zero mismatches |

**Prereg deviation, disclosed.** The prereg registered L-SC1 at a tolerance of 1e-9 and said the run
would halt if it failed. That tolerance cannot be met against a stored record that was rounded to
four decimals before it was written. The check was therefore split in two and both halves are
reported above. No number was moved to make either half pass. The deviation is the interpretation
rule, not the numbers.

## 9. WHAT IS STILL TRUE AND WAS NOT CHANGED

Nothing in the board changed. The two open defects the Order K box names are still open: picks 31-40
and picks 41-64 still lose money in year one on the primary window, and they lose more in the modern
window. Supplemental selection still appreciates about 50% in year one. The two gate breaches Order K
reported — Daniel Annable rising 7 points, and the veteran net cap at -695 against -667.92 — are
unchanged and untraded. The "what is in this board and what is still broken" box is carried on the
new page byte for byte out of the Order K document.

## 10. FILES

```
docs/evidence/order_l_2026-08-18/
  PREREG_L.md            registered before any number, commit 5e1d6e3
  PACKET_L.md            this file
  ORDER_L_NOARB.html     the owner document
  ol_bands.py            the ND band tables, both windows, both variants
  ol_arms.py             the pool arms, both windows, both variants
  ol_class.py            the class mark, and the W2 second reading
  ol_selfcheck.py        L-SC1a, L-SC1b, L-SC3
  ol_pages.py            the document builder
  bb_L.sh                the run script, thread-pinned and sequential
  BANDS_L.json  ARMS_L.json  CLASS_L.json
  BANDS_L_out.txt  ARMS_L_out.txt  CLASS_L_out.txt  SELFCHECK_L_out.txt
```

Seat: ORDER L INSTRUMENT SEAT, 2026-08-18.
