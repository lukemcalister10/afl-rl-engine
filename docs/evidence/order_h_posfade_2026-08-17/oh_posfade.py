#!/usr/bin/env python3
"""ORDER H — the POSITION lens on the year-1/2 sitter fade (PREREG_H.md, pushed first at 587bf76).

Plain words: Order D asked how much a year-one sit hurts, and let the answer bend with draft pick.
It never asked whether the answer is different for a ruck than for a mid. The owner asked that.
This harness asks it on D's own population, with D's own rulers, and changes nothing else.

Population, washout ruler and value ruler are copied verbatim from
  docs/evidence/order_d_2026-08-17/o35_fit_curve.py
  docs/evidence/order_d_2026-08-17/o35_value_contrast.py
"""
import os, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

# ---- D's constants, unchanged ----
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
D2 = 0.5582775239783688      # the ruled depth-2 fade
S_SH = 3.0
LB, LM, LW, LG = 105.0, 109.5, 1.85, 1.00
CARRY = 1.14
FM = {'paddy-mccartin', 'thomas-boyd'}
SEED = 35
B = 1000

GRP = {'RUCK': 'RUCK', 'KPD': 'KPP', 'KPF': 'KPP', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL'}
GROUPS = ('SMALL', 'KPP', 'RUCK')


def sp(x): return math.log1p(math.exp(x)) if x < 30 else x
def cp(l):
    c = LG * LW * (sp((l - LM) / LW) - sp((LB - LM) / LW))
    return c if c > 0 else 0.0
def pv(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def ws(g): return min(1.0, math.sqrt(max(0.0, g) / 10.0))


# ------------------------------------------------------------------ population
A = json.load(open(SP + '/per_entrant_O32RFINAL.json'))
print('store md5 %s ; engine %s ; board %s' % (A['meta']['store_md5'], A['meta']['engine_head'],
                                               A['meta']['basis_29c']['replication_board']))
ROWS = []
for r in A['recs']:
    if r['key'] in FM or not (r.get('teaches_curve') and r['type'] == 'ND'):
        continue
    if not (2005 <= r['year'] <= 2020) or not r.get('pick') or not (1 <= r['pick'] <= 64):
        continue
    sdv = 0.0
    for s in r['seasons']:
        if r['year'] < s['year'] <= r['year'] + 5 and s.get('bar') in BARS:
            sdv += float(s['games']) * max(0.0, float(s['avg']) - BARS[s['bar']])
    dv = 0.0
    for s in r['seasons']:
        if s['year'] > 2025 or s.get('bar') not in BARS:
            continue
        if s['year'] >= r['year'] + 2:
            dv += (CARRY ** -(s['year'] - (r['year'] + 1))) * ws(s['games']) \
                  * pv(s['avg'] + cp(s['avg']) - BARS[s['bar']]) * 21.0
    g1 = int(r.get('games_yr1') or 0)
    g12 = int(r['games_by']['2'])
    ROWS.append(dict(key=r['key'], player=r['player'], pick=int(r['pick']), pos=r['pos'],
                     grp=GRP[r['pos']], g1=g1, g12=g12, v0=float(r['v0']), dv=dv,
                     w=1.0 if sdv <= 0.0 else 0.0))
print('population: %d ND entrants 2005-2020, picks 1-64 (D\'s exact population)' % len(ROWS))
OUT = dict(order='ORDER H — the position lens on the year-1/2 sitter fade',
           prereg='PREREG_H.md @ 587bf76', n_population=len(ROWS))

# ------------------------------------------------------------------ 0. base rates (H3)
print('\n== SECTION 0. BASE RATES — is early sitting really more common for talls? (H3) ==')
print('%-6s %6s %10s %8s %10s %8s %8s' % ('group', 'n', 'sat_yr1', 'rate', 'sat_yr1+2', 'rate', 'played1+'))
BR = {}
for g in GROUPS:
    rs = [r for r in ROWS if r['grp'] == g]
    s1 = sum(1 for r in rs if r['g1'] == 0)
    s12 = sum(1 for r in rs if r['g12'] == 0)
    p1 = sum(1 for r in rs if r['g1'] >= 1)
    BR[g] = dict(n=len(rs), sat1=s1, rate1=s1 / len(rs), sat12=s12, rate12=s12 / len(rs),
                 played1p=p1, played11p=sum(1 for r in rs if r['g1'] >= 11))
    print('%-6s %6d %10d %8.3f %10d %8.3f %8d' % (g, len(rs), s1, s1 / len(rs), s12, s12 / len(rs), p1))
OUT['base_rates'] = BR


def irls(X, y, ridge=1e-9, iters=80):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = np.clip(X @ b, -30, 30)
        mu = 1.0 / (1.0 + np.exp(-eta))
        Wd = np.clip(mu * (1 - mu), 1e-9, None)
        z = eta + (y - mu) / Wd
        XtW = X.T * Wd
        bn = np.linalg.solve(XtW @ X + ridge * np.eye(X.shape[1]), XtW @ z)
        if np.max(np.abs(bn - b)) < 1e-10:
            return bn
        b = bn
    return b


def boot(rows, fn, seed=SEED, n=B):
    rng = np.random.default_rng(seed)
    keep = []
    for _ in range(n):
        idx = rng.integers(0, len(rows), len(rows))
        try:
            v = fn([rows[i] for i in idx])
            if v is not None and np.all(np.isfinite(v)):
                keep.append(v)
        except Exception:
            continue
    return np.array(keep)


def ci90(a):
    return [float(np.percentile(a, 5)), float(np.percentile(a, 95))]


# pick-controlled base rate: logit P(sat) = a + b ln(pick) + d_KPP + d_RUCK
def satfit(rows, key='g1'):
    X = np.array([[1.0, math.log(r['pick']), 1.0 * (r['grp'] == 'KPP'), 1.0 * (r['grp'] == 'RUCK')]
                  for r in rows])
    y = np.array([1.0 if r[key] == 0 else 0.0 for r in rows])
    return irls(X, y)


for key, lab in (('g1', 'SAT1  (0 games year 1)'), ('g12', 'SAT12 (0 games years 1+2)')):
    bb = satfit(ROWS, key)
    BS = boot(ROWS, lambda rr, k=key: satfit(rr, k))
    print('\npick-controlled odds of %s, vs SMALL at the same pick:' % lab)
    for j, g in ((2, 'KPP'), (3, 'RUCK')):
        print('  %-5s log-odds %+.3f -> odds ratio %5.2fx   90%% CI [%.2f, %.2f]'
              % (g, bb[j], math.exp(bb[j]), math.exp(np.percentile(BS[:, j], 5)),
                 math.exp(np.percentile(BS[:, j], 95))))
    OUT.setdefault('base_rate_pickcontrolled', {})[key] = dict(
        coef=[float(x) for x in bb],
        or_KPP=math.exp(bb[2]), or_KPP_ci=[math.exp(x) for x in ci90(BS[:, 2])],
        or_RUCK=math.exp(bb[3]), or_RUCK_ci=[math.exp(x) for x in ci90(BS[:, 3])])

# ------------------------------------------------------------------ 1. the interaction
print('\n== SECTION 1. THE INTERACTION — does a sit mean something different for a ruck? ==')


def make_fit(satkey, ctl_min, pooled_tall):
    """Returns (fitrows, fitfn, names). SAT = 0 games; control = >= ctl_min games in year 1."""
    if satkey == 'g1':
        sat = [r for r in ROWS if r['g1'] == 0]
        ctl = [r for r in ROWS if r['g1'] >= ctl_min]
    else:
        sat = [r for r in ROWS if r['g12'] == 0]
        ctl = [r for r in ROWS if r['g12'] >= ctl_min]
    rows = sat + ctl
    sk = satkey

    def design(rr):
        cols, names = [], []
        for r in rr:
            s = 1.0 if r[sk] == 0 else 0.0
            lp = math.log(r['pick'])
            if pooled_tall:
                t = 1.0 * (r['grp'] in ('KPP', 'RUCK'))
                cols.append([1.0, lp, t, s, s * lp, s * t])
            else:
                k = 1.0 * (r['grp'] == 'KPP'); u = 1.0 * (r['grp'] == 'RUCK')
                cols.append([1.0, lp, k, u, s, s * lp, s * k, s * u])
        names = (['a', 'b_lnpick', 'c_TALL', 'g0_SAT', 'g1_SATxlnpick', 'h_TALL'] if pooled_tall
                 else ['a', 'b_lnpick', 'c_KPP', 'c_RUCK', 'g0_SAT', 'g1_SATxlnpick', 'h_KPP', 'h_RUCK'])
        return np.array(cols), names

    def fn(rr):
        X, _ = design(rr)
        y = np.array([r['w'] for r in rr])
        return irls(X, y)

    _, names = design(rows[:1])
    return rows, fn, names, len(sat), len(ctl)


RES = {}
for satkey, satlab in (('g1', 'SAT1'), ('g12', 'SAT12')):
    for ctl_min, ctllab in ((1, 'vs all played (PRIMARY)'), (11, 'vs played 11+ (D primary; secondary here)')):
        for pooled, plab in ((False, '3-group'), (True, 'TALL-pooled')):
            rows, fn, names, ns, nc = make_fit(satkey, ctl_min, pooled)
            # cell honesty
            cells = {g: dict(sat=sum(1 for r in rows if r['grp'] == g and r[satkey] == 0),
                             ctl=sum(1 for r in rows if r['grp'] == g and r[satkey] != 0))
                     for g in GROUPS}
            b = fn(rows)
            BS = boot(rows, fn)
            tag = '%s|%s|%s' % (satlab, 'ctl%d' % ctl_min, plab)
            d = dict(names=names, coef=[float(x) for x in b], n_sat=ns, n_ctl=nc, cells=cells,
                     ci={names[j]: ci90(BS[:, j]) for j in range(len(names))},
                     boot_ok=int(len(BS)))
            for j, nm in enumerate(names):
                if nm.startswith('h_'):
                    d['share_neg_' + nm] = float(np.mean(BS[:, j] < 0))
            RES[tag] = d
            print('\n-- %s, %s, %s  (sitters %d, controls %d)' % (satlab, ctllab, plab, ns, nc))
            print('   cells: ' + '  '.join('%s sat=%d ctl=%d' % (g, cells[g]['sat'], cells[g]['ctl']) for g in GROUPS))
            for j, nm in enumerate(names):
                star = ' <== interaction' if nm.startswith('h_') else ''
                print('   %-14s %+8.4f   90%% CI [%+.3f, %+.3f]%s'
                      % (nm, b[j], d['ci'][nm][0], d['ci'][nm][1], star))
            for nm in names:
                if nm.startswith('h_'):
                    print('   share of 1000 bootstrap draws with %s < 0 (the owner\'s direction): %.1f%%'
                          % (nm, 100 * d['share_neg_' + nm]))
OUT['interaction'] = RES

# ------------------------------------------------------------------ 2. value retention
print('\n== SECTION 2. VALUE RETENTION — D\'s 0.535 / 0.128 object, split by position ==')


def retention(rows_sat, rows_ctl):
    ds = sum(r['v0'] for r in rows_sat); dc = sum(r['v0'] for r in rows_ctl)
    if ds <= 0 or dc <= 0:
        return None
    rs = sum(r['dv'] for r in rows_sat) / ds
    rc = sum(r['dv'] for r in rows_ctl) / dc
    return (rs, rc, rs / rc if rc > 0 else float('nan'))


VR = {}
print('\nAll picks 1-64, sitters vs all who played (the primary control):')
print('%-6s %6s %6s %10s %10s %9s %22s' % ('group', 'n_sat', 'n_ctl', 'ret_sat', 'ret_ctl', 'F', '90% CI on F'))
for g in GROUPS:
    sat = [r for r in ROWS if r['grp'] == g and r['g1'] == 0]
    ctl = [r for r in ROWS if r['grp'] == g and r['g1'] >= 1]
    t = retention(sat, ctl)
    rng = np.random.default_rng(SEED)
    fs = []
    for _ in range(B):
        ss = [sat[i] for i in rng.integers(0, len(sat), len(sat))]
        cc = [ctl[i] for i in rng.integers(0, len(ctl), len(ctl))]
        tt = retention(ss, cc)
        if tt and np.isfinite(tt[2]):
            fs.append(tt[2])
    c = ci90(fs)
    VR[g] = dict(n_sat=len(sat), n_ctl=len(ctl), ret_sat=t[0], ret_ctl=t[1], F=t[2], ci90=c)
    print('%-6s %6d %6d %10.3f %10.3f %9.3f       [%.3f, %.3f]'
          % (g, len(sat), len(ctl), t[0], t[1], t[2], c[0], c[1]))
OUT['value_retention_allpicks'] = VR

# pick-matched: rucks who sit live at picks 31-64, so compare all three groups THERE
print('\nPick-controlled the honest way — the same pick window for every group.')
VRB = {}
for nm, lo, hi in (('1-30', 1, 30), ('31-64', 31, 64)):
    print('  picks %s:' % nm)
    print('  %-6s %6s %6s %10s %10s %9s %22s' % ('group', 'n_sat', 'n_ctl', 'ret_sat', 'ret_ctl', 'F', '90% CI on F'))
    for g in GROUPS:
        sat = [r for r in ROWS if r['grp'] == g and r['g1'] == 0 and lo <= r['pick'] <= hi]
        ctl = [r for r in ROWS if r['grp'] == g and r['g1'] >= 1 and lo <= r['pick'] <= hi]
        if len(sat) < 3 or len(ctl) < 3:
            print('  %-6s %6d %6d   -- cell too thin to read, reported as a count only'
                  % (g, len(sat), len(ctl)))
            VRB['%s|%s' % (nm, g)] = dict(n_sat=len(sat), n_ctl=len(ctl), F=None, note='too thin')
            continue
        t = retention(sat, ctl)
        rng = np.random.default_rng(SEED)
        fs = []
        for _ in range(B):
            ss = [sat[i] for i in rng.integers(0, len(sat), len(sat))]
            cc = [ctl[i] for i in rng.integers(0, len(ctl), len(ctl))]
            tt = retention(ss, cc)
            if tt and np.isfinite(tt[2]):
                fs.append(tt[2])
        c = ci90(fs)
        VRB['%s|%s' % (nm, g)] = dict(n_sat=len(sat), n_ctl=len(ctl), ret_sat=t[0], ret_ctl=t[1],
                                      F=t[2], ci90=c)
        print('  %-6s %6d %6d %10.3f %10.3f %9.3f       [%.3f, %.3f]'
              % (g, len(sat), len(ctl), t[0], t[1], t[2], c[0], c[1]))
OUT['value_retention_by_pickwindow'] = VRB

# raw washout rates per cell, for the reader who wants the plain count
print('\nPlain washout rates (share of the cell that delivered nothing above bar in 5 years):')
print('%-6s %22s %22s' % ('group', 'sat yr1', 'played yr1'))
WR = {}
for g in GROUPS:
    sat = [r for r in ROWS if r['grp'] == g and r['g1'] == 0]
    ctl = [r for r in ROWS if r['grp'] == g and r['g1'] >= 1]
    ws_, wc = np.mean([r['w'] for r in sat]), np.mean([r['w'] for r in ctl])
    WR[g] = dict(wash_sat=float(ws_), n_sat=len(sat), wash_ctl=float(wc), n_ctl=len(ctl),
                 gap=float(ws_ - wc))
    print('%-6s   %.3f (n=%3d)          %.3f (n=%3d)     gap %+.3f' % (g, ws_, len(sat), wc, len(ctl), ws_ - wc))
OUT['washout_rates'] = WR

# same, inside picks 31-64 only (where the ruck sitters are)
print('\nSame rates inside picks 31-64 only — the window the ruck sitters actually occupy:')
WR2 = {}
for g in GROUPS:
    sat = [r for r in ROWS if r['grp'] == g and r['g1'] == 0 and r['pick'] >= 31]
    ctl = [r for r in ROWS if r['grp'] == g and r['g1'] >= 1 and r['pick'] >= 31]
    ws_, wc = np.mean([r['w'] for r in sat]), np.mean([r['w'] for r in ctl])
    WR2[g] = dict(wash_sat=float(ws_), n_sat=len(sat), wash_ctl=float(wc), n_ctl=len(ctl),
                  gap=float(ws_ - wc))
    print('%-6s   %.3f (n=%3d)          %.3f (n=%3d)     gap %+.3f' % (g, ws_, len(sat), wc, len(ctl), ws_ - wc))
OUT['washout_rates_31_64'] = WR2

# name the thin cells outright, so nobody reads a ratio without seeing whose careers it is
print('\n== SECTION 2c. THE THIN CELLS, NAMED ==')
THIN = {}
for lab, sel in (('RUCK sitters, picks 1-30 (the cell that reverses)',
                  lambda r: r['grp'] == 'RUCK' and r['g1'] == 0 and r['pick'] <= 30),
                 ('RUCK controls, picks 31-64 (the denominator of F_RUCK there)',
                  lambda r: r['grp'] == 'RUCK' and r['g1'] >= 1 and r['pick'] >= 31),
                 ('RUCK controls, all picks (the whole primary ruck control group)',
                  lambda r: r['grp'] == 'RUCK' and r['g1'] >= 1),
                 ('RUCK controls at D\'s 11+ threshold (why D\'s primary spec cannot be used here)',
                  lambda r: r['grp'] == 'RUCK' and r['g1'] >= 11)):
    cell = sorted([r for r in ROWS if sel(r)], key=lambda r: r['pick'])
    THIN[lab] = [dict(key=r['key'], player=r['player'], pick=r['pick'], g1=r['g1'], washout=r['w'])
                 for r in cell]
    print('\n%s  — n=%d' % (lab, len(cell)))
    for r in cell:
        print('   %-24s pick %-3d yr1 games %-3d  washed out: %s'
              % (r['player'], r['pick'], r['g1'], 'yes' if r['w'] else 'no'))
OUT['thin_cells'] = THIN

# ------------------------------------------------------------------ 3. what an adjustment would look like
print('\n== SECTION 3. THE ADJUSTMENT ARITHMETIC (published whether or not it is recommended) ==')
P = RES['SAT1|ctl1|3-group']
nm = P['names']
g0 = P['coef'][nm.index('g0_SAT')]; g1c = P['coef'][nm.index('g1_SATxlnpick')]
hK = P['coef'][nm.index('h_KPP')]; hR = P['coef'][nm.index('h_RUCK')]
SATROWS = [r for r in ROWS if r['g1'] == 0]


def s_of(p, g):
    return g0 + g1c * math.log(max(1, min(64, p))) + (hK if g == 'KPP' else hR if g == 'RUCK' else 0.0)


def kap(p, g, sn):
    return float(np.clip(s_of(p, g) / sn, 0.5, 2.0))


def ident(sn):
    return float(np.mean([D2 ** kap(r['pick'], r['grp'], sn) for r in SATROWS])) - D2


lo, hi = 0.05, 40.0
for _ in range(300):
    mid = 0.5 * (lo + hi)
    if ident(mid) < 0:
        lo = mid
    else:
        hi = mid
SN2 = 0.5 * (lo + hi)
print('re-solved redistribution constant s_norm\' = %.6f (D\'s was 1.747207); residual %.2e' % (SN2, ident(SN2)))
KTAB = {}
print('\n%-6s %s' % ('pick', '  '.join('%-8s' % g for g in GROUPS) + '   D pooled kappa'))
DG0, DG1, DSN = 0.1286221202379088, 0.4535958546743124, 1.7472066252064105
for p in (1, 5, 10, 16, 20, 24, 30, 40, 50, 53, 64):
    dk = float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))
    KTAB[str(p)] = dict({g: kap(p, g, SN2) for g in GROUPS}, D_pooled=dk)
    print('%-6d %s   %.4f' % (p, '  '.join('%-8.4f' % kap(p, g, SN2) for g in GROUPS), dk))
