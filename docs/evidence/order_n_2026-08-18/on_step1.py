#!/usr/bin/env python3
"""ORDER N STEP 1 — THE PROPERTY TEST. READ-ONLY.

Does the board pay a young row more for producing above his age expectation, holding games roughly
constant? PREREG_N.md section 3 fixes every window, every statistic and every falsifier used here.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_step1.py
"""
import json, math, os, sys
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

SEED, B_BOOT = 32, 2000
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


def ols(y, X):
    """X already carries its intercept column. Returns beta."""
    return np.linalg.lstsq(X, y, rcond=None)[0]


def boot_ci(fn, n, rng, B=B_BOOT):
    out = []
    for _ in range(B):
        idx = rng.integers(0, n, size=n)
        v = fn(idx)
        if v is not None and np.isfinite(v):
            out.append(v)
    if not out:
        return (float('nan'), float('nan'))
    a = np.array(out)
    return (float(np.percentile(a, 5)), float(np.percentile(a, 95)))


P('=' * 118)
P('ORDER N — STEP 1. THE PROPERTY TEST ON THE CURRENT BOARD AND THE LANDING CANDIDATE')
P('=' * 118)
P('prereg      : PREREG_N.md, pushed at 602d40a before any number here existed')
P('S4 ruler md5: %s  (falsifier N3 clear)' % LB.check_s4_copy())
P('age bar     : S1 C3 asserted against the engine literal O32_GATE_DELTA (falsifier N2 clear)')
P()

LED = LB.load_ledger()
MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')
P('ledger      : docs/ledgers/ORDER_K_MOVERS.json  rows=%d  boards=%s' % (
    len(LED['rows']), json.dumps(LED['meta']['boards'])))
P('setting     : %s' % json.dumps(LED['meta']['setting']))
P()

# ---- population -------------------------------------------------------------------------------------
AGE_MAX = 22
rows = []
skipped = {'no_matrix': 0, 'gameless': 0, 'g>60': 0, 'age>22': 0, 'no_PS': 0, 'v0<=0': 0}
for r in LED['rows']:
    k = r['key']
    m = MK.get(k)
    if m is None:
        skipped['no_matrix'] += 1; continue
    g = float(r['g'] or 0.0)
    if g <= 0:
        skipped['gameless'] += 1; continue
    if g > 60:
        skipped['g>60'] += 1; continue
    if int(r['age']) > AGE_MAX:
        skipped['age>22'] += 1; continue
    Y = max(s['year'] for s in m['seasons']) if m['seasons'] else None
    ps = LB.perf_surplus(m, Y) if Y else None
    if ps is None:
        skipped['no_PS'] += 1; continue
    if not (float(r['v0'] or 0) > 0):
        skipped['v0<=0'] += 1; continue
    rows.append(dict(key=k, name=r['name'], age=int(r['age']), g=g, pick=r.get('pick'),
                     pos=r['pos'], pathway=r['pathway'], v0=float(r['v0']),
                     orderk=float(r['orderk']), landing=float(r['landing']),
                     ps=ps, gbin=LB.binof(g, LB.G_BINS_1),
                     band=LB.band_of(r.get('pick')),
                     tall=('TALL' if r['pos'] in LB.TALLPOS else 'SMALL'),
                     v_eta0=float(ME[k]['cur']), v_etaK=float(MK[k]['cur'])))
P('POPULATION (prereg 2.3): ledger rows, age <= %d as of 2026, 1 <= career games <= 60, PS defined' % AGE_MAX)
P('  kept %d of %d ledger rows.  skipped: %s' % (len(rows), len(LED['rows']), json.dumps(skipped)))
P()

# sensitivity population, age <= 23
rows23 = []
for r in LED['rows']:
    k = r['key']; m = MK.get(k)
    if m is None: continue
    g = float(r['g'] or 0.0)
    if not (1 <= g <= 60) or int(r['age']) > 23: continue
    Y = max(s['year'] for s in m['seasons']) if m['seasons'] else None
    ps = LB.perf_surplus(m, Y) if Y else None
    if ps is None or not (float(r['v0'] or 0) > 0): continue
    rows23.append(dict(g=g, ps=ps, R=float(r['orderk']) / float(r['v0']),
                       gbin=LB.binof(g, LB.G_BINS_1), v0=float(r['v0'])))

