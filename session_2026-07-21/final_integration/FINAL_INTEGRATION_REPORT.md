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
| 11 | Forward-vector invariants: vP1 & vP2 present + numeric for all 804 + Board B key universe matches (structure gated). Semantic vP1/vP2 equality to the superseded R14 Board B is owner-DEFERRED — deltas MEASURED, never asserted as a pass (no accepted R19 forward oracle) | **DEFERRED** |
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

---

## 13. SUPERVISOR CORRECTIONS (2026-07-21, PR #132 review)

Final board identity moved `039ff8d4` → **`2ab73a6fed1f06fc8eecc2ce597c2aec`** (SHA256
`0026c3f82e6bb555…`). `config` `3a1e714f` and `store` `968de0c7` unchanged. `balanced_board_md5` `06d8af60`
preserved as present-lens lineage.

**S1 — Canonical reproducibility (no diagnostic build input).** The final board is now produced by the
CANONICAL ENGINE BUILD: `rl_export.py` (RL_LEGF=1 block) emits the visible future-draft ladder + F5
reconciliation directly. `build_final_board.py` is repurposed into the clean-room reproduction driver.
Clean-room proof `cleanroom_repro.json` gates on the ACCEPTED properties only (ITEM 408 present-oracle
migration 2026-07-24): bootstrap re-sync from checkout → canonical engine build → rebuilt board
BYTE-IDENTICAL to the committed board of record `6f07f7cb` → working/public bundles byte-identical
(`ok_rebuild`); present `v` gated against the committed accepted reference vector `reference_vector_1373e824`
(active 804, Σv 760253, exact key-set + per-row `v` — `ok_present`, NOT derived from the rebuilt board and
NOT Board B); vP1/vP2 present + numeric for all 804 and the Board B key universe matches
(`ok_forward_structure`). The Board B (`70ef0ff`) vP1/vP2 SEMANTIC comparison is owner-DEFERRED (no accepted
R19 forward oracle): the deltas are MEASURED and recorded, never asserted as a pass and never used to fail
the tool. No `git show` of a diagnostic, no other branch/commit, is a build input.

**S2 — Season-progress authority.** Investigated + classified + tested (`season_progress_inventory.json`,
`season_progress_test.py` **11/11**). Finding: valuation season progress is the FROZEN literal
`SEASON_PROG=0.58` (`rl_model.py:778`, pinned via rl_model + board md5), DECOUPLED from the dynamic
`as_of_round=14` (stamped, weekly, feeds no valuation). `RL_SEASON_ROUNDS`/`DEFAULT_SEASON_ROUNDS=24` is the
ingestion round-bound SANITY guard only — class B, inert for valuation. Controlled R14-vs-R24 test (7-games
player): grossed-up games 12.07→7.0, benefit-of-doubt 0.584→0.50, year-0 blend 83.2→100.0. `release_contract`
binds `season_metadata` with a fail-closed coherence check. Re-deriving the fraction from
as_of_round/season_total would move approved vectors — DEFERRED, owner-authorized, not this task.

**S3 — No row caps.** `board.js` renders EVERY row: removed the top-60 truncation, grouped-club top-6, and
the "+N more" counts. Current ladder = all 804 players; grouped mode = every player for every club; footer
reports the true rendered count.

**S4 — Unified +1/+2 ranking.** The future lenses are ONE combined value-descending ranking of **868**
assets (804 players at vP1/vP2 + 64 anonymous national-draft placeholders at PVC), picks interleaved with
players by value, global ranks 1..868, pick number shown separately from rank. Player-only filters
(position/club) remove the anonymous picks while active; clearing restores 868. UI check **40/40**: 868
rows, 64 picks, interleaved, last player + last pick in DOM, no overflow at 390/1440.

**S5 — F5 residuals + R15 survival.** The two residual aggregates are held OUT of the ranking in a separate
reconciliation panel (visible ΣPVC[1..64] 64617 + ND deep-tail 4649 + non-ND mech 14272 = sealed 83538).
Disposable R15 regeneration `r15_ladder_survival.json` **12/12**: the updater board-regen reproduces the
ladder + exact F5 reconciliation automatically (no manual post-processing); canonical store/board unchanged;
gate OFF.

Acceptance matrix `acceptance_matrix.json`: **OVERALL PASS**, all items + S1–S5 green.

---

## 14. SUPERVISOR 2nd REVIEW — WEEKLY SEASON-STATE CORRECTION (2026-07-21)

