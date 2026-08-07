# STAGE 4 AMENDMENT 1 — PINS, old → new

Baseline `44950de` (stage 4). Every identity below was **measured from the artifact that carries it**,
after that artifact was written. None was typed from an expectation.

## data/expected_boot.json

| pin | old (stage 4) | new | moved? | why |
|---|---|---|---|---|
| `engine_head` | `9a0c7fdc90f1ac8aed50692947e1b418` | **`bc45d773682ceec2cf8a7760c46c8edd`** | **MOVED** | `_merged_recover.py` is the one engine file this amendment touches (`SUR_W`, `_rho_res`, `_surprise`, the hoisted `gp`, the amended exponent in `sitout_ev`). |
| `config` | `0b5d27030136500373f558ea345ea4a7d0288b1795a23d38ae641da208a2ebdd` | **`38a73675b28f555cb866411fb295efba433730a45e8e1f195bbe1786a7c38e1f`** | **MOVED** | `RL_SUR_W` is a VALUED owner dial and is enumerated in `data/model_config.json` (61 vars, was 60). Re-stamped in the same commit, as the manifest's own doc requires. Verified: `python3 config_manifest.py check` → **PASS** (hash `38a73675b28f`, 61 vars, pin+stored consistent). |
| `board` | `b490ae8b3bbd28b908ccb923ed8412c1` | **`b56bbddea15fd48e35b5794b1b5e9e23`** | **MOVED** | the rebuilt board. Stamped AFTER the build, from the built artifact. |
| `v0surf` | `9713ec6c83270ab916bb4a5e3ded6cb3` | unchanged | **unmoved** | NOT refit and not owed one — `FIT_COUPLING.md`. Re-verified on this box at three dial values (0.0 / 5.0 / 20.0), all reproducing the committed pickle. |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | unchanged | unmoved | `rl_model.py` NOT touched. |
| `fv` | `0976195c8454…5f5f18a87` | unchanged | unmoved | `engine/forward_valuation/` untouched; recomputed and asserted by bootstrap (checkout + loaded-path). |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | unchanged | unmoved | read-only stage. |
| `band` (cm_400) `34faa865` / `q97m` `cfdc7321` / `register` `652d83e8` / `peak_model` `f305fe53` / `pvc_snapshot` `ade79790` / `bust_prior` `5942aa6a` / `balanced_board_md5` `123deccb` | — | unchanged | unmoved | nothing in those lanes moved. |
| `as_of_round` | 21 | unchanged | unmoved | no new match data entered this amendment. |

## data/model_config.json

| field | old | new |
|---|---|---|
| `vars.RL_SUR_W` | *(absent)* | **`"5.0"`** — inserted immediately after `RL_PED_BAR`, beside the stage it amends |
| `vars.RL_PED_BAR` | `"0.5"` | **`"0.5"` — UNCHANGED.** Stage 4 is composed with, not replaced. |
| `vars` count | 60 | **61** |
| `config_sha256` | `0b5d27030136500373…` | **`38a73675b28f555cb8…`** |
| `_stage4_amend1_note` | *(absent)* | added — what the dial is, the statistic and the resolution fade it is built from, why it is a manifest dial rather than a kill-switch, and why it is not a `_V0SURF_GATES` key |

## data/rl_build/rl_app_data.json + its sidecar

| field | old | new |
|---|---|---|
| board file md5 | `b490ae8b3bbd28b908ccb923ed8412c1` | **`b56bbddea15fd48e35b5794b1b5e9e23`** |
| `.srcmd5` `own_md5` | `b490ae8b3bbd28b908ccb923ed8412c1` | **`b56bbddea15fd48e35b5794b1b5e9e23`** |
| `.srcmd5` `source_md5` (the store) | `37ced3ce45914e6feb00d27e26922e9a` | unchanged — the store did not move |

## NOT re-pointed, and why

* **`_V0SURF_GATES`** — `RL_SUR_W` is deliberately absent. The change never leaves `sitout_ev`, whose only
  caller is `ev()`, and the year-zero surface never calls `ev()`. See `FIT_COUPLING.md`.
* **`engine/rl_after/pvc_curve_v2.json`** (the settled ladder, `curve_md5` `18203822`, pick 1 = 3000),
  **`ui/release_pick_curve.json`**, the **LEG F5 entrant seal** `5c38e8ba`, the numéraire block: all
  **UNTOUCHED**. This amendment moves no ladder, no curve and no numéraire, so none of their stamps is owed
  a move. Asserted programmatically in the side-by-side workbook build: the ladder is **byte-identical to
  stage 4 at all 64 picks**. `NUMÉRAIRE GUARD: PASS — shipped pick-1 = 3000`.
* **`one_source_selftest.py`** pins (`_contract_md5`, `_curve_source_store`, `_per_entrant_md5`) —
  **UNMOVED**. The self-test passed **143 / 0** with them as they stand; **0 re-points**.
* **The harness pins** (`harness_pvc_REPINNED_pass3.py`): `EXPECT_STORE` `37ced3ce`, `EXPECT_V0SURF`
  `3e8e50de5103`, `EXPECT_N` `1197`. All three RE-MEASURED on the amendment matrix and all three came back
  unchanged, so **nothing was re-pointed and no assert was patched**. Emitter banner:
  `store=37ced3ce engine=bc45d773 v0surf=3e8e50de51030297c99cf367161c161f frozen=True`.

## RE-POINTED, and disclosed

Two measurement instruments carry a **hardcoded input filename**, not a pin. Both were re-pointed from the
stage-4 matrix to this one, and that is the only edit either file received:

| file | change |
|---|---|
| `noarb/noarb_ext_338.py` | default `MATRIX` → `per_entrant_338_stage4a1.json` |
| `noarb/goal_metrics.py` | default `MATRIX` → `per_entrant_338_stage4a1.json`; board input → `board_STAGE4A1_b56bbdde.json` |

No method, constant, population filter or assertion in either file was touched.

## Gates, on the amendment build

| gate | result |
|---|---|
| ENV PIN (numpy 2.4.4 + bundled OpenBLAS `05c9f9eb`) | **PASS** |
| Guard 5 (boot store / rl_model / fv, checkout + loaded-path) | **PASS** |
| CONFIG MANIFEST (gate mode, 61 vars) | **LOADED**, hash `38a73675b28f`, ambient cleared |
| CONFIG-MANIFEST CHECK (`config_manifest.py check`) | **PASS** — pin + stored consistent |
| PARITY GATE (804 board values == engine gated `ev()`) | **PASS**, 804/804, eps=0 |
| NUMÉRAIRE GUARD (shipped pick-1 = 3000) | **PASS** |
| BOOK ↔ BOARD PARITY | **PASS**, all 802 shared players (2 `_pvc_exclude` outside the cohort book) |
| FUT-LABEL | **PASS** (87 dual rows) |
| ZERO-EMPTY-CLUB | **PASS** (0 blank across 1002 rows) |
| v0surf frozen-load assert | **PASS** — `frozen=True`, signature `3e8e50de5103`, zero fits at build |
| self-test | **PASSED**, **143 assertions, 0 FAIL**, exit 0 — same count as stage 4, **0 re-points** |
| `RL_SUR_W=0` kill-switch | **PASS** — reproduces board `b490ae8b` **byte-exact** through the full gate |
