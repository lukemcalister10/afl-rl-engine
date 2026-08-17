# PACKET S5 — Is pick band 21-30 underpriced at entry? Are the monotone v0 curves suppressing a real bump?

**ORDER 32, seat S5 (measurement only, read-only). 2026-08-17. Tree: land/order-29.**
**Prereg:** `PREREG_S5.md` in this directory, pushed before any result was computed.

---

## The answer, up front

**No real bump. The owner's monotone ruling is not the culprit, and nothing here clears noise.**

1. Picks 21-30 ARE fitted below their raw delivered-value mean (−61.9 v0 points, −9.1%) — but so are
   picks 11-20 (−89.6, −9.3%) and 1-10 (−97.2, −5.1%). The whole head of the curve sits under its raw
   means; 21-30 is not special.
2. Almost none of that comes from the monotone (PAVA) constraint. The constraint's own transfer at the
   band level is **+1.0 points at 21-30 and −1.1 points at 31-40 (about 0.2% of band value)** — two
   orders of magnitude smaller than the total residual. The underpricing lives in the *smoothing stage*
   (the local-linear curve estimator), which is not part of the monotone ruling.
3. The 21-30-vs-31-40 gap (G = −53.7 points) **does not clear noise**: bootstrap 95% CI [−290, +179],
   P(G<0) = 0.68. A coin flip leans the same way about two times in three.
4. The pattern is not a composition artifact in either direction — but it is not consistent within
   position either (MID says underpriced, SF says the opposite; the two big samples disagree).
5. It is era-stable in a way that suggests a *smooth* curve, not a bump: the raw 21-30/31-40 value
   ratio is **1.35 in the full window, 1.35 pre-2015, and 1.35 in 2015+** — a remarkably steady
   gradient with no era drift at that boundary.
6. The band-monotone counterfactual (relax the ruling to "monotone across bands, free within") would
   move the average 21-30 board row **down 3.7 points, not up**. No position's band means even ascend
   at the 21-30/31-40 boundary, so band-level monotonicity binds nowhere there.

Per the seat mandate: **a "no real bump" verdict is a complete result, and this is one.**

---

## Terms

| term | meaning |
|---|---|
| **v0** | a player's entry value: the board points assigned at draft entry, per position × pick (the `nd_v0.posv` surface, 6 positions × picks 1-64) |
| **delivered value** | realized career value on the #338 minimum-tenure basis (`grace_a.total` in the fit's own data path); the quantity v0 is fitted to track |
| **fit population** | the 1,142 ND draftees (entry years 2004-2021, picks 1-64) the surface is estimated from — `LAYER2.fit_nd_keys`. Exclusions: **none** (0 rows dropped) |
| **loclin** | the local-linear kernel estimator that turns 1,142 noisy careers into a smooth value-by-pick curve per position (the "smoothing stage") |
| **shrink** | the ORDER 31-F K=15 thin-sample shrink of positional relativities toward the all-in curve (head fix) |
| **PAVA** | pool-adjacent-violators: the weighted projection that enforces the owner's ruling that v0 must never increase with pick; followed by the floor-100, the −1-per-pick tiebreak, and one conservation scalar |
| **R (residual)** | fitted v0 minus raw delivered mean, averaged over the players in a band. **R < 0 = the band is underpriced at entry** (fit sits below the data) |
| **G (the gap)** | R(21-30) − R(31-40). G < 0 = 21-30 more underpriced than 31-40 |
| **bands** | 1-10 / 11-20 / 21-30 / 31-40 / 41-64 (n = 180/180/180/180/422 players) |

## Lineage (the fit's own path — no parallel lane)

The fitted surface, its PAVA input, and its raw data were all reconstructed from the candidate's own
committed pipeline and verified exactly (`s5_step1_inputs.py`, `s5_step1_out.txt`):

- artifact `nd_v0.posv` == `HEADFIX_31F.json::posv_headfixed`, max diff **0.0**;
- the o30b_v0refit PAVA→floor→tiebreak→λ block, lifted by source text (md5 `1d8e54cd…`, matches the
  committed pipeline md5), re-run on the reconstructed shrunk input, **reproduces the shipped surface
  to 0.0**, λ = 0.996095068756 (matches published);
