#!/usr/bin/env python3
"""ORDER 32 SEAT S3 — estimators. Reads DATASET_S3.json only. numpy+scipy, threads pinned by caller.
Everything here was declared in PREREG_S3.md before this file was run. Outputs RESULTS_S3.json +
RESULTS_S3_out.txt (full tables)."""
import os, json, math, collections
import numpy as np
from scipy import optimize, stats as sstats

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'DATASET_S3.json')))
ROWS = D['rows']
rng = np.random.default_rng(320317)
OUT = {}
LINES = []
def say(s=''):
    LINES.append(s); print(s)

# ---------------------------------------------------------------- helpers
def ols(X, y, cluster=None):
    """OLS with HC1 (or cluster-robust when cluster ids given). Returns b, se, n, k, r2."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape
    XtX = X.T @ X
    XtXi = np.linalg.pinv(XtX)
    b = XtXi @ (X.T @ y)
    e = y - X @ b
    if cluster is None:
        meat = (X * (e ** 2)[:, None]).T @ X
        V = XtXi @ meat @ XtXi * (n / max(1, n - k))
    else:
        cl = collections.defaultdict(list)
        for i, c in enumerate(cluster): cl[c].append(i)
        meat = np.zeros((k, k))
        for idx in cl.values():
            Xg = X[idx]; eg = e[idx]
            s = Xg.T @ eg
            meat += np.outer(s, s)
        G = len(cl)
        V = XtXi @ meat @ XtXi * (G / max(1, G - 1)) * ((n - 1) / max(1, n - k))
    se = np.sqrt(np.maximum(np.diag(V), 0))
    ssr = float(e @ e); sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ssr / sst if sst > 0 else float('nan')
    return b, se, n, k, r2

def dummies(vals, drop_first=True):
    levs = sorted(set(vals))
    if drop_first: levs = levs[1:]
    M = np.zeros((len(vals), len(levs)))
    for j, L in enumerate(levs):
        M[:, j] = [1.0 if v == L else 0.0 for v in vals]
    return M, levs

def design(rows, games_cols, extra_cols=(), fe_club_year=False):
    """[games_cols..., surplus, age, extra..., 1, band dummies, cohort dummies, pos dummies
       (+ club x year dummies)] -> X, names"""
    cols = [np.asarray(c, float) for c in games_cols[0]]
    names = list(games_cols[1])
    S = np.array([r['surplus'] for r in rows]); names_c = ['surplus', 'age']
    A = np.array([r['age'] if r['age'] is not None else 19 + r['k'] for r in rows])
    parts = cols + [S, A]
    for nm, c in extra_cols:
        parts.append(np.asarray(c, float)); names_c.append(nm)
    parts.append(np.ones(len(rows))); names_c.append('const')
    Xb, lb = dummies([r['band'] for r in rows]); Xc, lc = dummies([r['entry_year'] for r in rows])
    Xp, lp = dummies([r['pos'] for r in rows])
    X = np.column_stack(parts + [Xb, Xc, Xp])
    names = names + names_c + ['band:%s' % b for b in lb] + ['coh:%s' % c for c in lc] + ['pos:%s' % p for p in lp]
    if fe_club_year:
        cy = ['%s|%s' % (r.get('draft_club'), r['focal_year']) for r in rows]
        Xf, lf = dummies(cy)
        # drop cohort dummies (collinear-ish with year in FE) keep them; pinv handles rank
        X = np.column_stack([X, Xf])
        names = names + ['cy:%s' % f for f in lf]
    return X, names

def fit_games(rows, y_key, gspec='linear', cluster_by_player=False, fe_club_year=False, extra=None):
    rows = [r for r in rows if r.get(y_key) is not None]
    y = np.array([r[y_key] for r in rows], float)
    G = np.array([r['games'] for r in rows], float)
    if gspec == 'linear':
        gc = ([G], ['games'])
    elif gspec == 'sqrt':
        gc = ([np.sqrt(G)], ['sqrt_games'])
    elif gspec == 'spline':
        gc = ([np.minimum(G, 5), np.clip(G - 5, 0, 5), np.clip(G - 10, 0, 5), np.maximum(G - 15, 0)],
              ['g_0_5', 'g_5_10', 'g_10_15', 'g_15p'])
    elif gspec == 'belowbar':
        below = np.array([1.0 if r['surplus'] < 0 else 0.0 for r in rows])
        gc = ([G, G * below, below], ['games', 'games_x_below', 'below'])
    else:
        raise ValueError(gspec)
    ex = []
    if extra:
        for nm in extra: ex.append((nm, [r[nm] for r in rows]))
    X, names = design(rows, gc, ex, fe_club_year=fe_club_year)
    cl = [r['key'] for r in rows] if cluster_by_player else None
    b, se, n, k, r2 = ols(X, y, cluster=cl)
    res = dict(n=n, k=k, r2=round(r2, 4), coef={})
    for i, nm in enumerate(names):
        if nm.startswith(('band:', 'coh:', 'pos:', 'cy:')): continue
        t = b[i] / se[i] if se[i] > 0 else float('nan')
        res['coef'][nm] = dict(b=float(b[i]), se=float(se[i]), t=float(t),
                               ci=[float(b[i] - 1.96 * se[i]), float(b[i] + 1.96 * se[i])])
    return res, rows

def cellspec(rows, y_key):
    """PREREG spec 1: demean y,G,S,age within entry_year x band x pos cells (n>=3), OLS on demeaned."""
    rows = [r for r in rows if r.get(y_key) is not None]
    cells = collections.defaultdict(list)
    for r in rows: cells[(r['entry_year'], r['band'], r['pos'])].append(r)
    used = {c: v for c, v in cells.items() if len(v) >= 3}
    dropped = sum(len(v) for c, v in cells.items() if len(v) < 3)
    Y, G, S, A = [], [], [], []
    for c, v in used.items():
        yv = np.array([r[y_key] for r in v]); gv = np.array([r['games'] for r in v])
        sv = np.array([r['surplus'] for r in v])
        av = np.array([r['age'] if r['age'] is not None else 19 + r['k'] for r in v])
        Y += list(yv - yv.mean()); G += list(gv - gv.mean()); S += list(sv - sv.mean()); A += list(av - av.mean())
    X = np.column_stack([G, S, A])
    b, se, n, k, r2 = ols(X, np.array(Y))
    # dof correction for absorbed cell means
    adj = math.sqrt(max(1, n - k) / max(1, n - k - len(used)))
    se = se * adj
    return dict(n=n, n_cells=len(used), dropped_small_cells=dropped, r2=round(r2, 4),
                games=dict(b=float(b[0]), se=float(se[0]), t=float(b[0] / se[0]),
                           ci=[float(b[0] - 1.96 * se[0]), float(b[0] + 1.96 * se[0])]),
                surplus_b=float(b[1]), age_b=float(b[2]))

def logit(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape
    def nll(b):
        z = X @ b
        return float(np.sum(np.logaddexp(0, z)) - y @ z)
    def grad(b):
        p = 1 / (1 + np.exp(-(X @ b)))
        return X.T @ (p - y)
    r = optimize.minimize(nll, np.zeros(k), jac=grad, method='L-BFGS-B', options=dict(maxiter=2000))
    b = r.x
    p = 1 / (1 + np.exp(-(X @ b)))
    W = p * (1 - p)
    H = (X * W[:, None]).T @ X
    Vi = np.linalg.pinv(H)
    se = np.sqrt(np.maximum(np.diag(Vi), 0))
    return b, se, r.success

def qreg(X, y, tau):
    """Quantile regression by LP (highs)."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    n, k = X.shape
    # vars: b (free, split +/-), u>=0, v>=0
    c = np.concatenate([np.zeros(2 * k), tau * np.ones(n), (1 - tau) * np.ones(n)])
    A_eq = np.hstack([X, -X, np.eye(n), -np.eye(n)])
    r = optimize.linprog(c, A_eq=A_eq, b_eq=y, bounds=[(0, None)] * (2 * k + 2 * n), method='highs')
    if not r.success: return None
    return r.x[:k] - r.x[k:2 * k]

