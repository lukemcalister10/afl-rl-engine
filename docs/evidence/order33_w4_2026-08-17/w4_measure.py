#!/usr/bin/env python3
"""ORDER 33 SEAT W4 -- STEP 2: the preregistered measurement.

Runs exactly the PREREG_W4.md analysis on W4_PANEL.json (built step 1). READ-ONLY.
Writes TRAJ_W4.json + MEASURE_W4_out.txt. No engine import needed here -- the panel carries points.

    L* : controls + best-convex-weighted level (w chosen on training rows, grid preregistered)
    T* : L* + one df, the age-adjusted last-2-season slope TRAJ
    primary target (a) Y1 next-season points; verdict O1/O2/O3/O4 per the prereg, no shopping.
"""
import os, json, math, hashlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ART = json.load(open(os.path.join(HERE, 'W4_PANEL.json')))
PANEL = ART['panel']; PAIRS = ART['pairs']; META = ART['meta']
SHRINK_K = float(META['shrink_k'])
NF = 5
WGRID = [round(0.1 * i, 1) for i in range(11)]
BOOT_B = 1000
BOOT_SEED = 0

_LOG = []
def P(s=''):
    print(s, flush=True)
    _LOG.append(str(s))

def fold_of(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % NF

# ==================================================================================================
# age curve machinery (identical construction to step 1; re-derivable on any subset of players)
# ==================================================================================================
def age_curve(pairs, field='delta'):
    by_a = collections.defaultdict(list); by_ap = collections.defaultdict(list)
    for q in pairs:
        by_a[q['ab']].append(q[field]); by_ap[(q['ab'], q['pos'])].append(q[field])
    allm = sum(x for v in by_a.values() for x in v) / max(1, sum(len(v) for v in by_a.values()))
    amean = {a: sum(v) / len(v) for a, v in by_a.items()}
    d = {}
    for (a, pos), v in by_ap.items():
        n = len(v); m = sum(v) / n
        d[(a, pos)] = (n * m + SHRINK_K * amean[a]) / (n + SHRINK_K)
    return d, amean, allm

def d_look(cur, ab, pos):
    d, amean, allm = cur
    return d.get((ab, pos), amean.get(ab, allm))

POSL = sorted(set(r['pos'] for r in PANEL))

def Lw_col(rows, w):
    out = np.empty(len(rows))
    for i, r in enumerate(rows):
        if r['has_prev2']:
            out[i] = (r['p0'] + w * r['p1'] + w * w * r['p2']) / (1.0 + w + w * w)
        else:
            out[i] = (r['p0'] + w * r['p1']) / (1.0 + w)
    return out

def traj_col(rows, curve, mode='2'):
    out = np.empty(len(rows))
    for i, r in enumerate(rows):
        if mode == '2':
            out[i] = r['delta'] - d_look(curve, r['ab'], r['pos'])
        elif mode == '3':
            out[i] = r['delta3'] - d_look(curve, r['ab'], r['pos'])
        elif mode == 'avg':
            out[i] = (r['avg0'] - r['avg1']) - d_look(curve, r['ab'], r['pos'])
    return out

def design(rows, w, traj=None, extra_year=False):
    n = len(rows)
    names = ['const']; cols = [np.ones(n)]
    for p in POSL[1:]:
        names.append('pos_' + p); cols.append(np.array([1.0 if r['pos'] == p else 0.0 for r in rows]))
    age = np.array([r['age'] for r in rows], float)
    names += ['age', 'age2', 'lg', 'games_at_Y']
    cols += [age, age ** 2, np.array([math.log1p(r['g']) for r in rows]),
             np.array([r['games_at_Y'] for r in rows], float)]
    L = Lw_col(rows, w)
    names += ['Lw', 'Lw2', 'Lw_age']; cols += [L, L ** 2, L * age]
    if extra_year:
        names.append('year'); cols.append(np.array([r['year'] for r in rows], float))
    if traj is not None:
        if isinstance(traj, tuple):        # sign split
            t = traj[0]
            names += ['TRAJ_pos', 'TRAJ_neg']; cols += [np.maximum(t, 0.0), np.minimum(t, 0.0)]
        else:
            names.append('TRAJ'); cols.append(traj)
    return names, np.column_stack(cols)

def standardise(Xtr, Xte):
    mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0)
    sd = np.where(sd < 1e-12, 1.0, sd)
    A = (Xtr - mu) / sd; B = (Xte - mu) / sd
    A[:, 0] = 1.0; B[:, 0] = 1.0
    return A, B, mu, sd

