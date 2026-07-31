"""#279 PVC PANEL fitter: 'loclin' — LOCAL-LINEAR (degree-1 WLS) regression over log(pick),
everywhere in the domain. No kernel-mean segment anywhere; the only place a local mean appears is
the DISCLOSED, COUNTED ill-conditioning fallback described below.

Estimator, at each target pick p in 1..64:
    d_i = log(pick_i) - log(p)                       (design centred on the target)
    W_i = exp(-0.5 * (d_i / h_p)^2)                  (Gaussian weights)
    h_p = harness_pvc.bandwidth_at(rows, p)          (the PANEL'S OWN bandwidth policy, shared)
    solve  min_(a,b)  sum_i W_i (v_i - a - b d_i)^2  ;  fit(p) = a   (= value at d=0)

alpha = 1: plain weighted least squares. No certainty-equivalent / power-mean aggregator anywhere.

Ill-conditioning (the top of the draft has effective n ~ 35, so the 2x2 normal matrix can go
near-singular and the slope can go wild):
  * The 2x2 normal matrix A = X'WX is NORMALISED (weights by S0 = sum W, distances by h_p) so its
    condition number is dimensionless and comparable across picks.
  * A tiny ridge RIDGE_REL * S0 * h_p^2 is added to the SLOPE entry only (A[1,1]) — never to the
    intercept — so the regulariser can only pull the slope toward 0, i.e. toward the local mean, and
    can never shrink the fitted level.
  * If cond(A_normalised) > COND_MAX, or the ridged solve still fails / returns a non-finite value,
    the pick FALLS BACK to the local weighted mean sum(W v)/sum(W) and is COUNTED. The count and the
    thresholds are reported in diagnostics (full sample) and for the fold fits.
  * Fitted values are clamped at 0.0 (values are non-negative by construction); clampings counted.

Weights returned for the harness's isotonic pooling step are the local effective n, sum(W).
"""
import math
import numpy as np

import harness_pvc as H

NAME = 'loclin'
DESCRIPTION = ('local-linear (degree-1 WLS) on log(pick) with Gaussian weights at every pick 1..64, '
               'bandwidth from harness_pvc.bandwidth_at (nmin=35, h in [0.10,0.60] step 0.02); '
               'slope-only ridge RIDGE_REL=1e-06*S0*h^2, fallback to local weighted mean when '
               'cond(normalised X\'WX) > COND_MAX=1000000.0; isotonic weights = local effective n; '
               'alpha=1, plain WLS, no CE aggregator')

# ---- disclosed dials ----
RIDGE_REL = 1e-6        # ridge added to the SLOPE entry only, as RIDGE_REL * S0 * h^2
COND_MAX = 1.0e6        # condition-number threshold on the NORMALISED 2x2 normal matrix
NEG_CLAMP = 0.0         # fitted values clamped at this floor

# accumulator for the fold pass (the runner calls fold_fit before full_fit, so full_fit can report it)
_FOLD_STATS = {'fold_calls': 0, 'fold_point_fits': 0, 'fold_fallback_illcond': 0,
               'fold_clamped_negative': 0}


def _prep(rows):
    lp = np.array([math.log(r['pick']) for r in rows], float)
    v = np.array([max(float(r['value']), 0.0) for r in rows], float)
    return lp, v


