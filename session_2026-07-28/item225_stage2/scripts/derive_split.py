"""ITEM 225 STAGE 2 — THE ND 1-64 CURVE AND THE POOL LEVEL, DERIVED FROM SCRATCH.

THE METHOD IS HELD CONSTANT. This is derive_pvc2.py's R1 COMPOSED PATHWAY construction, function
for function, with tau=0.12 / nmin=35 / PW_FLOOR=0.11 / PIN1=3000 unchanged. pava_ni, build_points,
fit_year0 and monotone_strict are carried over verbatim. What changes is THE DATA (store e3aaba77,
not c120cfd5), THE SEPARATION (two populations), and THE POSITION ASSIGNMENTS (a consequence of the
data). A reader must be able to attribute every difference from the old numbers to one of those three
and never to a method this seat changed.

TWO FITS, TWO POPULATIONS, NOTHING CROSSING (Addendum 1 §B):

    ND curve, picks 1-64  trained on national draftees at picks 1-64
                          never sees a rookie, pre-season or pickless row
    pool level, per pos   trained on pool entrants (ND 65+, all RD, PSD, every pickless mechanism)
                          never sees a national 1-64 row

AND THE EXCLUSION RUNS THROUGH THE POOLING TERM, NOT ONLY THROUGH THE SAMPLED ROWS (owner ruling,
2026-07-28). Each fit pools WITHIN ITS OWN POPULATION. A pooled average computed over the combined
population and blended into an ND prior is a pool row teaching the national curve by a quieter
route, and a check that inspects sampled rows alone reads clean while it happens. Every aggregate
here is therefore computed inside one population and stamped with which one, so the check can
observe the pooling term as well as the sample.

THE POOL'S LEVEL DOES NOT COME FROM V0 (Addendum 1 §C). v0_start is a function of (position, age
band, pick) and carries no information about whether a player ever played, so a mean of it is a
statement about entry slots and ages. The level comes from REALISED OUTCOMES with never-established
players entered as 0.0 -- that zero is the survivorship fix and it is not optional.

DERIVES ONLY. Adoption is the owner's and is a separate release with its own word.
"""
import os, sys, json, hashlib, argparse, math
from collections import defaultdict, Counter
import numpy as np
from sklearn.isotonic import IsotonicRegression

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
BASE = REPO + '/session_2026-07-28/item225_stage2'
PER  = BASE + '/out/per_entrant_split.json'
OUT  = BASE + '/out'

# ---- THE SHIPPED DERIVATION'S DIALS. UNCHANGED. -------------------------------------------------
PW_FLOOR   = 0.11          # engine residual prior weight (_ev_pw floor)
PIN1       = 3000          # numeraire (owner-set; RL_PICK1)
TAU        = 0.12          # time-kernel bandwidth (pathway influence; gate-bounded)
NMIN       = 35.0          # adaptive-bw target eff-n
HMIN, HMAX = 0.10, 0.60    # adaptive pick-bandwidth bounds
YR_LO, YR_HI = 2004, 2024  # derive_pvc2's cohort window
# ---- THE PRIORS RECIPE'S DIALS. UNCHANGED (register v509; Addendum 1 §A keeps them). -------------
PRIOR_LO, PRIOR_HI = 2006, 2020   # bust-priors debut-cohort window
PRIOR_N_REF        = 200          # min(n_pos/200, 1)
PRIOR_CEIL         = 0.6          # ... * 0.6   -- the blend ceiling. REPORTED, NOT FIXED.
QUAL_GAMES         = 6            # a season counts toward best-3 at >=6 games
BEST_N             = 3            # best-3 season average
POSITIONS = ['MID', 'GEN_FWD', 'KEY_FWD', 'GEN_DEF', 'KEY_DEF', 'RUC']

ND_CURVE_LAST = 64


