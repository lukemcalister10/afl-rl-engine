#!/bin/bash
# ORDER 31-F -- the pinned analysis environment. Same five-var thread pinning, same pinned venv, same
# RL_V0SURF_PKL override and the same engine env vars bb31f.sh exports for board builds. Read-only tools
# are run through this so that a harness that imports the engine sees EXACTLY the board's environment.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=${RL_ROOT:-/home/user/afl-rl-engine/.claude/worktrees/agent-a8ab36345dce038ee}
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
exec /root/rl_venv312/bin/python3 "$@"
