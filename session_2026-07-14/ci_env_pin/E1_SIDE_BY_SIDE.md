# E1 — CI RUNNER vs THE PINNED BOX, SIDE BY SIDE
# measured 2026-07-14 · runner from ci-env-measure job 87095221044 (E1 step) · pinned box = this session

| field | GitHub runner (ubuntu-24.04) | pinned box (this session) | DIFFERS? |
|---|---|---|---|
| CPU model | **AMD EPYC 9V74** 80-Core | **Intel Xeon @ 2.80GHz** | ✅ vendor + model |
| nproc (slice) | 4 | 4 | same |
| SIMD flags | sse2 sse4_2 avx **avx2** fma (**no avx512**) | sse2 sse4_2 avx2 fma **avx512f** | ✅ **AVX512 present only on pinned box** |
| numpy SIMD found | X86_V3 (V4 NOT found) | X86_V3, **X86_V4** | ✅ |
| OpenBLAS build | 0.3.31 USE64BITINT DYNAMIC_ARCH NO_AFFINITY | 0.3.31 USE64BITINT DYNAMIC_ARCH NO_AFFINITY | same |
| **OpenBLAS RESOLVED kernel** | **Haswell** (AVX2) | **SkylakeX** (AVX512) | ✅ **THE MOVER** |
| OpenBLAS threads used | 4 | 4 | same |
| OPENBLAS_*/OMP_*/MKL_*/NPY_* set | none | none | same |
| numpy / scipy / sklearn | 2.4.4 / 1.17.1 / 1.8.0 | 2.4.4 / 1.17.1 / 1.8.0 | same |
| threading_layer | pthreads | pthreads | same |
| board built | `62d23265` | `3dc19fbb` | ✅ |

## WHAT DIFFERS — one line
**The CPU.** The runner is an **AMD EPYC without AVX512**; the pinned box is an **Intel Xeon with AVX512**.
OpenBLAS DYNAMIC_ARCH therefore selects a **different runtime kernel** — **Haswell (AVX2)** on the runner,
**SkylakeX (AVX512)** on the pinned box. Everything else that could matter — thread count (4=4), library
versions, threading layer, and the (empty) BLAS/thread env — is **identical**. The board follows the kernel, and
the kernel follows the silicon. No environment variable changes the silicon.

## Raw OpenBLAS resolution (threadpoolctl)
- runner:     `architecture=Haswell,  num_threads=4`  (lib libscipy_openblas64_ 0.3.31)
- pinned box: `architecture=SkylakeX, num_threads=4`  (lib libscipy_openblas64_ 0.3.31)
