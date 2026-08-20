#!/usr/bin/env python3
"""ORDER 32 S5 STEP 3 -- era control. Band residuals on 2015+ cohorts vs the full 2004-2021 window,
and era stability of the raw value-by-pick gradient itself. Fitted surface held fixed (it was fitted
on the pooled window; the question is whether the modern draft shows the same band pattern).
Sign convention: R = fitted v0 minus raw; R < 0 = underpriced.  Writes S5_ERA.json + s5_step3_out.txt.
CAVEAT (named): 2015+ careers are right-truncated relative to pre-2015 (the youngest cohorts have not
finished delivering); the #338 basis grace machinery mitigates but does not erase this. Era LEVELS are
therefore not directly comparable; the SHAPE across bands within an era is the comparable object.
"""
import json, os, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
INP = json.load(open(os.path.join(HERE, 'S5_INPUTS.json')))
_OUT = []
def P(s=''):
    print(s); _OUT.append(s)

POS = sorted(INP['posv_fitted'].keys())
fin = {g: {int(k): v for k, v in INP['posv_fitted'][g].items()} for g in POS}
rows = INP['rows']
BANDS = [('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)]
def band_of(p):
    for nm, lo, hi in BANDS:
        if lo <= p <= hi: return nm
def sd(vs):
    n = len(vs); m = sum(vs) / n
    return math.sqrt(sum((v - m) ** 2 for v in vs) / (n - 1)) if n > 1 else 0.0

ERAS = [('full 2004-2021', lambda y: True), ('pre-2015 (2004-2014)', lambda y: y < 2015),
        ('modern 2015+ (2015-2021)', lambda y: y >= 2015)]

OUTJ = {}
for label, f in ERAS:
    sub = [r for r in rows if f(r['entry_year'])]
    P('ERA: %s   (n=%d)' % (label, len(sub)))
    P('  %-6s %4s %9s %8s %9s %9s | %8s %7s | %9s' %
      ('band', 'n', 'raw_mean', 'raw_se', 'raw_sd', 'fit_mean', 'R_total', 'Rtot%', 'raw/fit'))
    era = {}
    byb = collections.defaultdict(list)
    for r in sub: byb[band_of(r['pick'])].append(r)
    for nm, lo, hi in BANDS:
        rws = byb[nm]; n = len(rws)
        vals = [r['value'] for r in rws]
        mraw = sum(vals) / n
        mfit = sum(fin[r['pos']][r['pick']] for r in rws) / n
        e = dict(n=n, raw_mean=mraw, raw_sd=sd(vals), raw_se=sd(vals) / math.sqrt(n),
                 fit_mean=mfit, R_total=mfit - mraw, R_total_pct=100.0 * (mfit - mraw) / mfit,
                 raw_over_fit=mraw / mfit)
        era[nm] = e
        P('  %-6s %4d %9.1f %8.1f %9.1f %9.1f | %+8.1f %+6.1f%% | %9.3f' %
          (nm, n, mraw, e['raw_se'], e['raw_sd'], mfit, e['R_total'], e['R_total_pct'], e['raw_over_fit']))
    G = era['21-30']['R_total'] - era['31-40']['R_total']
    era['gap_R_total'] = G
    P('  G = R(21-30) - R(31-40) = %+.1f v0 points' % G)
    # the gradient itself: band-to-band raw ratios (shape within era, immune to era level)
    r1, r2, r3, r4, r5 = (era[nm]['raw_mean'] for nm, _, _ in BANDS)
    P('  raw gradient (band ratios): 1-10/11-20 %.2f   11-20/21-30 %.2f   21-30/31-40 %.2f   31-40/41-64 %.2f   1-10/41-64 %.2f'
      % (r1 / r2, r2 / r3, r3 / r4, r4 / r5, r1 / r5))
    era['gradient'] = {'1-10/11-20': r1 / r2, '11-20/21-30': r2 / r3, '21-30/31-40': r3 / r4,
                       '31-40/41-64': r4 / r5, '1-10/41-64': r1 / r5}
    OUTJ[label] = era
    P('')

json.dump(dict(order='ORDER 32 S5 STEP 3 -- era control', eras=OUTJ,
               caveat='2015+ careers right-truncated; compare band SHAPE within era, not level'),
          open(os.path.join(HERE, 'S5_ERA.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 's5_step3_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('S5_ERA.json written.')
