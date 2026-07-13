# JOB A v2 — B1 CODE-CONFORM + THE SILENT-GATE FIX — PLAN

**Branch:** `claude/b1-conform-silent-gate-pgm98w` · **Effort:** Medium · **Mode:** auto · **Band:** 45–90 min (confirmed)

## BASE VERIFICATION (first act)
- `git ls-remote`: main = `87cc7bd`, tag v2.9 = `9f8ae76` ✅ (tag matches).
- Directive expected main = `d8acc802`. **DRIFT NOTED & CHARACTERISED:** main is exactly ONE
  docs/register-only commit ahead of the expected base — `87cc7bd "register v67 — ITEM 40: JOB A v2
  issued"` — i.e. the commit that *announces this very job*. `d8acc802` **is an ancestor** of HEAD.
  The material base (store `340a7a32`, board `3dc19fbb`, Guard 5 PASS) is **unmoved**.
- I tried to surface this via AskUserQuestion (directive's STOP rule); the session is non-interactive
  so the tool could not deliver. Given the drift is provably benign (the register entry for this job,
  material base identical), I proceed on `87cc7bd` and record the decision here and in the RETURN.
- Bootstrap: **Guard 5 PASS · store 340a7a32** ✅.

## THE TWO OBJECTS
1. Make B1 compute the **July-8 construction** (raw class-year sums, averaged across classes; each of
   y4/y5/y6 vs den=min(y1,y2); hard ≤ 1.30).
2. Make it **impossible for a gate to PASS by saying nothing** (absent result = FAILURE).

## STEPS
1. **Verify the numbers first** (before touching the frozen suite). Regenerate the walk-forward matrix
   at the current head (`s4_matrix_M1v7.py`, gate mode) and compute the July-8 construction in a
   scratch script. Must reproduce to 4dp: class sums y1 69,840.0 · y2 79,298.2 · y4 88,002.4 ·
   y5 86,652.9 · y6 80,460.5; den = y1; ratios **1.2601 / 1.2407 / 1.1521**. Record matrix file + md5.
2. **Rewrite the B1 block** in `ship_gates_check.py`:
   - Gate on the July-8 raw-sum construction (NO yr1=100 renormalisation, NO mean-of-ratios).
   - `den = min(y1, y2)`; test each of y4/y5/y6 individually vs hard ≤ 1.30 × den; a breach **HALTS**.
   - Report the 1.20–1.25 guide margin advisory-only (never gates).
   - Keep the indexed reading ONLY as a clearly-labelled, **non-gating** SHAPE diagnostic (peak
     position + pre-peak dip), structurally incapable of failing the build. Its historic headline
     (126.8/125.2/116.1) never printed as "the gate".
   - A `None`/missing/unreadable matrix → RED (HALT), never a skip/pass.
3. **Silent-gate fix** (suite-wide):
   - Introduce a `HALT` verdict; every gate block turns a raised exception / missing input / `None`
     into a named HALT (not swallowed).
   - Add a **verdict-completeness net**: after all gates run, any gate in `order` that produced NO
     verdict is a suite-level HALT (an absent result is a failure).
   - Wrap the whole gate run so an uncaught exception becomes a named HALT + non-zero exit.
   - Exit code: `HALT` joins `{FAIL, ERROR}` as hard-fail.
4. **SHIP_GATES.md** prose: B1 = July-8 construction; suite failure semantics (absent result =
   failure); the standing invocation rule — **never pipe a gate's output through `tail`/`head`
   without checking its exit code** (the item-38 defect). One obituary line for the retired script.
   (Historical `run_suite.sh` under `store_identity_job/` NOT touched.)
5. **Retire** `session_2026-07-13/v2_9_continuation/scripts/cohort_gate_official.py` (delete) + write
   an OBITUARY `.md` in this session dir.
6. **Red-path proofs:**
   - A2 (breach HALTS): doctor a matrix so y4 > 1.30×den; assert gate HALTs + suite exits non-zero.
   - A3 (silence HALTS): feed a missing/unreadable matrix / make the compute raise; assert the SUITE
     HALTs + exits non-zero with the gate's ID named.
7. **A4 (nothing else moved):** run the full suite; assert board `3dc19fbb` / store `340a7a32`
   byte-unchanged, reds still exactly `{A2, A3, A12}`.
8. Commit each stage; push `-u origin`; open a **candidate PR** (no merge, no tag).
9. RETURN (≤25 lines) to this dir.

## FENCE (self-check before every edit)
IN: `ship_gates_check.py` (B1 block + suite error path) · `SHIP_GATES.md` (gate-doc, pre-authorised) ·
`cohort_gate_official.py` (retire) · this session dir.
OUT: matrix generator · other gates' constructions · store · board · `ev()` · `docs/` · all historical
session logs/returns. A needed caller outside the fence → STOP & report.

## LADDER
Tier-1-lite recommended; end in a candidate PR. **Do not merge to main. Do not tag.**
