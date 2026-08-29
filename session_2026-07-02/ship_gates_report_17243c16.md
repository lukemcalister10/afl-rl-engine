# ship_gates_check report — STATE: PROTOTYPE/UNREGISTERED @ 17243c16 — NOT AN ENDORSED STATE — head 17243c16 store b4d23810 config d4f3c3cf8707
_Three-column rule (Luke, binding D10): every board output reports CONTROL / PREVIOUS / CURRENT with explicit deltas._
```
=== STATE: PROTOTYPE/UNREGISTERED @ 17243c16 — NOT AN ENDORSED STATE ===
=== SHIP GATES BOARD — head 17243c16 store b4d23810 config d4f3c3cf8707 — suite 764a0d91 — 2026-08-29 ===
=== CONFIG MANIFEST (gate mode): data/model_config.json hash d4f3c3cf8707350d — ambient model env cleared + pinned; unknown/divergent overrides rejected (halt) ===
=== THREE-COLUMN RULE (Luke, binding D10): CONTROL=7a07e369 · PREVIOUS=efea88e5 · CURRENT=17243c16 ===
A1        PASS    | PASS    | PASS     Duursma>Uwland: 3737 vs 2028
A2        FAIL    | FAIL    | FAIL     Curtis>=0.90xWard: 1640 vs 2549 (Ward=2832, ratio=0.579) [AMENDED 02/07/2026; UNCHANGED at 0.90 by ruling D7 — Luke: "we can look at Curtis down the line"]; Weddle>Ward: 1383 vs 2832
A3   [DC] FAIL    | FAIL    | FAIL     Connor Rozee: 2026=3357 2025=5255 ratio=0.64 (need >=0.75) [evaluated PRE-LTI-layer — Luke 02/07; AMENDED 0.80->0.75 Luke D7 data-caused (out for 2026), knife-edge by design]
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS    | PASS    | PASS     Harley Reid board rank=34 ev=4061 (need TOP 40)
A5        PASS    | PASS    | PASS     Jack Ginnivan=2314 (floor 1600); Jake Bowey=4188 (floor 2100); Nick Blakey=4274 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS    | PASS    | PASS     yr1-3 RUCK median=287 (n=11, pooled — thin slice) vs pick-matched MID kernel median=579 (n=70, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS    | PASS    | PASS     Ryan Maric: future_position=MID gfut=MID (need MID/MID) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]; Ed Langdon: future_position=SD gfut=SD (need SD/SD) [AMENDED 2026-07-05: _fut blend stripped -> single future_position, owner-authorised]
A8   [DC] PASS    | PASS    | PASS     Berry=2968 Tsatas=869 ratio=3.41x (need >=2.00x) [display de-ambiguated D4 02/07]
A9        PASS    | PASS    | STRUCK   Luke 2026-08-20 — player-ordering assertion RETIRED, verbatim: "Those player ordering assertions were retired and are outdated. Since they occurred, Ward has hit an excellent run of form." Prior pattern: scored-never-flagged (register A9/pair-2 precedent); dated reads retired wholesale RULEBOOK v2.1 PART 2 (owner 2026-07-22). Zombie note: retired while this suite was bricked at :49; surfaced FAIL only on the first run after the unbricking. scoring code deleted (shrink S5, 2026-08-28); the retirement note stands per P11.  <- MOVED
A10  [DC] PASS    | PASS    | PASS     Charlie Curnow: 2026=1322 2025=1976 ratio=0.67 (need >=0.50) [AMENDED 0.70->0.50 Luke 02/07 data-caused, PROVISIONAL — review at season-complete]
A11  [DC] PASS    | PASS    | PASS     Farrow>Patterson: 2174 vs 1193; Cumming>Annable: 2434 vs 1353
A12  [DC] FAIL    | FAIL    | FAIL     Travaglia>Moraes: 517 vs 712; Smillie>Retschko: 981 vs 883
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3313 lineball=True; Levi Ashcroft=3787 lineball=False
A14       PENDING | PENDING | PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1343: Trent Rivers=1597 lineball=True; Zach Reid=1348 lineball=True; Jase Burgoyne=2751 lineball=False
A15       STRUCK  | STRUCK  | STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS    | PASS    | STRUCK   [STRUCK — Luke 2026-08-20, verbatim: "That cohort rail again was retired. Weeks ago." The JULY-8 CONSTRUCTION is RETIRED. Its law, G-COHORT (walk-forward book ratio, max 1.3), was carried by the owner-signed RULEBOOK v2.1 and its twin docs/acceptance_v2_0.json; the v3 amendment of 2026-08-20 removed that twin and records G-COHORT in RULEBOOK PART 3 as RETIRED, with its 1.3 payload written down there. RULEBOOK PART 3 is the pointer of record. Zombie note: retired while this suite was bricked at :49; surfaced HALT only on the first run after the unbricking. SCORED, NEVER FLAGGED — every figure below still prints; only the alarm is removed] candidate matrix unavailable, so the struck rail scored nothing this run (the v2.5 comparator is NOT substituted): None  <- MOVED
B2        PASS    | PASS    | PASS     leave-cohort-out sensitivity (2014-2018 ND held out): median |IS-WF| leakage=0.000 %-pts (FULL precision; tol 0.5 UNCHANGED, SET 02/07/2026); worst cells RUCK|GOOD|T5:3.91, SD|GOOD|T4:3.02, KPF|GOOD|T4:2.95, RUCK|GOOD|T4:2.72; GOOD>BUST sep KPD 34.3/1.2, KPF 49.3/0.5, MID 39.0/0.6, RUCK 13.7/0.2, SD 41.0/1.1, SF 37.7/0.7 [cert engine 17243c16 store b4d23810 config d4f3c3cf]
B3        PASS    | PASS    | BAKE-SCOPED shrink S10 (owner word 2026-08-28): the freeze-stamp runs at bake acts (arm with SGC_B3=1) — the matrix it seals only moves when the book's inputs move, and rebuilding it cost 45-90 min of every board run for a comparison that cannot say anything new between bakes. The seal baseline stands untouched.  <- MOVED
B4        PASS    | PASS    | PASS     regenerated rl_app_data.json md5=4a52cc44 vs shipped 4a52cc44 (byte-agree gate; export exit=0)
B5        FEATURE | FEATURE | FAIL     floor-as-pricing-feature (Luke-ruled 02/07; VARIANT A flat .05 tail; #326 scope = national draftees + 225 engine-pool entrants on their signed division levels): 27 saves, aggregate lift +4938; the floor is still a pure lower bound: lowered=33 (bar 0), moved outside the floor scope=3 (bar 0); ORDER 46 denied-lift rows=38 (the ruled day-0 cap / never-repossess guard — reported, not a floor impurity; probed 2026-08-28, all explained); saves table printed below (the new alarm surface)  <- MOVED
B6        PASS    | PASS    | PASS     ramp(0..14g)=[1124, 1206, 1319, 1438, 1579, 1678, 1926, 2063, 2187, 2306, 2606, 2885, 3166, 3322, 3429]; dips(more games worth less)=none; 0->6 rise T=+802; 0->6 steps>50%T=none; rise by 3g=+315 (need >=201) [whole-ramp re-spec, DECLARED thresholds]
D14a      PASS    | PASS    | PASS     same pos×draft-age×recorded-pick ⇒ identical V0* across draft years: max cross-draft dispersion=0.0000 SCAR over the 1448 rows the surface prices (Luke's amended law; board path) [report-only, all ND incl. 122 pool rows at 65+: 235.4]
D14b      PASS    | PASS    | PASS     within (pos×draft-age×draft-year) V0 inversions under V0* = 0 (D13 guard-transform → assertion; obituary E5) [report-only, all ND incl. pool: 432 — ladder-vs-pool pairs, different price objects]
D14c      PASS    | PASS    | PASS     KPP retention floor O1 depth-monotone = True (max of isotonic-non-increasing KPP/nonKPP; comparator nonKPP-only)
D14d      —       | —       | PASS     SURFACE never-rises (R12): 0 rising step(s) picks 1-64 · 0 over the full 1-90 grid · scanned 90 pos×draft-age profiles (8010 adjacent pairs; players expose ~8%)  <- MOVED
C1        PENDING | PENDING | PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING | PENDING | PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
          columns: CONTROL | PREVIOUS | CURRENT (three-column rule; snapshots data/gates_snapshots/)
VERDICT: BAKE-SCOPED=1  FAIL=4  PASS=15  PENDING=4  STRUCK=3  (2110s)
```

