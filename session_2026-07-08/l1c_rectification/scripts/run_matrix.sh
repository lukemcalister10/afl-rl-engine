#!/bin/bash
# Build one walk-forward as-of matrix with a given env config. Guard 5 asserted on entry.
# usage: run_matrix.sh <out.json> [ENV=VAL ...]
set -e
OUT=$1; shift
HERE=/home/user/afl-rl-engine
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" run_matrix /home/claude/rl_workspace/rl_after/rl_model_data.json
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export PATH="/root/rl_venv312/bin:$PATH"
for kv in "$@"; do export "$kv"; done
S4_MATRIX="$OUT" python3 s4_matrix_M1v7.py
