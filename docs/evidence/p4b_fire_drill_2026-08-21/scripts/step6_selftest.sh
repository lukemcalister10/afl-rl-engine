#!/usr/bin/env bash
# P4b FIRE DRILL — step 6: (a) confirm the CANONICAL-posture rebuild alone reproduces the tagged
# board (5.1 was overwritten by 5.2), which doubles as a build-twice determinism reading; then
# (b) rebuild the book and run the tag's OWN one_source_selftest.py on the rebuilt world.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
P4B=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b
REST="$P4B/restore"; BLD="$P4B/rebuild"
export RL_REPO="$BLD" CLAUDE_PROJECT_DIR="$BLD" RL_FV="$BLD/engine/forward_valuation"
export PYTHONHASHSEED=0
export PYTHONPATH="$BLD:$BLD/engine/rl_after:$BLD/engine/forward_valuation:$BLD/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
cd "$BLD/engine/rl_after"

echo "== 6.1 canonical rebuild #2 (RL_CONFIG_MODE=bake) — parity + build-twice determinism =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 rl_export.py > "$P4B/logs/rebuild_canonical2_stdout.txt" 2> "$P4B/logs/rebuild_canonical2_stderr.txt"
rc=$?
t1=$(date +%s.%N)
B2=$(md5sum "$BLD/engine/rl_after/rl_app_data.json" | cut -d' ' -f1)
echo "REBUILD_CANONICAL2_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
echo "tagged   : $(md5sum "$REST/data/rl_build/rl_app_data.json" | cut -d' ' -f1)"
echo "rebuild#2: $B2"

echo
echo "== 6.2 rebuild the BOOK (s4_matrix_M1v7.py) — the selftest's F2 precondition =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 s4_matrix_M1v7.py > "$P4B/logs/book_stdout.txt" 2> "$P4B/logs/book_stderr.txt"
rc=$?
t1=$(date +%s.%N)
echo "BOOK_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
echo "book md5 rebuilt : $(md5sum "$BLD/engine/rl_after/s4_matrix.json" | cut -d' ' -f1)"
echo "book md5 tagged  : $(md5sum "$REST/engine/rl_after/s4_matrix.json" | cut -d' ' -f1)"
tail -5 "$P4B/logs/book_stderr.txt"

echo
echo "== 6.3 one_source_selftest.py — the tag's OWN self-test, on the rebuilt restored world =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 one_source_selftest.py > "$P4B/logs/selftest_stdout.txt" 2> "$P4B/logs/selftest_stderr.txt"
rc=$?
t1=$(date +%s.%N)
echo "SELFTEST_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
echo "--- PASS/FAIL/STALE tally ---"
grep -cE '^  PASS ' "$P4B/logs/selftest_stdout.txt" | sed 's/^/PASS count: /'
grep -cE '^  FAIL ' "$P4B/logs/selftest_stdout.txt" | sed 's/^/FAIL count: /'
grep -cE '^  STALE ' "$P4B/logs/selftest_stdout.txt" | sed 's/^/STALE count: /'
echo "--- non-PASS lines ---"
grep -E '^  (FAIL|STALE) ' "$P4B/logs/selftest_stdout.txt" || echo "(none)"
echo "--- last 12 lines ---"
tail -12 "$P4B/logs/selftest_stdout.txt"
