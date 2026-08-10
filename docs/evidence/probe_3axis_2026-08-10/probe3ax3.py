"""PROBE 3AX, pass 3 (READ-ONLY).  Two extra specifications the owner's question invites, plus the
compact comparison table.

  G  HARD sa TERCILES crossed with class and the log-pick Gaussian -- the literal reading of the
     cross-section's own cut (it terciled sa; it did not smooth it).
  H  The same three-axis kernel under a STRICTER thinness rule: the cell must average at least 35
     ACTUAL ROWS (sum of kernel weights >= 35), not merely score eff-n >= 35.  This is the test of
     whether the shipped eff-n rule certifies what a reader would think it certifies in three axes.
"""
import json
import numpy as np

S = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
exec(open(S + '/probe3ax2.py').read().split("B2, POOLED2 = kern2()")[0])

B2, POOLED2 = kern2()
SAK3 = [(SAT1 - SA_MU) / SA_SD, (SAMED - SA_MU) / SA_SD, (SAT2 - SA_MU) / SA_SD]
HS3 = float(np.mean(np.diff(SAK3))) * 1.1
_d = []
B3 = kern3(SAK3, HS3, _d)

GATES = [('picks 1-10 x TOP-TERCILE sa', lambda x: x['pk'] <= 10 and x['sa'] >= SAT2, 0.015),
         ('picks 1-20 x ABOVE-MEDIAN sa', lambda x: x['pk'] <= 20 and x['sa'] >= SAMED, 0.025),
         ('picks 41-64 (declared taper)', lambda x: 41 <= x['pk'] <= 64, 0.005),
         ('draft age 19+ (declared taper)', lambda x: x['age'] is not None and x['age'] >= 19, 0.005)]
BASE_LANDING = 0.990805
LIFT1 = 1.071991 - BASE_LANDING
MEAS_Y1 = sum(x['F'] for x in Y1) / sum(x['price'] for x in Y1) - 1.0


# ---------------- G: hard sa terciles ------------------------------------------------------------
T1U = (SAT1 - SA_MU) / SA_SD
T2U = (SAT2 - SA_MU) / SA_SD


def tercile_of(x):
    u = x['u'] if 'sa' not in x else (x['sa'] - SA_MU) / SA_SD
    return 0 if u < T1U else (1 if u < T2U else 2)


def kernG(diag):
    B = {c: [[0.0] * 3 for _ in LPK] for c in CLASSES}
    for c in CLASSES:
        for j, lpk in enumerate(LPK):
            for t in range(3):
                got = None
                for stage, src in ((1, [x for x in NONKPD if x['cls'] == c and tercile_of(x) == t]),
                                   (2, [x for x in NONKPD if tercile_of(x) == t])):
                    if not src: continue
                    h = 0.18
                    while True:
                        K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in src]
                        en = eff_n(src, K)
                        if en >= EFFN or h > 3.0: break
                        h *= 1.15
                    if en >= EFFN:
                        got = (stage, src, K, h, en); break
                if got is None:
                    src = NONKPD; h = 0.18
                    while True:
                        K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / h) ** 2)) for x in src]
                        en = eff_n(src, K)
                        if en >= EFFN or h > 3.0: break
                        h *= 1.15
                    got = (3, src, K, h, en)
                stage, src, K, h, en = got
                B[c][j][t] = loc_delta(src, K) / D1
                sk, nh = kernel_mass(K)
                diag.append(dict(cls=c, pk=PK_KNOTS[j], t=t, stage=stage, h=round(h, 3),
                                 effn=round(en, 1), sumK=round(sk, 1), nhalf=nh, n_src=len(src)))
    return B


def mk_bG(B):
    def f(x):
        col = [B[x['cls']][j][tercile_of(x)] for j in range(len(LPK))]
        return float(np.interp(x['lp'], LPK, col))
    return f


# ---------------- H: strict row-count rule -------------------------------------------------------
def kernH(sak, hs0, diag, need=35.0):
    B = {c: [[0.0] * len(sak) for _ in LPK] for c in CLASSES}
    for c in CLASSES:
        rc = [x for x in NONKPD if x['cls'] == c]
        for j, lpk in enumerate(LPK):
            for m, sk_ in enumerate(sak):
                got = None
                for stage, src in ((1, rc), (2, NONKPD)):
                    if not src: continue
                    hp, hs = 0.18, hs0
                    while True:
                        K = [float(np.exp(-0.5 * (((x['lp'] - lpk) / hp) ** 2 + ((x['u'] - sk_) / hs) ** 2)))
                             for x in src]
                        en = eff_n(src, K); mass = float(np.sum(K))
                        if (en >= EFFN and mass >= need) or hp > 3.0: break
                        hp *= 1.15; hs *= 1.15
                    if en >= EFFN and mass >= need:
                        got = (stage, src, K, hp, hs, en, mass); break
                if got is None:
                    hp = 0.18
                    while True:
                        K = [float(np.exp(-0.5 * ((x['lp'] - lpk) / hp) ** 2)) for x in NONKPD]
                        en = eff_n(NONKPD, K); mass = float(np.sum(K))
                        if (en >= EFFN and mass >= need) or hp > 3.0: break
                        hp *= 1.15
                    got = (3, NONKPD, K, hp, float('inf'), en, mass)
                stage, src, K, hp, hs, en, mass = got
                B[c][j][m] = loc_delta(src, K) / D1
                diag.append(dict(cls=c, pk=PK_KNOTS[j], u=round(sk_, 3), stage=stage, hp=round(hp, 3),
                                 hs=(None if hs == float('inf') else round(hs, 3)),
                                 effn=round(en, 1), sumK=round(mass, 1)))
    return B


