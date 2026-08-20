#!/usr/bin/env python3
"""ORDER P STEP 2 — THE PEDIGREE-CONDITIONAL EXPECTATION, MEASURED FROM OUTCOMES. READ-ONLY.

PREREG_P.md sections 3.3, 3.4 and 4. Nothing here reads a board price except v0, which is the
pedigree label (bound P-F3). The delivered-value ruler is the house one, reused whole and
md5-asserted. The age bar is the engine's own, asserted against its literal.

  usage: OPENBLAS_NUM_THREADS=1 ... python op_step2.py
"""
import json, math, os, sys, collections
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_BOOT = 32, 2000
AGE_MAX = 22
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


def partial_spear(x, y, z):
    rx, ry, rz = rankdata(x), rankdata(y), rankdata(z)
    Z = np.column_stack([np.ones(len(rz)), rz])
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    d = math.sqrt((ex ** 2).sum() * (ey ** 2).sum())
    return float((ex * ey).sum() / d) if d > 0 else float('nan')


def cluster_boot(fn, keys, rng, B=B_BOOT):
    """Resample PLAYERS, not rows. ORDER N's own routine, same B, same seed."""
    uk = sorted(set(keys))
    idx_by = collections.defaultdict(list)
    for i, k in enumerate(keys):
        idx_by[k].append(i)
    out = []
    nu = len(uk)
    for _ in range(B):
        pick = rng.integers(0, nu, size=nu)
        idx = []
        for j in pick:
            idx.extend(idx_by[uk[j]])
        v = fn(np.array(idx))
        if v is not None and np.isfinite(v):
            out.append(v)
    if not out:
        return (float('nan'), float('nan'))
    a = np.array(out)
    return (float(np.percentile(a, 5)), float(np.percentile(a, 95)))


P('=' * 118)
P('ORDER P — STEP 2. THE PEDIGREE-CONDITIONAL EXPECTATION, AND WHAT SURPLUS AGAINST IT PREDICTS')
P('=' * 118)
P('prereg : PREREG_P.md, pushed at 5911796 before any number in this file existed')
P('ruler  : the house S4 delivered-value ruler, md5 %s  (falsifier P3 clear)' % LB.check_s4_copy())
P('age bar: S1 C3, asserted against the engine literal O32_GATE_DELTA  (falsifier P2 clear)')
P('NOTHING HERE READS A BOARD PRICE EXCEPT v0, WHICH IS THE PEDIGREE LABEL.')
P()

M = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(M)
P('-' * 118)
P('0 · THE POPULATION THE SURFACE IS MEASURED ON')
P('-' * 118)
P('   season rows with games>0, played at age 18-23, entrants 2005+, position in the ruler\'s six')
P('   groups, season <= %d, force-majeure keys excluded.' % LB.LAST_REAL_SEASON)
P('   rows %d   players %d   games %.0f' % (
    len(ROWS), len(set(r['key'] for r in ROWS)), sum(r['games'] for r in ROWS)))
byca = collections.Counter((r['cls'], r['age']) for r in ROWS)
P('   %-8s' % 'age' + ''.join('%7d' % a for a in range(18, 24)))
for cls in ('TALL', 'SMALL'):
    P('   %-8s' % cls + ''.join('%7d' % byca[(cls, a)] for a in range(18, 24)))
P()

# ---- Q1 · THE SURFACE --------------------------------------------------------------------------------
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)
PG_RAW = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=False)
P('-' * 118)
P('Q1 · THE PEDIGREE PREMIUM. How far above his AGE bar a player priced at v0 actually produces.')
P('-' * 118)
P('   estimator: games-weighted local-linear kernel regression on ln(v0), tricube, H = %.2f log-v0' % PB.H_PRIMARY)
P('              units. The same estimator family par_build.py used over log-pick at H = 0.40.')
P('   the fit is evaluated over the 1st-99th percentile of ln(v0) and HELD FLAT outside it.')
P('   ESS is the effective sample size of the kernel at that point. A cell under %.0f is THIN.' % PB.ESS_THIN)
P()
ANCH = [50, 100, 150, 200, 300, 450, 600, 900, 1200, 1700, 2400, 3200]
P('   %10s | %-34s | %-34s' % ('v0', 'SMALL  (MID, SD, SF)', 'TALL  (KPD, KPF, RUCK)'))
P('   %10s | %9s %9s %8s %5s | %9s %9s %8s %5s' % (
    '', 'PG raw', 'PG iso', 'ESS', 'thin', 'PG raw', 'PG iso', 'ESS', 'thin'))
