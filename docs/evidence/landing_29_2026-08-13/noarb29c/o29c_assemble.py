"""ORDER 29C — assemble NOARB_LANDED_LAW_29C.json from the run artifacts.

Every number in the deliverable is READ FROM THE FILES THE INSTRUMENTS WROTE, never re-typed, so the
document and the evidence cannot drift apart.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
N = sys.argv[1]                                    # the instrument run directory
OUTJ = os.path.join(HERE, 'NOARB_LANDED_LAW_29C.json')

BASES = {
    'LIVE                  (control)': 'O29CLIVE',
    'HISTORICAL-PRINT      (the record)': 'O29BFINAL',
    'LANDED-LAW            (the merge criterion)': 'O29CFINAL',
}
CHARGE = 0.14
R = {'act': 'ORDER 29C — the re-based no-arb reading',
     'brief': '#334 comment 5289123976',
     'board': '36d5dfc73e2b508ece530bc7dfae2090',
     'charge': CHARGE,
     'basis_definitions': {
         'HISTORICAL-PRINT': "year-0 = emit_matrix_338.py:252 `round(v0_start(p),1)`, the FROZEN "
                             "FITTED SURFACE. Years 1-7 = ev(p,Y) under the landed 29B engine. "
                             "MIXED BASIS: landed-law numerator over a pre-landing denominator.",
         'LANDED-LAW': "year-0 = the ORDER 29B entry law's own day-0 price "
                       "(ND: nd_v0.posv[gfut][pick]; pool: pool_v0_of cell; x _PL_F), the same "
                       "object ev() returns for a day-0 entrant on board 36d5dfc7. Years 1-7 "
                       "IDENTICAL to the HISTORICAL-PRINT basis, byte for byte.",
         'LIVE': "the pinned matrix behind live board 88ce647f, read on the pre-re-point instrument "
                 "copies. Pipeline control only.",
     },
     'matrices': {}, 'allarm': [], 'legacy_nd': [], 'by_arm': {}, 'year0_by_arm': {}}

md = json.load(open(os.path.join(HERE, 'MATRIXDIFF_29C.json')))
lp = json.load(open(os.path.join(HERE, 'LAWPROBE_29C.json')))
vd = json.load(open(os.path.join(HERE, 'V0DELTA_29C.json')))
rt = json.load(open(os.path.join(HERE, 'ROUNDTRIP_29C.json')))
R['matrix_identity'] = md
R['replication'] = dict(lp['replication'], board='36d5dfc73e2b508ece530bc7dfae2090',
                        tolerance=0, note='printed integer AND unrounded derived_v0')
R['unmappable'] = dict(n=lp['replication']['n'] and len(lp['unmappable']),
                       rows=lp['unmappable'],
                       gfut_source_census=lp['gfut_source_census'])
R['v0_column_delta'] = vd
R['roundtrip_1dp'] = rt

for bname, lab in BASES.items():
    aj = os.path.join(N, 'allarm_%s.json' % lab)
    tj = os.path.join(N, 'table_%s.json' % lab)
    A = json.load(open(aj))
    R['matrices'][bname] = dict(label=lab, matrix=A['matrix'], store=A['store'][:8],
                                v0surf=A['v0surf'][:12], window_end=A['window_end'],
                                canonical_instrument_md5=A['canonical_instrument_md5'])
    for w, g in A['groups'].items():
        if 'rows' not in g: continue
        yr = {r['N']: r['ratio_meanN_over_mean0'] for r in g['rows']}
        a = yr[1] - 1.0
        R['allarm'].append(dict(basis=bname, instrument='noarb_table_allarm.py', window=w,
                                population='all arms, one cohort', n=g['n'],
                                year_path={str(k): yr[k] for k in sorted(yr)},
                                apprec_0_1=round(100 * a, 2), margin_v14=round(100 * (CHARGE - a), 2),
                                verdict='ARB' if (CHARGE - a) < 0 else 'no arb'))
        R['by_arm'].setdefault(w, {})[bname] = g['by_arm']
    T = json.load(open(tj))
    for gname, G in T['groups'].items():
        rows = {r['N']: r for r in G['rows']}
        # THE INSTRUMENT'S OWN RATIO FIELD, not a re-derivation: this is the exact quantity the
        # canonical margins reporter (o22_margins.py:55) reads, so the document and the reporter
        # cannot disagree in the last digit.
        yr = {k: v['ratio_meanN_over_mean0'] for k, v in rows.items()}
        a = yr[1] / yr[0] - 1.0
        R['legacy_nd'].append(dict(basis=bname, instrument='noarb_table_338.py (UNMODIFIED)',
                                   group=gname, population='legacy ND teaching set', n=rows[0]['n_included'],
                                   year_path={str(k): yr[k] for k in sorted(yr)},
                                   mean_year0=rows[0]['mean_year0_same_set'],
                                   apprec_0_1=round(100 * a, 2), margin_v14=round(100 * (CHARGE - a), 2),
                                   verdict='ARB' if (CHARGE - a) < 0 else 'no arb'))

R['year0_by_arm']['emitter_population'] = lp['by_arm']
R['n_arb'] = {b: sum(1 for x in R['allarm'] + R['legacy_nd']
                     if x['basis'] == b and x['verdict'] == 'ARB') for b in BASES}
json.dump(R, open(OUTJ, 'w'), indent=1)
print("arbitrages by basis: %s" % R['n_arb'])
print("wrote %s" % OUTJ)
