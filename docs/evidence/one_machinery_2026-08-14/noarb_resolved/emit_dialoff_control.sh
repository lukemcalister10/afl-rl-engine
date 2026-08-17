#!/bin/bash
# CONTROL: the identical 29C emit on the identical HEAD worktree, with the 30B-N dial OFF.
# Sole purpose: establish whether the ORDER 29C replication HALT is caused by this seat's dial or is
# PRE-EXISTING on this branch.
set -uo pipefail
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o30bn_O30BNCTL
OUT=$SP/o30bn/emit_O30BNCTL
REPO=/home/user/afl-rl-engine/.claude/worktrees/agent-a14698ead2bf8585d
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
mkdir -p "$OUT"
cp "$REPO/docs/evidence/landing_29_2026-08-13/noarb29c/emit_matrix_29c.py" "$OUT/emit.py"
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
unset RL_O30B_RESOLVED RL_O30B_PREVIEW
echo "DIAL OFF CONTROL. ref $(git -C "$WT" rev-parse --short HEAD)"
python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1
echo "exit=$?"
grep -E 'REPLICATION|HALT' "$OUT/emit.log" | head -3
