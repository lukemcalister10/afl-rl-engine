#!/bin/bash
# ORDER Q — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once).
# NOTHING HERE IS ADOPTED. Every board is a price, not a proposal.
#
#   candQ : every dial off but the base stack        -> must reproduce the landing candidate 1f176444
#   KrefQ : ORDER K's ruled line, RL_O37 UNSET       -> must reproduce ORDER K   f3101883 BYTE-EXACT
#   Qoff  : ORDER P's line, every RL_O38* UNSET      -> must reproduce ORDER P   374d4e44 BYTE-EXACT (Q1)
#   QA    : + RL_O38A=1        FIX A alone
#   QB1   : + RL_O38B1=1       FIX B1 alone
#   QB2   : + RL_O38B2=1       FIX B2 alone
#   QAB1  : + RL_O38A=1 RL_O38B1=1
#   QAB2  : + RL_O38A=1 RL_O38B2=1
#   QAimp : RL_O38A=1 ALONE, every RL_O36_*/RL_O37 unset -> must equal QA BYTE-EXACT (the dial carries
#           the whole stack on its own defaults)
#   *_2   : an identical repeat of each variant       -> the determinism proof (Q2)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/oq}
export RL_SCRATCH="$SP"
# ORDER K'S RULED SETTING — owner comment 5321546243, register v735. NOT a search axis in this order.
K_DOSE=0.40 K_KAPPA=0.20 K_GU=8.0 K_ETA=0.50 K_GD=14.0 K_REL=1.08
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=$K_DOSE RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=$K_KAPPA RL_O36_GAMMA=$K_GU RL_O36_ETA=$K_ETA RL_O36_GAMMA_D=$K_GD RL_O36_LAMBDA=$K_REL"
run () { # run TAG extra-env...
  local T=$1; shift
  echo; echo "--- $T : $* ---"
  env -u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 $KLINE "$@" bash "$HERE/bbQ.sh" "$T"
}
echo "=== ORDER Q BOARD SUITE ==="
echo "  base (ORDER K, unchanged): lambda_S1=$K_DOSE kappa=$K_KAPPA gamma_u=$K_GU eta=$K_ETA gamma_d=$K_GD relief=$K_REL"
echo "  ORDER P: pi *= exp(-LAMBDA*A(g)*T(s_P)) below age 24 — the base for this order"
echo "  ORDER Q: A = monotonise the pedigree leg in entry price · B1 = delete the age gate · B2 = ramp 23-26"
echo; echo "--- candQ (every ORDER I/P/Q dial off; must be 1f176444) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    -u RL_O38A -u RL_O38B1 -u RL_O38B2 \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bbQ.sh" candQ
run KrefQ
run Qoff  RL_O37=1
run QA    RL_O37=1 RL_O38A=1
run QB1   RL_O37=1 RL_O38B1=1
run QB2   RL_O37=1 RL_O38B2=1
run QAB1  RL_O37=1 RL_O38A=1 RL_O38B1=1
run QAB2  RL_O37=1 RL_O38A=1 RL_O38B2=1
echo; echo "--- QAimp (RL_O38A=1 ALONE — the dial must imply the O37/O36-K stack) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    -u RL_O38B1 -u RL_O38B2 \
    RL_O31=1 RL_O32=1 RL_O38A=1 bash "$HERE/bbQ.sh" QAimp
run QA_2   RL_O37=1 RL_O38A=1
run QB1_2  RL_O37=1 RL_O38B1=1
run QB2_2  RL_O37=1 RL_O38B2=1
run QAB1_2 RL_O37=1 RL_O38A=1 RL_O38B1=1
run QAB2_2 RL_O37=1 RL_O38A=1 RL_O38B2=1
echo; echo "=== BOARD MD5s ==="
declare -A M
for t in candQ KrefQ Qoff QA QB1 QB2 QAB1 QAB2 QAimp QA_2 QB1_2 QB2_2 QAB1_2 QAB2_2; do
  M[$t]=$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
  printf '  %-8s %s\n' "$t" "${M[$t]:-MISSING}"
done
echo
echo "  Q4 BASE STACK   = 1f176444 : $([ "${M[candQ]:0:8}" = "1f176444" ] && echo PASS || echo "FAIL — got ${M[candQ]:0:8}")"
echo "  Q5 ORDER K LINE = f3101883 : $([ "${M[KrefQ]:0:8}" = "f3101883" ] && echo PASS || echo "FAIL — got ${M[KrefQ]:0:8}")"
echo "  Q1 ALL O38 OFF  = 374d4e44 : $([ "${M[Qoff]:0:8}" = "374d4e44" ] && echo PASS || echo "FAIL — got ${M[Qoff]:0:8}  (Q1 FIRES)")"
echo "  Q3 DIAL CARRIES THE STACK  : $([ -n "${M[QA]}" ] && [ "${M[QA]}" = "${M[QAimp]}" ] && echo PASS || echo "FAIL ${M[QA]} vs ${M[QAimp]}")"
for v in QA QB1 QB2 QAB1 QAB2; do
  echo "  Q2 DETERMINISM x2 $v $(printf '%-5s' '') : $([ -n "${M[$v]}" ] && [ "${M[$v]}" = "${M[${v}_2]}" ] && echo PASS || echo "FAIL ${M[$v]} vs ${M[${v}_2]}")"
done
echo
echo "=== THE FIVE VARIANT BOARDS ==="
for v in QA QB1 QB2 QAB1 QAB2; do printf '  %-6s %s\n' "$v" "${M[$v]:0:8}"; done
