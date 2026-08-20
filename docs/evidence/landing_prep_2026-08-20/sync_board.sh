#!/bin/bash
# C3 COMPANION ACT — sync data/rl_build/rl_app_data.json to THE CANDIDATE BOARD a05fe951.
#
# WHY THIS EXISTS, AND WHY IT IS NOT "REALITY BENT TO MATCH A PIN".
#   boot_guard (0c) asserts the CHECKED-OUT data/rl_build/rl_app_data.json == the 'board' pin. So
#   the board pin cannot be re-stamped to the candidate on its own: pin and artifact move together
#   or Guard 5 goes red on the board leg. This is the SAME pairing ORDER 29B performed at 0260787
#   ("data/rl_build/rl_app_data.json synced to the new board -- Guard 5 asserts THAT copy, not the
#   engine one, and it fired in anger when it was stale"), and ORDER 25 / ORDER 23 before it
#   ("THE BOARD REBUILT DETERMINISTICALLY, AND THE PINS RESTAMPED").
#   The board written here is not authored: it is the byte-exact output of the candidate dial line
#   in docs/evidence/parity_2026-08-19/build_D7B.sh, reproduced in this seat and md5-verified
#   a05fe951f78482c70520480e184c80ec BEFORE and AFTER the copy.
#
# LEFT UNTOUCHED, DELIBERATELY, both per 0260787's own disclosure:
#   engine/rl_after/rl_app_data.json  — the engine-side copy Guard 5 does NOT assert (bbD7.sh
#       removes it from staging before every export, so it is never a build input).
#   data/rl_build/rl_app_data.json.srcmd5 — source_md5 is the STORE (cb38ef11), and the store does
#       not move in this act; own_md5 stays 4b448a82 per its documented contract. It was already
#       unequal to the committed board md5 before this act (pre-existing, disclosed, not created here).
#
# NOT ADOPTED. OWNER WORD PENDING. No tag, no main promote, the live board is untouched.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
SRC="${CAND_BOARD:?CAND_BOARD must point at the reproduced candidate board}"
DST="$ROOT/data/rl_build/rl_app_data.json"
EXPECT=a05fe951f78482c70520480e184c80ec

echo "=== C3 COMPANION — BOARD ARTIFACT SYNC ==="
echo "  source (reproduced this seat) : $SRC"
S=$(md5sum "$SRC" | cut -d' ' -f1)
echo "  source md5                    : $S"
[ "$S" = "$EXPECT" ] || { echo "HALT: source board $S != candidate $EXPECT"; exit 1; }
O=$(md5sum "$DST" | cut -d' ' -f1)
echo "  data/rl_build board BEFORE    : $O"
cp -f "$SRC" "$DST"
N=$(md5sum "$DST" | cut -d' ' -f1)
echo "  data/rl_build board AFTER     : $N"
[ "$N" = "$EXPECT" ] || { echo "HALT: destination board $N != candidate $EXPECT"; exit 1; }
echo "  engine-side copy (untouched)  : $(md5sum "$ROOT/engine/rl_after/rl_app_data.json" | cut -d' ' -f1)"
echo "  srcmd5 sidecar   (untouched)  : $(md5sum "$DST.srcmd5" | cut -d' ' -f1)"
echo "SYNC OK  $O -> $N"
