#!/bin/bash
# ORDER 29C -- PER-ENTRANT COHORT-BOOK EMIT (24-year walk-forward) ON THE LANDED TREE, LANDED-LAW YEAR-0.
#
# Sibling of docs/evidence/landing_29_2026-08-13/emit_variant_o29.sh, carried with ONE difference:
#   * THE EMITTER IS ORDER 29C's DISCLOSED COPY, docs/evidence/landing_29_2026-08-13/noarb29c/
#     emit_matrix_29c.py -- the standing emitter with exactly one declared change (the v0 column is the
#     LANDED ENTRY LAW, not v0_start). ORDER 29's runner copies the STANDING emitter; this one copies the
#     DISCLOSED one, and the standing emitter's md5 is asserted INSIDE the copy at run so the "one
#     declared change" claim is checked rather than stated.
# Everything else -- the detached worktree of HEAD, nothing staged, the declared RL_V0SURF_PKL
# first-precedence override, RL_GRACE deliberately unset, the five-var thread pinning, strictly
# sequential -- is carried verbatim from emit_variant_o29.sh and is not re-argued here.
#
# Usage: emit_variant_o29c.sh <label>
set -uo pipefail
LABEL="${1:-O29CFINAL}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o29c_$LABEL
OUT=$SP/o29c/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
# FULL FIVE-VAR THREAD PINNING. ENGINE RUNS ARE STRICTLY SEQUENTIAL.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: HEAD -> $(git -C "$WT" rev-parse --short HEAD)"
mkdir -p "$OUT"

echo "  LANDED IDENTITIES IN THE EMIT WORKTREE:"
md5sum "$WT/engine/rl_after/rl_model_data.json" "$WT/engine/rl_after/rl_app_data.json" \
       "$WT/engine/rl_after/pvc_curve_v2.json"  "$WT/engine/rl_after/rl_model.py" \
       "$WT/data/v0surf.pkl" | sed 's/^/    /'

cp "$HERE/emit_matrix_29c.py" "$OUT/emit.py"
echo "  emitter pins COMPUTED at run:"
echo "    emit_matrix_29c.py  (ORDER 29C disclosed copy) $(md5sum "$OUT/emit.py" | cut -c1-32)"
echo "    emit_matrix_338.py  (STANDING, must be bffde2f786be85037483e9f5f1563068, asserted in-copy) \
$(md5sum "$WT/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" | cut -c1-32)"

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
# RL_GRACE deliberately unset -- ORDER 29 makes grace-A the CODE DEFAULT and carries it in the pinned
# manifest, so the unset environment IS the landed configuration.
echo "  emit starting $(date -u +%H:%M:%S)"
S=$(date +%s)
python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1
rc=$?; E=$(date +%s)
echo "  emit exit=$rc  COST: $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUT/per_entrant_338_confirmation.json" ]; then
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/per_entrant_$LABEL.json"
  echo "  OK -> per_entrant_$LABEL.json  ($(md5sum "$SP/per_entrant_$LABEL.json" | cut -c1-8))"
  grep -E 'REPLICATION|census|unmappable|ruck_floor|records=|basis' "$OUT/emit.log" || tail -8 "$OUT/emit.log"
else
  echo "  NO MATRIX -- see $OUT/emit.log"; tail -40 "$OUT/emit.log"; fi
cp "$OUT/emit.log" "$HERE/EMIT_${LABEL}_out.txt" 2>/dev/null
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
