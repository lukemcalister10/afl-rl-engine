# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ edc47017 — NOT AN ENDORSED STATE — head edc47017 store 340a7a32 config c2d233aec104
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ edc47017 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head edc47017 store 340a7a32 config c2d233aec104 — suite 764a0d91 — 2026-07-15 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash c2d233aec1041a2d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=edc47017 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4572 vs 2555
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1555 vs 1814 (Ward=2016, ratio=0.771) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1615 vs 2016
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=2881 2025=4361 ratio=0.66 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=31 ev=3714 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1955 (floor 1600); Jake Bowey=3058 (floor 2100); Nick Blakey=3284 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=484 (n=12, pooled — thin slice) vs pick-matched MID kernel median=651 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2868 Tsatas=1256 ratio=2.28x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | FAIL     Ginnivan>Ward: 1955 vs 2016  <- MOVED
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1267 2025=2288 ratio=0.55 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2266 vs 1029; Cumming>Annable: 2252 vs 2147
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 669 vs 970; Smillie>Retschko: 1349 vs 881
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3160 lineball=True; Levi Ashcroft=3354 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=1738 lineball=True; Zach Reid=1767 lineball=True; Jase Burgoyne=2098 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine edc47017 store 340a7a32 config c2d233aec104): y1=71087.3 y2=82290.9 y3=83718.4 y4=88241.7 y5=86472.0 y6=80088.5 y7=70573.8; den=min(y1,y2)=y1=71087.3; ratios y4=1.2413(in-guide) y5=1.2164(in-guide) y6=1.1266(below-guide); hard<=1.30 -> PASS x3; guide 1.20-1.25 ADVISORY (margin reported, never gates)
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells GEN_DEF|GOOD|T2:4.01, RUC|GOOD|T5:3.56, GEN_DEF|GOOD|T4:3.19, KEY_FWD|GOOD|T5:2.39; GOOD>BUST sep GEN_DEF 39.5/1.0, GEN_FWD 39.9/0.6, KEY_DEF 48.7/1.1, KEY_FWD 62.0/0.6, MID 50.8/0.5, RUC 27.4/0.4 [cert engine edc47017 store 340a7a32 config c2d233ae]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine edc47017 store 340a7a32 config c2d233aec104): MATCHES the sealed baseline. current=3152fa061df870c8.. (2649 players) vs baseline=3152fa061df870c8.. (2649 players, sealed head edc47017) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=9a9889f8 vs shipped 9a9889f8 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 61 saves, aggregate lift +2251; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1353, 1552, 1882, 2587, 3244, 3362, 3491, 3572, 3670, 3765, 3942, 4120, 4318, 4449, 4532]; dips(more games worth less)=none; 0->6 rise T=+2138; 0->6 steps>50%T=none; rise by 3g=+1234 (need >=534) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=4  FEATURE=1  PASS=16  PENDING=4  STRUCK=1  (324s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr4, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 129 | 164 | 162 | 169 | 146 | 131 |
| 2005 | 4 | 100 | 151 | 139 | 182 | 171 | 162 | 137 |
| 2006 | 4 | 100 | 119 | 121 | 133 | 131 | 129 | 110 |
| 2007 | 5 | 100 | 120 | 107 | 108 | 132 | 121 | 102 |
| 2008 | 4 | 100 | 120 | 147 | 154 | 137 | 116 | 102 |
| 2009 | 2 | 100 | 113 | 94 | 93 | 92 | 82 | 70 |
| 2010 | 4 | 100 | 119 | 120 | 132 | 127 | 109 | 88 |
| 2011 | 4 | 100 | 118 | 129 | 140 | 135 | 127 | 106 |
| 2012 | 3 | 100 | 102 | 108 | 106 | 99 | 94 | 80 |
| 2013 | 5 | 100 | 120 | 129 | 146 | 147 | 129 | 98 |
| 2014 | 4 | 100 | 113 | 119 | 122 | 108 | 108 | 102 |
| 2015 | 2 | 100 | 107 | 102 | 100 | 99 | 98 | 93 |
| 2016 | 4 | 100 | 117 | 126 | 144 | 129 | 128 | 108 |
| 2017 | 2 | 100 | 112 | 109 | 99 | 94 | 90 | 85 |
| 2018 | 2 | 100 | 115 | 102 | 108 | 106 | 98 | 88 |
| 2019 | 5 | 100 | 100 | 104 | 110 | 118 | 107 | 89 |
| 2020 | 2 | 100 | 101 | 95 | 88 | 94 | 89 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _4_ | _100_ | _116_ | _119_ | _125_ | _123_ | _114_ | _99_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **71087** | **82291** | **83718** | **88242** | **86472** | **80088** | **70574** |

B5 FLOOR-SAVES table (n=61, aggregate lift=+2251 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 16 | 140.8 | 169 | +153 | clear |
| Stephen Coniglio | — | 15 | 23 | 140.8 | 169 | +146 | clear |
| Jaeger O'Meara | — | 15 | 63 | 150.0 | 192 | +129 | clear |
| Chayce Jones | — | 8 | 14 | 85.4 | 115 | +101 | clear |
| Steele Sidebottom | — | 18 | 3 | 81.2 | 103 | +100 | clear |
| Oliver Wiltshire | — | 3 | 14 | 98.3 | 109 | +95 | clear |
| Jacob Hopper | — | 11 | 43 | 87.0 | 126 | +83 | clear |
| Harvey Gallagher | — | 4 | 77 | 153.3 | 142 | +65 | clear |
| Luke Pedlar | — | 6 | 82 | 146.2 | 147 | +65 | clear |
| Bailey Laurie | — | 6 | 21 | 87.8 | 77 | +56 | clear |
| Jack Martin | — | 14 | 48 | 140.8 | 101 | +53 | clear |
| Conor Stone | — | 6 | 36 | 114.1 | 88 | +52 | clear |
| Billy Cootee | — | 1 | 44 | 305.6 | 92 | +48 | clear |
| Phoenix Gothard | — | 3 | 390 | 443.2 | 437 | +47 | clear |
| Callum Ah Chee | — | 11 | 44 | 87.0 | 89 | +45 | clear |
| Sam Sturt | — | 8 | 16 | 60.8 | 57 | +41 | clear |
| Liam Stocker | — | 8 | 2 | 58.6 | 43 | +41 | clear |
| Jade Gresham | — | 11 | 14 | 60.1 | 54 | +40 | clear |
| Finlay Macrae | — | 6 | 75 | 101.3 | 114 | +39 | clear |
| Nicholas Coffield | — | 9 | 16 | 87.0 | 55 | +39 | clear |
| Jake Melksham | — | 17 | 15 | 82.9 | 53 | +38 | clear |
| Oscar Adams | — | 5 | 43 | 58.8 | 80 | +37 | clear |
| Brandon Starcevich | — | 9 | 7 | 60.1 | 44 | +37 | clear |
| Charlie Spargo | — | 9 | 1 | 42.2 | 37 | +36 | clear |
| Judson Clarke | — | 5 | 62 | 106.9 | 95 | +33 | clear |
| Oliver Henry | — | 6 | 64 | 108.2 | 97 | +33 | clear |
| Laitham Vandermeer | — | 8 | 2 | 37.2 | 34 | +32 | clear |
| Jamie Elliott | — | 15 | 6 | 34.0 | 34 | +28 | clear |
| Jed Bews | — | 15 | 1 | 17.2 | 28 | +27 | clear |
| Darcy Gardiner | — | 13 | 22 | 51.0 | 48 | +26 | clear |
| Rhys Stanley | — | 18 | 12 | 27.4 | 38 | +26 | clear |
| Ben Long | — | 10 | 9 | 45.9 | 34 | +25 | clear |
| Alex Pearce | — | 13 | 15 | 37.2 | 40 | +25 | clear |
| Nicholas Holman | — | 13 | 0 | 24.8 | 25 | +25 | clear |
| Joel Hamling | — | 15 | 14 | 31.5 | 38 | +24 | clear |
| Matt Guelfi | — | 9 | 5 | 17.2 | 27 | +22 | clear |
| Ben McKay | — | 11 | 27 | 53.7 | 49 | +22 | clear |
| Ryan Gardner | — | 11 | 13 | 18.3 | 35 | +22 | clear |
| Daniel Butler | — | 12 | 0 | 17.2 | 22 | +22 | clear |
| Liam Henry | — | 7 | 67 | 85.4 | 87 | +20 | clear |
| Oskar Baker | — | 9 | 14 | 26.0 | 33 | +19 | clear |
| Mitch McGovern | — | 12 | 9 | 32.8 | 28 | +19 | clear |
| Reef McInnes | — | 6 | 64 | 84.7 | 82 | +18 | clear |
| Jacob Wehr | — | 6 | 4 | 31.6 | 22 | +18 | clear |
| Aidan Corr | — | 14 | 35 | 60.1 | 53 | +18 | clear |
| Noah Answerth | — | 8 | 17 | 19.6 | 33 | +16 | clear |
| Lachlan Weller | — | 12 | 69 | 67.8 | 85 | +16 | clear |
| Harry Schoenberg | — | 7 | 43 | 47.1 | 58 | +15 | clear |
| Finn Maginness | — | 7 | 23 | 42.2 | 37 | +14 | clear |
| Xavier O'Halloran | — | 8 | 30 | 51.0 | 44 | +14 | clear |
| Jake Kolodjashnij | — | 13 | 26 | 35.0 | 39 | +13 | clear |
| Jamie Cripps | — | 16 | 25 | 41.1 | 37 | +12 | clear |
| Jackson Archer | — | 5 | 69 | 46.8 | 80 | +11 | clear |
| Kaleb Smith | — | 4 | 119 | 104.0 | 129 | +10 | clear |
| Tom Cole | — | 11 | 23 | 37.4 | 32 | +9 | clear |
| Bailey Macdonald | — | 4 | 122 | 94.9 | 129 | +7 | clear |
| Callum Coleman-Jones | — | 9 | 37 | 56.3 | 44 | +7 | clear |
| James Jordon | — | 8 | 39 | 38.5 | 45 | +6 | clear |
| Hunter Clark | — | 9 | 52 | 87.0 | 57 | +5 | clear |
| Liam Ryan | — | 9 | 28 | 45.0 | 31 | +3 | clear |
| Nathan Broad | — | 11 | 9 | 17.2 | 12 | +3 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT edc47017
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 8115 | 7151 | 8014 | -101 | +863 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 7770 | -280 | +768 |
| 3 | Luke Jackson | RUC | 7799 | 6803 | 7734 | -65 | +931 |
| 4 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 6652 | +46 | +858 |
| 5 | Tristan Xerri | RUC | 6649 | 5795 | 6430 | -219 | +635 |
| 6 | Josh Treacy | KEY_FWD | — | — | 6375 | — | — |
| 7 | Max Holmes | MID | 6269 | 5386 | 6198 | -71 | +812 |
| 8 | Errol Gulden | MID | 5983 | 5256 | 5795 | -188 | +539 |
| 9 | Zak Butters | MID | 6059 | 5174 | 5749 | -310 | +575 |
| 10 | Finn Callaghan | MID | 5442 | 4904 | 5477 | +35 | +573 |
| 11 | Archie Roberts | GEN_DEF | 4577 | 4668 | 5264 | +687 | +596 |
| 12 | Will Ashcroft | MID | 5155 | 4768 | 5194 | +39 | +426 |
| 13 | Bailey Smith | MID | 5605 | 4715 | 5069 | -536 | +354 |
| 14 | Noah Anderson | MID | 4765 | 4091 | 4689 | -76 | +598 |
| 15 | Caleb Serong | MID | 4701 | 4170 | 4628 | -73 | +458 |
| 16 | Willem Duursma | MID | 4429 | 4110 | 4572 | +143 | +462 |
| 17 | Sam Darcy | KEY_FWD | 4013 | 4144 | 4557 | +544 | +413 |
| 18 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 4457 | -730 | -154 |
| 19 | Murphy Reid | GEN_FWD | 3953 | 3742 | 4413 | +460 | +671 |
| 20 | Tom Green | MID | 4391 | 4424 | 4413 | +22 | -11 |
| 21 | Matt Rowell | MID | 4185 | 3752 | 4233 | +48 | +481 |
| 22 | Jason Horne-Francis | MID | 3996 | 3702 | 4202 | +206 | +500 |
| 23 | Ryley Sanders | MID | 4129 | 3926 | 4168 | +39 | +242 |
| 24 | Isaac Heeney | MID | 3981 | 3301 | 3922 | -59 | +621 |
| 25 | Colby McKercher | MID | 3829 | 3627 | 3887 | +58 | +260 |
| 26 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 3865 | +47 | +163 |
| 27 | Mac Andrew | KEY_DEF | 3691 | 3504 | 3768 | +77 | +264 |
| 28 | Nick Watson | GEN_FWD | 3720 | 3538 | 3756 | +36 | +218 |
| 29 | Jai Newcombe | MID | — | — | 3752 | — | — |
| 30 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 3723 | -244 | -9 |
| 31 | Harley Reid | MID | 3726 | 3549 | 3714 | -12 | +165 |
| 32 | Brodie Grundy | RUC | 3959 | 3314 | 3698 | -261 | +384 |
| 33 | Marcus Bontempelli | MID | 3721 | 3084 | 3664 | -57 | +580 |
| 34 | Jagga Smith | MID | 3192 | 2822 | 3629 | +437 | +807 |
| 35 | Finn O'Sullivan | MID | 3643 | 3427 | 3559 | -84 | +132 |
| 36 | Sam Lalor | MID | 3574 | 3337 | 3505 | -69 | +168 |
| 37 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 3474 | -22 | +398 |
| 38 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3357 | -102 | +427 |
| 39 | Levi Ashcroft | MID | 3193 | 3028 | 3354 | +161 | +326 |
| 40 | Timothy English | RUC | 3349 | 2916 | 3305 | -44 | +389 |
| 41 | Nick Blakey | GEN_DEF | 3598 | 3266 | 3284 | -314 | +18 |
| 42 | Will Day | MID | 3108 | 2806 | 3209 | +101 | +403 |
| 43 | Bodhi Uwland | GEN_DEF | — | — | 3208 | — | — |
| 44 | Jordan Dawson | MID | 3312 | 2758 | 3189 | -123 | +431 |
| 45 | Logan Morris | KEY_FWD | 3171 | 3018 | 3179 | +8 | +161 |
| 46 | George Wardlaw | MID | 3206 | 3035 | 3160 | -46 | +125 |
| 47 | Callum Wilkie | KEY_DEF | — | — | 3145 | — | — |
| 48 | Jordan Clark | GEN_DEF | 3307 | 3007 | 3136 | -171 | +129 |
| 49 | Jack Sinclair | GEN_DEF | — | — | 3135 | — | — |
| 50 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3058 | -38 | +132 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
