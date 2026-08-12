#!/bin/bash
# ORDER 20C — faller_diag.py on the FIX tree at both caps.
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
echo "--- cap = 1.4 (shipped) ---"
RL_RUC_PRIOR_CAP=1.4 OUT="$SP/faller_cap14.json" python3 "$HERE/faller_diag.py" || exit 1
echo "--- cap = 99 (neutralised) ---"
RL_RUC_PRIOR_CAP=99  OUT="$SP/faller_cap99.json" python3 "$HERE/faller_diag.py" || exit 1
