"""THE EXACT MONOTONE CONSTRUCTION — rebake week ARM 2, the design arm. ONE home, four fit sites.

WHAT THIS IS
  Ruled at register v831 D1, owner word verbatim: "Exact it is." The construction of record is
  docs/proposals/rebake_study_B/DESIGN_STUDY_B.md section 2.3 (the estimator), 2.6 (the age hill) and
  3.3 / M-60 (the window-anchored recency weight). Prereg:
  docs/evidence/rebake_arm2_design_2026-08-24/PREREG.md, committed BEFORE this file existed (P9).

  It exists so the construction lives in ONE place. Study B section 4.1 records that the incumbent's
  hyperparameter block is duplicated VERBATIM across four files (conditional_prior.py, refit_q97m.py,
  _gate1_wf.py, _gate1_picksplit.py) — "a copy-paste lineage, not a comparison that was made and won" —
  and that a rebake "needs the hyperparameters changed in all four places at once". Four copies is how a
  gate ends up certifying a construction that is not the one under test. All four now import from here.

WHY THE SUBCLASS EXISTS (the mechanism, read out of the pinned sklearn source — study B M-26)
  sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:

      if not self._loss.differentiable:
          _update_leaves_values(loss=self._loss, grower=grower, ...)

  and sklearn/_loss/loss.py: PinballLoss.differentiable = False. So under quantile loss, AFTER the grower
  has enforced the monotone bounds, every leaf value is OVERWRITTEN with the empirical quantile of that
  leaf's residuals — a line search that does not respect the bounds it is overwriting. That is why
  `monotonic_cst` is NOT exact under quantile loss: study B measured 96.5% of rows still carrying a
  down-step, worst step -3.56% of the band (M-24). Under squared_error the overwrite never happens and
  the constraint is exact (M-25).

  Setting differentiable=True on the loss keeps the constrained leaf values. The property that follows is
  STRUCTURAL, not statistical: the band is non-decreasing in demonstrated level BECAUSE EVERY TREE IN
  EVERY FOREST IS, not because a sweep happened to find no counterexample.

THE RISK, STATED PLAINLY (study B I-6, and the reason FB4 below is a HALT and not a comment)
  sklearn._loss is a PRIVATE module. This construction depends on an internal contract
  (loss.differentiable gating _update_leaves_values) that sklearn is free to change without notice. It is
  safe today only because requirements-lock.txt pins scikit-learn==1.8.0 by hash and the environment is
  asserted at boot. The mitigation is selftest_or_halt() below: it fits a toy where the STOCK loss
  demonstrably violates and the subclass demonstrably does not, and HALTs the bake if either half of that
  contract has moved. Without that self-test this construction would not be defensible.

WHAT A CALLER GETS, AND WHAT IT MUST NOT DO
  Callers ask for design_spec() and quantile_family(). Nobody re-types a hyperparameter, a constraint
  vector or a feature index anywhere else. The spec RIDES WITH THE FITTED ARTIFACT (attached as
  _rl_design_spec, so it pickles with the model), which is why this arm needed no new model-semantics
  environment switch: the construction is a property of the artifact, not of the environment, and it is
  already covered by the pickle md5 that data/expected_boot.json pins and Guard 5 asserts.
"""
import os

import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn._loss.loss import PinballLoss

CONSTRUCTION = 'rebake-arm2-exact-monotone/1'

# The five band quantiles are conditional_prior.Q's own list; q97m is the sixth leg at 0.97. Kept as a
# module constant only so the self-test and the factories agree — the fit sites still read cp.Q.
LVL = 9                       # the level feature index, UNMOVED by the age reparameterisation
AGE = 10                      # the raw age index in the INCUMBENT 11-feature layout


