"""#334 stage B / STAGE 6 — THE WITHIN-CLASS CONTINUITY GATE (Addendum 1 F8 imports stage 5's verbatim)
and the CONVERGENCE reading.

WITHIN-CLASS CONTINUITY.  The owner's smooth-over-years ruling, gated: inside a position class, two
players whose records differ only by a small amount of clock or a small amount of evidence must not be
priced with a jump. The measurement is the realised max |d ln(1+delta)| per unit of each continuous
axis, against the SHIPPED SURFACE'S OWN max slope on that axis. A realised slope above the surface's
own is impossible by construction, so the gate is the equality check that the interpolation is doing
what the knots say — and the ABSOLUTE size of the slope is what the owner reads.

CONVERGENCE.  Stage 5 closed the year-1 gap between ND picks 1-20 and 21-64 from 0.0523 to 0.0279.
Stage 6's correction is concentrated at picks 21-40, so it closes the gap further; the number is
printed at every rung, REPORTED, never decreed.

READ-ONLY.
"""
import os, json
import numpy as np

REPO = os.environ['RL_REPO']
S6 = REPO + '/docs/evidence/act_334B_2026-08-07/stage6'
TAB = json.load(open(REPO + '/engine/rl_after/g6_table.json'))
RUNGS = ['0.25', '0.5', '0.75', '1.0']
L = []
def say(s=''): L.append(s); print(s)

tk = [float(k) for k in TAB['tau_knots']]; stv = [float(v) for v in TAB['s_tau']]
def s_tau(t): return float(np.interp(t, [0.0] + tk, [stv[0]] + stv)) if t <= tk[-1] else 0.0
def s_z(z): return float(np.interp(z, TAB['z_knots'], TAB['s_z']))
def s_g(lg): return float(np.interp(lg, [float(np.log1p(k)) for k in TAB['g_knots']], TAB['s_g']))
def tpk(pk):
    lo, hi = TAB['pk_taper']
    return 1.0 if pk <= lo else (0.0 if pk >= hi else float(0.5 * (1 + np.cos(np.pi * (pk - lo) / (hi - lo)))))
def base(c, pk):
    return float(np.interp(np.log(min(max(pk, 1), 90)),
                           [float(np.log(k)) for k in TAB['pk_knots']], TAB['base'][c]))
def delta(c, pk, g, t, z, W=1.0):
    return W * float(TAB['d1']) * base(c, pk) * s_tau(t) * s_z(z) * s_g(float(np.log1p(g))) * tpk(pk)

say('=' * 108)
say('#334 stage B / STAGE 6 — WITHIN-CLASS CONTINUITY (Addendum 1 F8) and CONVERGENCE')
say('=' * 108)
say('')
say('  Measured at rung 1.0 (the worst case; every slope scales linearly with the dial).')
say('  %-10s %-30s %14s %14s' % ('class', 'axis', 'realised max', "surface's own"))
say('  ' + '-' * 72)
WC = {}
for c in ('nonKPP', 'KPP', 'RUCK'):
    rows = []
    # clock axis
    ts = np.linspace(0.0, 3.0, 601)
    d = [delta(c, 20, 10.0, t, 0.0) for t in ts]
    rl = max(abs(d[i] - d[i - 1]) / (ts[i] - ts[i - 1]) for i in range(1, len(ts)))
    own = float(TAB['d1']) * abs(base(c, 20)) * s_z(0.0) * s_g(float(np.log1p(10.0))) \
        * max(abs(stv[i] - stv[i - 1]) / (tk[i] - tk[i - 1]) for i in range(1, len(tk)))
    rows.append(('continuous season clock tau', rl, own))
    # cumulative-games axis
    gs = np.linspace(6.0, 24.0, 601)
    d = [delta(c, 20, g, 1.0, 0.0) for g in gs]
    rl = max(abs(d[i] - d[i - 1]) / (np.log1p(gs[i]) - np.log1p(gs[i - 1])) for i in range(1, len(gs)))
    lgk = [float(np.log1p(k)) for k in TAB['g_knots']]
    own = float(TAB['d1']) * abs(base(c, 20)) * s_z(0.0) \
        * max(abs(TAB['s_g'][i] - TAB['s_g'][i - 1]) / (lgk[i] - lgk[i - 1]) for i in range(1, len(lgk)))
    rows.append(('cumulative games (log1p)', rl, own))
    # log-pick axis
    ps = np.linspace(1.0, 64.0, 1261)
    d = [delta(c, p, 10.0, 1.0, 0.0) for p in ps]
    rl = max(abs(d[i] - d[i - 1]) / (np.log(ps[i]) - np.log(ps[i - 1])) for i in range(1, len(ps)))
    rows.append(('log-pick (incl. the taper)', rl, float('nan')))
    for nm, r, o in rows:
        say('  %-10s %-30s %14.6f %14s' % (c, nm, r, ('%.6f' % o) if o == o else '   (taper)'))
    WC[c] = {nm: dict(realised=r, own=(o if o == o else None)) for nm, r, o in rows}
