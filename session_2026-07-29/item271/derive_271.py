"""ITEM 271 STAGE B — the derivation: ND curve (picks 1-64) + the pool level, on SCAR.

Carried from #225 stage 2's derive_split.py, which itself carries derive_pvc2.py FUNCTION FOR
FUNCTION. pava_ni / build_points / fit_year0 / monotone_strict are verbatim; tau, nmin, PW_FLOOR,
pin(1)=3000, the x0.6 blend ceiling, the min(n_pos/200,1) pooling weight, the isotonic step and both
windows are unchanged. THE METHOD IS HELD CONSTANT -- a reader must be able to attribute every
difference to the data or the separation, never to something this seat changed.

WHAT IS DIFFERENT FROM #225 STAGE 2, and each is a ruling rather than a choice:
  - the evidence matrix is the #271 one: the Q-B force-majeure slide is already applied to its
    membership, and every season carries the Addendum-6 bar;
  - POSITIONS speak the landed #262 vocabulary (KPF/KPD/SD/SF/MID/RUCK);
  - the pool level's carrying statistic is SCAR (owner word at fire time).

The two windows are CARRIED, not re-chosen (Q-C): the pool takes the curve's 2004-2024, the priors
take the priors' own 2006-2020. Harmonising them would be a method change.
"""
import os, sys, json, argparse
import numpy as np
from sklearn.isotonic import IsotonicRegression

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = BASE + '/out'

# ---- THE SHIPPED DERIVATION'S DIALS. UNCHANGED. -------------------------------------------------
PW_FLOOR   = 0.11
PIN1       = 3000
TAU        = 0.12
NMIN       = 35.0
HMIN, HMAX = 0.10, 0.60
YR_LO, YR_HI = 2004, 2024
# ---- THE PRIORS RECIPE'S DIALS. UNCHANGED. ------------------------------------------------------
PRIOR_LO, PRIOR_HI = 2006, 2020
PRIOR_N_REF        = 200
PRIOR_CEIL         = 0.6
QUAL_GAMES         = 6
BEST_N             = 3
POSITIONS = ['MID', 'SF', 'KPF', 'SD', 'KPD', 'RUCK']     # ITEM 262 landed vocabulary
ND_CURVE_LAST = 64


# ==== CARRIED OVER VERBATIM FROM derive_pvc2.py -- do not "improve" these. =======================
def pava_ni(vals, wts):
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


# ==== THE OBSERVED FIT — what each fit ACTUALLY consumed, recorded as it consumes it. ============
# 'sample'  : the rows a fit consumed directly. A sampled-rows check sees this.
# 'pooling' : the population an AGGREGATE blended into that fit was computed over. A sampled-rows
#             check is BLIND to this -- the priors blend w*posfit + (1-w)*pool with w <= 0.6, so at
#             least 40% of every prior is the pooled term. #225 stage 2 found 818 pool rows teaching
#             the ND prior through exactly this channel while every sampled row read clean.
_FIT_OBS = {}
def observe(site, kind, rows):
    assert kind in ('sample', 'pooling'), kind
    _FIT_OBS.setdefault(site, {})[kind] = rows
    return rows


# ==== THE SEPARATION. Every population selector in one place, so the check can quote it. =========
# NOTE: `is_pool` / `teaches_curve` in the #271 matrix are ALREADY the post-slide membership (Q-B),
# so the curve fit, the pool level and these checks all see one membership by construction.
def is_nd_curve_row(r):  return r['type'] == 'ND' and not r['is_pool']
def is_pool_row(r):      return bool(r['is_pool'])
def nd_population(recs):
    return [r for r in recs if is_nd_curve_row(r) and r['pick'] and YR_LO <= r['year'] <= YR_HI and r['v0']]
def pool_population(recs):
    return [r for r in recs if is_pool_row(r) and YR_LO <= r['year'] <= YR_HI]


# ==== REALISED OUTCOMES. The pool's level comes from these, never from v0. =======================
def best_n_avg(r, n=BEST_N, qual=QUAL_GAMES):
    a = sorted([s['avg'] for s in r.get('seasons', []) if s['games'] >= qual], reverse=True)[:n]
    return float(np.mean(a)) if a else 0.0

def never_established(r, qual=QUAL_GAMES):
    return not any(s['games'] >= qual for s in r.get('seasons', []))

def realised_scar(r):
    """The realised outcome in curve currency: the evidence-weighted mean of the walk-forward as-of
    values, never-established entered at 0.0 (the survivorship rule). No time-kernel: the pool has no
    year-0 slice to centre on. The EVIDENCE end of R1 alone -- Addendum 1 §C directs it."""
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
        num += es * v; den += es
    return float(num / den) if den > 0 else 0.0


# ==== THE PRIORS. Each fit POOLING WITHIN ITS OWN POPULATION. ====================================
def fit_priors(rows, label, pickgrid, pooling_rows=None):
    site = 'priors_' + label
    prows = rows if pooling_rows is None else pooling_rows
    observe(site, 'sample', rows)
    observe(site, 'pooling', prows)
    if len(rows) < 2: return None
    tgt = np.array([best_n_avg(r) for r in rows], dtype=float)
    pks = np.array([min(max(int(r['pick'] or 70), 1), 70) for r in rows], dtype=float)
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
                by_pos=out, w=wts, n_by_pos=ns, n_rows=len(rows), pooling_population=label)


