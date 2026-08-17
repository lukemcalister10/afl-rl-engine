#!/usr/bin/env python3
# =====================================================================================================
# ORDER B BUILD -- CONDITIONAL FADE FIT, SECOND (RESCUE) ATTEMPT — DISCLOSED PREREG DEVIATION.
#
# WHAT HAPPENED, plainly: the prereg'd loss (survivor-view tier LEVEL cells, bb_fade_fit.py) FAILED
# identification — A CI [0.00,0.60] includes 0, G(star) CI [0.00,0.77] not below 0.5 — because the
# survivor level cells mix directions (mid 29 B=.77, role 30 B=.57 sit UNDER par while role 28-29 sit
# over), so a monotone fade cannot improve that loss anywhere and its surface is flat. The DIAGNOSIS
# (bb_fade_diag.py) shows the output-conditional signal lives in the RATE instrument the level cells
# cannot see: tier-resolved survivor-linked steps — star engine-vs-realized gaps +0.006..+0.067 never
# called at any age; mid called (+0.32 at 27->28; pooled 29-30 +0.33 called); role called at 28->29,
# 29->30, 30->31 (gaps +0.40/+0.56/+1.90). This is the derivation's own instrument (b2_fit FIT-2 fit
# the flat knots on exactly these steps, un-tiered); the deviation swaps the LOSS to that instrument,
# tier-resolved. EVERYTHING ELSE IS THE PREREG: same family r(a,s)=0.14+A*phi(a)*G(s), same surplus,
# same grids, same seed/bootstrap, same full-view level floors (28-31, min(floor, B_at_zero) rule),
# same identification rule (A CI excludes 0 AND G(star) CI < 0.5), same star gate, same fallback.
# Both fits ship in the packet side by side.
# =====================================================================================================
import json, math, os, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'bb_fade_fit.py')).read().split('# control: reproduce')[0])

SEED2 = 37
RNG = np.random.default_rng(SEED2)


def frac_engine(a, pa):
    return DELTAS[max(-8, min(14, int(round(a - pa))))]


def frac_tall(a, pa_star=PA_T, ladder=LAD):
    j = int(round(a - pa_star))
    if j <= 0:
        return DELTAS[max(-8, j)]
    if j <= len(ladder):
        return ladder[j - 1]
    lr = ladder[-1] / ladder[-2]
    f = ladder[-1]
    for _ in range(j - len(ladder)):
        f *= lr
    return f


def replica_mark(bar, a, L, r, tall):
    fracfn = frac_tall if tall else frac_engine
    pa = PA_T if tall else PEAK_AGE[bar]
    f_a = fracfn(a, pa)
    if f_a < 1e-6:
        return 0.0
    lp = L / f_a
    cl = L
    prod = 0.0
    for k in range(18):
        ag = a + k
        fv = fracfn(ag, pa)
        if ag > 38 or fv < 0.42:
            break
        lev = lp * fv
        if ag <= pa or k == 0:
            lev = max(lev, cl)
        base = lev + capt_prem(lev)
        prod += posval(base - REPL[bar]) * 21 / (1.0 + r) ** k
    if bar in ('KPF', 'KPD'):
        prod *= 1.05
    runway = min(max((25 - a) / 6.0, 0), 1)
    elite = min(max((lp / PEAK[bar] - 0.97) / 0.30, 0), 1)
    return prod * (1 + runway * elite * PMAX)


def phi(a):
    return min(max((a - 27.0) / 4.0, 0.0), 1.0)


# tiers + surplus (as fit1)
for a in AGES:
    cell = [r for r in rows if r['age'] == a]
    t2 = np.array([r['t2'] for r in cell])
    q1, q2 = np.percentile(t2, [100 / 3, 200 / 3])
    for r in cell:
        r['tier'] = 'role' if r['t2'] <= q1 else ('mid' if r['t2'] <= q2 else 'star')
for x in rows:
    x['s'] = max(0.0, x['L'] - REPL[x['bar']]) if (x['L'] is not None and x['bar'] in REPL) else None

# pairs with replica-able rows
by_player_rows = collections.defaultdict(dict)
for x in rows:
    by_player_rows[x['key']][x['age']] = x
