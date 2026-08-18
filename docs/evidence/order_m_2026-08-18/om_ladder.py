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
# the MAXIMUM-KAPPA control: kappa as hard as rho32 monotonicity permits (0.60 at gamma_u 16), with
# eta at zero, at dose 0 and at the ruled dose 0.40. This is the built test of the packet's claim that
# kappa alone cannot charge the sub-expectation rows.
KMAXTAGS = [('KMAX', 0.00, 0.00), ('KMX4', 0.40, 0.00)]
TAGS = sorted({t for t, _, _ in LADDER_A + LADDER_B + KMAXTAGS} | {'cand'})
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
A = sorted(OUT['ladderA'], key=lambda r: r['eta'])


def cross(field, target, falling=True):
    """the eta at which `field` crosses `target`, by linear interpolation between built boards.
    Every row on this ladder is a REAL BOARD; only the crossing point between two of them is
    interpolated, and it is labelled as such wherever it is printed."""
    for a, b in zip(A, A[1:]):
        va, vb = a[field], b[field]
        if (va >= target >= vb) or (va <= target <= vb):
            if va == vb:
                return a['eta']
            return a['eta'] + (b['eta'] - a['eta']) * (va - target) / (va - vb)
    return None


P('  At the RULED DOSE 0.40, every knob but eta held. Crossings are interpolated between built boards.')
P()
ED = cross('dean', 2600)
EC = cross('cdt', 1800)
EX = cross('xavier', V['cand']['xavier-taylor'])
EA = cross('annable', V['cand']['daniel-annable'])
EP = cross('patterson', V['cand']['dylan-patterson'])
P('    harry-dean reaches ~2,600           at eta = %s   -> he needs eta AT OR BELOW this'
  % ('%.2f' % ED if ED is not None else 'not on the ladder'))
P('    cooper-duff-tytler reaches ~1,800   at eta = %s   -> he needs eta AT OR BELOW this'
  % ('%.2f' % EC if EC is not None else 'not on the ladder'))
P('    xavier-taylor stops rising          at eta = %s   -> G6 needs eta AT OR ABOVE this'
  % ('%.2f' % EX if EX is not None else 'not reached even at eta 0.50'))
P('    daniel-annable stops rising         at eta = %s   -> G6 needs eta AT OR ABOVE this'
  % ('%.2f' % EA if EA is not None else 'NOT REACHED even at eta 0.50 — this is ORDER K\'s own +7 breach'))
P('    dylan-patterson stops rising        at eta = %s   -> G6 needs eta AT OR ABOVE this'
  % ('%.2f' % EP if EP is not None else 'not reached even at eta 0.50'))
P('    the BOARD IS LEGAL                  at eta = 0.50 and above  (TRADEOFF_M.json Q1, dose 0.40)')
P()
need_lo = max([x for x in (EX, EA, EP) if x is not None] + [0.50])
want_hi = min([x for x in (ED, EC) if x is not None] or [0.0])
P('    THE TWO WINDOWS:')
P('      to satisfy G5 (the owner\'s two rows) eta must be at or below   %.2f' % want_hi)
P('      to satisfy G6 and the board\'s own rails eta must be at least   %.2f' % need_lo)
if want_hi < need_lo:
    P('      -> THEY DO NOT OVERLAP. The gap is %.2f of eta. There is no setting of eta at the ruled'
      % (need_lo - want_hi))
    P('         dose that gives the owner both. This is the finding, and it is not a near miss.')
else:
    P('      -> they overlap at eta in [%.2f, %.2f]' % (need_lo, want_hi))
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
# ---- the maximum-kappa control ---------------------------------------------------------------------
P()
P('=' * 128)
P('THE MAXIMUM-KAPPA CONTROL — can kappa charge the sub-expectation rows once eta is gone?')
P('=' * 128)
P('  kappa 0.60 with gamma_u 16 is the HARDEST kappa the ruled rho32-monotonicity constraint admits')
P('  anywhere on the declared grid. It is three times ORDER K\'s 0.20. eta is at zero on both rows.')
P()
P('  %-6s %5s %6s %5s | %8s %8s %8s | %8s %8s'
  % ('tag', 'dose', 'kappa', 'eta', 'x-tayl', 'annable', 'patters', 'dean', 'CDT'))
P('  %-6s %5s %6s %5s | %8d %8d %8d | %8d %8d'
  % ('base', '-', '-', '-', V['cand']['xavier-taylor'], V['cand']['daniel-annable'],
     V['cand']['dylan-patterson'], V['cand']['harry-dean'], V['cand']['cooper-duff-tytler']))
KM = []
for tag, dose, eta in KMAXTAGS:
    g6 = sum(1 for k in ('xavier-taylor', 'daniel-annable', 'dylan-patterson')
             if V[tag][k] > V['cand'][k])
    KM.append(dict(tag=tag, dose=dose, kappa=0.60, gamma_u=16.0, eta=eta, md5=MD5[tag][:8],
                   xavier=V[tag]['xavier-taylor'], annable=V[tag]['daniel-annable'],
                   patterson=V[tag]['dylan-patterson'], dean=V[tag]['harry-dean'],
                   cdt=V[tag]['cooper-duff-tytler'], g6_rising=g6))
    P('  %-6s %5.2f %6.2f %5.2f | %8d %8d %8d | %8d %8d   %s'
      % (tag, dose, 0.60, eta, V[tag]['xavier-taylor'], V[tag]['daniel-annable'],
         V[tag]['dylan-patterson'], V[tag]['harry-dean'], V[tag]['cooper-duff-tytler'],
         'G6: %d of 3 STILL RISE' % g6 if g6 else 'G6 holds'))
OUT['kappa_max'] = KM
P()
P('  -> %s'
  % ('KAPPA CANNOT CHARGE THEM. At the hardest kappa the ruled constraints allow, with eta at zero, '
     'the sub-expectation rows still rise above their landing values.'
     if any(r['g6_rising'] for r in KM) else
     'kappa DOES hold them at its hardest setting — the packet must be corrected.'))
P('     The reason is structural. Kappa moves weight BETWEEN two legs — off pedigree, onto shown')
P('     production. Eta charged one leg DOWN. Those are different operations. Kappa can tilt the')
P('     balance; only eta could subtract value from the row.')

json.dump(OUT, open(os.path.join(HERE, 'LADDER_M.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'LADDER_M_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: LADDER_M.json / LADDER_M_out.txt')
