#!/bin/bash
# ASSEMBLY BUILD — rebuild from L4_SD onward after the SD-offset site repair, plus the identity.
# The boards above L4_SD carry no RL_O41 dial at all and are unaffected by that repair; they are
# NOT rebuilt and their md5s are re-asserted from disk by as_boards.py.
# STRICTLY SEQUENTIAL. NOTHING IS ADOPTED.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm}
export RL_SCRATCH="$SP"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbASM.sh" "$T"; }
W=0.47; BSAT=0.105; CAPP=20; SDOFF=2.98
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=$BSAT RL_O40_CAPFORM=smooth RL_O40_CAPPCT=$CAPP RL_O40_RECW=$W RL_O40_PGMAT=1"

echo "=== ASSEMBLY REBUILD FROM L4_SD (SD-offset site repaired) ==="
echo "  engine: $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"

run IDENT_P  RL_O37=1
run L4_SD    $S RL_O41_SDOFF=$SDOFF
run L5A_CRED $S RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1
run L5B_RSET $S RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1
run L5C_INJ  $S RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
run CAND     $S RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1
run CAND_2   $S RL_O41_SDOFF=$SDOFF RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1

echo; echo "=== BOARD IDS ==="
for T in IDENT_P IDENT_K L0_R L1_REC L2_COMP L3_MAT L4_SD L5A_CRED L5B_RSET L5C_INJ CAND CAND_2; do
  F="$SP/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-10s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-10s %s\n' "$T" "NO BOARD"; fi
done
