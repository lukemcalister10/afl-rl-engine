#!/bin/bash
# ORDER 20B TASK 3 — nd_profile AT FIXED-ENGINE v0s.
#
# The published de-contamination figure (1.0253296290 -> 0.9944115616, ORDER 20 §3a) was computed on a
# HEAD-EMITTED matrix, i.e. at PRE-FIX v0s. nd_profile's denominator is SUM v0, so the figure has to be
# retaken on a matrix emitted by the FIXED engine before it can be the number ORDER 22 calibrates
# against. This runs ORDER 20's own instrument (imported, not re-derived) against BOTH matrices, so the
# v0-side contribution and the strata-side contribution are separated rather than conflated.
#
# Usage: bash run_ndprofile.sh
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ND="$HERE/../ndprofile"
SRC="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export RL_REPO="$SRC"

for T in HEAD FIX; do
  echo "############################################################################"
  echo "### nd_profile on the $T-EMITTED matrix   ($SP/matrix_$T.json)"
  echo "############################################################################"
  python3 "$ND/nd_profile_test.py" "$SP/matrix_$T.json"
  mv "$ND/ND_PROFILE_TEST.json" "$ND/ND_PROFILE_${T}emit.json"
done
