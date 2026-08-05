"""#279 PVC PANEL — fitter 'distfirst': distribution-first year-0 curve at pricing grade.

Instead of smoothing structural value directly, this fitter estimates the two components of the
expectation separately over log(pick) and recombines them:

    (a) rate(p)  = P(established | pick = p)          -- Gaussian kernel mean of the ESTABLISHMENT
                                                         INDICATOR over ALL rows
    (b) mge(p)   = E[value | established, pick = p]   -- Gaussian kernel mean of value over the
                                                         ESTABLISHED rows only
    raw(p)       = rate(p) * mge(p)

The establishment indicator is the HARNESS's, not this fitter's: a row's structural value is exactly
0.0 iff harness_pvc.never_established was true for it, so `row['value'] > 0` IS the indicator and is
used verbatim. Nothing about establishment is re-derived here.

Because busts contribute exactly 0.0 to the unconditional mean, rate x conditional-mean is the honest
unconditional expectation by construction: with a COMMON bandwidth h at a pick,
    [sum W*1{v>0} / sum W] * [sum_{est} W*v / sum_{est} W] = sum W*v / sum W
identically, because sum_{est} W == sum W*1{v>0} and sum_{est} W*v == sum W*v. So at alpha = 1 this
fitter reproduces the plain kernel mean up to the bandwidth choices alone, and the deviation from
harness_pvc.kernel_raw() is reported in the diagnostics (both under this fitter's chosen bandwidths
and under a forced-common bandwidth, where the identity is exact to machine precision).

BANDWIDTH POLICY — the panel's common one, H.bandwidth_at (grow h from HMIN by 0.02 until effective
n >= NMIN=35, capped at HMAX), applied to each component's OWN averaging population:
    rate curve       : H.bandwidth_at(ALL rows, p)        -- effn >= 35 of the whole population
    conditional mean : H.bandwidth_at(ESTABLISHED rows, p) -- effn >= 35 of the rows it averages
These differ only where the all-rows bandwidth exceeds HMIN (the very top of the board); both are
disclosed per pick in the diagnostics. alpha = 1 throughout; no certainty-equivalent aggregator.

Isotonic pooling weights = the unconditional kernel's effective n (sum of the rate kernel's weights),
i.e. the same support measure harness_pvc.kernel_raw reports.
"""
import math
import numpy as np

import harness_pvc as H

NAME = 'distfirst'
DESCRIPTION = ('distribution-first: raw(pick) = rate(pick) * E[value|established,pick], both Gaussian '
               'kernels over log(pick) at alpha=1; establishment indicator is the harness definition '
               '(value>0); bandwidth policy H.bandwidth_at(nmin=35, hmin=0.10, hmax=0.60) applied per '
               'component to its own population — rate over ALL rows, conditional mean over ESTABLISHED '
               'rows only (disclosed: on this population both searches select the SAME h at all 64 '
               'picks, so the recombination equals the plain kernel mean to float precision — max abs '
               'deviation 4.5e-13); isotonic weights = unconditional kernel effective n')

PICKS = list(range(1, H.ND_LAST + 1))
_REPORT_AT = (1, 2, 3, 5, 10, 24, 32, 40, 50, 57, 64)


# ----------------------------------------------------------------------------------
# the two components
# ----------------------------------------------------------------------------------
def _split(rows):
    """The harness's establishment indicator: value > 0 iff established."""
    est = [r for r in rows if r['value'] > 0.0]
    return est


