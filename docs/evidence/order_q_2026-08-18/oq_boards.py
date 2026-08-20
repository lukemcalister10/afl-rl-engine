#!/usr/bin/env python3
"""ORDER Q — THE BOARDS, SCORED. Pure JSON reads over boards already built. No engine run here.

  candQ  1f176444  the base stack, every ORDER I/P/Q dial off
  KrefQ  f3101883  ORDER K's ruled line, RL_O37 unset
  Qoff   374d4e44  ORDER P's line with every RL_O38* unset — FALSIFIER Q1, must be byte-exact
  QA / QB1 / QB2 / QAB1 / QAB2   the five variants this order prices
  Peta0  73bf9617  ORDER P's stack with the charge switched OFF (the uncharged ceiling; ORDER P's own)

NOTHING HERE IS ADOPTED. These are prices, not proposals.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
PATHS = {}
for t in ('candQ', 'KrefQ', 'Qoff', 'QA', 'QB1', 'QB2', 'QAB1', 'QAB2', 'QAimp',
          'QA_2', 'QB1_2', 'QB2_2', 'QAB1_2', 'QAB2_2'):
    q = SP + '/oq/bb_%s/rl_after/rl_app_data.json' % t
    if os.path.exists(q): PATHS[t] = q
for t, q in (('Peta0', SP + '/op/bb_Peta0/rl_after/rl_app_data.json'),
             ('cand31', None), ('landing', SP + '/op/bb_candP/rl_after/rl_app_data.json')):
    if q and os.path.exists(q): PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
VAR = [v for v in ('QA', 'QB1', 'QB2', 'QAB1', 'QAB2') if v in V]
NICE = {'QA': 'FIX A — the pedigree leg monotonised in entry price',
        'QB1': 'FIX B1 — the age-24 gate deleted',
        'QB2': 'FIX B2 — the charge ramped out across ages 23-26 (invented endpoint)',
        'QAB1': 'FIX A + B1', 'QAB2': 'FIX A + B2'}
K = sorted(V['Qoff']) if 'Qoff' in V else sorted(V[VAR[0]])
AGE = {k: B[VAR[0]][k]['age'] for k in K}
NAME = {k: (B[VAR[0]][k].get('name') or k) for k in K}
PK = {k: B[VAR[0]][k].get('pk') for k in K}
G = {k: (B[VAR[0]][k].get('g') or 0) for k in K}
TY = {k: B[VAR[0]][k].get('ty') for k in K}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 116)
P('ORDER Q — THE BOARDS. NOTHING IS ADOPTED AND NOTHING LANDS.')
P('=' * 116)
P('  boards: %s' % {t: MD5[t][:8] for t in sorted(MD5)})
P('  active priced rows: %d' % len(K))
P()
P('== THE BUILD-FAILING IDENTITIES ==')
P('  Q4  base stack        = 1f176444 : %s (%s)'
  % ('PASS' if MD5.get('candQ', '').startswith('1f176444') else 'FAIL', MD5.get('candQ', '-')[:8]))
P('  Q5  ORDER K line      = f3101883 : %s (%s)'
  % ('PASS' if MD5.get('KrefQ', '').startswith('f3101883') else 'FAIL', MD5.get('KrefQ', '-')[:8]))
P('  Q1  every RL_O38* off = 374d4e44 : %s (%s)'
  % ('PASS' if MD5.get('Qoff', '').startswith('374d4e44') else 'FAIL — Q1 FIRES', MD5.get('Qoff', '-')[:8]))
P('  Q3  RL_O38A alone carries the stack: %s (%s vs %s)'
  % ('PASS' if MD5.get('QA') == MD5.get('QAimp') else 'FAIL', MD5.get('QA', '-')[:8], MD5.get('QAimp', '-')[:8]))
for v in VAR:
    P('  Q2  determinism x2 %-5s          : %s (%s vs %s)'
      % (v, 'PASS' if MD5.get(v) == MD5.get(v + '_2') else 'FAIL — Q2 FIRES',
         MD5.get(v, '-')[:8], MD5.get(v + '_2', '-')[:8]))
P()

TOT = {t: sum(V[t][k] for k in K if k in V[t]) for t in V}
P('== BOARD TOTALS ==')
P('  %-8s %-10s %12s %14s %14s' % ('board', 'md5', 'total', 'vs ORDER P', 'vs ORDER K'))
for t in ['landing', 'KrefQ', 'Qoff'] + VAR + ['Peta0']:
    if t not in TOT: continue
    P('  %-8s %-10s %12d %+13d %+13d  %s'
      % (t, MD5[t][:8], TOT[t], TOT[t] - TOT['Qoff'], TOT[t] - TOT['KrefQ'], NICE.get(t, '')))
P('  (ORDER P 374d4e44 = 666,434, ORDER K f3101883 = 673,097, live 88ce647f = 752,429 never touched)')
P()

P('== WHERE THE MONEY MOVES, against ORDER P and against ORDER K ==')
for v in VAR:
    mvP = [k for k in K if V[v][k] != V['Qoff'][k]]
    mvK = [k for k in K if V[v][k] != V['KrefQ'][k]]
    P('  %-5s %s' % (v, NICE[v]))
    P('     vs ORDER P: %3d rows move (%3d up, %3d down)   net %+7d'
      % (len(mvP), sum(1 for k in mvP if V[v][k] > V['Qoff'][k]),
         sum(1 for k in mvP if V[v][k] < V['Qoff'][k]), TOT[v] - TOT['Qoff']))
    P('     vs ORDER K: %3d rows move (%3d up, %3d down)   net %+7d'
      % (len(mvK), sum(1 for k in mvK if V[v][k] > V['KrefQ'][k]),
         sum(1 for k in mvK if V[v][k] < V['KrefQ'][k]), TOT[v] - TOT['KrefQ']))
P()

P('== MATURE-ROW MOVEMENT. The order expects ZERO under A and B2 and NON-ZERO under B1. ==')
P('   "mature" = aged 24 and over at the year priced. Movement is measured against ORDER K, which is')
P('   the board those rows have been byte-identical to since ORDER P.')
P('  %-5s %26s %10s %10s %12s %12s' % ('', '', 'rows 24+', 'moving', 'net vs K', 'net vs P'))
for v in VAR:
    m24 = [k for k in K if AGE[k] is not None and AGE[k] >= 24]
    mv = [k for k in m24 if V[v][k] != V['KrefQ'][k]]
    P('  %-5s %-26s %10d %10d %+12d %+12d'
      % (v, NICE[v][:26], len(m24), len(mv), sum(V[v][k] - V['KrefQ'][k] for k in m24),
         sum(V[v][k] - V['Qoff'][k] for k in m24)))
P('  by exact age, net points against ORDER K:')
ages = sorted(set(a for a in AGE.values() if a is not None))
P('     %-6s %5s %s' % ('age', 'n', ' '.join('%9s' % v for v in VAR)))
for a in ages:
    ka = [k for k in K if AGE[k] == a]
    P('     %-6d %5d %s' % (a, len(ka), ' '.join('%+9d' % sum(V[v][k] - V['KrefQ'][k] for k in ka) for v in VAR)))
P()

P('== THE GAMELESS ROWS. A(0)=0, so no row with zero career games may move (Q9). ==')
z = [k for k in K if G[k] == 0]
for v in VAR:
    P('  %-5s zero-games rows %3d, of which move: %d  (net %+d)'
      % (v, len(z), sum(1 for k in z if V[v][k] != V['Qoff'][k]),
         sum(V[v][k] - V['Qoff'][k] for k in z)))
P()

if 'Peta0' in V:
    P('== Q8 — NO ROW MAY PRICE ABOVE ITS OWN UNCHARGED PRICE (the eta-zero board 73bf9617) ==')
    for t in ['KrefQ', 'Qoff'] + VAR:
        bad = [k for k in K if k in V['Peta0'] and V[t][k] > V['Peta0'][k]]
        P('  %-5s rows above their uncharged price: %d of %d  %s'
          % (t, len(bad), len(K), ('WORST %s %d vs %d' % (NAME[bad[0]], V[t][bad[0]], V['Peta0'][bad[0]])) if bad else ''))
    P()

P('== Q7 — FIX A MAY ONLY CAP A CHARGE. No row may price BELOW its ORDER P price under A. ==')
for v, basev in (('QA', 'Qoff'), ('QAB1', 'QB1'), ('QAB2', 'QB2')):
    if v not in V or basev not in V: continue
    low = [k for k in K if V[v][k] < V[basev][k]]
    P('  %-5s vs %-5s : %d rows price LOWER  %s'
      % (v, basev, len(low), ('WORST %s %d -> %d' % (NAME[low[0]], V[basev][low[0]], V[v][low[0]])) if low else '(PASS)'))
P()

P('== Q10 — UNDER B2 A ROW AGED 26 OR OVER MUST BE BYTE-IDENTICAL TO ORDER K ==')
for v in ('QB2', 'QAB2'):
    if v not in V: continue
    o = [k for k in K if AGE[k] is not None and AGE[k] >= 26 and V[v][k] != V['KrefQ'][k]]
    P('  %-5s rows aged 26+: %d, of which move against ORDER K: %d  %s'
      % (v, sum(1 for k in K if AGE[k] is not None and AGE[k] >= 26), len(o), '(PASS)' if not o else 'FAIL'))
P()

NAMED = ['sam-lalor', 'willem-duursma', 'zane-duursma', 'finn-osullivan', 'harley-reid',
         'zeke-uwland', 'josh-sinn', 'campbell-chesser', 'james-tunstill', 'sam-darcy', 'hotton']
P('== THE NAMED ROWS. CONSEQUENCES, NEVER TARGETS. No row\'s value is an acceptance criterion. ==')
P('  %-24s %4s %5s %5s %8s %8s %s' % ('row', 'age', 'pick', 'g', 'ORDER K', 'ORDER P',
                                       ' '.join('%8s' % v for v in VAR)))
byname = {}
for k in K:
    byname[NAME[k].lower().replace(' ', '-').replace("'", '')] = k
for nm in NAMED:
    k = nm if nm in V['Qoff'] else byname.get(nm)
    if k is None:
        cand = [kk for kk in K if nm.split('-')[-1] in NAME[kk].lower()]
        k = cand[0] if len(cand) == 1 else None
    if k is None:
        P('  %-24s (not on the 804-row active board — reported as a null, not as a zero)' % nm); continue
    P('  %-24s %4s %5s %5s %8d %8d %s'
      % (NAME[k][:24], AGE[k], PK[k], G[k], V['KrefQ'][k], V['Qoff'][k],
         ' '.join('%8d' % V[v][k] for v in VAR)))
P()

for v in VAR:
    P('== MOVERS LEDGER — %s (%s), against ORDER P ==' % (v, NICE[v]))
    mv = sorted([k for k in K if V[v][k] != V['Qoff'][k]], key=lambda k: -(V[v][k] - V['Qoff'][k]))
    for lab, sub in (('TOP 10 UP', mv[:10]), ('TOP 10 DOWN', mv[::-1][:10])):
        P('  %s:' % lab)
        for k in sub:
            d = V[v][k] - V['Qoff'][k]
            if (lab.endswith('UP') and d <= 0) or (lab.endswith('DOWN') and d >= 0): continue
            P('    %-26s %-5s age %2s %4dg   %6d -> %6d  %+6d'
              % (NAME[k][:26], PK[k], AGE[k], G[k], V['Qoff'][k], V[v][k], d))
    P('  games profile (net against ORDER P):')
    for lo, hi, lab in ((0, 0, '0'), (1, 4, '1-4'), (5, 9, '5-9'), (10, 15, '10-15'), (16, 29, '16-29'),
                        (30, 59, '30-59'), (60, 10 ** 9, '60+')):
        s = [k for k in K if lo <= G[k] <= hi]
        if not s: continue
        P('    %-8s rows %4d  net %+8d  per row %+8.1f'
          % (lab, len(s), sum(V[v][k] - V['Qoff'][k] for k in s),
             sum(V[v][k] - V['Qoff'][k] for k in s) / len(s)))
    P()

open(HERE + '/BOARDS_Q_out.txt', 'w').write('\n'.join(L) + '\n')
json.dump(dict(md5={t: MD5[t] for t in MD5}, totals=TOT), open(HERE + '/BOARDS_Q.json', 'w'), indent=1)
print('\nwrote BOARDS_Q_out.txt / BOARDS_Q.json')
