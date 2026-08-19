#!/bin/bash
# ASSEMBLY BUILD — D4 (fold the ramp in) + D5 (the owner's unwind shape). STRICTLY SEQUENTIAL.
# PREREG_D4_D5.md pushed at c6ae99d BEFORE the engine edit. NOTHING LANDS. NO PULL REQUEST.
#
#   IDENT_P      every RL_O38*/O39/O40/O41 dial UNSET -> must be 374d4e44          falsifier D-A1
#   V755_L5C     the last pre-R3 lever board          -> must be 1270991c unmoved  falsifier D-A7
#   V755_CAND    D4 FOLDED IN: the candidate + RL_O41_RAMP=1, break binary  = THE NEW CANDIDATE
#   V755_CAND2   determinism repeat                                                 falsifier D-A3
#   V755_CANDU   the same board with RL_O41_BREAK=binary set EXPLICITLY  (unset == binary, D-A6)
#   V755_UNW     D5 PRICED: + RL_O41_BREAK=unwind, U0=5 (the owner's ruled constant)
#   V755_UNW2    determinism repeat
#   V755_FRAC    the fractional variant, rebuilt on this engine so all three sit on ONE engine
#   V755_BIN0    the PRE-D4 binary board (no ramp) — isolates what folding the ramp in costs
# and, only under V755_SWEEP=1, the D6 break-speed sweep U0 in {3,7,11} as priced boards.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm}
export RL_SCRATCH="$SP"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbASM.sh" "$T"; }

# THE RULED LINE (v748 + v750 + v754). LAMBDA UNTOUCHED. D4: RL_O41_RAMP=1 IS NOW PART OF IT.
BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
S="$BASE RL_O41_R3=1 RL_O41_RAMP=1"

echo "=== ASSEMBLY BUILD — D4 FOLD-IN + D5 UNWIND ==="
echo "  engine  : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  ruled   : recency 0.47 · slope 0.105 · compression p15 · SD offset 2.98 · RAMP f**1.5 FOLDED IN"
echo "  LAMBDA  : UNTOUCHED at the anchor 0.1743833037 (RL_O40_LAMBDA never set)"
echo "  U0      : 5 return games — RULED BY THE OWNER, **NOT MEASURED**"

run IDENT_P     RL_O37=1
run V755_L5C    $BASE
run V755_BIN0   $BASE RL_O41_R3=1
run V755_CAND   $S
run V755_CAND2  $S
run V755_CANDU  $S RL_O41_BREAK=binary
run V755_UNW    $S RL_O41_BREAK=unwind RL_O41_UNWIND=5
run V755_UNW2   $S RL_O41_BREAK=unwind RL_O41_UNWIND=5
run V755_FRAC   $S RL_O41_BREAK=fractional

if [ "${V755_SWEEP:-0}" != "0" ]; then
  run V755_U3   $S RL_O41_BREAK=unwind RL_O41_UNWIND=3
  run V755_U7   $S RL_O41_BREAK=unwind RL_O41_UNWIND=7
  run V755_U11  $S RL_O41_BREAK=unwind RL_O41_UNWIND=11
fi

echo; echo "=== BOARD IDS ==="
for T in IDENT_P V755_L5C V755_BIN0 V755_CAND V755_CAND2 V755_CANDU V755_UNW V755_UNW2 V755_FRAC \
         V755_U3 V755_U7 V755_U11; do
  F="$SP/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; fi
done
