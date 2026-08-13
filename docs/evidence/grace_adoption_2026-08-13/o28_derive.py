#!/usr/bin/env python3
"""ORDER 28 -- STEP 2, THE RE-DERIVATION ON THE GRACE-A BASIS.

THE CANDIDATE LANDING CURVE AND v0s.  **NOTHING LANDS.**

Three owner rulings compose here, and the order they compose in is fixed in the preregs, not here:

  RULING A (grace-A, #334 c.5276077959)   -- the scoring basis. Layer-2 grace-A scores, Reading O,
      G_O = 2 in the CURVE k-convention (k = season_year - entry_year, k=1 the first played season).
      Read from LAYER2.json, computed on build/delivered-value and copied verbatim into inputs/.
      The board side of the SAME rule is the RL_GRACE dial in rl_model.py::disc_factor; the identity
      gate (o28_gate.py) is what proves the two sides speak one language.

  RULING B (asymmetric boundary, same comment) -- loclin holds NORTH and INTERIOR; the SOUTH tail
      reverts toward the shipped weighted-mean reading. Seam rule fixed in PREREG_ORDER28.md §2.

  RULING C (monotone, #334 c.5276216984 + addendum-2) -- the SHIPPED weighted PAVA, non-increasing,
      weights = per-pick cohort n, applied AFTER loclin+hybrid, then re-anchored. Positional curves
      are NOT monotonized (owner lean); their ascents are disclosed as data.

      raw cohorts -> LOCLIN -> HYBRID south boundary -> weighted PAVA -> anchor pick1=3000

Everything else is the operative 26B-C2 basis, unchanged: the 26B-C1 force-majeure whole-draft slide
and its assert, the Gaussian kernel and bandwidth-growth rule, window tiers, games weighting, K=15,
bars, positions, tails.  V5 is OFF and is not an arm here.

  usage:  python3 o28_derive.py   ->  DERIVE28.json / DERIVE28_out.txt
"""
import os, sys, json, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
IN = os.path.join(HERE, 'inputs')
sys.path.insert(0, IN)
import harness_pvc_REPINNED_pass3 as HP          # the SHIPPED aggregator: kernel_raw + NMIN/HMIN/HMAX/RANGES
import o26b_loclin as LL                          # the 26B-C2 local-linear estimator
import numpy as np, hashlib
# THE SHIPPED WEIGHTED PAVA, par_build.py::_pava (line 584).  It is LIFTED BY SOURCE TEXT rather than
# imported, because `import par_build` drags rl_model and the whole par machinery (and its pins) into a
# derivation harness -- the same reason o26b_loclin.py cites par_build's loclin instead of importing it.
# The lift is EXACT: the function's own source lines are exec'd verbatim, and the extracted text is
# md5'd and printed so the reuse is auditable. ENGINE BYTES TOUCHED BY THIS FILE: 0.
_PB = os.path.join(ROOT, 'engine', 'forward_valuation', 'par_build.py')
_src = open(_PB).read().split('\ndef _pava(')[1].split('\ndef ')[0]
_PAVA_SRC = 'def _pava(' + _src
_PAVA_MD5 = hashlib.md5(_PAVA_SRC.encode()).hexdigest()
_ns = {'np': np}
exec(_PAVA_SRC, _ns)
SHIPPED_PAVA = _ns['_pava']

L2 = json.load(open(os.path.join(IN, 'LAYER2.json')))
D0 = json.load(open(os.path.join(IN, 'DERIVE.json')))
L1 = json.load(open(os.path.join(IN, 'layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}
ATTR = L2['attribution']; FM = L2['force_majeure']; GRACE = L2['grace_cfg']
M = json.load(open(os.path.join(IN, 'per_entrant_O25R4.json'))); R = M['recs']
NUM = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])
PVC = {int(k): float(v) for k, v in json.load(open(ROOT + '/engine/rl_after/rl_app_data.json'))['PVC'].items()}
V26 = json.load(open(os.path.join(IN, 'VARIANTS_out.txt'))) if False else None

PICKS = list(range(1, 65))
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
K_SHRINK = int(D0['pool']['K']); PIN1 = 3000.0
BANDS = HP.RANGES
HEADP = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]

_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
LEVI = {k: int(float(v)) for k, v in dict(CUR['signed_flat']).items()}
LEVI['ND65+'] = int(float(CUR['signed_nd65_plus']['measured_k15']))
for k, v in dict(CUR['signed_rd_positional']).items(): LEVI['RD:' + k] = int(float(v))

# 26B-V grace-A reference values, transcribed from VARIANTS_out.txt (inputs/, md5 pinned) for the
# ANCHOR-INVARIANCE check. They are compared against, never used in the derivation.
REF_26BV = dict(head=3191.2, anchor_factor=0.9401, premium=-0.060,
                allin={1: 3000, 2: 2668, 3: 2569, 5: 1804, 7: 1243, 10: 1312, 15: 803, 20: 859,
                       30: 607, 40: 479, 50: 274, 64: 106},
                agg_der_prn=0.3477, agg_der_anch=0.8950)


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def anchor_of(r):
    if r.get('is_pool_engine'):
        d = ('RD:' + r['pos']) if r.get('type') == 'RD' else ('ND65+' if r.get('type') == 'ND'
                                                              else r.get('type'))
        if d in LEVI: return LEVI[d] * NUM
    return float(r['v0'])


