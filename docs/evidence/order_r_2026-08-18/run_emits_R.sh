#!/bin/bash
# ORDER R — the nine variant matrices. STRICTLY SEQUENTIAL. Never two engine runs at once.
# The two CONTROL matrices already exist and are NOT re-emitted: per_entrant_QB1.json is this
# order's RB1 (p5/b0/A-off) and per_entrant_QAB1.json is its RAB1 (p5/b0/A-on), both built by
# ORDER Q from the identical dial line. Re-emitting them would burn nine minutes to reproduce a
# file byte for byte. That reuse is DECLARED here rather than left to be noticed.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K="RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08 RL_O37=1 RL_O38B1=1"
for spec in \
  "R15:RL_O39_TMAXPCT=15" \
  "R20:RL_O39_TMAXPCT=20" \
  "R15A:RL_O38A=1 RL_O39_TMAXPCT=15" \
  "R20A:RL_O38A=1 RL_O39_TMAXPCT=20" \
  "Rb1:RL_O39_BETASAT=0.111" \
  "Rb2:RL_O39_BETASAT=0.105" \
  "R15b1:RL_O39_TMAXPCT=15 RL_O39_BETASAT=0.111" \
  "R20b2:RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105" \
  "R20b2A:RL_O38A=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105" ; do
  L=${spec%%:*}; D=${spec#*:}
  echo "=== EMIT $L  ($D) ==="
  env -u RL_O35 -u RL_O38A -u RL_O38B2 -u RL_O39_TMAXPCT -u RL_O39_BETASAT \
      OP_LABEL=$L $K $D bash "$HERE/run_emit_R.sh"
done
