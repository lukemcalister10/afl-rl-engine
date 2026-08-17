#!/usr/bin/env python3
"""ORDER J — THE DECLARED REFINEMENT PASS (PREREG_J §3.1: "a declared refinement pass around the
feasible set is permitted and its grid is printed").

The coarse sweep found the owner's laws G1 + G2-improve + G3 ARE jointly satisfiable, and that the
cheapest point in the whole 408,240-point grid moves exactly ONE counterweight knob: eta 0.41 -> 0.45,
with kappa, gamma_u and gamma_d left at the repair values. So the refinement asks the question the
owner actually needs answered:

    WHAT IS THE SMALLEST COUNTERWEIGHT MOVE THAT SATISFIES THE OWNER'S LAWS?

because the mature-row movement is proportional to that move, and therefore so is the price the
veteran pool pays. The grid is printed below and nothing outside it is searched.
"""
import os, sys, json, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]]
os.environ['O37_OUT'] = '/dev/null'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

# reuse the sweep module's instrument wholesale (controls included) without re-writing the maths
import importlib.util
spec = importlib.util.spec_from_file_location('o37sweep', os.path.join(HERE, 'o37_sweep.py'))
M = importlib.util.module_from_spec(spec)
import io, contextlib
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    spec.loader.exec_module(M)
print('instrument loaded from o37_sweep.py — controls re-run and re-passed '
      '(REMIX_32R exact, vector==scalar, landing candidate %.4f)' % M.CANDPT['mean_0515'])

BANDS5 = M.BANDS5
C = M.CANDPT
pct = lambda v: 100.0 * (v - 1.0)
REP = (0.24, 11.0, 0.41, 14.0, 1.08)

# ---- the refinement grid, printed ------------------------------------------------------------------
R_DOSE = [round(0.00 + 0.05 * i, 2) for i in range(0, 13)]        # 0.00 .. 0.60
R_KAP = [round(0.20 + 0.005 * i, 3) for i in range(0, 21)]        # 0.200 .. 0.300
R_GU = [10.0, 10.5, 11.0, 11.5, 12.0]
R_ETA = [round(0.410 + 0.005 * i, 3) for i in range(0, 19)]       # 0.410 .. 0.500
R_GD = [13.0, 13.5, 14.0, 14.5, 15.0]
R_REL = [1.08]
print('refinement grid: dose %s' % R_DOSE)
print('                 kappa %.3f..%.3f step 0.005 · eta %.3f..%.3f step 0.005'
      % (R_KAP[0], R_KAP[-1], R_ETA[0], R_ETA[-1]))
print('                 gamma_u %s · gamma_d %s · lam_rel %s (inert on this instrument)'
      % (R_GU, R_GD, R_REL))

# the legs only exist at the 15 extracted doses; refine the dose on that lattice
R_DOSE = [d for d in M.DOSES if d <= 0.60]
print('                 dose restricted to the 15 EXTRACTED leg doses <= 0.60: %s' % R_DOSE)
N = len(R_DOSE) * len(R_KAP) * len(R_GU) * len(R_ETA) * len(R_GD)
print('refinement points: %d' % N)

# extend the instrument's precomputed shape tables onto the refinement grid (same formulas)
for gu in R_GU:
    M.MU.setdefault(gu, np.where(M.gv > 0, (M.gv / gu) * np.exp(1.0 - M.gv / gu), 0.0))
    M.MU_G.setdefault(gu, np.where(M.GG > 0, (M.GG / gu) * np.exp(1.0 - M.GG / gu), 0.0))
for gd in R_GD:
    M.MD.setdefault(gd, np.where(M.gv > 0, (M.gv / gd) * np.exp(1.0 - M.gv / gd), 0.0))
    M.MD_G.setdefault(gd, np.where(M.GG > 0, (M.GG / gd) * np.exp(1.0 - M.GG / gd), 0.0))
MONO_R = {}
for kap in R_KAP:
    for gu in R_GU:
        mm = np.where(M.GGM > 0, (M.GGM / gu) * np.exp(1.0 - M.GGM / gu), 0.0)
        r = M.RHO_M + kap * mm * (1.0 - M.RHO_M)
        MONO_R[(kap, gu)] = bool(np.all(np.diff(r) >= -1e-12) and np.all(r < 1.0 + 1e-12))
print('rho32 monotonicity over the refinement grid: %d of %d (kappa, gamma_u) pairs pass'
      % (sum(MONO_R.values()), len(MONO_R)))


def cw_distance(kap, gu, eta, gd, rel):
    """the counterweight move, expressed in the units J-TOL charges for: each knob's step divided by
    its own measured FREE PLAY (the largest move that keeps every mature row inside its cap).
    free play is read off the board ladder in JTOL_J.json, by linearity."""
    FP = dict(kappa=0.00592, gamma_u=0.2794, eta=0.00403, gamma_d=0.1528, lam_rel=0.02083)
    return max(abs(kap - REP[0]) / FP['kappa'], abs(gu - REP[1]) / FP['gamma_u'],
               abs(eta - REP[2]) / FP['eta'], abs(gd - REP[3]) / FP['gamma_d'],
               abs(rel - REP[4]) / FP['lam_rel'])