MG = {g: float(np.mean([kap(p, g, SN2) / max(1e-9, kap(p, 'SMALL', SN2)) for p in range(1, 65)]))
      for g in GROUPS}
print('\nimplied multiplicative position factor on kappa, vs SMALL (mean over picks 1-64):')
for g in GROUPS:
    print('  m_%-6s = %.4f' % (g, MG[g]))
print('what that does to the depth-2 price multiplier at a few picks (D2^kappa):')
for p in (16, 24, 53):
    print('  pick %2d: SMALL %.4f   KPP %.4f   RUCK %.4f   (D pooled %.4f)'
          % (p, D2 ** kap(p, 'SMALL', SN2), D2 ** kap(p, 'KPP', SN2), D2 ** kap(p, 'RUCK', SN2),
             D2 ** float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))))
OUT['adjustment_arithmetic'] = dict(s_norm_prime=SN2, kappa_table=KTAB, m_g=MG,
                                    fitted_from='SAT1|ctl1|3-group',
                                    note='published as arithmetic; recommendation lives in PACKET_H.md')

# --- 3b. the SINGLE TALL factor: the reading whose interval actually excluded zero ---
print('\n-- 3b. the single TALL factor (the reading whose 90%% interval excluded zero) --')
T = RES['SAT1|ctl1|TALL-pooled']
tn = T['names']
tg0 = T['coef'][tn.index('g0_SAT')]; tg1 = T['coef'][tn.index('g1_SATxlnpick')]
hT = T['coef'][tn.index('h_TALL')]
print('h_TALL = %+.4f  90%% CI [%+.3f, %+.3f]' % (hT, T['ci']['h_TALL'][0], T['ci']['h_TALL'][1]))


