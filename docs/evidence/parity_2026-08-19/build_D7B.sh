#!/bin/bash
# ORDER D7b — THE THIRD WIRING SITE (o31_D). STRICTLY SEQUENTIAL (never two engine runs at once).
# PREREG_D7B.md pushed at cfd4748 BEFORE the engine edit. NOTHING IS ADOPTED. NOTHING LANDS. NO PR.
# build_D7.sh carried verbatim with the tags re-labelled D7B_* and the scratch re-pointed. The dial
# line is UNCHANGED from build_D7.sh -- read from it, not re-derived.
#
#   D7B_IDENT_P  every RL_O38*/O39/O40/O41/O42/O43 dial UNSET -> must be 374d4e44   acceptance
#   D7B_IDENT_K  ORDER K's ruled line, ORDER P dial off       -> must be f3101883   chain
#   D7B_L0R      A + B1 + TMAXPCT=20, the owner's reference   -> must be 7f88f509   chain
#   D7B_NOO42    the D5-final dial stack, RL_O42 UNSET        -> must be ff936186   chain
#   D7B_BASE     THE BASE, RL_O43 UNSET                       -> must be daa16812   falsifier D7B-F2
#   D7B_CAND     + RL_O43=1  THE PARITY GUARD, THIRD SITE     -> must be a05fe951   falsifier D7B-F1
#   D7B_CAND2    determinism repeat of D7B_CAND                                     falsifier D7B-F4
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/d7bbb}"
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"
CLEAR="-u RL_O35 -u RL_O37 -u RL_O38A -u RL_O38B1 -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
-u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
-u RL_O41_SDOFF -u RL_O41_CREDIT -u RL_O41_CREDITFORM -u RL_O41_RESET -u RL_O41_INJ -u RL_O41_R3 \
-u RL_O41_RAMP -u RL_O41_BREAK -u RL_O41_UNWIND -u RL_O42 -u RL_O43"
run () { local T=$1; shift; echo; echo "--- $T : $* ---"; env $CLEAR $KLINE "$@" bash "$HERE/bbD7.sh" "$T"; }

# THE OWNER-RULED D5-FINAL DIAL LINE. U0=7 IS OWNER-RULED, DATA-SUPPORTED (2026-08-19).
BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
S="$BASE RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"

echo "=== ORDER D7b BUILD — THE THIRD WIRING SITE o31_D (register v775, ruling v771) ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)  (D7 was 29376d5a)"
echo "  store  : $(md5sum "$RL_ROOT/engine/rl_after/rl_model_data.json" | cut -c1-32)  (pin cb38ef11)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  sheet  : $(md5sum "$RL_ROOT/docs/owner_annotations/SITTER_2026_v1.csv" | cut -c1-32)  (pin b26798c3)"
echo "  U0     : 7 return games — OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19)"
echo "  GUARD 5: RED, PRE-EXISTING on this branch. NOT claimed green anywhere. NOT re-pinned."
echo "  ONE SITE. THE LAW HAS NO FREE PARAMETER: it is a per-row max. Nothing here is fitted."

for T in "${RUNS:-D7B_IDENT_P D7B_IDENT_K D7B_L0R D7B_NOO42 D7B_BASE D7B_CAND D7B_CAND2}"; do :; done
case "${ONLY:-all}" in
  cand) run D7B_CAND $S RL_O42=1 RL_O43=1 ;;
  *)
    run D7B_IDENT_P  RL_O37=1
    run D7B_IDENT_K
    run D7B_L0R      RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
    run D7B_NOO42    $S
    run D7B_BASE     $S RL_O42=1
    run D7B_CAND     $S RL_O42=1 RL_O43=1
    run D7B_CAND2    $S RL_O42=1 RL_O43=1
    ;;
esac

echo; echo "=== BOARD IDS ==="
for T in D7B_IDENT_P D7B_IDENT_K D7B_L0R D7B_NOO42 D7B_BASE D7B_CAND D7B_CAND2; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-13s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-13s NO BOARD\n' "$T"; fi
done
echo
echo "=== EXPECTED ==="
echo "  D7B_IDENT_P 374d4e44 | D7B_IDENT_K f3101883 | D7B_L0R 7f88f509 | D7B_NOO42 ff936186"
echo "  D7B_BASE    daa16812 (D7B-F2: the dial UNSET must reproduce THE BASE byte-exact)"
echo "  D7B_CAND    a05fe951 (D7B-F1: THE BOARD MUST NOT MOVE. If it does: HALT, do not renormalise.)"
echo "  D7B_CAND == D7B_CAND2 (D7B-F4 determinism)"
