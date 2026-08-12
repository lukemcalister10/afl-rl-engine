#!/bin/bash
# ORDER 20C — engine_probe.py (ORDER 20B's, byte-identical) on the FIX tree with the cap NEUTRALISED
# through the env dial, reading the re-keyed v0surf pickle. Dev shell, exactly like run_probe.sh.
# Usage: bash run_probe_nocap.sh <out.json> [cap]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/tree_FIX
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset RL_CONFIG_MODE
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$SP/v0surf_merged.pkl"
export RL_RUC_PRIOR_CAP="${2:-99}"
export OUT="$1"
echo "  DIAL: RL_RUC_PRIOR_CAP=$RL_RUC_PRIOR_CAP  v0surf=$RL_V0SURF_PKL"
S=$(date +%s); python3 "$HERE/engine_probe.py"; rc=$?; E=$(date +%s)
echo "  probe(FIX nocap) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s -> $1"
exit $rc
