#!/usr/bin/env python3
"""ORDER 24B STEP 4 -- U'' RE-DERIVED UNDER THE QUALITY-CONDITIONED DELIVERY.

Adapted from docs/evidence/pool_dial_2026-08-12/o24_uderive.py. The population, the entry weights
`e = pool_level(division) * _PL_F` (with `_b_factor == 1.0` proven in the harvest), the depth
convention and the ND65+ uncapped level law are all CARRIED VERBATIM. ONE thing changes: the premium
leg is now conditioned on QUALITY.

ORDER 24 asked that the entry-weighted mean of  (1-phi)*R + phi*U'  be 1. ORDER 24B asks the same of

    M = (1-phi)*R + phi*(1 + q*(U''-1)),      q = clip(avg_y / par(pathway, d), 0, 1)

so every historical cell carries its OWN q -- its own year's average against its own cell's par --
and the instrument reads

    mean = SUM e*[ (1-phi)*R + phi*(1 + q*(U''-1)) ] / SUM e  ==  1.0000000000   (asserted; HALTS)
=>  U''  = 1 + [ SUM e*(1-phi)*(1-R) ] / [ SUM e*phi*q ]

The NUMERATOR IS IDENTICAL to ORDER 24's U' numerator, so the whole move is a denominator move:

    U'' - 1  =  (U' - 1) * ( SUM e*phi / SUM e*phi*q )  =  (U' - 1) / qbar,   qbar = the q-mass ratio

and since q <= 1 by the clip, qbar <= 1 and U'' >= U' FOR EVERY PATHWAY, ALWAYS. That identity is not
assumed -- it is computed both ways below and the residual printed.

CONTROL MODE reproduces ORDER 24's U' from this same file (q forced to 1 everywhere), and must match
the `uplift` block of the alpha=1.0 surface to 1e-9. It is the non-vacuity proof for the machinery.

  usage: o24b_uderive.py <ucells.json> <par.json> <surface_in.json> <surface_out.json|-> [label|CONTROL]
"""
import sys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CELLS = json.load(open(sys.argv[1]))
PARJ = json.load(open(sys.argv[2]))
SURF_IN, SURF_OUT = sys.argv[3], sys.argv[4]
LABEL = sys.argv[5] if len(sys.argv) > 5 else 'psi'
CONTROL = (LABEL.upper() == 'CONTROL')
PL_F = float(CELLS['pl_f'])
WC = CELLS['cells']
S = json.load(open(SURF_IN))
PAR = PARJ['par']
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']

assert abs(float(S.get('_ORDER24_alpha', -1)) - 1.0) < 1e-12, \
    "ORDER 24B rides the alpha=1.0 surface (the pure delivery fix). Refusing a dialled surface."

# ---- THE LEVELS ARE READ FROM THE FILE AS COMMITTED ON THIS BRANCH. NEVER HARDCODED. -------------
CURPL = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
flat = dict(CURPL['signed_flat']); rd = dict(CURPL['signed_rd_positional'])
nd65 = float(CURPL['signed_nd65_plus']['measured_k15'])
LEV = {k: int(float(v)) for k, v in flat.items()}
LEV['ND65+'] = int(nd65)
for k, v in rd.items():
    LEV['RD:' + k] = int(float(v))

PATHSURF = {pw: {cl: [float(x) for x in dv] for cl, dv in cls.items()}
            for pw, cls in S['pathway'].items()}
WHOLE = {cl: [float(x) for x in dv] for cl, dv in S['whole_pool'].items()}


def e_of(c):
    return LEV[c['div']] * PL_F


def dclip(c):
    return min(max(int(c['d']), 1), 6)


def R_of(c):
    return float(PATHSURF[c['stream']][c['cls']][dclip(c) - 1])


def phi_of(c):
    fe = float(c['fe'])
    return min(max(float(c['gy']) / (6.0 * fe), 0.0), 1.0) if fe > 0 else 0.0


def q_of(c):
    """THE QUALITY. games>0 with a missing/zero average gives q = 0, per the order."""
    if CONTROL:
        return 1.0                                   # ORDER 24's delivery, EXACTLY
    if c['gy'] <= 0:
        return 0.0                                   # no premium leg exists; phi is 0 anyway
    a = c.get('avg_y')
    if a is None or not (a > 0.0):
        return 0.0
    p = PAR[c['stream']][dclip(c) - 1]
    return float(min(max(a / p, 0.0), 1.0)) if p > 0 else 0.0


P = print
P("=" * 126)
P("U'' RE-DERIVED   label=%s   delivery=%s   surface=%s"
  % (LABEL, ('ORDER 24 CONTROL (q == 1 everywhere)' if CONTROL else
             "ORDER 24B: quality-conditioned, q = clip(avg_y/par(pathway,d), 0, 1)"),
     os.path.basename(SURF_IN)))
P("=" * 126)
P("  entry weights e = level(division) * _PL_F, unchanged. Levels read from pvc_curve_v2.json:")
P("    " + " . ".join("%s %d" % (k, LEV[k]) for k in sorted(LEV)))
P("  par read from %s (K=%g shrink, every cell disclosed in PAR_TABLE.md)"
  % (os.path.basename(sys.argv[2]), PARJ['K']))
P()
P("  %-9s %7s %10s %10s %10s %8s %11s %11s %9s %18s" %
  ('pathway', 'cells', 'sit mass', 'play mass', 'q-mass', 'qbar', "U' (o24)", "U''", "U''-1 /", 'post-redist mean'))