for r in rows:
    r['R_k'] = r['orderk'] / r['v0']
    r['R_l'] = r['landing'] / r['v0']
    r['charge_pct'] = LB.eta_charge(r['g'])                      # eta * m_d(g) at ETA = 0.50
    r['charge_pts'] = r['v_eta0'] - r['v_etaK']                  # the same charge in matrix points
    r['charge_pts_frac'] = r['charge_pts'] / r['v_eta0'] if r['v_eta0'] > 0 else float('nan')

rng = np.random.default_rng(SEED)

# ---- 1. the census ----------------------------------------------------------------------------------
P('-' * 118)
P('1 · THE POPULATION, BY GAMES BIN AND PERFORMANCE SURPLUS')
P('-' * 118)
P('%-10s %5s | %8s %8s %8s | %8s %8s | %8s %8s' % (
    'games bin', 'n', 'PS p25', 'PS med', 'PS p75', 'mean g', 'mean age', 'mean R_K', 'chg%'))
for lo, hi in LB.G_BINS_1:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rows if r['gbin'] == b]
    if not sub: continue
    ps = np.array([r['ps'] for r in sub])
    P('%-10s %5d | %8.2f %8.2f %8.2f | %8.1f %8.1f | %8.4f %7.1f%%' % (
        b, len(sub), np.percentile(ps, 25), np.median(ps), np.percentile(ps, 75),
        np.mean([r['g'] for r in sub]), np.mean([r['age'] for r in sub]),
        np.mean([r['R_k'] for r in sub]), 100 * np.mean([r['charge_pct'] for r in sub])))
allps = np.array([r['ps'] for r in rows])
P('%-10s %5d | %8.2f %8.2f %8.2f | %8.1f %8.1f | %8.4f %7.1f%%' % (
    'ALL', len(rows), np.percentile(allps, 25), np.median(allps), np.percentile(allps, 75),
    np.mean([r['g'] for r in rows]), np.mean([r['age'] for r in rows]),
    np.mean([r['R_k'] for r in rows]), 100 * np.mean([r['charge_pct'] for r in rows])))
P()

# ---- 2. slopes --------------------------------------------------------------------------------------
P('-' * 118)
P('2 · THE PRICE RESPONSE AGAINST PERFORMANCE SURPLUS')
P('-' * 118)
P('R = board price / v0. Slope is d(R) per one point-per-game of surplus. 90%% CI bootstrapped, %d resamples, seed %d.' % (B_BOOT, SEED))
P()

RES = {}
for lab, fld in (('orderk (f3101883)', 'R_k'), ('landing (1f176444)', 'R_l')):
    y = np.array([r[fld] for r in rows])
    ps = np.array([r['ps'] for r in rows])
    n = len(rows)
    # unconditional
    X = np.column_stack([np.ones(n), ps])
    b_un = ols(y, X)[1]
    ci_un = boot_ci(lambda i: ols(y[i], np.column_stack([np.ones(n), ps[i]]))[1], n, np.random.default_rng(SEED))
    # games-bin fixed effects
    bins = sorted(set(r['gbin'] for r in rows))
    Dm = np.column_stack([np.array([1.0 if r['gbin'] == b else 0.0 for r in rows]) for b in bins] + [ps])
    b_fe = ols(y, Dm)[-1]

    def _fe(i):
        Di = Dm[i]
        if np.linalg.matrix_rank(Di) < Di.shape[1]:
            return None
        return ols(y[i], Di)[-1]
    ci_fe = boot_ci(_fe, n, np.random.default_rng(SEED))
    # + log v0 control on top of the games FE
    lv = np.log(np.array([r['v0'] for r in rows]))
    Dm2 = np.column_stack([Dm[:, :-1], lv, ps])
    b_fe2 = ols(y, Dm2)[-1]

    def _fe2(i):
        Di = Dm2[i]
        if np.linalg.matrix_rank(Di) < Di.shape[1]:
            return None
        return ols(y[i], Di)[-1]
    ci_fe2 = boot_ci(_fe2, n, np.random.default_rng(SEED))
    rho_un = spear(ps, y)
    ci_rho = boot_ci(lambda i: spear(ps[i], y[i]), n, np.random.default_rng(SEED))
    P('%s' % lab)
    P('   unconditional slope        %+9.5f   90%% CI [%+.5f, %+.5f]' % (b_un, ci_un[0], ci_un[1]))
    P('   + games-bin fixed effects  %+9.5f   90%% CI [%+.5f, %+.5f]   <- the property test' % (b_fe, ci_fe[0], ci_fe[1]))
    P('   + games FE + ln(v0)        %+9.5f   90%% CI [%+.5f, %+.5f]' % (b_fe2, ci_fe2[0], ci_fe2[1]))
    P('   Spearman(PS, R)            %+9.4f   90%% CI [%+.4f, %+.4f]' % (rho_un, ci_rho[0], ci_rho[1]))
    RES[lab] = dict(slope_uncond=b_un, ci_uncond=ci_un, slope_gfe=b_fe, ci_gfe=ci_fe,
                    slope_gfe_v0=b_fe2, ci_gfe_v0=ci_fe2, spearman=rho_un, ci_spearman=ci_rho)
    P()

