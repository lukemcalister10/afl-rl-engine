#!/bin/bash
# Build the board at a given git ref into a named output, for PER-ITEM attribution.
# Usage: build_board_at.sh <ref> <outfile>
# Uses a detached worktree so the branch checkout is never disturbed.
set -uo pipefail
REF="$1"; OUT="$2"
REPO=/home/user/afl-rl-engine
WT=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/wt_$REF
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT"
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" "$REF" >/dev/null 2>&1 || { echo "WORKTREE FAILED for $REF"; exit 1; }

export RL_REPO="$WT"
export RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
cd "$WT/engine/rl_after"
rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
echo "rl_export exit=$? ref=$REF"
if [ -f rl_app_data.json ]; then
  cp rl_app_data.json "$OUT"
  md5sum rl_app_data.json | awk '{print "  board md5:", $1}'
else
  echo "  NO BOARD PRODUCED — see $OUT.log"; tail -5 "$OUT.log"
fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
