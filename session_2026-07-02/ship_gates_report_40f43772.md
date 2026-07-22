# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 40f43772 — NOT AN ENDORSED STATE — head 40f43772 store 968de0c7 config c2d233aec104
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 40f43772 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 40f43772 store 968de0c7 config c2d233aec104 — suite 764a0d91 — 2026-07-17 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash c2d233aec1041a2d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=40f43772 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4488 vs 2456
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1589 vs 1897 (Ward=2108, ratio=0.754) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1661 vs 2108
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3229 2025=4807 ratio=0.67 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | FAIL     Harley Reid board rank=48 ev=3523 (need TOP 40)  <- MOVED
A5        PASS    | PASS    | PASS     Jack Ginnivan=2172 (floor 1600); Jake Bowey=3522 (floor 2100); Nick Blakey=4433 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=515 (n=11, pooled — thin slice) vs pick-matched MID kernel median=901 (n=73, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=3596 Tsatas=1475 ratio=2.44x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 2172 vs 2108
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1312 2025=2228 ratio=0.59 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2363 vs 1039; Cumming>Annable: 2230 vs 2166
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 633 vs 974; Smillie>Retschko: 1393 vs 872
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3267 lineball=True; Levi Ashcroft=3347 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1709: Trent Rivers=2121 lineball=False; Zach Reid=1825 lineball=True; Jase Burgoyne=2195 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine 40f43772 store 968de0c7 config c2d233aec104): y1=71768.1 y2=82289.6 y3=85605.9 y4=90787.3 y5=91122.7 y6=87985.3 y7=79985.2; den=min(y1,y2)=y1=71768.1; ratios y4=1.2650(above-guide) y5=1.2697(above-guide) y6=1.2260(in-guide); hard<=1.30 -> PASS x3; guide 1.20-1.25 ADVISORY (margin reported, never gates)
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:5.28, GEN_DEF|GOOD|T4:4.84, KEY_DEF|GOOD|T3:4.49, GEN_DEF|GOOD|T5:3.62; GOOD>BUST sep GEN_DEF 41.0/1.0, GEN_FWD 39.7/0.6, KEY_DEF 48.4/1.1, KEY_FWD 61.8/0.6, MID 50.0/0.5, RUC 26.8/0.4 [cert engine 40f43772 store 968de0c7 config c2d233ae]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine 40f43772 store 968de0c7 config c2d233aec104): MATCHES the sealed baseline. current=745e3462007aec2f.. (2649 players) vs baseline=745e3462007aec2f.. (2649 players, sealed head 40f43772) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=270a2c5f vs shipped 270a2c5f (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 60 saves, aggregate lift +2066; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1349, 1549, 1881, 2587, 3245, 3367, 3502, 3587, 3689, 3788, 3974, 4161, 4368, 4506, 4585]; dips(more games worth less)=none; 0->6 rise T=+2153; 0->6 steps>50%T=none; rise by 3g=+1238 (need >=538) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=4  FEATURE=1  PASS=16  PENDING=4  STRUCK=1  (481s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr5, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 129 | 166 | 164 | 176 | 157 | 144 |
| 2005 | 4 | 100 | 151 | 141 | 189 | 178 | 177 | 155 |
| 2006 | 6 | 100 | 118 | 124 | 136 | 139 | 139 | 123 |
| 2007 | 5 | 100 | 118 | 107 | 109 | 137 | 130 | 109 |
| 2008 | 4 | 100 | 118 | 148 | 158 | 141 | 125 | 115 |
| 2009 | 2 | 100 | 112 | 95 | 95 | 97 | 89 | 80 |
| 2010 | 5 | 100 | 118 | 122 | 132 | 134 | 117 | 96 |
| 2011 | 4 | 100 | 116 | 128 | 140 | 138 | 136 | 119 |
| 2012 | 4 | 100 | 101 | 108 | 109 | 102 | 105 | 88 |
| 2013 | 5 | 100 | 119 | 131 | 150 | 156 | 142 | 113 |
| 2014 | 4 | 100 | 114 | 122 | 124 | 111 | 120 | 115 |
| 2015 | 2 | 100 | 107 | 105 | 103 | 102 | 106 | 105 |
| 2016 | 4 | 100 | 116 | 131 | 148 | 139 | 142 | 124 |
| 2017 | 3 | 100 | 111 | 113 | 102 | 100 | 102 | 98 |
| 2018 | 2 | 100 | 115 | 102 | 110 | 110 | 107 | 102 |
| 2019 | 5 | 100 | 99 | 103 | 109 | 123 | 116 | 99 |
| 2020 | 1 | 100 | 99 | 95 | 89 | 97 | 97 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _5_ | _100_ | _115_ | _120_ | _128_ | _128_ | _124_ | _112_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **71768** | **82290** | **85606** | **90787** | **91123** | **87985** | **79985** |

B5 FLOOR-SAVES table (n=60, aggregate lift=+2066 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 16 | 133.8 | 174 | +158 | clear |
| Jaeger O'Meara | — | 15 | 62 | 150.0 | 204 | +142 | clear |
| Chayce Jones | — | 8 | 14 | 81.2 | 119 | +105 | clear |
| Steele Sidebottom | — | 18 | 3 | 78.2 | 107 | +104 | clear |
| Oliver Wiltshire | — | 3 | 14 | 150.9 | 107 | +93 | clear |
| Stephen Coniglio | — | 15 | 91 | 133.8 | 174 | +83 | clear |
| Harvey Gallagher | — | 4 | 77 | 144.9 | 142 | +65 | clear |
| Luke Pedlar | — | 6 | 85 | 140.8 | 149 | +64 | clear |
| Bailey Laurie | — | 6 | 20 | 85.7 | 76 | +56 | clear |
| Conor Stone | — | 6 | 36 | 108.4 | 90 | +54 | clear |
| Jack Martin | — | 14 | 47 | 133.8 | 101 | +54 | clear |
| Billy Cootee | — | 1 | 45 | 293.9 | 94 | +49 | clear |
| Callum Ah Chee | — | 11 | 39 | 84.7 | 88 | +49 | clear |
| Phoenix Gothard | — | 3 | 386 | 418.6 | 432 | +46 | clear |
| Jacob Hopper | — | 11 | 88 | 91.1 | 130 | +42 | clear |
| Sam Sturt | — | 8 | 15 | 55.8 | 56 | +41 | clear |
| Liam Stocker | — | 8 | 2 | 53.0 | 42 | +40 | clear |
| Jade Gresham | — | 11 | 14 | 54.3 | 53 | +39 | clear |
| Oscar Adams | — | 5 | 42 | 75.8 | 79 | +37 | clear |
| Brandon Starcevich | — | 9 | 7 | 54.3 | 44 | +37 | clear |
| Jake Melksham | — | 17 | 15 | 80.2 | 52 | +37 | clear |
| Charlie Spargo | — | 9 | 1 | 41.2 | 37 | +36 | clear |
| Laitham Vandermeer | — | 8 | 1 | 35.9 | 34 | +33 | clear |
| Judson Clarke | — | 5 | 64 | 105.4 | 95 | +31 | clear |
| Jamie Elliott | — | 15 | 6 | 32.6 | 34 | +28 | clear |
| Darcy Gardiner | — | 13 | 21 | 49.0 | 47 | +26 | clear |
| Alex Pearce | — | 13 | 14 | 35.9 | 40 | +26 | clear |
| Jed Bews | — | 15 | 1 | 25.8 | 27 | +26 | clear |
| Rhys Stanley | — | 18 | 13 | 30.5 | 39 | +26 | clear |
| Ben Long | — | 10 | 9 | 45.0 | 34 | +25 | clear |
| Nicholas Holman | — | 13 | 0 | 29.8 | 25 | +25 | clear |
| Liam Henry | — | 7 | 63 | 81.2 | 87 | +24 | clear |
| Joel Hamling | — | 15 | 14 | 31.7 | 38 | +24 | clear |
| Finlay Macrae | — | 6 | 92 | 93.1 | 115 | +23 | clear |
| Matt Guelfi | — | 9 | 5 | 25.8 | 27 | +22 | clear |
| Ben McKay | — | 11 | 26 | 50.4 | 48 | +22 | clear |
| Reef McInnes | — | 6 | 60 | 83.2 | 81 | +21 | clear |
| Ryan Gardner | — | 11 | 13 | 27.5 | 34 | +21 | clear |
| Oskar Baker | — | 9 | 13 | 30.1 | 33 | +20 | clear |
| Lachlan Weller | — | 12 | 67 | 64.4 | 87 | +20 | clear |
| Jacob Wehr | — | 6 | 4 | 48.5 | 22 | +18 | clear |
| Daniel Butler | — | 12 | 3 | 26.4 | 21 | +18 | clear |
| Oliver Henry | — | 6 | 79 | 97.7 | 96 | +17 | clear |
| Aidan Corr | — | 14 | 35 | 54.3 | 52 | +17 | clear |
| Noah Answerth | — | 8 | 18 | 28.1 | 33 | +15 | clear |
| Finn Maginness | — | 7 | 25 | 41.2 | 37 | +12 | clear |
| Jake Kolodjashnij | — | 13 | 27 | 33.2 | 39 | +12 | clear |
| Kaleb Smith | — | 4 | 117 | 125.2 | 128 | +11 | clear |
| Hunter Clark | — | 9 | 47 | 91.1 | 58 | +11 | clear |
| Jackson Archer | — | 5 | 69 | 70.9 | 79 | +10 | clear |
| Jamie Cripps | — | 16 | 26 | 40.6 | 36 | +10 | clear |
| Bailey Macdonald | — | 4 | 119 | 122.4 | 128 | +9 | clear |
| Harry Schoenberg | — | 7 | 52 | 46.2 | 59 | +7 | clear |
| Callum Coleman-Jones | — | 9 | 37 | 51.7 | 44 | +7 | clear |
| Liam Ryan | — | 9 | 25 | 43.9 | 31 | +6 | clear |
| Luke McDonald | — | 13 | 52 | 84.7 | 56 | +4 | clear |
| Nicholas Coffield | — | 9 | 53 | 84.7 | 56 | +3 | clear |
| Nathan Broad | — | 11 | 9 | 26.4 | 12 | +3 | clear |
| Harvey Harrison | — | 5 | 62 | 75.0 | 63 | +1 | clear |
| Mitch McGovern | — | 12 | 28 | 32.1 | 29 | +1 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT 40f43772
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Luke Jackson | RUC | 7799 | 6803 | 9064 | +1265 | +2261 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 8437 | +387 | +1435 |
| 3 | Harry Sheezel | MID | 8115 | 7151 | 8381 | +266 | +1230 |
| 4 | Tristan Xerri | RUC | 6649 | 5795 | 8035 | +1386 | +2240 |
| 5 | Max Holmes | MID | 6269 | 5386 | 7295 | +1026 | +1909 |
| 6 | Josh Treacy | KEY_FWD | — | — | 7065 | — | — |
| 7 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 7061 | +455 | +1267 |
| 8 | Zak Butters | MID | 6059 | 5174 | 6523 | +464 | +1349 |
| 9 | Bailey Smith | MID | 5605 | 4715 | 6168 | +563 | +1453 |
| 10 | Errol Gulden | MID | 5983 | 5256 | 6164 | +181 | +908 |
| 11 | Finn Callaghan | MID | 5442 | 4904 | 5779 | +337 | +875 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5654 | +467 | +1043 |
| 13 | Archie Roberts | MID | 4577 | 4668 | 5456 | +879 | +788 |
| 14 | Noah Anderson | MID | 4765 | 4091 | 5430 | +665 | +1339 |
| 15 | Sam Darcy | KEY_FWD | 4013 | 4144 | 5077 | +1064 | +933 |
| 16 | Tom Green | MID | 4391 | 4424 | 5069 | +678 | +645 |
| 17 | Brodie Grundy | RUC | 3959 | 3314 | 5049 | +1090 | +1735 |
| 18 | Will Ashcroft | MID | 5155 | 4768 | 4977 | -178 | +209 |
| 19 | Caleb Serong | MID | 4701 | 4170 | 4784 | +83 | +614 |
| 20 | Willem Duursma | MID | 4429 | 4110 | 4488 | +59 | +378 |
| 21 | Isaac Heeney | MID | 3981 | 3301 | 4464 | +483 | +1163 |
| 22 | Nick Blakey | GEN_DEF | 3598 | 3266 | 4433 | +835 | +1167 |
| 23 | Jason Horne-Francis | MID | 3996 | 3702 | 4343 | +347 | +641 |
| 24 | Jai Newcombe | MID | — | — | 4341 | — | — |
| 25 | Sam Lalor | MID | 3574 | 3337 | 4331 | +757 | +994 |
| 26 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 4318 | +500 | +616 |
| 27 | Matt Rowell | MID | 4185 | 3752 | 4201 | +16 | +449 |
| 28 | Marcus Bontempelli | MID | 3721 | 3084 | 4101 | +380 | +1017 |
| 29 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 4072 | +105 | +340 |
| 30 | Murphy Reid | GEN_FWD | 3953 | 3742 | 4057 | +104 | +315 |
| 31 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 4032 | +536 | +956 |
| 32 | Colby McKercher | MID | 3829 | 3627 | 4024 | +195 | +397 |
| 33 | Jordan Clark | GEN_DEF | 3307 | 3007 | 3936 | +629 | +929 |
| 34 | Callum Wilkie | KEY_DEF | — | — | 3918 | — | — |
| 35 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3916 | +457 | +986 |
| 36 | Jordan Dawson | MID | 3312 | 2758 | 3908 | +596 | +1150 |
| 37 | Timothy English | RUC | 3349 | 2916 | 3875 | +526 | +959 |
| 38 | Ryley Sanders | MID | 4129 | 3926 | 3860 | -269 | -66 |
| 39 | Nicholas Martin | MID | — | — | 3839 | — | — |
| 40 | Mac Andrew | KEY_DEF | 3691 | 3504 | 3823 | +132 | +319 |
| 41 | Josh Worrell | GEN_DEF | 3180 | 2937 | 3822 | +642 | +885 |
| 42 | Will Day | MID | 3108 | 2806 | 3773 | +665 | +967 |
| 43 | Jagga Smith | MID | 3192 | 2822 | 3696 | +504 | +874 |
| 44 | Ed Richards | MID | 3078 | 2625 | 3611 | +533 | +986 |
| 45 | Sam Berry | MID | 2648 | 2495 | 3596 | +948 | +1101 |
| 46 | Max Gawn | RUC | 2538 | 2112 | 3595 | +1057 | +1483 |
| 47 | Finn O'Sullivan | MID | 3643 | 3427 | 3568 | -75 | +141 |
| 48 | Harley Reid | MID | 3726 | 3549 | 3523 | -203 | -26 |
| 49 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3522 | +426 | +596 |
| 50 | Jack Sinclair | GEN_DEF | — | — | 3479 | — | — |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
