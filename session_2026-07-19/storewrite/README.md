# WEEKLY-APPLY STORE-WRITE + DEDUP LEDGER (gate OFF, report-only)

Directive: `docs/DIRECTIVE_STOREWRITE_weekly_apply_2026-07-19.md`. Base `3055ea5` (#123, env-pin),
STRICT. Parallel to the v2.11 bake (conflict-free: both re-stamp the same two engine pins). **Writes
nothing to the real store** — the apply gate ships OFF; every write below is on a throwaway scratch
copy. This PR is **report-only, DO-NOT-MERGE until go-live**.

## What this builds (behind the existing double-OFF gate)
- **`engine/rl_after/ingestion/round_apply.py`** — `RoundApplier`, the store-write `apply()` the
  provision job deliberately left absent. Merge one validated weekly round's `merged_entry` per
  player into the single source **in place** → regenerate the board (`rl_export.py`) as a derived,
  source-stamped, read-only artifact → re-stamp `data/expected_boot.json`'s `store`+`board` pins →
  record the dedup ledger. All-or-nothing; every refusal fires before the store is touched.
- **`engine/rl_after/ingestion/applied_rounds_ledger.json`** — the dedup ledger, seeded EMPTY. One
  record per `(stable_player_id | season | round)`; a re-sent weekly feed reproduces the same triples
  so the across-feed re-send is refused (the in-feed `duplicate_round` anomaly is a separate catch).
- **Season bound** — a round beyond the season count (`DEFAULT_SEASON_ROUNDS=24`, owner pins exact at
  go-live) is refused before any merge.
- `score_ingestor.apply()` now delegates to `RoundApplier.for_repo()` when the gate is armed; the
  gate itself is unchanged (`APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset — both OFF).

## The gate (unchanged, ships OFF — belt-and-braces)
`apply()` refuses unless **both** halves are on: the code half (`score_ingestor.APPLY_DEFAULT`) AND
the env half (`INGEST_SCORE_APPLY`). Neither a stray env var nor a stray code edit can arm it alone.
The proof harness arms it **in-process only** (ephemeral, never committed) to exercise the write path
against scratch; no scratch path resolves to the real single source.

## PRE-STEP 0 (green-boot; not the deliverable)
Base `3055ea5` shipped STALE engine pins (item 399). Re-stamped `data/expected_boot.json`'s two
engine pins to the verified engine md5s (`rl_model → cc626d7d…`, `engine_head → 904722cd…`; md5'd the
files first), byte-identical to the parallel bake. Only those two pins; every other pin byte-unchanged.
Also corrected a STALE dry-run proof: `dry_run_proof.py` fed `affl_team` (the AFFL keeper team) as the
resolver's club, but the resolver vetoes on `afl_club` (the real AFL club, item 20d) — the proof.json
predated the `afl_club` import (built at store `b0c39d78`). Feeding `afl_club` resolves 625/625.

## Proofs (all on scratch; nothing to the real store)
- `python3 engine/rl_after/ingestion/dry_run_proof.py` → PROOF PASS, 625 sampled, 0 exc / 0 anomalies,
  byte-for-byte (store `968de0c7`).
- `python3 session_2026-07-19/storewrite/storewrite_proof.py --write` → proofs A–D (see `PROOF.md`):
  - **A** scratch round-15 apply: store+board move, all fed players move, re-stamp coherent, Guard 5 green.
  - **B** dedup blocks the re-send (store/board/ledger untouched).
  - **C** season bound refuses round 99.
  - **D** 5× single-env apply+regen → byte-stable board (single-env determinism; cross-machine is a
    separate item, not attempted).

## Go-live (later, owner-worded) — `docs/GO_LIVE_round_score_ingestion.md` FLIP ORDER
Rebase onto the baked v2.11 head; set both gate halves; `RoundApplier.for_repo()` applies ONE round to
the real store, re-pins in the same commit, regenerates the board. This build proves that path on scratch.
