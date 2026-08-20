#!/bin/bash
# ORDER R board build. ORDER K's bbK.sh with RL_O37 added to the pass-through list and the
# re-pointed at this seat's worktree. NOTHING ELSE IS CHANGED -- same staging, same five-var thread
# pinning, same RL_V0SURF_PKL override. Builds are STRICTLY SEQUENTIAL; PID-unique staging comes from
# the tag discipline (one tag, one dir, one run). ARG1 = tag for the output dir.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=${RL_ROOT:?RL_ROOT must be set to the worktree of this seat}
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/or}
TAG=${1:-x}
WS=$SP/bb_$TAG
rm -rf "$WS"; mkdir -p "$WS"
cp -rf "$ROOT/engine/rl_after"          "$WS/rl_after"
cp -rf "$ROOT/engine/forward_valuation" "$WS/forward_valuation"
cp -f  "$ROOT/config_manifest.py"       "$WS/rl_after/config_manifest.py"
cp -f  "$ROOT/fv_provenance.py"         "$WS/rl_after/fv_provenance.py"
cp -f  "$ROOT/boot_guard.py"            "$WS/rl_after/boot_guard.py"
cp -f  "$ROOT/LTI_REGISTER.md"          "$WS/rl_after/LTI_REGISTER.md"
chmod -R u+w "$WS"
# ORDER K FINDING, fixed here and disclosed on the packet: the repo TRACKS engine/rl_after/rl_app_data.json
# (36d5dfc7), so the staging copy already contains a board BEFORE the export runs. Order J's bb37.sh
# never removed it, which means a FAILED export leaves the stale file in place and the suite prints its
# md5 as though a board had been built. It is removed here so a failed export can only print nothing.
rm -f "$WS/rl_after/rl_app_data.json"
cd "$WS/rl_after"
md5sum "$WS/rl_after/rl_model.py" "$WS/rl_after/rl_model_data.json"
export RL_REPO="$ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
# FULL FIVE-VAR THREAD PINNING. ENGINE RUNS ARE STRICTLY SEQUENTIAL -- never two builds concurrently.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
for V in RL_O31 RL_O32 RL_O35 RL_O36 RL_O36_LAM_S1 RL_O36_TALL RL_O36_FLOORFIX \
         RL_O36_KAPPA RL_O36_GAMMA RL_O36_ETA RL_O36_GAMMA_D RL_O36_LAMBDA RL_O37 \
         RL_O38A RL_O38B1 RL_O38B2 RL_O39_TMAXPCT RL_O39_BETASAT; do
  if [ -n "${!V:-}" ]; then export $V; fi
done
python3 rl_export.py > "$WS/export_stdout.txt" 2> "$WS/export_stderr.txt" || {
  echo "EXPORT FAILED"; tail -60 "$WS/export_stderr.txt"; exit 1; }
md5sum "$WS/rl_after/rl_app_data.json"
grep -E 'REPLICATION|day-0|ORDER K|ORDER D PICK|LEVER 3' "$WS/export_stdout.txt" | head -14 || true
