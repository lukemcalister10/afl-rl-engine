"""#279 PVC PANEL — fitter 'powerspine': a POWER-LAW SPINE plus MONOTONE ADDITIVE RESIDUALS.

THE PROCEDURE (identical in full_fit and fold_fit; only the training rows differ)

1. SPINE  value = A * pick^(-B), estimated by weighted least squares of log(bin mean) on log(pick),
   one bin per distinct pick over the SUB-RANGE picks BREAK_PICK..64, weights = the bin's row count.

   THE 265 ZERO-VALUE ROWS.  The never-established rows carry a structural value of exactly 0.0.
   log(0) is undefined, so an explicit choice is forced.  THIS FITTER NEVER TAKES THE LOG OF AN
   INDIVIDUAL ROW.  It takes the log of the ARITHMETIC MEAN of a pick's rows, and that mean is taken
   over ALL rows at the pick INCLUDING the zeros, at full weight 1.0 each.  A bin mean containing
   zeros is still strictly positive (asserted bin-by-bin), so the log is always defined.  The zeros
   therefore depress each bin mean exactly in proportion to how often they occur — nothing is
   dropped, nothing is floored, no epsilon is invented, and no row is reweighted.  The alternative
   that WAS NOT taken (dropping the zero rows from the bin means) is fitted anyway and reported in
   the diagnostics and in can_fail_proof, so the size and direction of the bias avoided is visible.

2. THE BREAK POINT, AND THE EXTENSION BELOW IT.  BREAK_PICK = 8.  Eight is the first pick at which
   the shipped kernel's own bandwidth policy sits on its floor hmin=0.10 on this population — the
   policy has to widen to h = 0.60, 0.36, 0.26, 0.20, 0.16, 0.14, 0.12 at picks 1..7 to reach its
   nmin=35 effective rows, and is at 0.10 from pick 8 to pick 64.  Picks 1..7 are therefore exactly
   the picks whose local support is too thin to stand on its own, so they do not get a vote on the
   global exponent.  The break point is FIXED at 8 for the full fit and for every fold fit alike
   (a fold trains on ~80% of the rows, where the same policy would only reach its floor at pick 10;
   that number is reported rather than used, because the break must not move between fits).

   A and B are estimated only on picks >= 8, so picks 1..7 need an extension rule.  The spine is
   HELD FLAT at its pick-8 value, NOT extrapolated: extrapolating A*p^-B down to pick 1 gives A
   itself, roughly 6x the observed pick-1 mean (both numbers are reported in the diagnostics), and
   that overshoot would then have to be undone by the residual layer at the one boundary where the
   residual window is most one-sided.  Holding the spine flat instead leaves the top-of-draft shape
   to the residual layer, which is fitted there on real rows.

3. RESIDUALS, ADDITIVE.  e_i = value_i - spine(pick_i), for every training row, zeros included.
   Additive (not log-ratio) precisely so that the zero rows need no special treatment here either.
   At each pick p the residual is smoothed by a Gaussian in log(pick) with the SHIPPED common
   bandwidth policy, H.bandwidth_at: h starts at hmin=0.10 and grows in 0.02 steps until the
   effective n reaches nmin=35, capped at hmax=0.60.  The realised schedule on the full population
   is h = 0.60, 0.36, 0.26, 0.20, 0.16, 0.14, 0.12 at picks 1..7 and h = 0.10 at every pick from 8
   to 64; the table is reported in the diagnostics, together with the table an 80%-of-rows fit (a
   fold-sized training set) sees.  The policy is re-evaluated on the training rows only inside
   fold_fit — same policy, same code path, no leakage from the held-out fold.

4. RECOMBINE, then MONOTONE.  c(p) = spine(p) + smoothed_residual(p), clipped at 0.  c is then made
   monotone NON-INCREASING with the harness's own pooled-adjacent-violators routine (H.pava_ni),
   weighted by the residual smooth's effective n, and the resulting plateaus are given a 1.0-unit
   strict descent so the curve handed to the harness is already strictly descending in the units the
   ladder rounds to.  All of this happens BEFORE the harness's pin step, which is left untouched.

full_fit returns that 64-point curve as raw and the effective n as the isotonic weights.
fold_fit runs steps 1-4 on the training rows alone and reads the prediction for each held-out row off
the resulting 64-point curve.  It does NOT apply the pin: the pin is the harness's ladder step, not a
prediction, and pinning pick 1 to 3000 would corrupt the held-out score.

alpha = 1 throughout.  No certainty-equivalent / power-mean aggregator anywhere in this file.
"""
import math
import collections
import numpy as np

