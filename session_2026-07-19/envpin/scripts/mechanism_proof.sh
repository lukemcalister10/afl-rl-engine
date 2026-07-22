#!/bin/bash
# MECHANISM PROOF (env-pin, 2026-07-19). Sets up the dev-shell workspace ONCE, then builds the balanced
# board (RL_LEGE=0 RL_LEGF=0) under a sweep of np.interp perturbation magnitudes. EPS=0 is the pinned
# wheel; EPS>0 simulates a DIFFERENT numpy build's last-ULP interp output. Shows: the standard/pinned
# build holds 06d8af60; a >=threshold interp divergence (what a different wheel produces) flips it.
# Usage: mechanism_proof.sh <MODE> <EPS1> [EPS2 ...]
set -euo pipefail
REPO=/home/user/afl-rl-engine
BASE=/home/claude/rl_ws_mech
WS=$BASE/rl_after
MODE="${1:-coherent}"; shift
export PATH="/root/rl_venv312/bin:$PATH"
rm -rf "$BASE"; mkdir -p "$BASE"
cp -rf "$REPO/engine/rl_after"          "$BASE/"
cp -rf "$REPO/engine/forward_valuation" "$BASE/"
cp -f  "$REPO/config_manifest.py"       "$WS/config_manifest.py"
cp -f  "$REPO/LTI_REGISTER.md"          "$WS/LTI_REGISTER.md"
cp -f  "$REPO/session_2026-07-19/envpin/scripts/run_export_perturbed.py" "$WS/"
cp -f "$REPO/data/cm_400.pkl" /home/claude/cm_400.pkl
cp -f "$REPO/data/q97m.pkl"   /home/claude/q97m.pkl
cp -f "$REPO/data/v0surf.pkl" /home/claude/v0surf.pkl
cd "$WS"
export RL_REPO="$REPO" PYTHONHASHSEED=0
export PYTHONPATH="$WS:/home/claude/rl_vendor"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_LEGE=0 RL_LEGF=0 RL_INTERP_MODE="$MODE"
echo "mode=$MODE   (balanced board of record = 06d8af60, Sv=752427, Sheezel=7964)"
echo "EPS(np.interp rel)        board_md5     result           Sv / Sheezel"
for EPS in "$@"; do
  rm -f rl_app_data.json
  RL_INTERP_PERTURB="$EPS" python3 run_export_perturbed.py >/tmp/mech_$$.log 2>/tmp/mech_$$.err || { echo "BUILD FAILED at EPS=$EPS"; tail -20 /tmp/mech_$$.err; exit 1; }
  M=$(md5sum rl_app_data.json | cut -c1-8)
  RES=$(grep '\[result\]' /tmp/mech_$$.err | tail -1 | sed 's/\[result\] //')
  if [ "$M" = "06d8af60" ]; then V="HOLDS 06d8af60 "; else V="DIVERGED        "; fi
  printf "  %-24s %-12s %s %s\n" "$EPS" "$M" "$V" "$RES"
done
