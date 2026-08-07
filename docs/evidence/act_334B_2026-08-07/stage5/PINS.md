# STAGE 5 — PINS, old → new

**These pins ARE landed.** The owner authorized the consistency pass and ruled its result final (#334
comment 5217293177), so the product change installs. Every identity below was **measured from the artifact
that carries it**, after that artifact was built — none is typed from an expectation.

Baseline: `c05f214` (stage 4 amendment 1, board `b56bbdde`).

## data/expected_boot.json

| pin | old | new | why |
|---|---|---|---|
| `engine_head` | `bc45d773682ceec2cf8a7760c46c8edd` | **`98ed707042d3386298a6c4510f356f98`** | `_merged_recover.py` is the one engine file the stage touches (`G5_W`, `_g5_load`, `_g5`, the hoisted anchor in `sitout_ev`). Diff filed as `engine_sitout_ev.patch`. |
| `config` | `38a73675b28f555c…` | **`74b2a05604725f64263c4801949bff78a09d27f69a30edc6e8c30419d1fe68ec`** | `RL_G5_W` is a VALUED owner dial (1.0), not a declared kill-switch, so it is enumerated in `data/model_config.json` (**62 vars, was 61**) and `config_sha256` re-stamps in the same commit. `python3 config_manifest.py check` → **PASS**. |
| `board` | `b56bbddea15fd48e35b5794b1b5e9e23` | **`13f8c2e0240600733a5fb42414510445`** | the rebuilt board, stamped AFTER the build from the built artifact. |
| `v0surf` | `9713ec6c83270ab916bb4a5e3ded6cb3` | **unchanged** | NOT refit and not owed one. Re-verified by a declared refit at `RL_G5_W` 0 / 1.0 / 2.0, all three reproducing the committed pickle at signature `3e8e50de5103` (`fit_coupling_refit_log.txt`). |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | unchanged | read-only stage. |
| `rl_model` / `fv` / `band` / `q97m` / `register` / `peak_model` / `pvc_snapshot` / `bust_prior` / `balanced_board_md5` | — | unchanged | nothing in those lanes moved. |

## data/model_config.json

| field | old | new |
|---|---|---|
| `vars.RL_G5_W` | *(absent)* | **`"1.0"`** — inserted immediately after `RL_SUR_W`, beside the other valued thin-record dials |
| `vars` count | 61 | **62** |
| `config_sha256` | `38a73675b28f555c…` | **`74b2a0560472…`** |
| `_stage5_note` / `var_notes.RL_G5_W` | *(absent)* | added — what the dial is, why it is a manifest dial and not a kill-switch, why it is not a `_V0SURF_GATES` key, and that the taught surface is a frozen committed artifact rather than a config var |

## A NEW COMMITTED ARTIFACT

| file | md5 | what |
|---|---|---|
| `engine/rl_after/g5_table.json` | **`1bd109cb0b428ed91c1988c0c72d4000`** | the taught surface, from the CONSISTENCY PASS. Loaded read-only at build, never fitted — the `lti_return_table.json` / `ycred_table.json` precedent. `bootstrap.sh` seeds it automatically (it copies `engine/rl_after` verbatim). Filed beside this note as `stage5/g5_table_LANDED.json`. The superseded frozen-lam table (`stage5/g5_table.json`, md5 `1dc66750a51d04eb9b35b33685960feb`) is kept as part of the STOP record and is **not** what ships. |

## data/rl_build/rl_app_data.json + its sidecar

| field | old | new |
|---|---|---|
| board file md5 | `b56bbddea15fd48e35b5794b1b5e9e23` | **`13f8c2e0240600733a5fb42414510445`** |
| `.srcmd5` `own_md5` | `b56bbddea15fd48e35b5794b1b5e9e23` | **`13f8c2e0240600733a5fb42414510445`** |
| `.srcmd5` `source_md5` (the store) | `37ced3ce45914e6feb00d27e26922e9a` | unchanged — the store did not move |

