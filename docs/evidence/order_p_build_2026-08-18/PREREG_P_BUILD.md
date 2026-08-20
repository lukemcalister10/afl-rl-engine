# PREREG P-BUILD — WIRING THE PEDIGREE-CONDITIONAL CHARGE INTO THE ENGINE

**Seat:** ORDER P BUILD. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Base:** ORDER K's dial stack, board `f3101883`, board total 673,097.

**This document is pushed BEFORE the first engine edit.** Every number below is a prediction made in
advance. Nothing here is a result.

---

## 1 · WHAT IS BEING BUILT, AND WHAT IS BEING REMOVED

### 1.1 The defect being removed

ORDER K carries this charge on the pedigree leg, at `engine/rl_after/_merged_recover.py` line 3770:

```
pi *= max(0, 1 - ETA * ( (g/GAMMA_D) * exp(1 - g/GAMMA_D) ) )        ETA = 0.50, GAMMA_D = 14
```

It reads **games and nothing else**. It peaks at exactly 14 games and then falls away. A player with
36 games keeps more of his unearned entry price than a player with 17 games, no matter how either of
them played. The owner asked for that to go.

### 1.2 The charge being put in its place

```
pi *= exp( -LAMBDA * A(g) * T(s_P) )          for rows aged under 24 at the year being priced
pi *= the ORDER K charge above                for rows aged 24 and over

A(g)  = 1 - exp(-g / G0)                      how much evidence g games is. A(0) = 0 exactly.
T(s)  = clip( 1 - THETA_R * (s - s0), 0, TMAX )
s_P   = the games-weighted mean of ( season average - BAR_P ) over every season played to date
BAR_P = the S1 C3 age bar for that position and age  +  the pedigree premium PG(ln v0, class)
```

`PG` is a measured surface: how far above his age bar a player who entered at that price actually
produces. It was estimated in ORDER P by games-weighted local-linear kernel regression on `ln(v0)`,
tricube kernel, bandwidth 0.40 in log-v0 units, separately for TALL (KPD/KPF/RUCK) and SMALL
(MID/SD/SF), on 5,041 season rows over 1,575 players. It is **pooled over age**. The age-carrying
variant was measured in ORDER P and is worse on every rail; it is not built and will not be switched
to.

### 1.3 The constants. Measured, not tuned. None of them is re-fitted in this build.

| constant | value baked | source |
|---|---:|---|
| `G0` | 9.890000000000008 | `MECH_P.json::G0` — the `BETA_P(g)` curve fit, 90% CI [7.60, 12.98] |
| `BETA_sat` | 0.11464630061141393 | `MECH_P.json::BETA_sat`, 90% CI [0.10416, 0.12718] |
| `LAMBDA` | 0.1743833036575403 | `STEP4_P.json::mechanism.LAMBDA` — **solved** by the anchoring identity |
| `THETA_R` | derived as `BETA_sat / LAMBDA` = 0.6574385173741182 | not free |
| `s0` | -2.452720891469074 | games-weighted mean of `s_P` over the young cohort |
| `s_P5` | -33.06133449874688 | the cohort's own 5th percentile of `s_P` |
| `TMAX` | derived as `1 - THETA_R*(s_P5 - s0)` = 21.12328154884598 | not free |
| age gate | 24 | ORDER N / ORDER P |

**Asserted in the engine before any board is priced:** `LAMBDA * THETA_R == BETA_sat` to within
1e-15, and `A(0) == 0.0` exactly.

**Everything else from ORDER K is unchanged:** age-bar dose 0.40, kappa 0.20, gamma_u 8, the
tall/small sitter factor (`_O36_TALL`; TALL = KPD/KPF/RUCK, MID is NOT tall), the fade-floor fix,
the owner's pick-curve fade, lam_rel 1.08.

### 1.4 The dial

A new environment dial `RL_O37`. It implies the O36 stack (and therefore O35 / O32 / O31) and, where
the ORDER K constants are not passed explicitly, defaults them to ORDER K's ruled values.

**With `RL_O37` unset the board must reproduce `f3101883` BYTE-EXACT.** That is falsifier B1 and it
halts the build.

---

## 2 · PREDICTIONS. THESE ARE THE ORDER P OFFLINE ESTIMATES, AND THEY ARE PROVISIONAL BY CONSTRUCTION.

ORDER P priced this charge offline through a linear identity on two built matrices. That identity was
proved to 1.9e-16 on the charge itself, but the offline board is not a build: it does not run the
engine's downstream non-linearities, its rounding, or its assert wall.

**Two precedents say the built numbers can differ. ORDER K's built board came in materially off its
own predictions. ORDER N's offline estimate overstated the late-band damage.** So the table below is
what I expect, not what I claim. **Any material difference will be reported loudly and NOT quietly
reconciled.** I fix "material" now, before seeing anything: **0.5 percentage points on a band
appreciation, 0.002 on a class mark, 0.3% on the board total.**

