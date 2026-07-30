"""#279 PVC PANEL — the CONTROL arm.

The shipped kernel, unchanged, PLUS a local-linear boundary correction.

The shipped kernel (harness_pvc.kernel_raw) is a Gaussian kernel over log(pick) followed by a plain
weighted MEAN — i.e. a local CONSTANT (degree-0) fit. At the domain edges the window is one-sided:
there is no pick below 1 and none above 64, so the missing half of the window is silently replaced by
the mass that does exist, which drags the estimate inward (up at pick 64, down at pick 1). A degree-1
local-linear fit is not biased that way to first order, because it can carry the local slope.

This fitter therefore:
  * uses H.kernel_raw() as the base estimator EVERYWHERE;
  * replaces it with a degree-1 weighted least squares fit over log(pick) — same Gaussian weights,
    same bandwidth from H.bandwidth_at() — ONLY inside the boundary zones;
  * leaves the interior bit-for-bit equal to the shipped kernel.

BOUNDARY ZONE (disclosed): a pick is "boundary" when more than 1.0% of the Gaussian window's nominal
weight falls outside the pick domain [1, 64] — i.e. when the log-pick distance to the nearer edge is
less than 2.3263*h(p), h being the harness bandwidth at that pick. That is a direct measure of how
one-sided the window actually is, rather than a round number of picks. On the #279 matrix it resolves
to picks 1-2 at the low edge and picks 51-64 at the high edge; picks 3-50 are the shipped kernel
exactly. The zone is recomputed from whatever rows the fitter is given, so folds are self-consistent.

alpha = 1 throughout. Plain weighted means / plain weighted least squares only. No CE aggregator,
no power mean, no dial anywhere in this file.
"""
import math
import numpy as np

import harness_pvc as H

NAME = 'control'

# --- the one disclosed knob ---------------------------------------------------------------------
MISS_TOL = 0.01          # a pick is "boundary" if >1% of its nominal Gaussian weight is off-domain
_Z_TOL = 2.3263478740408408   # sqrt(2)*erfinv(1-2*MISS_TOL): log-distance/h at which miss == MISS_TOL

DESCRIPTION = (
    "shipped Gaussian log-pick kernel (H.kernel_raw, alpha=1, plain weighted mean) with a degree-1 "
    "local-linear WLS boundary correction over log(pick) applied only where >1.0% of the kernel's "
    "nominal weight falls off the pick domain [1,64] (log-distance to edge < 2.3263*h): boundary "
    "width = picks 1-2 at the low edge and picks 51-64 at the high edge on this matrix; interior "
    "picks 3-50 are the shipped kernel exactly; bandwidth from H.bandwidth_at() (harness policy)."
)

_EDGE_LO = math.log(1.0)
_EDGE_HI = math.log(float(H.ND_LAST))


# ================= helpers =======================================================================
def _arrays(rows):
    lp = np.array([math.log(r['pick']) for r in rows], float)
    v = np.array([max(r['value'], 0.0) for r in rows], float)
    return lp, v


def _miss_fraction(p, h):
    """Fraction of the nominal Gaussian window at pick p that lies outside [1, 64] in log-pick.
    Uses the nearer edge; this is the standard one-sidedness measure, Phi(-d/h)."""
    Lp = math.log(p)
    d = min(Lp - _EDGE_LO, _EDGE_HI - Lp)
    d = max(d, 0.0)
    return 0.5 * math.erfc(d / (h * math.sqrt(2.0)))


def _is_boundary(p, h):
    return _miss_fraction(p, h) > MISS_TOL


def _local_linear(lp, v, p, h):
    """Degree-1 weighted least squares of value on (log(pick) - log(p)), Gaussian weights, bandwidth h.
    Returns the intercept (the fit AT p), or None if the local design is degenerate."""
    Lp = math.log(p)
    x = lp - Lp
    W = np.exp(-0.5 * (x / h) ** 2)
    s0 = float(W.sum())
    if not (s0 > 0.0):
        return None
    s1 = float((W * x).sum())
    s2 = float((W * x * x).sum())
    t0 = float((W * v).sum())
    t1 = float((W * x * v).sum())
    det = s0 * s2 - s1 * s1
    # need real spread in log(pick) under the local weights, else the slope is unidentified
    if not (det > 1e-9 * max(s0 * s2, 1e-12)):
        return None
    a = (s2 * t0 - s1 * t1) / det
    if not np.isfinite(a):
        return None
    return float(a)