SURF = {}
for v in ANCH:
    x = math.log(v)
    row = dict(v0=v)
    cells = []
    for cls in ('SMALL', 'TALL'):
        gx, gy = PG.grid[cls]
        xc = min(max(x, gx[0]), gx[-1])
        i = int(np.argmin(np.abs(gx - xc)))
        pr = float(np.interp(xc, gx, PG_RAW.grid[cls][1]))
        pi = PG.at(x, cls)
        ess = float(PG.ess[cls][i])
        oos = '' if (gx[0] <= x <= gx[-1]) else ' held'
        cells.append((pr, pi, ess, ('THIN' if ess < PB.ESS_THIN else '-') + oos))
        row[cls] = dict(raw=pr, iso=pi, ess=ess, in_support=bool(gx[0] <= x <= gx[-1]))
    P('   %10d | %+9.2f %+9.2f %8.0f %5s | %+9.2f %+9.2f %8.0f %5s' % (
        v, cells[0][0], cells[0][1], cells[0][2], cells[0][3],
        cells[1][0], cells[1][1], cells[1][2], cells[1][3]))
    SURF[v] = row
P()
for cls in ('SMALL', 'TALL'):
    gx, gy = PG.grid[cls]
    nd = int(np.sum(np.diff(PG_RAW.grid[cls][1]) < -1e-9))
    P('   %-6s support ln(v0) [%.3f, %.3f] = v0 [%.0f, %.0f]; %d of %d raw grid steps were DECREASING '
      'and were isotonised.' % (cls, gx[0], gx[-1], math.exp(gx[0]), math.exp(gx[-1]), nd, len(gx) - 1))
    md = float(np.max(np.abs(PG_RAW.grid[cls][1] - gy)))
    P('          largest raw-vs-isotonised gap on the grid: %.3f points per game.' % md)
P()

# spread + falsifiers P4 / P5
P('   THE SPREAD, WITH A CLUSTER BOOTSTRAP ON PLAYER (%d resamples, seed %d). Falsifiers P4 and P5.' % (B_BOOT, SEED))
P('   %-7s %-34s %-30s' % ('class', 'PG(v0 p90) - PG(v0 p10)', 'PG at the median v0'))
SPREAD = {}
allv0 = np.array([r['v0'] for r in ROWS])
X10, X90 = math.log(np.percentile(allv0, 10)), math.log(np.percentile(allv0, 90))
X50 = math.log(np.percentile(allv0, 50))
for cls in ('SMALL', 'TALL'):
    sub = [r for r in ROWS if r['cls'] == cls]
    xs = np.array([r['x'] for r in sub]); ys = np.array([r['d'] for r in sub])
    ws = np.array([r['games'] for r in sub]); ky = [r['key'] for r in sub]

    def spr(i, xs=xs, ys=ys, ws=ws):
        a, _ = PB.loclin(X90, xs[i], ys[i], ws[i], PB.H_PRIMARY)
        b, _ = PB.loclin(X10, xs[i], ys[i], ws[i], PB.H_PRIMARY)
        return a - b

    def med(i, xs=xs, ys=ys, ws=ws):
        a, _ = PB.loclin(X50, xs[i], ys[i], ws[i], PB.H_PRIMARY)
        return a

    s0 = spr(np.arange(len(sub))); cs = cluster_boot(spr, ky, np.random.default_rng(SEED))
    m0 = med(np.arange(len(sub))); cm = cluster_boot(med, ky, np.random.default_rng(SEED))
    P('   %-7s %+8.2f  [%+.2f, %+.2f]           %+8.2f  [%+.2f, %+.2f]' % (cls, s0, cs[0], cs[1], m0, cm[0], cm[1]))
    SPREAD[cls] = dict(spread=s0, ci=cs, at_median=m0, ci_median=cm)