pairs_all, pairs = [], []
for k, d in by_player_rows.items():
    for a in (27, 28, 29, 30):
        if a in d and (a + 1) in d and d[a + 1]['Y'] == d[a]['Y'] + 1:
            pairs_all.append((d[a], d[a + 1]))
            if d[a]['s'] is not None and d[a + 1]['s'] is not None:
                pairs.append((d[a], d[a + 1]))
print('pairs total %d, replica-able %d (dropped rows lack a trailing-2 level; disclosed)'
      % (len(pairs_all), len(pairs)))

A_GRID = [round(x, 2) for x in np.arange(0.0, 0.601, 0.02)]
S0_GRID = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 13.0, 16.0, 20.0, 25.0, 32.0, 40.0, 50.0, 64.0]
GRID = [(Av, s0) for Av in A_GRID for s0 in S0_GRID]
NG = len(GRID)

CELLS = [(tr, a) for tr in ('star', 'mid', 'role') for a in (27, 28, 29, 30)]
CELL_PAIRS = {c: [i for i, (x0, x1) in enumerate(pairs) if x0['age'] == c[1] and x0.get('tier') == c[0]]
              for c in CELLS}
CELLS = [c for c in CELLS if len(CELL_PAIRS[c]) >= 20]
print('cells in the loss (n>=20): %s' % ['%s|%d(n=%d)' % (c[0], c[1], len(CELL_PAIRS[c])) for c in CELLS])

# realized targets + bootstrap sd per cell (cluster = pair rows; one pair per player per step)
TGT, SD = {}, {}
for c in CELLS:
    ix = CELL_PAIRS[c]
    R0 = np.array([pairs[i][0]['R'] for i in ix]); R1 = np.array([pairs[i][1]['R'] for i in ix])
    TGT[c] = float(R1.mean() / R0.mean())
    bs = []
    for _ in range(2000):
        jx = RNG.integers(0, len(ix), size=len(ix))
        m0 = R0[jx].mean()
        if m0 > 0:
            bs.append(R1[jx].mean() / m0)
    SD[c] = float(np.std(bs))
    print('  target %s|%d->%d: realized %.4f sd %.4f' % (c[0], c[1], c[1] + 1, TGT[c], SD[c]))

# per-pair-row replica marks: flat base (ladder, 0.14) and per grid candidate
PAIR_ROWS = sorted({id(x) for p in pairs for x in p})
ROW_BY_ID = {id(x): x for p in pairs for x in p}
REP_FLAT = {rid: replica_mark(ROW_BY_ID[rid]['bar'], ROW_BY_ID[rid]['age'], ROW_BY_ID[rid]['L'], 0.14,
                              ROW_BY_ID[rid]['pos'] == 'TALL') for rid in PAIR_ROWS}
REP_G = {}   # rid -> vector over grid
for rid in PAIR_ROWS:
    x = ROW_BY_ID[rid]
    v = np.empty(NG)
    for gi, (Av, s0) in enumerate(GRID):
        r_eff = 0.14 + Av * phi(x['age']) * math.exp(-x['s'] / s0)
        v[gi] = REP_FLAT[rid] if r_eff == 0.14 else replica_mark(x['bar'], x['age'], x['L'], r_eff,
                                                                x['pos'] == 'TALL')
    REP_G[rid] = v

# engine step per cell (fixed) and per-cell replica mean-vectors over the grid
CELL_ARR = {}
for c in CELLS:
    ix = CELL_PAIRS[c]
    E0 = np.array([pairs[i][0]['mark'] for i in ix]); E1 = np.array([pairs[i][1]['mark'] for i in ix])
    M0 = np.stack([REP_G[id(pairs[i][0])] for i in ix])   # n x NG
    M1 = np.stack([REP_G[id(pairs[i][1])] for i in ix])
    F0 = np.array([REP_FLAT[id(pairs[i][0])] for i in ix]); F1 = np.array([REP_FLAT[id(pairs[i][1])] for i in ix])
    CELL_ARR[c] = dict(E0=E0, E1=E1, M0=M0, M1=M1, F0=F0, F1=F1,
                       pl=np.array([pairs[i][0]['key'] for i in ix]))


