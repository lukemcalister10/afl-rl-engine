#!/usr/bin/env python3
"""ORDER N — the packet's remaining tables, computed at the SAME setting the packet quotes
(LAMBDA = the gated anchoring solve, age gate 24), so no number in PACKET_N.md is carried across
from a different run. READ-ONLY.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402
PL_F = 1.0524
L = []


def P(s=''):
    print(s); L.append(str(s))


M = json.load(open(os.path.join(HERE, 'MECH_N.json')))
G0, BSAT, S0, S_P5 = M['G0'], M['BETA_sat'], M['s0'], M['s_p5']
LAM = M['variantB']['LAMBDA_anchor']
THR = BSAT / LAM
TMAX = 1.0 - THR * (S_P5 - S0)


def A_of(g):
    return 1.0 - math.exp(-float(g) / G0)


def T_of(s, tmin=0.0):
    return min(max(1.0 - THR * (float(s) - S0), tmin), TMAX)


def F_old(g):
    return max(0.0, LB.ETA_K * LB.m_d(g))


def F_var(g, s, age, tmin=0.0):
    if g <= 0:
        return 0.0
    if age is None or age >= 24 or s is None:
        return F_old(g)
    return 1.0 - math.exp(-LAM * A_of(g) * T_of(s, tmin))


P('=' * 118)
P('ORDER N — THE PACKET CHECK. Every table below is computed at LAMBDA = %.5f, THETA_R = %.5f,' % (LAM, THR))
P('age gate 24 — the exact setting PACKET_N.md quotes.')
P('=' * 118)
P()

MK = LB.load_matrix('OKRULED')
ME = LB.load_matrix('M0ETA0')
LED = LB.load_ledger()
CUR = {}
for k, a in MK.items():
    ca, cb = a.get('cur'), ME[k].get('cur')
    if ca is None or cb is None:
        continue
    g = float(a.get('games_total') or 0.0); md = LB.m_d(g)
    CUR[k] = dict(g=g, s=LB.perf_surplus(a, 2026), age=LB.age_at(a, 2026),
                  C=((float(cb) - float(ca)) / (0.50 * md)) if md > 1e-12 else 0.0,
                  v0eta=float(cb), vK=float(ca))


def bp(k, tmin=0.0):
    d = CUR.get(k)
    if d is None:
        return None
    if d['C'] <= 0:
        return round(d['vK'] / PL_F)
    return round((d['v0eta'] - d['C'] * F_var(d['g'], d['s'], d['age'], tmin)) / PL_F)


# ---- 1 · where the money moves, GATED --------------------------------------------------------------
P('-' * 118)
P('1 · WHERE THE MONEY MOVES, WHOLE BOARD, AT THE GATED SETTING  (PACKET §7.5)')
P('-' * 118)
mv = []
for r in LED['rows']:
    k = r['key']
    n = bp(k)
    if n is None:
        continue
    mv.append(dict(key=k, name=r['name'], age=int(r['age']), g=float(r['g'] or 0),
                   pick=r.get('pick'), orderk=float(r['orderk']), new=float(n), d=n - float(r['orderk'])))
tk = sum(x['orderk'] for x in mv); tn = sum(x['new'] for x in mv)
P('   board total  ORDER K %d  ->  ORDER N %d   (%+d points, %+.2f%%)' % (
    round(tk), round(tn), round(tn - tk), 100 * (tn - tk) / tk))
P('   rows that move: %d of %d  (up %d, down %d)' % (
    sum(1 for x in mv if abs(x['d']) >= 0.5), len(mv),
    sum(1 for x in mv if x['d'] >= 0.5), sum(1 for x in mv if x['d'] <= -0.5)))
P()
P('   %-12s %6s %13s %10s' % ('career games', 'rows', 'total points', 'per row'))
for lo, hi, lab in ((0, 0, '0'), (1, 4, '1-4'), (5, 9, '5-9'), (10, 15, '10-15'),
                    (16, 29, '16-29'), (30, 59, '30-59'), (60, 10 ** 9, '60+')):
    s = [x for x in mv if lo <= x['g'] <= hi]
    if not s:
        continue
    P('   %-12s %6d %+13.0f %+10.1f' % (lab, len(s), sum(x['d'] for x in s), np.mean([x['d'] for x in s])))
P()
P('   %-12s %6s %13s' % ('age in 2026', 'rows', 'total points'))
for lo, hi, lab in ((0, 20, '<= 20'), (21, 23, '21-23'), (24, 999, '24 and over')):
    s = [x for x in mv if lo <= x['age'] <= hi]
    P('   %-12s %6d %+13.0f' % (lab, len(s), sum(x['d'] for x in s)))
P()
mv.sort(key=lambda x: -x['d'])
P('   ten largest rises:')
for x in mv[:10]:
    P('     %+8.0f  %-26s age %2d  g %5.0f  pick %-5s  %d -> %d' % (
        x['d'], x['name'][:26], x['age'], x['g'], x['pick'], round(x['orderk']), round(x['new'])))
P('   ten largest falls:')
for x in mv[-10:]:
    P('     %+8.0f  %-26s age %2d  g %5.0f  pick %-5s  %d -> %d' % (
        x['d'], x['name'][:26], x['age'], x['g'], x['pick'], round(x['orderk']), round(x['new'])))
P()

# ---- 2 · charge by surplus tercile, gated ------------------------------------------------------------
P('-' * 118)
P('2 · CHARGE PAID BY PERFORMANCE-SURPLUS TERCILE, AT THE GATED SETTING  (PACKET §7.2)')
P('-' * 118)
S1 = json.load(open(os.path.join(HERE, 'STEP1_N.json')))
rows = sorted(S1['rows'], key=lambda r: r['ps'])
n = len(rows); cuts = [0, n // 3, 2 * n // 3, n]
for t, lab in enumerate(('below expectation', 'middle', 'above expectation')):
    pt = rows[cuts[t]:cuts[t + 1]]
    P('   %-20s n=%-4d mean surplus %+7.2f  mean games %5.1f | CURRENT %5.1f%%  ORDER N %5.1f%%' % (
        lab, len(pt), np.mean([r['ps'] for r in pt]), np.mean([r['g'] for r in pt]),
        100 * np.mean([F_old(r['g']) for r in pt]),
        100 * np.mean([F_var(r['g'], r['ps'], r['age']) for r in pt])))
P()

# ---- 3 · the named rows, gated -----------------------------------------------------------------------
P('-' * 118)
P('3 · THE NAMED ROWS AT THE GATED SETTING  (PACKET §9)')
P('-' * 118)
byk = {r['key']: r for r in LED['rows']}
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie', 'anthony-scerri', 'milan-murdock']
P('   %-22s %3s %5s %5s %9s | %7s %7s | %7s %7s %7s' % (
    'row', 'age', 'pick', 'g', 'surplus', 'chg K', 'chg N', 'landing', 'ORDER K', 'ORDER N'))
for k in NAMED:
    r = byk.get(k)
    if r is None:
        P('   %-22s  NOT ON THE 804-ROW BOARD' % k); continue
    a = MK[k]
    Y = max((s['year'] for s in a['seasons']), default=None)
    s = LB.perf_surplus(a, Y) if Y else None
    g = float(r['g'] or 0)
    P('   %-22s %3d %5s %5.0f %9s | %6.1f%% %6.1f%% | %7d %7d %7d' % (
        r['name'][:22], r['age'], r['pick'], g, ('%+.2f' % s) if s is not None else 'n/a',
        100 * F_old(g), 100 * F_var(g, s, int(r['age'])),
        round(r['landing']), round(r['orderk']), bp(k)))
P()

# ---- 4 · Step 2 terciles, for the packet's plain-read table ------------------------------------------
P('-' * 118)
P('4 · STEP 2 TERCILES, THE PLAIN READ  (PACKET §4.2)')
P('-' * 118)
S2 = json.load(open(os.path.join(HERE, 'STEP2_N.json')))
T = S2['terciles']
P('   %-8s %-6s %6s | %9s %9s | %11s %11s' % (
    'games', 'tercile', 'rows', 'mean PS', 'mean v0', 'DVREST mean', 'DV1 mean'))
for b in ('1-3', '4-7', '8-12', '13-17', '18-24', '25-39', '40-60'):
    if b not in T:
        continue
    for lab in ('low', 'mid', 'high'):
        d = T[b][lab]
        P('   %-8s %-6s %6d | %+9.2f %9.0f | %11.1f %11.1f' % (
            b, lab, d['n'], d['ps'], d['v0'], d['dvrest'], d['dv1']))
P()

# ---- 5 · the charge table at the gated setting -------------------------------------------------------
P('-' * 118)
P('5 · THE CHARGE TABLE AT THE GATED SETTING  (PACKET §5.4)')
P('-' * 118)
P('   zero point: surplus %+.2f points per game.  TMAX %.4f.' % (S0 + 1.0 / THR, TMAX))
rowsS2 = S2['rows']
P('   share of the young cohort at or past the zero point: %.1f%%' % (
    100 * float(np.mean([1.0 if r['ps'] >= S0 + 1.0 / THR else 0.0 for r in rowsS2]))))
P()
P('   %-8s | %-14s | %9s %9s %9s %9s' % ('games', 'CURRENT blind', 's=-25', 's=-10', 's=0', 's=+15'))
for g in (1, 2, 3, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50):
    P('   %-8d | %13.1f%% | %8.1f%% %8.1f%% %8.1f%% %8.1f%%' % (
        g, 100 * F_old(g), *[100 * F_var(g, s, 19) for s in (-25, -10, 0, 15)]))
P()

open(os.path.join(HERE, 'CHECK_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote CHECK_N_out.txt')
