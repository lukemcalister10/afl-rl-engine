#!/bin/bash
# ORDER 20 — build one board per perturbation, then diff each against BASE.
# Usage: run_perturbations.sh [perturbation ...]     (default: all six)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
LIST=${*:-"x1.5 x0.5 x3.0 tilt rd_only flat100"}

# THE BASE IS ALWAYS REBUILT FROM THE CURRENT TREE. Reusing a cached BASE would silently compare a board
# built from an OLD engine against perturbed boards built from the CURRENT one, which is not a perturbation
# test at all — it is an engine diff wearing a perturbation's name. Set RL_O20_KEEP_BASE=1 only when you have
# just built it from this same tree and are re-running the diffs.
if [ "${RL_O20_KEEP_BASE:-0}" != "1" ] || [ ! -f "$SP/o20/board_BASE.json" ]; then
  bash "$HERE/build_board_o20.sh" "$SP/o20/board_BASE.json" -
fi
echo "BASE md5 $(md5sum "$SP/o20/board_BASE.json" | cut -c1-32)"

FAIL=0
for P in $LIST; do
  echo "--- $P ---"
  RL_O20_PERTURB=$P bash "$HERE/build_board_o20.sh" "$SP/o20/board_P_$P.json" "$HERE/perturb_pool.py" 2>&1 | tail -2
  python3 "$HERE/nd_diff.py" "$SP/o20/board_BASE.json" "$SP/o20/board_P_$P.json" "pool perturbation: $P" || FAIL=1
done
echo
echo "OVERALL: $([ $FAIL -eq 0 ] && echo 'ALL PERTURBATIONS — SEPARATION HOLDS ON THE BOARD' || echo 'AT LEAST ONE PERTURBATION MOVED THE NATIONAL ARM')"
exit $FAIL