class GradOnlyPinball(PinballLoss):
    """Pinball loss with the post-hoc leaf line search DISABLED — study B section 2.3, verbatim.

    Two attributes, and each one is load-bearing:
      differentiable = True             gradient_boosting.py's `if not self._loss.differentiable:` gate
                                        stops firing, so _update_leaves_values is never called and the
                                        grower's monotone bounds survive into the fitted leaves.
      need_update_leaves_values = False the same statement of the same fact on the attribute sklearn's
                                        own loss classes carry, so a reader of either attribute agrees.

    COST, MEASURED AND NOT WAVED THROUGH (study B M-29 / I-7): removing the line search makes every
    boosting step small and bounded (|gradient| <= 1, hessian == 1), so the learning rate and iteration
    count that reproduce the incumbent's FIT are not the ones that reproduce its GENERALISATION. The
    hyperparameters are therefore re-selected OUT OF SAMPLE at every bake, on a grid declared in the
    prereg before the run. They are NOT carried in this file as literals, on purpose.
    """
    differentiable = True
    need_update_leaves_values = False


# --------------------------------------------------------------------------- FB4, the HALTing self-test
_SELFTEST_DONE = []


def selftest(strict=True):
    """FB4 — THE PRIVATE-CONTRACT TRIPWIRE. Returns a dict of measurements; raises on a broken contract.

    Four legs, and the third and fourth are the ones that matter — the first two would pass on a library
    that had renamed the mechanism out from under us while keeping the attribute names.

      (1) the STOCK contract is what we think it is        PinballLoss.differentiable is False
      (2) the SUBCLASS overrides it                        GradOnlyPinball.differentiable is True
      (3) NON-VACUITY: the stock construction VIOLATES     a toy fit with loss='quantile' +
          monotonic_cst produces at least one strictly negative step on the constrained feature
      (4) EXACTNESS: the subclass does NOT violate         the same toy, same seed, same settings, with
          GradOnlyPinball produces ZERO negative steps

    Leg (3) is why this is a guard and not a wish. A self-test that only asserts the good case passes
    just as happily on a library where monotonic_cst became exact by itself AND on one where the whole
    mechanism was replaced — it cannot tell the two apart, and it cannot fail. This one can: if sklearn
    ever makes the stock path exact, leg (3) fires and the bake HALTs asking to be re-read, which is the
    correct outcome for a construction whose entire justification is a private internal.

    THE TOY IS DESIGNED TO VIOLATE, AND THAT TOOK MEASUREMENT RATHER THAN GUESSWORK. Study B M-25 is
    explicit that a SINGLE-DRIVER toy does NOT violate: "quantile + monotonic_cst gives 0 violations when
    the constrained feature is the only driver". This seat's first toy was exactly that shape and leg (3)
    fired on it — correctly. What the leaf line search needs in order to do visible damage is what the
    real design has: MANY features, so the constrained one is a minority of each leaf's story;
    HETEROSCEDASTIC, SKEWED residuals, so the empirical leaf quantile differs materially from the bounded
    gradient step; and an INTERACTION, so leaves are not separable in the constrained axis. Ten features,
    exponential noise scaled by another feature, and one product term reproduce it stably at all three
    quantiles. The sweep is taken over MANY rows, not one, for the same reason V3 is a population census
    and not three archetypes.
    """
    rng = np.random.default_rng(0)
    n, nf = 6000, 10
    X = rng.normal(0.0, 1.0, (n, nf))
    X[:, 0] = rng.uniform(0.0, 10.0, n)                       # the constrained driver
    y = (0.4 * X[:, 0] + 3.0 * X[:, 1] - 2.5 * X[:, 2] + 1.5 * X[:, 3] * X[:, 1]
         + rng.standard_exponential(n) * (1.0 + 0.8 * np.abs(X[:, 1])) * 3.0)
    cst = [0] * nf
    cst[0] = 1
    grid = np.linspace(0.0, 10.0, 201)
    rows = X[rng.choice(n, 40, replace=False)]

    def steps(model):
        neg, worst = 0, 0.0
        for r in rows:
            F = np.repeat(r[None, :], grid.size, axis=0)
            F[:, 0] = grid
            d = np.diff(np.asarray(model.predict(F), dtype=float))
            neg += int((d < -1e-12).sum())
            worst = min(worst, float(d.min()) if d.size else 0.0)
        return neg, worst

    kw = dict(max_iter=200, max_depth=4, learning_rate=0.2, min_samples_leaf=20,
              monotonic_cst=cst, early_stopping=False, random_state=0)
    s_neg = e_neg = 0
    s_worst = e_worst = 0.0
    per_q = {}
    for q in (0.10, 0.50, 0.90):
        stock = HistGradientBoostingRegressor(loss='quantile', quantile=q, **kw).fit(X, y)
        exact = HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), **kw).fit(X, y)
        sn, sw = steps(stock)
        en, ew = steps(exact)
        per_q['q%.2f' % q] = {'stock_negative': sn, 'stock_worst': sw,
                              'exact_negative': en, 'exact_worst': ew}
        s_neg += sn; e_neg += en
        s_worst = min(s_worst, sw); e_worst = min(e_worst, ew)

    res = {
        'construction': CONSTRUCTION,
        'sklearn': __import__('sklearn').__version__,
        'stock_PinballLoss_differentiable': bool(PinballLoss.differentiable),
        'subclass_differentiable': bool(GradOnlyPinball.differentiable),
        'subclass_need_update_leaves_values': bool(GradOnlyPinball.need_update_leaves_values),
        'toy_rows': n, 'toy_features': nf, 'toy_sweep_rows': int(len(rows)),
        'toy_sweep_points_per_row': int(grid.size), 'per_quantile': per_q,
        'STOCK_negative_steps': s_neg, 'STOCK_worst_step': s_worst,
        'EXACT_negative_steps': e_neg, 'EXACT_worst_step': e_worst,
    }
    fail = []
    if PinballLoss.differentiable is not False:
        fail.append("sklearn's PinballLoss.differentiable is %r, not False — the gate this construction "
                    "defeats no longer reads the way study B M-26 read it out of the source"
                    % PinballLoss.differentiable)
    if GradOnlyPinball.differentiable is not True:
        fail.append('GradOnlyPinball.differentiable is not True — the subclass is not overriding')
    if s_neg <= 0:
        fail.append("NON-VACUITY LEG FAILED: the STOCK loss='quantile' + monotonic_cst toy produced %d "
                    "negative steps. It is supposed to VIOLATE (study B M-24/M-25 measured 97/100 rows "
                    "violating on the real design). Either sklearn changed the leaf line search, or this "
                    "toy no longer exercises it. A self-test that cannot fail is not a self-test — "
                    "re-read the mechanism before trusting the exact arm." % s_neg)
    if e_neg != 0:
        fail.append('EXACTNESS LEG FAILED: the subclass produced %d negative steps (worst %.9f). The '
                    'private contract has MOVED — sklearn is no longer gating _update_leaves_values on '
                    'loss.differentiable, or is enforcing the constraint elsewhere. This is prereg '
                    'falsifier FB4.' % (e_neg, e_worst))
    res['verdict'] = 'PASS' if not fail else 'FAIL'
    res['failures'] = fail
    if fail and strict:
        raise SystemExit(
            '\n============ FB4 HALT — THE sklearn._loss PRIVATE CONTRACT HAS MOVED ============\n'
            '  The exact-monotone construction (study B section 2.3) subclasses the PRIVATE module\n'
            '  sklearn._loss. Its correctness depends on an internal contract that sklearn is free to\n'
            '  change. requirements-lock.txt pins scikit-learn==1.8.0 by hash; the running library is\n'
            '  %s. The self-test says:\n\n    - %s\n\n'
            '  THE BAKE IS HALTED BEFORE ANY FIT. Nothing has been written. Do not "work around" this:\n'
            '  the whole case for the exact arm (register v831 D1, "Exact it is.") rests on this\n'
            '  contract holding, and a rebake that ships past a red tripwire ships a board that may\n'
            '  violate law 3 on most rows, invisibly (study B I-5).\n'
            '=================================================================================='
            % (res['sklearn'], '\n    - '.join(fail)))
    return res


