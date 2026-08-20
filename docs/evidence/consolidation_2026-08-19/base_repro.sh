#!/bin/bash
# D6-CONSOLIDATION — BASELINE REPRODUCTION of the D5-final board ff936186 / 659,222.
# Uses the assembly seat's OWN bbASM.sh unchanged, with the D5-final dial line
# (RL_O41_BREAK=unwind, RL_O41_UNWIND=7). Nothing edited yet.
set -uo pipefail
export RL_ROOT="/home/claude/d6_build"
export RL_SCRATCH="/home/claude/d6scratch/bb"
HERE="$RL_ROOT/docs/evidence/assembly_2026-08-19"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbASM.sh" "$T"; }
BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
S="$BASE RL_O41_R3=1 RL_O41_RAMP=1"
echo "=== D6-CONSOLIDATION BASELINE REPRO ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  store  : $(md5sum "$RL_ROOT/engine/rl_after/rl_model_data.json" | cut -c1-32)  (pin cb38ef11)"
run D6_BASE $S RL_O41_BREAK=unwind RL_O41_UNWIND=7
echo; echo "=== BOARD IDS ==="
for T in D6_BASE; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  [ -f "$F" ] && printf '%-10s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)" || printf '%-10s NO BOARD\n' "$T"
done
