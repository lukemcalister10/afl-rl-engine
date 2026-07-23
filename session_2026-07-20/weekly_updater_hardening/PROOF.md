# FAILURE-INJECTION + ACCEPTANCE PROOF — weekly updater safe-local (gate OFF, scratch only)

Writes **nothing** to the real store (gate ships OFF: `APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset; real-store apply refused = `True`). Every write below is on a throwaway scratch repo.

## RESULT: **ALL PASS**  (1195.6s)

## Failure injection (8 points) — rollback leaves the scratch byte-identical (incl season_state + release_contract)
| injection point | files byte-identical | no dedup entry | no partial board | txn status | pass |
|---|---|---|---|---|---|
| `before_store_staging` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `during_board_generation` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `after_board_generation` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `during_manifest_staging` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `during_contract_staging` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `during_ledger_staging` | True | True | True | ABORTED_PRECOMMIT | ✅ |
| `after_first_replacement` | True | True | True | ROLLED_BACK | ✅ |
| `after_subsequent_replacement` | True | True | True | ROLLED_BACK | ✅ |

## Crash recovery (hard-exit mid-commit -> refuse -> recover)
| check | value |
|---|---|
| child crashed after first replacement | True |
| mid-crash: store changed, board still stale (inconsistent) | True / True |
| incomplete transaction detected | True |
| next apply REFUSED until recovered | True |
| recover restored ALL originals (byte-identical) | True |
| no dedup entry after recover | True |
| transaction marked RECOVERED (evidence kept) | True |

## Acceptance
| case | result |
|---|---|
| clean apply: store `968de0c7`→`4a17ffb0`, board `2ab73a6f`→`baf80bb4`, 5 players, Guard 5 GREEN, pins coherent | ✅ |
| immediate re-send BLOCKED (dedup), files unchanged | ✅ |
| stale snapshot BLOCKED (store md5 moved), files unchanged | ✅ |
| altered snapshot hash BLOCKED | ✅ |
| invalid round BLOCKED (season bound) | ✅ |
| unresolved residue cannot apply | ✅ |
| snapshot→preview preserves score meaning (== score_ingestor, 8 players) | ✅ |

> Single-env, scratch-only. No numerical-determinism verdict is claimed — the board is validated for structure, source-stamp coherence, Guard-5 pins and player universe, not for a cross-run/cross-machine value guarantee (a separate, external item).
> Boards here are built under the hardened, fail-closed forward-valuation path (RL_FV bound to the staged repo + config policy from the release manifest) — see `FV_PROOF.md`.