# ================================================================ samples
K1 = [r for r in ROWS if r['k'] == 1]
K1Y5 = [r for r in K1 if r['y5'] is not None]
ALLK = ROWS

say('=' * 100)
say('S3 RESULTS — selection (season games) as a predictor of subsequent delivered value, at fixed output')
say('=' * 100)
gv = np.array([r['games'] for r in K1Y5]); yv = np.array([r['y5'] for r in K1Y5])
say('PRIMARY SAMPLE k=1 (rookie season), Y5 observable: n=%d | games mean %.1f sd %.1f terciles(%.0f,%.0f)'
    % (len(K1Y5), gv.mean(), gv.std(), np.percentile(gv, 33.34), np.percentile(gv, 66.67)))
say('Y5 (next-5yr delivered board pts, undiscounted): mean %.0f sd %.0f med %.0f q25 %.0f q75 %.0f  P(Y5=0)=%.3f'
    % (yv.mean(), yv.std(), np.median(yv), np.percentile(yv, 25), np.percentile(yv, 75), float(np.mean(yv == 0))))
t1, t2 = np.percentile(gv, 33.34), np.percentile(gv, 66.67)
OUT['sample'] = dict(n_k1=len(K1), n_k1_y5=len(K1Y5), terciles=[float(t1), float(t2)],
                     y5_mean=float(yv.mean()), y5_sd=float(yv.std()))

