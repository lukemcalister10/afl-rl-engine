#!/bin/bash
# THE BAKE — F1/F2/F3 BOARD ARMS (register v780, 2026-08-20). STRICTLY SEQUENTIAL (never two engine runs
# at once). PREREG_BAKE.md pushed at 907b2da BEFORE the engine was touched. NOTHING IS ADOPTED.
#
# THE POINT OF THIS FILE. build_D7B.sh proved the candidate by SETTING 29 dials on an all-OFF engine.
# After the defaults flip the polarity is inverted: the CANDIDATE is what you get by setting NOTHING, and
# every historical board is reached by a DECLARED KILL-SWITCH combination. So `CLEAR` (a list of `-u`
# unsets) is replaced by `OFFALL` (a list of explicit off-values). Same arms, same expected identities.
#
#   BAKE_CAND     nothing set at all, BARE                     -> must be a05fe951   falsifier F1
#   BAKE_CAND2    determinism repeat of BAKE_CAND               -> must equal CAND    falsifier F3
#   BAKE_BASE     kill-switch RL_O43=0                          -> must be daa16812   falsifier F2
#   BAKE_NOO42    kill-switch RL_O42=0 RL_O43=0                 -> must be ff936186   falsifier F2
#   BAKE_IDENT_P  OFFALL minus RL_O37=0 (P charge stays live)   -> must be 374d4e44   falsifier F2
#   BAKE_IDENT_K  OFFALL + KLINE (with _O37 off, KLINE is no
#                 longer implied and must be supplied)          -> must be f3101883   falsifier F2
#   BAKE_L0R      OFFALL minus RL_O37=0, + O38A/O38B1/TMAXPCT=20-> must be 7f88f509   falsifier F2
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:?RL_SCRATCH must be set}"
export PATH="/root/rl_venv312/bin:$PATH"

# ORDER K's ruled line. Post-flip it is IMPLIED by RL_O37 (which now defaults ON): _O37 -> _O36 -> _O35
# -> _O32 -> _O31, and O36_LAM_S1/KAPPA/GAMMA/ETA take their ORDER K values from the _O37 branch of their
# own defaults. It is supplied EXPLICITLY only for BAKE_IDENT_K, the one arm that turns _O37 OFF.
KLINE="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08"

# THE FULL 18-DIAL KILL-SWITCH LINE — every off-value from the PREREG_BAKE.md flip table. The five
# empty-string entries are the kill-switches for the dials whose OLD default was the empty string; they
# reach the engine only because bbBAKE.sh exports vars that are SET-BUT-EMPTY (BAKE CHANGE 1 of 3).
OFFALL="RL_O37=0 RL_O38A=0 RL_O38B1=0 RL_O39_BETASAT= RL_O40_CAPFORM= RL_O40_CAPPCT= \
RL_O40_RECW= RL_O40_PGMAT=0 RL_O41_SDOFF= RL_O41_CREDIT=0 RL_O41_RESET=0 RL_O41_INJ=0 \
RL_O41_R3=0 RL_O41_RAMP=0 RL_O41_BREAK=binary RL_O41_UNWIND=5 RL_O42=0 RL_O43=0"
# The same line with RL_O37=0 removed: the ORDER P charge stays LIVE while everything downstream is off.
OFF_KEEP_P="${OFFALL/RL_O37=0 /}"

run () { local T=$1; shift; echo; echo "--- $T : ${*:-<nothing set — BARE>} ---"; env "$@" bash "$HERE/bbBAKE.sh" "$T"; }

echo "=== THE BAKE — BOARD ARMS (register v780) ==="
echo "  engine : $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)  (pre-flip was 5f434b95)"
echo "  rl_model: $(md5sum "$RL_ROOT/engine/rl_after/rl_model.py" | cut -c1-32)  (pre-flip was 98f16794)"
echo "  store  : $(md5sum "$RL_ROOT/engine/rl_after/rl_model_data.json" | cut -c1-32)  (pin cb38ef11)"
echo "  v0surf : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8, IN-REPO)"
echo "  out-of-repo /home/claude/v0surf.pkl : $( [ -f /home/claude/v0surf.pkl ] && md5sum /home/claude/v0surf.pkl | cut -c1-32 || echo ABSENT )  — NOT TOUCHED, and no longer in the precedence"
echo "  U0     : 7 return games — OWNER-RULED, DATA-SUPPORTED (D5-final, 2026-08-19). RULED, NOT MEASURED."
echo "  EVERY ARM RUNS UNBOUND: RL_V0SURF_PKL is set NOWHERE."

case "${ONLY:-all}" in
  cand) run BAKE_CAND  BAKE_BARE=1 ;;
  *)
    run BAKE_CAND     BAKE_BARE=1
    run BAKE_CAND2    BAKE_BARE=1
    run BAKE_BASE     RL_O43=0
    run BAKE_NOO42    RL_O42=0 RL_O43=0
    run BAKE_IDENT_P  $OFF_KEEP_P
    run BAKE_IDENT_K  $OFFALL $KLINE
    run BAKE_L0R      $OFF_KEEP_P RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
    ;;
esac

echo; echo "=== BOARD IDS ==="
for T in BAKE_CAND BAKE_CAND2 BAKE_BASE BAKE_NOO42 BAKE_IDENT_P BAKE_IDENT_K BAKE_L0R; do
  F="$RL_SCRATCH/bb_$T/rl_after/rl_app_data.json"
  if [ -f "$F" ]; then printf '%-14s %s\n' "$T" "$(md5sum "$F" | cut -c1-32)"; else printf '%-14s NO BOARD\n' "$T"; fi
done
echo
echo "=== EXPECTED ==="
echo "  BAKE_CAND    a05fe951 (F1: the BARE build — nothing set — must produce the candidate BYTE-EXACT)"
echo "  BAKE_CAND2   == BAKE_CAND (F3 determinism)"
echo "  BAKE_BASE    daa16812 | BAKE_NOO42 ff936186 | BAKE_IDENT_P 374d4e44"
echo "  BAKE_IDENT_K f3101883 | BAKE_L0R    7f88f509        (F2: every kill-switch restores its history)"
echo
echo "  IF ANY ARM MOVES: HALT AND REPORT IT AS FIRED. Do not add dials until the number matches."
