#!/bin/bash
set -e
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=$SP/ws/rl_after:/home/claude/rl_vendor
export RL_REPO=/home/user/afl-rl-engine
export RL_FV=$RL_REPO/engine/forward_valuation
export RL_WORKDIR=$SP/ws/rl_after
export RL_VENDOR=/home/claude/rl_vendor
export RL_V0SURF_PKL=$RL_REPO/data/v0surf.pkl
export RL_OUT=$SP
python3 $SP/ruck_cf2_main.py
