#!/bin/bash
# ORDER 20C — run ruck_extra.py against one staged tree (dev shell, like run_probe.sh).
# Usage: bash run_extra.sh <HEAD|FIX> <out.json>
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/tree_$1
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset RL_CONFIG_MODE
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export OUT="$2"
S=$(date +%s); python3 "$HERE/ruck_extra.py"; rc=$?; E=$(date +%s)
echo "  extra($1) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s -> $2"
exit $rc
