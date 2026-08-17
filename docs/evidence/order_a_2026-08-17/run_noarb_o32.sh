#!/bin/bash
# ORDER A / CANDIDATE 32 -- THE STANDING NO-ARB INSTRUMENT SUITE, run on the fresh Candidate 32
# matrix. Sibling of docs/evidence/candidate_31f/run_noarb_o31f.sh, carried. THE INSTRUMENTS ARE
# ORDER 29's DISCLOSED COPIES (landing_29_2026-08-13/noarb), COPIED and NEVER MODIFIED. md5s are
# COMPUTED at run and printed; the canonical pins asserted in the console: noarb_table_338.py must
# be 0f8220351c64c56ccfa90c60edcdfa5f and the harness 02dcf28c. O29CFINAL is re-run beside it as
# the same-session pipeline control. Margins: the COMMITTED o22_margins.py, 14% carry, arb iff
# margin < 0, over O31FLIVE (live-basis control, already produced by the 31-F act) + O31FFINAL
# (Candidate 31) + O32FINAL (this candidate).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/o22/noarb                 # o22_margins.py reads this directory BY NAME; do not move it
E22="$REPO/docs/evidence/pool_final_2026-08-12"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
{
mkdir -p "$N"
cp "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/noarb_table_338.py \
   "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/noarb_table_allarm.py \
   "$REPO"/docs/evidence/landing_29_2026-08-13/noarb/harness_pvc_REPINNED_pass3.py "$N/"
echo "instrument pins COMPUTED at run (ORDER 29's disclosed copies, unmodified by ORDER A):"
echo "  noarb_table_338.py            $(md5sum "$N/noarb_table_338.py" | cut -c1-32)   <- must be 0f8220351c64c56ccfa90c60edcdfa5f"
echo "  noarb_table_allarm.py         $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
echo "  harness_pvc_REPINNED_pass3.py $(md5sum "$N/harness_pvc_REPINNED_pass3.py" | cut -c1-32)   <- must begin 02dcf28c"
cd "$N"
for pair in "$SP/per_entrant_O29CFINAL.json:O29CFINAL" "$SP/per_entrant_O32FINAL.json:O32FINAL"; do
  MX="${pair%%:*}"; L="${pair##*:}"
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python noarb_table_338.py "$MX" > "t338_$L.txt" 2>&1
  [ -f noarb_table_338.json ] && mv noarb_table_338.json "table_$L.json"
  python noarb_table_allarm.py "$MX" "$L" > "allarm_$L.txt" 2>&1
  tail -4 "t338_$L.txt"
done
echo
python3 "$E22/o22_margins.py" "$HERE/MARGINS_O32.json" O31FLIVE O31FFINAL O32FINAL
} 2>&1 | tee "$HERE/NOARB_MARGINS_32_out.txt"
cp "$N"/t338_O32FINAL.txt "$N"/allarm_O32FINAL.txt "$N"/allarm_O32FINAL.json \
   "$N"/table_O32FINAL.json "$HERE/" 2>/dev/null
cp "$N"/t338_O29CFINAL.txt "$HERE/t338_O29CFINAL_control32.txt" 2>/dev/null
