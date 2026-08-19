#!/bin/bash
# FINAL-CANDIDATE — THE R3-OFF COMPANION BOARD. STRICTLY SEQUENTIAL.
#
# WHY IT EXISTS. Two acceptance items need a board that matches the candidate on EVERY dial except
# RL_O41_R3:
#   · as_r3age.py (the R3-aware birthday probe) needs it as its denominator. Its own header is
#     explicit that a baseline differing in any OTHER dial mis-attributes those rows to R3.
#   · os_census.py's burn sweep reconstructs price as [rho*e + age credit] + pi_base*(v*PL_F)*factor(v),
#     an identity with NO absence-collector term, so it asserts on any R3-live board. The assembly
#     seat ran the censuses on its own R3-off line for exactly this reason (PACKET_ASSEMBLY §10).
#
#   FC_NOR3   the candidate's dial line with RL_O41_R3 UNSET — ramp ON, break/unwind ON, RL_O42=1
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

# the candidate line, MINUS RL_O41_R3 — AND MINUS RL_O41_BREAK/RL_O41_UNWIND, WHICH IS FORCED.
#
# DISCLOSED, because it is a deviation from the one-dial-apart ideal as_r3age.py's header asks for.
# The first attempt dropped R3 ALONE and the ENGINE REFUSED TO BUILD IT:
#     ORDER 41 HALT: RL_O41_BREAK=unwind but RL_O41_R3 is unset. The break rule shapes a
#     collector that is not switched on.
# (raw: BUILD_FC_NOR3_HALT_out.txt). BREAK and UNWIND do nothing except shape the R3 collector, so
# with R3 off they are not merely unused, they are refused. The only R3-off line the engine will
# build therefore drops all three together, and the CAND-minus-NOR3 delta is "R3 AND ITS SHAPING"
# as one unit rather than R3 alone. That is NOT silently assumed to be harmless: as_r3age.py's
# SELF-CHECK 2 re-forms R3's take from the engine's own objects and requires it to reproduce every
# per-row board delta at tolerance 0. If BREAK/UNWIND moved a row that R3 alone does not explain,
# that self-check FAILS and the probe draws no conclusion. It is the guard on this deviation.
NOR3="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_RAMP=1"

echo "=== FINAL-CANDIDATE — THE R3-OFF COMPANION ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"

run FC_NOR3 $NOR3 RL_O42=1

echo; echo "=== BOARD IDS ==="
for T in FC_CAND FC_NOR3; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s NO BOARD\n' "$T"; fi
done
