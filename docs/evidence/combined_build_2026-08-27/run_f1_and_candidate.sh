#!/usr/bin/env bash
# COMBINED BUILD — F1 (the byte-exact off-proof) then the candidate board.
#   Step 0: bake_cand.py — declares the dials in the manifest (default '1'), bakes the S_LL5G pvc,
#           preserves the originals under pre_bake/, restamps pins coherently.
#   Leg A:  dials '0' + ORIGINAL pvc in the ws  => board MUST equal live 3167cba6 byte-exact (F1).
#   Leg B:  dials '1' + BAKED pvc in the ws     => the candidate board, saved + md5'd.
set -eu
export PATH="/root/rl_venv312/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 PYTHONHASHSEED=0
ROOT=/home/user/cand_build/root
WS=/home/user/cand_build/ws/rl_after
EV="$ROOT/docs/evidence/combined_build_2026-08-27"
LIVE_MD5=3167cba643a6b16e5ef5d904d8957fcd

cp "$ROOT/engine/rl_after/_merged_recover.py" "$WS/_merged_recover.py"
find "$WS" -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true

echo "== STEP 0: the bake (manifest dials + S_LL5G pvc; originals preserved) =="
python3 "$EV/bake_cand.py" "$ROOT"

echo "== LEG A (F1): dials OFF + original pvc + ORIGINAL v0surf => byte-exact =="
python3 "$EV/set_cand_dials.py" "$ROOT" 0
python3 "$EV/set_v0surf.py" "$ROOT" pre
cp "$EV/pre_bake/pvc_curve_v2.json" "$WS/pvc_curve_v2.json"
cp "$EV/pre_bake/pvc_snapshot.json" "$WS/pvc_snapshot.json"
cp "$EV/pre_bake/sealed_entrant_structure.json" "$ROOT/session_2026-07-18/legf5/sealed_entrant_structure.json"
cp "$EV/pre_bake/rl_export.py" "$WS/rl_export.py"
rm -f "$WS/rl_app_data.json"
( cd "$WS" && env RL_CONFIG_MODE=gate RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" \
    PYTHONPATH="$WS:/home/claude/rl_vendor" python3 rl_export.py ) > "$EV/f1_legA.log" 2>&1
A=$(md5sum "$WS/rl_app_data.json" | cut -d' ' -f1)
echo "leg A board: $A"
if [ "$A" != "$LIVE_MD5" ]; then echo "F1 RED: dials-off board != live 3167cba6"; exit 5; fi
echo "F1 GREEN: the dials-off candidate reproduces the live board byte-exact"

echo "== LEG B: dials ON + baked pvc + REFIT v0surf => the candidate board =="
python3 "$EV/set_cand_dials.py" "$ROOT" 1
python3 "$EV/set_v0surf.py" "$ROOT" refit
cp "$ROOT/engine/rl_after/pvc_curve_v2.json" "$WS/pvc_curve_v2.json"
cp "$ROOT/engine/rl_after/pvc_snapshot.json" "$WS/pvc_snapshot.json"
cp "$EV/sealed_entrant_structure_CAND.json" "$ROOT/session_2026-07-18/legf5/sealed_entrant_structure.json"
cp "$ROOT/engine/rl_after/rl_export.py" "$WS/rl_export.py"
rm -f "$WS/rl_app_data.json"
( cd "$WS" && env RL_CONFIG_MODE=gate RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" \
    PYTHONPATH="$WS:/home/claude/rl_vendor" python3 rl_export.py ) > "$EV/candidate_build.log" 2>&1
B=$(md5sum "$WS/rl_app_data.json" | cut -d' ' -f1)
cp "$WS/rl_app_data.json" "$EV/board_candidate.json"
echo "candidate board: $B (saved)"
if [ "$B" = "$LIVE_MD5" ]; then echo "RED: the candidate board equals live — the levers did not act"; exit 4; fi
echo "BUILD LEGS DONE: off=$A on=$B"