# ---------------------------------------------------------------- H1 primary
say(); say('--- H1: pooled spec (spec 2) — Y ~ games + surplus + age + band + cohort + pos ---')
tab = {}
for yk, samp, note in (('y1', K1, 'k=1, next-1yr'), ('y5', K1Y5, 'k=1, next-5yr'),
                       ('y5d', K1Y5, 'k=1, next-5yr disc-to-focal'),
                       ('yrc', [r for r in K1 if r['yrc'] is not None], 'k=1, rest-of-career RETIRED ONLY')):
    res, _ = fit_games(samp, yk)
    c = res['coef']['games']
    say('  %-38s n=%4d  games b=%8.2f  se=%6.2f  t=%6.2f  95%%CI [%8.2f, %8.2f]  R2=%.3f'
        % (note, res['n'], c['b'], c['se'], c['t'], c['ci'][0], c['ci'][1], res['r2']))
    tab[yk] = res
OUT['h1_pooled'] = tab

say(); say('--- H1: cell spec (spec 1) — within entry_year x band x pos cells, demeaned ---')
ct = {}
for yk, samp, note in (('y1', K1, 'k=1 next-1yr'), ('y5', K1Y5, 'k=1 next-5yr')):
    r = cellspec(samp, yk)
    g = r['games']
    say('  %-22s n=%4d cells=%3d (dropped n<3: %d)  games b=%8.2f se=%6.2f t=%6.2f CI [%8.2f, %8.2f]'
        % (note, r['n'], r['n_cells'], r['dropped_small_cells'], g['b'], g['se'], g['t'], g['ci'][0], g['ci'][1]))
    ct[yk] = r
OUT['h1_cell'] = ct

say(); say('--- H1 replication: pooled k=1..3, cluster-by-player; prior_games control added ---')
res, _ = fit_games([r for r in ALLK if r['y5'] is not None], 'y5', cluster_by_player=True, extra=['prior_games'])
c = res['coef']['games']; pgc = res['coef']['prior_games']
say('  k=1..3 Y5: n=%d  games b=%.2f se=%.2f t=%.2f CI [%.2f, %.2f] | prior_games b=%.2f (se %.2f)  R2=%.3f'
    % (res['n'], c['b'], c['se'], c['t'], c['ci'][0], c['ci'][1], pgc['b'], pgc['se'], res['r2']))
OUT['h1_pooled_k123'] = res

# ---------------------------------------------------------------- H2 shape
say(); say('--- H2: SHAPE (k=1, Y5) ---')
sh = {}
for spec in ('linear', 'sqrt', 'spline'):
    res, _ = fit_games(K1Y5, 'y5', gspec=spec)
    sh[spec] = res
    if spec == 'spline':
        seg = ['%s b=%.1f (se %.1f)' % (nm, res['coef'][nm]['b'], res['coef'][nm]['se'])
               for nm in ('g_0_5', 'g_5_10', 'g_10_15', 'g_15p')]
        say('  spline R2=%.4f  ' % res['r2'] + '  '.join(seg))
    else:
        nm = 'games' if spec == 'linear' else 'sqrt_games'
        say('  %-7s R2=%.4f  %s b=%.2f (se %.2f)' % (spec, res['r2'], nm, res['coef'][nm]['b'], res['coef'][nm]['se']))
