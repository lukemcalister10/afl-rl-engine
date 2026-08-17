#!/usr/bin/env python
# ORDER 33 W3 — STEP 2: does career exposure add predictive power for future improvement
# at fixed age x position x current output? Specs M1-M4 per PREREG_W3.md (pushed first).
# READ-ONLY. Deterministic: seed 33, thread pins expected in env.
import json, os, collections
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(OUT, 'W3_TABLE.json')))
META = T['meta']; ROWS = T['rows']
BARS = META['bars']
BANDS = ['B0<-10', 'B1[-10,0)', 'B2[0,10)', 'B3>=10']

def band(r):
    x = r['avg'] - BARS[r['pos']]
    return 0 if x < -10 else (1 if x < 0 else (2 if x < 10 else 3))

base = [r for r in ROWS if 2005 <= r['year'] <= 2025 and r['games'] >= 6.0 * r['u']
        and 18 <= r['age'] <= 30]
cond = [r for r in base if r['next_full6']]
for r in base:
    r['band'] = band(r)
    r['first2'] = 1.0 if r['sidx'] <= 2 else 0.0
    r['impsurv'] = 1.0 if (r['next_full6'] and r['next_avg'] is not None
                           and r['next_avg'] >= r['avg']) else 0.0
for r in cond:
    r['d1'] = r['next_avg'] - r['avg']

L = []
P = L.append
P('ORDER 33 W3 MEASURE — store %s — seed 33' % META['store_md5'][:8])
P('base n=%d (players %d), conditional n=%d' % (len(base), len(set(r['key'] for r in base)), len(cond)))

# ---------- longitudinal age curve of next-season change (pooling n>=20) ----------
def agegroups(rows_):
    out = {}
    for tall in (False, True):
        sub = collections.defaultdict(list)
        for r in rows_:
            if r['tall'] == tall: sub[min(r['age'], 27)].append(r['d1'])
        ages = sorted(sub)
        groups = []; cur = []; curn = []
        for a in ages:
            cur.extend(sub[a]); curn.append(a)
            if len(cur) >= 20:
                groups.append((tuple(curn), cur)); cur = []; curn = []
        if cur:
            if groups:
                pa, pv = groups[-1]; groups[-1] = (pa + tuple(curn), pv + cur)
            else:
                groups.append((tuple(curn), cur))
        for aa, vv in groups:
            m = float(np.mean(vv))
            for a in aa: out[(tall, a)] = (m, len(vv), float(np.std(vv)))
    return out

CURVE = agegroups(cond)
P('')
P('LONGITUDINAL AGE CURVE of next-season change d1 = avg(Y+1)-avg(Y), conditional sample')
P('(the age-adjustment reference; cells pooled to n>=20; 27 = 27+)')
P('%-6s %-24s %-24s' % ('age', 'TALL mean d1 (n, sd)', 'SMALL mean d1 (n, sd)'))
for a in range(18, 28):
    def cell(t):
        v = CURVE.get((t, a))
        return '%+6.2f (n%d, sd %.1f)' % v if v else '--'
    P('%-6s %-24s %-24s' % (a if a < 27 else '27+', cell(True), cell(False)))

for r in cond:
    r['dA'] = r['d1'] - CURVE[(r['tall'], min(r['age'], 27))][0]
P('overall: mean d1 %+0.2f sd %.1f | mean dA %+0.3f sd %.1f' %
  (np.mean([r['d1'] for r in cond]), np.std([r['d1'] for r in cond]),
   np.mean([r['dA'] for r in cond]), np.std([r['dA'] for r in cond])))

# ---------- design matrix machinery ----------
POSL = ['KPD', 'KPF', 'RUCK', 'SD', 'SF']  # MID dropped
def design(rows_, expo_cols):
    n = len(rows_)
    cols = []; names = []
    cols.append(np.ones(n)); names.append('const')
    for a in range(18, 31):
        if a == 24: continue
        cols.append(np.array([1.0 if r['age'] == a else 0.0 for r in rows_])); names.append('age%d' % a)
    for p_ in POSL:
        cols.append(np.array([1.0 if r['pos'] == p_ else 0.0 for r in rows_])); names.append(p_)
    cols.append(np.array([r['avg'] - BARS[r['pos']] for r in rows_])); names.append('avg-bar')
    for b in (0, 1, 3):  # B2 dropped
        cols.append(np.array([1.0 if r['band'] == b else 0.0 for r in rows_])); names.append(BANDS[b])
    for nm, f in expo_cols:
        cols.append(np.array([f(r) for r in rows_], dtype=float)); names.append(nm)
    return np.column_stack(cols), names

def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]