# within-bin Spearman
P('   Spearman(PS, R) WITHIN each games bin — the property, bin by bin:')
P('   %-10s %5s | %10s %10s | %10s %10s' % ('games bin', 'n', 'rho orderk', '90% CI', 'rho landing', '90% CI'))
BINROWS = {}
for lo, hi in LB.G_BINS_1:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rows if r['gbin'] == b]
    if len(sub) < 8:
        P('   %-10s %5d | thin, not scored' % (b, len(sub))); continue
    ps = np.array([r['ps'] for r in sub]); n = len(sub)
    rk = np.array([r['R_k'] for r in sub]); rl = np.array([r['R_l'] for r in sub])
    a = spear(ps, rk); ca = boot_ci(lambda i: spear(ps[i], rk[i]), n, np.random.default_rng(SEED))
    c = spear(ps, rl); cc = boot_ci(lambda i: spear(ps[i], rl[i]), n, np.random.default_rng(SEED))
    P('   %-10s %5d | %+10.4f [%+.3f,%+.3f] | %+10.4f [%+.3f,%+.3f]' % (b, n, a, ca[0], ca[1], c, cc[0], cc[1]))
    BINROWS[b] = dict(n=n, rho_k=a, ci_k=ca, rho_l=c, ci_l=cc)
P()

# ---- 2b. the reward per point of surplus, BY GAMES LEVEL --------------------------------------------
P('-' * 118)
P('2b · HOW MUCH THE BOARD PAYS FOR ONE POINT PER GAME OF SURPLUS, AT EACH GAMES LEVEL')
P('-' * 118)
P('   Within each games bin: OLS of R on PS, and the same with ln(v0) controlled. This is the number')
P('   the owner is asking about — the price the board puts on being ahead of your age bar.')
P('   %-10s %5s | %11s %-20s | %11s | %11s' % (
    'games bin', 'n', 'dR/dPS', '90% CI', 'dR/dPS +ln v0', 'pts/point'))
PERPT = {}
for lo, hi in LB.G_BINS_1:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rows if r['gbin'] == b]
    if len(sub) < 8:
        continue
    n = len(sub)
    y = np.array([r['R_k'] for r in sub]); psb = np.array([r['ps'] for r in sub])
    lvb = np.log(np.array([r['v0'] for r in sub]))
    X1 = np.column_stack([np.ones(n), psb])
    s1 = ols(y, X1)[1]
    ci1 = boot_ci(lambda i: (ols(y[i], np.column_stack([np.ones(n), psb[i]]))[1]
                             if np.ptp(psb[i]) > 0 else None), n, np.random.default_rng(SEED))
    X2 = np.column_stack([np.ones(n), lvb, psb])
    s2 = ols(y, X2)[-1]
    # the same slope read in board points rather than in ratio units
    yp = np.array([r['orderk'] for r in sub])
    sp = ols(yp, X1)[1]
    P('   %-10s %5d | %+11.5f [%+.5f,%+.5f] | %+11.5f | %+11.1f' % (b, n, s1, ci1[0], ci1[1], s2, sp))
    PERPT[b] = dict(n=n, dR_dPS=s1, ci=ci1, dR_dPS_v0=s2, dpts_dPS=sp)
