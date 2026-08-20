#!/bin/bash
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export D8REPO=$SP/wt-d8
mkdir -p $SP/d8/out
cd $D8REPO
source tools/build_lock.sh && build_lock_acquire d8-base 7200 || exit 1
D8TAG=BASE_CANON D8MODE=canonical D8OUT=$SP/d8/out/BASE_CANON python3 $SP/d8/d8_build.py
D8TAG=BASE_DEV   D8MODE=dev       D8OUT=$SP/d8/out/BASE_DEV   python3 $SP/d8/d8_build.py
build_lock_release
