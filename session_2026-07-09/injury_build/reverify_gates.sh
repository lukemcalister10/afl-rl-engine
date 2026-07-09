#!/bin/bash
# Re-seed the shipped candidate board (gate-mode, matching ship_gates' B4 subprocess) into BOTH the repo
# (data/rl_build, committed) and the shipped path (/home/claude/rl_build), then re-run the self-test + gates.
set -e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-09/injury_build/artifacts
python3 $REPO/session_2026-07-09/injury_build/restamp_head.py >/dev/null
bash $REPO/bootstrap.sh >/dev/null 2>&1
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor

echo "### building candidate board in GATE mode (matches ship_gates B4 subprocess)"
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null || true
RL_REPO=$REPO RL_CONFIG_MODE=gate python3 rl_export.py >/dev/null 2>&1
BMD5=$(md5sum rl_app_data.json | cut -c1-8)
echo "gate-mode candidate board md5=$BMD5"
cp -f rl_app_data.json "$REPO/data/rl_build/rl_app_data.json"          # repo (committed) shipped board
cp -f rl_app_data.json /home/claude/rl_build/rl_app_data.json          # runtime shipped board (B4 comparand)

echo "### ship_gates re-run"
cd "$REPO"
RL_REPO="$REPO" python3 ship_gates_check.py > "$ART/ship_gates.txt" 2>&1 || true
grep -E "VERDICT|^A2|^A3 |^A12|^B1 |^B3 |^B4 |^B5 " "$ART/ship_gates.txt"
echo "### panel"; bash "$REPO/run_panel.sh" 2>&1 | tail -1
echo "### REVERIFY DONE  (shipped board md5=$BMD5)"
