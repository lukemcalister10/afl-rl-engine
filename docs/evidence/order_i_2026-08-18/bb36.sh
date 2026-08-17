#!/bin/bash
# ORDER I board build. ORDER A's bb32.sh with ROOT re-pointed to this seat's worktree and RL_O36 /
# RL_O36_LAM_S1 passed through. NOTHING ELSE IS CHANGED -- same staging, same five-var thread pinning,
# same RL_V0SURF_PKL override. Builds are STRICTLY SEQUENTIAL; PID-unique staging comes from the tag
# discipline (one tag, one dir, one run). ARG1 = tag for the output dir.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=${RL_ROOT:-/home/user/afl-rl-engine/.claude/worktrees/agent-a829d44bb2e77334d}
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o36}
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
cd "$WS/rl_after"
md5sum "$WS/rl_after/rl_model.py" "$WS/rl_after/rl_model_data.json"
export RL_REPO="$ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
# FULL FIVE-VAR THREAD PINNING. ENGINE RUNS ARE STRICTLY SEQUENTIAL -- never two builds concurrently.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
if [ -n "${RL_O31:-}" ]; then export RL_O31; fi
if [ -n "${RL_O32:-}" ]; then export RL_O32; fi
if [ -n "${RL_O35:-}" ]; then export RL_O35; fi
if [ -n "${RL_O36:-}" ]; then export RL_O36; fi
if [ -n "${RL_O36_LAM_S1:-}" ]; then export RL_O36_LAM_S1; fi
if [ -n "${RL_O36_TALL:-}" ]; then export RL_O36_TALL; fi
python3 rl_export.py > "$WS/export_stdout.txt" 2> "$WS/export_stderr.txt" || {
  echo "EXPORT FAILED"; tail -60 "$WS/export_stderr.txt"; exit 1; }
md5sum "$WS/rl_after/rl_app_data.json"
grep -E 'REPLICATION|day-0|ORDER I|ORDER D PICK' "$WS/export_stdout.txt" | head -12 || true
