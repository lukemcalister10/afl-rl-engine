#!/usr/bin/env bash
# P4b FIRE DRILL — step 3: do the TAG-ERA BOOT GUARDS accept the restored bytes?
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
REST=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore
export RL_REPO="$REST" CLAUDE_PROJECT_DIR="$REST" RL_FV="$REST/engine/forward_valuation"
export PYTHONHASHSEED=0
cd "$REST"

hr(){ echo; echo "================================================================================"; echo "$1"; echo "================================================================================"; }

hr "3.1  boot_guard.py (Guard 5) — CLI entry point, restored tree, RL_REPO bound to the restore"
t0=$(date +%s.%N)
python3 boot_guard.py p4b_fire_drill \
  "$REST/engine/rl_after/rl_model_data.json" \
  "$REST/engine/rl_after/_merged_recover.py" \
  "$REST/data/cm_400.pkl" \
  "$REST/LTI_REGISTER.md"
rc31=$?
t1=$(date +%s.%N)
echo "GUARD5_CLI_RC=$rc31   SECONDS=$(echo "$t1 - $t0" | bc)"

hr "3.2  boot_guard.assert_fv_provenance() — forward-valuation checkout + loaded-path legs"
t0=$(date +%s.%N)
python3 -c "
import boot_guard, sys
try:
    boot_guard.assert_fv_provenance()
    print('assert_fv_provenance PASS')
except SystemExit as e:
    print(e.code); sys.exit(1)
"
rc32=$?
t1=$(date +%s.%N)
echo "GUARD5_FV_RC=$rc32   SECONDS=$(echo "$t1 - $t0" | bc)"

hr "3.3  release_contract.py check — the tag's own release-state verifier, fenced mode gate"
t0=$(date +%s.%N)
RL_CONFIG_MODE=gate python3 release_contract.py
rc33=$?
t1=$(date +%s.%N)
echo "RELEASE_CONTRACT_RC=$rc33   SECONDS=$(echo "$t1 - $t0" | bc)"

hr "3.4  ruling_config_check.py — the tag's config-ruling gate"
t0=$(date +%s.%N)
python3 ruling_config_check.py
rc34=$?
t1=$(date +%s.%N)
echo "RULING_CONFIG_RC=$rc34   SECONDS=$(echo "$t1 - $t0" | bc)"

echo
echo "SUMMARY_RCS guard5_cli=$rc31 guard5_fv=$rc32 release_contract=$rc33 ruling_config=$rc34"
