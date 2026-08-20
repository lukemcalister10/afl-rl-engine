#!/bin/bash
# ORDER B BUILD board builder. bb32.sh (Order A's, itself Order 31-F's) with ROOT re-pointed at THIS
# seat's worktree, the scratch directory renamed o33, and RL_O33 / RL_O33_STAGE / RL_O33_SSTAR passed
# through beside RL_O31 / RL_O32. NOTHING ELSE CHANGED — same staging, same five-var thread pinning,
# same RL_V0SURF_PKL override. Builds STRICTLY SEQUENTIAL; PID-unique staging via the tag discipline.
# ARG1 = tag for the output dir.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=${RL_ROOT:-/home/user/afl-rl-engine/.claude/worktrees/agent-ac05497987a45d522}
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33}
TAG=${1:-x}
WS=$SP/bb_$TAG
rm -rf "$WS"; mkdir -p "$WS"
cp -rf "$ROOT/engine/rl_after"          "$WS/rl_after"
cp -rf "$ROOT/engine/forward_valuation" "$WS/forward_valuation"
cp -f  "$ROOT/config_manifest.py"       "$WS/rl_after/config_manifest.py"
cp -f  "$ROOT/fv_provenance.py"         "$WS/rl_after/fv_provenance.py"
cp -f  "$ROOT/boot_guard.py"            "$WS/rl_after/boot_guard.py"
cp -f  "$ROOT/LTI_REGISTER.md"          "$WS/rl_after/LTI_REGISTER.md"
if [ -n "${ART:-}" ]; then cp -f "$ART" "$WS/rl_after/pvc_curve_v2.json"; fi
chmod -R u+w "$WS"
cd "$WS/rl_after"
md5sum "$WS/rl_after/rl_model.py" "$WS/rl_after/rl_model_data.json"
export RL_REPO="$ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
if [ -n "${RL_O31:-}" ]; then export RL_O31; fi
if [ -n "${RL_O32:-}" ]; then export RL_O32; fi
if [ -n "${RL_O32_STAGE:-}" ]; then export RL_O32_STAGE; fi
if [ -n "${RL_O33:-}" ]; then export RL_O33; fi
if [ -n "${RL_O33_STAGE:-}" ]; then export RL_O33_STAGE; fi
if [ -n "${RL_O33_SSTAR:-}" ]; then export RL_O33_SSTAR; fi
python3 rl_export.py > "$WS/export_stdout.txt" 2> "$WS/export_stderr.txt" || {
  echo "EXPORT FAILED"; tail -60 "$WS/export_stderr.txt"; exit 1; }
md5sum "$WS/rl_after/rl_app_data.json"
