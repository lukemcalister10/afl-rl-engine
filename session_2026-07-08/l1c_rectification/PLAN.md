# PLAN — L1c EVIDENCE-CONDITIONED EXPECTED-RERATING CREDIT · 2026-07-08
**Directive: RECTIFICATION_BUILD_DIRECTIVE_L1C_v1 · effort High · mode auto (this PLAN = first committed
artifact) · time band: 4–6h (within the directive's 3–6h expectation; ~6 walk-forward book builds dominate).**

## FENCE (asserted)
Branch `claude/fable-wave-4-integration-w4rfpb`, head `e84833a53fa57f2b66e9533587c4d4b0d21e32fd` == directive
pin. Store `engine/rl_after/rl_model_data.json` md5 `e1b4d8bf` == pinned (Guard 5 PASS at bootstrap on this
branch; asserted again at exit). Workspace re-seeded from THIS branch (engine head 375b11ef). Out of scope:
PVC (RL_PVCFIT stays a dial), aging side, docs.

## THE LEVER AS I WILL BUILD IT
1. **Basis book (credit-off)**: walk-forward as-of matrix (s4_matrix machinery, evidence-truncated per year,
   backtest path) built with `RL_YOUNG=0` — the engine that "prices year-1 on delivered evidence only".
   The measured re-rating of THAT engine's prices is exactly the gap the credit pays forward (declared:
   one-shot derivation, no fixed-point iteration — the credit is measured off the credit-off book).
2. **Cell table (task 1)**: per cell = position-group (6) × played/sat-year-1, re-rating as a SMOOTH function
   of log-pick (adaptive-bandwidth Gaussian kernel grown until eff-n≥35 — the D14 V0-curve convention; never
   wide bins as one number). Measured quantity R = (kernel-weighted class SUM at career-year 2) /
   (kernel-weighted class SUM at career-year 1) − 1, attrition and busts included (a player out of the
   system contributes 0 to the y2 sum). Pooling rungs declared per cell: (pos × sat) → (KPP/nonKPP/RUC × sat)
   → (sat only) — finest rung the sample supports at max bandwidth; census reports n, rung, R, top-decile
   share. TRAILING: table_T uses only classes C with C+2 ≤ T (their y2 as-of values are data ≤ T — leak-free);
   T < first table (2006) ⇒ R=0, declared. Trailing-vs-full comparison printed once as evidence; TRAILING ships.
3. **Wiring (task 2)**: in `_merged_recover.py`, the W4 runway leg (`W4_YCRED·thin·yage·c_yng(k)` in `_w4_W`)
   is REPLACED (not stacked) by a multiplier applied inside the W4 `raw_ev` wrapper for real in-curve (ND/RD,
   picked) players:  `e' = e · (1 + w · R_cell(pos, pick, sat↔played blend, T=Y) · φ(g))`, with
   - `g` = career games ≤ Y (EVIDENCE QUANTITY, not career-year); `φ(g) = (1−g/G0)²` for g<G0 else 0 —
     smooth, φ(0)=1 (full at zero evidence ⇒ V0, day 0, carries the full credit by construction: V0 IS
     raw_ev at debut−1 with g=0), C¹ landing at G0; G0 derived from the store as the median cumulative games
     at end of career-year 3–4 for a normally-developing player (committed in the census).
   - sat↔played blend `s(g)=clip(g/6,0,1)`: R_eff = (1−s)·R_sat + s·R_played — no cliff at the first game.
   - R clipped ≥ 0 (fix direction: raise year-1, never cut young; measured-negative cells REPORTED as tension,
     never shipped as cuts).
   - CONTINUITY: the multiplier is continuous in g, pick (kernel curve), and time-in-career (no career-year
     key anywhere) ⇒ pick PVC → V0 → end-y1 → y2/3/4 sit on one curve; V0-boundary smoothness demonstrated
     numerically (task 5). D14 V0 laws hold by construction: the V0 curve refits on credited inputs and stays
     a function of (pos, draft-age, pick) only.
   - Kill-switch: existing `RL_YOUNG` (family unchanged, 8 switches); dial `RL_YCRED_W` default **0.7**
     (shipped). ALL-OFF byte-exact v2.5 (re-verified). Table loaded from committed
     `engine/rl_after/ycred_table.json`; absent table + switch on ⇒ HALT (no silent no-credit).
   - Engine-head pin in `data/expected_boot.json` bumped in the same commit as every engine edit; final head
     at close.
4. **Conforming G-COHORT script (task 3)**: `book_ratio.py` REWRITTEN (the avg(4-6)/avg(1-2) aggregation is
   the DECISIONS-obituary non-conformer): class-year SUMS per class 2004–2020 (incurve), AVERAGED across
   classes → one figure per career year; EACH of y4/y5/y6 vs min(y1,y2) ≤130 hard (guide 120–125);
   walk-forward basis asserted in code comments. VALIDATION: run on the untouched W4 candidate book first —
   must reproduce the audited breach figures (y1 57,558.5 · y2 70,211 · 142.4/140.8/131.7) before I trust it
   on the new book.
5. **Owner w-table (task 4)**: books at w∈{0.5,0.6,0.7,0.8} (4 matrix builds, parallelised 2-at-a-time on
   4 cores) → per-year ratios + y1/y2 sums; named before/after (baked v2.5 · W4-pre-L1c · each w): Willem
   Duursma, a top-3 pick, Gulden/Darcy/Goad shapes, one pure sit-out, one mature-age pick. Committed; 0.7
   ships as default, owner rules w on sight.
6. **Suite (task 5)**: ship_gates_check.py + panel (re-stamped CANDIDATE values, all-off still reproduces the
   baked panel byte-exact) + G-ATTR leave-one-out on RL_YOUNG (per-player separable delta) + A-DUUR direction
   + G-MONO incl. V0-boundary smoothness sweep + OQ-B: three narrowest margins named for the supervisor.
7. **Hypothesis test (task 6, report only)**: per-cell top-decile share of the class's y1→y2 (and y1→y4)
   re-rating gain; plain verdict on the owner's "few reach convex tiers" distribution story. Build nothing.

## RISKS / FLAGS
- The G-COHORT ratio at w=0.7 is NOT pre-committed to pass: early classes (2004–2005) get thin/zero trailing
  credit by leak-free construction, so the averaged y1 lifts less than the 2026 board's. The w-table is the
  owner's ruling surface; I report per-year ratios at 0.7 honestly, pass or fail.
- y2 sums also rise (partial φ at y2 evidence) — min(y1,y2) may stay y1; both figures reported per WD-1b.
- Panel re-stamp changes expected values — labelled CANDIDATE, baked panel reproduced with all-off (stated in
  the stamp comment), consistent with the W4 convention.
