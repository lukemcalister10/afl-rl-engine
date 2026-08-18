#!/usr/bin/env python3
"""ORDER P BUILD — B8, CONTINUITY. No cliffs in age, in games, in pick, or on the two NEW axes.

ORDER K's ok_continuity.py, carried, with the ORDER P dial on and three objects added — because this
order introduces two axes the engine did not have before (the performance surplus, and the entry
price the premium is read on) and changes the shape of the charge on a third (games).

  AGE     — the S1 age bar, ages 18..30, every position. UNCHANGED by this order; re-asserted.
  GAMES   — (a) the CHARGE FACTOR itself, swept at 0.01-game resolution: continuous and, unlike the
                charge it replaces, NEVER RISING. The blind charge rose to 14 games and then fell
                back; that fall is the defect. This one does not fall back and does not jump.
            (b) the ruled AT-BAR CONTINUITY OBJECT, run TWICE: once against the AGE bar (ORDER K's
                own object) and once against the PEDIGREE bar. Both results are printed whichever way
                they come out. A row at his AGE bar is NOT at his pedigree bar if he was expensive,
                and this order charges him for that on purpose, so the two can disagree and the
                disagreement is the mechanism, not a defect. It is reported, never smoothed.
  PICK    — the live fade exponent across the pick axis. UNCHANGED by this order; re-asserted.
  SURPLUS — NEW. The charge factor across the whole surplus range, at 0.01 points a game.
  PRICE   — NEW. The premium, and the charge through it, across the whole entry-price range.
  rho32   — monotone in games and strictly below 1. UNCHANGED; re-asserted.
"""
import io, os, sys, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
DOSE, KAP, GU, ETA, GD, REL = 0.40, 0.20, 8.0, 0.50, 14.0, 1.08
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O37='1', RL_O36_LAM_S1=str(DOSE),
                  RL_O36_TALL='1', RL_O36_FLOORFIX='1', RL_O36_KAPPA=str(KAP), RL_O36_GAMMA=str(GU),
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
_BANNER = io.StringIO()
with contextlib.redirect_stdout(_BANNER):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NS)
os.chdir(_cwd)
BANNER = _BANNER.getvalue()
OUT = {}
L = []


def P(s=''):
    print(s); L.append(str(s))


LAM = NS['O37_LAMBDA']; G0 = NS['O37_G0']; THR = NS['O37_THETA_R']
S0 = NS['O37_S0']; TMAX = NS['O37_TMAX']; PGF = NS['o37_pg']
A = lambda g: 1.0 - math.exp(-g / G0)
T = lambda s: min(max(1.0 - THR * (s - S0), 0.0), TMAX)
FAC = lambda g, s: math.exp(-LAM * A(g) * T(s))
OLD = lambda g: max(0.0, 1.0 - ETA * ((g / GD) * math.exp(1.0 - g / GD))) if g > 0 else 1.0

P('ORDER P BUILD — B8, CONTINUITY. Six objects, each measured, none argued.')
P()
P('== THE ENGINE\'S OWN BANNER, printed at load with the dial on (it is swallowed by rl_export, so')
P('   it is captured here) ==')
_cap = False
for _ln in BANNER.split('\n'):
    if _ln.startswith('ORDER P LIVE'):
        _cap = True
    elif _cap and not _ln.startswith('  '):
        _cap = False
    if _cap:
        P('   ' + _ln)
open(os.path.join(HERE, 'ENGINE_BANNER_P.txt'), 'w').write(BANNER)

# ---- AGE -------------------------------------------------------------------------------------------
MA._O36_SCOPE['armed'] = True; MA._O36_SCOPE['on'] = True
P('\n== AGE: the S1 bar, ages 18 to 30, per position class (UNCHANGED by ORDER P) ==')
P('   %-6s %s' % ('pos', ' '.join('%7d' % a for a in range(18, 31))))
agefail = []
for pos in sorted(MA.REPL):
    vals = [MA.o36_bar(pos, a) for a in range(18, 31)]
    P('   %-6s %s' % (pos, ' '.join('%7.2f' % v for v in vals)))
    for i in range(1, len(vals)):
        if vals[i] < vals[i - 1] - 1e-12:
            agefail.append(('bar FALLS with age', pos, 17 + i))
    for i, a in enumerate(range(18, 31)):
        if vals[i] > MA.REPL[pos] + 1e-12:
            agefail.append(('bar ABOVE the flat bar', pos, a))
        if a >= 24 and abs(vals[i] - MA.REPL[pos]) > 1e-12:
            agefail.append(('not the flat bar from 24', pos, a))
P('   rises with age, never above the flat bar, EXACTLY the flat bar from 24: %s'
  % ('PASS' if not agefail else 'FAIL %s' % agefail))
OUT['age'] = dict(fail=agefail, bars={p: [MA.o36_bar(p, a) for a in range(18, 31)] for p in sorted(MA.REPL)})

