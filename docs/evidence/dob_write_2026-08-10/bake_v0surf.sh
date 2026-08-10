#!/bin/bash
# v0surf RE-CUT — the sanctioned refit lane, on the WRITTEN store.
# Owner word 2026-08-10, issue #334 comment 5235816134: "Authorise the refit."
#
# ISOLATION NOTE: another seat is live in /home/claude and has placed a NON-PINNED
# v0surf at /home/claude/v0surf.pkl, which sits ahead of <repo>/data/v0surf.pkl in the
# engine's load precedence. RL_V0SURF_PKL is set explicitly to THIS checkout's artifact,
# which is the highest-precedence slot, so the engine provably loads our own surface and
# never that seat's. Guard 5 re-asserts the loaded path against the pin on every entry.
set -uo pipefail
REPO=/home/claude/dobwrite
WS=/home/claude/dob_ws/rl_after
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$WS:/home/claude/rl_vendor"
export RL_V0SURF_PKL="$REPO/data/v0surf.pkl"
export RL_V0SURF_REFIT=1
export RL_BAKE_V0SURF=1
cd "$WS"
echo "== store in workspace =="
md5sum rl_model_data.json
echo "== v0surf BEFORE =="
md5sum "$REPO/data/v0surf.pkl"
echo "== refit_v0surf.py --bake =="
python3 "$REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py" --bake
echo "bake exit=$?"
echo "== v0surf AFTER =="
md5sum "$REPO/data/v0surf.pkl"
echo BAKE_DONE
