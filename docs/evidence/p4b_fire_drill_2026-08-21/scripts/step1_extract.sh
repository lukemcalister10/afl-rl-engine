#!/usr/bin/env bash
# P4b FIRE DRILL — step 1: restore the tagged BYTES into a scratch checkout.
set -uo pipefail
SRC=/home/user/afl-rl-engine/.claude/worktrees/agent-a08984efece15f9d4
P4B=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b
TAG=baked-v2.11-2026-08-20
REST="$P4B/restore"

rm -rf "$REST"
mkdir -p "$REST"
t0=$(date +%s.%N)
git -C "$SRC" archive --format=tar "$TAG" | tar -x -C "$REST"
rc=$?
t1=$(date +%s.%N)
echo "extract_rc=$rc"
echo "STEP1_EXTRACT_SECONDS=$(echo "$t1 - $t0" | bc)"
echo "files=$(find "$REST" -type f | wc -l)"
echo "bytes=$(du -sb "$REST" | cut -f1)"
