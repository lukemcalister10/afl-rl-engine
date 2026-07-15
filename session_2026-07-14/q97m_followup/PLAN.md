# PLAN — q97m FOLLOW-UP: PROVE A1, ATTRIBUTE THE RESIDUAL, CLOSE THE LOAD-PATH HOLE
**auto mode. This PLAN is the first committed artifact (the last chat committed none).**
branch `claude/q97m-freeze-determinism-s9v8ky` @ BASE `f14710d` (== directive BASE; based on ed13177/PR#74).
effort band: **Extra** (confirmed). Box: **AVX512** (avx512f/bw/cd/dq/vl), OpenBLAS DYNAMIC_ARCH→Haswell,
numpy dispatch AVX512_ICL/SPR — i.e. this box is the **bake-box analog**; the CI-red non-AVX512 environment
is simulated on the same box via `NPY_DISABLE_CPU_FEATURES` (numpy SIMD) and `OPENBLAS_CORETYPE` (BLAS kernel).

## ⚠ Branch-name discrepancy (flagged for the owner, not resolved by me)
The harness assigned me branch `claude/q97m-freeze-determinism-s9v8ky`. The directive's freeze branch (PR #76)
is `claude/freeze-q97m-determinism-5hitu3`. Harness rule is hard ("NEVER push to a different branch"), so I
base on `f14710d` and push to the assigned branch. **This means my commits do NOT land on #76's branch.**
I do NOT merge or tag anything. The owner must decide whether to repoint #76 or open a PR on this branch.

## PART 1 — PROOF & ATTRIBUTION (NO CODE CHANGES)
- **P0 (outranks all):** rebuild BOTH boards + BOTH books; print 4 hashes; state construction in full incl.
  any guard bypass. Leg A = working-head board (expect `3dc19fbb`, store `340a7a32`, engine `2334f570`,
  config `c2d233ae`), on this branch, no bypass. Leg B = tag board of record (expect `81e48293`, store
  `b0c39d78`, tag `9f8ae76`, engine `2030e5df`, config `69ead79b`) — via a git worktree at the tag, its own
  bootstrap/pins (no false-halt, no bypass); also build at config `c2d233ae` to re-prove #74 board-neutrality.
  Books = the B3 stable_sha256 (id(p)-keyed raw bytes are non-deterministic by design). Commit → `A1_PROOF/`.
- **P1:** commit PLAN (this file), RETURN, and A3's two HALT proofs (corrupt `data/q97m.pkl` ⇒ HALT naming
  it ⇒ restore ⇒ PASS; same for one newly-pinned artifact e.g. `bust_prior_table.json`).
- **P2:** enumerate ALL runtime `.fit`/`.fit_transform` (the "72") by instrumenting a real engine load —
  file·line·what it fits·what feeds it·what consumes output·cross-env movability. Rank by what they touch.
- **P3:** on the non-AVX512 sim vs AVX512: how many of the 804 move; the pick curve (V0 + priced picks
  1,2,3,5,10,20,30,50,70) side by side, does pick-1 still price 3000; the book; can any guard verdict flip
  (y4 1.2601 vs 1.30). Measured on BOTH the frozen engine (residual) and the unfrozen tag engine (original).
- **P4:** three SEPARATE builds — baseline / BLAS-only (`OPENBLAS_CORETYPE`) / SIMD-only
  (`NPY_DISABLE_CPU_FEATURES`) — sharpest at the q97m FIT via `refit_q97m.py --verify` (isolates the mover),
  plus board md5. If neither pin moves it: **say the cause is UNKNOWN.**
- **P5:** book rebuilt or re-stamped — one word + evidence (the freeze commit touched no book artifact; the
  seal still carries head `2030e5df`). Confirm by regenerating on `2334f570`.

## PART 2 — ONE FIX (start only after Part 1 committed)
- **F1:** `boot_guard.py` — add a LOADED-PATH assertion (block 0e) that resolves q97m through the engine's
  precedence (`$RL_Q97M_PKL`→`/home/claude/q97m.pkl`→`<repo>/data/q97m.pkl`) and cm through
  `/home/claude/cm_<trees>.pkl`, and asserts THAT path's md5 == pin; HALT names resolved + expected. Keep the
  existing (0d) repo-checkout assertion. `bootstrap.sh`: add an explicit q97m assertion (F1 assertion only).
  RED-PATH proofs: `$RL_Q97M_PKL`→corrupt ⇒ HALT; stale workspace copy ⇒ HALT; restore ⇒ PASS. Commit all 3.
- **F2:** annotated line-by-line `boot_guard.py` diff `ed13177..HEAD` (disclosure only). ✅ drafted.

## LADDER / FENCE
The board MUST NOT MOVE — if any player's value moves, STOP AND REPORT. IN: `boot_guard.py`, `bootstrap.sh`
(F1 assertion only), `session_2026-07-14/q97m_followup/`, the Part-1 artifacts. OUT: the residual mover
(`_iso_dec`, `_build_ruc_ceiling`, RUC V0 path, `_fit_pick_curve`, the pick curve), the store, board values,
gate construction, engine maths, `docs/`, CI steps. Candidate only — DO NOT MERGE, DO NOT TAG.

## SPEED
Long computes backgrounded with markers; polled, not blocked. One store/engine-adjacent writer at a time.
