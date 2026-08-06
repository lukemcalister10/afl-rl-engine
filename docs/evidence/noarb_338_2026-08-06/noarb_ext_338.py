# noarb_ext_338.py -- the extended cuts (years 0..9, the 2020 class, the recency windows).
# COPY of docs/evidence/noarb_2026-08-05/noarb_ext.py, re-pointed to the #338 matrix. The original is
# FILED EVIDENCE and is NOT touched. Diff = the input matrix name and the import name; no method change.
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_pvc_REPINNED_pass3 as H
from noarb_table_338 import value_at
HERE = os.path.dirname(os.path.abspath(__file__))
MATRIX = os.path.join(HERE, 'per_entrant_338_confirmation.json')
meta, ND = H.load_matrix(MATRIX)
full = json.load(open(MATRIX))['recs']
WINDOW_END = max(y for r in full for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

def table(rows, years, label):
    print('==', label, 'cohort n=%d classes %d-%d' % (len(rows), min(r['year'] for r in rows), max(r['year'] for r in rows)))
    print('  yr |    n  zero | mean_yrN  mean_yr0  ratio | total_yrN(k)')
    for N in years:
        inc = [r for r in rows if r['year'] + N <= WINDOW_END]
        if not inc: continue
        vals = [value_at(r, N)[0] for r in inc]
        v0s = [float(r['v0']) for r in inc]
        zeros = sum(1 for v in vals if v == 0.0)
        m, m0 = sum(vals)/len(vals), sum(v0s)/len(v0s)
        print('  %2d | %4d  %4d |  %7.1f   %7.1f  %5.3f |  %8.1f' % (N, len(inc), zeros, m, m0, m/m0, sum(vals)/1000))

table(ND, range(0, 10), 'ALL picks 1-64, classes 2004-2022')
c2020 = [r for r in ND if r['year'] == 2020]
table(c2020, range(0, 7), '2020 draft class only')
print('2020 class picks present:', sorted(r['pick'] for r in c2020)[:12], '...')
for lo, name in ((2013, 'last 10 classes (2013-2022)'), (2011, 'last 12 (2011-2022)'), (2008, 'last 15 (2008-2022)')):
    table([r for r in ND if r['year'] >= lo], range(0, 8), name)
