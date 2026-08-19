#!/bin/bash
# ASSEMBLY BUILD — THE CANDIDATE AND ITS LEVER STACK. STRICTLY SEQUENTIAL (never two engine runs at
# once). NOTHING HERE IS ADOPTED. NOTHING LANDS. NO PULL REQUEST. THE CANDIDATE IS FOR OWNER REVIEW.
#
# CONTROLS (must reproduce byte-exact, or a falsifier fires):
#   IDENT_P : every RL_O38*/RL_O39_*/RL_O40_*/RL_O41_* UNSET -> 374d4e44 (ORDER P)     A-F1
#   IDENT_K : the ORDER K ruled line, ORDER P dial off       -> f3101883 (ORDER K)     A-F2
#   L0_R    : A + B1 + TMAXPCT=20                            -> 7f88f509 (R20A)        A-F1
#
# THE LEVER STACK — each board is the one before it plus ONE lever, so the marginal effect of every
# ruled dial is a subtraction and not an argument (register v742, the owner's own ask).
#   L1_REC   + recency w = 0.47                                              (v748)
#   L2_COMP  + the compressed cap p20 AND the slope 0.105, replacing the clip (v745 + standing)
#   L3_MAT   + the mature refit                                              (v745)
#   L4_SD    + the SD level offset 2.98, standalone                          (v744)
#   L5A_CRED + the measured credit curve            (absence package I1)
#   L5B_RSET + the graded reset + the F4 depth>=3 row (absence package I2)
#   L5C_INJ  + the injury stream, live board only   (absence package I3)
#   CAND     + the R3 production fade               (absence package I4)  = THE CANDIDATE
#   CAND_2   an identical repeat of the candidate -> the determinism proof
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm}
export RL_SCRATCH="$SP"
# ORDER K'S RULED SETTING — owner comment 5321546243, register v735. NOT a search axis here.
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3"
run () { # run TAG extra-env...
  local T=$1; shift
  echo; echo "--- $T : $* ---"
  env $CLEAR $KLINE "$@" bash "$HERE/bbASM.sh" "$T"
}
# THE RULED SETTINGS. LAMBDA IS UNTOUCHED — RL_O40_LAMBDA IS NEVER SET ON ANY BOARD BELOW.
W=0.47            # recency, v748
BSAT=0.105        # the slope, v745
CAPP=20           # the compression anchor, standing + v748
SDOFF=2.98        # the SD level offset, T1 measured, v744

echo "=== ASSEMBLY BUILD — THE CANDIDATE AND ITS LEVER STACK ==="
echo "  engine  : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  ruled   : recency w=$W · slope BETA_sat=$BSAT · compression p$CAPP · SD offset $SDOFF"
echo "  LAMBDA  : UNTOUCHED at the anchor 0.1743833037 (RL_O40_LAMBDA never set)"
echo "  RUCK    : NOT WIRED — the diagnosis names the C3 age delta, not PG (PREREG_ASSEMBLY.md §3)"
echo "  SF      : NOT WIRED — survivor-bias caveat (v744)"

# ---- the identities ----
run IDENT_P  RL_O37=1
run IDENT_K

# ---- the reference ----
run L0_R     RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20

# ---- the lever stack ----
run L1_REC   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O40_RECW=$W
run L2_COMP  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W
run L3_MAT   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1
run L4_SD    RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF
run L5A_CRED RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1
run L5B_RSET RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1
run L5C_INJ  RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
run CAND     RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1
run CAND_2   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1 RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1

echo; echo "=== BOARD IDS ==="
for T in IDENT_P IDENT_K L0_R L1_REC L2_COMP L3_MAT L4_SD L5A_CRED L5B_RSET L5C_INJ CAND CAND_2; do
  F="$SP/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-10s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-10s %s\n' "$T" "NO BOARD"; fi
done
