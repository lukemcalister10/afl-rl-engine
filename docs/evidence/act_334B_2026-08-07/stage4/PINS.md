# STAGE 4 — PINS, old → new

Baseline `c0ea507` (stage 3). Every identity below was **measured from the artifact that carries it**,
after that artifact was written. None was typed from an expectation.

## data/expected_boot.json

| pin | old | new | moved? | why |
|---|---|---|---|---|
| `engine_head` | `a0a20d6e1a9b0d1a7dbb0aa64908aa13` | **`9a0c7fdc90f1ac8aed50692947e1b418`** | **MOVED** | `_merged_recover.py` is the one engine file this stage touches (`PED_BAR`, `_ped_prior`, the conditioned `lam` in `sitout_ev`). |
| `config` | `cef06fd6250be868…` | **`0b5d27030136500373f558ea345ea4a7d0288b1795a23d38ae641da208a2ebdd`** | **MOVED** | `RL_PED_BAR` is a VALUED owner dial and is enumerated in `data/model_config.json` (60 vars, was 59). Re-stamped in the same commit, as the manifest's own doc requires. Verified: `python3 config_manifest.py check` → PASS. |
| `board` | `6c9f8d3a92ca82c29dfaa8273a4f3ada` | **`b490ae8b3bbd28b908ccb923ed8412c1`** | **MOVED** | the rebuilt board. Stamped AFTER the build, from the built artifact. |
| `v0surf` | `9713ec6c83270ab916bb4a5e3ded6cb3` | unchanged | **unmoved** | NOT refit and not owed one — `FIT_COUPLING.md`. Re-verified on this box at three dial values, all reproducing the committed pickle. |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | unchanged | unmoved | `rl_model.py` NOT touched. |
| `fv` | `0976195c8454…5f5f18a87` | unchanged | unmoved | `engine/forward_valuation/` untouched; recomputed and asserted by bootstrap (checkout + loaded-path). |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | unchanged | unmoved | read-only stage. |
| `band` (cm_400) / `q97m` / `register` / `peak_model` / `pvc_snapshot` / `bust_prior` / `balanced_board_md5` | — | unchanged | unmoved | nothing in those lanes moved. |

## data/model_config.json

| field | old | new |
|---|---|---|
| `vars.RL_PED_BAR` | *(absent)* | **`"0.5"`** — inserted after `RL_YCRED_KPF`, beside the other valued young/thin-record dials |
| `vars` count | 59 | **60** |
| `config_sha256` | `cef06fd6250be868…` | **`0b5d27030136500373…`** |
| `_stage4_note` | *(absent)* | added — what the dial is, why it is a manifest dial rather than a kill-switch, and why it is not a `_V0SURF_GATES` key |

## data/rl_build/rl_app_data.json + its sidecar

| field | old | new |
|---|---|---|
| board file md5 | `6c9f8d3a92ca82c29dfaa8273a4f3ada` | **`b490ae8b3bbd28b908ccb923ed8412c1`** |
| `.srcmd5` `own_md5` | `6c9f8d3a92ca82c29dfaa8273a4f3ada` | **`b490ae8b3bbd28b908ccb923ed8412c1`** |
| `.srcmd5` `source_md5` (the store) | `37ced3ce45914e6feb00d27e26922e9a` | unchanged — the store did not move |

## NOT re-pointed, and why

* **`_V0SURF_GATES`** — `RL_PED_BAR` is deliberately absent. See `FIT_COUPLING.md` §(c).
* **`engine/rl_after/pvc_curve_v2.json`** (the settled ladder, payload `18203822`, pick 1 = 3000),
  **`ui/release_pick_curve.json`**, the **LEG F5 entrant seal** `5c38e8ba`, the numéraire block: all
  UNTOUCHED. This stage moves no ladder, no curve and no numéraire, so none of their stamps is owed a
  move. `NUMÉRAIRE GUARD: PASS — shipped pick-1 = 3000`.
* **`one_source_selftest.py`** pins (`_contract_md5`, `_curve_source_store`, `_per_entrant_md5`) —
  UNMOVED. The self-test passed 143/0 with them as they stand; nothing in this stage moves the artifacts
  they name.
* **The harness pins** (`harness_pvc_REPINNED_pass3.py`): `EXPECT_STORE` `37ced3ce`,
  `EXPECT_V0SURF` `3e8e50de5103`, `EXPECT_N` `1197`. All three RE-MEASURED on the stage-4 matrix and all
  three came back unchanged, so **nothing was re-pointed and no assert was patched**. The emitter's own
  banner confirms it: `store=37ced3ce engine=9a0c7fdc v0surf=3e8e50de5103 frozen=True`.

## Gates, on the stage-4 build

| gate | result |
|---|---|
| ENV PIN (numpy 2.4.4 + bundled OpenBLAS `05c9f9eb`) | **PASS** |
| Guard 5 (boot store / rl_model / fv, checkout + loaded-path) | **PASS**, twice — at bootstrap and again post-pin |
| CONFIG MANIFEST (gate mode, 60 vars) | **LOADED**, hash `0b5d27030136`, ambient cleared |
| CONFIG-MANIFEST CHECK (`config_manifest.py check`) | **PASS** — pin + stored consistent |
| PARITY GATE (804 board values == engine gated `ev()`) | **PASS**, 804/804, eps=0 |
| NUMÉRAIRE GUARD (shipped pick-1 = 3000) | **PASS** |
| BOOK ↔ BOARD PARITY | **PASS**, all 802 shared players (2 `_pvc_exclude` outside the cohort book) |
| FUT-LABEL | **PASS** (87 dual rows) |
| ZERO-EMPTY-CLUB | **PASS** (0 blank across 1002 rows) |
| v0surf frozen-load assert | **PASS** — `frozen=True`, signature `3e8e50de5103`, zero fits at build |
| self-test | **PASSED**, **143 assertions, 0 FAIL**, exit 0 — same count as stage 3, **0 re-points** |