P()

# ---- 3. binned means --------------------------------------------------------------------------------
P('-' * 118)
P('3 · BINNED MEANS — R BY PERFORMANCE-SURPLUS TERCILE WITHIN EACH GAMES BIN')
P('-' * 118)
P('   Terciles are cut WITHIN the games bin, so games is held as close to constant as the data allows.')
P('   %-10s %-8s %5s | %8s %8s | %9s %9s | %8s' % (
    'games bin', 'PS terc', 'n', 'mean PS', 'mean g', 'mean R_K', 'mean R_L', 'chg%'))
TERC = {}
for lo, hi in LB.G_BINS_1:
    b = '%d-%d' % (lo, hi)
    sub = sorted([r for r in rows if r['gbin'] == b], key=lambda r: r['ps'])
    if len(sub) < 9:
        continue
    n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
    for t in range(3):
        part = sub[cuts[t]:cuts[t + 1]]
        P('   %-10s %-8s %5d | %8.2f %8.1f | %9.4f %9.4f | %7.1f%%' % (
            b, ('low', 'mid', 'high')[t], len(part),
            np.mean([r['ps'] for r in part]), np.mean([r['g'] for r in part]),
            np.mean([r['R_k'] for r in part]), np.mean([r['R_l'] for r in part]),
            100 * np.mean([r['charge_pct'] for r in part])))
        TERC.setdefault(b, {})[('low', 'mid', 'high')[t]] = dict(
            n=len(part), ps=float(np.mean([r['ps'] for r in part])),
            R_k=float(np.mean([r['R_k'] for r in part])), R_l=float(np.mean([r['R_l'] for r in part])),
            chg=float(np.mean([r['charge_pct'] for r in part])))
    P()

# ---- 4. the eta charge in isolation ------------------------------------------------------------------
P('-' * 118)
P('4 · THE ETA CHARGE IN ISOLATION — charge(g) = 0.50 * (g/14) * exp(1 - g/14)')
P('-' * 118)
ps = np.array([r['ps'] for r in rows]); n = len(rows)
ch = np.array([r['charge_pct'] for r in rows])
chp = np.array([r['charge_pts'] for r in rows])
chf = np.array([r['charge_pts_frac'] for r in rows])
r1 = spear(ps, ch); c1 = boot_ci(lambda i: spear(ps[i], ch[i]), n, np.random.default_rng(SEED))
P('   Spearman(PS, charge%%)  UNCONDITIONAL      %+8.4f   90%% CI [%+.4f, %+.4f]' % (r1, c1[0], c1[1]))
r2 = spear(ps, chp); c2 = boot_ci(lambda i: spear(ps[i], chp[i]), n, np.random.default_rng(SEED))
P('   Spearman(PS, charge in POINTS)            %+8.4f   90%% CI [%+.4f, %+.4f]' % (r2, c2[0], c2[1]))
r3 = spear(ps, chf); c3 = boot_ci(lambda i: spear(ps[i], chf[i]), n, np.random.default_rng(SEED))
P('   Spearman(PS, charge as %% of eta=0 price)  %+8.4f   90%% CI [%+.4f, %+.4f]' % (r3, c3[0], c3[1]))
P()
P('   WITHIN games bins (the charge is a pure function of g, so this is a construction check):')
for lo, hi in LB.G_BINS_1:
    b = '%d-%d' % (lo, hi)
    sub = [r for r in rows if r['gbin'] == b]
    if len(sub) < 8: continue
    pss = np.array([r['ps'] for r in sub])
    P('   %-10s n=%-4d  Spearman(PS, charge%%) = %+7.4f   Spearman(PS, charge pts) = %+7.4f' % (
        b, len(sub), spear(pss, np.array([r['charge_pct'] for r in sub])),
        spear(pss, np.array([r['charge_pts'] for r in sub]))))