## Supporting detail

B5 FLOOR-SAVES table (n=27, aggregate lift=+4938 — printed every gates-board run, the new alarm surface):
| player | club | yrs-in-system | raw ev | floor | saved-to | lift | register status |
|---|---|---|---|---|---|---|---|
| Tom Green | — | 7 | 4278 | 90.9 | 5530 | +1253 | clear |
| Nicholas Martin | — | 5 | 3121 | 42.3 | 4100 | +979 | clear |
| Connor Rozee | — | 8 | 2512 | 111.7 | 3357 | +845 | clear |
| Joshua Kelly | — | 13 | 424 | 157.6 | 770 | +347 | clear |
| Jack Viney | — | 14 | 244 | 77.0 | 555 | +311 | clear |
| Brayden Fiorini | — | 11 | 240 | 52.9 | 439 | +200 | clear |
| Darcy Jones | — | 4 | 1392 | 133.2 | 1574 | +182 | clear |
| Latrelle Pickett | — | 1 | 396 | 486.8 | 538 | +142 | clear |
| Mitchell Hinge | — | 10 | 272 | 12.9 | 413 | +141 | clear |
| Wil Dawson | — | 3 | 301 | 169.8 | 417 | +116 | clear |
| Sam Powell-Pepper | — | 10 | 133 | 33.4 | 230 | +96 | clear |
| Thomas Sims | — | 2 | 585 | 187.5 | 636 | +51 | clear |
| Alex Dodson | — | 2 | 106 | 125.3 | 151 | +45 | clear |
| Jordan Croft | — | 3 | 508 | 191.7 | 540 | +32 | clear |
| William McCabe | — | 3 | 342 | 183.1 | 371 | +29 | clear |
| Harry Edwards | — | 8 | 129 | 19.4 | 157 | +28 | clear |
| Riley Garcia | — | 7 | 85 | 8.0 | 113 | +28 | clear |
| Daniel Annable | — | 1 | 1326 | 938.7 | 1353 | +27 | clear |
| Matt Whitlock | — | 2 | 286 | 192.2 | 307 | +21 | clear |
| Jesse Motlop | — | 5 | 136 | 64.9 | 155 | +18 | clear |
| Sid Draper | — | 2 | 954 | 860.7 | 964 | +10 | clear |
| Dylan Patterson | — | 1 | 1184 | 516.2 | 1193 | +9 | clear |
| Josh Sinn | — | 5 | 205 | 122.1 | 213 | +8 | clear |
| Oliver Hannaford | — | 2 | 238 | 233.8 | 245 | +7 | clear |
| Ollie Lord | — | 6 | 127 | 17.9 | 133 | +7 | clear |
| Tew Jiath | — | 3 | 111 | 120.9 | 116 | +5 | clear |
| Harrison Oliver | — | 2 | 379 | 244.2 | 381 | +2 | clear |

