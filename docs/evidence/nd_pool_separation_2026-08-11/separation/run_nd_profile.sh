#!/bin/bash
# ORDER 20 — the nd_profile leg alone, against matrices already emitted into $SP/o20.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH RL_REPO="$ROOT" OPENBLAS_NUM_THREADS=1
python3 "$HERE/nd_profile_test.py" "$SP/o20/per_entrant_BASE.json" \
    "$SP/o20/per_entrant_P_x3.0.json" "$SP/o20/per_entrant_P_flat100.json" \
    | tee "$HERE/ND_PROFILE_TEST.txt"
