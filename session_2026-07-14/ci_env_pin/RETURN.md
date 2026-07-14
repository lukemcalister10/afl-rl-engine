# RETURN — ci-env-pin: READ CI'S ENVIRONMENT, THEN PIN WHAT THE MEASUREMENT NAMES
# 2026-07-14 · branch claude/ci-environment-measurement-names-zbqg78 · base addef03 (STRICT, verified ancestor)

## VERDICT IN ONE LINE
**UNKNOWN — the CI board mover is NEITHER the thread count NOR the OpenBLAS coretype. PIN NOTHING.**
The board of record `3dc19fbb` is produced only by the Intel **SkylakeX (AVX512)** BLAS kernel; the GitHub runner
is an **AMD EPYC without AVX512** and can only run the **Haswell (AVX2)** kernel, which no environment variable
can change. Part 2 (F1/F2/F3) is therefore NOT executed — there is nothing to pin.

## BRANCH / PUSH
Owner-ruled Option 2 (mid-session): work BASED on `addef03` (strict; `git merge-base --is-ancestor addef03 HEAD`
= YES), pushed to my assigned branch `claude/ci-environment-measurement-names-zbqg78`, my own PR. Not pushed to
the q97m branch. The "push to the same branch" line was withdrawn.

## E0 — CI'S BOARD MD5 (it had NEVER been printed)
Added one diagnostic print line to the ci-guards panel step. CI's board = **`62d23265ea2e9fb66c9f223a51a9aae2`**.
⚠ This is a **THIRD board — NEITHER `3dc19fbb` NOR the inferred SSE `935c2c29`.** The register's "CI builds the
SSE board" inference (item 101) is **refuted by the measured hash.** The panel still fails on the same 3 rucks
(Gawn 2395/2393 · Goad 874/873 · Green 658/655), so `62d23265` IS the board behind the CI red.

## E1 — CI vs THE PINNED BOX (full dump committed: E1_SIDE_BY_SIDE.md)
The ONLY material difference: the **CPU**. Runner = AMD EPYC 9V74, **no AVX512** → OpenBLAS resolves **Haswell**.
Pinned box = Intel Xeon, **AVX512** → OpenBLAS resolves **SkylakeX**. Thread count (4=4), library versions
(numpy 2.4.4 / scipy 1.17.1 / sklearn 1.8.0), threading layer (pthreads), and BLAS/thread env (none set on
either) are IDENTICAL. The board follows the kernel; the kernel follows the silicon.

## E2 — FOUR BOARD BUILDS ON THE RUNNER (full table: E2_RESULTS.md)
| run | forced env | resolved | board |
|---|---|---|---|
| 1 baseline | — | Haswell/4 | `62d23265` |
| 2 threads=1 | OPENBLAS_NUM_THREADS=1 | Haswell/1 | `62d23265` |
| 3 kernel | OPENBLAS_CORETYPE=Haswell | Haswell/4 | `62d23265` |
| 4 both | threads=1 + Haswell | Haswell/1 | `62d23265` |
All four identical; **none recovers `3dc19fbb`.** Threads pinned → no change (**threading REFUTED**). Coretype
pinned to Haswell → no change (**the runner is already Haswell; the pin is a no-op — INEFFECTIVE**).
**Pinning `OPENBLAS_CORETYPE` would have been R99.2's "guard that cannot fail." Run 3 proves it.**

Pinned-box corroboration (each build's resolved kernel VERIFIED via threadpoolctl, not assumed):
SkylakeX native → `3dc19fbb` · SkylakeX + threads=1 → `3dc19fbb` · **forced Haswell → `5546c120`** (a FOURTH hash,
reproduced twice). ⇒ the board is sensitive to **kernel generation** (SkylakeX `3dc19fbb` ≠ Haswell `5546c120`
on the SAME Intel box) AND to **CPU vendor within the same kernel name** (Intel-Haswell `5546c120` ≠ AMD-Haswell
`62d23265`), and NOT to threads. ⚠ **This refutes register item 101's "AVX2 Haswell == SkylakeX ⇒ 3dc19fbb".**
Most-likely reconciliation (flagged for the supervisor): P4's forced-Haswell almost certainly hit the **silent
coretype-fallback** — an unrecognized/unverified `OPENBLAS_CORETYPE` is ignored by OpenBLAS, which keeps the
native SkylakeX kernel and returns `3dc19fbb`. My builds verify the resolved arch each time, so they cannot make
that error. P4's "the board IS kernel-sensitive" still stands; "Haswell equals SkylakeX" does not.

## F1/F2/F3 — NOT DONE (by verdict)
Neither knob recovers the board ⇒ nothing to pin. No `bootstrap.sh` pin, no `boot_guard` assertion, no
`expected_boot.json` field, no `SHIP_GATES` fence. A pin here would be decorative (threads) or dead (coretype).

## ACCEPTANCE
- **A1 — PASS.** The board does NOT move on the pinned box: native `3dc19fbb`; threads=1 `3dc19fbb`; drift-and-
  restore returns to `3dc19fbb`. My changes moved no player value.
- **A2 — NOT MET, AND CANNOT BE by this job.** CI is RED (`62d23265`); the panel now PRINTS the board md5 (E0
  works), but it is `62d23265`, not `3dc19fbb`. Making CI green requires either a new board of record built on
  the runner's kernel class (changes player VALUES — out of fence) or removing the runtime BLAS-fed isotonic
  fits (the separate job). I did NOT adjust my way past this — I report it (SILENCE IS A RED; so is a faked green).
- **A3 — N/A** (no pin ⇒ no red-path proofs).
- **A4 — PASS.** Store untouched (`340a7a32`); no store file in the diff; no player value moved.
- **A5 — see A5_REBUILD.md** (81e48293 re-proved at the tag's own tree; hash printed there).

## IN PLAIN TERMS
We finally made CI tell us the exact fingerprint of the board it builds, and read the actual chips it runs on.
The answer is blunt: GitHub's machines are AMD chips without the AVX-512 math unit our reference machine has, so
their math library adds the same numbers in a slightly different order and three ruck values land a point or two
off. It is not the number of threads, and it is not a setting we can flip — you cannot tell an AMD chip to be an
Intel one. So we deliberately pinned NOTHING: a "fix" here would have been a knob that quietly does nothing while
we tell ourselves it is solved. The real repair is to compute those three fragile numbers once, save them, and
stop recomputing them on every machine — and that is a separate, already-identified job.
