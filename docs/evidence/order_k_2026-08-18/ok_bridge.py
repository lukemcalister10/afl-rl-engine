#!/usr/bin/env python3
"""ORDER K — THE CALIBRATOR BRIDGE.

Answers, on Order J's own calibrator legs and with no new maths:
  (1) which fade the REGION_J frontier rows were scored on — read off the sweep source, and
      PROVED here by reproducing the ruled row's numbers on each fade in turn;
  (2) what the same ruled setting reads once the FADE FLOOR IS FIXED.

Dfade      = D_raw ** kappa_TALL(pick, group)      (Order H wire, the defective floor)
Dfade_pool = D_raw ** kappa_POOLED(pick)           (Order D wire)
=> Dfade_fix = Dfade_pool ** ( kappa_FIX(pick, group) / kappa_POOLED(pick) )
which needs no D_raw and no engine.
"""
import os, sys, json, math, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

G0, G1, SN = 0.1286221202379088, 0.4535958546743124, 1.7472066252064105
TG0, TG1, HT = -0.8778138796894399, 0.7100022285392401, -0.6921227120657417
SN_WIRED = 1.4284052406915069
SN_FIX = json.load(open(SP + '/ok/FLOOR_DESIGN.json'))['s_norm_fix']
TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))


def kpool(p):
    p = max(1.0, min(64.0, float(p)))
    return min(2.0, max(0.5, (G0 + G1 * math.log(p)) / SN))


def kwired(p, tall):
    p = max(1.0, min(64.0, float(p)))
    return min(2.0, max(0.5, (TG0 + TG1 * math.log(p) + (HT if tall else 0.0)) / SN_WIRED))


def kfix(p, tall):
    p = max(1.0, min(64.0, float(p)))
    k = (TG0 + TG1 * math.log(p) + (HT if tall else 0.0)) / SN_FIX
    return min(2.0, max(0.5, k)) if tall else min(2.0, max(kpool(p), k))


# ---------- positions ----------
POS = {}
for f in ('per_entrant_O32RFINAL.json', 'per_entrant_O37TALL.json'):
    try:
        for r in json.load(open(SP + '/' + f))['recs']:
            POS.setdefault(r['key'], r.get('pos'))
    except Exception as e:
        print('  (no %s: %s)' % (f, e))

L = json.load(open(SP + '/O36_LEGS.json'))
DOSES = L['doses']; POP = L['pop']; PLF = L['PLF']
LEGS = {float(k): v for k, v in L['legs'].items()}
POP = [q for q in POP if q['key'] in LEGS[DOSES[0]]]
N = len(POP)
KEYS = [q['key'] for q in POP]
A0 = LEGS[DOSES[0]]
missing = [k for k in KEYS if POS.get(k) is None]
print('rows %d ; positions resolved %d ; missing %d' % (N, N - len(missing), len(missing)))

# ---------- the row's EFFECTIVE pick, recovered from the legs themselves ----------
# 50 of 1,986 rows carry an engine `_eff` that differs from the stored pick (the draft-order
# effective pick). Rather than guess it, it is RECOVERED: the only e in 1..64 for which
#   Dfade_pool ** ( kappa_TALLwired(e, group) / kappa_POOLED(e) )  ==  Dfade
# to 1e-12. Rows whose fade is 1.0 (never faded) are untouched by any exponent.
EFF = {}
unres = []
for q in POP:
    k = q['key']; lg = A0[k]
    dp, dt = lg['Dfade_pool'], lg['Dfade']
    tall = POS.get(k) in TALLPOS
    if not (0.0 < dp < 1.0):
        EFF[k] = max(1, min(64, int(q['pick'] or 64))); continue
    cands = [e for e in range(1, 65)
             if abs(dp ** (kwired(e, tall) / kpool(e)) - dt) < 1e-12]
    pk = max(1, min(64, int(q['pick'] or 64)))
    if pk in cands:
        EFF[k] = pk
    elif cands:
        EFF[k] = cands[0]
    else:
        EFF[k] = pk; unres.append(k)
worst = 0.0
for q in POP:
    k = q['key']; lg = A0[k]
    dp, dt = lg['Dfade_pool'], lg['Dfade']
    if not (0.0 < dp < 1.0):
        continue
    worst = max(worst, abs(dp ** (kwired(EFF[k], POS.get(k) in TALLPOS) / kpool(EFF[k])) - dt))
neq = sum(1 for q in POP if EFF[q['key']] != max(1, min(64, int(q['pick'] or 64))))
print('CONTROL A — Dfade reproduced from Dfade_pool + (effective pick, TALL): worst dev %.3e over %d '
      'rows -> %s ; %d rows carry an effective pick != stored pick ; %d unresolved'
      % (worst, N, 'EXACT' if worst < 1e-9 else 'DEVIATION', neq, len(unres)))
assert worst < 1e-9, 'ORDER K HALT: the calibrator bridge does not reproduce the wired tall fade'

gv = np.array([A0[k]['g'] for k in KEYS])
rho = np.array([A0[k]['rho'] for k in KEYS])
Dft = np.array([A0[k]['Dfade'] for k in KEYS])
Dfp = np.array([A0[k]['Dfade_pool'] for k in KEYS])
Dfx = np.array([(A0[k]['Dfade_pool'] ** (kfix(EFF[k], POS.get(k) in TALLPOS) / kpool(EFF[k])))
                if 0.0 < A0[k]['Dfade_pool'] < 1.0 else A0[k]['Dfade_pool']
                for k in KEYS])