def ols(X, y):
    return np.linalg.lstsq(X, y, rcond=None)[0]

def spearman(a, b):
    """Tie-averaged, transcribed from o30bm_measure.py::spearman for fidelity."""
    def rank(x):
        order = np.argsort(x, kind='stable'); xs = np.asarray(x)[order]
        i = 0; rr = np.empty(len(x))
        while i < len(xs):
            j = i
            while j + 1 < len(xs) and xs[j + 1] == xs[i]:
                j += 1
            avg = (i + j) / 2.0
            for t in range(i, j + 1):
                rr[order[t]] = avg
            i = j + 1
        return rr
    ra, rb = rank(np.asarray(a)), rank(np.asarray(b))
    ra = ra - ra.mean(); rb = rb - rb.mean()
    den = math.sqrt(float((ra ** 2).sum()) * float((rb ** 2).sum()))
    return float((ra * rb).sum() / den) if den > 0 else 0.0

def cluster_se(X, y, b, keys):
    """CR1 cluster-robust SEs."""
    n, k = X.shape
    e = y - X @ b
    XtXi = np.linalg.pinv(X.T @ X)
    groups = collections.defaultdict(list)
    for i, kk in enumerate(keys):
        groups[kk].append(i)
    meat = np.zeros((k, k))
    for idx in groups.values():
        s = X[idx].T @ e[idx]
        meat += np.outer(s, s)
    G = len(groups)
    c = (G / (G - 1)) * ((n - 1) / (n - k))
    V = c * XtXi @ meat @ XtXi
    return np.sqrt(np.diag(V))

