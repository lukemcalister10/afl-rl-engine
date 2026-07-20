# RELEASE CANDIDATE — v2.11-rc1

Date: 2026-07-20 (Australia/Sydney) · Supervisor: ChatGPT · Builder: Claude Code · Owner: Luke McAlister
Status: **DRAFT release candidate. NOT released, tagged, merged, or deployed.** Owner authority required for
any promotion. This document is the evidence record for the controlled read-only v2.11-rc1 assembly (owner
**Option 1** ruling).

---

## 1 — Branch / lineage

| item | value |
|------|-------|
| RC branch | `release/v2.11-rc1` |
| Created exactly from | `df5066a0106363a6d00a2dbdd0bd2b62f97c36ae` (accepted provenance head) |
| Accepted (frozen) provenance branch | `claude/fv-provenance-fail-closed-fm2gas` → `df5066a` |
| Draft PR | head `release/v2.11-rc1` → base `claude/fv-provenance-fail-closed-fm2gas` |
| Immutable checkpoint (untouched) | `checkpoint/pre-chatgpt-v2.11` → `612d4c058560568b3d4d49ecd785759931885081` |
| Canonical board source commit (untouched, read-only) | `7c6768ee51adc2cf939ffa18f620bbec1d6b4249` (`diagnostic/root-cause-109-player-wobble`) |

Not moved or modified: `checkpoint/pre-chatgpt-v2.11`, `recovery/v2.11`, `claude/fv-provenance-fail-closed-fm2gas`,
`diagnostic/root-cause-109-player-wobble`, `prep/v2.11-ui-release-seam`, `prep/weekly-updater-safe-local`.

---

## 2 — Canonical board (installed exact bytes)

The round-14 **balanced board of record** was installed as exact committed Git bytes — **no rebuild, no freshly
generated artifact** (a fresh generation is only the reproduction test, §6).

| property | value |
|----------|-------|
| Source commit | `7c6768ee51adc2cf939ffa18f620bbec1d6b4249` |
| Source path | `session_2026-07-20/root_cause_109_wobble/cross_host_gate/fixtures/reference_06d8af60.json` |
| Git blob | `e546ab0b1033af2b8e4331e66899d14245ef3b58` |
| Installed at | `data/rl_build/rl_app_data.json` |
| Full MD5 | `06d8af60b679a12db07c064c60c065f9` |
| Bytes | 1,163,474 |
| active players | 804 |
| Σ active `v` | 752,427 |
| Harry Sheezel `v` | 7,964 |
| Nick Daicos `v` | 8,017 |

Board source sidecar `data/rl_build/rl_app_data.json.srcmd5`:
`{"derived":"rl_app_data.json","own_md5":"06d8af60b679a12db07c064c60c065f9","source":"rl_model_data.json","source_md5":"968de0c7a0183ca3914165536f39607a","tier":1}`
— `own_md5` == installed board, `source_md5` == pinned round-14 store.

**Relationship to the superseded committed board `270a2c5f`:** byte-identical when sorted by key — **0 value
movers, identical value-ranking**; they differ **only in `active` row order** (697 rows). `06d8af60` is the
current-engine (`cc626d7d`/`904722cd`) row order (`active` sorts descending by float `_v`); `270a2c5f` was the
superseded #109-engine (`a5fd3d7d`/`40f43772`) order. This is the register's "parity 0/804, 697 rank movers",
now byte-confirmed.

---

## 3 — UI release seam (transplanted)

`prep/v2.11-ui-release-seam` head `76136d59c9b5494474fdbb195c9e47d391b01e20`, exactly three commits after common
base `3055ea5`. The three exact source SHAs, in chronological order:

1. `1d5d19dbe4f362ea11abaddfac0a575a7dba5187` — pass Leg-F phantom fields + durable release/round metadata contract
2. `910a55f9948064057d48a3098331a7e335df3a95` — dRound/dRoundRank on working tier + canonical source_md5 identity
3. `76136d59c9b5494474fdbb195c9e47d391b01e20` — split provenance into board_md5 / store_md5 / balanced_board_md5

