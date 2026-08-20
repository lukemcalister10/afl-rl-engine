#!/bin/bash
# ORDER P BUILD — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once).
#
#   candP : every dial off but the base stack   -> must reproduce the landing candidate 1f176444
#   Kref  : ORDER K's EXACT ruled line, RL_O37 UNSET
#                                               -> must reproduce ORDER K f3101883 BYTE-EXACT (B1)
#   P     : Kref + RL_O37=1                     -> THE DECISION BOARD
#   Pimp  : RL_O37=1 ALONE, every RL_O36_* left unset, so the new dial has to carry the O36-K stack
#           on its own defaults                 -> must equal P BYTE-EXACT
#   P2    : an identical repeat of P            -> the determinism proof (B2)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/op}
# ORDER K'S RULED SETTING — owner comment 5321546243, register v735. NOT a search axis in this order.
K_DOSE=0.40 K_KAPPA=0.20 K_GU=8.0 K_ETA=0.50 K_GD=14.0 K_REL=1.08
echo "=== ORDER P BUILD SUITE ==="
echo "  base (ORDER K, unchanged): lambda_S1=$K_DOSE kappa=$K_KAPPA gamma_u=$K_GU eta=$K_ETA gamma_d=$K_GD relief=$K_REL"
echo "  ORDER P: pi *= exp(-LAMBDA*A(g)*T(s_P)) below age 24, LAMBDA 0.1743833 SOLVED, nothing re-tuned"
echo; echo "--- candP (every ORDER I/P dial off; must be 1f176444) ---"
env -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA -u RL_O36_GAMMA \
    -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bbP.sh" candP
echo; echo "--- Kref (ORDER K's ruled line, RL_O37 UNSET; must be f3101883 -- FALSIFIER B1) ---"
env -u RL_O35 -u RL_O37 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 \
    RL_O36_FLOORFIX=1 RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" \
    RL_O36_GAMMA_D="$K_GD" RL_O36_LAMBDA="$K_REL" bash "$HERE/bbP.sh" Kref
echo; echo "--- P (THE DECISION BOARD) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O37=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 \
    RL_O36_FLOORFIX=1 RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" \
    RL_O36_GAMMA_D="$K_GD" RL_O36_LAMBDA="$K_REL" bash "$HERE/bbP.sh" P
echo; echo "--- Pimp (RL_O37=1 ALONE -- the dial must imply the O36-K stack) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA \
    RL_O31=1 RL_O32=1 RL_O37=1 bash "$HERE/bbP.sh" Pimp
echo; echo "--- P2 (determinism repeat) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O37=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 \
    RL_O36_FLOORFIX=1 RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" \
    RL_O36_GAMMA_D="$K_GD" RL_O36_LAMBDA="$K_REL" bash "$HERE/bbP.sh" P2
echo; echo "=== BOARD MD5s ==="
for t in candP Kref P Pimp P2; do
  printf '  %-6s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
C=$(md5sum "$SP/bb_candP/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
R=$(md5sum "$SP/bb_Kref/rl_after/rl_app_data.json"  2>/dev/null | cut -c1-32)
A=$(md5sum "$SP/bb_P/rl_after/rl_app_data.json"     2>/dev/null | cut -c1-32)
I=$(md5sum "$SP/bb_Pimp/rl_after/rl_app_data.json"  2>/dev/null | cut -c1-32)
B=$(md5sum "$SP/bb_P2/rl_after/rl_app_data.json"    2>/dev/null | cut -c1-32)
echo "  BASE STACK = 1f176444    : $([ "${C:0:8}" = "1f176444" ] && echo PASS || echo "FAIL -- got ${C:0:8}")"
echo "  DIAL-OFF   = f3101883 (B1): $([ "${R:0:8}" = "f3101883" ] && echo PASS || echo "FAIL -- got ${R:0:8}  (B1 FIRES)")"
echo "  DIAL IMPLIES THE STACK   : $([ -n "$A" ] && [ "$A" = "$I" ] && echo PASS || echo "FAIL $A vs $I")"
echo "  DETERMINISM x2       (B2): $([ -n "$A" ] && [ "$A" = "$B" ] && echo PASS || echo "FAIL $A vs $B  (B2 FIRES)")"
echo "  ORDER P BOARD            : ${A:0:8}"
