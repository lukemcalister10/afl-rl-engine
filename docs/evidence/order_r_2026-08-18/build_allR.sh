#!/bin/bash
# ORDER R — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once).
# NOTHING HERE IS ADOPTED. Every board is a price, not a proposal.
#
# CONTROLS (must reproduce byte-exact, or a falsifier fires):
#   candR : every ORDER I/P/Q/R dial off but the base stack -> 1f176444  (the landing candidate)
#   KrefR : ORDER K's ruled line, RL_O37 UNSET              -> f3101883  (ORDER K)
#   Roff  : ORDER P's line, every RL_O38*/RL_O39_* UNSET    -> 374d4e44  (ORDER P)   R1
#   RB1   : + RL_O38B1=1, R dials unset                     -> 1b1817f3  (ORDER Q FIX B1)  R2
#   RAB1  : + RL_O38A=1 RL_O38B1=1, R dials unset           -> cbbb94d4  (ORDER Q A+B1)    R3
#
# THE GRID. Every variant sits ON TOP OF B1. b0 = ORDER P's point estimate (dial unset).
#   R15    p15 b0     A off      the TMAX lever alone
#   R20    p20 b0     A off      the TMAX lever alone, far end
#   R15A   p15 b0     A ON       the TMAX lever with FIX A
#   R20A   p20 b0     A ON       the TMAX lever with FIX A, far end
#   Rb1    p5  0.111  A off      the BETA lever alone (clears the average SMALL premium slope)
#   Rb2    p5  0.105  A off      the BETA lever alone, near the CI floor
#   R15b1  p15 0.111  A off      both levers, middle
#   R20b2  p20 0.105  A off      both levers, softest
#   R20b2A p20 0.105  A ON       both levers, softest, with FIX A
#
#   RimpA : RL_O39_TMAXPCT=20 RL_O38B1=1 ALONE, every RL_O36_*/RL_O37 unset -> must equal R20 BYTE-EXACT
#   *_2   : an identical repeat of each variant -> the determinism proof (R4)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/or}
export RL_SCRATCH="$SP"
# ORDER K'S RULED SETTING — owner comment 5321546243, register v735. NOT a search axis in this order.
K_DOSE=0.40 K_KAPPA=0.20 K_GU=8.0 K_ETA=0.50 K_GD=14.0 K_REL=1.08
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=$K_DOSE RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=$K_KAPPA RL_O36_GAMMA=$K_GU RL_O36_ETA=$K_ETA RL_O36_GAMMA_D=$K_GD RL_O36_LAMBDA=$K_REL"
run () { # run TAG extra-env...
  local T=$1; shift
  echo; echo "--- $T : $* ---"
  env -u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 \
      -u RL_O39_TMAXPCT -u RL_O39_BETASAT $KLINE "$@" bash "$HERE/bbR.sh" "$T"
}
B1=0.111
B2=0.105
echo "=== ORDER R BOARD SUITE ==="
echo "  base (ORDER K, unchanged): lambda_S1=$K_DOSE kappa=$K_KAPPA gamma_u=$K_GU eta=$K_ETA gamma_d=$K_GD relief=$K_REL"
echo "  ORDER P : pi *= exp(-LAMBDA*A(g)*T(s_P)) · ORDER Q B1 : the age-24 gate deleted (settled, the base here)"
echo "  ORDER R : TMAX at the young cohort's p5 / p15 / p20 of s_P · BETA_sat inside its published 90% CI only"
echo "  BETA_sat values: b0 = ORDER P point estimate (dial unset) · b1 = $B1 · b2 = $B2"
echo; echo "--- candR (every ORDER I/P/Q/R dial off; must be 1f176444) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
    RL_O31=1 RL_O32=1 RL_O35=1 bash "$HERE/bbR.sh" candR
run KrefR
run Roff   RL_O37=1
run RB1    RL_O37=1 RL_O38B1=1
run RAB1   RL_O37=1 RL_O38A=1 RL_O38B1=1
run R15    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run R20    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run R15A   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run R20A   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run Rb1    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=$B1
run Rb2    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=$B2
run R15b1  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15 RL_O39_BETASAT=$B1
run R20b2  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=$B2
run R20b2A RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=$B2
echo; echo "--- RimpA (RL_O38B1 + RL_O39_TMAXPCT=20 ALONE — the dial must imply the O37/O36-K stack) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    -u RL_O38A -u RL_O38B2 -u RL_O39_BETASAT \
    RL_O31=1 RL_O32=1 RL_O38B1=1 RL_O39_TMAXPCT=20 bash "$HERE/bbR.sh" RimpA
for t in R15 R20 R15A R20A Rb1 Rb2 R15b1 R20b2 R20b2A; do :; done
run R15_2    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run R20_2    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run R15A_2   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run R20A_2   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run Rb1_2    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=$B1
run Rb2_2    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=$B2
run R15b1_2  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15 RL_O39_BETASAT=$B1
run R20b2_2  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=$B2
run R20b2A_2 RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=$B2
echo; echo "=== BOARD MD5s ==="
declare -A M
ALL="candR KrefR Roff RB1 RAB1 R15 R20 R15A R20A Rb1 Rb2 R15b1 R20b2 R20b2A RimpA \
R15_2 R20_2 R15A_2 R20A_2 Rb1_2 Rb2_2 R15b1_2 R20b2_2 R20b2A_2"
for t in $ALL; do
  M[$t]=$(md5sum "$SP/bb_$t/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
  printf '  %-9s %s\n' "$t" "${M[$t]:-MISSING}"
done
echo
echo "  BASE STACK      = 1f176444 : $([ "${M[candR]:0:8}" = "1f176444" ] && echo PASS || echo "FAIL — got ${M[candR]:0:8}")"
echo "  ORDER K LINE    = f3101883 : $([ "${M[KrefR]:0:8}" = "f3101883" ] && echo PASS || echo "FAIL — got ${M[KrefR]:0:8}")"
echo "  R1 ALL R/Q OFF  = 374d4e44 : $([ "${M[Roff]:0:8}" = "374d4e44" ] && echo PASS || echo "FAIL — got ${M[Roff]:0:8}  (R1 FIRES)")"
echo "  R2 B1, R OFF    = 1b1817f3 : $([ "${M[RB1]:0:8}" = "1b1817f3" ] && echo PASS || echo "FAIL — got ${M[RB1]:0:8}  (R2 FIRES)")"
echo "  R3 A+B1, R OFF  = cbbb94d4 : $([ "${M[RAB1]:0:8}" = "cbbb94d4" ] && echo PASS || echo "FAIL — got ${M[RAB1]:0:8}  (R3 FIRES)")"
echo "  R8 DIAL CARRIES THE STACK  : $([ -n "${M[R20]}" ] && [ "${M[R20]}" = "${M[RimpA]}" ] && echo PASS || echo "FAIL ${M[R20]} vs ${M[RimpA]}")"
for v in R15 R20 R15A R20A Rb1 Rb2 R15b1 R20b2 R20b2A; do
  printf "  R4 DETERMINISM x2 %-7s : %s\n" "$v" "$([ -n "${M[$v]}" ] && [ "${M[$v]}" = "${M[${v}_2]}" ] && echo PASS || echo "FAIL ${M[$v]} vs ${M[${v}_2]}")"
done
echo
echo "=== THE NINE ORDER R VARIANT BOARDS ==="
for v in R15 R20 R15A R20A Rb1 Rb2 R15b1 R20b2 R20b2A; do printf '  %-7s %s\n' "$v" "${M[$v]:0:8}"; done
