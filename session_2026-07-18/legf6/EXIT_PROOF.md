# LEG F6 — EXIT PROOF · FREEZE `_iso_dec`

Base 15a9abd (Leg F5). Single-thread (OPENBLAS/OMP/MKL/NUMEXPR=1), fresh clone, this-session fetch. Docs on MAIN.

## Clean-instance precondition
Balanced board (RL_LEGE=0 RL_LEGF=0) == **`06d8af60`** byte-exact · Σv 752427 · Sheezel 7964 (5/5 consecutive;
holds under forced Prescott/Nehalem/Haswell). New engine in FIT mode reproduces `06d8af60` → the freeze code
does not perturb the fit path. (First-commit HALT corrected: it used the wrong env RL_LEGE=1 → d85901af, and
saw a one-off cold-start flip; see BASE_PROOF.txt. User ruled: freeze here with the full job-4 safety net.)

## What changed (FENCE)
- `engine/rl_after/_merged_recover.py` — `_load_v0surf()` + config signature `_v0surf_sig()` + `_build_v0_curve`
  loads the frozen shipped surface (fits only for the refit entry point or a non-shipped/kill-switch config).
- `data/v0surf.pkl` (new) — md5 `3af2b7258b8c8c596c4184617f99d3ca`; payload `{sig a610237ed541: {c18,surfN,surfR,meta}}`.
- `data/expected_boot.json` — one pin add: `v0surf`.
- `boot_guard.py` — v0surf added to `_FITTED` (checkout) + `_LOADED` (load-path), mirroring q97m (job-5 wiring).
- `session_2026-07-18/legf6/` — PLAN, BASE_PROOF, refit_v0surf.py, probe_fits.py, proofs, provenance log.

## Job-4 proof
| check | result |
|---|---|
| LOAD-mode balanced board | `06d8af60` (Σv 752427); `_v0surf_frozen=True` (LOADED, not fitted) |
| FULL k=0 row-diff vs pre-freeze clean board | **0 rows (EMPTY)** |
| forced-kernel determinism (pickle loaded) | `06d8af60` on SkylakeX · Prescott/Katmai · Nehalem · Haswell |

## Identity across configs — pristine (pre-freeze, fits) vs frozen (loads shipped, fits kill switches)
| config | pristine | frozen |
|---|---|---|
| default RL_LEGF1 RL_LEGE1 | `1f10220c` | `1f10220c` |
| balanced RL_LEGF0 RL_LEGE0 | `06d8af60` | `06d8af60` |
| forward RL_LEGF0 RL_LEGE1 | `d85901af` | `d85901af` |
| kill switch RL_PVC2=0 | `9829d01a` | `9829d01a` |

The freeze is a pure identity on a clean box — it removes only the weather flip.

## Exit invariants
- RL_LEGF=0 chain byte-exact; k=0 phantom NONE: active `v` (RL_LEGF=1) == (RL_LEGF=0), **0/804**.
- Dormancy **F3 / F4 / F5 : PASS / PASS / PASS**.
- Store `968de0c7` · curve `56dd7a7b` · q97m `cfdc7321` — UNTOUCHED.
- Guard 5 asserts `v0surf` (checkout + load-path); fails on a bad pin, passes on `3af2b725`.
- **Pre-bake RED** persists on the OTHER pins (`rl_model` a5fd3d7d, `engine_head` 40f43772) exactly as at pristine
  15a9abd — pre-existing candidate-head pin drift, NOT introduced here (those pins move only at an owner bake).
