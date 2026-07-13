#!/bin/bash
# v2.9 BAKE — FINAL suite on the bake head (post L7 numéraire + override + re-seal + re-pins).
# Fresh BAKE-mode bootstrap: Guard 5 + config/ruling gates + five SSI guards (selftest + guard-4 canary) +
# owner-override exclusion (must stay GREEN) + the three red-path proofs + numéraire panel 10/10.
# ship_gates is run SEPARATELY (long; already run). Writes a DONE marker. Detached-safe.
set +e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-13/v2_9_bake/final; mkdir -p "$ART"
export PATH="/root/rl_venv312/bin:$PATH" RL_REPO=$REPO PYTHONHASHSEED=0
export PYTHONPATH=$WS:/home/claude/rl_vendor
{
echo "### 1. fresh bootstrap (BAKE mode) — Guard 5 boot-store (asserts board pin 81e48293, full hash)"
bash "$REPO/bootstrap.sh" 2>&1 | grep -E "Guard 5|store md5|engine md5|bootstrap OK|FAIL|HALT"
echo "### 2. config-manifest + ruling-config"
cd "$WS"
python3 "$REPO/config_manifest.py" check 2>&1 | tail -1
python3 "$REPO/ruling_config_check.py" 2>&1 | tail -1
echo "### 3. five SSI guards — one_source_selftest (guards 1-4 + lookalike/canary)"
RL_REPO=$REPO python3 one_source_selftest.py 2>&1 | tail -3
echo "### 4. guard-4 correction canary (edits+restores store; must survive board AND book)"
RL_REPO=$REPO python3 guard_correction_canary.py 2>&1 | tail -2
echo "store after canary = $(md5sum rl_model_data.json | cut -c1-8)  (expect b0c39d78)"
echo "### 5. OWNER-OVERRIDE EXCLUSION TEST (must stay GREEN — override OUT of guards/aggregates)"
RL_REPO=$REPO python3 "$REPO/session_2026-07-09/ci_guard_brodie/test_owner_override_exclusion.py" 2>&1 | tail -2
echo "### 6. THE THREE RED-PATH PROOFS (each must HALT)"
cd "$WS"; RL_REPO=$REPO python3 "$REPO/session_2026-07-13/v2_9_bake/prove_red_paths.py" 2>&1 | tail -8
echo "### 7. numéraire panel 10/10"
bash "$REPO/run_panel.sh" 2>&1 | grep -E "RESULT"
echo "### 8. shipped board (repo) md5 = $(md5sum $REPO/data/rl_build/rl_app_data.json | cut -c1-8)  (must be 81e48293, unchanged)"
echo "FINAL_SUITE_DONE"
} > "$ART/final_suite.log" 2>&1
echo "FINAL_DONE exit-marker" > "$ART/final_done.txt"
