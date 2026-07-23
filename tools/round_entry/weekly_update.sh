#!/usr/bin/env bash
# weekly_update.sh — the owner's one-command weekly updater (Linux / macOS / WSL / Git-Bash).
#
# A thin wrapper over the Python CLI (tools/round_entry/round_entry.py). It sets a portable,
# deterministic environment (vendored unidecode on the path, PYTHONHASHSEED=0, single-thread BLAS to
# match the board-of-record recipe) and forwards every argument to the CLI. NO Python editing needed.
#
# THE 2-MINUTE WORKFLOW
#   ./weekly_update.sh enter    --round 15 --body-file round15.csv  # paste name,score -> snapshot
#   ./weekly_update.sh confirm  --round 15                          # (only if there was residue)
#   ./weekly_update.sh show     --round 15                          # inspect the EXACT snapshot
#   ./weekly_update.sh apply    --round 15                          # apply (gate-guarded) + finalize
#   ./weekly_update.sh recover                                      # after an interrupted apply (rollback)
#   ./weekly_update.sh finalize --round 15                          # finish/resume finalization (no re-apply)
#   ./weekly_update.sh repair   --round 15                          # force-rebuild derived outputs (no re-apply)
#
# TWO PHASES PER ROUND. `apply`/`run`/`catchup` first make the CANONICAL commit (store/board/ledger/
# history, staged + atomic, rollback on a mid-swap crash), then run a JOURNALED, IDEMPOTENT
# FINALIZATION of the re-derivable owner-facing outputs (UI board bundles + movers report/bundle +
# round-delta injection). A finalization failure NEVER rolls back the commit: the round is left
# FINALIZATION_INCOMPLETE and the command exits non-zero. `finalize`/`repair` finish or rebuild those
# outputs from the committed state; a restart auto-detects a committed-but-unfinalized round and will
# not advance to the next round until it is FINALIZED.
#
# APPLY IS GATED OFF BY DEFAULT (this build applies no real round). `apply` will REFUSE and print
# instructions unless you arm BOTH halves LOCALLY for the run — no code edit, just two env vars:
#   INGEST_SCORE_APPLY_ARMED=1  INGEST_SCORE_APPLY=<your-own-token>  ./weekly_update.sh apply --round 15
# See tools/round_entry/README.md. Nothing is armed in the committed repo.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
cd "$REPO"

# deterministic single-env board build (matches session_*/build_board.sh)
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-1}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-1}"

# portable vendor: prefer an already-seeded workspace vendor, else the repo's own vendored copy.
if [ -z "${RL_VENDOR:-}" ]; then
  if [ -d "/home/claude/rl_vendor/unidecode" ]; then
    export RL_VENDOR="/home/claude/rl_vendor"
  else
    export RL_VENDOR="$REPO/vendor"
  fi
fi
export PYTHONPATH="$REPO/engine/rl_after:$RL_VENDOR${PYTHONPATH:+:$PYTHONPATH}"

PY="${PYTHON:-python3}"

# ITEM 408 item 5 — the balanced/strict SIBLING advance-repin is folded INTO the Python round-advance
# transaction (engine/rl_after/ingestion/staged_apply.py::_stage_sibling): a store advance regenerates the
# sibling board + FV reference vector and moves every dependent pin/aggregate/seal/view UNDER THE SAME
# transaction journal + rollback boundary as the store/board. The invariant therefore lives in the Python
# transaction every launcher (.sh / .bat / direct CLI) drives via round_entry.py — NOT in this shell — so
# no launcher can bypass it and there is never an externally-committed store/board state with stale siblings.
set +e
"$PY" "$REPO/tools/round_entry/round_entry.py" "$@"
RC=$?
set -e
if [ "$RC" -ne 0 ]; then
  exit "$RC"
fi

# Refresh current club totals after every successful operation that can move/rebuild the weekly board.
case "${1:-}" in
  apply|run|catchup|finalize|repair)
    "$PY" "$REPO/ui/tools/ingest_inputs.py"
    ;;
esac
