#!/usr/bin/env python3
"""ORDER 25 -- U''' RE-DERIVED UNDER THE AMENDED PARS, AT A CANDIDATE LEVEL TABLE.

Two parents, and the join is the whole content of this file:

  * docs/evidence/pool_quality_2026-08-12/o24b_uderive.py -- the quality-conditioned instrument
    `M = (1-phi)*R + phi*(1 + q*(U-1))`, its mean-preservation HALT, and the `U-1 = (U'-1)/qbar`
    identity check. CARRIED VERBATIM except for the par it reads.
  * docs/evidence/pool_landing_2026-08-12/o23_uderive.py -- U IS RE-DERIVED AT THE CANDIDATE LEVELS
    OF EACH ITERATION ROUND, not at the levels committed in the checkout.

WHY THE SECOND PARENT MATTERS, STATED PLAINLY. `e = entry_anchor = pool_level(division) * _PL_F`
weights every cell of the mean-preservation instrument. The level IS the weight. ORDER 24B could read
the levels from the checkout because ORDER 24B FROZE them (#469 values, the cheap path). ORDER 25
moves them, so U must move with them or the instrument would be preserving the mean of a population
weighted by prices nobody pays. ORDER 22 and ORDER 23 both re-derived U inside the iteration loop --
`o22_iterate.sh` / `o23_iterate.sh` call the uderive step between the level step and the emit -- and
THIS FILE MATCHES THAT CONVENTION EXACTLY, which is what the ORDER 25 brief asks be checked and
matched rather than assumed.

R CARRIES UNCHANGED at every round. It is a ratio and is calibration-independent (ORDER 21 handback
item 4); only the entry weights and the q-mass move.

    U''' = 1 + [ SUM e*(1-phi)*(1-R) ] / [ SUM e*phi*q ]
    mean = SUM e*[ (1-phi)*R + phi*(1 + q*(U'''-1)) ] / SUM e  ==  1.0000000000  (HALT otherwise)

CONTROL MODE (`--control`) forces q == 1 everywhere and must reproduce ORDER 24's U' from this same
file -- the non-vacuity proof that the quality factor is the only thing this instrument adds.

  usage: o25_uderive.py <ucells.json> <par.json> <levels.json|CHECKOUT> <surface_in.json>
                        <surface_out.json|-> [label] [--control]
"""
import sys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CELLS = json.load(open(sys.argv[1]))
PARJ = json.load(open(sys.argv[2]))
LEVARG = sys.argv[3]
SURF_IN, SURF_OUT = sys.argv[4], sys.argv[5]
ARGS = [a for a in sys.argv[6:] if not a.startswith('--')]
LABEL = ARGS[0] if ARGS else LEVARG
CONTROL = '--control' in sys.argv
PL_F = float(CELLS['pl_f'])
WC = CELLS['cells']
S = json.load(open(SURF_IN))
PAR = PARJ['par']
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']

assert abs(float(S.get('_ORDER24_alpha', -1)) - 1.0) < 1e-12, \
    "ORDER 25 lands the alpha=1.0 delivery. Refusing a dialled surface."
assert PARJ.get('donor_axis', '').startswith('ALL-POOL SAME-DEPTH'), \
    "this file requires the AMENDED par table (all-pool same-depth donor); got %r" % PARJ.get('donor_axis')

# ---- THE LEVELS IN FORCE FOR THIS ROUND ---------------------------------------------------------
CURPL = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
if LEVARG == 'CHECKOUT':
    flat = dict(CURPL['signed_flat']); rd = dict(CURPL['signed_rd_positional'])
    nd65 = float(CURPL['signed_nd65_plus']['measured_k15'])
else:
    Lv = json.load(open(LEVARG))
    flat = dict(Lv['signed_flat']); rd = dict(Lv['signed_rd_positional'])
    nd65 = float(Lv['nd65_measured_k15'])
# the engine's own lookup: rl_model.py int() truncation, and the ND65+ law AS AMENDED by ORDER 23
# (owner ruling 5262928754) -- no cap, the derived level read verbatim.
LEV = {k: int(float(v)) for k, v in flat.items()}
LEV['ND65+'] = int(nd65)
for k, v in rd.items():
    LEV['RD:' + k] = int(float(v))

PATHSURF = {pw: {cl: [float(x) for x in dv] for cl, dv in cls.items()} for pw, cls in S['pathway'].items()}
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
    """THE QUALITY against the AMENDED par. games>0 with a missing/zero average gives q = 0."""
    if CONTROL:
        return 1.0
    if c['gy'] <= 0:
        return 0.0
    a = c.get('avg_y')
    if a is None or not (a > 0.0):
        return 0.0
    p = PAR[c['stream']][dclip(c) - 1]
    return float(min(max(a / p, 0.0), 1.0)) if p > 0 else 0.0


