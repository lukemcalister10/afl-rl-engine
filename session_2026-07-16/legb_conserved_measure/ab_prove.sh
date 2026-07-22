#!/bin/bash
# LEG B CONSERVED — A/B byte-exact proof (dev-shell, store untouched). CONSERVED reuses the SAME
# engine as unfunded; the toggle stays UNSET throughout, so behaviour is the shipped path.
#   (1) RL_UNCOMP=0                 board == 8d90c9ac  (kill-switch identity)
#   (2) toggle UNSET, map default   board == 8d90c9ac  (map inert by default; UNCOMP_S_DEFAULT=None)
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cd "$WS"
export RL_REPO="$HERE"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
echo "workspace store md5 : $(md5sum rl_model_data.json | cut -c1-8)  (expect b1fd0bce)"
echo "workspace engine md5: $(md5sum _merged_recover.py | cut -c1-8)"
chk () { local lbl="$1"; local md="$2"; echo "$lbl board md5: $md  ->  $([ "$md" = "8d90c9ac" ] && echo 'PASS BYTE-EXACT' || echo 'FAIL <<<')"; }
rm -f rl_app_data.json; RL_UNCOMP=0 python3 rl_export.py >/tmp/cab1.log 2>&1
chk "(1) RL_UNCOMP=0        " "$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)"
rm -f rl_app_data.json; python3 rl_export.py >/tmp/cab2.log 2>&1
chk "(2) toggle unset/dflt  " "$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)"