def boot(rows_, expo_cols, ykey, B=1000, seed=33):
    X, names = design(rows_, expo_cols)
    y = np.array([r[ykey] for r in rows_], dtype=float)
    beta = ols(X, y)
    keys = [r['key'] for r in rows_]
    groups = collections.defaultdict(list)
    for i, k in enumerate(keys): groups[k].append(i)
    plist = sorted(groups); garr = [np.array(groups[k]) for k in plist]
    npl = len(plist)
    rng = np.random.default_rng(seed)
    nb = len(expo_cols)
    bs = np.empty((B, len(names)))
    for b in range(B):
        pick = rng.integers(0, npl, npl)
        idx = np.concatenate([garr[i] for i in pick])
        bs[b] = ols(X[idx], y[idx])
    lo = np.percentile(bs, 2.5, axis=0); hi = np.percentile(bs, 97.5, axis=0)
    return names, beta, lo, hi

def report(tag, rows_, expo_cols, ykey, show):
    names, beta, lo, hi = boot(rows_, expo_cols, ykey)
    P('%s  (n=%d, y=%s)' % (tag, len(rows_), ykey))
    for nm in show:
        i = names.index(nm)
        star = ' *' if (lo[i] > 0 or hi[i] < 0) else ''
        P('  %-14s %+7.3f  [%+7.3f, %+7.3f]%s' % (nm, beta[i], lo[i], hi[i], star))

# ---------- M1 pooled regressions ----------
P('')
P('M1 POOLED REGRESSIONS — dA ~ exposure + age dummies + pos + avg-bar + band dummies')
P('cluster bootstrap by player, B=1000, seed 33; * = 95% CI excludes 0')
P("owner's claim predicts: careergames/50 < 0, sidx < 0, FIRST2 > 0")
report('M1a exposure = career games / 50', cond, [('cg/50', lambda r: r['careergames'] / 50.0)], 'dA', ['cg/50'])
report('M1b exposure = played-season index X2', cond, [('sidx', lambda r: float(r['sidx']))], 'dA', ['sidx'])
report('M1c exposure = FIRST2 (X2<=2)', cond, [('FIRST2', lambda r: r['first2'])], 'dA', ['FIRST2'])
report('M1d exposure = listed tenure X3', cond, [('ltenure', lambda r: float(r['ltenure']))], 'dA', ['ltenure'])

# ---------- M3 shape ----------
P('')
P('M3 SHAPE — X2 dummies (baseline = 5+), same frame')
sx = [('sidx=%d' % k, (lambda kk: (lambda r: 1.0 if r['sidx'] == kk else 0.0))(k)) for k in (1, 2, 3, 4)]
report('M3', cond, sx, 'dA', [n for n, _ in sx])

# ---------- censoring: LPMs on the BASE sample ----------
P('')
P('CENSORING LPMs on base sample (linear probability, same controls):')
for r in base: r['exit1f'] = 1.0 if r['exit1'] else 0.0
report('LPM exit1 (no Y+1 season at all)', base, [('FIRST2', lambda r: r['first2'])], 'exit1f', ['FIRST2'])
report('LPM improve&survive (O3)', base, [('FIRST2', lambda r: r['first2'])], 'impsurv', ['FIRST2'])

# ---------- O4 horizon ----------
P('')
hor = [r for r in base if r['year'] <= 2023]
hcond = [r for r in hor if r['best3'] is not None]
for r in hcond: r['d3'] = r['best3'] - r['avg']
C3 = agegroups([dict(r, d1=r['d3']) for r in hcond])
for r in hcond: r['dA3'] = r['d3'] - C3[(r['tall'], min(r['age'], 27))][0]
for r in hor: r['any3'] = 1.0 if r['best3'] is not None else 0.0
P('O4 HORIZON (Y<=2023): best avg in Y+1..Y+3 (games>=6u) minus avg(Y)')
P('  n=%d, with any qualifying later season %d (%.1f%%)' %
  (len(hor), len(hcond), 100.0 * len(hcond) / len(hor)))
report('O4 dA3 ~ FIRST2', hcond, [('FIRST2', lambda r: r['first2'])], 'dA3', ['FIRST2'])
report('O4 P(any season in Y+1..Y+3) ~ FIRST2', hor, [('FIRST2', lambda r: r['first2'])], 'any3', ['FIRST2'])

# ---------- M2 key cells ----------
P('')
P('M2 KEY CELLS — LOW = first/second played season (X2<=2), HIGH = X2>=4 (veterans)')
P('columns per group: n | mean d1 | sd | mean dA | exit1% | P(imp&surv)%  (d-cols on cond rows)')
def cellstats(rows_b):
    rc = [r for r in rows_b if r['next_full6']]
    if rc:
        d1m = '%+6.2f' % np.mean([r['d1'] for r in rc]); sd = '%5.1f' % np.std([r['d1'] for r in rc])
        dAm = '%+6.2f' % np.mean([r['dA'] for r in rc])
    else:
        d1m = sd = dAm = '    --'
    ex = 100.0 * np.mean([1.0 if r['exit1'] else 0.0 for r in rows_b]) if rows_b else float('nan')
    im = 100.0 * np.mean([r['impsurv'] for r in rows_b]) if rows_b else float('nan')
    return len(rows_b), len(rc), d1m, sd, dAm, ex, im

