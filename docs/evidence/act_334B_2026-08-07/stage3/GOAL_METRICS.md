# Stage 3 step 9 — GOAL METRICS from the final board + the final matrix

Board `6c9f8d3a92ca82c29dfaa8273a4f3ada` · matrix `b7ed144ec5e4d44263d553a2c23d919b`.
Raw output: `goal_metrics.txt`; script `goal_metrics.py`.

## 1. TOP-END RATIO

| | |
|---|---|
| max active display value | **10668** |
| player | **Harry Sheezel** (North Melbourne) |
| ratio to the numéraire (pick 1 = 3000) | **10668 / 3000 = 3.556000** |

Runners-up: Nick Daicos 9649 · Luke Jackson 8670 · Nasiah Wanganeen-Milera 8633.
(Prior board `f94e0778`: Sheezel 11963, ratio 3.987667.)

## 2. PER-ENTRY-YEAR TABLE

For N = 0..5: mean value at the PEAK year (4) ÷ mean value at year N, over entrants whose window
covers BOTH years. Whole cohort, busts at 0 in every denominator, **denominators printed**.

| N | n (covers both) | mean yr4 | mean yrN | ratio |
|---|---|---|---|---|
| 0 | 1197 | 1149.8747 | 802.7809 | **1.432364** |
| 1 | 1197 | 1149.8747 | 775.2189 | **1.483290** |
| 2 | 1197 | 1149.8747 | 961.0877 | **1.196431** |
| 3 | 1197 | 1149.8747 | 1086.0201 | **1.058797** |
| 4 | 1197 | 1149.8747 | 1149.8747 | **1.000000** |
| 5 | 1139 | 1165.0246 | 1142.8077 | **1.019441** |

Row 5 is the only row whose denominator differs (1139, not 1197): 58 entrants' windows do not yet
reach year 5, so both means on that row are taken over the 1139 that do — the yr4 mean is 1165.0246
there rather than 1149.8747 for exactly that reason.

## 3. YEAR-OVER-YEAR INCREMENTS + THE FRONT-LOADED ASSERT

Whole-cohort path in ratio-to-year-0 units, same-set means:

| step | increment |
|---|---|
| yr0 → yr1 | −0.034333 |
| **yr1 → yr2** | **+0.231531** |
| yr2 → yr3 | +0.155624 |
| **yr3 → yr4** | **+0.079542** |
| yr4 → yr5 | −0.001725 |
| yr5 → yr6 | −0.036655 |
| yr6 → yr7 | −0.183193 |

**FRONT-LOADED ASSERT — yr1→2 increment strictly exceeds yr3→4: +0.231531 > +0.079542 → PASS**
(asserted in `goal_metrics.py`, which raises if it fails). The path is monotonically decelerating
across the whole rise (0.2315 → 0.1556 → 0.0795), so the assert is not passing on a knife edge.

## 4. THE NO-FORWARD-ESCALATOR PROOF

**The 1.40 target appears in NO runtime path. Proven three ways, not asserted.**

### (a) It has exactly two definition sites, both teaching artifacts

```
$ grep -rln "1\.40" --include=*.py .
./docs/evidence/act_334B_2026-08-07/stage2_erafree/derive_reanchor_stage2_erafree.py
./docs/evidence/act_334B_2026-08-07/stage2/derive_reanchor_stage2.py
```

`TARGET_RESIDUAL = 1.40` at line 60 of the era-free derivation, self-labelled *"TEACHING-STAGE ONLY.
Never read by a runtime engine path."* `grep -rn` for either script name, or for `per_pick_reanchor`,
across `engine/`, `ui/` and the repo-root modules returns **nothing** — no runtime module imports or
opens either file. The literal `1.40` does not occur anywhere in `engine/`, in `data/model_config.json`
or in `config_manifest.py`, and no target-shaped identifier (`RL_TARGET`, `target_residual`,
`TARGET_RESIDUAL`, `reanchor`, `R_s`) exists in the engine. Its only appearance outside those two
scripts is as **prose** in `pvc_curve_v2.json`'s `derived_from` documentation string — a field the
engine never reads (it reads `curve`, `pool_value`, `pool_levels`, `numeraire` and nothing else).

### (b) Perturbed at build time: the board is BYTE-IDENTICAL

`TARGET_RESIDUAL` was changed **1.40 → 1.75** in the live derivation script and the canonical board
rebuilt from a clean `rl_app_data.json`:

```
board md5 = 6c9f8d3a92ca82c29dfaa8273a4f3ada     (identical to the landed board)
```

The script was then restored (`git diff --stat` clean). A parameter that reached any runtime path
could not leave the board byte-identical.

### (c) It cannot even be INTRODUCED at runtime

Injecting it as an environment override under four plausible names on the same build:

```
============ CONFIG MANIFEST (gate mode) REJECTED — BUILD HALTED ============
  - UNKNOWN model override RL_TARGET='1.75' is not in the manifest (data/model_config.json)
  - UNKNOWN model override RL_TARGET_RESIDUAL='1.75' is not in the manifest
  - UNKNOWN model override RL_REANCHOR_TARGET='1.75' is not in the manifest
  - UNKNOWN model override RL_RESIDUAL='1.75' is not in the manifest
```

The gate-mode config manifest refuses to build at all rather than accept an unpinned model variable,
so there is no runtime surface on which such a parameter could be added without a manifest amendment
that re-stamps `config_sha256` in the same commit. `config_sha256` is **unmoved** this stage.

Log: `escalator_probe_log.txt` (both runs).
