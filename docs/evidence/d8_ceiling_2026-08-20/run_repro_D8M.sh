#!/bin/bash
# MEASUREMENT SEAT — THE D8 REPRODUCTION. Both boards, byte-exact, before any table is read.
# The D8 seat's run_price.sh recipe, carried: same disposable FV builder, same d8_build.py driver
# (md5 da7d80ce4a45fafe1a8ec538fdfe2b50, byte-copied), strictly sequential, under tools/build_lock.sh.
# The driver drops RL_BUILD_LOCK_HELD from the CHILD env — the D8 claims' disclosed finding: the lock
# exports it and config_manifest.enforce() rejects any unknown RL_-prefixed var, so a canonical-mode
# build launched from inside the lock would HALT. The lock itself stays held by this shell's fd.
# NOTHING IS ADOPTED. NO BOARD PIN MOVES.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export D8REPO=$SP/wt-d8n
cd $D8REPO
echo "=== D8 MEASUREMENT SEAT — REPRODUCTION OF BOTH BOARDS ==="
echo "  worktree: $D8REPO @ $(git rev-parse --short HEAD)"
echo "  engine  : $(md5sum engine/rl_after/_merged_recover.py | cut -c1-32)  (D8 tree: 338a790b773cfbbff0e1283794c72efe)"
echo "  rl_model: $(md5sum engine/rl_after/rl_model.py        | cut -c1-32)  (pin 6fe7c4155866d80e8045bed2d3bf2802)"
echo "  store   : $(md5sum engine/rl_after/rl_model_data.json | cut -c1-32)  (pin cc02567f80bef39228f25854d121a766)"
echo "  q97m    : $(md5sum data/q97m.pkl                      | cut -c1-32)  (pin cfdc73216c099e5e8f1fda3968f31c00)"
echo
source tools/build_lock.sh && build_lock_acquire d8-measure 7200 || exit 1
D8TAG=M_OFF_DEV D8MODE=dev       D8ENV='{}'                      D8OUT=$SP/d8m/out/M_OFF_DEV python3 $SP/d8m/d8_build.py
D8TAG=M_OFF_CAN D8MODE=canonical D8ENV='{}'                      D8OUT=$SP/d8m/out/M_OFF_CAN python3 $SP/d8m/d8_build.py
D8TAG=M_ON_DEV  D8MODE=dev       D8ENV='{"RL_O33_TAPEROFF":"1"}' D8OUT=$SP/d8m/out/M_ON_DEV  python3 $SP/d8m/d8_build.py
build_lock_release
echo
echo "=== BOARD IDS, AGAINST THE D8 CLAIMS ==="
for T in M_OFF_DEV M_OFF_CAN M_ON_DEV; do
  printf '  %-10s %s\n' "$T" "$(python3 -c "import json;print(json.load(open('$SP/d8m/out/$T.meta.json'))['board_md5'])" 2>/dev/null || echo NO-META)"
done
echo "  EXPECTED  M_OFF_DEV = M_OFF_CAN = a05fe951f78482c70520480e184c80ec   (THE LIVE BOARD / THE BASE)"
echo "  EXPECTED  M_ON_DEV                = 5ea978f7b6a073abb2012f10cccbc3e3   (THE PRICED CANDIDATE)"
