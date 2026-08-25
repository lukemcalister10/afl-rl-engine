#!/usr/bin/env bash
# ORDER 45 falsifiers 1+2 (PREREG_ORDER45.md §5). Gate mode rejects divergent overrides, so the
# kill-switch proof rides a manifest that DECLARES RL_O45='0' (restamped coherently), then the
# manifest is restored to the landing posture RL_O45='1' for the with-net emit.
set -eu
export PATH="/root/rl_venv312/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
SC=/home/user/arm2_norec
# Review finding NEW-3: any failure between the '0' flip and the '1' restore would strand the
# candidate root COHERENTLY sealed in the net-OFF posture. The trap restores the landing posture
# on EVERY exit path; the pre-flip check (manifest '1', config 29fdfd1e...) remains mandatory.
trap 'python3 "$SC/set_o45_manifest.py" 1 >/dev/null 2>&1 || true' EXIT
cd "$SC/wsF/rl_after"
find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

echo "== FALSIFIER 1: kill-switch proof (manifest RL_O45='0' => 543bf900 byte-exact) =="
python3 "$SC/set_o45_manifest.py" 0
rm -f rl_app_data.json
env RL_CONFIG_MODE=gate RL_REPO="$SC/root_final" RL_FV="$SC/root_final/engine/forward_valuation" \
  RL_CM_PKL="$SC/root_final/data/cm_400.pkl" RL_Q97M_PKL="$SC/root_final/data/q97m.pkl" \
  PYTHONPATH="$SC/wsF/rl_after:/home/claude/rl_vendor" \
  python3 rl_export.py > "$SC/emit_o45_off.log" 2>&1
md5sum rl_app_data.json | tee "$SC/board_o45_off_md5.txt"
cp rl_app_data.json "$SC/board_o45_off.json"
# REVIEW NEW-7: rl_export execs the engine inside a discarded StringIO, so NO module-level print
# (D7's included) ever reaches these logs — an announce-grep here is a VACUOUS pass and its ON-leg
# mirror a guaranteed false RED. Both are RETIRED. Installation is proven by what the boards SAY:
# the OFF board byte-equals 543bf900 and the ON board differs from it exactly as predicted.
OFF=$(cut -d' ' -f1 "$SC/board_o45_off_md5.txt"); REF=$(cut -d' ' -f1 "$SC/board_final_md5.txt")
echo "off-board $OFF vs 543bf900-ref $REF"
if [ "$OFF" != "$REF" ]; then echo "FALSIFIER 1 RED: kill-switch-off board != 543bf900"; exit 5; fi
echo "FALSIFIER 1 GREEN"

echo "== FALSIFIER 2: the with-net emit (manifest RL_O45='1', the landing posture) =="
python3 "$SC/set_o45_manifest.py" 1
rm -f rl_app_data.json
env RL_CONFIG_MODE=gate RL_REPO="$SC/root_final" RL_FV="$SC/root_final/engine/forward_valuation" \
  RL_CM_PKL="$SC/root_final/data/cm_400.pkl" RL_Q97M_PKL="$SC/root_final/data/q97m.pkl" \
  PYTHONPATH="$SC/wsF/rl_after:/home/claude/rl_vendor" \
  python3 rl_export.py > "$SC/emit_o45_on.log" 2>&1
md5sum rl_app_data.json | tee "$SC/board_o45_md5.txt"
cp rl_app_data.json "$SC/board_o45.json"
ON=$(cut -d' ' -f1 "$SC/board_o45_md5.txt")
if [ "$ON" = "$OFF" ]; then echo "FALSIFIER 2 RED: the ON board equals the OFF board — the wrapper did not act"; exit 4; fi
echo "wrapper installation proven by the boards: ON $ON != OFF $OFF (self-test binds ON to the filed prediction)"
echo EMITS DONE
