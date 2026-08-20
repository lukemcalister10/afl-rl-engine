#!/bin/bash
# ASSEMBLY BUILD — THE F2 FIX PASS (audit finding F2, PREREG_F2_FIX.md pushed at 74d9520 BEFORE the
# engine edit). STRICTLY SEQUENTIAL — never two engine runs at once. NOTHING LANDS. NO PULL REQUEST.
#
# WHY ONLY FOUR BOARDS AND NOT THE WHOLE STACK. The edit adds one helper and one clause, BOTH inside
# `o41_r3_take`, which is unreachable unless RL_O41_R3 is set. Every board in the lever stack up to
# and including L5C_INJ therefore cannot move, and the previously built V750_L5* boards stay valid.
# THIS IS NOT ASSUMED: IDENT_P is rebuilt on the edited engine as the dial-off control, and V750_L5C
# is rebuilt as V754_L5C and asserted byte-identical to the board already on disk.
#
#   IDENT_P    every RL_O38*/O39/O40/O41 dial UNSET      -> must be 374d4e44 (ORDER P)   falsifier F2-A1
#   V754_L5C   the last pre-R3 lever board               -> must be 1270991c (unmoved)
#   V754_CAND  the candidate, F2 fix live                -> NEW IDENTITY
#   V754_CAND2 an identical repeat                       -> determinism x2               falsifier F2-A3
#   V754_FRAC  the priced fractional-break variant        -> NEW IDENTITY (v754, not adopted)
#   V754_FRAC2 an identical repeat                       -> determinism x2
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
-u RL_O41_RAMP -u RL_O41_BREAK"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbASM.sh" "$T"; }

# THE RULED LINE (register v748 + v750: the compression anchor is p15, LAMBDA UNTOUCHED).
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"

echo "=== ASSEMBLY BUILD — THE F2 FIX PASS ==="
echo "  engine  : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  ruled   : recency w=0.47 · slope 0.105 · compression p15 · SD offset 2.98"
echo "  LAMBDA  : UNTOUCHED at the anchor 0.1743833037 (RL_O40_LAMBDA never set)"
echo "  fix     : o41_completed_absent >= 1 required beside the untouched depth < 2 guard"

run IDENT_P    RL_O37=1
run V754_L5C   $S
run V754_CAND  $S RL_O41_R3=1
run V754_CAND2 $S RL_O41_R3=1
run V754_FRAC  $S RL_O41_R3=1 RL_O41_BREAK=fractional
run V754_FRAC2 $S RL_O41_R3=1 RL_O41_BREAK=fractional

echo; echo "=== BOARD IDS ==="
for T in IDENT_P V754_L5C V754_CAND V754_CAND2 V754_FRAC V754_FRAC2; do
  F="$SP/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s %s\n' "$T" "NO BOARD"; fi
done

# ---- the two PRICED, NOT ADOPTED variants, rebuilt so every comparison sits on ONE engine ----
#   V754_RAW   the candidate with F1's RAW credit cells instead of the guarded curve (credit OOS)
#   V754_RAMP  the candidate with the D12 f**1.5 in-season ramp on the two DEPTH clocks
if [ "${V754_VARIANTS:-0}" != "0" ]; then
  run V754_RAW   $S RL_O41_R3=1 RL_O41_CREDITFORM=raw
  run V754_RAW2  $S RL_O41_R3=1 RL_O41_CREDITFORM=raw
  run V754_RAMP  $S RL_O41_R3=1 RL_O41_RAMP=1
  for T in V754_RAW V754_RAW2 V754_RAMP; do
    F="$SP/bb_$T/rl_after/rl_app_data.json"
    printf '%-12s %s\n' "$T" "$(md5sum "$F" 2>/dev/null | cut -c1-32)"
  done
fi
