#!/bin/bash
# item-221 diagnostic: production-value blend (RL_UNCOMP_L2_S). Inert-board byte check + frozen-estimator grid.
set -uo pipefail
HERE=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$HERE/config_manifest.py" "$HERE/session_2026-07-16/uncompress/beta_measure.py" "$WS/"
cd "$WS"
export RL_REPO="$HERE" PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor PATH="/root/rl_venv312/bin:$PATH"
echo "=== INERT byte-check: no flags -> board must stay 8d90c9ac (L2 diagnostic code adds no default effect) ==="
rm -f rl_app_data.json; python3 rl_export.py >/tmp/l2inert.log 2>&1; echo "inert board md5: $(md5sum rl_app_data.json 2>/dev/null|cut -c1-8)"
echo "=== item-221 PRODUCTION-VALUE-LEVEL blend: frozen-estimator beta grid ==="
python3 beta_measure.py 2>&1 | grep -E 'beta'                       # L2 off = beta_c (base)
for s in 0.45 0.50 0.55 0.60; do RL_UNCOMP_L2_S=$s python3 beta_measure.py 2>&1 | grep -E 'beta'; done
echo "=== reference table at s=0.55 (V_ref_b per pos) ==="
RL_UNCOMP_L2_S=0.55 python3 -c "
import io,contextlib
g={}; buf=io.StringIO()
with contextlib.redirect_stdout(buf): exec(open('_merged_recover.py').read().split('print(\"=== AFTER')[0], g)
for L in buf.getvalue().splitlines():
    if 'RL_UNCOMP_L2' in L or 'V_ref_b' in L: print(L)
" 2>&1 | grep -v -i warning
