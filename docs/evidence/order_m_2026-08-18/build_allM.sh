#!/bin/bash
# ORDER M — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once), PID-unique staging
# via the tag discipline (one tag, one directory, one run).
#
#   cand : RL_O36 UNSET                     -> must reproduce the landing candidate 1f176444 BYTE-EXACT
#   K    : ORDER K's RULED SETTING           -> must reproduce f3101883 BYTE-EXACT (reproducibility)
#   s1   : the AGE BAR ALONE at dose 0.40, counterweight at the repair values, tall factor removed
#          -> S1's zero-tolerance mature law is read here, exactly as ORDER K read it
#   M0   : THE OWNER'S RULING APPLIED TO HIS OWN SETTING -- ORDER K's knobs with ETA SET TO ZERO
#   M0R  : an identical repeat of M0                                  -- the determinism proof
#   MLO  : the COOLEST point in the whole eta=0 grid (dose 0.00, kappa 0.15, gamma_u 16) -- the proof
#          that the breach is not a dose artefact: with the age bar switched off entirely and the
#          counterweight at its gentlest legal setting, the board is STILL outside the owner's rails
#   MMIN : the SMALLEST LEGAL ETA ANYWHERE (dose 0.00, eta 0.31) -- the least blind charge that keeps
#          the board inside the owner's own +14% rail, offered so the owner can choose knowingly
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/om}
K_DOSE=0.40 K_KAPPA=0.20 K_GU=8.0 K_ETA=0.50 K_GD=14.0 K_REL=1.08
echo "=== ORDER M BOARD SUITE ==="
echo "  ORDER K's ruled setting: dose $K_DOSE kappa $K_KAPPA gamma_u $K_GU eta $K_ETA gamma_d $K_GD rel $K_REL"
echo "  ORDER M applies the owner's ruling: ETA := 0"
echo; echo "--- cand (RL_O36 unset; must be 1f176444) ---"
env -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA -u RL_O36_GAMMA \
    -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bbM.sh" cand
echo; echo "--- K (ORDER K's ruled setting; must be f3101883) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbM.sh" K
echo; echo "--- s1 (the age bar alone at dose 0.40, tall factor removed) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=0 \
    bash "$HERE/bbM.sh" s1
echo; echo "--- M0 (ORDER K's knobs with ETA := 0) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA=0.0 RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbM.sh" M0
echo; echo "--- M0R (determinism repeat of M0) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA=0.0 RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbM.sh" M0R
echo; echo "--- MLO (the coolest eta=0 point in the grid: dose 0.00 kappa 0.15 gamma_u 16) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA=0.15 RL_O36_GAMMA=16.0 RL_O36_ETA=0.0 RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbM.sh" MLO
echo; echo "--- MMIN (the smallest legal eta anywhere: dose 0.00 kappa 0.20 gamma_u 8 eta 0.31) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA=0.31 RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbM.sh" MMIN
echo; echo "=== BOARD MD5s ==="
for t in cand K s1 M0 M0R MLO MMIN; do
  printf '  %-6s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
C=$(md5sum "$SP/bb_cand/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
KK=$(md5sum "$SP/bb_K/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
A=$(md5sum "$SP/bb_M0/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
B=$(md5sum "$SP/bb_M0R/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
echo "  M1 DIAL-OFF = 1f176444    : $([ "${C:0:8}" = "1f176444" ] && echo PASS || echo "FAIL -- got ${C:0:8}  (M1 FIRES)")"
echo "  M2 ORDER K = f3101883     : $([ "${KK:0:8}" = "f3101883" ] && echo PASS || echo "FAIL -- got ${KK:0:8}  (M2 FIRES)")"
echo "  M3 DETERMINISM x2         : $([ -n "$A" ] && [ "$A" = "$B" ] && echo PASS || echo "FAIL $A vs $B  (M3 FIRES)")"
