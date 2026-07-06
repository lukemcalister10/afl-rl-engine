# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 4226b61d — NOT AN ENDORSED STATE — head 4226b61d store e1b4d8bf
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 4226b61d — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 4226b61d store e1b4d8bf — suite 764a0d91 — 2026-07-06 ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=efea88e5 · PREVIOUS=c8051893 · CURRENT=4226b61d ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4110 vs 1984
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1355 vs 1485 (Ward=1650, ratio=0.821) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1543 vs 1650
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=2892 2025=3958 ratio=0.73 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=28 ev=3549 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1781 (floor 1600); Jake Bowey=2926 (floor 2100); Nick Blakey=3266 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=393 (n=13, pooled — thin slice) vs pick-matched MID kernel median=509 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2495 Tsatas=1149 ratio=2.17x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 1781 vs 1650
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1053 2025=1854 ratio=0.57 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 1526 vs 762; Cumming>Annable: 1918 vs 1502
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 716 vs 878; Smillie>Retschko: 974 vs 729
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3035 lineball=True; Levi Ashcroft=3028 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=1740 lineball=True; Zach Reid=1609 lineball=True; Jase Burgoyne=2140 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     cross-cohort AVERAGE peak N=4 AVG(peak)=143 (need peak in yrs 4-6, >100; pre-peak dips of the AVERAGE <5% tolerated, path_ok=True; per-cohort UNGATED, table printed every run — Luke redefinition 02/07 D5); avg row: 1:100 2:122 3:133 4:143 5:141 6:133 7:116; cohorts n=17; matrix=s4_matrix_baked_efea88e5.json
B2        PASS    | PASS    | PASS     median |IS-WF| leakage=0.0 %-pts (tol 0.5, SET 02/07/2026 — N=5 spread 0.00); GOOD>BUST separation: GEN_DEF 38/1, GEN_FWD 36/1, KEY_DEF 46/1, KEY_FWD 58/0, MID 47/0
B3        PASS    | PENDING | PASS     book stable-key seal MATCHES baseline: current=5799a9ceae5ca3ef.. (2649 players) vs baseline=5799a9ceae5ca3ef.. (2649 players, sealed head efea88e5); matrix=s4_matrix_baked_efea88e5.json [raw-file sha is id(p)-keyed / non-deterministic by design]  <- MOVED
B4        PASS    | FAIL    | PASS     regenerated rl_app_data.json md5=417e419d vs shipped 417e419d (byte-agree gate; export exit=0)  <- MOVED
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 52 saves, aggregate lift +1296; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1260, 1530, 1825, 2474, 3072, 3161, 3215, 3268, 3285, 3295, 3348, 3413, 3495, 3533, 3562]; dips(more games worth less)=none; 0->6 rise T=+1955; 0->6 steps>50%T=none; rise by 3g=+1214 (need >=489) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | —       | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)  <- MOVED
D14b      PASS    | —       | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)  <- MOVED
D14c      PASS    | —       | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)  <- MOVED
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1  (143s)
```

## Supporting detail

B1 per-cohort curves (UNGATED — printed every gates-board run, Luke eyeball channel):
| cohort | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 128 | 156 | 159 | 170 | 151 | 133 |
| 2005 | 4 | 100 | 130 | 132 | 177 | 165 | 157 | 135 |
| 2006 | 4 | 100 | 123 | 138 | 152 | 150 | 148 | 128 |
| 2007 | 5 | 100 | 124 | 119 | 126 | 148 | 143 | 120 |
| 2008 | 4 | 100 | 126 | 167 | 181 | 162 | 145 | 126 |
| 2009 | 2 | 100 | 119 | 107 | 107 | 108 | 97 | 84 |
| 2010 | 4 | 100 | 130 | 142 | 160 | 153 | 135 | 113 |
| 2011 | 4 | 100 | 127 | 148 | 169 | 166 | 156 | 128 |
| 2012 | 4 | 100 | 112 | 124 | 126 | 122 | 116 | 97 |
| 2013 | 5 | 100 | 132 | 149 | 177 | 180 | 157 | 120 |
| 2014 | 4 | 100 | 125 | 141 | 151 | 137 | 134 | 131 |
| 2015 | 4 | 100 | 116 | 120 | 123 | 119 | 119 | 112 |
| 2016 | 4 | 100 | 124 | 139 | 160 | 148 | 151 | 128 |
| 2017 | 3 | 100 | 113 | 119 | 107 | 100 | 101 | 94 |
| 2018 | 4 | 100 | 123 | 121 | 130 | 125 | 117 | 106 |
| 2019 | 5 | 100 | 109 | 119 | 128 | 136 | 123 | 106 |
| 2020 | 3 | 100 | 111 | 112 | 102 | 105 | 104 | — |
| **AVG (the gated row)** | **4** | **100** | **122** | **133** | **143** | **141** | **133** | **116** |

B5 FLOOR-SAVES table (n=52, aggregate lift=+1296 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | Carlton | 9 | 13 | 112.5 | 112 | +99 | clear |
| Stephen Coniglio | GWS | 15 | 23 | 112.5 | 112 | +89 | clear |
| Chayce Jones | Adelaide | 8 | 9 | 80.2 | 83 | +74 | clear |
| Steele Sidebottom | Collingwood | 18 | 3 | 69.0 | 74 | +71 | clear |
| Jaeger O'Meara | Gold Coast | 15 | 61 | 150.0 | 125 | +64 | clear |
| Oliver Wiltshire | Geelong | 3 | 13 | 86.2 | 75 | +62 | clear |
| Jacob Hopper | GWS | 11 | 41 | 89.8 | 91 | +50 | clear |
| Luke Pedlar | Adelaide | 6 | 66 | 124.3 | 110 | +44 | clear |
| Conor Stone | GWS | 6 | 27 | 96.7 | 70 | +43 | clear |
| Billy Cootee | Sydney | 1 | 29 | 225.0 | 70 | +41 | clear |
| Bailey Laurie | Melbourne | 6 | 20 | 55.5 | 58 | +38 | clear |
| Phoenix Gothard | GWS | 3 | 295 | 355.6 | 330 | +35 | clear |
| Liam Stocker | Carlton | 8 | 2 | 39.8 | 33 | +31 | clear |
| Brandon Starcevich | Brisbane | 9 | 6 | 43.0 | 35 | +29 | clear |
| Jake Melksham | Essendon | 17 | 15 | 74.6 | 44 | +29 | clear |
| Charlie Spargo | Melbourne | 9 | 1 | 30.4 | 29 | +28 | clear |
| Callum Ah Chee | Gold Coast | 11 | 38 | 85.3 | 65 | +27 | clear |
| Jade Gresham | St Kilda | 11 | 13 | 43.0 | 40 | +27 | clear |
| Jack Martin | Gold Coast | 14 | 46 | 112.5 | 73 | +27 | clear |
| Nicholas Coffield | St Kilda | 9 | 16 | 85.3 | 42 | +26 | clear |
| Laitham Vandermeer | Western Bulldogs | 8 | 2 | 27.9 | 26 | +24 | clear |
| Nicholas Holman | Carlton | 13 | 0 | 20.0 | 22 | +22 | clear |
| Xavier O'Halloran | GWS | 8 | 13 | 32.3 | 33 | +20 | clear |
| Daniel Butler | Richmond | 12 | 0 | 15.4 | 19 | +19 | clear |
| Sam Butler | Hawthorn | 5 | 66 | 80.2 | 84 | +18 | clear |
| Oliver Henry | Collingwood | 6 | 55 | 77.3 | 73 | +18 | clear |
| Jed Bews | Geelong | 15 | 1 | 15.4 | 19 | +18 | clear |
| Rhys Stanley | St Kilda | 18 | 12 | 21.2 | 30 | +18 | clear |
| Harvey Gallagher | Western Bulldogs | 4 | 91 | 112.3 | 108 | +17 | clear |
| Ben Long | St Kilda | 10 | 9 | 30.7 | 26 | +17 | clear |
| Finlay Macrae | Collingwood | 6 | 71 | 66.1 | 86 | +15 | clear |
| Matt Guelfi | Essendon | 9 | 5 | 15.4 | 19 | +14 | clear |
| Alex Pearce | Fremantle | 13 | 14 | 27.9 | 28 | +14 | clear |
| Jacob Wehr | GWS | 6 | 3 | 27.7 | 16 | +13 | clear |
| Ryan Gardner | Geelong | 11 | 9 | 15.4 | 22 | +13 | clear |
| Corey Durdin | Carlton | 6 | 34 | 48.1 | 46 | +12 | clear |
| Mitch McGovern | Adelaide | 12 | 9 | 24.2 | 21 | +12 | clear |
| Darcy Gardiner | Brisbane | 13 | 21 | 32.3 | 33 | +12 | clear |
| Joel Hamling | Geelong | 15 | 14 | 23.4 | 26 | +12 | clear |
| Ben McKay | North Melbourne | 11 | 27 | 34.2 | 34 | +7 | clear |
| Finn Maginness | Hawthorn | 7 | 23 | 30.4 | 29 | +6 | clear |
| Oskar Baker | Melbourne | 9 | 19 | 20.6 | 25 | +6 | clear |
| Liam Henry | Fremantle | 7 | 59 | 80.2 | 64 | +5 | clear |
| Tom Cole | West Coast | 11 | 20 | 28.2 | 25 | +5 | clear |
| Harry Schoenberg | Adelaide | 7 | 40 | 30.8 | 44 | +4 | clear |
| Bailey Scott | North Melbourne | 8 | 22 | 20.0 | 26 | +4 | clear |
| Jamie Cripps | St Kilda | 16 | 24 | 30.3 | 28 | +4 | clear |
| Sam Sturt | Fremantle | 8 | 40 | 46.5 | 43 | +3 | clear |
| Noah Answerth | Brisbane | 8 | 20 | 16.8 | 23 | +3 | clear |
| Aidan Corr | GWS | 14 | 33 | 43.0 | 36 | +3 | clear |
| Reef McInnes | Collingwood | 6 | 56 | 55.4 | 58 | +2 | LTI (2025 AND again 2026) |
| Harry Morrison | Hawthorn | 10 | 20 | 15.4 | 22 | +2 | clear |

## Board top-50 (A4 context) — CONTROL efea88e5 · PREVIOUS c8051893 · CURRENT 4226b61d
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 7151 | 7207 | 7151 | +0 | -56 |
| 2 | Nick Daicos | MID | 7002 | 7069 | 7002 | +0 | -67 |
| 3 | Luke Jackson | RUC | 6803 | 6986 | 6803 | +0 | -183 |
| 4 | Tristan Xerri | RUC | 5795 | 5755 | 5795 | +0 | +40 |
| 5 | Nasiah Wanganeen-Milera | MID | 5794 | 5961 | 5794 | +0 | -167 |
| 6 | Max Holmes | MID | 5386 | 5499 | 5386 | +0 | -113 |
| 7 | Josh Treacy | KEY_FWD | — | — | 5312 | — | — |
| 8 | Errol Gulden | MID | 5256 | 5299 | 5256 | +0 | -43 |
| 9 | Zak Butters | MID | 5174 | 5225 | 5174 | +0 | -51 |
| 10 | Finn Callaghan | MID | 4904 | 4952 | 4904 | +0 | -48 |
| 11 | Will Ashcroft | MID | 4768 | 4823 | 4768 | +0 | -55 |
| 12 | Bailey Smith | MID | 4715 | 4773 | 4715 | +0 | -58 |
| 13 | Archie Roberts | GEN_DEF | 4668 | 4597 | 4668 | +0 | +71 |
| 14 | Lachlan Ash | GEN_DEF | 4611 | 4663 | 4611 | +0 | -52 |
| 15 | Tom Green | MID | 4424 | 4472 | 4424 | +0 | -48 |
| 16 | Caleb Serong | MID | 4170 | 4202 | 4170 | +0 | -32 |
| 17 | Sam Darcy | KEY_FWD | 4144 | 3978 | 4144 | +0 | +166 |
| 18 | Willem Duursma | MID | 4110 | 4160 | 4110 | +0 | -50 |
| 19 | Noah Anderson | MID | 4091 | 4131 | 4091 | +0 | -40 |
| 20 | Jai Newcombe | MID | — | — | 3974 | — | — |
| 21 | Ryley Sanders | MID | 3926 | 4212 | 3926 | +0 | -286 |
| 22 | Matt Rowell | MID | 3752 | 3779 | 3752 | +0 | -27 |
| 23 | Murphy Reid | GEN_FWD | 3742 | 3843 | 3742 | +0 | -101 |
| 24 | Darcy Wilmot | GEN_DEF | 3732 | 3774 | 3732 | +0 | -42 |
| 25 | Jason Horne-Francis | MID | 3702 | 4199 | 3702 | +0 | -497 |
| 26 | Riley Thilthorpe | KEY_FWD | 3702 | 3555 | 3702 | +0 | +147 |
| 27 | Colby McKercher | MID | 3627 | 3814 | 3627 | +0 | -187 |
| 28 | Harley Reid | MID | 3549 | 3565 | 3549 | +0 | -16 |
| 29 | Nick Watson | GEN_FWD | 3538 | 3579 | 3538 | +0 | -41 |
| 30 | Mac Andrew | KEY_DEF | 3504 | 3530 | 3504 | +0 | -26 |
| 31 | Finn O'Sullivan | MID | 3427 | 3495 | 3427 | +0 | -68 |
| 32 | Sam Lalor | MID | 3337 | 3703 | 3337 | +0 | -366 |
| 33 | Brodie Grundy | RUC | 3314 | 3344 | 3314 | +0 | -30 |
| 34 | Isaac Heeney | MID | 3301 | 3327 | 3301 | +0 | -26 |
| 35 | Bodhi Uwland | GEN_DEF | — | — | 3288 | — | — |
| 36 | Nick Blakey | GEN_DEF | 3266 | 3287 | 3266 | +0 | -21 |
| 37 | Nicholas Martin | MID | — | — | 3116 | — | — |
| 38 | Marcus Bontempelli | MID | 3084 | 3109 | 3084 | +0 | -25 |
| 39 | Kysaiah Pickett | GEN_FWD | 3076 | 3031 | 3076 | +0 | +45 |
| 40 | George Wardlaw | MID | 3035 | 3033 | 3035 | +0 | +2 |
| 41 | Levi Ashcroft | MID | 3028 | 3270 | 3028 | +0 | -242 |
| 42 | Logan Morris | KEY_FWD | 3018 | 2843 | 3018 | +0 | +175 |
| 43 | Jordan Clark | GEN_DEF | 3007 | 3031 | 3007 | +0 | -24 |
| 44 | Aaron Cadman | KEY_FWD | 2970 | 2818 | 2970 | +0 | +152 |
| 45 | Josh Worrell | GEN_DEF | 2937 | 3236 | 2937 | +0 | -299 |
| 46 | Luke Davies-Uniacke | MID | 2930 | 2952 | 2930 | +0 | -22 |
| 47 | Jake Bowey | GEN_DEF | 2926 | 2969 | 2926 | +0 | -43 |
| 48 | Timothy English | RUC | 2916 | 2907 | 2916 | +0 | +9 |
| 49 | Connor Rozee | MID | 2892 | 2917 | 2892 | +0 | -25 |
| 50 | Callum Wilkie | KEY_DEF | — | — | 2885 | — | — |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
