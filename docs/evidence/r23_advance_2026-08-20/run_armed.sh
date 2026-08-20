#!/bin/bash
# ACT 3 — THE R23 ADVANCE, ARMED. The runbook §3 step-3 invocation exactly.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO=/home/user/afl-rl-engine
export RL_FV="$RL_REPO/engine/forward_valuation"
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd "$RL_REPO"
echo "=== ACT 3 — THE R23 ADVANCE, ARMED ==="
echo "  commit : $(git rev-parse HEAD)"
echo "  store  : $(md5sum engine/rl_after/rl_model_data.json | cut -c1-32)"
echo "  board  : $(md5sum data/rl_build/rl_app_data.json     | cut -c1-32)   (B0)"
echo "  sheet  : $(md5sum docs/owner_annotations/SITTER_2026_v1.csv | cut -c1-32)"
echo "  scores : $(md5sum scores/R23.csv | cut -c1-32)"
echo
source tools/build_lock.sh && build_lock_acquire r23-advance 7200 || exit 1
# The lock exports RL_BUILD_LOCK_HELD and config_manifest.enforce() rejects any unknown RL_-prefixed
# var as a model override, so a canonical/bake-mode build launched from inside the lock would HALT.
# Drop it from the CHILD's environment only; the lock itself stays held by THIS shell's fd.
env -u RL_BUILD_LOCK_HELD \
  INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=R23-2026-08-20-owner-approved \
  python3 tools/round_entry/round_entry.py catchup --file 23=scores/R23.csv --approve
rc=$?
build_lock_release
echo "ARMED RUN EXIT=$rc"
exit $rc
