#!/usr/bin/env bash
# verify_restore.sh — scripted restore-verify (required kickoff asset; CONTEXT_BUDGET_RULES §1).
# Run from the extracted tree root:  bash verify_restore.sh [TREE_ROOT]
# Prints a short PASS/FAIL verdict with actual reproduced values. Verify by SCRIPT, never by inspection.
set -uo pipefail
ROOT="${1:-$(cd "$(dirname "$0")" && pwd)}"
RA="$ROOT/engine/rl_after"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$RA:$ROOT/engine/forward_valuation:$ROOT/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
pass=0; fail=0
chk(){ if [ "$2" = "$3" ]; then echo "PASS  $1 = $2"; pass=$((pass+1)); else echo "FAIL  $1 = $2  (expected $3)"; fail=$((fail+1)); fi; }
chk "head  _merged_recover.py" "$(md5sum "$RA/_merged_recover.py"|cut -c1-8)" "8aed420a"
chk "store rl_model_data.json" "$(md5sum "$RA/rl_model_data.json"|cut -c1-8)" "644d1254"
chk "band  cm_400.pkl"         "$(md5sum "$ROOT/data/cm_400.pkl"|cut -c1-8)" "34faa865"
cd "$RA"
PF=$(python3 - <<'PY' 2>/dev/null
import io,contextlib
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
ev=g['ev']; MA=g['MA']
def v(k):
    p=next((x for x in MA.data if x.get('key')==k),None); return ev(p,2026) if p else -1
print(f"{v('ryan-maric')} {v('ed-langdon')}")
PY
)
chk "Maric   ev(2026)" "$(echo "$PF"|cut -d' ' -f1)" "1409"
chk "Langdon ev(2026)" "$(echo "$PF"|cut -d' ' -f2)" "593"
for h in _gate1_wf.py _gate1_picksplit.py s4_matrix_M1v7.py s4_render_M1v7.py; do
  if [ -f "$RA/$h" ]; then echo "PASS  harness present: $h"; pass=$((pass+1)); else echo "FAIL  harness MISSING: $h"; fail=$((fail+1)); fi
done
if [ -f "$ROOT/run_panel.sh" ]; then echo "--- run_panel.sh tail (10-panel; confirm 10/10) ---"; (cd "$ROOT" && bash run_panel.sh 2>&1 | grep -v Warning | tail -4); fi
echo "===================================="
echo "VERDICT: $pass PASS / $fail FAIL  =>  $([ "$fail" = 0 ] && echo RESTORE-VERIFY PASS || echo RESTORE-VERIFY FAIL)"