def arm_of(r):
    a = ATTR.get(r['key'])
    return a['mechanism'] if a else None


POOLROWS_M = [r for r in R if arm_of(r) in POOLM and (r.get('v0') or 0) > 0 and cohort(r) is not None]
NDROWS_M = [r for r in R if arm_of(r) == 'ND 1-64' and (r.get('v0') or 0) > 0]

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


# ==================================================================================================
# RULING B -- THE SEAM RULE, exactly as fixed in PREREG_ORDER28.md §2
# ==================================================================================================
NORM_LO, NORM_HI = 4, 48          # the interior-norm window, fixed in prereg
ZONE_NORTH_LIMIT = 50             # the zone may not reach north of this (prereg guard)


def smoothstep(t):
    return 3.0 * t * t - 2.0 * t * t * t


def hybrid_boundary(ll, wm, picks):
    """LL north+interior, reverting to WM in the south tail, smoothstep blend, no cliff at the seam."""
    d = {p: (ll[i] / wm[i] - 1.0) if wm[i] else float('nan') for i, p in enumerate(picks)}
    normsample = sorted(abs(d[p]) for p in picks if NORM_LO <= p <= NORM_HI)
    nu = normsample[min(len(normsample) - 1, int(0.90 * len(normsample)))]
    zone = []
    for p in reversed(picks):
        if abs(d[p]) > nu: zone.append(p)
        else: break
    zone = sorted(zone)
    truncated = False
    if zone and zone[0] < ZONE_NORTH_LIMIT:
        zone = [p for p in zone if p >= ZONE_NORTH_LIMIT]; truncated = True
    out, meth, wts = [], [], []
    if not zone:
        for i, p in enumerate(picks):
            out.append(ll[i]); meth.append('LL'); wts.append(0.0)
        return out, meth, wts, dict(nu=nu, zone=[], seam=None, truncated=truncated, dev=d)
    p0 = zone[0] - 1
    for i, p in enumerate(picks):
        if p not in zone:
            out.append(ll[i]); meth.append('LL'); wts.append(0.0)
        else:
            t = (p - p0) / float(64 - p0)
            w = smoothstep(t)
            out.append((1 - w) * ll[i] + w * wm[i])
            meth.append('WM' if w >= 1.0 - 1e-15 else 'blend')
            wts.append(w)
    return out, meth, wts, dict(nu=nu, zone=zone, seam=p0, truncated=truncated, dev=d)


