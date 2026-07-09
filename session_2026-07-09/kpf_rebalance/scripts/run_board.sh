#!/bin/bash
# one-engine-load board dump with the pinned env; usage: run_board.sh <out.json> [ENV=VAL ...]
set -e
OUT=$1; shift
HERE=/home/user/afl-rl-engine
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export PATH="/root/rl_venv312/bin:$PATH"
RL_REPO="$HERE" python3 $HERE/session_2026-07-09/kpf_rebalance/scripts/board_dump.py "$OUT" "$@"
