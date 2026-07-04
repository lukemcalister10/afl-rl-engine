#!/usr/bin/env python3
"""
localise.py  [BAKED c47cb43d]  READ-ONLY

Where is the compression? Separates two questions the naive stdev conflates:
  (1) AGGREGATE spread of the value scale vs a survivorship-aware realised ref
  (2) LOCAL rank-fidelity (does value order same-stage peers by production?)

Result: aggregate spread is healthy/expanded; the compression is LOCAL, in the
aging-elite regime, driven by the age/retention decay decoupling value from
continuing production. Reads dataset.json.
"""
import json, os, numpy as np
from scipy.stats import spearmanr

D = os.path.dirname(__file__)
recs = json.load(open(os.path.join(D, 'dataset.json')))
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

live = [r for r in recs if not r['retired_now']]
for r in recs:
    r['age'] = (2026 - (r['year'] + 1)) if r['year'] else None   # ~seasons since debut

P('='*78); P('[BAKED c47cb43d]  LOCALISATION — aggregate spread vs local rank-fidelity'); P('='*78)

# ---- (1) survivorship-aware realised reference: peak-vs-peak, settled cohort
P('\n(1) AGGREGATE: engine value spread vs REALISED spread (settled 2008-2016 ND,')
P('    every drafted player incl. busts at ~0 — survivorship-aware).')
settled = [r for r in recs if r['type'] == 'ND' and r['pick'] and r['year'] and 2008 <= r['year'] <= 2016]
def ratios(v, lab):
    v = np.asarray(v, float); q = lambda p: np.percentile(v, p)
    P(f'    {lab:16s} p50={q(50):7.1f} p90={q(90):7.1f} p99={q(99):7.1f} | '
      f'p90/50={q(90)/q(50):.2f} p99/50={q(99)/q(50):.2f} p99/90={q(99)/q(90):.2f}')
    return q(99)/q(50), q(99)/q(90)
r_p5099, r_p9099 = ratios([r['peakP'] for r in settled], 'realised peakP')
v_p5099, v_p9099 = ratios([r['peakV'] for r in settled], 'engine peakV')
sp = spearmanr([r['peakP'] for r in settled], [r['peakV'] for r in settled]).correlation
P(f'    realised/engine spread ratio: p99/50 {r_p5099/v_p5099:.2f}  p99/90 {r_p9099/v_p9099:.2f}   (<1 => engine spreads MORE)')
P(f'    spearman(peakP, peakV) = {sp:.3f}  (aggregate RANK agreement strong)')
P('    => the value SCALE is not globally compressed; it is if anything EXPANDED')
P('       vs realised outcomes (convex transform: pick prior + keeper economics).')

# ---- (2) local rank-fidelity by career-age band
P('\n(2) LOCAL: does value rank SAME-STAGE peers by current production?')
est = [r for r in live if r['nseas'] >= 4 and r['recentP'] > 0 and r['age'] is not None]
P('    established live (nseas>=4). spearman(recentP,cur) within age band:')
for lo, hi in [(0, 4), (5, 7), (8, 10), (11, 20)]:
    b = [r for r in est if lo <= r['age'] <= hi]
    if len(b) < 8: continue
    R = np.array([r['recentP'] for r in b]); V = np.array([r['cur'] for r in b])
    sp = spearmanr(R, V).correlation
    ret = np.array([r['cur']/r['peakV'] for r in b if r['peakV']])
    P(f'    age {lo:2d}-{hi:2d}yr  n={len(b):3d}  spearman={sp:.2f}  '
      f'retention(cur/peakV) p10-p90 = {np.percentile(ret,10):.2f}-{np.percentile(ret,90):.2f}')

# ---- (3) the aging-elite locus in detail
P('\n(3) AGING-ELITE LOCUS (age 11-15, recentP>=100) — the Petracca/Bont regime:')
ag = sorted([r for r in est if 11 <= r['age'] <= 15 and r['recentP'] >= 100], key=lambda r: -r['recentP'])
P('    player                 age recentP   cur  peakV  retention')
for r in ag:
    P(f'    {r["player"]:22s} {r["age"]:3d} {r["recentP"]:7.1f} {r["cur"]:5d} {r["peakV"]:6d}   {r["cur"]/r["peakV"]:.2f}')
R = np.array([r['recentP'] for r in ag]); V = np.array([r['cur'] for r in ag])
P(f'    n={len(ag)}  spearman(recentP,cur)={spearmanr(R,V).correlation:.2f}')
P(f'    production spread {R.min():.0f}-{R.max():.0f} = {R.max()/R.min():.2f}x  |  '
  f'value spread {V.min()}-{V.max()} = {V.max()/V.min():.2f}x')
P('    -> retention (cur/peakV) swings 0.2-0.8 and is NOT production-aligned:')
P('       the top-2 producers (Grundy 131 / Bont 129) retain only ~0.42-0.45,')
P('       while lower producers (Sinclair 117 @0.83, Dale 104 @0.65) retain more.')
P('       The decay scrambles the production order -> LOCAL compression among veterans.')

open(os.path.join(D, 'localise_report.txt'), 'w').write('\n'.join(out))
P('\nwrote localise_report.txt')