def _fit(rows, picks):
    """The estimator. Returns (fit, effn, kernel, info) with fit == kernel off the boundary zones."""
    kern, effn = H.kernel_raw(rows, picks)
    lp, v = _arrays(rows)
    fit = [float(x) for x in kern]
    info = {'h': [], 'miss': [], 'boundary': [], 'used_ll': []}
    for i, p in enumerate(picks):
        h = H.bandwidth_at(rows, p)
        miss = _miss_fraction(p, h)
        onb = miss > MISS_TOL
        used = 0
        if onb:
            a = _local_linear(lp, v, p, h)
            if a is not None:
                fit[i] = max(a, 0.0)      # values are non-negative by construction; keep that
                used = 1
        info['h'].append(h)
        info['miss'].append(miss)
        info['boundary'].append(1 if onb else 0)
        info['used_ll'].append(used)
    return fit, [float(x) for x in effn], [float(x) for x in kern], info


# ================= the three entry points ========================================================
def full_fit(rows):
    picks = list(range(1, 65))
    fit, effn, kern, info = _fit(rows, picks)

    lo = [p for p, b in zip(picks, info['boundary']) if b and p <= 32]
    hi = [p for p, b in zip(picks, info['boundary']) if b and p > 32]
    interior = [p for p, b in zip(picks, info['boundary']) if not b]
    # proof the interior was untouched
    int_max_diff = max([abs(fit[p - 1] - kern[p - 1]) for p in interior], default=0.0)

    dpct = [100.0 * (fit[i] - kern[i]) / kern[i] if kern[i] > 0 else 0.0 for i in range(64)]

    def seam(zone, side):
        """Size of the discontinuity the hard zone edge introduces, in % of the kernel there."""
        if not zone:
            return None
        p = max(zone) if side == 'low' else min(zone)
        return round(dpct[p - 1], 3)

    diag = {
        'estimator': 'H.kernel_raw (alpha=1 weighted mean) + degree-1 local-linear WLS in boundary zones',
        'alpha': 1.0,
        'bandwidth_rule': 'harness',
        'bandwidth_source': 'harness_pvc.bandwidth_at (nmin=%.0f, hmin=%.2f, hmax=%.2f)' % (H.NMIN, H.HMIN, H.HMAX),
        'boundary_rule': 'off-domain nominal kernel mass > %.1f%% (log-pick distance to edge < %.4f*h)'
                         % (100.0 * MISS_TOL, _Z_TOL),
        'boundary_miss_tol_pct': 100.0 * MISS_TOL,
        'boundary_picks_low': lo,
        'boundary_picks_high': hi,
        'boundary_width_low_picks': len(lo),
        'boundary_width_high_picks': len(hi),
        'interior_picks_span': [min(interior), max(interior)] if interior else None,
        'n_interior_picks': len(interior),
        'n_boundary_picks': len(lo) + len(hi),
        'n_local_linear_used': int(sum(info['used_ll'])),
        'n_local_linear_declined_degenerate': int(sum(info['boundary']) - sum(info['used_ll'])),
        'interior_max_abs_diff_vs_shipped_kernel': round(float(int_max_diff), 12),
        'off_domain_mass_pct_at': {str(p): round(100.0 * info['miss'][p - 1], 4)
                                   for p in (1, 2, 3, 10, 32, 50, 51, 56, 60, 64)},
        'bandwidth_at': {str(p): round(info['h'][p - 1], 4)
                         for p in (1, 2, 3, 8, 10, 24, 32, 40, 50, 57, 64)},
        'shipped_kernel_at': {str(p): round(kern[p - 1], 2)
                              for p in (1, 2, 3, 10, 24, 32, 40, 50, 51, 57, 60, 64)},
        'corrected_at': {str(p): round(fit[p - 1], 2)
                         for p in (1, 2, 3, 10, 24, 32, 40, 50, 51, 57, 60, 64)},
        'correction_pct_at': {str(p): round(dpct[p - 1], 3)
                              for p in (1, 2, 3, 10, 24, 32, 40, 50, 51, 57, 60, 64)},
        'max_abs_correction_pct': round(max(abs(x) for x in dpct), 3),
        'max_abs_correction_pct_low_zone': round(max([abs(dpct[p - 1]) for p in lo], default=0.0), 3),
        'max_abs_correction_pct_high_zone': round(max([abs(dpct[p - 1]) for p in hi], default=0.0), 3),
        'correction_at_pick64_abs': round(fit[63] - kern[63], 2),
        'seam_step_pct_at_low_zone_inner_edge': seam(lo, 'low'),
        'seam_step_pct_at_high_zone_inner_edge': seam(hi, 'high'),
        'shipped_kernel_raw_monotone_violations': H.raw_monotone_violations(np.asarray(kern, float)),
        'sum_abs_correction': round(float(sum(abs(fit[i] - kern[i]) for i in range(64))), 2),
    }
    return fit, effn, diag


