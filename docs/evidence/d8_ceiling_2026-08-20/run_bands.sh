#!/bin/bash
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export D8REPO=$SP/wt-d8
cd $D8REPO
source tools/build_lock.sh && build_lock_acquire d8-bands 7200 || exit 1
echo "=== ORDER D8 — F2 (ladder unreachable) + F4 (ceiling v-inversions). READ-ONLY. ==="
D8TAPER=0 D8OUT=$SP/d8/out/BANDS_OFF.json python3 $SP/d8/d8_bands.py
D8TAPER=1 D8OUT=$SP/d8/out/BANDS_ON.json  python3 $SP/d8/d8_bands.py
build_lock_release
