#!/bin/bash
# THE DECLARED v0surf RE-BAKE on the FINAL (tiebroken) curve.
# The engine's ONE committed fit path. Writes data/v0surf.pkl + re-pins expected_boot.json::v0surf.
set -euo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
ROOT=/home/user/afl-rl-engine/.claude/worktrees/agent-ad9e6968bb495065a
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o29r
WS=$SP/bake
rm -rf "$WS"
mkdir -p "$WS"
cp -rf "$ROOT/engine/rl_after"          "$WS/rl_after"
cp -rf "$ROOT/engine/forward_valuation" "$WS/forward_valuation"
cp -f  "$ROOT/config_manifest.py" "$WS/rl_after/config_manifest.py"
cp -f  "$ROOT/fv_provenance.py"   "$WS/rl_after/fv_provenance.py"
cp -f  "$ROOT/boot_guard.py"      "$WS/rl_after/boot_guard.py"
cp -f  "$ROOT/LTI_REGISTER.md"    "$WS/rl_after/LTI_REGISTER.md"
chmod -R u+w "$WS"
cd "$WS/rl_after"
echo "=== curve the bake is keyed to:"
md5sum "$WS/rl_after/pvc_curve_v2.json"
python3 -c "import json;d=json.load(open('pvc_curve_v2.json'));print('   curve_md5',d['curve_md5'])"
echo "=== v0surf BEFORE:"
md5sum "$ROOT/data/v0surf.pkl"
python3 -c "import json;print('   pinned',json.load(open('$ROOT/data/expected_boot.json'))['v0surf'])"
export RL_REPO="$ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$ROOT/vendor:$ROOT"
export RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1
echo "=== DECLARED BAKE (RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1):"
python3 "$ROOT/session_2026-07-18/legf6/scripts/refit_v0surf.py" --bake
echo "=== v0surf AFTER:"
md5sum "$ROOT/data/v0surf.pkl"
python3 -c "import json;print('   pinned',json.load(open('$ROOT/data/expected_boot.json'))['v0surf'])"
