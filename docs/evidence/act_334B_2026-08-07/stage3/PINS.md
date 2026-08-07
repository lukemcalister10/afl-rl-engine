# Stage 3 — PINS, old → new

Baseline is `93c2a9a` (stage 2 era-free). Every identity below was **measured from the artifact that
carries it**, at the moment it was written; none was typed from an expectation.

## data/expected_boot.json

| pin | old | new | moved? | why |
|---|---|---|---|---|
| `v0surf` | `d594dc034e86935b370c49b240a18370` | `9713ec6c83270ab916bb4a5e3ded6cb3` | **MOVED** | the DECLARED surface refit around the settled ladder. Written by `refit_v0surf.py --bake` itself (surgical single-line edit), not by hand. |
| `board` | `f94e0778f8ab49e81bba8658f1c14a4d` | `6c9f8d3a92ca82c29dfaa8273a4f3ada` | **MOVED** | the rebuilt board. Stamped AFTER the build, from the built artifact. |
| `engine_head` | `a0a20d6e1a9b0d1a7dbb0aa64908aa13` | `a0a20d6e1a9b0d1a7dbb0aa64908aa13` | unmoved | `_merged_recover.py` was **NOT touched**. No engine change was needed for the numéraire. |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | `b35c5521b78dcdfb2423d54f5574330b` | unmoved | `rl_model.py` was NOT touched. |
| `fv` | `0976195c8454…5f5f18a87` | unchanged | unmoved | `engine/forward_valuation/` untouched; `fv_identity()` recomputed and asserted by bootstrap. |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | unchanged | unmoved | read-only stage. |
| `q97m` / `band` (cm_400) / `register` / `config` / `peak_model` / `pvc_snapshot` / `bust_prior` | — | unchanged | unmoved | nothing in those lanes moved; no manifest dial moved (`config_sha256` unmoved). |
| `balanced_board_md5` | `123deccb0838c7370ce614d7f4310b01` | unchanged | unmoved | not regenerated this stage, as at stages 1 / 2 / ER. |

## engine/rl_after/pvc_curve_v2.json

| field | old | new |
|---|---|---|
| `curve` (64 values) | payload `df766dff…` (stage-2 teaching value `77408ecd…`) | **`18203822cf438ecef03ed77a771f9942`** |
| `curve_md5` (the in-file pin) | `df766dff` — STALE since stage 2 | **`18203822`** |
| file md5 | `988135efd99454f2363f02aa135b4840` (stage-2: `0c798f363418da038be93c8473fe54de`) | **`73d6f679dc62281b1640fb81a5ba5fe4`** |
| `numeraire.pooled_head_pre_scale` | 3017.9232 | **3384.3148448406** |
| `numeraire.s` | 0.9940610814748366 | **0.8864423487588727** |
| `numeraire.published_pin` | 3000.0 | 3000.0 — **UNMOVED** |
| `stamp.store_md5` | `f1e8c9fe` | **`37ced3ce`** |
| `stamp.per_entrant_md5` | `999d24c8` | **`b7ed144e`** |
| `stamp.v0surf_sig_at_fit` | `aca37f9f0e24…` | **`3e8e50de5103…`** |
| `stamp.item` / `ladder_total` / `nd_curve_rows` / `prev_curve_md5` | 271-stageB / 65925 / 1325 / f14a6622 | 334B-stage3 / 51221 / 1197 / df766dff |
| `pool_value`, `pool_levels`, `pin`, `numeraire_pin1_3000`, `gate`, `split`, `domain` | — | **UNTOUCHED** (owner-signed / structural) |

The superseded item-271 stamp is carried verbatim inside `stamp._superseded_stamp` rather than deleted.
Four derive_271-specific fields (`pool_rows`, `pool_never_established`, `prev_pool_value`, `windows`)
are NOT re-asserted here because this stage's machinery does not re-measure them; they live in
`_superseded_stamp` and the reason is recorded in `stamp._note`.

## ui/release_pick_curve.json (the FROZEN-RULER provenance contract, re-derived)

| field | old | new |
|---|---|---|
| file md5 | `eae593f220460d880be20da38e3de39d` | **`160f9fe77fd3f99707c48916f3d59e50`** |
| `curve_source_store_md5` | `f1e8c9fed35462536d00add604f69a3f` | **`37ced3ce45914e6feb00d27e26922e9a`** (full 32 chars, asymmetric stamp convention) |
| `per_entrant_md5` | `999d24c8` | **`b7ed144e`** (the final stage-3 matrix) |
| `pick_curve_curve_md5` | `df766dff` | **`18203822`** |
| `pick_curve_file_md5` | `988135efd99454f2363f02aa135b4840` | **`73d6f679dc62281b1640fb81a5ba5fe4`** |
| `pool_levels`, `pool_value`, `numeraire_pin1` | — | re-mirrored verbatim from the artifact (unchanged values) |
| `supersedes` | the pre-#271 `968de0c7` entry | the **`df766dff` / `f1e8c9fe`** entry, carrying the old `968de0c7` entry nested inside it |

The prior stamp went into `supersedes` following the file's own structure (`curve_source_store_md5`,
`per_entrant_md5`, `pick_curve_curve_md5`, `pick_curve_file_md5`, `pick_curve_path`, `pathway`, `note`),
with the previous `supersedes` object nested as this entry's own `supersedes` so the chain is not lost.

