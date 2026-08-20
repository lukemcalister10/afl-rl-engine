#!/bin/bash
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
export RL_ROOT=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audit-wt
export RL_SCRATCH=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audbb
OUT=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/audout
BB="$RL_ROOT/docs/evidence/assembly_2026-08-19/bbASM.sh"
CAND="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1"

echo "===== POST-BREAK-COMMIT · candidate must STILL be fbf61d05 (break dial unset) ====="
env $CAND bash "$BB" AUD_C3 > "$OUT/AUD_C3.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_C3.txt"

echo "===== FRACTIONAL VARIANT (target 2eac9bc7) ====="
env $CAND RL_O41_BREAK=fractional bash "$BB" AUD_FR1 > "$OUT/AUD_FR1.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_FR1.txt"

echo "===== FRACTIONAL determinism repeat ====="
env $CAND RL_O41_BREAK=fractional bash "$BB" AUD_FR2 > "$OUT/AUD_FR2.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_FR2.txt"

echo "===== DIAL-OFF must STILL be 374d4e44 ====="
env RL_O37=1 bash "$BB" AUD_P2 > "$OUT/AUD_P2.txt" 2>&1; echo "exit=$?"; cat "$OUT/AUD_P2.txt"
echo "ALL DONE 2"
