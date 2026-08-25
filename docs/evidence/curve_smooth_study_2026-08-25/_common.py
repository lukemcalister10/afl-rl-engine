#!/usr/bin/env python3
"""Shared machinery for the SMOOTHING-PASS CANDIDATE seat.  READ-ONLY on the repo.

Everything load-bearing here is LIFTED from the estate's own committed files, by source text where
the estate itself lifts by source text.  Engine bytes touched: 0.  Repo bytes touched: 0.
"""
import os, sys, json, math, collections, hashlib
import numpy as np

ROOT = '/home/user/afl-rl-engine'
O28 = os.path.join(ROOT, 'docs/evidence/grace_adoption_2026-08-13')
IN = os.path.join(O28, 'inputs')
OUT = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/curve_smooth'
sys.path.insert(0, IN)

import harness_pvc_REPINNED_pass3 as HP      # SHIPPED aggregator: kernel_raw + NMIN/HMIN/HMAX/RANGES
import o26b_loclin as LL                     # 26B-C2 local-linear estimator

# ---- the SHIPPED weighted PAVA, lifted by source text exactly as o28_derive.py does --------------
_PB = os.path.join(ROOT, 'engine', 'forward_valuation', 'par_build.py')
_src = open(_PB).read().split('\ndef _pava(')[1].split('\ndef ')[0]
_PAVA_SRC = 'def _pava(' + _src
PAVA_MD5 = hashlib.md5(_PAVA_SRC.encode()).hexdigest()
_ns = {'np': np}
exec(_PAVA_SRC, _ns)
SHIPPED_PAVA = _ns['_pava']

# ---- the L-SMOOTH moving-average half, LIFTED BY SOURCE TEXT from the modernized bust table ------
# docs/evidence/bust_prior_rederivation_2026-08-24/build_bust_prior.py :: smooth_curve, L62-68.
# Only the MA lines are lifted; the recipe's non-increasing re-projection stage is supplied by
# RULING C's SHIPPED weighted PAVA downstream (PREREG deviation D1).
_BUST = os.path.join(ROOT, 'docs/evidence/bust_prior_rederivation_2026-08-24/build_bust_prior.py')
_bs = open(_BUST).read().split('def smooth_curve(iso, picks):')[1].split('\ndef ')[0]
_MA_LINES = [l for l in _bs.split('\n') if ('np.ones' in l or 'ypad' in l or 'ysm' in l)]
MA_SRC = '\n'.join(l.strip() for l in _MA_LINES)
MA_MD5 = hashlib.md5(MA_SRC.encode()).hexdigest()


def l_smooth_ma(y, width=5):
    """The 5-point CENTERED moving average with edge-replicate padding, verbatim from
    build_bust_prior.py::smooth_curve.  Generalised only in `width` for the declared ablation;
    width=5 reproduces the lifted lines exactly."""
    y = np.asarray(y, float)
    half = width // 2
    k = np.ones(width) / float(width)
    ypad = np.concatenate([[y[0]] * half, y, [y[-1]] * half])
    return np.convolve(ypad, k, mode='valid')