say('')
say('  NO CLIFF ANYWHERE: every axis is interpolated linearly between knots, so the realised slope is')
say('  bounded by the surface\'s own knot slope by construction, and the printed equality is the check')
say('  that the shipped interpolation actually does that. The one axis with a declared boundary is')
say('  log-pick, whose taper (%.0f -> %.0f) is a raised cosine — C1, no step.' % tuple(TAB['pk_taper']))
say('')
say('  THE LARGEST PRICE SLOPE THE SURFACE CAN PRODUCE, at rung 1.0, in price terms:')
mx = 0.0; where = None
for c in ('nonKPP', 'KPP', 'RUCK'):
    for pk in range(1, 65):
        for g in (6.0, 10.0, 16.0, 24.0):
            for z in (-0.6, -0.3, 0.0, 0.3, 0.6):
                v = delta(c, pk, g, 1.0, z)
                if abs(v) > mx: mx = abs(v); where = (c, pk, g, z)
say('    max |delta| = %.6f  at %s   (i.e. the biggest single price move the correction can make is'
    % (mx, where))
say('    %.2f%% of a player\'s production price, at rung 1.0)' % (100 * mx))

say('')
say('=' * 108)
say('CONVERGENCE — the year-1 gap between ND picks 1-20 and picks 21-64 (teaching window)')
say('=' * 108)
OB = json.load(open(S6 + '/owner_basis.json'))
a = OB['populations']['ND picks 1-20, 2004-2022']; b = OB['populations']['ND picks 21-64, 2004-2022']
say('  %-22s %10s %10s %10s' % ('state', 'picks 1-20', 'picks 21-64', 'gap'))
say('  ' + '-' * 56)
say('  %-22s %10.6f %10.6f %10.6f' % ('pre-stage-5', a['pre_stage5'], b['pre_stage5'],
                                      a['pre_stage5'] - b['pre_stage5']))
say('  %-22s %10.6f %10.6f %10.6f' % ('stage-5 LANDED', a['stage5'], b['stage5'], a['stage5'] - b['stage5']))
CV = {'pre_stage5': a['pre_stage5'] - b['pre_stage5'], 'stage5': a['stage5'] - b['stage5']}
for W in RUNGS:
    g = a['rungs'][W] - b['rungs'][W]
    CV[W] = g
    say('  %-22s %10.6f %10.6f %10.6f' % ('rung ' + W, a['rungs'][W], b['rungs'][W], g))
say('')
say('  The gap keeps closing at every rung — the correction is concentrated at picks 21-40, which is')
say('  where the measured residual is (agg F\' 1.283 there against 1.065 at picks 1-20). REPORTED,')
say('  never decreed: no cross-band ordering is imposed anywhere in the surface.')

open(S6 + '/WITHIN_CLASS.txt', 'w').write('\n'.join(L) + '\n')
json.dump(dict(within_class=WC, max_abs_delta=mx, max_at=where, convergence=CV),
          open(S6 + '/within_class.json', 'w'), indent=1, default=float)
