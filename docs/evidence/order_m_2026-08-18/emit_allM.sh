#!/bin/bash
# ORDER M — the three walk-forward matrices this order needs, STRICTLY SEQUENTIAL, one at a time.
#   M0ETA0  ORDER K's knobs with ETA := 0            (the owner's ruling applied to his own setting)
#   MLOETA0 the coolest eta=0 point in the grid      (dose 0.00 kappa 0.15 gamma_u 16)
#   MMIN031 the smallest legal eta anywhere          (dose 0.00 eta 0.31)
# ORDER K's own matrix (per_entrant_OKRULED.json), the landing candidate's (O35FINAL) and candidate
# 31's (O31FFINAL) are already on disk from ORDER K and ORDER L and are REUSED, not rebuilt.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "=== ORDER M EMITS (strictly sequential) ==="
echo; echo "--- M0ETA0 (dose .40 k .20 gu 8 ETA 0 gd 14 rel 1.08) ---"
env RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20 \
    RL_O36_GAMMA=8.0 RL_O36_ETA=0.0 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 \
    OM_LABEL=M0ETA0 bash "$HERE/run_emit_M.sh"
echo; echo "--- MLOETA0 (dose 0 k .15 gu 16 ETA 0 gd 14 rel 1.08) ---"
env RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.15 \
    RL_O36_GAMMA=16.0 RL_O36_ETA=0.0 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 \
    OM_LABEL=MLOETA0 bash "$HERE/run_emit_M.sh"
echo; echo "--- MMIN031 (dose 0 k .20 gu 8 ETA 0.31 gd 14 rel 1.08) ---"
env RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20 \
    RL_O36_GAMMA=8.0 RL_O36_ETA=0.31 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 \
    OM_LABEL=MMIN031 bash "$HERE/run_emit_M.sh"
echo; echo "=== MATRICES ==="
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
for L in O31FFINAL O35FINAL OKRULED M0ETA0 MLOETA0 MMIN031; do
  printf '  %-9s %s\n' "$L" "$(md5sum "$SP/per_entrant_$L.json" 2>/dev/null | cut -c1-32)"
done
