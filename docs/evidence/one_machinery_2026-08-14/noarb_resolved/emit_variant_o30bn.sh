#!/bin/bash
# ORDER 30B-N -- PER-ENTRANT COHORT-BOOK EMIT (24-year walk-forward) UNDER THE RESOLVED CANDIDATE.
#
# Sibling of docs/evidence/landing_29_2026-08-13/noarb29c/emit_variant_o29c.sh, carried with exactly
# ONE difference: RL_O30B_RESOLVED=1 is exported, so ev() is the RESOLVED LAW at every as-of year.
#
#   * THE EMITTER IS ORDER 29C's DISCLOSED COPY, emit_matrix_29c.py, BYTE-UNMODIFIED. Its md5 is
#     computed at run and printed. ORDER 30B-N changes NOTHING inside it. In particular the YEAR-0
#     COLUMN IS UNTOUCHED: it stays the LANDED ENTRY LAW, which is the basis the ORDER 29C reading and
#     the 2026-08-13 sitter-law preview both used, so the three columns of the owner's table are on a
#     COMMON DENOMINATOR. That is the whole reason year-0 is not re-based here.
#   * The year-0 column is dial-INDEPENDENT by construction: _landed_v0_board() reads the artifact's
#     nd_v0.posv and MA.pool_v0_of, neither of which the resolved dial touches. The emitter's own
#     fail-closed 89-of-89 replication proof against DAY0_29B_FINAL.json re-checks that AT RUN.
#
# Everything else -- the detached worktree of HEAD, nothing staged, the declared RL_V0SURF_PKL
# first-precedence override, RL_GRACE deliberately unset, the five-var thread pinning, strictly
# sequential -- is carried verbatim and is not re-argued here.
#
# Usage: emit_variant_o30bn.sh <label>
set -uo pipefail
LABEL="${1:-O30BNRES}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
EMITTER="$REPO/docs/evidence/landing_29_2026-08-13/noarb29c/emit_matrix_29c.py"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o30bn_$LABEL
OUT=$SP/o30bn/emit_$LABEL
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

cp "$EMITTER" "$OUT/emit.py"
echo "  emitter pins COMPUTED at run (ORDER 29C's disclosed copy, BYTE-UNMODIFIED by 30B-N):"
echo "    emit_matrix_29c.py  $(md5sum "$OUT/emit.py" | cut -c1-32)"
echo "    emit_matrix_338.py  (STANDING, must be bffde2f786be85037483e9f5f1563068, asserted in-copy) \
$(md5sum "$WT/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" | cut -c1-32)"

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
# ---- THE ONE DIFFERENCE FROM emit_variant_o29c.sh -------------------------------------------------
export RL_O30B_RESOLVED=1
echo "  DIAL: RL_O30B_RESOLVED=1 (implies RL_O30B_PREVIEW=1). NOTHING IS GREENLIT; PRE-NUMERAIRE."
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
