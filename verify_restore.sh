#!/usr/bin/env bash
# verify_restore.sh — scripted restore-verify (required kickoff asset; CONTEXT_BUDGET_RULES §1).
# Run from the extracted tree root:  bash verify_restore.sh [TREE_ROOT]
# Prints a short PASS/FAIL verdict with actual reproduced values. Verify by SCRIPT, never by inspection.
set -uo pipefail
ROOT="${1:-$(cd "$(dirname "$0")" && pwd)}"
RA="$ROOT/engine/rl_after"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
# fv-provenance remediation 2026-07-20: bind RL_REPO + RL_FV to THIS restored tree so the engine's cp/PR chain
# imports forward_valuation from the tree being verified — NOT the ambient /home/claude/rl_workspace copy. This
# is the "parameterize _FV" root fix the pair-guard below anticipated (D8 mixed-pair caveat); wire_redesign now
# fails closed if RL_FV/RL_REPO are unset rather than defaulting to the workspace.
export RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation"
export PYTHONPATH="$RA:$ROOT/engine/forward_valuation:$ROOT/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
pass=0; fail=0
chk(){ if [ "$2" = "$3" ]; then echo "PASS  $1 = $2"; pass=$((pass+1)); else echo "FAIL  $1 = $2  (expected $3)"; fail=$((fail+1)); fi; }
# Expected md5s come from the ONE pinned manifest (data/expected_boot.json) — no per-bake hex duplicated here.
_exp(){ python3 -c "import json,sys; print(json.load(open('$ROOT/data/expected_boot.json'))[sys.argv[1]][:8])" "$1"; }
E_HEAD=$(_exp engine_head); E_STORE=$(_exp store); E_RLM=$(_exp rl_model); E_BAND=$(_exp band)
chk "head  _merged_recover.py" "$(md5sum "$RA/_merged_recover.py"|cut -c1-8)" "$E_HEAD"
chk "store rl_model_data.json" "$(md5sum "$RA/rl_model_data.json"|cut -c1-8)" "$E_STORE"
chk "rl_model.py (DPP strip)"  "$(md5sum "$RA/rl_model.py"|cut -c1-8)" "$E_RLM"   # v2.5: DPP strip (drafted/present/future single-valued cols) lives here
chk "band  cm_400.pkl"         "$(md5sum "$ROOT/data/cm_400.pkl"|cut -c1-8)" "$E_BAND"
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
chk "Maric   ev(2026)" "$(echo "$PF"|cut -d' ' -f1)" "1271"
chk "Langdon ev(2026)" "$(echo "$PF"|cut -d' ' -f2)" "567"
for h in _gate1_wf.py _gate1_picksplit.py s4_matrix_M1v7.py s4_render_M1v7.py; do
  if [ -f "$RA/$h" ]; then echo "PASS  harness present: $h"; pass=$((pass+1)); else echo "FAIL  harness MISSING: $h"; fail=$((fail+1)); fi
done
# PAIR-GUARD (D8 ASK 3iii — closes the D7 mixed-pair instrument caveat): historically wire_redesign.py's
# HARDCODED _FV=/home/claude/rl_workspace/forward_valuation meant the named-player axes above ran
# repo-engine x WORKSPACE-forward_valuation. That root cause is now FIXED (RL_FV bound to $ROOT above; the
# engine loads THIS tree's forward_valuation), so the axes ran repo-engine x repo-forward_valuation. This
# guard is now a defense-in-depth check that a lingering workspace copy still matches the repo — a mismatch
# no longer changes the verify above, but is surfaced LOUD:
WFV="/home/claude/rl_workspace/forward_valuation"
if [ -d "$WFV" ] && [ -d "$ROOT/engine/forward_valuation" ]; then
  pgfail=0
  for f in "$ROOT/engine/forward_valuation"/*.py; do
    b=$(basename "$f")
    [ "$(md5sum "$f"|cut -c1-8)" = "$(md5sum "$WFV/$b" 2>/dev/null|cut -c1-8)" ] || { pgfail=1; echo "      pair-guard MISMATCH: $b (repo tree != workspace _FV target)"; }
  done
  chk "cp-pair guard (repo fv == workspace fv, all .py)" "$pgfail" "0"
else
  echo "NOTE  cp-pair guard skipped: $WFV absent — imports fail loudly rather than mix (root fix = parameterize _FV, candidate-branch item)"
fi
if [ -f "$ROOT/run_panel.sh" ]; then echo "--- run_panel.sh tail (10-panel; confirm 10/10) ---"; (cd "$ROOT" && bash run_panel.sh 2>&1 | grep -v Warning | tail -4); fi
echo "===================================="
echo "VERDICT: $pass PASS / $fail FAIL  =>  $([ "$fail" = 0 ] && echo RESTORE-VERIFY PASS || echo RESTORE-VERIFY FAIL)"
# SUITE HYGIENE 2026-07-13: the EXIT CODE is the authority, not the printed verdict string. This script
# intentionally runs ALL chk()s and tallies (so a bare `set -e` — which would abort on the first failure
# and hide the report — is deliberately NOT used); instead a non-zero fail count exits non-zero here.
exit $(( fail > 0 ? 1 : 0 ))
