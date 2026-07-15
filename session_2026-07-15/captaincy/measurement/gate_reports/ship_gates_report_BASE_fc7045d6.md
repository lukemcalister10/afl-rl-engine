# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ fc7045d6 — NOT AN ENDORSED STATE — head fc7045d6 store b1fd0bce config c2d233aec104
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ fc7045d6 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head fc7045d6 store b1fd0bce config c2d233aec104 — suite 764a0d91 — 2026-07-15 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash c2d233aec1041a2d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=fc7045d6 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4572 vs 2555
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1619 vs 1934 (Ward=2149, ratio=0.753) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1662 vs 2149
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3163 2025=4864 ratio=0.65 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=39 ev=3688 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=2324 (floor 1600); Jake Bowey=3841 (floor 2100); Nick Blakey=4354 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=484 (n=12, pooled — thin slice) vs pick-matched MID kernel median=674 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=3623 Tsatas=1481 ratio=2.45x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 2324 vs 2149
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1295 2025=2288 ratio=0.57 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2266 vs 1034; Cumming>Annable: 2252 vs 2147
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 669 vs 970; Smillie>Retschko: 1349 vs 881
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3285 lineball=True; Levi Ashcroft=3354 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=2205 lineball=False; Zach Reid=1822 lineball=True; Jase Burgoyne=2300 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine fc7045d6 store b1fd0bce config c2d233aec104): y1=71090.1 y2=82294.5 y3=86310.9 y4=91893.8 y5=92382.8 y6=88469.2 y7=79210.1; den=min(y1,y2)=y1=71090.1; ratios y4=1.2926(above-guide) y5=1.2995(above-guide) y6=1.2445(in-guide); hard<=1.30 -> PASS x3; guide 1.20-1.25 ADVISORY (margin reported, never gates)
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:5.88, KEY_DEF|GOOD|T5:5.25, GEN_DEF|GOOD|T2:4.25, GEN_DEF|GOOD|T4:4.14; GOOD>BUST sep GEN_DEF 37.8/0.9, GEN_FWD 40.5/0.6, KEY_DEF 50.5/1.1, KEY_FWD 62.9/0.6, MID 47.5/0.5, RUC 26.1/0.4 [cert engine fc7045d6 store b1fd0bce config c2d233ae]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine fc7045d6 store b1fd0bce config c2d233aec104): MATCHES the sealed baseline. current=cf90c4f4844ba26d.. (2649 players) vs baseline=cf90c4f4844ba26d.. (2649 players, sealed head fc7045d6) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=800d0399 vs shipped 800d0399 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 60 saves, aggregate lift +2195; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1353, 1552, 1882, 2587, 3244, 3362, 3491, 3572, 3670, 3765, 3942, 4120, 4318, 4449, 4525]; dips(more games worth less)=none; 0->6 rise T=+2138; 0->6 steps>50%T=none; rise by 3g=+1234 (need >=534) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1  (483s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr5, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 129 | 169 | 167 | 182 | 160 | 144 |
| 2005 | 4 | 100 | 151 | 142 | 190 | 180 | 177 | 153 |
| 2006 | 5 | 100 | 120 | 126 | 137 | 142 | 141 | 124 |
| 2007 | 5 | 100 | 120 | 110 | 113 | 141 | 134 | 112 |
| 2008 | 4 | 100 | 120 | 152 | 161 | 146 | 128 | 116 |
| 2009 | 2 | 100 | 113 | 97 | 97 | 97 | 89 | 78 |
| 2010 | 5 | 100 | 119 | 124 | 137 | 138 | 120 | 98 |
| 2011 | 4 | 100 | 118 | 132 | 147 | 144 | 141 | 120 |
| 2012 | 4 | 100 | 102 | 110 | 111 | 106 | 103 | 86 |
| 2013 | 5 | 100 | 120 | 133 | 151 | 157 | 143 | 113 |
| 2014 | 4 | 100 | 113 | 123 | 127 | 115 | 122 | 116 |
| 2015 | 6 | 100 | 107 | 106 | 105 | 104 | 107 | 105 |
| 2016 | 4 | 100 | 117 | 132 | 151 | 141 | 143 | 121 |
| 2017 | 3 | 100 | 112 | 113 | 104 | 101 | 101 | 95 |
| 2018 | 2 | 100 | 115 | 104 | 111 | 111 | 108 | 101 |
| 2019 | 5 | 100 | 100 | 106 | 112 | 125 | 118 | 99 |
| 2020 | 2 | 100 | 101 | 97 | 91 | 99 | 99 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _5_ | _100_ | _116_ | _122_ | _130_ | _131_ | _126_ | _111_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **71090** | **82294** | **86311** | **91894** | **92383** | **88469** | **79210** |

B5 FLOOR-SAVES table (n=60, aggregate lift=+2195 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 16 | 140.8 | 169 | +153 | clear |
| Stephen Coniglio | — | 15 | 23 | 140.8 | 169 | +146 | clear |
| Jaeger O'Meara | — | 15 | 63 | 150.0 | 192 | +129 | clear |
| Chayce Jones | — | 8 | 14 | 85.4 | 115 | +101 | clear |
| Steele Sidebottom | — | 18 | 3 | 81.2 | 103 | +100 | clear |
| Oliver Wiltshire | — | 3 | 14 | 98.3 | 109 | +95 | clear |
| Harvey Gallagher | — | 4 | 77 | 153.3 | 142 | +65 | clear |
| Luke Pedlar | — | 6 | 82 | 146.2 | 147 | +65 | clear |
| Bailey Laurie | — | 6 | 21 | 87.8 | 77 | +56 | clear |
| Conor Stone | — | 6 | 36 | 114.1 | 90 | +54 | clear |
| Jack Martin | — | 14 | 48 | 140.8 | 101 | +53 | clear |
| Billy Cootee | — | 1 | 44 | 305.6 | 92 | +48 | clear |
| Callum Ah Chee | — | 11 | 41 | 87.0 | 89 | +48 | clear |
| Phoenix Gothard | — | 3 | 390 | 443.2 | 437 | +47 | clear |
| Sam Sturt | — | 8 | 16 | 60.8 | 57 | +41 | clear |
| Liam Stocker | — | 8 | 2 | 58.6 | 43 | +41 | clear |
| Nicholas Coffield | — | 9 | 16 | 87.0 | 56 | +40 | clear |
| Jade Gresham | — | 11 | 14 | 60.1 | 54 | +40 | clear |
| Finlay Macrae | — | 6 | 75 | 101.3 | 114 | +39 | clear |
| Brandon Starcevich | — | 9 | 7 | 60.1 | 45 | +38 | clear |
| Jake Melksham | — | 17 | 15 | 82.9 | 53 | +38 | clear |
| Oscar Adams | — | 5 | 43 | 58.8 | 80 | +37 | clear |
| Charlie Spargo | — | 9 | 1 | 42.2 | 37 | +36 | clear |
| Jacob Hopper | — | 11 | 90 | 87.0 | 126 | +36 | clear |
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
| Liam Henry | — | 7 | 67 | 85.4 | 87 | +20 | clear |
| Oskar Baker | — | 9 | 14 | 26.0 | 33 | +19 | clear |
| Mitch McGovern | — | 12 | 9 | 32.8 | 28 | +19 | clear |
| Daniel Butler | — | 12 | 3 | 17.2 | 22 | +19 | clear |
| Reef McInnes | — | 6 | 64 | 84.7 | 82 | +18 | clear |
| Jacob Wehr | — | 6 | 4 | 31.6 | 22 | +18 | clear |
| Aidan Corr | — | 14 | 35 | 60.1 | 53 | +18 | clear |
| Noah Answerth | — | 8 | 17 | 19.6 | 33 | +16 | clear |
| Lachlan Weller | — | 12 | 69 | 67.8 | 85 | +16 | clear |
| Harry Schoenberg | — | 7 | 43 | 47.1 | 58 | +15 | clear |
| Finn Maginness | — | 7 | 23 | 42.2 | 37 | +14 | clear |
| Jake Kolodjashnij | — | 13 | 26 | 35.0 | 39 | +13 | clear |
| Jamie Cripps | — | 16 | 25 | 41.1 | 37 | +12 | clear |
| Jackson Archer | — | 5 | 69 | 46.8 | 80 | +11 | clear |
| Kaleb Smith | — | 4 | 119 | 104.0 | 129 | +10 | clear |
| Bailey Macdonald | — | 4 | 121 | 94.9 | 129 | +8 | clear |
| Tom Cole | — | 11 | 24 | 37.4 | 32 | +8 | clear |
| Callum Coleman-Jones | — | 9 | 37 | 56.3 | 44 | +7 | clear |
| James Jordon | — | 8 | 39 | 38.5 | 45 | +6 | clear |
| Hunter Clark | — | 9 | 52 | 87.0 | 58 | +6 | clear |
| Liam Ryan | — | 9 | 28 | 45.0 | 31 | +3 | clear |
| Nathan Broad | — | 11 | 9 | 17.2 | 12 | +3 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT fc7045d6
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Luke Jackson | RUC | 7799 | 6803 | 8648 | +849 | +1845 |
| 2 | Harry Sheezel | MID | 8115 | 7151 | 8209 | +94 | +1058 |
| 3 | Nick Daicos | MID | 8050 | 7002 | 8069 | +19 | +1067 |
| 4 | Max Holmes | MID | 6269 | 5386 | 6918 | +649 | +1532 |
| 5 | Josh Treacy | KEY_FWD | — | — | 6887 | — | — |
| 6 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 6849 | +243 | +1055 |
| 7 | Tristan Xerri | RUC | 6649 | 5795 | 6742 | +93 | +947 |
| 8 | Errol Gulden | MID | 5983 | 5256 | 6278 | +295 | +1022 |
| 9 | Zak Butters | MID | 6059 | 5174 | 6143 | +84 | +969 |
| 10 | Finn Callaghan | MID | 5442 | 4904 | 5973 | +531 | +1069 |
| 11 | Bailey Smith | MID | 5605 | 4715 | 5848 | +243 | +1133 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5768 | +581 | +1157 |
| 13 | Archie Roberts | GEN_DEF | 4577 | 4668 | 5417 | +840 | +749 |
| 14 | Noah Anderson | MID | 4765 | 4091 | 5337 | +572 | +1246 |
| 15 | Will Ashcroft | MID | 5155 | 4768 | 5222 | +67 | +454 |
| 16 | Tom Green | MID | 4391 | 4424 | 4880 | +489 | +456 |
| 17 | Sam Darcy | KEY_FWD | 4013 | 4144 | 4858 | +845 | +714 |
| 18 | Caleb Serong | MID | 4701 | 4170 | 4730 | +29 | +560 |
| 19 | Willem Duursma | MID | 4429 | 4110 | 4572 | +143 | +462 |
| 20 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 4450 | +483 | +718 |
| 21 | Murphy Reid | GEN_FWD | 3953 | 3742 | 4413 | +460 | +671 |
| 22 | Nick Blakey | GEN_DEF | 3598 | 3266 | 4354 | +756 | +1088 |
| 23 | Ryley Sanders | MID | 4129 | 3926 | 4246 | +117 | +320 |
| 24 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 4245 | +427 | +543 |
| 25 | Matt Rowell | MID | 4185 | 3752 | 4231 | +46 | +479 |
| 26 | Jai Newcombe | MID | — | — | 4183 | — | — |
| 27 | Jason Horne-Francis | MID | 3996 | 3702 | 4182 | +186 | +480 |
| 28 | Mac Andrew | KEY_DEF | 3691 | 3504 | 4129 | +438 | +625 |
| 29 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 4114 | +618 | +1038 |
| 30 | Jordan Clark | GEN_DEF | 3307 | 3007 | 4059 | +752 | +1052 |
| 31 | Isaac Heeney | MID | 3981 | 3301 | 3998 | +17 | +697 |
| 32 | Brodie Grundy | RUC | 3959 | 3314 | 3939 | -20 | +625 |
| 33 | Colby McKercher | MID | 3829 | 3627 | 3887 | +58 | +260 |
| 34 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3841 | +745 | +915 |
| 35 | Will Day | MID | 3108 | 2806 | 3816 | +708 | +1010 |
| 36 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3798 | +339 | +868 |
| 37 | Nick Watson | GEN_FWD | 3720 | 3538 | 3768 | +48 | +230 |
| 38 | Callum Wilkie | KEY_DEF | — | — | 3735 | — | — |
| 39 | Harley Reid | MID | 3726 | 3549 | 3688 | -38 | +139 |
| 40 | Marcus Bontempelli | MID | 3721 | 3084 | 3664 | -57 | +580 |
| 41 | Jagga Smith | MID | 3192 | 2822 | 3629 | +437 | +807 |
| 42 | Sam Berry | MID | 2648 | 2495 | 3623 | +975 | +1128 |
| 43 | Aaron Cadman | KEY_FWD | 3122 | 2970 | 3579 | +457 | +609 |
| 44 | Finn O'Sullivan | MID | 3643 | 3427 | 3559 | -84 | +132 |
| 45 | Ed Richards | MID | 3078 | 2625 | 3524 | +446 | +899 |
| 46 | Bodhi Uwland | GEN_DEF | — | — | 3517 | — | — |
| 47 | Sam Lalor | MID | 3574 | 3337 | 3505 | -69 | +168 |
| 48 | Logan Morris | KEY_FWD | 3171 | 3018 | 3490 | +319 | +472 |
| 49 | Jordan Dawson | MID | 3312 | 2758 | 3486 | +174 | +728 |
| 50 | Timothy English | RUC | 3349 | 2916 | 3424 | +75 | +508 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
