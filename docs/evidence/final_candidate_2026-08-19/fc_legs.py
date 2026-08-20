#!/usr/bin/env python3
"""FINAL-CANDIDATE — THE MECHANISM LEGS. The assembly seat's as_legs.py with its dial line
corrected to the candidate's own (see the block below) and the output renamed. Every measurement is
otherwise byte-identical.

ORIGINAL ASSEMBLY HEADER FOLLOWS.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as L

# THE CANDIDATE'S OWN DIAL LINE. TWO CORRECTIONS TO THE INHERITED FILE, BOTH DISCLOSED:
#   1. RL_O40_CAPPCT was '20' in as_legs.py. THE CANDIDATE IS p15 — and so was the assembly seat's
#      own candidate. The assembly's LEGS_CAND.json was therefore computed on a cap anchor its board
#      was not built on. Corrected here to '15'; reported in PACKET_FINAL as a finding against the
#      inherited instrument, not smoothed over.
#   2. RL_O41_RAMP/BREAK/UNWIND and RL_O42 were absent entirely. Added, so the legs are read in the
#      state this board is actually priced in.
D = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
         RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
         RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1', RL_O41_R3='1',
         RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7', RL_O42='1')
print('loading the engine on THE CANDIDATE dial line:')
for k in sorted(D):
    print('   %s=%s' % (k, D[k]))
NS = L.load(**D)
MA = NS['_MA']
Y = MA.BASE_REF
print('evaluated year Y = %s' % Y)

rho31 = NS['rho31']; o31_pi = NS['o31_pi']; pv_ped = NS['pv_pedigree']
age_cr = NS['o32_age_credit']; o31_D = NS['o31_D']; o31_cu = NS['o31_cu']
pv_games = NS['pv_games']; r3 = NS.get('o41_r3_take'); inj = NS.get('o41_injured')
PRED8 = NS.get('_O41_PRED8', {})

# the S-S5 limb-2 window, read off the loaded namespace so the packet can quote it exactly
o38_T = NS['o38_T']; O40_TH = NS['O40_THETA_R']; O37_TH = NS['O37_THETA_R']
O37_S0 = NS['O37_S0']; O37_TMAX = NS['O37_TMAX']; O40_CAPC = NS['O40_CAPC']
LAM = NS['O40_LAMBDA']; G0 = NS['O37_G0']
s5n = 0; s5max = 0.0; s5lo = None; s5hi = None
for i in range(0, 22001):
    ss = 20.0 - 0.01 * i
    Ts = o38_T(ss)
    TP = min(max(1.0 - O37_TH * (ss - O37_S0), 0.0), O37_TMAX)
    if Ts > TP + 1e-12:
        s5n += 1; s5max = max(s5max, Ts - TP)
        s5lo = ss if s5lo is None else min(s5lo, ss)
        s5hi = ss if s5hi is None else max(s5hi, ss)
worst_pct = 100.0 * (1.0 - math.exp(-LAM * (1.0 - math.exp(-38.0 / G0)) * s5max)) if s5n else 0.0
print()
print('S-S5 LIMB 2 (the disclosed window, vs ORDER P\'s own p5 clip):')
if s5n == 0:
    print('  NO surplus at which this board\'s cap exceeds ORDER P\'s.')
else:
    print('  window s in [%.4f, %.4f], %.4f points a game wide; worst excess in T %.9f,'
          % (s5lo, s5hi, s5hi - s5lo, s5max))
    print('  i.e. AT MOST %.4f%% of the pedigree leg at 38 games. The cohort centre s0 is %.4f, so the'
          % (worst_pct, O37_S0))
    print('  window sits ABOVE it — on rows already producing at or above what their price implies.')

rows = {}
nz = 0
for p in MA.data:
    k = p.get('key')
    if not k:
        continue
    try:
        g = pv_games(p, Y)
        ped = pv_ped(p)
    except SystemExit:
        continue
    except Exception:
        continue
    try:
        pi = o31_pi(p, Y, g)
        prod = rho31(g) * 0.0
        cu = o31_cu(p, Y)
        Dv = o31_D(p, Y)
    except Exception:
        continue
    rows[k] = dict(g=g, ped=ped * pi, ped_raw=ped, charge=pi, D=Dv, cu=cu,
                   injured=bool(inj(p)) if inj else False)
    nz += 1

# the production leg and the absence take need `e`, which only the blend site sees. Wrap it.
PV = NS['_PV']
base = PV['blend']
seen = {}


def wrapped(p, YY, e):
    k = p.get('key')
    if k is not None:
        seen[k] = float(e)
    return base(p, YY, e)


PV['blend'] = wrapped
# re-price every row through the engine's own path so `e` is captured in the real clock state
for p in MA.data:
    try:
        MA.pv(p, Y) if hasattr(MA, 'pv') else None
    except Exception:
        pass
PV['blend'] = base

for k, r in rows.items():
    e = seen.get(k)
    if e is None:
        r['prod'] = None; r['take'] = None; r['v0'] = None
        continue
    g = r['g']
    r['prod'] = rho31(g) * e
    r['v0'] = r['ped_raw']

out = dict(n=len(rows), Y=Y,
           s5=dict(n=s5n, lo=s5lo, hi=s5hi, worst_T=s5max, worst_pct=worst_pct),
           rows={k: {kk: vv for kk, vv in r.items()} for k, r in rows.items()})
json.dump(out, open(os.path.join(HERE, 'LEGS_FC.json'), 'w'), indent=1, sort_keys=True)
print()
print('rows with legs: %d   (production leg captured on %d)' % (len(rows), len(seen)))
print('written: LEGS_FC.json')