OUT['h2_shape'] = sh
# tercile means (raw, and within surplus bands below)
say('  raw tercile means: ' + '  '.join('T%d(n=%d) Y5=%.0f' % (i + 1, len(ix), np.mean([K1Y5[j]['y5'] for j in ix]))
    for i, ix in enumerate([[j for j in range(len(K1Y5)) if (K1Y5[j]['games'] <= t1, t1 < K1Y5[j]['games'] <= t2, K1Y5[j]['games'] > t2)[i]] for i in range(3)])))

# ---------------------------------------------------------------- H5 below-bar
say(); say('--- H5: THE NEW-CHANNEL TEST — games slope within BELOW-BAR output stratum ---')
res, _ = fit_games(K1Y5, 'y5', gspec='belowbar')
cg, ci_, cb = res['coef']['games'], res['coef']['games_x_below'], res['coef']['below']
slope_below = cg['b'] + ci_['b']
# se of sum via refit on below-only subsample as well (cleaner, declared equivalent)
below_rows = [r for r in K1Y5 if r['surplus'] < 0]
res_b, _ = fit_games(below_rows, 'y5')
cbb = res_b['coef']['games']
say('  interaction spec: games b=%.2f (se %.2f) | games x below b=%.2f (se %.2f) -> below-bar slope %.2f'
    % (cg['b'], cg['se'], ci_['b'], ci_['se'], slope_below))
say('  below-bar-only refit (n=%d): games b=%.2f se=%.2f t=%.2f CI [%.2f, %.2f]'
    % (res_b['n'], cbb['b'], cbb['se'], cbb['t'], cbb['ci'][0], cbb['ci'][1]))
OUT['h5'] = dict(interaction=res, below_only=res_b, n_below=len(below_rows))

# ---------------------------------------------------------------- H4 channels
say(); say('--- H4: CHANNEL DECOMPOSITION (k=1) ---')
res_g, _ = fit_games(K1Y5, 'g5')
played = [r for r in K1Y5 if r['s5w'] is not None]
res_s, _ = fit_games(played, 's5w')
cgg = res_g['coef']['games']; css = res_s['coef']['games']
say('  future GAMES (sum yrs +1..+5):    games b=%.3f se=%.3f t=%.2f  (selection persists)' % (cgg['b'], cgg['se'], cgg['t']))
say('  future AVG-SURPLUS (games-wtd, played only n=%d): games b=%.4f se=%.4f t=%.2f' % (res_s['n'], css['b'], css['se'], css['t']))
OUT['h4'] = dict(future_games=res_g, future_surplus=res_s)

# ---------------------------------------------------------------- H3 bust
say(); say('--- H3: BUST TAIL ---')
def terc(g): return 0 if g <= t1 else (1 if g <= t2 else 2)
def sband(s): return 'S<0' if s < 0 else ('0<=S<10' if s < 10 else 'S>=10')
def pgrp(r):
    b = r['band']
    return b if b.startswith('ND') else 'POOL'
say('  P(Y5=0) by games tercile x surplus band x pedigree group   [tercile cuts: <=%.0f | <=%.0f | >%.0f]' % (t1, t2, t2))
bt = {}
for pg in ['ND1-10', 'ND11-20', 'ND21-30', 'ND31-40', 'ND41-64', 'ND>64', 'POOL']:
    for sb in ['S<0', '0<=S<10', 'S>=10']:
        cells = []
        for tt in range(3):
            v = [r['y5'] for r in K1Y5 if pgrp(r) == pg and sband(r['surplus']) == sb and terc(r['games']) == tt]
            cells.append((len(v), float(np.mean([x == 0 for x in v])) if v else None,
                          float(np.median(v)) if v else None))
        if sum(c[0] for c in cells) >= 8:
            say('    %-8s %-8s  ' % (pg, sb) + '  '.join(
                ('T%d n=%-3d P0=%s med=%s' % (i + 1, c[0], ('%.2f' % c[1]) if c[1] is not None else ' -- ',
                                              ('%6.0f' % c[2]) if c[2] is not None else '   -- ')) for i, c in enumerate(cells)))
            bt['%s|%s' % (pg, sb)] = cells