# ==================================================================================================
# the CV harness (player-clustered folds; d and w chosen on training rows only)
# ==================================================================================================
def cv_compare(rows, target, traj_mode='2', pair_filter=None, extra_year=False, wgrid=WGRID,
               curve_field='delta', label=''):
    y = np.array([r[target] for r in rows], float)
    keys = [r['key'] for r in rows]
    fo = np.array([fold_of(k) for k in keys])
    predL = np.zeros(len(y)); predT = np.zeros(len(y))
    per = []; wstars = []; gsigns = []
    for k in range(NF):
        te = fo == k; tr = ~te
        trk = set(np.array(keys)[tr])
        prs = [q for q in PAIRS if q['key'] in trk]
        if pair_filter:
            prs = [q for q in prs if pair_filter(q)]
        curve = age_curve(prs, curve_field)
        rtr = [r for r, m in zip(rows, tr) if m]; rte = [r for r, m in zip(rows, te) if m]
        # pick w on TRAINING rows, level family only
        best = None
        for w in wgrid:
            _, X = design(rtr, w, extra_year=extra_year)
            A = standardise(X, X)[0]
            b = ols(A, y[tr]); rms = float(np.sqrt(((y[tr] - A @ b) ** 2).mean()))
            if best is None or rms < best[1]:
                best = (w, rms)
        wstar = best[0]; wstars.append(wstar)
        namesL, XtrL = design(rtr, wstar, extra_year=extra_year)
        _, XteL = design(rte, wstar, extra_year=extra_year)
        A, B, _, _ = standardise(XtrL, XteL)
        bL = ols(A, y[tr]); predL[te] = B @ bL
        ttr = traj_col(rtr, curve, traj_mode); tte = traj_col(rte, curve, traj_mode)
        namesT, XtrT = design(rtr, wstar, traj=ttr, extra_year=extra_year)
        _, XteT = design(rte, wstar, traj=tte, extra_year=extra_year)
        A, B, _, _ = standardise(XtrT, XteT)
        bT = ols(A, y[tr]); predT[te] = B @ bT
        gsigns.append(float(np.sign(bT[namesT.index('TRAJ')])))
        eL = y[te] - predL[te]; eT = y[te] - predT[te]
        per.append(dict(fold=k, n=int(te.sum()), w=wstar,
                        rmsL=float(np.sqrt((eL ** 2).mean())), rmsT=float(np.sqrt((eT ** 2).mean())),
                        traj_coef_sign=gsigns[-1]))
    eL = y - predL; eT = y - predT
    rmsL = float(np.sqrt((eL ** 2).mean())); rmsT = float(np.sqrt((eT ** 2).mean()))
    red = (rmsL - rmsT) / rmsL
    wins = sum(1 for p in per if p['rmsT'] < p['rmsL'])
    # rank movement between the two predictions
    pctL = np.argsort(np.argsort(predL)) / (len(y) - 1.0)
    pctT = np.argsort(np.argsort(predT)) / (len(y) - 1.0)
    out = dict(label=label, n=len(y), n_players=len(set(keys)),
               rms_L=rmsL, rms_T=rmsT, rms_reduction=red, folds_won_by_T=wins,
               mae_L=float(np.abs(eL).mean()), mae_T=float(np.abs(eT).mean()),
               spearman_L=spearman(y, predL), spearman_T=spearman(y, predT),
               mean_abs_rank_move_pct=float(np.abs(pctL - pctT).mean() * 100.0),
               w_by_fold=wstars, traj_sign_by_fold=gsigns,
               sign_stable_folds=int(max(sum(1 for s in gsigns if s > 0), sum(1 for s in gsigns if s < 0))),
               folds=per)
    return out

def full_fit(rows, target, traj_mode='2', pair_filter=None, extra_year=False, sign_split=False,
             wgrid=WGRID, curve_field='delta'):
    """Full-sample fit, full-panel d, w* by training RMS on all rows; CR1 SEs; bootstrap CI."""
    y = np.array([r[target] for r in rows], float)
    keys = [r['key'] for r in rows]
    prs = PAIRS if pair_filter is None else [q for q in PAIRS if pair_filter(q)]
    curve = age_curve(prs, curve_field)
    best = None
    for w in wgrid:
        _, X = design(rows, w, extra_year=extra_year)
        A = standardise(X, X)[0]
        b = ols(A, y); rms = float(np.sqrt(((y - A @ b) ** 2).mean()))
        if best is None or rms < best[1]:
            best = (w, rms)
    wstar = best[0]
    t = traj_col(rows, curve, traj_mode)
    traj_arg = (t,) if sign_split else t
    names, X = design(rows, wstar, traj=traj_arg, extra_year=extra_year)
    A, _, mu, sd = standardise(X, X)
    b = ols(A, y)
    se = cluster_se(A, y, b, keys)
    res = dict(w_star=wstar, n=len(y), n_players=len(set(keys)), names=names,
               traj_sd=float(t.std()))
    tgt_names = ['TRAJ_pos', 'TRAJ_neg'] if sign_split else ['TRAJ']
    for nm in tgt_names:
        i = names.index(nm)
        beta_std = float(b[i])                       # points of target per 1 SD of the column
        raw_sd = float(sd[i])
        res[nm] = dict(beta_per_sd=beta_std, se_per_sd=float(se[i]),
                       t=float(b[i] / se[i]) if se[i] > 0 else 0.0,
                       beta_raw=beta_std / raw_sd if raw_sd > 0 else 0.0,
                       col_sd=raw_sd)
    res['_internals'] = (names, A, y, keys, t, wstar, curve)
    return res

