#!/usr/bin/env python3
"""WORD B — FIT THE PEAK MODEL BOTH WAYS AND SHOW THE OWNER. Neither version is adopted here.

OWNER WORD B, verbatim: "Fit both and show me on word B, please."

  FIT (1) STATIC      bust_prior = B(pos, effpk), read from the v838 MODERNIZED table (owner word A).
                      This is the arm's peak model as word A leaves it.
  FIT (2) CONDITIONED bust_prior = mu(pos, effpk, tenure, games, cameo_avg), the seam-lever CAND-B
                      surface (scripts/wordb_cameo_prior.py), applied at TRAINING and at INFERENCE.

  B is the SAME modernized table in both, so the ONLY difference is the conditioning. Fit (2) NESTS
  fit (1): zero evidence gives A = 0 gives mu == B exactly.

WHAT IS MEASURED
  * both pickles' md5s, and the training-row census by conditioning regime
  * DAY-0 BYTE-EXACTNESS between the two fits — asserted, not assumed. The draft row carries no
    evidence, so A == 0 identically and the two models must see an IDENTICAL draft feature row.
    (The two MODELS still differ, because their non-draft training rows differ — so the assertion is
    on the FEATURE, which is what the construction actually claims, and the day-0 PRICE is then
    checked on the built boards.)
  * out-of-sample score under BOTH protocols, study-A whole-career PRIMARY
  * the conditioned feature's importance against the static one (permutation importance on held-out
    rows, so it is a statement about the fitted model and not about the training fit)

READ-ONLY on the repository: it writes only into the scratch root/workspace it is pointed at.
"""
import argparse, contextlib, hashlib, importlib.util, io, json, os, pickle, sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wordb_cameo_prior as CP

# STUDY A'S PROTOCOL — WHOLE CAREERS HELD OUT — BUT ON THE PEAK MODEL'S OWN WINDOW.
# The band's folds (2013-15 / 2016-18 / 2019-21) DO NOT TRANSFER: build_peak_model_v4 trains on
# build(2006, 2015), so two of those three test sets are EMPTY and the third is the only fold that
# runs. This seat's first cut used them anyway, got a single fold, and then crashed the importance
# block on an empty held-out set — the crash is what exposed it. The folds below keep study A's
# PRINCIPLE (a test player has no training row at all) inside the window that actually has rows.
FOLDS_A = ((2009, 2010, 2011), (2011, 2012, 2013), (2013, 2014, 2015))
SPLITS_B = (2008, 2010, 2012)     # as-of year, inside the same window, for the leaky-protocol contrast
IMPORTANCE_FOLD = (2013, 2014, 2015)


