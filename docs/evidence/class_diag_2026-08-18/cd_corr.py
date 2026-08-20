#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART B, THE DECISIVE TEST.

Does ORDER P's per-class mark track REALISED class strength better than ORDER K's?

n = 11 classes. That is small. Every correlation is reported with a bootstrap CI over classes and
the paired difference (ORDER P minus ORDER K) is reported with its own CI, because the two
correlations are computed on the same eleven classes and are not independent.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

M = {t: L.class_marks(L.load(t))[0] for t in ('O35FINAL', 'OKRULED', 'PBUILT')}
MEAS = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'CD_OUTCOMES.json')))['meas'].items()}
YS = L.W2
NB = 20000
rng = np.random.default_rng(20260818)

KEYS = [('surp_per_row', 'year-1 surplus points per row'),
        ('prod_per_row', 'year-1 production per row'),
        ('games_per_row', 'year-1 games per row'),
        ('surp_ppg', 'year-1 points per game above the age bar'),
        ('ppg', 'year-1 points per game'),
        ('share_above', 'share of year-1 players above the age bar'),
        ('share_played', 'share of the class that played in year 1'),
        ('career_games_per_row', 'career games per row'),
        ('share_100', 'share reaching 100 career games')]


def rankv(a):
    a = np.asarray(a, float)
    o = a.argsort()
    r = np.empty(len(a))
    r[o] = np.arange(1, len(a) + 1)
    for v in set(a):
        m = a == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def _pear_rows(A, B):
    """Pearson row by row over two (nboot, n) arrays. NaN where a row has no spread."""
    A = A - A.mean(1, keepdims=True)
    B = B - B.mean(1, keepdims=True)
    num = (A * B).sum(1)
    den = np.sqrt((A * A).sum(1) * (B * B).sum(1))
    out = np.full(len(num), np.nan)
    m = den > 0
    out[m] = num[m] / den[m]
    return out


def _rank_rows(A):
    """Average-tie ranks row by row over an (nboot, n) array."""
    o = A.argsort(1, kind='stable')
    n = A.shape[1]
    r = np.empty(A.shape)
    np.put_along_axis(r, o, np.tile(np.arange(1.0, n + 1), (A.shape[0], 1)), 1)
    S = np.take_along_axis(A, o, 1)
    # average ranks inside runs of equal values
    R = np.take_along_axis(r, o, 1)
    for i in range(A.shape[0]):
        j = 0
        while j < n:
            k = j
            while k + 1 < n and S[i, k + 1] == S[i, j]:
                k += 1
            if k > j:
                R[i, j:k + 1] = R[i, j:k + 1].mean()
            j = k + 1
    np.put_along_axis(r, o, R, 1)
    return r


def pear(a, b):
    return float(_pear_rows(np.asarray(a, float)[None, :], np.asarray(b, float)[None, :])[0])


def spear(a, b):
    return pear(rankv(a), rankv(b))


def _idx(n):
    return rng.integers(0, n, size=(NB, n))


def _rows(a, b, idx, kind):
    A = np.asarray(a, float)[idx]
    B = np.asarray(b, float)[idx]
    if kind == 'spear':
        A = _rank_rows(A); B = _rank_rows(B)
    return _pear_rows(A, B)


def boot(a, b, kind):
    v = _rows(a, b, _idx(len(a)), kind)
    v = v[np.isfinite(v)]
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def boot_diff(a1, a2, b, kind):
    idx = _idx(len(b))
    x = _rows(a1, b, idx, kind)
    y = _rows(a2, b, idx, kind)
    d = x - y
    d = d[np.isfinite(d)]
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), float((d > 0).mean())


mk = {t: [M[t][y] for y in YS] for t in M}
dPK = [M['PBUILT'][y] - M['OKRULED'][y] for y in YS]