def boot_beta(rows, target, res, B=BOOT_B, seed=BOOT_SEED, tgt='TRAJ'):
    """Player-cluster bootstrap of the TRAJ coefficient (w*, d fixed at full-sample values)."""
    names, A, y, keys, t, wstar, curve = res['_internals']
    i = names.index(tgt)
    ky = sorted(set(keys))
    idx_of = collections.defaultdict(list)
    for j, k in enumerate(keys):
        idx_of[k].append(j)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(B):
        pick = rng.choice(len(ky), size=len(ky), replace=True)
        idx = np.concatenate([np.array(idx_of[ky[p]], int) for p in pick])
        b = ols(A[idx], y[idx])
        out.append(float(b[i]))
    lo, hi = np.percentile(out, [2.5, 97.5])
    return dict(B=B, seed=seed, ci95_per_sd=[float(lo), float(hi)],
                boot_sd=float(np.std(out)))

# ==================================================================================================
# quantile regression (pinball LP, HiGHS)
# ==================================================================================================
from scipy.optimize import linprog
import scipy.sparse as sp

def quantreg(A, y, q):
    n, k = A.shape
    c = np.concatenate([np.zeros(k), q * np.ones(n), (1 - q) * np.ones(n)])
    Aeq = sp.hstack([sp.csr_matrix(A), sp.eye(n), -sp.eye(n)], format='csr')
    bounds = [(None, None)] * k + [(0, None)] * (2 * n)
    r = linprog(c, A_eq=Aeq, b_eq=y, bounds=bounds, method='highs')
    assert r.status == 0, 'LP failed'
    return r.x[:k]

# ==================================================================================================
# RUN -- PRIMARY
# ==================================================================================================
P('=' * 100)
P('ORDER 33 W4 STEP 2 -- THE MEASUREMENT (prereg PREREG_W4.md; store %s)' % META['store_md5'][:8])
P('=' * 100)

RES = dict(meta=dict(store_md5=META['store_md5'], nf=NF, wgrid=WGRID, boot=[BOOT_B, BOOT_SEED]))

ROWS_A = [r for r in PANEL if 'Y1' in r]
ROWS_B = [r for r in PANEL if 'R3' in r]
ROWS_C = [r for r in PANEL if 'R6' in r]

P('')
P('PRIMARY -- target (a) next-season points Y1, n=%d states / %d players'
  % (len(ROWS_A), len(set(r['key'] for r in ROWS_A))))
cvA = cv_compare(ROWS_A, 'Y1', label='a:Y1')
P('  held-out:  L* rms %.2f  |  T* rms %.2f  |  reduction %+.3f%%  |  folds won by T %d/5'
  % (cvA['rms_L'], cvA['rms_T'], 100 * cvA['rms_reduction'], cvA['folds_won_by_T']))
P('  spearman:  L* %.4f   T* %.4f    mean |rank move| %.2f percentile points'
  % (cvA['spearman_L'], cvA['spearman_T'], cvA['mean_abs_rank_move_pct']))
P('  w* by fold: %s   TRAJ coefficient sign by fold: %s (stable in %d/5)'
  % (cvA['w_by_fold'], ['+' if s > 0 else '-' for s in cvA['traj_sign_by_fold']], cvA['sign_stable_folds']))
for p in cvA['folds']:
    P('    fold %d  n=%4d  w*=%.1f  rms L %.2f  T %.2f  %s'
      % (p['fold'], p['n'], p['w'], p['rmsL'], p['rmsT'], 'T wins' if p['rmsT'] < p['rmsL'] else 'L wins'))

ffA = full_fit(ROWS_A, 'Y1')
btA = boot_beta(ROWS_A, 'Y1', ffA)
tr = ffA['TRAJ']
P('')
P('  full-sample fit (w*=%.1f): TRAJ beta %+.2f points of next season per 1 SD of TRAJ (SD=%.1f pts of slope)'
  % (ffA['w_star'], tr['beta_per_sd'], tr['col_sd']))
