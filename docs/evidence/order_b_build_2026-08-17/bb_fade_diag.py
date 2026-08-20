#!/usr/bin/env python3
# =====================================================================================================
# ORDER B BUILD -- IDENTIFICATION DIAGNOSIS for the failed conditional-fade fit (disclosed; runs AFTER
# bb_fade_fit.py). Question: does the SURVIVOR-LINKED RATE instrument (the instrument that demanded the
# terminal rise in the derivation) carry output-conditional signal that the prereg'd LEVEL-cell loss
# cannot see? Output-tercile-resolved engine vs realized step declines, cluster bootstrap.
# =====================================================================================================
import json, math, os, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'bb_fade_fit.py')).read().split('# control: reproduce')[0])

by_player_rows = collections.defaultdict(dict)
for x in rows:
    by_player_rows[x['key']][x['age']] = x
pairs = []
for k, d in by_player_rows.items():
    for a in range(26, 31):
        if a in d and (a + 1) in d and d[a + 1]['Y'] == d[a]['Y'] + 1:
            pairs.append((d[a], d[a + 1]))

RNG = np.random.default_rng(36)
B = 2000
OUT = {}
print('SURVIVOR-LINKED STEPS, OUTPUT-TERCILE RESOLVED (tercile = the x0 vantage tier)')
print('%-6s %-6s %4s %10s %10s %10s  %s' % ('tier', 'step', 'n', 'engine', 'realized', 'gap', 'gap 90% CI'))
for tr in ('star', 'mid', 'role'):
    for a in (27, 28, 29, 30):
        P2 = [(x0, x1) for x0, x1 in pairs if x0['age'] == a and x0.get('tier') == tr]
        if len(P2) < 12:
            OUT['%s|%d' % (tr, a)] = dict(n=len(P2), status='n<12')
            print('%-6s %d->%d n=%d  THIN' % (tr, a, a + 1, len(P2)))
            continue
        M0 = np.array([x0['mark'] for x0, _ in P2]); M1 = np.array([x1['mark'] for _, x1 in P2])
        R0 = np.array([x0['R'] for x0, _ in P2]); R1 = np.array([x1['R'] for _, x1 in P2])
        eng = M1.mean() / M0.mean(); rel = R1.mean() / R0.mean()
        gaps = []
        for _ in range(B):
            ix = RNG.integers(0, len(P2), size=len(P2))
            r0m = R0[ix].mean()
            if r0m <= 0:
                continue
            gaps.append(M1[ix].mean() / M0[ix].mean() - R1[ix].mean() / r0m)
        lo, hi = np.percentile(gaps, [5, 95])
        OUT['%s|%d' % (tr, a)] = dict(n=len(P2), engine=round(float(eng), 4), realized=round(float(rel), 4),
                                      gap=round(float(eng - rel), 4), gap_ci=[round(float(lo), 4), round(float(hi), 4)],
                                      called=bool(lo > 0 or hi < 0))
        print('%-6s %d->%d  %4d %10.4f %10.4f %+10.4f  [%+.4f, %+.4f]%s' % (
            tr, a, a + 1, len(P2), eng, rel, eng - rel, lo, hi, '  *CALLED*' if (lo > 0 or hi < 0) else ''))
# pooled 29-30 steps per tier (thin-cell pooling per the mandate)
print('\npooled steps 29->31 territory (x0 age in {29,30}) per tier:')
for tr in ('star', 'mid', 'role'):
    P2 = [(x0, x1) for x0, x1 in pairs if x0['age'] in (29, 30) and x0.get('tier') == tr]
    M0 = np.array([x0['mark'] for x0, _ in P2]); M1 = np.array([x1['mark'] for _, x1 in P2])
    R0 = np.array([x0['R'] for x0, _ in P2]); R1 = np.array([x1['R'] for _, x1 in P2])
    eng = M1.mean() / M0.mean(); rel = R1.mean() / R0.mean()
    gaps = []
    for _ in range(B):
        ix = RNG.integers(0, len(P2), size=len(P2))
        r0m = R0[ix].mean()
        if r0m > 0:
            gaps.append(M1[ix].mean() / M0[ix].mean() - R1[ix].mean() / r0m)
    lo, hi = np.percentile(gaps, [5, 95])
    OUT['%s|pool2930' % tr] = dict(n=len(P2), engine=round(float(eng), 4), realized=round(float(rel), 4),
                                   gap=round(float(eng - rel), 4), gap_ci=[round(float(lo), 4), round(float(hi), 4)],
                                   called=bool(lo > 0 or hi < 0))
    print('  %-6s n=%3d engine %.4f realized %.4f gap %+.4f [%+.4f, %+.4f]%s' % (
        tr, len(P2), eng, rel, eng - rel, lo, hi, '  *CALLED*' if (lo > 0 or hi < 0) else ''))

with open(os.path.join(HERE, 'RESULTS_B_FADE_DIAG.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_FADE_DIAG.json')
