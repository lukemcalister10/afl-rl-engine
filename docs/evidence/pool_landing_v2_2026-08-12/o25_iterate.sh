#!/bin/bash
# ORDER 25 -- ONE FULL ROUND OF THE ITERATE-TO-TOLERANCE STEP, ON THE LANDED DELIVERY.
# Carried from docs/evidence/pool_landing_2026-08-12/o23_iterate.sh; the loop's SHAPE is identical
# and the order of the four steps is identical. What differs is only which scripts do them:
#
#   next levels  <- the previous round's measured lambdas   (o22_next_levels.py, CARRIED VERBATIM,
#                                                            including the secant acceleration)
#   U re-derived <- AT THOSE LEVELS, under the AMENDED PARS (o25_uderive.py). R carries unchanged.
#                   This is ORDER 22/23's convention matched exactly: the entry anchor IS the level,
#                   so the mean-preservation instrument must be re-weighted every round.
#   matrix emitted on the staged engine WITH those levels and that surface (emit_variant_o25.sh)
#   derivation re-run on the emitted matrix -> the lambdas this round actually landed on
#
# Usage: o25_iterate.sh <PREV_LABEL> <NEW_LABEL> [PREVPREV_LABEL]
#   a third argument switches on the declared secant acceleration, fitted on the last two rounds.
set -uo pipefail
PREV="$1"; NEW="$2"; PP="${3:-}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
E22="$REPO/docs/evidence/pool_final_2026-08-12"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
IT=$SP/o25/iter
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1
mkdir -p "$IT"

echo "### ROUND $NEW -- next levels from $PREV"
if [ -n "$PP" ]; then
  python3 "$E22/o22_next_levels.py" "$IT/derive_$PREV.json" "$IT/levels_$NEW.json" --accel "$IT/derive_$PP.json" || exit 1
else
  python3 "$E22/o22_next_levels.py" "$IT/derive_$PREV.json" "$IT/levels_$NEW.json" || exit 1
fi
echo "### ROUND $NEW -- U re-derived at those levels, under the AMENDED pars"
python3 "$HERE/o25_uderive.py" "$SP/o25/ucells.json" "$SP/o25/par_v2.json" "$IT/levels_$NEW.json" \
        "$REPO/docs/evidence/pool_quality_2026-08-12/SURFACE_psi.json" "$IT/surface_$NEW.json" "$NEW" \
        | sed -n '6,22p' || exit 1
echo "### ROUND $NEW -- emit"
bash "$HERE/emit_variant_o25.sh" "$NEW" "$IT/surface_$NEW.json" "$IT/levels_$NEW.json" | tail -4 || exit 1
echo "### ROUND $NEW -- measure"
python3 "$HERE/o25_derive.py" "$SP/per_entrant_O25$NEW.json" "$IT/levels_$NEW.json" \
        "$IT/derive_$NEW.json" "$NEW" > "$IT/derive_$NEW.txt" 2>&1 || { tail -20 "$IT/derive_$NEW.txt"; exit 1; }
sed -n '/THE TARGET, MEASURED FRESH/,/^====/p' "$IT/derive_$NEW.txt" | head -8
sed -n '/pathway      n        w |/,/ALL POOL/p' "$IT/derive_$NEW.txt"
