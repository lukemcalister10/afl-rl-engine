#!/bin/bash
# THE D8 ADOPTION — THE PROOFS. F1 (BARE) and F2 (KILL-SWITCH), measured on the EDITED tree.
# The D8 pricing seat's own recipe, carried: the accepted disposable FV builder
# (test_fv_provenance._run_build), the byte-carried d8_build.py driver (da7d80ce, +the srcmd5
# preservation noted in the file), strictly sequential, ONE WRITER under tools/build_lock.sh.
# The driver drops RL_BUILD_LOCK_HELD from the CHILD env — the lock exports it and
# config_manifest.enforce() rejects any unknown RL_-prefixed var, so a canonical-mode build launched
# from inside the lock would HALT. The lock itself stays held by this shell's fd.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/d8adopt
export D8REPO=/home/user/afl-rl-engine
mkdir -p $SP/out
cd $D8REPO
echo "=== THE D8 ADOPTION — THE PROOFS. PREREG_ADOPTION.md governs (16ec23b). ==="
echo "  commit  : $(git rev-parse --short HEAD)  ($(git rev-parse HEAD))"
echo "  engine  : $(md5sum engine/rl_after/_merged_recover.py | cut -c1-32)  (was 338a790b773cfbbff0e1283794c72efe pre-edit)"
echo "  rl_model: $(md5sum engine/rl_after/rl_model.py        | cut -c1-32)  (pin 6fe7c4155866d80e8045bed2d3bf2802, must be UNMOVED)"
echo "  store   : $(md5sum engine/rl_after/rl_model_data.json | cut -c1-32)  (pin cc02567f80bef39228f25854d121a766, must be UNMOVED)"
echo "  q97m    : $(md5sum data/q97m.pkl                      | cut -c1-32)  (pin cfdc73216c099e5e8f1fda3968f31c00, FROZEN)"
echo "  v0surf  : $(md5sum data/v0surf.pkl                    | cut -c1-32)  (pin 5dd34ca82735f5c8f021b1c7320df8f8)"
echo
echo "  P1 BARE       expects 5ea978f7b6a073abb2012f10cccbc3e3  total 693753  n=804"
echo "  P2 KILLSWITCH expects a05fe951f78482c70520480e184c80ec  total 664949  n=804"
echo
source tools/build_lock.sh && build_lock_acquire d8-adopt 7200 || exit 1
D8TAG=BARE_DEV  D8MODE=dev       D8ENV='{}'                      D8OUT=$SP/out/BARE_DEV  python3 $SP/d8_build.py
D8TAG=BARE_CANON D8MODE=canonical D8ENV='{}'                     D8OUT=$SP/out/BARE_CANON python3 $SP/d8_build.py
D8TAG=KILL_DEV  D8MODE=dev       D8ENV='{"RL_O33_TAPEROFF":"0"}' D8OUT=$SP/out/KILL_DEV  python3 $SP/d8_build.py
build_lock_release
echo
echo "=== BOARD IDS ==="
for T in BARE_DEV BARE_CANON KILL_DEV; do
  printf '  %-11s %s\n' "$T" "$(python3 -c "import json;print(json.load(open('$SP/out/$T.meta.json'))['board_md5'])" 2>/dev/null || echo NO-META)"
done
