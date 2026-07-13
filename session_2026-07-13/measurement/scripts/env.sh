#!/bin/bash
# Shared env for the measurement build. TAGGED BOARD (store b0c39d78 / board 81e48293).
# Mirrors run_panel.sh exactly so ev() reproduces the shipped numeraire panel.
SP=/tmp/claude-0/-home-user-afl-rl-engine/3f426bde-6344-5c1b-926e-458effd5209d/scratchpad
export WS_TAG=$SP/ws_tag
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=$WS_TAG:/home/claude/rl_vendor
export RL_REPO=/home/user/afl-rl-engine
