#!/usr/bin/env python3
"""ORDER M — THE TRADE-OFF LADDER, READ IN BOARD POINTS.

Pure JSON reads over the boards build_allM.sh and build_ladderM.sh already wrote. No engine run.

LADDER A — eta walked from 0.00 to 0.50 at ORDER K's RULED DOSE 0.40, every other knob held.
           The question: is there an eta that puts harry-dean near 2,600 AND holds the three G6 rows
           at or below their landing values AND keeps the board legal?

LADDER B — the LEGAL FRONTIER: at each dose, the smallest eta the board can carry (TRADEOFF_M.json
           Q1). The question: over the whole frontier, what is the best harry-dean the owner can buy?
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OM = SP + '/om'
TD = json.load(open(os.path.join(HERE, 'TRADEOFF_M.json')))
Q1 = {round(r['dose'], 2): r for r in TD['q1_min_eta_by_dose']}
W3 = {r['eta']: r for r in TD['q3_walk_dose040']}

LADDER_A = [('M0', 0.40, 0.00), ('E10', 0.40, 0.10), ('E20', 0.40, 0.20), ('E30', 0.40, 0.30),
            ('E40', 0.40, 0.40), ('K', 0.40, 0.50)]
LADDER_B = [('MLO', 0.00, 0.00), ('MMIN', 0.00, 0.31), ('F20', 0.20, 0.39), ('K', 0.40, 0.50),
            ('F60', 0.60, 0.64), ('F70', 0.70, 0.72)]
TAGS = sorted({t for t, _, _ in LADDER_A + LADDER_B} | {'cand'})
BP = {t: OM + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
V = {t: {r['key']: r['v'] for r in json.load(open(BP[t]))['active']} for t in TAGS}
AGE = {k: r['age'] for k, r in
       {r['key']: r for r in json.load(open(BP['cand']))['active']}.items()}
MAT = [k for k in V['cand'] if AGE[k] >= 24]
BOARD = sum(V['cand'].values())
ROWS = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
        'isaac-kako', 'josh-smillie']
L = []


def P(s=''):
    print(s); L.append(str(s))


def jtol(t):
    mv = [(k, V[t][k] - V['cand'][k]) for k in MAT if V[t][k] != V['cand'][k]]
    return sum(abs(d) for _, d in mv), sum(d for _, d in mv)


P('=' * 128)
P('ORDER M — THE TRADE-OFF LADDER, IN BOARD POINTS')
P('=' * 128)
P('  landing candidate 1f176444 is the base every column is compared to.')
P('  harry-dean lands there at %d; the owner wants ~2,600.  cooper-duff-tytler %d; the owner wants ~1,800.'
  % (V['cand']['harry-dean'], V['cand']['cooper-duff-tytler']))
P('  the three G6 rows land at xavier-taylor %d, daniel-annable %d, dylan-patterson %d, and the law is'
  % (V['cand']['xavier-taylor'], V['cand']['daniel-annable'], V['cand']['dylan-patterson']))
P('  that none of them may go UP.')

OUT = {'ladderA': [], 'ladderB': []}
for nm, LAD, title, note in (
        ('ladderA', LADDER_A, 'LADDER A — ETA WALKED AT THE RULED DOSE 0.40 (every other knob held)',
         'the navigation instrument says the smallest LEGAL eta at dose 0.40 is 0.50 — the row at the '
         'bottom.'),
        ('ladderB', LADDER_B, 'LADDER B — THE LEGAL FRONTIER: the SMALLEST eta each dose can carry',
         'every row except the first is the CHEAPEST legal eta at that dose. the first row is dose 0 '
         'with NO eta at all, and it is illegal — it is there as the far end of the curve.')):
    P()
    P('=' * 128)
    P(title)
    P('=' * 128)
    P('  ' + note)
    P()
    P('  %-4s %5s %5s | %8s %8s | %8s %8s %8s | %9s %8s | %8s'
      % ('tag', 'dose', 'eta', 'dean', 'CDT', 'x-tayl', 'annable', 'patters', 'nav class', 'nav 1-10',
         'vet net'))
    P('  %-4s %5s %5s | %8s %8s | %8s %8s %8s | %9s %8s | %8s'
      % ('', '', '', '~2600', '~1800', 'no rise', 'no rise', 'no rise', '<1.14', '<=+14%', '<=668'))
    P('  ' + '-' * 122)
    P('  %-4s %5s %5s | %8d %8d | %8d %8d %8d | %9s %8s | %8s'
      % ('base', '-', '-', V['cand']['harry-dean'], V['cand']['cooper-duff-tytler'],
         V['cand']['xavier-taylor'], V['cand']['daniel-annable'], V['cand']['dylan-patterson'],
         '1.0421', '+7.20%', '0'))
    for tag, dose, eta in LAD:
        ch, net = jtol(tag)
        nav = W3.get(eta) if abs(dose - 0.40) < 1e-9 else None
        navc = ('%.4f' % nav['mean_0515']) if nav else (
            '%.4f' % Q1[round(dose, 2)]['at']['mean_0515'] if (Q1.get(round(dose, 2)) and
                                                               Q1[round(dose, 2)]['at'] and
                                                               abs(Q1[round(dose, 2)]['eta_both'] - eta) < 1e-9)
            else '-')
        nav110 = ('%+.2f%%' % (100 * (nav['band']['1-10'] - 1))) if nav else (
            '%+.2f%%' % (100 * (Q1[round(dose, 2)]['at']['band']['1-10'] - 1))
            if (Q1.get(round(dose, 2)) and Q1[round(dose, 2)]['at'] and
                abs(Q1[round(dose, 2)]['eta_both'] - eta) < 1e-9) else '-')
        rec = dict(tag=tag, dose=dose, eta=eta, md5=MD5[tag][:8],
                   dean=V[tag]['harry-dean'], cdt=V[tag]['cooper-duff-tytler'],
                   xavier=V[tag]['xavier-taylor'], annable=V[tag]['daniel-annable'],
                   patterson=V[tag]['dylan-patterson'], kako=V[tag]['isaac-kako'],
                   smillie=V[tag]['josh-smillie'],
                   vet_churn=ch, vet_net=net, nav_class=navc, nav_110=nav110,
                   total=sum(V[tag].values()))
        OUT[nm].append(rec)
        g6 = sum(1 for k in ('xavier-taylor', 'daniel-annable', 'dylan-patterson')
                 if V[tag][k] > V['cand'][k])
        P('  %-4s %5.2f %5.2f | %8d %8d | %8d %8d %8d | %9s %8s | %+8d   %s'
          % (tag, dose, eta, rec['dean'], rec['cdt'], rec['xavier'], rec['annable'],
             rec['patterson'], navc, nav110, net,
             'G6: %d of 3 rise' % g6 if g6 else 'G6 holds'))

P()
P('=' * 128)
P('WHAT THE LADDER SAYS, IN ONE PLACE')
P('=' * 128)
A = OUT['ladderA']
cross_dean = [r for r in A if r['dean'] >= 2600]
hold_g6 = [r for r in A if r['xavier'] <= V['cand']['xavier-taylor']
           and r['annable'] <= V['cand']['daniel-annable']
           and r['patterson'] <= V['cand']['dylan-patterson']]
P('  At the ruled dose 0.40:')
P('    harry-dean reaches the owner\'s ~2,600 at eta <= %s'
  % (max(r['eta'] for r in cross_dean) if cross_dean else 'no eta on the ladder'))
P('    all three G6 rows hold at eta >= %s'
  % (min(r['eta'] for r in hold_g6) if hold_g6 else 'no eta on the ladder'))
P('    the board is legal at eta >= 0.50 (the navigation curve, Q1)')
if cross_dean and hold_g6:
    lo = min(r['eta'] for r in hold_g6); hi = max(r['eta'] for r in cross_dean)
    P('    -> the dean window and the G6 window %s'
      % ('OVERLAP at eta in [%.2f, %.2f]' % (lo, hi) if lo <= hi else
         'DO NOT OVERLAP: G6 needs eta >= %.2f, dean needs eta <= %.2f' % (lo, hi)))
B = OUT['ladderB']
best = max(B, key=lambda r: r['dean'])
legal = [r for r in B if r['eta'] > 0]
bestlegal = max(legal, key=lambda r: r['dean'])
P()
P('  Over the whole LEGAL FRONTIER (ladder B, every row a cheapest-legal-eta point):')
P('    the best harry-dean available is %d, at dose %.2f / eta %.2f  (tag %s)'
  % (bestlegal['dean'], bestlegal['dose'], bestlegal['eta'], bestlegal['tag']))
P('    the owner wants ~2,600. The frontier is short of it by %d points.' % (2600 - bestlegal['dean']))
P('    the best cooper-duff-tytler available is %d, against ~1,800 — short by %d.'
  % (max(r['cdt'] for r in legal), 1800 - max(r['cdt'] for r in legal)))
illegal = [r for r in B if r['eta'] == 0]
if illegal:
    P('    the ILLEGAL far end (dose 0, no eta at all) buys dean %d and CDT %d.'
      % (illegal[0]['dean'], illegal[0]['cdt']))
P('    That gap is the trade the owner is being asked to make, and it is priced here rather than argued.')
json.dump(OUT, open(os.path.join(HERE, 'LADDER_M.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'LADDER_M_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: LADDER_M.json / LADDER_M_out.txt')