def s_t(p, tall):
    return tg0 + tg1 * math.log(max(1, min(64, p))) + (hT if tall else 0.0)


def kap_t(p, tall, sn):
    return float(np.clip(s_t(p, tall) / sn, 0.5, 2.0))


def ident_t(sn):
    return float(np.mean([D2 ** kap_t(r['pick'], r['grp'] in ('KPP', 'RUCK'), sn)
                          for r in SATROWS])) - D2


lo, hi = 0.05, 40.0
for _ in range(300):
    mid = 0.5 * (lo + hi)
    if ident_t(mid) < 0:
        lo = mid
    else:
        hi = mid
SNT = 0.5 * (lo + hi)
print('re-solved s_norm\' (TALL form) = %.6f ; identity residual %.2e ; D\'s was 1.747207' % (SNT, ident_t(SNT)))
print('\n%-6s %-9s %-9s %-9s %-9s %-9s %s' % ('pick', 'kap SMALL', 'kap TALL', 'D pooled',
                                              'D2^SMALL', 'D2^TALL', 'D2^Dpooled  [clip?]'))
KT2 = {}
CLIPPED = []
for p in (1, 5, 10, 16, 20, 24, 30, 40, 50, 53, 64):
    ks, kt = kap_t(p, False, SNT), kap_t(p, True, SNT)
    dk = float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))
    cl = []
    if abs(ks - 0.5) < 1e-9 or abs(ks - 2.0) < 1e-9: cl.append('SMALL')
    if abs(kt - 0.5) < 1e-9 or abs(kt - 2.0) < 1e-9: cl.append('TALL')
    KT2[str(p)] = dict(SMALL=ks, TALL=kt, D_pooled=dk, clipped=cl)
    if cl: CLIPPED.append(p)
    print('%-6d %-9.4f %-9.4f %-9.4f %-9.4f %-9.4f %-9.4f  %s'
          % (p, ks, kt, dk, D2 ** ks, D2 ** kt, D2 ** dk, ('CLIP ' + '+'.join(cl)) if cl else ''))
