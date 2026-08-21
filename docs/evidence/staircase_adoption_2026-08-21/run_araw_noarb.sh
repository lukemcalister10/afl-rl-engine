#!/bin/bash
# THE FOUR B-RAW INSTRUMENT PASSES + THE RENDERED PAGE + THE INPUT CHECKS.
# Order matters: bands -> tables -> class produce the three JSONs that the page and the checks read.
set -uo pipefail
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
D=/home/user/afl-rl-engine/docs/evidence/staircase_adoption_2026-08-21
cd /home/user/afl-rl-engine
export PATH="/root/rl_venv312/bin:$PATH"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
rc=0
# The emit writes to $SP/sfx/; the instruments read per_entrant_<LABEL>.json from $SP root, which is
# where the pricing seat put its three. Same placement, same instruments, no special case.
cp "$SP/sfx/per_entrant_SFXARAW.json" "$SP/per_entrant_SFXARAW.json"
cp "$SP/sfx/EMIT_SFXARAW_out.txt" "$D/EMIT_SFXARAW_out.txt"
echo "per_entrant_SFXARAW.json  $(md5sum "$SP/per_entrant_SFXARAW.json" | cut -c1-32)"
for s in bands tables class; do
  echo "##### araw_noarb_$s.py #####"
  python3 "$D/araw_noarb_$s.py" > "$SP/araw_${s}_run.txt" 2>&1
  r=$?; echo "  exit=$r"; [ $r -ne 0 ] && { rc=1; tail -30 "$SP/araw_${s}_run.txt"; }
done
echo "##### araw_noarb_page.py (SFX_CAND=SFXARAW) #####"
SFX_CAND=SFXARAW python3 "$D/araw_noarb_page.py" > "$SP/araw_page_run.txt" 2>&1
r=$?; echo "  exit=$r"; [ $r -ne 0 ] && { rc=1; tail -30 "$SP/araw_page_run.txt"; }
echo "##### araw_noarb_checks.py #####"
python3 "$D/araw_noarb_checks.py" > "$SP/araw_checks_run.txt" 2>&1
r=$?; echo "  exit=$r (checks exits non-zero when a check FAILS)"
tail -25 "$SP/araw_checks_run.txt"
echo "##### DONE rc=$rc #####"
exit $rc
