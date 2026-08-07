"""334 stage B / stage 3 STEP 1 — the BASE-CURVE RE-TEACH, era-free.

Machinery of record: session_2026-07-30/item279/panel/harness_pvc.py, re-pinned copy
docs/evidence/act_334B_2026-08-07/stage2_erafree/harness_pvc_REPINNED_pass3.py.

  base_erafree = H.pin_and_check(H.kernel_raw(H.structural_values(ND), 1..64))

Runs the same derivation across FOUR matrices so the delta vs the shipped base can be
ATTRIBUTED rather than asserted:

  A  per_entrant_328_corrected_store.json  store f1e8c9fe  — the matrix the SHIPPED base was derived from
  B  per_entrant_338_confirmation.json     store 37ced3ce  — A + the current gate store + #338 tenure
  C  per_entrant_338_stage1basis.json      store 37ced3ce  — B + the #336 reference layer  (era-ADJUSTED)
  D  per_entrant_338_erafree.json          store 37ced3ce  — C with era normalization removed  (THE BASIS)

Each matrix is loaded with the harness loader, with the store/surface pins RE-POINTED to that
matrix's own committed meta (never patched away: the assert stays, the value moves, and both the
old and the new value are printed).
"""
import os, sys, json, math, hashlib, importlib.util, collections
import numpy as np

REPO = '/home/claude/seamcheck_landing'
EV = os.path.join(REPO, 'docs/evidence')
HARNESS = os.path.join(EV, 'act_334B_2026-08-07/stage2_erafree/harness_pvc_REPINNED_pass3.py')

spec = importlib.util.spec_from_file_location('harness_pvc', HARNESS)
H = importlib.util.module_from_spec(spec)
sys.modules['harness_pvc'] = H
spec.loader.exec_module(H)

PICKS = list(range(1, 65))

MATRICES = [
 ('A_328_shipped_basis', os.path.join(EV, 'store_328_jujn3g/per_entrant_328_corrected_store.json')),
 ('B_338_tenure',        os.path.join(EV, 'noarb_338_2026-08-06/per_entrant_338_confirmation.json')),
 ('C_338_336layer_era',  os.path.join(EV, 'act_334B_2026-08-07/stage2/per_entrant_338_stage1basis.json')),
 ('D_338_336layer_free', os.path.join(EV, 'act_334B_2026-08-07/stage2_erafree/per_entrant_338_erafree.json')),
]


def load_repinned(path):
    """The harness loader, with the identity pins RE-POINTED to this matrix's own meta.

    NOT a weakening: load_matrix's asserts run verbatim; only the constants they compare against
    move, and the move is printed old -> new.  EXPECT_N is RE-MEASURED from the matrix (never
    assumed) and then asserted, exactly as the re-pinned harness header requires."""
    meta = json.load(open(path))['meta']
    old = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    H.EXPECT_STORE = meta['store_md5']
    H.EXPECT_V0SURF = meta['v0surf_sig'][:12]
    # re-measure the population with the loader's OWN predicate, then pin it
    M = json.load(open(path))
    n = len([r for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
             and 1 <= r['pick'] <= H.ND_LAST and H.YR_LO <= r['year'] <= H.CLASS_CUT])
    H.EXPECT_N = n
    new = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    m, ND = H.load_matrix(path)
    return m, ND, old, new


def derive(path):
    meta, ND, old, new = load_repinned(path)
    rows, prov = H.structural_values(ND)
    raw, effn = H.kernel_raw(rows, PICKS)
    ic, forced = H.pin_and_check(raw, effn)
    return {'meta': meta, 'n': len(ND), 'prov': prov, 'raw': raw, 'effn': effn,
            'ladder': ic, 'forced': forced, 'pins_old': old, 'pins_new': new,
            'payload': H.payload(ic), 'total': int(sum(ic)),
            'mean_structural': float(np.mean([r['value'] for r in rows]))}


