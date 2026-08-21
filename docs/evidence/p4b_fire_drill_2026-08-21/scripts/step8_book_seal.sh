#!/usr/bin/env bash
# P4b FIRE DRILL — step 8: the BOOK leg. The raw s4_matrix.json md5 is not a pinned identity;
# data/book_stable_seal.json pins stable_sha256 over the STABLE-KEYED content. The tag's own
# re-seal instrument has a --check mode that regenerates the book in gate mode and re-verifies
# the committed seal, writing nothing.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
P4B=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b
REST="$P4B/restore"
export RL_REPO="$REST" CLAUDE_PROJECT_DIR="$REST"
t0=$(date +%s.%N)
python3 "$REST/docs/evidence/bake_2026-08-20/reseal_bake.py" --check
rc=$?
t1=$(date +%s.%N)
echo "BOOK_SEAL_CHECK_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