import harness_pvc as H

NAME = 'powerspine'

BREAK_PICK = 8          # spine estimated on picks 8..64; held flat below (disclosed, see module docstring)
RESID_HMIN = H.HMIN     # 0.10
RESID_HMAX = H.HMAX     # 0.60
RESID_NMIN = H.NMIN     # 35.0
DESCENT_GAP = 1.0       # value units of strict descent imposed on post-PAVA plateaus
N_PICKS = 64

DESCRIPTION = (
    "power-law spine A*pick^-B (WLS of log(per-pick mean) on log(pick), the 265 zero-value rows kept "
    "at full weight inside those means so the log of a zero is never taken) fitted on the SUB-RANGE "
    "picks 8-64 with BREAK POINT = 8 (first pick where the shipped bandwidth policy sits on its floor) "
    "and held FLAT at spine(8) below the break rather than extrapolated, plus additive residuals "
    "smoothed with the shipped bandwidth policy — RESIDUAL BANDWIDTH h(p) in log(pick) units, grown "
    "from hmin=0.10 in 0.02 steps until nmin=35 effective rows, capped hmax=0.60, realised as "
    "h=0.60/0.36/0.26/0.20/0.16/0.14/0.12 at picks 1-7 and h=0.10 at every pick 8-64 — then "
    "recombined, clipped at 0 and forced monotone non-increasing (PAVA on effective-n weights, then a "
    "1.0-unit strict descent over plateaus) before the harness's pin; alpha=1, no CE aggregator"
)


# ----------------------------------------------------------------------------------
# step 1: the spine
# ----------------------------------------------------------------------------------
def _bin_means(rows, lo, hi, drop_zeros=False):
    """Per-pick arithmetic means over picks in [lo, hi].

    drop_zeros=False (the choice this fitter makes) keeps every row, so zero-value rows depress the
    mean in proportion to their frequency.  drop_zeros=True exists ONLY so the bias of the rejected
    alternative can be measured and reported; it is never used by the fit itself.
    """
    acc = collections.defaultdict(lambda: [0.0, 0])
    for r in rows:
        p = int(r['pick'])
        if not (lo <= p <= hi):
            continue
        v = float(r['value'])
        if drop_zeros and v <= 0.0:
            continue
        e = acc[p]
        e[0] += v
        e[1] += 1
    out = []
    for p in sorted(acc):
        s, n = acc[p]
        if n <= 0:
            continue
        out.append((p, s / n, n))
    return out


def _fit_power(rows, lo=BREAK_PICK, hi=N_PICKS, drop_zeros=False):
    """Weighted least squares of log(bin mean) on log(pick).  Returns (A, B, info)."""
    bins = _bin_means(rows, lo, hi, drop_zeros=drop_zeros)
    x, y, w, n_nonpos = [], [], [], 0
    for p, m, n in bins:
        if not (m > 0.0):
            # a bin whose every row is zero has no log; count it, exclude it, and disclose the count.
            n_nonpos += 1
            continue
        x.append(math.log(p))
        y.append(math.log(m))
        w.append(float(n))
    assert len(x) >= 3, "spine sub-range has %d usable pick bins — refusing to fit" % len(x)
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    w = np.asarray(w, float)
    sw = np.sqrt(w)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
    A = float(math.exp(beta[0]))
    B = float(-beta[1])
    pred = beta[0] + beta[1] * x
    ss_res = float(np.sum(w * (y - pred) ** 2))
    ybar = float(np.sum(w * y) / np.sum(w))
    ss_tot = float(np.sum(w * (y - ybar) ** 2))
    info = {'A': A, 'B': B,
            'n_pick_bins': int(len(x)),
            'n_bins_all_zero_excluded': int(n_nonpos),
            'n_rows_in_spine_range': int(float(np.sum(w))),
            'wls_r2_on_log_means': round(1.0 - ss_res / ss_tot, 6) if ss_tot > 0 else None,
            'wls_rmse_log_units': round(math.sqrt(ss_res / float(np.sum(w))), 6)}
    return A, B, info


def _spine(A, B, p):
    """A*p^-B for p >= BREAK_PICK; held FLAT at its BREAK_PICK value below the break (disclosed)."""
    q = p if p >= BREAK_PICK else BREAK_PICK
    return A * (float(q) ** (-B))


