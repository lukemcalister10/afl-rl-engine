#!/usr/bin/env bash
# P4b FIRE DRILL — CONTROL: the same verifier against the CURRENT tree (this worktree, read-only),
# so the tag's contract red is attributed to the TAG, not to the instrument or the box.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
LIVE=/home/user/afl-rl-engine/.claude/worktrees/agent-a08984efece15f9d4
export RL_REPO="$LIVE" CLAUDE_PROJECT_DIR="$LIVE" RL_FV="$LIVE/engine/forward_valuation"
cd "$LIVE"
echo "== CONTROL: release_contract.py check on the CURRENT head (read-only) =="
python3 release_contract.py check
echo "CONTROL_RELEASE_CONTRACT_RC=$?"
echo
echo "== CONTROL: boot_guard.py on the CURRENT head (read-only) =="
python3 boot_guard.py p4b_control \
  "$LIVE/engine/rl_after/rl_model_data.json" \
  "$LIVE/engine/rl_after/_merged_recover.py" \
  "$LIVE/data/cm_400.pkl" \
  "$LIVE/LTI_REGISTER.md" 2>&1 | cut -c1-200
echo "CONTROL_GUARD5_RC=${PIPESTATUS[0]}"