def _loclin_at(lp, v, p, h, cond_max=COND_MAX):
    """One local-linear fit at pick p with bandwidth h.
    Returns (fit, effn, slope, cond_normalised, used_fallback, clamped)."""
    Lp = math.log(p)
    d = lp - Lp
    W = np.exp(-0.5 * (d / h) ** 2)

    S0 = float(np.sum(W))
    if not (S0 > 0.0) or not np.isfinite(S0):
        # no support at all: nothing to fit. Reported as a fallback with a zero level.
        return 0.0, 0.0, 0.0, float('inf'), True, False

    S1 = float(np.sum(W * d))
    S2 = float(np.sum(W * d * d))
    T0 = float(np.sum(W * v))
    T1 = float(np.sum(W * d * v))

    # normalised (dimensionless) normal matrix, for a comparable condition number
    An = np.array([[1.0, S1 / (S0 * h)],
                   [S1 / (S0 * h), S2 / (S0 * h * h)]], float)
    try:
        cond = float(np.linalg.cond(An))
    except Exception:
        cond = float('inf')

    local_mean = T0 / S0

    if (not np.isfinite(cond)) or cond > cond_max:
        fit = local_mean
        clamped = fit < NEG_CLAMP
        return (max(fit, NEG_CLAMP), S0, 0.0, cond, True, bool(clamped))

    lam = RIDGE_REL * S0 * h * h          # slope-only ridge, in the units of S2
    A = np.array([[S0, S1], [S1, S2 + lam]], float)
    b = np.array([T0, T1], float)
    try:
        coef = np.linalg.solve(A, b)
        a, slope = float(coef[0]), float(coef[1])
        if not (np.isfinite(a) and np.isfinite(slope)):
            raise np.linalg.LinAlgError('non-finite solution')
    except Exception:
        fit = local_mean
        clamped = fit < NEG_CLAMP
        return (max(fit, NEG_CLAMP), S0, 0.0, cond, True, bool(clamped))

    clamped = a < NEG_CLAMP
    return (max(a, NEG_CLAMP), S0, slope, cond, False, bool(clamped))


def _fit_picks(rows, picks, cond_max=COND_MAX):
    """Local-linear fit at each pick in `picks`, trained on `rows`. Returns (fits, effn, info)."""
    lp, v = _prep(rows)
    fits, effn, slopes, conds, bws = [], [], [], [], []
    fb_picks, clamp_picks = [], []
    hcache = {}
    for p in picks:
        pi = int(p)
        h = hcache.get(pi)
        if h is None:
            h = float(H.bandwidth_at(rows, pi))
            hcache[pi] = h
        f, n, s, c, fb, cl = _loclin_at(lp, v, pi, h, cond_max=cond_max)
        fits.append(f); effn.append(n); slopes.append(s)
        conds.append(c); bws.append(h)
        if fb:
            fb_picks.append(pi)
        if cl:
            clamp_picks.append(pi)
    info = {'bandwidths': bws, 'slopes': slopes, 'conds': conds,
            'fallback_picks': fb_picks, 'clamped_picks': clamp_picks}
    return fits, effn, info


