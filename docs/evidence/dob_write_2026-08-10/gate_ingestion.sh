#!/bin/bash
# The live-scoring ingestion suites, run against the landed tree.
set -uo pipefail
REPO=/home/claude/dobwrite
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export PYTHONHASHSEED=0
cd "$REPO"
for t in \
  "python3 engine/rl_after/ingestion/test_weekly_updater.py" \
  "python3 engine/rl_after/ingestion/test_catchup_preflight.py" \
  "python3 engine/rl_after/ingestion/test_movers_transition.py" \
  "python3 engine/rl_after/ingestion/sibling_repin.py check --repo $REPO" \
  "python3 ui/tools/generate_movers_transition.py --check" \
  ; do
  out=$($t 2>&1)
  rc=$?
  if [ $rc -eq 0 ]; then echo "PASS  $t"
  else
    echo "FAIL($rc)  $t"
    echo "$out" | tail -8 | sed 's/^/        /'
  fi
done
echo INGEST_DONE