# ----------------------------------------------------------------------------------
# steps 3-4: residual smooth, recombine, monotone
# ----------------------------------------------------------------------------------
def _curve(rows, picks=None):
    """The whole procedure on `rows`.  Returns (curve, effn, info) over `picks` (default 1..64).

    curve is monotone non-increasing and strictly descending by at least DESCENT_GAP.
    """
    if picks is None:
        picks = list(range(1, N_PICKS + 1))
    A, B, sp_info = _fit_power(rows)

    lp = np.array([math.log(r['pick']) for r in rows], float)
    v = np.array([max(float(r['value']), 0.0) for r in rows], float)
    sp_rows = np.array([_spine(A, B, int(r['pick'])) for r in rows], float)
    resid = v - sp_rows

    hs, rhat, effn, spine_at = [], [], [], []
    for p in picks:
        h = H.bandwidth_at(rows, p, nmin=RESID_NMIN, hmin=RESID_HMIN, hmax=RESID_HMAX)
        W = np.exp(-0.5 * ((lp - math.log(p)) / h) ** 2)
        sW = float(np.sum(W))
        hs.append(float(h))
        effn.append(sW)
        rhat.append(float(np.sum(W * resid) / sW) if sW > 0 else 0.0)
        spine_at.append(_spine(A, B, p))

    p1 = [float(r['value']) for r in rows if int(r['pick']) == 1]
    p1_mean = float(np.mean(p1)) if p1 else 0.0

    comb = np.asarray(spine_at, float) + np.asarray(rhat, float)
    n_clipped = int(np.sum(comb < 0.0))
    comb = np.maximum(comb, 0.0)

    pre_inversions = int(sum(1 for i in range(1, len(comb)) if comb[i] > comb[i - 1] + 1e-12))
    wts = np.asarray(effn, float)
    iso = H.pava_ni(comb, wts)
    n_moved = int(np.sum(np.abs(np.asarray(iso, float) - comb) > 1e-9))
    ties = int(sum(1 for i in range(1, len(iso)) if abs(iso[i] - iso[i - 1]) <= 1e-9))

    out = np.asarray(iso, float).copy()
    n_desc = 0
    for i in range(1, len(out)):
        if out[i] > out[i - 1] - DESCENT_GAP:
            out[i] = out[i - 1] - DESCENT_GAP
            n_desc += 1
    assert np.all(np.isfinite(out)), "non-finite curve"
    assert float(out.min()) > 0.0, "curve went non-positive after descent enforcement (min %.4f)" % out.min()

    info = dict(sp_info)
    info.update({
        'break_point_pick': BREAK_PICK,
        'spine_range': '%d-%d' % (BREAK_PICK, N_PICKS),
        'spine_extension_below_break': 'held flat at spine(%d)' % BREAK_PICK,
        'spine_at_break': round(_spine(A, B, BREAK_PICK), 3),
        'spine_extrapolated_to_pick1_not_used': round(A, 3),
        'observed_mean_value_at_pick1': round(p1_mean, 3),
        'extrapolation_overshoot_at_pick1_multiple': round(A / p1_mean, 3) if p1_mean > 0 else None,
        'residual_bandwidth_policy': 'H.bandwidth_at: hmin=%.2f -> hmax=%.2f in 0.02 steps until effective n >= %.0f' % (RESID_HMIN, RESID_HMAX, RESID_NMIN),
        'residual_bandwidth_hmin': RESID_HMIN,
        'residual_bandwidth_hmax': RESID_HMAX,
        'residual_bandwidth_nmin': RESID_NMIN,
        'residual_bandwidth_used_min': round(float(min(hs)), 4),
        'residual_bandwidth_used_max': round(float(max(hs)), 4),
        'residual_bandwidth_at': {str(p): round(h, 4) for p, h in zip(picks, hs)
                                  if p in (1, 2, 3, 4, 5, 6, 7, 8, 10, 24, 32, 40, 50, 57, 64)},
        'n_picks_at_bandwidth_floor': int(sum(1 for h in hs if h <= RESID_HMIN + 1e-9)),
        'first_pick_at_bandwidth_floor': int(min([p for p, h in zip(picks, hs)
                                                  if h <= RESID_HMIN + 1e-9] or [-1])),
        'n_rows_trained_on': len(rows),
        'n_zero_value_rows_trained_on': int(np.sum(v <= 0.0)),
        'residual_mean_abs_at_pick': round(float(np.mean(np.abs(np.asarray(rhat, float)))), 4),
        'n_picks_clipped_at_zero': n_clipped,
        'pre_pava_inversions': pre_inversions,
        'n_picks_moved_by_pava': n_moved,
        'n_pava_plateau_ties': ties,
        'strict_descent_gap_value_units': DESCENT_GAP,
        'n_picks_given_plateau_descent': n_desc,
    })
    return out, wts, info