P('   v0 p10 = %.0f, p50 = %.0f, p90 = %.0f over the %d season rows.' % (
    math.exp(X10), math.exp(X50), math.exp(X90), len(ROWS)))
P()

# ---- Q4 · the null that matters: does pedigree predict at LOW GAMES? ---------------------------------
P('-' * 118)
P('Q4 · THE NULL THAT MATTERS. Does the pedigree premium carry information at LOW career games?')
P('-' * 118)
P('   Career games counted BEFORE the season being scored, so this is what was knowable at the time.')
P('   %-12s %6s %6s | %-32s' % ('games before', 'rows', 'plyrs', 'PG(p90) - PG(p10)  [90% CI]'))
LOWG = {}
for lab, lo, hi in (('0-3', 0, 3), ('4-7', 4, 7), ('8-19', 8, 19), ('20-49', 20, 49), ('50+', 50, 10 ** 9)):
    sub = [r for r in ROWS if lo <= r['cg_before'] <= hi]
    if len(sub) < 60:
        P('   %-12s %6d THIN — not scored' % (lab, len(sub))); continue
    xs = np.array([r['x'] for r in sub]); ys = np.array([r['d'] for r in sub])
    ws = np.array([r['games'] for r in sub]); ky = [r['key'] for r in sub]

    def spr(i, xs=xs, ys=ys, ws=ws):
        a, _ = PB.loclin(X90, xs[i], ys[i], ws[i], PB.H_PRIMARY)
        b, _ = PB.loclin(X10, xs[i], ys[i], ws[i], PB.H_PRIMARY)
        return a - b

    s0 = spr(np.arange(len(sub))); cs = cluster_boot(spr, ky, np.random.default_rng(SEED))
    P('   %-12s %6d %6d | %+8.2f  [%+.2f, %+.2f]' % (
        lab, len(sub), len(set(ky)), s0, cs[0], cs[1]))
    LOWG[lab] = dict(n=len(sub), spread=s0, ci=cs)
P()

# ---- the age and bandwidth slices ---------------------------------------------------------------------
P('-' * 118)
P('Q1b · THE SLICES. Reported where thin, bounded, never smoothed away.')
P('-' * 118)
P('   BY AGE — is the premium itself age-dependent, over and above the age bar already removing level?')
P('   %-6s %6s | %-26s' % ('age', 'rows', 'PG(p90) - PG(p10)'))
AGES = {}
for a in range(18, 24):
    sub = [r for r in ROWS if r['age'] == a]
    if len(sub) < 60:
        P('   %-6d %6d | THIN — not scored' % (a, len(sub))); continue
    xs = np.array([r['x'] for r in sub]); ys = np.array([r['d'] for r in sub]); ws = np.array([r['games'] for r in sub])
    s0 = PB.loclin(X90, xs, ys, ws, PB.H_PRIMARY)[0] - PB.loclin(X10, xs, ys, ws, PB.H_PRIMARY)[0]
    P('   %-6d %6d | %+8.2f' % (a, len(sub), s0))
    AGES[a] = dict(n=len(sub), spread=s0)
P()
P('   BY BANDWIDTH — the two declared sensitivities.')
BW = {}
for h in (PB.H_SENS[0], PB.H_PRIMARY, PB.H_SENS[1]):
    g2 = PB.Premium(ROWS, h=h, iso=True)
    line = '   H = %.2f :' % h
    BW[h] = {}
    for cls in ('SMALL', 'TALL'):
        sp = g2.at(X90, cls) - g2.at(X10, cls)
        line += '  %s spread %+6.2f' % (cls, sp)
        BW[h][cls] = sp
    P(line + ('   <- PRIMARY' if abs(h - PB.H_PRIMARY) < 1e-9 else ''))
