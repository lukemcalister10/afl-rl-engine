#!/usr/bin/env python3
"""ORDER 26B-C2 -- THE LOCAL-LINEAR BOUNDARY FIT.

OWNER RULING, #334 comment 5275737926 (2026-08-13):

    "But pick 2, to a lesser extent, is still punished by not having north neigbours. I think we use
     local linear fits to 'extend' the north and south ends of the Pick Curve, do you agree?"

THE DEFECT. The shipped year-zero aggregator (harness_pvc_REPINNED_pass3.py::kernel_raw) is a Gaussian
kernel over log(pick) followed by a weighted MEAN -- a LOCAL-CONSTANT estimator. At an interior pick
the borrowed weight comes from both sides of a declining curve and the two pulls cancel to first order.
At pick 1 every borrowed point is southern and worth less, so the estimate is dragged DOWN (-7.1%
measured). At pick 64 every borrowed point is northern and worth more, so the tail is FLATTERED UP.
That is textbook one-sided boundary bias, and a local-constant estimator cannot fix it: it averages the
slope instead of fitting it.

THE FIX, AS RULED. Replace the weighted-mean step with a LOCAL-LINEAR fit over the same log(pick) axis,
using the same Gaussian kernel and the same bandwidth-growth rule, applied across the WHOLE curve --
one method, no seam. In the interior a local-linear fit reproduces the weighted mean wherever the curve
is locally straight; at both boundaries it fits the local slope and extrapolates along it, which
cancels the first-order bias in both directions.

NOTHING HERE IS INVENTED. Two objects are reused, both cited:

  * THE KERNEL AND THE BANDWIDTH RULE come from the SHIPPED aggregator,
    docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py::kernel_raw --
    Gaussian over log(pick), bandwidth grown from HMIN in 0.02 steps until the effective n reaches
    NMIN, capped at HMAX. Byte-identical rule; only the final estimator changes.

  * THE SOLVER IS THE ENGINE'S OWN, engine/forward_valuation/par_build.py::loclin (lines 382-428),
    reused algebra, not a new solver: the 2-parameter weighted normal equations accumulated with
    math.fsum (order-fixed and correctly-rounded, the engine's own 2026-07-14 determinism fix), solved
    by LU WITH PARTIAL PIVOTING -- the same algorithm LAPACK dgesv uses -- with the engine's own
    RANK-DEFICIENT FALLBACK: when relcond = det/(Sw*Swuu) drops below 1e-9 the weighted design has no
    x-spread, the local-linear fit is undefined, and the estimator degrades to the local-CONSTANT
    weighted mean. That fallback is the engine's ruled behaviour and it is kept exactly.

THE ONE DELIBERATE DIFFERENCE from par_build.py::loclin, declared: par_build weights with a TRICUBE
kernel at a fixed bandwidth H_LOGPICK; this file weights with the pick curve's own GAUSSIAN kernel at
its own grown bandwidth, because the ruling is to change the ESTIMATOR while holding the kernel and the
bandwidth rule fixed. The normal equations, the fsum accumulation, the pivot and the fallback are
par_build's, unchanged.

ENGINE BYTES: 0. par_build.py is READ and CITED, never modified and never imported (importing it would
drag the whole par machinery and its pins into a derivation harness).
"""
import math as _math

# The shipped aggregator's dials, restated here ONLY so this module is self-describing; the harness
# that calls it passes the live values through, and o26b_derive.py asserts they match the shipped ones.
NMIN_DEFAULT, HMIN_DEFAULT, HMAX_DEFAULT = 35.0, 0.10, 0.60

PROVENANCE = dict(
    ruling='#334 comment 5275737926 (2026-08-13), OWNER: local-linear fits to extend the north and '
           'south ends of the pick curve',
    estimator_source='engine/forward_valuation/par_build.py::loclin, lines 382-428 -- fsum normal '
                     'equations, LU with partial pivoting, rank-deficient fallback to the local-'
                     'constant weighted mean at relcond < 1e-9',
    kernel_source='docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py::'
                  'kernel_raw -- Gaussian over log(pick), bandwidth grown from HMIN in 0.02 steps '
                  'until effective n >= NMIN, capped at HMAX',
    declared_difference='par_build weights with a TRICUBE kernel at a fixed bandwidth; this file '
                        'weights with the pick curve\'s own GAUSSIAN kernel at its own grown '
                        'bandwidth. The ruling changes the ESTIMATOR, not the kernel.',
    engine_bytes=0,
)