def prcell(label, rows_b):
    lo = [r for r in rows_b if r['sidx'] <= 2]
    hi = [r for r in rows_b if r['sidx'] >= 4]
    out = [label]
    for gname, g in (('LOW', lo), ('HIGH', hi)):
        n, ncond, d1m, sd, dAm, ex, im = cellstats(g)
        supp = '' if min(n, ncond) >= 5 else '  UNSUPPORTED(n<5)'
        out.append('  %-4s n=%3d/%3d  d1 %s sd %s  dA %s  exit1 %4.1f%%  imp&surv %4.1f%%%s'
                   % (gname, n, ncond, d1m, sd, dAm, ex, im, supp))
    for line in out: P(line)

for ageband, f in [('23', lambda r: r['age'] == 23), ('24', lambda r: r['age'] == 24),
                   ('25', lambda r: r['age'] == 25), ('26+', lambda r: r['age'] >= 26),
                   ('POOLED 23+', lambda r: r['age'] >= 23)]:
    P('')
    P('AGE %s' % ageband)
    for tall, tn in ((True, 'TALL'), (False, 'SMALL')):
        for b in range(4):
            sub = [r for r in base if f(r) and r['tall'] == tall and r['band'] == b]
            if not sub: continue
            prcell(' %s %s' % (tn, BANDS[b]), sub)
    prcell(' ALL pos/bands age %s' % ageband, [r for r in base if f(r)])

# pooled 23+ contrast with bootstrap CI on the dA difference (LOW - HIGH), controls-free cell read
sub = [r for r in cond if r['age'] >= 23]
lo_ = [r for r in sub if r['sidx'] <= 2]; hi_ = [r for r in sub if r['sidx'] >= 4]
rng = np.random.default_rng(33)
diffs = []
ga = collections.defaultdict(list); gb = collections.defaultdict(list)
for r in lo_: ga[r['key']].append(r['dA'])
for r in hi_: gb[r['key']].append(r['dA'])
pa = sorted(ga); pb = sorted(gb)
for _ in range(1000):
    sa = [v for i in rng.integers(0, len(pa), len(pa)) for v in ga[pa[i]]]
    sb = [v for i in rng.integers(0, len(pb), len(pb)) for v in gb[pb[i]]]
    diffs.append(np.mean(sa) - np.mean(sb))
P('')
P('POOLED 23+ raw cell contrast (no controls beyond the dA age adjustment):')
P('  mean dA LOW (n=%d) %+0.2f  vs HIGH (n=%d) %+0.2f;  diff %+0.2f  [%+0.2f, %+0.2f] (cluster boot)'
  % (len(lo_), np.mean([r['dA'] for r in lo_]), len(hi_), np.mean([r['dA'] for r in hi_]),
     np.mean([r['dA'] for r in lo_]) - np.mean([r['dA'] for r in hi_]),
     np.percentile(diffs, 2.5), np.percentile(diffs, 97.5)))
q = lambda v: (np.percentile(v, 25), np.percentile(v, 50), np.percentile(v, 75))
P('  IQR dA LOW  p25/p50/p75: %+0.1f/%+0.1f/%+0.1f' % q([r['dA'] for r in lo_]))
P('  IQR dA HIGH p25/p50/p75: %+0.1f/%+0.1f/%+0.1f' % q([r['dA'] for r in hi_]))

# ---------- M4 named rows ----------
P('')
P('M4 NAMED ROWS (2026 in progress, u=0.92) + veteran comparators (rule: same age & POS in 2026,')
P('games>=6u, X2>=4, nearest avg)')
byname = {}
for r in ROWS:
    if r['year'] == 2026: byname.setdefault(r['key'], r)
def show(k):
    r = byname.get(k)
    if not r: P('  %s: no 2026 row' % k); return None
    P('  %-22s %-4s age %d  %2dg @ %.1f  careerG %3d  X2=%d  X3=%d  type %s' %
      (k, r['pos'], r['age'], int(r['games']), r['avg'], int(r['careergames']),
       r['sidx'], r['ltenure'], r['typ']))
    return r
for k in ('milan-murdock', 'hugo-hall-kahan', 'lachlan-mcandrew'):
    r = show(k)
    if not r: continue
    cands = [c for c in byname.values() if c['pos'] == r['pos'] and c['age'] == r['age']
             and c['sidx'] >= 4 and c['games'] >= 6.0 * 0.92 and c['key'] != k]
    if cands:
        c = min(cands, key=lambda c: abs(c['avg'] - r['avg']))
        P('    comparator:')
        show(c['key'])
    else:
        P('    no same-age same-POS veteran comparator in 2026 store')
    P('')

open(os.path.join(OUT, 'MEASURE_W3_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
