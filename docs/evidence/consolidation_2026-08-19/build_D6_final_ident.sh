#!/bin/bash
# D6-CONSOLIDATION — THE IDENTITIES RE-RUN ON THE FINAL ENGINE.
#
# WHY. The identities were first proven on engine 56ee8ce6, before D6-F8 fired and the guard inside
# _o42_state was corrected. That correction lives on the RL_O42=1 lane only, so the dial-off path is
# untouched by construction — but "by construction" is an argument, and this project prices identities
# rather than arguing them. These four boards are rebuilt on the FINAL engine so every identity claim
# in PACKET_D6.md stands on the engine that is actually committed.
#
#   D6F_IDENT_P  every RL_O38*/O39/O40/O41/O42 dial UNSET  -> must be 374d4e44   D6-F2
#   D6F_IDENT_K  ORDER K's ruled line                      -> must be f3101883   chain
#   D6F_L0R      R20A, the owner's reference               -> must be 7f88f509   chain
#   D6F_BASE     the D5-final stack, RL_O42 UNSET          -> must be ff936186   D6-F1
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:-/home/claude/d6scratch/bb}"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42 -u RL_AVAIL"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbD6.sh" "$T"; }
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"

echo "=== D6-CONSOLIDATION — IDENTITIES ON THE FINAL ENGINE ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
run D6F_IDENT_P  RL_O37=1
run D6F_IDENT_K
run D6F_L0R      RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run D6F_BASE     $S

echo; echo "=== BOARD IDS (expected: 374d4e44 · f3101883 · 7f88f509 · ff936186) ==="
for T in D6F_IDENT_P D6F_IDENT_K D6F_L0R D6F_BASE; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-13s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-13s NO BOARD\n' "$T"; fi
done
