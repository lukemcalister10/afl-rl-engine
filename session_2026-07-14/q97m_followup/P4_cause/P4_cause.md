# P4 — THE CAUSE TEST: three separate builds, each knob isolated

**The last return asserted "the mover is the OpenBLAS GEMM kernel" WITHOUT running the test. Here it is run.**
Each knob is varied ALONE, holding the others native. Sharpest at the q97m FIT itself, via
`refit_q97m.py --verify` (in-memory fit → md5), the exact object the freeze froze; then at the board.

## The q97m FIT under each isolated knob (native/pin = `cfdc7321`)
| build | knob | q97m fit md5 | moved? |
|---|---|---|---|
| baseline | native (Haswell/AVX2 BLAS, full numpy SIMD incl AVX512) | `cfdc73216c099e5e8f1fda3968f31c00` | — (== pin) |
| **BLAS-only** | `OPENBLAS_CORETYPE=Prescott` (SSE) | **`d791a608bb6fa264877fff418fb09d8d`** | **YES** |
| **BLAS-only** | `OPENBLAS_CORETYPE=Nehalem` (SSE) | **`d791a608…`** | **YES** (== Prescott) |
| BLAS-only | `OPENBLAS_CORETYPE=SkylakeX` (AVX512) | `cfdc73216c099e5e8f1fda3968f31c00` | no (== native AVX2) |
| **SIMD-only** | `NPY_DISABLE_CPU_FEATURES=<all AVX512>` | `cfdc73216c099e5e8f1fda3968f31c00` | **no** |
| **SIMD-only** | `NPY_DISABLE_CPU_FEATURES=<AVX512+AVX2+FMA>` (down to SSE2 baseline) | `cfdc73216c099e5e8f1fda3968f31c00` | **no** |
| combined | `Prescott` + `NPY_DISABLE avx512` | `d791a608…` (== Prescott alone) | YES (BLAS dominates) |

## The BOARD (frozen engine 2334f570, q97m LOADED) under each knob (native/pin = `3dc19fbb`)
| build | knob | board md5 | moved? |
|---|---|---|---|
| baseline | native (Haswell/AVX2) | `3dc19fbbf920958affe7c6a2be9697d2` | — (== pin) |
| non-AVX512 | `Prescott` (SSE) + `NPY_DISABLE avx512` | **`935c2c297288dd699584d5857305f32d`** | **YES** |
| SSE-only | `Prescott` + `NPY_DISABLE avx512+avx2+fma` | `935c2c29…` | YES (== above; numpy adds nothing) |

*(SkylakeX and numpy-SIMD-off-only board builds: see `P3_crossenv/isolation.txt`.)*

## Verdict — MEASURED, not asserted
1. **The mover is the OpenBLAS kernel selection (`OPENBLAS_CORETYPE`), NOT numpy's SIMD dispatch.**
   Disabling numpy SIMD entirely — AVX512, then AVX2 and FMA too, down to the SSE2 baseline — leaves the
   q97m fit **byte-identical** (`cfdc7321`). Only changing the BLAS kernel moves it.
   **This REFUTES item 76's hypothesis** ("a likelier driver is numpy's SIMD dispatch"). The SIMD-dispatch
   story is dead — measured dead.
2. **The split is SSE vs AVX2/AVX512, not "AVX512 vs not".** Haswell (AVX2) and SkylakeX (AVX512) BLAS
   kernels AGREE (`cfdc7321`); only the SSE kernels (Prescott/Nehalem) differ (`d791a608`). So the cross-
   environment red is between SSE-class BLAS kernels and AVX-class ones — i.e. OpenBLAS DYNAMIC_ARCH mapping
   different runners' CPUs to different-generation kernels, exactly the mechanism the `_fitted_note` names.
3. **"GEMM specifically" is still NOT established.** `OPENBLAS_CORETYPE` swaps the WHOLE kernel family, not
   just GEMM; a GradientBoostingRegressor is tree-based and its BLAS touch-points (loss/gradient reductions,
   input array ops) are not necessarily GEMM. So the honest statement is: **the mover is the OpenBLAS kernel
   generation (SSE vs AVX), measured; naming it "the GEMM kernel" is not proven and should not be written as
   fact.** (Register item 76 honoured.)
4. **The pins DO move the board** — so the OpenBLAS story is NOT wrong. But it moves it through the RESIDUAL
   72 isotonic fits (their `np.dot` NW-smoother inputs), NOT through q97m (which is frozen/loaded and does
   not move the board). The cause of the *original* red was q97m's per-CPU fit; the cause of the *residual*
   red is the same OpenBLAS-kernel mechanism acting on the 72 fits' inputs. Both are OpenBLAS-kernel, neither
   is numpy SIMD.

Raw: `results.txt` (every md5, per build).