# =================================================================================================
# CARRIED OVER VERBATIM FROM derive_pvc2.py -- do not "improve" these.
# =================================================================================================
def pava_ni(vals, wts):
    """Non-increasing weighted isotonic regression (PAVA)."""
    n = len(vals)
    v = [float(x) for x in vals]; w = [float(x) for x in wts]
    stackv = []; stackw = []; stackn = []
    for j in range(n):
        cv, cw, cn = v[j], w[j], 1
        while stackv and stackv[-1] < cv - 1e-12:
            pv, pw_, pn = stackv.pop(), stackw.pop(), stackn.pop()
            cv = (pv * pw_ + cv * cw) / (pw_ + cw); cw = pw_ + cw; cn = pn + cn
        stackv.append(cv); stackw.append(cw); stackn.append(cn)
    out = []
    for bv, bn in zip(stackv, stackn):
        out += [bv] * bn
    return np.array(out)


def build_points(P, drop_poles=False):
    """(logpick, tyear, value, weight, pos) for the 2-D fit. t=0 -> v0 (weight 1.0);
    t=k -> vpath[k-1] (weight = evidence share). derive_pvc2.build_points, verbatim."""
    lp, ty, val, wt, pos = [], [], [], [], []
    for r in P:
        L = np.log(r['pick'])
        is_pole = (r['games_yr1'] == 0)
        lp.append(L); ty.append(0); val.append(r['v0']); wt.append(1.0); pos.append(r['pos'])
        pw = r.get('pw', {}); vp = r.get('vpath', [])
        for k in range(1, len(vp) + 1):
            v = vp[k - 1]
            if v is None: continue
            pwk = pw.get(str(k), pw.get(k))
            if pwk is None:
                pwk = pw.get(str(min(k, 6)), pw.get(min(k, 6), 1.0))
            es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
            if drop_poles and is_pole: es = 0.0
            if es <= 0: continue
            lp.append(L); ty.append(k); val.append(v); wt.append(es); pos.append(r['pos'])
    return (np.array(lp), np.array(ty, float), np.array(val, float), np.array(wt, float), np.array(pos))


def fit_year0(points, tau=TAU, nmin=NMIN, hmin=HMIN, hmax=HMAX, kmin=1, kmax=ND_CURVE_LAST):
    """2-D NW fit read at the year-0 slice. Non-median (weighted mean). derive_pvc2.fit_year0,
    verbatim except that the grid stops at the national curve's last pick -- the domain change is
    the RULING (there is no price for pick 70), not a method change."""
    lp, ty, val, wt, _ = points
    t0 = (ty == 0)
    lp0 = lp[t0]
    tw = wt * np.exp(-ty / tau)
    grid = list(range(kmin, kmax + 1))
    raw, effn = [], []
    for p in grid:
        Lp = np.log(p)
        h = hmin
        while h < hmax:
            if np.sum(np.exp(-0.5 * ((lp0 - Lp) / h) ** 2)) >= nmin: break
            h += 0.02
        W = np.exp(-0.5 * ((lp - Lp) / h) ** 2) * tw
        raw.append(float(np.sum(W * val) / np.sum(W)))
        effn.append(float(np.sum(np.exp(-0.5 * ((lp0 - Lp) / h) ** 2))))
    return grid, np.array(raw), np.array(effn)


def monotone_strict(grid, raw, effn):
    """PAVA non-increasing (weighted by eff-n) then strict-descent epsilon; pin(1)=PIN1.
    derive_pvc2.monotone_strict, verbatim."""
    fit = pava_ni(raw, effn).copy()
    fit[0] = PIN1
    EPS = 1e-3
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS: fit[i] = fit[i - 1] - EPS
    ic = [int(round(x)) for x in fit]
    ic[0] = PIN1
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]: ic[i] = ic[i - 1] - 1
    return ic