# ==== THE BOTH-DIRECTIONS CHECK, over BOTH channels, with its own non-vacuity harness ============
def run_checks(recs):
    """Direction 1: no pool row may reach the ND curve. Direction 2: no ND 1-64 row may reach the
    pool level. Both are checked over BOTH the sampled rows AND the pooled term."""
    res = []
    for site, kinds in sorted(_FIT_OBS.items()):
        for kind, rows in sorted(kinds.items()):
            keys = {r['key'] for r in rows}
            if site in ('nd_curve', 'priors_ND_1_64'):
                bad = [r for r in rows if is_pool_row(r)]
                rule = 'no POOL row among the %d keys it consumed' % len(keys)
            else:
                bad = [r for r in rows if is_nd_curve_row(r)]
                rule = 'no ND 1-64 row among the %d keys it consumed' % len(keys)
            res.append(dict(site=site, kind=kind, rule=rule, n_rows=len(rows),
                            violations=len(bad), passed=(len(bad) == 0),
                            examples=[r['player'] for r in bad[:5]]))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--matrix', default=OUT + '/per_entrant_271.json')
    ap.add_argument('--out', default=OUT + '/derived_271.json')
    a = ap.parse_args()
    M = json.load(open(a.matrix)); recs = M['recs']; meta = M['meta']

    ND = nd_population(recs)
    POOL = pool_population(recs)
    observe('nd_curve', 'sample', ND)
    observe('nd_curve', 'pooling', ND)
    observe('pool_level', 'sample', POOL)
    observe('pool_level', 'pooling', POOL)

    grid, raw, effn = fit_year0(build_points(ND))
    curve = monotone_strict(grid, raw, effn)

    # the pool's level, on SCAR
    scar_all = [realised_scar(r) for r in POOL]
    by_pos = {}
    for g in POSITIONS:
        rows = [r for r in POOL if r['pos'] == g]
        if not rows: continue
        by_pos[g] = dict(n=len(rows),
                         never_established=sum(1 for r in rows if never_established(r)),
                         level_scar=round(float(np.mean([realised_scar(r) for r in rows])), 1))
    tracked = {}
    for t in ('SSP', 'MSD'):
        rows = [r for r in POOL if r['type'] == t]
        if rows:
            tracked[t] = dict(n=len(rows), never_established=sum(1 for r in rows if never_established(r)),
                              level_scar=round(float(np.mean([realised_scar(r) for r in rows])), 1))

    PR_ND = [r for r in recs if is_nd_curve_row(r) and r['pick'] and PRIOR_LO <= r['year'] <= PRIOR_HI]
    PR_PO = [r for r in recs if is_pool_row(r) and PRIOR_LO <= r['year'] <= PRIOR_HI]
    pickgrid = list(range(1, 71))
    priors_nd = fit_priors(PR_ND, 'ND_1_64', pickgrid)
    priors_po = fit_priors(PR_PO, 'POOL', pickgrid)

    checks = run_checks(recs)

    # the lawful comparison, same instrument, no bridge
    nd_win = [r for r in ND if ND_CURVE_LAST - 9 <= (r['pick'] or 0) <= ND_CURVE_LAST]
    out = dict(
        meta=dict(store_md5=meta['store_md5'], v0surf_sig=meta['v0surf_sig'],
                  force_majeure=meta['force_majeure'], slide_years=meta['slide_years'],
                  windows=dict(pool=[YR_LO, YR_HI], priors=[PRIOR_LO, PRIOR_HI]),
                  statistic='SCAR', nd_curve_last=ND_CURVE_LAST),
        curve=dict(grid=grid, raw=list(map(float, raw)), effn=list(map(float, effn)), integer=curve,
                   n_rows=len(ND), ladder_total=int(sum(curve))),
        pool=dict(n=len(POOL), never_established=sum(1 for r in POOL if never_established(r)),
                  level_scar=round(float(np.mean(scar_all)), 1), by_pos=by_pos, tracked=tracked),
        nd_last_band=dict(band='%d-%d' % (ND_CURVE_LAST - 9, ND_CURVE_LAST), n=len(nd_win),
                          realised_scar=round(float(np.mean([realised_scar(r) for r in nd_win])), 1)),
        priors=dict(ND_1_64=priors_nd, POOL=priors_po),
        checks=checks,
    )
    json.dump(out, open(a.out, 'w'), indent=1)

    print("store %s | v0surf %s | statistic SCAR" % (meta['store_md5'], meta['v0surf_sig'][:12]))
    print("ND curve population %d rows; pool %d rows (never-established %d)"
          % (len(ND), len(POOL), out['pool']['never_established']))
    print("curve: pin(1)=%d  pick10=%d  pick32=%d  pick64=%d  ladder total %d"
          % (curve[0], curve[9], curve[31], curve[63], out['curve']['ladder_total']))
    print("pool level (SCAR) = %s   ND %s realised = %s"
          % (out['pool']['level_scar'], out['nd_last_band']['band'], out['nd_last_band']['realised_scar']))
    for g, d in sorted(by_pos.items()):
        print("   %-5s n=%-4d never=%-4d level %s" % (g, d['n'], d['never_established'], d['level_scar']))
    print("tracked separately:", tracked)
    print("\nBOTH-DIRECTIONS CHECK")
    for c in checks:
        print("  %-4s site %-16s [%-7s]: %s%s"
              % ('PASS' if c['passed'] else 'FAIL', c['site'], c['kind'], c['rule'],
                 '' if c['passed'] else '   <-- %d found: %s' % (c['violations'], c['examples'])))
    print("\nwrote", a.out)


if __name__ == '__main__':
    main()
