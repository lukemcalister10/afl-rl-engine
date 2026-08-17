#!/bin/bash
# ORDER B — the standing no-arb instrument runs. The instruments are ORDER 29's/31-F's DISCLOSED
# COPIES, copied and never modified: the extended five-band table (candidate_31f/ext_2026-08-17,
# owner-asked bands), the canonical 338 table (md5-asserted by the allarm sibling), the all-arm
# cohort instrument, and the ORDER-29 re-pointed harness. Run over the O32RFINAL control and the
# O33B candidate matrix; the composed two-sided tables come from bb_standing_tables.py after this.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/o33/noarb
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
echo "instrument pins COMPUTED at run (disclosed copies, unmodified by ORDER B):"
echo "  noarb_table_338.py            $(md5sum "$N/noarb_table_338.py" | cut -c1-32)   <- must be 0f8220351c64c56ccfa90c60edcdfa5f"
echo "  t338_extended_DISCLOSED.py    $(md5sum "$N/t338_extended_DISCLOSED.py" | cut -c1-32)"
echo "  noarb_table_allarm.py         $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
echo "  harness_pvc_REPINNED_pass3.py $(md5sum "$N/harness_pvc_REPINNED_pass3.py" | cut -c1-32)   <- must begin 02dcf28c"
cd "$N"
for L in O32RFINAL O33B; do
  MX="$SP/per_entrant_$L.json"
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python t338_extended_DISCLOSED.py "$MX" > "t338ext_$L.txt" 2>&1 || tail -5 "t338ext_$L.txt"
  for CAND in noarb_table_338_EXT.json noarb_table_338.json; do
    [ -f "$CAND" ] && mv "$CAND" "table_EXT_$L.json"
  done
  python noarb_table_allarm.py "$MX" "$L" > "allarm_run_$L.txt" 2>&1 || tail -5 "allarm_run_$L.txt"
  [ -f "allarm_$L.json" ] || echo "  (no allarm json for $L)"
  tail -3 "t338ext_$L.txt"
done
} 2>&1 | tee "$HERE/NOARB_B_out.txt"
cp "$N"/t338ext_O33B.txt "$N"/t338ext_O32RFINAL.txt "$HERE/" 2>/dev/null || true