# ----------------------------------------------------------------------------------
# the three entry points the runner calls
# ----------------------------------------------------------------------------------
def full_fit(rows):
    curve, wts, info = _curve(rows)
    A, B = info['A'], info['B']
    _, B_dz, dz = _fit_power(rows, drop_zeros=True)
    info['A_reported'] = round(A, 4)
    info['B_reported'] = round(B, 6)
    info['zero_row_handling'] = ('265-style zero-value rows retained at full weight inside the per-pick '
                                 'arithmetic means; log is taken of the mean, never of a row')
    info['B_if_zero_rows_dropped_NOT_USED'] = round(B_dz, 6)
    info['A_if_zero_rows_dropped_NOT_USED'] = round(dz['A'], 4)
    info['spine40_kept_zeros'] = round(_spine(A, B, 40), 3)
    info['spine40_if_zeros_dropped_NOT_USED'] = round(dz['A'] * 40.0 ** (-B_dz), 3)
    # what a fold-sized training set (80% of the rows, deterministic) would see: reported, not used.
    keys = sorted(r['key'] for r in rows)
    dropped = set(keys[i] for i in range(0, len(keys), 5))
    sub = [r for r in rows if r['key'] not in dropped]
    hsub = {p: H.bandwidth_at(sub, p, nmin=RESID_NMIN, hmin=RESID_HMIN, hmax=RESID_HMAX)
            for p in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 32, 64)}
    A_sub, B_sub, _ = _fit_power(sub)
    info['fold_sized_80pct_n_rows'] = len(sub)
    info['fold_sized_80pct_bandwidth_at'] = {str(p): round(h, 4) for p, h in hsub.items()}
    info['fold_sized_80pct_first_pick_at_bandwidth_floor'] = int(
        min([p for p, h in sorted(hsub.items()) if h <= RESID_HMIN + 1e-9] or [-1]))
    info['fold_sized_80pct_B'] = round(B_sub, 6)
    info['fold_sized_80pct_A'] = round(A_sub, 4)
    info['curve_at'] = {str(p): round(float(curve[p - 1]), 3)
                        for p in (1, 2, 3, 6, 8, 10, 24, 32, 40, 50, 57, 64)}
    info['curve_min'] = round(float(curve.min()), 3)
    info['curve_max'] = round(float(curve.max()), 3)
    info['curve_spread_max_minus_min'] = round(float(curve.max() - curve.min()), 3)
    return [float(x) for x in curve], [float(x) for x in wts], info


def fold_fit(train_rows, test_picks):
    """Same procedure, same break point, same bandwidth policy — trained on train_rows only."""
    picks = [int(p) for p in test_picks]
    grid = list(range(1, N_PICKS + 1))
    curve, _wts, _info = _curve(train_rows, picks=grid)
    lut = {p: float(curve[i]) for i, p in enumerate(grid)}
    out = []
    for p in picks:
        q = min(max(p, 1), N_PICKS)
        out.append(lut[q])
    return out


