# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 05eebe0a — NOT AN ENDORSED STATE — head 05eebe0a store e1b4d8bf
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 05eebe0a — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 05eebe0a store e1b4d8bf — suite 764a0d91 — 2026-07-08 ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=efea88e5 · PREVIOUS=c8051893 · CURRENT=05eebe0a ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4199 vs 2089
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1355 vs 1485 (Ward=1650, ratio=0.821) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1543 vs 1650
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3019 2025=4235 ratio=0.71 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=29 ev=3549 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1772 (floor 1600); Jake Bowey=2932 (floor 2100); Nick Blakey=3431 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=393 (n=13, pooled — thin slice) vs pick-matched MID kernel median=542 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2520 Tsatas=1177 ratio=2.14x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 1772 vs 1650
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1005 2025=1707 ratio=0.59 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 1633 vs 849; Cumming>Annable: 2071 vs 1849
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 748 vs 956; Smillie>Retschko: 1189 vs 784
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3035 lineball=True; Levi Ashcroft=3032 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1167: Trent Rivers=1713 lineball=False; Zach Reid=1633 lineball=False; Jase Burgoyne=1975 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     cross-cohort AVERAGE peak N=4 AVG(peak)=132 (need peak in yrs 4-6, >100; pre-peak dips of the AVERAGE <5% tolerated, path_ok=True; per-cohort UNGATED, table printed every run — Luke redefinition 02/07 D5); avg row: 1:100 2:117 3:123 4:132 5:131 6:123 7:109; cohorts n=17; matrix=s4_matrix_w07.json
B2        PASS    | PASS    | PASS     median |IS-WF| leakage=0.0 %-pts (tol 0.5, SET 02/07/2026 — N=5 spread 0.00); GOOD>BUST separation: GEN_DEF 40/1, GEN_FWD 38/1, KEY_DEF 48/1, KEY_FWD 60/1, MID 49/1
B3        PASS    | PENDING | FAIL     book stable-key seal DIFFERS FROM baseline: current=fcc569c0696da32f.. (2649 players) vs baseline=5799a9ceae5ca3ef.. (2649 players, sealed head efea88e5); matrix=s4_matrix_w07.json [raw-file sha is id(p)-keyed / non-deterministic by design]  <- MOVED
B4        PASS    | FAIL    | PASS     regenerated rl_app_data.json md5=8e8e9250 vs shipped 8e8e9250 (byte-agree gate; export exit=0)  <- MOVED
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 57 saves, aggregate lift +1774; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1260, 1530, 1825, 2474, 3072, 3161, 3215, 3268, 3285, 3295, 3348, 3413, 3495, 3533, 3562]; dips(more games worth less)=none; 0->6 rise T=+1955; 0->6 steps>50%T=none; rise by 3g=+1214 (need >=489) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | —       | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)  <- MOVED
D14b      PASS    | —       | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)  <- MOVED
D14c      PASS    | —       | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)  <- MOVED
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=4  FEATURE=1  PASS=16  PENDING=4  STRUCK=1  (218s)
```

## Supporting detail

B1 per-cohort curves (UNGATED — printed every gates-board run, Luke eyeball channel):
| cohort | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 127 | 162 | 162 | 173 | 151 | 137 |
| 2005 | 4 | 100 | 142 | 136 | 180 | 171 | 163 | 142 |
| 2006 | 4 | 100 | 120 | 126 | 138 | 137 | 135 | 117 |
| 2007 | 5 | 100 | 118 | 110 | 114 | 137 | 130 | 110 |
| 2008 | 4 | 100 | 123 | 157 | 170 | 154 | 138 | 121 |
| 2009 | 2 | 100 | 113 | 98 | 98 | 100 | 88 | 76 |
| 2010 | 4 | 100 | 122 | 129 | 146 | 141 | 122 | 102 |
| 2011 | 4 | 100 | 120 | 134 | 152 | 151 | 144 | 119 |
| 2012 | 3 | 100 | 105 | 113 | 113 | 109 | 104 | 87 |
| 2013 | 5 | 100 | 124 | 137 | 160 | 163 | 143 | 111 |
| 2014 | 4 | 100 | 116 | 126 | 133 | 120 | 119 | 116 |
| 2015 | 4 | 100 | 109 | 109 | 110 | 108 | 108 | 104 |
| 2016 | 4 | 100 | 117 | 127 | 145 | 135 | 136 | 117 |
| 2017 | 3 | 100 | 109 | 112 | 100 | 94 | 94 | 88 |
| 2018 | 4 | 100 | 117 | 110 | 118 | 114 | 105 | 99 |
| 2019 | 5 | 100 | 103 | 108 | 116 | 126 | 115 | 99 |
| 2020 | 2 | 100 | 105 | 102 | 93 | 97 | 94 | — |
| **AVG (the gated row)** | **4** | **100** | **117** | **123** | **132** | **131** | **123** | **109** |

B5 FLOOR-SAVES table (n=57, aggregate lift=+1774 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | Carlton | 9 | 13 | 112.5 | 147 | +134 | clear |
| Stephen Coniglio | GWS | 15 | 23 | 112.5 | 147 | +124 | clear |
| Jaeger O'Meara | Gold Coast | 15 | 61 | 150.0 | 165 | +104 | clear |
| Chayce Jones | Adelaide | 8 | 9 | 80.2 | 101 | +92 | clear |
| Steele Sidebottom | Collingwood | 18 | 3 | 69.0 | 90 | +87 | clear |
| Oliver Wiltshire | Geelong | 3 | 12 | 86.2 | 89 | +77 | clear |
| Jacob Hopper | GWS | 11 | 41 | 89.8 | 111 | +70 | clear |
| Luke Pedlar | Adelaide | 6 | 66 | 124.3 | 129 | +63 | clear |
| Conor Stone | GWS | 6 | 28 | 96.7 | 78 | +50 | clear |
| Bailey Laurie | Melbourne | 6 | 20 | 55.5 | 68 | +48 | clear |
| Jack Martin | Gold Coast | 14 | 46 | 112.5 | 89 | +43 | clear |
| Billy Cootee | Sydney | 1 | 35 | 225.0 | 76 | +41 | clear |
| Phoenix Gothard | GWS | 3 | 343 | 355.6 | 384 | +41 | clear |
| Callum Ah Chee | Gold Coast | 11 | 38 | 85.3 | 78 | +40 | clear |
| Liam Stocker | Carlton | 8 | 2 | 39.8 | 37 | +35 | clear |
| Jade Gresham | St Kilda | 11 | 13 | 43.0 | 47 | +34 | clear |
| Sam Butler | Hawthorn | 5 | 66 | 80.2 | 98 | +32 | clear |
| Brandon Starcevich | Brisbane | 9 | 6 | 43.0 | 38 | +32 | clear |
| Charlie Spargo | Melbourne | 9 | 1 | 30.4 | 33 | +32 | clear |
| Jake Melksham | Essendon | 17 | 15 | 74.6 | 47 | +32 | clear |
| Nicholas Coffield | St Kilda | 9 | 16 | 85.3 | 47 | +31 | clear |
| Oliver Henry | Collingwood | 6 | 55 | 77.3 | 85 | +30 | clear |
| Laitham Vandermeer | Western Bulldogs | 8 | 2 | 27.9 | 29 | +27 | clear |
| Xavier O'Halloran | GWS | 8 | 13 | 32.3 | 39 | +26 | clear |
| Harvey Gallagher | Western Bulldogs | 4 | 98 | 112.3 | 123 | +25 | clear |
| Finlay Macrae | Collingwood | 6 | 76 | 66.1 | 100 | +24 | clear |
| Nicholas Holman | Carlton | 13 | 0 | 20.0 | 22 | +22 | clear |
| Darcy Gardiner | Brisbane | 13 | 21 | 32.3 | 42 | +21 | clear |
| Alex Pearce | Fremantle | 13 | 14 | 27.9 | 35 | +21 | clear |
| Jed Bews | Geelong | 15 | 1 | 15.4 | 22 | +21 | clear |
| Ben Long | St Kilda | 10 | 9 | 30.7 | 29 | +20 | clear |
| Ryan Gardner | Geelong | 11 | 9 | 15.4 | 29 | +20 | clear |
| Daniel Butler | Richmond | 12 | 0 | 15.4 | 19 | +19 | clear |
| Joel Hamling | Geelong | 15 | 14 | 23.4 | 33 | +19 | clear |
| Rhys Stanley | St Kilda | 18 | 12 | 21.2 | 30 | +18 | clear |
| Liam Henry | Fremantle | 7 | 59 | 80.2 | 76 | +17 | clear |
| Matt Guelfi | Essendon | 9 | 5 | 15.4 | 22 | +17 | clear |
| Ben McKay | North Melbourne | 11 | 27 | 34.2 | 43 | +16 | clear |
| Corey Durdin | Carlton | 6 | 34 | 48.1 | 49 | +15 | clear |
| Jacob Wehr | GWS | 6 | 3 | 27.7 | 18 | +15 | clear |
| Mitch McGovern | Adelaide | 12 | 9 | 24.2 | 24 | +15 | clear |
| Reef McInnes | Collingwood | 6 | 59 | 55.4 | 72 | +13 | LTI (2025 AND again 2026) |
| Aidan Corr | GWS | 14 | 33 | 43.0 | 46 | +13 | clear |
| Harry Schoenberg | Adelaide | 7 | 40 | 30.8 | 51 | +11 | clear |
| Finn Maginness | Hawthorn | 7 | 23 | 30.4 | 33 | +10 | clear |
| Sam Sturt | Fremantle | 8 | 40 | 46.5 | 50 | +10 | clear |
| Oskar Baker | Melbourne | 9 | 18 | 20.6 | 28 | +10 | clear |
| Bailey Scott | North Melbourne | 8 | 22 | 20.0 | 30 | +8 | clear |
| Lachlan Weller | Fremantle | 12 | 67 | 56.9 | 75 | +8 | clear |
| Jamie Cripps | St Kilda | 16 | 24 | 30.3 | 32 | +8 | clear |
| Noah Answerth | Brisbane | 8 | 20 | 16.8 | 27 | +7 | clear |
| Tom Cole | West Coast | 11 | 20 | 28.2 | 27 | +7 | clear |
| Jake Kolodjashnij | Geelong | 13 | 27 | 25.7 | 34 | +7 | clear |
| Harry Morrison | Hawthorn | 10 | 20 | 15.4 | 25 | +5 | clear |
| James Jordon | Melbourne | 8 | 36 | 30.1 | 40 | +4 | clear |
| James Tunstill | Brisbane | 5 | 85 | 66.7 | 87 | +2 | clear |
| Nathan Broad | Richmond | 11 | 9 | 15.4 | 10 | +1 | clear |

## Board top-50 (A4 context) — CONTROL efea88e5 · PREVIOUS c8051893 · CURRENT 05eebe0a
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 7151 | 7207 | 7734 | +583 | +527 |
| 2 | Nick Daicos | MID | 7002 | 7069 | 7626 | +624 | +557 |
| 3 | Luke Jackson | RUC | 6803 | 6986 | 7411 | +608 | +425 |
| 4 | Tristan Xerri | RUC | 5795 | 5755 | 6384 | +589 | +629 |
| 5 | Nasiah Wanganeen-Milera | MID | 5794 | 5961 | 6270 | +476 | +309 |
| 6 | Max Holmes | MID | 5386 | 5499 | 5959 | +573 | +460 |
| 7 | Zak Butters | MID | 5174 | 5225 | 5745 | +571 | +520 |
| 8 | Errol Gulden | MID | 5256 | 5299 | 5715 | +459 | +416 |
| 9 | Josh Treacy | KEY_FWD | — | — | 5478 | — | — |
| 10 | Bailey Smith | MID | 4715 | 4773 | 5282 | +567 | +509 |
| 11 | Finn Callaghan | MID | 4904 | 4952 | 5183 | +279 | +231 |
| 12 | Lachlan Ash | GEN_DEF | 4611 | 4663 | 4924 | +313 | +261 |
| 13 | Will Ashcroft | MID | 4768 | 4823 | 4895 | +127 | +72 |
| 14 | Tom Green | MID | 4424 | 4472 | 4885 | +461 | +413 |
| 15 | Noah Anderson | MID | 4091 | 4131 | 4528 | +437 | +397 |
| 16 | Caleb Serong | MID | 4170 | 4202 | 4490 | +320 | +288 |
| 17 | Archie Roberts | GEN_DEF | 4668 | 4597 | 4326 | -342 | -271 |
| 18 | Willem Duursma | MID | 4110 | 4160 | 4199 | +89 | +39 |
| 19 | Jai Newcombe | MID | — | — | 4187 | — | — |
| 20 | Sam Darcy | KEY_FWD | 4144 | 3978 | 4168 | +24 | +190 |
| 21 | Matt Rowell | MID | 3752 | 3779 | 3984 | +232 | +205 |
| 22 | Ryley Sanders | MID | 3926 | 4212 | 3930 | +4 | -282 |
| 23 | Jason Horne-Francis | MID | 3702 | 4199 | 3802 | +100 | -397 |
| 24 | Isaac Heeney | MID | 3301 | 3327 | 3772 | +471 | +445 |
| 25 | Brodie Grundy | RUC | 3314 | 3344 | 3770 | +456 | +426 |
| 26 | Darcy Wilmot | GEN_DEF | 3732 | 3774 | 3763 | +31 | -11 |
| 27 | Murphy Reid | GEN_FWD | 3742 | 3843 | 3747 | +5 | -96 |
| 28 | Colby McKercher | MID | 3627 | 3814 | 3627 | +0 | -187 |
| 29 | Harley Reid | MID | 3549 | 3565 | 3549 | +0 | -16 |
| 30 | Nick Watson | GEN_FWD | 3538 | 3579 | 3539 | +1 | -40 |
| 31 | Marcus Bontempelli | MID | 3084 | 3109 | 3524 | +440 | +415 |
| 32 | Mac Andrew | KEY_DEF | 3504 | 3530 | 3508 | +4 | -22 |
| 33 | Finn O'Sullivan | MID | 3427 | 3495 | 3446 | +19 | -49 |
| 34 | Nick Blakey | GEN_DEF | 3266 | 3287 | 3431 | +165 | +144 |
| 35 | Sam Lalor | MID | 3337 | 3703 | 3386 | +49 | -317 |
| 36 | Kysaiah Pickett | GEN_FWD | 3076 | 3031 | 3329 | +253 | +298 |
| 37 | Luke Davies-Uniacke | MID | 2930 | 2952 | 3274 | +344 | +322 |
| 38 | Nicholas Martin | MID | — | — | 3266 | — | — |
| 39 | Callum Wilkie | KEY_DEF | — | — | 3252 | — | — |
| 40 | Riley Thilthorpe | KEY_FWD | 3702 | 3555 | 3202 | -500 | -353 |
| 41 | Timothy English | RUC | 2916 | 2907 | 3187 | +271 | +280 |
| 42 | Jordan Dawson | MID | 2758 | 2774 | 3156 | +398 | +382 |
| 43 | Jordan Clark | GEN_DEF | 3007 | 3031 | 3142 | +135 | +111 |
| 44 | Bodhi Uwland | GEN_DEF | — | — | 3045 | — | — |
| 45 | George Wardlaw | MID | 3035 | 3033 | 3035 | +0 | +2 |
| 46 | Levi Ashcroft | MID | 3028 | 3270 | 3032 | +4 | -238 |
| 47 | Connor Rozee | MID | 2892 | 2917 | 3019 | +127 | +102 |
| 48 | Logan Morris | KEY_FWD | 3018 | 2843 | 3018 | +0 | +175 |
| 49 | Josh Worrell | GEN_DEF | 2937 | 3236 | 3016 | +79 | -220 |
| 50 | Jack Sinclair | GEN_DEF | — | — | 3013 | — | — |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
