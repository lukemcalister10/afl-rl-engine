#!/usr/bin/env bash
# P4b FIRE DRILL — step 4d: full unmuzzled output of the probe under (a) verify_restore.sh's
# env-var set + repo root on PYTHONPATH, and (b) a BARE env (no model-semantics RL_* at all),
# which is the posture the tag's own _bake_note says reproduces board a05fe951 byte-exact.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
REST=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore
RA="$REST/engine/rl_after"

probe(){
cd "$RA"
python3 - <<'PY'
import io,contextlib
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
ev=g['ev']; MA=g['MA']
def v(k):
    p=next((x for x in MA.data if x.get('key')==k),None); return ev(p,2026) if p else -1
print("MARIC_LANGDON: %s %s" % (v('ryan-maric'), v('ed-langdon')))
PY
}

echo "################ (a) verify_restore.sh env + repo root on PYTHONPATH ################"
( export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
  export RL_REPO="$REST" RL_FV="$REST/engine/forward_valuation"
  export PYTHONPATH="$REST:$RA:$REST/engine/forward_valuation:$REST/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
  t0=$(date +%s.%N); probe; rc=$?; t1=$(date +%s.%N)
  echo "PROBE_A_RC=$rc SECONDS=$(echo "$t1 - $t0" | bc)" )

echo
echo "################ (b) BARE env — no model-semantics RL_* set, RL_PRIOR_TREES only ################"
( export PYTHONHASHSEED=0 RL_PRIOR_TREES=400
  export RL_REPO="$REST" RL_FV="$REST/engine/forward_valuation"
  export PYTHONPATH="$REST:$RA:$REST/engine/forward_valuation:$REST/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
  t0=$(date +%s.%N); probe; rc=$?; t1=$(date +%s.%N)
  echo "PROBE_B_RC=$rc SECONDS=$(echo "$t1 - $t0" | bc)" )
