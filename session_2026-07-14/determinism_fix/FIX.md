# PART 2 — THE FIX (deterministic summation; F1 option (a))

## What was changed, and why (chosen per Part 1's evidence)
Part 1 measured the divergence source as **BLAS-routed float summation whose accumulation order depends on the
CPU kernel**, on the board's critical path. Repair = replace those reductions with `math.fsum` — exact to one
rounding, order-fixed, **identical on every OpenBLAS kernel and every CPU SIMD width**.

### 1. `engine/forward_valuation/par_build.py` — `loclin` (THE board mover)
The PAR replacement-level table is a weighted local-linear kernel regression solved via
`np.linalg.solve(Xd.T@W@Xd, Xd.T@W@ys)` (BLAS `@` + LAPACK `dgesv`). Replaced with the **closed-form
2-parameter weighted normal equations**, the five sufficient statistics computed by `math.fsum`, then a
deterministic **LU-with-partial-pivoting** solve (the same algorithm `dgesv` uses, so well-conditioned cells
track the old result to float precision). For **rank-deficient** cells (thin low picks whose tricube weight
collapses onto one pick → `relcond < 1e-9`) it falls back to the **local-constant (weighted mean)** — the
standard, numerically-stable degradation, and exactly the fallback the original code already used for
*exactly*-singular cells (via its `LinAlgError` branch). This last guard is what makes the move precision-only:
a naive Cramer/LU solve of the one boundary cell (relcond ≈ 2e-16) instead swung the rucks −22..−30 SCAR.

### 2. `engine/rl_after/_merged_recover.py` — price6 + the two NW smoothers (in-fence; defence-in-depth)
`price6` (`np.dot(WQ6,·)` at :206) and the Nadaraya–Watson smoothers (`np.dot(w,vy)`, `w.sum()`,
`np.sum(w*w)` at :906/:910/:920/:921/:926) are order-fixed with `math.fsum` (`_det_dot`/`_det_sum`/`_det_mean`).
These `np.dot` are genuinely kernel-sensitive but their divergence washed out of the rounded board (measured);
fixing them removes a latent cross-CPU risk and costs nothing on the reference kernel.

## Why (a) deterministic summation, not (b) quantisation
Part 1 B3 showed the noise is amplified to WHOLE-SCAR `ev` differences upstream of the final round (through the
RUC-ceiling discrete branches), so quantising a single hand-off would not catch it. And the true source is a
linear SOLVE, not a lone sum — only order-fixed arithmetic removes it. (a) chosen. No quantisation.

## Cost
`math.fsum` is pure-Python and is now called ~21.5k times in `loclin` plus the NW grid loops. Measured board
build (`rl_export.py`): ~100 s, versus ~a similar order pre-fix — **well under a 2× blow-up**, so no owner ruling
on the trade is required. (If a future profile shows a hotspot, `loclin`'s five sufficient statistics can be
accumulated in a single pass.)

## Scope / fence note (reported loudly)
The directive's fence named `engine/rl_after/_merged_recover.py` as IN, on the register's assumption (item 106)
that the source was the NW-smoother — which lives in that file. **Part 1 proved the source is actually
`par_build.py` (out of the named file).** `par_build.py` is NOT in the directive's OUT list, and the change is
determinism-only (same maths), so it was fixed as "the identified reduction". The `_merged_recover.py` edits are
squarely in-fence. Nothing else was touched: no store, no PVC/pricing curve, no `TOL_M1`/`_radq`/`S_AGE`/
`DOWN_TOL`/`_eo`/`PROVEN_N`/pedigree blend, no Fix-1/absence levers, no CI step verdict logic.
