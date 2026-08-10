"""PROBE 3AX, pass 2 (READ-ONLY).  Adds: thin-cell diagnostics (raw kernel mass + bootstrap CIs),
axis-vs-kernel controls, the declared-taper sensitivity, the seam proxy, and the ND top-pick fallers.
"""
import json
import numpy as np

S = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ROWS = json.load(open(S + '/s6_rows.json'))
rng = np.random.default_rng(20260810)

POP = [x for x in ROWS if x['nd'] and 1 <= x['pk'] <= 64 and 1 <= x['N'] <= 3]
Y1 = [x for x in POP if x['N'] == 1]
PK_KNOTS = [3.0, 8.0, 15.0, 25.0, 35.0, 45.0]
TAU_KNOTS = [1.0, 2.0, 3.0, 4.0]
Z_KNOTS = [-0.60, -0.30, 0.0, 0.30, 0.60]
G_KNOTS = [6.0, 10.0, 14.0, 18.0, 24.0]
PK_LO, PK_HI = 34.0, 48.0
AGE_LO, AGE_HI = 18.0, 19.0
CLASSES = ['nonKPP', 'KPP', 'RUCK']
EFFN = 35.0
LPK = [float(np.log(k)) for k in PK_KNOTS]
LGK = [float(np.log1p(k)) for k in G_KNOTS]


def mktaper(lo, hi):
    def t(v):
        if v is None: return 0.0
        if v <= lo: return 1.0
        if v >= hi: return 0.0
        return float(0.5 * (1.0 + np.cos(np.pi * (v - lo) / (hi - lo))))
    return t


tpk = mktaper(PK_LO, PK_HI); tage = mktaper(AGE_LO, AGE_HI)
for x in POP:
    x['lp'] = float(np.log(min(max(x['pk'], 1), 90)))
    x['z'] = float(np.clip(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)), Z_KNOTS[0], Z_KNOTS[-1]))
    x['lg'] = float(np.log1p(max(x['gcum'], 0.0)))
    x['r'] = x['F'] - x['price']
    x['tp'] = tpk(x['pk']); x['ta'] = tage(x['age'])
    x['iskpd'] = (x['pos'] == 'KPD')
