#!/bin/bash
# ORDER 25 (carried verbatim from ORDER 20C) — RE-SEAL THE BOOK (s4_matrix.json) against the LANDED board, in a SCRATCHPAD COPY.
#
# Sibling of ORDER 20B's build_board_o20b.sh, same discipline: the checkout is NEVER written to. The
# tree is copied with `cp`/tar, the identity restamp runs in the COPY so the guards stay armed, and
# the book builder (engine/rl_after/s4_matrix_M1v7.py) runs there. Only the resulting s4_matrix.json
# and its .srcmd5 are copied back out, to $OUTDIR — never straight into the checkout.
#
# Usage: build_book.sh <OUTDIR>
set -uo pipefail
OUTDIR="$1"
SRC=/home/user/afl-rl-engine/.claude/worktrees/agent-ae867318eb00a513e
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/o25_booktree
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

mkdir -p "$OUTDIR"
rm -rf "$WT"; mkdir -p "$WT"
tar -C "$SRC" --exclude=.git --exclude=docs/evidence -cf - . 2>/dev/null | tar -C "$WT" -xf -

# The landed tree's pins are ALREADY correct (this branch restamped them), so unlike the board build
# there is nothing to restamp — assert that instead, so a drifted pin cannot pass silently.
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
python3 "/home/user/afl-rl-engine/.claude/worktrees/agent-ae867318eb00a513e/docs/evidence/pool_landing_v2_2026-08-12/o25_assert_pins_in_copy.py" "$WT" || { echo "PIN ASSERT FAILED"; exit 1; }

cd "$WT/engine/rl_after"
python3 s4_matrix_M1v7.py > "$OUTDIR/book_build.log" 2>&1
rc=$?
if [ -f s4_matrix.json ]; then
  cp s4_matrix.json "$OUTDIR/s4_matrix.json"
  [ -f s4_matrix.json.srcmd5 ] && cp s4_matrix.json.srcmd5 "$OUTDIR/s4_matrix.json.srcmd5"
  echo "  BOOK OK  $(md5sum s4_matrix.json | cut -c1-32)"
else
  echo "  BOOK FAILED (exit $rc) — see $OUTDIR/book_build.log"; tail -25 "$OUTDIR/book_build.log"; exit 1
fi