The weekly updater no longer leaves valuation season-state frozen at Round 14. TWO distinct dynamic
concepts, both DERIVED, never conflated (`season_state.py` + `data/season_state.json`, single source):

1. **Calendar season progress** = `round_half_up(100·as_of_round/season_total_rounds)/100`.
   R14=**0.58**, R15=0.63, R16=0.67, R17=0.71, R18=0.75, R19=0.79, final=1.00. Replaces the frozen
   `SEASON_PROG` literal + `RL_M3_FE`; used everywhere those were read.
2. **Empirical exposure pace** (NOT calendar) = `round(median(current games of durable pop prior_games≥18)/22, 3)`,
   cap 1.0. R14 = **0.545** (305 durable, median 12, 12/22). Per-player scope `s=clip(1−g/11,0,1)`; ≥11
   current games untouched (s=0). Freshly derived from the staged store each round. Replaces `RL_EXPO_F`.

**R14 byte-identity PROVEN:** the canonical engine build under the rerouted engine reproduces board
`2ab73a6fed1f06fc8eecc2ce597c2aec` EXACTLY (derived == prior frozen values at R14). Only source identities
moved: rl_model `cc626d7d→c3a243ee`, engine_head `904722cd→feff9471`, fv `de4c7ec3→97abe963` (re-pinned).
`RL_M3_FE`+`RL_EXPO_F` removed from the manifest (config `3a1e714f→45b207c0`, 59 vars); immutable
derivation policy stamped `season_state_policy_id`.

**Updater derives + commits atomically:** the staged transaction derives the season-state from the staged
store after applying scores, before the board regen, and commits `data/season_state.json` in the atomic
TARGETS (with store/board/sidecar/manifest/ledger/histories) — a crash cannot leave a new round on stale
season-state.

**Contract verifies DERIVATION** (not equality): calendar == its formula; season_state internally
consistent + not stale (round/calendar/policy/season_year); exposure derived from the LIVE store
(`source_store_md5` == live store, else stale-exposure HALT).

**Evidence:** `season_progress_test.py` **20/20** (derivation, wiring, behaviour: 6-game s=0.4545 less
influence, ≥11-game untouched, direction-symmetric, calendar≠exposure, completed seasons byte-inert, stale
rejection); `season_advance_r14_r19.json` (R14 byte-identical + R15–R19 calendar advances + exposure freshly
derived + 804+64+64 survive + F5 exact + canonical untouched + gate OFF); `.github/workflows/final-integration.yml`
runs all generating tests on the pinned runner.

**Note:** the report's §5 board identity `039ff8d4` was superseded by the engine-native `2ab73a6f` (§13) and
carried unchanged through the season-state wiring (§14). Board of record = **`2ab73a6fed1f06fc8eecc2ce597c2aec`**.

---

## 15. SUPERVISOR 3rd REVIEW — FENCED READS, FAIL-CLOSED VERIFY, COHERENT WEEKLY AUTHORITY (2026-07-21)

Eight substantive corrections. R14 board stays **byte-identical `2ab73a6fed1f06fc8eecc2ce597c2aec`**; no
canonical R15–R19 scores applied; no real-store write; write gate stays OFF.

**1 — Fenced season-state reads HALT (never fall back).** Under `RL_CONFIG_MODE` in `bake|gate|canonical`
the engine readers (`rl_model`/`_merged_recover`/`conditional_prior` `_season_val`; `season_state`
`read_value`/`calendar_progress_value`/`exposure_pace_value`) now RAISE on missing / malformed / missing-key /
non-numeric / non-finite `season_state.json` or an unresolved-untrusted repo root; only an explicit UNFENCED
dev shell keeps the fallback. `rl_export.py` gives `canonical` the same fail-closed config/FV enforcement as
bake/gate (it was falling into the unfenced branch). Proof `season_state_fenced_test.py` **94/94** — every
fenced mode × corruption HALTs, unfenced falls back, and a gate build against a corrupt `season_state.json`
exits non-zero and writes **no board** (rejection before any board is written).

**2 — release_contract.verify is FAIL-CLOSED.** Removed every `except Exception: pass` around the
authoritative season-state checks; any error loading/parsing/verifying `season_state.py`, `season_state.json`,
the source store, the calendar/exposure derivation, or the policy/store/round/season identity is now an
explicit rejection stating the real cause. A fenced contract with no `season_metadata` is rejected.
`release_state_failclosed_test.py` **23/23** (8 new season red-paths).

