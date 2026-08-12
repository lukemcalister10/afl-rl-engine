#!/bin/bash
# ORDER 20C — the two declared refits (one process each) + the merge, against the staged FIX tree.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RC_TREE="$SP/tree_FIX"
export RL_REPO="$RC_TREE" RL_FV="$RC_TREE/engine/forward_valuation"
export PYTHONPATH="$RC_TREE/engine/rl_after:$RC_TREE:$RC_TREE/vendor"
unset RL_CONFIG_MODE RL_BAKE_V0SURF
S=$(date +%s)
RC_CAP=1.4 RC_OUT="$SP/v0fit_lo.pkl" python3 "$HERE/v0surf_fit_one.py" || exit 1
RC_CAP=99  RC_OUT="$SP/v0fit_hi.pkl" python3 "$HERE/v0surf_fit_one.py" || exit 1
python3 "$HERE/v0surf_merge.py" "$SP/v0fit_lo.pkl" "$SP/v0fit_hi.pkl" \
        "$RC_TREE/data/v0surf.pkl" "$SP/v0surf_merged.pkl"
rc=$?
E=$(date +%s)
echo "  capkeys exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
exit $rc
