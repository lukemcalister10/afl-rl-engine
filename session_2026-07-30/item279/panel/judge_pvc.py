"""#279 FOUR-FITTER PVC PANEL — the JUDGE. Phase 1 (built and proven before any fitter runs).

Scores held-out prediction error by pick range, on identical folds. It reads only fitter result files
written to the frozen schema, and it refuses to score a set whose fold fingerprints disagree — that is the
guard against a fitter having quietly re-cut the folds.

CAN-FAIL PROOF (run with --selftest): three synthetic fitters are scored.
  perfect   : predicted == actual        -> error must be exactly 0
  constant  : predicted == global mean   -> error must be materially worse than perfect
  inverted  : predicted == max-actual    -> error must be worse again
If the judge cannot separate these three, it is not measuring anything and must not be trusted.
"""
import os, sys, json, math, collections
import numpy as np

RANGES = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]


def _stats(errs):
    if not errs:
        return {'n': 0}
    e = np.array(errs, float)
    return {'n': len(errs),
            'median_abs_error': round(float(np.median(np.abs(e))), 2),
            'mean_abs_error': round(float(np.mean(np.abs(e))), 2),
            'median_signed_error': round(float(np.median(e)), 2),
            'rmse': round(float(np.sqrt(np.mean(e ** 2))), 2),
            'p90_abs_error': round(float(np.percentile(np.abs(e), 90)), 2)}


def score(preds):
    """preds: [{'pick','actual','predicted',...}] -> overall + per-range error stats."""
    by = collections.defaultdict(list)
    allerr = []
    for p in preds:
        e = p['predicted'] - p['actual']
        allerr.append(e)
        for lo, hi in RANGES:
            if lo <= p['pick'] <= hi:
                by['%d-%d' % (lo, hi)].append(e); break
    out = {'overall': _stats(allerr),
           'by_pick_range': {k: _stats(v) for k, v in sorted(by.items(),
                             key=lambda kv: int(kv[0].split('-')[0]))}}
    # relative error, only over rows with a positive actual (denominator named)
    rel = [(p['predicted'] - p['actual']) / p['actual'] for p in preds if p['actual'] > 0]
    out['relative'] = {'n_with_positive_actual': len(rel), 'n_total': len(preds),
                       'median_abs_relative_pct': round(100 * float(np.median(np.abs(rel))), 2) if rel else None,
                       'median_signed_relative_pct': round(100 * float(np.median(rel)), 2) if rel else None}
    return out


def selftest():
    rng = np.random.RandomState(7)
    n = 600
    picks = rng.randint(1, 65, n)
    actual = np.maximum(0.0, 3000.0 / np.sqrt(picks) * (1.0 + 0.4 * rng.randn(n)))
    mk = lambda pred: [{'key': 'k%d' % i, 'pick': int(picks[i]), 'fold': i % 5,
                        'actual': float(actual[i]), 'predicted': float(pred[i])} for i in range(n)]
    perfect = score(mk(actual))
    constant = score(mk(np.full(n, actual.mean())))
    inverted = score(mk(np.full(n, actual.max())))
    ok_perfect = perfect['overall']['median_abs_error'] == 0.0 and perfect['overall']['rmse'] == 0.0
    ok_order = (perfect['overall']['rmse'] < constant['overall']['rmse'] < inverted['overall']['rmse'])
    ok_range = all(perfect['by_pick_range'][k]['median_abs_error'] == 0.0
                   for k in perfect['by_pick_range'])
    res = {'perfect_is_zero': bool(ok_perfect), 'per_range_perfect_is_zero': bool(ok_range),
           'ordering_perfect_lt_constant_lt_inverted': bool(ok_order),
           'rmse': {'perfect': perfect['overall']['rmse'], 'constant': constant['overall']['rmse'],
                    'inverted': inverted['overall']['rmse']},
           'JUDGE_CAN_FAIL': bool(ok_perfect and ok_order and ok_range)}
    return res


def main(argv):
    if '--selftest' in argv:
        r = selftest()
        print(json.dumps(r, indent=1))
        assert r['JUDGE_CAN_FAIL'], "JUDGE IS VACUOUS — refusing to certify it"
        print("JUDGE CAN FAIL: PROVEN")
        return 0
    indir, outpath = argv[1], argv[2]
    files = sorted(f for f in os.listdir(indir) if f.startswith('fitter_') and f.endswith('.json'))
    assert files, "no fitter results found in %s" % indir
    loaded = {}
    fps = set()
    for f in files:
        d = json.load(open(os.path.join(indir, f)))
        assert d['schema'] == 'pvc-panel-1', "%s: wrong schema %s" % (f, d.get('schema'))
        assert d['alpha'] == 1.0, "%s: alpha must be 1.0 for this panel, got %s" % (f, d['alpha'])
        fps.add(d['folds']['fingerprint'])
        loaded[d['fitter']] = d
    assert len(fps) == 1, "FOLD FINGERPRINTS DISAGREE %s — refusing to score across different folds" % fps
    # every fitter must have predicted the SAME held-out rows
    keysets = {n: {p['key'] for p in d['fold_predictions']} for n, d in loaded.items()}
    common = set.intersection(*keysets.values())
    for n, ks in keysets.items():
        assert ks == common, "%s predicted a different held-out set (%d vs %d common)" % (n, len(ks), len(common))
    out = {'fold_fingerprint': fps.pop(), 'n_fitters': len(loaded),
           'n_held_out_rows': len(common), 'judge_selftest': selftest(), 'fitters': {}}
    for n, d in loaded.items():
        out['fitters'][n] = {'description': d['description'], 'ladder_payload': d['ladder_payload'],
                             'ladder_total': d['ladder_total'],
                             'diagnostics': d['diagnostics'], 'provenance': d.get('provenance'),
                             'can_fail_proof': d.get('can_fail_proof'),
                             'score': score(d['fold_predictions'])}
    json.dump(out, open(outpath, 'w'), indent=1, sort_keys=True)
    open(outpath, 'a').write("\n")
    print("scored %d fitters on %d identical held-out rows -> %s" % (len(loaded), len(common), outpath))
    for n in sorted(out['fitters']):
        s = out['fitters'][n]['score']['overall']
        print("  %-28s medAE %8.2f  RMSE %8.2f  ladder %d"
              % (n, s['median_abs_error'], s['rmse'], out['fitters'][n]['ladder_total']))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
