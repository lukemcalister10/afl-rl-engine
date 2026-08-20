#!/usr/bin/env python3
"""ORDER N STEP 2 — WHAT PERFORMANCE-VS-AGE ACTUALLY PREDICTS. READ-ONLY.

The derivation input. It comes from OUTCOMES, never from board prices. The delivered-value ruler is
the house one, reused whole out of docs/evidence/order32_s4_2026-08-17/s4_shootout.py and md5-asserted.

PREREG_N.md section 4 fixes the cohorts, the vantages, the estimands, the bins, the splits and the
falsifiers N5, N6, N7.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_step2.py
"""
import json, math, os, sys, collections
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

SEED, B_BOOT = 32, 2000
AGE_MAX = 22
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


def partial_spear(x, y, z):
    """Spearman of x and y with z partialled out, on ranks (the standard rank-residual method)."""
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    Z = np.column_stack([np.ones(len(rz)), rz])
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    d = math.sqrt((ex ** 2).sum() * (ey ** 2).sum())
    return float((ex * ey).sum() / d) if d > 0 else float('nan')


def ols(y, X):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def cluster_boot(fn, keys, rng, B=B_BOOT):
    """Resample PLAYERS, not rows. Rows from the same player travel together."""
    uk = sorted(set(keys))
    idx_by = collections.defaultdict(list)
    for i, k in enumerate(keys):
        idx_by[k].append(i)
    out = []
    nu = len(uk)
    for _ in range(B):
        pick = rng.integers(0, nu, size=nu)
        idx = []
        for j in pick:
            idx.extend(idx_by[uk[j]])
        v = fn(np.array(idx))
        if v is not None and np.isfinite(v):
            out.append(v)
    if not out:
        return (float('nan'), float('nan'))
    a = np.array(out)
    return (float(np.percentile(a, 5)), float(np.percentile(a, 95)))


P('=' * 118)
P('ORDER N — STEP 2. WHAT PERFORMANCE-VS-AGE PREDICTS ABOUT SUBSEQUENT DELIVERED VALUE')
P('=' * 118)
P('prereg      : PREREG_N.md, pushed at 602d40a')
P('ruler       : the house S4 delivered-value ruler, md5 %s (falsifier N3 clear)' % LB.check_s4_copy())
P('             DV1 = next season. DVREST = discounted sum of every observed later season at 1.14.')
P('             DV5 = the same, capped at five forward seasons, so censoring is equal across vantages.')
P('age bar     : S1 C3, asserted against the engine literal (falsifier N2 clear)')
P('NOTHING HERE READS A BOARD PRICE EXCEPT v0, WHICH IS THE PEDIGREE CONTROL.')
P()

M = LB.load_matrix('OKRULED')

# ---- build the vantage rows -------------------------------------------------------------------------
rowsv = []
excl = collections.Counter()
for k, r in M.items():
    if k in LB.FM:
        excl['force_majeure'] += 1; continue
    if (r.get('year') or 0) < LB.ENTRY_FLOOR:
        excl['pre_2005_entry'] += 1; continue
    if not (float(r.get('v0') or 0) > 0):
        excl['no_v0'] += 1; continue
    sv = LB.season_values(r)
    for N in range(1, 7):
        Y = int(r['year']) + N
        if Y + 1 > LB.LAST_REAL_SEASON:
            excl['future_unobservable'] += 1; continue
        a = LB.age_at(r, Y)
        if a is None or a > AGE_MAX:
            excl['age>%d' % AGE_MAX] += 1; continue
        g = LB.career_games(r, Y)
        if g < 1:
            excl['gameless_at_vantage'] += 1; continue
        if g > 60:
            excl['g>60'] += 1; continue
        ps = LB.perf_surplus(r, Y)
        if ps is None:
            excl['no_PS'] += 1; continue
        dv5 = sum((LB.DISC ** -(t - Y)) * v for t, v in sv.items() if Y < t <= Y + 5)
        rowsv.append(dict(key=k, N=N, Y=Y, g=g, age=a, ps=ps,
                          v0=float(r['v0']), pick=(r.get('pick') if r.get('type') == 'ND' else None),
                          typ=r.get('type'), pos=r.get('pos'),
                          tall=('TALL' if r.get('pos') in LB.TALLPOS else 'SMALL'),
                          band=LB.band_of(r.get('pick') if r.get('type') == 'ND' else None),
                          dv1=LB.dv1(sv, Y), dvrest=LB.dvrest(sv, Y), dv5=dv5,
                          dv5_ok=(Y + 5 <= LB.LAST_REAL_SEASON),
                          gbin=LB.binof(g, LB.G_BINS_2)))