P()
P('   BY PICK BAND — the declared sensitivity on the axis this order did NOT choose.')
P('   %-12s %6s %6s | %10s %10s' % ('pick band', 'rows', 'plyrs', 'mean d', 'games-wtd d'))
BAND = {}
for b in ('1-10', '11-20', '21-40', '41+/pool'):
    sub = [r for r in ROWS if r['band'] == b and r['typ'] == 'ND']
    if not sub: continue
    d = np.array([r['d'] for r in sub]); w = np.array([r['games'] for r in sub])
    P('   %-12s %6d %6d | %+10.2f %+10.2f' % (
        b, len(sub), len(set(r['key'] for r in sub)), d.mean(), float((d * w).sum() / w.sum())))
    BAND[b] = dict(n=len(sub), mean=float(d.mean()), wmean=float((d * w).sum() / w.sum()))
P('   (pool and non-ND rows sit on the v0 axis at their own price; on a pick axis they are a residual')
P('    bucket, which is the third reason the prereg chose v0.)')
P()

# ---- Q6 / P11 · the smuggle test S2 --------------------------------------------------------------------
P('-' * 118)
P('Q6 · SMUGGLE TEST S2 (falsifier P11). Is the measured production premium SHALLOWER than the price')
P('     premium? If it is, the bar does not rise as fast as the price does, and expensive players are')
P('     let off relative to what is priced into them.')
P('-' * 118)
P('   Common currency: the house ruler. A full 22-game season produced at the bar gives one number.')
P('   The price ratio is v0(p90)/v0(p10). The delivered ratio is what the ruler says those two')
P('   production levels are worth. If the delivered ratio is SMALLER, the bar is under-demanding.')
P()
V10, V90 = math.exp(X10), math.exp(X90)
S2T = {}
for cls, pos, age in (('SMALL', 'MID', 20), ('SMALL', 'SF', 20), ('TALL', 'KPD', 20), ('TALL', 'KPF', 20)):
    b = LB.bar(pos, age)
    lo_lvl = b + PG.at(X10, cls); hi_lvl = b + PG.at(X90, cls)
    dv_lo = LB.w_sqrt(22) * LB.season_raw(lo_lvl, pos)
    dv_hi = LB.w_sqrt(22) * LB.season_raw(hi_lvl, pos)
    pr = V90 / V10
    dr = (dv_hi / dv_lo) if dv_lo > 1e-9 else float('inf')
    P('   %-5s %-5s age %d : bar %.1f  ->  cheap bar %.1f, dear bar %.1f   delivered %.1f vs %.1f' % (
        cls, pos, age, b, lo_lvl, hi_lvl, dv_lo, dv_hi))
    P('        price ratio %.2fx   delivered ratio %.2fx   -> %s' % (
        pr, dr, 'production premium SHALLOWER than price (P11 fires)' if dr < pr else 'production premium at least as steep as price'))
    S2T['%s|%s' % (cls, pos)] = dict(bar=b, lo=lo_lvl, hi=hi_lvl, dv_lo=dv_lo, dv_hi=dv_hi,
                                     price_ratio=pr, deliv_ratio=dr, fires=bool(dr < pr))
P()

# ---- the vantage rows -----------------------------------------------------------------------------------
rowsv = []
excl = collections.Counter()
for k, r in M.items():
    if k in LB.FM:
        excl['force_majeure'] += 1; continue
    if (r.get('year') or 0) < LB.ENTRY_FLOOR:
        excl['pre_2005_entry'] += 1; continue
    if not (float(r.get('v0') or 0) > 0):
        excl['no_v0'] += 1; continue
    sv = LB.season_values(r)
    for N in range(1, 7):
        Y = int(r['year']) + N
        if Y + 1 > LB.LAST_REAL_SEASON:
            excl['future_unobservable'] += 1; continue
        a = LB.age_at(r, Y)
        if a is None or a > AGE_MAX:
            excl['age>22'] += 1; continue
        g = LB.career_games(r, Y)
        if g < 1:
            excl['gameless'] += 1; continue
        if g > 60:
            excl['g>60'] += 1; continue
        sN = LB.perf_surplus(r, Y)
        sP = PB.perf_surplus_P(r, Y, PG)
        if sN is None or sP is None:
            excl['no_surplus'] += 1; continue
        dv5 = sum((LB.DISC ** -(t - Y)) * v for t, v in sv.items() if Y < t <= Y + 5)
        rowsv.append(dict(key=k, N=N, Y=Y, g=g, age=a, sN=sN, sP=sP,
                          v0=float(r['v0']), pick=(r.get('pick') if r.get('type') == 'ND' else None),
                          typ=r.get('type'), pos=r.get('pos'),
                          tall=('TALL' if r.get('pos') in LB.TALLPOS else 'SMALL'),
                          band=LB.band_of(r.get('pick') if r.get('type') == 'ND' else None),
                          dv1=LB.dv1(sv, Y), dvrest=LB.dvrest(sv, Y), dv5=dv5,
                          dv5_ok=(Y + 5 <= LB.LAST_REAL_SEASON),
                          gbin=LB.binof(g, LB.G_BINS_2)))

