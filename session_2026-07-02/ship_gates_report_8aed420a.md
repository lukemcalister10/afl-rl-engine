# ship_gates_check report — head 8aed420a store 644d1254
```
=== SHIP GATES BOARD — head 8aed420a store 644d1254 — suite 764a0d91 — 2026-07-02 ===
A1        PASS     Duursma>Uwland: 4179 vs 1781
A2        FAIL     Curtis>Ward: 1162 vs 1782; Weddle>Ward: 1628 vs 1782
A3   [DC] FAIL     Connor Rozee: 2026=2679 2025=3874 ratio=0.69 (need >=0.80)
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A4        PASS     Harley Reid board rank=32 ev=3523 (need TOP 40)
A5        FAIL     Jack Ginnivan=1578 (floor 1600); Jake Bowey=2585 (floor 2100); Nick Blakey=3053 (floor 2600) [SCAR floors — RE-BASE if PVC re-levels]
A6        PASS     yr1-3 RUC median=314 (n=13, pooled — thin slice) vs pick-matched MID kernel median=502 (n=66, bw=0.6 log-pick, RATIFIED 02/07)
A7        PASS     Ryan Maric: fut-dominant=MID(60%) gfut=MID (need MID/MID); Ed Langdon: fut-dominant=GDEF(70%) gfut=GEN_DEF (need GDEF/GEN_DEF)
A8   [DC] PASS     Berry=3473 vs 2x Tsatas=2166 (Tsatas=1083)
A9        FAIL     Ginnivan>Ward: 1578 vs 1782
A10  [DC] FAIL     Charlie Curnow: 2026=944 2025=1849 ratio=0.51 (need >=0.70)
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A11  [DC] PASS     Farrow>Patterson: 1641 vs 982; Cumming>Annable: 2002 vs 936
A12  [DC] FAIL     Travaglia>Moraes: 601 vs 876; Smillie>Retschko: 896 vs 730
          triage: [DC] gate — attribute ENGINE- vs DATA-caused BEFORE this blocks (SHIP_GATES PROCESS)
A13       PENDING  PVC stage not run; advisory vs stand-in PVC[1]=3000: George Wardlaw=3035 lineball=True; Levi Ashcroft=3271 lineball=True
A14       PENDING  PVC stage not run; advisory vs stand-in PVC[8]=1704: Trent Rivers=1725 lineball=True; Zach Reid=1680 lineball=True; Jase Burgoyne=2191 lineball=False
A15       STRUCK   Luke 02/07/2026 — convexity dimension seeded as V_NEXT #1
B1        PASS     pooled peak N=4 R(peak)=160 (need peak by yr4-5, yr6 acceptable, >100; pre-peak dips <5% tolerated, path_ok=True; no yr6-hold required — Luke 02/07); cohorts rising to yr4-6 above yr1: 17/17; matrix=s4_matrix_nogames.json
B2        PASS     median |IS-WF| leakage=0.0 %-pts (DECLARED tol 5.0); GOOD>BUST separation: GEN_DEF 52/1, GEN_FWD 44/1, KEY_DEF 60/1, KEY_FWD 64/1, MID 52/0
B3        PENDING  book-gate set not yet enumerated as scripted checks — definition proposal in report; book headline shape covered by B1
B4        FAIL     regenerated rl_app_data.json md5=1898ead7 vs shipped b8f9e998 (byte-agree gate; export exit=0)
B5        FAIL     9 yr1-2 LISTED picked players below 0.25x draftval (floor PROVISIONAL; listed-only per Luke 02/07); worst: Jack Watkins=18/dv308; Flynn Perez=39/dv308; Zac Banch=45/dv308
B6        FAIL     ramp(0..14g)=[745, 745, 745, 745, 745, 745, 3263, 3352, 3357, 3538, 3318, 3464, 3531, 3583, 3578]; dips(more games worth less)=[(9, -220.0), (13, -5.0)]; 0->6 rise T=+2518; 0->6 steps>50%T=[(5, 2518)]; rise by 3g=+0 (need >=630) [whole-ramp re-spec, DECLARED thresholds]
C1        PENDING  naive-baseline book not yet built — definition proposal in report (needs its own directive)
C2        PENDING  V1-pick-model book not yet built — definition proposal in report (needs its own directive)
VERDICT: FAIL=9  PASS=8  PENDING=5  STRUCK=1  (104s)
```

## Supporting detail