P('    cluster-robust t = %+.2f   (CR1, %d player clusters)' % (tr['t'], ffA['n_players']))
P('    per +100 points of raw age-adjusted slope: %+.2f points of next season' % (100 * tr['beta_raw']))
P('    player-bootstrap 95%% CI (B=%d, seed %d): [%+.2f, %+.2f] per SD'
  % (btA['B'], btA['seed'], btA['ci95_per_sd'][0], btA['ci95_per_sd'][1]))

# verdict per prereg
red_ok = cvA['rms_reduction'] >= 0.02 and cvA['folds_won_by_T'] >= 4
t_ok = abs(tr['t']) >= 3.0
sign_ok = cvA['sign_stable_folds'] >= 4
heldout_ok = cvA['rms_reduction'] > 0
if red_ok:
    verdict = 'O1 ADOPTION-GRADE OVERTURN'
elif t_ok and sign_ok and heldout_ok:
    verdict = 'O2 REAL-BUT-SMALL SIGNAL (does NOT clear the adoption bar)'
elif not t_ok:
    verdict = 'O3 NULL CONFIRMED'
else:
    verdict = 'O4 AMBIGUOUS -- NULL STANDS'
P('')
P('  VERDICT (preregistered rule): %s' % verdict)
ffA.pop('_internals')
RES['primary'] = dict(cv=cvA, full=ffA, boot=btA, verdict=verdict)

# ==================================================================================================
# SECONDARY TARGETS
# ==================================================================================================
P('')
P('SECONDARY -- target (b) R3 3yr discounted, n=%d; target (c) R6 6yr discounted (ORIGINAL), n=%d'
  % (len(ROWS_B), len(ROWS_C)))
sec = {}
for lab, rows, tg in (('b:R3', ROWS_B, 'R3'), ('c:R6', ROWS_C, 'R6')):
    cvx = cv_compare(rows, tg, label=lab)
    ffx = full_fit(rows, tg)
    btx = boot_beta(rows, tg, ffx)
    ffx.pop('_internals')
    tx = ffx['TRAJ']
    P('  %s: L* rms %.1f T* rms %.1f (%+.3f%%, %d/5 folds)  TRAJ beta/SD %+.1f  t=%+.2f  CI [%+.1f,%+.1f]'
      % (lab, cvx['rms_L'], cvx['rms_T'], 100 * cvx['rms_reduction'], cvx['folds_won_by_T'],
         tx['beta_per_sd'], tx['t'], btx['ci95_per_sd'][0], btx['ci95_per_sd'][1]))
    sec[lab] = dict(cv=cvx, full=ffx, boot=btx)
RES['secondary_targets'] = sec

# ==================================================================================================
# SECONDARY READS on target (a)
# ==================================================================================================
P('')
P('READ 1 -- QUANTILE REGRESSION at q10/q50/q90 (pinball LP), target (a), full sample, w*=%.1f' % ffA['w_star'])
prs_curve = age_curve(PAIRS)
tA = traj_col(ROWS_A, prs_curve)
yA = np.array([r['Y1'] for r in ROWS_A], float)
keysA = [r['key'] for r in ROWS_A]
namesQ, XQ = design(ROWS_A, ffA['w_star'], traj=tA)
AQ, _, muQ, sdQ = standardise(XQ, XQ)
iT = namesQ.index('TRAJ')
qres = {}
ky = sorted(set(keysA)); idx_of = collections.defaultdict(list)
for j, k in enumerate(keysA):
    idx_of[k].append(j)