P('-' * 118)
P('THE VANTAGE POPULATION — ORDER N\'s, unchanged, so the two orders are comparable line by line')
P('-' * 118)
P('   entrants 2005+, vantages N=1..6, age at vantage <= %d, 1 <= g <= 60, one observable future season.' % AGE_MAX)
P('   vantage rows %d over %d players.  (ORDER N: 4,143 over 1,415.)' % (
    len(rowsv), len(set(r['key'] for r in rowsv))))
P('   exclusions: %s' % json.dumps(dict(sorted(excl.items()))))
P()

# ---- Q5 · the band balance, on the surplus itself, before any price -------------------------------------
P('-' * 118)
P('Q5 · THE OWNER\'S PREDICTION, TESTED ON THE SURPLUS ITSELF — BEFORE ANY PRICE IS COMPUTED')
P('-' * 118)
nd = [r for r in rowsv if r['pick'] is not None]
pk = np.array([float(r['pick']) for r in nd])
P('   Spearman(pick, surplus) over %d ND vantage rows:' % len(nd))
rN = spear(pk, np.array([r['sN'] for r in nd])); rP = spear(pk, np.array([r['sP'] for r in nd]))
P('      ORDER N, surplus vs the AGE bar        : %+.4f' % rN)
P('      ORDER P, surplus vs the PEDIGREE bar   : %+.4f' % rP)
P()
P('   %-10s %6s | %10s %10s | %10s %10s' % ('pick band', 'rows', 'med s_N', 'med s_P', 'mean s_N', 'mean s_P'))
BANDS5 = {}
for b in ('1-10', '11-20', '21-40', '41+/pool'):
    sub = [r for r in nd if r['band'] == b]
    if not sub: continue
    a = np.array([r['sN'] for r in sub]); c = np.array([r['sP'] for r in sub])
    P('   %-10s %6d | %+10.2f %+10.2f | %+10.2f %+10.2f' % (
        b, len(sub), np.median(a), np.median(c), a.mean(), c.mean()))
    BANDS5[b] = dict(n=len(sub), med_N=float(np.median(a)), med_P=float(np.median(c)),
                     mean_N=float(a.mean()), mean_P=float(c.mean()))
P()

# ---- Q2 / Q3 · BETA on the new surplus ------------------------------------------------------------------
P('-' * 118)
P('Q2 · BETA_P — ln(1 + DVREST) = a + year effects + c*ln(v0) + BETA_P * s_P')
P('Q3 · AND THE SAME REGRESSION ON ORDER N\'s SURPLUS, ON THE SAME ROWS, SO THE TWO ARE COMPARABLE')
P('-' * 118)


def ols(y, X):
    return np.linalg.lstsq(X, y, rcond=None)[0]


def beta_fit(sub, target, skey, i=None):
    s = [sub[j] for j in i] if i is not None else sub
    yy = np.log1p(np.array([r[target] for r in s]))
    lv = np.log(np.array([r['v0'] for r in s]))
    ss = np.array([r[skey] for r in s])
    yrs = sorted(set(r['Y'] for r in s))
    if len(yrs) < 2 or np.ptp(ss) <= 0:
        return None
    D = np.column_stack([np.array([1.0 if r['Y'] == y else 0.0 for r in s]) for y in yrs] + [lv, ss])
    if np.linalg.matrix_rank(D) < D.shape[1]:
        return None
    return float(ols(yy, D)[-1])


