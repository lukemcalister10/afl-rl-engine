# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 7a07e369 — NOT AN ENDORSED STATE — head 7a07e369 store a2fbc9a0 config 69ead79b944d
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 7a07e369 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 7a07e369 store a2fbc9a0 config 69ead79b944d — suite 764a0d91 — 2026-07-10 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash 69ead79b944d291b — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=efea88e5 · PREVIOUS=c8051893 · CURRENT=7a07e369 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4225 vs 2119
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1355 vs 1485 (Ward=1650, ratio=0.821) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1543 vs 1650
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=2271 2025=4235 ratio=0.54 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=30 ev=3549 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1772 (floor 1600); Jake Bowey=2932 (floor 2100); Nick Blakey=3431 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=393 (n=13, pooled — thin slice) vs pick-matched MID kernel median=553 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2520 Tsatas=1185 ratio=2.13x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 1772 vs 1650
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1198 2025=2161 ratio=0.55 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 1664 vs 874; Cumming>Annable: 2115 vs 1948
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 758 vs 979; Smillie>Retschko: 1250 vs 809
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3035 lineball=True; Levi Ashcroft=3032 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=1713 lineball=True; Zach Reid=1640 lineball=True; Jase Burgoyne=1975 lineball=True
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     CANDIDATE (regenerated this run — engine 7a07e369 store a2fbc9a0 config 69ead79b944d): cross-cohort AVERAGE peak N=4 AVG(peak)=130 (need peak in yrs 4-6, >100; pre-peak dips of the AVERAGE <5% tolerated, path_ok=True; per-cohort UNGATED, table printed — Luke D5); avg row: 1:100 2:116 3:121 4:130 5:128 6:120 7:107; cohorts n=17 | v2.5 comparator avg row [NAMED, NOT certified]: 1:100 2:122 3:133 4:143 5:141 6:133 7:116
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:6.35, RUC|GOOD|T3:3.07, GEN_DEF|GOOD|T5:2.38, GEN_FWD|GOOD|T5:2.37; GOOD>BUST sep GEN_DEF 41.5/0.8, GEN_FWD 39.6/0.6, KEY_DEF 49.4/1.1, KEY_FWD 61.2/0.6, MID 49.6/0.5, RUC 22.1/0.4 [cert engine 7a07e369 store a2fbc9a0 config 69ead79b]
B3        PASS    | PENDING | PASS     CANDIDATE book stable seal (regenerated this run — engine 7a07e369 store a2fbc9a0 config 69ead79b944d): MATCHES the sealed baseline. current=2a74c731e9ce603e.. (2649 players) vs baseline=2a74c731e9ce603e.. (2649 players, sealed head 7a07e369) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]  <- MOVED
B4        PASS    | FAIL    | PASS     regenerated rl_app_data.json md5=e2c9bc51 vs shipped e2c9bc51 (byte-agree gate; export exit=0)  <- MOVED
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 61 saves, aggregate lift +1952; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1260, 1530, 1825, 2474, 3072, 3161, 3215, 3268, 3285, 3295, 3348, 3413, 3495, 3533, 3562]; dips(more games worth less)=none; 0->6 rise T=+1955; 0->6 steps>50%T=none; rise by 3g=+1214 (need >=489) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | —       | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)  <- MOVED
D14b      PASS    | —       | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)  <- MOVED
D14c      PASS    | —       | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)  <- MOVED
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1  (591s)
```

## Supporting detail

B1 per-cohort curves — CANDIDATE, regenerated this run (UNGATED — Luke eyeball channel):
| cohort | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 127 | 164 | 164 | 175 | 154 | 140 |
| 2005 | 4 | 100 | 145 | 137 | 181 | 171 | 165 | 144 |
| 2006 | 4 | 100 | 119 | 124 | 135 | 135 | 133 | 116 |
| 2007 | 5 | 100 | 116 | 107 | 111 | 133 | 127 | 107 |
| 2008 | 4 | 100 | 122 | 153 | 165 | 150 | 134 | 118 |
| 2009 | 2 | 100 | 112 | 97 | 97 | 98 | 86 | 75 |
| 2010 | 4 | 100 | 120 | 126 | 142 | 137 | 119 | 99 |
| 2011 | 4 | 100 | 118 | 130 | 148 | 146 | 139 | 115 |
| 2012 | 3 | 100 | 103 | 111 | 110 | 106 | 101 | 85 |
| 2013 | 5 | 100 | 122 | 134 | 155 | 158 | 138 | 108 |
| 2014 | 4 | 100 | 114 | 122 | 128 | 116 | 115 | 112 |
| 2015 | 4 | 100 | 107 | 106 | 107 | 105 | 105 | 101 |
| 2016 | 4 | 100 | 116 | 124 | 141 | 131 | 131 | 114 |
| 2017 | 3 | 100 | 108 | 110 | 98 | 92 | 92 | 86 |
| 2018 | 2 | 100 | 116 | 108 | 115 | 111 | 103 | 96 |
| 2019 | 5 | 100 | 101 | 106 | 113 | 122 | 111 | 94 |
| 2020 | 2 | 100 | 103 | 100 | 91 | 96 | 93 | — |
| **AVG (the gated row — CANDIDATE)** | **4** | **100** | **116** | **121** | **130** | **128** | **120** | **107** |

B5 FLOOR-SAVES table (n=61, aggregate lift=+1952 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | Carlton | 9 | 13 | 112.5 | 157 | +144 | clear |
| Stephen Coniglio | GWS | 15 | 23 | 112.5 | 157 | +134 | clear |
| Jaeger O'Meara | Gold Coast | 15 | 61 | 150.0 | 177 | +116 | clear |
| Chayce Jones | Adelaide | 8 | 9 | 80.2 | 106 | +97 | clear |
| Steele Sidebottom | Collingwood | 18 | 3 | 69.0 | 95 | +92 | clear |
| Oliver Wiltshire | Geelong | 3 | 13 | 86.2 | 93 | +80 | clear |
| Jacob Hopper | GWS | 11 | 41 | 89.8 | 117 | +76 | clear |
| Luke Pedlar | Adelaide | 6 | 66 | 124.3 | 134 | +68 | clear |
| Conor Stone | GWS | 6 | 28 | 96.7 | 80 | +52 | clear |
| Bailey Laurie | Melbourne | 6 | 20 | 55.5 | 70 | +50 | clear |
| Jack Martin | Gold Coast | 14 | 46 | 112.5 | 93 | +47 | clear |
| Callum Ah Chee | Gold Coast | 11 | 38 | 85.3 | 82 | +44 | clear |
| Billy Cootee | Sydney | 1 | 37 | 225.0 | 79 | +42 | clear |
| Phoenix Gothard | GWS | 3 | 357 | 355.6 | 399 | +42 | clear |
| Liam Stocker | Carlton | 8 | 2 | 39.8 | 38 | +36 | clear |
| Jade Gresham | St Kilda | 11 | 13 | 43.0 | 49 | +36 | clear |
| Sam Butler | Hawthorn | 5 | 66 | 80.2 | 101 | +35 | clear |
| Oliver Henry | Collingwood | 6 | 55 | 77.3 | 88 | +33 | clear |
| Brandon Starcevich | Brisbane | 9 | 6 | 43.0 | 39 | +33 | clear |
| Charlie Spargo | Melbourne | 9 | 1 | 30.4 | 34 | +33 | clear |
| Nicholas Coffield | St Kilda | 9 | 16 | 85.3 | 48 | +32 | clear |
| Jake Melksham | Essendon | 17 | 15 | 74.6 | 47 | +32 | clear |
| Harvey Gallagher | Western Bulldogs | 4 | 100 | 112.3 | 128 | +28 | clear |
| Laitham Vandermeer | Western Bulldogs | 8 | 2 | 27.9 | 30 | +28 | clear |
| Finlay Macrae | Collingwood | 6 | 77 | 66.1 | 104 | +27 | clear |
| Xavier O'Halloran | GWS | 8 | 13 | 32.3 | 40 | +27 | clear |
| Jamie Elliott | — | 15 | 5 | 25.0 | 30 | +25 | clear |
| Ryan Gardner | Geelong | 11 | 9 | 15.4 | 32 | +23 | clear |
| Darcy Gardiner | Brisbane | 13 | 21 | 32.3 | 44 | +23 | clear |
| Alex Pearce | Fremantle | 13 | 14 | 27.9 | 37 | +23 | clear |
| Nicholas Holman | Carlton | 13 | 0 | 20.0 | 23 | +23 | clear |
| Jed Bews | Geelong | 15 | 1 | 15.4 | 24 | +23 | clear |
| Reef McInnes | Collingwood | 6 | 55 | 55.4 | 76 | +21 | clear |
| Liam Henry | Fremantle | 7 | 59 | 80.2 | 80 | +21 | clear |
| Ben Long | St Kilda | 10 | 9 | 30.7 | 30 | +21 | clear |
| Joel Hamling | Geelong | 15 | 14 | 23.4 | 35 | +21 | clear |
| Matt Guelfi | Essendon | 9 | 5 | 15.4 | 24 | +19 | clear |
| Ben McKay | North Melbourne | 11 | 27 | 34.2 | 46 | +19 | clear |
| Daniel Butler | Richmond | 12 | 0 | 15.4 | 19 | +19 | clear |
| Rhys Stanley | St Kilda | 18 | 12 | 21.2 | 30 | +18 | clear |
| Corey Durdin | Carlton | 6 | 34 | 48.1 | 51 | +17 | clear |
| Jacob Wehr | GWS | 6 | 3 | 27.7 | 19 | +16 | clear |
| Mitch McGovern | Adelaide | 12 | 9 | 24.2 | 25 | +16 | clear |
| Aidan Corr | GWS | 14 | 33 | 43.0 | 49 | +16 | clear |
| Harry Schoenberg | Adelaide | 7 | 40 | 30.8 | 53 | +13 | clear |
| Sam Sturt | Fremantle | 8 | 40 | 46.5 | 52 | +12 | clear |
| Finn Maginness | Hawthorn | 7 | 23 | 30.4 | 34 | +11 | clear |
| Oskar Baker | Melbourne | 9 | 18 | 20.6 | 29 | +11 | clear |
| Lachlan Weller | Fremantle | 12 | 67 | 56.9 | 78 | +11 | clear |
| Bailey Scott | North Melbourne | 8 | 22 | 20.0 | 32 | +10 | clear |
| Jake Kolodjashnij | Geelong | 13 | 27 | 25.7 | 36 | +9 | clear |
| Jamie Cripps | St Kilda | 16 | 24 | 30.3 | 33 | +9 | clear |
| Noah Answerth | Brisbane | 8 | 20 | 16.8 | 28 | +8 | clear |
| Tom Cole | West Coast | 11 | 20 | 28.2 | 28 | +8 | clear |
| Harry Morrison | Hawthorn | 10 | 20 | 15.4 | 27 | +7 | clear |
| James Jordon | Melbourne | 8 | 36 | 30.1 | 41 | +5 | clear |
| James Tunstill | Brisbane | 5 | 87 | 66.7 | 91 | +4 | clear |
| Bailey Macdonald | Hawthorn | 4 | 105 | 79.6 | 107 | +2 | clear |
| Nathan Broad | Richmond | 11 | 9 | 15.4 | 11 | +2 | clear |
| Hunter Clark | St Kilda | 9 | 49 | 89.8 | 50 | +1 | clear |
| Liam Ryan | West Coast | 9 | 27 | 30.6 | 28 | +1 | clear |

## Board top-50 (A4 context) — CONTROL efea88e5 · PREVIOUS c8051893 · CURRENT 7a07e369
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 7151 | 7207 | 7734 | +583 | +527 |
| 2 | Nick Daicos | MID | 7002 | 7069 | 7626 | +624 | +557 |
| 3 | Luke Jackson | RUC | 6803 | 6986 | 7411 | +608 | +425 |
| 4 | Tristan Xerri | RUC | 5795 | 5755 | 6384 | +589 | +629 |
| 5 | Nasiah Wanganeen-Milera | MID | 5794 | 5961 | 6270 | +476 | +309 |
| 6 | Josh Treacy | KEY_FWD | — | — | 6055 | — | — |
| 7 | Max Holmes | MID | 5386 | 5499 | 5959 | +573 | +460 |
| 8 | Zak Butters | MID | 5174 | 5225 | 5745 | +571 | +520 |
| 9 | Errol Gulden | MID | 5256 | 5299 | 5715 | +459 | +416 |
| 10 | Bailey Smith | MID | 4715 | 4773 | 5282 | +567 | +509 |
| 11 | Finn Callaghan | MID | 4904 | 4952 | 5183 | +279 | +231 |
| 12 | Lachlan Ash | GEN_DEF | 4611 | 4663 | 4924 | +313 | +261 |
| 13 | Will Ashcroft | MID | 4768 | 4823 | 4895 | +127 | +72 |
| 14 | Noah Anderson | MID | 4091 | 4131 | 4528 | +437 | +397 |
| 15 | Caleb Serong | MID | 4170 | 4202 | 4490 | +320 | +288 |
| 16 | Archie Roberts | GEN_DEF | 4668 | 4597 | 4327 | -341 | -270 |
| 17 | Willem Duursma | MID | 4110 | 4160 | 4225 | +115 | +65 |
| 18 | Jai Newcombe | MID | — | — | 4187 | — | — |
| 19 | Tom Green | MID | 4424 | 4472 | 4165 | -259 | -307 |
| 20 | Matt Rowell | MID | 3752 | 3779 | 3984 | +232 | +205 |
| 21 | Ryley Sanders | MID | 3926 | 4212 | 3930 | +4 | -282 |
| 22 | Sam Darcy | KEY_FWD | 4144 | 3978 | 3825 | -319 | -153 |
| 23 | Jason Horne-Francis | MID | 3702 | 4199 | 3802 | +100 | -397 |
| 24 | Isaac Heeney | MID | 3301 | 3327 | 3772 | +471 | +445 |
| 25 | Brodie Grundy | RUC | 3314 | 3344 | 3770 | +456 | +426 |
| 26 | Darcy Wilmot | GEN_DEF | 3732 | 3774 | 3763 | +31 | -11 |
| 27 | Murphy Reid | GEN_FWD | 3742 | 3843 | 3749 | +7 | -94 |
| 28 | Riley Thilthorpe | KEY_FWD | 3702 | 3555 | 3641 | -61 | +86 |
| 29 | Colby McKercher | MID | 3627 | 3814 | 3627 | +0 | -187 |
| 30 | Harley Reid | MID | 3549 | 3565 | 3549 | +0 | -16 |
| 31 | Nick Watson | GEN_FWD | 3538 | 3579 | 3539 | +1 | -40 |
| 32 | Marcus Bontempelli | MID | 3084 | 3109 | 3524 | +440 | +415 |
| 33 | Mac Andrew | KEY_DEF | 3504 | 3530 | 3508 | +4 | -22 |
| 34 | Finn O'Sullivan | MID | 3427 | 3495 | 3451 | +24 | -44 |
| 35 | Nick Blakey | GEN_DEF | 3266 | 3287 | 3431 | +165 | +144 |
| 36 | Sam Lalor | MID | 3337 | 3703 | 3400 | +63 | -303 |
| 37 | Kysaiah Pickett | GEN_FWD | 3076 | 3031 | 3329 | +253 | +298 |
| 38 | Luke Davies-Uniacke | MID | 2930 | 2952 | 3274 | +344 | +322 |
| 39 | Callum Wilkie | KEY_DEF | — | — | 3252 | — | — |
| 40 | Timothy English | RUC | 2916 | 2907 | 3187 | +271 | +280 |
| 41 | Jordan Dawson | MID | 2758 | 2774 | 3156 | +398 | +382 |
| 42 | Jordan Clark | GEN_DEF | 3007 | 3031 | 3142 | +135 | +111 |
| 43 | Bodhi Uwland | GEN_DEF | — | — | 3045 | — | — |
| 44 | George Wardlaw | MID | 3035 | 3033 | 3035 | +0 | +2 |
| 45 | Levi Ashcroft | MID | 3028 | 3270 | 3032 | +4 | -238 |
| 46 | Jagga Smith | MID | 2822 | 3188 | 3031 | +209 | -157 |
| 47 | Logan Morris | KEY_FWD | 3018 | 2843 | 3018 | +0 | +175 |
| 48 | Josh Worrell | GEN_DEF | 2937 | 3236 | 3016 | +79 | -220 |
| 49 | Jack Sinclair | GEN_DEF | — | — | 3013 | — | — |
| 50 | Aaron Cadman | KEY_FWD | 2970 | 2818 | 2970 | +0 | +152 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
