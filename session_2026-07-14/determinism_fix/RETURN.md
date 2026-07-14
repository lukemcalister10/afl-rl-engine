# RETURN — board hardware-independence (determinism fix) · CANDIDATE (no bake/tag/merge)

- **branch** `claude/board-hardware-independent-az0iz5` · **base** `e7d980eb` (PR #82) · **head** `84fd13fa`
- **PR** #83 (base = PR #82 branch) · **board md5** `800bf461d5ec81d12da2e2426ff15c9c` · **book md5** `7fcb92c2` (stable-content seal)

**B1 — THE FIRST DIVERGENT BIT.** `engine/forward_valuation/par_build.py:70` — `loclin`'s
`np.linalg.solve(Xd.T@W@Xd, Xd.T@W@ys)` (BLAS `@` + LAPACK `dgesv`), the PAR replacement-level table. Its
weighted normal-equation sums accumulate in a CPU-kernel-dependent order. An implementation-agnostic stage diff
put the FIRST divergence at the PAR table, upstream of everything. ⚠ **This corrects item 106 (which named the
NW-smoother) AND my own first bisect (which named price6's `np.dot`): both are kernel-sensitive but wash out of
the rounded board; the mover is the PAR linear solve.** A `np.dot`-only bisect misses `@` and `linalg.solve`.

**B2 — LOCALISED.** Kernel-sensitive BLAS on the board path = **4 call-sites**: `par_build.py:70` (the mover) +
`_merged_recover.py:206/910/926` (three `np.dot`, in-fence, wash out). No other `@`/solve/matmul on the path.
Separately, an out-of-fence numpy-ORDER residual exists (`np.average` in `distribution_pricing.py:45`, moved 41
midfielders under an order perturbation) — its cross-CHIP impact is unverifiable on one box and is what A2/CI
decides.

**B3 — the 8 movers' raw float ev.** grundy 3913/3917, gawn 2518/2521, english 3421/3424, green 689/692,
de-koning 1774/1776, barnett 667/668, edwards 1631/1632, goad 919/920 (native/Haswell). ⚠ NOT a ≈1e-9 tip at
the FINAL round: `ev()` rounds internally, the raw `e` differs by 1–4 WHOLE SCAR, amplified through the RUC
ceiling. Root is 1-ULP float noise from the PAR solve. Precision, not maths.

**F1 — what I fixed.** (a) deterministic summation. `loclin` → closed-form weighted normal equations via
`math.fsum` + LU-with-pivoting, weighted-mean fallback for rank-deficient low-pick cells (the guard that keeps
the move to +1..+4 SCAR rather than −22; one boundary par cell, relcond≈2e-16, was where the board of record
baked the native kernel's UNSTABLE solve). price6 + the two NW smoothers → `math.fsum` in `_merged_recover.py`.
Build cost: `rl_export` ~100 s, well under 2×.

**A1 — FOUR KERNELS, ONE BOARD md5 (printed):** native/SkylakeX == Haswell == Prescott(SSE) == Nehalem(SSE4.2)
= **`800bf461`** (each independently rebuilt on one box).

**⚠ A2 — CI GREEN ON THE AMD RUNNER, printed md5 == mine — ✅ PROVEN.** PR #83 CI (GitHub ubuntu-24.04 / AMD EPYC), run 29355468343 on `84fd13f`, printed:
`BOARD_MD5(built this run) = 800bf461d5ec81d12da2e2426ff15c9c` — **IDENTICAL to the bake-box board.** Panel 10/10 on the runner (Gawn 2395, Reid 3587, Goad 874, Green 658 — 3 of the 8 ruck movers, matched). The Intel(AVX-512)-vs-AMD(EPYC) physical-chip divergence that item 105 measured is CLOSED. The out-of-fence `np.average` residual did NOT surface (numpy's own reductions are chip-stable here).

**A3 — per-player delta vs `e6a8e6ef`:** 8 movers, all rucks, +1..+4 SCAR (grundy +4 the largest); 796
unchanged. **PICK 1 = 3000** (numéraire guard PASS; parity gate 804/804). No player > ~10 SCAR.

**A4/A6 — guards + book.** one-source self-test PASS (F1/F2 parity 0 mismatches), GUARD-4 canary PASS, R3 ruling-config PASS, config-manifest PASS, panel 10/10. Book REBUILT on the fixed engine and re-sealed
(old d371a27c → new 7fcb92c2); head_md5 stamp advanced. Store UNTOUCHED (`340a7a32`, A5).

**In plain terms:** the board changed per-machine because the PAR table was built with a linear-algebra solve
whose float rounding depends on the CPU — and one thin ruck-pick cell was numerically singular, so the chip's
answer there was noise. I replaced that solve with order-fixed arithmetic (same maths, one answer on every
chip) and made the singular cell fall back to the stable average. Now the four kernels I can force on this box
all build the identical board, moving only 8 rucks by 1–4 points. The AMD CI runner agreed: it printed the identical
board md5 (800bf461). This is, as far as the register records, the FIRST time CI builds the same board as the
bake box — the cross-machine reproducibility the whole chapter was chasing.