DG = []; BG = kernG(DG)
DH = []; BH = kernH(SAK3, HS3, DH)

SPECS = [('CONTROL 2-axis (shipped)', lambda x: b2_of(B2, x), ('z',)),
         ('3-axis A  pick x cls x sa(gauss 3k), no z', mk_b3(B3, SAK3), ()),
         ('3-axis B  pick x cls x sa(gauss 3k), z kept', mk_b3(B3, SAK3), ('z',)),
         ('3-axis G  pick x cls x sa(HARD terciles), no z', mk_bG(BG), ()),
         ('3-axis G+ pick x cls x sa(HARD terciles), z kept', mk_bG(BG), ('z',)),
         ('3-axis H  strict sumK>=35 rule, no z', mk_b3(BH, SAK3), ()),
         ('3-axis H+ strict sumK>=35 rule, z kept', mk_b3(BH, SAK3), ('z',)),
         ('CONTROL F 2-axis kernel + z AND sa gates', lambda x: b2_of(B2, x), ('z', 'sa'))]

print('=' * 122)
print('COMPACT COMPARISON.  Every surface conserves the SAME aggregate by construction, so the taught')
print("year-1 lift at equal intensity is IDENTICAL (%+0.6f at W=1); only the DISTRIBUTION differs and" % 0.133257)
print('therefore only the MAX FEASIBLE INTENSITY differs.  Measured year-1 residual = %+0.6f.' % MEAS_Y1)
print('=' * 122)
print('%-50s %9s %9s %9s %9s %8s %10s %9s' %
      ('surface', '1-10xT3', '1-20xA2', '41-64', 'kappa', 'W_max', 'yr1 land', '%resid'))
print('%-50s %9.3f %9.3f %9.3f' % ('BOUND', 0.015, 0.025, 0.005))
print('-' * 122)
RES = {}
for nm, bf, gts in SPECS:
    d, dg = build(bf, gts)
    g = {}
    for cn, f, bound in GATES:
        sub = [x for x in Y1 if f(x)]
        sp = sum(x['price'] for x in sub)
        v1 = sum(x['price'] * d(x, 1.0) for x in sub) / sp
        g[cn] = (v1, bound / abs(v1) if abs(v1) > 1e-12 else 9.9)
    wmax = min(v[1] for v in g.values())
    wby = min(g.items(), key=lambda kv: kv[1][1])[0]
    wsa = min(g[c][1] for c in list(g)[:2])
    wsaby = min(list(g)[:2], key=lambda c: g[c][1])
    land = BASE_LANDING + LIFT1 * wmax
    RES[nm] = dict(g=g, wmax=wmax, wby=wby, wsa=wsa, wsaby=wsaby, land=land, Z=dg['Z'], kappa=dg['kappa'])
    print('%-50s %+9.5f %+9.5f %+9.5f %9.4f %8.4f %10.6f %9.1f' %
          (nm, g['picks 1-10 x TOP-TERCILE sa'][0], g['picks 1-20 x ABOVE-MEDIAN sa'][0],
           g['picks 41-64 (declared taper)'][0], dg['kappa'], wmax, land,
           100 * wmax * 0.133257 / MEAS_Y1))
    print('%-50s   bound by %-34s | sa-cells only: W %.4f -> land %.6f (%s)' %
          ('', wby, wsa, BASE_LANDING + LIFT1 * wsa, wsaby))

print('\n' + '=' * 122)
print('SPEC G thinness (hard terciles): the cell counts the eff-n rule accepted')
print('=' * 122)
print('  %-8s %6s %4s %6s %7s %8s %8s %8s %7s' % ('class', 'pick', 'terc', 'stage', 'h', 'eff-n', 'sumK', 'nhalf', 'n_src'))
for e in DG:
    if e['cls'] == 'RUCK': continue
    print('  %-8s %6.0f %4d %6d %7.3f %8.1f %8.1f %8d %7d' %
          (e['cls'], e['pk'], e['t'], e['stage'], e['h'], e['effn'], e['sumK'], e['nhalf'], e['n_src']))

print('\n' + '=' * 122)
print('SPEC H: what the eff-n>=35 rule was hiding.  Bandwidths required to average >=35 ACTUAL rows.')
print('=' * 122)
print('  %-8s %6s %8s %6s %8s %8s %8s %8s' % ('class', 'pick', 'sa-knot', 'stage', 'hp', 'hs', 'eff-n', 'sumK'))
for e in DH:
    if e['cls'] == 'RUCK': continue
    print('  %-8s %6.0f %8.3f %6d %8.3f %8s %8.1f %8.1f' %
          (e['cls'], e['pk'], e['u'], e['stage'], e['hp'],
           ('%.3f' % e['hs']) if e['hs'] is not None else 'inf', e['effn'], e['sumK']))
h3 = [e['hs'] for e in DH if e['hs'] is not None]
print('  sa bandwidth needed for a 35-row cell: median %.3f (standardised sa units); the whole'
      ' inter-tercile distance on this axis is %.3f, so the cell is smoothed over %.2fx the entire'
      ' contrast the third axis was added to resolve.'
      % (float(np.median(h3)), SAK3[2] - SAK3[0], float(np.median(h3)) / (SAK3[2] - SAK3[0])))
