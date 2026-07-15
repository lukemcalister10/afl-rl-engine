#!/bin/bash
# Build the board via rl_export.py in the workspace, print md5. Args: none (uses ambient env for CPU pins).
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO="/home/user/afl-rl-engine"
WS=/home/claude/rl_workspace/rl_after
export PYTHONPATH=$WS:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
cd "$WS"
rm -f rl_app_data.json
t0=$(date +%s)
python3 rl_export.py > /tmp/rlexport.$$.log 2>&1
rc=$?
t1=$(date +%s)
echo "rl_export exit=$rc wall=$((t1-t0))s"
if [ -f rl_app_data.json ]; then
  echo "board md5: $(md5sum rl_app_data.json | cut -d' ' -f1)"
else
  echo "board: MISSING"
  tail -20 /tmp/rlexport.$$.log
fi
