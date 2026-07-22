#!/bin/bash
# REAL DIFFERENT-BUILD test: build the balanced board with a DIFFERENT numpy build (2.3.5 wheel) instead
# of the pinned 2.4.4, everything else identical. If the board diverges from 06d8af60, cross-build numpy
# variation moves the board (the pin is necessary+sufficient). If it holds, this container's two builds
# happen to agree (report honestly).
set -euo pipefail
REPO=/home/user/afl-rl-engine
BASE=/home/claude/rl_ws_alt
WS=$BASE/rl_after
ALT_SITE=/root/rl_venv_alt/lib/python3.12/site-packages
BASE_SITE=/root/rl_venv312/lib/python3.12/site-packages
rm -rf "$BASE"; mkdir -p "$BASE"
cp -rf "$REPO/engine/rl_after"          "$BASE/"
cp -rf "$REPO/engine/forward_valuation" "$BASE/"
cp -f  "$REPO/config_manifest.py"       "$WS/config_manifest.py"
cp -f  "$REPO/LTI_REGISTER.md"          "$WS/LTI_REGISTER.md"
cp -f "$REPO/data/cm_400.pkl" /home/claude/cm_400.pkl
cp -f "$REPO/data/q97m.pkl"   /home/claude/q97m.pkl
cp -f "$REPO/data/v0surf.pkl" /home/claude/v0surf.pkl
cd "$WS"
export RL_REPO="$REPO" PYTHONHASHSEED=0
export PYTHONPATH="$WS:/home/claude/rl_vendor:$ALT_SITE:$BASE_SITE"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_LEGE=0 RL_LEGF=0
V=$(/root/rl_venv_alt/bin/python3 -c "import numpy;print(numpy.__version__)")
rm -f rl_app_data.json
/root/rl_venv_alt/bin/python3 rl_export.py > "$REPO/session_2026-07-19/envpin/out/exportlog_altnumpy.txt" 2>&1
M=$(md5sum rl_app_data.json | cut -c1-8)
echo "numpy $V  balanced board md5 = $M   ($([ "$M" = "06d8af60" ] && echo "HOLDS 06d8af60" || echo "DIVERGED from 06d8af60"))"