BQ = 200          # AMENDMENT A1 (filed in PREREG_W4.md before this run): quantile LP bootstrap only
rngq = np.random.default_rng(BOOT_SEED)
for q in (0.10, 0.50, 0.90):
    bq = quantreg(AQ, yA, q)
    boots = []
    for _ in range(BQ):
        pick = rngq.choice(len(ky), size=len(ky), replace=True)
        idx = np.concatenate([np.array(idx_of[ky[p]], int) for p in pick])
        boots.append(float(quantreg(AQ[idx], yA[idx], q)[iT]))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    qres['q%02d' % int(q * 100)] = dict(beta_per_sd=float(bq[iT]), ci95=[float(lo), float(hi)], B=BQ)
    P('  q%.0f: TRAJ beta %+.2f points per SD   bootstrap 95%% CI [%+.2f, %+.2f]'
      % (q * 100, bq[iT], lo, hi))
RES['quantiles'] = qres

P('')
P('READ 2 -- SIGN ASYMMETRY (improvers vs decliners), target (a), full sample, cluster SEs')
ffS = full_fit(ROWS_A, 'Y1', sign_split=True)
for nm in ('TRAJ_pos', 'TRAJ_neg'):
    btS = boot_beta(ROWS_A, 'Y1', ffS, tgt=nm)
    x = ffS[nm]
    P('  %s: beta %+.2f per SD of the column  t=%+.2f  CI [%+.2f, %+.2f]'
      % (nm, x['beta_per_sd'], x['t'], btS['ci95_per_sd'][0], btS['ci95_per_sd'][1]))
    ffS[nm]['boot'] = btS
ffS.pop('_internals')
RES['sign_split'] = ffS

P('')
P('READ 3 -- THE OWNER-READABLE SORT: within age-band x level-quintile, TRAJ terciles (within cell)')
LwA = Lw_col(ROWS_A, ffA['w_star'])
def abland(a):
    return '<=19' if a <= 19 else ('20-21' if a <= 21 else ('22-23' if a <= 23 else
           ('24-25' if a <= 25 else ('26-28' if a <= 28 else '29+'))))
ABL = ['<=19', '20-21', '22-23', '24-25', '26-28', '29+']
qs = np.percentile(LwA, [20, 40, 60, 80])
def lq(v):
    return int(np.searchsorted(qs, v, side='right')) + 1
cells = collections.defaultdict(list)
for i, r in enumerate(ROWS_A):
    cells[(abland(r['age']), lq(LwA[i]))].append(i)
def disp(idx):
    v = yA[idx]
    return dict(n=len(idx), mean=float(v.mean()), median=float(np.median(v)),
                p25=float(np.percentile(v, 25)), p75=float(np.percentile(v, 75)),
                exit_rate=float(np.mean([0.0 if ROWS_A[i]['Y1_played'] else 1.0 for i in idx])),
                mean_R3=float(np.mean([ROWS_A[i].get('R3') for i in idx
                                       if ROWS_A[i].get('R3') is not None] or [float('nan')])))
tbl = {}
gapsY1 = []; gapw = []
P('  %-6s L-qnt %5s | T1(fall) meanY1 exit%% | T2 meanY1 | T3(rise) meanY1 exit%% | T3-T1 gap' % ('age', 'n'))
for ab in ABL:
    for q5 in range(1, 6):
        idx = cells.get((ab, q5))
        if not idx or len(idx) < 9:
            if idx:
                tbl['%s|Q%d' % (ab, q5)] = dict(n=len(idx), thin=True)
            continue
        v = tA[np.array(idx)]
        t1, t2 = np.percentile(v, [100 / 3, 200 / 3])
        g1 = [i for i, x in zip(idx, v) if x <= t1]
        g3 = [i for i, x in zip(idx, v) if x > t2]
        g2 = [i for i, x in zip(idx, v) if t1 < x <= t2]
        d1, d2, d3 = disp(np.array(g1)), disp(np.array(g2)), disp(np.array(g3))
        gap = d3['mean'] - d1['mean']
        gapsY1.append(gap * len(idx)); gapw.append(len(idx))
        tbl['%s|Q%d' % (ab, q5)] = dict(T1=d1, T2=d2, T3=d3, gap_T3_T1=gap)
        P('  %-6s   Q%d  %5d |  %7.0f  %4.0f%%      | %7.0f   |  %7.0f  %4.0f%%       | %+7.0f'
          % (ab, q5, len(idx), d1['mean'], 100 * d1['exit_rate'], d2['mean'],
             d3['mean'], 100 * d3['exit_rate'], gap))