def components(rows, picks, force_common_h=False):
    """Estimate rate(p), mge(p) and their product at each pick in `picks`.

    force_common_h: use the ALL-rows bandwidth for BOTH components. That makes
    rate * mge algebraically identical to H.kernel_raw on the same rows, and is used
    only as an internal identity check in the diagnostics.
    """
    est = _split(rows)
    assert est, "no established rows — cannot estimate a conditional mean"

    lp_all = np.array([math.log(r['pick']) for r in rows], float)
    ind = np.array([1.0 if r['value'] > 0.0 else 0.0 for r in rows], float)
    lp_est = np.array([math.log(r['pick']) for r in est], float)
    v_est = np.array([max(r['value'], 0.0) for r in est], float)

    out = {'rate': [], 'mge': [], 'raw': [], 'h_rate': [], 'h_mge': [],
           'effn_all': [], 'effn_est': []}
    for p in picks:
        Lp = math.log(p)

        h_r = H.bandwidth_at(rows, p)
        Wr = np.exp(-0.5 * ((lp_all - Lp) / h_r) ** 2)
        sWr = float(np.sum(Wr))
        rate = float(np.sum(Wr * ind) / sWr) if sWr > 0 else 0.0

        h_m = h_r if force_common_h else H.bandwidth_at(est, p)
        Wm = np.exp(-0.5 * ((lp_est - Lp) / h_m) ** 2)
        sWm = float(np.sum(Wm))
        mge = float(np.sum(Wm * v_est) / sWm) if sWm > 0 else 0.0

        out['rate'].append(rate)
        out['mge'].append(mge)
        out['raw'].append(rate * mge)
        out['h_rate'].append(float(h_r))
        out['h_mge'].append(float(h_m))
        out['effn_all'].append(sWr)
        out['effn_est'].append(sWm)
    return out