NONKPD = [x for x in Y1 if not x['iskpd']]
SA_MU = float(np.mean([x['sa'] for x in NONKPD])); SA_SD = float(np.std([x['sa'] for x in NONKPD]))
for x in POP: x['u'] = (x['sa'] - SA_MU) / SA_SD
sas = sorted(x['sa'] for x in Y1)
SAMED = sas[len(sas) // 2]; SAT2 = sas[2 * len(sas) // 3]; SAT1 = sas[len(sas) // 3]
U_KNOTS = [-1.0, -0.4, 0.0, 0.4, 1.0]     # for the Ssa shape-gate control


def loc_delta(rows, K):
    num = float(sum(K[i] * rows[i]['r'] for i in range(len(rows))))
    den = float(sum(K[i] * rows[i]['price'] for i in range(len(rows))))
    return (num / den) if den > 1e-9 else 0.0


def eff_n(rows, K):
    W = np.array([K[i] * rows[i]['price'] for i in range(len(rows))])
    s2 = float((W * W).sum())
    return (float(W.sum()) ** 2 / s2) if s2 > 0 else 0.0


def kernel_mass(K):
    """Honest thin-cell counters that eff-n (a weight-concentration statistic) does NOT provide:
    sum(K) is the effective ROW COUNT the cell is averaging over; n_half is how many rows sit at
    least half-weight in the kernel."""
    a = np.array(K)
    return float(a.sum()), int((a >= 0.5).sum())


def boot_ci(rows, K, reps=600):
    """Percentile CI on loc_delta by row resampling inside the kernel-weighted cell."""
    n = len(rows)
    r = np.array([x['r'] for x in rows]); p = np.array([x['price'] for x in rows]); k = np.array(K)
    out = []
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        den = float((k[idx] * p[idx]).sum())
        out.append(float((k[idx] * r[idx]).sum()) / den if den > 1e-9 else 0.0)
    return float(np.percentile(out, 5)), float(np.percentile(out, 95))


D1 = loc_delta(NONKPD, [1.0] * len(NONKPD))
DKPD = loc_delta([x for x in Y1 if x['iskpd']], [1.0] * len([x for x in Y1 if x['iskpd']]))
raw = [loc_delta([x for x in POP if abs(x['tau'] - t) < 0.5 and not x['iskpd']],
                 [1.0] * len([x for x in POP if abs(x['tau'] - t) < 0.5 and not x['iskpd']]))
       for t in TAU_KNOTS]
unc = [v / D1 for v in raw]
STAU = []; cur = 1.0
for v in unc:
    cur = min(cur, max(0.0, min(1.0, v))); STAU.append(cur)
STAU[0] = 1.0


def s_tau(t): return float(np.interp(t, [0.0] + TAU_KNOTS, [STAU[0]] + STAU)) if t <= TAU_KNOTS[-1] else 0.0


def shape(keyf, knots, h0):
    h = h0; vals = []; ens = []
    for kk in knots:
        K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        while eff_n(NONKPD, K) < EFFN and h < 9.0:
            h *= 1.15
            K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        vals.append(loc_delta(NONKPD, K) / D1); ens.append(round(eff_n(NONKPD, K), 1))
    return vals, ens, h


SZ0, _, SZBW = shape(lambda x: x['z'], Z_KNOTS, (Z_KNOTS[1] - Z_KNOTS[0]) * 1.1)
SG, _, SGBW = shape(lambda x: x['lg'], LGK, (LGK[1] - LGK[0]) * 1.1)
SSA, SSA_EN, SSABW = shape(lambda x: x['u'], U_KNOTS, (U_KNOTS[1] - U_KNOTS[0]) * 1.1)


def s_g(lg): return float(np.interp(lg, LGK, SG))


# ---------------- kernels ------------------------------------------------------------------------
def kern2():
    B = {}; pooled = []
    for c in CLASSES:
        rc = [x for x in NONKPD if x['cls'] == c]; ok = bool(rc); vals = []
        for lpk in LPK:
            h = 0.18
            while True:
                K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in rc]
                en = eff_n(rc, K)
                if en >= EFFN or h > 3.0: break
                h *= 1.15
            if en < EFFN: ok = False
            vals.append(loc_delta(rc, K) / D1 if rc else 0.0)
        if not ok:
            pooled.append(c); vals = []
            for lpk in LPK:
                h = 0.18
                while True:
                    K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in NONKPD]
                    if eff_n(NONKPD, K) >= EFFN or h > 3.0: break
                    h *= 1.15
                vals.append(loc_delta(NONKPD, K) / D1)
        B[c] = vals
    return B, pooled


def kern3(sak, hs0, diag):
    B = {c: [[0.0] * len(sak) for _ in LPK] for c in CLASSES}
    for c in CLASSES:
        rc = [x for x in NONKPD if x['cls'] == c]
        for j, lpk in enumerate(LPK):
            for m, sk in enumerate(sak):
                got = None
                for stage, src in ((1, rc), (2, NONKPD)):
                    if not src: continue
                    hp, hs = 0.18, hs0
                    while True:
                        K = [float(np.exp(-0.5 * (((x['lp'] - lpk) / hp) ** 2 + ((x['u'] - sk) / hs) ** 2)))
                             for x in src]
                        en = eff_n(src, K)
                        if en >= EFFN or hp > 3.0: break
                        hp *= 1.15; hs *= 1.15
                    if en >= EFFN:
                        got = (stage, src, K, hp, hs, en); break
                if got is None:
                    hp = 0.18
                    while True:
                        K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / hp) ** 2)) for x in NONKPD]
                        en = eff_n(NONKPD, K)
                        if en >= EFFN or hp > 3.0: break
                        hp *= 1.15
                    got = (3, NONKPD, K, hp, float('inf'), en)
                stage, src, K, hp, hs, en = got
                v = loc_delta(src, K) / D1
                B[c][j][m] = v
                sk_, nh = kernel_mass(K)
                lo, hi = boot_ci(src, K)
                diag.append(dict(cls=c, pk=PK_KNOTS[j], u=round(sk, 3), stage=stage, hp=round(hp, 3),
                                 hs=(None if hs == float('inf') else round(hs, 3)), effn=round(en, 1),
                                 sumK=round(sk_, 1), nhalf=nh, val=v,
                                 ci=(lo / D1, hi / D1)))
    return B