# ============================== the three required entry points ==============================
def full_fit(rows):
    picks = list(range(1, 65))
    fits, effn, info = _fit_picks(rows, picks)

    finite_conds = [c for c in info['conds'] if np.isfinite(c)]
    diag = {
        'estimator': 'local-linear degree-1 weighted least squares on log(pick), Gaussian weights, '
                     'evaluated at the target pick (intercept of the centred design)',
        'alpha': 1.0,
        'aggregator': 'plain WLS (no certainty-equivalent, no power mean)',
        'bandwidth_source': 'harness_pvc.bandwidth_at (shared panel policy)',
        'bandwidth_policy': {'nmin': H.NMIN, 'hmin': H.HMIN, 'hmax': H.HMAX, 'step': 0.02},
        'bandwidth_at': {str(k): round(info['bandwidths'][k - 1], 4)
                         for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'bandwidth_min': round(min(info['bandwidths']), 4),
        'bandwidth_max': round(max(info['bandwidths']), 4),
        'bandwidth_all': [round(x, 4) for x in info['bandwidths']],

        # ---- the disclosed ill-conditioning handling ----
        'ridge_rel': RIDGE_REL,
        'ridge_applied_to': 'slope entry A[1,1] only, as RIDGE_REL * S0 * h^2 (never the intercept)',
        'cond_threshold': COND_MAX,
        'cond_matrix': "normalised X'WX (weights / S0, distances / h) — dimensionless",
        'n_fallback_local_mean': len(info['fallback_picks']),
        'fallback_picks': info['fallback_picks'],
        'fallback_rule': 'cond(normalised) > cond_threshold, or a non-finite ridged solve '
                         '-> local weighted mean sum(Wv)/sum(W) at that pick',
        'cond_max_observed': round(max(finite_conds), 3) if finite_conds else None,
        'cond_min_observed': round(min(finite_conds), 3) if finite_conds else None,
        'cond_at': {str(k): (round(info['conds'][k - 1], 3) if np.isfinite(info['conds'][k - 1]) else None)
                    for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'n_clamped_at_zero': len(info['clamped_picks']),
        'clamped_picks': info['clamped_picks'],

        # ---- fit shape ----
        'slope_at': {str(k): round(info['slopes'][k - 1], 3) for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'slope_min': round(min(info['slopes']), 3),
        'slope_max': round(max(info['slopes']), 3),
        'effn_at': {str(k): round(effn[k - 1], 3) for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'effn_min': round(min(effn), 3),
        'effn_max': round(max(effn), 3),
        'weights_are': 'local effective n = sum(W) at each pick (isotonic pooling weights)',
        'n_rows_trained': len(rows),

        # ---- what happened during the held-out fold pass (same procedure, train_rows only) ----
        'fold_pass': dict(_FOLD_STATS),
    }
    return [float(x) for x in fits], [float(x) for x in effn], diag


def fold_fit(train_rows, test_picks):
    """The SAME local-linear procedure, trained ONLY on train_rows, evaluated at each test pick.
    The bandwidth is also re-derived from train_rows, so nothing leaks from the held-out fold."""
    fits, effn, info = _fit_picks(train_rows, list(test_picks))
    _FOLD_STATS['fold_calls'] += 1
    _FOLD_STATS['fold_point_fits'] += len(fits)
    _FOLD_STATS['fold_fallback_illcond'] += len(info['fallback_picks'])
    _FOLD_STATS['fold_clamped_negative'] += len(info['clamped_picks'])
    return [float(x) for x in fits]


def can_fail_proof(rows):
    """Numbers showing this fitter is neither constant nor inert."""
    picks = list(range(1, 65))
    base, _, binfo = _fit_picks(rows, picks)
    base = np.asarray(base, float)

    # ---- (a) NOT CONSTANT across picks ----
    spread = float(base.max() - base.min())
    uniq = len(set(round(float(x), 6) for x in base))
    d1 = float(np.max(np.abs(np.diff(base))))

    # ---- (b1) responds to a global scaling of the input values: fit must scale by the same factor ----
    SC = 1.5
    scaled_rows = [dict(r, value=float(r['value']) * SC) for r in rows]
    scaled, _, _ = _fit_picks(scaled_rows, picks)
    scaled = np.asarray(scaled, float)
    ok = base > 1e-9
    ratios = scaled[ok] / base[ok]
    scale_ratio_med = float(np.median(ratios))
    scale_ratio_min = float(np.min(ratios))
    scale_ratio_max = float(np.max(ratios))

    # ---- (b2) responds LOCALLY: shift only the tail rows (pick >= 50) up by +400 ----
    SHIFT = 400.0
    tail_rows = [dict(r, value=float(r['value']) + (SHIFT if r['pick'] >= 50 else 0.0)) for r in rows]
    tail, _, _ = _fit_picks(tail_rows, picks)
    tail = np.asarray(tail, float)
    n_tail_rows = sum(1 for r in rows if r['pick'] >= 50)

    # ---- (b3) responds to a slope-only perturbation: tilt values in log(pick) ----
    # v_i -> v_i * (1 + 0.25 * (log(pick_i) - log(32))) : level at pick 32 ~unchanged, slope changes
    L32 = math.log(32)
    tilt_rows = [dict(r, value=max(0.0, float(r['value']) * (1.0 + 0.25 * (math.log(r['pick']) - L32))))
                 for r in rows]
    tilt, _, tinfo = _fit_picks(tilt_rows, picks)
    tilt = np.asarray(tilt, float)

    # ---- (c) the ill-conditioning fallback is live: force the threshold below every observed cond ----
    probe, _, pinfo = _fit_picks(rows, picks, cond_max=1.0)
    probe = np.asarray(probe, float)
    n_probe_fb = len(pinfo['fallback_picks'])

    return {
        'not_constant__spread_max_minus_min': round(spread, 4),
        'not_constant__n_distinct_of_64': uniq,
        'not_constant__max_abs_adjacent_step': round(d1, 4),
        'not_constant__raw_min': round(float(base.min()), 4),
        'not_constant__raw_max': round(float(base.max()), 4),
        'not_constant__raw_std': round(float(base.std()), 4),
        'not_constant__slope_min': round(min(binfo['slopes']), 4),
        'not_constant__slope_max': round(max(binfo['slopes']), 4),

        'perturb_scale_factor': SC,
        'perturb_scale__before_p1': round(float(base[0]), 4),
        'perturb_scale__after_p1': round(float(scaled[0]), 4),
        'perturb_scale__before_p10': round(float(base[9]), 4),
        'perturb_scale__after_p10': round(float(scaled[9]), 4),
        'perturb_scale__before_p32': round(float(base[31]), 4),
        'perturb_scale__after_p32': round(float(scaled[31]), 4),
        'perturb_scale__before_p64': round(float(base[63]), 4),
        'perturb_scale__after_p64': round(float(scaled[63]), 4),
        'perturb_scale__ratio_median': round(scale_ratio_med, 6),
        'perturb_scale__ratio_min': round(scale_ratio_min, 6),
        'perturb_scale__ratio_max': round(scale_ratio_max, 6),
        'perturb_scale__max_abs_ratio_error_vs_factor': round(float(np.max(np.abs(ratios - SC))), 9),

        'perturb_tail_shift_value': SHIFT,
        'perturb_tail_rows_shifted': n_tail_rows,
        'perturb_tail__before_p57': round(float(base[56]), 4),
        'perturb_tail__after_p57': round(float(tail[56]), 4),
        'perturb_tail__delta_p57': round(float(tail[56] - base[56]), 4),
        'perturb_tail__before_p64': round(float(base[63]), 4),
        'perturb_tail__after_p64': round(float(tail[63]), 4),
        'perturb_tail__delta_p64': round(float(tail[63] - base[63]), 4),
        'perturb_tail__delta_p1': round(float(tail[0] - base[0]), 4),
        'perturb_tail__delta_p10': round(float(tail[9] - base[9]), 4),
        'perturb_tail__delta_p24': round(float(tail[23] - base[23]), 4),
        'perturb_tail__locality_ratio_p64_over_p1': (
            round(float(abs(tail[63] - base[63]) / abs(tail[0] - base[0])), 3)
            if abs(tail[0] - base[0]) > 1e-6 else 'p1 unmoved to float precision (delta < 1e-6)'),

        'perturb_tilt_desc': 'v *= (1 + 0.25*(log(pick)-log(32))): pivots the curve about pick 32',
        'perturb_tilt__slope_p10_before': round(binfo['slopes'][9], 4),
        'perturb_tilt__slope_p10_after': round(tinfo['slopes'][9], 4),
        'perturb_tilt__slope_p32_before': round(binfo['slopes'][31], 4),
        'perturb_tilt__slope_p32_after': round(tinfo['slopes'][31], 4),
        'perturb_tilt__delta_p1': round(float(tilt[0] - base[0]), 4),
        'perturb_tilt__delta_p32': round(float(tilt[31] - base[31]), 4),
        'perturb_tilt__delta_p64': round(float(tilt[63] - base[63]), 4),

        'fallback_picks_in_base_fit': len(binfo['fallback_picks']),
        'cond_threshold': COND_MAX,
        'cond_max_observed_in_base_fit': round(max(c for c in binfo['conds'] if np.isfinite(c)), 4),
        'ridge_rel': RIDGE_REL,

        # ---- the ill-conditioning fallback is LIVE, not dead code: forcing the threshold below the
        # observed condition numbers makes it fire and visibly changes the fit to the local mean.
        'fallback_probe_desc': 'refit with cond_max forced to 1.0 (below every observed cond) — the '
                               'guard must fire at all 64 picks and the fit must move',
        'fallback_probe__cond_max': 1.0,
        'fallback_probe__n_fired_of_64': n_probe_fb,
        'fallback_probe__p1_loclin': round(float(base[0]), 4),
        'fallback_probe__p1_local_mean': round(float(probe[0]), 4),
        'fallback_probe__p1_delta': round(float(probe[0] - base[0]), 4),
        'fallback_probe__p64_loclin': round(float(base[63]), 4),
        'fallback_probe__p64_local_mean': round(float(probe[63]), 4),
        'fallback_probe__p64_delta': round(float(probe[63] - base[63]), 4),
        'fallback_probe__max_abs_delta_over_64': round(float(np.max(np.abs(probe - base))), 4),
    }
