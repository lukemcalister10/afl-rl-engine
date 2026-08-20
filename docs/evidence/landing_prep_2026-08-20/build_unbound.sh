#!/bin/bash
# THE UNBOUND-SURFACE BOARD BUILD (landing prep 2026-08-20, order item 2).
# The EXACT candidate dial line of docs/evidence/parity_2026-08-19/build_D7B.sh ONLY=cand, run through
# bbD7_unbound.sh -- which is bbD7.sh with the single line `export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"`
# replaced by `unset RL_V0SURF_PKL`, and NOTHING ELSE (the diff is in the record).
# THE QUESTION: after the C3 re-key, does a build with NO explicit surface binding still produce
# a05fe951 byte-exact -- i.e. is the boot-workspace footgun dead on this branch?
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:?}"
export PATH="/root/rl_venv312/bin:$PATH"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42 -u RL_O43 -u RL_V0SURF_PKL"
BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
S="$BASE RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"
echo "=== UNBOUND-SURFACE CANDIDATE BUILD — no RL_V0SURF_PKL anywhere ==="
echo "  engine       : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)  (pin now 5f434b95)"
echo "  branch v0surf: $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  /home/claude/v0surf.pkl : $( [ -f /home/claude/v0surf.pkl ] && md5sum /home/claude/v0surf.pkl | cut -c1-32 || echo ABSENT )"
echo "  engine precedence: \$RL_V0SURF_PKL -> /home/claude/v0surf.pkl -> <repo>/data/v0surf.pkl"
echo
env $CLEAR $KLINE $S RL_O42=1 RL_O43=1 bash "$HERE/bbD7_unbound.sh" UNBOUND_CAND
echo
F="$RL_SCRATCH/bb_UNBOUND_CAND/rl_after/rl_app_data.json"
echo "=== RESULT ==="
if [ -f "$F" ]; then
  G=$(md5sum "$F" | cut -c1-32)
  echo "  board built : $G"
  echo "  expected    : a05fe951f78482c70520480e184c80ec"
  [ "$G" = "a05fe951f78482c70520480e184c80ec" ] && echo "  VERDICT     : BYTE-EXACT — the footgun is DEAD on this branch." \
    || echo "  VERDICT     : NOT BYTE-EXACT — the out-of-repo surface WON. The footgun is ALIVE."
else
  echo "  NO BOARD — the build HALTED. Read the stderr tail above."
  echo "  expected    : a05fe951f78482c70520480e184c80ec"
  echo "  VERDICT     : the unbound build does not produce the candidate."
fi