P('COHORT (prereg 2.3 / 4): entrants 2005+, vantages N=1..6, age at vantage <= %d, 1 <= g <= 60,' % AGE_MAX)
P('                          at least one observable future season (vantage year + 1 <= %d).' % LB.LAST_REAL_SEASON)
P('  vantage rows kept: %d   distinct players: %d' % (len(rowsv), len(set(r['key'] for r in rowsv))))
P('  exclusions       : %s' % json.dumps(dict(sorted(excl.items()))))
P('  DEPENDENCE       : a player contributes up to 6 rows. EVERY CI below resamples PLAYERS, not rows.')
P()

# ---- E4 census --------------------------------------------------------------------------------------
P('-' * 118)
P('E4 · THE SURFACE, WITH DISPERSION AND SAMPLE SIZE')
P('-' * 118)
P('%-9s %5s %5s | %7s %7s %7s | %9s %9s %7s | %9s %7s' % (
    'games', 'rows', 'plyrs', 'PS p25', 'PS med', 'PS p75', 'DVREST mn', 'DVREST md', 'zero%', 'DV1 mean', 'zero%'))
CEN = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if not sub: continue
    ps = np.array([r['ps'] for r in sub]); dr = np.array([r['dvrest'] for r in sub])
    d1 = np.array([r['dv1'] for r in sub])
    P('%-9s %5d %5d | %7.2f %7.2f %7.2f | %9.1f %9.1f %6.1f%% | %9.1f %6.1f%%' % (
        b, len(sub), len(set(r['key'] for r in sub)),
        np.percentile(ps, 25), np.median(ps), np.percentile(ps, 75),
        dr.mean(), np.median(dr), 100 * (dr == 0).mean(), d1.mean(), 100 * (d1 == 0).mean()))
    CEN[b] = dict(rows=len(sub), players=len(set(r['key'] for r in sub)),
                  ps_p25=float(np.percentile(ps, 25)), ps_med=float(np.median(ps)),
                  ps_p75=float(np.percentile(ps, 75)), dvrest_mean=float(dr.mean()),
                  dvrest_med=float(np.median(dr)), dvrest_zero=float((dr == 0).mean()),
                  dv1_mean=float(d1.mean()), dv1_zero=float((d1 == 0).mean()))
P()

# ---- E1 / E3 ----------------------------------------------------------------------------------------
P('-' * 118)
P('E1 · RANK ASSOCIATION OF PERFORMANCE SURPLUS WITH SUBSEQUENT DELIVERED VALUE')
P('E3 · AND, ON THE SAME ROWS, PEDIGREE\'S OWN INCREMENTAL POWER')
P('-' * 118)
P('   partial rho(PS, DV | v0) is the number that justifies conditioning the charge on performance.')
P('   partial rho(v0, DV | PS) is the number that justifies letting the prior decay with evidence.')
P('   90%% CIs cluster-bootstrapped on player, %d resamples, seed %d.' % (B_BOOT, SEED))
P()
P('   %-9s %5s | %-30s | %-30s' % ('games', 'rows', 'partial rho(PS, DVREST | v0)', 'partial rho(v0, DVREST | PS)'))
E13 = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if len(sub) < 30:
        P('   %-9s %5d | THIN — not scored' % (b, len(sub))); continue
    ps = np.array([r['ps'] for r in sub]); dv = np.array([r['dvrest'] for r in sub])
    v0 = np.array([r['v0'] for r in sub]); ky = [r['key'] for r in sub]
    a = partial_spear(ps, dv, v0)
    ca = cluster_boot(lambda i: partial_spear(ps[i], dv[i], v0[i]), ky, np.random.default_rng(SEED))
    c = partial_spear(v0, dv, ps)
    cc = cluster_boot(lambda i: partial_spear(v0[i], dv[i], ps[i]), ky, np.random.default_rng(SEED))
    P('   %-9s %5d | %+8.4f  [%+.4f, %+.4f]     | %+8.4f  [%+.4f, %+.4f]' % (
        b, len(sub), a, ca[0], ca[1], c, cc[0], cc[1]))
    E13[b] = dict(n=len(sub), pr_ps=a, ci_ps=ca, pr_v0=c, ci_v0=cc,
                  raw_ps=spear(ps, dv), raw_v0=spear(v0, dv))
P()
P('   raw (unconditional) rank correlations, same bins:')
P('   %-9s | %-12s %-12s | %-12s %-12s' % ('games', 'rho(PS,DVREST)', 'rho(PS,DV1)', 'rho(v0,DVREST)', 'rho(v0,DV1)'))
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if len(sub) < 30: continue
    ps = np.array([r['ps'] for r in sub]); dv = np.array([r['dvrest'] for r in sub])
    d1 = np.array([r['dv1'] for r in sub]); v0 = np.array([r['v0'] for r in sub])
    P('   %-9s | %+12.4f %+12.4f | %+12.4f %+12.4f' % (b, spear(ps, dv), spear(ps, d1), spear(v0, dv), spear(v0, d1)))