P('=' * 126)
P('B — DOES THE CLASS MARK TRACK REALISED CLASS STRENGTH?  n = 11 classes. CIs are 2.5/97.5 percentile')
P('    over %d bootstrap resamples of the eleven classes.' % NB)
P('=' * 126)
P()
RES = {}
for k, nice in KEYS:
    x = [MEAS[y][k] for y in YS]
    P('  ---- realised measure: %s ----' % nice)
    P('  %-14s %8s %-20s %8s %-20s' % ('board', 'Spearman', '95% CI', 'Pearson', '95% CI'))
    row = {}
    for t, lab in (('OKRULED', 'ORDER K'), ('PBUILT', 'ORDER P'), ('O35FINAL', 'landing cand')):
        s = spear(mk[t], x); sc = boot(mk[t], x, 'spear')
        p = pear(mk[t], x); pc = boot(mk[t], x, 'pear')
        row[t] = dict(spear=s, spear_ci=sc, pear=p, pear_ci=pc)
        P('  %-14s %+8.3f [%+.3f, %+.3f]     %+8.3f [%+.3f, %+.3f]' % (lab, s, sc[0], sc[1], p, pc[0], pc[1]))
    ds = spear(mk['PBUILT'], x) - spear(mk['OKRULED'], x)
    dsl, dsh, pr = boot_diff(mk['PBUILT'], mk['OKRULED'], x, 'spear')
    dp = pear(mk['PBUILT'], x) - pear(mk['OKRULED'], x)
    dpl, dph, pr2 = boot_diff(mk['PBUILT'], mk['OKRULED'], x, 'pear')
    P('  %-14s %+8.3f [%+.3f, %+.3f] P>K in %.0f%% of resamples' % ('P minus K (S)', ds, dsl, dsh, 100 * pr))
    P('  %-14s %+8.3f [%+.3f, %+.3f] P>K in %.0f%% of resamples' % ('P minus K (r)', dp, dpl, dph, 100 * pr2))
    sd = spear(dPK, x); sdc = boot(dPK, x, 'spear')
    pd_ = pear(dPK, x); pdc = boot(dPK, x, 'pear')
    P('  %-14s %+8.3f [%+.3f, %+.3f]     %+8.3f [%+.3f, %+.3f]'
      % ('the MOVE P-K', sd, sdc[0], sdc[1], pd_, pdc[0], pdc[1]))
    P()
    row['diff'] = dict(spear=ds, spear_ci=[dsl, dsh], spear_prob=pr,
                       pear=dp, pear_ci=[dpl, dph], pear_prob=pr2,
                       move_spear=sd, move_spear_ci=sdc, move_pear=pd_, move_pear_ci=pdc)
    RES[k] = row

P('=' * 126)
P('B-SUMMARY — the paired difference in correlation, ORDER P minus ORDER K, on all nine measures')
P('=' * 126)
P('  %-42s %10s %-20s %10s %-20s' % ('realised measure', 'dSpearman', '95% CI', 'dPearson', '95% CI'))
ns = np_ = 0
for k, nice in KEYS:
    d = RES[k]['diff']
    P('  %-42s %+10.3f [%+.3f, %+.3f] %+10.3f [%+.3f, %+.3f]'
      % (nice, d['spear'], d['spear_ci'][0], d['spear_ci'][1], d['pear'], d['pear_ci'][0], d['pear_ci'][1]))
    ns += (d['spear'] > 0); np_ += (d['pear'] > 0)
P('  ORDER P correlates MORE strongly than ORDER K on %d of 9 measures (Spearman), %d of 9 (Pearson).'
  % (ns, np_))
P()
P('  raw inputs, for anyone who wants to redo this by hand:')
P('  %-6s %9s %9s %9s %10s %10s %9s' % ('class', 'mark K', 'mark P', 'move', 'surp/row', 'prod/row', 'gms/row'))
for y in YS:
    P('  %-6d %9.4f %9.4f %+9.4f %10.1f %10.1f %9.2f'
      % (y - 1, M['OKRULED'][y], M['PBUILT'][y], M['PBUILT'][y] - M['OKRULED'][y],
         MEAS[y]['surp_per_row'], MEAS[y]['prod_per_row'], MEAS[y]['games_per_row']))

json.dump(RES, open(os.path.join(HERE, 'CD_CORR.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CD_CORR_out.txt'), 'w').write('\n'.join(OUT) + '\n')
