#!/bin/bash
# ORDER 29B -- BOTH COHORT NO-ARB INSTRUMENTS ON THE ENTRY-WIRED BOARD (P29B-24 / P29B-26).
#
# Sibling of run_noarb_o29.sh. TWO differences, both because ORDER 29 section 13 already established
# the basis:
#   * THE INSTRUMENTS ARE ORDER 29's DISCLOSED COPIES under docs/evidence/landing_29_2026-08-13/noarb/
#     -- the pair whose five identity literals ORDER 29 re-pointed to the landed basis, with the header
#     log appended. They are COPIED into a scratch run directory and NEVER MODIFIED; their md5s are
#     COMPUTED at run and printed, never hardcoded here.
#   * ORDER 29B RE-POINTS NOTHING. The store does not move (cb38ef11), the surface does not re-bake
#     (4405cba2b42f) and the teaching population does not change (EXPECT_N 1200), so all three pinned
#     literals still hold and the instruments run as committed. If one refuses, the halt is the finding
#     and it is reported verbatim rather than worked around.
#
# THREE MATRICES, so the landed reading has BOTH a live control and the ORDER-29 reading beside it:
#   O29BLIVE   per_entrant_O25R4.json    the PINNED matrix behind the LIVE board 88ce647f. Byte-identical
#                                        input, so its numbers must reproduce NOARB_MARGINS_V2 exactly --
#                                        that reproduction IS the control on this run.
#   O29LANDED  per_entrant_O29FINAL.json ORDER 29's landed matrix (board 86c8d5d9), re-read here so the
#                                        29B column has its immediate predecessor beside it rather than
#                                        a number quoted from a document.
#   O29BFINAL  per_entrant_O29B.json     REGENERATED under the ENTRY-WIRED engine (board 36d5dfc7,
#                                        engine head a353a9d3, artifact 911774bc, store cb38ef11).
#
# The margins reporter is the COMMITTED, UNMODIFIED docs/evidence/pool_final_2026-08-12/o22_margins.py.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/o22/noarb                 # o22_margins.py reads this directory by name; do not move it
E22="$REPO/docs/evidence/pool_final_2026-08-12"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
{
mkdir -p "$N"
cp "$HERE"/noarb/noarb_table_338.py "$HERE"/noarb/noarb_table_allarm.py \
   "$HERE"/noarb/harness_pvc_REPINNED_pass3.py "$N/"
echo "instrument pins COMPUTED at run (ORDER 29's disclosed copies, unmodified by 29B):"
echo "  noarb_table_338.py      $(md5sum "$N/noarb_table_338.py" | cut -c1-32)   <- must be 0f8220351c64c56ccfa90c60edcdfa5f"
echo "  noarb_table_allarm.py   $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
echo "  harness_pvc_REPINNED_pass3.py $(md5sum "$N/harness_pvc_REPINNED_pass3.py" | cut -c1-32)"
cd "$N"
for pair in "$SP/per_entrant_O29FINAL.json:O29LANDED" "$SP/per_entrant_O29B.json:O29BFINAL"; do
  MX="${pair%%:*}"; L="${pair##*:}"
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python noarb_table_338.py "$MX" > "t338_$L.txt" 2>&1
  [ -f noarb_table_338.json ] && mv noarb_table_338.json "table_$L.json"
  python noarb_table_allarm.py "$MX" "$L" > "allarm_$L.txt" 2>&1
  tail -4 "t338_$L.txt"
done
echo
# ---- PHASE 2: THE LIVE-BASIS CONTROL, on the PRE-RE-POINT instrument copies.
# ORDER 29's disclosed copies are pinned to the LANDED store cb38ef11 and therefore REFUSE the live
# matrix (store d9a24282) -- correctly, and that refusal is printed above rather than hidden. The live
# control is what proves the pipeline and this seat are sound, so it is run on the copies that pin the
# LIVE store: docs/evidence/composition_2026-08-10/noarb/, via ORDER 22's own committed, unmodified
# runner. Its numbers must reproduce NOARB_MARGINS_V2 to the last digit.
echo "=== PHASE 2: LIVE-BASIS CONTROL on the PRE-RE-POINT copies (composition_2026-08-10/noarb) ==="
bash "$E22/run_noarb_o22.sh" "$SP/per_entrant_O25R4.json" O29BLIVE
echo
python3 "$E22/o22_margins.py" "$HERE/noarb29b/MARGINS_O29B.json" O29BLIVE O29LANDED O29BFINAL
} 2>&1 | tee "$HERE/NOARB_MARGINS_29B_out.txt"
mkdir -p "$HERE/noarb29b"
cp "$N"/t338_O29BFINAL.txt "$N"/allarm_O29BFINAL.txt "$N"/allarm_O29BFINAL.json \
   "$N"/table_O29BFINAL.json "$HERE/noarb29b/" 2>/dev/null
cp "$HERE/NOARB_MARGINS_29B_out.txt" "$HERE/noarb29b/MARGINS_O29B.txt"