P()

# ---- E2 the multiplicative slope --------------------------------------------------------------------
P('-' * 118)
P('E2 · THE MULTIPLICATIVE SLOPE — ln(1 + DV) = a + c*ln(v0) + BETA*PS + vantage-year effects')
P('-' * 118)
P('   BETA is the proportional change in subsequent delivered value per ONE POINT PER GAME of surplus,')
P('   holding pedigree fixed. exp(BETA*20) is the ratio between a row 10 points above his age bar and')
P('   a row 10 points below it. Vantage-year effects absorb the fact that later vantages have fewer')
P('   observable future seasons — a construction choice, stated here, made because censoring is not')
P('   constant across the panel.')
P()
P('   %-9s %5s | %-28s | %8s | %-28s' % ('games', 'rows', 'BETA on DVREST  [90% CI]', 'x(+/-10)', 'BETA on DV1  [90% CI]'))
E2 = {}


def beta_fit(sub, target, i=None):
    s = [sub[j] for j in i] if i is not None else sub
    n = len(s)
    yy = np.log1p(np.array([r[target] for r in s]))
    lv = np.log(np.array([r['v0'] for r in s]))
    pss = np.array([r['ps'] for r in s])
    yrs = sorted(set(r['Y'] for r in s))
    if len(yrs) < 2 or np.ptp(pss) <= 0:
        return None
    D = np.column_stack([np.array([1.0 if r['Y'] == y else 0.0 for r in s]) for y in yrs]
                        + [lv, pss])
    if np.linalg.matrix_rank(D) < D.shape[1]:
        return None
    return float(ols(yy, D)[-1])


for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if len(sub) < 30:
        P('   %-9s %5d | THIN — not scored' % (b, len(sub))); continue
    ky = [r['key'] for r in sub]
    br = beta_fit(sub, 'dvrest')
    cr = cluster_boot(lambda i: beta_fit(sub, 'dvrest', i), ky, np.random.default_rng(SEED))
    b1 = beta_fit(sub, 'dv1')
    c1 = cluster_boot(lambda i: beta_fit(sub, 'dv1', i), ky, np.random.default_rng(SEED))
    P('   %-9s %5d | %+8.5f [%+.5f,%+.5f] | %8.2f | %+8.5f [%+.5f,%+.5f]' % (
        b, len(sub), br, cr[0], cr[1], math.exp(br * 20.0), b1, c1[0], c1[1]))
    E2[b] = dict(n=len(sub), beta_dvrest=br, ci_dvrest=cr, beta_dv1=b1, ci_dv1=c1,
                 ratio_pm10=math.exp(br * 20.0))
# pooled
ky = [r['key'] for r in rowsv]
bp = beta_fit(rowsv, 'dvrest')
cp = cluster_boot(lambda i: beta_fit(rowsv, 'dvrest', i), ky, np.random.default_rng(SEED))
P('   %-9s %5d | %+8.5f [%+.5f,%+.5f] | %8.2f |' % ('POOLED', len(rowsv), bp, cp[0], cp[1], math.exp(bp * 20.0)))
E2['POOLED'] = dict(n=len(rowsv), beta_dvrest=bp, ci_dvrest=cp, ratio_pm10=math.exp(bp * 20.0))
P()

# ---- the requested anchors --------------------------------------------------------------------------
P('   THE ORDER\'S OWN ANCHORS — the bin containing each games count:')
for anc in (2, 5, 10, 15, 20, 30):
    b = LB.binof(anc, LB.G_BINS_2)
    e = E2.get(b)
    if e is None:
        P('   at %2d games (bin %-6s): thin, not scored' % (anc, b)); continue
    P('   at %2d games (bin %-6s): BETA %+8.5f  90%% CI [%+.5f, %+.5f]   a +10 row is worth %.2fx a -10 row' % (
        anc, b, e['beta_dvrest'], e['ci_dvrest'][0], e['ci_dvrest'][1], e['ratio_pm10']))
P()

