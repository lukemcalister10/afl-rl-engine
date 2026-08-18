#!/usr/bin/env python3
"""ORDER N — the comparison tables the packet prints: bands in BOTH windows, the veteran caps, the
named rows against the landing candidate. Reads BANDS_N.json and the ledger. READ-ONLY.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

PL_F = 1.0524
L = []


def P(s=''):
    print(s); L.append(str(s))


B = json.load(open(os.path.join(HERE, 'BANDS_N.json')))
M = json.load(open(os.path.join(HERE, 'MECH_N.json')))
BOARDS = ['NDERIV', 'OKRULED', 'O35FINAL', 'M0ETA0', 'MMIN031', 'O31FFINAL']
NICE = {'NDERIV': 'ORDER N', 'OKRULED': 'ORDER K', 'O35FINAL': 'landing', 'M0ETA0': 'eta=0',
        'MMIN031': 'dose0 e.31', 'O31FFINAL': 'cand 31'}
BANDNAMES = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
             'picks 21-30', 'picks 31-40', 'picks 41-64']

P('=' * 118)
P('ORDER N — THE STANDING TABLES ON THE DERIVED CHARGE. ESTIMATE PENDING A BUILD.')
P('=' * 118)
P('mechanism: pi *= exp( -%.5f * (1 - exp(-g/%.4f)) * clip(1 - %.5f*(s %+0.4f), 0, %.4f) )'
  % (M['LAMBDA'], M['G0'], M['THETA_R'], -M['s0'], M['TMAX']))
P()

for win in ('PRIMARY', 'MODERN'):
    P('-' * 118)
    P('%s window — year-0 -> year-1 appreciation. Below 0%% is a sell-side red. Above +14%% is a buy-side red.' % win)
    P('-' * 118)
    P('  %-16s %5s | %11s %11s %11s %11s %11s %11s' % (
        'band', 'n', *[NICE[b] for b in BOARDS]))
    for bn in BANDNAMES:
        cells = []
        n = None
        for b in BOARDS:
            d = B['nd'][b]['%s|ALLCOH|%s' % (win, bn)]
            n = d['n']
            a = d['apprec01']
            v = d['verdict']
            tag = '' if v.startswith('ok') else ('B' if 'BUY' in v else 'S')
            cells.append('%+10.2f%%%s' % (100 * a, tag) if a is not None else '%11s' % '-')
        P('  %-16s %5d | %s' % (bn, n, ' '.join(cells)))
    P('  (B = buy-side red, over the +14%% rail.  S = sell-side red, below 0%%.)')
    P()

# ---- the veteran caps -------------------------------------------------------------------------------
P('-' * 118)
P('THE VETERAN POOL — J-TOL, on the same definition ORDER M used: ledger rows aged 24+, measured')
P('against the LANDING candidate, board total = the landing candidate\'s.')
P('-' * 118)
LED = LB.load_ledger()
MN = LB.load_matrix('NDERIV')
rows = []
for r in LED['rows']:
    k = r['key']
    if k not in MN or MN[k].get('cur') is None:
        continue
    rows.append(dict(key=k, name=r['name'], age=int(r['age']), landing=float(r['landing']),
                     orderk=float(r['orderk']), new=round(float(MN[k]['cur']) / PL_F)))
BOARD_TOTAL = sum(x['landing'] for x in rows)
MAT = [x for x in rows if x['age'] >= 24]
P('  board total (landing) = %d ;  mature rows aged 24+ = %d' % (round(BOARD_TOTAL), len(MAT)))
P('  rails: per row min(25, max(1, 0.5%% of his own price)) · churn <= %.2f (0.15%%) · net <= %.2f (0.10%%)'
  % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
P()
P('  %-12s %6s %8s %9s %8s %8s' % ('board', 'move', 'churn', 'net', 'worst', 'per-row breaches'))
JT = {}
for lab, fld in (('ORDER K', 'orderk'), ('ORDER N', 'new')):
    mv = [(x['key'], x[fld] - x['landing']) for x in MAT if x[fld] != x['landing']]
    churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    worst = max(mv, key=lambda t: abs(t[1]))[1] if mv else 0
    br = sum(1 for x in MAT if abs(x[fld] - x['landing']) > min(25.0, max(1.0, 0.005 * x['landing'])))
    P('  %-12s %6d %8d %+9d %+8d %8d   churn %s · net %s' % (
        lab, len(mv), churn, net, worst, br,
        'OK' if churn <= 0.0015 * BOARD_TOTAL else 'BREACH',
        'OK' if abs(net) <= 0.0010 * BOARD_TOTAL else 'BREACH'))
    JT[lab] = dict(move=len(mv), churn=churn, net=net, worst=worst, per_row_breaches=br)
P()
P('  ORDER M read the same three numbers on the eta = 0 board as churn 2923 / net +2781 / 105 breaches.')
P()

# ---- named rows against the landing candidate --------------------------------------------------------
P('-' * 118)
P('THE NAMED ROWS — against the landing candidate as well as ORDER K. ILLUSTRATIONS, NEVER TARGETS.')
P('-' * 118)
MK = LB.load_matrix('OKRULED')
byk = {r['key']: r for r in LED['rows']}
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie', 'anthony-scerri', 'milan-murdock']
P('  %-22s %3s %5s %5s %8s | %8s %8s %8s | %8s' % (
    'row', 'age', 'pick', 'g', 'surplus', 'landing', 'ORDER K', 'ORDER N', 'vs K'))
for k in NAMED:
    r = byk.get(k)
    if r is None:
        m = MK.get(k)
        P('  %-22s  NOT ON THE 804-ROW BOARD%s' % (
            k, ('' if m is None else '  (in the matrix: %s, draft %s, pick %s, %s games)'
                % (m.get('pos'), m.get('year'), m.get('pick'), m.get('games_total')))))
        continue
    m = MK.get(k)
    Y = max((s['year'] for s in m['seasons']), default=None)
    s = LB.perf_surplus(m, Y) if Y else None
    new = round(float(MN[k]['cur']) / PL_F)
    P('  %-22s %3d %5s %5.0f %8s | %8d %8d %8d | %+8d' % (
        r['name'][:22], r['age'], r['pick'], float(r['g'] or 0),
        ('%+.2f' % s) if s is not None else 'n/a (0 g)',
        round(r['landing']), round(r['orderk']), new, new - round(r['orderk'])))
P()

json.dump(dict(bands={w: {bn: {b: B['nd'][b]['%s|ALLCOH|%s' % (w, bn)]['apprec01'] for b in BOARDS}
                          for bn in BANDNAMES} for w in ('PRIMARY', 'MODERN')},
               jtol=JT, board_total_landing=BOARD_TOTAL),
          open(os.path.join(HERE, 'TABLES_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'TABLES_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote TABLES_N.json / TABLES_N_out.txt')
