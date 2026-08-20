#!/bin/bash
# ORDER 30B-P board build. VERBATIM bb30b.sh with ROOT re-pointed to the PREVIEW seat's worktree and
# the ORDER 30B-P dial pass-throughs added (RL_O30B_PREVIEW / _NOPOLE / _NOISO). NOTHING ELSE CHANGED --
# same staging, same five-var thread pinning, same RL_V0SURF_PKL override (packet 29 3.3).
# ARG1 = tag for the output dir.  ARG2 = RL_GRACE ('UNSET' => not exported, tests the code default).
# ARG3 = optional rl_model.py to install over the staged one (control builds only).
# ENV ART = optional pvc_curve_v2.json to install over the staged one.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=${RL_ROOT:-/home/user/afl-rl-engine/.claude/worktrees/agent-af5b512e41e41b194}
SP=${RL_SCRATCH:-/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o30bp}
TAG=${1:-x}
GR=${2:-UNSET}
RLM=${3:-}
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
# FULL FIVE-VAR THREAD PINNING. ENGINE RUNS ARE STRICTLY SEQUENTIAL -- never two builds concurrently.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
if [ "$GR" != "UNSET" ]; then export RL_GRACE="$GR"; fi
if [ -n "${RL_ENTRY29B:-}" ]; then export RL_ENTRY29B; fi
# ORDER 30B's DECLARED kill-switch: RL_ONEMACH=0 must reproduce board 36d5dfc7 byte-exact.
if [ -n "${RL_ONEMACH:-}" ]; then export RL_ONEMACH; fi
# ORDER 30B-P: the PREVIEW dial and the two 30B measurement dials. ALL DEFAULT-OFF; unset => not exported.
if [ -n "${RL_O30B_PREVIEW:-}" ]; then export RL_O30B_PREVIEW; fi
if [ -n "${RL_O30B_NOPOLE:-}" ];  then export RL_O30B_NOPOLE;  fi
if [ -n "${RL_O30B_NOISO:-}" ];   then export RL_O30B_NOISO;   fi
python3 rl_export.py > "$WS/export_stdout.txt" 2> "$WS/export_stderr.txt" || {
  echo "EXPORT FAILED"; tail -60 "$WS/export_stderr.txt"; exit 1; }
md5sum "$WS/rl_after/rl_app_data.json"