def b2_of(B, x): return float(np.interp(x['lp'], LPK, B[x['cls']]))


def mk_b3(B, sak):
    def f(x):
        tab = B[x['cls']]
        col = [float(np.interp(x['u'], sak, tab[j])) for j in range(len(LPK))]
        return float(np.interp(x['lp'], LPK, col))
    return f


# ---------------- surface builder ----------------------------------------------------------------
def build(bfun, gates, pk_lo=PK_LO, pk_hi=PK_HI):
    """gates: subset of {'z','sa'} multiplied in beside Sg and the tapers."""
    tp_ = mktaper(pk_lo, pk_hi)
    sup = [x for x in NONKPD if tp_(x['pk']) * x['ta'] > 0.0]
    meas_sup = loc_delta(sup, [1.0] * len(sup))
    SZ = list(SZ0)
    WMZ = (sum(x['price'] * float(np.interp(x['z'], Z_KNOTS, SZ0)) for x in NONKPD) /
           sum(x['price'] for x in NONKPD))

    def m_of(x, SZL):
        s = s_tau(x['tau']) * s_g(x['lg']) * tp_(x['pk']) * x['ta']
        if 'z' in gates: s *= float(np.interp(x['z'], Z_KNOTS, SZL))
        if 'sa' in gates: s *= float(np.interp(x['u'], U_KNOTS, SSA))
        return s

    KAPPA = 1.0; worst = None
    for _ in range(400):
        SZ = [WMZ + KAPPA * (v - WMZ) for v in SZ0] if 'z' in gates else SZ0
        raw_t = sum(x['price'] * D1 * bfun(x) * m_of(x, SZ) for x in sup) / sum(x['price'] for x in sup)
        ZC = raw_t / meas_sup
        if 'z' not in gates:
            worst = None; break
        w = 9.9
        zs = np.linspace(Z_KNOTS[0], Z_KNOTS[-1], 121)
        for c in CLASSES:
            for pk in (3, 5, 8, 12, 15, 20, 25, 30, 35, 40, 45):
                tt = tp_(pk)
                if tt == 0.0: continue
                for g in (6.0, 10.0, 16.0, 24.0):
                    for t in (1.0, 1.5):
                        for uu in (-1.0, 0.0, 1.0):
                            pr = dict(cls=c, pk=pk, lp=float(np.log(pk)), lg=float(np.log1p(g)),
                                      tau=t, u=uu, z=0.0, iskpd=False)
                            base = D1 * (bfun(pr) / ZC) * s_tau(t) * s_g(pr['lg']) * tt
                            if 'sa' in gates: base *= float(np.interp(uu, U_KNOTS, SSA))
                            d = [base * float(np.interp(z, Z_KNOTS, SZ)) for z in zs]
                            for i in range(1, len(zs)):
                                dd = (d[i] - d[i - 1]) / (zs[i] - zs[i - 1])
                                w = min(w, 1.0 + d[i] + dd)
        worst = w
        if w > 0.02: break
        KAPPA *= 0.97

    def delta_of(x, W):
        if x['iskpd']: return 0.0
        if tp_(x['pk']) <= 0 or x['age'] is None or x['ta'] <= 0: return 0.0
        return float(W) * D1 * (bfun(x) / ZC) * m_of(x, SZ)

    return delta_of, dict(Z=ZC, kappa=KAPPA, mono=worst, meas_sup=meas_sup, n_sup=len(sup))


GATES = [('picks 1-10 x TOP-TERCILE sa', lambda x: x['pk'] <= 10 and x['sa'] >= SAT2, 0.015),
         ('picks 1-20 x ABOVE-MEDIAN sa', lambda x: x['pk'] <= 20 and x['sa'] >= SAMED, 0.025),
         ('picks 41-64 (declared taper)', lambda x: 41 <= x['pk'] <= 64, 0.005),
         ('draft age 19+ (declared taper)', lambda x: x['age'] is not None and x['age'] >= 19, 0.005),
         ('draft age UNKNOWN', lambda x: x['age'] is None, 0.0)]
RUNGS = [0.25, 0.5, 0.75, 1.0]
BASE_LANDING = 0.990805
LIFT1 = 1.071991 - BASE_LANDING
SEAM = {0.25: 1.014493, 0.5: 1.925722, 0.75: 2.753623, 1.0: 3.768116}
SEAM_BAND = lambda x: 20 <= x['pk'] <= 33      # the picks that carry the seam maximum (pick 24)