def selftest_or_halt():
    """Run FB4 once per process, before any production fit. Memoised so four fit sites cost one toy."""
    if not _SELFTEST_DONE:
        _SELFTEST_DONE.append(selftest(strict=True))
    return _SELFTEST_DONE[0]


# --------------------------------------------------------------------------- the age hill (study B 2.6)
def age_hill(age, a_star):
    """u = max(0, a* - age)  (years short of peak) and v = max(0, age - a*)  (years past peak).

    Both carry monotonic_cst = -1, so "value falls the further you are from the peak, in EITHER
    direction" is true BY CONSTRUCTION. That contains law 6 (AGE FADES, direction-only) as its right
    half and does NOT forbid the measured rise on its left half — which matters, because study B M-33
    measured only 0.67% of tenure<=3 rows monotone non-increasing in age. Forcing a signed -1 on raw age
    would make it structurally impossible for a 19-year-old to be worth more at 21 on identical evidence,
    on exactly the population the board is most sensitive about (I-9).

    a* IS A CHOSEN CONSTANT AND THE ESTATE KNOWS IT (I-24: "a* has no boundary solution. It is a number
    someone picks."). v831 D2 rules that it is NOT hand-fixed: it is SELECTED OUT OF SAMPLE at the bake,
    over a grid declared before the run that includes 21/22/23/24, with the owner's prior (~23) and the
    study's fitted response peak (~21.5) both reported. Hence a_star is an ARGUMENT here and a literal
    nowhere.
    """
    a = np.asarray(age, dtype=float)
    return np.maximum(0.0, a_star - a), np.maximum(0.0, a - a_star)