# ==================================================================================================
# THE DERIVATION, PARAMETRIC IN THE SCORING
# ==================================================================================================
def derive(SC, boundary='hybrid', monotone=True):
    nd = [dict(key=k, pick=ATTR[k]['pick'], value=SC[k]['total'], pos=E[k]['position_group'])
          for k in L2['fit_nd_keys']]
    assert not (set(FM['excluded_keys']) & set(L2['fit_nd_keys'])), "26B-C1 (a) breached"
    nper = collections.Counter(r['pick'] for r in nd)
    rawmean = {p: (sum(r['value'] for r in nd if r['pick'] == p) / nper[p]) if nper[p] else 0.0
               for p in PICKS}
    ll, effn, dg = LL.kernel_loclin(nd, PICKS, HP.NMIN, HP.HMIN, HP.HMAX)   # 26B-C2
    wm, _e2 = HP.kernel_raw(nd, PICKS)                                       # the SHIPPED aggregator
    if boundary == 'hybrid':
        hyb, meth, wts, zinfo = hybrid_boundary(ll, wm, PICKS)
    elif boundary == 'loclin':
        hyb, meth, wts = list(ll), ['LL'] * 64, [0.0] * 64
        zinfo = dict(nu=None, zone=[], seam=None, truncated=False, dev={})
    else:
        hyb, meth, wts = list(wm), ['WM'] * 64, [1.0] * 64
        zinfo = dict(nu=None, zone=[], seam=None, truncated=False, dev={})

    # ---- RULING C: the SHIPPED weighted PAVA, non-increasing, weights = per-pick cohort n -------
    wts_n = [float(nper[p]) for p in PICKS]
    pre = list(hyb)
    ascents = [(PICKS[i], PICKS[i + 1], pre[i + 1] - pre[i])
               for i in range(len(PICKS) - 1) if pre[i + 1] > pre[i]]
    if monotone:
        post = [float(x) for x in SHIPPED_PAVA(pre, wts_n, increasing=False)]
        # A1 -- PAVA must not pool pick 1 with pick 2
        a1 = not (abs(post[0] - post[1]) < 1e-12 and abs(pre[0] - pre[1]) > 1e-12)
        # A2 -- weighted-sum conservation
        sw_pre = math.fsum(w * v for w, v in zip(wts_n, pre))
        sw_post = math.fsum(w * v for w, v in zip(wts_n, post))
        a2 = abs(sw_post / sw_pre - 1.0) if sw_pre else 0.0
        a3 = all(post[i] >= post[i + 1] - 1e-12 for i in range(len(post) - 1))
        assert a1, "A1 BREACHED: PAVA pooled pick 1 -- HALT (never silently rescale the anchor)"
        assert a2 < 1e-12, "A2 BREACHED: weighted sum not conserved: %.3e" % a2
        assert a3, "A3 BREACHED: PAVA output is not non-increasing"
    else:
        post = list(pre); sw_pre = sw_post = math.fsum(w * v for w, v in zip(wts_n, pre))
        a1, a2, a3 = True, 0.0, all(post[i] >= post[i + 1] - 1e-12 for i in range(len(post) - 1))

    head = post[0]; af = PIN1 / head
    allin = {p: post[i] * af for i, p in enumerate(PICKS)}
    allin_pre = {p: pre[i] * af for i, p in enumerate(PICKS)}
    ll_anch = {p: ll[i] * af for i, p in enumerate(PICKS)}
    wm_anch = {p: wm[i] * af for i, p in enumerate(PICKS)}

    # ---- positional relativities: CONTINUOUS PER PICK (addendum-2: machinery unchanged) --------
    share, rawpos = {}, {}
    posrows = {g: [r for r in nd if r['pos'] == g] for g in POSN}
    for g in POSN:
        ind = [dict(key=r['key'], pick=r['pick'], value=(1.0 if r['pos'] == g else 0.0)) for r in nd]
        s, _ = HP.kernel_raw(ind, PICKS)
        share[g] = {p: s[i] for i, p in enumerate(PICKS)}
    for p in PICKS:
        t = sum(share[g][p] for g in POSN)
        for g in POSN: share[g][p] = share[g][p] / t if t else 0.0
    for g in POSN:
        nm = min(HP.NMIN, max(8.0, len(posrows[g]) / 4.0))
        v, _e, _d = LL.kernel_loclin(posrows[g], PICKS, nm, HP.HMIN, HP.HMAX)
        rawpos[g] = {p: v[i] for i, p in enumerate(PICKS)}
    posv = {g: {} for g in POSN}
    posv_pre = {g: {} for g in POSN}
    for p in PICKS:
        nrm = sum(share[g][p] * rawpos[g][p] for g in POSN)
        for g in POSN:
            posv[g][p] = allin[p] * rawpos[g][p] / nrm if nrm else allin[p]
            posv_pre[g][p] = allin_pre[p] * rawpos[g][p] / nrm if nrm else allin_pre[p]
    # A4 -- Ruling 13 reconciliation, re-run AFTER the monotone all-in is substituted
    recon = max(abs(sum(share[g][p] * posv[g][p] for g in POSN) / allin[p] - 1.0) for p in PICKS)
    assert recon < 1e-12, "A4 / RULING 13 RECONCILIATION BREACHED: %.3e" % recon
    relat = {g: {p: posv[g][p] / allin[p] for p in PICKS} for g in POSN}
    pos_ascents = {g: [(p, p + 1, relat[g][p + 1] - relat[g][p])
                       for p in PICKS[:-1] if posv[g][p + 1] > posv[g][p]] for g in POSN}
    bands = {}
    for lo, hi in BANDS:
        ps = [p for p in PICKS if lo <= p <= hi]
        a = sum(allin[p] for p in ps) / len(ps)
        bands['%d-%d' % (lo, hi)] = {g: (sum(posv[g][p] for p in ps) / len(ps)) / a for g in POSN}

    # ---- pool ladders (unchanged machinery; they do not read the ND curve except for equivalents)
    pool = [dict(key=k, mech=ATTR[k]['mechanism'], pos=E[k]['position_group'], value=SC[k]['total'])
            for k in L2['fit_pool_keys']]
    ap = sum(r['value'] for r in pool) / len(pool)
    lens = {}
    for g in POSN:
        sub = [r for r in pool if r['pos'] == g]
        lens[g] = (sum(r['value'] for r in sub) / len(sub) / ap) if sub and ap else 1.0
    path = {}
    for m in POOLM:
        sub = [r for r in pool if r['mech'] == m]
        n = len(sub); a = (sum(r['value'] for r in sub) / n) if n else 0.0
        w = n / float(n + K_SHRINK)
        path[m] = dict(n=n, raw=a, shrunk=w * a + (1 - w) * ap)
    cells = {}
    for m in POOLM:
        for g in POSN:
            sub = [r for r in pool if r['mech'] == m and r['pos'] == g]
            n = len(sub); w = n / float(n + K_SHRINK)
            own = (sum(r['value'] for r in sub) / n) if n else 0.0
            cells[(m, g)] = w * own + (1 - w) * path[m]['shrunk'] * lens[g]

    def nd_equiv(v):
        a = v * af
        if a >= allin[1]: return '<1'
        for p in PICKS:
            if allin[p] <= a: return str(p)
        return '>64'

    def dv0(r):
        a = ATTR.get(r['key'])
        if a is None or a.get('excluded'): return None
        if a['mechanism'] == 'ND 1-64' and a['pick'] and 1 <= a['pick'] <= 64:
            return allin[a['pick']] * NUM
        c = cells.get((a['mechanism'], (E.get(r['key']) or {}).get('position_group')))
        return (c * af * NUM) if c is not None else None

    cmp_ = []
    for r in POOLROWS_M:
        d = dv0(r)
        if d is None: continue
        cmp_.append((arm_of(r), (E.get(r['key']) or {}).get('position_group'), d, float(r['v0']),
                     anchor_of(r)))
    agg_prn = sum(c[2] for c in cmp_) / sum(c[3] for c in cmp_)
    agg_anc = sum(c[2] for c in cmp_) / sum(c[4] for c in cmp_)
    bypos = {}
    for g in POSN:
        sub = [c for c in cmp_ if c[1] == g]
        if sub:
            bypos[g] = dict(n=len(sub), der_prn=q([c[2] / c[3] for c in sub], .5),
                            der_anch=q([c[2] / c[4] for c in sub], .5))
    bypath = {}
    for m in POOLM:
        sub = [c for c in cmp_ if c[0] == m]
        if sub:
            bypath[m] = dict(n=len(sub), derived=sum(c[2] for c in sub) / len(sub),
                             der_prn=q([c[2] / c[3] for c in sub], .5),
                             der_anch=q([c[2] / c[4] for c in sub], .5))
    return dict(head=head, anchor_factor=af, premium=af - 1.0, allin=allin, allin_pre=allin_pre,
                ll_anch=ll_anch, wm_anch=wm_anch, ll=ll, wm=wm, pre=pre, post=post,
                meth=meth, blendw=wts, zinfo=zinfo, nper=dict(nper), rawmean=rawmean,
                ascents=ascents, asserts=dict(A1=a1, A2=a2, A3=a3, A4=recon),
                sw_pre=sw_pre, sw_post=sw_post,
                bands=bands, recon=recon, relat=relat, posv=posv, posv_pre=posv_pre,
                share=share, pos_ascents=pos_ascents,
                pathways=path, all_pool=ap, lens=lens,
                nd_equiv={m: nd_equiv(path[m]['shrunk']) for m in POOLM},
                anchored_path={m: path[m]['shrunk'] * af for m in POOLM},
                cells={'%s|%s' % k: v for k, v in cells.items()},
                agg_der_prn=agg_prn, agg_der_anch=agg_anc, n_cmp=len(cmp_),
                by_pos=bypos, by_path=bypath,
                nd_mean=sum(r['value'] for r in nd) / len(nd),
                derived_v0={r['key']: dv0(r) for r in POOLROWS_M + NDROWS_M if dv0(r) is not None})


