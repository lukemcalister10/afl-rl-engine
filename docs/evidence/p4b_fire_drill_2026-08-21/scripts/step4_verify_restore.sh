#!/usr/bin/env bash
# P4b FIRE DRILL — step 4: the tag's OWN scripted restore-verifier, run against the restored bytes.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
REST=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore
cd "$REST"
echo "== verify_restore.sh $REST =="
t0=$(date +%s.%N)
bash verify_restore.sh "$REST"
rc=$?
t1=$(date +%s.%N)
echo "VERIFY_RESTORE_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
