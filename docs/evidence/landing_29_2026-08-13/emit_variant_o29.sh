#!/bin/bash
# ORDER 29 -- PER-ENTRANT COHORT-BOOK EMIT (24-year walk-forward) ON THE LANDED TREE.
#
# Sibling of docs/evidence/pool_landing_v2_2026-08-12/emit_variant_o25.sh. TWO differences, both
# because the ORDER 29 landing is ALREADY COMMITTED to this branch:
#   * NOTHING IS STAGED. ORDER 25 had to inject a candidate surface/levels into a detached worktree
#     because its candidate was not yet source. Here the ruled curve, the re-baked v0 surface, the
#     re-sealed book and the numeraire re-pin are all committed at HEAD, so the emit runs against a
#     plain detached worktree of HEAD and nothing is written into it.
#   * RL_V0SURF_PKL is exported. /home/claude/v0surf.pkl (a bootstrap-seeded workspace cache) SHADOWS
#     <repo>/data/v0surf.pkl in _load_v0surf's own precedence and still holds the PRE-BAKE pickle
#     fbc5b393. Without the declared first-precedence override the emit would read the stale surface.
#     The shared copy is NOT overwritten (SHIPPING_PACKET_29 section 3.3). RL_V0SURF_PKL is not in the
#     release contract's must_be_unset -- only RL_V0SURF_REFIT is, and it is not set here.
#
# The emitter itself -- docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py -- is COPIED, never
# modified. Its md5 is computed and printed at run.
#
# Usage: emit_variant_o29.sh <label>
set -uo pipefail
LABEL="${1:-O29FINAL}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o29e_$LABEL
OUT=$SP/o29/emit_$LABEL
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

cp "$REPO/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUT/emit.py"
echo "  emitter pin COMPUTED at run: emit_matrix_338.py $(md5sum "$OUT/emit.py" | cut -c1-32)"

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
# RL_GRACE is DELIBERATELY NOT SET: ORDER 29 makes grace-A the CODE DEFAULT ('1') and carries it in
# the pinned manifest data/model_config.json, so the unset environment is the landed configuration.
echo "  emit starting $(date -u +%H:%M:%S)"
S=$(date +%s)
python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1
rc=$?; E=$(date +%s)
echo "  emit exit=$rc  COST: $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUT/per_entrant_338_confirmation.json" ]; then
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/per_entrant_$LABEL.json"
  echo "  OK -> per_entrant_$LABEL.json  ($(md5sum "$SP/per_entrant_$LABEL.json" | cut -c1-8))"
  tail -8 "$OUT/emit.log"
else
  echo "  NO MATRIX -- see $OUT/emit.log"; tail -30 "$OUT/emit.log"; fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
