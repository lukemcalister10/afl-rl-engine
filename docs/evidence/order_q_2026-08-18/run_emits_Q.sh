#!/bin/bash
# ORDER Q — the five variant matrices. STRICTLY SEQUENTIAL.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 RL_O37=1"
for spec in "QA:RL_O38A=1" "QB1:RL_O38B1=1" "QB2:RL_O38B2=1" "QAB1:RL_O38A=1 RL_O38B1=1" "QAB2:RL_O38A=1 RL_O38B2=1"; do
  L=${spec%%:*}; D=${spec#*:}
  echo "=== EMIT $L  ($D) ==="
  env -u RL_O35 -u RL_O38A -u RL_O38B1 -u RL_O38B2 OP_LABEL=$L $K $D bash "$HERE/run_emit_Q.sh"
done
