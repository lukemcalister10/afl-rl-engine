#!/bin/bash
# ORDER S — the walk-forward per-entrant emit. ORDER R's file with the five RL_O40_* dials added
# to the pass-through list and the staging re-pointed.
# ORIGINAL ORDER R HEADER FOLLOWS.
# ORDER R — the walk-forward per-entrant emit. ORDER K's run_emit_K.sh with RL_O37 passed
# through and the label and staging re-pointed. The ORDER 31-F emitter
# (docs/evidence/candidate_31f/emit_matrix_31f.py) is BYTE-CARRIED; the engine is THIS TREE's engine.
# Same env, same five-var thread pinning, strictly sequential.
#
# THE DAY-0 GUARD IS NOT RE-BASED. It is pointed at ORDER K's OWN DAY0_K.json on purpose, because
# ORDER P changes NOTHING about entry prices or the sitter fade: A(0) = 0 exactly, so a row with no
# games cannot move. Pointing the replication proof at ORDER K's file therefore MAKES IT FALSIFIER B3
# — if any of the 89 printed day-0 prices moves, this emit FAILS CLOSED rather than quietly
# regenerating a new reference. ORDER D and ORDER K both had to regenerate, because both changed the
# fade; this order does not, so it must not.
set -uo pipefail
LABEL=${OP_LABEL:-SC20}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
OUT=$SP/os/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
rm -rf "$OUT"; mkdir -p "$OUT"
cp "$REPO/docs/evidence/candidate_31f/emit_matrix_31f.py" "$OUT/emit.py"
echo "  emitter (ORDER 31-F disclosed copy, byte-carried): $(md5sum "$OUT/emit.py" | cut -c1-32)"
echo "  engine: $(md5sum "$REPO/engine/rl_after/_merged_recover.py" | cut -c1-32)"
export RL_REPO="$REPO" RL_FV="$REPO/engine/forward_valuation"
export RL_WORKDIR="$REPO/engine/rl_after" RL_VENDOR="$REPO/vendor" RL_OUT="$OUT"
export PYTHONPATH="$REPO/engine/rl_after:$REPO:$REPO/vendor"
export RL_V0SURF_PKL="$REPO/data/v0surf.pkl"
export RL_O31=1 RL_O32=1
for V in RL_O35 RL_O36 RL_O37 RL_O38A RL_O38B1 RL_O38B2 RL_O39_TMAXPCT RL_O39_BETASAT RL_O36_LAM_S1 RL_O36_TALL RL_O36_FLOORFIX RL_O36_KAPPA RL_O36_GAMMA \
         RL_O36_ETA RL_O36_GAMMA_D RL_O36_LAMBDA \
         RL_O40_RECW RL_O40_CAPFORM RL_O40_CAPPCT RL_O40_LAMBDA RL_O40_PGMAT; do
  if [ -n "${!V:-}" ]; then export $V; fi
done
export RL_DAY0_FINAL="${RL_DAY0_FINAL:-$REPO/docs/evidence/order_k_2026-08-18/DAY0_K.json}"
echo "  emit starting $(date -u +%H:%M:%S)  (RL_O37=${RL_O37:-unset} A=${RL_O38A:-unset} B1=${RL_O38B1:-unset} pct=${RL_O39_TMAXPCT:-unset} w=${RL_O40_RECW:-unset} cap=${RL_O40_CAPFORM:-unset}${RL_O40_CAPPCT:-} lam=${RL_O40_LAMBDA:-unset} pgm=${RL_O40_PGMAT:-unset})"
S=$(date +%s)
python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1
rc=$?; E=$(date +%s)
echo "  emit exit=$rc  COST: $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUT/per_entrant_338_confirmation.json" ]; then
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/per_entrant_$LABEL.json"
  echo "  OK -> per_entrant_$LABEL.json  ($(md5sum "$SP/per_entrant_$LABEL.json" | cut -c1-8))"
  grep -E 'REPLICATION|records=' "$OUT/emit.log"
else
  echo "  NO MATRIX -- see $OUT/emit.log"; tail -40 "$OUT/emit.log"; fi
cp "$OUT/emit.log" "$HERE/EMIT_${LABEL}_out.txt" 2>/dev/null
exit 0
