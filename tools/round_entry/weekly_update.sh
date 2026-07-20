#!/usr/bin/env bash
# weekly_update.sh — the owner's one-command weekly updater (Linux / macOS / WSL / Git-Bash).
#
# A thin wrapper over the Python CLI (tools/round_entry/round_entry.py). It sets a portable,
# deterministic environment (vendored unidecode on the path, PYTHONHASHSEED=0, single-thread BLAS to
# match the board-of-record recipe) and forwards every argument to the CLI. NO Python editing needed.
#
# THE 2-MINUTE WORKFLOW
#   ./weekly_update.sh enter   --round 15 --body-file round15.csv   # paste name,score -> snapshot
#   ./weekly_update.sh confirm --round 15                           # (only if there was residue)
#   ./weekly_update.sh show    --round 15                           # inspect the EXACT snapshot
#   ./weekly_update.sh apply   --round 15                           # apply it (gate-guarded)
#   ./weekly_update.sh recover                                      # after an interrupted apply
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
exec "$PY" "$REPO/tools/round_entry/round_entry.py" "$@"
