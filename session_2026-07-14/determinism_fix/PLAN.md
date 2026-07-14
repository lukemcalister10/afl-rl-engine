# PLAN — BISECT THE DIVERGENCE, THEN FIX THE SUMS (board hardware-independence)

**Auto-mode first committed artifact.** Branch from BASE `e7d980eb` (PR #82 head: Fix 1 + absence term).
Board of record on this base = **`e6a8e6ef`** (native/SkylakeX). Engine head `fef5719d`. Store `340a7a32`.

## What is KNOWN vs HYPOTHESIS (I must not assume the hypothesis)
- **KNOWN (re-measured on THIS box, kernel verified live):** native (SkylakeX) → `e6a8e6ef`; forced
  `OPENBLAS_CORETYPE=Haswell` (verified it resolves to Haswell, not a silent fallback) → **`800bf461`**.
  Two runs, one box, one store, one engine → two boards. The divergence reproduces locally.
- **HYPOTHESIS (register item 106, NOT yet measured):** BLAS-routed `np.dot` in the NW-smoother, whose float
  summation order depends on the CPU, feeds the 72 runtime isotonic fits; board rounded to whole SCAR; 8 of 804
  sit on a rounding boundary. **PART 1 verifies WHERE the first bit diverges. If it contradicts 106, say so.**

## Key lever that makes this tractable
`OPENBLAS_CORETYPE` changes ONLY the OpenBLAS kernel; it does NOT touch numpy's own SIMD reductions. So in the
native-vs-Haswell experiment the divergence is *guaranteed* to originate at a BLAS op (`np.dot`/`matmul`/`gemm`)
— nothing else varies. That isolates the culprit exactly.

**But A2 (AMD runner) needs more:** register item 105 measured Intel-Haswell (`5546c120`) ≠ AMD-Haswell
(`62d23265`) — SAME BLAS kernel, different board. That residual can only be numpy's OWN SIMD (Intel AVX512 vs
AMD AVX2) in `np.sum`/`np.mean`/`.sum()`. So the fix must neutralise BLAS **and** verify numpy-SIMD-independence
locally (via `NPY_DISABLE_CPU_FEATURES`) before trusting CI.

## PART 1 — BISECT (no maths change)
- **B0** ✅ reproduce both boards on this box, kernel VERIFIED (done: e6a8e6ef vs 800bf461).
- **B1** fingerprint every `np.dot`/`matmul` over a full board build (engine load incl `_build_v0_curve` +
  ISO guard, then `ev()` as-of sequence for all 804). Run native + forced-Haswell. Walk both logs in call
  order; the FIRST call with **bit-identical inputs but different output** is the culprit reduction. Name
  function / line / array. Candidate sites: `price6` `np.dot(WQ6,·)` (:206), NW smoother `np.dot(w,vy)` in
  `_fit_pick_curve` (:910) and `_fit_mature` (:926).
- **B2** count DISTINCT culprit call-sites. Handful ⇒ localised ⇒ Part 2. Spread across many independent
  reductions (incl. numpy's own) ⇒ **STOP, report, the declared-tolerance road is the answer** (owner's call).
- **B3** report the 8 movers' RAW float `ev` on both runs. Confirm/refute the round-to-integer amplification
  (tiny ~1e-9 delta tipped by rounding) vs a large delta (whole picture wrong).

## PART 2 — FIX (only if B2 = LOCALISED)
- **F0** the board WILL move (float precision). Declare full per-player delta vs `e6a8e6ef`. Any player moving
  > ~10 SCAR ⇒ maths changed, STOP.
- **F1** repair per the evidence: (a) deterministic order-fixed summation (`math.fsum` / pairwise / explicit
  ordered reduce) replacing the offending BLAS reduction; and/or (b) quantise the fragile intermediate at the
  seam before it enters the isotonic fits. Report which + why + build-time cost.
- **Scope fence — IN:** `engine/rl_after/_merged_recover.py` (the identified reductions ONLY), rebuilt
  board+book, `data/expected_boot.json` re-pin, this session dir. **OUT:** Fix-1/absence levers, store, PVC/PVC
  curve, TOL_M1/_radq/S_AGE/DOWN_TOL/_eo/PROVEN_N, pedigree blend, docs, CI step logic. (E0 diagnostic print is
  expected in CI — my base branched before it was added, so I will port the OUTPUT-ONLY print, updated to the
  new board md5; no verdict logic touched.)

## ACCEPTANCE
- **A1** native == forced-Haswell == forced-SSE(Prescott/Katmai) == AVX512-off → ONE md5, print all four.
- **A2** (only real proof) CI green on the AMD runner, its printed board md5 == mine. De-risk locally first by
  forcing numpy to AVX2 (`NPY_DISABLE_CPU_FEATURES=AVX512F,...`) and confirming the board is stable.
- **A3** full per-player delta vs `e6a8e6ef`; no player > ~10 SCAR; PICK 1 still prices 3000.
- **A4** every guard on the frozen suite; anchors; three narrowest margins.
- **A5** store untouched (`340a7a32`).
- **A6** book rebuilt (formula moved); re-pin every stamp; record old→new md5.

## Ladder
TIER 1 — moves value (float precision only). NO bake, NO tag, NO merge. Candidate PR only.