GA = L2['grace_a']
CAND = derive(GA, 'hybrid', True)                 # THE CANDIDATE LANDING CURVE
NOMONO = derive(GA, 'hybrid', False)              # the hybrid before the monotone step
PURE_LL = derive(GA, 'loclin', False)             # 26B-V's grace-A curve, reproduced here
PURE_WM = derive(GA, 'wm', False)                 # the weighted-mean reading, for the tail comparison
FLAT = derive(L2['base'], 'loclin', False)        # the operative flat-14 C2 basis, for context

# ==================================================================================================
P("=" * 130)
P("ORDER 28  --  STEP 2, THE RE-DERIVATION ON THE GRACE-A BASIS WITH THE ASYMMETRIC BOUNDARY")
P("             AND THE MONOTONE STEP.   THE CANDIDATE LANDING CURVE AND v0s.   NOTHING LANDS.")
P("=" * 130)
P("  rulings: grace-A everywhere (#334 c.5276077959) | asymmetric south boundary (same) |")
P("           the monotone ruling (#334 c.5276216984, as corrected by addendum-2)")
P("  basis:   LAYER2.json grace-A, Reading O -- %s" % GRACE['reading_O'].split('.')[0])
P("  pipeline: raw cohorts -> LOCLIN (26B-C2) -> HYBRID south boundary -> weighted PAVA -> anchor 3000")
P("  estimators, all reused and cited, none reinvented:")
P("    LOCLIN  o26b_loclin.kernel_loclin  (par_build.py::loclin algebra on the shipped kernel)")
P("    WM      harness_pvc_REPINNED_pass3.kernel_raw  (the SHIPPED year-zero aggregator)")
P("    PAVA    par_build.py::_pava(increasing=False)  (the SHIPPED weighted pool-adjacent-violators,")
P("            lifted by SOURCE TEXT, md5 %s -- engine bytes touched: 0)" % _PAVA_MD5)
P("  V5 is OFF and is not an arm.  K=%d.  NMIN=%.0f HMIN=%.2f HMAX=%.2f" % (K_SHRINK, HP.NMIN, HP.HMIN, HP.HMAX))
P()
P("  26B-C1 (force-majeure whole-draft slide) ASSERT (a): the two excluded keys appear in NO")
P("  ND or pool fit input .......................................................... PASS")
P("     excluded: %s" % ", ".join(FM['excluded_keys']))
P()

# -------------------------------------------------------------------------------- the seam
Z = CAND['zinfo']
P("-" * 130)
P("1.  THE SOUTH SEAM  (RULING B) -- the zone, disclosed")
P("-" * 130)
P("  interior norm  nu = p90 |LL/WM - 1| over picks %d-%d  =  %.6f  (%.3f%%)"
  % (NORM_LO, NORM_HI, Z['nu'], 100 * Z['nu']))
P("  SOUTH TAIL ZONE  = picks %s   (length %d)   truncated at %d: %s"
  % (("%d-%d" % (Z['zone'][0], Z['zone'][-1])) if Z['zone'] else 'EMPTY', len(Z['zone']),
     ZONE_NORTH_LIMIT, Z['truncated']))
P("  SEAM PICK p0 = %s   (the last pure-loclin pick; HYB(p0) == LL(p0) exactly)" % Z['seam'])
P("  blend  w(p) = smoothstep((p-p0)/(64-p0)),  HYB = (1-w)*LL + w*WM;  w(p0)=0, w(64)=1")
P()
P("  %-6s %10s %10s %10s %8s %10s %8s" % ('pick', 'LL', 'WM', 'LL/WM-1', 'w', 'HYB', 'method'))
for p in PICKS:
    i = p - 1
    if p < (Z['seam'] or 64) - 2 and p not in (1, 2, 3, 40, 45): continue
    P("  %-6d %10.1f %10.1f %+9.3f%% %8.4f %10.1f %8s"
      % (p, CAND['ll'][i], CAND['wm'][i], 100 * (CAND['ll'][i] / CAND['wm'][i] - 1),
         CAND['blendw'][i], CAND['pre'][i], CAND['meth'][i]))