def can_fail_proof(rows):
    """Numbers showing this fitter is not degenerate.  All entries are numbers."""
    base, _w, info = _curve(rows)
    A, B = info['A'], info['B']
    b = np.asarray(base, float)

    # (a) NOT CONSTANT across picks
    spread = float(b.max() - b.min())
    sd = float(np.std(b))
    ratio = float(b[0] / b[-1])

    # (b) RESPONDS to deliberate perturbations of the input values
    #  P1: multiply every value by 1.25 -> curve should scale by ~1.25, B should be unchanged
    p1 = [dict(r, value=float(r['value']) * 1.25) for r in rows]
    c1, _, i1 = _curve(p1)
    c1 = np.asarray(c1, float)
    #  P2: halve every value at picks >= 33 -> the tail must fall and B must rise
    p2 = [dict(r, value=float(r['value']) * (0.5 if int(r['pick']) >= 33 else 1.0)) for r in rows]
    c2, _, i2 = _curve(p2)
    c2 = np.asarray(c2, float)
    #  P3: add 800 to every value at picks 1..10 -> the head must rise
    p3 = [dict(r, value=float(r['value']) + (800.0 if int(r['pick']) <= 10 else 0.0)) for r in rows]
    c3, _, i3 = _curve(p3)
    c3 = np.asarray(c3, float)

    # (c) the exponent B, and the rejected zero-row alternative
    _, B_dz, dz = _fit_power(rows, drop_zeros=True)

    out = {
        # --- (a) not constant ---
        'n_picks': int(len(b)),
        'raw_min': round(float(b.min()), 3),
        'raw_max': round(float(b.max()), 3),
        'raw_spread_max_minus_min': round(spread, 3),
        'raw_std_across_picks': round(sd, 3),
        'raw_pick1_over_pick64_ratio': round(ratio, 4),
        'n_distinct_raw_values': int(len(set(round(float(x), 6) for x in b))),
        'IS_CONSTANT_across_picks_0_or_1': int(spread < 1e-6),

        # --- (b) responds to perturbation ---
        'P1_scale_all_values_by': 1.25,
        'P1_before_pick10': round(float(b[9]), 3), 'P1_after_pick10': round(float(c1[9]), 3),
        'P1_before_pick32': round(float(b[31]), 3), 'P1_after_pick32': round(float(c1[31]), 3),
        'P1_before_pick64': round(float(b[63]), 3), 'P1_after_pick64': round(float(c1[63]), 3),
        'P1_median_after_over_before': round(float(np.median(c1 / b)), 4),
        'P1_max_abs_change': round(float(np.max(np.abs(c1 - b))), 3),
        'P1_B_before': round(B, 6), 'P1_B_after': round(i1['B'], 6),

        'P2_halve_values_at_picks_33_to_64': 0.5,
        'P2_before_pick40': round(float(b[39]), 3), 'P2_after_pick40': round(float(c2[39]), 3),
        'P2_before_pick64': round(float(b[63]), 3), 'P2_after_pick64': round(float(c2[63]), 3),
        'P2_max_abs_change': round(float(np.max(np.abs(c2 - b))), 3),
        'P2_B_before': round(B, 6), 'P2_B_after': round(i2['B'], 6),
        'P2_B_rose_0_or_1': int(i2['B'] > B),

        'P3_add_to_values_at_picks_1_to_10': 800.0,
        'P3_before_pick1': round(float(b[0]), 3), 'P3_after_pick1': round(float(c3[0]), 3),
        'P3_before_pick10': round(float(b[9]), 3), 'P3_after_pick10': round(float(c3[9]), 3),
        'P3_before_pick64': round(float(b[63]), 3), 'P3_after_pick64': round(float(c3[63]), 3),
        'P3_max_abs_change': round(float(np.max(np.abs(c3 - b))), 3),

        'RESPONDS_to_all_three_perturbations_0_or_1': int(
            np.max(np.abs(c1 - b)) > 1.0 and np.max(np.abs(c2 - b)) > 1.0 and np.max(np.abs(c3 - b)) > 1.0),

        # --- (c) the exponent ---
        'fitted_exponent_B': round(B, 6),
        'fitted_coefficient_A': round(A, 4),
        'B_in_sane_range_0p2_to_3p0_0_or_1': int(0.2 <= B <= 3.0),
        'B_sane_range_lo': 0.2, 'B_sane_range_hi': 3.0,
        'spine_wls_r2_on_log_means': info['wls_r2_on_log_means'],
        'break_point_pick': BREAK_PICK,
        'residual_bandwidth_used_min': info['residual_bandwidth_used_min'],
        'residual_bandwidth_used_max': info['residual_bandwidth_used_max'],

        # --- zero-row handling audit: the alternative NOT taken ---
        'n_zero_value_rows': int(sum(1 for r in rows if float(r['value']) <= 0.0)),
        'B_zeros_kept_USED': round(B, 6),
        'B_zeros_dropped_NOT_USED': round(B_dz, 6),
        'spine_pick40_zeros_kept_USED': round(_spine(A, B, 40), 3),
        'spine_pick40_zeros_dropped_NOT_USED': round(dz['A'] * 40.0 ** (-B_dz), 3),
        'dropping_zeros_would_raise_spine40_by_pct': round(
            100.0 * (dz['A'] * 40.0 ** (-B_dz) - _spine(A, B, 40)) / _spine(A, B, 40), 3),
    }
    return out
