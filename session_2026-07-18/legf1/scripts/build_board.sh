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
# DETERMINISM: pin BLAS/OpenMP to a single thread. The board reduces over player features through OpenBLAS
# (DYNAMIC_ARCH); with >1 thread the cross-thread reduction order is not fixed => run-to-run last-ULP jitter
# in 6-dp float display fields => a wandering whole-board md5. Single-thread makes the board bit-stable AND
# reproduces the filed hashes byte-exact (06d8af60 / d85901af / 9829d01a). This is determinism, not a
# CORETYPE/microarch pin (supervisor item 347: no CORETYPE archaeology).
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
rm -f rl_app_data.json
python3 rl_export.py > "/home/user/afl-rl-engine/session_2026-07-18/legf1/out/exportlog_${LABEL}.txt" 2>&1
MD5=$(md5sum rl_app_data.json | cut -c1-8)
echo "$MD5"
