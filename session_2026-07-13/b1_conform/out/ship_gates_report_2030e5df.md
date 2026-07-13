# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 2030e5df — NOT AN ENDORSED STATE — head 2030e5df store 340a7a32 config 69ead79b944d
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 2030e5df — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 2030e5df store 340a7a32 config 69ead79b944d — suite 764a0d91 — 2026-07-13 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash 69ead79b944d291b — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=2030e5df ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4566 vs 2833
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1598 vs 1562 (Ward=1735, ratio=0.921) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1661 vs 1735
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=2396 2025=4464 ratio=0.54 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=30 ev=3782 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1941 (floor 1600); Jake Bowey=3388 (floor 2100); Nick Blakey=3504 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=484 (n=12, pooled — thin slice) vs pick-matched MID kernel median=639 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2874 Tsatas=1243 ratio=2.31x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 1941 vs 1735
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1249 2025=2257 ratio=0.55 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 1822 vs 1029; Cumming>Annable: 2258 vs 2090
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 824 vs 1041; Smillie>Retschko: 1349 vs 873
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3221 lineball=True; Levi Ashcroft=3259 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=1798 lineball=True; Zach Reid=1719 lineball=True; Jase Burgoyne=2098 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine 2030e5df store 340a7a32 config 69ead79b944d): y1=69840.0 y2=79298.2 y3=82016.2 y4=88002.4 y5=86652.9 y6=80460.5 y7=71285.8; den=min(y1,y2)=y1=69840.0; ratios y4=1.2601(above-guide) y5=1.2407(in-guide) y6=1.1521(below-guide); hard<=1.30 -> PASS x3; guide 1.20-1.25 ADVISORY (margin reported, never gates)
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:4.54, KEY_DEF|GOOD|T3:3.19, GEN_DEF|GOOD|T5:2.97, KEY_DEF|GOOD|T2:2.91; GOOD>BUST sep GEN_DEF 43.0/0.9, GEN_FWD 39.8/0.6, KEY_DEF 50.6/1.1, KEY_FWD 60.6/0.6, MID 50.6/0.5, RUC 26.1/0.3 [cert engine 2030e5df store 340a7a32 config 69ead79b]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine 2030e5df store 340a7a32 config 69ead79b944d): MATCHES the sealed baseline. current=d371a27c787a34c9.. (2649 players) vs baseline=d371a27c787a34c9.. (2649 players, sealed head 2030e5df) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=3dc19fbb vs shipped 3dc19fbb (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 63 saves, aggregate lift +2231; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1353, 1643, 1956, 2649, 3289, 3389, 3447, 3505, 3525, 3539, 3601, 3674, 3765, 3806, 3836]; dips(more games worth less)=none; 0->6 rise T=+2094; 0->6 steps>50%T=none; rise by 3g=+1296 (need >=524) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1  (531s)
```

## Supporting detail

B1 — THE GATE is the July-8 raw-class-sum construction (bold row); the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr4, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 124 | 161 | 162 | 171 | 146 | 133 |
| 2005 | 4 | 100 | 143 | 134 | 176 | 171 | 161 | 138 |
| 2006 | 4 | 100 | 117 | 121 | 133 | 131 | 129 | 112 |
| 2007 | 5 | 100 | 114 | 105 | 108 | 134 | 123 | 103 |
| 2008 | 4 | 100 | 118 | 145 | 159 | 140 | 122 | 108 |
| 2009 | 2 | 100 | 111 | 94 | 97 | 96 | 85 | 73 |
| 2010 | 4 | 100 | 118 | 122 | 139 | 135 | 114 | 93 |
| 2011 | 4 | 100 | 116 | 127 | 145 | 142 | 133 | 110 |
| 2012 | 3 | 100 | 101 | 108 | 107 | 102 | 98 | 82 |
| 2013 | 5 | 100 | 121 | 131 | 152 | 153 | 136 | 103 |
| 2014 | 4 | 100 | 111 | 118 | 124 | 111 | 111 | 107 |
| 2015 | 2 | 100 | 106 | 104 | 105 | 102 | 102 | 98 |
| 2016 | 4 | 100 | 114 | 121 | 139 | 126 | 126 | 107 |
| 2017 | 3 | 100 | 107 | 108 | 97 | 91 | 90 | 83 |
| 2018 | 2 | 100 | 114 | 106 | 114 | 109 | 99 | 92 |
| 2019 | 5 | 100 | 100 | 104 | 110 | 119 | 108 | 91 |
| 2020 | 2 | 100 | 101 | 98 | 90 | 95 | 91 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _4_ | _100_ | _114_ | _118_ | _127_ | _125_ | _116_ | _102_ |
| **July-8 raw-sum AVG (THE GATED ROW)** | **—** | **69840** | **79298** | **82016** | **88002** | **86653** | **80460** | **71286** |

B5 FLOOR-SAVES table (n=63, aggregate lift=+2231 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | — | 9 | 14 | 140.8 | 169 | +155 | clear |
| Stephen Coniglio | — | 15 | 23 | 140.8 | 169 | +146 | clear |
| Jaeger O'Meara | — | 15 | 63 | 150.0 | 192 | +129 | clear |
| Chayce Jones | — | 8 | 10 | 85.4 | 115 | +105 | clear |
| Steele Sidebottom | — | 18 | 3 | 81.2 | 103 | +100 | clear |
| Oliver Wiltshire | — | 3 | 14 | 98.3 | 109 | +95 | clear |
| Jacob Hopper | — | 11 | 43 | 87.0 | 126 | +83 | clear |
| Luke Pedlar | — | 6 | 73 | 146.2 | 147 | +74 | clear |
| Bailey Laurie | — | 6 | 22 | 87.8 | 77 | +55 | clear |
| Billy Cootee | — | 1 | 39 | 305.6 | 92 | +53 | clear |
| Jack Martin | — | 14 | 48 | 140.8 | 101 | +53 | clear |
| Conor Stone | — | 6 | 36 | 114.1 | 88 | +52 | clear |
| Callum Ah Chee | — | 11 | 40 | 87.0 | 89 | +49 | clear |
| Phoenix Gothard | — | 3 | 390 | 443.2 | 437 | +47 | clear |
| Liam Stocker | — | 8 | 2 | 58.6 | 43 | +41 | clear |
| Jade Gresham | — | 11 | 14 | 60.1 | 54 | +40 | clear |
| Nicholas Coffield | — | 9 | 17 | 87.0 | 55 | +38 | clear |
| Jake Melksham | — | 17 | 15 | 82.9 | 53 | +38 | clear |
| Finlay Macrae | — | 6 | 77 | 101.3 | 114 | +37 | clear |
| Brandon Starcevich | — | 9 | 7 | 60.1 | 44 | +37 | clear |
| Sam Butler | — | 5 | 75 | 126.8 | 111 | +36 | clear |
| Oliver Henry | — | 6 | 61 | 108.2 | 97 | +36 | clear |
| Charlie Spargo | — | 9 | 1 | 42.2 | 37 | +36 | clear |
| Laitham Vandermeer | — | 8 | 2 | 37.2 | 34 | +32 | clear |
| Xavier O'Halloran | — | 8 | 13 | 51.0 | 44 | +31 | clear |
| Harvey Gallagher | — | 4 | 113 | 153.3 | 142 | +29 | clear |
| Jamie Elliott | — | 15 | 6 | 34.0 | 34 | +28 | clear |
| Jed Bews | — | 15 | 1 | 17.2 | 28 | +27 | clear |
| Ryan Gardner | — | 11 | 9 | 18.3 | 35 | +26 | clear |
| Darcy Gardiner | — | 13 | 22 | 51.0 | 48 | +26 | clear |
| Rhys Stanley | — | 18 | 12 | 27.4 | 38 | +26 | clear |
| Ben Long | — | 10 | 9 | 45.9 | 34 | +25 | clear |
| Alex Pearce | — | 13 | 15 | 37.2 | 40 | +25 | clear |
| Nicholas Holman | — | 13 | 0 | 24.8 | 25 | +25 | clear |
| Joel Hamling | — | 15 | 14 | 31.5 | 38 | +24 | clear |
| Matt Guelfi | — | 9 | 5 | 17.2 | 27 | +22 | clear |
| Daniel Butler | — | 12 | 0 | 17.2 | 22 | +22 | clear |
| Corey Durdin | — | 6 | 35 | 65.7 | 56 | +21 | clear |
| Ben McKay | — | 11 | 28 | 53.7 | 49 | +21 | clear |
| Liam Henry | — | 7 | 67 | 85.4 | 87 | +20 | clear |
| Jacob Wehr | — | 6 | 3 | 31.6 | 22 | +19 | clear |
| Mitch McGovern | — | 12 | 9 | 32.8 | 28 | +19 | clear |
| Reef McInnes | — | 6 | 64 | 84.7 | 82 | +18 | clear |
| Aidan Corr | — | 14 | 35 | 60.1 | 53 | +18 | clear |
| Lachlan Weller | — | 12 | 69 | 67.8 | 85 | +16 | clear |
| Harry Schoenberg | — | 7 | 43 | 47.1 | 58 | +15 | clear |
| Sam Sturt | — | 8 | 43 | 60.8 | 57 | +14 | clear |
| Oskar Baker | — | 9 | 19 | 26.0 | 33 | +14 | clear |
| Finn Maginness | — | 7 | 24 | 42.2 | 37 | +13 | clear |
| Noah Answerth | — | 8 | 20 | 19.6 | 33 | +13 | clear |
| Bailey Scott | — | 8 | 23 | 24.8 | 35 | +12 | clear |
| Tom Cole | — | 11 | 20 | 37.4 | 32 | +12 | clear |
| Jamie Cripps | — | 16 | 25 | 41.1 | 37 | +12 | clear |
| Jake Kolodjashnij | — | 13 | 28 | 35.0 | 39 | +11 | clear |
| Kaleb Smith | — | 4 | 119 | 104.0 | 129 | +10 | clear |
| Bailey Macdonald | — | 4 | 119 | 94.9 | 129 | +10 | clear |
| Harry Morrison | — | 10 | 21 | 17.2 | 30 | +9 | clear |
| James Jordon | — | 8 | 37 | 38.5 | 45 | +8 | clear |
| Judson Clarke | — | 5 | 88 | 106.9 | 95 | +7 | clear |
| James Tunstill | — | 5 | 95 | 91.0 | 100 | +5 | clear |
| Hunter Clark | — | 9 | 52 | 87.0 | 57 | +5 | clear |
| Liam Ryan | — | 9 | 28 | 45.0 | 31 | +3 | clear |
| Nathan Broad | — | 11 | 9 | 17.2 | 12 | +3 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT 2030e5df
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 8115 | 7151 | 8204 | +89 | +1053 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 8069 | +19 | +1067 |
| 3 | Luke Jackson | RUC | 7799 | 6803 | 7851 | +52 | +1048 |
| 4 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 6681 | +75 | +887 |
| 5 | Tristan Xerri | RUC | 6649 | 5795 | 6579 | -70 | +784 |
| 6 | Josh Treacy | KEY_FWD | — | — | 6550 | — | — |
| 7 | Max Holmes | MID | 6269 | 5386 | 6472 | +203 | +1086 |
| 8 | Errol Gulden | MID | 5983 | 5256 | 6044 | +61 | +788 |
| 9 | Zak Butters | MID | 6059 | 5174 | 5986 | -73 | +812 |
| 10 | Finn Callaghan | MID | 5442 | 4904 | 5837 | +395 | +933 |
| 11 | Bailey Smith | MID | 5605 | 4715 | 5518 | -87 | +803 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5307 | +120 | +696 |
| 13 | Will Ashcroft | MID | 5155 | 4768 | 5199 | +44 | +431 |
| 14 | Noah Anderson | MID | 4765 | 4091 | 4762 | -3 | +671 |
| 15 | Caleb Serong | MID | 4701 | 4170 | 4728 | +27 | +558 |
| 16 | Archie Roberts | GEN_DEF | 4577 | 4668 | 4616 | +39 | -52 |
| 17 | Willem Duursma | MID | 4429 | 4110 | 4566 | +137 | +456 |
| 18 | Jai Newcombe | MID | — | — | 4464 | — | — |
| 19 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 4459 | +492 | +727 |
| 20 | Tom Green | MID | 4391 | 4424 | 4416 | +25 | -8 |
| 21 | Matt Rowell | MID | 4185 | 3752 | 4188 | +3 | +436 |
| 22 | Jason Horne-Francis | MID | 3996 | 3702 | 4172 | +176 | +470 |
| 23 | Ryley Sanders | MID | 4129 | 3926 | 4168 | +39 | +242 |
| 24 | Sam Darcy | KEY_FWD | 4013 | 4144 | 4067 | +54 | -77 |
| 25 | Murphy Reid | GEN_FWD | 3953 | 3742 | 3993 | +40 | +251 |
| 26 | Isaac Heeney | MID | 3981 | 3301 | 3922 | -59 | +621 |
| 27 | Brodie Grundy | RUC | 3959 | 3314 | 3913 | -46 | +599 |
| 28 | Colby McKercher | MID | 3829 | 3627 | 3864 | +35 | +237 |
| 29 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 3849 | +31 | +147 |
| 30 | Harley Reid | MID | 3726 | 3549 | 3782 | +56 | +233 |
| 31 | Nick Watson | GEN_FWD | 3720 | 3538 | 3769 | +49 | +231 |
| 32 | Mac Andrew | KEY_DEF | 3691 | 3504 | 3731 | +40 | +227 |
| 33 | Finn O'Sullivan | MID | 3643 | 3427 | 3712 | +69 | +285 |
| 34 | Sam Lalor | MID | 3574 | 3337 | 3665 | +91 | +328 |
| 35 | Marcus Bontempelli | MID | 3721 | 3084 | 3664 | -57 | +580 |
| 36 | Nick Blakey | GEN_DEF | 3598 | 3266 | 3504 | -94 | +238 |
| 37 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 3503 | +7 | +427 |
| 38 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3427 | -32 | +497 |
| 39 | Jake Bowey | GEN_DEF | 3096 | 2926 | 3388 | +292 | +462 |
| 40 | Callum Wilkie | KEY_DEF | — | — | 3315 | — | — |
| 41 | Jordan Clark | GEN_DEF | 3307 | 3007 | 3300 | -7 | +293 |
| 42 | Timothy English | RUC | 3349 | 2916 | 3296 | -53 | +380 |
| 43 | Levi Ashcroft | MID | 3193 | 3028 | 3259 | +66 | +231 |
| 44 | Jagga Smith | MID | 3192 | 2822 | 3252 | +60 | +430 |
| 45 | Jordan Dawson | MID | 3312 | 2758 | 3238 | -74 | +480 |
| 46 | Logan Morris | KEY_FWD | 3171 | 3018 | 3235 | +64 | +217 |
| 47 | Bodhi Uwland | GEN_DEF | — | — | 3233 | — | — |
| 48 | George Wardlaw | MID | 3206 | 3035 | 3221 | +15 | +186 |
| 49 | Josh Worrell | GEN_DEF | 3180 | 2937 | 3168 | -12 | +231 |
| 50 | Jack Sinclair | GEN_DEF | — | — | 3164 | — | — |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
