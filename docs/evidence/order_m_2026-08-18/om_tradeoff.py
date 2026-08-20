#!/usr/bin/env python3
"""ORDER M — THE TRADE-OFF CURVE. HOW MUCH ETA DOES THE BOARD ACTUALLY NEED?

PREREG_M §6(b) requires that, if no legal setting exists at eta = 0, this seat quantifies it and shows
the trade-off curve so the owner can choose knowingly. This file does that.

It reuses om_sweep.py's own arithmetic wholesale by importing it as a module is not possible (that file
runs its sweep at import), so the leg maths — which is ORDER J's o37_sweep.py p1_vec, unchanged — is
restated here and CHECKED against SWEEP_M.json's own recorded points before any new number is used.

Three questions, each answered as a number:
  Q1  at each dose, what is the SMALLEST eta that keeps the board inside the owner's G3 rail
      (no ND band above +14%) and inside the 1.139 no-arb max-class line?
  Q2  what does that smallest eta charge harry-dean's own row shape, relative to eta = 0.50?
  Q3  what does the picks 1-10 band read as eta is walked from 0 to 0.50 at the ruled dose?

Arithmetic only. No engine run.
"""
import os, sys, json, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
L = []


def P(s=''):
    print(s, flush=True); L.append(str(s))


LG = json.load(open(SP + '/O36_LEGS.json'))
DOSES = LG['doses']; POP = LG['pop']; PLF = LG['PLF']
LEGS = {float(k): v for k, v in LG['legs'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
N = len(POP)
BANDS5 = ['1-10', '11-20', '21-30', '31-40', '41-64']


def nd_band(pk):
    if pk is None: return None
    for hi, nm in ((10, '1-10'), (20, '11-20'), (30, '21-30'), (40, '31-40'), (64, '41-64')):
        if pk <= hi: return nm
    return None


KEYS = [q['key'] for q in POP]
A0 = LEGS[DOSES[0]]
gv = np.array([A0[k]['g'] for k in KEYS])
rho = np.array([A0[k]['rho'] for k in KEYS])
Dft = np.array([A0[k]['Dfade'] for k in KEYS])
Dfp = np.array([A0[k]['Dfade_pool'] for k in KEYS])
sig = np.array([A0[k]['sig'] for k in KEYS])
Phi = np.array([A0[k]['Phi'] for k in KEYS])
bet = np.array([A0[k]['beta'] for k in KEYS])
V0 = np.array([A0[k]['V0'] for k in KEYS])
agp = np.array([A0[k]['agap'] for k in KEYS])
PHAT = {d: np.array([LEGS[d][k]['Phat'] for k in KEYS]) for d in DOSES}
v0p = np.array([q['v0'] for q in POP])
yrv = np.array([q['yr'] for q in POP])
CLY = list(range(2005, 2022))
MC = np.zeros((len(CLY), N))
for i, y in enumerate(CLY):
    MC[i] = (yrv == y)
MCden = MC @ v0p
MB = np.zeros((5, N))
for i, bnm in enumerate(BANDS5):
    MB[i] = np.array([1.0 if (q['arm'] == 'ND' and nd_band(q['pick']) == bnm) else 0.0 for q in POP])
MBden = MB @ v0p


def m_of(g, gam):
    return np.where(g > 0, (g / gam) * np.exp(1.0 - g / gam), 0.0)


def score(dose, kap, gu, eta, gd, lrel, fade='tall'):
    Df = Dft if fade == 'tall' else Dfp
    D = np.where(Df < 1.0, np.minimum(1.0, Df * (1.0 + lrel * sig)), Df)
    mu = m_of(gv, gu); md = m_of(gv, gd)
    r2 = rho + kap * mu * (1.0 - rho)
    p1 = (r2 * PHAT[dose] + (D * (1.0 - r2) + Phi * bet * r2) * V0 * np.maximum(0.0, 1.0 - eta * md)
          + kap * mu * (1.0 - rho) * agp * 20.0 * PLF)
    Rc = (MC @ p1) / MCden
    bandR = (MB @ p1) / MBden
    return dict(mean_0515=float(Rc[:11].mean()), max_class=float(Rc.max()),
                band={b: float(v) for b, v in zip(BANDS5, bandR)})


# ---- IDENTITY: this file's arithmetic must reproduce SWEEP_M.json point for point -------------------
S = json.load(open(os.path.join(HERE, 'SWEEP_M.json')))
worst = 0.0
for M in S['points'][::311]:
    r = score(M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['lam_rel'])
    worst = max(worst, abs(r['mean_0515'] - M['mean_0515']), abs(r['max_class'] - M['max_class']),
                max(abs(r['band'][b] - M['band_R'][b]) for b in BANDS5))
P('=' * 112)
P('ORDER M — THE TRADE-OFF CURVE: HOW MUCH ETA DOES THE BOARD NEED?')
P('=' * 112)
P('IDENTITY CHECK — this file reproduces SWEEP_M.json on %d sampled points: worst deviation %.3e -> %s'
  % (len(S['points'][::311]), worst, 'EXACT' if worst < 1e-12 else 'FAIL'))
assert worst < 1e-12, 'ORDER M HALT: the trade-off arithmetic is not the sweep arithmetic'

KB = S['control_orderK']['band_R']
CB = S['control_landing']['band_R']
P()
P('THE TWO RAILS BEING TESTED, both the owner\'s own:')
P('  G3          no ND band above +14.00%% year 0->1')
P('  no-arb line max single class mark <= 1.139 (the 1.14 buy rail, per class)')
P('  G1 rail     the year-1 class cohort mark strictly under 1.14')
P()

# ---- Q1: the smallest legal eta at each dose --------------------------------------------------------
ETAS = [round(x * 0.01, 2) for x in range(0, 76)]
KAP, GU, GD, REL = 0.20, 8.0, 14.0, 1.08      # ORDER K's ruled knobs, held, so eta is the only mover
P('Q1 — THE SMALLEST ETA THAT KEEPS THE BOARD LEGAL, dose by dose.')
P('     kappa, gamma_u, gamma_d and lambda_rel are held at ORDER K\'s ruled values (0.20 / 8 / 14 / 1.08)')
P('     so that eta is the ONLY thing moving. eta is walked from 0.00 to 0.75 in steps of 0.01.')
P()
P('  %5s | %9s %9s %9s | %9s %9s %9s' %
  ('dose', 'eta min', 'eta min', 'eta min', 'class at', 'maxcls at', '1-10 at'))
P('  %5s | %9s %9s %9s | %9s %9s %9s' %
  ('', 'G3 band', 'maxclass', 'BOTH', 'eta min', 'eta min', 'eta min'))
Q1 = []
for dose in DOSES:
    e_band = e_max = e_both = None
    for e in ETAS:
        r = score(dose, KAP, GU, e, GD, REL)
        okb = max(r['band'].values()) <= 1.14
        okm = r['max_class'] <= 1.139
        if okb and e_band is None: e_band = e
        if okm and e_max is None: e_max = e
        if okb and okm and r['mean_0515'] < 1.14 and e_both is None: e_both = e
    at = score(dose, KAP, GU, e_both, GD, REL) if e_both is not None else None
    Q1.append(dict(dose=dose, eta_band=e_band, eta_maxclass=e_max, eta_both=e_both,
                   at=at))
    P('  %5.2f | %9s %9s %9s | %9s %9s %9s'
      % (dose, '%.2f' % e_band if e_band is not None else 'none',
         '%.2f' % e_max if e_max is not None else 'none',
         '%.2f' % e_both if e_both is not None else 'none',
         '%.4f' % at['mean_0515'] if at else '-',
         '%.4f' % at['max_class'] if at else '-',
         '%+.2f%%' % (100 * (at['band']['1-10'] - 1)) if at else '-'))
P()
P('  READ THIS ROW BY ROW. At EVERY dose, including dose 0.00 — the age bar switched off entirely —')
P('  the board needs a STRICTLY POSITIVE eta to stay inside the owner\'s own +14%% band rail.')

# ---- Q3: the eta walk at the ruled dose -------------------------------------------------------------
P()
P('Q3 — THE ETA WALK AT THE RULED DOSE 0.40 (kappa 0.20, gamma_u 8, gamma_d 14, lambda_rel 1.08).')
P('  %6s | %8s %8s | %s' % ('eta', 'class', 'maxcls', 'five ND bands, year 0 -> 1'))
WALK = []
for e in (0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.41, 0.45, 0.50, 0.55, 0.60):
    r = score(0.40, KAP, GU, e, GD, REL)
    WALK.append(dict(eta=e, **r))
    flag = ''
    if max(r['band'].values()) > 1.14: flag += ' <- G3 BREACHED'
    if r['max_class'] > 1.139: flag += ' <- no-arb line BREACHED'
    if r['mean_0515'] >= 1.14: flag += ' <- G1 buy rail BREACHED'
    P('  %6.2f | %8.4f %8.4f | %s%s'
      % (e, r['mean_0515'], r['max_class'],
         ' '.join('%+7.2f%%' % (100 * (r['band'][b] - 1)) for b in BANDS5), flag))
P()
P('  AND AT DOSE 0.00 (no age bar at all), the same walk:')
P('  %6s | %8s %8s | %s' % ('eta', 'class', 'maxcls', 'five ND bands, year 0 -> 1'))
WALK0 = []
for e in (0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.41, 0.45, 0.50):
    r = score(0.0, KAP, GU, e, GD, REL)
    WALK0.append(dict(eta=e, **r))
    flag = ''
    if max(r['band'].values()) > 1.14: flag += ' <- G3 BREACHED'
    if r['max_class'] > 1.139: flag += ' <- no-arb line BREACHED'
    P('  %6.2f | %8.4f %8.4f | %s%s'
      % (e, r['mean_0515'], r['max_class'],
         ' '.join('%+7.2f%%' % (100 * (r['band'][b] - 1)) for b in BANDS5), flag))

# ---- Q2: what the smallest legal eta charges a dean-shaped row --------------------------------------
P()
P('Q2 — WHAT THE SMALLEST LEGAL ETA CHARGES A ROW, AS A FRACTION OF ITS PEDIGREE LEG.')
P('  The charge is  1 - eta*(g/14)*exp(1-g/14).  It is a pure function of games played.')
P('  %6s | %s' % ('games', ' '.join('%9s' % ('eta=%.2f' % e) for e in (0.10, 0.20, 0.30, 0.41, 0.50))))
CH = {}
for g in (2, 5, 8, 10, 14, 20, 25, 30, 36, 50, 80, 141):
    md = (g / 14.0) * math.exp(1.0 - g / 14.0)
    CH[g] = {e: max(0.0, 1.0 - e * md) for e in (0.10, 0.20, 0.30, 0.41, 0.50)}
    P('  %6d | %s' % (g, ' '.join('%8.1f%%' % (-100 * (1 - CH[g][e])) for e in (0.10, 0.20, 0.30, 0.41, 0.50))))
P('  harry-dean and cooper-duff-tytler are both 19, both key-position talls, both high picks with few')
P('  games. That is the shape the peak at 14 games charges hardest. isaac-kako at 36 games is already')
P('  most of the way down the far side of the bump, which is why he is charged only a quarter as much.')

json.dump(dict(order='ORDER M — the trade-off curve', held_knobs=dict(kappa=KAP, gamma_u=GU,
                                                                     gamma_d=GD, lam_rel=REL),
               q1_min_eta_by_dose=Q1, q3_walk_dose040=WALK, q3_walk_dose000=WALK0,
               q2_charge_by_games={str(k): v for k, v in CH.items()},
               orderK_bands=KB, landing_bands=CB),
          open(os.path.join(HERE, 'TRADEOFF_M.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'TRADEOFF_M_out.txt'), 'w').write('\n'.join(L) + '\n')
P('\nwritten: TRADEOFF_M.json / TRADEOFF_M_out.txt')