def assess(name, delta_of, diag, ref=None):
    out = dict(name=name, diag=diag)
    sp1 = sum(x['price'] for x in Y1)
    out['agg1'] = sum(x['price'] * delta_of(x, 1.0) for x in Y1) / sp1
    G = {}
    for nm, f, bound in GATES:
        sub = [x for x in Y1 if f(x)]
        sp = sum(x['price'] for x in sub)
        v1 = sum(x['price'] * delta_of(x, 1.0) for x in sub) / sp
        G[nm] = dict(n=len(sub), bound=bound, v1=v1,
                     meas=sum(x['F'] for x in sub) / sp - 1.0,
                     wmax=(bound / abs(v1) if abs(v1) > 1e-12 else 9.9))
    out['G'] = G
    out['wmax_all'] = min(d['wmax'] for d in G.values())
    out['wby_all'] = min(G.items(), key=lambda kv: kv[1]['wmax'])[0]
    sa_only = {k: v for k, v in G.items() if 'sa' in k}
    out['wmax_sa'] = min(d['wmax'] for d in sa_only.values())
    out['wby_sa'] = min(sa_only.items(), key=lambda kv: kv[1]['wmax'])[0]
    # tail vs typical
    tt = {}
    for W in RUNGS + [round(out['wmax_all'], 4)]:
        newp = [x['price'] * (1.0 + delta_of(x, W)) for x in Y1]
        tt[W] = (sum(x['F'] for x in Y1) / sum(newp),
                 float(np.median([Y1[i]['F'] / newp[i] for i in range(len(Y1))])),
                 float(np.mean([1.0 if Y1[i]['F'] > newp[i] else 0.0 for i in range(len(Y1))])))
    out['tt'] = tt
    # seam proxy: scale the shipped per-rung seam by this surface's lift in the seam-carrying band
    band = [x for x in Y1 if SEAM_BAND(x)]
    spb = sum(x['price'] for x in band)
    out['band_lift'] = sum(x['price'] * delta_of(x, 1.0) for x in band) / spb
    out['delta_of'] = delta_of
    return out


B2, POOLED2 = kern2()
D3A = []; D3C = []
SAK3 = [(SAT1 - SA_MU) / SA_SD, (SAMED - SA_MU) / SA_SD, (SAT2 - SA_MU) / SA_SD]
HS3 = float(np.mean(np.diff(SAK3))) * 1.1
B3 = kern3(SAK3, HS3, D3A)
QS = [float(np.quantile([x['u'] for x in NONKPD], q)) for q in (0.1, 0.3, 0.5, 0.7, 0.9)]
HS5 = float(np.mean(np.diff(QS))) * 1.1
B5 = kern3(QS, HS5, D3C)

SURF = []
for nm, bf, gts in (
        ('CONTROL 2-axis (shipped): pick x class, gate z', lambda x: b2_of(B2, x), ('z',)),
        ('3-axis A: pick x class x sa(3 knots), no z gate', mk_b3(B3, SAK3), ()),
        ('3-axis B: pick x class x sa(3 knots), z gate kept', mk_b3(B3, SAK3), ('z',)),
        ('3-axis C: pick x class x sa(5 knots), no z gate', mk_b3(B5, QS), ()),
        ('CONTROL E 2-axis kernel, gate sa instead of z', lambda x: b2_of(B2, x), ('sa',)),
        ('CONTROL F 2-axis kernel, gates z AND sa', lambda x: b2_of(B2, x), ('z', 'sa'))):
    d, dg = build(bf, gts)
    SURF.append(assess(nm, d, dg))

print('=' * 116)
print('BASELINE FACTS')
print('=' * 116)
print('  n year-1 ND 1-64 = %d (bonus %d, KPD %d)   D1 = %+0.6f   D_KPD = %+0.6f' %
      (len(Y1), len(NONKPD), len(Y1) - len(NONKPD), D1, DKPD))
print('  Ssa (sa as a SHAPE GATE, knots %s) = %s   eff-n %s  bw %.3f' %
      (U_KNOTS, [round(v, 4) for v in SSA], SSA_EN, SSABW))
print('  Sz  (z  as a SHAPE GATE, knots %s) = %s  bw %.3f' %
      (Z_KNOTS, [round(v, 4) for v in SZ0], SZBW))