# ---- DV5, censoring-balanced ------------------------------------------------------------------------
P('-' * 118)
P('E2b · THE SAME ON A FIXED FIVE-YEAR FORWARD WINDOW (censoring held equal). AN ADDITION, NOT A SWAP.')
P('-' * 118)
sub5 = [r for r in rowsv if r['dv5_ok']]
P('   rows with a full five observable forward seasons: %d of %d' % (len(sub5), len(rowsv)))
P('   %-9s %5s | %-28s | %8s' % ('games', 'rows', 'BETA on DV5  [90% CI]', 'x(+/-10)'))
E2B = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    s = [r for r in sub5 if r['gbin'] == b]
    if len(s) < 30:
        P('   %-9s %5d | THIN' % (b, len(s))); continue
    ky = [r['key'] for r in s]
    bb = beta_fit(s, 'dv5')
    cc = cluster_boot(lambda i: beta_fit(s, 'dv5', i), ky, np.random.default_rng(SEED))
    P('   %-9s %5d | %+8.5f [%+.5f,%+.5f] | %8.2f' % (b, len(s), bb, cc[0], cc[1], math.exp(bb * 20.0)))
    E2B[b] = dict(n=len(s), beta=bb, ci=cc, ratio_pm10=math.exp(bb * 20.0))
P()

# ---- splits -----------------------------------------------------------------------------------------
P('-' * 118)
P('SPLITS — position class and pick band. A cell under 30 rows is reported THIN and derives nothing.')
P('-' * 118)
SPL = {}
for name, keyf, vals in (('position class', 'tall', ['TALL', 'SMALL']),
                         ('pick band', 'band', ['1-10', '11-20', '21-40', '41+/pool'])):
    P('   by %s:' % name)
    P('   %-10s %-9s %5s | %-28s | %8s' % (name, 'games', 'rows', 'BETA on DVREST [90% CI]', 'x(+/-10)'))
    for v in vals:
        for lo, hi in LB.G_BINS_2:
            b = '%d-%d' % (lo, hi)
            s = [r for r in rowsv if r[keyf] == v and r['gbin'] == b]
            if len(s) < 30:
                continue
            ky = [r['key'] for r in s]
            bb = beta_fit(s, 'dvrest')
            if bb is None: continue
            cc = cluster_boot(lambda i: beta_fit(s, 'dvrest', i), ky, np.random.default_rng(SEED))
            P('   %-10s %-9s %5d | %+8.5f [%+.5f,%+.5f] | %8.2f' % (v, b, len(s), bb, cc[0], cc[1], math.exp(bb * 20.0)))
            SPL.setdefault(name, {})[v + '|' + b] = dict(n=len(s), beta=bb, ci=cc)
        # pooled over games for the split level
        s = [r for r in rowsv if r[keyf] == v]
        if len(s) >= 30:
            ky = [r['key'] for r in s]
            bb = beta_fit(s, 'dvrest')
            cc = cluster_boot(lambda i: beta_fit(s, 'dvrest', i), ky, np.random.default_rng(SEED))
            P('   %-10s %-9s %5d | %+8.5f [%+.5f,%+.5f] | %8.2f   <- pooled over games' % (
                v, 'ALL', len(s), bb, cc[0], cc[1], math.exp(bb * 20.0)))
            SPL.setdefault(name, {})[v + '|ALL'] = dict(n=len(s), beta=bb, ci=cc)
    P()

# ---- binned means, the plain-language read ----------------------------------------------------------
P('-' * 118)
P('THE PLAIN READ — mean subsequent delivered value by performance-surplus tercile, within games bins')
P('-' * 118)
P('   %-9s %-6s %5s | %8s %8s | %10s %10s | %8s' % (
    'games', 'PS', 'rows', 'mean PS', 'mean v0', 'DVREST mn', 'DVREST md', 'DV1 mn'))
TERC = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = sorted([r for r in rowsv if r['gbin'] == b], key=lambda r: r['ps'])
    if len(sub) < 30: continue
    n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
    for t, lab in enumerate(('low', 'mid', 'high')):
        pt = sub[cuts[t]:cuts[t + 1]]
        P('   %-9s %-6s %5d | %+8.2f %8.0f | %10.1f %10.1f | %8.1f' % (
            b, lab, len(pt), np.mean([r['ps'] for r in pt]), np.mean([r['v0'] for r in pt]),
            np.mean([r['dvrest'] for r in pt]), np.median([r['dvrest'] for r in pt]),
            np.mean([r['dv1'] for r in pt])))
        TERC.setdefault(b, {})[lab] = dict(n=len(pt), ps=float(np.mean([r['ps'] for r in pt])),
                                           v0=float(np.mean([r['v0'] for r in pt])),
                                           dvrest=float(np.mean([r['dvrest'] for r in pt])),
                                           dv1=float(np.mean([r['dv1'] for r in pt])))
    P()

json.dump(dict(cohort=dict(rows=len(rowsv), players=len(set(r['key'] for r in rowsv)),
                           exclusions=dict(sorted(excl.items())), age_max=AGE_MAX),
               census=CEN, E1_E3=E13, E2=E2, E2b_dv5=E2B, splits=SPL, terciles=TERC,
               rows=rowsv),
          open(os.path.join(HERE, 'STEP2_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP2_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STEP2_N.json and STEP2_N_out.txt')
