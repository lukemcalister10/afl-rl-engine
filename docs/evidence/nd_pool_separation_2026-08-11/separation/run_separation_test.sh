#!/bin/bash
# ============================================================================================================
# ORDER 20 — THE STANDING SEPARATION GUARD.
#
#   "The ND and pool need to be entirely separated. Nothing here can impact ND pricing."
#
# This is not a one-off check. It is the re-runnable guard for the owner's law: it perturbs the POOL PRICE
# PRIMITIVE (the signed per-division pool levels in pvc_curve_v2.json — the only owner-signed input that sets
# what a pool entrant is worth) by six different amounts including absurd ones, rebuilds the board from a
# scratchpad copy of this checkout each time, and asserts that
#
#     every national-draft price (v / vRaw / vP1 / vP2 / vM1 / vM2),
#     every point of the national pick curve (PVC 1..64 and picks[]),
#     and nd_profile (the calibration target every lambda is measured against)
#
# move by EXACTLY ZERO. Not "below tolerance" — zero. A non-zero residue anywhere is a BLOCKER.
#
# LEG 1 (board)      : ~1 min per perturbation. Run always.
# LEG 2 (nd_profile) : ~2 min per matrix emit. Run with `full` — it needs the per-entrant matrices.
#
# Usage:  run_separation_test.sh [board|full]      (default: board)
# ============================================================================================================
set -uo pipefail
MODE=${1:-board}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIR="$(cd "$HERE/.." && pwd)"
ROOT="$(cd "$DIR/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
RC=0

echo "############ LEG 1 — THE BOARD ############"
bash "$DIR/run_perturbations.sh" x1.5 x0.5 x3.0 tilt rd_only flat100 || RC=1

if [ "$MODE" = "full" ]; then
  echo
  echo "############ LEG 2 — nd_profile ############"
  bash "$DIR/run_emits.sh"
  export RL_REPO="$ROOT"
  python3 "$HERE/nd_profile_test.py" \
      "$SP/o20/per_entrant_BASE.json" \
      "$SP/o20/per_entrant_P_x3.0.json" \
      "$SP/o20/per_entrant_P_flat100.json" || RC=1
fi

echo
if [ $RC -eq 0 ]; then echo "SEPARATION GUARD: PASS — every checked national quantity moved by EXACTLY ZERO."
else echo "SEPARATION GUARD: FAIL — a national quantity moved under a pool-only change. THIS IS A BLOCKER."; fi
exit $RC
