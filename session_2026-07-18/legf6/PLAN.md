# LEG F6 — FREEZE `_iso_dec` (THE RESIDUAL WEATHER) · PLAN

**Owner-ruled "fix it" (item 381) on the item-380 diagnosis.** Freeze the one live import-time/board-time fit
q97m's 2026-07-14 freeze missed. Tier-1-lite (k=0 diff bounded ≤1 row; expected 0). Base = 15a9abd (Leg F5).

## Job 1 — confirm scope is ONE
Enumerated every live fit in `engine/rl_after/_merged_recover.py`:
- `GradientBoostingRegressor` → **q97m only, frozen** (loaded pickle); `cm_400` also a frozen pickle.
- `_dev_advance`/`v_at_peak` (:361) + the NW kernels (:1228/1242) → **order-fixed** (`_det_sum`/`_det_dot`/`_det_mean`).
- `IsotonicRegression` at :463/:466 (ISO pick-tax table) → fit on **synthetic** archetypes over frozen models;
  **kernel-invariant** in the forced-coretype probe (`14876ea15a8e` across SkylakeX/Katmai/Haswell/Nehalem) →
  deterministic-by-construction, not a residual-weather source.
- `_iso_dec` (:1222) via `_build_v0_curve` → the **one live fit over the real roster's value path** = the target.

## Job 2 — freeze `_iso_dec` the q97m way (option a: freeze the OUTPUT surface)
`_build_v0_curve` fits three isotonic surfaces (`c18`,`surfN`,`surfR`). It is re-run 3× as `_PVC0` swaps
(base → L1b under `RL_PVCADOPT` → v2 under `RL_PVC2`); the **final (v2) call is the shipped surface**.
- Compute the shipped surface ONCE (clean instance), pickle to `data/v0surf.pkl`, LOAD thereafter.
- **Load key = a deterministic config signature** = active pick curve (`_PVC0`/`MA.PVC`) + roster geometry +
  normalized value-gate env — **never `_v0_raw` values**, so a future weather box computes the SAME signature
  and loads the SAME clean surface (the flip is removed). Lens gates (`RL_LEGF`/`RL_LEGE`) are excluded (they
  never touch V0). A non-shipped config (a kill switch) has a different signature → not in the frozen set →
  **still fits, exactly as before** → every declared kill switch stays byte-exact.
- `load-or-halt`, md5-pinned; the ONE refit entry point is `scripts/refit_v0surf.py` (`RL_V0SURF_REFIT=1`).

## Job 3 — pin it
Add `data/expected_boot.json` `'v0surf'` (the one pin add). Wire Guard 5 (`boot_guard.py` `_FITTED` + `_LOADED`,
mirroring q97m) so it asserts the frozen artifact on entry (checkout + engine load-path).

## Job 4 — the proof (bounded)
k=0 balanced board == `06d8af60` byte-exact; FULL k=0 row-diff vs the pre-freeze clean board must be EMPTY;
forced-kernel determinism (load the pickle, force a BLAS coretype change, assert the board holds `06d8af60`).

## Job 5 — exit
`RL_LEGF=0` chain byte-exact; dormancy F3/F4/F5 PASS; store/curve/q97m untouched; Guard 5 asserts v0surf.

## FENCE
IN: `_merged_recover.py` (`_iso_dec` + load path) · `data/v0surf.pkl` · `data/expected_boot.json` (one pin) ·
`session_2026-07-18/legf6/`. Guard-5 wiring (`boot_guard.py`, 2 additive entries) is the mechanism job 5
requires. HARD-OUT: store · curve · rl_model.py · the rest of the V0/`_iso_dec` chain logic (freeze the OUTPUT,
don't re-derive the surface) · pins beyond the one add · docs · ui.
