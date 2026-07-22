# Weekly Updater — safe-local hardening (DESIGN)

Branch `prep/weekly-updater-safe-local`, from PR #125 head `f6e7f8457c…` (descends `3055ea5f…`).
Builds on PR #125's store-write functionality; corrects its material safety + usability gaps. **The
real apply gate stays OFF; no real round is applied.** The numerical value wobble is out of scope and
left as an external blocker (this design makes no cross-run/cross-machine determinism claim).

## Gaps corrected (vs PR #125)

| PR #125 gap | fix |
|---|---|
| stale preview/snapshot could apply to a moved store | snapshot carries the **full** source-store md5; apply refuses unless the live store still hashes to it |
| partial store/board/manifest/ledger writes (in-place, no rollback) | **staged transaction**: stage → validate → atomic swap, with rollback + crash recovery |
| `name,score` CLI and store-writer disconnected | `apply` consumes the **exact snapshot** (no re-resolve) via `preview_from_snapshot` |
| no simple owner apply command | `round_entry apply` + `weekly_update.sh`/`.bat` launcher, plain-language summary |
| no failure-injection / rollback proof | `failure_injection_proof.py` — 7 injection points + crash recovery + acceptance |

## Files

- `engine/rl_after/ingestion/round_entry.py` — snapshot library; **strong identity** (JOB 2): full+short
  store md5, round/season, stable IDs, exact scores, module/version identity, deterministic
  `content_hash`; `verify_snapshot`/`is_strong`/`compute_content_hash`. v1 snapshots still load; the
  strong apply requires v2.
- `engine/rl_after/ingestion/staged_apply.py` — `StagedRoundApplier` (JOB 3/4) + `preview_from_snapshot`.
- `tools/round_entry/round_entry.py` — CLI `enter`/`confirm`/`show`/`apply`/`recover` (JOB 1/4).
- `tools/round_entry/weekly_update.sh` + `.bat` + `README.md` — launcher (JOB 7).
- `engine/rl_after/ingestion/score_ingestor.py` — gate now also armable via `INGEST_SCORE_APPLY_ARMED=1`
  (local, no code edit); **shipped default OFF unchanged** (`APPLY_DEFAULT=False`, no token).
- `session_2026-07-20/weekly_updater_hardening/` — this design + the proofs.

## Snapshot → preview (score meaning preserved — HARD-HALT guard)

