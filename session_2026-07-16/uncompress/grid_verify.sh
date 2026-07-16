#!/bin/bash
# Full s-grid beta measurement (frozen estimator) + hygiene byte-safety check.
set -uo pipefail
HERE=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$HERE/config_manifest.py" "$HERE/session_2026-07-16/uncompress/beta_measure.py" "$WS/"
cd "$WS"
export RL_REPO="$HERE" PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor PATH="/root/rl_venv312/bin:$PATH"
echo "=== HYGIENE byte-safety: map-inert board must stay 8d90c9ac after the _coreM1 branch deletion ==="
rm -f rl_app_data.json; python3 rl_export.py >/tmp/hyg.log 2>&1; echo "inert board md5: $(md5sum rl_app_data.json 2>/dev/null|cut -c1-8)"
echo "=== FROZEN-ESTIMATOR s-GRID (PLAN §7 acceptance leg_b.beta_proven27; gate: pt>=0.85) ==="
python3 beta_measure.py 2>&1 | grep -E 'beta'          # OFF = beta_c
for s in 0.45 0.50 0.60; do RL_UNCOMP_S=$s python3 beta_measure.py 2>&1 | grep -E 'beta'; done