def loss_vec(weights=None):
    ls = np.zeros(NG)
    for c in CELLS:
        S = CELL_ARR[c]
        w = weights.get(c) if weights else np.ones(len(S['E0']))
        sw = w.sum()
        if sw < 20:
            continue
        eng = (w * S['E1']).sum() / (w * S['E0']).sum()
        flat = ((w @ S['M1'] * 0 + (w * S['F1']).sum()) / sw) / ((w * S['F0']).sum() / sw)
        m1 = (w @ S['M1']) / sw
        m0 = (w @ S['M0']) / sw
        ns = eng * (m1 / m0) / flat
        r0 = (w * S['R0v']).sum() / sw if 'R0v' in S else None
        tgt = TGT[c] if weights is None else weights['tgt'][c]
        ls += ((ns - tgt) / SD[c]) ** 2
    return ls


# level floors: reuse fit1's MARKS machinery for feasibility (full view, ages 28-31, min(floor, B0) rule)
print('building level-floor MARKS grid (fit1 machinery)...')
MK = np.array([x['mark'] for x in rows])
RR = np.array([x['R'] for x in rows])
AGE_A = np.array([x['age'] for x in rows])
TIER = np.array([x.get('tier') or '' for x in rows])
POS = np.array([x['pos'] or '' for x in rows])
IS_ANC = np.isin(AGE_A, list(ANCHOR_AGES))
REP_BASE_ALL = {}
for x in rows:
    if x['s'] is not None and x['bar'] in BARS:
        REP_BASE_ALL[id(x)] = replica_mark(x['bar'], x['age'], x['L'], 0.14, x['pos'] == 'TALL')
MARKS = np.tile(MK, (NG, 1))
for j, x in enumerate(rows):
    rb = REP_BASE_ALL.get(id(x), 0.0)
    if rb <= 0:
        continue
    for gi, (Av, s0) in enumerate(GRID):
        r_eff = 0.14 + Av * phi(x['age']) * math.exp(-x['s'] / s0)
        if r_eff != 0.14:
            MARKS[gi, j] = x['mark'] * replica_mark(x['bar'], x['age'], x['L'], r_eff,
                                                    x['pos'] == 'TALL') / rb
FLOOR_AGES = (28, 29, 30, 31)
GI0 = GRID.index((0.0, S0_GRID[0]))
feas = np.ones(NG, bool)
FLOOR_REPORT = []
for gname, msel in ([('tier:star', TIER == 'star'), ('tier:mid', TIER == 'mid'), ('tier:role', TIER == 'role'),
                     ('ALL', np.ones(len(rows), bool)), ('TALL', POS == 'TALL'),
                     ('SMALL', POS == 'SMALL'), ('RUCK', POS == 'RUCK')]):
    ancf = msel & IS_ANC
    if ancf.sum() < 20:
        continue
    Rancf = RR[ancf].mean()
    ancf_vec = MARKS[:, ancf].mean(axis=1) / Rancf
    for a in FLOOR_AGES:
        cmf = msel & (AGE_A == a)
        if cmf.sum() < 20:
            continue
        Rcf = RR[cmf].mean()
        if Rcf <= 0:
            continue
        Bf = (MARKS[:, cmf].mean(axis=1) / Rcf) / ancf_vec
        fl = FLOOR_FULL.get((gname, a))
        if fl:
            fl_eff = min(fl, float(Bf[GI0]))
            feas &= (Bf >= fl_eff - 1e-9)
            FLOOR_REPORT.append((gname, a, fl, round(float(Bf[GI0]), 4)))

L0 = loss_vec()
order = np.argsort(L0)
gi_u = order[0]
gi_c = next(gi for gi in order if feas[gi])
A_FIT, S0_FIT = GRID[gi_c]
print('\nFIT2 (rate instrument): CONSTRAINED A=%.2f s0=%.1f loss=%.2f  (unconstrained A=%.2f s0=%.1f loss=%.2f, feasible=%s; %d/%d grid feasible)'
      % (A_FIT, S0_FIT, L0[gi_c], GRID[gi_u][0], GRID[gi_u][1], L0[gi_u], bool(feas[gi_u]), int(feas.sum()), NG))

star_s = [x['s'] for x in rows if x.get('tier') == 'star' and 28 <= x['age'] <= 31 and x['s'] is not None]
S_STAR_MEAN = float(np.mean(star_s))
G_STAR = math.exp(-S_STAR_MEAN / S0_FIT)
print('  mean star surplus (28-31) %.2f -> G(star)=%.3f at fit;  r(31, star)=%.3f  r(31, s=0)=%.3f'
      % (S_STAR_MEAN, G_STAR, 0.14 + A_FIT * G_STAR, 0.14 + A_FIT))

