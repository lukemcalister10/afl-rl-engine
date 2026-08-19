#!/bin/bash
# ORDER S — the variant matrices. STRICTLY SEQUENTIAL. Never two engine runs at once.
# THE CONTROL MATRICES ARE NOT RE-EMITTED AND THAT REUSE IS DECLARED HERE RATHER THAN LEFT TO BE
# NOTICED: per_entrant_QB1.json is this order's SB1 (FIX B1, every S dial unset), per_entrant_QAB1
# is its SAB1, per_entrant_R20A is its SR20A, and per_entrant_PBUILT is ORDER P itself. All four
# were emitted from the IDENTICAL dial line by ORDER Q / ORDER P / ORDER R, and this order has
# already proved byte-exact board identity on all four (BOARDS_S_out.txt). Re-emitting them would
# burn nine minutes each reproducing a file byte for byte.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 RL_O37=1 RL_O38B1=1"
for spec in \
  "SW47:RL_O40_RECW=0.47" \
  "SW47A:RL_O38A=1 RL_O40_RECW=0.47" \
  "SC20:RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20" \
  "SC20A:RL_O38A=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20" \
  "SM:RL_O40_PGMAT=1" \
  "SMA:RL_O38A=1 RL_O40_PGMAT=1" \
  "SL56:RL_O40_LAMBDA=0.56" \
  "SL10:RL_O40_LAMBDA=0.10" \
  "SALL:RL_O38A=1 RL_O40_RECW=0.47 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 RL_O40_PGMAT=1" ; do
  L=${spec%%:*}; D=${spec#*:}
  echo "=== EMIT $L  ($D) ==="
  env -u RL_O35 -u RL_O38A -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
      -u RL_O40_RECW -u RL_O40_CAPFORM -u RL_O40_CAPPCT -u RL_O40_LAMBDA -u RL_O40_PGMAT \
      OP_LABEL=$L $K $D bash "$HERE/run_emit_S.sh"
done