mT = float(np.mean([kap_t(p, True, SNT) / max(1e-9, kap_t(p, False, SNT)) for p in range(1, 65)]))
pins = [p for p in range(1, 65) if abs(kap_t(p, True, SNT) - 0.5) < 1e-9]
print('\nimplied single multiplicative factor  m_TALL = %.4f  (mean over picks 1-64 of kap_TALL/kap_SMALL)' % mT)
print('picks where the TALL curve is PINNED ON D\'s 0.5 CLIP FLOOR (the clip, not the fit, is setting the price):')
print('   picks %d-%d  (%d of 64 picks)' % (min(pins), max(pins), len(pins)) if pins else '   none')
pins_s = [p for p in range(1, 65) if abs(kap_t(p, False, SNT) - 0.5) < 1e-9]
print('   same for SMALL: picks %d-%d (%d)' % (min(pins_s), max(pins_s), len(pins_s)) if pins_s else '   SMALL: none')
print('\nside effect the owner must see: re-solving the constant MOVES THE SMALL CURVE TOO.')
for p in (10, 30, 64):
    dk = float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))
    print('   pick %2d  SMALL kappa %.4f vs D pooled %.4f  ->  depth-2 multiplier %.4f vs %.4f'
          % (p, kap_t(p, False, SNT), dk, D2 ** kap_t(p, False, SNT), D2 ** dk))
