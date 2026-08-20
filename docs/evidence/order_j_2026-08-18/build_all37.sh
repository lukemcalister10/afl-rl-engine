#!/bin/bash
# ORDER J — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once), PID-unique staging
# via the tag discipline (one tag, one directory, one run).
#
#   cand  : RL_O36 UNSET                          -> must reproduce the landing candidate 1f176444 BYTE-EXACT
#   tall  : the OWNER-RULED tall/small factor ALONE (lambda_S1 = 0, repair knobs) -- R-TALLFACTOR
#   tall2 : an identical repeat of `tall`           -> the determinism proof
#   ref   : the DISCLOSED SUB-GATE REFERENCE -- the cheapest setting that satisfies the owner's laws.
#           IT FAILS THE PREREGISTERED MATURE-ROW GATE J-TOL AND IS NOT CARRIED. It is built so the
#           owner can read what ~2% of veteran movement buys on the STANDING instruments, not on the
#           calibrator, before he rules.
#   s1    : S1 alone at the reference dose, tall factor removed -> the mechanism leg for the ledger
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
: "${J_DOSE:=0.10}" "${J_KAPPA:=0.240}" "${J_GU:=10.5}" "${J_ETA:=0.425}" "${J_GD:=14.0}" "${J_REL:=1.08}"
echo "=== ORDER J BOARD SUITE ==="
echo "  reference point: lambda_S1=$J_DOSE kappa=$J_KAPPA gamma_u=$J_GU eta=$J_ETA gamma_d=$J_GD relief=$J_REL"
echo "  ruled tall factor: lambda_S1=0, knobs at the repair point"
echo; echo "--- cand (RL_O36 unset; must be 1f176444) ---"
env -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_KAPPA -u RL_O36_GAMMA -u RL_O36_ETA \
    -u RL_O36_GAMMA_D -u RL_O36_LAMBDA \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bb37.sh" cand
echo; echo "--- tall (the owner-ruled factor alone) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 bash "$HERE/bb37.sh" tall
echo; echo "--- tall2 (determinism repeat) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 bash "$HERE/bb37.sh" tall2
echo; echo "--- ref (the disclosed sub-gate reference; NOT CARRIED) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$J_DOSE" RL_O36_TALL=1 \
    RL_O36_KAPPA="$J_KAPPA" RL_O36_GAMMA="$J_GU" RL_O36_ETA="$J_ETA" RL_O36_GAMMA_D="$J_GD" \
    RL_O36_LAMBDA="$J_REL" bash "$HERE/bb37.sh" ref
echo; echo "--- s1 (S1 alone at the reference dose, tall factor removed) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$J_DOSE" RL_O36_TALL=0 bash "$HERE/bb37.sh" s1
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o37
echo; echo "=== BOARD MD5s ==="
for t in cand tall tall2 ref s1; do
  printf '  %-6s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
A=$(md5sum "$SP/bb_tall/rl_after/rl_app_data.json" | cut -c1-32)
B=$(md5sum "$SP/bb_tall2/rl_after/rl_app_data.json" | cut -c1-32)
C=$(md5sum "$SP/bb_cand/rl_after/rl_app_data.json" | cut -c1-32)
echo "  DETERMINISM x2      : $([ "$A" = "$B" ] && echo PASS || echo "FAIL $A vs $B")"
echo "  DIAL-OFF = 1f176444 : $([ "${C:0:8}" = "1f176444" ] && echo PASS || echo "FAIL -- got ${C:0:8}  (F3 FIRES)")"