# per-cell closure at the fit
CLOSE = {}
for c in CELLS:
    S = CELL_ARR[c]
    eng = S['E1'].mean() / S['E0'].mean()
    flat = S['F1'].mean() / S['F0'].mean()
    ns = eng * (S['M1'][:, gi_c].mean() / S['M0'][:, gi_c].mean()) / flat
    CLOSE[c] = dict(n=len(S['E0']), engine=round(float(eng), 4), new=round(float(ns), 4),
                    realized=round(TGT[c], 4), sd=round(SD[c], 4))
    print('  %s|%d->%d: engine %.4f -> new %.4f (realized %.4f)' % (c[0], c[1], c[1] + 1, eng, ns, TGT[c]))

# bootstrap (cluster by player over pairs; floors held at point estimate, as the derivation's b2 did)
pair_players = sorted({x0['key'] for x0, _ in pairs})
pp_ix = {k: i for i, k in enumerate(pair_players)}
for c in CELLS:
    S = CELL_ARR[c]
    S['pli'] = np.array([pp_ix[k] for k in S['pl']])
    S['R0'] = np.array([pairs[i][0]['R'] for i in CELL_PAIRS[c]])
    S['R1'] = np.array([pairs[i][1]['R'] for i in CELL_PAIRS[c]])
boot_A, boot_s0, boot_G = [], [], []
for b in range(B_BOOT):
    cnt = np.bincount(RNG.integers(0, len(pair_players), size=len(pair_players)), minlength=len(pair_players))
    ls = np.zeros(NG)
    ok = True
    for c in CELLS:
        S = CELL_ARR[c]
        w = cnt[S['pli']].astype(float)
        sw = w.sum()
        if sw < 20:
            ok = False
            break
        r0 = (w * S['R0']).sum() / sw
        if r0 <= 0:
            ok = False
            break
        tgt = (w * S['R1']).sum() / sw / r0
        eng = (w * S['E1']).sum() / (w * S['E0']).sum()
        flat = ((w * S['F1']).sum() / sw) / ((w * S['F0']).sum() / sw)
        ns = eng * (((w @ S['M1']) / sw) / ((w @ S['M0']) / sw)) / flat
        ls += ((ns - tgt) / SD[c]) ** 2
    if not ok:
        continue
    orderb = np.argsort(ls)
    gib = next((gi for gi in orderb if feas[gi]), None)
    if gib is None:
        continue
    Ab, s0b = GRID[gib]
    boot_A.append(Ab); boot_s0.append(s0b)
    boot_G.append(math.exp(-S_STAR_MEAN / s0b) if Ab > 0 else 0.0)
A_CI = [float(np.percentile(boot_A, 5)), float(np.percentile(boot_A, 95))]
S0_CI = [float(np.percentile(boot_s0, 5)), float(np.percentile(boot_s0, 95))]
G_CI = [float(np.percentile(boot_G, 5)), float(np.percentile(boot_G, 95))]
print('  boot (%d draws): A CI [%.2f,%.2f]  s0 CI [%.1f,%.1f]  G(star) CI [%.3f,%.3f]'
      % (len(boot_A), A_CI[0], A_CI[1], S0_CI[0], S0_CI[1], G_CI[0], G_CI[1]))
IDENT_A = A_CI[0] > 0.0
IDENT_G = G_CI[1] < 0.5
IDENTIFIED = IDENT_A and IDENT_G
print('  IDENTIFICATION: A-CI excludes 0: %s;  G(star) CI < 0.5: %s  ==> %s'
      % (IDENT_A, IDENT_G, 'FITTED — wire the conditional fade' if IDENTIFIED else 'FAILED -> FALLBACK (flat hazard knots)'))

