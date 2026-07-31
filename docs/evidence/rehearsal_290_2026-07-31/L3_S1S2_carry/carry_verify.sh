#!/usr/bin/env bash
# S-1/S-2 CARRY — the verification, re-runnable. #290 L3 act (2), 2026-07-31.
#
# Proves three things, in order, and prints nothing it has not measured:
#   A. ROUND TRIP  — the carried lane reproduces the RULED stop-point curve from the matrix it was
#                    originally derived from: payload e69a3f38, ladder 54,722, s 0.977688,
#                    pooled_head_pre_scale 3068.4647 (the N14 primitive).
#   B. INTERLOCK   — the harness/matrix pairing assert fires on BOTH cross-pairings and passes on
#                    both correct ones. Four cells, because a guard proven in one direction is half
#                    a guard.
#   C. RULED PASS  — S-1/S-2 on the committed ruled matrix: the provenance counts, their
#                    sums-to-population assert, and the WATCHED NUMBER with its denominator; then a
#                    FIRST-PASS candidate curve on the ruled substrate.
#
# C's curve is a WAYPOINT, NOT A LANDING FIGURE. Nothing between L1 and L6 is one. It is a single
# pass; L6's convergence iterates curve <-> surface and is where a fixed point is reached.
#
# Run from the repo root:  bash docs/evidence/rehearsal_290_2026-07-31/L3_S1S2_carry/carry_verify.sh
set -u

PANEL=session_2026-07-30/item279/panel
M_VOR=session_2026-07-30/item279/out/per_entrant_279_vor.json
M_RULED=docs/evidence/rehearsal_290_2026-07-31/L3_watched_number/nd_matrix_ruled.json
REPIN_SRC=session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py

bash tools/preboot_assert.sh || exit 1
[ -n "${RL_VENV:-}" ] && export PATH="$RL_VENV/bin:$PATH"

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
# the re-pinned harness is staged UNDER THE NAME harness_pvc.py, never committed under it:
# two importable files of one name with different pins would be the hazard this guards against.
mkdir -p "$TMP/repin" "$TMP/outA" "$TMP/outC"
cp "$REPIN_SRC" "$TMP/repin/harness_pvc.py"
cp $PANEL/fitter_*.py $PANEL/pooled_numeraire.py "$TMP/repin/"

echo "=============================================================================="
echo "A · ROUND TRIP — the carried lane vs the ruled stop-point curve"
echo "=============================================================================="
echo "matrix : $M_VOR"
echo "md5    : $(md5sum $M_VOR | cut -d' ' -f1)   (expect 77eba4d308a27a881b36a5424d3bb389)"
PYTHONPATH=$PANEL python3 $PANEL/pooled_numeraire.py "$M_VOR" "$PANEL" "$TMP/outA" >/dev/null 2>&1
echo "lane exit: $?"
PYTHONPATH=$PANEL python3 - "$TMP/outA" <<'PY'
import json, glob, sys
d = json.load(open(glob.glob(sys.argv[1] + '/*.json')[0]))
want = {'payload': 'e69a3f38', 'ladder': 54722, 's': 0.977688, 'head': 3068.4647}
got = {'payload': d['payloads']['ruled'], 'ladder': d['ladder_totals']['ruled'],
       's': d['THE_FACTOR_S']['s'], 'head': d['THE_FACTOR_S']['pooled_head_pre_scale']}
for k in ('payload', 'ladder', 's', 'head'):
    print('  %-8s got %-12s want %-12s %s' % (k, got[k], want[k], 'MATCH' if got[k] == want[k] else 'DIVERGES'))
print('  VERDICT: %s' % ('ROUND TRIP PROVEN — the carried lane IS the lane that produced the ruled curve'
                         if got == want else 'HALT — the carried lane does not reproduce the ruled curve'))
PY

echo
echo "=============================================================================="
echo "B · INTERLOCK — the pairing assert, proven able to fire, all four cells"
echo "=============================================================================="
run_cell () {  # $1 pythonpath  $2 matrix  $3 label  $4 expect(HALT|PASS)
  PYTHONPATH=$1 python3 - "$2" "$3" "$4" <<'PY'
import sys, harness_pvc as H
mat, label, expect = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    meta, nd = H.load_matrix(mat)
    got, detail = 'PASS', 'ND=%d' % len(nd)
except AssertionError as e:
    got, detail = 'HALT', str(e)[:78]
print('  %-28s %-4s (expect %-4s) %s  %s' % (label, got, expect, 'OK' if got == expect else 'WRONG', detail))
PY
}
run_cell "$PANEL"     "$M_RULED" "ORIG harness + RULED mx"   HALT
run_cell "$TMP/repin" "$M_VOR"   "REPIN harness + VOR mx"    HALT
run_cell "$PANEL"     "$M_VOR"   "ORIG harness + VOR mx"     PASS
run_cell "$TMP/repin" "$M_RULED" "REPIN harness + RULED mx"  PASS

echo
echo "=============================================================================="
echo "C · THE RULED SUBSTRATE — S-1/S-2, the watched number, and a FIRST-PASS candidate"
echo "=============================================================================="
PYTHONPATH=$TMP/repin python3 - "$M_RULED" <<'PY'
import json, sys, harness_pvc as H
meta, ND = H.load_matrix(sys.argv[1])
rows, prov = H.structural_values(ND)
c, n = prov['counts'], prov['of_population']
print('  substrate  : store %s · v0surf %s · frozen %s'
      % (meta['store_md5'], meta['v0surf_sig'][:12], meta.get('v0surf_frozen')))
print('  counts     : %s' % json.dumps(c, sort_keys=True))
tot = c.get('concluded_realised', 0) + c.get('completed', 0) + prov['fallback_rows']
print('  sums assert: %d + %d + %d = %d == %d  %s'
      % (c.get('concluded_realised', 0), c.get('completed', 0), prov['fallback_rows'], tot, n,
         'OK' if tot == n else 'HALT'))
print('  S-1        : %d of %d = %.1f%% concluded, realised at FULL weight, prior RETIRED'
      % (c['concluded_realised'], n, 100.0 * c['concluded_realised'] / n))
print('  S-2        : %d of %d = %.1f%% actives completed actuarially from concluded look-alikes'
      % (c['completed'], n, 100.0 * c['completed'] / n))
print('  WATCHED    : %d of %d = %s%% counted thin-stratum fallback'
      % (prov['fallback_rows'], n, prov['fallback_share_pct']))
PY
PYTHONPATH=$TMP/repin python3 "$TMP/repin/pooled_numeraire.py" "$M_RULED" "$TMP/repin" "$TMP/outC" >/dev/null 2>&1
echo "  lane exit  : $?"
python3 - "$TMP/outC" <<'PY'
import json, glob, sys
d = json.load(open(glob.glob(sys.argv[1] + '/*.json')[0]))
print('  payload    : %s        (stop-point was e69a3f38)' % d['payloads']['ruled'])
print('  ladder     : %s           (stop-point was 54722)' % d['ladder_totals']['ruled'])
print('  s          : %s' % d['THE_FACTOR_S']['s'])
print('  head       : %s        (stop-point was 3068.4647)' % d['THE_FACTOR_S']['pooled_head_pre_scale'])
print()
print('  WAYPOINT, NOT A LANDING FIGURE. One pass, not a fixed point. L6 converges.')
PY
