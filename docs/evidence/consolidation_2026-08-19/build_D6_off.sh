#!/bin/bash
# D6-CONSOLIDATION — THE LAYER-OFF CONTROL. STRICTLY SEQUENTIAL (run only after build_D6.sh finishes).
#
#   D6_OFF   the D5-final dial stack with RL_AVAIL=0 — the availability layer entirely absent.
#
# WHY IT EXISTS. The R1 combined-take guard must print the WHOLE take (Part 1 + Part 2) per row.
# The engine exports Part-1 attribution (avail_nerf) but NOT the Part-2 delta, so the combined take is
# measured against a board on which the layer does not run at all:  take = v(board) - v(D6_OFF).
# This is the engine's own price on both sides, not a re-derivation from unexported internals.
#
# RL_O42 IS DELIBERATELY NOT SET HERE. With RL_AVAIL=0 the layer is off for base and candidate alike,
# so ONE control serves both — and the ORDER 42 guard rejects RL_O42=1 with RL_AVAIL=0 outright,
# precisely so a silent no-op cannot be mistaken for a consolidation.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:-/home/claude/d6scratch/bb}"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbD6.sh" "$T"; }
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"

echo "=== D6-CONSOLIDATION — THE LAYER-OFF CONTROL ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
run D6_OFF $S RL_AVAIL=0

# THE ORDER 42 GUARD, EXERCISED: RL_O42=1 with RL_AVAIL=0 must HALT rather than silently no-op.
echo; echo "--- D6_GUARD : RL_O42=1 with RL_AVAIL=0 must HALT ---"
env $CLEAR $KLINE $S RL_O42=1 RL_AVAIL=0 bash "$HERE/bbD6.sh" D6_GUARD 2>&1 | tail -12
echo "(a non-zero exit and an 'ORDER 42 HALT' line above is the PASS for this check)"

echo; echo "=== BOARD IDS ==="
for T in D6_OFF; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s NO BOARD\n' "$T"; fi
done
