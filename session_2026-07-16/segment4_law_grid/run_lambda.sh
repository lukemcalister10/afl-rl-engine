#!/bin/bash
# LEG B SEGMENT-4 λ PRE-GATE — dev-shell run of rho_axis_v12.py (measures λ_ρ of the v1.2 construction).
# Seeds the workspace with the v1.2 engine (rl_model.py + _merged_recover.py + config_manifest.py), pinned env.
# Store/data/vendor were seeded by bootstrap and are UNCHANGED (FENCE: store b1fd0bce untouched).
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/config_manifest.py" "$WS/config_manifest.py"
cp -f "$HERE/session_2026-07-16/segment4_law_grid/rho_axis_v12.py" "$WS/"
cd "$WS"
export RL_REPO="$HERE"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
echo "workspace store md5: $(md5sum rl_model_data.json | cut -c1-8)  (expect b1fd0bce)"
echo "workspace engine md5: $(md5sum _merged_recover.py | cut -c1-8)  (v1.2 edited)"
echo "--- rho_axis_v12.py ---"
python3 rho_axis_v12.py
