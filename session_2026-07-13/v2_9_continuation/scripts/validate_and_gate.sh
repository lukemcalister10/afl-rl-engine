#!/bin/bash
# Sequential: validate each single lever's board vs the inherited sims, then build the ONE combined
# candidate matrix (L1+L4+L2+L3) for the reconciled G-COHORT gate. Background-friendly.
set -e
REPO=/home/user/afl-rl-engine
RUN="$REPO/session_2026-07-13/v2_9_continuation/scripts/run_levers.sh"
SC=/tmp/claude-0/-home-user-afl-rl-engine/3c2e6b18-8ee5-5535-9b38-adbb45999814/scratchpad
OUTD="$REPO/session_2026-07-13/v2_9_continuation/out"

echo "########## SINGLE-LEVER VALIDATION (vs inherited sims) ##########"
for L in L1 L4 L2 L3; do
  echo "---- $L ----"
  bash "$RUN" "$L" board "$SC/board_${L}.json" 2>&1 | grep -E 'BOARD|\[patch\]|\[restore\]'
done

echo "########## COMBINED CANDIDATE MATRIX (L1,L4,L2,L3) ##########"
bash "$RUN" "L1,L4,L2,L3" matrix "$SC/s4_combined.json" 2>&1 | grep -E 'matrix saved|\[patch\]|\[restore\]|eligible'
echo "########## DONE ##########"