_seam = Z['seam'] or 1
_par = max(max(abs(CAND['ll'][i + 1] / CAND['ll'][i] - 1) for i in range(_seam - 1, 63)),
           max(abs(CAND['wm'][i + 1] / CAND['wm'][i] - 1) for i in range(_seam - 1, 63)))
_hybstep = max(abs(CAND['pre'][i + 1] / CAND['pre'][i] - 1) for i in range(_seam - 1, 63))
P()
P("  NO-CLIFF ASSERT (prereg §2.7): max adjacent relative step over [p0,64]")
P("     hybrid %.4f   worst parent %.4f   ->  %s"
  % (_hybstep, _par, "PASS (hybrid no rougher than either parent)" if _hybstep <= _par + 1e-12
     else "FAIL -- RETURN TO OWNER"))
P("  monotone over [p0,64] BEFORE the PAVA step: %s"
  % all(CAND['pre'][i] >= CAND['pre'][i + 1] for i in range(_seam - 1, 63)))

# -------------------------------------------------------------------------------- the monotone step
P()
P("-" * 130)
P("2.  THE MONOTONE STEP  (RULING C) -- every removed ascent disclosed, and the conservation ledger")
P("-" * 130)
P("  estimator: par_build.py::_pava(y, w, increasing=False), weights = per-pick cohort n")
P("  ASCENDING ADJACENT PAIRS in the pre-PAVA hybrid curve: %d" % len(CAND['ascents']))
P("  %-9s %11s %11s %11s %11s   %11s %11s   %11s" %
  ('pair', 'pre A', 'pre B', 'ascent', 'ascent(anch)', 'raw mean A', 'raw mean B', 'PAVA value'))
for (pa, pb, sz) in CAND['ascents']:
    P("  %-9s %11.1f %11.1f %+11.1f %+11.1f   %11.1f %11.1f   %11.1f"
      % ('%d->%d' % (pa, pb), CAND['pre'][pa - 1], CAND['pre'][pb - 1], sz, sz * CAND['anchor_factor'],
         CAND['rawmean'][pa], CAND['rawmean'][pb], CAND['post'][pa - 1]))
P()
P("  ASSERTS")
P("    A1  PAVA did not pool pick 1 with pick 2 ..................... %s" % ('PASS' if CAND['asserts']['A1'] else 'HALT'))
P("    A2  weighted-sum conservation |post/pre - 1| = %.3e ......... %s"
  % (CAND['asserts']['A2'], 'PASS' if CAND['asserts']['A2'] < 1e-12 else 'HALT'))
P("    A3  output non-increasing over picks 1-64 ................... %s" % ('PASS' if CAND['asserts']['A3'] else 'HALT'))
P("    A4  Ruling-13 reconciliation, post-monotone = %.3e ......... %s"
  % (CAND['asserts']['A4'], 'PASS' if CAND['asserts']['A4'] < 1e-12 else 'HALT'))
P()
P("  THE CONSERVATION LEDGER")
_plain_pre = math.fsum(CAND['pre']); _plain_post = math.fsum(CAND['post'])
P("    1. weighted   SUM w*value   pre %14.4f   post %14.4f   drift %+0.3e  (exact by construction)"
  % (CAND['sw_pre'], CAND['sw_post'], CAND['sw_post'] / CAND['sw_pre'] - 1))
P("    2. plain      SUM value     pre %14.4f   post %14.4f   drift %+7.4f%%"
  % (_plain_pre, _plain_post, 100 * (_plain_post / _plain_pre - 1)))
P("    3. anchor     head          pre %14.4f   post %14.4f   factor pre %.4f post %.4f"
  % (NOMONO['head'], CAND['head'], NOMONO['anchor_factor'], CAND['anchor_factor']))
P("       (A1 forbids PAVA from reaching pick 1, so these MUST be identical -- they are: %s)"
  % (abs(CAND['head'] - NOMONO['head']) < 1e-12))
P("    4. per-position SUM posv(p) over picks 1-64, pre vs post the renormalisation onto the")
P("       monotone all-in:")
P("       %-6s %14s %14s %10s" % ('pos', 'pre', 'post', 'drift'))
for g in POSN:
    a = math.fsum(NOMONO['posv'][g][p] for p in PICKS)
    b = math.fsum(CAND['posv'][g][p] for p in PICKS)
    P("       %-6s %14.1f %14.1f %+9.4f%%" % (g, a, b, 100 * (b / a - 1)))
_alla = math.fsum(NOMONO['allin'][p] for p in PICKS); _allb = math.fsum(CAND['allin'][p] for p in PICKS)
P("       %-6s %14.1f %14.1f %+9.4f%%" % ('ALL-IN', _alla, _allb, 100 * (_allb / _alla - 1)))

