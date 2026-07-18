#!/bin/bash
# LEG F1 dev-shell board recipe (mirrors the Leg E recipe: RL_REPO set, PYTHONHASHSEED=0, no RL_CONFIG_MODE).
# Reproduces rl_app_data.json from the cc58570 candidate engine synced into a private workspace, and prints
# the board md5 (== the 8-hex board hash of record). Env gates (RL_LEGE/RL_PVC2/RL_LEGF) pass through.
# Usage: RL_LEGE=.. RL_PVC2=.. RL_LEGF=.. build_board.sh [label]
set -euo pipefail
REPO=/home/user/afl-rl-engine
BASE=/home/claude/rl_ws_legf
WS=$BASE/rl_after
LABEL="${1:-board}"
cd "$WS"
export RL_REPO="$REPO"
export PYTHONHASHSEED=0
export PYTHONPATH="$WS:/home/claude/rl_vendor"
rm -f rl_app_data.json
python3 rl_export.py > "/home/user/afl-rl-engine/session_2026-07-18/legf1/out/exportlog_${LABEL}.txt" 2>&1
MD5=$(md5sum rl_app_data.json | cut -c1-8)
echo "$MD5"
