"""DATE THE FIT — sweep every historical version of the store and ask which one reproduces the
band pickles' own six init_ constants (the exact quantiles of their training target).

Also dates q97m (alpha=0.97, 111.43333333) the same way, and reports the T1 population size at
each era so the 13,221 figure in the T1 comment can be located in time.
"""
import json, os, glob, sys
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/afl-rl-engine'
sys.path.insert(0, S)
from importlib import import_module
F = import_module('02_provenance_forensic') if False else None  # not importable (numeric name)

TARGETS = {0.10: 42.0, 0.30: 58.86666666666667, 0.50: 69.36666666666666,
           0.70: 82.23333333333333, 0.90: 99.73333333333333, 0.97: 111.43333333333334}
CM_Q = [0.10, 0.30, 0.50, 0.70, 0.90]      # the five in cm_400.pkl
VOCAB = {'MID': 'MID', 'GFWD': 'SF', 'GDEF': 'SD', 'KFWD': 'KPF', 'KDEF': 'KPD',
         'RUC': 'RUCK', 'DEF': 'SD'}
GRP = {'MID', 'RUCK', 'SF', 'KPF', 'SD', 'KPD'}


def pos_of(p):
    v = p.get('drafted_position') or p.get('pos')
    return VOCAB.get(v, v)


def is_ft(p):
    return p.get('type') in ('ND', 'RD', 'PSD')


def debutyr(p):
    return p['year'] if p['type'] == 'MSD' else p['year'] + 1


def fwd_best3_from(p, Y, cap):
    lo = max(Y, debutyr(p))
    qual = sorted([x['avg'] for x in p['scoring'] if x['games'] >= 6 and lo <= x['year'] <= cap],
                  reverse=True)
    if len(qual) >= 3:
        return float(np.mean(qual[:3]))
    if len(qual) >= 1:
        return float(np.mean(qual))
    a = [x['avg'] for x in p['scoring'] if lo <= x['year'] <= cap and x['games'] > 0]
    return float(max(a)) if a else 0.0


def build_y(store, cap=2026, resolved_cut=2021, t1=True):
    yrs = [x['year'] for p in store for x in (p.get('scoring') or [])]
    fo = min(yrs) if yrs else None
    ys = []
    for p in store:
        if pos_of(p) not in GRP:
            continue
        if debutyr(p) > resolved_cut:
            continue
        if not (p.get('pick') or is_ft(p)):
            continue
        d0 = debutyr(p) - 1
        last = max([x['year'] for x in p['scoring']] + [d0])
        for Y in range(d0, min(last, cap) + 1):
            if t1 and fo is not None and d0 < Y < fo:
                continue
            ys.append(fwd_best3_from(p, Y, cap))
    return np.array(ys), fo


rows = []
for f in sorted(glob.glob(os.path.join(S, 'out', 'stores', '*.json'))):
    base = os.path.basename(f)[:-5]
    date, sha = base.split('_')
    store = json.load(open(f))
    for t1 in (False, True):
        y, fo = build_y(store, t1=t1)
        got = {q: float(np.percentile(y, q * 100.0)) for q in TARGETS}
        err = {q: got[q] - TARGETS[q] for q in TARGETS}
        cm_worst = max(abs(err[q]) for q in CM_Q)
        cm_exact = sum(1 for q in CM_Q if abs(err[q]) < 1e-9)
        q97_err = abs(err[0.97])
        rows.append(dict(date=date, sha=sha, t1=t1, n=len(y), first_obs=fo,
                         cm_exact_of_5=cm_exact, cm_worst=cm_worst, q97_err=q97_err,
                         got={('%.2f' % q): round(v, 8) for q, v in got.items()}))

rows.sort(key=lambda r: (r['date'], r['sha'], r['t1']))
print('%-11s %-8s %-5s %6s  %10s %12s  %10s' %
      ('date', 'store', 'T1', 'n', 'cm exact/5', 'cm worst err', 'q97 err'))
for r in rows:
    flag = ''
    if r['cm_exact_of_5'] == 5:
        flag += '  <== cm_400 ALL FIVE EXACT'
    if r['q97_err'] < 1e-9:
        flag += '  <== q97m EXACT'
    print('%-11s %-8s %-5s %6d  %10d %12.6f  %10.6f%s' %
          (r['date'], r['sha'], r['t1'], r['n'], r['cm_exact_of_5'], r['cm_worst'],
           r['q97_err'], flag))

json.dump(rows, open(os.path.join(S, 'out', 'store_sweep.json'), 'w'), indent=1, default=str)
print('\nwrote out/store_sweep.json')
