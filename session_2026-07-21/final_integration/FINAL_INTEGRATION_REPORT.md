# v2.11 Final Integration — Report of Record

**Branch:** `integration/v2.11-final-rc` (also mirrored to `claude/afl-rl-engine-final-integration-468j4t`)
**Base:** `release/v2.11-rc1` @ `f05ebe6df49b653b053f0ebdd82ddc56ee8d4187`
**Status:** provisional final-RC — **no merge, tag, release, deploy, canonical R15–R19 application, or real-store write is authorised or performed.**

---

## 1. Live-state verification (all confirmed live before any change)

| Foundation | Expected | Verified live |
|---|---|---|
| Starting branch | `release/v2.11-rc1` | points to `f05ebe6df49b653b053f0ebdd82ddc56ee8d4187` ✓ |
| Accepted Track B head | `a3d345bae40b18f479fffe91c2738b7ecdef9ccc` | exists = HEAD of PR #128 ✓ |
| Approved Board B diagnostic head | `70ef0ff36ca7633aa4097a9b7c1a730013870abe` | exists = HEAD of PR #131 ✓ |
| PR #127 (RC) | open / unmerged | open, draft, head `f05ebe6` ✓ |
| PR #128 (Track B) | open / unmerged | open, draft, head `a3d345b` ✓ |
| PR #130 (evidence) | open / unmerged | open, draft, head `cca7e72` ✓ |
| PR #131 (Board B evidence) | open / unmerged | open, draft, head `70ef0ff` ✓ |

## 2. Integrated source heads

