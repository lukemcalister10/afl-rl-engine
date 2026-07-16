#!/bin/bash
# LEG B SELECTION — clean battery at the WIRED DEFAULT (s=0.10, owner-set item 265).
# NO env override on the ON side: UNCOMP_S_DEFAULT=0.10 drives the map => proves the DEFAULT PATH.
# CONSERVED (shipped C applied): RL_UNCONSERVE stays UNSET. Store b1fd0bce untouched.
# Frozen instruments only (beta_measure 14c59139, ship_gates_check._b1_july8, ledger_dump).
# Sequential + single-threaded BLAS (order-fixed determinism). Writes to out/.
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
DIR="$HERE/session_2026-07-16/legb_selection_s010"
OUT="$DIR/out"
mkdir -p "$OUT"
# seed wired engine + frozen instruments
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/session_2026-07-16/uncompress/beta_measure.py" "$WS/beta_measure.py"
cp -f "$HERE/session_2026-07-16/segment5_law_grid/ledger_dump.py" "$WS/ledger_dump.py"
cp -f "$HERE/session_2026-07-16/legb_conserved_measure/measure_gcohort.py" "$WS/measure_gcohort.py"
[ "$(md5sum "$WS/beta_measure.py"|cut -c1-8)" = "14c59139" ] || { echo "FROZEN beta_measure md5 MISMATCH — HALT"; exit 3; }
cd "$WS"
export RL_REPO="$HERE" PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
echo "== store $(md5sum rl_model_data.json|cut -c1-8) (expect b1fd0bce) | engine $(md5sum _merged_recover.py|cut -c1-8) | s-default $(grep -o 'UNCOMP_S_DEFAULT=[0-9.]*' rl_model.py) =="

echo "[$(date +%H:%M:%S)] OFF baseline (ledger + beta + gcohort) — RL_UNCOMP=0 => board 8d90c9ac"
RL_UNCOMP=0 python3 ledger_dump.py "$OUT/led_OFF.json" >"$OUT/led_OFF.log" 2>&1
RL_UNCOMP=0 python3 beta_measure.py 2>"$OUT/beta_OFF.txt"
RL_UNCOMP=0 python3 measure_gcohort.py OFF >"$OUT/gc_OFF.txt" 2>"$OUT/gc_OFF.err"
echo "[$(date +%H:%M:%S)] OFF beta: $(grep '^s=' "$OUT/beta_OFF.txt") | $(grep RATIOS "$OUT/gc_OFF.txt")"

echo "[$(date +%H:%M:%S)] DEFAULT PATH (no override; s=0.10 wired) — ledger + beta + gcohort"
python3 ledger_dump.py "$OUT/led_default.json" >"$OUT/led_default.log" 2>&1
python3 beta_measure.py 2>"$OUT/beta_default.txt"
python3 measure_gcohort.py default >"$OUT/gc_default.txt" 2>"$OUT/gc_default.err"
echo "[$(date +%H:%M:%S)] DEFAULT beta: $(grep '^s=' "$OUT/beta_default.txt") | $(grep RATIOS "$OUT/gc_default.txt")"

echo "[$(date +%H:%M:%S)] ANALYZE — sincerity ledger + pools + census + E/B + Bontempelli (OFF -> default)"
python3 "$HERE/session_2026-07-16/legb_selection_s010/analyze_s010.py" "$OUT/led_OFF.json" "$OUT/led_default.json" 0.10 >"$OUT/analyze.log" 2>&1
echo "[$(date +%H:%M:%S)] analyze: $(grep PTJSON "$OUT/analyze.log")"

echo "[$(date +%H:%M:%S)] SELF-TEST SUITE — build board+book at default, one_source_selftest (R105.5/R105.4 + SSI)"
cp -f "$HERE"/engine/rl_after/*.py "$WS/" 2>/dev/null
for f in pick_redenomination.json model_config.json; do cp -f "$HERE/engine/rl_after/$f" "$WS/" 2>/dev/null || true; done
rm -f rl_app_data.json s4_matrix.json
python3 rl_export.py >"$OUT/st_export.log" 2>&1; echo "  board md5: $(md5sum rl_app_data.json|cut -c1-8) (expect f2f077b2)"
python3 s4_matrix_M1v7.py >"$OUT/st_book.log" 2>&1; echo "  book built: $(ls -la s4_matrix.json 2>/dev/null|awk '{print $5}') bytes"
python3 one_source_selftest.py >"$OUT/selftest.log" 2>&1; ST=$?
echo "  one_source_selftest EXIT=$ST -> $([ $ST -eq 0 ] && echo 'GREEN' || echo 'RED <<<')"
grep -E "SELF-TEST PASSED|FAIL|R105" "$OUT/selftest.log" | head -20
echo "[$(date +%H:%M:%S)] GUARD 4 correction-canary (full rebuild)"
timeout 1200 python3 guard_correction_canary.py >"$OUT/canary.log" 2>&1; CN=$?
echo "  guard_correction_canary EXIT=$CN -> $([ $CN -eq 0 ] && echo 'GREEN' || echo 'RED/timeout <<<')"
tail -3 "$OUT/canary.log"

echo "[$(date +%H:%M:%S)] S1 STAMPS on the new default board"
python3 - << 'PY' 2>&1 | tee "$OUT/s1_stamps.txt"
import os,stat,hashlib,json
WS=os.getcwd()
for f in ('rl_app_data.json','s4_matrix.json'):
    p=os.path.join(WS,f)
    if not os.path.exists(p): print("  MISSING",f); continue
    md=hashlib.md5(open(p,'rb').read()).hexdigest()[:8]
    mode=stat.S_IMODE(os.stat(p).st_mode)
    smp=p+'.srcmd5'; s=open(smp).read().strip() if os.path.exists(smp) else 'NO-STAMP'
    print("  %-20s md5=%s  mode=0o%o  srcmd5=%s"%(f,md,mode,s))
PY

echo "[$(date +%H:%M:%S)] ALL DONE"
