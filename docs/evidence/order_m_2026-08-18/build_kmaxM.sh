#!/bin/bash
# ORDER M — THE KAPPA-CANNOT-CHARGE-THEM TEST, BUILT RATHER THAN ARGUED.
#
# PACKET_M §4 claims that kappa alone cannot hold the three sub-expectation rows down once eta is
# gone. A claim like that has to be measured at the STRONGEST kappa the ruled constraints allow, not
# at a convenient one. rho32 monotonicity is what caps kappa, and the highest monotone value on the
# declared grid is kappa 0.60 at gamma_u 16 (SWEEP_M.json; at gamma_u 8 it caps at 0.40).
#
#   KMAX  dose 0.00 · kappa 0.60 · gamma_u 16 · eta 0 · gamma_d 14 · lambda_rel 1.08
#         the age bar OFF, eta OFF, kappa as hard as the ruled constraints permit.
#   KMX4  dose 0.40 · kappa 0.60 · gamma_u 16 · eta 0 · gamma_d 14 · lambda_rel 1.08
#         the same, at the RULED dose, so the claim is tested with the age bar on as well.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/om}
run () {  # tag dose
  echo; echo "--- $1 (dose $2, kappa 0.60, gamma_u 16, eta 0) ---"
  env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$2" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
      RL_O36_KAPPA=0.60 RL_O36_GAMMA=16.0 RL_O36_ETA=0.0 RL_O36_GAMMA_D=14.0 \
      RL_O36_LAMBDA=1.08 bash "$HERE/bbM.sh" "$1"
}
echo "=== ORDER M — THE MAXIMUM-KAPPA TEST ==="
run KMAX 0.0
run KMX4 0.40
echo; echo "=== MD5s ==="
for t in KMAX KMX4; do
  printf '  %-5s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
