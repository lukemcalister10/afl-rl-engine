#!/bin/bash
# D6-CONSOLIDATION — THE CANDIDATE, ITS DETERMINISM REPEAT, AND THE LAYER-OFF CONTROL.
# STRICTLY SEQUENTIAL. Run after build_D6.sh (which established the identities and the base).
#
# WHY THIS FILE EXISTS SEPARATELY. The first candidate build HALTED on this order's OWN guard:
#   ORDER 42 HALT: andy-moniz-wakefield — the re-base is not the stated form (g=2 L22=0.909091 L18=0.888889)
# Falsifier D6-F8 fired, and the diagnosis went against this seat: the FALSIFIER was mis-stated, not
# the re-base. Re-basing to a SHORTER season LOWERS the haircut on a row that played some games
# (g/18 > g/22), so L18 <= L22. The re-base form is exactly the one briefed and preregistered,
# 1 - min(g/18, 1); nothing about it moved. The guard now checks the invariant the form actually has.
# PREREG_D6.md §11 records the fire; PACKET_D6.md reports it.
#
#   D6_CAND   the D5-final stack + RL_O42=1   = THE PRICED BOARD
#   D6_CAND2  determinism repeat                                          falsifier D6-F3
#   D6_OFF    the D5-final stack, RL_AVAIL=0  = the layer-off control for the R1 combined take
#   D6_GUARD  RL_O42=1 with RL_AVAIL=0 must HALT rather than silently no-op
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

echo "=== D6-CONSOLIDATION — THE CANDIDATE + CONTROLS ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  sheet  : $(md5sum "$RL_ROOT/docs/owner_annotations/SITTER_2026_v1.csv" | cut -c1-32)"
echo "  U0     : 7 return games — OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19)"

run D6_CAND   $S RL_O42=1
run D6_CAND2  $S RL_O42=1
run D6_OFF    $S RL_AVAIL=0

echo; echo "--- D6_GUARD : RL_O42=1 with RL_AVAIL=0 MUST HALT ---"
env $CLEAR $KLINE $S RL_O42=1 RL_AVAIL=0 bash "$HERE/bbD6.sh" D6_GUARD 2>&1 | grep -E "ORDER 42 HALT|EXPORT FAILED" | head -4
echo "(an 'ORDER 42 HALT' line above is the PASS for this check — the dial refuses to be a silent no-op)"

echo; echo "=== BOARD IDS ==="
for T in D6_BASE D6_CAND D6_CAND2 D6_OFF; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s NO BOARD\n' "$T"; fi
done
