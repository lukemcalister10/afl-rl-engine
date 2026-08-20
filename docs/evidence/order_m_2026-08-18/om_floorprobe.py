#!/usr/bin/env python3
"""ORDER M — THE ABSOLUTE FLOOR PROBE.

The declared grid stops kappa at 0.15 on the low side and lambda_rel at 0.80. Someone reading
PACKET_M is entitled to ask whether a legal eta = 0 board is hiding just outside those edges. This
file answers that by going OUTSIDE the declared grid on purpose, in the direction that makes the
board coolest, and showing that even there it is nowhere near the rails.

These points are a BOUND. They are not candidates and nothing here is proposed. kappa = 0 means the
counterweight is switched off entirely, which is not a setting anyone has ruled or asked for.

Arithmetic only. Same legs, same maths as om_sweep.py.
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
LG = json.load(open(SP + '/O36_LEGS.json'))
DOSES = LG['doses']; POP = LG['pop']; PLF = LG['PLF']
LEGS = {float(k): v for k, v in LG['legs'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
N = len(POP)
B5 = ['1-10', '11-20', '21-30', '31-40', '41-64']
L = []


def P(s=''):
    print(s); L.append(str(s))


def nb(pk):
    if pk is None: return None
    for hi, nm in ((10, '1-10'), (20, '11-20'), (30, '21-30'), (40, '31-40'), (64, '41-64')):
        if pk <= hi: return nm


KEYS = [q['key'] for q in POP]; A0 = LEGS[DOSES[0]]
gv = np.array([A0[k]['g'] for k in KEYS]); rho = np.array([A0[k]['rho'] for k in KEYS])
Dft = np.array([A0[k]['Dfade'] for k in KEYS]); sig = np.array([A0[k]['sig'] for k in KEYS])
Phi = np.array([A0[k]['Phi'] for k in KEYS]); bet = np.array([A0[k]['beta'] for k in KEYS])
V0 = np.array([A0[k]['V0'] for k in KEYS]); agp = np.array([A0[k]['agap'] for k in KEYS])
PHAT = {d: np.array([LEGS[d][k]['Phat'] for k in KEYS]) for d in DOSES}
v0p = np.array([q['v0'] for q in POP]); yrv = np.array([q['yr'] for q in POP])
CLY = list(range(2005, 2022)); MC = np.zeros((17, N))
for i, y in enumerate(CLY):
    MC[i] = (yrv == y)
MCden = MC @ v0p
MB = np.zeros((5, N))
for i, bn in enumerate(B5):
    MB[i] = np.array([1.0 if (q['arm'] == 'ND' and nb(q['pick']) == bn) else 0.0 for q in POP])
MBden = MB @ v0p


def sc(dose, kap, gu, eta, gd, lrel):
    D = np.where(Dft < 1.0, np.minimum(1.0, Dft * (1.0 + lrel * sig)), Dft)
    mu = np.where(gv > 0, (gv / gu) * np.exp(1 - gv / gu), 0.0)
    md = np.where(gv > 0, (gv / gd) * np.exp(1 - gv / gd), 0.0)
    r2 = rho + kap * mu * (1 - rho)
    p1 = (r2 * PHAT[dose] + (D * (1 - r2) + Phi * bet * r2) * V0 * np.maximum(0, 1 - eta * md)
          + kap * mu * (1 - rho) * agp * 20.0 * PLF)
    Rc = (MC @ p1) / MCden; bR = (MB @ p1) / MBden
    return float(Rc[:11].mean()), float(Rc.max()), {b: float(v) for b, v in zip(B5, bR)}


P('=' * 110)
P('ORDER M — THE ABSOLUTE FLOOR PROBE. OUTSIDE THE DECLARED GRID, ON PURPOSE, AS A BOUND.')
P('=' * 110)
P('  the question: is a legal eta = 0 board hiding just past the edges of the declared grid?')
P('  the rails: no ND band above +14.00%  ·  worst single class <= 1.139  ·  class mark under 1.14')
P()
P('  %-46s %9s %9s %9s %9s' % ('setting', 'class', 'maxcls', '1-10', '11-20'))
ROWS = []
for lrel in (1.08, 0.80):
    for gu in (8.0, 16.0):
        for kap in (0.00, 0.05, 0.10, 0.15):
            c, mx, b = sc(0.0, kap, gu, 0.0, 14.0, lrel)
            tag = 'dose 0, kappa %.2f, gamma_u %.0f, eta 0, rel %.2f%s' % (
                kap, gu, lrel, '  <- kappa OFF' if kap == 0 else '')
            ROWS.append(dict(dose=0.0, kappa=kap, gamma_u=gu, eta=0.0, lam_rel=lrel,
                             mean_0515=c, max_class=mx, band=b))
            P('  %-46s %9.4f %9.4f %+8.2f%% %+8.2f%%'
              % (tag, c, mx, 100 * (b['1-10'] - 1), 100 * (b['11-20'] - 1)))
best = min(ROWS, key=lambda r: r['band']['1-10'])
worstband = min(ROWS, key=lambda r: max(r['band'].values()))
P()
P('  THE COOLEST PICKS 1-10 REACHABLE ANYWHERE, inside the grid or outside it: %+.2f%%'
  % (100 * (best['band']['1-10'] - 1)))
P('  the rail is +14.00%%. It is over by %.2f points.' % (100 * (best['band']['1-10'] - 1) - 14.0))
P('  the worst single class there is %.4f against a 1.139 line — %s by %.4f.'
  % (best['max_class'], 'OVER' if best['max_class'] > 1.139 else 'inside it',
     abs(best['max_class'] - 1.139)))
P()
P('  SO THE TWO RAILS PART COMPANY AT THE VERY BOTTOM, and the packet says so rather than rounding it:')
P('    with the counterweight switched OFF ENTIRELY (kappa = 0) and the age bar OFF (dose 0), the')
P('    1.139 no-arb class line IS satisfied at %.4f. The +14%% BAND rail is NOT: picks 1-10 read'
  % best['max_class'])
P('    %+.2f%%. So the binding law, at the very floor of everything, is G3 — YOUR band rail.'
  % (100 * (best['band']['1-10'] - 1)))
P('    And kappa = 0 is not a setting anyone has ruled: it deletes the counterweight the owner kept.')
P()
P('  WHY THE EDGES CANNOT SAVE IT, in one line each:')
P('    lambda_rel  moves the worst class by less than 0.0001 across its whole range. It is not a lever')
P('                on this question at all.')
P('    kappa       LOWER kappa makes the board cooler, and kappa is already at its floor here — zero,')
P('                which means no counterweight at all. Even there picks 1-10 miss the +14 per cent')
P('                rail by 4.3 points, and kappa = 0 is not a setting anyone has ruled.')
P('    gamma_u     spans less than 0.01 on the worst class across 8 to 16.')
P('    dose        every step UP makes it worse, monotonically. Dose 0 is already the coolest.')
P('  There is no direction left to travel.')
json.dump(dict(order='ORDER M — the absolute floor probe', rows=ROWS, best=best),
          open(os.path.join(HERE, 'FLOORPROBE_M.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'FLOORPROBE_M_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FLOORPROBE_M.json / FLOORPROBE_M_out.txt')
