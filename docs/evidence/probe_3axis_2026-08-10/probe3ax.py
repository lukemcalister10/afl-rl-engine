"""PROBE 3AX (READ-ONLY MEASUREMENT).  Owner ruling 2.4: can a THREE-AXIS stage-6 surface
(log-pick x position class x demonstrated performance on `sa`) deliver materially more of the
measured development residual than the shipped TWO-AXIS surface, while holding the already-priced
cells at zero?

Conventions taken VERBATIM from the stage-6 conformance repair (teach_g6.py / probes_g6.py):
  - population: s6_rows.json, nd, pk 1..64, classes 2004-2022, N==1 for the kernel (n=414), N 1..3
    pooled on the continuous clock for the fade.
  - estimand: the REGISTERED F (fixed career-year-4 discounted at 1.0939); r = F - price;
    every local read is the value-weighted residual ratio loc_delta = sum(K r)/sum(K price).
  - eff-n on the INFLUENCE weight (kernel x price), threshold 35, bandwidth grown x1.15.
  - single declared conservation scalar Z on the taper-supported bonus population.
  - declared pick taper 34->48, declared age taper 18->19, KPD excluded from the base kernel.
Nothing is written outside /tmp.
"""
import json, math, sys
import numpy as np

S = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ROWS = json.load(open(S + '/s6_rows.json'))

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


def tpk(pk):
    if pk <= PK_LO: return 1.0
    if pk >= PK_HI: return 0.0
    return float(0.5 * (1.0 + np.cos(np.pi * (pk - PK_LO) / (PK_HI - PK_LO))))


def tage(a):
    if a is None: return 0.0
    if a <= AGE_LO: return 1.0
    if a >= AGE_HI: return 0.0
    return float(0.5 * (1.0 + np.cos(np.pi * (a - AGE_LO) / (AGE_HI - AGE_LO))))


for x in POP:
    x['lp'] = float(np.log(min(max(x['pk'], 1), 90)))
    x['z'] = float(np.clip(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)), Z_KNOTS[0], Z_KNOTS[-1]))
    x['lg'] = float(np.log1p(max(x['gcum'], 0.0)))
    x['r'] = x['F'] - x['price']
    x['tp'] = tpk(x['pk']); x['ta'] = tage(x['age'])
    x['iskpd'] = (x['pos'] == 'KPD')

NONKPD = [x for x in Y1 if not x['iskpd']]
# ---- the sa axis, standardised on the bonus (non-KPD) year-1 population -------------------------
SA_MU = float(np.mean([x['sa'] for x in NONKPD]))
SA_SD = float(np.std([x['sa'] for x in NONKPD]))
for x in POP:
    x['u'] = (x['sa'] - SA_MU) / SA_SD