POOLGAP = sum(gapsY1) / sum(gapw)
P('  pooled n-weighted within-cell T3-T1 gap in mean next-season points: %+.1f' % POOLGAP)
# bootstrap the pooled gap by player
rng = np.random.default_rng(BOOT_SEED)
kyA = sorted(set(keysA))
idx_by_key = collections.defaultdict(list)
for j, k in enumerate(keysA):
    idx_by_key[k].append(j)
bg = []
for _ in range(BOOT_B):
    pick = rng.choice(len(kyA), size=len(kyA), replace=True)
    sel = np.concatenate([np.array(idx_by_key[kyA[p]], int) for p in pick])
    cc = collections.defaultdict(list)
    for i in sel:
        cc[(abland(ROWS_A[i]['age']), lq(LwA[i]))].append(i)
    num = den = 0.0
    for idx in cc.values():
        if len(idx) < 9:
            continue
        v = tA[np.array(idx)]
        t1, t2 = np.percentile(v, [100 / 3, 200 / 3])
        y1 = yA[[i for i, x in zip(idx, v) if x <= t1]]
        y3 = yA[[i for i, x in zip(idx, v) if x > t2]]
        if len(y1) and len(y3):
            num += (y3.mean() - y1.mean()) * len(idx); den += len(idx)
    if den:
        bg.append(num / den)
lo, hi = np.percentile(bg, [2.5, 97.5])
P('  player-bootstrap 95%% CI on the pooled gap: [%+.1f, %+.1f]  (B=%d)' % (lo, hi, BOOT_B))
RES['sort_table'] = dict(cells=tbl, pooled_gap=POOLGAP, pooled_gap_ci95=[float(lo), float(hi)])

P('')
P('READ 4 -- AGE LOCALISATION, target (a), separate full fits, cluster SEs')
agecells = {'<=21': lambda r: r['age'] <= 21, '22-25': lambda r: 22 <= r['age'] <= 25,
            '26-28': lambda r: 26 <= r['age'] <= 28, '29+': lambda r: r['age'] >= 29}
aged = {}
for lab in ('<=21', '22-25', '26-28', '29+'):
    rows = [r for r in ROWS_A if agecells[lab](r)]
    ff = full_fit(rows, 'Y1')
    bt = boot_beta(rows, 'Y1', ff)
    ff.pop('_internals')
    x = ff['TRAJ']
    P('  age %-6s n=%5d  TRAJ beta %+.2f/SD  t=%+.2f  CI [%+.2f, %+.2f]'
      % (lab, ff['n'], x['beta_per_sd'], x['t'], bt['ci95_per_sd'][0], bt['ci95_per_sd'][1]))
    aged[lab] = dict(full=ff, boot=bt)
RES['age_local'] = aged

# ==================================================================================================
# SENSITIVITIES (preregistered list; none replaces the primary)
# ==================================================================================================
P('')
P('SENSITIVITIES')
sens = {}

rows_s1 = [r for r in ROWS_A if r['g0'] >= 6 and r['g1'] >= 6]
pf1 = lambda q: q['g_now'] >= 6 and q['g_prev'] >= 6
for q in PAIRS:
    q['davg'] = q['avg_now'] - q['avg_prev']
cv1 = cv_compare(rows_s1, 'Y1', traj_mode='avg', pair_filter=pf1, curve_field='davg', label='s1')
ff1 = full_fit(rows_s1, 'Y1', traj_mode='avg', pair_filter=pf1, curve_field='davg'); ff1.pop('_internals')
P('  s1 raw-avg slope, games>=6 both seasons: n=%d  red %+.3f%% (%d/5)  t=%+.2f'
  % (cv1['n'], 100 * cv1['rms_reduction'], cv1['folds_won_by_T'], ff1['TRAJ']['t']))
