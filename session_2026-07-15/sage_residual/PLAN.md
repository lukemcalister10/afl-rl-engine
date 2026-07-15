# PLAN — THE S_AGE 30+ RESIDUAL (L-SAGE-FADE) · register 122a · 2026-07-15

**Basis (STRICT):** analysis checked out at candidate-line HEAD
`62352729ec3523cec4bb117e713e1bec67a0d490` (branch
`claude/absence-penalty-evidence-fade-glcl8b`). Store `340a7a32` == pinned (Guard 5 PASS).
Engine `_merged_recover.py` exec'd exactly as `run_panel.sh` does (config gate = manifest defaults).
Write fence: `session_2026-07-15/sage_residual/` ONLY. Read-only everywhere else.

## What S_AGE actually is (measured from the code, not the framing)

`_S_AGE(a)` (engine `_merged_recover.py:274-276`) is the **breakout-persistence slope** in the
proven-riser UP-branch of `_coreM1` (`:293`):

```
if n>=PROVEN_N(4) and Lc>=Lo:
    if (Lc-Lo)>=TOL_M1(5.0) and _radq(p,Y,Lo):
        L_pred = Lo + _S_AGE(age)*(Lc-Lo)      # <-- S_AGE fires here
    else: L_pred = Lo
```

- `Lo = cp._lvl_eff_orig(p,Y)` — recency-anchored baseline level.
- `Lc = _lvlcurr(p,Y)`  — steeper-recency CURRENT level (trend-aware).
- Gap `Lc-Lo` = how far a proven player's current form sits **above** their baseline (a breakout).
- `_S_AGE(age)` = fraction of that breakout the engine keeps. Curve `_L3_AY`:
  `age 29 → 0.0269`, **`age 30 → 0.0`, `age 31 → 0.0`** (clipped flat 0 for 30+).

So the engine's claim at 30+ is: **a proven 30+ player who posts a season above their baseline
carries NONE of it forward — full mean-reversion to `Lo`.** That zero has never been tested.

## Estimand

The realised analogue of the slope: **`s_real(age)` = the fraction of a proven player's
current-over-baseline elevation `(Lc-Lo)` that is actually realised in the FOLLOWING season.**

- **Residual(age) = `s_real(age) − _S_AGE(age)`.** At 30/31 `_S_AGE=0`, so residual = `s_real`.
- Zero-at-30 is "real" iff `0 ∈ CI[s_real(age)]` at that age.

## Sample (the population the zero actually touches)

One observation per player-year `(p,Y)`, drawn from the full historical panel in the store
(so `n` is real, not just the 2026 cut):

- **Proven:** `_nqual(p,Y) ≥ PROVEN_N (4)`  (engine's exact gate).
- **Up-branch trigger fires:** `Lc-Lo ≥ TOL_M1 (5.0)` AND `_radq(p,Y,Lo)` — i.e. exactly the
  rows where `_S_AGE` is applied. (This is the honest population: the zero only mis/correctly-prices
  players it touches.)
- **Realised next season exists:** a scoring row at `Y+1` with `games ≥ 10` (qualifying).
- **Age band:** `age = _age_asof(p,Y) ∈ [29,36]` reported; 29 kept as the last nonzero-curve anchor.
- `Y ≤ 2024` so `Y+1 ≤ 2025` is a completed season (exclude the 2026 in-progress cut from the
  realised side; the M3 age pin only affects Y=2026 so historical ages are unpinned).

For each obs: `x = Lc-Lo` (≥5 by gate), `y = L_next - Lo` where `L_next` = the `Y+1` season avg.

## Estimator (CORE rule 7 — finest resolution, kernel-smoothed, per-age n, no wide bins)

- **Per-age realised slope:** ratio-of-means through the origin,
  `s_real(a) = Σ_kernel w·y / Σ_kernel w·x`, Gaussian age kernel (bandwidth **h = 1.5 yr**),
  so each integer age borrows strength from neighbours without collapsing the band into one bin.
- **CI:** cluster bootstrap by player (5000 resamples; players, not player-years, are the
  independent unit) → 95% percentile CI on `s_real(a)` and on the residual.
- **Per-age n** (raw player-years and distinct players) reported at every age; ages whose raw n is
  too thin to resolve are flagged, not silently pooled (rule 7: "thin slices pooled deliberately and
  declared").
- **Sensitivity** (reported, not buried): realised-games threshold 10 vs 6; gap floor 5 vs 3;
  per-obs `y/x` mean vs ratio-of-means — to show the shape is not an artefact of one knob.

## Deliverables (all under the fence)

1. `residual_by_age.csv` + `RESIDUAL.md` — `s_real(a)`, `_S_AGE(a)`, residual, 95% CI, n, "0 in CI?".
2. `mispriced_30plus.csv` — current 30+ proven up-branch players: implied level (`Lo`, S_AGE=0) vs
   measured (`Lo + s_real(age)·(Lc-Lo)`), ranked by level-point mispricing.
3. `FINDING.md` — one page. FINDINGS, NOT VERDICTS (S4): the measured shape only, no fix proposal.
4. `measure_sage_residual.py` — the reproducible harness.
