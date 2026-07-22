#!/bin/bash
# LEG B SEGMENT-5 — A/B RE-PROVE + THE GRID (directive steps 1-2). Dev-shell (bypasses run_panel/ship_gates
# boot-guard: the engine head moved, expected_boot re-pins only at the regeneration commit). Store/data/
# vendor seeded by the initial bootstrap and UNCHANGED (FENCE: store b1fd0bce untouched).
#   step 1  A/B: RL_UNCOMP=0 board == 8d90c9ac BYTE-EXACT (the kill-switch identity).
#   step 2  frozen fit_beta (beta_measure.py, verbatim) at map-off (beta_c) and each grid s; owner bar 0.80.
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/config_manifest.py" "$WS/config_manifest.py"
cp -f "$HERE/session_2026-07-16/segment5_law_grid/beta_measure.py" "$WS/"
cd "$WS"
export RL_REPO="$HERE"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
echo "workspace store md5 : $(md5sum rl_model_data.json | cut -c1-8)  (expect b1fd0bce)"
echo "workspace engine md5: $(md5sum _merged_recover.py | cut -c1-8)  (v1.3 d=0.25)"
echo "UNCOMP_DECAY in seeded engine: $(python3 -c "import re;print(re.search(r'^UNCOMP_DECAY\s*=\s*([0-9.]+)',open('rl_model.py').read(),re.M).group(1))")"

echo ""
echo "================= STEP 1 — A/B RE-PROVE (RL_UNCOMP=0 -> 8d90c9ac BYTE-EXACT) ================="
rm -f rl_app_data.json; RL_UNCOMP=0 python3 rl_export.py >/tmp/s5_off.log 2>&1
_off=$(md5sum rl_app_data.json 2>/dev/null | cut -c1-8)
echo "RL_UNCOMP=0 board md5: $_off  (expect 8d90c9ac)  ->  $([ "$_off" = "8d90c9ac" ] && echo 'A/B PASS BYTE-EXACT' || echo 'A/B FAIL <<<')"

echo ""
echo "================= STEP 2 — THE GRID (frozen fit_beta; owner bar beta >= 0.80) ================="
echo "point       beta      CI_lo    CI_hi    width    n      >=0.80  CI>1.0  w<=.35  n>=120"
# beta_c (map OFF): no RL_UNCOMP_S => UNCOMP_S_DEFAULT=None => map inert
RL_UNCOMP=0 python3 beta_measure.py 2>&1 | grep -E '^s=' | sed 's/^/beta_c  /'
for s in 0.55 0.60 0.65 0.70; do
  RL_UNCOMP_S=$s python3 beta_measure.py 2>&1 | grep -E '^s=' | sed "s/^/s=$s   /"
done
echo "(bar = OWNER-SET 0.80; selection = smallest s with beta point >= 0.80; empty => HALT with this table)"
