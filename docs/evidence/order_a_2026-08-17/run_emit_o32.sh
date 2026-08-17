#!/bin/bash
# ORDER A / CANDIDATE 32 — the walk-forward per-entrant emit. The ORDER 31-F emitter
# (docs/evidence/candidate_31f/emit_matrix_31f.py, itself the 29C disclosed copy) is BYTE-CARRIED;
# the engine is THIS TREE's wired engine with RL_O32=1 (RL_O31 implied and also exported for the
# emitter's own lane assert); the day-0 replication guard re-points at DAY0_32_FINAL.json — the
# Candidate 32 board's own printed day-0 file (89/89 at tolerance 0, and byte-identical prints to
# fe6be9d6's — A10). Same env, same five-var thread pinning, strictly sequential.
set -uo pipefail
LABEL="O32RFINAL"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
OUT=$SP/o32/emit_$LABEL
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
export RL_DAY0_FINAL="$HERE/DAY0_32_FINAL.json"
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
cp "$OUT/emit.log" "$HERE/EMIT_O32FINAL_out.txt" 2>/dev/null