# star gate on the LEVEL instrument at the fitted point (survivor view, as prereg)
def anchored_B_masked(mask_rows, marks=None):
    mk = (lambda x: marks[id(x)]) if marks else (lambda x: x['mark'])
    anc = [x for x in mask_rows if x['age'] in ANCHOR_AGES]
    if len(anc) < 20:
        return None, {}
    anc_ratio = np.mean([mk(x) for x in anc]) / np.mean([x['R'] for x in anc])
    prof = {}
    for a in TEST_AGES:
        cell = [x for x in mask_rows if x['age'] == a]
        if len(cell) < 20:
            continue
        Rm = np.mean([x['R'] for x in cell])
        if Rm <= 0:
            continue
        prof[a] = (np.mean([mk(x) for x in cell]) / Rm) / anc_ratio
    return float(anc_ratio), prof


marks_fit = {id(x): MARKS[gi_c, j] for j, x in enumerate(rows)}
STAR_GATE, star_ok = {}, True
TIER_B_FIT = {}
for tr in ('star', 'mid', 'role'):
    _, pf = anchored_B_masked([x for x in rows if x.get('tier') == tr and x['surv']], marks_fit)
    TIER_B_FIT[tr] = {a: round(v, 4) for a, v in pf.items()}
for a in TEST_AGES:
    b_new = TIER_B_FIT['star'].get(a)
    ok = (b_new is not None and STAR_CI[a][0] <= b_new <= STAR_CI[a][1] and abs(b_new - STAR_PT[a]) <= 0.05)
    STAR_GATE[a] = dict(B_new=b_new, B_meas=STAR_PT[a], ci=STAR_CI[a], passes=bool(ok))
    star_ok &= ok
print('  STAR GATE (level instrument): %s  ' % ('PASS' if star_ok else 'FAIL') +
      ' '.join('%d:%.3f(meas %.3f)' % (a, STAR_GATE[a]['B_new'], STAR_PT[a]) for a in TEST_AGES))
for tr in ('star', 'mid', 'role'):
    print('  %s|surv B with fade: ' % tr + ' '.join('%d:%.2f' % (a, TIER_B_FIT[tr][a]) for a in sorted(TIER_B_FIT[tr])))

RATE_TABLE = {}
for a in (27, 28, 29, 30, 31, 32):
    RATE_TABLE[a] = {s: round(0.14 + A_FIT * phi(a) * math.exp(-s / S0_FIT), 4)
                     for s in (0, 2, 5, 10, 15, 20, 30)}
print('  effective rate r(a,s):')
for a in RATE_TABLE:
    print('   age %d: ' % a + '  '.join('s=%d:%.3f' % (s, v) for s, v in RATE_TABLE[a].items()))

OUT = dict(meta=dict(deviation='DISCLOSED: loss moved from tier LEVEL cells (prereg; failed identification, '
                               'bb_fade_fit.py) to the tier-resolved RATE instrument (bb_fade_diag.py shows '
                               'the signal lives there); family/surplus/grids/floors/ident-rule/star-gate unchanged',
                     input=dict(path=CAND_P, md5=m5), seed=SEED2, B_boot=B_BOOT,
                     pairs=len(pairs), cells={'%s|%d' % c: len(CELL_PAIRS[c]) for c in CELLS}),
           targets={'%s|%d' % c: dict(realized=round(TGT[c], 4), sd=round(SD[c], 4)) for c in CELLS},
           fit=dict(A=A_FIT, s0=S0_FIT, A_ci=A_CI, s0_ci=S0_CI,
                    star_mean_surplus=round(S_STAR_MEAN, 2), G_at_star=round(G_STAR, 4), G_star_ci=G_CI,
                    identified=bool(IDENTIFIED), ident_A=bool(IDENT_A), ident_G=bool(IDENT_G),
                    unconstrained=dict(A=GRID[gi_u][0], s0=GRID[gi_u][1], feasible=bool(feas[gi_u])),
                    n_feasible_grid=int(feas.sum())),
           closure={'%s|%d' % c: v for c, v in CLOSE.items()},
           tier_B_fit_surv=TIER_B_FIT,
           star_gate={str(a): v for a, v in STAR_GATE.items()}, star_gate_pass=bool(star_ok),
           rate_table={str(a): v for a, v in RATE_TABLE.items()},
           floors_used=[dict(group=g, age=a, floor=round(f, 4), B_at_zero=b) for g, a, f, b in FLOOR_REPORT])
with open(os.path.join(HERE, 'RESULTS_B_FADE_FIT2.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_FADE_FIT2.json')