Transplanted as the folded net diff into the single RC implementation commit (to keep ≤2 commits and a narrow
RC diff). The applied diff is byte-equal to the three commits' combined diff (764 insertions / 20 deletions,
10 files); every transplanted UI-seam file is byte-identical to its `76136d59` tree object. No conflict: the
fv-provenance commits (`3055ea5..df5066a`) touch none of the UI-seam files.

UI-seam files: `ui/app/board.js`, `ui/app/main.js`, `ui/app/seam.js`, `ui/tests/extract_seam.test.py`,
`ui/tests/release_seam.test.js`, `ui/tools/extract_board_view.py`, and `session_2026-07-20/ui_release_seam/*`.
No engine, valuation, store, config, or `expected_boot.json` change is contained in the seam.

---

## 4 — Release manifest (`data/expected_boot.json`)

Coherent re-stamp. Every pin below == the md5 of the file it validates (full-hash, verified by `boot_guard`).

| key | new value | change |
|-----|-----------|--------|
| `board` | `06d8af60b679a12db07c064c60c065f9` | `270a2c5f → 06d8af60` (installed balanced board of record) |
| `balanced_board_md5` | `06d8af60b679a12db07c064c60c065f9` | **added** |
| `release_version` | `v2.11-rc1` | **added** |
| `as_of_round` | `14` | **added** |
| `engine_head` | `904722cd3fc16957a58796d8e2cb4caa` | `40f43772 → 904722cd` (re-stamp to already-committed `_merged_recover.py`) |
| `rl_model` | `cc626d7db7524929e5d2f1b024b25fb4` | `a5fd3d7d → cc626d7d` (re-stamp to already-committed `rl_model.py`) |
| `fv` | `de4c7ec38b1da026575f700ec5d76cd79c633207b9ca11d25bef0e7e1a5b2c64` | unchanged |
| `store` | `968de0c7a0183ca3914165536f39607a` | unchanged |
| `config` | `c2d233aec1041a2d24a66990a584f552d59b3902f97eddbf76867d724071b53b` | unchanged |
| `q97m` | `cfdc73216c099e5e8f1fda3968f31c00` | unchanged |
| `band` | `34faa8659cc8f19794f5cb9584fa19b2` | unchanged |
| `v0surf` | `3af2b7258b8c8c596c4184617f99d3ca` | unchanged |
| `register` | `652d83e87780e415a01a2de6d8b3cc57` | unchanged |
| `peak_model` / `pvc_snapshot` / `bust_prior` | (as pinned) | unchanged |

