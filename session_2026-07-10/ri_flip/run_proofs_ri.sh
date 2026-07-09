#!/bin/bash
# R-i FLIP PROOFS — regenerate the advance candidate board and run the full acceptance suite from a fresh
# bootstrap. Advance is now the CODE DEFAULT (owner ruling R-i, DECISIONS v90 §36); the board is built in
# GATE mode so the manifest pins RL_LTI_CLOCK=advance into artifact identity. Proves: only the R-i register
# names move vs the merged head (byte parity elsewhere) · full suite green · reds exactly {A2,A3,A12} ·
# store a2fbc9a0 UNCHANGED. Comparand = the merged-head (pause) board committed at 99941f1 (md5 d9728208).
set -e
REPO=/home/user/afl-rl-engine; WS=/home/claude/rl_workspace/rl_after
ART=$REPO/session_2026-07-10/ri_flip/artifacts; mkdir -p "$ART"
git -C "$REPO" show 99941f1:data/rl_build/rl_app_data.json > /tmp/board_mergedhead.json
python3 "$REPO/session_2026-07-10/ri_flip/restamp_ri.py" >/dev/null
bash "$REPO/bootstrap.sh" >/dev/null 2>&1
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor

echo "### building ADVANCE candidate board (GATE mode = manifest-pinned advance)"
chmod +w rl_app_data.json rl_app_data.json.srcmd5 2>/dev/null || true
RL_REPO=$REPO RL_CONFIG_MODE=gate python3 rl_export.py >/dev/null 2>&1
BMD5=$(md5sum rl_app_data.json | cut -c1-8)
echo "advance candidate board md5=$BMD5"
cp -f rl_app_data.json /tmp/board_advance.json
cp -f rl_app_data.json "$REPO/data/rl_build/rl_app_data.json"     # repo (committed) shipped board
cp -f rl_app_data.json /home/claude/rl_build/rl_app_data.json     # runtime shipped board (B4 comparand)
# stamp the board pin from the freshly-built advance board
python3 - "$BMD5" <<'PY'
import json,sys
eb=json.load(open('/home/user/afl-rl-engine/data/expected_boot.json')); eb['board']=sys.argv[1]
open('/home/user/afl-rl-engine/data/expected_boot.json','w').write(json.dumps(eb,indent=1)+'\n')
PY

echo "### R-i board parity (advance vs merged-head pause)"
python3 - <<'PY' | tee "$ART/nonmover_parity_ri.txt"
import json, lti_register as LR
adv={r['key']:r for r in json.load(open('/tmp/board_advance.json'))['active']}
pau={r['key']:r for r in json.load(open('/tmp/board_mergedhead.json'))['active']}
store=json.load(open('rl_model_data.json')); regkeys=set(LR.build_state({p['key']:p for p in store}))
allkeys=set(adv)|set(pau)
movers=[k for k in allkeys if adv.get(k,{}).get('v')!=pau.get(k,{}).get('v')]
nonreg=[k for k in movers if k not in regkeys]
bytediff=[k for k in (set(adv)&set(pau)) if json.dumps(adv[k],sort_keys=True)!=json.dumps(pau[k],sort_keys=True)]
byte_nonreg=[k for k in bytediff if k not in regkeys]
print("R-i BOARD PARITY (advance %s vs merged-head pause d9728208):"%(len(adv)))
print("  value movers=%d  register movers=%d  NON-REGISTER movers=%d  byte diffs=%d  NON-REGISTER byte diffs=%d"%(
      len(movers),len([k for k in movers if k in regkeys]),len(nonreg),len(bytediff),len(byte_nonreg)))
print("  PARITY %s"%("PASS — only R-i register names move; byte-identical elsewhere" if not byte_nonreg else "FAIL: %s"%byte_nonreg[:20]))
for k in sorted(movers,key=lambda k:pau.get(k,{}).get('v',0)-adv.get(k,{}).get('v',0),reverse=True):
    a=adv.get(k,{}).get('v'); p=pau.get(k,{}).get('v'); nm=adv.get(k,{}).get('name') or pau.get(k,{}).get('name') or k
    print("    %-22s pause=%-6s advance=%-6s d=%+d"%(nm,p,a,a-p))
PY

echo "### build the book (s4_matrix_M1v7.py) — F2/B3 input; CI-order: before the self-test"
RL_REPO=$REPO RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py >/dev/null 2>&1 || echo "s4_matrix note"
echo "### self-test (guards 1-5 + F1/F2 + collision sentry) — RL_REPO set so Guard 5 locates the checkout"
RL_REPO=$REPO python3 one_source_selftest.py > "$ART/selftest.txt" 2>&1 || true; tail -2 "$ART/selftest.txt"
echo "### guard 4 correction canary"
python3 guard_correction_canary.py > "$ART/canary.txt" 2>&1 || true; tail -1 "$ART/canary.txt"
echo "### ruling-config (incl. NEW R-i assertion)"
RL_REPO=$REPO python3 "$REPO/ruling_config_check.py" > "$ART/ruling_config.txt" 2>&1 || true; tail -1 "$ART/ruling_config.txt"
echo "### config-manifest check"
RL_REPO=$REPO python3 "$REPO/config_manifest.py" check > "$ART/config_manifest.txt" 2>&1 || true; tail -1 "$ART/config_manifest.txt"
echo "### ship_gates"
cd "$REPO"; RL_REPO="$REPO" python3 ship_gates_check.py > "$ART/ship_gates.txt" 2>&1 || true
grep -E "VERDICT|^A2|^A3 |^A12|^B1 |^B3 |^B4 |^B5 " "$ART/ship_gates.txt"
echo "### panel"; bash "$REPO/run_panel.sh" 2>&1 | tail -1
echo "### store md5 (must be a2fbc9a0)"; md5sum "$REPO/engine/rl_after/rl_model_data.json" | cut -c1-8
echo "### PROOFS DONE (advance board md5=$BMD5)"
