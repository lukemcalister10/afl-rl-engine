#!/bin/bash
# ORDER 20B TASK 2 — render the gate report (frozen reading + refit reading).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
python3 "$HERE/gates_report.py" \
  "$SP/probe_HEAD.json" "$SP/probe_FIX.json" \
  "$SP/probe_HEAD_refit.json" "$SP/probe_FIX_refit.json" \
  "$HERE/../gates/GATES" | tee "$HERE/../gates/GATES.txt"