OUT = {}
for name, path in MATRICES:
    print('=' * 100)
    print('MATRIX %s  %s' % (name, os.path.relpath(path, REPO)))
    r = derive(path)
    print('  pins re-pointed: store %s -> %s | v0surf %s -> %s | EXPECT_N %s -> %s'
          % (r['pins_old'][0], r['pins_new'][0], r['pins_old'][1], r['pins_new'][1],
             r['pins_old'][2], r['pins_new'][2]))
    print('  meta: store %s engine %s v0surf %s  n_recs %s'
          % (r['meta']['store_md5'], r['meta'].get('engine_head'), r['meta']['v0surf_sig'][:12],
             r['meta'].get('n_records')))
    print('  ND=%d  provenance=%s' % (r['n'], json.dumps(r['prov'])))
    print('  mean structural value %.4f' % r['mean_structural'])
    print('  raw head %.4f  raw[64] %.4f  raw monotone violations %d'
          % (r['raw'][0], r['raw'][63], H.raw_monotone_violations(r['raw'])))
    print('  ladder payload %s total %d  forced-descent picks %s'
          % (r['payload'], r['total'], r['forced']))
    print('  ladder[1,2,3,10,20,40,64] = %s' % [r['ladder'][k - 1] for k in (1, 2, 3, 10, 20, 40, 64)])
    OUT[name] = r

SHIPPED = json.load(open(os.path.join(EV,
    'act_334B_2026-08-07/stage2_erafree/pvc_curve_v2_PRE_stage2ef.json')))
SH = [int(SHIPPED['curve'][str(k)]) for k in PICKS]
print('=' * 100)
print('SHIPPED BASE (pvc_curve_v2_PRE_stage2ef.json) payload %s total %d'
      % (H.payload(SH), sum(SH)))

OUT['_shipped'] = {'ladder': SH, 'payload': H.payload(SH), 'total': int(sum(SH))}
json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'meta'} for k, v in OUT.items()},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base_reteach.json'), 'w'),
          indent=1, sort_keys=True, default=str)

# ---------------- the attribution table ----------------
D = OUT['D_338_336layer_free']['ladder']
A = OUT['A_328_shipped_basis']['ladder']
B = OUT['B_338_tenure']['ladder']
C = OUT['C_338_336layer_era']['ladder']
print()
print('PER-PICK BASE DELTA AND ATTRIBUTION — no buckets, all 64 rows')
print('%4s %7s %7s %8s %8s | %8s %8s %8s %8s' % ('pick', 'shipped', 'base_ef', 'delta', 'pct',
                                                 'recipe', 'tenure', 'lay336', 'era'))
for i, p in enumerate(PICKS):
    d = D[i] - SH[i]
    print('%4d %7d %7d %8d %7.3f%% | %8d %8d %8d %8d'
          % (p, SH[i], D[i], d, 100.0 * d / SH[i], A[i] - SH[i], B[i] - A[i], C[i] - B[i], D[i] - C[i]))
dl = [D[i] - SH[i] for i in range(64)]
print()
print('SUMMARY  mean delta %.4f  mean |delta| %.4f  max |delta| %d at pick %d  total %d -> %d (%.6f)'
      % (float(np.mean(dl)), float(np.mean(np.abs(dl))), int(max(abs(x) for x in dl)),
         PICKS[int(np.argmax(np.abs(dl)))], sum(SH), sum(D), sum(D) / sum(SH)))
for lbl, a, b in (('recipe (derive_271 -> harness on the SAME 328 matrix)', SH, A),
                  ('#338 tenure + gate store', A, B),
                  ('#336 reference layer', B, C),
                  ('ERA REMOVAL', C, D)):
    dd = [b[i] - a[i] for i in range(64)]
    print('  %-52s mean %+8.3f  mean|.| %7.3f  max|.| %4d  total %+6d'
          % (lbl, float(np.mean(dd)), float(np.mean(np.abs(dd))), int(max(abs(x) for x in dd)), sum(dd)))
