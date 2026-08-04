#!/usr/bin/env bash
# #306 L6 RE-ENTRY — one pass under R-H/R-I/N19 UNCHANGED. Strictly serial; preboot before every act.
set -uo pipefail
P="${1:?pass number}"
R=/home/user/afl-rl-engine
O=$R/docs/evidence/exec_306_zlaarm/l6
W=/home/claude/rl_workspace/rl_after
export RL_VENV=/root/rl_venv312; export PATH="$RL_VENV/bin:$PATH"
export RL_REPO=$R RL_FV=$R/engine/forward_valuation
export PYTHONPATH=$W:/home/claude/rl_vendor
L=$O/pass${P}.log
say(){ echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$L"; }
: > "$L"
say "PASS $P — host $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2 | xargs) stepping $(grep -m1 stepping /proc/cpuinfo | awk '{print $3}') uptime $(uptime | grep -o 'up [^,]*')"
bash $R/tools/preboot_assert.sh >>"$L" 2>&1 || { say "PREBOOT HALT"; exit 1; }
bash $R/bootstrap.sh >>"$L" 2>&1 || { say "BOOTSTRAP HALT"; exit 1; }
say "bootstrap OK (Guard 5)"
say "installed curve payload: $(python3 -c "
import json,hashlib
c=json.load(open('$R/engine/rl_after/pvc_curve_v2.json'))['curve']
print(hashlib.md5(json.dumps({str(k):int(round(v)) for k,v in c.items()},sort_keys=True).encode()).hexdigest()[:8])")"
say "refit (declared lane, bake) ..."
cd $W
RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 RL_V0_LENS=1 python3 \
  $R/session_2026-07-18/legf6/scripts/refit_v0surf.py --bake >>"$L" 2>&1 || { say "REFIT HALT"; exit 1; }
SURF=$(md5sum $R/data/v0surf.pkl | cut -d' ' -f1)
say "surface baked: $SURF"
mkdir -p $O/pass${P}_surface && cp $R/data/v0surf.pkl $O/pass${P}_surface/v0surf.pkl
say "board ..."
RL_CONFIG_MODE=bake python3 rl_export.py >>"$L" 2>&1 || { say "BOARD HALT"; exit 1; }
BOARD=$(md5sum $W/rl_app_data.json | cut -d' ' -f1)
say "board: $BOARD"
say "book ..."
RL_CONFIG_MODE=bake python3 s4_matrix_M1v7.py >>"$L" 2>&1 || { say "BOOK HALT"; exit 1; }
say "book done"
say "selftest ..."
python3 one_source_selftest.py > $O/pass${P}_selftest.txt 2>&1
say "selftest rc=$?"
grep -iE "G-?Y0|year.?zero|gy0" $O/pass${P}_selftest.txt | head -8 | tee -a "$L"
say "PASS $P COMPLETE — surface $SURF board $BOARD"