sig = np.array([A0[k]['sig'] for k in KEYS])
Phi = np.array([A0[k]['Phi'] for k in KEYS])
bet = np.array([A0[k]['beta'] for k in KEYS])
V0 = np.array([A0[k]['V0'] for k in KEYS])
agp = np.array([A0[k]['agap'] for k in KEYS])
PHAT = {d: np.array([LEGS[d][k]['Phat'] for k in KEYS]) for d in DOSES}
yrv = np.array([q['yr'] for q in POP])
pkv = np.array([q['pick'] for q in POP])
armv = [q['arm'] for q in POP]

CLY = list(range(2005, 2022))
MC = np.zeros((len(CLY), N))
for i, y in enumerate(CLY):
    m = (yrv == y).astype(float)
    MC[i] = m
MCden = np.array([max(1.0, MC[i].sum()) for i in range(len(CLY))])
v0p = np.array([q['v0'] for q in POP])
MCv = np.zeros((len(CLY), N))
for i, y in enumerate(CLY):
    MCv[i] = (yrv == y).astype(float) * v0p
# class ratio = mean(p1)/mean(v0) per class, exactly as the sweep's MC/MCden pair does
MCden = np.array([max(1e-9, MCv[i].sum() / max(1.0, MC[i].sum())) * max(1.0, MC[i].sum())
                  for i in range(len(CLY))])

BANDS5 = ['1-10', '11-20', '21-30', '31-40', '41-64']


def nd_band(pk, arm):
    if arm != 'ND' or pk is None:
        return None
    for hi, nm in ((10, '1-10'), (20, '11-20'), (30, '21-30'), (40, '31-40'), (64, '41-64')):
        if pk <= hi:
            return nm
    return None


MB = np.zeros((5, N)); MBv = np.zeros((5, N))
for j, b in enumerate(BANDS5):
    m = np.array([1.0 if nd_band(pkv[i], armv[i]) == b else 0.0 for i in range(N)])
    MB[j] = m; MBv[j] = m * v0p
MBden = np.array([max(1e-9, MBv[j].sum()) for j in range(5)])
MCden2 = np.array([max(1e-9, MCv[i].sum()) for i in range(len(CLY))])

MU = lambda gu: np.where(gv > 0, (gv / gu) * np.exp(1.0 - gv / gu), 0.0)
MD = lambda gd: np.where(gv > 0, (gv / gd) * np.exp(1.0 - gv / gd), 0.0)


def p1_vec(dose, kap, gu, eta, gd, lrel, Df):
    D = np.where(Df < 1.0, np.minimum(1.0, Df * (1.0 + lrel * sig)), Df)
    mu = MU(gu); md = MD(gd)
    r2 = rho + kap * mu * (1.0 - rho)
    ped = (D * (1.0 - r2) + Phi * bet * r2) * V0 * np.maximum(0.0, 1.0 - eta * md)
    return r2 * PHAT[dose] + ped + kap * mu * (1.0 - rho) * agp * 20.0 * PLF


def read(dose, kap, gu, eta, gd, lrel, Df):
    p1 = p1_vec(dose, kap, gu, eta, gd, lrel, Df)
    Rc = (MC * p1).sum(1) / MCden2
    band = (MB * p1).sum(1) / MBden
    return dict(mean_0515=float(Rc[:11].mean()), max_class=float(Rc.max()),
                max_class_year=int(CLY[int(Rc.argmax())]),
                band_R={b: float(v) for b, v in zip(BANDS5, band)})


REG = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order_j_2026-08-18', 'REGION_J.json')))
RULED = None
for s in REG['shortlist']:
    if (abs(s['dose'] - 0.40) < 1e-9 and abs(s['kappa'] - 0.20) < 1e-9 and abs(s['eta'] - 0.50) < 1e-9
            and abs(s['gamma_u'] - 8.0) < 1e-9 and abs(s['gamma_d'] - 14.0) < 1e-9):
        RULED = s
print('\nREGION_J ruled row found: class %.4f bands %s'
      % (RULED['mean_0515'], {k: '%+.2f%%' % (100 * (v - 1)) for k, v in RULED['band_R'].items()}))

pt = (0.40, 0.20, 8.0, 0.50, 14.0, 1.08)
for nm, Df in (('POOLED (Order D)', Dfp), ('TALL wired (Order H+J)', Dft), ('TALL floor-FIXED (K)', Dfx)):
    r = read(*pt, Df)
    m = 'MATCHES REGION_J' if abs(r['mean_0515'] - RULED['mean_0515']) < 1e-9 and all(
        abs(r['band_R'][b] - RULED['band_R'][b]) < 1e-9 for b in BANDS5) else ''
    print('  %-24s class %.4f maxcls %.4f  %s   %s'
          % (nm, r['mean_0515'], r['max_class'],
             ' '.join('%+6.2f%%' % (100 * (r['band_R'][b] - 1)) for b in BANDS5), m))

print('\nCONTROL — the landing candidate (dose 0, repair knobs) on the POOLED fade:')
c = read(0.0, 0.24, 11.0, 0.41, 14.0, 1.08, Dfp)
print('   class %.4f  %s' % (c['mean_0515'], ' '.join('%+6.2f%%' % (100 * (c['band_R'][b] - 1)) for b in BANDS5)))

json.dump(dict(ruled=RULED,
               pooled=read(*pt, Dfp), tall_wired=read(*pt, Dft), tall_fixed=read(*pt, Dfx),
               landing_pool=c, s_norm_fix=SN_FIX),
          open(SP + '/ok/BRIDGE_K.json', 'w'), indent=1)