# -------------------------------------------------------------------------------- the curve
P()
P("-" * 130)
P("3.  THE FULL CURVE  --  three-way table, tail zone marked, per-pick method disclosed")
P("-" * 130)
P("  ANCHORED at pick 1 = 3000.  'CANDIDATE' = loclin -> hybrid -> PAVA -> anchor.")
P("  %-5s %5s %10s %10s %10s %10s %10s %10s %9s %8s %s"
  % ('pick', 'n', 'raw mean', 'LOCLIN', 'WM-hybrid', 'pre-PAVA', 'CANDIDATE', 'today PVC',
     'cand/PVC', 'blend w', 'method'))
for p in PICKS:
    i = p - 1
    tag = ' <<< TAIL ZONE' if p in Z['zone'] else (' <<< SEAM' if p == Z['seam'] else '')
    P("  %-5d %5d %10.1f %10.1f %10.1f %10.1f %10.1f %10.0f %9.4f %8.4f %-6s%s"
      % (p, CAND['nper'][p], CAND['rawmean'][p], CAND['ll_anch'][p], CAND['wm_anch'][p],
         CAND['allin_pre'][p], CAND['allin'][p], PVC[p], CAND['allin'][p] / PVC[p],
         CAND['blendw'][i], CAND['meth'][i], tag))
P()
P("  HEADLINE PICKS -- CANDIDATE vs 26B-V grace-A (pure loclin) vs today's PVC")
P("  %-16s %s" % ('pick', "".join("%8d" % p for p in HEADP)))
P("  %-16s %s" % ('CANDIDATE', "".join("%8.0f" % CAND['allin'][p] for p in HEADP)))
P("  %-16s %s" % ('26B-V grace-A', "".join("%8.0f" % PURE_LL['allin'][p] for p in HEADP)))
P("  %-16s %s" % ('  (published)', "".join("%8d" % REF_26BV['allin'][p] for p in HEADP)))
P("  %-16s %s" % ('flat-14 (26B C2)', "".join("%8.0f" % FLAT['allin'][p] for p in HEADP)))
P("  %-16s %s" % ('today PVC', "".join("%8.0f" % PVC[p] for p in HEADP)))
P("  %-16s %s" % ('cand/26B-V', "".join("%8.3f" % (CAND['allin'][p] / PURE_LL['allin'][p]) for p in HEADP)))
P("  %-16s %s" % ('cand/PVC', "".join("%8.3f" % (CAND['allin'][p] / PVC[p]) for p in HEADP)))
_nmax = max(abs(CAND['allin'][p] / PURE_LL['allin'][p] - 1) for p in PICKS if p <= (Z['seam'] or 64))
P()
P("  NORTH/INTERIOR IDENTITY: max |CANDIDATE/26B-V grace-A - 1| over picks 1..p0 = %.3e" % _nmax)
P("     (non-zero only where PAVA removed an interior ascent -- which is RULING C, not the boundary)")

# -------------------------------------------------------------------------------- head/factor/premium
P()
P("-" * 130)
P("4.  HEAD, ANCHOR FACTOR, PREMIUM  --  and the anchor-invariance check (A5)")
P("-" * 130)
P("  %-28s %14s %14s %14s %14s" % ('metric', 'CANDIDATE', '26B-V grace-A', 'published', 'flat-14 C2'))
P("  %-28s %14.1f %14.1f %14.1f %14.1f"
  % ('PRE-ANCHOR HEAD (pick 1)', CAND['head'], PURE_LL['head'], REF_26BV['head'], FLAT['head']))
P("  %-28s %14.4f %14.4f %14.4f %14.4f"
  % ('ANCHOR FACTOR', CAND['anchor_factor'], PURE_LL['anchor_factor'], REF_26BV['anchor_factor'],
     FLAT['anchor_factor']))
P("  %-28s %13.1f%% %13.1f%% %13.1f%% %13.1f%%"
  % ('PICK-vs-PLAYER PREMIUM', 100 * CAND['premium'], 100 * PURE_LL['premium'],
     100 * REF_26BV['premium'], 100 * FLAT['premium']))
P("  %-28s %14.1f %14.1f %14s %14.1f"
  % ('ND cohort mean', CAND['nd_mean'], PURE_LL['nd_mean'], '--', FLAT['nd_mean']))
P("  A5: |CANDIDATE head / 26B-V head - 1| = %.3e   -- the boundary and the monotone step BOTH"
  % abs(CAND['head'] / PURE_LL['head'] - 1))
P("      leave pick 1 alone, so the anchor, the factor and the premium are UNCHANGED.")

# -------------------------------------------------------------------------------- positional
P()
P("-" * 130)
P("5.  POSITIONAL RELATIVITIES  --  THE CONTINUOUS PER-PICK CURVES (addendum-2)")
P("-" * 130)
P("  These are the IMPLEMENTATION. The five-band table below is a SUMMARY OF BAND MEANS of these")
P("  curves and has never been the wiring. Per-position monotonicity is NOT enforced (owner lean:")
P("  a position may legitimately be better than all-in at some parts of the draft and worse at")
P("  others); positional ascents are DISCLOSED as data.")
P()
P("  RELATIVITY  V_pos(pick) / all-in(pick),  EVERY PICK 1-64")
P("  %-5s %9s %9s %9s %9s %9s %9s   %10s" % ('pick', *POSN, 'all-in'))
for p in PICKS:
    P("  %-5d %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f   %10.1f"
      % (p, *[CAND['relat'][g][p] for g in POSN], CAND['allin'][p]))
