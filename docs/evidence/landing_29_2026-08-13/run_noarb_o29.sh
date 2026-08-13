#!/bin/bash
# ORDER 29 -- BOTH COHORT NO-ARB INSTRUMENTS ON THE FINAL BOARD (P15).
#
# Sibling of docs/evidence/pool_landing_v2_2026-08-12 run_noarb.sh (the ORDER 25 landing's driver).
# It calls the COMMITTED, UNMODIFIED runner and the COMMITTED, UNMODIFIED margin reporter:
#     docs/evidence/pool_final_2026-08-12/run_noarb_o22.sh   (copies both instruments, computes their
#                                                             md5 pins AT RUN and prints them)
#     docs/evidence/pool_final_2026-08-12/o22_margins.py
# noarb_table_338.py and noarb_table_allarm.py are NOT touched by this file. noarb_table_allarm.py
# asserts noarb_table_338.py's md5 itself and refuses to proceed on a mismatch.
#
# TWO MATRICES, SO THE LANDED READING HAS A LIVE READING BESIDE IT:
#   O29LIVE   = per_entrant_O25R4.json  (3c6ffcde) -- the PINNED matrix behind the LIVE board 88ce647f.
#                                        This is the exact file the ORDER 25 landing scored as
#                                        "O25FINAL"; re-labelled here only so the two readings sit in
#                                        one table. Byte-identical input, so its numbers must
#                                        reproduce NOARB_MARGINS_V2 exactly -- and that reproduction
#                                        is itself the control on this run.
#   O29FINAL  = per_entrant_O29FINAL.json          -- REGENERATED under the LANDED engine by
#                                        emit_variant_o29.sh: landed store cb38ef11, landed board
#                                        86c8d5d9, ruled curve 52aa1125, re-baked surface 4405cba2.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
E22="$REPO/docs/evidence/pool_final_2026-08-12"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
{
bash "$E22/run_noarb_o22.sh" "$SP/per_entrant_O25R4.json" O29LIVE "$SP/per_entrant_O29FINAL.json" O29FINAL
echo
python3 "$E22/o22_margins.py" "$HERE/NOARB_MARGINS_29.json" O29LIVE O29FINAL
} 2>&1 | tee "$HERE/NOARB_MARGINS_29_out.txt"