## Board top-50 (A4 context) — CONTROL 7a07e369 · PREVIOUS efea88e5 · CURRENT 17243c16
| # | player | pos | CONTROL | PREVIOUS | CURRENT | D vs ctl | D vs prev |
|---|---|---|---|---|---|---|---|
| 1 | Harry Sheezel | MID | 8115 | 7151 | 11754 | +3639 | +4603 |
| 2 | Nick Daicos | MID | 8050 | 7002 | 11214 | +3164 | +4212 |
| 3 | Nasiah Wanganeen-Milera | MID | 6606 | 5794 | 9957 | +3351 | +4163 |
| 4 | Luke Jackson | RUCK | 7799 | 6803 | 9948 | +2149 | +3145 |
| 5 | Max Holmes | MID | 6269 | 5386 | 8910 | +2641 | +3524 |
| 6 | Errol Gulden | MID | 5983 | 5256 | 7918 | +1935 | +2662 |
| 7 | Tristan Xerri | RUCK | 6649 | 5795 | 7589 | +940 | +1794 |
| 8 | Will Ashcroft | MID | 5155 | 4768 | 7428 | +2273 | +2660 |
| 9 | Zak Butters | MID | 6059 | 5174 | 6721 | +662 | +1547 |
| 10 | Bailey Smith | MID | 5605 | 4715 | 6259 | +654 | +1544 |
| 11 | Josh Treacy | KPF | — | — | 6183 | — | — |
| 12 | Noah Anderson | MID | 4765 | 4091 | 5893 | +1128 | +1802 |
| 13 | Jason Horne-Francis | MID | 3996 | 3702 | 5850 | +1854 | +2148 |
| 14 | Finn Callaghan | MID | 5442 | 4904 | 5839 | +397 | +935 |
| 15 | Lachlan Ash | SD | 5187 | 4611 | 5672 | +485 | +1061 |
| 16 | Sam Darcy | KPF | 4013 | 4144 | 5619 | +1606 | +1475 |
| 17 | Tom Green | MID | 4391 | 4424 | 5530 | +1139 | +1106 |
| 18 | Izak Rankine | SF | 2768 | 2428 | 5292 | +2524 | +2864 |
| 19 | Matt Rowell | MID | 4185 | 3752 | 5185 | +1000 | +1433 |
| 20 | Jagga Smith | MID | 3192 | 2822 | 5135 | +1943 | +2313 |
| 21 | Jai Newcombe | MID | — | — | 4967 | — | — |
| 22 | Caleb Serong | MID | 4701 | 4170 | 4775 | +74 | +605 |
| 23 | Kysaiah Pickett | SF | 3496 | 3076 | 4665 | +1169 | +1589 |
| 24 | Riley Thilthorpe | KPF | 3818 | 3702 | 4513 | +695 | +811 |
| 25 | Colby McKercher | MID | 3829 | 3627 | 4488 | +659 | +861 |
| 26 | Bodhi Uwland | SD | — | — | 4350 | — | — |
| 27 | Ed Richards | MID | 3078 | 2625 | 4323 | +1245 | +1698 |
| 28 | Nick Blakey | SD | 3598 | 3266 | 4274 | +676 | +1008 |
| 29 | Brodie Grundy | RUCK | 3959 | 3314 | 4244 | +285 | +930 |
| 30 | Chad Warner | MID | — | — | 4190 | — | — |
| 31 | Jake Bowey | SD | 3096 | 2926 | 4188 | +1092 | +1262 |
| 32 | Nicholas Martin | MID | — | — | 4100 | — | — |
| 33 | Mac Andrew | KPD | 3691 | 3504 | 4085 | +394 | +581 |
| 34 | Harley Reid | MID | 3726 | 3549 | 4061 | +335 | +512 |
| 35 | Archie Roberts | SD | 4577 | 4668 | 4025 | -552 | -643 |
| 36 | Isaac Heeney | MID | 3981 | 3301 | 3971 | -10 | +670 |
| 37 | Ryley Sanders | MID | 4129 | 3926 | 3966 | -163 | +40 |
| 38 | Marcus Bontempelli | MID | 3721 | 3084 | 3816 | +95 | +732 |
| 39 | Nick Watson | SF | 3720 | 3538 | 3800 | +80 | +262 |
| 40 | Levi Ashcroft | MID | 3193 | 3028 | 3787 | +594 | +759 |
| 41 | Willem Duursma | MID | 4429 | 4110 | 3737 | -692 | -373 |
| 42 | Sam Lalor | MID | 3574 | 3337 | 3698 | +124 | +361 |
| 43 | Callum Wilkie | KPD | — | — | 3690 | — | — |
| 44 | Murphy Reid | SF | 3953 | 3742 | 3574 | -379 | -168 |
| 45 | Max Gawn | RUCK | 2538 | 2112 | 3554 | +1016 | +1442 |
| 46 | Timothy English | RUCK | 3349 | 2916 | 3525 | +176 | +609 |
| 47 | Jordan Clark | SD | 3307 | 3007 | 3364 | +57 | +357 |
| 48 | Connor Rozee | MID | 2392 | 2892 | 3357 | +965 | +465 |
| 49 | Zac Bailey | SF | 2519 | 2244 | 3345 | +826 | +1101 |
| 50 | Jack Sinclair | SD | — | — | 3314 | — | — |

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
