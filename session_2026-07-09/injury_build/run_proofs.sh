#!/bin/bash
# Full proofs run: rebuild the candidate board (ON) -> data/rl_build, build the OFF board, non-mover parity,
# then the full acceptance suite (self-test build + ship_gates + panel). Slow (~10-12 min). Writes artifacts/.
set -e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-09/injury_build/artifacts
python3 $REPO/session_2026-07-09/injury_build/restamp_head.py >/dev/null
bash $REPO/bootstrap.sh >/dev/null 2>&1
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor

echo "### building ON board (RL_AVAIL default on)"
python3 rl_export.py >/dev/null 2>&1
cp -f rl_app_data.json /tmp/bon.json
cp -f rl_app_data.json "$REPO/data/rl_build/rl_app_data.json"   # candidate shipped board (for B4)
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null || true
ON_MD5=$(md5sum /tmp/bon.json | cut -c1-8)
echo "ON board md5=$ON_MD5"

echo "### building OFF board (RL_AVAIL=0)"
RL_AVAIL=0 python3 rl_export.py >/dev/null 2>&1
cp -f rl_app_data.json /tmp/boff.json
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null || true

echo "### non-mover parity"
python3 - << 'PY' | tee "$ART/nonmover_parity.txt"
import json, lti_register as LR
on={r['key']:r['v'] for r in json.load(open('/tmp/bon.json'))['active']}
off={r['key']:r['v'] for r in json.load(open('/tmp/boff.json'))['active']}
store=json.load(open('rl_model_data.json')); regkeys=set(LR.build_state({p['key']:p for p in store}))
movers=[k for k in on if on[k]!=off.get(k)]
nonreg=[k for k in movers if k not in regkeys]
print("NON-MOVER PARITY (RL_AVAIL on vs off): board keys=%d  movers=%d  register movers=%d/43  NON-REGISTER movers=%d"%(
      len(on),len(movers),len([k for k in movers if k in regkeys]),len(nonreg)))
print("PARITY %s — non-register movers: %s"%("PASS" if not nonreg else "FAIL", nonreg[:20]))
PY

echo "### rebuild ON board for the suite (workspace must hold the shipped candidate board)"
python3 rl_export.py >/dev/null 2>&1
python3 s4_matrix_M1v7.py >/dev/null 2>&1 || echo "s4_matrix note"

echo "### self-test (guards 1-5 + F1/F2 + collision sentry)"
RL_REPO=$REPO python3 one_source_selftest.py > "$ART/selftest.txt" 2>&1 || true
tail -3 "$ART/selftest.txt"

echo "### ship_gates"
cd "$REPO"
RL_REPO="$REPO" python3 ship_gates_check.py > "$ART/ship_gates.txt" 2>&1 || true
grep -E "VERDICT|^A2|^A3|^A12|^B4|^B1 " "$ART/ship_gates.txt" | tail -8

echo "### panel"
bash "$REPO/run_panel.sh" 2>&1 | tail -1
echo "### PROOFS DONE"
