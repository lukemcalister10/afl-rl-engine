#!/bin/bash
# THE BAKE — THE EMIT, RUN BARE (falsifiers F4 and F6). register v780, 2026-08-20.
#
# docs/evidence/final_candidate_2026-08-19/run_emit_CP.sh is invoked COMPLETELY UNMODIFIED and with
# **NO DIAL EXPORTED AT ALL**. That is the whole test, and it is a sharp one:
#
#   PRE-FLIP, THIS EXACT RUN FAILED CLOSED. The landing-prep seat disclosed it in run_emit_LP.sh's own
#   header — "First attempt in this seat was run WITHOUT the dial line exported; the guard failed closed
#   at 1 of 89 and no matrix was written." run_emit_LP.sh therefore had to export the 29-assignment dial
#   line by hand to reach 89 of 89.
#
#   POST-FLIP, THE DIAL LINE IS THE DEFAULT. So the bare run must now read 89 of 89 by itself. If it
#   reads anything else, F4 has FIRED: the ORDER 31-F replication guard fails closed, no matrix is used,
#   and this seat reports the count rather than re-basing the reference. THE REFERENCE IS NOT RE-BASED —
#   the guard is pointed at the FROZEN docs/evidence/final_candidate_2026-08-19/DAY0_CP.json, unchanged.
#
# F6 (the class mark): the matrix this produces is byte-compared against per_entrant_LP.json (c231fda2),
# the matrix the landing-prep seat emitted PRE-FLIP with the full dial line exported. If the two are
# byte-identical the matrix identity has not moved, and the registered class mark 1.0672 stands without
# needing to be re-derived. If they differ, the class instrument is re-run and THE NEW MARK IS REPORTED.
#
# NOT ADOPTED. OWNER WORD PENDING.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad

echo "=== THE EMIT, BARE — no RL_O* dial exported anywhere in this script ==="
echo "  engine   : $(md5sum "$REPO/engine/rl_after/_merged_recover.py" | cut -c1-32)"
echo "  rl_model : $(md5sum "$REPO/engine/rl_after/rl_model.py" | cut -c1-32)"
echo "  day-0 ref: FROZEN docs/evidence/final_candidate_2026-08-19/DAY0_CP.json (NOT re-based)"
echo "  set RL_O* in this shell: $(env | grep -c '^RL_O' || true)   <-- must be 0"
env | grep '^RL_O' && { echo "HALT: an RL_O* dial is set; this would not be a bare run."; exit 2; }

OP_LABEL=${OP_LABEL:-BK} bash "$REPO/docs/evidence/final_candidate_2026-08-19/run_emit_CP.sh"
RC=$?

echo
echo "=== F6 — MATRIX IDENTITY, BYTE-COMPARED AGAINST THE PRE-FLIP EMIT ==="
NEW="$SP/per_entrant_${OP_LABEL:-BK}.json"
OLD="$SP/per_entrant_LP.json"
if [ -f "$NEW" ] && [ -f "$OLD" ]; then
  N=$(md5sum "$NEW" | cut -c1-32); O=$(md5sum "$OLD" | cut -c1-32)
  echo "  post-flip BARE emit : $N"
  echo "  pre-flip  LP   emit : $O   (registered c231fda2, dial line exported by hand)"
  if [ "$N" = "$O" ]; then
    echo "  VERDICT: BYTE-IDENTICAL — the matrix identity has NOT moved, so the class mark 1.0672 stands."
  else
    echo "  VERDICT: THE MATRIX MOVED. Re-run the class instrument and REPORT THE NEW MARK. Do not restate 1.0672."
  fi
else
  echo "  NO MATRIX — the emit did not write one (the replication guard fails closed). F4 has FIRED."
fi
exit $RC