# registered gate thresholds are terciles over ALL year-1 ND 1-64 rows (probes_g6.py convention)
sas = sorted(x['sa'] for x in Y1)
SAMED = sas[len(sas) // 2]
SAT2 = sas[2 * len(sas) // 3]
SAT1 = sas[len(sas) // 3]


def loc_delta(rows, K):
    num = float(sum(K[i] * rows[i]['r'] for i in range(len(rows))))
    den = float(sum(K[i] * rows[i]['price'] for i in range(len(rows))))
    return (num / den) if den > 1e-9 else 0.0


def eff_n(rows, K):
    W = np.array([K[i] * rows[i]['price'] for i in range(len(rows))])
    s2 = float((W * W).sum())
    return (float(W.sum()) ** 2 / s2) if s2 > 0 else 0.0


D1 = loc_delta(NONKPD, [1.0] * len(NONKPD))
DKPD = loc_delta([x for x in Y1 if x['iskpd']], [1.0] * len([x for x in Y1 if x['iskpd']]))

# ---- the fade (identical to shipped; taught on the whole POP, not per-cell) ----------------------
raw = []
for t in TAU_KNOTS:
    sub = [x for x in POP if abs(x['tau'] - t) < 0.5 and not x['iskpd']]
    raw.append(loc_delta(sub, [1.0] * len(sub)))
unc = [v / D1 for v in raw]
iso = []; cur = 1.0
for v in unc:
    cur = min(cur, max(0.0, min(1.0, v))); iso.append(cur)
iso[0] = 1.0
STAU = iso


def s_tau(t):
    return float(np.interp(t, [0.0] + TAU_KNOTS, [STAU[0]] + STAU)) if t <= TAU_KNOTS[-1] else 0.0


# ---- Sg and Sz (Sz used only by the two-axis control and by variant B) --------------------------
def shape(keyf, knots, h0):
    h = h0; vals = []; ens = []
    for kk in knots:
        K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        while eff_n(NONKPD, K) < EFFN and h < 9.0:
            h *= 1.15
            K = [float(np.exp(-0.5 * ((keyf(x) - kk) / h) ** 2)) for x in NONKPD]
        vals.append(loc_delta(NONKPD, K) / D1); ens.append(round(eff_n(NONKPD, K), 1))
    return vals, ens, h


SZ0, SZ_EN, SZ_BW = shape(lambda x: x['z'], Z_KNOTS, (Z_KNOTS[1] - Z_KNOTS[0]) * 1.1)
SG, SG_EN, SG_BW = shape(lambda x: x['lg'], LGK, (LGK[1] - LGK[0]) * 1.1)


def s_g(lg): return float(np.interp(lg, LGK, SG))


# =================================================================================================
# THE THREE-AXIS KERNEL
# =================================================================================================
def teach_3ax(sa_knots_u, hs0, label, pool_log):
    """B3[cls][j][m] = loc_delta over a product Gaussian in (log-pick, standardised sa) / D1.
    Bandwidths are grown TOGETHER by x1.15 until eff-n >= 35 (the shipped idiom, lifted to 2-D).
    Pooling ladder, each step DECLARED per cell:
        1. own class, own (pick,sa) cell
        2. pooled over classes (all non-KPD), own (pick,sa) cell
        3. pooled over classes AND over sa (i.e. the two-axis value) -- the sa axis collapses
    """
    B3 = {c: [[0.0] * len(sa_knots_u) for _ in LPK] for c in CLASSES}
    for c in CLASSES:
        rows_c = [x for x in NONKPD if x['cls'] == c]
        for j, lpk in enumerate(LPK):
            for m, sak in enumerate(sa_knots_u):
                got = None
                for stage, src in ((1, rows_c), (2, NONKPD)):
                    if not src: continue
                    hp, hs = 0.18, hs0
                    while True:
                        K = [float(np.exp(-0.5 * (((x['lp'] - lpk) / hp) ** 2 +
                                                  ((x['u'] - sak) / hs) ** 2))) for x in src]
                        en = eff_n(src, K)
                        if en >= EFFN or hp > 3.0: break
                        hp *= 1.15; hs *= 1.15
                    if en >= EFFN:
                        got = (stage, loc_delta(src, K) / D1, hp, hs, en, len(src))
                        break
                if got is None:
                    # stage 3: collapse the sa axis entirely for this (class, pick) cell
                    hp = 0.18
                    while True:
                        K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / hp) ** 2)) for x in NONKPD]
                        en = eff_n(NONKPD, K)
                        if en >= EFFN or hp > 3.0: break
                        hp *= 1.15
                    got = (3, loc_delta(NONKPD, K) / D1, hp, float('inf'), en, len(NONKPD))
                B3[c][j][m] = got[1]
                pool_log.append(dict(label=label, cls=c, pick_knot=PK_KNOTS[j],
                                     sa_knot_u=round(sak, 4), stage=got[0],
                                     hp=round(got[2], 4), hs=(None if got[3] == float('inf') else round(got[3], 4)),
                                     effn=round(got[4], 1), n_src=got[5], val=round(got[1], 5)))
    return B3


def b3_of(B3, x, sa_knots_u):
    tab = B3[x['cls']]
    col = [float(np.interp(x['u'], sa_knots_u, tab[j])) for j in range(len(LPK))]
    return float(np.interp(x['lp'], LPK, col))