OUT['adjustment_TALL_single_factor'] = dict(h_TALL=hT, ci=T['ci']['h_TALL'], s_norm_prime=SNT,
                                            kappa_table=KT2, m_TALL=mT,
                                            clip_pinned_picks_TALL=pins,
                                            clip_pinned_picks_SMALL=pins_s,
                                            fitted_from='SAT1|ctl1|TALL-pooled')

# ------------------------------------------------------------------ 4. named rows
print('\n== SECTION 4. NAMED ROWS ==')
NAMED = ['will-green', 'alex-dodson', 'toby-conway', 'ned-moyle', 'nick-madden', 'steely-green']
idx = {r['key']: r for r in A['recs']}
NR = {}
print('%-16s %-20s %-5s %-6s %-5s %-4s %-4s %s' % ('key', 'player', 'route', 'pos', 'year', 'pick', 'g1', 'g1+2'))
for k in NAMED:
    r = idx.get(k)
    if not r:
        print('%-16s NOT IN STORE' % k); continue
    NR[k] = dict(player=r['player'], route=r['type'], pos=r['pos'], year=r['year'], pick=r['pick'],
                 g1=int(r.get('games_yr1') or 0), g12=int(r['games_by']['2']),
                 in_nd_curve=bool(r.get('teaches_curve') and r['type'] == 'ND' and 1 <= (r['pick'] or 0) <= 64),
                 v0=float(r['v0']))
    print('%-16s %-20s %-5s %-6s %-5d %-4d %-4d %d' % (k, r['player'], r['type'], r['pos'], r['year'],
                                                       r['pick'], NR[k]['g1'], NR[k]['g12']))