## The re-emitted book

| artifact | md5 |
|---|---|
| `stage5/noarb/per_entrant_338_stage5.json` (walk-forward matrix, post-change) | `bfc104f4…` (banner: `store=37ced3ce engine=98ed7070 v0surf=3e8e50de51030297c99cf367161c161f frozen=True`) |
| the frozen TEACHING matrix (baseline, never re-emitted for teaching) | `b564b12e533119f49c2c6bb0c92a5d91` — **unmoved, and it must stay unmoved** |

## NOT re-pointed, and why

* **`_V0SURF_GATES`** — `RL_G5_W` is deliberately absent. `sitout_ev` has exactly one caller (the `ns==0`
  arm of `ev()`); `_build_v0_curve` fits `_v0_raw` and never calls `ev()`. Proven, not asserted, by the
  three-dial declared refit.
* **`engine/rl_after/pvc_curve_v2.json`** (the settled ladder, `curve_md5` `18203822`, pick 1 = 3000),
  `ui/release_pick_curve.json`, the LEG F5 entrant seal `5c38e8ba`, the numéraire block — all UNTOUCHED.
  `NUMÉRAIRE GUARD: PASS — shipped pick-1 = 3000`. The candidate workbook's `picks` sheet re-asserts the
  ladder unmoved at all 64 picks.
* **`one_source_selftest.py` pins** (`_contract_md5`, `_curve_source_store`, `_per_entrant_md5`) — UNMOVED.
  The self-test passed **143 / 0 with zero re-points**.
* **The harness pins** (`harness_pvc_REPINNED_pass3.py`): `EXPECT_STORE` `37ced3ce`, `EXPECT_V0SURF`
  `3e8e50de5103`, `EXPECT_N` `1197`. All three re-measured on the stage-5 matrix; **all three came back
  unchanged**, so nothing was re-pointed and no assert was patched.
* **`docs/OPEN_ITEMS_REGISTER.md` / `docs/CURRENT_STATE.md`** — supervisor pen. Untouched by this seat.
* **`side_by_side/board_before_after.xlsx` and `SIDE_BY_SIDE.md`** — **REFRESHED**, because the board landed.
  The workbook now carries the **SIXTH** stage column (Δ quiet-starter reprice, `b56bbdde → 13f8c2e0`) with
  the per-row six-stage identity asserted **804/804** in Python by `side_by_side/verify_xlsx.py`, and a
  third movers sheet. `SIDE_BY_SIDE.md` leads with the FULL-COHORT conservation table per the owner's
  presentation ruling (#334 comment 5217177098).

## Gates on the stage-5 build, for the record

| gate | result |
|---|---|
| ENV PIN (numpy 2.4.4 + bundled OpenBLAS `05c9f9eb`) | **PASS** |
| Guard 5 (boot store / rl_model / fv, checkout + loaded-path) | **PASS** |
| CONFIG MANIFEST (gate mode, 62 vars) | **LOADED**, hash `74b2a0560472`, ambient cleared |
| `config_manifest.py check` | **PASS** |
| PARITY GATE (804 board values == engine gated `ev()`) | **PASS**, 804/804, eps=0 |
| NUMÉRAIRE GUARD | **PASS** — shipped pick-1 = 3000 |
| BOOK↔BOARD PARITY | **PASS** (802 shared; 2 `_pvc_exclude` rows outside the cohort book) |
| FUT-LABEL / ZERO-EMPTY-CLUB | **PASS** / **PASS** |
| one_source_selftest | **PASSED, 143 assertions, 0 FAIL, exit 0, 0 re-points** |
| DIAL-0 (`RL_G5_W=0`) through the full gate | **PASS — board `b56bbdde` byte-exact** |
| BOOK↔BOARD PARITY | **PASS** (802 shared; 2 `_pvc_exclude` rows outside the cohort book) |
