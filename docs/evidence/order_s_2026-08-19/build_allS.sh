#!/bin/bash
# ORDER S — the board suite. STRICTLY SEQUENTIAL (never two engine runs at once).
# NOTHING HERE IS ADOPTED. Every board is a price, not a proposal.
#
# CONTROLS (must reproduce byte-exact, or a falsifier fires):
#   SRoff : ORDER P's line, every RL_O38*/RL_O39_*/RL_O40_* UNSET -> 374d4e44 (ORDER P)   S-F0
#   SB1   : + RL_O38B1=1                                          -> 1b1817f3 (ORDER Q FIX B1)
#   SAB1  : + RL_O38A=1 RL_O38B1=1                                -> cbbb94d4 (ORDER Q A+B1)
#   SR20A : + RL_O39_TMAXPCT=20 with A+B1                         -> 7f88f509 (ORDER R R20A)
#           — the ORDER S edits must not disturb ORDER R's own boards either.
#
# THE VARIANTS. Every one sits ON TOP OF FIX B1, exactly as ORDER R's did.
#   SW47  / SW28  / SW47A   S1 RECENCY. w = 0.47 (the DIRECT out-of-sample optimum) and 0.28 (the
#                           CALIBRATED one). Both are THIS ORDER's own walk-forward numbers.
#   SC15  / SC20  / SC20A   S2 THE OWNER'S COMPRESSION, anchored at p15 and p20.
#   SL56  / SL10            S3 THE LEVEL. 0.56 is the STIFFEST level the W2 class floor 1.03 admits;
#                           0.10 is the softening direction. NEITHER IS A PROPOSAL — the frontier
#                           HALTS and these two boards are its endpoints, built so the offline
#                           frontier can be checked against real boards.
#   SM    / SMA             S5 THE MATURE PREMIUM at 24+.
#   SALL                    all four together with FIX A — the far corner of the grid, NOT a
#                           recommendation.
#
#   SimpA : RL_O38B1 + RL_O40_CAPFORM/CAPPCT ALONE -> must equal SC20 BYTE-EXACT (the dial implies
#           the whole O37/O36/O35/O32/O31 stack, and nowhere else)
#   *_2   : an identical repeat of each variant -> the determinism proof
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/os}
export RL_SCRATCH="$SP"
# ORDER K'S RULED SETTING — owner comment 5321546243, register v735. NOT a search axis in this order.
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT"
run () { # run TAG extra-env...
  local T=$1; shift
  echo; echo "--- $T : $* ---"
  env $CLEAR $KLINE "$@" bash "$HERE/bbS.sh" "$T"
}
W1=0.47
W2=0.28
LSTIFF=0.56
LSOFT=0.10
echo "=== ORDER S BOARD SUITE ==="
echo "  engine: $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  ORDER S dials: RL_O40_RECW · RL_O40_CAPFORM+RL_O40_CAPPCT · RL_O40_LAMBDA · RL_O40_PGMAT"
echo "  recency w priced: $W1 (direct OOS optimum) and $W2 (calibrated OOS optimum) — this order's own fit"
echo "  LAMBDA priced   : $LSTIFF (the stiffest the W2 class floor admits) and $LSOFT (the softening direction)"

run SRoff  RL_O37=1
run SB1    RL_O37=1 RL_O38B1=1
run SAB1   RL_O37=1 RL_O38A=1 RL_O38B1=1
run SR20A  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20

run SW47   RL_O37=1 RL_O38B1=1 RL_O40_RECW=$W1
run SW28   RL_O37=1 RL_O38B1=1 RL_O40_RECW=$W2
run SW47A  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=$W1
run SC15   RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
run SC20   RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20
run SC20A  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20
run SL56   RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=$LSTIFF
run SL10   RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=$LSOFT
run SM     RL_O37=1 RL_O38B1=1 RL_O40_PGMAT=1
run SMA    RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_PGMAT=1
run SALL   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=$W1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 RL_O40_PGMAT=1

echo; echo "--- SimpA (RL_O38B1 + the S2 dials ALONE — the dial must imply the O37/O36-K stack) ---"
env -u RL_O35 -u RL_O36 -u RL_O36_LAM_S1 -u RL_O36_TALL -u RL_O36_FLOORFIX -u RL_O36_KAPPA \
    -u RL_O36_GAMMA -u RL_O36_ETA -u RL_O36_GAMMA_D -u RL_O36_LAMBDA -u RL_O37 \
    -u RL_O38A -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
    -u RL_O40_RECW -u RL_O40_LAMBDA -u RL_O40_PGMAT \
    RL_O31=1 RL_O32=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 bash "$HERE/bbS.sh" SimpA

echo; echo "=== DETERMINISM REPEATS ==="
run SW47_2   RL_O37=1 RL_O38B1=1 RL_O40_RECW=$W1
run SW28_2   RL_O37=1 RL_O38B1=1 RL_O40_RECW=$W2
run SW47A_2  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=$W1
run SC15_2   RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15
run SC20_2   RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20
run SC20A_2  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20
run SL56_2   RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=$LSTIFF
run SL10_2   RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=$LSOFT
run SM_2     RL_O37=1 RL_O38B1=1 RL_O40_PGMAT=1
run SMA_2    RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_PGMAT=1
run SALL_2   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=$W1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 RL_O40_PGMAT=1

echo; echo "=== BOARD MD5s ==="
for d in "$SP"/bb_S*; do
  t=$(basename "$d"); t=${t#bb_}
  m=$(md5sum "$d/rl_after/rl_app_data.json" 2>/dev/null | cut -c1-32)
  echo "  ${t}: ${m:-NO BOARD}"
done
