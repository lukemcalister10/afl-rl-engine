#!/usr/bin/env python3
"""ORDER 32 S5 STEP 4 -- noise honesty: player-level bootstrap of the band residuals and the gap.

Primary (preregistered): resample the 1,142 fit rows with replacement, 4,000 reps, fitted surface
HELD FIXED; per rep recompute band means of raw value and of fitted-at-cell, hence
R_band = mean(fit) - mean(raw) and G = R(21-30) - R(31-40).  95% percentile CIs.
Subsets bootstrapped separately (within-subset resampling): modern 2015+, MID-only, SF-only.

DISCLOSED DEVIATION from PREREG step 5: the optional full-pipeline bootstrap (loclin->shrink->PAVA
per rep) is NOT run. Reason: the fit's persisted loclin surface (posv_raw = relat*curve) is built by
the ORDER-28 harness relativity construction, which a direct kernel_loclin call approximates only to
~5-10% (checked); re-deriving that construction would be exactly the parallel lane the seat mandate
forbids. The constraint-suppression channel is instead bounded directly by the measured PAVA-stage
transfer on the true lineage (Step 2: |R_pava| <= 1.3 points pooled, <= 0.5% of band value).
Writes S5_BOOT.json + s5_step4_out.txt.  Seed 3251142 (fixed, arbitrary).
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
INP = json.load(open(os.path.join(HERE, 'S5_INPUTS.json')))
_OUT = []
def P(s=''):
    print(s); _OUT.append(s)

POS = sorted(INP['posv_fitted'].keys())
fin = {g: {int(k): v for k, v in INP['posv_fitted'][g].items()} for g in POS}
rows = INP['rows']
BANDS = [('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)]

pick = np.array([r['pick'] for r in rows])
val = np.array([r['value'] for r in rows])
fitv = np.array([fin[r['pos']][r['pick']] for r in rows])
year = np.array([r['entry_year'] for r in rows])
posn = np.array([r['pos'] for r in rows])
bandidx = np.full(len(rows), -1)
for bi, (nm, lo, hi) in enumerate(BANDS):
    bandidx[(pick >= lo) & (pick <= hi)] = bi

REPS = 4000
rng = np.random.default_rng(3251142)

def boot(mask, label):
    idx = np.flatnonzero(mask)
    n = len(idx)
    samp = idx[rng.integers(0, n, size=(REPS, n))]
    v = val[samp]; f = fitv[samp]; b = bandidx[samp]
    out = {}
    Rb = {}
    for bi, (nm, lo, hi) in enumerate(BANDS):
        m = (b == bi)
        cnt = m.sum(axis=1)
        # guard: a rep with an empty band (possible in small subsets) is excluded for that band
        ok = cnt > 0
        rawm = np.where(ok, (v * m).sum(axis=1) / np.maximum(cnt, 1), np.nan)
        fitm = np.where(ok, (f * m).sum(axis=1) / np.maximum(cnt, 1), np.nan)
        Rb[nm] = fitm - rawm
        q = np.nanpercentile(Rb[nm], [2.5, 50, 97.5])
        out[nm] = dict(point=float(fitv[idx][bandidx[idx] == bi].mean() - val[idx][bandidx[idx] == bi].mean())
                       if (bandidx[idx] == bi).any() else None,
                       ci_lo=float(q[0]), med=float(q[1]), ci_hi=float(q[2]),
                       excluded_reps=int((~ok).sum()))
    G = Rb['21-30'] - Rb['31-40']
    qG = np.nanpercentile(G, [2.5, 50, 97.5])
    i2, i3 = (bandidx[idx] == 2), (bandidx[idx] == 3)
    ptG = float((fitv[idx][i2].mean() - val[idx][i2].mean()) - (fitv[idx][i3].mean() - val[idx][i3].mean())) \
        if i2.any() and i3.any() else None
    frac_neg = float(np.nanmean(G < 0))
    out['G'] = dict(point=ptG, ci_lo=float(qG[0]), med=float(qG[1]), ci_hi=float(qG[2]),
                    frac_reps_negative=frac_neg,
                    clears_noise=bool(qG[0] > 0 or qG[2] < 0))
    P('%s  (n=%d, %d reps)' % (label, n, REPS))
    P('  %-6s %10s %22s %14s' % ('band', 'R point', '95%% CI', 'excl reps'))
    for nm, lo, hi in BANDS:
        o = out[nm]
        P('  %-6s %+10.1f   [%+8.1f, %+8.1f] %10d' % (nm, o['point'] if o['point'] is not None else float('nan'),
                                                      o['ci_lo'], o['ci_hi'], o['excluded_reps']))
    P('  G = R(21-30)-R(31-40): point %+.1f   95%% CI [%+.1f, %+.1f]   P(G<0) = %.3f   CLEARS NOISE: %s'
      % (out['G']['point'], out['G']['ci_lo'], out['G']['ci_hi'], frac_neg,
         'YES' if out['G']['clears_noise'] else 'NO'))
    P('')
    return out

P('ORDER 32 S5 STEP 4 -- BOOTSTRAP (player-level, fitted surface fixed, percentile CIs, seed 3251142)')
P('')
RES = {}
RES['full'] = boot(np.ones(len(rows), bool), 'FULL WINDOW 2004-2021, all positions')
RES['modern_2015plus'] = boot(year >= 2015, 'MODERN 2015+, all positions')
RES['MID_only'] = boot(posn == 'MID', 'MID only, full window')
RES['SF_only'] = boot(posn == 'SF', 'SF only, full window')

# also: does 21-30's own underpricing clear noise? R(21-30) CI vs 0, full window
o = RES['full']['21-30']
P('R(21-30) alone, full window: point %+.1f, 95%% CI [%+.1f, %+.1f] -> %s' %
  (o['point'], o['ci_lo'], o['ci_hi'],
   'clears noise' if (o['ci_hi'] < 0 or o['ci_lo'] > 0) else 'does NOT clear noise'))

json.dump(dict(order='ORDER 32 S5 STEP 4 -- bootstrap', reps=REPS, seed=3251142, results=RES,
               deviation='full-pipeline bootstrap not run; see docstring'),
          open(os.path.join(HERE, 'S5_BOOT.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 's5_step4_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('')
P('S5_BOOT.json written.')
