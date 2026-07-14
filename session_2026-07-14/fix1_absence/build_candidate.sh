#!/bin/bash
# Rebuild the candidate board + book from the edited engine (Fix 1 + absence term, both default-ON),
# re-pin expected_boot.json (engine_head + board), then run the gate suite + panel. CANDIDATE ONLY.
set -euo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
export PATH="/root/rl_venv312/bin:$PATH" RL_REPO="$HERE" PYTHONHASHSEED=0
export PYTHONPATH="$WS:/home/claude/rl_vendor"
PIN="$HERE/data/expected_boot.json"
SESS="$HERE/session_2026-07-14/fix1_absence"

echo "===== 1. sync workspace engine = repo engine ====="
cp -f "$HERE/engine/rl_after/_merged_recover.py" "$WS/_merged_recover.py"
ENG=$(md5sum "$WS/_merged_recover.py" | awk '{print $1}')
echo "engine md5 = $ENG   (was 2334f570e91c555630be86e36408eea1)"

echo "===== 2. re-pin engine_head BEFORE any boot_guard runs ====="
python3 - "$PIN" "$ENG" <<'PY'
import json,sys
p,eng=sys.argv[1],sys.argv[2]
d=json.load(open(p)); old=d['engine_head']; d['engine_head']=eng
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)
print(f"engine_head {old[:8]} -> {eng[:8]}")
PY

echo "===== 3. build board (gate mode; RL_DAMP/RL_ABSENCE default-ON, not in manifest) ====="
cd "$WS"
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null || true
RL_CONFIG_MODE=gate RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 \
  RL_PRIOR_TREES=400 PAR_RAMPS=22 python3 rl_export.py 2>&1 | grep -v -i warning | tail -8
BOARD=$(md5sum rl_app_data.json | awk '{print $1}')
echo "board md5 = $BOARD   (was 3dc19fbbf920958affe7c6a2be9697d2)"
cp -f rl_app_data.json "$HERE/data/rl_build/rl_app_data.json"
cp -f rl_app_data.json /home/claude/rl_build/rl_app_data.json
cp -f rl_app_data.json.srcmd5 "$HERE/data/rl_build/rl_app_data.json.srcmd5" 2>/dev/null || true

echo "===== 4. re-pin board ====="
python3 - "$PIN" "$BOARD" <<'PY'
import json,sys
p,b=sys.argv[1],sys.argv[2]
d=json.load(open(p)); old=d['board']; d['board']=b
json.dump(d,open(p,'w'),indent=2,ensure_ascii=False)
print(f"board {old[:8]} -> {b[:8]}")
PY

echo "===== 5. build book (walk-forward matrix) ====="
cd "$WS"
S4_MATRIX="$SESS/measurement/s4_matrix_candidate.json" RL_CONFIG_MODE=gate RL_GAMMA=0.85 \
  RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22 \
  python3 s4_matrix_M1v7.py 2>&1 | grep -v -i warning | tail -6
echo "book meta:"; python3 -c "import json;m=json.load(open('$SESS/measurement/s4_matrix_candidate.json')).get('__meta__');print(m)"

echo "DONE. engine=$ENG board=$BOARD"
