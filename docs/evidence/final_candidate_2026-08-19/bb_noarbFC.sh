#!/bin/bash
# FINAL-CANDIDATE — the standing no-arb instrument run, ON THE BASE MATRIX ONLY.
#
# THE CANDIDATE IS ABSENT FROM THIS RUN AND THAT IS NOT AN OVERSIGHT. The no-arb instruments read a
# WALK-FORWARD MATRIX, not a board, and daa16812 HAS NO MATRIX: the emit halts on the ORDER 31-F
# day-0 replication guard (PACKET_FINAL section 4). What runs here is per_entrant_FCBASE.json — the
# D5-final BASE ff936186, the candidate minus RL_O42 only.
#
# THIS OUTPUT IS THE BASE'S NO-ARB STATUS. IT IS NOT THE CANDIDATE'S AND IS NEVER TO BE PRESENTED
# AS THE CANDIDATE'S. It is run so the documented-red ledger has measured evidence behind it on the
# nearest board that can carry it, and so the supervisor can see exactly what is and is not known.
# NO OWNER PAGE IS WRITTEN FROM IT.
# ORIGINAL ASSEMBLY HEADER FOLLOWS.
# ORDER S — the standing no-arb instrument runs. ORDER R's file, only the matrix list changed.
# ORIGINAL ORDER R HEADER FOLLOWS.
# ORDER R — the standing no-arb instrument runs. The instruments are ORDER 29's / 31-F's DISCLOSED
# COPIES, copied and NEVER MODIFIED: the extended five-band table (candidate_31f/ext_2026-08-17,
# committed md5 d59ad550116ebbe3d90ed82becd2c4d5 — the owner's standing bands, yr0..12), the canonical
# 338 table, the all-arm cohort instrument, and the ORDER-29 re-pointed harness. Run over THREE
# matrices: the LANDING CANDIDATE (O35FINAL = 1f176444), ORDER K (OKRULED = f3101883) and ORDER P
# (PBUILT). Not one instrument line is modified by this order; the md5s are printed at run.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/fc/noarb
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
{
mkdir -p "$N"
cp "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/noarb_table_338.py \
   "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/noarb_table_allarm.py \
   "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/harness_pvc_REPINNED_pass3.py \
   "$REPO"/docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py "$N/"
cp "$N/harness_pvc_REPINNED_pass3.py" "$N/harness_repointed.py"
echo "instrument pins COMPUTED at run (disclosed copies, unmodified by ORDER S):"
echo "  noarb_table_338.py            $(md5sum "$N/noarb_table_338.py" | cut -c1-32)   <- must be 0f8220351c64c56ccfa90c60edcdfa5f"
echo "  t338_extended_DISCLOSED.py    $(md5sum "$N/t338_extended_DISCLOSED.py" | cut -c1-32)   <- must be d59ad550116ebbe3d90ed82becd2c4d5"
echo "  noarb_table_allarm.py         $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
echo "  harness_pvc_REPINNED_pass3.py $(md5sum "$N/harness_pvc_REPINNED_pass3.py" | cut -c1-32)   <- must begin 02dcf28c"
cd "$N"
for L in FCBASE; do
  MX="$SP/per_entrant_$L.json"
  [ -f "$MX" ] || { echo "=== $L  (MATRIX MISSING — skipped) ==="; continue; }
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python t338_extended_DISCLOSED.py "$MX" > "t338ext_$L.txt" 2>&1 || tail -5 "t338ext_$L.txt"
  for CAND in noarb_table_338_EXT.json noarb_table_338.json; do
    [ -f "$CAND" ] && mv "$CAND" "table_EXT_$L.json"
  done
  python noarb_table_allarm.py "$MX" "$L" > "allarm_run_$L.txt" 2>&1 || tail -5 "allarm_run_$L.txt"
  [ -f "allarm_$L.json" ] || echo "  (no allarm json for $L)"
  tail -3 "t338ext_$L.txt"
done
} 2>&1 | tee "$HERE/NOARB_FCBASE_out.txt"
for L in FCBASE; do
  cp "$N/t338ext_$L.txt" "$HERE/" 2>/dev/null || true
done