OK = []
for dose in R_DOSE:
    for kap in R_KAP:
        for gu in R_GU:
            if not MONO_R[(kap, gu)]:
                continue
            for eta in R_ETA:
                for gd in R_GD:
                    m = M.metrics(dose, kap, gu, eta, gd, 1.08)
                    if m['max_class'] > 1.139: continue
                    if not (M.W_LO <= m['W'] <= M.W_HI): continue
                    if not (0.885 <= m['slope'] <= 1.115): continue
                    if not M.continuity_ok(dose, kap, gu, eta, gd, 1.08): continue
                    if m['mean_0515'] < 1.03 or m['mean_0515'] >= 1.14: continue
                    if max(m['band_R'].values()) > 1.14: continue
                    if m['band_R']['31-40'] <= C['band_R']['31-40']: continue
                    if m['band_R']['41-64'] <= C['band_R']['41-64']: continue
                    m['cw'] = cw_distance(kap, gu, eta, gd, 1.08)
                    OK.append(m)
print('\nrefinement points satisfying the RULED constraints AND G1 + G2-improve + G3: %d of %d'
      % (len(OK), N))

OK.sort(key=lambda m: (m['cw'], m['obj']))
print('\n=== THE CHEAPEST COUNTERWEIGHT MOVES THAT SATISFY THE OWNER\'S LAWS ===')
print('   "cw" = the move in units of the knob\'s own J-TOL free play. cw <= 1.0 would pass the gate.')
print('   %5s %6s %6s %6s %6s | %7s | %8s %8s | %s'
      % ('dose', 'kappa', 'gu', 'eta', 'gd', 'cw', 'class', 'maxcls', 'five bands yr0->1'))
seen = set(); CHEAP = []
for m in OK:
    k = (round(m['cw'], 3),)
    if len(CHEAP) >= 20: break
    CHEAP.append(m)
    print('   %5.2f %6.3f %6.1f %6.3f %6.1f | %7.2f | %8.4f %8.4f | %s'
          % (m['dose'], m['kappa'], m['gamma_u'], m['eta'], m['gamma_d'], m['cw'],
             m['mean_0515'], m['max_class'],
             ' '.join('%+6.2f%%' % pct(m['band_R'][b]) for b in BANDS5)))

print('\n=== THE OWNER\'S DECISION TABLE — what each level of veteran movement buys ===')
print('   For a per-row tolerance of p%% of a veteran\'s own value, the admissible counterweight move')
print('   scales as p/0.5 (the gate\'s own 0.5%%), i.e. cw <= p/0.5. Best laws reachable at each p:')
print('   %8s %7s | %8s %9s %9s %9s | %s'
      % ('tol p%', 'cw<=', 'class', 'picks31-40', 'picks41-64', 'worst band', 'the setting'))
for p in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.5, 10.0):
    lim = p / 0.5
    sub = [m for m in OK if m['cw'] <= lim]
    if not sub:
        print('   %7.1f%% %7.1f | %s' % (p, lim, 'NOTHING satisfies the owner\'s laws at this tolerance'))
        continue
    b = max(sub, key=lambda m: (min(m['band_R']['31-40'], m['band_R']['41-64']), m['mean_0515']))
    print('   %7.1f%% %7.1f | %8.4f %+8.2f%% %+8.2f%% %+8.2f%% | d%.2f k%.3f gu%.1f e%.3f gd%.1f'
          % (p, lim, b['mean_0515'], pct(b['band_R']['31-40']), pct(b['band_R']['41-64']),
             100 * (min(b['band_R']['31-40'], b['band_R']['41-64']) - 1),
             b['dose'], b['kappa'], b['gamma_u'], b['eta'], b['gamma_d']))
print('   (landing candidate for comparison: class %.4f · 31-40 %+.2f%% · 41-64 %+.2f%%)'
      % (C['mean_0515'], pct(C['band_R']['31-40']), pct(C['band_R']['41-64'])))

# ---- the dose-alone ladder: what is reachable with the counterweight FROZEN (Order I's world) ------
print('\n=== THE COUNTERWEIGHT FROZEN AT THE REPAIR POINT — the dose alone, against the ruled 1.139 line ===')
print('   %6s %9s %10s %6s | %s' % ('dose', 'class', 'max class', 'ruled', 'five bands yr0->1'))
FROZEN = []
for d in M.DOSES:
    m = M.metrics(d, *REP)
    ruled = 'ok' if m['max_class'] <= 1.139 else 'OVER'
    FROZEN.append(dict(dose=d, mean_0515=m['mean_0515'], max_class=m['max_class'],
                       band_R=m['band_R'], ruled_ok=(m['max_class'] <= 1.139)))
    print('   %6.2f %9.4f %10.4f %6s | %s'
          % (d, m['mean_0515'], m['max_class'], ruled,
             ' '.join('%+6.2f%%' % pct(m['band_R'][b]) for b in BANDS5)))
best_frozen = max([f for f in FROZEN if f['ruled_ok']], key=lambda f: f['dose'])
print('   => with the counterweight frozen, the ruled 1.139 line caps the dose at %.2f, where the'
      % best_frozen['dose'])
print('      class mark is %.4f (G1 floor 1.03 met, ideal 1.08 NOT reachable) and picks 31-40 sit at'
      % best_frozen['mean_0515'])
print('      %+.2f%% against the landing candidate\'s %+.2f%%.'
      % (pct(best_frozen['band_R']['31-40']), pct(C['band_R']['31-40'])))

json.dump(dict(order='ORDER J — the declared refinement pass',
               grid=dict(dose=R_DOSE, kappa=R_KAP, gamma_u=R_GU, eta=R_ETA, gamma_d=R_GD, lam_rel=R_REL),
               n_points=N, n_law_ok=len(OK), cheapest=CHEAP[:20], frozen_ladder=FROZEN,
               control_landing=C, control_tall_only=M.FADEONLY),
          open(os.path.join(HERE, 'REFINE_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: REFINE_J.json')
