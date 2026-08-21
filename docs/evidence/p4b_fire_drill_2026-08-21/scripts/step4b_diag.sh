#!/usr/bin/env bash
# P4b FIRE DRILL — step 4b: diagnose the two verify_restore.sh reds WITHOUT the 2>/dev/null muzzle.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
REST=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/p4b/restore
RA="$REST/engine/rl_after"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export RL_REPO="$REST" RL_FV="$REST/engine/forward_valuation"
export PYTHONPATH="$RA:$REST/engine/forward_valuation:$REST/vendor:${RL_VENDOR:-/home/claude/rl_vendor}"
cd "$RA"
echo "== the named-player probe, stderr UNMUZZLED (verify_restore.sh runs this with 2>/dev/null) =="
t0=$(date +%s.%N)
python3 - <<'PY'
import io,contextlib
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
ev=g['ev']; MA=g['MA']
def v(k):
    p=next((x for x in MA.data if x.get('key')==k),None); return ev(p,2026) if p else -1
print(f"{v('ryan-maric')} {v('ed-langdon')}")
PY
rc=$?
t1=$(date +%s.%N)
echo "PROBE_RC=$rc   SECONDS=$(echo "$t1 - $t0" | bc)"
