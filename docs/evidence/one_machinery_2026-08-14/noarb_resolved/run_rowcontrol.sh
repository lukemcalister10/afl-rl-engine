#!/bin/bash
# ORDER 30B-N -- the row control, run against a RESOLVED-lane staged build. Same pinning as every other
# run in this order: pinned venv, five-var thread pinning, PYTHONHASHSEED=0, strictly sequential.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
TAG=${1:-resA}
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o30bn
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
export RL_O30B_RESOLVED=1
export RL_REPO="$REPO" RL_FV="$SP/bb_$TAG/forward_valuation" STAGE="$SP/bb_$TAG/rl_after"
export RL_V0SURF_PKL="$REPO/data/v0surf.pkl"
export PREVIEW_EV="$SP/PREVIEW_EV_UNROUNDED.json"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
python3 "$HERE/o30bn_rowcontrol.py" "$SP/bb_$TAG/rl_after/rl_app_data.json" \
        "$HERE/ROWCONTROL_30BN.json" 2>&1 | tee "$HERE/ROWCONTROL_30BN_out.txt"