# ==================================================================================================
# THE INPUTS (all serialised; nothing re-derived from the store)
# ==================================================================================================
L2 = json.load(open(os.path.join(IN, 'LAYER2.json')))
D0 = json.load(open(os.path.join(IN, 'DERIVE.json')))
L1 = json.load(open(os.path.join(IN, 'layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}
ATTR = L2['attribution']
FM = L2['force_majeure']
GA = L2['grace_a']
K_SHRINK = int(D0['pool']['K'])
PIN1 = 3000.0
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']

V2 = json.load(open(os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')))
CURVE_SHIPPED = {int(k): float(v) for k, v in V2['curve'].items()}
SHARE = {g: {int(k): float(v) for k, v in V2['nd_v0']['share'][g].items()} for g in POSN}
POSV_SHIPPED = {g: {int(k): float(v) for k, v in V2['nd_v0']['posv'][g].items()} for g in POSN}
CRED_W = {g: {int(k): float(v) for k, v in V2['nd_v0']['head_shrink_31f']['credibility_w'][g].items()}
          for g in POSN}
R30 = json.load(open(os.path.join(ROOT, 'docs/evidence/one_machinery_2026-08-14/V0REFIT30B.json')))
POSV_RAW = {g: {int(k): float(v) for k, v in R30['posv_in'][g].items()} for g in POSN}

DERIVE28 = json.load(open(os.path.join(O28, 'DERIVE28.json')))

# ---- RULING B seam constants, carried from o28_derive.py -----------------------------------------
NORM_LO, NORM_HI = 4, 48
ZONE_NORTH_LIMIT = 50


def smoothstep(t):
    return 3.0 * t * t - 2.0 * t * t * t


def hybrid_boundary(ll, wm, picks, end=None):
    """o28_derive.py::hybrid_boundary, carried verbatim except that the blend denominator is the
    DOMAIN ENDPOINT rather than the literal 64 (PREREG §2.2).  With picks=1..64 and end=64 this is
    byte-for-byte the ORDER-28 behaviour."""
    end = end if end is not None else picks[-1]
    d = {p: (ll[i] / wm[i] - 1.0) if wm[i] else float('nan') for i, p in enumerate(picks)}
    normsample = sorted(abs(d[p]) for p in picks if NORM_LO <= p <= NORM_HI)
    nu = normsample[min(len(normsample) - 1, int(0.90 * len(normsample)))]
    zone = []
    for p in reversed(picks):
        if abs(d[p]) > nu:
            zone.append(p)
        else:
            break
    zone = sorted(zone)
    truncated = False
    if zone and zone[0] < ZONE_NORTH_LIMIT:
        zone = [p for p in zone if p >= ZONE_NORTH_LIMIT]
        truncated = True
    out, meth, wts = [], [], []
    if not zone:
        return (list(ll), ['LL'] * len(picks), [0.0] * len(picks),
                dict(nu=nu, zone=[], seam=None, truncated=truncated))
    p0 = zone[0] - 1
    for i, p in enumerate(picks):
        if p not in zone:
            out.append(ll[i]); meth.append('LL'); wts.append(0.0)
        else:
            w = smoothstep((p - p0) / float(end - p0))
            out.append((1 - w) * ll[i] + w * wm[i])
            meth.append('WM' if w >= 1.0 - 1e-15 else 'blend')
            wts.append(w)
    return out, meth, wts, dict(nu=nu, zone=zone, seam=p0, truncated=truncated)


# ==================================================================================================
# THE FIT POPULATIONS
# ==================================================================================================
def nd_rows_1_64():
    """The ORDER-28 ND fit population, EXACTLY as o28_derive.py builds it."""
    rows = [dict(key=k, pick=ATTR[k]['pick'], value=GA[k]['total'], pos=E[k]['position_group'])
            for k in L2['fit_nd_keys']]
    assert not (set(FM['excluded_keys']) & set(L2['fit_nd_keys'])), "26B-C1 (a) breached"
    return rows


def nd_rows_65_70():
    """The picks 65-70 entrants, under the SAME window rule as the ND fit (2004-2021), force-majeure
    keys excluded.  Today these sit in fit_pool_keys as the ND>64 pathway; for candidate X they enter
    the curve fit and LEAVE that pathway (LAYER2.json::force_majeure.mechanics precedent)."""
    fm = set(FM['excluded_keys'])
    out = []
    for k, a in ATTR.items():
        if a.get('mechanism') != 'ND>64' or k in fm:
            continue
        p = a.get('pick')
        if not p or not (65 <= p <= 70):
            continue
        e = E.get(k)
        if not e or e.get('entry_year') is None or not (2004 <= e['entry_year'] <= 2021):
            continue
        out.append(dict(key=k, pick=p, value=GA[k]['total'], pos=e['position_group']))
    return sorted(out, key=lambda r: (r['pick'], r['key']))


# ==================================================================================================
# THE CURVE DERIVATION, parametric in the smoothing step and the domain
# ==================================================================================================
def derive_curve(nd, picks, smooth=None, end=None, boundary='hybrid'):
    """raw cohorts -> LOCLIN -> HYBRID -> [L-SMOOTH] -> weighted PAVA -> anchor pick1=3000.

    smooth=None reproduces ORDER 28 exactly.  smooth=int applies the L-SMOOTH MA of that width
    between the hybrid stage and the monotone projection (PREREG §1.1)."""
    end = end if end is not None else picks[-1]
    nper = collections.Counter(r['pick'] for r in nd)
    rawmean = {p: (sum(r['value'] for r in nd if r['pick'] == p) / nper[p]) if nper[p] else 0.0
               for p in picks}
    ll, effn, _dg = LL.kernel_loclin(nd, picks, HP.NMIN, HP.HMIN, HP.HMAX)
    wm, _e2 = HP.kernel_raw(nd, picks)
    if boundary == 'hybrid':
        hyb, meth, blendw, zinfo = hybrid_boundary(ll, wm, picks, end=end)
    elif boundary == 'loclin':
        hyb, meth, blendw = list(ll), ['LL'] * len(picks), [0.0] * len(picks)
        zinfo = dict(nu=None, zone=[], seam=None, truncated=False)
    else:
        hyb, meth, blendw = list(wm), ['WM'] * len(picks), [1.0] * len(picks)
        zinfo = dict(nu=None, zone=[], seam=None, truncated=False)

    # ---- THE ONE ADDED STEP -----------------------------------------------------------------
    if smooth:
        pre = [float(x) for x in l_smooth_ma(hyb, smooth)]
    else:
        pre = list(hyb)

    wts_n = [float(nper[p]) for p in picks]
    ascents = [(picks[i], picks[i + 1], pre[i + 1] - pre[i])
               for i in range(len(picks) - 1) if pre[i + 1] > pre[i]]
    post = [float(x) for x in SHIPPED_PAVA(pre, wts_n, increasing=False)]

    # ---- the ORDER-28 asserts, verbatim -------------------------------------------------------
    a1 = not (abs(post[0] - post[1]) < 1e-12 and abs(pre[0] - pre[1]) > 1e-12)
    sw_pre = math.fsum(w * v for w, v in zip(wts_n, pre))
    sw_post = math.fsum(w * v for w, v in zip(wts_n, post))
    a2 = abs(sw_post / sw_pre - 1.0) if sw_pre else 0.0
    a3 = all(post[i] >= post[i + 1] - 1e-12 for i in range(len(post) - 1))

    head = post[0]
    af = PIN1 / head
    allin = {p: post[i] * af for i, p in enumerate(picks)}
    return dict(picks=list(picks), head=head, anchor_factor=af, premium=af - 1.0,
                allin=allin, ll=list(ll), wm=list(wm), hyb=list(hyb), pre=pre, post=post,
                meth=meth, blendw=blendw, zinfo=zinfo, nper=dict(nper), rawmean=rawmean,
                effn=list(effn), ascents=ascents, wts_n=wts_n,
                asserts=dict(A1=a1, A2=a2, A3=a3), sw_pre=sw_pre, sw_post=sw_post)


def blocks_of(vals, tol=1e-9):
    """Contiguous runs of equal value (the PAVA plateaus), as index ranges into `vals`."""
    runs = []
    i = 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and abs(vals[j + 1] - vals[i]) <= tol:
            j += 1
        if j > i:
            runs.append((i, j))
        i = j + 1
    return runs
