#!/bin/bash
# ORDER 20B TASK 1 — render the v0 delta tables.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
python3 "$HERE/v0_delta.py" "$SP/probe_HEAD.json" "$SP/probe_FIX.json" "$HERE/../v0/V0_DELTA" \
  | tee "$HERE/../v0/V0_DELTA.txt"
