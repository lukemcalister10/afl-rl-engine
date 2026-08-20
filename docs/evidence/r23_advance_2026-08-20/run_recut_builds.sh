#!/bin/bash
# ACT 1 — THE SHEET RE-CUT REBUILD. The D8 adoption's own recipe, carried byte-for-byte:
# the accepted disposable FV builder (test_fv_provenance._run_build) via the byte-carried d8_build.py
# driver, PYTHONHASHSEED=0, BLAS threads pinned to 1, staging into a throwaway dir, writing nothing
# under the repo, strictly sequential, ONE WRITER under tools/build_lock.sh.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r23_work
export D8REPO=/home/user/afl-rl-engine
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd $D8REPO
echo "=== ACT 1 REBUILD — THE SHEET RE-CUT. PREREG b86bc9e governs. ==="
echo "  commit  : $(git rev-parse --short HEAD)  ($(git rev-parse HEAD))"
echo "  engine  : $(md5sum engine/rl_after/_merged_recover.py | cut -c1-32)  (was 3cfc4325aa323b7f26594cb2a202a976 pre-recut)"
echo "  sheet   : $(md5sum docs/owner_annotations/SITTER_2026_v1.csv | cut -c1-32)  (was b26798c35adcd9bda5cef50ff2c884da)"
echo "  rl_model: $(md5sum engine/rl_after/rl_model.py        | cut -c1-32)  (pin 6fe7c4155866d80e8045bed2d3bf2802, must be UNMOVED)"
echo "  store   : $(md5sum engine/rl_after/rl_model_data.json | cut -c1-32)  (pin cc02567f80bef39228f25854d121a766, must be UNMOVED)"
echo "  board   : $(md5sum data/rl_build/rl_app_data.json     | cut -c1-32)  (B_precut 5ea978f7b6a073abb2012f10cccbc3e3)"
echo
echo "  B0 is COMPUTED FROM THE BUILD, never typed. BARE_DEV and BARE_CANON must agree byte-for-byte."
echo
source tools/build_lock.sh && build_lock_acquire r23-recut 7200 || exit 1
D8TAG=BARE_DEV   D8MODE=dev       D8ENV='{}' D8OUT=$SP/out/BARE_DEV   python3 $SP/build.py
D8TAG=BARE_CANON D8MODE=canonical D8ENV='{}' D8OUT=$SP/out/BARE_CANON python3 $SP/build.py
build_lock_release
echo
echo "=== BOARD IDS ==="
for T in BARE_DEV BARE_CANON; do
  printf '  %-11s %s\n' "$T" "$(python3 -c "import json;print(json.load(open('$SP/out/$T.meta.json'))['board_md5'])" 2>/dev/null || echo NO-META)"
done
