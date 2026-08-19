#!/bin/bash
# FINAL-CANDIDATE ASSEMBLY — THE BOARDS, ON THIS SEAT'S OWN BUILD.
# STRICTLY SEQUENTIAL. Modelled byte-for-byte on the D6 seat's build_D6_cand.sh / build_D6.sh dial
# lines; only the tags and the scratch dir differ.
#
# THE FIRST PRICING ACT IS FC_CAND. If it is not daa16812 / 660,578 / 804 rows this order HALTS.
#
#   FC_CAND    the D5-final stack + RL_O42=1   = THE CANDIDATE          -> must be daa16812
#   FC_CAND2   determinism repeat                                        -> must be daa16812
#   FC_BASE    the D5-final stack, RL_O42 UNSET                          -> must be ff936186
#   FC_IDENT_P every ORDER-38*/39/40/41/42 dial OFF                      -> must be 374d4e44
#   FC_IDENT_K ORDER K's ruled line                                      -> must be f3101883
#   FC_L0R     R20A, the owner's reference                               -> must be 7f88f509
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/fc}"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42 -u RL_AVAIL"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbFC.sh" "$T"; }
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"

echo "=== FINAL-CANDIDATE ASSEMBLY — THE BOARDS ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)   (RL_V0SURF_PKL bound explicitly by bbFC.sh)"
echo "  sheet  : $(md5sum "$RL_ROOT/docs/owner_annotations/SITTER_2026_v1.csv" | cut -c1-32)"
echo "  U0     : 7 return games — OWNER-RULED, DATA-SUPPORTED"

# THE FIRST PRICING ACT.
run FC_CAND    $S RL_O42=1
run FC_CAND2   $S RL_O42=1
run FC_BASE    $S
# The identity lines are the D6 seat's, character for character (build_D6.sh). `run` already
# prepends $KLINE, so FC_IDENT_K takes no extra dials.
run FC_IDENT_P  RL_O37=1
run FC_IDENT_K
run FC_L0R      RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20

echo; echo "=== BOARD IDS ==="
for T in FC_CAND FC_CAND2 FC_BASE FC_IDENT_P FC_IDENT_K FC_L0R; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s NO BOARD\n' "$T"; fi
done
