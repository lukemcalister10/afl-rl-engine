#!/bin/bash
# MECHANISM PROOF (final): balanced board under np.interp coherent perturbation, saving each board so the
# divergence can be diffed against the pinned board (value + rank movement). EPS=0 == pinned wheel.
set -euo pipefail
REPO=/home/user/afl-rl-engine
BASE=/home/claude/rl_ws_mech
WS=$BASE/rl_after
OUT=$REPO/session_2026-07-19/envpin/out
export PATH="/root/rl_venv312/bin:$PATH"
rm -rf "$BASE"; mkdir -p "$BASE"
cp -rf "$REPO/engine/rl_after" "$BASE/"; cp -rf "$REPO/engine/forward_valuation" "$BASE/"
cp -f "$REPO/config_manifest.py" "$WS/config_manifest.py"; cp -f "$REPO/LTI_REGISTER.md" "$WS/LTI_REGISTER.md"
cp -f "$REPO/session_2026-07-19/envpin/scripts/run_export_perturbed.py" "$WS/"
cp -f "$REPO/data/cm_400.pkl" /home/claude/cm_400.pkl; cp -f "$REPO/data/q97m.pkl" /home/claude/q97m.pkl; cp -f "$REPO/data/v0surf.pkl" /home/claude/v0surf.pkl
cd "$WS"
export RL_REPO="$REPO" PYTHONHASHSEED=0 PYTHONPATH="$WS:/home/claude/rl_vendor"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_LEGE=0 RL_LEGF=0 RL_INTERP_MODE=coherent
echo "EPS            board_md5     result"
for EPS in 0 1e-7 3e-7 5e-7 1e-6; do
  rm -f rl_app_data.json
  RL_INTERP_PERTURB="$EPS" python3 run_export_perturbed.py >/dev/null 2>&1
  M=$(md5sum rl_app_data.json | cut -c1-8)
  cp -f rl_app_data.json "$OUT/board_eps_${EPS}.json"
  printf "  %-12s %-12s %s\n" "$EPS" "$M" "$([ "$M" = "06d8af60" ] && echo HOLDS || echo DIVERGED)"
done
echo ""
echo "=== pinned board (EPS=0) stats ==="
python3 "$REPO/session_2026-07-19/envpin/scripts/board_stats.py" "$OUT/board_eps_0.json"
echo ""
echo "=== divergence at EPS=1e-6 vs pinned (value + rank) ==="
python3 "$REPO/session_2026-07-19/envpin/scripts/board_stats.py" "$OUT/board_eps_0.json" "$OUT/board_eps_1e-6.json"