- **RC foundation:** `f05ebe6df49b653b053f0ebdd82ddc56ee8d4187` (branch base).
- **Track B:** `a3d345bae40b18f479fffe91c2738b7ecdef9ccc` — 3-way merged (merge-base `df5066a`, zero conflicts).
- **Board B (forward lens):** `70ef0ff36ca7633aa4097a9b7c1a730013870abe` — **source only**, read via `git show`, **not transplanted** (PRs #130/#131 remain evidence-only).

## 3. PR non-modification confirmation

PRs **#127, #128, #130, #131 were NOT modified, retargeted, or merged.** Only two branches were pushed:
`integration/v2.11-final-rc` and `claude/afl-rl-engine-final-integration-468j4t` (identical heads). The Track B
merge brings a3d345b's commits *into this branch*; it does not touch the a3d345b branch or PR #128.

## 4. Commit list (first-parent)

```
CP1  release-state identity machinery + complete RL_*/PAR_* static inventory (audit addendum)
CP2  canonical release-state identity move + final board (Board B + visible future-draft ladder)
CP3  UI — visible future-draft asset ladder on the +1/+2 lenses (ring-fenced)
CP4  3-way merge accepted Track B live-scoring updater (a3d345b)
CP4b reconcile Track B into the release-state identity + lineage
CP5  scratch R15-R19 catch-up proof (green) + machine-readable acceptance matrix
```
(Exact SHAs printed by `git log --oneline --first-parent f05ebe6..HEAD`.)

## 5. Final board identity

| Field | Value |
|---|---|
| **MD5** | `039ff8d45a3a47e2f34f183933353bd9` |
| **SHA256** | `3445d0ffe1732e6c3af8399d16d946c9457f76a183273a8a937af0c2be835e70` |
| **Git blob** | `80eb536bc8dc9dcb64e037ad912a2b7219cb0769` |
| **expected_boot `board`** | `039ff8d45a3a…` (pinned) |
| **`balanced_board_md5` (present-lens lineage)** | `06d8af60b679…` (preserved, **not** the final file hash) |
| **`config` (config_sha256)** | `3a1e714f2fa0…` (was `c2d233ae…`; 14 class-A switches now stamped) |
| **`store`** | `968de0c7…` (unchanged) |
| Sidecar `rl_app_data.json.srcmd5` `own_md5` | `039ff8d4…` |

The final board = accepted forward-lens **Board B** (`1f10220c`, `RL_LEGE=1 RL_LEGF=1 RL_PVC2=1`) + the owner-facing
visible future-draft asset ladder. Recipe: `tools/build_final_board.py` (reads Board B from `70ef0ff` via `git show`,
verifies md5 `1f10220c`, adds the ladder, writes `sort_keys=True` — byte-deterministic).

## 6. Canonical switch-manifest closure + audit addendum

`data/model_config.json` now pins **all class-A live semantics**, including the owner-approved posture
`RL_PVC2=1 RL_LEGE=1 RL_LEGF=1` and the 11 further board-affecting kill-switches that previously resolved from
code defaults (`RL_FLEX RL_CAPT RL_DAMP RL_EVW RL_ISOFADE RL_SAGE29 RL_LSYM RL_EO2 RL_ABSENCE RL_UNCOMP RL_UNCONSERVE`).
Override hooks `RL_UNCOMP_S / RL_LSYM_TAB / RL_V0SURF_REFIT` are declared **must-be-unset** (reject-if-set).
`RL_DAMP_K / RL_ABS_LREF / RL_ABS_CAP` are class-C (retired to pinned literals; no live read).

- **`release_contract.py` + `data/release_contract.json`** — the authoritative jointly-stamped release-state
  identity: config + board/balanced/store/engine/rl_model/fv/register/band identities + switch posture + PVC
  provenance + must-be-unset hooks, with self-hash `contract_sha256`. Fail-closed on missing / stale /
  contradictory / ambient-only / unknown state. `require_canonical()` halts a release build with `RL_CONFIG_MODE`
  unset (no ambient-only / diagnostic-only board).
- **`config_inventory.py`** — complete static inventory of every `RL_*/PAR_*` read on the canonical + release +
  Track B surfaces (153 reads, 84 vars, **0 unclassified**), classified A/B/C, machine-readable evidence.

## 7. Acceptance matrix (machine-readable: `evidence/acceptance_matrix.json`)

| # | Requirement | Result |
|---|---|---|
| 07 | Canonical manifest posture `RL_PVC2=1 RL_LEGE=1 RL_LEGF=1` | **PASS** |
| 08 | Fail-closed tests (missing/ambient-only/contradictory/unknown/stale/missing-contract/conflicting-PVC) | **PASS** 15/15 |
| 09 | Final board identity (md5/sha256/blob/sidecar/config) | **PASS** |
| 10 | Present-lens invariants: 804 active; Σv=752427; 0 present-v/rank/order movers vs Board A | **PASS** |
| 11 | Forward-vector invariants: vP1 & vP2 == Board B for all 804 (equal 804/804, changed 0, missing/added 0) | **PASS** |
| 12 | Visible draft assets: 64 (2027) + 64 (2028), 0 on current ladder, unique ids, PVC equality, monotone, sorted | **PASS** 32/32 + UI 26/26 |
| 13 | F5 reconciliation: 64617 + 4649 + 14272 = **83538** per lens; no double-count vs sealed phantomTotals | **PASS** |
| 14 | Club valuation: PVC fail-closed (RL_PVC2, curve_md5 89c14729), 160 held picks, 16 clubs | **PASS** 26/26 |
| 15 | UI: current player-only, +1/+2 asset views, desktop+mobile, no overflow, empty Movers | **PASS** 26/26 + responsive 72/72 |
| 16 | Track B: fast unit + preflight + movers; atomic/exactly-once/finalization/conflict/repair/lineage/gate-off | **PASS** (47 movers) |
| 17 | Scratch R15-R19: 5 rounds, exactly-once, histories→R19, repair byte-deterministic, **no canonical file moved** | **PASS** (ALL_PASS) |

## 8. F5 reconciliation (exact, per lens)

```
visible national-draft picks 1-64  =  Σ PVC[1..64]              =  64,617
residual — national-draft deep tail (chained RD/PSD 65-82 + partial occupancy) = draft_pvc 69,266 − 64,617 = 4,649
residual — non-national-draft entry (MSD 5946 + SSP/PDN/PDA/IRE/UNR 8,326)     = mech_pvc                = 14,272
--------------------------------------------------------------------------------------------------------
visible + residual = 64,617 + 4,649 + 14,272 = 83,538  ==  sealed F5 entrant layer (seal a17aafed)
```
No double count: `draftAssets` is a face-value re-presentation of the same F5 draft; `phantomPicks` (occupancy) and
`draftAssets` are never summed; club-held real picks (`club_valuation`, 160) are a separate owned-asset namespace.

## 9. Track B protections preserved (settled architecture, unchanged)

Atomic store update; exactly-once; staging+validation before atomic swap; rollback on mid-apply failure; committed
txn manifests (round score map + board/store ids); journalled post-commit finalization with FINALIZED written last;
crash-gap recovery (before finalization / after derivatives-before-validation / after validation-before-FINALIZED);
same-round conflict refusal + byte-preservation; corrupt-non-conflicting repair; historical repair on the frozen
identity (latest board not moved back); full release-lineage fail-closed checks; **Movers honestly empty**; **real-store
write gate OFF** (`APPLY_DEFAULT=False` + dual `INGEST_SCORE_APPLY`/`_ARMED`).

## 10. Rounds 15–19 boundary

The final integration branch stays at the **clean round-14 release boundary**. Genuine R15–R19 inputs were used only
in **disposable scratch copies** to prove the integrated updater performs the complete catch-up
(`session_2026-07-20/live_scoring_catchup/proof.json` ALL_PASS; `F_no_production_touched: changed=[]`). Canonical
store `968de0c7` and canonical board `039ff8d4` are unchanged. No canonical score, ledger, history, or as-of-round
was advanced.

## 11. Environment / reproduction

Engine runs deterministically here: pinned `numpy 2.4.4` + bundled OpenBLAS `05c9f9eb` (byte-exact to the env-pin);
`bootstrap.sh` Guard 5 PASS (store/rl_model/fv/register all == pins); `rl_export.py` under `RL_CONFIG_MODE=bake`
loads the new manifest ("CONFIG ACCEPTED 3a1e714f, 61 model vars pinned, ambient cleared") and FV provenance matches.

## 12. Limitations (clearly classified)

- **Visible-ladder engine reproduction (go-live wiring, deferred):** the 64-pick owner-facing ladder + residual
  aggregates (`draftAssets` / 64-row `lensPicks`) are a **deterministic post-processing presentation layer** over
  the accepted Board B, applied by `tools/build_final_board.py`. The engine's `rl_export.py` produces Board B's
  native 30-pick lens ladder + the F5 phantom layer; no gate rebuilds-and-compares (boot_guard authenticates the
  installed board `039ff8d4` by file hash, and F1/F2 parity checks only `active[].v`), so all guards/CI are green.
  At the **deferred** R15–R19 go-live, the weekly updater's board-regen should re-apply `build_final_board.py`'s
  presentation step — a documented wiring point, out of scope for this integration (R15–R19 is not applied here).
- **CI on the pinned runner:** `.github/workflows/{ci-guards,fv-provenance,live-scoring}.yml` re-run on the PR;
  locally the gates were verified (config acceptance, Guard 5, fast suites, both scratch proofs).
