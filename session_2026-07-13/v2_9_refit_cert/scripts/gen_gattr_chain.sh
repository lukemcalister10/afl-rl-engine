#!/bin/bash
# Generate the G-ATTR cumulative chain on the WIRED engine (env-gated levers; no patching).
cd /home/claude/rl_workspace/rl_after
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
BP=/home/user/afl-rl-engine/session_2026-07-13/v2_9_continuation/scripts/board_pass.py
O=/home/user/afl-rl-engine/session_2026-07-13/v2_9_refit_cert/out
echo "TARGETS: base n=804 sum=723075 emmett1178 bont3721 gawn2538 butters6060 | comb bont3664 gawn2518 butters5986 emmett851"
RL_PVCADOPT=0 RL_MSD_POOL_EXCL=0 RL_DIAL14=0 RL_AGE=0 RL_L5_PICKLESS=0 python3 "$BP" "$O/g_base.json" base 2>/dev/null
RL_PVCADOPT=1 RL_MSD_POOL_EXCL=0 RL_DIAL14=0 RL_AGE=0 RL_L5_PICKLESS=0 python3 "$BP" "$O/g_L1.json" +L1 2>/dev/null
RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=0 RL_AGE=0 RL_L5_PICKLESS=0 python3 "$BP" "$O/g_L1L4.json" +L1+L4 2>/dev/null
RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=1 RL_AGE=0 RL_L5_PICKLESS=0 python3 "$BP" "$O/g_L1L4L2.json" +L1+L4+L2 2>/dev/null
RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=1 RL_AGE=1 RL_L5_PICKLESS=0 python3 "$BP" "$O/g_L1L4L2L3.json" +L1+L4+L2+L3 2>/dev/null
RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=1 RL_AGE=1 RL_L5_PICKLESS=1 python3 "$BP" "$O/g_full.json" FULL+L5 2>/dev/null
echo "DONE gattr chain"
