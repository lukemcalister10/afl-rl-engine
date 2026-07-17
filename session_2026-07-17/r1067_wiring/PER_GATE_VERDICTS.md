# R106.7 — PER-GATE COMMITTED VERDICTS (item-295 cure)

ship_gates_check.py ran to completion (**not** env-killed; 454s) on head bea8fea8 / store 968de0c7 /
config c2d233ae / board 9829d01a. Its report: `session_2026-07-02/ship_gates_report_bea8fea8.md` (md5 d215c44d).
Constituent verdicts below, each with its source and exit status. **The sole hard HALT (G-COHORT 1.30 cap)
PASSES**; every FAIL is pre-existing (FAIL on CONTROL too / data-caused) or an expected re-seal flag — none is
engine-caused by this build.

| directive gate | result | exit | evidence |
|---|---|---|---|
| **Guard 5** (boot-store) | **PASS** | 0 | store 968de0c7 == pinned, rl_model a5fd3d7d == pinned, engine bea8fea8; asserted by boot_guard on entry to panel/selftest/ship_gates |
| **F1** (export parity, board==engine ev) | **PASS** | 0 | one_source_selftest: every board v == round(engine gated ev/1.0524), mismatches=0 |
| **F2** (book parity, book==board) | **PASS** | 0 | one_source_selftest: every shared board v == round(book cur/1.0524), mismatches=0 |
| **G-COHORT y-band** | **PASS ×3** | 0 | B1: y4=1.2692 y5=1.2748 y6=1.2314 vs hard ≤1.30 → PASS×3; guide 1.20–1.25 ADVISORY (margin reported, never gates); den=y1=71436.8 |
| **earned-component** | **PASS / FEATURE** | 0 | B6 ramp(0..14g) monotone, 0→6 rise +2153, no dips → PASS; B5 floor-as-pricing-feature (Luke-ruled, VARIANT A .05 tail): 60 saves, +2065 lift, lowered=0 |
| **A-PAIRS** | mixed (no NEW fail) | — | PASS: A1,A5,A6,A7,A8,A9,A10,A11,D14a/b/c. Pre-existing FAIL (FAIL on CONTROL): A2 Curtis (D7 ruling, unchanged), A3 Rozee [DC], A12 Travaglia/Smillie [DC]. A4 Reid rank 48 = **pre-existing on ee70335a** (v=3348 identical base↔new; "MOVED" flag is vs an older pre-flex snapshot, not this build). PENDING A13/A14 (PVC stage not run); STRUCK A15 |
| **E/B** | n/a in frozen suite | — | not separately enumerated in suite 764a0d91; the expected-vs-realized separation A8 (Berry/Tsatas 2.44x, need ≥2.00x) PASSES |
| **β / CI** | REPORTED (F13) | — | no β gate in the frozen suite; the spec β/CI gate is the KNOWN queued-re-seal matter (item-283 **F13**) — a red there is a REPORTED finding, not a halt. B2 leave-cohort-out separation PASSES (median \|IS-WF\| leakage 0.000 %-pts) |
| **Guard 4** (correction-sticks canary) | see guard4_canary_output.txt | (filled below) | guard_correction_canary.py, run separately per the selftest note |

## ship_gates VERDICT line
`DIFFERS-BY-DESIGN=1  FAIL=5  FEATURE=1  PASS=14  PENDING=4  STRUCK=1  (454s)`
- FAIL=5 = A2 + A3 + A4 + A12 (all pre-existing / data-caused, unchanged by this build) + **B4** (board md5
  9829d01a vs shipped ee70335a — the byte-agree gate flagging the board MOVED **by design**; re-seal flag).
- DIFFERS-BY-DESIGN=1 = B3 (book must be re-sealed at the bake — owner action).
- No engine-caused correctness regression. The board/book moved by design (§1b floor half); re-seal is owner-only.

## Bottom line
G-COHORT (sole hard HALT) GREEN. No sub-1.08 floor self-halt triggered. The build is a clean CANDIDATE;
tag/main promote + the B3/B4 re-seal remain owner-only.
