# LANE B — DATA ARTIFACTS: derivation-basis inventory (READ-ONLY)

Repo `/home/user/afl-rl-engine`, working tree = `6df4eea` (same content/subject line as the stated
`43e3095`: "register v544 + CURRENT_STATE v36 …"). Nothing was written, committed or pushed in the repo.

## Reference identities used for classification

| Token | Value | Standing |
|---|---|---|
| store (current) | `81d2470440a80f72afea4405e94338c5` | RULED-CURRENT |
| store (predecessor, same era) | `6b9d00a75ca88122c42da9189739916b` | acceptable same-era |
| store `265f55d5…`, `e3aaba77…`, `968de0c7…`, `c120cfd5…`, `f37d9716…`, `b0c39d78`, `b1fd0bce`, `340a7a32`, `a2fbc9a0` | pre-adoption | STALE |
| ruled pick curve | payload `e69a3f38` (session_2026-07-30/item279) | RULED-CURRENT |
| shipped pick curve | payload `08ea9375` (`pvc_curve_v2.json`) | STALE (canonical example) |
| ruled basis | VOR γ=1.0 · structural completion · ≤2022 cut · per-season par | — |
| superseded | SCAR γ=0.85 · prior-blend · gfut-keyed par · v3.4 kernel heads · hard pick-1 pin · pool_value 299 (ruled level 234.3) | — |

**Tree-level finding, stated once up front:** *no artifact anywhere in the tree carries the ruled payload
`e69a3f38`.* An exhaustive scan of every `*.json` in the repo for a `curve`/`curve_md5` block returns exactly
five curve artifacts — `pvc_curve_L1b.json` (`645fce16`), `pvc_fit_candidate.json` (unstamped),
`pvc_curve_v2.json` (`08ea9375`), and the two `session_2026-07-28/item207_stage1` candidates (`735face8`,
`536ba9ef`). `session_2026-07-30/item279` does not exist as a directory. The ruled curve is a ruling, not yet
an artifact; every curve-rooted row below is therefore stale by construction, not by drift.

---

## Table

Classification key: **SR** = STALE-ROOTED · **RC** = RULED-CURRENT · **HS** = HISTORICAL-SEALED · **UN** = UNCLEAR.

### A. Pick-curve artifacts (`engine/rl_after/`)

| # | Artifact | Path (+field) | Role | Derivation basis (as stamped in the file) | Class | Evidence pointer |
|---|---|---|---|---|---|---|
| A1 | **Shipped pick curve** | `engine/rl_after/pvc_curve_v2.json` → `curve` (1–64), `curve_md5` | THE release-active pricing curve; loaded into `_PVC0` and into the shipped ladder | `derived_from`: "session_2026-07-29/item271/out/per_entrant_271.json **(store 265f55d5)**"; `stamp.store_md5` `265f55d5`; `stamp.statistic` **"SCAR"**; `stamp.per_entrant_md5` `2f8b4bd4`; `stamp.v0surf_sig_at_fit` `85e57195…`; `source`: "session_2026-07-29/item271/derive_271.py — ITEM 271 stage B … Carries derive_pvc2.py function for function via #225 stage 2"; windows pool 2004–2024 / priors 2006–2020; `curve_md5` `08ea9375` | **SR** | file lines 69–96, 104; loaded `rl_export.py:135-138`, `_merged_recover.py:1614`, `rl_model.py:931` |
| A2 | **Pool level** | `engine/rl_after/pvc_curve_v2.json` → `pool_value` = **299** | the single position-blind ladder level for everything past pick 64 | Same artifact. Its own `note`: *"pool_value is the RULED pool level **on SCAR** … build_pvc_v34's step 5 maps posval-VOR units to SCAR by anchoring the pooled top band to the legacy realised value, so this artifact is **SCAR-denominated BY CONSTRUCTION**"*; `stamp.prev_pool_value` 528 | **SR** | `pvc_curve_v2.json:104,108`; ruled level is 234.3, tree carries 299 |
| A3 | Curve fit-time diagnostics | `pvc_curve_v2.json` → `gy0_offline` {pooled_abs_pct 0.257, mean_rel_pct 0.11}, `ladder_total` 65925, `pool_rows` 1093, `nd_curve_rows` 1325 | measurements-of-record for the stage-B fit | Same SCAR/`265f55d5` fit | **HS** | measurements, not consumed as inputs; they document A1 |
| A4 | Superseded L1b curve | `engine/rl_after/pvc_curve_L1b.json` → `curve` (1–99), `curve_md5` `645fce16` | fallback curve selected when `RL_PVC2=0` — still a live code path | `derived_from`: `session_2026-07-12/v2_9_candidate/out/pvc_curve_smoothed.json`; `source`: "l1_adopt_sim.py option-(b) … PAVA isotonic + kernel-smoothed adaptive-bandwidth fit; **pick-1 pinned to the owner's 3000 anchor**" | **SR** | `rl_export.py:135` (`_pvc_art` branch), `_merged_recover.py:1585`; pre-split 1–99 domain, hard pick-1 pin |
| A5 | Non-bakeable fit candidate | `engine/rl_after/pvc_fit_candidate.json` → `curve` (1–99), `store_md5` | v2.9 L1 candidate curve, loaded when `RL_PVCFIT`/`_W4PVC` set (manifest holds `RL_PVCFIT=0`) | `store_md5` **`b0c39d78`**; `fitted_from`: "derived_curve.json pinned_d15_H10 (icbhpu 3c1d610f) + L1b local-linear smoothing h=0.20"; `window` "2004-2016 classes, d15 live lens, H=10"; `n_anchors` 543; `candidate`: "v2.9 L1 — NON-BAKEABLE (R3 bake-guard)" | **SR** | file lines 103–108; `_merged_recover.py:1625-1627` |
| A6 | Train-time PVC feature | `engine/rl_after/pvc_snapshot.json` (bare 1–99 map, 3000/2496/2241/2076…) | **live `logPVC` feature** fed to the peak model at serve time | No stamp in the file. Consumer comment: *"the peak-model's TRAIN-TIME PVC feature (logPVC), FROZEN by design to break the SCALE↔PVC↔peak_est bootstrap cycle. **This is NOT the live PVC and must NOT track it**"*. Co-emitted by `build_peak_model_v4.py`. Pinned in `expected_boot.json:pvc_snapshot` = `735d2dec…` | **UN** | `rl_model.py:657`; `build_peak_model_v4.py:74-93`. It IS a live pricing input on a curve that is neither the ruled curve nor A1, but an explicit anti-skew law forbids re-pointing it alone — it can only move together with `peak_model_v4.pkl`. Needs an owner call. |
| A7 | Numéraire / v3.4 curve sidecar | `engine/rl_after/pick_redenomination.json` → `factor` 1.0524, `frozen_v34_pvc_baked_v2_7` (1–99) | `factor` is read live as the numéraire divisor on every displayed player value; the embedded curve is the **v3.4 kernel-head** ladder | `factor_provenance`: "MEASURED … from the regenerated board SCALE ratio (new 4.68336 / baked 4.45 = 1.052440)"; owner ruling 2026-07-11; the v3.4 map is the "frozen v3.4 pick values" the redenomination restated | **SR** | `rl_export.py:132`, `s4_matrix_M1v7.py:129`, `one_source_selftest.py:65`. The `frozen_v34_pvc_baked_v2_7` values (3000/2501/2249/2085/1967/1875/1795/1706/1604/1492/1381/1270…) are exactly the `draftval` column of the walk-forward book (row B7) — the v3.4 heads are still live through that path. |
| A8 | Provenance contract mirror *(adjacent to lane, in `ui/`)* | `ui/release_pick_curve.json` → `curve_source_store_md5`, `pool_value`, `per_entrant_md5` | the frozen-ruler contract the self-test binds A1 against | `curve_source_store_md5` **`265f55d568f35af33a3e27c0a7d7886a`**; nested `curve_source_store_md5` `968de0c7…`; `pool_value` **299**; `per_entrant_md5` `2f8b4bd4`; `_doc`: "The curve was DERIVED on store 265f55d5; the adopted store is 6b9d00a7 …" | **SR** | file lines 2, 9, 16, 21–24; pinned by `one_source_selftest.py:499-500` as `_curve_source_store='265f55d5…'`, `_per_entrant_md5='2f8b4bd4'`, contract md5 `11adecc8…` (verified on disk) |