P()
P("  POSITIONAL v0 (ANCHORED BOARD POINTS), EVERY PICK 1-64")
P("  %-5s %9s %9s %9s %9s %9s %9s   %10s" % ('pick', *POSN, 'all-in'))
for p in PICKS:
    P("  %-5d %9.0f %9.0f %9.0f %9.0f %9.0f %9.0f   %10.1f"
      % (p, *[CAND['posv'][g][p] for g in POSN], CAND['allin'][p]))
P()
P("  SUMMARY MEANS OF THE CONTINUOUS CURVES, BY THE ENGINE'S OWN BOARD BANDS")
P("  (a summary, NOT the implementation)")
P("  band       %s       all-in" % "".join("%10s" % g for g in POSN))
for lo, hi in BANDS:
    ps = [p for p in PICKS if lo <= p <= hi]
    P("  %-9s %s %12.0f" % ('%d-%d' % (lo, hi),
                            "".join("%10.3f" % CAND['bands']['%d-%d' % (lo, hi)][g] for g in POSN),
                            sum(CAND['allin'][p] for p in ps) / len(ps)))
P("  n          %s" % "".join("%10d" % len([r for r in L2['fit_nd_keys']
                                            if E[r]['position_group'] == g]) for g in POSN))
P()
P("  PER-POSITION ASCENTS (adjacent pairs where the positional v0 RISES with a deeper pick)")
P("  DISCLOSED AS DATA -- monotonized NOWHERE.")
for g in POSN:
    asc = CAND['pos_ascents'][g]
    P("    %-5s %2d ascents%s" % (g, len(asc),
                                  ('  at picks ' + ", ".join('%d->%d' % (a, b) for a, b, _ in asc[:14])
                                   + (' ...' if len(asc) > 14 else '')) if asc else ''))
P("  RECONCILIATION LAW (Ruling 13), post-monotone: max |sum_g share*posv / all-in - 1| = %.3e"
  % CAND['recon'])

# -------------------------------------------------------------------------------- pool
P()
P("-" * 130)
P("6.  POOL LADDERS, PATHWAY ALL-INS, ND-PICK EQUIVALENTS AND THE NEW PICK-64 THRESHOLD")
P("-" * 130)
P("  ALL-POOL all-in mean %.1f   K=%d.  The pool ladder does NOT read the ND curve; only the"
  % (CAND['all_pool'], K_SHRINK))
P("  EQUIVALENT PICK LABEL moves when the tail moves.")
P()
P("  THE PICK-64 THRESHOLD")
P("    26B-V grace-A (pure loclin) ........ %8.1f" % PURE_LL['allin'][64])
P("    weighted-mean reading, same anchor . %8.1f" % CAND['wm_anch'][64])
P("    CANDIDATE (hybrid + PAVA) .......... %8.1f   <-- the new threshold" % CAND['allin'][64])
P("    today's PVC at pick 64 ............. %8.0f" % PVC[64])
P("    the owner's '198-class' shorthand is the weighted-mean curve anchored on its OWN head")
P("    (%.1f x %.4f = %.1f). On the RULED loclin head it reads %.1f instead. The difference is"
  % (PURE_WM['head'] / PURE_WM['anchor_factor'] * 0 + CAND['wm'][63], PIN1 / CAND['wm'][0],
     CAND['wm'][63] * PIN1 / CAND['wm'][0], CAND['wm_anch'][64]))
P("    THE ANCHORING, NOT THE ESTIMATOR, and it is disclosed rather than reconciled away.")
P()
P("  %-7s %5s %11s %11s %11s   %10s %10s %10s   %s"
  % ('path', 'n', 'raw all-in', 'shrunk', 'ANCHORED', 'eq CAND', 'eq 26B-V', 'eq flat-14', 'in/out of 64'))
for m in sorted(POOLM, key=lambda x: -CAND['anchored_path'][x]):
    inout = 'INSIDE' if CAND['anchored_path'][m] >= CAND['allin'][64] else 'OUTSIDE'
    P("  %-7s %5d %11.1f %11.1f %11.1f   %10s %10s %10s   %s"
      % (m, CAND['pathways'][m]['n'], CAND['pathways'][m]['raw'], CAND['pathways'][m]['shrunk'],
         CAND['anchored_path'][m], CAND['nd_equiv'][m], PURE_LL['nd_equiv'][m],
         FLAT['nd_equiv'][m], inout))
P()
P("  ALL-POOL POSITIONAL LENS (rung 2)")
P("  %-6s %10s" % ('pos', 'lens'))
for g in POSN: P("  %-6s %10.4f" % (g, CAND['lens'][g]))
P()
P("  POOL POSITIONAL v0 CELLS (anchored board points; pathway x day-0 position, K=15 borrowing)")
P("  %-7s %s" % ('path', "".join("%10s" % g for g in POSN)))
for m in POOLM:
    P("  %-7s %s" % (m, "".join("%10.0f" % (CAND['cells']['%s|%s' % (m, g)] * CAND['anchor_factor'])
                                for g in POSN)))

# -------------------------------------------------------------------------------- aggregates
P()
P("-" * 130)
P("7.  POOLED AGGREGATES AND BOTH INSTRUMENTS")
P("-" * 130)
P("  %-30s %14s %14s %14s" % ('metric', 'CANDIDATE', '26B-V grace-A', 'flat-14 C2'))
P("  %-30s %14.4f %14.4f %14.4f"
  % ('pooled derived/printed', CAND['agg_der_prn'], PURE_LL['agg_der_prn'], FLAT['agg_der_prn']))