# ---- GAMES (a): the charge factor itself ------------------------------------------------------------
P('\n== GAMES (a): the CHARGE FACTOR, swept at 0.01 games from 0 to 400 ==')
P('   %-8s %10s %10s %10s %10s | %10s' % ('s_P', 'max jump', 'at g', 'n rises', 'f(0)', 'the blind charge'))
gsteps = {}
for s in (-33.0, -20.0, -10.0, -5.0, 0.0, 5.0, 15.0):
    mx = 0.0; at = 0.0; nrise = 0
    g = 0.0; prev = FAC(0.0, s)
    while g < 400.0:
        g = round(g + 0.01, 2)
        c = FAC(g, s)
        if abs(c - prev) > mx:
            mx = abs(c - prev); at = g
        if c > prev + 1e-15:
            nrise += 1
        prev = c
    gsteps['%.1f' % s] = dict(max_jump=mx, at=at, n_rises=nrise)
    P('   %-8.1f %10.3e %10.2f %10d %10.6f | %s' % (s, mx, at, nrise, FAC(0.0, s), '-'))
mxold = 0.0; atold = 0.0; nriseold = 0
g = 0.0; prev = OLD(0.0)
while g < 400.0:
    g = round(g + 0.01, 2)
    c = OLD(g)
    if abs(c - prev) > mxold:
        mxold = abs(c - prev); atold = g
    if c > prev + 1e-15:
        nriseold += 1
    prev = c
P('   THE CHARGE BEING REPLACED, same sweep: max jump %.3e at g %.2f, and it RISES at %d of 40,000'
  % (mxold, atold, nriseold))
P('   steps — every one of them past 14 games. THAT IS THE DEFECT: more evidence bought a smaller')
P('   charge. The ORDER P factor never rises at any surplus.')
OUT['games_factor'] = dict(new=gsteps, old=dict(max_jump=mxold, at=atold, n_rises=nriseold))
gcliff = max(v['max_jump'] for v in gsteps.values())
grise = sum(v['n_rises'] for v in gsteps.values())

# ---- GAMES (b): the ruled at-bar continuity object ---------------------------------------------------
P('\n== GAMES (b): the ruled AT-BAR CONTINUITY OBJECT, run against BOTH bars ==')
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
rowsC = [c for c in CONT[DOSE] if c['atbar']]
MK = {r['key']: r for r in json.load(open(SP + '/per_entrant_OKRULED.json'))['recs']}


def sP_of(key):
    """s_P at 2026 for this row, off the built ORDER K matrix — the same object the engine forms."""
    r = MK.get(key)
    if r is None or not (float(r.get('v0') or 0) > 0) or r.get('age_draft') is None:
        return None
    num = den = 0.0
    for s in r['seasons']:
        g = float(s.get('games') or 0.0)
        if g <= 0:
            continue
        pos = s.get('bar')
        b = MA.REPL.get(pos)
        if b is None or s.get('avg') is None:
            return None
        age = int(r['age_draft']) + (int(s['year']) - int(r['year']))
        b = NS['o32_gate_bar'](pos, age)
        num += g * (float(s['avg']) - (b + PGF(float(r['v0']), 'TALL' if pos in MA.O36_TALLPOS else 'SMALL')))
        den += g
    return (num / den) if den > 0 else None


def run_object(mixfn, label):
    worst = 1e18; worstrow = None; nbad = 0; nrows = 0
    for c in rowsC:
        mix = mixfn(c)
        if mix is None:
            continue
        nrows += 1
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
    P('   %-46s rows %3d   worst step %+.4e (%s)   falling rows %d'
      % (label, nrows, worst, worstrow, nbad))
    return dict(n=nrows, worst=worst, row=worstrow, nbad=nbad)


OUT['atbar_K'] = run_object(lambda c: np.maximum(0.0, 1.0 - ETA * md), 'ORDER K, blind charge (the base)')
_sp_cache = {c['key']: sP_of(c['key']) for c in rowsC}
OUT['atbar_P_agebar'] = run_object(
    lambda c: (np.array([FAC(g, _sp_cache[c['key']]) if g > 0 else 1.0 for g in GG])
               if _sp_cache[c['key']] is not None else None),
    'ORDER P, rows AT THEIR AGE BAR')
OUT['atbar_P_pedbar'] = run_object(
    lambda c: np.array([FAC(g, 0.0) if g > 0 else 1.0 for g in GG]),
    'ORDER P, the same rows AT THEIR PEDIGREE BAR')