### 2.1 The board

| quantity | ORDER K | **ORDER P predicted** |
|---|---:|---:|
| board total | 673,097 | **666,450 (-0.99%)** |
| rows that move | — | **288 of 804 (133 up, 155 down)** |
| veteran churn (age 24+) | 947 | **951**, rail 1,002 |
| veteran net (age 24+) | -601 | **-595**, rail ±668 |

### 2.2 The class

| basis | ORDER K | **ORDER P predicted** |
|---|---:|---:|
| W2 scorer, draft classes **2005-2015**, `ENTRY_FLOOR = 2005` (the registered basis) | 1.0513 | **1.0613** |
| cohort clock | 1.0324 | **1.0322** |

**The registered basis is drafts 2005-2015 with `ENTRY_FLOOR = 2005`. It is NOT the `ok_class.py`
2004-2014 window.** That confusion cost a full day on an earlier seat and it is written here so it
cannot happen again.

### 2.3 The bands, year 0 to year 1

**PRIMARY window, cohorts 2005-2023:**

| band | ORDER K | **ORDER P predicted** |
|---|---:|---:|
| ALL picks 1-64 | +4.23% | **+5.33%** |
| picks 1-20 | +9.22% | **+9.79%** |
| picks 21-64 | -3.67% | **-1.73%** |
| picks 1-10 | +8.22% | **+8.62%** |
| picks 11-20 | +11.16% | **+12.07%** |
| picks 21-30 | +5.26% | **+7.38%** |
| picks 31-40 | -10.70% | **-8.88%** |
| picks 41-64 | -6.89% | **-5.03%** |

**MODERN window, cohorts 2019-2023:**

| band | ORDER K | **ORDER P predicted** |
|---|---:|---:|
| ALL picks 1-64 | -0.96% | **+1.45%** |
| picks 1-20 | +9.58% | **+12.88%** |
| picks 21-64 | -17.97% | **-17.01%** |
| **picks 1-10** | +13.65% | **+18.85% — EXPECTED TO BREACH THE +14% RAIL** |
| picks 11-20 | +2.11% | **+1.94%** |
| picks 21-30 | -14.26% | **-13.84%** |
| picks 31-40 | -14.27% | **-11.73%** |
| picks 41-64 | -25.06% | **-24.88%** |

### 2.4 The pool arms, PRIMARY window

| arm | ORDER K | **ORDER P predicted** |
|---|---:|---:|
| ALLPOOL | -4.93% | **-3.60%** |
| RD | -3.39% | **-1.86%** |
| UNR | -42.91% | **-43.12%** |
| IRE | +13.34% | **+13.62%** |
| PDA | -20.70% | **-20.25%** |
| PDN | -40.32% | **-40.78%** |
| PDS | -27.70% | **-26.15%** |
| **SSP** | **+52.71% — ALREADY OVER THE RAIL UNDER ORDER K** | **+58.17%** |

**SSP is an INHERITED breach.** It is over the +14% buy rail on ORDER K, before this order touched
anything. It will be reported separately and on its own line. It will never be folded into a pass.

### 2.5 The named rows — DIRECTIONS ONLY, NEVER TARGETS

**No constant in this build was chosen with any of these rows in view, and no row's value is an
acceptance criterion.** This is a standing prohibition in this project after a real error. What is
written below is the DIRECTION the derived rule predicts, so the build can be checked for sign
agreement, and nothing else.

| row | ORDER K | predicted direction under ORDER P | why, in one sentence |
|---|---:|---|---|
| Harry Dean | 2403 | **up, substantially** | 17 games, and still above his own pedigree bar, so he pays nothing |
| Cooper Duff-Tytler | 1505 | **up** | below his pedigree bar but only just, so he pays far less than ORDER K's blind 49.9% |
| Xavier Taylor | 1162 | **down** | 2 games and 22 points a game below what a player at his price produces |
| Daniel Annable | 1537 | **down** | same shape, further below |
| Dylan Patterson | 1440 | **down** | 5 games, 33 points a game below his pedigree bar |
| Isaac Kako | 832 | **down** | 36 games sat on the far side of the blind bump; the new charge does not fall back |
| Josh Smillie | 772 | **unchanged, exactly** | zero career games, `A(0) = 0` |
| Milan Murdock | 156 | **unchanged, exactly** | age 26, outside the age gate |
| Zeke Uwland | 1949 | **down** | pick 2, 17 games, 20.9 points a game below his pedigree bar |
| Cooper Harvey | 331 | **up** | pick 56, 17 games, half a point below his pedigree bar, so he pays nothing |