P = print
P("=" * 126)
P("U''' RE-DERIVED   label=%s   levels=%s   par=AMENDED (all-pool same-depth donor, K=%g)"
  % (LABEL, os.path.basename(LEVARG), PARJ['K']))
P("=" * 126)
if CONTROL:
    P("  *** CONTROL MODE: q forced to 1 everywhere -- this is ORDER 24's U', reproduced. ***")
P("  R carries UNCHANGED (a ratio, calibration-independent). Entry weights and q-mass move.")
P("  engine level lookup (int-truncated; ND65+ UNCAPPED per owner ruling 5262928754):")
P("    " + " . ".join("%s %d" % (k, LEV[k]) for k in sorted(LEV)))
P()
P("  %-9s %7s %10s %10s %10s %8s %11s %11s %18s" %
  ('pathway', 'cells', 'sit mass', 'play mass', 'q-mass', 'qbar', "U'' (o24b)", "U'''", 'post-redist mean'))
P("  %-9s %7s %10s %10s %10s %8s %11s %11s %18s" %
  ('', '', 'Se(1-phi)', 'Se*phi', 'Se*phi*q', 'ratio', 'this level', 'THIS ACT', '(HALT if != 1)'))
P("  " + "-" * 122)
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
    U3 = 1.0 + (sitw - num) / qmass if qmass > 0 else float('nan')
    U1 = 1.0 + (sitw - num) / playw if playw > 0 else float('nan')
    qbar = qmass / playw if playw > 0 else float('nan')
    ident = abs((U3 - 1.0) - (U1 - 1.0) / qbar) if qbar == qbar and qbar > 0 else 0.0
    worst_ident = max(worst_ident, ident)
    mean = (num + playw + qmass * (U3 - 1.0)) / tot if tot > 0 else float('nan')
    MP[pw] = dict(cells=len(sub), sit_mass=sitw, play_mass=playw, q_mass=qmass, qbar=qbar,
                  meanR=(num / sitw if sitw > 0 else float('nan')), U=U3, U_flat=U1,
                  mean=mean, identity_residual=ident)
    if abs(mean - 1.0) > 1e-9: bad.append(pw)
    P("  %-9s %7d %10.1f %10.1f %10.1f %8.4f %11.6f %11.6f %18.10f"
      % (pw, len(sub), sitw, playw, qmass, qbar, U1, U3, mean))
P()
P("  MEAN-PRESERVATION INSTRUMENT: pathways whose post-redistribution entry-weighted mean is not")
P("  1.0000000000 (tol 1e-9): %d" % len(bad))
assert not bad, "MEAN-PRESERVATION FAILED on %s -- BUILD HALTS" % bad
P("  IDENTITY CHECK  U-1 == (U_flat-1)/qbar, computed independently: worst |residual| = %.3e" % worst_ident)
assert worst_ident < 1e-9, "the U/qbar identity does not hold -- the derivation is not what it claims"
P()

if CONTROL:
    LANDED = S['uplift']
    P("  CONTROL: with q == 1 the instrument must reproduce the surface's own uplift block exactly.")
    worst = 0.0
    for pw in PATHS:
        d = abs(MP[pw]['U'] - float(LANDED[pw])); worst = max(worst, d)
        P("    %-9s surface %-14.10f  reproduced %-14.10f  |diff| %.3e" % (pw, LANDED[pw], MP[pw]['U'], d))
    P("    worst |diff| = %.3e" % worst)

out = dict(S)
out['pathway'] = PATHSURF
out['whole_pool'] = WHOLE
out['uplift'] = {pw: round(MP[pw]['U'], 10) for pw in PATHS}
out['par'] = {pw: [round(x, 6) for x in PAR[pw]] for pw in PATHS}
out['par_all'] = [round(x, 6) for x in PAR['ALL POOL']]
out['mean_preserving'] = {pw: {k: (round(v, 10) if isinstance(v, float) else v)
                               for k, v in MP[pw].items()} for pw in MP}
out['_ORDER25'] = ("ORDER 25, THE LANDING: M = (1-phi)*R + phi*(1 + q*(U-1)) with q = clip(avg_y/par,0,1) "
                   "and par shrunk toward THE ALL-POOL SAME-DEPTH par at K=%g (owner amendment, #334 "
                   "comment 5267147448, the ORDER 21 class-axis convention). U re-derived AT THIS ROUND'S "
                   "CANDIDATE LEVELS (%s) so the mean-preservation instrument is weighted by the entry "
                   "anchors actually in force -- the ORDER 22/23 iteration convention, matched. "
                   "Entry-weighted mean of M over the ORDER 21 harvest population = 1.0000000000 exactly."
                   % (PARJ['K'], LABEL))
out['_ORDER25_par_K'] = PARJ['K']
out['_ORDER25_par_donor'] = PARJ['donor_axis']
out['_ORDER25_levels'] = LEV
if SURF_OUT != '-':
    json.dump(out, open(SURF_OUT, 'w'), indent=1, default=float)
    P("  wrote %s" % SURF_OUT)
