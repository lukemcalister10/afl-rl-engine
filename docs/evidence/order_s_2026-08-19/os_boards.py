#!/usr/bin/env python3
"""ORDER S — THE BOARDS, SCORED. Pure JSON reads over boards already built. NO ENGINE RUN HERE.

  SRoff   374d4e44  ORDER P's line, every RL_O38*/RL_O39_*/RL_O40_* unset  — S-F0, must be byte-exact
  SB1     1b1817f3  ORDER Q FIX B1, S dials unset                          — must be byte-exact
  SAB1    cbbb94d4  ORDER Q FIX A+B1, S dials unset                        — must be byte-exact
  SR20A   7f88f509  ORDER R R20A, S dials unset                            — must be byte-exact
  the eleven ORDER S variants, all on top of FIX B1
  Peta0   73bf9617  the charge OFF — the UNCHARGED CEILING (ORDER P's own board, reused)
  KrefS   f3101883  ORDER K's ruled line (ORDER R's own board, reused — declared, not hidden)
  live    88ce647f  the live board, NEVER TOUCHED, carried for reference only

NOTHING HERE IS ADOPTED. These are prices, not proposals.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
VAR = ['SW47', 'SW28', 'SW47A', 'SC15', 'SC20', 'SC20A', 'SL56', 'SL10', 'SM', 'SMA', 'SALL']
CTRL = ['SRoff', 'SB1', 'SAB1', 'SR20A']
NICE = {'SB1':   'FIX B1 alone            = the control every variant sits on',
        'SAB1':  'FIX A + B1              = the control with FIX A',
        'SR20A': 'ORDER R p20 + A + B1    = the ORDER R control',
        'SW47':  'S1 recency w=0.47       the DIRECT out-of-sample optimum',
        'SW28':  'S1 recency w=0.28       the CALIBRATED out-of-sample optimum',
        'SW47A': 'S1 recency w=0.47 + A',
        'SC15':  'S2 compression p15      the owner\'s smooth cap',
        'SC20':  'S2 compression p20      the owner\'s smooth cap, far end',
        'SC20A': 'S2 compression p20 + A',
        'SL56':  'S3 LAMBDA 0.56          the STIFFEST the W2 class floor admits',
        'SL10':  'S3 LAMBDA 0.10          the softening direction',
        'SM':    'S5 mature premium at 24+',
        'SMA':   'S5 mature premium + A',
        'SALL':  'ALL FOUR + FIX A        the far corner. NOT A RECOMMENDATION.'}
EXPECT = {'SRoff': '374d4e44', 'SB1': '1b1817f3', 'SAB1': 'cbbb94d4', 'SR20A': '7f88f509'}
PATHS = {}
for t in CTRL + VAR + ['SimpA'] + [v + '_2' for v in VAR]:
    q = SP + '/os/bb_%s/rl_after/rl_app_data.json' % t
    if os.path.exists(q):
        PATHS[t] = q
for t, q in (('Peta0', SP + '/op/bb_Peta0/rl_after/rl_app_data.json'),
             ('KrefS', SP + '/or/bb_KrefR/rl_after/rl_app_data.json'),
             ('live', ROOT + '/engine/rl_after/rl_app_data.json')):
    if q and os.path.exists(q):
        PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
VAR = [v for v in VAR if v in V]
K = sorted(V['SRoff'])
ref = 'SRoff'
AGE = {k: B[ref][k].get('age') for k in K}
NAME = {k: (B[ref][k].get('name') or k) for k in K}
PK = {k: B[ref][k].get('pk') for k in K}
# TWO GAMES FIELDS AND THEY ARE DIFFERENT OBJECTS. `g` is games in the PRICED SEASON; `cg` is CAREER
# games, which is the argument A(g) actually takes. ORDER R's §14 correction is carried here: the
# A(0)=0 law's population is cg == 0, not g == 0. BOTH readings are printed.
G = {k: (B[ref][k].get('g') or 0) for k in K}
CG = {k: (B[ref][k].get('cg') or 0) for k in K}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 118)
P('ORDER S — THE BOARDS. NOTHING IS ADOPTED AND NOTHING LANDS. NO VARIANT IS RECOMMENDED.')
P('=' * 118)
P('  active priced rows: %d' % len(K))
P('  boards on disk: %s' % ' '.join('%s=%s' % (t, MD5[t][:8]) for t in sorted(MD5)))
P('  DECLARED REUSE: KrefS is ORDER R\'s own bb_KrefR board and Peta0 is ORDER P\'s own uncharged')
P('  ceiling board. Neither is rebuilt here. The ORDER S engine\'s dial-off identity is proved by')
P('  SRoff/SB1/SAB1/SR20A above, which is the stronger test.')
P()
P('== THE BUILD-FAILING IDENTITIES ==')
allpass = True
for t, e in sorted(EXPECT.items()):
    got = MD5.get(t, '-')[:8]
    ok = got == e
    allpass = allpass and ok
    P('  %-6s must be %s : %-30s (%s)'
      % (t, e, 'PASS' if ok else '**FAIL — THE FALSIFIER FIRES**', got))
P('  S-D1  RL_O38B1 + the S2 dials ALONE carry the O37/O36/O35/O32/O31 stack: %s (%s vs %s)'
  % ('PASS' if MD5.get('SC20') == MD5.get('SimpA') else '**FAIL**',
     MD5.get('SC20', '-')[:8], MD5.get('SimpA', '-')[:8]))
det = True
for v in VAR:
    ok = MD5.get(v) == MD5.get(v + '_2')
    det = det and ok
    P('  S-D2  determinism x2 %-7s : %-28s (%s vs %s)'
      % (v, 'PASS' if ok else '**FAIL — DETERMINISM FIRES**',
         MD5.get(v, '-')[:8], MD5.get(v + '_2', '-')[:8]))
P()

TOT = {t: sum(V[t][k] for k in K if k in V[t]) for t in V}
P('== BOARD TOTALS ==')
P('  %-8s %-10s %12s %14s %14s %14s  %s'
  % ('board', 'md5', 'total', 'vs ORDER P', 'vs ORDER K', 'vs FIX B1', 'the dial line'))
order = ['KrefS', 'SRoff', 'SB1', 'SAB1', 'SR20A'] + [v for v in VAR] + ['Peta0', 'live']
for t in order:
    if t not in TOT:
        continue
    P('  %-8s %-10s %12d %+13d %+13d %+13d  %s'
      % (t, MD5[t][:8], TOT[t], TOT[t] - TOT['SRoff'],
         TOT[t] - TOT.get('KrefS', TOT['SRoff']), TOT[t] - TOT['SB1'], NICE.get(t, '')))
P('  (ORDER P 374d4e44 = 666,434 · ORDER K f3101883 = 673,097 · ORDER Q FIX B1 1b1817f3 = 659,867')
P('   · ORDER R R20A 7f88f509 = 664,950 · live 88ce647f = 752,429, NEVER TOUCHED)')
P()

P('== EACH REPAIR ISOLATED, AGAINST FIX B1 (1b1817f3) ==')
P('  %-8s %-40s %12s %12s' % ('board', 'what changed against B1', 'total', 'vs B1'))
LEV = [('SW47', 'S1 recency w=0.47'), ('SW28', 'S1 recency w=0.28'),
       ('SC15', 'S2 compression, p15 anchor'), ('SC20', 'S2 compression, p20 anchor'),
       ('SL56', 'S3 LAMBDA 0.1743833 -> 0.56'), ('SL10', 'S3 LAMBDA 0.1743833 -> 0.10'),
       ('SM', 'S5 mature premium at 24+'),
       ('SAB1', 'FIX A alone (ORDER Q, the reference lever)'),
       ('SR20A', 'ORDER R p20 clip + FIX A (the reference)'),
       ('SW47A', 'S1 w=0.47 AND FIX A'), ('SC20A', 'S2 p20 AND FIX A'),
       ('SMA', 'S5 mature AND FIX A'), ('SALL', 'ALL FOUR AND FIX A')]
for t, w in LEV:
    if t not in TOT:
        continue
    P('  %-8s %-40s %12d %+12d' % (t, w, TOT[t], TOT[t] - TOT['SB1']))
P()
P('  ADDITIVITY — are the repairs readable off each other?')
for combo, parts in (('SW47A', ('SW47', 'SAB1')), ('SC20A', ('SC20', 'SAB1')),
                     ('SMA', ('SM', 'SAB1')),
                     ('SALL', ('SW47', 'SC20', 'SM', 'SAB1'))):
    if combo not in TOT or any(p not in TOT for p in parts):
        continue
    pred = TOT['SB1'] + sum(TOT[p] - TOT['SB1'] for p in parts)
    P('    %-8s actual %8d   additive prediction %8d   gap %+6d (%+.3f%% of the board)  [B1 + %s]'
      % (combo, TOT[combo], pred, TOT[combo] - pred,
         100.0 * (TOT[combo] - pred) / TOT[combo], ' + '.join(parts)))
P()

P('== WHERE THE MONEY MOVES ==')
MOVE = {}
for v in VAR:
    for base, lab in (('SRoff', 'ORDER P'), ('SB1', 'FIX B1')):
        mv = [k for k in K if V[v][k] != V[base][k]]
        up = sum(1 for k in mv if V[v][k] > V[base][k])
        dn = sum(1 for k in mv if V[v][k] < V[base][k])
        if base == 'SB1':
            MOVE[v] = dict(n=len(mv), up=up, down=dn, net=TOT[v] - TOT[base])
        P('  %-7s vs %-8s: %3d rows move (%3d up, %3d down)   net %+7d   %s'
          % (v, lab, len(mv), up, dn, TOT[v] - TOT[base], NICE.get(v, '') if base == 'SRoff' else ''))
P()

P('== MATURE-ROW MOVEMENT — rows aged 24 and over, against ORDER K ==')
P('   Under ORDER P these rows are byte-identical to ORDER K. FIX B1 breaks that (245 rows, -6,567).')
P('   S5 is the repair aimed straight at that break: the premium B1 reads on them was fitted on kids.')
P('  %-8s %-40s %9s %9s %12s %12s' % ('board', '', 'rows 24+', 'moving', 'net vs K', 'net vs P'))
m24 = [k for k in K if AGE[k] is not None and AGE[k] >= 24]
MAT = {}
for v in ['SB1', 'SAB1'] + [x for x in VAR]:
    if v not in V or 'KrefS' not in V:
        continue
    mv = [k for k in m24 if V[v][k] != V['KrefS'][k]]
    MAT[v] = dict(n=len(m24), moving=len(mv),
                  net_k=sum(V[v][k] - V['KrefS'][k] for k in m24),
                  net_p=sum(V[v][k] - V['SRoff'][k] for k in m24))
    P('  %-8s %-40s %9d %9d %+12d %+12d'
      % (v, NICE.get(v, '')[:40], len(m24), len(mv), MAT[v]['net_k'], MAT[v]['net_p']))
P()

P('== THE LAW: A(0)=0 EXACTLY, so NO ROW WITH ZERO CAREER GAMES MAY MOVE ==')
zc = [k for k in K if CG[k] == 0]
zs = [k for k in K if G[k] == 0]
P('   rows with ZERO CAREER GAMES: %d.   rows with zero games IN THE PRICED SEASON: %d.' % (len(zc), len(zs)))
P('   Only the FIRST is the law\'s population — ORDER R\'s §14 correction, carried.')
bad6 = 0
P('  %-8s %14s %10s %10s | %16s %10s' % ('board', 'zero-career n', 'moving', 'net', 'zero-season n', 'moving'))
for v in VAR:
    n = sum(1 for k in zc if V[v][k] != V['SRoff'][k])
    ns = sum(1 for k in zs if V[v][k] != V['SRoff'][k])
    bad6 += n
    P('  %-8s %14d %10d %10d | %16d %10d  %s'
      % (v, len(zc), n, sum(V[v][k] - V['SRoff'][k] for k in zc), len(zs), ns,
         '' if n == 0 else '**THE LAW FIRES**'))
P('  VERDICT: %s' % ('PASS — 0 of %d zero-career-games rows move on any variant.' % len(zc)
                     if bad6 == 0 else '**FAIL**'))
P()

bad5 = 0
if 'Peta0' in V:
    P('== THE LAW: NO ROW MAY PRICE ABOVE ITS OWN UNCHARGED PRICE (the eta-zero board 73bf9617) ==')
    for t in ['SRoff', 'SB1'] + [v for v in VAR]:
        bad = [k for k in K if k in V['Peta0'] and V[t][k] > V['Peta0'][k]]
        bad5 += len(bad)
        P('  %-7s rows above their uncharged price: %d of %d  %s'
          % (t, len(bad), len(K),
             ('**WORST %s %d vs %d**' % (NAME[bad[0]], V[t][bad[0]], V['Peta0'][bad[0]])) if bad else ''))
    P('  VERDICT: %s' % ('PASS' if bad5 == 0 else '**FAIL — THE LAW FIRES**'))
else:
    P('== the uncharged ceiling board is NOT on disk. REPORTED AS UNMEASURED, NOT AS PASSED. ==')
P()

P('== FIX A MAY ONLY CAP A CHARGE — no row may price BELOW its A-off partner ==')
for v, basev in (('SAB1', 'SB1'), ('SW47A', 'SW47'), ('SC20A', 'SC20'), ('SMA', 'SM')):
    if v not in V or basev not in V:
        continue
    low = [k for k in K if V[v][k] < V[basev][k]]
    P('  %-7s vs %-7s : %d rows price LOWER  %s'
      % (v, basev, len(low),
         ('**WORST %s %d -> %d**' % (NAME[low[0]], V[basev][low[0]], V[v][low[0]])) if low else '(PASS)'))
P()

P('== S2-F2: THE COMPRESSION MAY NEVER CHARGE MORE THAN THE HARD CLIP IT REPLACES ==')
P('   T\' < C = TMAX(anchor) <= TMAX(p5) pointwise, so every row must price AT OR ABOVE its')
P('   clip partner. Asserted in the engine at load (S-S5); measured on the board here.')
for v, basev, why in (('SC15', 'SB1', 'compression p15 vs ORDER P\'s p5 clip'),
                      ('SC20', 'SB1', 'compression p20 vs ORDER P\'s p5 clip'),
                      ('SC20A', 'SAB1', 'compression p20 + A vs ORDER P\'s p5 clip + A'),
                      ('SC20A', 'SR20A', 'compression p20 + A vs ORDER R\'s p20 CLIP + A')):
    if v not in V or basev not in V:
        continue
    low = [k for k in K if V[v][k] < V[basev][k]]
    P('  %-7s vs %-7s : %d rows price LOWER   (%s)  %s'
      % (v, basev, len(low), why,
         ('**WORST %s %d -> %d**' % (NAME[low[0]], V[basev][low[0]], V[v][low[0]])) if low else '(PASS)'))
P()

json.dump(dict(md5={t: MD5[t] for t in MD5}, totals=TOT, nice=NICE, expect=EXPECT,
               move=MOVE, mature=MAT, identities=dict(controls=allpass, determinism=det,
                                                      gameless=bad6, uncharged=bad5)),
          open(HERE + '/BOARDS_S.json', 'w'), indent=1)

P('== MOVERS LEDGERS, against ORDER P. CONSEQUENCES, NEVER TARGETS. ==')
for v in VAR:
    P('-- %s (%s) --' % (v, NICE.get(v, '')))
    mv = sorted([k for k in K if V[v][k] != V['SRoff'][k]], key=lambda k: -(V[v][k] - V['SRoff'][k]))
    for lab, sub in (('TOP 10 UP', mv[:10]), ('TOP 10 DOWN', mv[::-1][:10])):
        P('  %s:' % lab)
        shown = 0
        for k in sub:
            d = V[v][k] - V['SRoff'][k]
            if (lab.endswith('UP') and d <= 0) or (lab.endswith('DOWN') and d >= 0):
                continue
            shown += 1
            P('    %-26s %-5s age %2s %4dg   %6d -> %6d  %+6d'
              % (NAME[k][:26], PK[k], AGE[k], G[k], V['SRoff'][k], V[v][k], d))
        if shown == 0:
            P('    (none — a NULL, reported as one)')
    P('  by age band, net against ORDER P:')
    for lo, hi, lab in ((0, 20, '<=20'), (21, 23, '21-23'), (24, 26, '24-26'),
                        (27, 29, '27-29'), (30, 99, '30+')):
        s = [k for k in K if AGE[k] is not None and lo <= AGE[k] <= hi]
        if not s:
            continue
        P('    %-8s rows %4d  net %+8d  movers %4d'
          % (lab, len(s), sum(V[v][k] - V['SRoff'][k] for k in s),
             sum(1 for k in s if V[v][k] != V['SRoff'][k])))
    P()

open(HERE + '/BOARDS_S_out.txt', 'w').write('\n'.join(L) + '\n')
print('\nwrote BOARDS_S_out.txt / BOARDS_S.json')
