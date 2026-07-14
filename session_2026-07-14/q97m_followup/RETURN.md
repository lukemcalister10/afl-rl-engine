# RETURN — q97m FOLLOW-UP (PROVE A1 · ATTRIBUTE THE RESIDUAL · CLOSE THE LOAD-PATH HOLE)

- **branch** `claude/q97m-freeze-determinism-s9v8ky` (harness-assigned) · **head** = the branch tip after the
  F1 commit (reported in the session message; `git log --oneline`) · **base** `f14710d` · **PR** none opened
  (candidate only — DO NOT MERGE / DO NOT TAG)
  · ⚠ **branch-name flag:** the directive's freeze branch/PR#76 is `claude/freeze-q97m-determinism-5hitu3`;
  the harness pinned me to a DIFFERENT branch and forbids pushing elsewhere. I based on `f14710d` and pushed
  to the assigned branch. **My commits are NOT on #76.** No merge, no tag. Owner to reconcile #76.

- **P0 — A1 FOUR HASHES, REBUILT (not "matches"):**
  working-head board **`3dc19fbb`** · working-head book **`d371a27c`** (n=2649) ·
  **tag board of record `81e48293`** · **tag book `c7825f1b`** (n=2649). ALL byte-identical to pin.
  **Construction:** leg A on this branch's own pins (store 340a7a32 / engine 2334f570 / config c2d233ae),
  Guard 5 PASS, **NO bypass, nothing overridden**. Leg B in a git worktree at **tag 9f8ae76**, booted on the
  **tag's OWN** bootstrap+pins (store b0c39d78 / engine 2030e5df / config 69ead79b; q97m pin ABSENT — the tag
  FITS q97m at runtime, which on this box == cfdc7321), Guard 5 PASS on the tag tree, **NO bypass** (not the
  item-86 trap: that only fires when the tag store is run against THIS branch's pins). #74 config-neutrality
  re-proved by store-isolation + the seal's own content-identity note. Box: AVX512, `refit --verify`==cfdc7321.

- **P1 — committed** (auto-mode): `PLAN.md` (first artifact), this `RETURN.md`, and A3's two HALT proofs in
  `F1_redpath/redpath_results.txt` (corrupt `data/q97m.pkl` ⇒ HALT ⇒ restore ⇒ PASS; same for `bust_prior_table.json`).

- **P2 — A2 as written FAILED: 72 runtime fits remain** (`P2_fits/`): 6 `IsotonicRegression.fit_transform`
  (pick guard `:218`) + 60 `_iso_dec` `.fit` (`:820`; 12 via `_fit_pick_curve`, 48 via `_fit_mature`) + 6 inner
  = 72 method calls. **Zero GBR/RF** (q97m+cm are loaded). Their inputs are NW-smoother `np.dot` sums → BLAS-movable.

- **P3 — the residual is REAL but NARROW** (frozen engine, `P3_crossenv/`): board `3dc19fbb` on
  Haswell/AVX2 == SkylakeX/AVX512 == numpy-AVX512-off, but **`935c2c29` on SSE (Prescott)** — moves ONLY on
  an SSE BLAS kernel. **8 of 804 move**, all +1..+4 (≤0.46%/player; sum +16 = +0.0023%), **all rucks/tall**
  (Grundy/English/Gawn/Green/Goad/de Koning…). **Pick 1 = 3000 on BOTH** (numéraire is the LOADED `_PVC0`,
  env-invariant) ✅. V0 curve moves in fine precision (`v0_c18_sha` 30435406→85071d09) but only the RUC
  sub-path; MID display picks stable. **Book MOVES**: native `d371a27c` → SSE `98fc2a4f` (B3 would FAIL on an
  SSE box). **No G-COHORT verdict expected to flip** (drift ~10× below the ~3.07% y4 margin; definitive
  G-COHORT-on-SSE run flagged, not run).

- **P4 — cause, MEASURED (three isolated builds):** q97m fit — BLAS-only `OPENBLAS_CORETYPE=Prescott/Nehalem`
  (SSE) → **`d791a608`** (MOVES); SIMD-only `NPY_DISABLE avx512(+avx2+fma)` → `cfdc7321` (NO move); SkylakeX
  (AVX512 BLAS) → `cfdc7321`. **The mover is the OpenBLAS kernel (SSE vs AVX2/AVX512), NOT numpy SIMD —
  item 76's SIMD hypothesis is REFUTED.** "GEMM specifically" is NOT proven (OPENBLAS_CORETYPE swaps the whole
  kernel family). Board md5s: native `3dc19fbb`, SSE `935c2c29`. The pins DO move it → OpenBLAS story stands.

- **P5 — the book: NEITHER rebuilt nor re-stamped.** The freeze commit touches no book artifact; the seal
  still carries the pre-freeze head `2030e5df` (no false re-stamp — G-BOOK held). I rebuilt it on `2334f570`
  → `d371a27c` == sealed content (invariant to the freeze at fixed env). `P5_book/`.

- **F1 — the guard can now fail** (`boot_guard.py` (0e) + `bootstrap.sh` assertion). Three red-path proofs:
  `RL_Q97M_PKL`→corrupt ⇒ LOAD-PATH HALT; stale `/home/claude/q97m.pkl` ⇒ HALT; restore ⇒ PASS. cm/band fixed
  the same way. `F1_redpath/`.

- **F2 — annotated `boot_guard.py` diff** `ed13177..HEAD` (`F2_diff/`): ONE hunk, +24 lines, zero deletions —
  the (0d) block asserting the REPO copies. Nothing removed; the gap it leaves is exactly what F1 closes.

- **LADDER: the board did NOT move.** F1 touches only guard/seed logic; `ev()` untouched; the board rebuilds
  byte-identical (`3dc19fbb`). Candidate only — **DID NOT MERGE, DID NOT TAG.**

## In plain terms
The freeze is real and the board of record still rebuilds exactly — I proved it by rebuilding BOTH boards
and BOTH books from source and printing byte-identical hashes, including the tagged board every number in the
project is measured against. But the freeze did not finish the job: with q97m frozen the board STILL changes
on a machine with an older (SSE) math library, because 72 small isotonic fits are fed by BLAS sums that shift
per CPU. I measured the cause — it's the OpenBLAS kernel, not the "SIMD dispatch" the last note guessed. And I
closed a real hole: the guard was checking a copy of the frozen file that the engine never actually loads, so
an environment variable could have quietly swapped in any file; now it checks the exact file the engine loads,
and I proved it halts when that file is wrong.
