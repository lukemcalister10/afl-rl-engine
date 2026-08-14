#!/bin/bash
# ORDER 29B -- Guard 5 (the stale-boot guard) on the ENTRY-WIRED checkout, run against the restamped
# pins. Reads the checkout in place; writes only its own transcript.
set -uo pipefail
ROOT=${RL_ROOT:-/home/user/afl-rl-engine/.claude/worktrees/agent-a37dad81e950d907f}
export PATH="/root/rl_venv312/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$ROOT:$ROOT/engine/rl_after:$ROOT/vendor"
export RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
cd "$ROOT"
python3 boot_guard.py ORDER29B engine/rl_after/rl_model_data.json engine/rl_after/_merged_recover.py \
    > "$ROOT/docs/evidence/landing_29_2026-08-13/BOOTGUARD29B.txt" 2>&1
echo "GUARD_EXIT=$?" >> "$ROOT/docs/evidence/landing_29_2026-08-13/BOOTGUARD29B.txt"
cat "$ROOT/docs/evidence/landing_29_2026-08-13/BOOTGUARD29B.txt"