- raw data: value = `grace_a.total`, pick = `attribution.pick`, position = layer1 `position_group`,
  era = `entry_year`. All 1,142 rows used; every input file md5-pinned in the console output.

The chain, per band: **raw player means → loclin (smoothing) → shrink → PAVA machinery → fitted v0**,
so the total residual decomposes exactly: `R_total = R_smooth + R_shrink + R_pava`.

---

## 1. Residuals by band, pooled (full window 2004-2021, player-weighted)

```
band      n  raw_mean  raw_se  raw_sd  fit_mean | R_total  R_smooth R_shrink  R_pava |  Rtot%   Rpava%
1-10    180    1992.5   163.5  2193.3    1895.3 |   -97.2    -87.8    -10.5     +1.2 |  -5.1%   +0.1%
11-20   180    1054.0   111.4  1495.2     964.4 |   -89.6    -88.3     -0.8     -0.5 |  -9.3%   -0.1%
21-30   180     739.2    98.2  1317.4     677.3 |   -61.9    -69.3     +6.4     +1.0 |  -9.1%   +0.2%
31-40   180     547.5    82.3  1104.8     539.3 |    -8.2     -2.9     -4.2     -1.1 |  -1.5%   -0.2%
41-64   422     287.2    34.5   709.4     279.1 |    -8.1     -8.8     -0.6     +1.3 |  -2.9%   +0.5%

G       = R_total(21-30) - R_total(31-40) = -53.7 v0 points
G_pava  = R_pava (21-30) - R_pava (31-40) =  +2.1 v0 points
```

**Reading it:** the owner's question was whether the monotone constraint transfers value from 21-30
into its neighbours. The constraint's entire pooled contribution (R_pava column) is ±1.3 points at
worst — ≤0.5% of band value everywhere. If the ruling were repealed tomorrow and everything else
kept, the band values would barely move. The −62-point total at 21-30 comes almost wholly from the
smoothing stage (R_smooth −69.3), and 11-20 carries an even larger smoothing deficit (−88.3). The
smoothing stage flattens the steep head of the value curve — a known property of kernel smoothers on
convex declines — and it does so across all of picks 1-30, not at 21-30 specifically.

