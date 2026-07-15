#!/bin/bash
# Build the board (rl_app_data.json) in the workspace exactly as CI's build step does, then md5 it.
# Pass OPENBLAS_CORETYPE / OPENBLAS_NUM_THREADS via the environment to force a kernel.
set -euo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
export RL_REPO="$HERE" RL_CONFIG_MODE=bake
export PYTHONHASHSEED=0
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
cd "$WS"
# report the kernel this build will actually use (numpy import happens inside rl_export)
python3 "$HERE/session_2026-07-14/determinism_fix/kernel_probe.py" | grep -E "RESOLVED|env"
python3 rl_export.py >/tmp/rlexport_$$.log 2>&1 || { echo "rl_export FAILED"; tail -30 /tmp/rlexport_$$.log; exit 1; }
M=$(md5sum "$WS/rl_app_data.json" | cut -d' ' -f1)
echo "BOARD_MD5(built this run) = $M"