# =================================================================================================
# common machinery: conservation solve, gate measurement
# =================================================================================================
sup = [x for x in NONKPD if x['tp'] * x['ta'] > 0.0]
MEAS_SUP = loc_delta(sup, [1.0] * len(sup))


def build_surface(bfun, use_sz, szvals):
    """Returns delta_of(x, W) with the single declared conservation scalar Z solved on `sup`,
    plus the diagnostics.  Monotonicity kappa is solved only when Sz is present (it is the only
    axis that can invert prices)."""
    SZ = list(szvals)
    WMZ = (sum(x['price'] * float(np.interp(x['z'], Z_KNOTS, szvals)) for x in NONKPD) /
           sum(x['price'] for x in NONKPD))

    def m_of(x, SZL):
        s = s_tau(x['tau']) * s_g(x['lg']) * x['tp'] * x['ta']
        if use_sz: s *= float(np.interp(x['z'], Z_KNOTS, SZL))
        return s

    KAPPA = 1.0
    for _ in range(400):
        SZ = [WMZ + KAPPA * (v - WMZ) for v in szvals] if use_sz else szvals
        raw_t = sum(x['price'] * D1 * bfun(x) * m_of(x, SZ) for x in sup) / sum(x['price'] for x in sup)
        ZC = raw_t / MEAS_SUP
        assert 0.3 < ZC < 3.0, 'conservation normaliser out of the sane range'
        if not use_sz:
            break
        # monotonicity sweep, shipped grid
        worst = 9.9
        zs = np.linspace(Z_KNOTS[0], Z_KNOTS[-1], 121)
        for c in CLASSES:
            for pk in (3, 5, 8, 12, 15, 20, 25, 30, 35, 40, 45):
                tt = tpk(pk)
                if tt == 0.0: continue
                for g in (6.0, 10.0, 16.0, 24.0):
                    for t in (1.0, 1.5):
                        probe = dict(cls=c, pk=pk, lp=float(np.log(pk)), lg=float(np.log1p(g)),
                                     tau=t, tp=tt, ta=1.0, u=0.0, z=0.0, iskpd=False)
                        bb = bfun(probe) / ZC
                        base = D1 * bb * s_tau(t) * s_g(probe['lg']) * tt
                        d = [base * float(np.interp(z, Z_KNOTS, SZ)) for z in zs]
                        for i in range(1, len(zs)):
                            dd = (d[i] - d[i - 1]) / (zs[i] - zs[i - 1])
                            worst = min(worst, 1.0 + d[i] + dd)
        if worst > 0.02:
            break
        KAPPA *= 0.97

    def delta_of(x, W):
        if x['iskpd']: return 0.0
        if x['tp'] <= 0 or x['age'] is None or x['ta'] <= 0: return 0.0
        return float(W) * D1 * (bfun(x) / ZC) * m_of(x, SZ)

    return delta_of, dict(Z=ZC, kappa=KAPPA, SZ=[round(v, 5) for v in SZ])


GATES = [('picks 1-10 x TOP-TERCILE sa  [REGISTERED]', lambda x: x['pk'] <= 10 and x['sa'] >= SAT2, 0.015),
         ('picks 1-20 x ABOVE-MEDIAN sa [REGISTERED]', lambda x: x['pk'] <= 20 and x['sa'] >= SAMED, 0.025),
         ('picks 41-64 (declared taper)', lambda x: 41 <= x['pk'] <= 64, 0.005),
         ('draft age 19+ (declared taper)', lambda x: x['age'] is not None and x['age'] >= 19, 0.005),
         ('draft age UNKNOWN (identically 0)', lambda x: x['age'] is None, 0.0)]
RUNGS = [0.25, 0.5, 0.75, 1.0]


