# PLAN — READ CI'S ENVIRONMENT, THEN PIN WHAT THE MEASUREMENT NAMES
# branch: claude/ci-environment-measurement-names-zbqg78 · base: addef03 (open q97m PR head) · auto-mode, effort High

## BRANCH NOTE (read first)
The directive says BASE = `addef03` (STRICT EQUALITY) and "push to the SAME branch" (the open q97m
PR, `claude/q97m-freeze-determinism-s9v8ky`). The harness assigned me a *different* branch,
`claude/ci-environment-measurement-names-zbqg78`, and forbids pushing elsewhere "without explicit
permission". This session is non-interactive, so I cannot obtain that permission. Resolution: work is
BASED on `addef03` (satisfies the directive's strict-equality base + the technical dependency on the
freeze) and pushed to the harness-assigned branch. The supervisor can retarget/rebase onto the q97m
PR if that was the intent — the commits are a clean stack on `addef03`.

## THE TRAP THIS JOB EXISTS TO AVOID
P4 proved the board is *sensitive* to the OpenBLAS kernel (forcing SSE moves it). It did NOT prove the
kernel is what *differs in CI*. An untested alternative has the identical signature: **OPENBLAS thread
count** — N threads sum a dot product in a different order than 1 thread ⇒ the NW-smoother sums shift
⇒ the 72 runtime isotonic fits shift ⇒ the board shifts. The pinned box and a GitHub runner differ in
core count. Nobody has ever read CI's actual BLAS config, and CI does not print the board md5.
⇒ **MEASURE FIRST (Part 1). PIN ONLY WHAT PART 1 NAMES (Part 2). If neither threads nor kernel
recovers `3dc19fbb`, PIN NOTHING and report UNKNOWN.**

## GROUND TRUTH (verified live this session)
- Pinned board of record = `3dc19fbb` (data/expected_boot.json 'board', full 32-char).
- This box (the pinned box) rebuilds the board byte-identical = `3dc19fbb` ✓ (confirms A5/A1 basis).
- This box: OpenBLAS 0.3.31 DYNAMIC_ARCH, runtime arch = **SkylakeX (AVX512)**, **4 threads**, no
  OPENBLAS_*/OMP_*/MKL_* env vars set. CPU: Intel Xeon, avx512f+avx2+fma. numpy 2.4.4 / scipy 1.17.1
  / sklearn 1.8.0.
- CI (run 29332043147, addef039, ubuntu-24.04): panel FAILS on exactly 3 rucks — Gawn 2395 vs 2393,
  Goad 874 vs 873, Green 658 vs 655. Two prior runs identical ⇒ CI stably builds a *different* board.
  CI does NOT print the board md5 (confirmed in the log). config hash c2d233ae (matches pin).

## PART 1 — MEASURE (no code changes to engine, no pins)
- **E0**: add ONE diagnostic print line to the CI panel step of `.github/workflows/ci-guards.yml` —
  md5 of the board this run just built (`/home/claude/rl_workspace/rl_after/rl_app_data.json`). Output
  only; changes no step's verdict. This is permanent (A2 requires the panel to print the board md5).
- **E1**: dump the runner's full environment — `numpy.show_config()`, the resolved OpenBLAS
  kernel/CORETYPE + thread count (threadpoolctl), every OPENBLAS_*/OMP_*/MKL_*/NPY_* var already set,
  `/proc/cpuinfo` flags + CPU model + nproc, numpy/scipy/sklearn versions. Put side by side with the
  pinned box (dumped above).
- **E2**: on the runner, in ONE job (one CPU), build the board FOUR times, separately, md5 each:
  1. baseline (as CI runs today)
  2. `OPENBLAS_NUM_THREADS=1` — the untested threading hypothesis, tested first
  3. `OPENBLAS_CORETYPE=Haswell` — the kernel the pinned box's board is stable under (P4: AVX2 & AVX512
     both → `3dc19fbb`; Haswell is SIGILL-safe on every ubuntu runner; == the pinned box's board).
     Also capture what the runner picks by default so SkylakeX-vs-Haswell is unambiguous.
  4. both (`OPENBLAS_NUM_THREADS=1` + `OPENBLAS_CORETYPE=Haswell`)
  Mechanism: a SEPARATE temporary workflow `.github/workflows/ci-env-measure.yml` (measurement
  instrument, not part of the guard suite). It is REMOVED before finalizing — no permanent CI-logic
  change beyond the E0 print line.

### VERDICT RULE (target to recover = `3dc19fbb`)
- threads=1 alone recovers `3dc19fbb` ⇒ **THREADING**. Pin `OPENBLAS_NUM_THREADS=1`; do NOT pin CORETYPE.
- kernel alone recovers ⇒ **KERNEL**. Pin `OPENBLAS_CORETYPE`.
- only both recover ⇒ **BOTH**. Pin both.
- neither recovers ⇒ **UNKNOWN**. STOP. Pin nothing. Report.
- If CI's board md5 (E0) is neither `3dc19fbb` nor `935c2c29` ⇒ a third board — STOP and report.

## PART 2 — PIN WHAT PART 1 NAMED (only after Part 1 committed + verdict written)
- **F1**: pin in `bootstrap.sh` (every environment picks it up — CI, bake box, build sandbox), NOT in
  the CI workflow (CI-only pin makes CI green but does nothing for a bake).
- **F2**: ASSERT it in `boot_guard.py` — HALT if the pinned var is UNSET or WRONG, naming it. An
  unasserted pin is a wish. Three red-path proofs committed: unset ⇒ HALT; wrong ⇒ HALT; right ⇒ PASS.
- **F3**: record in `SHIP_GATES.md` as a FENCE not a cure — what is pinned, WHY, what it does NOT fix
  (the 72 runtime isotonic fits fed by BLAS-routed np.dot sums remain; the real repair is a separate
  job), and the trigger to remove it.

## ACCEPTANCE
A1 board does not move on the pinned box (`3dc19fbb`, byte-identical) — if it moves, STOP (Tier-1
escalates to Tier-1 and halts). A2 CI green AND panel prints board md5 == `3dc19fbb`. A3 the pin bites
(3 red-path proofs). A4 store untouched (`340a7a32`, no player value moves). A5 `81e48293` still
rebuilds at the tag's own tree.

## FENCE
IN: bootstrap.sh · boot_guard.py · data/expected_boot.json (if the pin is recorded there) ·
SHIP_GATES.md · ONE diagnostic print line in the CI panel step · session_2026-07-14/ci_env_pin/ ·
(temporary, then removed) .github/workflows/ci-env-measure.yml.
OUT: the store · board VALUES · every gate's construction · engine maths · docs/ · _merged_recover.py ·
the 72 isotonic fits and the RUC/V0/pick-curve path · every CI step's LOGIC · the two pre-existing
boot_guard holes (item 93).
