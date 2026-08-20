#!/bin/bash
# ORDER 33 W1 -- COUNTERFACTUAL EMIT: the ORDER 31-F per-entrant emit, run whole, with EXACTLY ONE
# declared substitution in the scratch worktree's ENGINE COPY: the O31_BETA tuple is replaced by the
# PREREG_W1.md s4 proposed curve. The repo tree is NEVER touched (read-only seat); the worktree is
# detached, patched, used, destroyed. Everything else is carried verbatim from
# docs/evidence/candidate_31f/emit_variant_o31f.sh (same emitter, same env, same thread pinning,
# same RL_O31=1 lane assert, same DAY0 replication guard -- day-0 rows have g=0, so the guard MUST
# still pass under the new deep curve; a failure means the substitution touched something it must
# not, and the run is discarded).
set -uo pipefail
LABEL="W1CF"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o33w1_$LABEL
OUT=$SP/o33w1/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: HEAD -> $(git -C "$WT" rev-parse --short HEAD)"
mkdir -p "$OUT"

echo "  engine BEFORE substitution: $(md5sum "$WT/engine/rl_after/_merged_recover.py" | cut -c1-32) (must be 71d9949ae6592decf462c8f2fc3dff48, the O31FFINAL emit engine)"

# ---- THE ONE DECLARED SUBSTITUTION (worktree copy only) -----------------------------------------
python3 - "$WT/engine/rl_after/_merged_recover.py" <<'PYEOF'
import sys, hashlib
p = sys.argv[1]
src = open(p).read()
OLD = ("    O31_BETA=((2.5,0.2878886216033701),(10.5,0.2878886216033701),(25.5,0.21772876584106796),\n"
       "              (53.0,0.14155152291809878),(85.5,0.023849021706229417))")
NEW = ("    O31_BETA=((2.5,0.2878886216033701),(10.5,0.2878886216033701),(25.5,0.21772876584106796),\n"
       "              (53.0,0.21772876584106796),(85.5,0.015157500325177839))  # ORDER 33 W1 COUNTERFACTUAL (PREREG_W1.md s4)")
assert hashlib.md5(src.encode()).hexdigest() == '71d9949ae6592decf462c8f2fc3dff48', 'engine moved'
assert src.count(OLD) == 1, 'O31_BETA site not unique/found'
open(p, 'w').write(src.replace(OLD, NEW))
print("  O31_BETA SUBSTITUTED: (53.0 -> 0.21772876584106796, 85.5 -> 0.015157500325177839); shallow knots and every other constant UNTOUCHED")
PYEOF
echo "  engine AFTER  substitution: $(md5sum "$WT/engine/rl_after/_merged_recover.py" | cut -c1-32)"

cp "$WT/docs/evidence/candidate_31f/emit_matrix_31f.py" "$OUT/emit.py"
echo "  emitter (ORDER 31-F disclosed copy, byte-carried): $(md5sum "$OUT/emit.py" | cut -c1-32)"

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$WT/data/v0surf.pkl"
export RL_O31=1
export RL_DAY0_FINAL="$WT/docs/evidence/candidate_31f/DAY0_31F_FINAL.json"
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
cp "$OUT/emit.log" "$HERE/EMIT_W1CF_out.txt" 2>/dev/null
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