---

## 3 · FALSIFIERS

**HALT-AND-REPORT means: stop, do not trade the broken law against another, report it.**

| # | falsifier | consequence |
|---|---|---|
| **B1** | the dial-off board is not `f3101883` byte-exact | **HALT.** The dial is not clean and nothing may be read off the dial-on board |
| **B2** | two identical dial-on runs do not produce the identical board file | **HALT.** Determinism |
| **B3** | any of the 89 wired day-0 ENTRY values moves | **HALT.** `A(0) = 0` is a structural law of this engine |
| **B4** | the veteran pool (age 24+) breaches churn 1,002 or net ±668 | **HALT** |
| **B5** | the year-1 class mark on the registered W2 basis falls below 1.03, or reaches 1.14 | **HALT** |
| **B6** | any pick band or pool arm goes above +14% year-0-to-1, **other than** (a) the inherited SSP arm and (b) MODERN picks 1-10 | **HALT** |
| **B7** | picks 31-40 or picks 41-64 do not materially improve against ORDER K in the PRIMARY window | **REPORT.** The owner's second complaint about ORDER N is not answered |
| **B8** | a cliff appears in age, games or pick — a discontinuity the ORDER K continuity object does not already carry | **HALT** |
| **B9** | `LAMBDA * THETA_R != BETA_sat` in the wired code | **HALT.** The tilt is no longer the measurement |
| **B10** | any row prices above its own uncharged (eta-zero) price | **HALT.** This is the forbidden-set bound P-F1 |
| **B11** | the engine's baked premium surface does not reproduce `op_lib.Premium` to 1e-9 at every grid node | **HALT** |
| **B12** | any mature row's age-bar behaviour changes — the S1 bar must stay byte-identical from age 24 | **HALT** |
| **B13** | **a built number differs materially from the ORDER P estimate** (0.5pp on a band, 0.002 on a class mark, 0.3% on the board total) | **NOT a halt. A LOUD REPORT.** The estimate is provisional by construction |

**MODERN picks 1-10 breaching at about +18.85% is the EXPECTED BRANCH TRIGGER, not a build failure.**
It will be reported as prominently as every pass. No cap will be bolted on to hide it. No constant
will be re-tuned to move it.

---

## 4 · DISCLOSED IN ADVANCE

1. **The sitter PRINT reference regenerates.** Every ruled fade change in this project has required
   it, and ORDER D disclosed it in the same words. The RAW ENTRY OBJECT `derived_v0` must stay
   byte-identical on all 89 rows; the printed day-0 price is entry value times the sitter fade, and
   a build that changes what a young row is worth after games can change nothing at day 0 because
   `A(0) = 0`. **If the printed reference file needs regenerating, that is disclosed on the packet
   as a gate result, never folded into a pass.**
2. **The engine's games axis is `pv_games`, which applies the mid-season-draft games-of-12 scaling.
   The ORDER P offline estimate used raw career games.** They differ only for MSD rows in their own
   entry season. I am using the engine's own axis, because that is the axis the charge it replaces
   already uses. The difference is disclosed and measured on the packet.
3. **The pedigree label `v0` is the row's own derived day-0 entry price in engine currency.** In the
   ORDER P offline files it was rounded to one decimal by the matrix emitter. The engine will round
   it the same way, so the two agree exactly rather than nearly.
4. **The premium is held flat outside the support of the fit** — below `v0` 91.2 (SMALL) / 96.2
   (TALL) and above 3,444.3 (SMALL) / 2,946.9 (TALL). It is never extrapolated.
5. **The premium is a lower bound**, because it is estimated on players who play. ORDER P disclosed
   this and did not repair it. This build does not repair it either.
6. **The mature-row PATH identity will move**, as ORDER I recorded and ORDER N disclosed. The age
   gate holds the *current* prices of 24-plus rows; rows now over 24 had younger vantages, and those
   vantages are priced by the new charge, so their historical paths move. The veteran caps are
   scored on current prices, which is what the rail is written on.

---

## 5 · WHAT THIS SEAT WILL NOT DO

- It will not re-tune `G0`, `BETA_sat`, `LAMBDA`, `THETA_R`, `s0` or `TMAX`.
- It will not switch to the age-carrying premium.
- It will not bolt a cap on the modern picks 1-10 cell.
- It will not turn any named player's value into an acceptance criterion.
- It will not trade one owner law against another, silently or otherwise.
- It will not open a pull request or push to `main`.

**Deliverables:** the three owner documents (the 804-row player list, the year-1 class in draft
order, the no-arb tables in the standing format in both windows with the pool arms), each carrying a
plain-words "what is in this board and what is still broken" box; plus `PACKET_P_BUILD.md` and
`docs/ledgers/ORDER_P_MOVERS.json`.