def fold_fit(train_rows, test_picks):
    """Identical procedure, trained ONLY on train_rows; one prediction per test pick."""
    picks = [int(p) for p in test_picks]
    if not picks:
        return []
    uniq = sorted(set(picks))
    fit, _, _, _ = _fit(train_rows, uniq)
    at = {p: fit[i] for i, p in enumerate(uniq)}
    return [at[p] for p in picks]


# ================= can-fail proof =================================================================
def can_fail_proof(rows):
    """Numbers only. (a) the fit is not constant across picks; (b) it RESPONDS to deliberate
    perturbations of the input values — a global 1.5x scale, and a tail-only halving that must move
    the tail and leave the head essentially alone."""
    picks = list(range(1, 65))
    base, _, kern, _ = _fit(rows, picks)
    b = np.asarray(base, float)

    # (a) not constant
    spread = float(b.max() - b.min())
    kb = np.asarray(kern, float)

    # (b1) global scale by 1.5 — a linear estimator must scale by exactly 1.5
    s_rows = [dict(r, value=r['value'] * 1.5) for r in rows]
    s_fit, _, _, _ = _fit(s_rows, picks)
    ratios = [s_fit[i] / base[i] for i in range(64) if base[i] > 0]

    # (b2) halve the values of the tail rows only (pick >= 50): the tail must move, the head must not
    t_rows = [dict(r, value=(r['value'] * 0.5 if r['pick'] >= 50 else r['value'])) for r in rows]
    t_fit, _, _, _ = _fit(t_rows, picks)

    # (b3) the boundary correction itself must be doing something at the top edge
    out = {
        'n_rows': len(rows),
        'n_picks': 64,
        # --- (a) not constant ---
        'fit_min': round(float(b.min()), 2),
        'fit_max': round(float(b.max()), 2),
        'fit_spread': round(spread, 2),
        'fit_spread_over_mean': round(spread / float(b.mean()), 4),
        'fit_p1': round(base[0], 2),
        'fit_p32': round(base[31], 2),
        'fit_p64': round(base[63], 2),
        'fit_p1_over_p64': round(base[0] / base[63], 4),
        'n_distinct_fit_values_2dp': len({round(x, 2) for x in base}),
        'is_constant': 0 if spread > 1.0 else 1,
        # --- (b1) global 1.5x scale ---
        'scale15_p1_before': round(base[0], 2), 'scale15_p1_after': round(s_fit[0], 2),
        'scale15_p32_before': round(base[31], 2), 'scale15_p32_after': round(s_fit[31], 2),
        'scale15_p64_before': round(base[63], 2), 'scale15_p64_after': round(s_fit[63], 2),
        'scale15_ratio_min': round(float(min(ratios)), 6),
        'scale15_ratio_max': round(float(max(ratios)), 6),
        'scale15_max_abs_ratio_error_vs_1p5': round(float(max(abs(r - 1.5) for r in ratios)), 9),
        # --- (b2) tail-only halving ---
        'tailhalf_rows_perturbed': int(sum(1 for r in rows if r['pick'] >= 50)),
        'tailhalf_p64_before': round(base[63], 2), 'tailhalf_p64_after': round(t_fit[63], 2),
        'tailhalf_p64_pct_change': round(100.0 * (t_fit[63] - base[63]) / base[63], 3),
        'tailhalf_p57_before': round(base[56], 2), 'tailhalf_p57_after': round(t_fit[56], 2),
        'tailhalf_p57_pct_change': round(100.0 * (t_fit[56] - base[56]) / base[56], 3),
        'tailhalf_p50_pct_change': round(100.0 * (t_fit[49] - base[49]) / base[49], 3),
        'tailhalf_p32_pct_change': round(100.0 * (t_fit[31] - base[31]) / base[31], 3),
        'tailhalf_p10_pct_change': round(100.0 * (t_fit[9] - base[9]) / base[9], 3),
        'tailhalf_p1_pct_change': round(100.0 * (t_fit[0] - base[0]) / base[0], 3),
        # --- (b3) the boundary correction is not a no-op ---
        'shipped_kernel_p64': round(kern[63], 2),
        'corrected_p64': round(base[63], 2),
        'boundary_correction_p64_pct': round(100.0 * (base[63] - kern[63]) / kern[63], 3),
        'boundary_correction_max_abs_pct': round(float(max(
            abs(100.0 * (base[i] - kern[i]) / kern[i]) for i in range(64) if kern[i] > 0)), 3),
        'interior_max_abs_diff_vs_kernel': round(float(max(
            abs(base[i] - kern[i]) for i, p in enumerate(picks)
            if not _is_boundary(p, H.bandwidth_at(rows, p)))), 12),
        # --- fold path responds too (same perturbation through fold_fit) ---
        'foldpath_p64_before': round(fold_fit(rows, [64])[0], 2),
        'foldpath_p64_after_scale15': round(fold_fit(s_rows, [64])[0], 2),
    }
    return out