def bandwidth_at(lp, Lp, nmin, hmin, hmax):
    """The SHIPPED bandwidth-growth rule, carried verbatim from kernel_raw/bandwidth_at."""
    h = hmin
    while h < hmax:
        if _math.fsum(_math.exp(-0.5 * ((x - Lp) / h) ** 2) for x in lp) >= nmin:
            break
        h += 0.02
    return h


def loclin_at(lp, v, Lp, h):
    """par_build.py::loclin's algebra, reused verbatim on this kernel's weights.

    Returns (yhat, Sw, ess, relcond, used_fallback)."""
    w = [_math.exp(-0.5 * ((x - Lp) / h) ** 2) for x in lp]
    nz = [(wi, xi - Lp, yi) for wi, xi, yi in zip(w, lp, v) if wi > 0.0]
    if not nz:
        return float('nan'), 0.0, 0.0, 0.0, True
    Sw = _math.fsum(a for a, _b, _c in nz)
    if Sw <= 0:
        return float('nan'), 0.0, 0.0, 0.0, True
    Swu = _math.fsum(a * b for a, b, _c in nz)
    Swuu = _math.fsum(a * b * b for a, b, _c in nz)
    Swy = _math.fsum(a * c for a, _b, c in nz)
    Swuy = _math.fsum(a * b * c for a, b, c in nz)
    # relcond = det/(Sw*Swuu) -- par_build's own rank-deficiency flag, at machine epsilon
    relcond = (Sw * Swuu - Swu * Swu) / (Sw * Swuu) if Sw * Swuu > 0 else 0.0
    if relcond < 1e-9:
        yhat = Swy / Sw                       # rank-deficient -> local-CONSTANT (the weighted mean)
        fallback = True
    else:
        a, b, c, d, e, f = Sw, Swu, Swu, Swuu, Swy, Swuy
        if abs(c) > abs(a):                   # partial pivot on the larger leading entry
            a, b, e, c, d, f = c, d, f, a, b, e
        m = c / a
        d2 = d - m * b
        f2 = f - m * e
        b1 = (f2 / d2) if d2 != 0.0 else 0.0
        yhat = (e - b * b1) / a               # b0 = the fit AT x0 (the intercept)
        fallback = False
    ess = (Sw * Sw) / _math.fsum(a * a for a, _b, _c in nz)
    return float(yhat), float(Sw), float(ess), float(relcond), fallback


def kernel_loclin(rows, picks, nmin=NMIN_DEFAULT, hmin=HMIN_DEFAULT, hmax=HMAX_DEFAULT):
    """The C2 aggregator. Same signature and same value-clipping as the shipped kernel_raw, so it is a
    drop-in replacement for the weighted-mean step.

    Returns (yhat[], effn[], diag[]) where diag carries per-pick h, ESS, relcond, fallback and the
    borrowed-weight share -- reported per pick, as the shipped harness reports weights and bandwidths.

    NEGATIVE FITS: a local-linear extrapolation can in principle go below zero where the local slope is
    steep and the boundary is thin. Delivered value is >= 0 by construction, so a negative fit is
    floored at 0.0 and the event is FLAGGED in diag (`floored`), never silently clipped."""
    lp = [_math.log(r['pick']) for r in rows]
    v = [max(r['value'], 0.0) for r in rows]        # identical clipping to kernel_raw
    out, effn, diag = [], [], []
    for p in picks:
        Lp = _math.log(p)
        h = bandwidth_at(lp, Lp, nmin, hmin, hmax)
        yhat, Sw, ess, relcond, fb = loclin_at(lp, v, Lp, h)
        own = _math.fsum(_math.exp(-0.5 * ((x - Lp) / h) ** 2)
                         for x, r in zip(lp, rows) if r['pick'] == p)
        floored = (yhat == yhat and yhat < 0.0)
        if floored:
            yhat = 0.0
        out.append(yhat)
        effn.append(Sw)
        diag.append(dict(pick=p, h=h, effn=Sw, ess=ess, relcond=relcond, fallback=fb,
                         own_weight=own, borrowed_share=(1.0 - own / Sw) if Sw else float('nan'),
                         floored=floored))
    return out, effn, diag
