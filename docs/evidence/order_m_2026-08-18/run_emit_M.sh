#!/bin/bash
# ORDER M — the walk-forward per-entrant emit. ORDER K's run_emit_K.sh, reused, with the label and the
# knob set passed in from the caller. The ORDER 31-F emitter (docs/evidence/candidate_31f/
# emit_matrix_31f.py, itself the 29C disclosed copy) is BYTE-CARRIED; the engine is THIS TREE's wired
# engine. Same env, same five-var thread pinning, STRICTLY SEQUENTIAL.
#
#   OM_LABEL   the matrix label, e.g. M0ETA0
#   the RL_O36* variables are read from the environment the caller sets.
set -uo pipefail
LABEL=${OM_LABEL:-M0ETA0}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
OUT=$SP/om/emit_$LABEL
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
export RL_O31=1 RL_O32=1 RL_O35=1
for V in RL_O36 RL_O36_LAM_S1 RL_O36_TALL RL_O36_FLOORFIX RL_O36_KAPPA RL_O36_GAMMA RL_O36_ETA \
         RL_O36_GAMMA_D RL_O36_LAMBDA; do
  if [ -n "${!V:-}" ]; then export $V; fi
done
# The day-0 guard is RE-BASED on this board, exactly as ORDER K's was, ORDER J's before it and
# ORDER D's before that. The sitter fade is changed by the ruled tall factor, and a day-0 sitter price
# IS entry value x sitter fade, so the landing candidate's printed file cannot match by construction.
# The RAW ENTRY OBJECT derived_v0 is checked separately and must be bit-identical on all 89 rows.
export RL_DAY0_FINAL="${RL_DAY0_FINAL:-$REPO/docs/evidence/order_k_2026-08-18/DAY0_K.json}"
echo "  emit starting $(date -u +%H:%M:%S)  (lambda_S1=${RL_O36_LAM_S1:-unset} kappa=${RL_O36_KAPPA:-unset} eta=${RL_O36_ETA:-unset})"
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
