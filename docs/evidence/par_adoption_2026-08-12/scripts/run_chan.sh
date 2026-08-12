#!/bin/bash
# ORDER 20B — run channel_harness.py for one MODE.
# Usage: bash run_chan.sh <MODE> <out.json>
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_REPO="$SP/tree_FIX" RL_FV="$SP/tree_FIX/engine/forward_valuation"
export HEAD_TREE="$SP/tree_HEAD"
export PYTHONPATH="$SP/tree_FIX/engine/rl_after:$SP/tree_FIX:$SP/tree_FIX/vendor"
export GRID_HEAD="$SP/probe_HEAD.json" GRID_FIX="$SP/probe_FIX.json"
export MODE="$1" OUT="$2"
S=$(date +%s); python3 "$HERE/channel_harness.py"; rc=$?; E=$(date +%s)
echo "  chan($1) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s -> $2"
exit $rc
