#!/bin/bash
# BAKE v2.7 — FINAL suite re-run on the bake head (post-reseal, post-state-strings).
# Full suite from a fresh BAKE-mode bootstrap: Guard 5 + config/ruling gates + regen (board byte-agree
# e2c9bc51, book stable-sha 2a74c731) + self-test + guard-4 canary + ship_gates (B3 now PASS) + panel.
# Detached (run in background) so no timeout can interrupt the canary mid-edit. Writes a DONE marker.
set +e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-10/bake_v2_7/final; mkdir -p "$ART"
export PATH="/root/rl_venv312/bin:$PATH" RL_REPO=$REPO RL_CONFIG_MODE=bake PYTHONHASHSEED=0
export PYTHONPATH=$WS:/home/claude/rl_vendor
{
echo "### 1. fresh bootstrap (BAKE mode) — Guard 5 boot-store"
bash "$REPO/bootstrap.sh" 2>&1 | grep -E "Guard 5|store md5|engine md5|register md5|bootstrap OK"
cd "$WS"
export RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
echo "### 2. config-manifest + ruling-config"
python3 "$REPO/config_manifest.py" check 2>&1 | tail -1
python3 "$REPO/ruling_config_check.py" 2>&1 | tail -1
echo "### 3. regenerate board (bake) — must be e2c9bc51"
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null
RL_REPO=$REPO RL_CONFIG_MODE=bake python3 rl_export.py > /dev/null 2>&1
echo "board md5 = $(md5sum rl_app_data.json | cut -c1-8)  (expect e2c9bc51)"
echo "### 4. regenerate book (bake) — stable-sha must be 2a74c731"
RL_REPO=$REPO RL_CONFIG_MODE=bake python3 s4_matrix_M1v7.py > /dev/null 2>&1
python3 - <<'PY'
import json,hashlib
d=json.load(open('s4_matrix.json')); by={}
for idk,rec in d.items():
    if idk.startswith('__'): continue
    by[(rec.get('player'),rec.get('type'),rec.get('year'),rec.get('pick'))]=rec
h=hashlib.sha256()
for k in sorted(by.keys(),key=lambda t: json.dumps(t,sort_keys=True)):
    h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
print("book stable-sha =",h.hexdigest()[:16],"(expect 2a74c731e9ce603e)  n=%d"%len(by))
PY
echo "### 5. self-test"
RL_REPO=$REPO python3 one_source_selftest.py 2>&1 | tail -1
echo "### 6. guard-4 canary (edits+restores store)"
RL_REPO=$REPO python3 guard_correction_canary.py 2>&1 | tail -1
echo "store after canary = $(md5sum rl_model_data.json | cut -c1-8)  (expect a2fbc9a0)"
echo "### 7. ship_gates (final head; B3 must be PASS now)"
cd "$REPO"; RL_REPO=$REPO python3 ship_gates_check.py > "$ART/ship_gates_final.txt" 2>&1
grep -E "VERDICT|^B3 |^B4 " "$ART/ship_gates_final.txt"
echo "### 8. panel"
bash "$REPO/run_panel.sh" 2>&1 | grep -E "RESULT"
echo "### 9. shipped board (repo) md5 = $(md5sum $REPO/data/rl_build/rl_app_data.json | cut -c1-8)  (must be e2c9bc51, unchanged)"
echo "FINAL_SUITE_DONE"
} > "$ART/final_suite.log" 2>&1
echo "FINAL_DONE exit-marker" > "$ART/final_done.txt"
