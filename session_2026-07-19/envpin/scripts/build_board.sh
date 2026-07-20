#!/bin/bash
# ENV-PIN dev-shell board recipe (mirrors leg F6/F1: RL_REPO set, PYTHONHASHSEED=0, single-thread BLAS,
# no RL_CONFIG_MODE). Fresh copy of engine/rl_after @ HEAD into a private workspace, run rl_export.py,
# print the 8-hex board md5. Balanced board of record = RL_LEGE=0 RL_LEGF=0 (ties 06d8af60).
# Usage: RL_LEGE=.. RL_LEGF=.. RL_PVC2=.. build_board.sh [label]
set -euo pipefail
REPO=/home/user/afl-rl-engine
BASE=/home/claude/rl_ws_envpin
WS=$BASE/rl_after
LABEL="${1:-board}"
export PATH="/root/rl_venv312/bin:$PATH"
rm -rf "$BASE"; mkdir -p "$BASE"
cp -rf "$REPO/engine/rl_after"          "$BASE/"
cp -rf "$REPO/engine/forward_valuation" "$BASE/"
cp -f  "$REPO/config_manifest.py"       "$WS/config_manifest.py"
cp -f  "$REPO/LTI_REGISTER.md"          "$WS/LTI_REGISTER.md"
# data deps the engine loads by absolute path (seeded by the session-start bootstrap; re-assert here)
cp -f "$REPO/data/cm_400.pkl"  /home/claude/cm_400.pkl
cp -f "$REPO/data/q97m.pkl"    /home/claude/q97m.pkl
cp -f "$REPO/data/v0surf.pkl"  /home/claude/v0surf.pkl
cd "$WS"
export RL_REPO="$REPO"
export PYTHONHASHSEED=0
export PYTHONPATH="$WS:/home/claude/rl_vendor"
# DETERMINISM (leg F1/F6): pin BLAS/OpenMP to one thread so the reduction order is fixed.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
rm -f rl_app_data.json
python3 rl_export.py > "$REPO/session_2026-07-19/envpin/out/exportlog_${LABEL}.txt" 2>&1
md5sum rl_app_data.json | cut -c1-8
