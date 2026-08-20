#!/usr/bin/env python3
"""ORDER M — THE OWNER'S LAWS, SCORED ON THE BUILT BOARDS, IN BOARD POINTS, ROW BY NAMED ROW.

ORDER K's ok_gates.py, reused. Pure JSON reads over the boards build_allM.sh already wrote — no engine
run here, so nothing can drift between what is scored and what was built.

The boards:
  cand  1f176444  the landing candidate — the base every gate is scored against (dial off)
  K     f3101883  ORDER K's ruled setting — rebuilt in this seat, and the comparison column
  s1              the age bar alone at dose 0.40, tall factor removed — S1's mature law reads here
  M0              ORDER K's knobs WITH ETA SET TO ZERO — the owner's ruling applied to his own setting
  M0R             the determinism repeat of M0
  MLO             the coolest point in the whole eta=0 grid (dose 0.00, kappa 0.15, gamma_u 16)
  MMIN            the smallest legal eta anywhere (dose 0.00, eta 0.31)
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OM = SP + '/om'
TAGS = ['cand', 'K', 's1', 'M0', 'M0R', 'MLO', 'MMIN']
BP = {t: OM + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
RAW = {t: json.load(open(BP[t])) for t in TAGS}
B = {t: {r['key']: r for r in RAW[t]['active']} for t in TAGS}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in TAGS}
KEYS = sorted(V['cand'])
AGE = {k: B['cand'][k]['age'] for k in KEYS}
POS = {k: (B['cand'][k].get('gf') or B['cand'][k]['grp']) for k in KEYS}
C31 = json.load(open(SP + '/cand31.json'))
R31 = {r['key']: r for r in C31['rows']}
TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))
L = []


def P(s=''):
    print(s); L.append(str(s))


NICE = {'cand': 'the landing candidate 1f176444 (dial off)',
        'K': "ORDER K f3101883 — dose .40 k .20 gu 8 eta .50 gd 14 rel 1.08",
        's1': 'the age bar ALONE at dose 0.40 (tall factor removed)',
        'M0': "ORDER M0 — ORDER K's knobs with ETA := 0",
        'M0R': 'the determinism repeat of M0',
        'MLO': 'the COOLEST eta=0 point in the grid (dose 0.00 k 0.15 gu 16)',
        'MMIN': 'the SMALLEST LEGAL ETA anywhere (dose 0.00 k .20 gu 8 eta 0.31)'}

P('=' * 116)
P('ORDER M — THE BOARD GATES. Board points, the currency the owner reads.')
P('=' * 116)
for t in TAGS:
    P('  %-5s %s  %s' % (t, MD5[t][:8], NICE[t]))
P('  active priced rows: %d' % len(KEYS))

P('\n== THE BUILD-FAILING IDENTITIES ==')
m1 = MD5['cand'].startswith('1f176444')
m2 = MD5['K'].startswith('f3101883')
m3 = (MD5['M0'] == MD5['M0R'])
P('  M1  dial-off reproduces the landing candidate 1f176444 : %s  (%s)'
  % ('PASS' if m1 else 'FAIL — M1 FIRES', MD5['cand']))
P('  M2  ORDER K\'s own setting rebuilds to f3101883         : %s  (%s)'
  % ('PASS' if m2 else 'FAIL — M2 FIRES', MD5['K']))
P('  M3  determinism x2 on the M0 board                     : %s  (%s vs %s)'
  % ('PASS' if m3 else 'FAIL — M3 FIRES', MD5['M0'][:8], MD5['M0R'][:8]))
assert m1 and m2 and m3, 'ORDER M HALT: a build-failing identity did not hold'

# ------------------------------------------------------------------ G5 · the owner's two reference rows
P('\n' + '=' * 116)
P('G5 — THE POINT OF THIS ORDER. harry-dean ~2,600 and cooper-duff-tytler ~1,800.')
P('=' * 116)
G5 = {}
for k, target, c31 in (('harry-dean', 2600, 2670), ('cooper-duff-tytler', 1800, 1832)):
    row = dict(target=target, c31=c31)
    for t in TAGS:
        row[t] = V[t][k]
    row['M0_minus_K'] = V['M0'][k] - V['K'][k]
    row['M0_minus_landing'] = V['M0'][k] - V['cand'][k]
    row['M0_short_of_target'] = target - V['M0'][k]
    G5[k] = row
    P('\n  %s  (age %d, pick %s, %d career games, %s)'
      % (k, AGE[k], B['cand'][k].get('pk'), float(B['cand'][k].get('cg') or 0), POS[k]))
    P('    owner\'s reference ~%d   ·   candidate 31 %d' % (target, c31))
    P('    landing candidate        %6d' % V['cand'][k])
    P('    ORDER K (eta 0.50)       %6d   (%+d vs landing)' % (V['K'][k], V['K'][k] - V['cand'][k]))
    P('    ORDER M0 (ETA = 0)       %6d   (%+d vs ORDER K, %+d vs landing)'
      % (V['M0'][k], V['M0'][k] - V['K'][k], V['M0'][k] - V['cand'][k]))
    P('    MMIN (dose 0, eta 0.31)  %6d' % V['MMIN'][k])
    P('    MLO  (dose 0, eta 0)     %6d' % V['MLO'][k])
    P('    -> at eta = 0 he is %s the owner\'s ~%d by %d points.'
      % ('ABOVE' if V['M0'][k] >= target else 'SHORT OF', target, abs(target - V['M0'][k])))

# ------------------------------------------------------------------ G6 · the sub-expectation rows
P('\n' + '=' * 116)
P('G6 — SUB-EXPECTATION-WITH-GAMES ROWS MUST NOT RISE. (against the landing candidate)')
P('=' * 116)
P('  %-20s %5s %5s %5s | %8s %8s %8s %8s %8s'
  % ('row', 'age', 'pick', 'games', 'landing', 'ORDER K', 'ORDER M0', 'MLO', 'MMIN'))
G6 = {}
for k in ('xavier-taylor', 'daniel-annable', 'dylan-patterson'):
    a = V['cand'][k]
    G6[k] = {t: V[t][k] for t in TAGS}
    G6[k]['d_M0_vs_landing'] = V['M0'][k] - a
    G6[k]['d_K_vs_landing'] = V['K'][k] - a
    P('  %-20s %5d %5s %5.0f | %8d %8d %8d %8d %8d'
      % (k, AGE[k], B['cand'][k].get('pk'), float(B['cand'][k].get('cg') or 0),
         a, V['K'][k], V['M0'][k], V['MLO'][k], V['MMIN'][k]))
P()
P('  %-20s %28s %10s %10s' % ('row', 'ORDER K vs landing', 'M0 vs K', 'M0 vs landing'))
for k in G6:
    P('  %-20s %+28d %+10d %+10d   -> %s'
      % (k, G6[k]['d_K_vs_landing'], V['M0'][k] - V['K'][k], G6[k]['d_M0_vs_landing'],
         'RISES — G6 BREACHED' if G6[k]['d_M0_vs_landing'] > 0 else 'holds'))
nb = sum(1 for k in G6 if G6[k]['d_M0_vs_landing'] > 0)
P('  -> G6 on ORDER M0: %d of 3 rows RISE. %s' % (nb, 'BREACH' if nb else 'PASS'))
P('  and on the coolest eta=0 point MLO (age bar OFF entirely):')
for k in G6:
    P('    %-20s landing %5d -> MLO %5d  (%+d)  %s'
      % (k, V['cand'][k], V['MLO'][k], V['MLO'][k] - V['cand'][k],
         'RISES' if V['MLO'][k] > V['cand'][k] else 'holds'))

# ------------------------------------------------------------------ the other named rows
NAMED = ['harry-dean', 'cooper-duff-tytler', 'isaac-kako', 'alix-tauru', 'jedd-busslinger',
         'xavier-taylor', 'daniel-annable', 'dylan-patterson', 'josh-smillie', 'oskar-taylor',
         'will-brodie', 'campbell-chesser', 'james-leake', 'tom-brown', 'sam-sturt',
         'will-green', 'toby-conway', 'william-mccabe', 'alex-dodson', 'steely-green',
         'milan-murdock', 'chris-scerri', 'thomas-burton', 'murphy-reid', 'noah-mraz',
         'logan-morris', 'levi-ashcroft', 'colby-mckercher', 'sam-taylor', 'tom-green',
         'toby-greene', 'taylor-walker', 'will-ashcroft']
P('\n' + '=' * 116)
P('THE NAMED ROWS, ACROSS EVERY BOARD (board points)')
P('=' * 116)
P('  %-22s %4s %5s %6s | %8s %8s %8s %8s %8s | %9s'
  % ('row', 'age', 'pick', 'games', 'C31', 'landing', 'ORDER K', 'M0 eta=0', 'MMIN', 'M0 - K'))
NAMEDOUT = {}
for k in NAMED:
    if k not in V['cand']:
        P('  %-22s (not on the 804-row active board)' % k); continue
    NAMEDOUT[k] = {t: V[t][k] for t in TAGS}
    NAMEDOUT[k]['c31'] = R31.get(k, {}).get('cand')
    P('  %-22s %4d %5s %6.0f | %8s %8d %8d %8d %8d | %+9d'
      % (k, AGE[k], B['cand'][k].get('pk'), float(B['cand'][k].get('cg') or 0),
         R31.get(k, {}).get('cand', '-'), V['cand'][k], V['K'][k], V['M0'][k], V['MMIN'][k],
         V['M0'][k] - V['K'][k]))

# ------------------------------------------------------------------ G7 smillie, G8 mature law, J-TOL
P('\n' + '=' * 116)
P('G7 — JOSH SMILLIE HOLDS HIS RULED ~700s')
P('=' * 116)
sk = 'josh-smillie'
P('  landing %d · ORDER K %d · ORDER M0 %d · MLO %d · MMIN %d'
  % (V['cand'][sk], V['K'][sk], V['M0'][sk], V['MLO'][sk], V['MMIN'][sk]))
P('  -> %s on M0' % ('PASS — inside the ruled ~700s' if 700 <= V['M0'][sk] < 800
                     else 'FAIL — he reads %d' % V['M0'][sk]))

MAT = [k for k in KEYS if AGE[k] >= 24]
BOARD_TOTAL = sum(V['cand'].values())
P('\n' + '=' * 116)
P('G8 — S1\'s ZERO-TOLERANCE MATURE LAW, and J-TOL on the veteran pool')
P('=' * 116)
P('  board total (landing candidate, integer prices) = %d;  mature rows aged 24+ = %d'
  % (BOARD_TOTAL, len(MAT)))
JTOL = {}
for lab, t in (('the AGE BAR ALONE at dose 0.40 (ZERO TOLERANCE — the owner\'s law)', 's1'),
               ('ORDER K in full', 'K'),
               ('ORDER M0 — ORDER K with ETA := 0', 'M0'),
               ('MLO — the coolest eta=0 point', 'MLO'),
               ('MMIN — dose 0, eta 0.31', 'MMIN')):
    mv = [(k, V[t][k] - V['cand'][k]) for k in MAT if V[t][k] != V['cand'][k]]
    tot = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    w = max(mv, key=lambda x: abs(x[1])) if mv else (None, 0)
    cap = [(k, d) for k, d in mv if abs(d) > min(25.0, max(1.0, 0.005 * V['cand'][k]))]
    JTOL[t] = dict(n_move=len(mv), churn=tot, net=net, worst=w[1],
                   worst_row=(B['cand'][w[0]].get('name') if w[0] else None),
                   per_row_breaches=len(cap))
    P('  %-62s %3d move · churn %6d · net %+6d · worst %+5d (%s)'
      % (lab, len(mv), tot, net, w[1], (B['cand'][w[0]].get('name') if w[0] else '-')))
P('  J-TOL rails: per row min(25, max(1, 0.5%% of his own price)) · churn <= %.2f (0.15%% of the board)'
  ' · net <= %.2f (0.10%%)' % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
for t in ('s1', 'K', 'M0', 'MLO', 'MMIN'):
    d = JTOL[t]
    P('  %-6s per-row breaches %3d · churn %6d vs %8.2f %-6s · net %+7d vs %8.2f %s'
      % (t, d['per_row_breaches'], d['churn'], 0.0015 * BOARD_TOTAL,
         'OK' if d['churn'] <= 0.0015 * BOARD_TOTAL else 'BREACH',
         d['net'], 0.0010 * BOARD_TOTAL,
         'OK' if abs(d['net']) <= 0.0010 * BOARD_TOTAL else 'BREACH'))
P('  -> G8 (the age bar alone moves ZERO mature rows): %s'
  % ('PASS — 0 of %d' % len(MAT) if JTOL['s1']['n_move'] == 0
     else 'FAIL — M4 FIRES, %d rows move' % JTOL['s1']['n_move']))

# ------------------------------------------------------------------ the year-1 class on today's board
Y1 = [k for k in KEYS if (R31.get(k, {}).get('yr') == 2025)
      or (R31.get(k, {}).get('yr') == 2026 and R31.get(k, {}).get('pathway') == 'MSD')]
P('\n' + '=' * 116)
P('THE YEAR-1 CLASS ON THE 2026 BOARD (board points — a DIFFERENT object from the historical mark)')
P('=' * 116)
t0 = sum(V['cand'][k] for k in Y1)
for t in ('K', 'M0', 'MLO', 'MMIN'):
    tt = sum(V[t][k] for k in Y1)
    up = sum(1 for k in Y1 if V[t][k] > V['cand'][k]); dn = sum(1 for k in Y1 if V[t][k] < V['cand'][k])
    P('  %-5s %d rows, %d -> %d (%+.2f%%);  %d up, %d down, %d unchanged'
      % (t, len(Y1), t0, tt, 100 * (tt - t0) / max(1, t0), up, dn, len(Y1) - up - dn))

P('\n' + '=' * 116)
P('BOARD TOTALS')
P('=' * 116)
for t in TAGS:
    P('  %-5s %s  total %8d  (%+d vs the landing candidate)'
      % (t, MD5[t][:8], sum(V[t].values()), sum(V[t].values()) - BOARD_TOTAL))

# ------------------------------------------------------------------ the biggest movers, M0 vs ORDER K
P('\n' + '=' * 116)
P('WHERE THE MONEY GOES WHEN ETA IS SET TO ZERO (ORDER M0 minus ORDER K)')
P('=' * 116)
mv = sorted(((k, V['M0'][k] - V['K'][k]) for k in KEYS), key=lambda x: -x[1])
P('  %d of %d rows move.  total %+d board points.'
  % (sum(1 for _, d in mv if d != 0), len(KEYS), sum(d for _, d in mv)))
P('\n  THE TWENTY LARGEST RISES')
for k, d in mv[:20]:
    P('    %-26s %-5s age %2d  %4.0f games  %6d -> %6d  %+5d'
      % (B['cand'][k].get('name') or k, POS[k], AGE[k], float(B['cand'][k].get('cg') or 0),
         V['K'][k], V['M0'][k], d))
P('\n  THE TWENTY LARGEST FALLS')
for k, d in mv[::-1][:20]:
    P('    %-26s %-5s age %2d  %4.0f games  %6d -> %6d  %+5d'
      % (B['cand'][k].get('name') or k, POS[k], AGE[k], float(B['cand'][k].get('cg') or 0),
         V['K'][k], V['M0'][k], d))
byg = collections.defaultdict(lambda: [0, 0])
for k, d in mv:
    g = float(B['cand'][k].get('cg') or 0)
    bkt = '0' if g == 0 else ('1-4' if g <= 4 else ('5-9' if g <= 9 else ('10-15' if g <= 15 else
          ('16-29' if g <= 29 else ('30-59' if g <= 59 else '60+')))))
    byg[bkt][0] += 1; byg[bkt][1] += d
P('\n  BY CAREER GAMES — this is the shape of the charge eta was levying:')
P('    %-8s %6s %10s %10s' % ('games', 'rows', 'total pts', 'per row'))
for bkt in ('0', '1-4', '5-9', '10-15', '16-29', '30-59', '60+'):
    n, s = byg[bkt]
    P('    %-8s %6d %+10d %10.1f' % (bkt, n, s, s / max(1, n)))
P('    Read the 10-15 row. That is where GAMMA_D = 14 puts the peak of the bump. It is a pure')
P('    function of games played, so it lands on every row in that band whatever he is producing.')

json.dump(dict(order='ORDER M — the board gates', boards={t: MD5[t] for t in TAGS},
               m1_dial_off=m1, m2_orderK_reproduces=m2, m3_determinism=m3,
               g5=G5, g6=G6, named=NAMEDOUT, jtol=JTOL,
               smillie={t: V[t][sk] for t in TAGS},
               year1=dict(n=len(Y1), landing=t0, **{t: sum(V[t][k] for k in Y1) for t in TAGS}),
               totals={t: sum(V[t].values()) for t in TAGS},
               movers_M0_vs_K=dict(up=[[k, d] for k, d in mv[:40]],
                                   down=[[k, d] for k, d in mv[::-1][:40]]),
               by_games={k: v for k, v in byg.items()}),
          open(os.path.join(HERE, 'GATES_M.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'GATES_M_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: GATES_M.json / GATES_M_out.txt')
