#!/bin/bash
# A1 LEG B — reproduce the TAG board of record 81e48293 from the tag's OWN tree (9f8ae76 / v2.9).
# Uses the tag's own bootstrap + pins (store b0c39d78, engine 2030e5df, config 69ead79b) => NO boot_guard bypass,
# NO false halt (the false-halt trap is only when the tag's store is run against THIS branch's pins). The tag
# engine FITS q97m at runtime; on this box the fit reproduces cfdc7321 (native == bake box), so it should
# rebuild 81e48293. Restores my branch's workspace at the end.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
MAIN=/home/user/afl-rl-engine
TW=/tmp/tag_v29
OUT=$MAIN/session_2026-07-14/q97m_followup/A1_PROOF
: > $OUT/legB_tag_board.txt
exec >>$OUT/legB_tag_board.txt 2>&1
echo "A1 LEG B — TAG BOARD OF RECORD (tag 9f8ae76 / v2.9) — $(date -u +%FT%TZ)"
echo "=================================================================="

cd "$MAIN"
git worktree remove --force "$TW" 2>/dev/null
git worktree add --detach "$TW" 9f8ae7616555ce55c67ae2076247662960b731e5 2>&1 | tail -2
echo "-- tag tree pins --"
python3 -c "import json;d=json.load(open('$TW/data/expected_boot.json'));print('  store:',d.get('store','?')[:8],'board:',d.get('board','?')[:8],'engine_head:',d.get('engine_head','?')[:8],'config:',(d.get('config') or '-')[:8],'band:',d.get('band','?')[:8]); print('  q97m pin present:', 'q97m' in d)"
echo "-- tag book seal --"
python3 -c "import json;d=json.load(open('$TW/data/book_stable_seal.json'));print('  head_md5:',d.get('head_md5'),'store:',d.get('store_md5'),'stable_sha256:',d.get('stable_sha256'),'n:',d.get('n_players'))" 2>&1 | head -2

echo "-- bootstrap the tag tree (seeds workspace with tag store/engine; Guard 5 = tag's own pins) --"
bash "$TW/bootstrap.sh" > /tmp/tagboot.log 2>&1; echo "  tag bootstrap rc=$?"
grep -E 'PASS|store md5|engine md5|q97m|cm_400' /tmp/tagboot.log | head -6

echo "-- BUILD tag board (rl_export, gate mode, tag config 69ead79b) --"
WS=/home/claude/rl_workspace/rl_after
cd "$WS"; rm -f rl_app_data.json
RL_REPO="$TW" RL_CONFIG_MODE=gate PYTHONPATH=$WS:/home/claude/rl_vendor python3 rl_export.py >/tmp/tagexport.log 2>&1
rc=$?
echo "  rl_export exit=$rc"
if [ -f rl_app_data.json ]; then
  cp rl_app_data.json $OUT/legB_tag_board.json
  echo "  TAG BOARD md5     : $(md5sum rl_app_data.json | cut -d' ' -f1)"
  echo "  EXPECTED (tag pin): 81e48293... (board of record; store b0c39d78 tag 9f8ae76)"
else
  echo "  BOARD MISSING — export tail:"; tail -15 /tmp/tagexport.log
fi

echo "-- BUILD tag book (s4_matrix, tag tree) --"
CAND=/tmp/tag_book.json
RL_REPO="$TW" S4_MATRIX=$CAND RL_CONFIG_MODE=gate PYTHONPATH=$WS:/home/claude/rl_vendor python3 s4_matrix_M1v7.py >/tmp/tagbook.log 2>&1
echo "  s4_matrix exit=$?"
if [ -f "$CAND" ]; then
python3 - "$CAND" "$TW" << 'PY'
import json,sys,hashlib
d=json.load(open(sys.argv[1])); meta=d.get('__meta__',{}); by={}
for k,rec in d.items():
    if k.startswith('__'): continue
    by[(rec.get('player'),rec.get('type'),rec.get('year'),rec.get('pick'))]=rec
h=hashlib.sha256()
for k in sorted(by.keys(), key=lambda t: json.dumps(t,sort_keys=True)):
    h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
seal=json.load(open(sys.argv[2]+'/data/book_stable_seal.json'))
print("  TAG BOOK meta engine:",meta.get('engine_head_md5','?')[:8],"store:",meta.get('store_md5','?')[:8])
print("  TAG BOOK regenerated stable_sha256:", h.hexdigest(), "n:", len(by))
print("  TAG BOOK committed  stable_sha256:", seal.get('stable_sha256'), "n:", seal.get('n_players'))
print("  MATCH:", h.hexdigest()==seal.get('stable_sha256'))
PY
fi
rm -f "$CAND"

echo "-- CLEANUP: remove tag worktree + restore my branch workspace --"
cd "$MAIN"
git worktree remove --force "$TW" 2>&1 | tail -1
bash "$MAIN/bootstrap.sh" >/tmp/reboot.log 2>&1; echo "  my-branch bootstrap rc=$? (workspace restored to 340a7a32/2334f570)"
grep -E 'store md5|engine md5|q97m md5' /tmp/reboot.log | head -3
echo "DONE_legB"
