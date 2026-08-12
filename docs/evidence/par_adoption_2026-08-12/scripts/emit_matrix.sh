#!/bin/bash
# ORDER 20B — per-entrant matrix emit from a STAGED tree (tree_HEAD / tree_FIX).
#
# Sibling of ORDER 20's emit_matrix_o20.sh. Same deliberate property: it never runs `git worktree add`
# against the primary checkout and never writes the checkout. It runs the PINNED emitter
# docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py (md5-checked below) against the staged tree.
#
# Usage: bash emit_matrix.sh <HEAD|FIX> <out.json>
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
T="$1"; OUTF="$2"; WT=$SP/tree_$T; OUTD=$SP/emit_$T
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$OUTD"; mkdir -p "$OUTD"
cp "$SRC/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUTD/emit.py"
echo "  emitter md5 $(md5sum "$OUTD/emit.py" | cut -c1-32)  (pinned emit_matrix_338.py)"
# the emitter reads the board + the lens basis out of docs/evidence, which the tree copies exclude
mkdir -p "$WT/docs/evidence"
for d in noarb_338_2026-08-06 composition_2026-08-10 exec_306_zlaarm; do
  [ -e "$WT/docs/evidence/$d" ] || cp -a "$SRC/docs/evidence/$d" "$WT/docs/evidence/$d"
done

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUTD"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
S=$(date +%s); python3 "$OUTD/emit.py" > "$OUTD/emit.log" 2>&1; rc=$?; E=$(date +%s)
echo "  emit($T) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUTD/per_entrant_338_confirmation.json" ]; then
  mv "$OUTD/per_entrant_338_confirmation.json" "$OUTF"
  echo "  OK -> $OUTF  ($(md5sum "$OUTF" | cut -c1-8))"
  grep -E "exec OK|boundary crossers|band reading differs" "$OUTD/emit.log" || true
else
  echo "  NO MATRIX — tail of log:"; tail -15 "$OUTD/emit.log"; exit 1
fi
