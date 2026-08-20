#!/bin/bash
# THE EMIT RE-RUN on the RE-KEYED branch (landing prep 2026-08-20, order item 4).
# run_emit_CP.sh is invoked UNMODIFIED. It only passes through dials that are ALREADY SET in the
# ambient environment, so the candidate dial line -- read verbatim from build_D7B.sh, not re-derived --
# is exported here first. The ORDER 31-F replication guard is NOT weakened: same two legs, tolerance 0,
# against the FROZEN docs/evidence/final_candidate_2026-08-19/DAY0_CP.json.
# (First attempt in this seat was run WITHOUT the dial line exported; the guard failed closed at
#  1 of 89 and no matrix was written. Disclosed rather than quietly retried.)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
export RL_O31=1 RL_O32=1 RL_O36=1 RL_O36_LAM_S1=0.40 RL_O36_TALL=1 RL_O36_FLOORFIX=1 \
       RL_O36_KAPPA=0.20 RL_O36_GAMMA=8.0 RL_O36_ETA=0.50 RL_O36_GAMMA_D=14.0 RL_O36_LAMBDA=1.08
export RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
       RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1
export RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1 RL_O43=1
OP_LABEL=${OP_LABEL:-LP} bash "$REPO/docs/evidence/final_candidate_2026-08-19/run_emit_CP.sh"
