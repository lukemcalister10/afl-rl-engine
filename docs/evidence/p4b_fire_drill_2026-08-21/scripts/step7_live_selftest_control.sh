#!/usr/bin/env bash
# P4b FIRE DRILL — step 7: CONTROL. Run the SAME build + one_source_selftest against the CURRENT
# HEAD, in a scratch copy (the live tree is never written). Purpose: attribute the 13 self-test reds
# seen on the restored tag world — instrument era-drift (also red today) vs restore damage (green today).
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
P4B=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b
LIVE=/home/user/afl-rl-engine/.claude/worktrees/agent-a08984efece15f9d4
CTRL="$P4B/live_control"

rm -rf "$CTRL"; mkdir -p "$CTRL"
t0=$(date +%s.%N)
tar -C "$LIVE" --exclude=.git --exclude=.claude -cf - . | tar -x -C "$CTRL"
t1=$(date +%s.%N)
echo "CONTROL_COPY_SECONDS=$(echo "$t1 - $t0" | bc)"

export RL_REPO="$CTRL" CLAUDE_PROJECT_DIR="$CTRL" RL_FV="$CTRL/engine/forward_valuation"
export PYTHONHASHSEED=0
export PYTHONPATH="$CTRL:$CTRL/engine/rl_after:$CTRL/engine/forward_valuation:$CTRL/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
cd "$CTRL/engine/rl_after"

echo "== control build (RL_CONFIG_MODE=bake) =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 rl_export.py > "$P4B/logs/ctrl_build_out.txt" 2> "$P4B/logs/ctrl_build_err.txt"
echo "CTRL_BUILD_RC=$?  SECONDS=$(echo "$(date +%s.%N) - $t0" | bc)"
echo "live pinned board : $(python3 -c "import json;print(json.load(open('$CTRL/data/expected_boot.json'))['board'])")"
echo "control rebuilt   : $(md5sum "$CTRL/engine/rl_after/rl_app_data.json" | cut -d' ' -f1)"

echo "== control book =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 s4_matrix_M1v7.py > "$P4B/logs/ctrl_book_out.txt" 2> "$P4B/logs/ctrl_book_err.txt"
echo "CTRL_BOOK_RC=$?  SECONDS=$(echo "$(date +%s.%N) - $t0" | bc)"

echo "== control one_source_selftest =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 one_source_selftest.py > "$P4B/logs/ctrl_selftest_out.txt" 2> "$P4B/logs/ctrl_selftest_err.txt"
echo "CTRL_SELFTEST_RC=$?  SECONDS=$(echo "$(date +%s.%N) - $t0" | bc)"
grep -cE '^  PASS ' "$P4B/logs/ctrl_selftest_out.txt" | sed 's/^/CTRL PASS count: /'
grep -cE '^  FAIL ' "$P4B/logs/ctrl_selftest_out.txt" | sed 's/^/CTRL FAIL count: /'
echo "--- control non-PASS lines (truncated to 160 cols) ---"
grep -E '^  (FAIL|STALE) ' "$P4B/logs/ctrl_selftest_out.txt" | cut -c1-160 || echo "(none)"
