# PART 1 — THE BISECT (measured; TWO register/first-pass claims CORRECTED)

Base engine `fef5719d`, board of record `e6a8e6ef` (PR #82: Fix 1 + absence). One Intel Xeon (AVX-512) box;
OpenBLAS kernel VERIFIED live each run via `kernel_probe.py` (reads `scipy_openblas_get_corename64_` from
numpy's OWN loaded `.so` — no silent-fallback, the exact hole that produced the false register item 101).

## B0 — the divergence reproduces on ONE box (kernel verified)
native → **SkylakeX** → `e6a8e6ef` (== board of record). `OPENBLAS_CORETYPE=Haswell` → **Haswell** →
**`800bf461`**. Two runs, same box/store/code, two boards. Override verified to take effect (native→SkylakeX,
Haswell→Haswell, Prescott→Katmai, Nehalem→Nehalem, SandyBridge→Sandybridge, Zen→Haswell).

## B1 — THE FIRST DIVERGENT BIT ⇒ the PAR table (`par_build.py:70`), not the NW-smoother, not price6
Two instruments were needed, and the first one MISLED:
1. A `np.dot`-only fingerprint (native vs Haswell) flagged **`price6:206`** (`np.dot(WQ6,·)`) as the first
   divergent `np.dot`. **That was a false lead**: `np.dot` is only ONE BLAS entry point. I fixed it — and the
   Haswell board did **not budge** (still `800bf461`). Lesson logged: a `np.dot`-only bisect misses the `@`
   operator (`ndarray.__matmul__`) and `np.linalg.solve`, which never route through the `np.dot` name.
2. An implementation-agnostic **stage diff** (hash the full float state at every pipeline stage) found the truth:

   | stage | diverges native-vs-Haswell? |
   |---|---|
   | **A — PAR table** | **YES ← FIRST** |
   | B — ISO pick guard | yes (consumes par) |
   | C — V0 curve (NW-smoother) | yes (consumes par) |
   | D — RUC ceiling grid | no |
   | E — price6 | no (after the np.dot fix) |
   | F — final ev | yes (consumes par) |

> **THE FIRST DIVERGENT BIT: `engine/forward_valuation/par_build.py:70` —
> `np.linalg.solve(Xd.T@W@Xd, Xd.T@W@ys)` (BLAS `@` + LAPACK `dgesv`).** The PAR replacement-level table is
> built by a weighted local-linear kernel regression whose weighted normal-equation sums are accumulated in a
> CPU-kernel-dependent ORDER. It runs at import, upstream of everything, and feeds `raw_ev` for every player.

⚠ **THIS CORRECTS BOTH the register AND my own first pass.** Item 106 named *"`np.dot` in the NW-smoother"*;
my first bisect named *price6's `np.dot`*. **Both are wrong.** The NW-smoother's `np.dot` and price6's `np.dot`
ARE kernel-sensitive, but they wash out of the rounded board — the mover is the PAR linear solve.

## B2 — LOCALISED (a handful of BLAS reductions), plus one OUT-OF-FENCE numpy-order residual
The complete set of kernel-sensitive BLAS ops on the board path is small and enumerable:
- **`par_build.py:70`** — `@` + `np.linalg.solve` (the actual board mover). *(out of the directive's named
  fence file, but it IS the identified reduction — the fence assumed item 106's NW-smoother location.)*
- **`_merged_recover.py:206 / :910 / :926`** — three `np.dot` (in-fence; kernel-sensitive but wash out).
No other `@`/`solve`/`matmul`/`einsum` on the board path (the `np.dot` in `dist_redesign`/`distribution_pricing`
is the superseded `dist_value` path, never called during a board build). **⇒ LOCALISED.**

Separately (measured, reported for honesty): a full reduction audit + an order-perturbation board test show the
board is also sensitive to numpy summation ORDER via **`np.average`** in `distribution_pricing.py:45`
(`fwd_peak`, out of fence) — a perturbation moved 41 midfielders ±1. Whether that surfaces cross-CHIP on the
AMD runner is unverifiable on one box (`NPY_DISABLE_CPU_FEATURES` is silently ignored by this numpy); numpy's
own reduction tree may be SIMD-width-independent, in which case it never diverges. **A2 (the AMD CI run) is the
only instrument that settles it.**

## B3 — the 8 movers, and the rounding hypothesis is REFINED
The 8 board movers (native vs Haswell) are EXACTLY item 106's "8 rucks", +1..+4 SCAR (grundy +4, gawn +3…).
⚠ The supervisor's specific mechanism — *"tiny ≈1e-9 `ev` amplified ONLY by the final round-to-integer"* — is
**wrong**: `ev()` rounds INTERNALLY (`round(e)`, line 1047), and the raw `e` differs by **1–4 WHOLE SCAR**. The
root IS 1-ULP float noise, but its origin is the PAR solve, and it is amplified through the RUC path, not tipped
at the final round. Still precision-rooted; nobody moves materially.

## The subtlety that decided the FIX (A3)
Many low-pick par cells (picks 1–4, thin data) are rank-deficient — the weighted local-linear design collapses
to a single point. For **exactly**-singular cells LAPACK raises `LinAlgError` and the code already falls back to
the weighted mean. But **one boundary cell** (relcond ≈ 2e-16, pick~4) is det≈0-but-nonzero: LAPACK *solves* it
to an UNSTABLE value that differs per kernel (SkylakeX 35.5, Haswell ≈ the stable mean). The board of record
`e6a8e6ef` baked the SkylakeX reading. The deterministic fix uses the numerically-stable local-CONSTANT
(weighted mean) for every rank-deficient cell — standard practice — which lands the 8 rucks within +1..+4 SCAR
of `e6a8e6ef`. (A naive Cramer/LU solve of that boundary cell instead produced a −30/−22 SCAR ruck swing; the
explicit `relcond<1e-9 → weighted mean` guard is what keeps the move precision-only.)
