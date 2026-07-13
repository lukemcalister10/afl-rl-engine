#!/bin/bash
# ITEM 20 — full validation suite (fresh bootstrap → 5 SSI guards + canary + red-paths + panel +
# ship_gates + official cohort gate). Detached-safe; writes a DONE marker + a log.
set +e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-13/store_identity_job/out; mkdir -p "$ART"
export PATH="/root/rl_venv312/bin:$PATH" RL_REPO=$REPO PYTHONHASHSEED=0
export PYTHONPATH=$WS:/home/claude/rl_vendor
{
echo "### 1. fresh bootstrap — Guard 5 (asserts store 340a7a32, board 3dc19fbb)"
bash "$REPO/bootstrap.sh" 2>&1 | grep -E "Guard 5 .*PASS|store md5|bootstrap OK|FAIL|HALT"
cd "$WS"
echo "### 2. config-manifest + ruling-config"
python3 "$REPO/config_manifest.py" check 2>&1 | tail -1
python3 "$REPO/ruling_config_check.py" 2>&1 | tail -1
echo "### 3. build board (bake) + book (gate) for F1/F2 parity"
chmod +w rl_app_data.json rl_app_data.json.srcmd5 s4_matrix.json s4_matrix.json.srcmd5 2>/dev/null
RL_REPO=$REPO RL_CONFIG_MODE=bake python3 rl_export.py 2>&1 | grep -E "ZERO-EMPTY-CLUB|PARITY GATE|exported active"
echo "  board $(md5sum rl_app_data.json|cut -c1-8) (expect 3dc19fbb)"
RL_REPO=$REPO RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py >/dev/null 2>&1 && echo "  book s4_matrix built"
echo "### 4. one_source_selftest (guards 1-5 + F1/F2 + collision sentry)"
RL_REPO=$REPO python3 one_source_selftest.py 2>&1 | tail -3
echo "### 5. guard-4 correction canary (edits+restores store; survives board AND book)"
RL_REPO=$REPO python3 guard_correction_canary.py 2>&1 | tail -2
echo "  store after canary = $(md5sum rl_model_data.json | cut -c1-8)  (expect 340a7a32)"
echo "### 6. red-path proofs (each must HALT)"
RL_REPO=$REPO python3 "$REPO/session_2026-07-13/v2_9_bake/prove_red_paths.py" 2>&1 | tail -6
echo "### 7. numéraire panel 10/10"
bash "$REPO/run_panel.sh" 2>&1 | grep -E "RESULT|MISMATCH"
echo "### 8. official cohort gate (July-8 binding basis)"
python3 "$REPO/session_2026-07-13/v2_9_continuation/scripts/cohort_gate_official.py" 2>&1 | tail -8
echo "### 9. ship_gates (frozen acceptance suite B1-B6 + anchors)"
python3 "$REPO/ship_gates_check.py" 2>&1 | tail -18
echo "### 10. shipped board (repo) md5 = $(md5sum $REPO/data/rl_build/rl_app_data.json | cut -c1-8)  (expect 3dc19fbb)"
echo "SUITE_DONE"
} > "$ART/suite.log" 2>&1
echo "SUITE_DONE_MARKER" > "$ART/suite_done.txt"
