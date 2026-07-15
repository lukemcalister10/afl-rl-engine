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
B1        PASS    | PASS    | HALT     candidate matrix unavailable — B1 produced NO result and HALTS rather than pass silently (the v2.5 comparator is NOT substituted): JSONDecodeError: Expecting value: line 1 column 1 (char 0)  <- MOVED
B2        PASS    | PASS    | NOT-RUN  SGC_SKIP=B2  <- MOVED
B3        PASS    | PASS    | FAIL     candidate matrix unavailable — B3 cannot seal the candidate: JSONDecodeError: Expecting value: line 1 column 1 (char 0)  <- MOVED
B4        PASS    | PASS    | FAIL     regenerated rl_app_data.json md5=MISSING vs shipped 800d0399 (byte-agree gate; export exit=1)  <- MOVED
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail): 60 saves, aggregate lift +2195; pure lower bound: lowered=0 (bar 0), non-ND moved=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1353, 1552, 1882, 2587, 3244, 3362, 3491, 3572, 3670, 3765, 3942, 4120, 4318, 4449, 4525]; dips(more games worth less)=none; 0->6 rise T=+2138; 0->6 steps>50%T=none; rise by 3g=+1234 (need >=534) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR (Luke's amended law; board path)
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 roster-wide (D13 guard-transform → assertion; obituary E5)
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=5  FEATURE=1  HALT=1  NOT-RUN=1  PASS=13  PENDING=4  STRUCK=1  (65s)
```

## Supporting detail

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
