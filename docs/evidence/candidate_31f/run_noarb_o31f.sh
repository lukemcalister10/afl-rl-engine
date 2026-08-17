#!/bin/bash
# ORDER 31-F -- BOTH COHORT NO-ARB INSTRUMENTS ON THE CANDIDATE AND ON LIVE, SIDE BY SIDE.
#
# Sibling of run_noarb_o29b.sh, carried. THE INSTRUMENTS ARE ORDER 29's DISCLOSED COPIES under
# docs/evidence/landing_29_2026-08-13/noarb/ -- the pair whose five identity literals ORDER 29
# re-pointed at the landed basis -- COPIED into a scratch run directory and NEVER MODIFIED by this
# act. Their md5s are COMPUTED at run and printed, never hardcoded here. ORDER 29C RE-POINTS NOTHING:
# the store does not move (cb38ef11), the surface does not re-bake (4405cba2b42f) and the teaching
# population does not change (EXPECT_N 1200), so all three pinned literals must still hold. IF ONE
# REFUSES, THE HALT IS THE FINDING and it is reported verbatim rather than worked around.
#
# THREE MATRICES:
#   O29CLIVE    per_entrant_O25R4.json      the PINNED matrix behind the LIVE board 88ce647f. Run on
#                                           the PRE-re-point copies (composition_2026-08-10/noarb) via
#                                           ORDER 22's own committed runner, because ORDER 29's copies
#                                           pin the LANDED store and correctly REFUSE the live matrix.
#                                           Reproducing NOARB_MARGINS_V2 is the pipeline control.
#   O29BFINAL   per_entrant_O29B.json       THE HISTORICAL-PRINT BASIS (the record). Re-run here rather
#                                           than quoted from a document, so the two bases are read by
#                                           the SAME instrument copies in the SAME session. Must
#                                           reproduce NOARB_MARGINS_29.md section B2 to the digit.
#   O29CFINAL   per_entrant_O29CFINAL.json  THE LANDED-LAW BASIS -- the merge criterion. Identical to
#                                           the 29B matrix in every field except v0 (asserted by
#                                           o29c_matrixdiff.py before this script runs).
#
# The margins reporter is the COMMITTED, UNMODIFIED docs/evidence/pool_final_2026-08-12/o22_margins.py.
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
echo "instrument pins COMPUTED at run (ORDER 29's disclosed copies, unmodified by 31-F):"
echo "  noarb_table_338.py            $(md5sum "$N/noarb_table_338.py" | cut -c1-32)   <- must be 0f8220351c64c56ccfa90c60edcdfa5f"
echo "  noarb_table_allarm.py         $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
echo "  harness_pvc_REPINNED_pass3.py $(md5sum "$N/harness_pvc_REPINNED_pass3.py" | cut -c1-32)"
echo "  emit_matrix_338.py (STANDING) $(md5sum "$REPO/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" | cut -c1-32)   <- must be bffde2f786be85037483e9f5f1563068"
cd "$N"
for pair in "$SP/per_entrant_O29CFINAL.json:O29CFINAL" "$SP/per_entrant_O31FFINAL.json:O31FFINAL"; do
  MX="${pair%%:*}"; L="${pair##*:}"
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python noarb_table_338.py "$MX" > "t338_$L.txt" 2>&1
  [ -f noarb_table_338.json ] && mv noarb_table_338.json "table_$L.json"
  python noarb_table_allarm.py "$MX" "$L" > "allarm_$L.txt" 2>&1
  tail -4 "t338_$L.txt"
done
echo
echo "=== PHASE 2: LIVE-BASIS CONTROL on the PRE-RE-POINT copies (composition_2026-08-10/noarb) ==="
bash "$E22/run_noarb_o22.sh" "$SP/per_entrant_O25R4.json" O31FLIVE
echo
python3 "$E22/o22_margins.py" "$HERE/MARGINS_O31F.json" O31FLIVE O29CFINAL O31FFINAL
} 2>&1 | tee "$HERE/NOARB_MARGINS_31F_out.txt"
cp "$N"/t338_O31FFINAL.txt "$N"/allarm_O31FFINAL.txt "$N"/allarm_O31FFINAL.json \
   "$N"/table_O31FFINAL.json "$HERE/" 2>/dev/null
cp "$N"/t338_O31FLIVE.txt "$N"/allarm_O31FLIVE.txt "$N"/table_O31FLIVE.json "$HERE/" 2>/dev/null
cp "$N"/t338_O29CFINAL.txt "$HERE/t338_O29CFINAL_control.txt" 2>/dev/null
cp "$HERE/NOARB_MARGINS_31F_out.txt" "$HERE/MARGINS_O31F.txt"