P()
P('   Charge by PS tercile, POOLED over the whole young window (games NOT held):')
sub = sorted(rows, key=lambda r: r['ps']); n = len(sub); cuts = [0, n // 3, 2 * n // 3, n]
POOLT = {}
for t in range(3):
    part = sub[cuts[t]:cuts[t + 1]]
    lab = ('below expectation', 'middle', 'above expectation')[t]
    P('   %-20s n=%-4d  mean PS %+7.2f  mean g %5.1f  mean charge %5.1f%%  mean charge %7.1f pts  R_K %.4f' % (
        lab, len(part), np.mean([r['ps'] for r in part]), np.mean([r['g'] for r in part]),
        100 * np.mean([r['charge_pct'] for r in part]), np.mean([r['charge_pts'] for r in part]),
        np.mean([r['R_k'] for r in part])))
    POOLT[lab] = dict(n=len(part), ps=float(np.mean([r['ps'] for r in part])),
                      g=float(np.mean([r['g'] for r in part])),
                      chg=float(np.mean([r['charge_pct'] for r in part])),
                      chg_pts=float(np.mean([r['charge_pts'] for r in part])),
                      R_k=float(np.mean([r['R_k'] for r in part])))
P()

# ---- 5. matched pairs -------------------------------------------------------------------------------
P('-' * 118)
P('5 · MATCHED PAIRS — rows within 2 career games of each other, sorted by the surplus gap')
P('-' * 118)
P('   Every pair below has games held to within 2. The charge column is the eta charge each row pays.')
P('   %-24s %-24s %5s %5s | %7s %7s | %7s %7s' % ('above-bar row', 'below-bar row', 'g_a', 'g_b', 'PS_a', 'PS_b', 'chg_a', 'chg_b'))
prs = []
for i, a in enumerate(rows):
    for bqq in rows[i + 1:]:
        if abs(a['g'] - bqq['g']) <= 2 and abs(a['ps'] - bqq['ps']) >= 12:
            hi_, lo_ = (a, bqq) if a['ps'] > bqq['ps'] else (bqq, a)
            prs.append((hi_['ps'] - lo_['ps'], hi_, lo_))
prs.sort(key=lambda t: -t[0])
for gap, hi_, lo_ in prs[:12]:
    P('   %-24s %-24s %5.0f %5.0f | %+7.1f %+7.1f | %6.1f%% %6.1f%%' % (
        hi_['name'][:24], lo_['name'][:24], hi_['g'], lo_['g'], hi_['ps'], lo_['ps'],
        100 * hi_['charge_pct'], 100 * lo_['charge_pct']))
P('   pairs found: %d' % len(prs))
P()

# ---- 6. sensitivity age <= 23 -----------------------------------------------------------------------
P('-' * 118)
P('6 · PRE-DECLARED SENSITIVITY — age <= 23 instead of <= 22')
P('-' * 118)
y = np.array([r['R'] for r in rows23]); ps = np.array([r['ps'] for r in rows23]); n = len(rows23)
bins = sorted(set(r['gbin'] for r in rows23))
Dm = np.column_stack([np.array([1.0 if r['gbin'] == b else 0.0 for r in rows23]) for b in bins] + [ps])
b_fe = ols(y, Dm)[-1]
ci = boot_ci(lambda i: (ols(y[i], Dm[i])[-1] if np.linalg.matrix_rank(Dm[i]) == Dm.shape[1] else None),
             n, np.random.default_rng(SEED))
P('   n = %d.  slope of R_K on PS with games-bin FE: %+.5f   90%% CI [%+.5f, %+.5f]' % (n, b_fe, ci[0], ci[1]))
P('   Spearman(PS, R_K) = %+.4f' % spear(ps, y))
P()

json.dump(dict(population=dict(n=len(rows), age_max=AGE_MAX, skipped=skipped),
               slopes=RES, within_bin=BINROWS, terciles=TERC, pooled_terciles=POOLT,
               charge_isolation=dict(spearman_pct=[r1, c1], spearman_pts=[r2, c2], spearman_frac=[r3, c3]),
               per_point=PERPT, sens_age23=dict(n=n, slope_gfe=b_fe, ci=ci),
               rows=[{k: v for k, v in r.items()} for r in rows]),
          open(os.path.join(HERE, 'STEP1_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP1_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STEP1_N.json and STEP1_N_out.txt')