# the contrast the owner asked for: mid/small sitters at the same picks
print('\nthe contrast rows — small/mid sitters at or beside the same picks, same classes:')
CONTRA = []
for r in A['recs']:
    if r['type'] != 'ND' or not r.get('pick') or not (1 <= r['pick'] <= 64):
        continue
    if r['year'] < 2021 or GRP.get(r['pos']) != 'SMALL':
        continue
    if int(r.get('games_yr1') or 0) != 0:
        continue
    if r['pick'] in range(12, 21) or r['pick'] in range(21, 29) or r['pick'] in range(48, 59):
        CONTRA.append(dict(key=r['key'], player=r['player'], pos=r['pos'], year=r['year'],
                           pick=r['pick'], g1=0, g12=int(r['games_by']['2']), v0=float(r['v0'])))
CONTRA.sort(key=lambda d: d['pick'])
for d in CONTRA:
    print('  %-22s %-5s %-4s pick %-3d g1=0 g1+2=%d' % (d['player'], d['pos'], d['year'], d['pick'], d['g12']))
print('\nwhat the TALL adjustment would do to the depth-2 fade multiplier on each named row:')
print('%-20s %-6s %-5s %-10s %-10s %-10s %s' % ('player', 'pos', 'pick', 'D pooled', 'H TALL',
                                                'change', 'note'))
