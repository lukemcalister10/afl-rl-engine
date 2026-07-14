#!/usr/bin/env bash
# ACCEPTANCE A3 — NOTHING GREEN TURNED RED. A normal run is unchanged:
#   ship_gates reds exactly {A2,A3,A12}; B1 PASS 1.2601/1.2407/1.1521; panel 10/10;
#   the five SSI guards green (one_source_selftest guards 1-4 + Guard 5 boot-store).
set -uo pipefail
REPO=/home/user/afl-rl-engine
OUT="$REPO/session_2026-07-13/suite_hygiene"
export RL_REPO="$REPO" PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor

echo "===== bootstrap (Guard 5 = SSI guard #5) ====="
bash "$REPO/bootstrap.sh" 2>&1 | grep -E "Guard 5|store md5|bootstrap OK"

echo "===== SSI guards 1-4 (one_source_selftest) ====="
( cd /home/claude/rl_workspace/rl_after && RL_REPO="$REPO" python3 one_source_selftest.py 2>&1 ) | tail -8

echo "===== panel (run_panel.sh) ====="
bash "$REPO/run_panel.sh" 2>&1 | grep -E "RESULT|MISMATCH"; echo "panel exit via pipefail PIPESTATUS=${PIPESTATUS[0]}"

echo "===== ship_gates suite ====="
python3 "$REPO/ship_gates_check.py" > "$OUT/A3_ship_gates.log" 2>&1
echo "ship_gates rc=$?"
grep -E "^A2 |^A3 |^A12 |^B1 |VERDICT" "$OUT/A3_ship_gates.log"
echo "A3 DONE"