**Where the constraint actually binds in picks 21-40** (cell-level `fit − PAVA-input`, from the PAVA
block map): RUCK picks 14-34 pooled into one block (moves of −40…−119 points, on a 5-player 21-30
sample — thin-sample noise the shrink already damps), and SF 25-37 pooled (moving value *into* 25-30
from 31-37, i.e. the **opposite** direction of the owner's worry). KPD/KPF/MID/SD moves in 21-40 are
single-digit points. Full cell map in `s5_step2_out.txt`.

## 2. Composition control

Position mix per band (share of band n):

```
band       KPD      KPF      MID     RUCK       SD       SF
1-10    19 11%   31 17%   96 53%    7  4%   12  7%   15  8%
11-20   17  9%   24 13%   65 36%    8  4%   33 18%   33 18%
21-30   21 12%   17  9%   77 43%    5  3%   23 13%   37 21%
31-40   22 12%   23 13%   60 33%   14  8%   28 16%   33 18%
41-64   46 11%   48 11%  124 29%   26  6%   84 20%   94 22%
```

21-30 is somewhat MID-heavy (43% vs 33% in 31-40) and RUCK-light. But the residual pattern is **not**
a clean mix artifact, because within position the story splits:

```
R_total as % of fitted, by position x band (n):
pos          1-10       11-20       21-30       31-40       41-64
KPD      +14% (19)    -7% (17)   +25% (21)   +22% (22)   -18% (46)
KPF      +10% (31)   +10% (24)   -41% (17)   +14% (23)   +11% (48)
MID      -13% (96)   -19% (65)   -13% (77)   +10% (60)  -16% (124)
RUCK      -30% (7)    +26% (8)  -112% (5)    -69% (14)    +6% (26)
SD       +16% (12)   -13% (33)    -8% (23)   +14% (28)   +29% (84)
SF       +14% (15)    -3% (33)   +36% (37)    -5% (33)    +0% (94)

within-position G (positions with n>=20 in both bands):
KPD +35.6    MID -175.6    SD -92.4    SF +182.5
```

Two positions say 21-30 is underpriced relative to 31-40 (MID, SD), two say the opposite (KPD, SF).
The pooled G is carried mostly by MID (the largest sample) and partially cancelled by SF. A real
structural bump should not flip sign across the two biggest non-MID samples. Neither within-position
G clears its own bootstrap noise (§4).

## 3. Era control

Fitted surface held fixed (it was fitted on the pooled window); the question is whether the modern
draft's raw data shows the same band shape. **Named caveat:** 2015+ careers are right-truncated (the
youngest cohorts haven't finished delivering), so era *levels* are not comparable — the *shape across
bands within an era* is the comparable object.

```
                      full 2004-21      pre-2015 (04-14)     modern 2015+
band                 R_tot   raw/fit     R_tot   raw/fit     R_tot   raw/fit
1-10                 -97.2    1.051      +41.2    0.979     -314.6    1.170
11-20                -89.6    1.093     -120.0    1.126      -41.9    1.043
21-30                -61.9    1.091      -48.8    1.073      -82.4    1.120
31-40                 -8.2    1.015       +6.0    0.989      -30.5    1.057
41-64                 -8.1    1.029      -57.1    1.204      +68.2    0.754

G                    -53.7               -54.8               -51.9
raw 21-30/31-40 ratio 1.35                1.35                1.35
raw 1-10/41-64 ratio  6.94                5.57               10.38
```

G is uncannily stable (−52…−55) — but so is the *smooth* 21-30→31-40 gradient: the raw band ratio is
1.35 in every era. There is no era in which 21-30 spikes against its neighbours; what the eras share
is the same smooth decline that the fit's smoothing stage under-tracks at the head. **The overall
pick curve does drift**: the head-to-tail ratio steepens from 5.6× (pre-2015) to 10.4× (2015+),
partly real concentration of value at the top of the modern draft, partly truncation biting the
late-pick slow-delivery tail (41-64 raw/fit collapses from 1.204 to 0.754). That drift is a finding
about the whole curve, not about the 21-30/31-40 boundary, and is flagged for the program rather than
resolved here.

## 4. Noise honesty — the bootstrap

Player-level bootstrap, 4,000 reps, resampling the fit rows with replacement, fitted surface held
fixed, percentile CIs, seed 3251142 (`s5_step4_boot.py`):

```
                               G point     95% CI            P(G<0)   clears noise?
full window, all positions      -53.7   [-290.0, +178.9]      0.68        NO
modern 2015+                    -51.9   [-436.1, +345.9]      0.60        NO
MID only                       -175.6   [-657.8, +307.8]      0.77        NO
SF only                        +182.5   [-106.1, +471.4]      0.90 (>0)   NO

R(21-30) alone, full window     -61.9   [-254.0, +114.3]                  NO
```

Delivered value is wildly dispersed (band SDs 1,100-2,200 points against band means of 550-2,000), so
180 players per band buys a standard error of ~80-100 points on each band mean. A −54-point gap
cannot be distinguished from zero at this sample size. **That is the answer:** the data cannot
support repricing 21-30 against 31-40, in either direction.

**Disclosed deviation from prereg step 5:** the optional full-pipeline bootstrap (re-running
loclin→shrink→PAVA per rep) was not run. The persisted loclin surface comes from the ORDER-28
harness relativity construction, which a direct kernel call reproduces only to ~5-10% — rebuilding it
would be exactly the parallel lane this seat is forbidden to derive. The constraint channel is
instead bounded directly on the true lineage: |R_pava| ≤ 1.3 points pooled (§1).

## 5. Reconciling the year-path finding

The motivating measurement (21-30 peaking at 1.675× entry vs 31-40 at 1.373×, ext_2026-08-17) is a
*ratio to entry v0*. Both 11-20 and 21-30 carry entry v0 about 9% below their raw delivered means
(§1), which mechanically inflates every ratio-to-entry path for those bands; 31-40 is priced at par
(−1.5%), deflating its path. About 7-8 points of the 30-point peak-ratio gap is this denominator
effect; the rest is path shape and noise. Nothing in the entry-lane raw means shows a bump: the raw
gradient through the boundary is the same smooth 1.35× in every era.

## 6. Decision framing (evidence only — no recommendation)

**Option A — keep strict per-pick monotonicity (the owner's standing ruling).**
Board impact: none (status quo). Measured cost of the ruling at the band level: ≤1.3 points per band
pooled (≤0.5%). Cell-level costs are confined to RUCK 14-34 (5-player band sample; the block moves
−40…−119 points per cell, but the head-fix shrink already treats those cells as thin) and SF 25-37
(where the ruling moves value INTO 25-30 — it currently *favors* the band the owner worried about).
The −9% head underpricing is untouched by this choice; it belongs to the smoothing stage.

**Option B — relax to band-level monotonicity (monotone across band means, free within band).**
Constructed on the fit's own shrunk input (`s5_step5_bandctf.py`, surface in `S5_BANDCTF.json`), same
floor and conservation scalar. Findings:
- Band means already descend at every band boundary for every position except one: RUCK 11-20/21-30
  (1022 vs 1130, pooled to 1074) — on RUCK's 5-player 21-30 sample. **Nothing pools at 21-30/31-40.**
- The average 21-30 board row moves **−3.7 points** (down). The relaxation does not deliver what the
  hypothesis wanted; there is no suppressed bump for it to release.
- 125 of the 561 ND pick-1-64 rows on the 804-row candidate board would move ≥10 v0 points. Largest
  movers: Will Green (RUCK p16, −122), Luke Jackson (RUCK p3, +89), Lawson Humphries (SD p63, +85),
  Brodie Grundy (RUCK p22, +61), the pick-12 SD cluster (Sinn/Fletcher/Duggan/Vlastuin, +60 each),
  the pick-7 MID cluster (8 players, −54 each). Most moves are within-band loclin wiggle set free, and
  the pick-55-64 tail moves are the loss of the −1 tiebreak ramp — noise and side effects, not the
  21-30 question. (v0 is the entry stock; live prices move less — v0 is scaled by the law's
  D/Φ/β bracket — so these are upper bounds on price moves.)
- It also creates 10-17 within-band ascents per position (later pick priced above earlier pick),
  which is precisely what the ruling exists to forbid.

**If the owner wants to chase the year-path signal**, the evidence points at the smoothing stage
(loclin's flattening of the steep 1-30 head, a uniform −5…−9% underpricing) — a program-level
question about the estimator, not about the monotone ruling, and not one this read-only seat acted on.

## Prereg scorecard (predictions registered before any number)

| pred | registered | outcome |
|---|---|---|
| P1 | R(21-30) < 0 | **CONFIRMED** (−61.9) |
| P2 | G < 0 | **CONFIRMED** (−53.7) |
| P3 | bootstrap CI of G includes 0 (no real bump) | **CONFIRMED** ([−290, +179], P(G<0)=0.68) |
| P4 | sign survives within the two largest positions | **MIXED / half-failed**: MID yes (−175.6), SF no (+182.5). The registered falsifier (majority of qualifying positions positive) was not tripped (2 of 4), but the point prediction failed for SF |
| P5 | same sign of G on 2015+, within ~2× magnitude | **CONFIRMED** (−51.9 vs −53.7) |
| P6 | all band residuals ≤12%; PAVA-stage ≤6% at 21-30/31-40 | **CONFIRMED** (max 9.3%; PAVA-stage 0.2%) |

## Honesty ledger

- **Exclusions: none.** All 1,142 fit rows used; 0 rows lacked pick/position/value/entry_year.
- Dispersion shown for every mean (SD and SE in §1, §3; CIs in §4). Full per-cell SD/n in the
  appendix table and `S5_INPUTS.json::raw_cell_stats`.
- The fit window is 2004-2021 (prereg brief said 2005+; the fit's own population starts 2004 — used
  as found).
- Right-truncation of modern cohorts named in §3; the packet compares band shape, not era levels.
- Deviation from prereg (full-pipeline bootstrap skipped) disclosed in §4 with the reason.
- Band n in the brief (~190) is actually 180/180/180/180/422 in the fit population — used as found.
- One process hygiene note: the first Step-5 push carried the script but not its outputs (a truncated
  preview pipe killed the writes); the full run was replayed and pushed in the next commit.

## Appendix A — raw delivered-value means, pick × position (mean±SD(n))

From `s5_step1_out.txt` (also machine-readable in `S5_INPUTS.json::raw_cell_stats`):

```
  pick                   KPD                   KPF                   MID                  RUCK                    SD                    SF         ALL
     1            1942+-0(1)         1052+-1213(2)        4093+-1704(12)            1942+-0(1)            1681+-0(1)             573+-0(1)    3186(18)
     2            3778+-0(1)         2309+-2036(6)         2761+-1932(9)            4341+-0(1)                     -            2325+-0(1)    2731(18)
     3                     -           111+-139(2)        2954+-2583(14)            8448+-0(1)                     -            3501+-0(1)    2974(18)
     4           395+-232(2)          1057+-992(3)        3177+-3796(10)                     -         2229+-2486(2)             564+-0(1)    2264(18)
     5          3536+-397(2)         3038+-3108(3)        2189+-2434(10)             974+-0(1)             151+-0(1)            3951+-0(1)    2397(18)
     6           125+-179(5)           115+-114(2)          773+-1444(6)                     -                     -           677+-526(5)     493(18)
     7            3177+-0(1)          817+-1155(2)        1734+-1670(10)                     -          934+-1016(4)             950+-0(1)    1491(18)
     8           191+-190(2)           867+-542(4)         3198+-3334(7)               0+-0(1)         1824+-2371(2)         1716+-2220(2)    1851(18)
     9          797+-1031(2)           985+-562(5)         1030+-1229(8)            2754+-0(1)             293+-0(1)             125+-0(1)     996(18)
    10           591+-223(3)         2423+-1147(2)        1960+-2469(10)              41+-0(1)            1479+-0(1)               7+-0(1)    1542(18)
    11               7+-0(1)            2726+-0(1)         1702+-1745(7)              74+-0(1)         3025+-4574(3)           290+-480(5)    1402(18)
    12             582+-0(1)         1157+-1272(5)         2235+-2870(7)                     -          816+-1084(2)          2964+-861(3)    1808(18)
    13           733+-479(2)              13+-7(2)         1656+-1656(8)                     -         1230+-1216(4)          731+-1034(2)    1173(18)
    14            1645+-0(1)         1797+-2276(2)         1408+-2442(5)               3+-0(1)          1076+-613(6)           304+-278(3)    1092(18)
    15           288+-256(2)           270+-387(4)          815+-1277(3)                     -          958+-1658(3)           444+-478(6)     535(18)
    16           111+-152(2)           598+-628(3)           602+-731(4)             882+-0(1)         1240+-1448(5)           388+-670(3)     704(18)
    17         1589+-1410(2)           456+-632(2)          961+-1262(8)                     -           474+-203(2)           579+-541(4)     836(18)
    18         1592+-1843(2)            1257+-0(1)          761+-1134(8)            83+-101(3)         1432+-2020(2)           708+-885(2)     837(18)
    19           394+-291(3)           798+-852(2)         1198+-1630(6)            4952+-0(1)           490+-460(4)           192+-209(2)     959(18)
    20             793+-0(1)             46+-65(2)         1740+-2594(9)             296+-0(1)           356+-444(2)          1311+-972(3)    1194(18)
    21           113+-124(3)         1145+-1464(3)         1007+-2147(8)                     -            2007+-0(1)           247+-276(3)     810(18)
    22             591+-0(1)                     -         430+-1029(12)            6992+-0(1)         2003+-1747(3)               0+-0(1)    1042(18)
    23             265+-0(1)            2793+-0(1)           357+-693(8)                     -          826+-1168(2)             20+-20(6)     427(18)
    24           439+-509(3)               0+-0(1)          938+-1456(9)            1238+-0(1)             24+-31(3)              21+-0(1)     616(18)
    25           154+-295(4)             359+-0(1)         2058+-2566(9)               2+-0(1)                     -           475+-745(3)    1162(18)
    26               0+-0(1)           241+-338(2)           613+-975(6)                     -           193+-335(3)           307+-270(6)     366(18)
    27                     -               1+-1(2)           473+-515(7)                     -            73+-117(4)           492+-351(5)     337(18)
    28         1681+-1544(3)         1739+-1656(2)         1092+-1615(9)            1455+-0(1)               0+-0(1)               0+-0(2)    1100(18)
    29             12+-16(2)         1396+-1922(3)         1608+-1875(6)                     -           607+-858(2)          512+-1105(5)     979(18)
    30           106+-184(3)            112+-50(2)         1505+-1304(3)            1593+-0(1)           474+-565(4)           280+-484(5)     553(18)
    31                     -           176+-297(5)           385+-813(5)           649+-814(3)             192+-0(1)           297+-354(4)     341(18)
    32             255+-0(1)             374+-0(1)          288+-465(11)                     -           449+-741(4)               0+-0(1)     311(18)
    33          796+-1361(3)           698+-980(5)           491+-687(7)            6135+-0(1)             15+-21(2)                     -     860(18)
    34           200+-173(3)               0+-0(2)         1638+-2708(6)         1934+-1425(3)               0+-0(1)           108+-133(3)     919(18)
    35           511+-723(2)          612+-1060(3)           125+-182(5)            1300+-0(1)              7+-10(3)          902+-1116(4)     467(18)
    36             35+-57(3)             62+-86(2)           378+-791(5)                     -           540+-914(5)           303+-519(3)     318(18)
    37          914+-1176(3)           414+-494(3)             15+-21(4)           351+-314(3)             55+-68(3)           205+-290(2)     315(18)
    38            83+-117(2)                     -         1260+-2167(8)         2501+-2400(3)               0+-0(2)             19+-31(3)     989(18)
    39             15+-15(2)          844+-1190(2)           324+-470(4)                     -             62+-96(3)           852+-838(7)     509(18)
    40             96+-84(3)                     -          538+-1159(5)                     -          790+-1573(4)           313+-540(6)     445(18)
    41             163+-0(1)           441+-764(3)          741+-1769(6)           704+-578(3)             46+-80(3)             63+-69(2)     462(18)
    42         1044+-1005(2)           159+-225(2)         1101+-1772(7)           316+-289(2)          707+-1225(3)               5+-6(2)     715(18)
    43            1391+-0(1)           107+-128(5)          773+-1175(7)                     -             69+-86(3)             21+-30(2)     422(18)
    44            107+-68(2)           189+-378(4)          986+-1734(6)                     -                     -           633+-765(6)     593(18)
    45            95+-134(2)                     -          656+-1257(8)                     -               0+-0(2)             27+-57(6)     311(18)
    46           376+-541(3)           509+-653(3)           475+-671(2)                     -             43+-86(4)           105+-216(6)     245(18)
    47               3+-5(3)                     -           228+-532(6)           617+-849(2)               0+-1(3)            71+-133(4)     161(18)
    48             452+-0(1)               0+-0(1)             40+-78(7)          942+-1322(2)           317+-360(4)               4+-7(3)     216(18)
    49         1013+-1417(3)           482+-834(3)            81+-114(2)           206+-293(3)           126+-272(5)               0+-0(2)     327(18)
    50            208+-91(2)             323+-0(1)            51+-101(4)             22+-38(3)             20+-30(4)           122+-244(4)      88(18)
    51           111+-170(3)           120+-106(2)           100+-179(4)                     -            54+-102(4)          947+-1554(5)     329(18)
    52           152+-214(2)               6+-8(2)         1102+-1558(2)               0+-0(1)             10+-17(9)             69+-73(2)     152(18)
    53           770+-778(3)             648+-0(1)           718+-503(4)               0+-0(1)             18+-33(4)          499+-1010(5)     466(18)
    54         1033+-1405(4)               0+-0(1)               0+-0(4)           180+-239(2)             54+-77(2)           183+-333(5)     306(18)
    55               0+-0(1)           228+-455(4)          557+-1416(7)                     -               6+-3(3)         1182+-2047(3)     465(18)
    56                     -               0+-0(1)            76+-199(7)             765+-0(1)           256+-431(3)           293+-693(6)     213(18)
    57              32+-0(1)           141+-178(2)           405+-648(6)                     -             14+-19(2)           373+-580(7)     299(18)
    58             26+-40(4)               0+-0(1)           297+-409(5)               0+-0(1)           111+-144(4)               5+-9(3)     114(18)
    59         1601+-2244(2)              6+-10(4)            63+-102(6)                     -             14+-16(2)               0+-0(4)     202(18)
    60             45+-53(2)               0+-0(2)               1+-1(3)                     -           346+-914(7)             16+-18(4)     143(18)
    61                     -               0+-0(2)           291+-758(7)             376+-0(1)           292+-619(6)             642+-0(1)     283(17)
    62           353+-499(2)                     -             26+-55(5)             20+-26(2)               0+-0(2)               0+-0(5)      55(16)
    63               0+-0(1)               0+-0(1)               0+-0(5)               0+-0(1)             43+-75(3)             17+-34(4)      13(15)
    64              71+-0(1)          857+-1260(3)             45+-89(4)               4+-0(1)            95+-135(2)            59+-103(3)     228(14)
```
(also machine-readable in `S5_INPUTS.json::raw_cell_stats`; '-' = no player at that cell)

## Appendix B — fitted v0 vs PAVA input, pick × position

All 64 picks × 6 positions, `fitted/input` pairs — the exact surface the board prices from, next
to the surface the monotone machinery consumed (also in `fitted_table.txt`):

```
  pick        KPD fit/in        KPF fit/in        MID fit/in       RUCK fit/in         SD fit/in         SF fit/in
     1         2727/2729         2372/2376         3273/3283         2802/2701         2697/2707         2574/2574
     2         2531/2532         2180/2183         2869/2878         2801/2854         2454/2463         2421/2420
     3         2316/2317         2035/2038         2729/2737         2800/2890         2281/2290         2331/2331
     4         1866/1865         1765/1767         2479/2486         2542/2547         1923/1930         1975/1973
     5         1451/1449         1487/1487         2062/2067         2073/2077         1595/1601         1583/1579
     6         1050/1046         1149/1148         1579/1551         1500/1501         1292/1247         1161/1155
     7         1009/1005         1148/1147         1578/1524         1414/1415         1291/1275         1108/1103
     8           963/959         1126/1125         1577/1561         1321/1321         1290/1275         1047/1041
     9           927/923         1112/1111         1576/1590         1253/1253         1289/1269          1005/999
    10           912/907         1111/1106         1575/1595         1219/1219         1288/1279           983/977
    11           911/906         1110/1109         1574/1618         1218/1217         1287/1312           977/969
    12           910/908         1109/1118         1573/1621         1217/1222         1286/1346           976/971
    13           838/834         1022/1022         1445/1448         1116/1116         1243/1247           891/885
    14           705/700           856/856         1174/1176          1078/948         1040/1044           736/729
    15           651/619           759/751           978/979          1077/855           904/907           634/627
    16           650/635           758/759           956/957          1076/907           899/902           626/619
    17           649/657           757/765           927/919          1075/966           889/892           616/609
    18           648/660           756/758           926/910         1074/1005           862/865           595/588
    19           647/647           730/731           925/930         1073/1032           813/816           563/555
    20           644/635           726/721           924/936         1072/1076           784/786           546/539
    21           643/643           725/732           923/929         1071/1148           775/777           538/531
    22           634/629           722/723           896/896         1070/1189           742/745           521/513
    23           590/585           682/683           855/856         1069/1165           677/680           478/470
    24           548/543           645/645           843/841         1068/1130           612/614           441/433
    25           519/514           614/615           842/842         1067/1107           561/563           428/408
    26           503/498           604/604           841/845         1066/1110           524/525           427/398
    27           496/490           601/602           840/842         1065/1114           494/496           426/397
    28           493/488           590/591           824/825         1064/1114           464/466           425/408
    29           487/482           581/581           792/793         1063/1123           438/439           424/412
    30           486/482           564/565           755/756         1062/1108           411/413           423/416
    31           480/475           548/548           713/714         1061/1087           392/394           422/418
    32           474/469           529/529           678/679         1060/1075           378/379           421/421
    33           471/466           508/508           650/651         1059/1085           367/368           420/421
    34           463/458           489/490           634/635         1058/1078           358/359           419/421
    35           454/449           471/471           632/629         1057/1061           348/349           418/419
    36           443/437           450/450           631/625         1015/1019           346/347           417/428
    37           434/429           433/433           630/631           958/961           337/338           416/423
    38           427/421           416/416           629/637           897/900           327/328           415/414
    39           416/410           396/396           628/634           826/828           312/313           414/413
    40           407/401           377/377           627/629           758/761           311/312           390/389
    41           398/393           362/362           619/621           696/699           296/297           366/364
    42           391/386           344/344           600/602           637/639           278/278           340/338
    43           387/381           328/328           574/576           582/584           259/259           317/316
    44           382/376           312/311           540/542           530/532           239/239           298/296
    45           381/372           296/295           500/501           480/481           227/227           282/281
    46           380/370           282/281           461/463           435/436           204/204           281/272
    47           379/370           269/268           425/426           394/395           182/182           280/269
    48           378/369           258/257           393/395           358/359           174/164           279/271
    49           377/370           247/246           363/365           325/326           173/148           278/275
    50           376/373           238/237           339/340           297/298           172/137           277/280
    51           375/374           229/228           317/318           274/275           171/131           276/284
    52           374/374           221/220           297/298           254/255           170/128           275/286
    53           373/370           216/215           280/281           237/238           169/129           274/285
    54           372/365           215/209           265/265           223/223           168/132           273/279
    55           371/359           214/204           249/250           209/210           167/137           268/268
    56           370/350           213/200           234/234           195/196           166/143           252/252
    57           369/342           212/196           216/217           182/182           165/149           230/231
    58           368/339           211/193           200/200           164/164           164/157           208/208
    59           367/336           210/193           183/184           153/154           163/166           183/183
    60           366/348           209/196           168/169           135/135           162/179           158/159
    61           365/364           208/208           154/154           128/129           161/198           134/134
    62           364/407           207/224           140/140           106/106           160/222           108/108
    63           363/441           206/234           116/116            101/88           159/244           101/101
    64           362/499           205/257            100/89            100/88           158/274            100/65
```

## Files

| file | content |
|---|---|
| `PREREG_S5.md` | predictions + falsifiers, pushed first |
| `s5_step1_inputs.py` / `s5_step1_out.txt` / `S5_INPUTS.json` | lineage verification (exact), raw pick×pos table, reconstructed surfaces |
| `s5_step2_residuals.py` / `s5_step2_out.txt` / `S5_RESIDUALS.json` | band residuals, stage decomposition, composition |
| `s5_step3_era.py` / `s5_step3_out.txt` / `S5_ERA.json` | era control |
| `s5_step4_boot.py` / `s5_step4_out.txt` / `S5_BOOT.json` | bootstrap, noise verdict |
| `s5_step5_bandctf.py` / `s5_step5_out.txt` / `S5_BANDCTF.json` | band-monotone counterfactual + board impact |
| `fitted_table.txt` | Appendix B table |