P('   %-9s %5s | %-30s | %8s | %-22s' % ('games', 'rows', 'BETA_P on DVREST  [90% CI]', 'x(+/-10)', 'BETA_N, same rows'))
E2 = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if len(sub) < 30:
        P('   %-9s %5d | THIN — not scored' % (b, len(sub))); continue
    ky = [r['key'] for r in sub]
    bp = beta_fit(sub, 'dvrest', 'sP')
    cp = cluster_boot(lambda i: beta_fit(sub, 'dvrest', 'sP', i), ky, np.random.default_rng(SEED))
    bn = beta_fit(sub, 'dvrest', 'sN')
    P('   %-9s %5d | %+9.5f [%+.5f,%+.5f] | %8.2f | %+9.5f' % (
        b, len(sub), bp, cp[0], cp[1], math.exp(bp * 20.0), bn))
    E2[b] = dict(n=len(sub), beta=bp, ci=cp, ratio_pm10=math.exp(bp * 20.0), beta_N=bn,
                 gmean=float(np.mean([r['g'] for r in sub])))
ky = [r['key'] for r in rowsv]
bp = beta_fit(rowsv, 'dvrest', 'sP')
cp = cluster_boot(lambda i: beta_fit(rowsv, 'dvrest', 'sP', i), ky, np.random.default_rng(SEED))
P('   %-9s %5d | %+9.5f [%+.5f,%+.5f] | %8.2f | %+9.5f' % (
    'POOLED', len(rowsv), bp, cp[0], cp[1], math.exp(bp * 20.0), beta_fit(rowsv, 'dvrest', 'sN')))
E2['POOLED'] = dict(n=len(rowsv), beta=bp, ci=cp, ratio_pm10=math.exp(bp * 20.0),
                    beta_N=beta_fit(rowsv, 'dvrest', 'sN'))
P()
P('   THE ORDER\'S OWN ANCHORS — the bin containing each games count:')
for anc in (2, 5, 10, 15, 20, 30):
    b = LB.binof(anc, LB.G_BINS_2)
    e = E2.get(b)
    if e is None: continue
    P('   at %2d games (bin %-6s): BETA_P %+8.5f  90%% CI [%+.5f, %+.5f]   a +10 row is worth %.2fx a -10 row'
      % (anc, b, e['beta'], e['ci'][0], e['ci'][1], e['ratio_pm10']))
P()
P('   E2b · THE SAME ON A FIXED FIVE-YEAR FORWARD WINDOW (censoring held equal). An addition.')
sub5 = [r for r in rowsv if r['dv5_ok']]
P('   rows with five full observable forward seasons: %d of %d' % (len(sub5), len(rowsv)))
E2B = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    s = [r for r in sub5 if r['gbin'] == b]
    if len(s) < 30: continue
    bb = beta_fit(s, 'dv5', 'sP')
    E2B[b] = dict(n=len(s), beta=bb)
    P('   %-9s %5d | %+9.5f' % (b, len(s), bb))
P()

# ---- E1 / E3 --------------------------------------------------------------------------------------------
P('-' * 118)
P('E1 / E3 · RANK ASSOCIATIONS, ON THE NEW SURPLUS')
P('-' * 118)
P('   %-9s %5s | %-30s | %-30s' % ('games', 'rows', 'partial rho(s_P, DVREST | v0)', 'partial rho(v0, DVREST | s_P)'))
E13 = {}
for lo, hi in LB.G_BINS_2:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rowsv if r['gbin'] == b]
    if len(sub) < 30: continue
    sp = np.array([r['sP'] for r in sub]); dv = np.array([r['dvrest'] for r in sub])
    v0 = np.array([r['v0'] for r in sub]); ky = [r['key'] for r in sub]
    a = partial_spear(sp, dv, v0)
    ca = cluster_boot(lambda i: partial_spear(sp[i], dv[i], v0[i]), ky, np.random.default_rng(SEED))
    c = partial_spear(v0, dv, sp)
    cc = cluster_boot(lambda i: partial_spear(v0[i], dv[i], sp[i]), ky, np.random.default_rng(SEED))
    P('   %-9s %5d | %+8.4f  [%+.4f, %+.4f]     | %+8.4f  [%+.4f, %+.4f]' % (
        b, len(sub), a, ca[0], ca[1], c, cc[0], cc[1]))
    E13[b] = dict(n=len(sub), pr_s=a, ci_s=ca, pr_v0=c, ci_v0=cc)
