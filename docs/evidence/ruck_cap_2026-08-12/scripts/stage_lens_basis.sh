#!/bin/bash
# ORDER 20C — stage_trees.sh (carried from ORDER 20B byte-identical) excludes docs/evidence, which is
# fine for a BOARD build (it loads the frozen v0surf and never fits the lens) but not for the DECLARED
# REFIT lane: _build_v0_curve's #306 branch reads the structural basis artifact as a declared input and
# halts loudly without it. This copies that ONE artifact into the staged trees. Nothing else is added.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
REL=docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json
for T in HEAD FIX; do
  mkdir -p "$SP/tree_$T/$(dirname $REL)"
  cp "$SRC/$REL" "$SP/tree_$T/$REL"
  echo "  staged $T  $(md5sum "$SP/tree_$T/$REL" | cut -c1-32)"
done
