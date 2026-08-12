#!/bin/bash
# ORDER 20B — stage the two engines into SCRATCHPAD COPIES. The checkout is NEVER edited.
#
#   $SP/tree_HEAD   this worktree as-is (== origin/main content)
#   $SP/tree_FIX    the same tree + ORDER 20's two changed files, taken from the branch
#                   build/nd-pool-separation by `git show` (no checkout, no worktree add)
#
# Usage: bash stage_trees.sh          (idempotent; re-stages both trees from scratch)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../../.." && pwd)"              # the worktree root
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
FIXREF=${FIXREF:-build/nd-pool-separation}

for T in HEAD FIX; do
  WT=$SP/tree_$T
  rm -rf "$WT"; mkdir -p "$WT"
  tar -C "$SRC" --exclude=.git --exclude=docs/evidence -cf - . 2>/dev/null | tar -C "$WT" -xf -
done

# the fix: ORDER 20's two files, byte-for-byte off its branch
for f in engine/forward_valuation/par_build.py engine/forward_valuation/par_redesign.py; do
  git -C "$SRC" show "$FIXREF:$f" > "$SP/tree_FIX/$f" || exit 1
done

echo "STAGED"
echo "  HEAD par_build.py   $(md5sum $SP/tree_HEAD/engine/forward_valuation/par_build.py | cut -c1-32)"
echo "  FIX  par_build.py   $(md5sum $SP/tree_FIX/engine/forward_valuation/par_build.py  | cut -c1-32)"
echo "  HEAD par_redesign   $(md5sum $SP/tree_HEAD/engine/forward_valuation/par_redesign.py | cut -c1-32)"
echo "  FIX  par_redesign   $(md5sum $SP/tree_FIX/engine/forward_valuation/par_redesign.py  | cut -c1-32)"
echo "  trees differ ONLY in those two files:"
diff -rq "$SP/tree_HEAD" "$SP/tree_FIX" 2>/dev/null | sed 's/^/    /'