def report(name, delta_of, diag, extra_cells=()):
    print('\n' + '=' * 104)
    print('SURFACE: %s' % name)
    print('=' * 104)
    print('  conservation Z = %.6f   |Z-1| = %.4f   L-SMOOTH kappa = %.6f'
          % (diag['Z'], abs(diag['Z'] - 1), diag['kappa']))
    sp1 = sum(x['price'] for x in Y1)
    agg1 = sum(x['price'] * delta_of(x, 1.0) for x in Y1) / sp1
    spS = sum(x['price'] for x in sup)
    aggS = sum(x['price'] * delta_of(x, 1.0) for x in sup) / spS
    print('  taught aggregate delta at W=1, year-1 whole leg (n=%d)         %+0.6f' % (len(Y1), agg1))
    print('  taught aggregate delta at W=1, taper-supported bonus pop (n=%d) %+0.6f   [measured %+0.6f]'
          % (len(sup), aggS, MEAS_SUP))
    print('\n  %-42s %5s %7s %10s %10s %10s %10s' % ('cell', 'n', 'bound', 'W=.25', 'W=.50', 'W=.75', 'W=1.0'))
    print('  ' + '-' * 100)
    wmax = 9.9; wby = None
    G = {}
    for nm, f, bound in GATES:
        sub = [x for x in Y1 if f(x)]
        if not sub: continue
        sp = sum(x['price'] for x in sub)
        v1 = sum(x['price'] * delta_of(x, 1.0) for x in sub) / sp
        vals = [v1 * W for W in RUNGS]
        meas = sum(x['F'] for x in sub) / sp - 1.0
        G[nm] = dict(n=len(sub), bound=bound, v1=v1, measured=meas)
        print('  %-42s %5d %7.3f %+10.5f %+10.5f %+10.5f %+10.5f   [measured %+0.4f]'
              % (nm, len(sub), bound, vals[0], vals[1], vals[2], vals[3], meas))
        if abs(v1) > 1e-12:
            w = bound / abs(v1)
            if w < wmax: wmax, wby = w, nm
    for nm, f in extra_cells:
        sub = [x for x in Y1 if f(x)]
        if not sub: continue
        sp = sum(x['price'] for x in sub)
        v1 = sum(x['price'] * delta_of(x, 1.0) for x in sub) / sp
        meas = sum(x['F'] for x in sub) / sp - 1.0
        print('  %-42s %5d %7s %+10.5f %+10.5f %+10.5f %+10.5f   [measured %+0.4f]'
              % ('  [disclosed] ' + nm, len(sub), '-', v1 * .25, v1 * .5, v1 * .75, v1, meas))
    print('\n  MAX FEASIBLE INTENSITY on the registered gates = %.4f   bound by: %s' % (wmax, wby))
    # tail-vs-typical
    print('\n  %-10s %10s %12s %12s %14s' % ('W', "agg F'", "corr agg F'", "corr median F'", 'frac out-earn'))
    sp = sum(x['price'] for x in Y1)
    agg0 = sum(x['F'] for x in Y1) / sp
    med0 = float(np.median([x['F'] / x['price'] for x in Y1]))
    frac0 = float(np.mean([1.0 if x['F'] > x['price'] else 0.0 for x in Y1]))
    print('  %-10s %10.4f %12.4f %12.4f %14.3f' % ('0', agg0, agg0, med0, frac0))
    TT = {}
    for W in RUNGS + [round(wmax, 4)]:
        newp = [x['price'] * (1.0 + delta_of(x, W)) for x in Y1]
        aggc = sum(x['F'] for x in Y1) / sum(newp)
        medc = float(np.median([Y1[i]['F'] / newp[i] for i in range(len(Y1))]))
        fr = float(np.mean([1.0 if Y1[i]['F'] > newp[i] else 0.0 for i in range(len(Y1))]))
        TT[W] = (aggc, medc, fr)
        print('  %-10s %10.4f %12.4f %12.4f %14.3f' % (W, agg0, aggc, medc, fr))
    # corner
    mx = max((abs(delta_of(x, 1.0)), x['key'], x['pk']) for x in Y1)
    print('\n  max |taught delta| on a REALISED teaching row at W=1: %.4f (%s, pick %d)' % mx)
    return dict(agg1=agg1, aggS=aggS, wmax=wmax, wby=wby, gates=G, tt=TT)


