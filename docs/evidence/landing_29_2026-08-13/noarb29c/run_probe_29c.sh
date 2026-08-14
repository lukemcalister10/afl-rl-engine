#!/bin/bash
# ORDER 29C -- the landed-entry-law probe, run on a detached worktree of HEAD.
# Sibling of emit_variant_o29.sh; identical worktree/env discipline, including the declared
# RL_V0SURF_PKL first-precedence override (the shared /home/claude/v0surf.pkl still holds the
# PRE-BAKE pickle and would otherwise shadow the landed surface). Nothing is staged; nothing is
# written into the worktree.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o29c_probe
OUT=$SP/o29c/probe
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: HEAD -> $(git -C "$WT" rev-parse --short HEAD)"
mkdir -p "$OUT"
echo "  LANDED IDENTITIES IN THE PROBE WORKTREE:"
md5sum "$WT/engine/rl_after/rl_model_data.json" "$WT/engine/rl_after/rl_app_data.json" \
       "$WT/engine/rl_after/pvc_curve_v2.json"  "$WT/engine/rl_after/rl_model.py" \
       "$WT/data/v0surf.pkl" | sed 's/^/    /'

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$HERE"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
export RL_DAY0_FINAL="$REPO/docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json"
python3 "$HERE/o29c_lawprobe.py" 2>&1 | tee "$HERE/LAWPROBE_29C_out.txt"
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
