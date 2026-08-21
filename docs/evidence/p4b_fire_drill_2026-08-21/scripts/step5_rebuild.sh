#!/usr/bin/env bash
# P4b FIRE DRILL — step 5 (SECONDARY, best-effort): rebuild the board FROM SOURCE at the tag and
# compare the rebuilt board md5 to the tagged board. Per PLAN_v6 4b a mismatch is a REPRODUCIBILITY
# finding, not a rollback failure. Runs in a COPY so the restored bytes stay pristine.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
P4B=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b
REST="$P4B/restore"
BLD="$P4B/rebuild"

echo "== 5.0 copy the restored tree to a rebuild sandbox =="
rm -rf "$BLD"
t0=$(date +%s.%N)
cp -a "$REST" "$BLD"
t1=$(date +%s.%N)
echo "COPY_SECONDS=$(echo "$t1 - $t0" | bc)"
echo "tagged board (pristine restore): $(md5sum "$REST/data/rl_build/rl_app_data.json" | cut -d' ' -f1)"
echo "engine/rl_after copy in tree   : $(md5sum "$BLD/engine/rl_after/rl_app_data.json" | cut -d' ' -f1)"

export RL_REPO="$BLD" CLAUDE_PROJECT_DIR="$BLD" RL_FV="$BLD/engine/forward_valuation"
export PYTHONHASHSEED=0
export PYTHONPATH="$BLD:$BLD/engine/rl_after:$BLD/engine/forward_valuation:$BLD/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
cd "$BLD/engine/rl_after"

echo
echo "== 5.1 CANONICAL posture first: RL_CONFIG_MODE=bake (the fenced build the estate requires) =="
t0=$(date +%s.%N)
RL_CONFIG_MODE=bake python3 rl_export.py > "$P4B/logs/rebuild_canonical_stdout.txt" 2> "$P4B/logs/rebuild_canonical_stderr.txt"
rc_canon=$?
t1=$(date +%s.%N)
echo "REBUILD_CANONICAL_RC=$rc_canon   SECONDS=$(echo "$t1 - $t0" | bc)"
echo "--- last 20 lines of stderr ---"
tail -20 "$P4B/logs/rebuild_canonical_stderr.txt"

echo
echo "== 5.2 BARE posture: no model-semantics RL_* at all (the tag's own _bake_note claim) =="
t0=$(date +%s.%N)
python3 rl_export.py > "$P4B/logs/rebuild_bare_stdout.txt" 2> "$P4B/logs/rebuild_bare_stderr.txt"
rc_bare=$?
t1=$(date +%s.%N)
echo "REBUILD_BARE_RC=$rc_bare   SECONDS=$(echo "$t1 - $t0" | bc)"
echo "--- last 20 lines of stderr ---"
tail -20 "$P4B/logs/rebuild_bare_stderr.txt"

echo
echo "== 5.3 PARITY COMPARISON =="
TAGGED=$(md5sum "$REST/data/rl_build/rl_app_data.json" | cut -d' ' -f1)
REBUILT=$(md5sum "$BLD/engine/rl_after/rl_app_data.json" | cut -d' ' -f1)
echo "tagged  board md5 : $TAGGED"
echo "rebuilt board md5 : $REBUILT"
if [ "$TAGGED" = "$REBUILT" ]; then
  echo "REBUILD PARITY: BYTE-EXACT  (bonus — the tag is a recipe as well as bytes)"
else
  echo "REBUILD PARITY: MISMATCH    (REPRODUCIBILITY finding per PLAN_v6 4b — NOT a rollback failure)"
  echo "sizes: tagged $(stat -c%s "$REST/data/rl_build/rl_app_data.json")  rebuilt $(stat -c%s "$BLD/engine/rl_after/rl_app_data.json")"
fi