OUT['h3_bust_table'] = bt
# pooled all-pedigree by surplus band
say('  ALL pedigree pooled:')
for sb in ['S<0', '0<=S<10', 'S>=10']:
    cells = []
    for tt in range(3):
        v = [r['y5'] for r in K1Y5 if sband(r['surplus']) == sb and terc(r['games']) == tt]
        cells.append((len(v), float(np.mean([x == 0 for x in v])) if v else None, float(np.median(v)) if v else None))
    say('    ALL      %-8s  ' % sb + '  '.join('T%d n=%-3d P0=%s med=%s' % (i + 1, c[0],
        ('%.2f' % c[1]) if c[1] is not None else ' -- ', ('%6.0f' % c[2]) if c[2] is not None else '   -- ') for i, c in enumerate(cells)))
    bt['ALL|%s' % sb] = cells

# logistic
rows = K1Y5
y = np.array([1.0 if r['y5'] == 0 else 0.0 for r in rows])
G = np.array([r['games'] for r in rows], float)
X, names = design(rows, ([G], ['games']))
b, se, okc = logit(X, y)
i = names.index('games')
say('  logistic bust ~ games + controls: games b=%.4f se=%.4f  (odds ratio per game %.3f, per 7 games %.3f) conv=%s'
    % (b[i], se[i], math.exp(b[i]), math.exp(7 * b[i]), okc))
OUT['h3_logit'] = dict(b=float(b[i]), se=float(se[i]), or_per_game=float(math.exp(b[i])), converged=bool(okc))
# secondary threshold
y2 = np.array([1.0 if r['y5'] < 100 else 0.0 for r in rows])
b2, se2, okc2 = logit(X, y2)
say('  logistic (Y5<100 pts) ~ games + controls: games b=%.4f se=%.4f conv=%s' % (b2[i], se2[i], okc2))
OUT['h3_logit_100'] = dict(b=float(b2[i]), se=float(se2[i]), converged=bool(okc2))

# quantile regressions with pairs bootstrap
say(); say('--- H3b: QUANTILE EFFECTS (k=1, Y5) — pairs bootstrap B=150, seed 320317 ---')
yq = np.array([r['y5'] for r in rows], float)
qr = {}
for tau in (0.25, 0.50, 0.75):
    bq = qreg(X, yq, tau)
    boots = []
    for _ in range(150):
        ix = rng.integers(0, len(rows), len(rows))
        bb = qreg(X[ix], yq[ix], tau)
        if bb is not None: boots.append(bb[i])
    bs = np.array(boots)
    say('  q%.0f  games b=%.2f  boot-se=%.2f  CI [%.2f, %.2f]  (B ok=%d)'
        % (tau * 100, bq[i], bs.std(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(bs)))
    qr['q%d' % int(tau * 100)] = dict(b=float(bq[i]), se=float(bs.std()),
                                      ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))])
OUT['h3_quantile'] = qr

# ---------------------------------------------------------------- stability
say(); say('--- STABILITY (k=1, Y5, pooled spec games coefficient) ---')
stab = {}
def substab(label, subset):
    if len([r for r in subset if r['y5'] is not None]) < 40:
        say('  %-16s n<40 — reported, not fitted' % label); stab[label] = dict(n=len(subset)); return
    res, _ = fit_games(subset, 'y5')
    c = res['coef']['games']
    say('  %-16s n=%4d  b=%8.2f  se=%6.2f  t=%6.2f' % (label, res['n'], c['b'], c['se'], c['t']))
    stab[label] = dict(n=res['n'], b=c['b'], se=c['se'], t=c['t'])
for bnd in ['ND1-10', 'ND11-20', 'ND21-30', 'ND31-40', 'ND41-64', 'ND>64']:
    substab('band %s' % bnd, [r for r in K1Y5 if r['band'] == bnd])