print('  -> the SPAN of each level axis on the residual: Sz %.2fx   Ssa %.2fx' %
      (max(SZ0) / max(min(SZ0), 1e-9), max(SSA) / max(min(SSA), 1e-9)))

print('\n' + '=' * 116)
print('GATE TABLE (value-weighted absolute move, year-1 ND 1-64) AND MAX FEASIBLE INTENSITY')
print('=' * 116)
hdr = '%-50s %9s %9s %9s %9s %9s %9s' % ('surface', 'Z', 'kappa', '1-10xT3', '1-20xA2', '41-64', 'age19+')
print(hdr + '   (all at W=1)')
print('-' * 116)
print('%-50s %9s %9s %9.3f %9.3f %9.3f %9.3f' % ('BOUND', '', '', 0.015, 0.025, 0.005, 0.005))
for s in SURF:
    g = s['G']
    print('%-50s %9.4f %9.4f %+9.5f %+9.5f %+9.5f %+9.5f' %
          (s['name'], s['diag']['Z'], s['diag']['kappa'],
           g['picks 1-10 x TOP-TERCILE sa']['v1'], g['picks 1-20 x ABOVE-MEDIAN sa']['v1'],
           g['picks 41-64 (declared taper)']['v1'], g['draft age 19+ (declared taper)']['v1']))
print()
print('%-50s %10s %-30s %10s %-24s' % ('surface', 'W_max ALL', 'bound by', 'W_max sa-only', 'bound by'))
print('-' * 116)
for s in SURF:
    print('%-50s %10.4f %-30s %10.4f %-24s' %
          (s['name'], s['wmax_all'], s['wby_all'], s['wmax_sa'], s['wby_sa']))

print('\n' + '=' * 116)
print('IMPLIED ND YEAR-1 LANDING  (base %.6f; the shipped surface delivers %.6f per unit intensity)'
      % (BASE_LANDING, LIFT1))
print('=' * 116)
ref = SURF[0]
print('%-50s %9s %11s %11s %11s %11s' % ('surface', 'agg@W=1', 'land@.25', 'land@.50', 'land@1.0',
                                         'land@W_max'))
print('-' * 116)
for s in SURF:
    sc = s['agg1'] / ref['agg1']
    f = lambda W: BASE_LANDING + LIFT1 * sc * W
    print('%-50s %+9.6f %11.6f %11.6f %11.6f %11.6f  (W_max %.4f)' %
          (s['name'], s['agg1'], f(0.25), f(0.5), f(1.0), f(s['wmax_all']), s['wmax_all']))
    print('%-50s %s' % ('   sa-gates-only ceiling (41-64 taper set aside)',
                        '%11.6f  (W %.4f)' % (f(s['wmax_sa']), s['wmax_sa'])))

print('\n' + '=' * 116)
print('TAIL-vs-TYPICAL at each intensity (year-1 ND 1-64; uncorrected median F\' = %.4f, frac out-earn %.3f)'
      % (float(np.median([x['F'] / x['price'] for x in Y1])),
         float(np.mean([1.0 if x['F'] > x['price'] else 0.0 for x in Y1]))))
print('=' * 116)
print('%-50s %8s %10s %10s %10s' % ('surface', 'W', "corr agg", 'corr med', 'frac out'))
for s in SURF:
    for W in sorted(s['tt']):
        a, m, fr = s['tt'][W]
        print('%-50s %8s %10.4f %10.4f %10.3f' % (s['name'] if W == 0.25 else '', W, a, m, fr))

print('\n' + '=' * 116)
print('SEAM PROXY (pick/player seam tolerance +-2.00%%; shipped max move sits at pick 24, band 20-33)')
print('=' * 116)
print('  shipped two-axis measured seam: %s' % {k: round(v, 4) for k, v in SEAM.items()})
print('  proxy: seam(W) = shipped seam(W) x (this surface\'s value-weighted lift on picks 20-33 / the')
print('         shipped surface\'s lift on the same band).  APPROXIMATION - the true seam needs a board')
print('         re-emit, which a read-only seat cannot run.')
print('%-50s %12s %10s %10s %10s %12s' % ('surface', 'band lift@1', 'seam@.25', 'seam@.5', 'seam@.75', 'W at 2.00%'))
for s in SURF:
    r = s['band_lift'] / ref['band_lift']
    sv = {W: SEAM[W] * r for W in RUNGS}
    # linear-in-W interpolation of the measured seam ladder, scaled
    ws = np.array(RUNGS); ys = np.array([SEAM[W] * r for W in RUNGS])
    w2 = float(np.interp(2.0, ys, ws)) if ys[-1] >= 2.0 else 9.9
    print('%-50s %12.5f %10.4f %10.4f %10.4f %12.4f' %
          (s['name'], s['band_lift'], sv[0.25], sv[0.5], sv[0.75], w2))

