#!/bin/bash
# ORDER 20C — P4a. Drive the COMMITTED refit entry point in its NO-WRITE --verify mode against a staged
# tree, at the shipped cap. Nothing is baked: --bake additionally requires RL_BAKE_V0SURF=1, which is
# never set here.
#
# Usage: bash run_refit_verify.sh <HEAD|FIX> [RL_RUC_PRIOR_CAP value]
set -uo pipefail
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
WT=$SP/tree_$1
CAP=${2:-1.4}
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_RUC_PRIOR_CAP="$CAP"
unset RL_CONFIG_MODE RL_BAKE_V0SURF
cd "$WT/engine/rl_after"
S=$(date +%s)
RL_V0SURF_REFIT=1 python3 "$WT/session_2026-07-18/legf6/scripts/refit_v0surf.py" --verify
rc=$?
E=$(date +%s)
echo "  refit_verify($1, cap=$CAP) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
exit $rc
