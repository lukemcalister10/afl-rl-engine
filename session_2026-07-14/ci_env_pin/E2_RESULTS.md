# E2 — THE FOUR HASHES, ON THE RUNNER ITSELF · VERDICT
# measured 2026-07-14 · ci-env-measure run 29335985967 (job 87095221044) · commit 19627570

## THE FOUR RUNNER BUILDS (one job, one runner, one CPU — AMD EPYC 9V74)
| run | forced env | OpenBLAS resolved | board md5 | recovers 3dc19fbb? |
|---|---|---|---|---|
| 1 baseline (as CI runs) | — | Haswell / 4 threads | `62d23265ea2e9fb66c9f223a51a9aae2` | NO |
| 2 threads pinned | `OPENBLAS_NUM_THREADS=1` | Haswell / 1 thread | `62d23265ea2e9fb66c9f223a51a9aae2` | NO |
| 3 kernel pinned | `OPENBLAS_CORETYPE=Haswell` | Haswell / 4 threads | `62d23265ea2e9fb66c9f223a51a9aae2` | NO |
| 4 both | threads=1 + Haswell | Haswell / 1 thread | `62d23265ea2e9fb66c9f223a51a9aae2` | NO |

**All four are IDENTICAL (`62d23265`). NONE recovers `3dc19fbb`.**

## ⚠ VERDICT: **UNKNOWN — the CI mover is neither the thread count nor the OpenBLAS coretype. PIN NOTHING.**
- Threads pinned (run 2): no change. **Threading is REFUTED as the CI mover.**
- Kernel pinned to Haswell (run 3): no change — because the runner's OpenBLAS ALREADY resolves to Haswell
  natively (DYNAMIC_ARCH, no AVX512 on the AMD runner). Forcing the coretype it already uses is a no-op.
  **`OPENBLAS_CORETYPE` is INEFFECTIVE on the runner.**
- Both (run 4): no change.
Per the directive's rubric: *NEITHER recovers `3dc19fbb` ⇒ the cause is something we have not named by these two
knobs. STOP. PIN NOTHING.* Pinning `OPENBLAS_CORETYPE` would have been the "guard that cannot fail" (R99.2) —
run 3 proves it changes nothing.

## ⚠ E0 STOP-CONDITION ALSO TRIPPED: CI's BOARD IS A **THIRD** BOARD
CI's actual board (E0 print, ci-guards run 29335985606 panel step) = **`62d23265ea2e9fb66c9f223a51a9aae2`** —
**neither `3dc19fbb` NOR the inferred SSE board `935c2c29`.** The "CI builds the SSE board" inference (register
item 101) is **REFUTED by the measured hash.** The runner is not running an SSE kernel — it runs the **Haswell
(AVX2)** kernel and still produces a board no env var recovers.

## PINNED-BOX CORROBORATION (this session's box: Intel Xeon, SkylakeX/AVX512)
| build | OpenBLAS resolved | board md5 |
|---|---|---|
| native | SkylakeX / 4 threads | `3dc19fbb…` (board of record) |
| `OPENBLAS_NUM_THREADS=1` | SkylakeX / 1 thread | `3dc19fbb…` (threads do NOT move it) |
| `OPENBLAS_CORETYPE=Haswell` | Haswell / 4 threads | **`5546c120…`** (a FOURTH hash) |

**This directly REFUTES register item 101's "AVX2 Haswell == SkylakeX ⇒ 3dc19fbb".** On this Intel box, forcing
the Haswell kernel yields `5546c120`, NOT `3dc19fbb`. And the runner's Haswell yields `62d23265`. So:
- the board is sensitive to **kernel generation** (SkylakeX `3dc19fbb` vs Haswell `5546c120` on the SAME Intel box), and
- the board is sensitive to **CPU vendor even within the same kernel name** (Intel-Haswell `5546c120` vs AMD-Haswell `62d23265`), and
- the board is **NOT** sensitive to thread count on either box.

## WHY NO PIN CAN FIX THIS
`3dc19fbb` is produced only by the Intel **SkylakeX (AVX512)** BLAS kernel. The AMD GitHub runner **physically
lacks AVX512**, so it can never run SkylakeX — no `OPENBLAS_CORETYPE` value makes AVX512 hardware appear. Even
forcing both machines to the same-named Haswell kernel does not agree (`5546c120` ≠ `62d23265`). Therefore the
two env vars in scope (`OPENBLAS_NUM_THREADS`, `OPENBLAS_CORETYPE`) **cannot** make the runner reproduce the
board of record. The residual is the 72 runtime isotonic fits fed by BLAS-routed `np.dot` NW-smoother sums,
whose float results differ by CPU microarchitecture/vendor. **The real repair — removing the runtime fits (bake
them once, load them) — is the fenced-OUT separate job.**
