# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 1867e953 — NOT AN ENDORSED STATE — head 1867e953 store b745002e config eed19a75f775
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 1867e953 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 1867e953 store b745002e config eed19a75f775 — suite 764a0d91 — 2026-08-20 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash eed19a75f775aeaf — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=1867e953 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 3915 vs 1847
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1553 vs 2554 (Ward=2837, ratio=0.547) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1456 vs 2837
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3532 2025=5048 ratio=0.70 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=30 ev=4125 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=2198 (floor 1600); Jake Bowey=4100 (floor 2100); Nick Blakey=4369 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUCK median=222 (n=11, pooled — thin slice) vs pick-matched MID kernel median=581 (n=70, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=SD gfut=SD (need SD/SD) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=3565 Tsatas=973 ratio=3.66x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | STRUCK   Luke 2026-08-20 — player-ordering assertion RETIRED, verbatim: "Those player ordering assertions were retired and are outdated. Since they occurred, Ward has hit an excellent run of form." Prior pattern: scored-never-flagged (register A9/pair-2 precedent); dated reads retired wholesale RULEBOOK v2.1 PART 2 (owner 2026-07-22). Zombie note: retired while this suite was bricked at :49; surfaced FAIL only on the first run after the unbricking. SCORED (never flagged): Ginnivan=2198 vs Ward=2837 (retired assertion was Ginnivan>Ward; ratio=0.775)  <- MOVED
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1366 2025=2040 ratio=0.67 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2618 vs 1254; Cumming>Annable: 2254 vs 1182
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 461 vs 570; Smillie>Retschko: 799 vs 1216
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3130 lineball=True; Levi Ashcroft=3879 lineball=False
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1320: Trent Rivers=1839 lineball=False; Zach Reid=1123 lineball=True; Jase Burgoyne=2347 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | STRUCK   [STRUCK — Luke 2026-08-20, verbatim: "That cohort rail again was retired. Weeks ago." The JULY-8 CONSTRUCTION is SUPERSEDED by the modern class-discipline law: G-COHORT as carried by the owner-signed RULEBOOK v2.1 + docs/acceptance_v2_0.json (walk-forward book ratio, max 1.3), reported UNMEASURED at R19 under RULEBOOK PART 3 — never assumed passing, never silently waived. Zombie note: retired while this suite was bricked at :49; surfaced HALT only on the first run after the unbricking. SCORED, NEVER FLAGGED — every figure below still prints; only the alarm is removed] JULY-8 construction (owner-ruled 2026-07-13, register v52 — CONFORMED; raw class-year sums of Vpath averaged UNWEIGHTED across 17 classes 2004-2020 incurve ND+RD; CANDIDATE regenerated this run — engine 1867e953 store b745002e config eed19a75f775): y1=62073.9 y2=68070.9 y3=78013.9 y4=88527.6 y5=89498.0 y6=86685.1 y7=79201.6; den=min(y1,y2)=y1=62073.9; ratios y4=1.4262(above-guide) y5=1.4418(above-guide) y6=1.3965(above-guide); RETIRED hard<=1.30 bar -> would have BREACHED at y[4, 5, 6] — SCORED, NOT FLAGGED (struck); guide 1.20-1.25 ADVISORY (margin reported, never gates)  <- MOVED
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells SD|GOOD|T2:4.36, RUCK|GOOD|T4:3.78, SD|GOOD|T4:2.41, KPD|GOOD|T5:2.11; GOOD>BUST sep KPD 36.2/1.3, KPF 45.9/0.6, MID 40.2/0.6, RUCK 16.7/0.3, SD 40.7/1.1, SF 38.3/0.8 [cert engine 1867e953 store b745002e config eed19a75]
B3        PASS    | PASS    | PASS     CANDIDATE book stable seal (regenerated this run — engine 1867e953 store b745002e config eed19a75f775): MATCHES the sealed baseline. current=9f46aba3ba8b056d.. (2650 players) vs baseline=9f46aba3ba8b056d.. (2650 players, sealed head 1867e953) [full stable-keyed content seal; raw-file sha is id(p)-keyed / non-deterministic by design]
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=68be10c7 vs shipped 68be10c7 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FEATURE  floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail; #326 scope = national draftees + 225 engine-pool entrants on their signed division levels): 15 saves, aggregate lift +4575; the floor is still a pure lower bound: lowered=0 (bar 0), moved outside the floor scope=0 (bar 0); saves table printed below (the new alarm surface)
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1138, 1206, 1308, 1427, 1623, 1798, 2074, 2190, 2293, 2405, 2583, 2731, 2868, 2983, 3100]; dips(more games worth less)=none; 0->6 rise T=+936; 0->6 steps>50%T=none; rise by 3g=+289 (need >=234) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR over the 1448 rows the surface prices (Luke's amended law; board path) [report-only, all ND incl. 122 pool rows at 65+: 656.7]
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 (D13 guard-transform → assertion; obituary E5) [report-only, all ND incl. pool: 712 — ladder-vs-pool pairs, different price objects]
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
D14d      —       | —       | PASS     SURFACE never-rises (R12): 0 rising step(s) picks 1-64 · 0 over the full 1-90 grid · scanned 90 pos×draft-age profiles (8010 adjacent pairs; players expose ~8%)  <- MOVED
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: FAIL=3  FEATURE=1  PASS=16  PENDING=4  STRUCK=3  (537s)
```

## Supporting detail

B1 — STRUCK (Luke 2026-08-20, "That cohort rail again was retired. Weeks ago."). The bold row is the RETIRED July-8 raw-class-sum construction, still SCORED and still printed; the indexed yr1=100 row is a NON-GATING SHAPE diagnostic (peak position + pre-peak dip), DEMOTED 2026-07-13 — its historic headline 126.8/125.2/116.1 is NOT the gate.
  SHAPE read (indexed, advisory): peak at yr5, pre-peak low 100.0 (index yr1=100).
| class | peakN | d1 | d2 | d3 | d4 | d5 | d6 | d7 |
|---|---|---|---|---|---|---|---|---|
| 2004 | 5 | 100 | 113 | 145 | 146 | 156 | 139 | 128 |
| 2005 | 4 | 100 | 122 | 142 | 183 | 171 | 176 | 160 |
| 2006 | 5 | 100 | 110 | 128 | 156 | 156 | 155 | 142 |
| 2007 | 5 | 100 | 112 | 112 | 126 | 165 | 159 | 132 |
| 2008 | 4 | 100 | 120 | 162 | 192 | 176 | 160 | 144 |
| 2009 | 4 | 100 | 107 | 99 | 116 | 110 | 102 | 92 |
| 2010 | 4 | 100 | 115 | 126 | 150 | 147 | 127 | 104 |
| 2011 | 5 | 100 | 111 | 134 | 157 | 160 | 157 | 136 |
| 2012 | 6 | 100 | 96 | 111 | 121 | 120 | 126 | 106 |
| 2013 | 5 | 100 | 113 | 140 | 166 | 170 | 158 | 127 |
| 2014 | 4 | 100 | 117 | 135 | 147 | 134 | 145 | 139 |
| 2015 | 6 | 100 | 106 | 116 | 119 | 116 | 120 | 119 |
| 2016 | 4 | 100 | 118 | 145 | 172 | 163 | 164 | 146 |
| 2017 | 3 | 100 | 102 | 115 | 111 | 112 | 111 | 108 |
| 2018 | 5 | 100 | 106 | 105 | 111 | 122 | 113 | 110 |
| 2019 | 5 | 100 | 100 | 112 | 139 | 151 | 145 | 123 |
| 2020 | 6 | 100 | 90 | 104 | 102 | 115 | 116 | — |
| _indexed AVG (SHAPE DIAGNOSTIC — DEMOTED 2026-07-13, NOT the gate)_ | _5_ | _100_ | _109_ | _125_ | _142_ | _144_ | _140_ | _126_ |
| **July-8 raw-sum AVG (the STRUCK rail, scored but never flagged — Luke 2026-08-20)** | **—** | **62074** | **68071** | **78014** | **88528** | **89498** | **86685** | **79202** |

B5 FLOOR-SAVES table (n=15, aggregate lift=+4575 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Tom Green | — | 7 | 4576 | 91.1 | 5867 | +1290 | clear |
| Nicholas Martin | — | 5 | 3268 | 42.3 | 4274 | +1005 | clear |
| Connor Rozee | — | 8 | 2665 | 110.9 | 3532 | +868 | clear |
| Joshua Kelly | — | 13 | 443 | 153.2 | 799 | +356 | clear |
| Jack Viney | — | 14 | 257 | 79.9 | 574 | +317 | clear |
| Brayden Fiorini | — | 11 | 247 | 53.0 | 448 | +201 | clear |
| Darcy Jones | — | 4 | 1183 | 134.0 | 1347 | +164 | clear |
| Mitchell Hinge | — | 10 | 263 | 12.9 | 402 | +138 | clear |
| Sam Powell-Pepper | — | 10 | 131 | 33.5 | 227 | +96 | clear |
| Thomas Sims | — | 2 | 705 | 190.4 | 775 | +71 | clear |
| Harry Edwards | — | 8 | 126 | 19.4 | 153 | +27 | clear |
| Riley Garcia | — | 7 | 64 | 8.0 | 84 | +20 | clear |
| Jesse Motlop | — | 5 | 87 | 65.5 | 95 | +9 | clear |
| Josh Sinn | — | 5 | 213 | 122.5 | 221 | +8 | clear |
| Ollie Lord | — | 6 | 128 | 18.0 | 133 | +5 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT 1867e953
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 8115 | 7151 | 10975 | +2860 | +3824 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 10410 | +2360 | +3408 |
| 3 | Luke Jackson | RUCK | 7799 | 6803 | 9751 | +1952 | +2948 |
| 4 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 9113 | +2507 | +3319 |
| 5 | Max Holmes | MID | 6269 | 5386 | 7986 | +1717 | +2600 |
| 6 | Errol Gulden | MID | 5983 | 5256 | 7445 | +1462 | +2189 |
| 7 | Tristan Xerri | RUCK | 6649 | 5795 | 7393 | +744 | +1598 |
| 8 | Will Ashcroft | MID | 5155 | 4768 | 6934 | +1779 | +2166 |
| 9 | Zak Butters | MID | 6059 | 5174 | 6924 | +865 | +1750 |
| 10 | Josh Treacy | KPF | — | — | 6502 | — | — |
| 11 | Bailey Smith | MID | 5605 | 4715 | 6494 | +889 | +1779 |
| 12 | Lachlan Ash | SD | 5187 | 4611 | 6065 | +878 | +1454 |
| 13 | Jason Horne-Francis | MID | 3996 | 3702 | 5903 | +1907 | +2201 |
| 14 | Tom Green | MID | 4391 | 4424 | 5867 | +1476 | +1443 |
| 15 | Finn Callaghan | MID | 5442 | 4904 | 5846 | +404 | +942 |
| 16 | Sam Darcy | KPF | 4013 | 4144 | 5384 | +1371 | +1240 |
| 17 | Noah Anderson | MID | 4765 | 4091 | 5217 | +452 | +1126 |
| 18 | Izak Rankine | SF | 2768 | 2428 | 5072 | +2304 | +2644 |
| 19 | Caleb Serong | MID | 4701 | 4170 | 4993 | +292 | +823 |
| 20 | Jai Newcombe | MID | — | — | 4828 | — | — |
| 21 | Matt Rowell | MID | 4185 | 3752 | 4762 | +577 | +1010 |
| 22 | Jagga Smith | MID | 3192 | 2822 | 4540 | +1348 | +1718 |
| 23 | Colby McKercher | MID | 3829 | 3627 | 4486 | +657 | +859 |
| 24 | Brodie Grundy | RUCK | 3959 | 3314 | 4432 | +473 | +1118 |
| 25 | Nick Blakey | SD | 3598 | 3266 | 4369 | +771 | +1103 |
| 26 | Chad Warner | MID | — | — | 4308 | — | — |
| 27 | Nicholas Martin | MID | — | — | 4274 | — | — |
| 28 | Riley Thilthorpe | KPF | 3818 | 3702 | 4260 | +442 | +558 |
| 29 | Isaac Heeney | MID | 3981 | 3301 | 4165 | +184 | +864 |
| 30 | Harley Reid | MID | 3726 | 3549 | 4125 | +399 | +576 |
| 31 | Jake Bowey | SD | 3096 | 2926 | 4100 | +1004 | +1174 |
| 32 | Kysaiah Pickett | SF | 3496 | 3076 | 4082 | +586 | +1006 |
| 33 | Ed Richards | MID | 3078 | 2625 | 3928 | +850 | +1303 |
| 34 | Willem Duursma | MID | 4429 | 4110 | 3915 | -514 | -195 |
| 35 | Mac Andrew | KPD | 3691 | 3504 | 3909 | +218 | +405 |
| 36 | Marcus Bontempelli | MID | 3721 | 3084 | 3896 | +175 | +812 |
| 37 | Levi Ashcroft | MID | 3193 | 3028 | 3879 | +686 | +851 |
| 38 | Bodhi Uwland | SD | — | — | 3852 | — | — |
| 39 | Ryley Sanders | MID | 4129 | 3926 | 3807 | -322 | -119 |
| 40 | Luke Davies-Uniacke | MID | 3459 | 2930 | 3805 | +346 | +875 |
| 41 | Nick Watson | SF | 3720 | 3538 | 3782 | +62 | +244 |
| 42 | Sam Lalor | MID | 3574 | 3337 | 3771 | +197 | +434 |
| 43 | Archie Roberts | SD | 4577 | 4668 | 3758 | -819 | -910 |
| 44 | Callum Wilkie | KPD | — | — | 3666 | — | — |
| 45 | Murphy Reid | SF | 3953 | 3742 | 3607 | -346 | -135 |
| 46 | Sam Berry | MID | 2648 | 2495 | 3565 | +917 | +1070 |
| 47 | Connor Rozee | MID | 2392 | 2892 | 3532 | +1140 | +640 |
| 48 | Timothy English | RUCK | 3349 | 2916 | 3511 | +162 | +595 |
| 49 | Jordan Clark | SD | 3307 | 3007 | 3492 | +185 | +485 |
| 50 | Dyson Sharp | MID | 1701 | 1338 | 3402 | +1701 | +2064 |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