P("  %-9s %7s %10s %10s %10s %8s %11s %11s %9s %18s" %
  ('', '', 'Se(1-phi)', 'Se*phi', 'Se*phi*q', 'qmass/', '', '', "U'-1", '(HALT if != 1)'))
MP = {}
bad = []
worst_ident = 0.0
for pw in PATHS + ['ALL POOL']:
    sub = WC if pw == 'ALL POOL' else [c for c in WC if c['stream'] == pw]
    tot = sitw = playw = qmass = num = 0.0
    for c in sub:
        e = e_of(c); ph = phi_of(c); R = R_of(c); q = q_of(c)
        tot += e
        sitw += e * (1.0 - ph)
        playw += e * ph
        qmass += e * ph * q
        num += e * (1.0 - ph) * R
    U2 = 1.0 + (sitw - num) / qmass if qmass > 0 else float('nan')
    U1 = 1.0 + (sitw - num) / playw if playw > 0 else float('nan')
    qbar = qmass / playw if playw > 0 else float('nan')
    # the identity U''-1 == (U'-1)/qbar, computed the other way and residualised
    ident = abs((U2 - 1.0) - (U1 - 1.0) / qbar) if qbar == qbar and qbar > 0 else 0.0
    worst_ident = max(worst_ident, ident)
    mean = (num + playw + qmass * (U2 - 1.0)) / tot if tot > 0 else float('nan')
    MP[pw] = dict(cells=len(sub), sit_mass=sitw, play_mass=playw, q_mass=qmass, qbar=qbar,
                  meanR=(num / sitw if sitw > 0 else float('nan')), U=U2, U_order24=U1,
                  ratio=((U2 - 1.0) / (U1 - 1.0) if U1 != 1.0 else float('nan')), mean=mean,
                  identity_residual=ident)
    if abs(mean - 1.0) > 1e-9: bad.append(pw)
    P("  %-9s %7d %10.1f %10.1f %10.1f %8.4f %11.6f %11.6f %9.4f %18.10f"
      % (pw, len(sub), sitw, playw, qmass, qbar, U1, U2,
         ((U2 - 1.0) / (U1 - 1.0) if U1 != 1.0 else float('nan')), mean))
P()
P("  MEAN-PRESERVATION INSTRUMENT: pathways whose post-redistribution entry-weighted mean is not")
P("  1.0000000000 (tol 1e-9): %d" % len(bad))
assert not bad, "MEAN-PRESERVATION FAILED on %s -- BUILD HALTS" % bad
P("  IDENTITY CHECK  U''-1 == (U'-1)/qbar  computed independently: worst |residual| = %.3e" % worst_ident)
assert worst_ident < 1e-9, "the U''/U' identity does not hold -- the derivation is not what it claims"
P("  U'' >= U' on every pathway: %s  (violations: %s)"
  % ('YES' if all(MP[p]['U'] >= MP[p]['U_order24'] - 1e-12 for p in MP) else 'NO',
     [p for p in MP if MP[p]['U'] < MP[p]['U_order24'] - 1e-12]))
P()

if CONTROL:
    LANDED = S['uplift']
    P("  CONTROL: with q forced to 1 everywhere the instrument must reproduce ORDER 24's U' exactly.")
    worst = 0.0
    for pw in PATHS:
        d = abs(MP[pw]['U'] - float(LANDED[pw])); worst = max(worst, d)
        P("    %-9s order24 %-14.10f  reproduced %-14.10f  |diff| %.3e" % (pw, LANDED[pw], MP[pw]['U'], d))
    P("    worst |diff| = %.3e" % worst)
    assert worst < 1e-9, "CONTROL FAILED: the ORDER 24B machinery does not reproduce ORDER 24's U'"
    P("  CONTROL PASSES -- the machinery is ORDER 24's with exactly one factor added.")

out = dict(S)
out['pathway'] = PATHSURF
out['whole_pool'] = WHOLE
out['uplift'] = {pw: round(MP[pw]['U'], 10) for pw in PATHS}
out['par'] = {pw: [round(x, 6) for x in PAR[pw]] for pw in PATHS}
out['par_all'] = [round(x, 6) for x in PAR['ALL POOL']]
out['mean_preserving'] = {pw: {k: (round(v, 10) if isinstance(v, float) else v)
                               for k, v in MP[pw].items()} for pw in MP}
out['_ORDER24B'] = ("ORDER 24B: the quality-conditioned premium. M = (1-phi)*R + phi*(1 + q*(U''-1)), "
                    "q = clip(avg_y/par(pathway,d),0,1), par = games-weighted playing par by pathway x "
                    "depth with a K=%g shrink toward the pathway's all-depth par. U'' re-derived per "
                    "pathway so the entry-weighted mean of M over the ORDER 21 harvest population is "
                    "1.0000000000 exactly. Levels read from engine/rl_after/pvc_curve_v2.json as "
                    "committed; NOT modified. Retention surface = ORDER 24's alpha=1.0 (unchanged)."
                    % PARJ['K'])
out['_ORDER24B_par_K'] = PARJ['K']
if SURF_OUT != '-':
    json.dump(out, open(SURF_OUT, 'w'), indent=1, default=float)
    P("  wrote %s" % SURF_OUT)