`preview_from_snapshot(snapshot, store)` builds the store-writer's preview **without re-resolving
names** (uses the snapshot's stable IDs/keys). Each resolved row is one *played* round at its snapshot
score; the season entry is merged with the **same weighted-mean arithmetic** `ScoreIngestor.preview`
uses. The proof cross-checks this: the merged entries equal what `score_ingestor.preview` produces from
the equivalent structured feed — so the conversion never changes score meaning.

## Staged transaction (JOB 3)

1. **STAGE** in a disposable workspace (a full repo-shaped copy): merge the snapshot into the workspace
   store; regenerate the board (+ fresh sidecar) from the *staged* store; re-stamp the workspace boot
   manifest; update the workspace ledger. **The live files are untouched.**
2. **VALIDATE the staged outputs** (all against the workspace):
   staged store parses · only the fed players' season scores changed (nothing else) · board generated
   + parses · **board source-stamp == staged store** · **boot pins == staged store+board** · **Guard 5
   GREEN** (real `boot_guard.py`, `RL_REPO=`workspace) · ledger holds the exact snapshot triples ·
   board **player universe unchanged**. No numerical-determinism verdict is invented.
3. **COMMIT**: copy the validated outputs into `txn/staged` (same filesystem as the live files,
   md5-verified byte-identical to what was validated), back up the live originals into
   `txn/originals`, then `os.replace` each staged file over its live target — atomic swaps.

Every refusal (incomplete-txn / gate / stale / altered / residue / clean / season / dedup) fires
**before** any staging, so a refused apply leaves all five targets byte-unchanged.

## Rollback + crash recovery (JOB 4)

Transaction directory (`engine/rl_after/ingestion/.weekly_txn/<txn_id>/`, on the live filesystem):
`originals/` (immutable backups) · `staged/` (validated replacements) · `manifest.json` (status +
snapshot identity + targets) · `journal.jsonl` (append-only, fsync'd phase log).

- **Failure during the swap** → the applier restores **every** original (`ROLLED_BACK`); the store is
  never left with a stale board/manifest/ledger.
- **Crash mid-swap** (process killed, no handler) → the transaction is left non-terminal
  (`COMMITTING`). The next `apply` **refuses** (`IncompleteTransactionError`); `recover` rolls back to
  the originals and marks the txn `RECOVERED`. **Evidence is never silently deleted** (on success the
  heavy payload is pruned but `manifest.json`+`journal.jsonl` are kept as the record).

## Gate stays OFF (JOB 6)

`APPLY_DEFAULT=False`, no `INGEST_SCORE_APPLY` token committed, empty ledger, byte-identical real store
(`968de0c7`) and canonical board (`270a2c5f`). All write tests use isolated scratch copies; the harness
arms the gate in-process only. Local arming (`INGEST_SCORE_APPLY_ARMED=1` + a token) is the owner's
deliberate, uncommitted action.

## Provenance hardening — 2026-07-20 follow-up (fixes a critical defect found by the audit)

The first pass had a **critical defect**: the staged board build inherited the ambient/workspace
`forward_valuation`. `RL_FV` defaults to `/home/claude/rl_workspace/forward_valuation`, which in this
container holds a **stale `distribution_pricing` (`21d530bf`)** — the exact module the audit named as
producing the wrong board `d7a95e8d`. `RL_FV` ∈ `config_manifest.INFRA_ALLOW`, so the config gate does
**not** catch it, and Guard 5 does not check the valuation module — so the first pass silently built
boards from the stale module. **The "no blocking UNKNOWNs" claim is withdrawn.**

**Fail-closed FV provenance (`staged_apply`).** For every staged generation the board build now:
- binds `RL_FV` **explicitly to the staged repo's** `engine/forward_valuation`;
- sets `PYTHONPATH` from the **staged repo only** + the pinned vendor;
- **clears every inherited `RL_*`/`PAR_*`** variable (model flags AND path redirects: `RL_FV`,
  `RL_APP_DATA`, `RL_Q97M_PKL`, `RL_V0SURF_PKL`, …) so nothing ambient can redirect a valuation import;
- **records `distribution_pricing`'s resolved path + full md5** and asserts it is **inside the staged
  repo AND byte-identical to the staged source**, **halting before board generation** on any mismatch;
- stamps the FV path/hash into the **transaction manifest + validation evidence** (`fv_provenance`).

The FV resolution is entirely `RL_FV`-anchored (dist_redesign loads `distribution_pricing` from its own
dir; there is no plain `import distribution_pricing` anywhere), so binding `RL_FV` + asserting the
resolved file's location and hash is a complete, fail-closed guard. Proof: `fv_provenance_proof.py`
(`FV_PROOF.md`) — green build uses the staged `d0c8c69f`; the ambient `21d530bf` halts; an adversarial
inherited `RL_FV` is forced back to the staged module; the stale `d7a95e8d` board is never produced.

**Accepted valuation configuration.** The build no longer inherits arbitrary `RL_*` flags. An inherited
model-semantic flag that is unknown to, or conflicts with, the release config manifest
(`data/model_config.json`) **halts before staging** (`ConfigPolicyError`); the build runs with
`RL_CONFIG_MODE=gate`, so `config_manifest.enforce` clears ambient model vars and loads the pinned
policy (the config hash is recorded in the transaction evidence, and the build confirms it engaged).
The board sidecar is also staged + published + atomically swapped (the first pass published only the
board JSON).

## Scope & status — CORRECTED (this branch is a transaction-core prototype, NOT a safe weekly updater)

Explicitly **not** delivered here, and **not to be built on this base** until the numerical root result
is final, the v2.11 release head exists, and this branch is rebased onto it:
- **UI bundle generation is still outside this transaction** (the Matchday working/public bundles,
  `extract_board_view.py`, the entrant banner, five-lens/browser validation).
- **Previous-round movement data is not yet generated** (no `dRound`/movement report).
- **Immutable weekly history, correction and undo remain pending** (the transaction dir keeps originals
  + a journal for recovery, but not a full per-round immutable record; there is no `correct`/`undo`).
- **The tool is NOT ready for real owner use.** The gate **must remain OFF**; no real round is applied.

## Audit reconciliation (independent systems audit, 2026-07-20)

| # | audit finding | status |
|---|---|---|
| 2.1 | numerical root fix unresolved (d7a95e8d ≠ 06d8af60 on a clean container) | **STILL OPEN** — external blocker; not touched here |
| 2.2 | final candidate stack not baked (no v2.11 head) | **DEFERRED-UNTIL-V2.11-REBASE** |
| 2.3 | canonical identities stale/inconsistent (board pin, UI config, tag/round) | **DEFERRED-UNTIL-V2.11-REBASE** |
| 2.4 | Leg-F entrant objects not copied by the UI extractor | **DEFERRED-UNTIL-V2.11-REBASE** (UI tranche) |
| 2.5 | previous-round fields dropped/unwired; Round Review empty | **DEFERRED-UNTIL-V2.11-REBASE** (movement tranche) |
| 2.6 | retrospective seam metadata-key mismatch + stale fallback | **DEFERRED-UNTIL-V2.11-REBASE** (UI tranche) |
| 2.7 | build/release ops fragmented, hardcoded machine paths | **DEFERRED-UNTIL-V2.11-REBASE** |
| 2.8 | weekly regen can use the wrong valuation config; sidecar not published | **CLOSED** — FV provenance bound + `RL_CONFIG_MODE=gate` policy + sidecar staged/swapped |
| 3.1 | no single owner workflow (snapshot→preview adapter) | **CLOSED** — `apply` + `preview_from_snapshot` (no re-resolve) |
| 3.2 | stale previews overwrite newer scores | **CLOSED** — snapshot full-md5 gate; apply refuses on a moved store (proven) |
| 3.3 | not transactional across store/board/manifest/ledger | **CLOSED** — staged txn + atomic swaps + sidecar |
| 3.4 | no recovery mechanism | **CLOSED** — journal + pending-detector + `recover` + before-backups + rollback |
| 3.5 | weekly history not immutable | **STILL OPEN** — recovery backups only; full immutable per-round record deferred |
| 3.6 | correction/undo unsupported | **STILL OPEN** — `correct`/`undo` not built (deferred tranche) |
| 3.7 | partial feeds/late additions (amendment modes) | **STILL OPEN** — dedup blocks re-send; no amendment mode |
| 3.8 | DNP semantics (absence = no game) | **DEFERRED-UNTIL-V2.11-REBASE** — contract documented; real-round completeness test pending |
| 3.9 | season/round hardcoded (2026 / 24) | **DEFERRED-UNTIL-V2.11-REBASE** — should come from release metadata that does not exist yet |
| 3.10 | single-round vs full-season not owner-visible | **STILL OPEN** — only single-round merge; explicit modes deferred |
| 3.11 | UI regeneration missing | **DEFERRED-UNTIL-V2.11-REBASE** — out of this transaction by design |
| 3.12 | local runtime not owner-ready (Windows one-command install) | **DEFERRED-UNTIL-V2.11-REBASE** — launcher shipped; full WSL2/Docker distribution pending |

Test-matrix (audit §8) coverage: stale-preview, duplicate, fault-injection, process-termination,
board-validation, repeat-build, DNP-structured-path → covered (see `PROOF.md`/`FV_PROOF.md`). Correction,
undo, single/full-season, real FootyWire parse, movement controls, fresh-machine recovery, owner
usability → **STILL OPEN / DEFERRED**. Related residual noted for the rebase: `distribution_pricing`
also does `sys.path.insert(0,'/home/claude/rl_after'); import rl_model` — inert in the board build
(`rl_model` is import-cached from the staged workspace first) and Guard-5-covered for the repo copy, but
the ambient `/home/claude/rl_after` should be removed from that path at the v2.11 bake.