def apply_age_hill(X, a_star, age_index=AGE):
    """Incumbent 11-feature design -> 12-feature design: raw age REMOVED, u and v APPENDED.

    Layout after:  oh[0..5] + [log(effpk), exposure, tenure, LEVEL(9), u(10), v(11)]
    The level index is UNMOVED at 9 — deliberately, so the level constraint, the census sweep, ORDER 44's
    _O44_LVL and every downstream reader keep the same index across the reparameterisation.
    """
    X = np.asarray(X, dtype=float)
    u, v = age_hill(X[:, age_index], a_star)
    keep = [i for i in range(X.shape[1]) if i != age_index]
    return np.column_stack([X[:, keep], u, v])


def feature_row(base11, a_star):
    """The same transform for ONE row given as a plain list — the engine's per-row feature path.

    Kept beside apply_age_hill on purpose: a row builder and a matrix builder that drift apart is the
    exact class of defect ORDER 44's _o44_rows6 was factored to prevent ("the sample set and the row's
    own point are built by ONE expression and cannot drift apart").
    """
    age = float(base11[AGE])
    return list(base11[:AGE]) + list(base11[AGE + 1:]) + [max(0.0, a_star - age), max(0.0, age - a_star)]


# --------------------------------------------------------------- the window-anchored recency weight
def recency_weight(year, halflife, anchor):
    """w(Y) = 0.5 ** ((anchor - Y) / halflife), ANCHORED TO THE END OF THE TRAINING WINDOW.

    THE ANCHOR IS THE WHOLE FINDING (study B M-60). M-55 decayed from a GLOBAL anchor (YEAR.max() = 2026)
    and concluded every weight was worse than flat. On the T=2014 walk-forward split that leaves every
    training row far down the curve and the early cohorts nearly weightless — it was measuring the
    distance to TODAY rather than the distance to the end of its own training window, which is what a
    rebake actually uses. Re-anchored, a 16-year half-life went from 3.9404 to 3.9143, the best of
    everything the study measured, and a 6-year half-life went from 6% worse than flat to a wash.
    A MIS-SPECIFIED WEIGHT IS WORSE THAN NO WEIGHT AT ALL.

    STATED AT THE SIZE OF THE EFFECT (I-25): this is worth about a fifth of one per cent. It is a
    declared dial, never a derived constant, and it must not be presented as a significant improvement.
    The load-bearing half of study B section 3.3 is the DELETION result (deleting the pre-2014 half costs
    2.1%; deletion never helps at any setting tried), not the weighting result.

    halflife None => uniform (returns None, which is sklearn's own "no sample_weight").
    """
    if halflife is None:
        return None
    y = np.asarray(year, dtype=float)
    return 0.5 ** ((float(anchor) - y) / float(halflife))