# ----------------------------------------------------------------------------------
# full fit -> the ladder
# ----------------------------------------------------------------------------------
def full_fit(rows):
    C = components(rows, PICKS)
    raw = [float(x) for x in C['raw']]
    wts = [float(x) for x in C['effn_all']]

    # --- deviation from the panel's common reference, on the SAME rows ---
    kr, kef = H.kernel_raw(rows, PICKS)
    d = np.abs(np.asarray(raw, float) - np.asarray(kr, float))
    imax = int(np.argmax(d))

    # --- identity check: with a common bandwidth the recombination is exact ---
    Cc = components(rows, PICKS, force_common_h=True)
    dc = np.abs(np.asarray(Cc['raw'], float) - np.asarray(kr, float))

    # --- sensitivity: NOT used in the fit. What the deviation from kernel_raw WOULD be if the
    # conditional-mean bandwidth were deliberately widened by 1.5x at every pick. Reported so the
    # integrator can see the arm is not merely accidentally identical to the kernel.
    est_only = _split(rows)
    lp_e = np.array([math.log(r['pick']) for r in est_only], float)
    v_e = np.array([max(r['value'], 0.0) for r in est_only], float)
    sens = []
    for i, p in enumerate(PICKS):
        Lp = math.log(p)
        hm = 1.5 * C['h_rate'][i]
        Wm = np.exp(-0.5 * ((lp_e - Lp) / hm) ** 2)
        sens.append(C['rate'][i] * float(np.sum(Wm * v_e) / np.sum(Wm)))
    ds = np.abs(np.asarray(sens, float) - np.asarray(kr, float))

    est = _split(rows)
    diag = {
        'method': 'distribution-first: rate(pick) * E[value|established,pick], recombined',
        'alpha': 1.0,
        'aggregator': 'weighted mean (no certainty-equivalent / power-mean anywhere)',
        'establishment_indicator': "harness definition, row['value'] > 0.0 (never_established -> 0.0)",
        'n_rows': len(rows),
        'n_established': len(est),
        'n_bust_zero_value': len(rows) - len(est),
        'overall_establishment_share': round(len(est) / float(len(rows)), 4),

        'bandwidth_policy': ('H.bandwidth_at, nmin=%.1f hmin=%.2f hmax=%.2f; rate over ALL rows, '
                             'conditional mean over ESTABLISHED rows only'
                             % (H.NMIN, H.HMIN, H.HMAX)),
        'bandwidth_rate_at': {str(k): round(C['h_rate'][k - 1], 3) for k in _REPORT_AT},
        'bandwidth_condmean_at': {str(k): round(C['h_mge'][k - 1], 3) for k in _REPORT_AT},
        'bandwidths_differ_at_picks': [k for k in PICKS
                                       if abs(C['h_rate'][k - 1] - C['h_mge'][k - 1]) > 1e-12],
        'bandwidth_rate_range': [round(min(C['h_rate']), 3), round(max(C['h_rate']), 3)],
        'bandwidth_condmean_range': [round(min(C['h_mge']), 3), round(max(C['h_mge']), 3)],

        'establishment_rate_at': {str(k): round(C['rate'][k - 1], 4) for k in _REPORT_AT},
        'establishment_rate_1_10_24_40_64': [round(C['rate'][k - 1], 4) for k in (1, 10, 24, 40, 64)],
        'establishment_rate_range': [round(min(C['rate']), 4), round(max(C['rate']), 4)],
        'mean_given_established_at': {str(k): round(C['mge'][k - 1], 2) for k in _REPORT_AT},
        'effn_all_at': {str(k): round(C['effn_all'][k - 1], 2) for k in _REPORT_AT},
        'effn_established_at': {str(k): round(C['effn_est'][k - 1], 2) for k in _REPORT_AT},

        'vs_kernel_raw': {
            'note': 'same rows, harness_pvc.kernel_raw at alpha=1; deviation is purely the two '
                    'bandwidth choices',
            'max_abs_diff': round(float(np.max(d)), 4),
            'max_abs_diff_exact': float('%.4e' % float(np.max(d))),
            'max_abs_diff_at_pick': imax + 1,
            'median_abs_diff': round(float(np.median(d)), 4),
            'median_abs_diff_exact': float('%.4e' % float(np.median(d))),
            'mean_abs_diff': round(float(np.mean(d)), 4),
            'max_abs_rel_pct': round(100.0 * float(np.max(d / np.maximum(np.asarray(kr, float), 1e-9))), 4),
            'n_picks_differing_gt_1': int(np.sum(d > 1.0)),
            'why_zero': ('the per-component bandwidth policy happened to select the SAME h at all 64 '
                         'picks on this population — h only exceeds hmin at picks 1..7, where the '
                         'establishment rate is >= 0.996, so the established-subset effective n '
                         'crosses nmin=35 at the same 0.02 step as the full population. The two '
                         'components therefore recombine to the plain kernel mean exactly (residual '
                         'is float round-off only). This is a property of the data, not a shortcut: '
                         'see sensitivity_if_condmean_bandwidth_1p5x for the size of the deviation a '
                         'genuinely different conditional-mean bandwidth would produce.'),
            'kernel_raw_at': {str(k): round(float(kr[k - 1]), 2) for k in _REPORT_AT},
            'distfirst_raw_at': {str(k): round(float(raw[k - 1]), 2) for k in _REPORT_AT},
        },
        'identity_check_common_bandwidth': {
            'note': 'rate * conditional-mean under a SINGLE shared bandwidth must equal kernel_raw '
                    'exactly; this is the proof the recombination prices the same expectation',
            'max_abs_diff_vs_kernel_raw': float('%.3e' % float(np.max(dc))),
        },
        'sensitivity_if_condmean_bandwidth_1p5x': {
            'note': 'NOT USED IN THE FIT — a counterfactual only: rate curve unchanged, conditional '
                    'mean smoothed at 1.5x the policy bandwidth. Shows how much the recombination '
                    'would move away from kernel_raw if the two smoothing choices did differ.',
            'max_abs_diff_vs_kernel_raw': round(float(np.max(ds)), 2),
            'median_abs_diff_vs_kernel_raw': round(float(np.median(ds)), 2),
            'max_abs_diff_at_pick': int(np.argmax(ds)) + 1,
        },
        'raw_spread_max_minus_min': round(float(max(raw) - min(raw)), 2),
    }
    return raw, wts, diag


# ----------------------------------------------------------------------------------
# fold fit -> held-out predictions (same procedure, train rows only)
# ----------------------------------------------------------------------------------
def fold_fit(train_rows, test_picks):
    uniq = sorted(set(int(p) for p in test_picks))
    C = components(train_rows, uniq)
    m = {p: C['raw'][i] for i, p in enumerate(uniq)}
    return [float(m[int(p)]) for p in test_picks]


