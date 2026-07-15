# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ fc7045d6 — NOT AN ENDORSED STATE — head fc7045d6 store b1fd0bce config c2d233aec104
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ fc7045d6 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head fc7045d6 store b1fd0bce config c2d233aec104 — suite 764a0d91 — 2026-07-15 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash c2d233aec1041a2d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=fc7045d6 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4555 vs 2522
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1597 vs 1910 (Ward=2122, ratio=0.753) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1640 vs 2122
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3145 2025=4883 ratio=0.64 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=40 ev=3649 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=2293 (floor 1600); Jake Bowey=3794 (floor 2100); Nick Blakey=4330 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=482 (n=12, pooled — thin slice) vs pick-matched MID kernel median=666 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=3608 Tsatas=1467 ratio=2.46x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 2293 vs 2122
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1277 2025=2258 ratio=0.57 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2237 vs 1021; Cumming>Annable: 2232 vs 2140
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 660 vs 958; Smillie>Retschko: 1346 vs 869
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3248 lineball=True; Levi Ashcroft=3344 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1709: Trent Rivers=2176 lineball=False; Zach Reid=1797 lineball=True; Jase Burgoyne=2269 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | HALT     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine fc7045d6 store b1fd0bce config c2d233aec104): y1=70457.8 y2=81467.2 y3=85521.8 y4=91311.3 y5=91996.6 y6=88380.6 y7=79185.7; den=min(y1,y2)=y1=70457.8; ratios y4=1.2960(above-guide) y5=1.3057(above-guide) y6=1.2544(above-guide); hard<=1.30 -> BREACH at y[5] (HALT); guide 1.20-1.25 ADVISORY (margin reported, never gates)  <- MOVED
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells KEY_DEF|GOOD|T5:5.29, RUC|GOOD|T5:5.12, GEN_DEF|GOOD|T2:4.20, GEN_DEF|GOOD|T4:4.12; GOOD>BUST sep GEN_DEF 37.8/1.0, GEN_FWD 40.5/0.6, KEY_DEF 50.5/1.1, KEY_FWD 62.9/0.6, MID 47.1/0.5, RUC 26.0/0.4 [cert engine fc7045d6 store b1fd0bce config c2d233ae]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine fc7045d6 store b1fd0bce config c2d233aec104): MATCHES the sealed baseline. current=99be9b3672bc1e12.. (2649 players) vs baseline=99be9b3672bc1e12.. (2649 players, sealed head fc7045d6) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=790136a3 vs shipped 790136a3 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 60 saves, aggregate lift +2176; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1341, 1540, 1871, 2573, 3227, 3348, 3483, 3567, 3669, 3768, 3953, 4139, 4344, 4481, 4560]; dips(more games worth less)=none; 0->6 rise T=+2142; 0->6 steps>50%T=none; rise by 3g=+1232 (need >=536) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  HALT=1  PASS=16  PENDING=4  STRUCK=1  (540s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr5, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 128 | 168 | 167 | 181 | 160 | 144 |
| 2005 | 4 | 100 | 151 | 142 | 191 | 181 | 179 | 155 |
| 2006 | 5 | 100 | 119 | 126 | 138 | 143 | 142 | 125 |
| 2007 | 5 | 100 | 119 | 109 | 113 | 142 | 135 | 113 |
| 2008 | 4 | 100 | 120 | 152 | 163 | 147 | 129 | 117 |
| 2009 | 2 | 100 | 112 | 96 | 97 | 97 | 89 | 78 |
| 2010 | 5 | 100 | 119 | 125 | 137 | 139 | 121 | 98 |
| 2011 | 4 | 100 | 118 | 132 | 147 | 145 | 142 | 121 |
| 2012 | 4 | 100 | 102 | 110 | 111 | 106 | 106 | 88 |
| 2013 | 5 | 100 | 120 | 133 | 152 | 158 | 145 | 114 |
| 2014 | 4 | 100 | 113 | 123 | 127 | 115 | 123 | 117 |
| 2015 | 6 | 100 | 107 | 106 | 105 | 105 | 109 | 106 |
| 2016 | 4 | 100 | 117 | 132 | 152 | 141 | 143 | 122 |
| 2017 | 3 | 100 | 112 | 113 | 104 | 101 | 102 | 96 |
| 2018 | 2 | 100 | 115 | 104 | 111 | 112 | 109 | 102 |
| 2019 | 5 | 100 | 100 | 106 | 113 | 127 | 120 | 100 |
| 2020 | 2 | 100 | 101 | 98 | 91 | 100 | 100 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _5_ | _100_ | _116_ | _122_ | _130_ | _132_ | _127_ | _112_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **70458** | **81467** | **85522** | **91311** | **91997** | **88381** | **79186** |

B5 FLOOR-SAVES table (n=60, aggregate lift=+2176 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 16 | 140.8 | 169 | +153 | clear |
| Stephen Coniglio | — | 15 | 23 | 140.8 | 169 | +146 | clear |
| Jaeger O'Meara | — | 15 | 62 | 150.0 | 192 | +130 | clear |
| Chayce Jones | — | 8 | 14 | 85.4 | 114 | +100 | clear |
| Steele Sidebottom | — | 18 | 3 | 81.2 | 102 | +99 | clear |
| Oliver Wiltshire | — | 3 | 14 | 98.3 | 107 | +93 | clear |
| Harvey Gallagher | — | 4 | 76 | 153.3 | 140 | +64 | clear |
| Luke Pedlar | — | 6 | 81 | 146.2 | 145 | +64 | clear |
| Bailey Laurie | — | 6 | 20 | 87.8 | 76 | +56 | clear |
| Conor Stone | — | 6 | 35 | 114.1 | 88 | +53 | clear |
| Jack Martin | — | 14 | 47 | 140.8 | 99 | +52 | clear |
| Billy Cootee | — | 1 | 43 | 305.6 | 91 | +48 | clear |
| Phoenix Gothard | — | 3 | 385 | 443.2 | 432 | +47 | clear |
| Callum Ah Chee | — | 11 | 41 | 87.0 | 88 | +47 | clear |
| Sam Sturt | — | 8 | 16 | 60.8 | 56 | +40 | clear |
| Liam Stocker | — | 8 | 2 | 58.6 | 42 | +40 | clear |
| Finlay Macrae | — | 6 | 74 | 101.3 | 113 | +39 | clear |
| Nicholas Coffield | — | 9 | 16 | 87.0 | 55 | +39 | clear |
| Jade Gresham | — | 11 | 14 | 60.1 | 53 | +39 | clear |
| Oscar Adams | — | 5 | 42 | 58.8 | 79 | +37 | clear |
| Brandon Starcevich | — | 9 | 7 | 60.1 | 44 | +37 | clear |
| Jacob Hopper | — | 11 | 89 | 87.0 | 126 | +37 | clear |
| Jake Melksham | — | 17 | 15 | 82.9 | 52 | +37 | clear |
| Charlie Spargo | — | 9 | 1 | 42.2 | 37 | +36 | clear |
| Judson Clarke | — | 5 | 62 | 106.9 | 94 | +32 | clear |
| Oliver Henry | — | 6 | 63 | 108.2 | 95 | +32 | clear |
| Laitham Vandermeer | — | 8 | 2 | 37.2 | 33 | +31 | clear |
| Jed Bews | — | 15 | 1 | 17.2 | 28 | +27 | clear |
| Jamie Elliott | — | 15 | 6 | 34.0 | 33 | +27 | clear |
| Darcy Gardiner | — | 13 | 21 | 51.0 | 47 | +26 | clear |
| Rhys Stanley | — | 18 | 12 | 27.4 | 38 | +26 | clear |
| Alex Pearce | — | 13 | 14 | 37.2 | 39 | +25 | clear |
| Nicholas Holman | — | 13 | 0 | 24.8 | 25 | +25 | clear |
| Ben Long | — | 10 | 9 | 45.9 | 33 | +24 | clear |
| Ben McKay | — | 11 | 26 | 53.7 | 49 | +23 | clear |
| Joel Hamling | — | 15 | 14 | 31.5 | 37 | +23 | clear |
| Matt Guelfi | — | 9 | 5 | 17.2 | 27 | +22 | clear |
| Ryan Gardner | — | 11 | 13 | 18.3 | 35 | +22 | clear |
| Liam Henry | — | 7 | 66 | 85.4 | 86 | +20 | clear |
| Oskar Baker | — | 9 | 13 | 26.0 | 33 | +20 | clear |
| Mitch McGovern | — | 12 | 9 | 32.8 | 28 | +19 | clear |
| Reef McInnes | — | 6 | 63 | 84.7 | 81 | +18 | clear |
| Jacob Wehr | — | 6 | 4 | 31.6 | 22 | +18 | clear |
| Daniel Butler | — | 12 | 3 | 17.2 | 21 | +18 | clear |
| Aidan Corr | — | 14 | 35 | 60.1 | 52 | +17 | clear |
| Harry Schoenberg | — | 7 | 42 | 47.1 | 58 | +16 | clear |
| Noah Answerth | — | 8 | 17 | 19.6 | 33 | +16 | clear |
| Lachlan Weller | — | 12 | 68 | 67.8 | 84 | +16 | clear |
| Finn Maginness | — | 7 | 23 | 42.2 | 37 | +14 | clear |
| Jake Kolodjashnij | — | 13 | 26 | 35.0 | 38 | +12 | clear |
| Kaleb Smith | — | 4 | 117 | 104.0 | 128 | +11 | clear |
| Jamie Cripps | — | 16 | 25 | 41.1 | 36 | +11 | clear |
| Jackson Archer | — | 5 | 69 | 46.8 | 79 | +10 | clear |
| Bailey Macdonald | — | 4 | 119 | 94.9 | 128 | +9 | clear |
| Tom Cole | — | 11 | 24 | 37.4 | 32 | +8 | clear |
| James Jordon | — | 8 | 38 | 38.5 | 44 | +6 | clear |
| Hunter Clark | — | 9 | 51 | 87.0 | 57 | +6 | clear |
| Callum Coleman-Jones | — | 9 | 37 | 56.3 | 43 | +6 | clear |
| Liam Ryan | — | 9 | 27 | 45.0 | 31 | +4 | clear |
| Nathan Broad | — | 11 | 9 | 17.2 | 12 | +3 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT fc7045d6
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Luke Jackson | RUC | 7799 | 6803 | 9252 | +1453 | +2449 |
| 2 | Harry Sheezel | MID | 8115 | 7151 | 8520 | +405 | +1369 |
| 3 | Nick Daicos | MID | 8050 | 7002 | 8471 | +421 | +1469 |
| 4 | Tristan Xerri | RUC | 6649 | 5795 | 7225 | +576 | +1430 |
| 5 | Max Holmes | MID | 6269 | 5386 | 7150 | +881 | +1764 |
| 6 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 7010 | +404 | +1216 |
| 7 | Josh Treacy | KEY_FWD | — | — | 6800 | — | — |
| 8 | Errol Gulden | MID | 5983 | 5256 | 6394 | +411 | +1138 |
| 9 | Zak Butters | MID | 6059 | 5174 | 6369 | +310 | +1195 |
| 10 | Bailey Smith | MID | 5605 | 4715 | 6044 | +439 | +1329 |
| 11 | Finn Callaghan | MID | 5442 | 4904 | 6027 | +585 | +1123 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5842 | +655 | +1231 |
| 13 | Noah Anderson | MID | 4765 | 4091 | 5401 | +636 | +1310 |
| 14 | Archie Roberts | GEN_DEF | 4577 | 4668 | 5385 | +808 | +717 |
| 15 | Will Ashcroft | MID | 5155 | 4768 | 5216 | +61 | +448 |
| 16 | Tom Green | MID | 4391 | 4424 | 4995 | +604 | +571 |
| 17 | Sam Darcy | KEY_FWD | 4013 | 4144 | 4794 | +781 | +650 |
| 18 | Caleb Serong | MID | 4701 | 4170 | 4735 | +34 | +565 |
| 19 | Willem Duursma | MID | 4429 | 4110 | 4555 | +126 | +445 |
| 20 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 4400 | +433 | +668 |
| 21 | Murphy Reid | GEN_FWD | 3953 | 3742 | 4353 | +400 | +611 |
| 22 | Nick Blakey | GEN_DEF | 3598 | 3266 | 4330 | +732 | +1064 |
| 23 | Ryley Sanders | MID | 4129 | 3926 | 4220 | +91 | +294 |
| 24 | Jai Newcombe | MID | — | — | 4193 | — | — |
| 25 | Matt Rowell | MID | 4185 | 3752 | 4189 | +4 | +437 |
| 26 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 4187 | +369 | +485 |
| 27 | Jason Horne-Francis | MID | 3996 | 3702 | 4135 | +139 | +433 |
| 28 | Isaac Heeney | MID | 3981 | 3301 | 4131 | +150 | +830 |
| 29 | Brodie Grundy | RUC | 3959 | 3314 | 4109 | +150 | +795 |
| 30 | Mac Andrew | KEY_DEF | 3691 | 3504 | 4074 | +383 | +570 |
| 31 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 4065 | +569 | +989 |
| 32 | Jordan Clark | GEN_DEF | 3307 | 3007 | 4017 | +710 | +1010 |
| 33 | Colby McKercher | MID | 3829 | 3627 | 3864 | +35 | +237 |
| 34 | Will Day | MID | 3108 | 2806 | 3802 | +694 | +996 |
| 35 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3794 | +698 | +868 |
| 36 | Marcus Bontempelli | MID | 3721 | 3084 | 3773 | +52 | +689 |
| 37 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3768 | +309 | +838 |
| 38 | Nick Watson | GEN_FWD | 3720 | 3538 | 3718 | -2 | +180 |
| 39 | Callum Wilkie | KEY_DEF | — | — | 3685 | — | — |
| 40 | Harley Reid | MID | 3726 | 3549 | 3649 | -77 | +100 |
| 41 | Jagga Smith | MID | 3192 | 2822 | 3617 | +425 | +795 |
| 42 | Sam Berry | MID | 2648 | 2495 | 3608 | +960 | +1113 |
| 43 | Finn O'Sullivan | MID | 3643 | 3427 | 3545 | -98 | +118 |
| 44 | Aaron Cadman | KEY_FWD | 3122 | 2970 | 3532 | +410 | +562 |
| 45 | Jordan Dawson | MID | 3312 | 2758 | 3497 | +185 | +739 |
| 46 | Ed Richards | MID | 3078 | 2625 | 3490 | +412 | +865 |
| 47 | Bodhi Uwland | GEN_DEF | — | — | 3474 | — | — |
| 48 | Sam Lalor | MID | 3574 | 3337 | 3472 | -102 | +135 |
| 49 | Logan Morris | KEY_FWD | 3171 | 3018 | 3443 | +272 | +425 |
| 50 | Timothy English | RUC | 3349 | 2916 | 3405 | +56 | +489 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
