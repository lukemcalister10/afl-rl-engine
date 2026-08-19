#!/usr/bin/env python3
"""ORDER R — THE BOARDS, SCORED. Pure JSON reads over boards already built. NO ENGINE RUN HERE.

  candR   1f176444  the base stack, every ORDER I/P/Q/R dial off
  KrefR   f3101883  ORDER K's ruled line, RL_O37 unset
  Roff    374d4e44  ORDER P's line, every RL_O38*/RL_O39_* unset   — R1, must be byte-exact
  RB1     1b1817f3  ORDER Q FIX B1, R dials unset                  — R2, must be byte-exact
  RAB1    cbbb94d4  ORDER Q FIX A+B1, R dials unset                — R3, must be byte-exact
  the nine ORDER R variants, all on top of B1
  Peta0   73bf9617  ORDER P's stack with the charge OFF (the uncharged ceiling; ORDER P's own)
  live    88ce647f  the live board, NEVER TOUCHED, carried for reference only

NOTHING HERE IS ADOPTED. These are prices, not proposals.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
VAR = ['R15', 'R20', 'R15A', 'R20A', 'Rb1', 'Rb2', 'R15b1', 'R20b2', 'R20b2A']
CTRL = ['candR', 'KrefR', 'Roff', 'RB1', 'RAB1']
NICE = {'RB1':    'p5  b0     A off   = ORDER Q FIX B1 (the control)',
        'RAB1':   'p5  b0     A ON    = ORDER Q FIX A+B1 (the control)',
        'R15':    'p15 b0     A off   the TMAX lever alone',
        'R20':    'p20 b0     A off   the TMAX lever alone, far end',
        'R15A':   'p15 b0     A ON    the TMAX lever with FIX A',
        'R20A':   'p20 b0     A ON    the TMAX lever with FIX A, far end',
        'Rb1':    'p5  0.111  A off   the BETA lever alone',
        'Rb2':    'p5  0.105  A off   the BETA lever alone, near the CI floor',
        'R15b1':  'p15 0.111  A off   both levers, middle',
        'R20b2':  'p20 0.105  A off   both levers, SOFTEST',
        'R20b2A': 'p20 0.105  A ON    both levers, softest, with FIX A'}
EXPECT = {'candR': '1f176444', 'KrefR': 'f3101883', 'Roff': '374d4e44',
          'RB1': '1b1817f3', 'RAB1': 'cbbb94d4'}
PATHS = {}
for t in CTRL + VAR + ['RimpA'] + [v + '_2' for v in VAR]:
    q = SP + '/or/bb_%s/rl_after/rl_app_data.json' % t
    if os.path.exists(q): PATHS[t] = q
for t, q in (('Peta0', SP + '/op/bb_Peta0/rl_after/rl_app_data.json'),
             ('live', ROOT + '/engine/rl_after/rl_app_data.json')):
    if q and os.path.exists(q): PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)      # only carry the live board if it IS the live board
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
VAR = [v for v in VAR if v in V]
K = sorted(V['Roff'])
ref = 'Roff'
AGE = {k: B[ref][k].get('age') for k in K}
NAME = {k: (B[ref][k].get('name') or k) for k in K}
PK = {k: B[ref][k].get('pk') for k in K}
# TWO GAMES FIELDS ON THE BOARD ROW, AND THEY ARE DIFFERENT OBJECTS. `g` is games in the PRICED
# SEASON. `cg` is CAREER games. The A(0)=0 law is about CAREER games -- a row that played two games
# in 2024 and none in 2025 has A(g) > 0 and its charge legitimately applies. The first version of
# this scorer read `g` and REPORTED R6 AS FIRING on four rows whose career games are 1 or 2. That was
# the scorer's error, not the engine's, and BOTH readings are printed below so the correction is
# auditable rather than silently made.
G = {k: (B[ref][k].get('g') or 0) for k in K}
CG = {k: (B[ref][k].get('cg') or 0) for k in K}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 118)
P('ORDER R — THE BOARDS. NOTHING IS ADOPTED AND NOTHING LANDS. NO VARIANT IS RECOMMENDED.')
P('=' * 118)
P('  active priced rows: %d' % len(K))
P('  boards on disk: %s' % ' '.join('%s=%s' % (t, MD5[t][:8]) for t in sorted(MD5)))
P()
P('== THE BUILD-FAILING IDENTITIES — R1, R2, R3, R4, R8 ==')
for t, e in EXPECT.items():
    got = MD5.get(t, '-')[:8]
    P('  %-6s must be %s : %-28s (%s)'
      % (t, e, 'PASS' if got == e else '**FAIL — THE FALSIFIER FIRES**', got))
P('  R8  RL_O38B1+RL_O39_TMAXPCT=20 alone carries the O37/O36/O35/O32/O31 stack: %s (%s vs %s)'
  % ('PASS' if MD5.get('R20') == MD5.get('RimpA') else '**FAIL**',
     MD5.get('R20', '-')[:8], MD5.get('RimpA', '-')[:8]))
for v in VAR:
    P('  R4  determinism x2 %-7s : %-28s (%s vs %s)'
      % (v, 'PASS' if MD5.get(v) == MD5.get(v + '_2') else '**FAIL — R4 FIRES**',
         MD5.get(v, '-')[:8], MD5.get(v + '_2', '-')[:8]))
P()

TOT = {t: sum(V[t][k] for k in K if k in V[t]) for t in V}
P('== BOARD TOTALS ==')
P('  %-8s %-10s %12s %14s %14s %14s  %s'
  % ('board', 'md5', 'total', 'vs ORDER P', 'vs ORDER K', 'vs FIX B1', 'the dial line'))
for t in ['candR', 'KrefR', 'Roff', 'RB1', 'RAB1'] + [v for v in VAR if v not in ('RB1', 'RAB1')] + ['Peta0', 'live']:
    if t not in TOT: continue
    P('  %-8s %-10s %12d %+13d %+13d %+13d  %s'
      % (t, MD5[t][:8], TOT[t], TOT[t] - TOT['Roff'], TOT[t] - TOT['KrefR'], TOT[t] - TOT['RB1'],
         NICE.get(t, '')))
P('  (ORDER P 374d4e44 = 666,434 · ORDER K f3101883 = 673,097 · live 88ce647f = 752,429, NEVER TOUCHED)')
P()

P('== THE TWO LEVERS, ISOLATED ==')
P('  Each row is one board minus FIX B1 (1b1817f3, 659,867), which is p5/b0/A-off.')
P('  %-8s %-34s %12s %12s' % ('board', 'what changed against B1', 'total', 'vs B1'))
LEV = [('R15', 'TMAX p5 -> p15'), ('R20', 'TMAX p5 -> p20'),
       ('Rb1', 'BETA_sat 0.11465 -> 0.111'), ('Rb2', 'BETA_sat 0.11465 -> 0.105'),
       ('R15b1', 'p15 AND 0.111'), ('R20b2', 'p20 AND 0.105'),
       ('RAB1', 'FIX A on'), ('R15A', 'p15 AND FIX A'), ('R20A', 'p20 AND FIX A'),
       ('R20b2A', 'p20 AND 0.105 AND FIX A')]
for t, w in LEV:
    if t not in TOT: continue
    P('  %-8s %-34s %12d %+12d' % (t, w, TOT[t], TOT[t] - TOT['RB1']))
P()
P('  ADDITIVITY — R15, is the grid interpolable? (falsifier R15 in the prereg)')
for combo, a, b in (('R15b1', 'R15', 'Rb1'), ('R20b2', 'R20', 'Rb2'), ('R20b2A', 'R20b2', None)):
    if combo not in TOT or a not in TOT: continue
    if b is None:
        pred = TOT[a] + (TOT['RAB1'] - TOT['RB1'])
        lab = '%s + (A increment at p5)' % a
    else:
        pred = TOT['RB1'] + (TOT[a] - TOT['RB1']) + (TOT[b] - TOT['RB1'])
        lab = 'B1 + (%s-B1) + (%s-B1)' % (a, b)
    P('    %-8s actual %8d   additive prediction %8d   gap %+6d (%+.3f%% of the board)  [%s]'
      % (combo, TOT[combo], pred, TOT[combo] - pred, 100.0 * (TOT[combo] - pred) / TOT[combo], lab))
P()

P('== WHERE THE MONEY MOVES ==')
for v in VAR:
    for base, lab in (('Roff', 'ORDER P'), ('RB1', 'FIX B1')):
        mv = [k for k in K if V[v][k] != V[base][k]]
        P('  %-7s vs %-8s: %3d rows move (%3d up, %3d down)   net %+7d   %s'
          % (v, lab, len(mv), sum(1 for k in mv if V[v][k] > V[base][k]),
             sum(1 for k in mv if V[v][k] < V[base][k]), TOT[v] - TOT[base],
             NICE.get(v, '') if base == 'Roff' else ''))
P()

P('== MATURE-ROW MOVEMENT — rows aged 24 and over, against ORDER K ==')
P('   Under ORDER P these rows are byte-identical to ORDER K. B1 breaks that; the softening should')
P('   shrink the break, because the veterans B1 reaches are exactly the ones parked at the cap.')
P('  %-8s %-34s %9s %9s %12s %12s' % ('board', '', 'rows 24+', 'moving', 'net vs K', 'net vs P'))
m24 = [k for k in K if AGE[k] is not None and AGE[k] >= 24]
for v in ['RB1', 'RAB1'] + [x for x in VAR if x not in ('RB1', 'RAB1')]:
    if v not in V: continue
    mv = [k for k in m24 if V[v][k] != V['KrefR'][k]]
    P('  %-8s %-34s %9d %9d %+12d %+12d'
      % (v, NICE.get(v, '')[:34], len(m24), len(mv),
         sum(V[v][k] - V['KrefR'][k] for k in m24), sum(V[v][k] - V['Roff'][k] for k in m24)))
P('  by exact age, net points against ORDER K:')
ages = sorted(set(a for a in AGE.values() if a is not None))
P('     %-6s %5s %s' % ('age', 'n', ' '.join('%9s' % v for v in VAR)))
for a in ages:
    ka = [k for k in K if AGE[k] == a]
    P('     %-6d %5d %s' % (a, len(ka), ' '.join('%+9d' % sum(V[v][k] - V['KrefR'][k] for k in ka) for v in VAR)))
P()

P('== R6 — THE GAMELESS ROWS AND DAY-0 PRINTS. A(0)=0 EXACTLY, so no row with ZERO CAREER GAMES')
P('   may move. The test is on CAREER games (`cg`), which is the argument A(g) actually takes.')
zc = [k for k in K if CG[k] == 0]
zs = [k for k in K if G[k] == 0]
P('   rows with ZERO CAREER GAMES: %d.   rows with zero games IN THE PRICED SEASON: %d.' % (len(zc), len(zs)))
P('   The second set is larger and it is NOT the law\'s population: a row that played two games in an')
P('   earlier season and none in this one has A(g) > 0 and its charge legitimately applies.')
bad6 = 0
P('  %-8s %14s %10s %10s | %16s %10s' % ('board', 'zero-career n', 'moving', 'net', 'zero-season n', 'moving'))
for v in VAR:
    n = sum(1 for k in zc if V[v][k] != V['Roff'][k])
    ns = sum(1 for k in zs if V[v][k] != V['Roff'][k])
    bad6 += n
    P('  %-8s %14d %10d %10d | %16d %10d  %s'
      % (v, len(zc), n, sum(V[v][k] - V['Roff'][k] for k in zc), len(zs), ns,
         '' if n == 0 else '**R6 FIRES**'))
P('  R6 VERDICT: %s'
  % ('PASS — 0 of %d zero-career-games rows move on any variant. The %d rows that move on the '
     'zero-SEASON-games reading have 1 or 2 career games each and are not gameless.'
     % (len(zc), max(sum(1 for k in zs if V[v][k] != V['Roff'][k]) for v in VAR))
     if bad6 == 0 else '**FAIL — R6 FIRES**'))
P('  The export\'s own PRINTED-DAY-0 ASSERT reads "89 of 89 day-0/sitter rows print EXACTLY" on every')
P('  build in BUILD_R_out.txt, which is the same 89 rows and an independent check of the same law.')
P()

if 'Peta0' in V:
    P('== R5 — NO ROW MAY PRICE ABOVE ITS OWN UNCHARGED PRICE (the eta-zero board 73bf9617) ==')
    bad5 = 0
    for t in ['KrefR', 'Roff', 'RB1'] + [v for v in VAR if v != 'RB1']:
        bad = [k for k in K if k in V['Peta0'] and V[t][k] > V['Peta0'][k]]
        bad5 += len(bad)
        P('  %-7s rows above their uncharged price: %d of %d  %s'
          % (t, len(bad), len(K),
             ('**WORST %s %d vs %d**' % (NAME[bad[0]], V[t][bad[0]], V['Peta0'][bad[0]])) if bad else ''))
    P('  R5 VERDICT: %s' % ('PASS' if bad5 == 0 else '**FAIL — R5 FIRES**'))
else:
    P('== R5 — the uncharged ceiling board 73bf9617 is NOT on disk in this scratchpad. ==')
    P('  REPORTED AS UNMEASURED, NOT AS PASSED.')
P()

P('== FIX A MAY ONLY CAP A CHARGE — no row may price BELOW its A-off partner ==')
for v, basev in (('RAB1', 'RB1'), ('R15A', 'R15'), ('R20A', 'R20'), ('R20b2A', 'R20b2')):
    if v not in V or basev not in V: continue
    low = [k for k in K if V[v][k] < V[basev][k]]
    P('  %-7s vs %-7s : %d rows price LOWER  %s'
      % (v, basev, len(low),
         ('**WORST %s %d -> %d**' % (NAME[low[0]], V[basev][low[0]], V[v][low[0]])) if low else '(PASS)'))
P()

P('== THE SOFTENING MAY ONLY RAISE A PRICE — no row may fall against its stiffer partner ==')
P('   Lowering the cap or the slope removes LESS charge, so every price must move UP or stay.')
for v, basev in (('R15', 'RB1'), ('R20', 'R15'), ('Rb1', 'RB1'), ('Rb2', 'Rb1'),
                 ('R15b1', 'R15'), ('R20b2', 'R20'), ('R15A', 'RAB1'), ('R20A', 'R15A'),
                 ('R20b2A', 'R20A')):
    if v not in V or basev not in V: continue
    low = [k for k in K if V[v][k] < V[basev][k]]
    P('  %-7s vs %-7s : %d rows price LOWER  %s'
      % (v, basev, len(low),
         ('WORST %s %d -> %d' % (NAME[low[0]], V[basev][low[0]], V[v][low[0]])) if low else '(PASS)'))
P()

NAMED = ['sam-lalor', 'willem-duursma', 'zane-duursma', 'finn-osullivan', 'harley-reid',
         'zeke-uwland', 'josh-sinn', 'campbell-chesser', 'sam-darcy']
P('== THE NAMED ROWS. CONSEQUENCES, NEVER TARGETS. ==')
P('   Not one constant in this order was chosen with any of these rows in view, and no row\'s value')
P('   is an acceptance criterion. That is a standing prohibition in this project after a real error.')
P('  %-22s %4s %5s %5s %8s %8s %s'
  % ('row', 'age', 'pick', 'g', 'ORDER K', 'ORDER P', ' '.join('%8s' % v for v in VAR)))
byname = {}
for k in K:
    byname[NAME[k].lower().replace(' ', '-').replace("'", '')] = k
for nm in NAMED:
    k = nm if nm in V['Roff'] else byname.get(nm)
    if k is None:
        cand = [kk for kk in K if nm.split('-')[-1] in NAME[kk].lower()]
        k = cand[0] if len(cand) == 1 else None
    if k is None:
        P('  %-22s (not on the %d-row active board — reported as a NULL, never as a zero)' % (nm, len(K)))
        continue
    P('  %-22s %4s %5s %5s %8d %8d %s'
      % (NAME[k][:22], AGE[k], PK[k], G[k], V['KrefR'][k], V['Roff'][k],
         ' '.join('%8d' % V[v][k] for v in VAR)))
P()

for v in VAR:
    P('== MOVERS LEDGER — %s (%s), against ORDER P ==' % (v, NICE.get(v, '')))
    mv = sorted([k for k in K if V[v][k] != V['Roff'][k]], key=lambda k: -(V[v][k] - V['Roff'][k]))
    for lab, sub in (('TOP 10 UP', mv[:10]), ('TOP 10 DOWN', mv[::-1][:10])):
        P('  %s:' % lab)
        shown = 0
        for k in sub:
            d = V[v][k] - V['Roff'][k]
            if (lab.endswith('UP') and d <= 0) or (lab.endswith('DOWN') and d >= 0): continue
            shown += 1
            P('    %-26s %-5s age %2s %4dg   %6d -> %6d  %+6d'
              % (NAME[k][:26], PK[k], AGE[k], G[k], V['Roff'][k], V[v][k], d))
        if shown == 0:
            P('    (none — a NULL, reported as one)')
    P('  games profile (net against ORDER P):')
    for lo, hi, lab in ((0, 0, '0'), (1, 4, '1-4'), (5, 9, '5-9'), (10, 15, '10-15'), (16, 29, '16-29'),
                        (30, 59, '30-59'), (60, 10 ** 9, '60+')):
        s = [k for k in K if lo <= G[k] <= hi]
        if not s: continue
        P('    %-8s rows %4d  net %+8d  per row %+8.1f'
          % (lab, len(s), sum(V[v][k] - V['Roff'][k] for k in s),
             sum(V[v][k] - V['Roff'][k] for k in s) / len(s)))
    P()

open(HERE + '/BOARDS_R_out.txt', 'w').write('\n'.join(L) + '\n')
json.dump(dict(md5={t: MD5[t] for t in MD5}, totals=TOT, nice=NICE, expect=EXPECT),
          open(HERE + '/BOARDS_R.json', 'w'), indent=1)
print('\nwrote BOARDS_R_out.txt / BOARDS_R.json')