# --------------------------------------------------------------------------- the estimator factories
def constraint_vector(n_features, age_hill_present):
    """+1 on level; -1 on u and v when the age hill is present; 0 everywhere else. Never hand-typed."""
    cst = [0] * n_features
    cst[LVL] = 1
    if age_hill_present:
        cst[n_features - 2] = -1
        cst[n_features - 1] = -1
    return cst


def make_estimator(quantile, n_features, age_hill_present, hp):
    """ONE estimator constructor. hp carries learning_rate / max_iter / max_depth / min_samples_leaf.

    early_stopping=False is not a tuning choice: with early stopping on, sklearn carves an internal
    validation split out of the training rows, which would make the fit depend on a random split the
    walk-forward selection never saw and would silently break bit-reproducibility of the artifact.
    """
    return HistGradientBoostingRegressor(
        loss=GradOnlyPinball(quantile=float(quantile)),
        max_iter=int(hp['max_iter']), max_depth=int(hp['max_depth']),
        learning_rate=float(hp['learning_rate']), min_samples_leaf=int(hp['min_samples_leaf']),
        monotonic_cst=constraint_vector(n_features, age_hill_present),
        early_stopping=False, random_state=0)


def design_spec(a_star, hp, halflife, n_features, quantiles, note=''):
    """THE CONTRACT THAT RIDES WITH THE ARTIFACT.

    Attached to every fitted estimator as _rl_design_spec, so it pickles with the model. The engine reads
    it at ONE site (wire_redesign.build(), already the one site that loads the band) and binds the
    feature contract from it. This is why ARM 2 adds no new model-semantics environment switch: the
    feature DIMENSION and the estimator CLASS are properties of the artifact, and an environment variable
    that disagreed with the loaded pickle would be a silent dimension mismatch. It is also strictly
    better guarded than a switch would be — the spec is inside the pickle whose md5 expected_boot.json
    already pins and Guard 5 already asserts on entry.
    """
    return {
        'construction': CONSTRUCTION,
        'exact_monotone_level': True,
        'level_index': LVL,
        'n_features': int(n_features),
        'age_hill': {'a_star': float(a_star), 'u_index': int(n_features - 2),
                     'v_index': int(n_features - 1)} if a_star is not None else None,
        'monotonic_cst': constraint_vector(n_features, a_star is not None),
        'hyperparameters': {k: hp[k] for k in sorted(hp)},
        'recency_halflife_years': halflife,
        'recency_anchor': 'end of training window',
        'quantiles': [float(q) for q in quantiles],
        'ratchet': 'RL_O44_LVLMONO RETIRED — law 3 is a property of this fit, not of a read-site repair',
        'note': note,
    }


def stamp(model, spec):
    """Attach the spec to a fitted estimator (it pickles with the model). Returns the model."""
    model._rl_design_spec = dict(spec)
    return model


def spec_of(obj):
    """Read the spec off a fitted estimator, or off a {quantile: estimator} band dict. None => incumbent."""
    if isinstance(obj, dict):
        for k in sorted(obj):
            return spec_of(obj[k])
        return None
    return getattr(obj, '_rl_design_spec', None)


def specs_agree(a, b):
    """Coherence: two artifacts must declare the SAME feature contract, or both declare none.

    Compared on the FEATURE CONTRACT only (construction, feature count, level index, a*), not on the
    hyperparameters — the band and the ceiling legitimately select different settings out of sample, but
    they must build the same feature vector or the engine is pricing one model's rows through another
    model's columns. That is the mixed-board class register v834's F7 exposed, made impossible here
    rather than merely visible.
    """
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    def key(s):
        return (s.get('construction'), s.get('n_features'), s.get('level_index'),
                (s.get('age_hill') or {}).get('a_star'))
    return key(a) == key(b)
