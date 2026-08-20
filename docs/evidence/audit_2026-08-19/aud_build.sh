#!/bin/bash
# AUDIT REBUILD — independent reproduction of the candidate and the dial-off identity.
# Strictly sequential. Staging copied from bbASM.sh verbatim.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
export RL_ROOT=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audit-wt
export RL_SCRATCH=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audbb
OUT=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audout
mkdir -p "$OUT" "$RL_SCRATCH"
BB="$RL_ROOT/docs/evidence/assembly_2026-08-19/bbASM.sh"

CANDNOR3="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
CAND="$CANDNOR3 RL_O41_R3=1"

echo "===== A2 · DIAL-OFF (ORDER P target 374d4e44) ====="
env RL_O37=1 bash "$BB" AUD_P            > "$OUT/AUD_P.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_P.txt"

echo "===== A1a · CANDIDATE run 1 (target fbf61d05) ====="
env $CAND bash "$BB" AUD_C1              > "$OUT/AUD_C1.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_C1.txt"

echo "===== A1b · CANDIDATE run 2 (determinism) ====="
env $CAND bash "$BB" AUD_C2              > "$OUT/AUD_C2.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_C2.txt"

echo "===== R = R20A (target 7f88f509) ====="
env RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 bash "$BB" AUD_R > "$OUT/AUD_R.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_R.txt"

echo "ALL BUILDS DONE"
