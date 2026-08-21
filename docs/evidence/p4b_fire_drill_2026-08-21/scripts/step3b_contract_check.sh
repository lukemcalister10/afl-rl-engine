#!/usr/bin/env bash
# P4b FIRE DRILL — step 3.3 (corrected): the tag's OWN release-state VERIFIER entry point.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
REST=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore
export RL_REPO="$REST" CLAUDE_PROJECT_DIR="$REST" RL_FV="$REST/engine/forward_valuation"
cd "$REST"
echo "== release_contract.py check  (verify(), fenced mode 'gate') =="
t0=$(date +%s.%N)
python3 release_contract.py check
rc=$?
t1=$(date +%s.%N)
echo "RELEASE_CONTRACT_CHECK_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
