#!/bin/bash
# PHASE 1 MEASUREMENT SUITE (frozen-engine branch f14710d workspace). Absolute paths throughout.
set -uo pipefail
REPO=/home/user/afl-rl-engine
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO="$REPO"
WS=/home/claude/rl_workspace/rl_after
export PYTHONPATH=$WS:/home/claude/rl_vendor
REFIT=$REPO/refit_q97m.py
DIR=$REPO/session_2026-07-14/q97m_followup
RES=$DIR/P4_cause/results.txt
BOOKRES=$DIR/P5_book/results.txt
AVX512_OFF="AVX512F AVX512CD AVX512BW AVX512DQ AVX512VL AVX512_SKX AVX512_CLX AVX512_CNL AVX512_ICL AVX512_SPR AVX512_KNL AVX512_KNM"
ALLSIMD_OFF="$AVX512_OFF AVX2 FMA3 AVX F16C"

: > "$RES"
{
echo "PHASE 1 — box: AVX512 native (OpenBLAS DYNAMIC_ARCH Haswell); native pin q97m=cfdc7321 board=3dc19fbb"
echo "== P4: q97m FIT md5 under isolated CPU knobs =="
} >> "$RES"

fit_under () {  # $1=label  $2..=env assignments
  local label="$1"; shift
  local md
  md=$(env "$@" python3 "$REFIT" --verify 2>>$DIR/P4_cause/stderr.log | grep -oE 'new md5 [0-9a-f]+' | awk '{print $3}')
  echo "q97m_fit  $label : ${md:-FAILED}" >> "$RES"
}
fit_under "baseline_native                         "
fit_under "BLAS-only  OPENBLAS_CORETYPE=Prescott   " OPENBLAS_CORETYPE=Prescott
fit_under "BLAS-only  OPENBLAS_CORETYPE=Nehalem    " OPENBLAS_CORETYPE=Nehalem
fit_under "BLAS-only  OPENBLAS_CORETYPE=SkylakeX   " OPENBLAS_CORETYPE=SkylakeX
fit_under "SIMD-only  NPY_DISABLE=avx512           " NPY_DISABLE_CPU_FEATURES="$AVX512_OFF"
fit_under "SIMD-only  NPY_DISABLE=avx512+avx2+fma  " NPY_DISABLE_CPU_FEATURES="$ALLSIMD_OFF"
fit_under "COMBINED   Prescott + NPYdisable avx512 " OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$AVX512_OFF"
echo "DONE_p4_q97m" >> "$RES"

board_under () {  # $1=label $2..=env
  local label="$1"; shift
  cd "$WS"; rm -f rl_app_data.json
  env "$@" RL_CONFIG_MODE=gate python3 rl_export.py >/tmp/board_build.log 2>&1
  local md='MISSING'; [ -f rl_app_data.json ] && md=$(md5sum rl_app_data.json | cut -d' ' -f1)
  echo "board(frozen 2334f570)  $label : $md" >> "$RES"
}
echo "== P3/P4: BOARD md5 on FROZEN engine 2334f570 (q97m LOADED) — native pin 3dc19fbb ==" >> "$RES"
board_under "baseline_native                              "
board_under "non-avx512  Prescott+NPYdisable avx512        " OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$AVX512_OFF"
board_under "SSE-only    Prescott+NPYdisable avx512+avx2+fma" OPENBLAS_CORETYPE=Prescott NPY_DISABLE_CPU_FEATURES="$ALLSIMD_OFF"
echo "DONE_p3p4_board" >> "$RES"

# working-head BOOK (P0 leg-A + P5)
: > "$BOOKRES"
cd "$WS"
CAND=/tmp/wh_book.json
S4_MATRIX=$CAND RL_CONFIG_MODE=gate python3 s4_matrix_M1v7.py >/tmp/book.log 2>&1
brc=$?
if [ -f "$CAND" ]; then
python3 - "$CAND" >> "$BOOKRES" 2>>$DIR/P5_book/stderr.log << 'PY'
import json,sys,hashlib
d=json.load(open(sys.argv[1])); meta=d.get('__meta__',{}); by={}
for k,rec in d.items():
    if k.startswith('__'): continue
    by[(rec.get('player'),rec.get('type'),rec.get('year'),rec.get('pick'))]=rec
h=hashlib.sha256()
for k in sorted(by.keys(), key=lambda t: json.dumps(t,sort_keys=True)):
    h.update(json.dumps(k,sort_keys=True).encode()); h.update(json.dumps(by[k],sort_keys=True,separators=(',',':')).encode())
print("WORKING-HEAD BOOK (regenerated on engine 2334f570 store 340a7a32):")
print("  __meta__ engine_head:", meta.get('engine_head_md5','?')[:8], "store:", meta.get('store_md5','?')[:8], "config:", (meta.get('config_sha256') or '-')[:12])
print("  regenerated stable_sha256:", h.hexdigest(), " n_players:", len(by))
print("  SEALED baseline (data/book_stable_seal.json): d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f  n=2649  sealed_head=2030e5df")
print("  MATCH:", h.hexdigest()=="d371a27c787a34c93de18c1bcc824c63c63aadcaa68f8a0a4d9c7291871bc44f")
PY
else
  echo "book regen FAILED rc=$brc — see /tmp/book.log" >> "$BOOKRES"
fi
rm -f "$CAND"
echo "DONE_phase1" >> "$RES"