B1 per-cohort table:
  cohort 2004: peakN=5 R={1:100, 2:139, 3:168, 4:175, 5:190, 6:168, 7:146}
  cohort 2005: peakN=4 R={1:100, 2:145, 3:148, 4:203, 5:185, 6:179, 7:157}
  cohort 2006: peakN=5 R={1:100, 2:142, 3:159, 4:178, 5:180, 6:172, 7:148}
  cohort 2007: peakN=5 R={1:100, 2:133, 3:128, 4:140, 5:166, 6:155, 7:135}
  cohort 2008: peakN=4 R={1:100, 2:134, 3:181, 4:197, 5:177, 6:158, 7:139}
  cohort 2009: peakN=2 R={1:100, 2:122, 3:111, 4:114, 5:117, 6:104, 7:91}
  cohort 2010: peakN=4 R={1:100, 2:143, 3:160, 4:178, 5:169, 6:153, 7:130}
  cohort 2011: peakN=4 R={1:100, 2:136, 3:167, 4:192, 5:187, 6:174, 7:142}
  cohort 2012: peakN=4 R={1:100, 2:123, 3:136, 4:140, 5:135, 6:128, 7:106}
  cohort 2013: peakN=5 R={1:100, 2:137, 3:159, 4:192, 5:193, 6:167, 7:129}
  cohort 2014: peakN=4 R={1:100, 2:134, 3:156, 4:169, 5:156, 6:150, 7:145}
  cohort 2015: peakN=4 R={1:100, 2:126, 3:131, 4:136, 5:135, 6:134, 7:123}
  cohort 2016: peakN=4 R={1:100, 2:138, 3:157, 4:183, 5:174, 6:175, 7:152}
  cohort 2017: peakN=3 R={1:100, 2:119, 3:125, 4:115, 5:109, 6:105, 7:98}
  cohort 2018: peakN=4 R={1:100, 2:126, 3:134, 4:144, 5:139, 6:128, 7:118}
  cohort 2019: peakN=5 R={1:100, 2:132, 3:148, 4:162, 5:170, 6:151, 7:135}
  cohort 2020: peakN=3 R={1:100, 2:112, 3:118, 4:109, 5:110, 6:110}

## Board top-50 (A4 context)
  1. Luke Jackson             RUC         7731
  2. Harry Sheezel            MID         7287
  3. Nick Daicos              MID         7059
  4. Nasiah Wanganeen-Milera  MID         5730
  5. Tristan Xerri            RUC         5469
  6. Max Holmes               MID         5154
  7. Bailey Smith             MID         5122
  8. Zak Butters              MID         5020
  9. Errol Gulden             MID         4947
 10. Josh Treacy              KEY_FWD     4928
 11. Will Ashcroft            MID         4885
 12. Archie Roberts           GEN_DEF     4625
 13. Finn Callaghan           MID         4538
 14. Caleb Serong             MID         4276
 15. Ryley Sanders            MID         4268
 16. Noah Anderson            MID         4216
 17. Willem Duursma           MID         4179
 18. Jason Horne-Francis      MID         4050
 19. Jai Newcombe             MID         3991
 20. Tom Green                MID         3950
 21. Lachlan Ash              GEN_DEF     3934
 22. Sam Darcy                KEY_FWD     3902
 23. Colby McKercher          MID         3862
 24. Kysaiah Pickett          GEN_FWD     3860
 25. Murphy Reid              GEN_FWD     3819
 26. Riley Thilthorpe         KEY_FWD     3649
 27. Matt Rowell              MID         3628
 28. Darcy Wilmot             GEN_DEF     3606
 29. Nick Watson              GEN_FWD     3598
 30. Mac Andrew               KEY_DEF     3569
 31. Sam Lalor                MID         3552
 32. Harley Reid              MID         3523
 33. Sam Berry                MID         3473
 34. Finn O'Sullivan          MID         3467
 35. Bodhi Uwland             GEN_DEF     3376
 36. Josh Worrell             GEN_DEF     3341
 37. Brodie Grundy            RUC         3318
 38. Isaac Heeney             MID         3298
 39. Chad Warner              MID         3297
 40. Levi Ashcroft            MID         3271
 41. Jagga Smith              MID         3270
 42. Jordan Clark             GEN_DEF     3123
 43. Marcus Bontempelli       MID         3101
 44. Christian Petracca       MID         3057
 45. Nick Blakey              GEN_DEF     3053
 46. George Wardlaw           MID         3035
 47. Luke Davies-Uniacke      MID         2967
 48. Reuben Ginbey            KEY_DEF     2896
 49. Timothy English          RUC         2893
 50. Logan Morris             KEY_FWD     2879

## C1/C2 DEFINITION PROPOSAL (for supervisor ruling)
Rebuild the walk-forward book (s4 matrix protocol, as-of values, only <=T data) twice more:
(a) NAIVE BASELINE: last-2-season era-adjusted avg -> value via simple age curve + position multipliers;
(b) ORIGINAL V1 PICK MODEL: value = PVC(effective pick) with the V1 age/tenure profile.
Headline metrics, engine must beat both on: (1) within-player GATE-1 protocol (WF good/bust separation,
leakage-matched); (2) rank correlation of as-of value vs realized fwd best-3 production (real_mat);
(3) cohort growth-law shape error vs the realized production curve. Each becomes C1x/C2x scripted lines.
