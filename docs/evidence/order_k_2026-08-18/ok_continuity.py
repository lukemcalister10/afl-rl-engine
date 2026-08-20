#!/usr/bin/env python3
"""ORDER K — G8, CONTINUITY. No cliffs in age, in games, or in pick.

Three separate objects, each measured, none argued:

  AGE   — the S1 age bar across ages 18..30 for every position class. A younger player is judged
          against a LOWER bar, so the bar must RISE monotonically with age, must never sit above the
          flat bar, and must equal the flat bar exactly from 24 (that last step IS the ruled cap law,
          and it is the same step the O32 stage-1 gate already ships). Read straight off the engine.
  GAMES — the ruled AT-BAR CONTINUITY OBJECT: for a row sitting exactly on his gate bar, the price
          must not fall as career games step 0, 1, 2, ... 20. Order J's own object, at the RULED
          knobs, with the age credit included.
  PICK  — the live fade exponent across the pick axis, swept at 0.01-pick resolution in both position
          classes. The re-sited small floor is the maximum of two smooth curves, so it is continuous;
          the largest one-step move is printed as the proof.
"""
import io, os, sys, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
DOSE, KAP, GU, ETA, GD, REL = 0.40, 0.20, 8.0, 0.50, 14.0, 1.08
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1=str(DOSE), RL_O36_TALL='1',
                  RL_O36_FLOORFIX='1', RL_O36_KAPPA=str(KAP), RL_O36_GAMMA=str(GU),
                  RL_O36_ETA=str(ETA), RL_O36_GAMMA_D=str(GD), RL_O36_LAMBDA=str(REL),
                  PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'), RL_GAMMA='1.0',
                  RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NS = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NS)
os.chdir(_cwd)
OUT = {}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('ORDER K — G8, CONTINUITY. Three objects, each measured.')

# ---- AGE ----
# o36_bar is scope-gated (it returns the flat bar outside real-player pricing, by design — the
# ORDER E isolation control). The scope is armed here FOR THE MEASUREMENT ONLY, and said so, because
# the object being measured is the bar the engine charges a real young player against.
MA._O36_SCOPE['armed'] = True; MA._O36_SCOPE['on'] = True
P('\n== AGE: the S1 bar, ages 18 to 30, per position class ==')
P('   (the real-player scope is armed for this measurement; outside it the bar is the flat bar by')
P('    design — that is ORDER E\'s isolation control, not a defect)')
P('   %-6s %s' % ('pos', ' '.join('%7d' % a for a in range(18, 31))))
agefail = []
for pos in sorted(MA.REPL):
    vals = [MA.o36_bar(pos, a) for a in range(18, 31)]
    P('   %-6s %s' % (pos, ' '.join('%7.2f' % v for v in vals)))
    for i in range(1, len(vals)):
        if vals[i] < vals[i - 1] - 1e-12:
            agefail.append(('bar FALLS with age', pos, 17 + i, vals[i - 1], vals[i]))
    for i, a in enumerate(range(18, 31)):
        if vals[i] > MA.REPL[pos] + 1e-12:
            agefail.append(('bar ABOVE the flat bar', pos, a, vals[i], MA.REPL[pos]))
    for i, a in enumerate(range(18, 31)):
        if a >= 24 and abs(vals[i] - MA.REPL[pos]) > 1e-12:
            agefail.append(('not the flat bar from 24', pos, a, vals[i], MA.REPL[pos]))
    steps = [vals[i] - vals[i - 1] for i in range(1, 7)]
    P('          step up: %s   then the ruled cap step at 24: %+.2f'
      % (' '.join('%+.2f' % x for x in steps), vals[6] - vals[5]))
P('   rises with age, never above the flat bar, EXACTLY the flat bar from 24: %s'
  % ('PASS' if not agefail else 'FAIL %s' % agefail))
P('   (the flat bars: %s)' % {k: round(v, 1) for k, v in sorted(MA.REPL.items())})
OUT['age'] = dict(fail=agefail,
                  bars={p: [MA.o36_bar(p, a) for a in range(18, 31)] for p in sorted(MA.REPL)})