print('\n' + '=' * 116)
print('THIN-CELL HONESTY: what the eff-n>=35 rule does and does NOT certify in three axes')
print('=' * 116)
print('  eff-n is a WEIGHT-CONCENTRATION statistic, not a count.  Printed beside it: sum(K), the')
print('  effective number of rows the cell actually averages, and n_half, rows at >=0.5 kernel weight.')
print('  CI is a 600-rep row-resample 90%% percentile interval on the cell value (in D1 units).')
for lab, dg, kn in (('3-axis A/B (3 sa knots)', D3A, SAK3), ('3-axis C (5 sa knots)', D3C, QS)):
    print('\n  --- %s ---' % lab)
    print('  %-8s %6s %8s %6s %7s %7s %8s %7s %10s %22s %9s' %
          ('class', 'pick', 'sa-knot', 'stage', 'hp', 'hs', 'eff-n', 'sumK', 'nhalf', 'value [90% CI]', 'CI width'))
    for e in dg:
        if e['cls'] == 'RUCK': continue   # identical to KPP (both pooled) - printed once
        print('  %-8s %6.0f %8.3f %6d %7.3f %7s %8.1f %7.1f %10d %+10.3f [%+6.2f,%+6.2f] %9.3f' %
              (e['cls'], e['pk'], e['u'], e['stage'], e['hp'],
               ('%.3f' % e['hs']) if e['hs'] is not None else 'inf',
               e['effn'], e['sumK'], e['nhalf'], e['val'], e['ci'][0], e['ci'][1],
               e['ci'][1] - e['ci'][0]))
    ws = [e['ci'][1] - e['ci'][0] for e in dg]
    print('  CI width over all cells: median %.3f  min %.3f  max %.3f  (in units of D1 = %.4f, so median'
          ' CI = %.1f%% of the headline residual)' %
          (float(np.median(ws)), min(ws), max(ws), D1, 100 * float(np.median(ws))))
    st = {1: 0, 2: 0, 3: 0}
    for e in dg: st[e['stage']] += 1
    print('  pooling: own-class %d   POOLED over classes %d   sa axis COLLAPSED %d   of %d cells'
          % (st[1], st[2], st[3], len(dg)))

# two-axis comparison of CI width
print('\n  --- two-axis control, same diagnostics ---')
for c in CLASSES:
    if c != 'nonKPP': continue
    rc = [x for x in NONKPD if x['cls'] == c]
    for j, lpk in enumerate(LPK):
        h = 0.18
        while True:
            K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in rc]
            if eff_n(rc, K) >= EFFN or h > 3.0: break
            h *= 1.15
        sk, nh = kernel_mass(K); lo, hi = boot_ci(rc, K)
        print('  %-8s %6.0f %8s %6d %7.3f %7s %8.1f %7.1f %10d %+10.3f [%+6.2f,%+6.2f] %9.3f' %
              (c, PK_KNOTS[j], '-', 1, h, '-', eff_n(rc, K), sk, nh,
               loc_delta(rc, K) / D1, lo / D1, hi / D1, (hi - lo) / D1))

print('\n' + '=' * 116)
print('KPD AND THE ND TOP-PICK FALLERS')
print('=' * 116)
print('  KPD: excluded from the base kernel on every surface tested (the shipped exclusion is untouched');
print('       by adding an axis), so the bonus-dial delta on a KPD row is IDENTICALLY 0 at every')
print('       intensity.  The KPD sub-dial RL_G6_KPD ships 0 and nothing here moves it.')
for s in SURF:
    kd = [x for x in Y1 if x['iskpd']]
    mx = max(abs(s['delta_of'](x, 1.0)) for x in kd)
    print('    %-50s max |delta| on a KPD row at W=1 = %.10f' % (s['name'], mx))

