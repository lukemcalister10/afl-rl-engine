#!/usr/bin/env python3
"""ORDER R — a compact digest of every result, so the packet quotes files rather than memory.
Read-only over the JSON this order produced. Builds nothing, changes nothing."""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
VAR = ['RB1', 'RAB1', 'R15', 'R20', 'R15A', 'R20A', 'Rb1', 'Rb2', 'R15b1', 'R20b2', 'R20b2A']
L = []
def P(s=''):
    print(s); L.append(str(s))

def jload(n):
    p = os.path.join(HERE, n)
    return json.load(open(p)) if os.path.exists(p) else None

P('=' * 118); P('ORDER R DIGEST'); P('=' * 118)
B = jload('BOARDS_R.json')
if B:
    P('\n-- BOARD TOTALS --')
    T = B['totals']
    for t in ['candR', 'KrefR', 'Roff'] + VAR + ['Peta0', 'live']:
        if t in T:
            P('  %-8s %-9s %8d  vsP %+7d  vsK %+7d  vsB1 %+7d'
              % (t, B['md5'].get(t, '')[:8], T[t], T[t] - T['Roff'], T[t] - T['KrefR'],
                 T[t] - T.get('RB1', T['Roff'])))
P('\n-- CENSUS: BURN, CHARGE DISTRIBUTION, NAMED ROWS --')
CS = {}
for t in ['RP'] + VAR:
    d = jload('CENSUS_%s.json' % t)
    if d: CS[t] = d
P('  %-8s %10s %8s %9s %10s %8s %8s %8s %11s'
  % ('board', 'total', 'burned', 'burn pts', 'max chg', '>90%', '>75%', '>50%', 'TMAX'))
for t in ['RP'] + VAR:
    d = CS.get(t)
    if not d: continue
    sel = [r for r in d['burn'] if abs(float(r['fK']) - float(r['fP37'])) >= 0.02]
    nb = [r for r in sel if int(r['burn_board']) > 0]
    ch = [c for c in d['charge'] if c.get('f') is not None]
    cond = [c for c in ch if c.get('cond')]
    mx = max((1.0 - c['f']) for c in cond) if cond else None
    k = d.get('constants') or {}
    P('  %-8s %10d %8d %9d %10s %8d %8d %8d %11s'
      % (t, d['board_total'], len(nb), sum(int(r['burn_board']) for r in nb),
         ('%.2f%%' % (100 * mx)) if mx is not None else 'n/a',
         sum(1 for c in cond if 1 - c['f'] > 0.90), sum(1 for c in cond if 1 - c['f'] > 0.75),
         sum(1 for c in cond if 1 - c['f'] > 0.50),
         ('%.4f' % k['TMAX']) if k.get('TMAX') else '-'))
P('\n  BURN BY BAND')
P('  %-8s %s' % ('board', ' '.join('%8s' % b for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'))))
for t in ['RP'] + VAR:
    d = CS.get(t)
    if not d: continue
    sel = [r for r in d['burn'] if abs(float(r['fK']) - float(r['fP37'])) >= 0.02]
    row = []
    for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
        s = [r for r in sel if r['band'] == b and int(r['burn_board']) > 0]
        row.append('%8d' % len(s))
    P('  %-8s %s' % (t, ' '.join(row)))
P('\n  NAMED ROWS (consequences, never targets)')
names = ['Zane Duursma', 'Josh Sinn', 'Campbell Chesser', "Finn O'Sullivan", 'Zeke Uwland',
         'Harley Reid', 'Sam Darcy', 'Willem Duursma', 'Sam Lalor']
P('  %-20s %s' % ('row', ' '.join('%8s' % t for t in ['RP'] + VAR)))
for nm in names:
    row = []
    for t in ['RP'] + VAR:
        d = CS.get(t)
        if not d: row.append('%8s' % '-'); continue
        hit = [x for x in d['named'] if x['name'] == nm and x.get('found')]
        row.append('%8s' % (hit[0]['price'] if hit else 'ABSENT'))
    P('  %-20s %s' % (nm, ' '.join(row)))
P('  charge on those rows:')
P('  %-20s %s' % ('row', ' '.join('%8s' % t for t in ['RP'] + VAR)))
for nm in names:
    row = []
    for t in ['RP'] + VAR:
        d = CS.get(t)
        hit = [x for x in (d['named'] if d else []) if x['name'] == nm and x.get('found')]
        c = hit[0].get('charge') if hit else None
        row.append('%8s' % (('%.1f%%' % (100 * c)) if c is not None else '-'))
    P('  %-20s %s' % (nm, ' '.join(row)))
C = jload('CLASS_R.json')
if C:
    P('\n-- CLASS MARKS, REGISTERED W2 BASIS --')
    P('  %-9s %9s %9s %10s %6s' % ('board', 'W2', 'cohort', 'max class', 'year'))
    for t, d in C.items():
        if isinstance(d, dict) and 'w2' in d:
            P('  %-9s %9.4f %9.4f %10.4f %6s' % (t, d['w2'], d['cohort'], d['max_class'], d['max_class_year']))
S = jload('STANDING_TABLES_R.json')
if S:
    P('\n-- YEAR-1 APPRECIATION, PRIMARY WINDOW --')
    bands = ['ALL picks 1-64', 'picks 1-20', 'picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
    P('  %-9s %s' % ('board', ' '.join('%11s' % b.replace('picks ', '') for b in bands)))
    for t, d in S['nd'].items():
        P('  %-9s %s' % (t, ' '.join('%+10.2f%%' % (100 * d[b]['apprec01']) if b in d else '%11s' % '-' for b in bands)))
BN = jload('BANDS_R.json')
if BN:
    P('\n-- YEAR-1 APPRECIATION, MODERN WINDOW (ALLCOH) --')
    bands = ['ALL picks 1-64', 'picks 1-20', 'picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
    P('  %-9s %s' % ('board', ' '.join('%11s' % b.replace('picks ', '') for b in bands)))
    for t, d in BN['nd'].items():
        row = []
        for b in bands:
            k = 'MODERN|ALLCOH|' + b
            row.append('%+10.2f%%' % (100 * d[k]['apprec01']) if k in d else '%11s' % '-')
        P('  %-9s %s' % (t, ' '.join(row)))
PT = jload('PATHTEST_R.json')
if PT:
    P('\n-- THE OWNER\'S PATH TEST --')
    cs = PT['cells']
    P('  breaching cells %d · PASS %d · FAIL %d'
      % (len(cs), sum(1 for c in cs if c['passes']), sum(1 for c in cs if not c['passes'])))
    seen = collections.Counter()
    for c in cs:
        seen[(c['band'], c['passes'])] += 1
    for (b, ok), n in sorted(seen.items()):
        P('    %-30s %-6s on %d board(s)' % (b, 'PASS' if ok else 'FAIL', n))
A = jload('ARC_R.json')
if A:
    P('\n-- WHOLE-ARC MOVERS --')
    s = A['summary']
    P('  spanning variant: %s' % s['span'])
    for k, e in s['steps'].items():
        P('  %-8s %-52s up %3d down %3d flat %3d null %2d net %+8d | rank up %3d down %3d'
          % (k, e['name'], e['up'], e['down'], e['flat'], e['null'], e['net'], e['rank_up'], e['rank_down']))
open(os.path.join(HERE, 'DIGEST_R_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote DIGEST_R_out.txt')