P()
P('   the elasticity of delivered value in the entry price, pooled (the other half of test S2):')
yy = np.log1p(np.array([r['dvrest'] for r in rowsv]))
lv = np.log(np.array([r['v0'] for r in rowsv]))
ss = np.array([r['sP'] for r in rowsv])
yrs = sorted(set(r['Y'] for r in rowsv))
D = np.column_stack([np.array([1.0 if r['Y'] == y else 0.0 for r in rowsv]) for y in yrs] + [lv, ss])
co = ols(yy, D)
P('      d ln(1+DVREST) / d ln(v0), surplus held = %+0.4f' % co[-2])
P('      a value of 1.00 would mean delivered value rises exactly in proportion to price.')
P()

# ---- the plain read ---------------------------------------------------------------------------------------
P('-' * 118)
P('THE PLAIN READ — mean subsequent delivered value by surplus tercile, within games bins')
P('-' * 118)
P('   %-8s %-8s %5s | %8s %8s %9s | %10s' % ('games', 'tercile', 'rows', 'mean s_P', 'mean s_N', 'mean v0', 'mean DVREST'))
PLAIN = {}
for lo, hi in ((1, 3), (8, 12), (13, 17), (25, 39)):
    b = '%d-%d' % (lo, hi)
    sub = sorted([r for r in rowsv if r['gbin'] == b], key=lambda r: r['sP'])
    if len(sub) < 30: continue
    n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
    for t, lab in enumerate(('low', 'mid', 'high')):
        pt = sub[cuts[t]:cuts[t + 1]]
        P('   %-8s %-8s %5d | %+8.2f %+8.2f %9.0f | %10.1f' % (
            b, lab, len(pt), np.mean([r['sP'] for r in pt]), np.mean([r['sN'] for r in pt]),
            np.mean([r['v0'] for r in pt]), np.mean([r['dvrest'] for r in pt])))
        PLAIN['%s|%s' % (b, lab)] = dict(n=len(pt), sP=float(np.mean([r['sP'] for r in pt])),
                                         sN=float(np.mean([r['sN'] for r in pt])),
                                         v0=float(np.mean([r['v0'] for r in pt])),
                                         dv=float(np.mean([r['dvrest'] for r in pt])))
P()

json.dump(dict(surface=SURF, spread=SPREAD, lowgames=LOWG, ages=AGES, bandwidth={str(k): v for k, v in BW.items()},
               pickband=BAND, s2=S2T, band_balance=BANDS5,
               spear_pick_sN=rN, spear_pick_sP=rP,
               beta=E2, beta5=E2B, ranks=E13, plain=PLAIN,
               v0_p10=math.exp(X10), v0_p50=math.exp(X50), v0_p90=math.exp(X90),
               grid={c: dict(x=list(map(float, PG.grid[c][0])), pg=list(map(float, PG.grid[c][1])),
                             raw=list(map(float, PG_RAW.grid[c][1])), ess=list(map(float, PG.ess[c])))
                     for c in ('SMALL', 'TALL')},
               rows=[dict(key=r['key'], N=r['N'], Y=r['Y'], g=r['g'], age=r['age'], sN=r['sN'], sP=r['sP'],
                          v0=r['v0'], pick=r['pick'], band=r['band'], tall=r['tall'],
                          dvrest=r['dvrest'], gbin=r['gbin']) for r in rowsv]),
          open(os.path.join(HERE, 'STEP2_P.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP2_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STEP2_P.json and STEP2_P_out.txt')
