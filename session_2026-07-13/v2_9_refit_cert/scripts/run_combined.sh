#!/bin/bash
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
# all lever gates default-ON (the candidate) — explicit for clarity
export RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=1 RL_AGE=1 RL_L5_PICKLESS=1
python3 /home/user/afl-rl-engine/session_2026-07-13/v2_9_continuation/scripts/board_pass.py \
  /home/user/afl-rl-engine/session_2026-07-13/v2_9_refit_cert/out/g_full.json FULL+L5 2>/dev/null
echo "COMBINED_DONE rc=$?"