print('\n  THE FIVE ND TOP-PICK FALLERS (rung 0.25 board, movers_rung0.25.json).  Their board `sa` is')
print('  NOT in any committed artefact, so their three-axis delta is reported ACROSS the sa terciles.')
FALL = [('zeke-uwland', 'SD', 2, 2322.949, 16, 18, -0.004966),
        ('willem-duursma', 'MID', 1, 4035.462, 18, 18, -0.003174),
        ('finn-o-sullivan', 'MID', 2, 3335.157, 38, 18, -0.001146),
        ('sam-lalor', 'MID', 1, 4325.017, 21, 18, -0.000792),
        ('jagga-smith', 'MID', 3, 4780.166, 19, 18, -0.000613)]
print('  %-18s %4s %6s %9s %11s %11s %11s %11s' %
      ('player', 'pick', 'games', '2ax@1.0', '3axA lo-sa', '3axA mid', '3axA hi-sa', '3axB(hi z)'))
d2 = SURF[0]['delta_of']; dA = SURF[1]['delta_of']; dB = SURF[2]['delta_of']
for key, pos, pk, e, g, age, td25 in FALL:
    # recover z from the shipped two-axis taught_delta at W=0.25 (everything else is known)
    lp = float(np.log(pk)); lg = float(np.log1p(g))
    b = float(np.interp(lp, LPK, B2['nonKPP']))
    denom = 0.25 * D1 * (b / SURF[0]['diag']['Z']) * s_tau(1.0) * s_g(lg)
    szhat = td25 / denom if abs(denom) > 1e-12 else float('nan')
    zhat = float(np.interp(szhat, list(reversed(SURF[0]['diag'].get('SZ_shipped', SZ0))),
                           list(reversed(Z_KNOTS)))) if False else None
    rowbase = dict(cls='nonKPP', pos=pos, pk=pk, lp=lp, lg=lg, tau=1.0, gcum=g, age=age,
                   tp=1.0, ta=1.0, iskpd=False, z=0.0, u=0.0)
    vals = []
    for uu in (SAK3[0], SAK3[1], SAK3[2]):
        r = dict(rowbase); r['u'] = uu
        vals.append(dA(r, 1.0))
    rB = dict(rowbase); rB['u'] = SAK3[2]; rB['z'] = Z_KNOTS[-1]
    print('  %-18s %4d %6d %+9.5f %+11.5f %+11.5f %+11.5f %+11.5f' %
          (key, pk, g, td25 * 4.0, vals[0], vals[1], vals[2], dB(rB, 1.0)))
print('  (2ax@1.0 = the shipped board figure x4, the surface being linear in intensity.)')
print('  Sz implied for each faller from the shipped delta is high-z (top picks price far above their')
print('  entry anchor), so under 3-axis B the z gate DAMPS their fall; under 3-axis A there is no z')
print('  gate and the fall is set by the sa cell alone.')

print('\n' + '=' * 116)
print('DECLARED-TAPER SENSITIVITY (the 41-64 bound is what strikes every three-axis variant)')
print('=' * 116)
print('  The shipped endpoints 34->48 are a DECLARED boundary and were deliberately NOT re-picked by')
print('  the repair.  Measured here, held fixed, and then re-measured at the 32->44 endpoints the')
print('  shipped sweep printed as the only pair MEETING the 0.5pp bound at rung 1.0.  Reported as a')
print('  measurement only.')
for nm, bf, gts in (('CONTROL 2-axis', lambda x: b2_of(B2, x), ('z',)),
                    ('3-axis A', mk_b3(B3, SAK3), ()),
                    ('3-axis B', mk_b3(B3, SAK3), ('z',)),
                    ('3-axis C', mk_b3(B5, QS), ())):
    d, dg = build(bf, gts, 32.0, 44.0)
    a = assess(nm, d, dg)
    print('  %-16s endpoints 32->44 :  41-64 move@1.0 %+0.5f   W_max ALL %.4f (%s)   landing@W_max %.6f'
          % (nm, a['G']['picks 41-64 (declared taper)']['v1'], a['wmax_all'], a['wby_all'],
             BASE_LANDING + LIFT1 * (a['agg1'] / ref['agg1']) * a['wmax_all']))