**3 & 5 — One coherent weekly authority.** Investigation confirmed the flagged incoherence: `_restamp_manifest`
(`round_apply.py`) moved only `store`+`board` (`expected_boot.as_of_round` frozen at 14), and
`release_contract.json` had **no runtime writer** and was **not** a transaction target. Fix: `_restamp_manifest`
now also advances `expected_boot.as_of_round`; new `release_contract.restamp_dynamic` re-stamps the contract's
`as_of_round` + `identities.store/board` + `season_metadata` + `contract_sha256` from the staged
manifest/board/season-state; `release_contract.json` is now an atomic **TARGET**; staged phase (c2) re-stamps
it after the board exists; `_validate_staged` (vii-c) rejects a stale round on season_state/expected_boot/
contract, a stale contract pin, exposure off a stale store, and runs the fail-closed contract verify — all
before commit. `data/release_lineage.json` (immutable present-lens baseline) is deliberately NOT a target.

**Writers of the five artifacts (authoritative):** `expected_boot.json` — `_restamp_manifest` (store+board+
`as_of_round`), INSIDE the atomic txn. `season_state.json` — staged phase (a2) `derive`, INSIDE the txn.
`release_contract.json` — staged phase (c2) `restamp_dynamic`, INSIDE the txn (**new**). `release_lineage.json`
— **no runtime writer** (immutable). UI `stamp.release` — `round_movers.inject_release_contract` at finalize
(Tier-3, derivative), reads the advanced authority; not a substitute for repository state.

**4 — Superseded contract text removed.** `release_contract.json` `season_metadata` no longer states
"frozen literal SEASON_PROG", "DECOUPLED", "never re-bakes", or "DEFERRED"; replaced with the derived/coupled
truth; contract re-stamped. Historical lineage stays in this report, not in hashed authority.

**6 — Extended R14–R19 evidence** (`season_advance_r14_r19.json`): per round now records + verifies
`as_of_round`, calendar, durable count, median games, exposure, season-state source-store md5, store md5,
board md5, **expected_boot as_of_round/store/board, release-contract as_of_round/store/board, contract_sha256,
release-contract verification result**, derivation-policy id, active count, picks-by-lens, F5, **write-gate
status**. Required results hold: R14 `2ab73a6f`, calendar 0.58/exposure 0.545; R15–R19 calendar
0.63/0.67/0.71/0.75/0.79 with freshly-derived exposure; 804 + 64+64 survive; F5 83,538; canonical R14 files
untouched; gate OFF; and at every round season_state == expected_boot == release_contract on the SAME round.

**7 — Rollback / crash recovery cover the dynamic authority.** `failure_injection_proof.py` byte-state now
includes `season_state.json` + `release_contract.json`; a new injection point `during_contract_staging`; and a
round-coherence assertion — every pre-commit fault leaves all authoritative files byte-identical, every
partial commit / crash recovery restores them, and recovery never leaves them split across rounds.

**8 — CI.** `final-integration.yml` runs `season_state_fenced_test.py` + the extended
`season_advance_r14_r19_proof.py`/`release_state_failclosed_test.py`; `live-scoring.yml` runs the extended
`failure_injection_proof.py` (8 points + round-coherence). Committed JSON alone is never sufficient — the red
paths and sequential/rollback proofs are re-run on the pinned runner.

**Immutable vs dynamic identity.** Immutable release policy = the derivation policy (`derivation_policy_id`),
the config manifest, and the source identities (`rl_model`/`engine_head`/`fv`/`register`/`band`). Dynamic
release state = `as_of_round`, `store`/`board` pins, `calendar_progress`, `exposure_pace` — advanced together
each week across `expected_boot.json` + `season_state.json` + `release_contract.json`; the present-lens
baseline `release_lineage.json` never moves for a weekly round.

**Re-pin (source edits for the fencing).** `rl_model` `c3a243ee→4f776e07`, `engine_head` `feff9471→dc7e34b0`,
`fv` `97abe963→6a9a520f` in `expected_boot.json` + `release_contract.json` identities; regenerated
`board_view_working.js` + `club_valuation.js`. Board bytes unchanged (`2ab73a6f`); only source identities move.
Clean-room rebuild-equality **9/9**; R15 ladder **12/12**; R14–R19 sequential proof green.
