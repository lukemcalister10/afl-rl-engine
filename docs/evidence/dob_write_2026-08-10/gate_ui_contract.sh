#!/bin/bash
# The final-integration UI/contract gate set, run against the landed tree.
set -uo pipefail
REPO=/home/claude/dobwrite
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export PYTHONHASHSEED=0
cd "$REPO"
for t in \
  "python3 config_manifest.py check" \
  "python3 release_contract.py check" \
  "python3 ruling_config_check.py" \
  "python3 session_2026-07-21/final_integration/tests/release_state_failclosed_test.py" \
  "python3 session_2026-07-21/final_integration/tools/invariant_proof.py" \
  "python3 ui/tests/extract_seam.test.py" \
  "node    ui/tests/release_seam.test.js" \
  "node    ui/tests/counting_rule.test.js" \
  "python3 ui/tests/club_curve_provenance.test.py" \
  "python3 ui/tests/test_club_valuation_current.py" \
  "node    ui/tests/club_totals_parity.test.js" \
  "node    ui/tests/ownership_single_source.test.js" \
  "python3 ui/tests/ownership_store_apply.test.py" \
  "node    ui/tests/ownership_sidecar.test.js" \
  "node    ui/tests/movers.test.js" \
  "node    ui/tests/adoption_gate.test.js" \
  ; do
  out=$($t 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then echo "PASS  $t"
  else
    echo "FAIL($rc)  $t"
    echo "$out" | tail -6 | sed 's/^/        /'
  fi
done
echo UIGATES_DONE