# =================================================================================================
print('=' * 104)
print('POPULATION / ESTIMAND CHECK')
print('=' * 104)
print('  year-1 ND 1-64 rows n=%d   bonus (non-KPD) n=%d   KPD n=%d' % (len(Y1), len(NONKPD), len(Y1) - len(NONKPD)))
print("  year-1 value-weighted aggregate F' (whole leg) = %.6f   [record 1.136]"
      % (sum(x['F'] for x in Y1) / sum(x['price'] for x in Y1)))
print('  D1 (bonus population residual) = %+0.6f    D_KPD = %+0.6f' % (D1, DKPD))
print('  measured residual on taper-supported bonus population = %+0.6f (n=%d)' % (MEAS_SUP, len(sup)))
print('  sa: mean %.3f sd %.3f   tercile knots %.2f / %.2f   median %.2f' % (SA_MU, SA_SD, SAT1, SAT2, SAMED))
print('  sa in standardised units: t1 %.4f  t2 %.4f  med %.4f'
      % ((SAT1 - SA_MU) / SA_SD, (SAT2 - SA_MU) / SA_SD, (SAMED - SA_MU) / SA_SD))
print('  fade installed Stau = %s (unclamped %s)' % ([round(v, 4) for v in STAU], [round(v, 4) for v in unc]))
print('  Sz = %s (eff-n %s, bw %.3f)' % ([round(v, 4) for v in SZ0], SZ_EN, SZ_BW))
print('  Sg = %s (eff-n %s, bw %.3f)' % ([round(v, 4) for v in SG], SG_EN, SG_BW))

# ---------------- CONTROL: the shipped two-axis surface ------------------------------------------
POOL2 = []
B2 = {}
for c in CLASSES:
    rows_c = [x for x in NONKPD if x['cls'] == c]
    vals = []; ok = bool(rows_c)
    for j, lpk in enumerate(LPK):
        h = 0.18
        while True:
            K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in rows_c]
            en = eff_n(rows_c, K)
            if en >= EFFN or h > 3.0: break
            h *= 1.15
        if en < EFFN: ok = False
        vals.append(loc_delta(rows_c, K) / D1 if rows_c else 0.0)
    if not ok:
        POOL2.append(c)
        vals = []
        for j, lpk in enumerate(LPK):
            h = 0.18
            while True:
                K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in NONKPD]
                if eff_n(NONKPD, K) >= EFFN or h > 3.0: break
                h *= 1.15
            vals.append(loc_delta(NONKPD, K) / D1)
    B2[c] = vals
print('\n  two-axis kernel pooled classes: %s' % POOL2)
for c in CLASSES:
    print('    B2[%-6s] = %s' % (c, [round(v, 4) for v in B2[c]]))

d2, diag2 = build_surface(lambda x: float(np.interp(x['lp'], LPK, B2[x['cls']])), True, SZ0)
R2 = report('CONTROL — shipped TWO-AXIS (log-pick x class), Sz shape gate on z', d2, diag2)

# ---------------- THREE-AXIS, primary: 3 sa knots at the tercile boundaries ----------------------
POOL3 = []
SAK3 = [(SAT1 - SA_MU) / SA_SD, (SAMED - SA_MU) / SA_SD, (SAT2 - SA_MU) / SA_SD]
HS0 = float(np.mean(np.diff(SAK3))) * 1.1
B3a = teach_3ax(SAK3, HS0, '3ax-3knot', POOL3)
d3a, diag3a = build_surface(lambda x: b3_of(B3a, x, SAK3), False, SZ0)
R3a = report('THREE-AXIS A — log-pick x class x sa (3 knots), Sz DROPPED (sa carries the level axis)',
             d3a, diag3a)

# ---------------- THREE-AXIS, variant B: 3 sa knots, Sz RETAINED --------------------------------
POOL3b = []
B3b = teach_3ax(SAK3, HS0, '3ax-3knot-withSz', POOL3b)
d3b, diag3b = build_surface(lambda x: b3_of(B3b, x, SAK3), True, SZ0)
R3b = report('THREE-AXIS B — log-pick x class x sa (3 knots), Sz RETAINED (disclosed variant)',
             d3b, diag3b)

