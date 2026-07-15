#!/bin/bash
# PHASE 2 — isolate the BOARD residual + pick curve + book, frozen engine 2334f570.
set -uo pipefail
REPO=/home/user/afl-rl-engine
export PATH="/root/rl_venv312/bin:$PATH"; export RL_REPO="$REPO"
WS=/home/claude/rl_workspace/rl_after
export PYTHONPATH=$WS:/home/claude/rl_vendor
DIR=$REPO/session_2026-07-14/q97m_followup/P3_crossenv
RES=$DIR/isolation.txt
AVX512_OFF="AVX512F AVX512CD AVX512BW AVX512DQ AVX512VL AVX512_SKX AVX512_CLX AVX512_CNL AVX512_ICL AVX512_SPR AVX512_KNL AVX512_KNM"
: > "$RES"
board () { local label="$1" save="$2"; shift 2
  cd "$WS"; rm -f rl_app_data.json
  env "$@" RL_CONFIG_MODE=gate python3 rl_export.py >/tmp/p2b.log 2>&1
  local md='MISSING'; [ -f rl_app_data.json ] && md=$(md5sum rl_app_data.json|cut -d' ' -f1)
  [ -n "$save" ] && [ -f rl_app_data.json ] && cp rl_app_data.json "$save"
  echo "BOARD  $label : $md" >> "$RES"; }
{
echo "PHASE 2 ISOLATION — frozen engine 2334f570 — native(Haswell/AVX2) board pin 3dc19fbb, SSE 935c2c29"
} >> "$RES"
board "native (Haswell AVX2 BLAS)                   " "$DIR/boardA_native.json"
board "SkylakeX (AVX512 BLAS) — realistic CI boundary" ""  OPENBLAS_CORETYPE=SkylakeX
board "numpy-avx512-off only (BLAS native Haswell)  " ""  NPY_DISABLE_CPU_FEATURES="$AVX512_OFF"
board "SSE (Prescott + numpy-avx512-off)            " "$DIR/boardB_sse.json"  OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$AVX512_OFF"
echo "DONE_boards" >> "$RES"
echo "" >> "$RES"; echo "== BOARD DIFF native vs SSE (804 active) ==" >> "$RES"
python3 "$DIR/board_diff.py" "$DIR/boardA_native.json" "$DIR/boardB_sse.json" >> "$RES" 2>&1
echo "" >> "$RES"; echo "== PICK CURVE native vs SSE ==" >> "$RES"
cd "$WS"
echo "-- NATIVE --" >> "$RES"; python3 "$DIR/pick_curve_dump.py" >> "$RES" 2>&1
echo "-- SSE --" >> "$RES"; OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$AVX512_OFF" python3 "$DIR/pick_curve_dump.py" >> "$RES" 2>&1
echo "== BOOK under SSE (s4_matrix Prescott+numpy-off) — native book stable_sha in P5 results ==" >> "$RES"
CAND=/tmp/sse_book.json
OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$AVX512_OFF" S4_MATRIX=$CAND RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py >/tmp/ssebook.log 2>&1
if [ -f "$CAND" ]; then
python3 - "$CAND" >> "$RES" 2>&1 << 'PY'
import json,sys,hashlib
d=json.load(open(sys.argv[1])); by={}
for k,rec in d.items():
    if k.startswith('__'): continue
    by[(rec.get('player'),rec.get('type'),rec.get('year'),rec.get('pick'))]=rec
h=hashlib.sha256()
for k in sorted(by.keys(), key=lambda t: json.dumps(t,sort_keys=True)):
    h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
print("SSE book stable_sha256:", h.hexdigest(), "n:", len(by))
print("native/sealed stable_sha256: d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f")
print("BOOK MOVES ACROSS ENV:", h.hexdigest()!="d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f")
PY
fi
rm -f "$CAND"
echo "DONE_phase2" >> "$RES"
