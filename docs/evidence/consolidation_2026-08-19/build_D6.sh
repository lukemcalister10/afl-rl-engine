#!/bin/bash
# D6-CONSOLIDATION — THE INJURY CONSOLIDATION. STRICTLY SEQUENTIAL (never two engine runs at once).
# PREREG_D6.md pushed at bd365f9 BEFORE the engine edit. NOTHING IS ADOPTED. NOTHING LANDS. NO PR.
#
#   D6_IDENT_P  every RL_O38*/O39/O40/O41/O42 dial UNSET      -> must be 374d4e44   falsifier D6-F2
#   D6_IDENT_K  ORDER K's ruled line, ORDER P dial off        -> must be f3101883   chain
#   D6_L0R      A + B1 + TMAXPCT=20, the owner's reference    -> must be 7f88f509   chain
#   D6_BASE     the D5-final dial stack, RL_O42 UNSET         -> must be ff936186   falsifier D6-F1
#   D6_CAND     + RL_O42=1  THE CONSOLIDATION                 = THE PRICED BOARD
#   D6_CAND2    determinism repeat of D6_CAND                                       falsifier D6-F3
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

# THE OWNER-RULED D5-FINAL DIAL LINE. U0=7 IS OWNER-RULED, DATA-SUPPORTED (2026-08-19).
BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
S="$BASE RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"

echo "=== D6-CONSOLIDATION BUILD — THE INJURY CONSOLIDATION ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  store  : $(md5sum "$RL_ROOT/engine/rl_after/rl_model_data.json" | cut -c1-32)  (pin cb38ef11)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  sheet  : $(md5sum "$RL_ROOT/docs/owner_annotations/SITTER_2026_v1.csv" | cut -c1-32)  (pin b26798c35adcd9bd...)"
echo "  U0     : 7 return games — OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19)"
echo "  GUARD 5: RED, PRE-EXISTING on this branch — see PREREG_D6.md §1. NOT claimed green anywhere."

run D6_IDENT_P  RL_O37=1
run D6_IDENT_K
run D6_L0R      RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run D6_BASE     $S
run D6_CAND     $S RL_O42=1
run D6_CAND2    $S RL_O42=1

echo; echo "=== BOARD IDS ==="
for T in D6_IDENT_P D6_IDENT_K D6_L0R D6_BASE D6_CAND D6_CAND2; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-12s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-12s NO BOARD\n' "$T"; fi
done