substab('POOL pathways', [r for r in K1Y5 if not r['band'].startswith('ND')])
substab('era 2004-2012', [r for r in K1Y5 if r['entry_year'] <= 2012])
substab('era 2013-2021', [r for r in K1Y5 if r['entry_year'] >= 2013])
for pg in ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']:
    substab('pos %s' % pg, [r for r in K1Y5 if r['pos'] == pg])
OUT['stability'] = stab

# ---------------------------------------------------------------- opportunity confounder
say(); say('--- OPPORTUNITY CONFOUNDER: draft_club x focal_year FE (approx team-season; movers misattributed, undisclosed by store) ---')
res_fe, _ = fit_games(K1Y5, 'y5', fe_club_year=True)
c = res_fe['coef']['games']
say('  with club x year FE:    n=%d  games b=%.2f  se=%.2f  t=%.2f  CI [%.2f, %.2f]' %
    (res_fe['n'], c['b'], c['se'], c['t'], c['ci'][0], c['ci'][1]))
c0 = OUT['h1_pooled']['y5']['coef']['games']
say('  without (from above):   b=%.2f  se=%.2f' % (c0['b'], c0['se']))
OUT['confounder_fe'] = res_fe

# ---------------------------------------------------------------- named rows
say(); say('--- NAMED ROWS (read through the historical cells; their 2026 seasons are IN PROGRESS and teach nothing) ---')
NAMED = [dict(key='kye-annand', g=9, avg=59.8, pos='KPD', band='MSD', age=23),
         dict(key='lukas-cooke', g=2, avg=43.5, pos='KPD', band='MSD', age=23),
         dict(key='cooper-duff-tytler', g=13, avg=50.3, pos='KPF', band='ND1-10', age=19),
         dict(key='harry-dean', g=17, avg=59.7, pos='KPD', band='ND1-10', age=19),
         dict(key='milan-murdock', g=17, avg=70.1, pos='SF', band='SSP', age=26)]
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
bl = res_b['coef']['games']['b']    # below-bar slope (most named rows are below bar)
full = OUT['h1_pooled']['y5']['coef']['games']['b']
nm_out = {}
for nr in NAMED:
    s = nr['avg'] - BARS[nr['pos']]
    sb = sband(s); tt = terc(nr['g'])
    peer = [r for r in K1Y5 if sband(r['surplus']) == sb and (pgrp(r) == (nr['band'] if nr['band'].startswith('ND') else 'POOL'))]
    pv = [r['y5'] for r in peer]
    pt = [r['y5'] for r in peer if terc(r['games']) == tt]
    say('  %-20s g=%2d surplus %+6.1f (%s) band %-7s tercile T%d | cell n=%d P(Y5=0)=%s med=%s | same-tercile n=%d med=%s'
        % (nr['key'], nr['g'], s, sb, nr['band'], tt + 1, len(pv),
           ('%.2f' % np.mean([x == 0 for x in pv])) if pv else '--',
           ('%.0f' % np.median(pv)) if pv else '--', len(pt), ('%.0f' % np.median(pt)) if pt else '--'))
    nm_out[nr['key']] = dict(surplus=s, sband=sb, tercile=tt + 1, cell_n=len(pv),
                             cell_p0=float(np.mean([x == 0 for x in pv])) if pv else None,
                             cell_med=float(np.median(pv)) if pv else None,
                             same_terc_n=len(pt), same_terc_med=float(np.median(pt)) if pt else None)
say('  model-implied pair gaps (below-bar slope %.2f pts/game; full-sample %.2f pts/game):' % (bl, full))
say('    annand(9g) vs cooke(2g), same cell, both below bar: 7 games x %.2f = %+.0f Y5 pts' % (bl, 7 * bl))
OUT['named'] = nm_out

json.dump(OUT, open(os.path.join(HERE, 'RESULTS_S3.json'), 'w'), indent=1)
open(os.path.join(HERE, 'RESULTS_S3_out.txt'), 'w').write('\n'.join(LINES) + '\n')
say(); say('written RESULTS_S3.json / RESULTS_S3_out.txt')
