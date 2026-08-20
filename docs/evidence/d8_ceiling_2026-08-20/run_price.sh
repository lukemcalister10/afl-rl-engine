#!/bin/bash
# ORDER D8 — the five builds. STRICTLY SEQUENTIAL, one writer, under tools/build_lock.sh.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export D8REPO=$SP/wt-d8
mkdir -p $SP/d8/out
cd $D8REPO
echo "=== ORDER D8 BUILDS — PREREG_D8.md governs. PRICED, NOT ADOPTED. ==="
echo "  engine  : $(md5sum engine/rl_after/_merged_recover.py | cut -c1-32)  (base was 5ac6780f3c4931edcaa527576bbdfb88)"
echo "  rl_model: $(md5sum engine/rl_after/rl_model.py        | cut -c1-32)  (pin 6fe7c4155866d80e8045bed2d3bf2802, UNMOVED)"
echo "  store   : $(md5sum engine/rl_after/rl_model_data.json | cut -c1-32)  (pin cc02567f80bef39228f25854d121a766)"
echo "  q97m    : $(md5sum data/q97m.pkl                      | cut -c1-32)  (pin cfdc73216c099e5e8f1fda3968f31c00, FROZEN)"
echo
source tools/build_lock.sh && build_lock_acquire d8-price 7200 || exit 1
D8TAG=OFF_DEV_1  D8MODE=dev       D8ENV='{}'                      D8OUT=$SP/d8/out/OFF_DEV_1  python3 $SP/d8/d8_build.py
D8TAG=OFF_DEV_2  D8MODE=dev       D8ENV='{}'                      D8OUT=$SP/d8/out/OFF_DEV_2  python3 $SP/d8/d8_build.py
D8TAG=OFF_CANON  D8MODE=canonical D8ENV='{}'                      D8OUT=$SP/d8/out/OFF_CANON  python3 $SP/d8/d8_build.py
D8TAG=ON_DEV_1   D8MODE=dev       D8ENV='{"RL_O33_TAPEROFF":"1"}' D8OUT=$SP/d8/out/ON_DEV_1   python3 $SP/d8/d8_build.py
D8TAG=ON_DEV_2   D8MODE=dev       D8ENV='{"RL_O33_TAPEROFF":"1"}' D8OUT=$SP/d8/out/ON_DEV_2   python3 $SP/d8/d8_build.py
build_lock_release
echo
echo "=== BOARD IDS ==="
for T in OFF_DEV_1 OFF_DEV_2 OFF_CANON ON_DEV_1 ON_DEV_2; do
  printf '%-10s %s\n' "$T" "$(python3 -c "import json;print(json.load(open('$SP/d8/out/$T.meta.json'))['board_md5'])" 2>/dev/null || echo NO-META)"
done
echo
echo "=== EXPECTED (PREREG_D8 F1/F3) ==="
echo "  OFF_DEV_1 == OFF_DEV_2 == OFF_CANON == a05fe951f78482c70520480e184c80ec   (F1 no-op, F3 determinism)"
echo "  ON_DEV_1  == ON_DEV_2  == THE PRICED BOARD                                (F3 determinism)"