# ---------------- THREE-AXIS, variant C: 5 sa knots (finer) -------------------------------------
POOL3c = []
qs = [float(np.quantile([x['u'] for x in NONKPD], q)) for q in (0.1, 0.3, 0.5, 0.7, 0.9)]
HS0c = float(np.mean(np.diff(qs))) * 1.1
B3c = teach_3ax(qs, HS0c, '3ax-5knot', POOL3c)
d3c, diag3c = build_surface(lambda x: b3_of(B3c, x, qs), False, SZ0)
R3c = report('THREE-AXIS C — log-pick x class x sa (5 knots, finer), Sz dropped', d3c, diag3c)

# ---------------- pooling disclosure -------------------------------------------------------------
print('\n' + '=' * 104)
print('POOLING DISCLOSURE — every three-axis cell, its resolution stage and its bandwidths')
print('=' * 104)
for lab, pl, kn in (('A (3 knots, no Sz)', POOL3, SAK3), ('C (5 knots)', POOL3c, qs)):
    print('\n  surface %s   sa knots (standardised) %s   start bandwidth hs0' % (lab, [round(k, 3) for k in kn]))
    print('  %-8s %8s %10s %7s %8s %8s %8s %9s' % ('class', 'pickknot', 'sa knot u', 'stage', 'hp', 'hs', 'eff-n', 'value'))
    ns = {1: 0, 2: 0, 3: 0}
    for e in pl:
        ns[e['stage']] += 1
        print('  %-8s %8.0f %10.3f %7d %8.3f %8s %8.1f %+9.4f'
              % (e['cls'], e['pick_knot'], e['sa_knot_u'], e['stage'], e['hp'],
                 ('%.3f' % e['hs']) if e['hs'] is not None else 'inf', e['effn'], e['val']))
    print('  stage counts: own-class %d   POOLED over classes %d   sa axis COLLAPSED %d   (of %d cells)'
          % (ns[1], ns[2], ns[3], len(pl)))

# ---------------- summary -------------------------------------------------------------------------
BASE_LANDING = 0.990805
LIFT1_2AX = 1.071991 - BASE_LANDING     # delivered board lift at W=1 for the shipped surface
print('\n' + '=' * 104)
print('SUMMARY — max feasible intensity and implied ND year-1 landing')
print('=' * 104)
print('  linearity check on the published two-axis landings (0.25/0.5/0.75/1.0):')
lands = [1.011071, 1.031377, 1.051681, 1.071991]
print('    %s   first differences %s' % (lands, [round(lands[i + 1] - lands[i], 6) for i in range(3)]))
print('    linear fit intercept %.6f vs the quoted base %.6f (gap %.6f)'
      % (lands[0] - 0.25 * (lands[3] - lands[0]) / 0.75, BASE_LANDING,
         lands[0] - 0.25 * (lands[3] - lands[0]) / 0.75 - BASE_LANDING))
print()
print('  %-46s %9s %9s %11s %11s' % ('surface', 'agg@W=1', 'W_max', 'lift@W_max', 'yr-1 land'))
for nm, R in (('two-axis (shipped, control)', R2),
              ('three-axis A (sa 3 knots, Sz dropped)', R3a),
              ('three-axis B (sa 3 knots, Sz retained)', R3b),
              ('three-axis C (sa 5 knots, Sz dropped)', R3c)):
    scale = R['agg1'] / R2['agg1']
    lift = LIFT1_2AX * scale * R['wmax']
    print('  %-46s %+9.6f %9.4f %11.6f %11.6f'
          % (nm, R['agg1'], R['wmax'], lift, BASE_LANDING + lift))
    print('  %-46s %s' % ('    bound by', R['wby']))
print('\n  (landing proxy: board lift scales with the surface\'s value-weighted taught aggregate on the')
print('   teaching rows, at the shipped surface\'s measured delivery of %.6f per unit of intensity.)' % LIFT1_2AX)
