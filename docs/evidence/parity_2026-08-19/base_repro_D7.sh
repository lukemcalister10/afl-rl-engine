#!/bin/bash
# ORDER D7 — THE FIRST PRICING ACT. Reproduce THE BASE daa16812 / 660,578 / 804 byte-exact on this
# seat's own clean worktree of origin/land/order-29 @ d5c37da, BEFORE the engine is edited.
# Uses the D6 seat's OWN bbD6.sh unchanged. Halt if it does not reproduce.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
export RL_ROOT="${RL_ROOT:?set RL_ROOT to this seat worktree}"
export RL_SCRATCH="${RL_SCRATCH:?set RL_SCRATCH}"
HERE="$RL_ROOT/docs/evidence/consolidation_2026-08-19"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42 -u RL_O43"
S="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1"
echo "=== ORDER D7 — BASE REPRODUCTION (must be daa16812 / 660,578 / 804) ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  store  : $(md5sum "$RL_ROOT/engine/rl_after/rl_model_data.json" | cut -c1-32)  (pin cb38ef11)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  sheet  : $(md5sum "$RL_ROOT/docs/owner_annotations/SITTER_2026_v1.csv" | cut -c1-32)  (pin b26798c3)"
echo "  GUARD 5: RED, PRE-EXISTING on this branch. NOT claimed green. NOT re-pinned."
env $CLEAR $KLINE $S bash "$HERE/bbD6.sh" D7_BASEREPRO
F="$RL_SCRATCH/bb_D7_BASEREPRO/rl_after/rl_app_data.json"
python3 - "$F" <<'PY'
import json,sys
a=json.load(open(sys.argv[1]))['active']
print("  rows  %d"%len(a)); print("  total %s"%'{:,}'.format(sum(r['v'] for r in a)))
PY