# =================================================================================================
# THE OBSERVED FIT — what each fit ACTUALLY consumed, recorded as it consumes it.
# -------------------------------------------------------------------------------------------------
# #217 shipped a check that re-implemented the builders' filter inside the selftest and asserted on
# its own copy. It could not fail: the seam broke the exclusion at two real call sites and the suite
# stayed green both times. The instrument that replaced it observes the ACTUAL row list each site
# sampled. This registry is that instrument, extended to the thing it still could not see.
#
# TWO KINDS, AND THE SECOND IS THE POINT:
#   'sample'  — the rows a fit consumed directly. A sampled-rows check sees this.
#   'pooling' — the population an AGGREGATE blended into that fit was computed over. A sampled-rows
#               check is BLIND to this. The priors blend w*posfit + (1-w)*pool with w <= 0.6, so at
#               least 40% of every prior is the pooled term; compute that term over the combined
#               population and the other population is inside every prior, while every sampled row
#               stays clean and the check reads green. That is the defect this half exists to catch.
#
# It records references to the caller's own list. It observes; it does not copy, filter or recompute.
# =================================================================================================
_FIT_OBS = {}

def observe(site, kind, rows):
    """Register what a fit consumed, and return it unchanged."""
    assert kind in ('sample', 'pooling'), kind
    _FIT_OBS.setdefault(site, {})[kind] = rows
    return rows

FIT_SITES = ('nd_curve', 'pool_level', 'priors_ND_1_64', 'priors_POOL')


# =================================================================================================
# THE SEPARATION. Every population selector is here, in one place, so the check can quote it.
# =================================================================================================
def is_nd_curve_row(r):
    """A national draftee on the national curve. The ND fit's population, and nothing else."""
    return r['type'] == 'ND' and not r['is_pool']

def is_pool_row(r):
    """The RULED pool: ND 65+, all rookie draft, pre-season draft, every pickless mechanism.
    SSP and MSD are IN (valued at the pool) and tracked separately so they can split out later."""
    return bool(r['is_pool'])

def nd_population(recs):
    return [r for r in recs if is_nd_curve_row(r) and r['pick'] and YR_LO <= r['year'] <= YR_HI and r['v0']]

def pool_population(recs):
    return [r for r in recs if is_pool_row(r) and YR_LO <= r['year'] <= YR_HI]

def old_combined_population(recs):
    """The PRE-SPLIT population: 'in-curve' = ND/RD at any pick. Used ONLY to produce the
    before/after comparison the directive requires. Never feeds a shipped value."""
    return [r for r in recs if r['incurve'] and r['pick'] and YR_LO <= r['year'] <= YR_HI and r['v0']]


# =================================================================================================
# REALISED OUTCOMES. The pool's level comes from these, never from v0.
# =================================================================================================
def best_n_avg(r, n=BEST_N, qual=QUAL_GAMES):
    """The bust-priors target: best-n season average over seasons with >= qual games.
    A player who never established one is entered as 0.0 -- THAT ZERO IS THE SURVIVORSHIP FIX.
    Dropping him is what produces a level set by survivors."""
    a = sorted([s['avg'] for s in r.get('seasons', []) if s['games'] >= qual], reverse=True)[:n]
    return float(np.mean(a)) if a else 0.0

def never_established(r, qual=QUAL_GAMES):
    return not any(s['games'] >= qual for s in r.get('seasons', []))

def realised_scar(r):
    """The realised outcome IN CURVE CURRENCY: the evidence-weighted mean of the walk-forward
    as-of values (vpath), i.e. the EVIDENCE END of the same R1 construction the curve uses --
    with a never-established player entered at 0.0.

    Why the evidence end alone, when the ND curve uses both ends: Addendum 1 §C DIRECTS it. The
    entry end is v0, a function of (pos, age band, pick) that carries no information about whether
    a player ever played, and the pool's own figures prove what happens when it sets a level --
    never-played 618.31 sits ABOVE played 553.12. This is a DIRECTED difference from the ND fit,
    disclosed, not a method the seat chose."""
    if never_established(r): return 0.0
    pw = r.get('pw', {}); vp = r.get('vpath', [])
    num = den = 0.0
    for k in range(1, len(vp) + 1):
        v = vp[k - 1]
        if v is None: continue
        pwk = pw.get(str(k), pw.get(k))
        if pwk is None: pwk = pw.get(str(min(k, 6)), pw.get(min(k, 6), 1.0))
        es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
        if es <= 0: continue
        # NO time-kernel here. exp(-t/tau) exists in the curve fit to centre the 2-D surface on the
        # YEAR-0 SLICE; the pool has no year-0 slice to read (there is no ordering and no entry
        # anchor), so every evidence year carries its own evidence share and nothing else.
        num += es * v; den += es
    return float(num / den) if den > 0 else 0.0


