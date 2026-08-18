#!/bin/bash
# ORDER K — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once), PID-unique staging
# via the tag discipline (one tag, one directory, one run).
#
#   cand  : RL_O36 UNSET                         -> must reproduce the landing candidate 1f176444 BYTE-EXACT
#   tallJ : the tall/small factor with ORDER J's WIRED FLOOR (RL_O36_FLOORFIX=0) -- the fix's own
#           before-picture, so the floor fix is priced by removal on every row and every band
#   tallK : the tall/small factor with the ORDER K RE-SITED FLOOR, alone   -- the leg for the ledger
#   s1    : S1 alone at the RULED dose 0.40, tall factor removed           -- the leg for the ledger
#   K     : THE OWNER'S RULED SETTING IN FULL (dose 0.40 k 0.20 gu 8 eta 0.50 gd 14 rel 1.08 + the
#           floor-fixed tall/small factor)                                 -- THE DECISION BOARD
#   K2    : an identical repeat of K                                       -- the determinism proof
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/ok}
# THE RULED SETTING -- owner comment 5321546243. NOT a search axis in this order.
K_DOSE=0.40 K_KAPPA=0.20 K_GU=8.0 K_ETA=0.50 K_GD=14.0 K_REL=1.08
echo "=== ORDER K BOARD SUITE ==="
echo "  THE RULED SETTING: lambda_S1=$K_DOSE kappa=$K_KAPPA gamma_u=$K_GU eta=$K_ETA gamma_d=$K_GD relief=$K_REL"
echo "  plus the owner-ruled tall/small sitter factor, with the ORDER K re-sited fade floor"
echo; echo "--- cand (RL_O36 unset; must be 1f176444) ---"
env -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA -u RL_O36_GAMMA \
    -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bbK.sh" cand
echo; echo "--- tallJ (the factor with ORDER J's WIRED floor -- the defect, priced) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=0 \
    bash "$HERE/bbK.sh" tallJ
echo; echo "--- tallK (the factor with the ORDER K RE-SITED floor, alone) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    bash "$HERE/bbK.sh" tallK
echo; echo "--- s1 (S1 alone at the ruled dose 0.40, tall factor removed) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=0 \
    bash "$HERE/bbK.sh" s1
echo; echo "--- K (THE RULED SETTING IN FULL -- the decision board) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbK.sh" K
echo; echo "--- K2 (determinism repeat) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$K_DOSE" RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
    RL_O36_KAPPA="$K_KAPPA" RL_O36_GAMMA="$K_GU" RL_O36_ETA="$K_ETA" RL_O36_GAMMA_D="$K_GD" \
    RL_O36_LAMBDA="$K_REL" bash "$HERE/bbK.sh" K2
echo; echo "=== BOARD MD5s ==="
for t in cand tallJ tallK s1 K K2; do
  printf '  %-6s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
A=$(md5sum "$SP/bb_K/rl_after/rl_app_data.json" | cut -c1-32)
B=$(md5sum "$SP/bb_K2/rl_after/rl_app_data.json" | cut -c1-32)
C=$(md5sum "$SP/bb_cand/rl_after/rl_app_data.json" | cut -c1-32)
echo "  DETERMINISM x2      : $([ -n "$A" ] && [ "$A" = "$B" ] && echo PASS || echo "FAIL $A vs $B  (K7 FIRES)")"
echo "  DIAL-OFF = 1f176444 : $([ "${C:0:8}" = "1f176444" ] && echo PASS || echo "FAIL -- got ${C:0:8}  (K5 FIRES)")"
