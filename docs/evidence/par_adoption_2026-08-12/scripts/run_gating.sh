#!/bin/bash
# ORDER 20B — run gating_probe.py against one staged tree.
# Usage: bash run_probe.sh <HEAD|FIX|treedir> <out.json>
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
T="$1"; OUTF="$2"
case "$T" in HEAD|FIX) WT=$SP/tree_$T ;; *) WT="$T" ;; esac
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0 RL_CONFIG_MODE=
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export OUT="$OUTF"
S=$(date +%s)
python3 "$HERE/gating_probe.py"
rc=$?
E=$(date +%s)
echo "  gating($T) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s  -> $OUTF"
exit $rc
