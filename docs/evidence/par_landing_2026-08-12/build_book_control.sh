#!/bin/bash
# ORDER 20C — BOOK CONTROL. Build the book on an origin/main tree and check it reproduces main's own
# committed s4_matrix.json (6f356d827b4bfa60a9a19fe2add04484). If it does, the builder is deterministic
# here and my re-sealed book differs from main's ONLY because the board moved.
set -uo pipefail
SRC=/home/user/afl-rl-engine/.claude/worktrees/agent-a6af0d68789879235
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/o20c_booktree_ctrl
OUTDIR=$SP/o20c/book_ctrl
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

mkdir -p "$OUTDIR"
rm -rf "$WT"; mkdir -p "$WT"
# the tree exactly as origin/main has it
git -C "$SRC" archive origin/main | tar -C "$WT" -xf -
# the untracked-but-needed bits the checkout carries (vendor etc.) come from the worktree
for d in vendor; do
  [ -d "$SRC/$d" ] && [ ! -d "$WT/$d" ] && cp -a "$SRC/$d" "$WT/$d"
done

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
cd "$WT/engine/rl_after"
python3 s4_matrix_M1v7.py > "$OUTDIR/book_build.log" 2>&1
rc=$?
if [ -f s4_matrix.json ]; then
  cp s4_matrix.json "$OUTDIR/s4_matrix.json"
  echo "  CONTROL BOOK  $(md5sum s4_matrix.json | cut -c1-32)"
  echo "  main's committed book  $(git -C "$SRC" show origin/main:engine/rl_after/s4_matrix.json | md5sum | cut -c1-32)"
else
  echo "  CONTROL BOOK FAILED (exit $rc)"; tail -25 "$OUTDIR/book_build.log"; exit 1
fi
