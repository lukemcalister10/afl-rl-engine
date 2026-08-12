#!/bin/bash
# ORDER 23 -- ONE FULL ROUND OF THE ITERATE-TO-TOLERANCE STEP, WITH ALL NINE PATHWAYS REPRICEABLE.
# Carried from docs/evidence/pool_final_2026-08-12/o22_iterate.sh; the only changes are the three
# ORDER 23 scripts (uncapped U re-derivation, uncapped emit stage, uncapped derivation).
#
#   next levels  <- the previous round's measured lambdas (o22_next_levels.py, CARRIED VERBATIM)
#   U re-derived <- at those levels (R carries unchanged; ORDER 21 handback item 4)
#   matrix emitted on the staged engine WITH those levels, that surface, and THE CAP REMOVED
#   derivation re-run on the emitted matrix -> the lambdas this round actually landed on
#
# Usage: o23_iterate.sh <PREV_LABEL> <NEW_LABEL> [PREVPREV_LABEL]
#   a third argument switches on the declared secant acceleration, fitted on the last two rounds.
set -uo pipefail
PREV="$1"; NEW="$2"; PP="${3:-}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
E22="$REPO/docs/evidence/pool_final_2026-08-12"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
IT=$SP/o23/iter
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1
SURF="${O23_SURFACE:-$E22/POOL_RETENTION_SURFACE_FINAL.json}"
export O23_SURFACE="$SURF"
mkdir -p "$IT"
echo "### surface in force: $SURF"

echo "### ROUND $NEW -- next levels from $PREV"
if [ -n "$PP" ]; then
  python3 "$E22/o22_next_levels.py" "$IT/derive_$PREV.json" "$IT/levels_$NEW.json" --accel "$IT/derive_$PP.json" || exit 1
else
  python3 "$E22/o22_next_levels.py" "$IT/derive_$PREV.json" "$IT/levels_$NEW.json" || exit 1
fi
echo "### ROUND $NEW -- U re-derived at those levels"
python3 "$HERE/o23_uderive.py" "$SP/o22/ucells.json" "$IT/levels_$NEW.json" \
        "$SURF" "$IT/surface_$NEW.json" "$NEW" | sed -n '4,22p' || exit 1
echo "### ROUND $NEW -- emit"
O23_SURFACE="$IT/surface_$NEW.json" bash "$HERE/emit_variant_o23.sh" "$NEW" derived \
        "$IT/levels_$NEW.json" RL_H_POOLSIT=1.0 RL_H_UNION=1.0 | tail -5 || exit 1
echo "### ROUND $NEW -- measure"
python3 "$HERE/o23_derive.py" "$SP/per_entrant_O23$NEW.json" "$IT/levels_$NEW.json" \
        "$IT/derive_$NEW.json" "$NEW" > "$IT/derive_$NEW.txt" 2>&1 || { tail -20 "$IT/derive_$NEW.txt"; exit 1; }
sed -n '/THE TARGET, MEASURED FRESH/,/^====/p' "$IT/derive_$NEW.txt" | head -12
sed -n '/pathway      n        w |/,/ALL POOL/p' "$IT/derive_$NEW.txt"
