# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ a83c9f6d — NOT AN ENDORSED STATE — head a83c9f6d store b1fd0bce config c2d233aec104
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ a83c9f6d — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head a83c9f6d store b1fd0bce config c2d233aec104 — suite 764a0d91 — 2026-07-16 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash c2d233aec1041a2d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=a83c9f6d ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4569 vs 2592
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1510 vs 1898 (Ward=2109, ratio=0.716) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1662 vs 2109
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3145 2025=4883 ratio=0.64 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | FAIL     Harley Reid board rank=44 ev=3650 (need TOP 40)  <- MOVED
A5        PASS    | PASS    | PASS     Jack Ginnivan=2304 (floor 1600); Jake Bowey=3706 (floor 2100); Nick Blakey=4568 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=478 (n=12, pooled — thin slice) vs pick-matched MID kernel median=669 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=3799 Tsatas=1475 ratio=2.58x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 2304 vs 2109
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1315 2025=2324 ratio=0.57 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2363 vs 1021; Cumming>Annable: 2230 vs 2135
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 633 vs 968; Smillie>Retschko: 1352 vs 872
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3288 lineball=True; Levi Ashcroft=3347 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1709: Trent Rivers=2225 lineball=False; Zach Reid=1825 lineball=True; Jase Burgoyne=2202 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | HALT     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine a83c9f6d store b1fd0bce config c2d233aec104): y1=70555.8 y2=81592.1 y3=85772.9 y4=91843.1 y5=92849.8 y6=89354.4 y7=80318.2; den=min(y1,y2)=y1=70555.8; ratios y4=1.3017(above-guide) y5=1.3160(above-guide) y6=1.2664(above-guide); hard<=1.30 -> BREACH at y[4, 5] (HALT); guide 1.20-1.25 ADVISORY (margin reported, never gates)  <- MOVED
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:6.17, KEY_DEF|GOOD|T5:5.33, GEN_DEF|GOOD|T2:4.70, GEN_DEF|GOOD|T4:4.54; GOOD>BUST sep GEN_DEF 37.6/1.0, GEN_FWD 40.2/0.6, KEY_DEF 50.4/1.1, KEY_FWD 62.9/0.6, MID 47.1/0.5, RUC 25.8/0.4 [cert engine a83c9f6d store b1fd0bce config c2d233ae]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine a83c9f6d store b1fd0bce config c2d233aec104): MATCHES the sealed baseline. current=ef2fbf9caf2ef63e.. (2649 players) vs baseline=ef2fbf9caf2ef63e.. (2649 players, sealed head a83c9f6d) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=8d90c9ac vs shipped 8d90c9ac (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 62 saves, aggregate lift +2199; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1349, 1549, 1881, 2587, 3245, 3368, 3502, 3587, 3689, 3789, 3975, 4162, 4369, 4506, 4586]; dips(more games worth less)=none; 0->6 rise T=+2153; 0->6 steps>50%T=none; rise by 3g=+1238 (need >=538) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=4  FEATURE=1  HALT=1  PASS=15  PENDING=4  STRUCK=1  (369s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr5, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 128 | 168 | 168 | 182 | 160 | 145 |
| 2005 | 4 | 100 | 151 | 143 | 192 | 183 | 181 | 156 |
| 2006 | 5 | 100 | 120 | 127 | 139 | 146 | 144 | 127 |
| 2007 | 5 | 100 | 119 | 109 | 114 | 143 | 135 | 113 |
| 2008 | 4 | 100 | 118 | 152 | 164 | 148 | 130 | 118 |
| 2009 | 2 | 100 | 113 | 97 | 98 | 99 | 91 | 81 |
| 2010 | 5 | 100 | 120 | 125 | 138 | 140 | 122 | 99 |
| 2011 | 4 | 100 | 118 | 132 | 147 | 146 | 143 | 122 |
| 2012 | 4 | 100 | 102 | 111 | 112 | 107 | 108 | 90 |
| 2013 | 5 | 100 | 120 | 133 | 152 | 157 | 145 | 114 |
| 2014 | 4 | 100 | 112 | 123 | 126 | 115 | 124 | 118 |
| 2015 | 6 | 100 | 107 | 106 | 106 | 105 | 109 | 107 |
| 2016 | 4 | 100 | 117 | 133 | 154 | 144 | 146 | 126 |
| 2017 | 3 | 100 | 112 | 113 | 105 | 103 | 105 | 100 |
| 2018 | 2 | 100 | 115 | 104 | 112 | 113 | 109 | 103 |
| 2019 | 5 | 100 | 100 | 105 | 112 | 126 | 120 | 100 |
| 2020 | 6 | 100 | 101 | 97 | 91 | 100 | 101 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _5_ | _100_ | _116_ | _122_ | _131_ | _133_ | _128_ | _114_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **70556** | **81592** | **85773** | **91843** | **92850** | **89354** | **80318** |

B5 FLOOR-SAVES table (n=62, aggregate lift=+2199 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 16 | 140.8 | 170 | +154 | clear |
| Stephen Coniglio | — | 15 | 23 | 140.8 | 170 | +147 | clear |
| Jaeger O'Meara | — | 15 | 62 | 150.0 | 193 | +131 | clear |
| Chayce Jones | — | 8 | 14 | 85.4 | 115 | +101 | clear |
| Steele Sidebottom | — | 18 | 3 | 81.2 | 102 | +99 | clear |
| Oliver Wiltshire | — | 3 | 14 | 98.3 | 106 | +92 | clear |
| Harvey Gallagher | — | 4 | 77 | 153.3 | 140 | +63 | clear |
| Luke Pedlar | — | 6 | 85 | 146.2 | 148 | +63 | clear |
| Bailey Laurie | — | 6 | 20 | 87.8 | 76 | +56 | clear |
| Conor Stone | — | 6 | 36 | 114.1 | 90 | +54 | clear |
| Jack Martin | — | 14 | 47 | 140.8 | 100 | +53 | clear |
| Callum Ah Chee | — | 11 | 39 | 87.0 | 88 | +49 | clear |
| Phoenix Gothard | — | 3 | 394 | 443.2 | 442 | +48 | clear |
| Billy Cootee | — | 1 | 45 | 305.6 | 91 | +46 | clear |
| Sam Sturt | — | 8 | 15 | 60.8 | 56 | +41 | clear |
| Liam Stocker | — | 8 | 2 | 58.6 | 42 | +40 | clear |
| Nicholas Coffield | — | 9 | 15 | 87.0 | 55 | +40 | clear |
| Finlay Macrae | — | 6 | 75 | 101.3 | 114 | +39 | clear |
| Jacob Hopper | — | 11 | 88 | 87.0 | 127 | +39 | clear |
| Jade Gresham | — | 11 | 14 | 60.1 | 53 | +39 | clear |
| Oscar Adams | — | 5 | 42 | 58.8 | 79 | +37 | clear |
| Brandon Starcevich | — | 9 | 7 | 60.1 | 44 | +37 | clear |
| Jake Melksham | — | 17 | 15 | 82.9 | 52 | +37 | clear |
| Charlie Spargo | — | 9 | 1 | 42.2 | 37 | +36 | clear |
| Oliver Henry | — | 6 | 63 | 108.2 | 96 | +33 | clear |
| Laitham Vandermeer | — | 8 | 1 | 37.2 | 33 | +32 | clear |
| Judson Clarke | — | 5 | 64 | 106.9 | 94 | +30 | clear |
| Jamie Elliott | — | 15 | 6 | 34.0 | 33 | +27 | clear |
| Darcy Gardiner | — | 13 | 21 | 51.0 | 47 | +26 | clear |
| Alex Pearce | — | 13 | 14 | 37.2 | 40 | +26 | clear |
| Jed Bews | — | 15 | 1 | 17.2 | 27 | +26 | clear |
| Nicholas Holman | — | 13 | 0 | 24.8 | 25 | +25 | clear |
| Rhys Stanley | — | 18 | 13 | 27.4 | 38 | +25 | clear |
| Liam Henry | — | 7 | 63 | 85.4 | 87 | +24 | clear |
| Ben Long | — | 10 | 9 | 45.9 | 33 | +24 | clear |
| Joel Hamling | — | 15 | 14 | 31.5 | 37 | +23 | clear |
| Matt Guelfi | — | 9 | 5 | 17.2 | 27 | +22 | clear |
| Ben McKay | — | 11 | 26 | 53.7 | 48 | +22 | clear |
| Reef McInnes | — | 6 | 60 | 84.7 | 81 | +21 | clear |
| Ryan Gardner | — | 11 | 13 | 18.3 | 34 | +21 | clear |
| Oskar Baker | — | 9 | 13 | 26.0 | 33 | +20 | clear |
| Mitch McGovern | — | 12 | 9 | 32.8 | 28 | +19 | clear |
| Jacob Wehr | — | 6 | 4 | 31.6 | 22 | +18 | clear |
| Lachlan Weller | — | 12 | 67 | 67.8 | 85 | +18 | clear |
| Daniel Butler | — | 12 | 3 | 17.2 | 21 | +18 | clear |
| Harry Schoenberg | — | 7 | 41 | 47.1 | 58 | +17 | clear |
| Aidan Corr | — | 14 | 35 | 60.1 | 52 | +17 | clear |
| Noah Answerth | — | 8 | 18 | 19.6 | 33 | +15 | clear |
| Finn Maginness | — | 7 | 25 | 42.2 | 37 | +12 | clear |
| Jake Kolodjashnij | — | 13 | 27 | 35.0 | 39 | +12 | clear |
| Kaleb Smith | — | 4 | 117 | 104.0 | 127 | +10 | clear |
| Jackson Archer | — | 5 | 69 | 46.8 | 79 | +10 | clear |
| Hunter Clark | — | 9 | 47 | 87.0 | 57 | +10 | clear |
| Tom Cole | — | 11 | 22 | 37.4 | 32 | +10 | clear |
| Jamie Cripps | — | 16 | 26 | 41.1 | 36 | +10 | clear |
| Bailey Macdonald | — | 4 | 118 | 94.9 | 127 | +9 | clear |
| James Jordon | — | 8 | 38 | 38.5 | 45 | +7 | clear |
| Callum Coleman-Jones | — | 9 | 37 | 56.3 | 43 | +6 | clear |
| Liam Ryan | — | 9 | 25 | 45.0 | 31 | +6 | clear |
| Nathan Broad | — | 11 | 9 | 17.2 | 12 | +3 | clear |
| Luke McDonald | — | 13 | 52 | 87.0 | 55 | +3 | clear |
| Harvey Harrison | — | 5 | 62 | 56.4 | 63 | +1 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT a83c9f6d
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Luke Jackson | RUC | 7799 | 6803 | 9260 | +1461 | +2457 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 8567 | +517 | +1565 |
| 3 | Harry Sheezel | MID | 8115 | 7151 | 8426 | +311 | +1275 |
| 4 | Tristan Xerri | RUC | 6649 | 5795 | 8004 | +1355 | +2209 |
| 5 | Max Holmes | MID | 6269 | 5386 | 7260 | +991 | +1874 |
| 6 | Josh Treacy | KEY_FWD | — | — | 7196 | — | — |
| 7 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 7011 | +405 | +1217 |
| 8 | Zak Butters | MID | 6059 | 5174 | 6369 | +310 | +1195 |
| 9 | Errol Gulden | MID | 5983 | 5256 | 6237 | +254 | +981 |
| 10 | Bailey Smith | MID | 5605 | 4715 | 6005 | +400 | +1290 |
| 11 | Finn Callaghan | MID | 5442 | 4904 | 5960 | +518 | +1056 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5843 | +656 | +1232 |
| 13 | Noah Anderson | MID | 4765 | 4091 | 5401 | +636 | +1310 |
| 14 | Archie Roberts | GEN_DEF | 4577 | 4668 | 5327 | +750 | +659 |
| 15 | Will Ashcroft | MID | 5155 | 4768 | 5217 | +62 | +449 |
| 16 | Sam Darcy | KEY_FWD | 4013 | 4144 | 5094 | +1081 | +950 |
| 17 | Tom Green | MID | 4391 | 4424 | 4996 | +605 | +572 |
| 18 | Brodie Grundy | RUC | 3959 | 3314 | 4807 | +848 | +1493 |
| 19 | Caleb Serong | MID | 4701 | 4170 | 4799 | +98 | +629 |
| 20 | Willem Duursma | MID | 4429 | 4110 | 4569 | +140 | +459 |
| 21 | Nick Blakey | GEN_DEF | 3598 | 3266 | 4568 | +970 | +1302 |
| 22 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 4447 | +629 | +745 |
| 23 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 4401 | +434 | +669 |
| 24 | Jai Newcombe | MID | — | — | 4388 | — | — |
| 25 | Murphy Reid | GEN_FWD | 3953 | 3742 | 4200 | +247 | +458 |
| 26 | Matt Rowell | MID | 4185 | 3752 | 4189 | +4 | +437 |
| 27 | Isaac Heeney | MID | 3981 | 3301 | 4178 | +197 | +877 |
| 28 | Ryley Sanders | MID | 4129 | 3926 | 4160 | +31 | +234 |
| 29 | Jason Horne-Francis | MID | 3996 | 3702 | 4135 | +139 | +433 |
| 30 | Jordan Clark | GEN_DEF | 3307 | 3007 | 4078 | +771 | +1071 |
| 31 | Mac Andrew | KEY_DEF | 3691 | 3504 | 4075 | +384 | +571 |
| 32 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 4070 | +574 | +994 |
| 33 | Colby McKercher | MID | 3829 | 3627 | 3866 | +37 | +239 |
| 34 | Timothy English | RUC | 3349 | 2916 | 3846 | +497 | +930 |
| 35 | Marcus Bontempelli | MID | 3721 | 3084 | 3815 | +94 | +731 |
| 36 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3810 | +351 | +880 |
| 37 | Will Day | MID | 3108 | 2806 | 3803 | +695 | +997 |
| 38 | Sam Berry | MID | 2648 | 2495 | 3799 | +1151 | +1304 |
| 39 | Callum Wilkie | KEY_DEF | — | — | 3781 | — | — |
| 40 | Nick Watson | GEN_FWD | 3720 | 3538 | 3722 | +2 | +184 |
| 41 | Jordan Dawson | MID | 3312 | 2758 | 3714 | +402 | +956 |
| 42 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3706 | +610 | +780 |
| 43 | Josh Worrell | GEN_DEF | 3180 | 2937 | 3652 | +472 | +715 |
| 44 | Harley Reid | MID | 3726 | 3549 | 3650 | -76 | +101 |
| 45 | Jagga Smith | MID | 3192 | 2822 | 3587 | +395 | +765 |
| 46 | Finn O'Sullivan | MID | 3643 | 3427 | 3553 | -90 | +126 |
| 47 | Bodhi Uwland | GEN_DEF | — | — | 3552 | — | — |
| 48 | Nicholas Martin | MID | — | — | 3514 | — | — |
| 49 | Ed Richards | MID | 3078 | 2625 | 3490 | +412 | +865 |
| 50 | Sam Lalor | MID | 3574 | 3337 | 3484 | -90 | +147 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
