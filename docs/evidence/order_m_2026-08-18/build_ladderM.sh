#!/bin/bash
# ORDER M — THE TRADE-OFF LADDER, BUILT. STRICTLY SEQUENTIAL.
#
# PREREG_M §6(b): if no legal setting exists at eta = 0, quantify it and show the trade-off curve so
# the owner can choose knowingly. The navigation curve (TRADEOFF_M.json) says what eta each dose needs.
# This suite BUILDS the two ladders that turn that curve into board points on the owner's own rows.
#
# LADDER A — eta walked at ORDER K's RULED DOSE 0.40, everything else held at ORDER K's values.
#            Where does harry-dean cross 2,600? Where do the three G6 rows stop rising?
#   E10 E20 E30 E40   (eta 0.10, 0.20, 0.30, 0.40)   -- E00 is M0, E50 is ORDER K, both already built
#
# LADDER B — THE LEGAL FRONTIER ITSELF: at each dose, the SMALLEST eta that keeps the board inside the
#            owner's +14% rail and the 1.139 no-arb line (from TRADEOFF_M.json Q1).
#   F20 = dose 0.20 eta 0.39 · F60 = dose 0.60 eta 0.64 · F70 = dose 0.70 eta 0.72
#   (dose 0.00 eta 0.31 is MMIN and dose 0.40 eta 0.50 is ORDER K -- both already built)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/om}
run () {  # tag dose eta
  echo; echo "--- $1 (dose $2, eta $3) ---"
  env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$2" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
      RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA="$3" RL_O36_GAMMA_D=14.0 \
      RL_O36_LAMBDA=1.08 bash "$HERE/bbM.sh" "$1"
}
echo "=== ORDER M TRADE-OFF LADDER ==="
run E10 0.40 0.10
run E20 0.40 0.20
run E30 0.40 0.30
run E40 0.40 0.40
run F20 0.20 0.39
run F60 0.60 0.64
run F70 0.70 0.72
echo; echo "=== LADDER BOARD MD5s ==="
for t in E10 E20 E30 E40 F20 F60 F70; do
  printf '  %-4s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
