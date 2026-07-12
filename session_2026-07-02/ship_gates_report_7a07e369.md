# ship_gates_check report — STATE: BAKED v2.8 (chapter-lever L1 young-GDEF transition credit + pick redenomination; store 04f38dad, board 9ecbe0fa, config 69ead79b944d, book-seal a19b3cb8; discount 15%; CONTROL as of 2026-07-12). Engine head SHARED with v2.7 — the store 04f38dad and board 9ecbe0fa are the disambiguators; verify by regeneration (DECISIONS v93 §43). — head 7a07e369 store b0c39d78 config 69ead79b944d
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: BAKED v2.8 (chapter-lever L1 young-GDEF transition credit + pick redenomination; store 04f38dad, board 9ecbe0fa, config 69ead79b944d, book-seal a19b3cb8; discount 15%; CONTROL as of 2026-07-12). Engine head SHARED with v2.7 — the store 04f38dad and board 9ecbe0fa are the disambiguators; verify by regeneration (DECISIONS v93 §43). ===
=== SHIP GATES BOARD — head 7a07e369 store b0c39d78 config 69ead79b944d — suite 764a0d91 — 2026-07-12 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash 69ead79b944d291b — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=7a07e369 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 4430 vs 2746
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1420 vs 1571 (Ward=1746, ratio=0.813) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1618 vs 1746
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=2392 2025=4464 ratio=0.54 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=30 ev=3726 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=1844 (floor 1600); Jake Bowey=3097 (floor 2100); Nick Blakey=3598 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUC median=392 (n=13, pooled — thin slice) vs pick-matched MID kernel median=615 (n=67, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=GDEF gfut=GEN_DEF (need GDEF/GEN_DEF) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2648 Tsatas=1240 ratio=2.14x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | PASS     Ginnivan>Ward: 1844 vs 1746
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1260 2025=2271 ratio=0.55 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 1750 vs 992; Cumming>Annable: 2186 vs 2021
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 791 vs 1023; Smillie>Retschko: 1302 vs 838
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3206 lineball=True; Levi Ashcroft=3194 lineball=True
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1706: Trent Rivers=1794 lineball=True; Zach Reid=1721 lineball=True; Jase Burgoyne=2108 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | PASS     CANDIDATE (regenerated this run — engine 7a07e369 store b0c39d78 config 69ead79b944d): cross-cohort AVERAGE peak N=4 AVG(peak)=129 (need peak in yrs 4-6, >100; pre-peak dips of the AVERAGE <5% tolerated, path_ok=True; per-cohort UNGATED, table printed — Luke D5); avg row: 1:100 2:115 3:120 4:129 5:127 6:119 7:106; cohorts n=17 | v2.5 comparator avg row [NAMED, NOT certified]: 1:100 2:122 3:133 4:143 5:141 6:133 7:116
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUC|GOOD|T5:6.45, GEN_FWD|GOOD|T1:5.45, MID|GOOD|T2:2.54, RUC|GOOD|T3:2.45; GOOD>BUST sep GEN_DEF 44.4/0.9, GEN_FWD 38.8/0.6, KEY_DEF 50.3/1.1, KEY_FWD 61.8/0.5, MID 49.3/0.5, RUC 21.0/0.3 [cert engine 7a07e369 store b0c39d78 config 69ead79b]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine 7a07e369 store b0c39d78 config 69ead79b944d): MATCHES the sealed baseline. current=e559eb6cafb5b79d.. (2649 players) vs baseline=e559eb6cafb5b79d.. (2649 players, sealed head 7a07e369) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=de4baef9 vs shipped de4baef9 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 63 saves, aggregate lift +2085; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1316, 1600, 1910, 2594, 3225, 3319, 3375, 3430, 3445, 3457, 3512, 3580, 3666, 3706, 3736]; dips(more games worth less)=none; 0->6 rise T=+2059; 0->6 steps>50%T=none; rise by 3g=+1278 (need >=515) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=17  PENDING=4  STRUCK=1  (622s)
```

## Supporting detail

B1 per-cohort curves — CANDIDATE, regenerated this run (UNGATED — Luke eyeball channel):
| cohort | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 127 | 164 | 165 | 175 | 151 | 138 |
| 2005 | 4 | 100 | 145 | 137 | 181 | 172 | 166 | 144 |
| 2006 | 4 | 100 | 119 | 123 | 135 | 135 | 133 | 116 |
| 2007 | 5 | 100 | 115 | 107 | 110 | 131 | 124 | 106 |
| 2008 | 4 | 100 | 119 | 148 | 161 | 142 | 125 | 112 |
| 2009 | 2 | 100 | 113 | 96 | 97 | 98 | 87 | 75 |
| 2010 | 4 | 100 | 120 | 124 | 140 | 134 | 117 | 96 |
| 2011 | 4 | 100 | 117 | 130 | 147 | 143 | 137 | 113 |
| 2012 | 3 | 100 | 102 | 110 | 109 | 105 | 100 | 84 |
| 2013 | 5 | 100 | 122 | 133 | 155 | 158 | 138 | 107 |
| 2014 | 4 | 100 | 112 | 120 | 126 | 114 | 112 | 111 |
| 2015 | 4 | 100 | 107 | 105 | 107 | 104 | 104 | 100 |
| 2016 | 4 | 100 | 115 | 123 | 140 | 129 | 130 | 113 |
| 2017 | 3 | 100 | 108 | 110 | 98 | 92 | 92 | 86 |
| 2018 | 2 | 100 | 116 | 108 | 115 | 111 | 103 | 96 |
| 2019 | 5 | 100 | 101 | 105 | 112 | 121 | 111 | 94 |
| 2020 | 2 | 100 | 102 | 99 | 90 | 95 | 92 | — |
| **AVG (the gated row — CANDIDATE)** | **4** | **100** | **115** | **120** | **129** | **127** | **119** | **106** |

B5 FLOOR-SAVES table (n=63, aggregate lift=+2085 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Paddy Dow | Carlton | 9 | 14 | 112.5 | 165 | +151 | clear |
| Stephen Coniglio | GWS | 15 | 24 | 112.5 | 165 | +141 | clear |
| Jaeger O'Meara | Gold Coast | 15 | 64 | 150.0 | 186 | +122 | clear |
| Chayce Jones | Adelaide | 8 | 10 | 80.2 | 111 | +101 | clear |
| Steele Sidebottom | Collingwood | 18 | 4 | 69.0 | 99 | +95 | clear |
| Oliver Wiltshire | Geelong | 3 | 11 | 84.3 | 101 | +90 | clear |
| Jacob Hopper | GWS | 11 | 44 | 89.8 | 122 | +78 | clear |
| Luke Pedlar | Adelaide | 6 | 72 | 124.3 | 141 | +69 | clear |
| Conor Stone | GWS | 6 | 31 | 96.7 | 85 | +54 | clear |
| Bailey Laurie | Melbourne | 6 | 21 | 55.4 | 74 | +53 | clear |
| Jack Martin | Gold Coast | 14 | 48 | 112.5 | 98 | +50 | clear |
| Billy Cootee | Sydney | 1 | 37 | 225.0 | 83 | +46 | clear |
| Callum Ah Chee | Gold Coast | 11 | 40 | 85.3 | 86 | +46 | clear |
| Phoenix Gothard | GWS | 3 | 374 | 355.6 | 419 | +45 | clear |
| Sam Butler | Hawthorn | 5 | 67 | 80.1 | 107 | +40 | clear |
| Liam Stocker | Carlton | 8 | 2 | 39.8 | 41 | +39 | clear |
| Jade Gresham | St Kilda | 11 | 14 | 43.0 | 51 | +37 | clear |
| Nicholas Coffield | St Kilda | 9 | 17 | 85.3 | 52 | +35 | clear |
| Brandon Starcevich | Brisbane | 9 | 7 | 43.0 | 42 | +35 | clear |
| Charlie Spargo | Melbourne | 9 | 1 | 30.4 | 36 | +35 | clear |
| Jake Melksham | Essendon | 17 | 15 | 74.5 | 50 | +35 | clear |
| Oliver Henry | Collingwood | 6 | 59 | 77.3 | 92 | +33 | clear |
| Harvey Gallagher | Western Bulldogs | 4 | 105 | 112.3 | 136 | +31 | clear |
| Finlay Macrae | Collingwood | 6 | 79 | 66.1 | 109 | +30 | clear |
| Laitham Vandermeer | Western Bulldogs | 8 | 2 | 27.9 | 32 | +30 | clear |
| Xavier O'Halloran | GWS | 8 | 14 | 32.3 | 43 | +29 | clear |
| Jamie Elliott | — | 15 | 6 | 25.0 | 32 | +26 | clear |
| Darcy Gardiner | Brisbane | 13 | 22 | 32.3 | 47 | +25 | clear |
| Jed Bews | Geelong | 15 | 1 | 15.1 | 26 | +25 | clear |
| Ryan Gardner | Geelong | 11 | 9 | 15.1 | 33 | +24 | clear |
| Alex Pearce | Fremantle | 13 | 15 | 27.9 | 39 | +24 | clear |
| Nicholas Holman | Carlton | 13 | 0 | 20.0 | 24 | +24 | clear |
| Ben Long | St Kilda | 10 | 9 | 30.7 | 32 | +23 | clear |
| Liam Henry | Fremantle | 7 | 62 | 80.2 | 84 | +22 | clear |
| Joel Hamling | Geelong | 15 | 15 | 23.4 | 37 | +22 | clear |
| Reef McInnes | Collingwood | 6 | 60 | 55.3 | 81 | +21 | clear |
| Matt Guelfi | Essendon | 9 | 5 | 15.1 | 26 | +21 | clear |
| Ben McKay | North Melbourne | 11 | 28 | 34.2 | 48 | +20 | clear |
| Daniel Butler | Richmond | 12 | 0 | 15.1 | 20 | +20 | clear |
| Corey Durdin | Carlton | 6 | 35 | 48.1 | 54 | +19 | clear |
| Jacob Wehr | GWS | 6 | 3 | 27.1 | 21 | +18 | clear |
| Mitch McGovern | Adelaide | 12 | 9 | 24.2 | 27 | +18 | clear |
| Rhys Stanley | St Kilda | 18 | 13 | 21.2 | 30 | +17 | clear |
| Aidan Corr | GWS | 14 | 36 | 43.0 | 51 | +15 | clear |
| Harry Schoenberg | Adelaide | 7 | 42 | 30.7 | 56 | +14 | clear |
| Finn Maginness | Hawthorn | 7 | 23 | 30.4 | 36 | +13 | clear |
| Sam Sturt | Fremantle | 8 | 41 | 46.5 | 54 | +13 | clear |
| Oskar Baker | Melbourne | 9 | 19 | 20.6 | 32 | +13 | clear |
| Lachlan Weller | Fremantle | 12 | 70 | 56.9 | 82 | +12 | clear |
| Noah Answerth | Brisbane | 8 | 20 | 16.7 | 31 | +11 | clear |
| Tom Cole | West Coast | 11 | 21 | 28.2 | 31 | +10 | clear |
| Jamie Cripps | St Kilda | 16 | 26 | 30.3 | 36 | +10 | clear |
| Bailey Scott | North Melbourne | 8 | 24 | 20.0 | 33 | +9 | clear |
| Jake Kolodjashnij | Geelong | 13 | 29 | 25.7 | 38 | +9 | clear |
| Harry Morrison | Hawthorn | 10 | 21 | 15.1 | 28 | +7 | clear |
| Judson Clarke | Richmond | 5 | 86 | 78.8 | 92 | +6 | clear |
| Bailey Macdonald | Hawthorn | 4 | 117 | 79.6 | 122 | +5 | clear |
| James Jordon | Melbourne | 8 | 38 | 30.1 | 43 | +5 | clear |
| James Tunstill | Brisbane | 5 | 92 | 66.7 | 96 | +4 | clear |
| Kaleb Smith | Richmond | 4 | 119 | 84.0 | 122 | +3 | clear |
| Nathan Broad | Richmond | 11 | 9 | 15.1 | 12 | +3 | clear |
| Hunter Clark | St Kilda | 9 | 53 | 89.8 | 55 | +2 | clear |
| Liam Ryan | West Coast | 9 | 28 | 30.6 | 30 | +2 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT 7a07e369
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 8115 | 7151 | 8116 | +1 | +965 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 8050 | +0 | +1048 |
| 3 | Luke Jackson | RUC | 7799 | 6803 | 7800 | +1 | +997 |
| 4 | Tristan Xerri | RUC | 6649 | 5795 | 6649 | +0 | +854 |
| 5 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 6607 | +1 | +813 |
| 6 | Josh Treacy | KEY_FWD | — | — | 6299 | — | — |
| 7 | Max Holmes | MID | 6269 | 5386 | 6270 | +1 | +884 |
| 8 | Zak Butters | MID | 6059 | 5174 | 6060 | +1 | +886 |
| 9 | Errol Gulden | MID | 5983 | 5256 | 5983 | +0 | +727 |
| 10 | Bailey Smith | MID | 5605 | 4715 | 5605 | +0 | +890 |
| 11 | Finn Callaghan | MID | 5442 | 4904 | 5443 | +1 | +539 |
| 12 | Lachlan Ash | GEN_DEF | 5187 | 4611 | 5188 | +1 | +577 |
| 13 | Will Ashcroft | MID | 5155 | 4768 | 5156 | +1 | +388 |
| 14 | Noah Anderson | MID | 4765 | 4091 | 4765 | +0 | +674 |
| 15 | Caleb Serong | MID | 4701 | 4170 | 4702 | +1 | +532 |
| 16 | Archie Roberts | GEN_DEF | 4577 | 4668 | 4577 | +0 | -91 |
| 17 | Jai Newcombe | MID | — | — | 4496 | — | — |
| 18 | Willem Duursma | MID | 4429 | 4110 | 4430 | +1 | +320 |
| 19 | Tom Green | MID | 4391 | 4424 | 4391 | +0 | -33 |
| 20 | Matt Rowell | MID | 4185 | 3752 | 4185 | +0 | +433 |
| 21 | Ryley Sanders | MID | 4129 | 3926 | 4129 | +0 | +203 |
| 22 | Sam Darcy | KEY_FWD | 4013 | 4144 | 4013 | +0 | -131 |
| 23 | Jason Horne-Francis | MID | 3996 | 3702 | 3996 | +0 | +294 |
| 24 | Isaac Heeney | MID | 3981 | 3301 | 3981 | +0 | +680 |
| 25 | Darcy Wilmot | GEN_DEF | 3967 | 3732 | 3967 | +0 | +235 |
| 26 | Brodie Grundy | RUC | 3959 | 3314 | 3959 | +0 | +645 |
| 27 | Murphy Reid | GEN_FWD | 3953 | 3742 | 3953 | +0 | +211 |
| 28 | Colby McKercher | MID | 3829 | 3627 | 3830 | +1 | +203 |
| 29 | Riley Thilthorpe | KEY_FWD | 3818 | 3702 | 3819 | +1 | +117 |
| 30 | Harley Reid | MID | 3726 | 3549 | 3726 | +0 | +177 |
| 31 | Marcus Bontempelli | MID | 3721 | 3084 | 3721 | +0 | +637 |
| 32 | Nick Watson | GEN_FWD | 3720 | 3538 | 3720 | +0 | +182 |
| 33 | Mac Andrew | KEY_DEF | 3691 | 3504 | 3691 | +0 | +187 |
| 34 | Finn O'Sullivan | MID | 3643 | 3427 | 3643 | +0 | +216 |
| 35 | Nick Blakey | GEN_DEF | 3598 | 3266 | 3598 | +0 | +332 |
| 36 | Sam Lalor | MID | 3574 | 3337 | 3574 | +0 | +237 |
| 37 | Kysaiah Pickett | GEN_FWD | 3496 | 3076 | 3497 | +1 | +421 |
| 38 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3459 | +0 | +529 |
| 39 | Callum Wilkie | KEY_DEF | — | — | 3416 | — | — |
| 40 | Timothy English | RUC | 3349 | 2916 | 3350 | +1 | +434 |
| 41 | Jordan Dawson | MID | 3312 | 2758 | 3312 | +0 | +554 |
| 42 | Jordan Clark | GEN_DEF | 3307 | 3007 | 3307 | +0 | +300 |
| 43 | George Wardlaw | MID | 3206 | 3035 | 3206 | +0 | +171 |
| 44 | Levi Ashcroft | MID | 3193 | 3028 | 3194 | +1 | +166 |
| 45 | Jagga Smith | MID | 3192 | 2822 | 3192 | +0 | +370 |
| 46 | Josh Worrell | GEN_DEF | 3180 | 2937 | 3180 | +0 | +243 |
| 47 | Bodhi Uwland | GEN_DEF | — | — | 3176 | — | — |
| 48 | Logan Morris | KEY_FWD | 3171 | 3018 | 3172 | +1 | +154 |
| 49 | Jack Sinclair | GEN_DEF | — | — | 3140 | — | — |
| 50 | Aaron Cadman | KEY_FWD | 3122 | 2970 | 3122 | +0 | +152 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
