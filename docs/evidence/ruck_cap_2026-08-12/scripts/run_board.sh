#!/bin/bash
# ORDER 20C — thin, plain-command wrapper around ORDER 20B's build_board_o20b.sh (which is carried
# here BYTE-IDENTICAL). Exists only so the harness-isolation guard sees one simple command per build.
#
# Usage: bash run_board.sh <arm>
#   arm = HEAD_gate | FIX_gate
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
ARM="$1"
S=$(date +%s)
case "$ARM" in
  HEAD_gate) bash "$HERE/build_board_o20b.sh" "$SP/board_HEAD_gate.json" - ;;
  FIX_gate)  bash "$HERE/build_board_o20b.sh" "$SP/board_FIX_gate.json"  "$HERE/mut_fix.py" ;;
  *) echo "unknown arm $ARM"; exit 2 ;;
esac
rc=$?
E=$(date +%s)
echo "  board($ARM) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
exit $rc
