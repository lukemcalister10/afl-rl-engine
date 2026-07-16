#!/bin/bash
# LEG B UNFUNDED — A/B byte-exact proof for the RL_UNCONSERVE toggle (dev-shell, store untouched).
#   (1) RL_UNCOMP=0                 board == 8d90c9ac  (kill-switch identity)
#   (2) toggle UNSET, map default   board == 8d90c9ac  (map inert by default; UNCOMP_S_DEFAULT=None)
#   (3) RL_UNCONSERVE=1, no s        board == 8d90c9ac  (flag inert while map inert)
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/config_manifest.py" "$WS/config_manifest.py"
cd "$WS"
export RL_REPO="$HERE"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
echo "workspace store md5 : $(md5sum rl_model_data.json | cut -c1-8)  (expect b1fd0bce)"
echo "workspace engine md5: $(md5sum _merged_recover.py | cut -c1-8)"
chk () { local lbl="$1"; local md="$2"; echo "$lbl board md5: $md  ->  $([ "$md" = "8d90c9ac" ] && echo 'PASS BYTE-EXACT' || echo 'FAIL <<<')"; }
rm -f rl_app_data.json; RL_UNCOMP=0 python3 rl_export.py >/tmp/ab1.log 2>&1
chk "(1) RL_UNCOMP=0        " "$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)"
rm -f rl_app_data.json; python3 rl_export.py >/tmp/ab2.log 2>&1
chk "(2) toggle unset/dflt  " "$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)"
rm -f rl_app_data.json; RL_UNCONSERVE=1 python3 rl_export.py >/tmp/ab3.log 2>&1
chk "(3) RL_UNCONSERVE=1,no s" "$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)"