sens['s1'] = dict(cv=cv1, full=ff1)

rows_s2 = [r for r in ROWS_A if r['has_prev2'] and r['delta3'] is not None]
# d3 curve: estimated from panel triples themselves (they are exactly the has_prev2 pairs set)
TRIP = [dict(key=r['key'], ab=r['ab'], pos=r['pos'], delta=r['delta3']) for r in PANEL
        if r['has_prev2'] and r['delta3'] is not None]
_savePAIRS = PAIRS
PAIRS = TRIP
cv2 = cv_compare(rows_s2, 'Y1', traj_mode='3', label='s2')
ff2 = full_fit(rows_s2, 'Y1', traj_mode='3'); ff2.pop('_internals')
PAIRS = _savePAIRS
P('  s2 3-season slope: n=%d  red %+.3f%% (%d/5)  t=%+.2f'
  % (cv2['n'], 100 * cv2['rms_reduction'], cv2['folds_won_by_T'], ff2['TRAJ']['t']))
sens['s2'] = dict(cv=cv2, full=ff2)

rows_s3 = [r for r in ROWS_C if r['typ'] == 'ND' and r['pick'] and 1 <= r['pick'] <= 64
           and r['entry_year'] and r['entry_year'] >= 2005]
cv3 = cv_compare(rows_s3, 'R6', label='s3')
ff3 = full_fit(rows_s3, 'R6'); ff3.pop('_internals')
P('  s3 ND 1-64 entry>=2005, target (c) R6 [the original panel shape]: n=%d  red %+.3f%% (%d/5)  t=%+.2f'
  % (cv3['n'], 100 * cv3['rms_reduction'], cv3['folds_won_by_T'], ff3['TRAJ']['t']))
sens['s3'] = dict(cv=cv3, full=ff3)

for lab, cond in (('<=2014', lambda r: r['year'] <= 2014), ('>=2015', lambda r: r['year'] >= 2015)):
    rows = [r for r in ROWS_A if cond(r)]
    cvx = cv_compare(rows, 'Y1', label='s4' + lab)
    ffx = full_fit(rows, 'Y1'); ffx.pop('_internals')
    P('  s4 era %s: n=%d  red %+.3f%% (%d/5)  t=%+.2f'
      % (lab, cvx['n'], 100 * cvx['rms_reduction'], cvx['folds_won_by_T'], ffx['TRAJ']['t']))
    sens['s4' + lab] = dict(cv=cvx, full=ffx)

wg5 = [round(0.05 * i, 2) for i in range(21)]
cv5 = cv_compare(ROWS_A, 'Y1', wgrid=wg5, label='s5')
P('  s5 finer w-grid (0.05): red %+.3f%% (%d/5)  w* by fold %s'
  % (100 * cv5['rms_reduction'], cv5['folds_won_by_T'], cv5['w_by_fold']))
sens['s5'] = dict(cv=cv5)

cv6 = cv_compare(ROWS_A, 'Y1', extra_year=True, label='s6')
ff6 = full_fit(ROWS_A, 'Y1', extra_year=True); ff6.pop('_internals')
P('  s6 + year control: red %+.3f%% (%d/5)  t=%+.2f'
  % (100 * cv6['rms_reduction'], cv6['folds_won_by_T'], ff6['TRAJ']['t']))
sens['s6'] = dict(cv=cv6, full=ff6)

RES['sensitivities'] = sens

P('')
P('FINAL PREREGISTERED VERDICT ON THE PRIMARY: %s' % verdict)

json.dump(RES, open(os.path.join(HERE, 'TRAJ_W4.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'MEASURE_W4_out.txt'), 'w').write('\n'.join(_LOG) + '\n')
P('wrote TRAJ_W4.json + MEASURE_W4_out.txt')