## engine/rl_after/one_source_selftest.py — pins re-pointed, asserts byte-identical

| pin | old | new |
|---|---|---|
| `_contract_md5` | `eae593f220460d880be20da38e3de39d` | **`160f9fe77fd3f99707c48916f3d59e50`** |
| `_curve_source_store` | `f1e8c9fed35462536d00add604f69a3f` | **`37ced3ce45914e6feb00d27e26922e9a`** |
| `_per_entrant_md5` | `999d24c8` | **`b7ed144e`** |

## The LEG F5 seal — `c9e7491b` → `5c38e8ba`

Four sites: `rl_export.py` (assert + message + provenance comment),
`session_2026-07-18/legf5/scripts/gate_f5.py`, `session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py`.
Full record in `SEAL.md`.

## The harness pin (instrument, not repo state)

`harness_pvc_REPINNED_pass3.py`: `EXPECT_V0SURF` `af556bdca53d` → **`3e8e50de5103`** — the declared
refit moved the year-zero surface signature. `EXPECT_STORE` (37ced3ce) and `EXPECT_N` (1197) unmoved,
re-measured not assumed. The assert is byte-identical; only the pinned value moved.

## The OLD-IDENTITY SWEEP

`grep -rIl` over the worktree for `df766dff`, `988135ef`, `d594dc03`, `af556bdc`, `77408ecd`,
`0c798f36`, **excluding `docs/evidence/` and the `session_*` history** (historical evidence is never
rewritten):

| hit | verdict |
|---|---|
| `ui/release_pick_curve.json` `supersedes.pick_curve_curve_md5` / `.pick_curve_file_md5` = df766dff / 988135ef | **CORRECT** — that is the superseded record, written there by this stage |
| `engine/rl_after/pvc_curve_v2.json` `stamp.prev_curve_md5` = df766dff | **CORRECT** — the previous ladder, by the field's meaning |
| `engine/rl_after/pvc_curve_v2.json` `_working_substrate_note` (77408ecd), `derived_from` (af556bdc) | **CORRECT** — prose naming the superseded stage-2 ladder and the matrix's own emit-time surface signature |
| `engine/rl_after/rl_export.py` L660, `one_source_selftest.py` L493/499/500 | **CORRECT** — the re-pin comment chains, which name what each pin superseded. Required by the files' own convention. |
| `data/release_contract.json` `pvc_provenance.curve_payload_md5` = df766dff | **DELIBERATELY NOT MOVED** — see below |
| `ui/data/club_valuation.js` `stamp.pvcCurveMd5` / `pvcCurveFileMd5` | **DELIBERATELY NOT MOVED** — see below |
| `docs/OPEN_ITEMS_REGISTER.md`, `docs/CURRENT_STATE.md` (d594dc03, df766dff, 988135ef) | **NOT TOUCHED** — supervisor-pen documents; this is a build seat |
| `0c798f36` | **zero live hits** |

### The two release-lineage artifacts, and why they stay

`data/release_contract.json` and `ui/data/club_valuation.js` (with its sibling `ui/data/board_view_*.js`)
are **RELEASE-lineage** artifacts: they name the curve and board that are ADOPTED, not the candidate
this branch is building. `data/release_contract.json` is self-sealed by `contract_sha256`, and its
`pvc_provenance` block is the released ruler's identity — moving it would assert an adoption this
branch does not have, and adoption is explicitly the owner's separate click. Stages 1, 2 and ER
likewise left both alone. Recorded here so the omission is a decision, not an oversight.

**Pre-existing, NOT caused by this stage:** `ui/tests/club_curve_provenance.test.py` is red on this
branch (9/35) with `bundle board 113b36f8 != current release board …` — the UI board-view bundle was
last regenerated against the release board `113b36f8` and has not tracked any candidate board since
stage 1. The failure is produced entirely by two files this stage did not modify, and it was red at
`93c2a9a` for the same reason (the message names `expected_boot.board`, which stage ER had already
moved to `f94e0778`).

## Stamping order — Guard 5 halts mid-flight on a stale recomputable pin

1. installed the settled ladder + re-based numéraire into `pvc_curve_v2.json`;
2. `RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 refit_v0surf.py --bake` → wrote `data/v0surf.pkl` and
   **re-pinned `expected_boot.json` `v0surf` itself**;
3. first board build → the LEG F5 seal halt fired (non-vacuity proof), then re-sealed and re-pointed;
4. re-derived the curve `stamp` + `ui/release_pick_curve.json` + the three selftest pins;
5. re-sealed a second time (the curve file md5 is inside the sealed payload) and re-pointed to `5c38e8ba`;
6. `bootstrap.sh` → **Guard 5 PASS**;
7. `rm -f rl_app_data.json && rl_export.py` → PARITY GATE PASS, NUMÉRAIRE GUARD PASS, board `6c9f8d3a`;
8. `s4_matrix_M1v7.py` → BOOK↔BOARD PARITY GATE PASS;
9. `one_source_selftest.py` → PASSED, 143 assertions, 0 FAIL, exit 0;
10. **stamped `board`** `f94e0778` → `6c9f8d3a`; copied the board **and its `.srcmd5` sidecar** verbatim
    from the workspace build output into `data/rl_build/`;
11. re-ran `bootstrap.sh` against the final pins → **Guard 5 PASS** (clean re-entry).
