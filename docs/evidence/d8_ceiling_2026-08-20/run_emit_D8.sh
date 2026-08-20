#!/bin/bash
# ORDER D8 MEASUREMENT — the walk-forward per-entrant emit for THE PRICED CANDIDATE 5ea978f7.
# docs/evidence/final_candidate_2026-08-19/run_emit_CP.sh (md5 33bb5d25a763603c7c12bc98a01910c0), the
# COMPLETED-PASS-THROUGH lineage (run_emit_D6 -> run_emit_CP), carried with THREE declared changes:
#   (1) RL_O33_TAPEROFF ADDED TO THE DIAL PASS-THROUGH. It was absent because it did not exist when
#       that file was written. WITHOUT IT the emit would silently price the OFF board a05fe951 under
#       a candidate label -- exactly the mismatch the pass-through list exists to prevent. This is the
#       same disclosed script change class as run_emit_CP.sh's own RL_O43 addition.
#   (2) the staging re-pointed at this seat's own dir.
#   (3) the label defaults to D8CAND.
# register v767: NEVER run_emit_ASM.sh -- it drops the newer dials.
#
# THE ORDER 31-F REPLICATION GUARD IS NOT WEAKENED AND ITS REFERENCE IS NOT RE-BASED: same two legs,
# tolerance 0, against the FROZEN docs/evidence/final_candidate_2026-08-19/DAY0_CP.json (210510fe5d09)
# -- the current reference, the one the bake ran bare against and read 89 of 89 on. The B-3 taper is
# inert at age<=20 and every day-0 row is an entrant, so if ANY day-0 print moves this emit FAILS
# CLOSED, no matrix is used, and the seat reports which rows moved rather than regenerating a
# reference. THAT IS THE POINT OF POINTING IT HERE.
#
# NOTHING IS ADOPTED. NO BOARD PIN MOVES. NO ENGINE FILE IS EDITED BY THIS SCRIPT.
set -uo pipefail
LABEL=${OP_LABEL:-D8CAND}
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
REPO=${RL_REPO_D8:-$SP/wt-d8n}
OUT=$SP/d8m/emit_$LABEL
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
         RL_O40_RECW RL_O40_CAPFORM RL_O40_CAPPCT RL_O40_LAMBDA RL_O40_PGMAT \
         RL_O41_SDOFF RL_O41_CREDIT RL_O41_CREDITFORM RL_O41_RESET RL_O41_INJ RL_O41_R3 RL_O41_RAMP RL_O41_BREAK RL_O41_UNWIND RL_O42 RL_O43 \
         RL_O33_TAPEROFF; do
  if [ -n "${!V:-}" ]; then export $V; fi
done
export RL_DAY0_FINAL="${RL_DAY0_FINAL:-$REPO/docs/evidence/final_candidate_2026-08-19/DAY0_CP.json}"
echo "  RL_O33_TAPEROFF=${RL_O33_TAPEROFF:-unset}   <-- THE PRICED DIAL. 'unset' here means this emit is the BASE, not the candidate."
echo "  day0 ref: $(basename $RL_DAY0_FINAL) ($(md5sum $RL_DAY0_FINAL | cut -c1-12))  NOT re-based"
echo "  emit starting $(date -u +%H:%M:%S)"
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
cp "$OUT/emit.log" "$SP/d8m/EMIT_${LABEL}_out.txt" 2>/dev/null
exit 0
