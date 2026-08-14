"""ORDER 29C — THE MATRIX IDENTITY ASSERT.

The act's whole claim is that the ONLY difference between ORDER 29B's matrix and ORDER 29C's is the
year-0 column. This file does not repeat that sentence; it DIFFS THE TWO MATRICES, record by record
and field by field, and fails loudly on any non-`v0` difference. If years 1-7 had moved, every
margin below would be uninterpretable, so this runs before the instruments are read.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(sys.argv[1]))     # 29B — the historical-print basis
B = json.load(open(sys.argv[2]))     # 29C — the landed-law basis
OUTJ = sys.argv[3]

RA, RB = A['recs'], B['recs']
print("records: 29B %d   29C %d" % (len(RA), len(RB)))
assert len(RA) == len(RB), "POPULATION MOVED — the two matrices are not comparable"

kA = [(r['key'], r['type'], r['year']) for r in RA]
kB = [(r['key'], r['type'], r['year']) for r in RB]
assert kA == kB, "RECORD ORDER/IDENTITY MOVED"

fieldsA = set().union(*[set(r) for r in RA])
fieldsB = set().union(*[set(r) for r in RB])
print("schema: identical=%s   only_29B=%s   only_29C=%s"
      % (fieldsA == fieldsB, sorted(fieldsA - fieldsB), sorted(fieldsB - fieldsA)))

diff_fields = {}
v0_moved = 0
v0_rows = []
for a, b in zip(RA, RB):
    for f in sorted(set(a) | set(b)):
        if a.get(f) != b.get(f):
            diff_fields.setdefault(f, 0)
            diff_fields[f] += 1
            if f == 'v0':
                v0_moved += 1
                v0_rows.append((a['key'], a['type'], a['v0'], b['v0']))

print("fields that differ anywhere: %s" % diff_fields)
nonv0 = {f: n for f, n in diff_fields.items() if f != 'v0'}
if nonv0:
    print("HALT: NON-v0 FIELDS MOVED — %s" % nonv0)
    sys.exit(1)
print("ASSERT HELD: every field except `v0` is byte-identical on all %d records." % len(RA))
print("v0 cells moved: %d of %d" % (v0_moved, len(RA)))

# meta comparison, printed rather than asserted (meta is the emitter's own identity block)
mA, mB = A['meta'], B['meta']
mdiff = {k: (mA.get(k), mB.get(k)) for k in sorted(set(mA) | set(mB))
         if mA.get(k) != mB.get(k)}
print("meta keys that differ: %s" % sorted(mdiff))
for k in ('store_md5', 'engine_head', 'v0surf_sig', 'v0surf_frozen', 'n_records',
          'nd_curve_last', 'pool_pick'):
    print("  %-14s 29B %-22s 29C %s" % (k, mA.get(k), mB.get(k)))

json.dump(dict(n_records=len(RA), schema_identical=bool(fieldsA == fieldsB),
               fields_differing=diff_fields, non_v0_fields_differing=nonv0,
               v0_moved=v0_moved, meta_keys_differing=sorted(mdiff),
               pins=dict(store_29B=mA.get('store_md5'), store_29C=mB.get('store_md5'),
                         v0surf_29B=mA.get('v0surf_sig'), v0surf_29C=mB.get('v0surf_sig'))),
          open(OUTJ, 'w'), indent=1)
print("wrote %s" % OUTJ)
