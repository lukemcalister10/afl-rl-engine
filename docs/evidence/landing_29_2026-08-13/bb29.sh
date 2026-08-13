#!/bin/bash
# ORDER 29 board build: stage the checked-out engine into a scratch workspace, rebuild rl_app_data.json.
# ARG1 = tag for the output dir.  ARG2 = RL_GRACE value (default 0 = unset-equivalent, dial OFF).
# If ARG2 is the literal string 'UNSET' the variable is not exported at all (tests the code default).
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=/home/user/afl-rl-engine/.claude/worktrees/agent-ad9e6968bb495065a
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o29r
TAG=${1:-x}
GR=${2:-0}
RLM=${3:-}        # optional: an rl_model.py to install over the staged one (control builds only)
WS=$SP/bb_$TAG
rm -rf "$WS"; mkdir -p "$WS"
cp -rf "$ROOT/engine/rl_after"          "$WS/rl_after"
cp -rf "$ROOT/engine/forward_valuation" "$WS/forward_valuation"
cp -f  "$ROOT/config_manifest.py"       "$WS/rl_after/config_manifest.py"
cp -f  "$ROOT/fv_provenance.py"         "$WS/rl_after/fv_provenance.py"
cp -f  "$ROOT/boot_guard.py"            "$WS/rl_after/boot_guard.py"
cp -f  "$ROOT/LTI_REGISTER.md"          "$WS/rl_after/LTI_REGISTER.md"
if [ -n "$RLM" ]; then cp -f "$RLM" "$WS/rl_after/rl_model.py"; fi
if [ -n "${ART:-}" ]; then cp -f "$ART" "$WS/rl_after/pvc_curve_v2.json"; fi
chmod -R u+w "$WS"
cd "$WS/rl_after"
md5sum "$WS/rl_after/rl_model.py" "$WS/rl_after/rl_model_data.json"
export RL_REPO="$ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
# FULL FIVE-VAR THREAD PINNING (the proven fix; unpinned OMP/MKL/NUMEXPR/VECLIB workers spin-wait
# and starve this box).  ENGINE RUNS ARE STRICTLY SEQUENTIAL -- never two builds concurrently.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
# THE WORKSPACE CACHE /home/claude/v0surf.pkl SHADOWS <repo>/data/v0surf.pkl in the engine's own
# precedence (_load_v0surf, and boot_guard mirrors it byte-for-byte). It still holds the PRE-BAKE
# pickle, so without this the build reads a stale surface and halts on an unknown signature.
# The shared copy is NOT overwritten: it carries signature 6ef67f07 that other sessions on this box
# build against, and the re-baked pickle drops it. RL_V0SURF_PKL is the declared first-precedence
# override and is NOT in the release contract's must_be_unset (only RL_V0SURF_REFIT is).
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
if [ "$GR" != "UNSET" ]; then export RL_GRACE="$GR"; fi
python3 rl_export.py > "$WS/export_stdout.txt" 2> "$WS/export_stderr.txt" || {
  echo "EXPORT FAILED"; tail -40 "$WS/export_stderr.txt"; exit 1; }
md5sum "$WS/rl_after/rl_app_data.json"
