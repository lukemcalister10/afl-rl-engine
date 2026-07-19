# DIRECTIVE — LEG F7 · THE RESIDUAL PICK-TAX DETERMINISM FIX · seat 14 · 2026-07-19
### Finish what F6 started. F6 froze the V0 surface (_iso_dec/_build_v0_curve) but the viewing render
### (item 389, PR #122) proved F6 is PARTIAL: on a non-clean container the balanced board flips 5/5 to
### d7a95e8d (Σv 750171, Sheezel −95) with v0surf loaded CORRECTLY — so a RESIDUAL weather-susceptible
### fit remains on the value path. Located: engine/rl_after/_merged_recover.py:463
### `IsotonicRegression(increasing=False).fit_transform(PICKS,raw)` (pick-tax / multiplier) + :466 (the
### _ISOFADE variant). Both run a fresh PAVA fit at EVERY board build; F6 cleared them as
### "kernel-invariant (14876ea15a8e)" on a CLEAN box (forced-coretype only) — INSUFFICIENT. GOAL: make
### the residual value-path fit deterministic across ALL containers, so EVERY box reproduces 06d8af60.
### Owner ruled B (extend the freeze), 2026-07-19.

## ★ THE PROOF BAR IS HIGHER THAN F6 — READ FIRST ★
F6's determinism clearance was forced-coretype on ONE CLEAN box, and it was WRONG. That check is
BANNED here as the sole determinism proof. The fix's determinism MUST be established by ONE of:
  (a) IDENTIFY the real trigger that makes :463/:466 flip (the render proved coretype is NOT it — find
      the actual knob: thread count, reduction order, numpy/BLAS build path, memory layout), REPRODUCE
      the d7a95e8d flip on demand with the CURRENT engine, then show the FIXED engine reproduces
      06d8af60 under that same trigger; OR
  (b) a rigorous BY-CONSTRUCTION argument: eliminate the non-deterministic op at the SOURCE (order-fix
      the BLAS/reduction feeding `raw`/`fs` with the file's existing `_det_*` pattern, and/or
      rational-quantise the isotonic input grid so PAVA near-ties resolve identically everywhere), PLUS
      a targeted op-level test showing that specific computation is now order/kernel-invariant, PLUS
      k=0 clean-box identity.
Forced-coretype-on-clean PASSING is necessary-not-sufficient and NEVER the whole proof.

## CLEAN-INSTANCE PRECONDITION (MANDATORY, FIRST — the CORRECTED LEGE=0 recipe)
Build the balanced board with **`RL_LEGE=0 RL_LEGF=0`**, single-thread (OPENBLAS/OMP/MKL/NUMEXPR=1),
PYTHONHASHSEED=0, v0surf LOAD mode. If it reproduces `06d8af60` byte-exact → CLEAN box: usable for the
k=0 identity proof, but you MUST still establish determinism per (a)/(b) — a clean box alone cannot
prove the residual is fixed. If it reproduces a WEATHER signature (d7a95e8d / Sheezel −95, or anything
≠ 06d8af60) → DIVERGING box: PRIZED — this is exactly where you prove the fix removes the flip. Either
way, DO NOT skip the determinism proof. (F6's first HALT was a wrong-env RL_LEGE=1 error — the board of
record is the RL_LEGE=0 board, rl_export.py:100; do not repeat it.)

## THE JOB (PLAN FIRST — the PLAN is commit #1, before any fix)
1. CONFIRM THE RESIDUAL is :463/:466 and it is COMPLETE. Neutralise them and show the board reproduces
   06d8af60 where it otherwise flips. If the board STILL flips, there is MORE residual — STOP and report
   the full set (candidates: rl_model.py isotonic/PAVA at 654/680/715/934; any other live
   fit_transform/.fit on the real-roster path). Do NOT fix a partial set.
2. DIAGNOSE where the weather enters :463/:466 — the upstream BLAS/reduction that computes `raw`/`fs`,
   or the isotonic PAVA tie-break itself? Name the exact op.
3. FIX AT THE SOURCE (preferred): order-fix / rational-quantise per (b) — deterministic BY CONSTRUCTION,
   NO new frozen artifact. FALLBACK (only if the source cannot be cleanly order-fixed): freeze the
   pick-tax table OUTPUT as a pinned pickle keyed by a deterministic signature (curve + roster geometry
   + gates, NEVER the weather-varying input) — the v0surf pattern EXACTLY, incl. Guard-5 wiring +
   expected_boot pin + ONE loud refit path + loud HALT on missing. State the chosen path in the PLAN.
4. PROVE per THE PROOF BAR (a) or (b).
5. REPORT the pre-fix RANK impact: does the d7a95e8d flip differ from 06d8af60 in RANKS, or values
   only? (closes item 389 — was option A ever rank-unsafe?).

## VALUE-NEUTRALITY (same bar as F6 — the fix moves NO value on a clean box)
k=0 row-diff (fixed vs pre-fix clean board) = 0 rows EMPTY · identity across all 4 configs (default
1f10220c · balanced 06d8af60 · forward d85901af · killsw RL_PVC2=0 9829d01a) · RL_LEGF=0 chain
byte-exact, phantom 0/804 · dormancy F3/F4/F5 PASS · store 968de0c7 · curve 56dd7a7b · q97m cfdc7321 ·
**v0surf 3af2b725 UNTOUCHED** (F7 does NOT re-freeze the V0 surface).

## GIT ENTRY (item-338 law)
`git fetch origin main claude/legf6-iso-freeze-bhigmd`; base = the F6 head
`540b62f3c1600178aabc56f2dd1ab59c68460b2b` (PR #121) STRICT, HALT on mismatch; F7 STACKS on #121.
Branch parent = the F6 head. THREADS=1. Provenance stamps at load: store 968de0c7 · v0surf 3af2b725.

## EFFORT: High. Why not Medium: F6 was Medium and its Medium-grade determinism proof (forced-coretype
on clean) MISSED this residual — the harder proof bar earns High. Why not Extra: still one localised
fit-site (+ its upstream), not a multi-lever integration. MODE: auto, PLAN first (the PLAN = the
diagnosis + the chosen fix path + the proof strategy, committed BEFORE any fix). TIME: ~1.5–2.5 h (the
diagnosis + the harder proof is the sink; flag >2×/<½× per S3). Reuse S5: the board/gate emitters,
board_diff, the F6 refit/probe scripts as templates.

## FENCE: IN = engine/rl_after/_merged_recover.py (the :463/:466 fix + any upstream order-fix) + IF the
freeze-output fallback is used: a new data/*.pkl + its data/expected_boot.json pin + boot_guard.py
wiring (additive, mirroring v0surf) + session_2026-07-19/legf7/ proofs. HARD-OUT: the store, curve,
q97m, **v0surf.pkl**, rl_model.py, distribution_pricing.py values, and docs — HALT on any HARD-OUT
need. Delete-don't-disable; carry an OBITUARY for anything retired.

## EXIT (RETURN ≤25 lines): the CONFIRM-RESIDUAL result + the determinism proof (a/b) FIRST, then k=0 +
identity ×4 + dormancy + untouched stamps + the pre-fix rank-impact finding; branch · head SHA · PR
(stacked on #121). S1–S6 · SILENCE IS A RED · halt-not-warn · findings not verdicts.