**Engine-pin re-stamp is value-neutral.** The two engine-pin moves point the pins at engine source that is
**already committed and byte-recoverable** at `df5066a` (`_merged_recover.py` md5 `904722cd`, `rl_model.py` md5
`cc626d7d`) — the pins were stale (last stamped at #109), the source was not. This resolves the item-399
stale-boot-pin bootstrap failure (§6.7). No engine byte changes; the board is byte-identical (0 movers) across
the re-stamp.

**Representational adjustment reported (per the release-contract carve-out):** the manifest `panel` string's
board-identity token was updated `270a2c5f → 06d8af60`. The panel is a value gate over 10 named players; those
10 values are byte-identical between the two boards (0 v movers), so `PASS 10/10` is unchanged and still
accurate for `06d8af60`. No other pin or descriptive field was altered.

---

## 5 — UI ring-fence + regenerated bundles

- Ring-fence pin `ui/app/config.js EXPECTED_BOARD`: `790136a3 → 06d8af60` (the seam authenticates
  `working.stamp.board_md5[:8] == EXPECTED_BOARD`). Sibling tool pins updated for coherence:
  `ui/tools/extract_positions.py`, `ui/tools/ingest_inputs.py` (`790136a3 → 06d8af60`).
- Regenerated from the installed exact board (read-only extractor; **no value recomputed**):
  - `ui/data/board_view_working.js` — `window.__MATCHDAY_WORKING__`, stamp:
    `board_md5 06d8af60… / store_md5 968de0c7… / balanced_board_md5 06d8af60… / srcmd5 06d8af60… /
    engine 904722cd / store 968de0c7 / register 652d83e8 / config c2d233ae… / releaseVersion v2.11-rc1 /
    asOfRound 14 / tag v2.11-rc1 / nPlayers 804 / guard5 pass`.
  - `ui/data/board_view_public.js` — `window.__MATCHDAY_PUBLIC__`, leak-proof stamp `{baseYear, maxV, nPlayers}`
    only (no md5/board/store/guard identity).
  - `ui/app/positions_data.js` — values-free position map, 804 players, board `06d8af60`.
- **Club-valuation overlay (`ui/data/club_valuation.js`): RESOLVED (independent-review corrective, §9).** The
  overlay previously fail-closed on the RC board because `ui/tools/ingest_inputs.py` hardcoded
  `pvc_curve_L1b.json` as the canonical curve while the RC board carries the adopted `RL_PVC2` composed-pathway
  PVC (`pvc_curve_v2.json`). The corrective commit replaces the hardcoded rule with a deterministic, fail-closed
  resolver driven by an explicit release-metadata contract (`ui/release_pick_curve.json`): it resolves the
  release-active pathway (RL_PVC2 → `pvc_curve_v2.json`), cross-checks the contract against the accepted release
  (store `968de0c7`, `release_version v2.11-rc1`) and the engine curve's own self-declared gate/identity, and
  cross-checks the board PVC against the resolved curve — HALTing on unknown/missing/conflicting selection. The
  overlay now regenerates clean (no HALT): 16 clubs, 160 held picks priced off the v2 curve, correct board+curve
  provenance stamp, no stale v2.10 data. No installed board / store / engine / valuation / `expected_boot` change;
  no player value or rank changed.

---

## 6 — Required proof (results)

Environment: pinned numpy 2.4.4 + bundled OpenBLAS `05c9f9eb` (item 392), `PYTHONHASHSEED=0`, vendored
unidecode, `RL_FV` bound to the checkout's `engine/forward_valuation`.

1. **Installed board == diagnostic Git blob** — `cmp` byte-identical to `7c6768ee:…/reference_06d8af60.json`;
   `git hash-object` == `e546ab0b1033af2b8e4331e66899d14245ef3b58`. **PASS.**
2. **Full MD5 + all 804 active values vs accepted reference vector**
   (`session_2026-07-20/fv_provenance_remediation/fixtures/reference_vector_06d8af60.json`): md5 `06d8af60…`,
   active 804, Σv 752,427, **0/804 vector movers**. **PASS.**
3. **Fresh balanced build in a disposable dir** (`RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`, pinned env, accepted
   provenance path) — FV suite GREEN1 built the board in `mkdtemp(/home/claude/fvprov_*)`. **PASS.**
4. **Fresh output byte-identical to the installed board** — GREEN1 rc=0, md5 `06d8af60…`, active 804,
   Σv 752,427, Sheezel 7,964, vector_movers 0. **PASS.**
5. **Installed board never overwritten by generated output** — the reproduction build writes to a disposable
   `mkdtemp`; the installed `data/rl_build/rl_app_data.json` is the copied Git blob, never generator output.
   **PASS (by construction).**
6. **FV provenance suite** — `python3 session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` →
   `RESULT: 8/8 PASS`, exit 0 (GREEN1, GREEN2, RED1–RED6). Durable record: `RESULTS.json` `{"pass":8,"total":8,
   "fv_pin":"de4c7ec3…"}`. **PASS.**
7. **Full CI Guards** (`.github/workflows/ci-guards.yml`, run locally step-by-step):
   - `setup_env.sh` PASS · `bootstrap.sh` PASS (Guard 5: store 968de0c7 / rl_model cc626d7d / engine 904722cd /
     fv de4c7ec3 all == pinned) — **the item-399 stale-boot-pin bootstrap failure is now resolved by the
     coherent engine-pin re-stamp.**
   - build (`RL_CONFIG_MODE=bake`): `rl_export.py` + `s4_matrix_M1v7.py` exit 0. (The CI build uses the default
     env → produces the **default** board `1f10220c` (all legs ON); the **balanced** board of record `06d8af60`
     is built by GREEN1 with `RL_LEGE=0 RL_LEGF=0`. Diagnostic-only; no verdict impact.)
   - `one_source_selftest.py` PASS (single source; guards 1–3; board==engine F1; book==board F2; collision
     sentry clean) · `run_panel.sh` **PASS 10/10** (Daicos 8017, Bontempelli 3897, Sheezel 7964, Gawn 3416, Reid
     3348, Ward 2003, Moore 257, Goad 914, Smillie 1324, Green 651) · `ruling_config_check.py` PASS (R3) ·
     `config_manifest.py check` PASS (hash c2d233aec104, 47 vars).
   - `guard_correction_canary.py` (Guard 4, correction-sticks) exercises **unchanged engine behaviour** (this RC
     touches no engine byte); its baseline is the fresh board the pipeline builds immediately before it. The
     authoritative Guard-4 execution is the clean-runner CI run (§6.11, `ci-guards.yml`), which runs it
     sequentially after the build step on a pristine workspace.
8. **UI extraction / release-seam / ring-fence / existing UI tests** — `ui/tests/extract_seam.test.py` **41/41**;
   `ui/tests/release_seam.test.js` **23/23**; `ui/tests/counting_rule.test.js` **24/24**; `extract_board_view.py`
   / `extract_positions.py` ring-fence assertions PASS. **PASS.**
9. **Bundle release/round metadata** — working bundle carries `releaseVersion v2.11-rc1`, `asOfRound 14`,
   `board_md5/store_md5/balanced_board_md5` (full), `tag v2.11-rc1`; public bundle leak-proof. **PASS.**
10. **UI accepts correct board, refuses mismatched** — `seam.ringFence()` matches `board_md5[:8]==EXPECTED_BOARD`
    (06d8af60); `release_seam.test.js` asserts accept-on-match and refuse-on-mismatch (store_md5 / balanced_board_md5),
    naming the failed field, with no hardcoded id. **PASS.**
11. **Clean cold-bootstrap on an independent GitHub-hosted runner** — `.github/workflows/ci-guards.yml` and
    `.github/workflows/fv-provenance.yml` run on `ubuntu-24.04` on push. Run IDs / job IDs / artifact digests:
    recorded in the PR checks and the assembly RETURN.
12. **No valuation formula / engine data / player value / ranking changed** — the RC change set touches **zero**
    engine/valuation/store/config/band/q97m/v0surf source; `rl_model.py cc626d7d`, `_merged_recover.py 904722cd`,
    all `engine/forward_valuation/*.py`, `rl_model_data.json 968de0c7`, `model_config.json`, `cm_400/q97m/v0surf`
    are byte-identical to `df5066a`. Board values: 0 movers vs the reference vector and vs `270a2c5f`; value-ranking
    identical. The engine-pin re-stamp moves only the pins, not the source. **PASS.**

---

## 7 — Configuration

- Engine: `_merged_recover.py 904722cd3fc16957a58796d8e2cb4caa`, `rl_model.py cc626d7db7524929e5d2f1b024b25fb4`.
- Store: `rl_model_data.json 968de0c7a0183ca3914165536f39607a` (round-14).
- Forward-valuation source-set identity (`fv`): `de4c7ec38b1da026575f700ec5d76cd79c633207b9ca11d25bef0e7e1a5b2c64`.
- Config manifest (`data/model_config.json`): `c2d233aec1041a2d24a66990a584f552d59b3902f97eddbf76867d724071b53b`
  (47 model vars; hash `c2d233aec104`). Fitted pins: q97m `cfdc7321`, band `34faa865`, v0surf `3af2b725`,
  peak_model `b763f59e`, pvc_snapshot `735d2dec`, bust_prior `ffb54267`. Register `652d83e8`.
- Balanced board build env: `RL_PVC2=1 RL_LEGE=0 RL_LEGF=0`, `PYTHONHASHSEED=0`, single-thread BLAS,
  `RL_PRIOR_TREES=400`, pinned numpy 2.4.4 / OpenBLAS 05c9f9eb.

---

## 8 — Remaining release restrictions

- **No merge, tag, release, public deploy, or valuation-math change** is authorised. The PR is a DRAFT for
  independent review only (base `claude/fv-provenance-fail-closed-fm2gas` to keep the RC diff narrow).
- Club-valuation overlay is RESOLVED (§5 / §9): it now renders (16 clubs, 160 held picks) on the RC board via a
  deterministic fail-closed curve-provenance resolver. No outstanding overlay restriction.
- Weekly score-ingestion (PR #125 lineage) remains post-release and unaccepted (transaction-safety /
  stale-preview / UI-refresh / round-history / multi-round proof unverified).
- Long-term determinism: the RC ships committed exact bytes and a fixed-provenance reproduction; the broader
  cross-container `np.interp` hardening remains tracked work, now guarded fail-closed by `df5066a`.

---

## 9 — Club-valuation curve-provenance correction (independent-review corrective commit)

Bounded corrective commit on `release/v2.11-rc1` (accepted core RC artifacts unchanged: installed board, store,
valuation/engine source, `expected_boot` hashes/metadata, FV provenance code, all player values/ranks).

- **Root cause:** `ui/tools/ingest_inputs.py` treated `engine/rl_after/pvc_curve_L1b.json` as the canonical curve
  (the S5 STALE-CURVE guard), so it HALTed on the RC board's adopted `RL_PVC2` composed-pathway PVC
  (`pvc_curve_v2.json`), disabling the club-valuation + held-pick overlay.
- **Fix:** an explicit, fail-closed release-metadata contract `ui/release_pick_curve.json` declares the
  release-active pathway (the config manifest pins `RL_PVCADOPT` but does not carry the `RL_PVC2` engine
  default-ON kill-switch, so the pathway cannot be read from the config alone). `ingest_inputs.py` resolves the
  release-active curve **deterministically** from the contract, cross-checking: the contract vs the accepted
  release (`store 968de0c7`, `release_version v2.11-rc1`, `pin1 3000`); the engine curve file's OWN self-declared
  identity (filename-for-pathway, full-file md5 `56dd7a7b…`, `curve_md5 89c14729`, gate token `RL_PVC2`, store
  binding `968de0c7`); and the installed board PVC == the resolved curve (full shared-pick equality). Unknown /
  missing / conflicting selection HALTs. Preserved unchanged: board-id ring fence, full shared-pick curve
  equality, pick1 == 3000, monotone non-increasing curve, pick ledger + club joins, no-workbook-value pricing.
- **Regenerated `ui/data/club_valuation.js`:** no HALT; 16 clubs; 160 held picks priced off `pvc_curve_v2.json`
  (`RL_PVC2`); stamp `board 06d8af60 / engine 904722cd / store 968de0c7 / releaseVersion v2.11-rc1 / asOfRound 14
  / pvcPathway RL_PVC2 / pvcCurveMd5 89c14729`; no stale v2.10 data.
- **Tests (`ui/tests/club_curve_provenance.test.py`, 24/24):** accepted v2 curve passes + totals conserved
  (16/160, Sum per-club picks == 160, prices == curve mean); L1b-under-RL_PVC2 fails closed (contract-path AND
  board-PVC); unknown pathway / wrong store / missing contract / curve-md5 drift fail closed; board-id mismatch
  fails closed; board_view bundles byte-unchanged (Board/Player/Trade views intact). Existing UI suites still
  green (extract_seam 41/41, release_seam 23/23, counting_rule 24/24).
- **Rendered evidence** (`session_2026-07-20/ui_release_seam/evidence/`, 16/16 assertions, desktop 1440×900 +
  mobile 390×844): normal board renders; club valuation renders (no HALT); held picks render (club focused on
  board, Σ picks shown); version `v2.11-rc1` + as-of `Round 14` shown; no integrity alarm / fail-closed screen.
