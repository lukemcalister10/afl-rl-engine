"""ORDER 29C — the ROUND-TRIP check, run before the prereg is written.

The matrix's `v0` column is written in ENGINE currency and rounded to 1 dp, because that is the
STANDING emitter's convention (`v0=round(v0_start(p),1)`) and ORDER 29C changes the VALUE, never the
schema or the rounding. The replication proof is stated on the law's own UNROUNDED board-currency
number. This file measures whether the 1-dp matrix cell still round-trips back to the board's printed
integer for the 89 wired rows, so that the packet can state the round-trip as a MEASURED number
rather than assume it survives.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
d0 = json.load(open(sys.argv[1]))
PL_F = 1.0524
ok = bad = 0; mis = []
for r in d0['rows']:
    b = r['derived_v0']
    cell = round(b * PL_F, 1)                 # exactly what the 29C emitter will write
    back = int(round(cell / PL_F))
    if back == r['printed']: ok += 1
    else:
        bad += 1; mis.append((r['key'], r['printed'], back, cell))
print("ROUND-TRIP int(round(matrix_v0 / _PL_F)) == board printed day-0 : %d of %d exact" % (ok, len(d0['rows'])))
if mis: print("  off-by rows (the 1-dp matrix rounding, disclosed): %s" % mis)
json.dump(dict(ok=ok, n=len(d0['rows']), mismatches=mis),
          open(os.path.join(HERE, 'ROUNDTRIP_29C.json'), 'w'), indent=1)
