# P2 — THE 72 RUNTIME FITS, ENUMERATED (measured, not counted by eye)

**A2 as written by the freeze RETURN FAILED and was re-labelled.** The directive demanded ZERO runtime
fits; the truth is **72 sklearn fit-method calls per engine load remain.** They were re-scoped to "zero
BLAS-movable fits" — and this section shows that re-scope was wrong: **the residual that moves the board
across environments lives in exactly these 72** (measured — see P3: board `3dc19fbb`→`935c2c29` under an
SSE BLAS kernel, on the FROZEN engine).

## Method
Monkey-patched `sklearn.isotonic.IsotonicRegression.fit`/`.fit_transform` **and** every
`GradientBoosting*/RandomForest*` `.fit`, then did a full engine load
(`exec` of `_merged_recover.py` up to the AFTER banner — the exact path a board/gate/panel build takes).
Script + raw census committed: `instrument_fits.py`, `fit_census_raw.json`, `instrument_out.txt`.

## Result — 72 fit-method calls, ALL isotonic; ZERO GBR/RF
```
TOTAL runtime .fit/.fit_transform calls during engine load: 72
by estimator: {'IsotonicRegression.fit_transform': 6, 'IsotonicRegression.fit': 66}
```
- **ZERO GradientBoosting/RandomForest fits** — the freeze DID remove the two BLAS-movable *model* fits
  (q97m + cm are now LOADED). That part of A2 is real. What remains is **72 IsotonicRegression PAVA fits.**
- The 6 `fit_transform` each internally call `.fit` once, so the 66 `.fit` = 6 (inner, at :218) + 60
  (`_iso_dec`, at :820). **Distinct PAVA solves per load = 66; total fit-method calls = 72.**

## THE TABLE (ranked by what they touch)

| # | file:line | site / call-chain | fits (per load) | what it fits | what FEEDS it | what CONSUMES its output | env-movable? |
|---|---|---|---|---|---|---|---|
| **1** | `_merged_recover.py:820` | `_iso_dec` ← `_fit_mature:847` | **48** = 12 ages × 2 surfaces(nonRUC,RUC) × 2 builds | `IsotonicRegression(increasing=False,oob='clip').fit(_V0_LGRID[90], row).predict(...)` — pick-isotonic projection of the mature 2D (draft-age × log-pick) V0 surface, per age 19–30 | **adaptive-bandwidth Nadaraya–Watson kernel sums** `np.dot(w,vy)/sw` (`:840`,`:846`) over capped V0s — **`np.dot` routes through OpenBLAS** | `_V0CURVE` mature anchors → every mature ND player's start V0 → present/forward valuation, sit-out retention, staleness caps, B5 floor | **YES** (item 80) — PAVA is order-deterministic but its NW-sum inputs shift with the BLAS kernel |
| **2** | `_merged_recover.py:820` | `_iso_dec` ← `_fit_pick_curve:831` | **12** = 6 age-18 positions × 2 builds | same `_iso_dec` — pick-isotonic projection of the age-18 V0 pick curve, per position | adaptive-bandwidth NW kernel sums `np.dot(w,vy)/sw` (`:830`) — **`np.dot` → OpenBLAS** | `_V0CURVE` age-18 anchors → **`_fit_pick_curve` → the V0 curve → THE PICK CURVE** (the numéraire chain the directive names); every age-18 ND start V0 | **YES** — same NW→BLAS input path |
| **3** | `_merged_recover.py:218` | ISO PICK GUARD (`<module>`) | **6** = 6 positions (fit_transform; +6 inner `.fit`) | `IsotonicRegression(increasing=False).fit_transform(PICKS[1..70], raw)` — monotone-non-increasing pick correction, per position | `raw = raw_ev(synth(pk,par_at,pos))` for pk 1..70 — synthetic raw EVs via `price6`/`par_pole`/`recover` (numpy float math, some BLAS) | `ISO[pos]` → `iso_corr(pos,pk)` → `raw_ev` correction, RUC ceiling (`_build_ruc_ceiling` via `_sp`), and `_v0_uncapped` → the whole board valuation | **YES** — float-sum inputs; PAVA order-deterministic, inputs are not |

**Total: 48 + 12 + 6(+6 inner) = 72 fit-method calls (66 distinct PAVA solves).**

### Why ×2 ("builds")
`_build_v0_curve()` runs **twice** per load: once at import (`:869`) and once in the RL_PVCADOPT default-ON
rebuild (`:1040`, which swaps `_PVC0` to the L1b pinned curve and rebuilds the V0 guard + V0 curve + RUC
grid). So every `_iso_dec` fits twice. The pick-guard (`:218`) is module-level and fits once per load (its
6 fit_transform = 6+6 method calls).

## The load-bearing point (why the A2 re-scope was wrong)
"`_iso_dec` is order-deterministic in itself" is TRUE and IRRELEVANT. Its **inputs** are Nadaraya–Watson
kernel sums built with `np.dot` — which dispatches to the OpenBLAS kernel that P4 proves is the mover. So a
shift in an upstream BLAS sum shifts the smoothed grid, which shifts the isotonic output, which shifts the
V0 anchors, which shifts the board. **Measured, not argued:** on the frozen engine the board is `3dc19fbb`
on the AVX2/Haswell kernel and `935c2c29` on an SSE (Prescott) kernel. The residual is these 72 fits' input
path, and it is real.
