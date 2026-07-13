#!/bin/bash
OUT=/home/user/afl-rl-engine/session_2026-07-13/v2_9_refit_cert/out/wired_candidate_matrix.json
bash /home/user/afl-rl-engine/session_2026-07-13/v2_9_continuation/scripts/gen_matrix.sh "$OUT"
echo "MATRIX_DONE rc=$? bytes=$(wc -c < "$OUT" 2>/dev/null || echo 0)"