P("  %-30s %14.4f %14.4f %14.4f"
  % ('pooled derived/ANCHOR', CAND['agg_der_anch'], PURE_LL['agg_der_anch'], FLAT['agg_der_anch']))
P("  %-30s %14d %14d %14d" % ('n compared', CAND['n_cmp'], PURE_LL['n_cmp'], FLAT['n_cmp']))
P("  PREREG P8: these must be IDENTICAL to 26B-V grace-A (the pool ladder does not read the ND")
P("  curve). |cand/26BV - 1| : printed %.3e   anchor %.3e"
  % (abs(CAND['agg_der_prn'] / PURE_LL['agg_der_prn'] - 1),
     abs(CAND['agg_der_anch'] / PURE_LL['agg_der_anch'] - 1)))
P()
P("  BY DAY-0 POSITION (medians)")
P("  %-6s %10s %10s %10s %10s" % ('pos', 'der/prn C', 'der/prn V', 'der/anc C', 'der/anc V'))
for g in POSN:
    P("  %-6s %10.4f %10.4f %10.4f %10.4f"
      % (g, CAND['by_pos'][g]['der_prn'], PURE_LL['by_pos'][g]['der_prn'],
         CAND['by_pos'][g]['der_anch'], PURE_LL['by_pos'][g]['der_anch']))
P()
P("  BY PATHWAY, derived/ANCHOR (median)")
P("  %-7s %6s %12s %12s %12s" % ('path', 'n', 'CANDIDATE', '26B-V gA', 'flat-14'))
for m in POOLM:
    if m not in CAND['by_path']: continue
    P("  %-7s %6d %12.4f %12.4f %12.4f"
      % (m, CAND['by_path'][m]['n'], CAND['by_path'][m]['der_anch'],
         PURE_LL['by_path'][m]['der_anch'], FLAT['by_path'][m]['der_anch']))

# -------------------------------------------------------------------------------- named rows
P()
P("-" * 130)
P("8.  THE NAMED ROWS ON THE CANDIDATE BASIS")
P("-" * 130)
NAMED = ['willem-duursma', 'callum-moore', 'harrison-ramm', 'vigo-visentini', 'jai-newcombe']
P("  %-18s %-8s %5s %12s %12s %12s %12s"
  % ('key', 'path', 'age', 'deliv f14', 'deliv gA', 'v0 CAND', 'v0 26B-V'))
NAMEDOUT = {}
for k in NAMED:
    e = E[k]; ea = e['entry_age'] or e['entry_age_fallback_if_null']
    NAMEDOUT[k] = dict(age=ea, mech=ATTR[k]['mechanism'], flat=L2['base'][k]['total'],
                       gA=GA[k]['total'], v0_cand=CAND['derived_v0'].get(k),
                       v0_26bv=PURE_LL['derived_v0'].get(k))
    P("  %-18s %-8s %5s %12.1f %12.1f %12s %12s"
      % (k, ATTR[k]['mechanism'], ea, L2['base'][k]['total'], GA[k]['total'],
         ("%.1f" % NAMEDOUT[k]['v0_cand']) if NAMEDOUT[k]['v0_cand'] else 'n/a',
         ("%.1f" % NAMEDOUT[k]['v0_26bv']) if NAMEDOUT[k]['v0_26bv'] else 'n/a'))
P("  willem-duursma is ND pick 1: his DERIVED v0 sits at the north end and CANNOT move under either")
P("  ruling. His BOARD price does move under the dial (step 3) -- the two facts belong together.")

OUT = dict(status='CANDIDATE LANDING CURVE AND v0s -- NOTHING LANDED',
           rulings=dict(grace='#334 c.5276077959', boundary='#334 c.5276077959',
                        monotone='#334 c.5276216984 + addendum-2'),
           seam=dict(nu=Z['nu'], zone=Z['zone'], seam=Z['seam'], truncated=Z['truncated'],
                     nocliff_hybrid=_hybstep, nocliff_worst_parent=_par),
           asserts=CAND['asserts'], ascents=CAND['ascents'],
           conservation=dict(sw_pre=CAND['sw_pre'], sw_post=CAND['sw_post'],
                             plain_pre=_plain_pre, plain_post=_plain_post,
                             head_pre=NOMONO['head'], head_post=CAND['head']),
           candidate={k: CAND[k] for k in ('head', 'anchor_factor', 'premium', 'allin', 'allin_pre',
                                           'll_anch', 'wm_anch', 'bands', 'relat', 'posv', 'share',
                                           'pathways', 'nd_equiv', 'anchored_path', 'cells',
                                           'agg_der_prn', 'agg_der_anch', 'by_pos', 'by_path',
                                           'nd_mean', 'all_pool', 'lens', 'nper', 'rawmean',
                                           'meth', 'blendw', 'pos_ascents', 'recon')},
           ref_26bv_graceA={k: PURE_LL[k] for k in ('head', 'anchor_factor', 'premium', 'allin',
                                                    'nd_equiv', 'anchored_path', 'agg_der_prn',
                                                    'agg_der_anch', 'by_pos', 'by_path')},
           flat14={k: FLAT[k] for k in ('head', 'anchor_factor', 'premium', 'allin')},
           pvc=PVC, named=NAMEDOUT)
json.dump(OUT, open(os.path.join(HERE, 'DERIVE28.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'DERIVE28_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote DERIVE28.json / DERIVE28_out.txt")
