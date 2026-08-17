#!/bin/bash
# ORDER I — the board suite, STRICTLY SEQUENTIAL (never two engine runs at once), PID-unique staging
# via the tag discipline. Five boards:
#   cand  : RL_O36 UNSET                       -> must reproduce the landing candidate 1f176444 BYTE-EXACT
#   s1    : RL_O36=1, tall factor removed       -> lever 1 alone (the counterweight is pinned, so this is S1)
#   tall  : RL_O36=1, lambda_S1 = 0             -> lever 3 alone
#   full  : RL_O36=1, both                      -> ORDER I
#   full2 : an identical repeat of `full`        -> the determinism proof
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOSE=${O36_DOSE:?set O36_DOSE}
echo "=== ORDER I BOARD SUITE  (lambda_S1 = $DOSE) ==="
echo; echo "--- cand (RL_O36 unset; must be 1f176444) ---"
env -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bb36.sh" cand
echo; echo "--- s1 (lever 1 alone) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$DOSE" RL_O36_TALL=0 bash "$HERE/bb36.sh" s1
echo; echo "--- tall (lever 3 alone) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.0 RL_O36_TALL=1 bash "$HERE/bb36.sh" tall
echo; echo "--- full (ORDER I) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$DOSE" RL_O36_TALL=1 bash "$HERE/bb36.sh" full
echo; echo "--- full2 (determinism repeat) ---"
env -u RL_O35 RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1="$DOSE" RL_O36_TALL=1 bash "$HERE/bb36.sh" full2
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o36
echo; echo "=== BOARD MD5s ==="
for t in cand s1 tall full full2; do
  printf '  %-6s %s\n' "$t" "$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)"
done
A=$(md5sum "$SP/bb_full/rl_after/rl_app_data.json" | cut -c1-32)
B=$(md5sum "$SP/bb_full2/rl_after/rl_app_data.json" | cut -c1-32)
C=$(md5sum "$SP/bb_cand/rl_after/rl_app_data.json" | cut -c1-32)
echo "  DETERMINISM x2 : $([ "$A" = "$B" ] && echo PASS || echo "FAIL $A vs $B")"
echo "  DIAL-OFF = 1f176444 : $([ "${C:0:8}" = "1f176444" ] && echo PASS || echo "FAIL — got ${C:0:8}")"