### B. Position-layer, table and matrix artifacts (`engine/rl_after/`)

| # | Artifact | Path (+field) | Role | Derivation basis | Class | Evidence pointer |
|---|---|---|---|---|---|---|
| B1 | Young-credit cell table | `engine/rl_after/ycred_table.json` → `table`, `G0`, `grid_picks` | **LIVE pricing input** (manifest `RL_YOUNG=1`); halts the build if absent | **No store / curve / date stamp anywhere in the file.** `doc`: "INPUT: the CREDIT-OFF (RL_YOUNG=0) walk-forward as-of matrix (**s4_matrix machinery**)"; `G0_basis` "classes 2004-2020"; trailing tables T=2007..2026; GEN_DEF rows replaced 2026-07-11 by `session_2026-07-11/chapter_levers/`. `grid_picks` runs **1–90** | **SR** | `_merged_recover.py:1003-1006` (HALT if absent). Its input is the s4_matrix book, whose `draftval` is the frozen v3.4 curve (B7) → old-curve-rooted. Also pre-split domain (1–90). |
| B2 | Bust prior table | `engine/rl_after/bust_prior_table.json` → per-position pick→value, domain **1–70** | LIVE pricing input (`rl_model.py:656`) and a training input to `peak_model_v4.pkl` | **No `_doc`, no store, no curve, no date, no method note — zero provenance of any kind.** Pinned only by md5 in `expected_boot.json:bust_prior` = `5942aa6a…` | **UN** | `rl_model.py:656`; `build_peak_model_v4.py:1,16`; `single_source.py:35`. Cannot be classified by basis because the file records none; the 1–70 domain predates THE SPLIT. |
| B3 | LTI return table | `engine/rl_after/lti_return_table.json` → `age_surface`, `cap`, `leakcut` | LIVE pricing input (manifest `RL_LTI_RETURN=1`); halts if absent | `date` **2026-07-09**; `store_note`: *"derived on store **a2fbc9a0** (post King/Murphy fix)"*; `method` "net-of-aging … adaptive-bw NW over return-age, eff-n>=35; classes POOLED … monotone-in-age; capped at 0.15"; `leakcut` **2024** | **SR** | `_merged_recover.py:1701-1704`. Old store `a2fbc9a0` (not in the current lineage at all) and a 2024 leak-cut against the ruled ≤2022 cut. |
| B4 | Pass-mark / band table | `engine/rl_after/rl_passmark.json` → `pm_pos`, `pm_band`, `bands`, `BAND_ANCHOR`, `BUST_BAND` | LIVE pricing input — loaded unconditionally at engine import | **No store / curve / date / method stamp.** `bands` last band is `[49, 99]`, `BAND_ANCHOR` last is 60 | **UN** | `rl_model.py:29` (`PMD=json.load(open('rl_passmark.json'))`). Unstamped; `[49,99]` band is a pre-split domain. |
| B5 | Peak / age-curve params | `engine/rl_after/params.json` → `PEAK`, `PEAK_AGE`, `AGE_CURVE` | LIVE pricing input — loaded unconditionally at engine import | **No stamp of any kind.** | **UN** | `rl_model.py:29` (`P=json.load(open('params.json'))`) |
| B6 | ND-end chaining table | `engine/rl_after/national_draft_last_pick.json` → `last_national_pick` | LIVE — chains RD/PSD effective picks | `_provenance_summary`: "RE-DERIVED **2026-07-11** … from the store's own National rows, under the owner data law"; `basis`: "store MAX National ordinal per year"; `sources`: "engine store rl_model_data.json National (ND) sequences". **No store md5 recorded** | **UN** | `rl_model.py:253`. Basis is "the store" generically; the store has moved many times since 2026-07-11, so the pin cannot be verified. It is an *ordinal/identity* table, not a priced quantity — low blast radius. |
| B7 | **Walk-forward book / matrix** | `engine/rl_after/s4_matrix_M1v7.json` (+ `_blend.json`, `_retainonly.json`), 2 649 rows, field `draftval` | the book behind the F2 book↔board gate, the `ycred` derivation input, and the render path | `draftval` per row = **3000, 2501, 2249, 2085, 1967, 1875, 1795, 1706, 1604/1605, 1492, 1381, 1270 …** — byte-identical to `pick_redenomination.json:frozen_v34_pvc_baked_v2_7`, i.e. the **frozen v3.4 kernel-head curve**, not `pvc_curve_v2` (whose head is 3000/2767/2693/2469/2224…). No store/curve stamp inside the JSON; the generator is `s4_matrix_M1v7.py` | **SR** | compare `s4_matrix_M1v7.json` `draftval` vs `pick_redenomination.json:frozen_v34_pvc_baked_v2_7`; consumers `one_source_selftest.py:139`, `s4_render_M1v7.py:5`, `ship_gates_check.py:295`, `verify/d15/book_hashcheck.py:106` |
| B8 | Export attribution sidecar | `engine/rl_after/export_attribution.json` → `vPrev`, `levers`, `base_sum` 723075, `full_sum` 732725, n 804 | **read live** by the exporter; ships the board's `vPrev` and per-lever columns | `source`: *"certified G-ATTR stage boards (gen_gattr_chain.sh; **engine 2030e5df, store b0c39d78**)"* | **SR** | file `source` field; `rl_export.py:269-274`, consumed at `rl_export.py` `player_rec` → `'vPrev'`, `'levers'`. **Display-only** by declaration ("neither field feeds `v`"), but the values ship on the board and are two engine-eras + several stores behind. Visible in `ui/data/board_view_working.js` (e.g. Sheezel `"vPrev":8116`). |
| B9 | Collision sentry | `engine/rl_after/collision_sentry.json` → `pairs` | identity assertions against the single store | `version` 1.0, `date` 2026-07-09; asserts *against whatever the current store is* — no basis dependency | **RC** | `_doc`; basis-independent identity guard, not a pricing input |
| B10 | **The store** | `engine/rl_after/rl_model_data.json` (2 651 rows) | THE single source; every derived artifact roots here | on-disk md5 = **`81d2470440a80f72afea4405e94338c5`** = the ruled current store | **RC** | verified by `md5sum`; matches `expected_boot.json:store`, `release_contract.json:identities.store`, `season_state.json:source_store_md5` |