def md5f(p):
    with open(p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def _L(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    with contextlib.redirect_stdout(io.StringIO()):
        s.loader.exec_module(m)
    return m


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--table', required=True, help="bustpt/tables.json (key 'modern')")
    ap.add_argument('--out', required=True)
    ap.add_argument('--json', required=True)
    a = ap.parse_args(argv[1:])
    os.makedirs(a.out, exist_ok=True)

    root = os.environ['RL_REPO']
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path.insert(0, root)
    import config_manifest
    config_manifest.enforce('gate')
    sys.path.insert(0, '.')
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA

    from sklearn.ensemble import HistGradientBoostingRegressor
    POSI = {'MID': 0, 'SD': 1, 'SF': 2, 'KPD': 3, 'KPF': 4, 'RUCK': 5}
    PT = CP.load_table(a.table, 'modern')
    PVC = MA.PVC

    def B_of(pos, pk):
        return PT[pos][str(min(max(int(round(pk)), 1), 70))]

    def best(ss, n):
        v = sorted([x['avg'] for x in ss if x['games'] >= 6], reverse=True)[:n]
        return float(np.mean(v)) if v else None

    def age_at(p, Y):
        by = p.get('_by')
        return (Y - by) if by else (Y - (MA.debut(p) - 18))

    allp = [p for p in MA.data if MA.GRP.get(p['pos'])]

    def feats(p, Y, conditioned):
        """build_peak_model_v4.feats VERBATIM except the final bust_prior element."""
        d = MA.debut(p); pos = MA.GRP[p['pos']]; ep = MA.effpk(p); T = Y - d + 1
        sub = [x for x in p['scoring'] if x['year'] <= Y]
        g = sum(x['games'] for x in sub)
        nss = len([x for x in sub if x['games'] >= 6])
        b2 = best(sub, 2); b1 = best(sub, 1)
        maxg = max([x['games'] for x in sub], default=0)
        rs = [x for x in sub if x['games'] >= 6][-2:]
        recent = float(np.average([x['avg'] for x in rs], weights=[x['games'] for x in rs])) if rs else 0
        last = [x for x in sub if x['year'] == Y]
        la = last[0]['avg'] if last else 0
        lg = last[0]['games'] if last else 0
        early = sum(x['games'] for x in sub if x['year'] - d + 1 <= 2)
        seq = [x['avg'] for x in sub if x['games'] >= 6]
        slope = (seq[-1] - seq[0]) if len(seq) > 1 else 0.0
        bestyr = max([x['year'] for x in sub if x['games'] >= 6 and x['avg'] == (b1 or -1)], default=Y)
        ysb = Y - bestyr
        Bv = B_of(pos, ep)
        if conditioned:
            bpv, A, Tc, c = CP.mu(Bv, T, [(x['games'], x['avg']) for x in sub])
        else:
            bpv, A, Tc, c = Bv, 0.0, None, None
        return ([np.log(PVC[ep]), ep, POSI[pos], b2 or 0, b1 or 0, recent, la, lg, g, nss, maxg,
                 early, slope, ysb, age_at(p, Y), T, bpv], A, T)

    def draft_feat(p, conditioned):
        pos = MA.GRP[p['pos']]; ep = MA.effpk(p)
        Bv = B_of(pos, ep)
        bpv = CP.mu(Bv, 1, [])[0] if conditioned else Bv     # NO seasons => A == 0 => mu == B
        return [np.log(PVC[ep]), ep, POSI[pos], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                age_at(p, MA.debut(p) - 1), 0, bpv]

    def build(lo, hi, conditioned):
        X, y, debut, asof, keys, regime = [], [], [], [], [], []
        for p in allp:
            d = MA.debut(p)
            if d < lo or d > hi:
                continue
            X.append(draft_feat(p, conditioned))
            y.append(best([x for x in p['scoring']], 3) or 0.0)
            debut.append(d); asof.append(d - 1); keys.append(p.get('key')); regime.append('draft')
            for Y in sorted({x['year'] for x in p['scoring'] if x['year'] >= d}):
                fut = [x for x in p['scoring'] if x['year'] >= Y and x['games'] >= 6]
                if not fut:
                    continue
                f, A, T = feats(p, Y, conditioned)
                X.append(f); y.append(best([x for x in p['scoring'] if x['year'] >= Y], 3) or 0.0)
                debut.append(d); asof.append(Y); keys.append(p.get('key'))
                regime.append('conditioned' if A > 0 else ('in_scope_no_evidence' if T <= CP.TMAX
                                                           else 'out_of_scope_static'))
        return (np.array(X, float), np.array(y, float), np.array(debut, int), np.array(asof, int),
                np.array(keys), np.array(regime))

    KW = dict(max_iter=600, max_depth=5, learning_rate=0.04, min_samples_leaf=30,
              l2_regularization=2.0, random_state=0)
    R = {'_doc': __doc__, 'construction': CP.spec(),
         'table_source': os.path.abspath(a.table), 'table_key': 'modern',
         'table_md5_as_written': None, 'peak_model_hyperparameters': KW}

    out = {}
    for tag, cond in (('static', False), ('conditioned', True)):
        X, y, debut, asof, keys, regime = build(2006, 2015, cond)
        m = HistGradientBoostingRegressor(**KW).fit(X, y)
        pkl = os.path.join(a.out, 'peak_model_v4.wordb_%s.pkl' % tag)
        with open(pkl, 'wb') as f:
            pickle.dump({'model': m, 'fnames': ['logPVC', 'effpk', 'pos', 'best2', 'best1',
                                                'recent_gw', 'last_avg', 'last_g', 'games', 'nss',
                                                'maxg', 'early', 'slope', 'yrs_since_best', 'age',
                                                'T', 'bust_prior']}, f)
        from collections import Counter
        out[tag] = {'pkl': pkl, 'md5': md5f(pkl), 'rows': int(X.shape[0]),
                    'regime_census': dict(Counter(regime.tolist())),
                    'bust_prior_feature_stats': {
                        'mean': float(X[:, 16].mean()), 'std': float(X[:, 16].std()),
                        'min': float(X[:, 16].min()), 'max': float(X[:, 16].max())}}
        out[tag]['_X'] = X; out[tag]['_y'] = y
        out[tag]['_debut'] = debut; out[tag]['_asof'] = asof; out[tag]['_m'] = m
        print('%-12s rows=%d  md5=%s  bust_prior mean %.3f sd %.3f  regimes %s'
              % (tag, X.shape[0], out[tag]['md5'], out[tag]['bust_prior_feature_stats']['mean'],
                 out[tag]['bust_prior_feature_stats']['std'], out[tag]['regime_census']), flush=True)

    # ---- DAY-0 BYTE-EXACTNESS OF THE FEATURE, ASSERTED ----------------------------------------
    ds = np.array([draft_feat(p, False) for p in allp], float)
    dc = np.array([draft_feat(p, True) for p in allp], float)
    same = bool(np.array_equal(ds, dc))
    R['day0_feature_byte_exact'] = {
        'draft_rows_compared': int(ds.shape[0]), 'identical': same,
        'max_abs_delta': float(np.abs(ds - dc).max()),
        'verdict': ('BYTE-EXACT — the draft row carries no evidence, so A == 0 and mu == B exactly'
                    if same else 'NOT EXACT — the construction claim has failed')}
    print('\nDAY-0 FEATURE: %s (max |delta| %.3e over %d draft rows)'
          % ('BYTE-EXACT' if same else '*** NOT EXACT ***', np.abs(ds - dc).max(), ds.shape[0]))
    if not same:
        raise SystemExit('wordb HALT: day-0 feature is not byte-exact between the two fits.')

    # ---- OUT OF SAMPLE, BOTH PROTOCOLS -------------------------------------------------------
    def score(tag, protocol):
        X, y = out[tag]['_X'], out[tag]['_y']
        debut, asof = out[tag]['_debut'], out[tag]['_asof']
        per = []
        folds = (FOLDS_A if protocol == 'studyA' else
                 [((asof <= T), (asof > T) & (asof <= T + 3)) for T in SPLITS_B])
        if protocol == 'studyA':
            folds = [((debut <= aa), (debut >= b) & (debut <= c)) for aa, b, c in FOLDS_A]
        for tr, te in folds:
            if te.sum() == 0 or tr.sum() == 0:
                continue
            mm = HistGradientBoostingRegressor(**KW).fit(X[tr], y[tr])
            pred = mm.predict(X[te])
            rmse = float(np.sqrt(np.mean((y[te] - pred) ** 2)))
            ss = float(1 - np.sum((y[te] - pred) ** 2) / np.sum((y[te] - y[te].mean()) ** 2))
            per.append({'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                        'rmse': round(rmse, 4), 'r2': round(ss, 4)})
        return {'folds': per, 'mean_rmse': round(float(np.mean([f['rmse'] for f in per])), 4),
                'mean_r2': round(float(np.mean([f['r2'] for f in per])), 4)}

    print('\n=== OUT OF SAMPLE — study A (whole careers held out) is PRIMARY ===')
    for protocol in ('studyA', 'studyB'):
        for tag in ('static', 'conditioned'):
            out[tag].setdefault('oos', {})[protocol] = score(tag, protocol)
            s = out[tag]['oos'][protocol]
            print('  %-10s %-8s  RMSE %.4f   R2 %.4f   %s'
                  % (protocol, tag, s['mean_rmse'], s['mean_r2'],
                     [f['rmse'] for f in s['folds']]), flush=True)

    # ---- PERMUTATION IMPORTANCE OF THE bust_prior FEATURE ON HELD-OUT ROWS --------------------
    print('\n=== bust_prior FEATURE IMPORTANCE (permutation, held-out, study A fold 3) ===')
    for tag in ('static', 'conditioned'):
        X, y = out[tag]['_X'], out[tag]['_y']
        debut = out[tag]['_debut']
        aa, b, c = IMPORTANCE_FOLD
        tr = debut <= aa
        te = (debut >= b) & (debut <= c)
        if te.sum() == 0 or tr.sum() == 0:
            raise SystemExit('wordb HALT: the importance fold is empty (train %d, test %d) — a '
                             'permutation importance on no rows is not a measurement.'
                             % (tr.sum(), te.sum()))
        mm = HistGradientBoostingRegressor(**KW).fit(X[tr], y[tr])
        base = float(np.sqrt(np.mean((y[te] - mm.predict(X[te])) ** 2)))
        rng = np.random.default_rng(0)
        deltas = []
        for _ in range(10):
            Xp = X[te].copy()
            rng.shuffle(Xp[:, 16])
            deltas.append(float(np.sqrt(np.mean((y[te] - mm.predict(Xp)) ** 2))) - base)
        out[tag]['bust_prior_permutation_importance'] = {
            'baseline_rmse': round(base, 4),
            'mean_rmse_increase_when_shuffled': round(float(np.mean(deltas)), 4),
            'sd': round(float(np.std(deltas)), 4)}
        print('  %-12s baseline RMSE %.4f  -> +%.4f when bust_prior is shuffled'
              % (tag, base, float(np.mean(deltas))))

    for tag in out:
        for k in ('_X', '_y', '_debut', '_asof', '_m'):
            out[tag].pop(k, None)
    R['fits'] = out
    R['oos_reading'] = (
        'study A (whole careers held out) is the PRIMARY protocol, per the arm\'s own FB2 finding: '
        'study B\'s as-of-year split shares 76-100%% of its test players with its training set, so it '
        'rewards a model that has already seen the player. Both are reported; only study A is a '
        'statement about a player the model has never seen.')
    json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    print('\nWROTE %s' % a.json)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