# =================================================================================================
# THE PRIORS. Same mechanism (register v509), each fit POOLING WITHIN ITS OWN POPULATION.
# =================================================================================================
def fit_priors(rows, label, pickgrid, pooling_rows=None):
    """The recovered priors recipe, unchanged:
         target    = best-3 season avg over >=6-game seasons, never-established at 0.0
         estimator = IsotonicRegression(increasing=False, out_of_bounds='clip') of target on pick
         fitted TWICE -- once POOLED ACROSS POSITIONS, once PER POSITION
         blended     w*posfit + (1-w)*pool,  w = min(n_pos/200, 1.0) * 0.6

    THE POOLED-ACROSS-POSITIONS FIT IS COMPUTED OVER `rows` AND NOTHING ELSE. That is the owner's
    ruling of 2026-07-28: each fit pools within its own population. Passing the combined population
    here is the contamination the reverse-direction check exists to catch -- it would not change a
    single sampled row, only the (1-w) >= 40% pooled term blended into every prior.

    The *0.6 ceiling and the increasing=False plateau behaviour are KEPT and REPORTED (Addendum 1
    §A). They are the old system's low-sample handling; replacing them would be a different model."""
    site = 'priors_' + label
    # THE POOLED-ACROSS-POSITIONS TERM. Defaults to `rows` — the fit's own population — which is the
    # owner's ruling. `pooling_rows` exists ONLY so the non-vacuity harness can cross it and prove
    # the check fails; no production path passes it.
    prows = rows if pooling_rows is None else pooling_rows
    observe(site, 'sample', rows)
    observe(site, 'pooling', prows)

    tgt = np.array([best_n_avg(r) for r in rows], dtype=float)
    pks = np.array([min(max(int(r['pick'] or 70), 1), 70) for r in rows], dtype=float)
    if len(rows) < 2:
        return None
    ptgt = np.array([best_n_avg(r) for r in prows], dtype=float)
    ppks = np.array([min(max(int(r['pick'] or 70), 1), 70) for r in prows], dtype=float)
    pooled = IsotonicRegression(increasing=False, out_of_bounds='clip').fit(ppks, ptgt)
    pool_pred = pooled.predict(np.array(pickgrid, dtype=float))
    out = {}; wts = {}; ns = {}
    for g in POSITIONS:
        idx = [i for i, r in enumerate(rows) if r['pos'] == g]
        n_pos = len(idx); ns[g] = n_pos
        w = min(n_pos / PRIOR_N_REF, 1.0) * PRIOR_CEIL
        wts[g] = w
        if n_pos >= 2:
            pf = IsotonicRegression(increasing=False, out_of_bounds='clip').fit(pks[idx], tgt[idx])
            pos_pred = pf.predict(np.array(pickgrid, dtype=float))
        else:
            pos_pred = pool_pred
        out[g] = list(map(float, w * pos_pred + (1.0 - w) * pool_pred))
    return dict(label=label, grid=list(pickgrid), pooled=list(map(float, pool_pred)),
                by_pos=out, w=wts, n_by_pos=ns, n_rows=len(rows),
                pooling_population=label)   # STAMPED: which population the pooled term came from


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT + '/derived_split.json')
    ap.add_argument('--break-site', default=None, choices=[None] + list(FIT_SITES),
                    help='NON-VACUITY HARNESS ONLY: cross this site\'s population and prove the '
                         'check fails by name. Never a production path.')
    ap.add_argument('--break-kind', default='pooling', choices=['sample', 'pooling'],
                    help='cross the SAMPLE (a sampled-rows check sees this) or the POOLING term '
                         '(a sampled-rows check is blind to this).')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    BS, BK = args.break_site, args.break_kind

    blob = json.load(open(PER))
    meta = blob['meta']; recs = blob['recs']

    ND   = nd_population(recs)
    POOL = pool_population(recs)
    OLDC = old_combined_population(recs)

    # ---------- (A) THE ND 1-64 CURVE, ND ROWS ONLY -----------------------------------------
    nd_sample = OLDC if (BS == 'nd_curve' and BK == 'sample') else ND
    observe('nd_curve', 'sample', nd_sample)
    # The curve fit's aggregate is the kernel's own per-pick neighbourhood, drawn from the SAME
    # list it samples — pooling population and sample are one object here, so crossing one crosses
    # both. Registered separately anyway so the check treats every site uniformly.
    observe('nd_curve', 'pooling', OLDC if (BS == 'nd_curve' and BK == 'pooling') else nd_sample)
    ND = nd_sample
    pts_nd = build_points(ND)
    grid, raw, effn = fit_year0(pts_nd)
    curve_after = monotone_strict(grid, raw, effn)

    # ---------- (A') THE SAME FIT ON THE PRE-SPLIT POPULATION -- the before/after ------------
    # Not a candidate. It exists so the directive's "before and after the exclusion" comparison
    # is a measurement rather than an assertion, and so a failure to move is VISIBLE.
    pts_old = build_points(OLDC)
    grid_o, raw_o, effn_o = fit_year0(pts_old)
    curve_before = monotone_strict(grid_o, raw_o, effn_o)

    # ---------- (B) THE POOL'S LEVEL, ONE VALUE PER POSITION --------------------------------
    # No isotonic step: order of selection carries no value inside the pool, so there is no
    # ordering to fit. One number per position and the position layer (iso_corr) applies it.
    pool_sample = (POOL + [r for r in recs if is_nd_curve_row(r) and YR_LO <= r['year'] <= YR_HI]) \
                  if (BS == 'pool_level' and BK == 'sample') else POOL
    observe('pool_level', 'sample', pool_sample)
    # The pool's per-position levels are means over the pool's OWN rows. The cross-position
    # aggregate (the all-pool level, and the fallback any thin position would take) is computed
    # over that same population — within-population, per the owner's ruling.
    observe('pool_level', 'pooling',
            (POOL + [r for r in recs if is_nd_curve_row(r) and YR_LO <= r['year'] <= YR_HI])
            if (BS == 'pool_level' and BK == 'pooling') else pool_sample)
    POOL = pool_sample

    pool_by_pos = {}
    for g in POSITIONS:
        rows = [r for r in POOL if r['pos'] == g]
        if not rows: continue
        ne = [r for r in rows if never_established(r)]
        scar = [realised_scar(r) for r in rows]
        prod = [best_n_avg(r) for r in rows]
        pool_by_pos[g] = dict(
            n=len(rows), never_established=len(ne),
            never_established_pct=round(100.0 * len(ne) / len(rows), 1),
            level_scar=round(float(np.mean(scar)), 1),
            level_production=round(float(np.mean(prod)), 2),
            # the pedigree quantity, carried ONLY so the report can name which is which
            mean_v0_DO_NOT_USE_AS_LEVEL=round(float(np.mean([r['v0'] for r in rows])), 2))
    # SSP and MSD valued at the pool but TRACKED SEPARATELY (they become their own pools later)
    tracked = {}
    for t in ('SSP', 'MSD'):
        rows = [r for r in POOL if r['type'] == t]
        if not rows: continue
        tracked[t] = dict(n=len(rows), never_established=sum(1 for r in rows if never_established(r)),
                          level_scar=round(float(np.mean([realised_scar(r) for r in rows])), 1),
                          level_production=round(float(np.mean([best_n_avg(r) for r in rows])), 2),
                          by_pos={g: dict(n=sum(1 for r in rows if r['pos'] == g),
                                          level_scar=round(float(np.mean([realised_scar(r) for r in rows if r['pos'] == g])), 1))
                                  for g in POSITIONS if any(r['pos'] == g for r in rows)})

    # the pool inversion, restated on THIS store and THIS surface
    played    = [r for r in POOL if not never_established(r)]
    neverest  = [r for r in POOL if never_established(r)]
    inversion = dict(
        n_pool=len(POOL), n_played=len(played), n_never=len(neverest),
        mean_v0_all=round(float(np.mean([r['v0'] for r in POOL])), 2),
        mean_v0_played=round(float(np.mean([r['v0'] for r in played])), 2),
        mean_v0_never=round(float(np.mean([r['v0'] for r in neverest])), 2),
        realised_scar_played=round(float(np.mean([realised_scar(r) for r in played])), 1),
        realised_scar_never=round(float(np.mean([realised_scar(r) for r in neverest])), 1))

    # ---------- (C) THE PRIORS, EACH POOLING WITHIN ITS OWN POPULATION ----------------------
    nd_prior_rows   = [r for r in recs if is_nd_curve_row(r) and r['pick']
                       and PRIOR_LO <= r['year'] <= PRIOR_HI]
    pool_prior_rows = [r for r in recs if is_pool_row(r) and PRIOR_LO <= r['year'] <= PRIOR_HI]
    combined_prior_rows = nd_prior_rows + pool_prior_rows
    priors_nd   = fit_priors(nd_prior_rows,   'ND_1_64', list(range(1, ND_CURVE_LAST + 1)),
                             pooling_rows=(combined_prior_rows if (BS == 'priors_ND_1_64' and BK == 'pooling') else None))
    if BS == 'priors_ND_1_64' and BK == 'sample':
        priors_nd = fit_priors(combined_prior_rows, 'ND_1_64', list(range(1, ND_CURVE_LAST + 1)))
    priors_pool = fit_priors(pool_prior_rows, 'POOL', [65],
                             pooling_rows=(combined_prior_rows if (BS == 'priors_POOL' and BK == 'pooling') else None))
    if BS == 'priors_POOL' and BK == 'sample':
        priors_pool = fit_priors(combined_prior_rows, 'POOL', [65])

    # ---------- (D) THE SAME-FOOTING COMPARISON ---------------------------------------------
    # The pool's level is a REALISED-outcome average with never-established at 0.0. The ND curve
    # is an ENTRY-ANCHOR ladder (its year-0 slice is dominated by v0). Those are different
    # footings, and putting 300-odd beside 570-odd invites exactly the category error the seam
    # committed comparing 575.9 against 544. So the national curve's realised outcome is measured
    # HERE on the IDENTICAL instrument, and the report shows both. No bridge, no pick-equivalent:
    # two numbers on one footing, and the reader does the comparing.
    nd_win = [r for r in recs if is_nd_curve_row(r) and YR_LO <= r['year'] <= YR_HI]
    same_footing = dict(
        pool=dict(n=len(POOL), never=sum(1 for r in POOL if never_established(r)),
                  realised_scar=round(float(np.mean([realised_scar(r) for r in POOL])), 1),
                  production=round(float(np.mean([best_n_avg(r) for r in POOL])), 2)),
        nd_1_64=dict(n=len(nd_win), never=sum(1 for r in nd_win if never_established(r)),
                     realised_scar=round(float(np.mean([realised_scar(r) for r in nd_win])), 1),
                     production=round(float(np.mean([best_n_avg(r) for r in nd_win])), 2)),
        nd_by_pick_band={})
    for lo, hi in ((1, 10), (11, 20), (21, 40), (41, 54), (55, 64)):
        rows = [r for r in nd_win if lo <= r['pick'] <= hi]
        if rows:
            same_footing['nd_by_pick_band']['%d-%d' % (lo, hi)] = dict(
                n=len(rows), never=sum(1 for r in rows if never_established(r)),
                realised_scar=round(float(np.mean([realised_scar(r) for r in rows])), 1),
                production=round(float(np.mean([best_n_avg(r) for r in rows])), 2))

    out = dict(
        meta=dict(store_md5=meta['store_md5'], v0surf_sig=meta['v0surf_sig'],
                  v0surf_frozen=meta['v0surf_frozen'], surface='FROZEN' if meta['v0surf_frozen'] else 'REFIT',
                  tau=TAU, nmin=NMIN, pw_floor=PW_FLOOR, pin1=PIN1,
                  window_curve=[YR_LO, YR_HI], window_priors=[PRIOR_LO, PRIOR_HI],
                  construction='R1_composed_pathway (derive_pvc2.py), method unchanged',
                  domain='1-%d (national draft curve). Selections past %d are NOT on the curve.'
                         % (ND_CURVE_LAST, ND_CURVE_LAST)),
        populations=dict(
            nd_fit_rows=len(ND), pool_rows=len(POOL), old_combined_rows=len(OLDC),
            nd_by_pos=Counter(r['pos'] for r in ND),
            pool_by_type=Counter(r['type'] for r in POOL)),
        curve_after=curve_after, curve_before=curve_before,
        curve_raw_after=[round(float(x), 2) for x in raw],
        effn_after=[round(float(x), 1) for x in effn],
        pool_level=pool_by_pos, pool_tracked_separately=tracked, pool_inversion=inversion,
        same_footing=same_footing,
        priors_nd=priors_nd, priors_pool=priors_pool,
        # THE OBSERVED POPULATIONS — what each fit actually consumed, by key, sample AND pooling
        # term. The check reads THIS. It never re-derives the selectors above.
        fit_observations={site: {kind: sorted(set(r['key'] or r['player'] for r in rows))
                                 for kind, rows in kinds.items()}
                          for site, kinds in _FIT_OBS.items()},
        broke=dict(site=BS, kind=BK) if BS else None)

    json.dump(out, open(args.out, 'w'), indent=1, default=lambda o: dict(o) if isinstance(o, Counter) else str(o))

    # ---------- report ----------------------------------------------------------------------
    print("STORE %s   surface %s (%s)" % (meta['store_md5'], out['meta']['surface'], meta['v0surf_sig'][:8]))
    print("ND fit rows        : %d   (national draftees, picks 1-%d, %d-%d)" % (len(ND), ND_CURVE_LAST, YR_LO, YR_HI))
    print("pre-split rows     : %d   (the old 'in-curve' ND/RD population, for the before/after only)" % len(OLDC))
    print("ruled pool rows    : %d" % len(POOL))
    print()
    print("%-6s %10s %10s %9s" % ('pick', 'BEFORE', 'AFTER', 'delta'))
    for k in [1] + list(range(55, 65)):
        b, a = curve_before[k - 1], curve_after[k - 1]
        print("%-6d %10d %10d %9d" % (k, b, a, a - b))
    print()
    print("POOL LEVEL, one value per position (realised outcomes; never-established entered as 0.0)")
    print("%-9s %6s %8s %12s %12s %14s" % ('pos', 'n', 'never', 'SCAR', 'production', 'meanV0(NOT level)'))
    for g in POSITIONS:
        d = pool_by_pos.get(g)
        if not d: continue
        print("%-9s %6d %8d %12.1f %12.2f %14.2f"
              % (g, d['n'], d['never_established'], d['level_scar'], d['level_production'],
                 d['mean_v0_DO_NOT_USE_AS_LEVEL']))
    print()
    print("THE INVERSION, restated on store %s / frozen surface:" % meta['store_md5'])
    print("  mean v0  all %.2f (n=%d) | played %.2f (n=%d) | NEVER-played %.2f (n=%d)  <- pedigree, inverted"
          % (inversion['mean_v0_all'], inversion['n_pool'], inversion['mean_v0_played'], inversion['n_played'],
             inversion['mean_v0_never'], inversion['n_never']))
    print("  realised SCAR  played %.1f | never-played %.1f  <- outcomes, not inverted"
          % (inversion['realised_scar_played'], inversion['realised_scar_never']))
    print()
    print("PRIORS blend weight w = min(n_pos/200,1)*0.6  -- KEPT (Addendum 1 A), reported not fixed")
    for g in POSITIONS:
        print("  %-9s n=%4d  w=%.3f  %s" % (g, priors_nd['n_by_pos'][g], priors_nd['w'][g],
              'CEILING BINDS' if priors_nd['n_by_pos'][g] >= PRIOR_N_REF else 'below n=200'))
    print("wrote %s" % args.out)


if __name__ == '__main__':
    main()
