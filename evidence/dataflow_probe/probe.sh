#!/bin/bash
# ============================================================================
# DATA-FLOW / DEAD-FEATURE / F1 PROBE  — READ-ONLY.  Reproduces every number
# in evidence/dataflow_probe/REPORT.md. Run from repo root:
#     bash evidence/dataflow_probe/probe.sh
# Baked head: git 389ac39 (tag baked-v2.4-2026-07-04), engine _merged_recover.py md5 c47cb43d.
# ENV: exactly run_panel.sh's env. RL_GAMMA/RL_PICK1/RL_PRIOR_TREES equal the code defaults,
#      but RL_RUCK_TAX / RL_RECENCY_DECAY are load-bearing (they feed cp.RECENCY_DECAY / rd.RUCK_TAX);
#      omitting them changes ~all values and FALSELY reads as "stale". They are required for byte-parity.
# ============================================================================
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RA="$ROOT/engine/rl_after"
SHIPPED="$ROOT/data/rl_build/rl_app_data.json"     # the file the board reads (bootstrap copies -> /home/claude/rl_build/)
OUT="$ROOT/evidence/dataflow_probe/out"; mkdir -p "$OUT"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$RA:/home/claude/rl_vendor:${PYTHONPATH:-}"

echo "===== STEP 0: GROUND TRUTH ====="
echo "git HEAD    : $(git -C "$ROOT" rev-parse HEAD)"
echo "git tag     : $(git -C "$ROOT" describe --tags --exact-match HEAD 2>/dev/null)"
echo "engine md5  : $(md5sum "$RA/_merged_recover.py" | cut -c1-8)  (expect c47cb43d)"
echo "store md5   : $(md5sum "$RA/rl_model_data.json" | cut -c1-8)  (== .pre_stage0 authoritative)"
echo "shipped md5 : $(md5sum "$SHIPPED" | cut -c1-8)  (expect eb5d6716)"

echo; echo "===== TASK 1.4: REGENERATE EXPORT (panel env) & BYTE-COMPARE TO SHIPPED (LIVE vs STALE) ====="
PREV="$RA/rl_app_data.json"; BAK="$PREV.probe_bak"
[ -f "$PREV" ] && mv "$PREV" "$BAK"
( cd "$RA" && python3 rl_export.py ) > "$OUT/export_baked.log" 2>&1
echo "export exit: $?"; tail -1 "$OUT/export_baked.log"
REGEN="$OUT/rl_app_data.regen_baked.json"
[ -f "$PREV" ] && cp "$PREV" "$REGEN" && rm -f "$PREV"
[ -f "$BAK" ] && mv "$BAK" "$PREV"
R=$(md5sum "$REGEN"|cut -c1-8); S=$(md5sum "$SHIPPED"|cut -c1-8)
echo "regen md5=$R  shipped md5=$S  -> $([ "$R" = "$S" ] && echo 'BYTE-MATCH: board is LIVE (current exporter reproduces it exactly)' || echo 'DIFFER')"

echo; echo "===== TASK 3: EXPORT-PATH _REAL MEMBERSHIP (dual-namespace layer-drop) ====="
( cd "$RA" && python3 "$ROOT/evidence/dataflow_probe/verify_export_path.py" ) 2>&1 | tail -6

echo; echo "===== TASK 3/5: TRUE-ENGINE gated values + BOARD-vs-ENGINE SWEEP + POPULATION ====="
( cd "$RA" && python3 "$ROOT/evidence/dataflow_probe/sweep_pop.py" ) 2>&1 | tee "$OUT/sweep_pop.log"
echo; echo "true gated ev(louis-emmett)=853 (cap ON) vs board 1361 (cap dropped) — see sweep_pop.log / verify_export_path"
echo "DONE. Full logs in evidence/dataflow_probe/out/."
