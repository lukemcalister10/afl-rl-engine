"""#279 PVC PANEL — the RUNNER. Frozen; fitters must not modify this or harness_pvc.py.

Usage:
  python3 run_fitter.py <fitter_module.py> <matrix.json> <outdir>

The runner owns the folds, the schema and the writing. A fitter module supplies exactly:

  NAME        : str, short slug (becomes fitter_<NAME>.json)
  DESCRIPTION : str, one line, including any disclosed parameters (break point, bandwidth, ...)

  full_fit(rows) -> (raw, weights, diagnostics)
      rows : [{'key','pick','value','concluded','how'}]  — ALL rows, the ruled structural values
      raw  : list of 64 floats, the fitted year-0 value at picks 1..64
      weights : list of 64 floats, the isotonic pooling weights (effective n, counts, or ones)
      diagnostics : dict — anything the fitter wants recorded (bandwidths, break point, ...)

  fold_fit(train_rows, test_picks) -> list of floats, len == len(test_picks)
      trained ONLY on train_rows; predicts the year-0 value at each held-out row's pick

  can_fail_proof(rows) -> dict
      a demonstration that this fitter is not degenerate: it must show the fitter RESPONDS to a
      deliberate perturbation of its input and does NOT return a constant. Include the numbers.

alpha = 1 throughout. No CE aggregator anywhere in this panel.
"""
import os, sys, json, importlib.util, collections
import numpy as np
import harness_pvc as H


def load_module(path):
    spec = importlib.util.spec_from_file_location('fitter_mod', path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    for attr in ('NAME', 'DESCRIPTION', 'full_fit', 'fold_fit', 'can_fail_proof'):
        assert hasattr(m, attr), "fitter module missing required attribute: %s" % attr
    return m


def main(argv):
    fitter_path, matrix, outdir = argv[1], argv[2], argv[3]
    m = load_module(fitter_path)
    meta, ND = H.load_matrix(matrix)
    rows, prov = H.structural_values(ND)
    fa = H.folds(rows)
    assert set(fa) == {r['key'] for r in rows}, "fold assignment does not cover the population"

    # ---- held-out predictions on the frozen folds ----
    preds = []
    for f in range(H.K_FOLDS):
        train = [r for r in rows if fa[r['key']] != f]
        test = [r for r in rows if fa[r['key']] == f]
        assert train and test, "fold %d is degenerate" % f
        got = m.fold_fit(train, [r['pick'] for r in test])
        assert len(got) == len(test), "fold %d: fitter returned %d predictions for %d rows" % (f, len(got), len(test))
        for r, p in zip(test, got):
            assert p == p and abs(p) != float('inf'), "fold %d: non-finite prediction for %s" % (f, r['key'])
            preds.append({'key': r['key'], 'pick': r['pick'], 'fold': f,
                          'actual': round(float(r['value']), 4), 'predicted': round(float(p), 4)})

    # ---- the ladder, trained on everything ----
    raw, wts, diag = m.full_fit(rows)
    assert len(raw) == 64 and len(wts) == 64, "full_fit must return 64 raw and 64 weights"
    assert all(x == x for x in raw), "full_fit produced NaN"
    ladder, forced = H.pin_and_check(np.asarray(raw, float), np.asarray(wts, float))
    diag = dict(diag or {})
    diag['raw_monotone_violations'] = H.raw_monotone_violations(np.asarray(raw, float))
    diag['forced_by_descent_enforcement'] = forced
    diag['n_forced'] = len(forced)
    diag['raw_at'] = {str(k): round(float(raw[k - 1]), 2) for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)}
    diag['raw_pick1_pre_pin'] = round(float(raw[0]), 2)

    cf = m.can_fail_proof(rows)
    assert isinstance(cf, dict) and cf, "can_fail_proof must return a non-empty dict"

    p = H.save_result(outdir, m.NAME, m.DESCRIPTION, ladder, preds, diag, cf, prov, fa)
    print("WROTE %s" % p)
    print("  fitter        : %s" % m.NAME)
    print("  fold fp       : %s  (harness %s)" % (H.folds_fingerprint(fa), H.folds_fingerprint(fa)))
    print("  ladder payload: %s  total %d" % (H.payload(ladder), sum(ladder)))
    print("  ladder        : 1=%d 10=%d 24=%d 40=%d 64=%d"
          % (ladder[0], ladder[9], ladder[23], ladder[39], ladder[63]))
    print("  raw viol      : %d   forced: %d" % (diag['raw_monotone_violations'], diag['n_forced']))
    print("  held-out rows : %d" % len(preds))
    print("  can_fail      : %s" % json.dumps(cf)[:300])
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