### C. `data/*.json`

| # | Artifact | Path (+field) | Role | Derivation basis | Class | Evidence pointer |
|---|---|---|---|---|---|---|
| C1 | **Board of record** | `data/rl_build/rl_app_data.json` → `PVC`, `picks`, `GAMMA` | THE shipped board / entire priced universe | On-disk md5 `f2df6e0a…` = `expected_boot.board`. Its `PVC` map is **byte-identical to `pvc_curve_v2.json`** (65 keys: 1–64 + pool index 65 = **299**; `PVC[64]`=571). Its `GAMMA` field = **`0.85`** | **SR** | `python3 -c` dump of `PVC`/`GAMMA`; the board is built on the SCAR γ=0.85 basis and the stale curve `08ea9375` |
| C2 | Board source pin | `data/rl_build/rl_app_data.json.srcmd5` | ties board→store | `{"derived":"rl_app_data.json","own_md5":"f2df6e0a…","source":"rl_model_data.json","source_md5":"81d2470440a80f72afea4405e94338c5","tier":1}` | **RC (store side) / SR (what it certifies)** | the *store* pin is current; it certifies a board built on the stale curve, so the pin is honest and the board is not |
| C3 | **Boot identity manifest** | `data/expected_boot.json` → `store`, `board`, `engine_head`, `rl_model`, `fv`, `config`, `band`, `register`, `balanced_board_md5`, `q97m`, `peak_model`, `pvc_snapshot`, `bust_prior`, `v0surf`, `as_of_round`, `release_version` | the pinned boot identity every gate/panel/bake asserts on entry (Guard 5) | **Pure ids (no measurement):** `store` `81d24704…` (RC), `board` `f2df6e0a…`, `engine_head` `404e8113…`, `rl_model` `7349a1e4…`, `fv` `d10aa93e…`, `config` `45b207c0…`, `band` `34faa865…`, `register` `652d83e8…`, `balanced_board_md5` `4939d740…`, plus the four fitted-artifact pins `q97m` `cfdc7321…`, `peak_model` `b763f59e…`, `pvc_snapshot` `735d2dec…`, `bust_prior` `5942aa6a…`, `v0surf` `ce08c2d1…`. **Measurements / state, not ids:** `as_of_round` **20**, `release_version` `v2.11-final-rc1-PROVISIONAL`. **Measurements embedded in `_*_note` prose:** `_board_note_split` ("Store **e3aaba77** UNCHANGED", "frozen v0surf … sig 76498b5a"), `_final_integration_note` (board pin `2ab73a6f…`, store `968de0c7`), `_engine_head_note` ("n=804 sum=723075", cohort gate 126.8/125.2/116.1), `_isofade_note` (1.561x→1.766x, +2749), `_reentry_trio_note` (106 v-movers, +30 num-SCAR), `_item20_note` (bramble +1, 182 club corrections) | **SR** | The *id block* is internally coherent with the current store, but every pin it certifies (`board`, `engine_head`, `rl_model`, `fv`) belongs to a build whose curve is `08ea9375` and whose γ is 0.85. The `_notes` are HS (dated narrative, incl. the `e3aaba77` reference which is provenance-of-record, not a live pin). Re-derivation moves `board`/`engine_head`/`rl_model`/`fv` here. |
| C4 | **Release contract — pvc block** | `data/release_contract.json` → `pvc_provenance` | binds the release to a curve | `adopted_pathway` "RL_PVC2", `curve_file` `pvc_curve_v2.json`, `curve_payload_md5` **`08ea9375`**, `numeraire_pin1` **3000** | **SR** | file lines 21–26. Points at the stale payload and pins the hard pick-1 anchor. |
| C5 | Release contract — identities | `data/release_contract.json` → `identities` | the bound release identity set | `store` `81d2470440a80f72…` (RC); `board` `f2df6e0a…`, `balanced_board_md5` `4939d740…`, `engine_head` `404e8113…`, `rl_model` `7349a1e4…`, `fv` `d10aa93e…`, `register` `652d83e8…`, `band` `34faa865…` | **SR** | same reading as C3: current store, stale-curve build |
| C6 | **Release contract — held_checks G-Y0** | `data/release_contract.json` → `held_checks[0].measured_at_declaration` | a DATED exception carrying live numbers | **Old-basis MEASUREMENTS:** `guard_population_pct` **3.035**, `ruled_population_pct` **2.929**, `stage_A_pct` **2.672**, `hard_bar_pct` **2.0**, `n_guard` **1326**, `n_ruled` **1325**, `ceiling_pct` **3.50**. `declared_by` "#271 Addendum 12 (owner word 2026-07-29)"; `cleared_at` "#279, post-adoption — a DATED exception"; `diagnostic_map` `session_2026-07-29/item271/GY0_DIAGNOSTIC_MAP.json` | **HS**, but **actively load-bearing** | file lines 72–91. These are measurements taken against the stage-B (SCAR / store `265f55d5`) fit. `n_ruled`=1325 equals `pvc_curve_v2.stamp.nd_curve_rows`=1325 — the declaration is welded to the stale fit population. `ceiling_pct` 3.50 is a live DO-NOT-EXCEED bar; a re-derivation invalidates the measured side while the bar keeps biting. |
| C7 | Release contract — F5 reconciliation | `data/release_contract.json` → `f5_entrant_reconciliation` | the entrant-layer ladder totals | `visible_1_64` **65925**, `residual_nd_tail` 2631, `residual_mech` 9055, `entrant_layer_pvc` 77611, `seal` `a17aafed` | **SR** | `visible_1_64` 65925 is *exactly* `pvc_curve_v2.stamp.ladder_total` 65925 (verified: sum of the 64 curve values = 65925). This block is a measurement on the stale curve, carried inside a live contract covered by `contract_sha256`. |
| C8 | Release contract — present-lens baseline | `data/release_contract.json` → `present_lens_baseline` | the accepted present-v anchor | `balanced_board_md5` `4939d740…`, `active` 804, `present_value_total` **767198**; note recites superseded values 764021 / 760253 / 757608 / 755072 / 752427 and boards `6f07f7cb`, `fa172ac1` | **HS** | dated narrative + a live baseline number measured on the stale-curve board |
| C9 | Release contract — season metadata | `data/release_contract.json` → `season_metadata`, `season_state_policy_id` | class-A live valuation semantics | `exposure_pace` 0.773, `calendar_progress` 0.83, `as_of_round` 20, `derivation_policy_id` `39938f68…`; declares these DERIVED from the staged store each round | **RC** | consistent with C11; policy id immutable and matches `season_state.json` |
| C10 | **Transition register** | `data/release_lineage.json` → `release_transition`, `release_transition_register[]` | the historical provenance bridge; read (not enforced) to LABEL a movers boundary | Entry 1 (ITEM 408 / ITEM 411 D1): source store `f37d9716…` → destination `c120cfd5…`, boards `92a8f3a0…`→`fa172ac1…`. Entry 2 (#271 adoption, owner word 2026-07-30 "30/7 rederivation for the label. Adopt."): source store **`e3aaba77…`**, board `8a38cca4…` → destination store **`6b9d00a7…`**, board `f2df6e0a…`. Entry 3 (#283 ownership): store `6b9d00a7…` → **`81d24704…`**, board unmoved `f2df6e0a…`. Top-level `balanced_board_md5` `06d8af60…` declared the immutable present-lens anchor | **HS** | These are provenance-of-record citations of old stores — correctly historical, *not* live pricing inputs. The register is the clean model for how a stale id may legitimately appear in a live file. |
| C11 | Season state | `data/season_state.json` → all | LIVE valuation input (`calendar_progress`, `exposure_pace`) | `source_store_md5` **`81d2470440a80f72afea4405e94338c5`** (current); `derivation_policy_id` `39938f68…`; `exposure_derivation` {eligible_durable_players 305, median_current_games 17, denominator 22.0, raw_ratio 0.7727…, released_value 0.773, durable_min_prior_games 18}; `calendar_progress` 0.83 = round_half_up(100·20/24)/100 | **RC** | the only live-valuation data artifact in `data/` that is cleanly rooted on the current store and an immutable policy |
| C12 | **Model config manifest** | `data/model_config.json` → `vars` | the single versioned source for every model-semantics variable; `config_sha256` `45b207c0…` matches C3 + C5 | `vars["RL_GAMMA"]` = **`"0.85"`** · `vars["RL_PICK1"]` = **`"3000"`** · `RL_PVC2` 1 · `RL_PVCADOPT` 1 · `RL_PVCFIT` 0 · `PAR_*` block · `baked_state`: "FINAL-INTEGRATION v2.11-final-rc … board 039ff8d4 … **store 968de0c7 unchanged**"; `date` 2026-07-09; `version` 1.0 | **SR** | the SCAR γ=0.85 and the hard pick-1 pin — two named superseded items — are the *live* manifest values, sealed into the config hash that `expected_boot`, `release_contract` and every txn manifest assert on |
| C13 | Owner overrides | `data/owner_overrides.json` → `overrides` | display-layer single-player multiplier (Brodie ×0.5) | Owner read 2026-07-08; declared never to touch `v`, aggregates, book or guards | **RC** | basis-independent by construction |
| C14 | Book stability seal | `data/book_stable_seal.json` | walk-forward book freeze stamp | `head_md5` **`40f43772`**, `store_md5` **`968de0c7`**, `config` `c2d233ae…`, `n_players` 2649, `stable_sha256` `745e3462…`, `sealed_date` 2026-07-17, sealed at "LEG D ACT-2" | **HS** | a dated seal, no live reader found in `engine/**.py`; superseded by C3's `engine_head` `404e8113…` and store `81d24704…` |
| C15 | W4 candidate seal | `data/book_stable_seal_w4candidate.json` | candidate-integrity comparison | `basis` "W4 integration candidate"; `vs_baked` 2136 records moved | **HS** | dated candidate artifact |
| C16 | Report states register | `data/report_states.json` → `control`, `previous`, `states` | names the CONTROL/PREVIOUS comparator boards for the three-column gate | `control` `7a07e369` ("BAKED v2.8 … store 04f38dad, board 9ecbe0fa, config 69ead79b944d"); `previous` `efea88e5` ("BAKED v2.5 canonical (DPP strip; store e1b4d8bf)") | **HS** | read live at `ship_gates_check.py:103`, `s4_render_7147.py:10` — but by design a *named historical* comparator; naming an old state is the point |
| C17 | v2.5 gate comparator matrix | `data/s4_matrix_baked_efea88e5.json` | `V25_COMPARATOR` in the ship gates | store `e1b4d8bf` era (v2.5 DPP strip) | **HS** | `ship_gates_check.py:273` — comment states "v2.5 comparator — NAMED, never 'current'" |
| C18 | Other baked/candidate matrices | `data/s4_matrix_{baked_7a07e369,baked_c47cb43d,control_8aed420a,gradedfix_efc15c6c,nogames,v2_4a134d05,v21_c8051893,v22_af1fc6aa}.json` (8 files) | historical snapshots keyed by engine head | each keyed to a named historical head/store per C16 | **HS** | no live reader other than the C16/C17 named-comparator path |
| C19 | Gate snapshots | `data/gates_snapshots/gates_*.json` (23 files) | per-head gate results | each carries `head`/`store`/`config` (e.g. `gates_fc7045d6.json`: head `fc7045d6`, store `b1fd0bce`) | **HS** | `tools/seat/gates_score.py` reads them as snapshots by name |
| C20 | Trajectory fit output | `data/traj_out_2026-06-28.json` | dated cohort trajectory fit (`pooled`, `percohort`, `intercept` 92.68, `slope` 0.2001) | dated 2026-06-28; no store/curve stamp | **HS** | no reader found in the tree — orphan historical output |

### D. Ingestion state artifacts (`engine/rl_after/ingestion/`)

| # | Artifact | Path (+field) | Role | Derivation basis | Class | Evidence pointer |
|---|---|---|---|---|---|---|
| D1 | **Sibling repin sidecar** | `engine/rl_after/ingestion/sibling_repin_state.json` → `source_store_md5` | LIVE state sidecar for the balanced-board / forward-vector repin | `source_store_md5` **`e3aaba772f339551cd223802ab115af7`** (stale); `balanced_board_md5` `4939d740…`; `forward_board_md5` `8a38cca4…`; `contract_sha256` **`26d962e0…`** (≠ the live contract's `3ede10d3…`); `present_value_total` 767198; `generated_at_commit` **2026-07-28T02:02:53Z**; `fv_identity` `6a9a520f…` (≠ boot `d10aa93e…`) | **SR** | file lines 5, 6, 12, 19. Known-stale and confirmed: it pins `e3aaba77`, a board (`8a38cca4`) and a contract hash and an fv identity that the tree has all moved past. |
| D2 | **Finalization state** | `engine/rl_after/ingestion/finalization_state.json` → `rounds["20"]` | LIVE round-finalization tail; `board_md5_after` is the "what did we last commit" pointer | Round 20: `board_md5_before` `fa172ac1…` → `board_md5_after` **`8a38cca4…`**, `store_md5_after` **`e3aaba77…`**, `core_committed_at` 2026-07-28T02:02:53Z, `release_identity.engine_head` `7c452715…`, `release_identity.balanced_board_md5` `06d8af60…`. Rounds 15–19: engine_head `dc7e34b0…`, stores `968de0c7`→`f37d9716` | **SR (round 20 tail) / HS (rounds 15–19)** | the live tail points at board `8a38cca4` and store `e3aaba77`, both superseded by `f2df6e0a` / `81d24704`; the R15–19 records are sealed production history |
| D3 | Movers report R20 | `engine/rl_after/ingestion/movers/movers_R20.json` → `source_store_md5_after`, `board_md5_after` | the current-round movers bundle | `source_store_md5_before` `c120cfd5…` → `source_store_md5_after` **`e3aaba77…`**; `board_md5_before` `fa172ac1…` → `board_md5_after` **`8a38cca4…`**; `previous_round` `"post-r19-redesign-1"`; `schema_version` 2; `release_identity.balanced_board_md5` `06d8af60…` | **SR** | same stale pair as D2; it is the *latest* bundle, i.e. the one a reader sees as "now" |
| D4 | Movers reports R15–R19 | `engine/rl_after/ingestion/movers/movers_R{15..19}.json` (+ `.csv`) | sealed production movers history | each stamps its own before/after board + store (e.g. R15 `968de0c7`→`692d6302`, R19 `64795076`→`f37d9716`), `engine_head` `dc7e34b0…`, generated 2026-07-21T16:17:44Z | **HS** | protected by the `release_lineage` transition bridge (C10); explicitly `historical_reports_immutable: true` |
| D5 | **Value history baseline** | `engine/rl_after/ingestion/value_history.json` → `players[*].by_round`, `columns` | week-to-week value baseline; re-read each round by the movers builder | `rounds` [14…20]; `columns` = `{after_round 19, board fa172ac1…, id "post-r19-redesign-1"}`, `{after_round 20, board **f2df6e0a…**, id "rederivation-30-7", label "30/7 rederivation"}`. So the latest column's values are the current board's — i.e. **the stale-curve, γ=0.85 board** | **HS** | `round_movers.py:273,575,593,646`. Classified HS because the values are consumed only to compute *deltas and rank columns* — they never re-enter `v`. Flagged: the baseline the next round diffs against is on the stale basis, so a re-derivation will show as a one-off league-wide mover unless a new column is written for it (the standing preference in C10 entry 2: "big moves get a movers snapshot when cheap; missed eras are never backfilled"). |
| D6 | Rank / pos-rank history | `engine/rl_after/ingestion/rank_history.json`, `pos_rank_history.json` | same, for overall and within-position rank | identical `columns` block, same `rederivation-30-7` / board `f2df6e0a…` tail | **HS** | `round_movers.py:274-275,594-595`; same reading as D5 |
| D7 | Applied-rounds ledger | `engine/rl_after/ingestion/applied_rounds_ledger.json` → `applied[]` | dedup ledger of `(stable_player_id\|season\|round)` triples | identity triples only; no store/curve/value | **RC** | basis-independent; frozen by `sibling_repin.FROZEN_REL["score_ledger"]` |
| D8 | Catch-up identity overrides | `engine/rl_after/ingestion/catchup_identity_overrides.json` → `overrides[]` | owner-authored name→stable-key resolution | owner ruling 2026-07-20; maps by stable key only | **RC** | basis-independent identity mapping |
| D9 | Ingestion proof | `engine/rl_after/ingestion/proof.json` | dated parser/ingest proof | `store_md5` **`968de0c7`**; sampled 625, passed 625; worked example Willem Duursma | **HS** | a dated proof pinned to the store it was run against |
| D10 | Weekly txn manifests | `engine/rl_after/ingestion/.weekly_txn/txn_catchup_r{15..20}/manifest.json` | per-round transaction records | each stamps `config_hash` `45b207c0…`, board before/after, `fv_provenance.distribution_pricing_md5` `dd19a234…`, `guard5_green` true, created 2026-07-21 / 2026-07-28 | **HS** | sealed transaction history |
| D11 | Finalization journal | `engine/rl_after/ingestion/finalization_journal.jsonl` | append-only journal | dated append log | **HS** | historical by construction |

### E. Session artifacts consumed at runtime

| # | Artifact | Path (+field) | Role | Derivation basis | Class | Evidence pointer |
|---|---|---|---|---|---|---|
| E1 | Leg-D per-entrant table | `session_2026-07-17/legd_derivation/out/per_entrant.json` (2 649 rows; on-disk md5 **`40d7da7c7461024048fe48fcba5692ff`**) | listed in `sibling_repin.FROZEN_REL` — asserted **byte-unchanged** before/after every reconcile | Leg-D act-2 derivation output (2026-07-17 era, store `968de0c7`). **Its values are never read** — only its bytes are hashed | **HS** | `sibling_repin.py:102`, and `:45` "…All are asserted byte-unchanged before/after every reconcile." **Important distinction:** this is a *freeze-guard target*, not a pricing input. It is also **not** the curve's derivation input — see E2. |
| E2 | **The curve's actual per-entrant input** | `session_2026-07-29/item271/out/per_entrant_271.json` (`per_entrant_md5` **`2f8b4bd4`**) | the file `pvc_curve_v2.json` was actually derived from | Its own header stamps `v0surf_sig` `85e57195…`; the curve's `derived_from` names it **"(store 265f55d5)"** | **SR** | `pvc_curve_v2.json:71,94-95`. This is the stale root. Note the naming trap: `one_source_selftest.py:500` pins `_per_entrant_md5='2f8b4bd4'` (this file) while `sibling_repin.py:102` freezes a *different* file (E1, `40d7da7c`) under the same word "per_entrant". |
| E3 | **Sealed entrant slot structure** | `session_2026-07-18/legf5/sealed_entrant_structure.json` → `draft_occupancy`, `mech_occupancy`, `pickeq`, `stamp` | **read live at build** and seal-verified (HALT on drift); its per-effective-pick occupancy counts are re-priced at the live PVC to produce the visible future-draft asset ladder | `stamp`: `store_md5` **`968de0c7`**, `curve_payload_md5` **`89c14729`** (the *pre-split* v2 payload), `curve_file_md5` `56dd7a7b`, `board_balanced_md5` `06d8af60`; `window` **[2019, 2025]**; `n_years` 7; `seal_sha256_8` `a17aafed`; `basis` "FULL expected annual intake measured from recorded store intake history" | **SR** | `rl_export.py:659` (+ pin at `:751`), `forward_lens.py:56,106,150`. The **counts** are what is consumed and they were measured on store `968de0c7`, not `81d24704`. Occupancy runs past pick 64 (`'65': 0.5714`, `'66': 1.0`, …) and `pickeq` still carries the mechanism pedestals 90/92 — a pre-split shape. |
| E4 | …its embedded price totals | same file → `entrant_pvc` {draft 69266, mech 14272, total 83538}, `mech_summary[*].pvc_each` (470/473), `round_counts[*].pvc` | recorded measurements only | priced at `curve_payload_md5` `89c14729` (pre-split) | **HS** | `rl_export.py:645`: "The sealed COUNTS are the frozen measurement and are NOT touched here"; the engine re-prices via `_lf_pvc()` off the live `PVC`. These stale numbers are *not* consumed — but they no longer agree with the contract's `entrant_layer_pvc` 77611 (C7), so the file reads as internally contradictory. |

---

## Counts

| Classification | Count | Rows |
|---|---|---|
| **STALE-ROOTED** | **19** | A1, A2, A4, A5, A7, A8, B1, B3, B7, B8, C1, C2*, C3, C4, C5, C7, C12, D1, D2*, D3, E2, E3 → deduplicated to the 19 distinct artifacts listed below |
| **RULED-CURRENT** | **6** | B9, B10, C11, C13, D7, D8 |
| **HISTORICAL-SEALED** | **17** | A3, C6, C8, C10, C14, C15, C16, C17, C18, C19, C20, D4, D5, D6, D9, D10, D11, E1, E4 |
| **UNCLEAR** | **5** | A6, B2, B4, B5, B6 |

\* C2's *store* side is current (RC) while what it certifies is stale; D2's rounds 15–19 are HS while its round-20 tail is SR. Counted once each, at the more consequential reading.

The 19 distinct STALE-ROOTED artifacts: `pvc_curve_v2.json` (curve + `pool_value` counted once),
`pvc_curve_L1b.json`, `pvc_fit_candidate.json`, `pick_redenomination.json`, `ui/release_pick_curve.json`,
`ycred_table.json`, `lti_return_table.json`, `s4_matrix_M1v7*.json` (3 files, counted once),
`export_attribution.json`, `rl_app_data.json` (+`.srcmd5`), `expected_boot.json`,
`release_contract.json:pvc_provenance`, `release_contract.json:identities`,
`release_contract.json:f5_entrant_reconciliation`, `model_config.json`, `sibling_repin_state.json`,
`finalization_state.json` (round-20 tail), `movers_R20.json`, `per_entrant_271.json`,
`sealed_entrant_structure.json`.

---

## Notes

**1. The stale root is single and load-bearing.** Everything priced in this tree descends from
`pvc_curve_v2.json` payload `08ea9375`, derived from `per_entrant_271.json` on store `265f55d5` under
statistic `SCAR`. The board's `PVC` map is byte-identical to it and the board's `GAMMA` is `0.85`. The store
has since moved `265f55d5 → … → e3aaba77 → c120cfd5 → 6b9d00a7 → 81d24704`; the curve did not move with it.
The self-test enforces exactly that: `one_source_selftest.py:499` hard-pins `_curve_source_store =
'265f55d568f35af33a3e27c0a7d7886a'`, so the *stale binding is the passing state* and a re-derivation must move
that literal, `ui/release_pick_curve.json`, and its `_contract_md5` pin in one commit.

**2. Provenance-of-record vs live-value — the distinction, worked.** Three files cite old store ids and are
*correct* to do so: `release_lineage.json` (a transition register whose whole purpose is to name the
`f37d9716`/`c120cfd5`/`e3aaba77`/`6b9d00a7` chain), `expected_boot.json:_board_note_split` ("Store `e3aaba77`
UNCHANGED" — dated narrative), and `report_states.json` (named historical comparators). Against that,
`sibling_repin_state.json:source_store_md5 = e3aaba77` is *not* a citation — it is the sidecar's live opinion
of which store the balanced board and forward vector were pinned against, and it also carries a
`contract_sha256` (`26d962e0…`) and an `fv_identity` (`6a9a520f…`) that no longer match the tree
(`3ede10d3…` / `d10aa93e…`). Same id, opposite classification.

**3. `held_checks` embeds measurements, not identities — and they are welded to the stale fit.** The G-Y0
declaration numbers (3.035 / 2.929 / 2.672 / hard bar 2.000 / ceiling 3.50, n_guard 1326, n_ruled 1325) were
measured on the stage-B population. `n_ruled = 1325` is exactly `pvc_curve_v2.stamp.nd_curve_rows = 1325`. The
record is correctly HISTORICAL-SEALED as a *declaration*, but `ceiling_pct 3.50` is a live DO-NOT-EXCEED bar
and its own `reason` field says removing the record is a FAIL. After a re-derivation the measured side is
void while the bar still bites — this needs an explicit owner act, not a silent re-measure. Same shape for
`f5_entrant_reconciliation.visible_1_64 = 65925`, which is the stale curve's own `ladder_total`
(verified: the 64 curve values sum to 65925).

**4. Unstamped live pricing inputs are a distinct hazard class from stale ones.** `bust_prior_table.json`,
`rl_passmark.json` and `params.json` are read unconditionally by the engine at import and carry **no**
store, curve, date or method stamp — only an `expected_boot` md5 pin, which proves the bytes have not changed
but says nothing about what they were derived from. `ycred_table.json` has a long `doc` but no identity
stamp either; its declared input is the s4_matrix walk-forward book, and that book's `draftval` column is
the frozen v3.4 curve, so it is old-curve-rooted by transitivity even though it never names a curve. These
cannot be cleared by inspection; they need a derivation record before they can be classified.

**5. The v3.4 kernel heads are still live, through the book.** `pick_redenomination.json`'s
`frozen_v34_pvc_baked_v2_7` and the `draftval` column of all three `s4_matrix_M1v7*` files are the same
ladder (3000 / 2501 / 2249 / 2085 / 1967 / 1875 / 1795 / 1706 / 1604 …), which is *not* the shipped curve
(3000 / 2767 / 2693 / 2469 / 2224 …). The book feeds the F2 book↔board gate, the `ycred` derivation and the
render path. So the tree currently prices players off `08ea9375` while the book that gates and calibrates
them is on v3.4. That is a second, older curve basis running underneath the first.

**6. Domain drift from THE SPLIT is unresolved in the data layer.** `pvc_curve_v2.json` is 1–64 + one pool
index, but `bust_prior_table.json` is 1–70, `ycred_table.json:grid_picks` is 1–90, `rl_passmark.json:bands`
ends `[49, 99]`, `pvc_snapshot.json` and `pvc_curve_L1b.json` are 1–99, and
`sealed_entrant_structure.json:draft_occupancy` carries live counts at picks 65–99 with `pickeq` pedestals at
90/92. Relatedly, the position layer the split delegates the pool's differentiation to — `iso_corr(pos,pk)` —
is not a data artifact at all: it is fit at module load over `PICKS = list(range(1,71))`
(`_merged_recover.py:485-493`), i.e. still on a 1–70 pick domain, and `iso_corr` clamps at
`min(pk,70)`. Any pool re-pricing that leans on iso_corr inherits that.

**7. `pvc_snapshot.json` is a genuine conflict, not an oversight.** It is a live serve-time feature
(`rl_model.py:657`) whose values are a superseded curve, and its own consumer comment forbids re-pointing it:
*"This is NOT the live PVC and must NOT track it … feeding the live (post-bake) PVC here would be train/serve
skew."* Under the ruling it is a live pricing input rooted in an old curve; under its own law it must not
move alone. The resolution is to re-derive the pair `pvc_snapshot.json` + `peak_model_v4.pkl` in one act via
`build_peak_model_v4.py`, or to rule the freeze explicitly. Flagged UNCLEAR for the owner rather than guessed.

**8. Two different files are called "per_entrant".** `one_source_selftest.py:500` pins
`_per_entrant_md5='2f8b4bd4'` = `session_2026-07-29/item271/out/per_entrant_271.json` (the curve's real
derivation input, store `265f55d5`). `sibling_repin.py:102` freezes
`session_2026-07-17/legd_derivation/out/per_entrant.json`, on-disk md5 `40d7da7c…` (the Leg-D era file, whose
*bytes* are guarded and whose *values* are never read). A re-derivation that updates "the per_entrant pin"
must be explicit about which. `session_2026-07-22/item408_stop1/build_stop1_candidate.py:44` records the
07-17 file as "per-entrant 40d7da7c", confirming the two are distinct and both tracked.

**9. `model_config.json` is where the two named superseded items actually live.** `RL_GAMMA = "0.85"` (SCAR)
and `RL_PICK1 = "3000"` (the hard pick-1 pin) are live manifest values, sealed into `config_sha256`
`45b207c0…` — which `expected_boot.json:config`, `release_contract.json:config_sha256` and every
`.weekly_txn/*/manifest.json:config_hash` assert on. Moving γ to 1.0 therefore moves the config hash and
re-stamps four other artifacts in the same commit. The manifest's `baked_state` still reads "store `968de0c7`
unchanged", three stores behind.

**10. The ingestion tail is one round behind the board.** `finalization_state.json:rounds["20"]` and
`movers_R20.json` both record `board_md5_after = 8a38cca4…` / `store_md5_after = e3aaba77…`, committed
2026-07-28T02:02:53Z — the same timestamp `sibling_repin_state.json` carries. The tree has since moved to
board `f2df6e0a` / store `81d24704` via the two `release_transition_register` entries (#271 adoption, #283
ownership), neither of which was a round apply. So the round-20 ingestion tail describes a board that is no
longer the board of record. The `value_history` / `rank_history` / `pos_rank_history` `columns` blocks *did*
get the `rederivation-30-7` column at board `f2df6e0a`, so the history layer is ahead of the finalization
layer — they disagree about what "now" is.

**11. `export_attribution.json` is display-only but ships stale numbers on the board.** Its `source` is
"certified G-ATTR stage boards (gen_gattr_chain.sh; engine `2030e5df`, store `b0c39d78`)" — the v2.9 era,
`base_sum` 723075. `rl_export.py` loads it live and stamps `vPrev` and `levers` onto every player row (visible
in `ui/data/board_view_working.js`, e.g. Sheezel `"vPrev":8116`, `"levers":{"L1":0,"L2":60,...}`). The
declaration "neither field feeds `v`" holds, so it is not a *pricing* input — but it is a live-read artifact
whose displayed deltas are measured against a board from several stores and two engine heads ago.

**12. What is actually clean.** Only six artifacts are RULED-CURRENT: the store itself
(`rl_model_data.json`, md5 verified `81d24704…`), `season_state.json` (current store + immutable
`derivation_policy_id` `39938f68…`), and four basis-independent identity/display artifacts
(`collision_sentry.json`, `owner_overrides.json`, `applied_rounds_ledger.json`,
`catchup_identity_overrides.json`). No priced artifact in the tree is currently on the ruled basis.
