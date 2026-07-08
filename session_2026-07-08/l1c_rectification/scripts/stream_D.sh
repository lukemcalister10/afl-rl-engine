#!/bin/bash
set -e
L=/home/user/afl-rl-engine/session_2026-07-08/l1c_rectification
HERE=/home/user/afl-rl-engine
RL_REPO="$HERE" python3 "$HERE/boot_guard.py" stream_D /home/claude/rl_workspace/rl_after/rl_model_data.json /home/claude/rl_workspace/rl_after/_merged_recover.py
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export PATH="/root/rl_venv312/bin:$PATH"
python3 rl_export.py > $L/out/rl_export_w07.log 2>&1
bash $L/scripts/run_matrix.sh $L/out/s4_matrix_w07.json RL_YCRED_W=0.7