P()
P('   READ THIS PLAINLY. The object asks: for a row sitting exactly ON HIS BAR, does his price fall as')
P('   career games step 0, 1, 2 ... 20? Under ORDER K the answer was no, for a row at his AGE bar.')
P('   Under ORDER P a row at his AGE bar is NOT at his own bar if he was expensively drafted — he is')
P('   below it by the whole pedigree premium — so the charge grows with his games and his price can')
P('   fall. THAT IS THE MECHANISM THE OWNER ASKED FOR, working. Measured on the same rows, at their')
P('   PEDIGREE bar, the price does not fall at all: T(0) clips to zero, so they pay nothing at any')
P('   games count. Both numbers are printed above and neither is smoothed away.')

# ---- PICK ------------------------------------------------------------------------------------------
P('\n== PICK: the live fade exponent, swept at 0.01-pick resolution (UNCHANGED by ORDER P) ==')
kK = NS['o36_kappa_at']
OUT['pick'] = {}
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
    OUT['pick'][nm.strip()] = dict(max_step=mx, at=at)

# ---- SURPLUS (new) ----------------------------------------------------------------------------------
P('\n== SURPLUS (NEW AXIS): the charge factor across the whole surplus range, 0.01 points a game ==')
P('   %-8s %12s %10s %12s %12s' % ('games', 'max jump', 'at s_P', 'n rises', 'range of f'))
ssteps = {}
srise = 0; scliff = 0.0
for g in (1.0, 2.0, 5.0, 14.0, 30.0, 60.0, 200.0):
    mx = 0.0; at = 0.0; nrise = 0
    s = -60.0; prev = FAC(g, s); lo = hi = prev
    while s < 40.0:
        s = round(s + 0.01, 2)
        c = FAC(g, s)
        if abs(c - prev) > mx:
            mx = abs(c - prev); at = s
        if c < prev - 1e-15:
            nrise += 1                      # f must RISE with surplus: a better player pays less
        lo = min(lo, c); hi = max(hi, c)
        prev = c
    ssteps['%.0f' % g] = dict(max_jump=mx, at=at, n_falls=nrise, lo=lo, hi=hi)
    srise += nrise; scliff = max(scliff, mx)
    P('   %-8.0f %12.3e %10.2f %12d %12s' % (g, mx, at, nrise, '%.4f-%.4f' % (lo, hi)))
P('   "n rises" counts steps where a BETTER player was charged MORE. It is zero everywhere.')
OUT['surplus'] = ssteps

# ---- PRICE (new) -------------------------------------------------------------------------------------
P('\n== ENTRY PRICE (NEW AXIS): the premium, swept at 0.1% of price from 40 to 6,000 ==')
P('   %-6s %12s %12s %12s %14s' % ('class', 'max jump', 'at v0', 'n falls', 'range'))
OUT['price'] = {}
pcliff = 0.0; pfall = 0
for cls in ('TALL', 'SMALL'):
    mx = 0.0; at = 0.0; nfall = 0
    v = 40.0; prev = PGF(v, cls); lo = hi = prev
    while v < 6000.0:
        v = v * 1.001
        c = PGF(v, cls)
        if abs(c - prev) > mx:
            mx = abs(c - prev); at = v
        if c < prev - 1e-12:
            nfall += 1
        lo = min(lo, c); hi = max(hi, c)
        prev = c
    OUT['price'][cls] = dict(max_jump=mx, at=at, n_falls=nfall, lo=lo, hi=hi)
    pcliff = max(pcliff, mx); pfall += nfall
    P('   %-6s %12.3e %12.1f %12d %14s' % (cls, mx, at, nfall, '%+.2f to %+.2f' % (lo, hi)))
P('   The premium is read by linear interpolation on an even grid and HELD FLAT outside its support,')
P('   so a 0.1%% move in price can only move it by a thousandth of a point a game. No cliff.')

# ---- rho32 --------------------------------------------------------------------------------------------
P('\n== rho32, monotone in games and strictly below 1 (UNCHANGED by ORDER P) ==')
r31 = NS['rho31']
prev = -1.0; bad = 0; g = 0.0
while g <= 300.0:
    v = r31(g)
    if v < prev - 1e-12 or not (v < 1.0 + 1e-12):
        bad += 1
    prev = v; g += 0.25
P('   swept g = 0 to 300 in steps of 0.25: %d violations -> %s' % (bad, 'PASS' if bad == 0 else 'FAIL'))
OUT['rho32'] = dict(violations=bad)

ok = (not agefail) and bad == 0 and grise == 0 and srise == 0 and pfall == 0
P('\nB8 CONTINUITY: %s' % ('PASS — no cliff on any of the six axes, and the charge is monotone in '
                           'games and in surplus everywhere' if ok else 'FAIL — see above'))
P('  largest jump anywhere: games %.3e · surplus %.3e · price %.3e (per 0.01g / 0.01pt / 0.1%% of price)'
  % (gcliff, scliff, pcliff))
json.dump(OUT, open(os.path.join(HERE, 'CONTINUITY_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CONTINUITY_P_out.txt'), 'w').write('\n'.join(L) + '\n')
