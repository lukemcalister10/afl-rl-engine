"""PROVENANCE FORENSIC — WHICH STORE FITTED THE BAND?

The pickles carry no training-store stamp. But a sklearn GradientBoostingRegressor with
loss='quantile' initialises with a DummyRegressor(strategy='quantile', quantile=alpha), whose
`constant_` is EXACTLY the alpha-quantile of the training target vector y.

data/cm_400.pkl and data/q97m.pkl therefore carry SIX exact statistics of their own training y:

    q0.10 -> 42.0            q0.70 -> 82.23333333
    q0.30 -> 58.86666667     q0.90 -> 99.73333333
    q0.50 -> 69.36666667     q0.97 -> 111.43333333

y is `fwd_best3_from(p,Y,cap)` over the population `build_cond_prior` assembles. It depends ONLY on
the store's scoring rows, the entry-type/pick filter, the position filter and the debut window —
NOT on the level feature. So the par-centring question (cp._lvl_eff = PR.lvl_par at training) does
not touch this test at all. That makes it a clean discriminator between store eras.

This script rebuilds y STANDALONE (no engine import) against
  (A) the current store          engine/rl_after/rl_model_data.json   (b745002e)
  (B) the fit-era proxy store    git f4a4d34 (2026-07-02 seed)        (644d1254)
under several variants of the population rule, and reports which combination reproduces the six
constants. Read-only; writes only into the scratch dir.
"""
import json, os, sys, collections, itertools
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/afl-rl-engine'

TARGETS = {0.10: 42.0, 0.30: 58.86666666666667, 0.50: 69.36666666666666,
           0.70: 82.23333333333333, 0.90: 99.73333333333333, 0.97: 111.43333333333334}

# ---------------------------------------------------------------- store loading
NEW = json.load(open(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')))
OLD = json.load(open(os.path.join(S, 'out', 'store_fitera.json')))

# position vocabulary of the pre-#262 store -> the current canonical six (derived empirically from
# the matched-pair census in 01_store_drift.py: the dominant image of each old label).
VOCAB = {'MID': 'MID', 'GFWD': 'SF', 'GDEF': 'SD', 'KFWD': 'KPF', 'KDEF': 'KPD',
         'RUC': 'RUCK', 'DEF': 'SD'}
GRP = {'MID', 'RUCK', 'SF', 'KPF', 'SD', 'KPD'}
ND_CURVE_LAST = 64


def pos_of(p, era):
    if era == 'new':
        return p.get('drafted_position')
    v = p.get('pos') or p.get('drafted_position')
    return VOCAB.get(v, v)


def is_ft(p):
    """rl_model's _ft flag, recomputed: True for ND and for RD/PSD (they carry a real draft slot
    mechanism); False for the pickless mechanisms (MSD/SSP/IRE/UNR/PD*). build_cond_prior admits a
    row when `p.get('pick') or p.get('_ft')`, so the pickless entrants are admitted only when the
    store happens to carry a pick for them (it does not)."""
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
    anyseason = [x['avg'] for x in p['scoring'] if lo <= x['year'] <= cap and x['games'] > 0]
    return float(max(anyseason)) if anyseason else 0.0


def build_y(store, era, cap=2026, resolved_cut=2021, t1=True, ycap=None):
    """build_cond_prior's population, target-only.  t1=False reproduces the PRE-2026-07-31 rule
    (no FIRST_OBSERVABLE filter — the fabricated-zero rows are in)."""
    yrs = [x['year'] for p in store for x in (p.get('scoring') or [])]
    fo = min(yrs) if yrs else None
    ys = []
    meta = []
    for p in store:
        if pos_of(p, era) not in GRP:
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
            meta.append((p, Y))
    return np.array(ys), meta, fo


def qtest(y):
    """sklearn DummyRegressor(strategy='quantile') uses np.percentile(y, q*100) (linear interp)."""
    return {q: float(np.percentile(y, q * 100.0)) for q in TARGETS}


def score(y):
    got = qtest(y)
    return got, max(abs(got[q] - TARGETS[q]) for q in TARGETS), all(
        abs(got[q] - TARGETS[q]) < 1e-9 for q in TARGETS)


results = []
print('TARGETS (the pickles\' own init_.constant_):')
for q in sorted(TARGETS):
    print('   q=%.2f  %.8f' % (q, TARGETS[q]))
print()

grid = []
for era, store, label in (('new', NEW, 'CURRENT store b745002e'),
                          ('old', OLD, 'FIT-ERA proxy 644d1254 (git f4a4d34, 2026-07-02)')):
    for t1 in (True, False):
        for cap in (2026, 2025, 2024, 2023, 2022, 2021):
            for rc in (2021, 2020):
                grid.append((era, store, label, t1, cap, rc))

best = None
for era, store, label, t1, cap, rc in grid:
    y, meta, fo = build_y(store, era, cap=cap, resolved_cut=rc, t1=t1)
    got, worst, exact = score(y)
    rec = dict(store=label, era=era, t1=t1, cap=cap, resolved_cut=rc, n=len(y),
               first_observable=fo, worst_abs_err=worst, exact=exact,
               got={('%.2f' % q): round(v, 8) for q, v in got.items()})
    results.append(rec)
    if best is None or worst < best['worst_abs_err']:
        best = rec
    if exact or worst < 0.5:
        print('  %-52s T1=%-5s cap=%d cut=%d  n=%6d  worst|err|=%.8f %s'
              % (label, t1, cap, rc, len(y), worst, 'EXACT MATCH' if exact else ''))

print()
print('BEST OVERALL:')
print(json.dumps(best, indent=1, default=str))
print()
print('worst-error ranking (top 12):')
for r in sorted(results, key=lambda r: r['worst_abs_err'])[:12]:
    print('  %-52s T1=%-5s cap=%d cut=%d n=%6d  worst=%.6f'
          % (r['store'], r['t1'], r['cap'], r['resolved_cut'], r['n'], r['worst_abs_err']))

json.dump({'targets': {str(k): v for k, v in TARGETS.items()}, 'results': results, 'best': best},
          open(os.path.join(S, 'out', 'provenance_forensic.json'), 'w'), indent=1, default=str)
print('\nwrote out/provenance_forensic.json')