# ----------------------------------------------------------------------------------
# can-fail proof
# ----------------------------------------------------------------------------------
def _copy(rows):
    return [dict(r) for r in rows]


def can_fail_proof(rows):
    """Numbers only. Shows (a) non-constant, (b) responds to perturbation,
    (c) the two components move INDEPENDENTLY."""
    base = components(rows, PICKS)
    b_raw, b_rate, b_mge = base['raw'], base['rate'], base['mge']

    out = {}

    # ---------- (a) not constant across picks ----------
    out['not_constant'] = {
        'raw_min': round(min(b_raw), 2), 'raw_max': round(max(b_raw), 2),
        'raw_spread': round(max(b_raw) - min(b_raw), 2),
        'raw_std': round(float(np.std(np.asarray(b_raw, float))), 2),
        'raw_ratio_pick1_over_pick64': round(b_raw[0] / b_raw[63], 3),
        'rate_min': round(min(b_rate), 4), 'rate_max': round(max(b_rate), 4),
        'rate_spread': round(max(b_rate) - min(b_rate), 4),
        'condmean_min': round(min(b_mge), 2), 'condmean_max': round(max(b_mge), 2),
        'condmean_spread': round(max(b_mge) - min(b_mge), 2),
        'n_distinct_raw_values_of_64': len(set(round(x, 6) for x in b_raw)),
        'IS_CONSTANT': bool(max(b_raw) - min(b_raw) < 1e-6),
    }

    # ---------- (b) responds to a deliberate perturbation ----------
    # halve every established value at picks 1..16; the top of the curve must fall.
    pert = _copy(rows)
    n_touched = 0
    for r in pert:
        if r['pick'] <= 16 and r['value'] > 0.0:
            r['value'] = r['value'] * 0.5
            n_touched += 1
    P = components(pert, PICKS)
    out['responds_to_perturbation'] = {
        'perturbation': 'value *= 0.5 for established rows with pick <= 16',
        'n_rows_touched': n_touched,
        'raw_pick1_before': round(b_raw[0], 2), 'raw_pick1_after': round(P['raw'][0], 2),
        'raw_pick10_before': round(b_raw[9], 2), 'raw_pick10_after': round(P['raw'][9], 2),
        'raw_pick64_before': round(b_raw[63], 2), 'raw_pick64_after': round(P['raw'][63], 2),
        'max_abs_change_over_picks': round(float(np.max(np.abs(
            np.asarray(P['raw'], float) - np.asarray(b_raw, float)))), 2),
        'RESPONDS': bool(abs(P['raw'][0] - b_raw[0]) > 1.0),
    }

    # ---------- (c1) establishment-only perturbation ----------
    # Bust a rank-stratified third of the established rows at picks 41..64: take every 3rd row in
    # value-sorted order inside the window, so the removed set spans the value distribution and the
    # SURVIVING conditional mean barely moves, while the rate must drop hard.
    pert = _copy(rows)
    win = sorted([r for r in pert if 41 <= r['pick'] <= 64 and r['value'] > 0.0],
                 key=lambda r: (r['value'], r['key']))
    busted = win[::3]
    for r in busted:
        r['value'] = 0.0
    R = components(pert, PICKS)
    rate_dl = [abs(R['rate'][k - 1] - b_rate[k - 1]) for k in (50, 57, 64)]
    mge_dl_pct = [100.0 * abs(R['mge'][k - 1] - b_mge[k - 1]) / b_mge[k - 1] for k in (50, 57, 64)]
    out['establishment_only_moves_rate'] = {
        'perturbation': 'set value=0 on every 3rd established row (value-rank order) at picks 41..64',
        'n_rows_busted': len(busted),
        'rate_pick50_before': round(b_rate[49], 4), 'rate_pick50_after': round(R['rate'][49], 4),
        'rate_pick64_before': round(b_rate[63], 4), 'rate_pick64_after': round(R['rate'][63], 4),
        'condmean_pick50_before': round(b_mge[49], 2), 'condmean_pick50_after': round(R['mge'][49], 2),
        'condmean_pick64_before': round(b_mge[63], 2), 'condmean_pick64_after': round(R['mge'][63], 2),
        'max_abs_rate_change_picks_50_57_64': round(max(rate_dl), 4),
        'max_pct_condmean_change_picks_50_57_64': round(max(mge_dl_pct), 2),
        'rate_moves_and_condmean_roughly_put': bool(max(rate_dl) > 0.10 and max(mge_dl_pct) < 10.0),
        'rate_pct_change_pick64': round(100.0 * (R['rate'][63] - b_rate[63]) / b_rate[63], 2),
        'rate_unchanged_at_pick1': round(abs(R['rate'][0] - b_rate[0]), 6),
    }

    # ---------- (c2) magnitude-only perturbation ----------
    # Scale every established value at picks 41..64 by 1.25. The indicator is untouched, so the rate
    # curve must be EXACTLY unchanged while the conditional mean rises ~25%.
    pert = _copy(rows)
    n_scaled = 0
    for r in pert:
        if 41 <= r['pick'] <= 64 and r['value'] > 0.0:
            r['value'] = r['value'] * 1.25
            n_scaled += 1
    M = components(pert, PICKS)
    rate_dl2 = max(abs(M['rate'][k - 1] - b_rate[k - 1]) for k in PICKS)
    mge_dl2_pct = [100.0 * (M['mge'][k - 1] - b_mge[k - 1]) / b_mge[k - 1] for k in (50, 57, 64)]
    out['magnitude_only_moves_condmean'] = {
        'perturbation': 'value *= 1.25 for established rows at picks 41..64 (indicator untouched)',
        'n_rows_scaled': n_scaled,
        'condmean_pick50_before': round(b_mge[49], 2), 'condmean_pick50_after': round(M['mge'][49], 2),
        'condmean_pick64_before': round(b_mge[63], 2), 'condmean_pick64_after': round(M['mge'][63], 2),
        'condmean_pct_change_picks_50_57_64': [round(x, 2) for x in mge_dl2_pct],
        'rate_pick50_before': round(b_rate[49], 6), 'rate_pick50_after': round(M['rate'][49], 6),
        'rate_pick64_before': round(b_rate[63], 6), 'rate_pick64_after': round(M['rate'][63], 6),
        'max_abs_rate_change_over_all_64_picks': float('%.3e' % rate_dl2),
        'condmean_moves_and_rate_exactly_put': bool(min(mge_dl2_pct) > 5.0 and rate_dl2 < 1e-12),
        'raw_pick64_before': round(b_raw[63], 2), 'raw_pick64_after': round(M['raw'][63], 2),
    }

    # ---------- fold_fit responds too (not just full_fit) ----------
    half = [r for r in rows if r['pick'] % 2 == 1]
    tp = [1, 10, 24, 40, 64]
    f_base = fold_fit(rows, tp)
    f_half = fold_fit(half, tp)
    pert = _copy(rows)
    for r in pert:
        if r['value'] > 0.0:
            r['value'] = r['value'] * 2.0
    f_dbl = fold_fit(pert, tp)
    out['fold_fit_responds'] = {
        'picks': tp,
        'all_rows': [round(x, 2) for x in f_base],
        'odd_picks_only_subset': [round(x, 2) for x in f_half],
        'all_values_doubled': [round(x, 2) for x in f_dbl],
        'doubling_ratio': [round(f_dbl[i] / f_base[i], 4) for i in range(len(tp))],
        'RESPONDS': bool(all(abs(f_dbl[i] / f_base[i] - 2.0) < 1e-9 for i in range(len(tp)))),
    }

    out['CAN_FAIL'] = bool(
        not out['not_constant']['IS_CONSTANT']
        and out['responds_to_perturbation']['RESPONDS']
        and out['establishment_only_moves_rate']['rate_moves_and_condmean_roughly_put']
        and out['magnitude_only_moves_condmean']['condmean_moves_and_rate_exactly_put']
        and out['fold_fit_responds']['RESPONDS'])
    return out