NRP = {}
for k in NAMED:
    if k not in NR:
        continue
    r = NR[k]
    if not r['in_nd_curve']:
        print('%-20s %-6s %-5s %-10s %-10s %-10s %s'
              % (r['player'], r['pos'], r['pick'], '--', '--', '--',
                 'pool route (%s) - a pick-keyed curve does not reach him' % r['route']))
        NRP[k] = dict(applies=False, route=r['route'])
        continue
    p = r['pick']
    tall = GRP[r['pos']] in ('KPP', 'RUCK')
    dk = float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))
    a, b_ = D2 ** dk, D2 ** kap_t(p, tall, SNT)
    NRP[k] = dict(applies=True, pick=p, tall=tall, mult_D=a, mult_H=b_, pct=100 * (b_ / a - 1))
    print('%-20s %-6s %-5d %-10.4f %-10.4f %+9.1f%% %s'
          % (r['player'], r['pos'], p, a, b_, 100 * (b_ / a - 1),
             'sat yr1' if r['g1'] == 0 else 'played %d games yr1 - not a sitter' % r['g1']))
print('\nthe same picks, if the player were a small instead (the owner\'s comparison):')
for p in (16, 24, 53):
    dk = float(np.clip((DG0 + DG1 * math.log(p)) / DSN, 0.5, 2.0))
    print('  pick %2d  small sitter %.4f   tall sitter %.4f   (D pooled treats both as %.4f)'
          % (p, D2 ** kap_t(p, False, SNT), D2 ** kap_t(p, True, SNT), D2 ** dk))
OUT['named_rows'] = NR
OUT['named_row_pricing'] = NRP
OUT['contrast_rows'] = CONTRA

# ------------------------------------------------------------------ write
pth = os.path.join(HERE, 'H_RESULTS.json')
json.dump(OUT, open(pth, 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: H_RESULTS.json  md5 %s' % hashlib.md5(open(pth, 'rb').read()).hexdigest()[:8])