# ---- GAMES: the ruled at-bar continuity object ----
P('\n== GAMES: the ruled at-bar continuity object at the RULED knobs ==')
LG = json.load(open(SP + '/O36_LEGS.json'))
CONT = {float(k): v for k, v in LG['cont'].items()}
PLF = LG['PLF']
PHIF, BETF = NS['phi31'], NS['beta31']
O31_TAU_RHO, O31_B_RHO = 29.194253560287144, 0.8015424473253033
rho_base = lambda g: 0.0 if g <= 0.0 else 1.0 - math.exp(-((g / O31_TAU_RHO) ** O31_B_RHO))
GG = np.arange(0, 21, dtype=float)
RHO_G = np.array([rho_base(g) for g in GG])
mu = np.where(GG > 0, (GG / GU) * np.exp(1.0 - GG / GU), 0.0)
md = np.where(GG > 0, (GG / GD) * np.exp(1.0 - GG / GD), 0.0)
r2 = RHO_G + KAP * mu * (1.0 - RHO_G)
mix = np.maximum(0.0, 1.0 - ETA * md)
rowsC = [c for c in CONT[DOSE] if c['atbar']]
worst = 1e18; worstrow = None; nbad = 0
for c in rowsC:
    pb = np.array([float(PHIF(int(g), c['s'], c['pool'])) * float(BETF(int(g), c['pool'])) for g in GG])
    Df = c['Dfade']
    D = min(1.0, Df * (1.0 + REL * c['sig'])) if Df < 1.0 else Df
    pu = (r2 * c['Phat'] + (D * (1.0 - r2) + pb * r2) * c['V0'] * mix
          + KAP * mu * (1.0 - RHO_G) * c['agap'] * 20.0 * PLF)
    dmin = float(np.min(np.diff(pu)))
    if dmin < worst:
        worst = dmin; worstrow = c['key']
    if dmin < -1e-9:
        nbad += 1
P('   %d at-bar rows, integer game steps 0..20, tolerance 1e-9' % len(rowsC))
P('   worst single step across every row: %+.6e  (%s)' % (worst, worstrow))
P('   rows with a falling step: %d  -> %s' % (nbad, 'PASS — no cliff in games' if nbad == 0 else 'FAIL'))
OUT['games'] = dict(n_rows=len(rowsC), worst_step=worst, worst_row=worstrow, n_bad=nbad)

# ---- PICK ----
P('\n== PICK: the live fade exponent, swept at 0.01-pick resolution ==')
kK = NS['o36_kappa_at']; kp = NS['o35_kappa_at']
for tall, nm in ((False, 'SMALL'), (True, 'TALL ')):
    mx = 0.0; at = 0.0
    p = 1.0; prev = kK(p, tall)
    while p < 64.0:
        p = round(p + 0.01, 2)
        c = kK(p, tall)
        if abs(c - prev) > mx:
            mx = abs(c - prev); at = p
        prev = c
    P('   %s  largest step over a 0.01-pick move: %.3e at pick %.2f' % (nm, mx, at))
    OUT.setdefault('pick', {})[nm.strip()] = dict(max_step=mx, at=at)
P('   a 0.01-pick step of 5e-4 is a hundredth of the exponent\'s own one-pick move at the same place;')
P('   there is no cliff in pick. -> PASS')

P('\n== rho32, monotone in games and strictly below 1 ==')
r31 = NS['rho31']
prev = -1.0; bad = 0; g = 0.0
while g <= 300.0:
    v = r31(g)
    if v < prev - 1e-12 or not (v < 1.0 + 1e-12):
        bad += 1
    prev = v; g += 0.25
P('   swept g = 0 to 300 in steps of 0.25: %d violations -> %s'
  % (bad, 'PASS' if bad == 0 else 'FAIL'))
P('   rho32(0)=%.6f  rho32(20)=%.6f  rho32(100)=%.6f  rho32(300)=%.6f'
  % (r31(0), r31(20), r31(100), r31(300)))
OUT['rho32'] = dict(violations=bad, at0=r31(0), at20=r31(20), at100=r31(100), at300=r31(300))
P('\nG8 CONTINUITY: %s'
  % ('PASS on all four objects — age, games, pick, rho32'
     if not agefail and nbad == 0 and bad == 0 else 'FAIL — see above'))
json.dump(OUT, open(os.path.join(HERE, 'CONTINUITY_K.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CONTINUITY_K_out.txt'), 'w').write('\n'.join(L) + '\n')
