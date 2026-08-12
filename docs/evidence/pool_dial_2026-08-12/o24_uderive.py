#!/usr/bin/env python3
"""ORDER 24 -- THE DIAL AND THE U' RE-DERIVATION UNDER CURRENT-STATE DELIVERY.

Adapted from docs/evidence/pool_landing_2026-08-12/o23_uderive.py. The population, the entry weights
`e = pool_level(division) * _PL_F` (with `_b_factor == 1.0` proven in the harvest), the depth
convention and the ND65+ uncapped level law are all CARRIED. Two things change.

1. THE DIAL.   R' = 1 + alpha*(R - 1), applied elementwise to the wired retention surface
               (`pathway` 9x3x6 and `whole_pool` 3x6). alpha=1.0 leaves R untouched, so alpha=1.0 is
               the PURE DELIVERY FIX.

2. THE DELIVERY. ORDER 21/22/23 partitioned each cell by the CAREER-state `sitout` flag and asked
   that the entry-weighted mean of {R on sitters, U on non-sitters} be 1. ORDER 24 delivers the same
   pair against CURRENT participation, so every cell carries a weight phi in [0,1] and the SAME
   instrument reads:

       mean = SUM_all e * [ (1-phi)*R' + phi*U' ]  /  SUM_all e   ==  1.0000000000   (asserted; HALTS)
   =>  U'   = ( SUM_all e  -  SUM_all e*(1-phi)*R' )  /  SUM_all e*phi
            = 1 + [ SUM_all e*(1-phi)*(1-R') ] / [ SUM_all e*phi ]

   which collapses to the ORDER 22/23 formula EXACTLY when phi is the career-state indicator. That
   collapse is not asserted -- it is RUN, as the CONTROL mode below, and must reproduce the landed
   `uplift` block of engine/rl_after/pool_retention_surface.json to 1e-9.

   Because (1-R') = alpha*(1-R) and the denominator is alpha-free, U'(alpha) - 1 == alpha*(U'(1)-1)
   EXACTLY. The dial therefore acts identically on both halves of the pair. Printed, not assumed.

  usage: o24_uderive.py <ucells.json> <alpha|CONTROL> <surface_in.json> <surface_out.json|-> [label]
"""
import sys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CELLS = json.load(open(sys.argv[1]))
AARG, SURF_IN, SURF_OUT = sys.argv[2], sys.argv[3], sys.argv[4]
LABEL = sys.argv[5] if len(sys.argv) > 5 else AARG
CONTROL = (AARG.upper() == 'CONTROL')
ALPHA = 1.0 if CONTROL else float(AARG)
PL_F = float(CELLS['pl_f'])
WC = CELLS['cells']
S = json.load(open(SURF_IN))
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']

# ---- STEP 4: THE LEVELS ARE READ FROM THE FILE AS COMMITTED ON THIS BRANCH. NEVER HARDCODED. ------
CURPL = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
flat = dict(CURPL['signed_flat']); rd = dict(CURPL['signed_rd_positional'])
nd65 = float(CURPL['signed_nd65_plus']['measured_k15'])
# The engine's own lookup, reproduced: rl_model.py:1436-1439 -- int() truncation, and the ND65+ CAP
# REMOVED (owner ruling 5262928754, landed on this branch). No min against the curve any more.
LEV = {k: int(float(v)) for k, v in flat.items()}
LEV['ND65+'] = int(nd65)
for k, v in rd.items():
    LEV['RD:' + k] = int(float(v))

# ---- THE DIAL, applied to the wired surface ------------------------------------------------------
def dial(v):
    return 1.0 + ALPHA * (float(v) - 1.0)


PATHSURF = {pw: {cl: [dial(x) for x in dv] for cl, dv in cls.items()}
            for pw, cls in S['pathway'].items()}
WHOLE = {cl: [dial(x) for x in dv] for cl, dv in S['whole_pool'].items()}


def e_of(c):
    return LEV[c['div']] * PL_F


def R_of(c):
    return float(PATHSURF[c['stream']][c['cls']][min(max(c['d'], 1), 6) - 1])


def phi_of(c):
    if CONTROL:
        return 0.0 if c['sitout'] else 1.0            # THE OLD DELIVERY, EXACTLY
    fe = float(c['fe'])
    return min(max(float(c['gy']) / (6.0 * fe), 0.0), 1.0) if fe > 0 else 0.0


P = print
P("=" * 118)
P("U' RE-DERIVED   label=%s   alpha=%s   delivery=%s   surface=%s"
  % (LABEL, ('n/a (control)' if CONTROL else ALPHA),
     ('CAREER-state (ORDER 21/22/23 CONTROL)' if CONTROL else 'CURRENT-state (ORDER 24)'),
     os.path.basename(SURF_IN)))
P("=" * 118)
P("  R' = 1 + alpha*(R-1) on the wired surface. Entry weights e = level(division) * _PL_F, unchanged.")
P("  engine level lookup (int-truncated; ND65+ UNCAPPED per the landed amendment):")
P("    " + " . ".join("%s %d" % (k, LEV[k]) for k in sorted(LEV)))
P()
P("  %-9s %7s %10s %10s %12s %12s %14s %18s" %
  ('pathway', 'cells', 'sit mass', 'play mass', 'sit share', "mean R'", "U'", 'post-redist mean'))
MP = {}
bad = []
for pw in PATHS + ['ALL POOL']:
    sub = WC if pw == 'ALL POOL' else [c for c in WC if c['stream'] == pw]
    tot = sitw = playw = num = 0.0
    for c in sub:
        e = e_of(c); ph = phi_of(c); R = R_of(c)
        tot += e
        sitw += e * (1.0 - ph)
        playw += e * ph
        num += e * (1.0 - ph) * R
    U = (tot - num) / playw if playw > 0 else float('nan')
    mean = (num + playw * U) / tot if tot > 0 else float('nan')
    meanR = num / sitw if sitw > 0 else float('nan')
    MP[pw] = dict(cells=len(sub), sit_mass=sitw, play_mass=playw, sit_share_w=sitw / tot,
                  meanR=meanR, U=U, mean=mean)
    if abs(mean - 1.0) > 1e-9: bad.append(pw)
    P("  %-9s %7d %10.1f %10.1f %10.4f %12.6f %14.6f %18.10f"
      % (pw, len(sub), sitw, playw, sitw / tot, meanR, U, mean))
P()
P("  MEAN-PRESERVATION INSTRUMENT: pathways whose post-redistribution entry-weighted mean is not")
P("  1.0000000000 (tol 1e-9): %d" % len(bad))
assert not bad, "MEAN-PRESERVATION FAILED on %s -- BUILD HALTS" % bad
P()

if CONTROL:
    LANDED = json.load(open(ROOT + '/engine/rl_after/pool_retention_surface.json'))['uplift']
    P("  CONTROL: the ORDER 24 instrument run on the CAREER-state delivery must reproduce the LANDED")
    P("  uplift block of engine/rl_after/pool_retention_surface.json exactly.")
    worst = 0.0
    for pw in PATHS:
        d = abs(MP[pw]['U'] - float(LANDED[pw])); worst = max(worst, d)
        P("    %-9s landed %-14.10f  reproduced %-14.10f  |diff| %.3e" % (pw, LANDED[pw], MP[pw]['U'], d))
    P("    worst |diff| = %.3e" % worst)
    assert worst < 1e-9, "CONTROL FAILED: the harvest does not reproduce the landed U -- BUILD HALTS"
    P("  CONTROL PASSES.")

out = dict(S)
out['pathway'] = PATHSURF
out['whole_pool'] = WHOLE
out['uplift'] = {pw: round(MP[pw]['U'], 10) for pw in PATHS}
out['mean_preserving'] = {pw: {k: (round(v, 10) if isinstance(v, float) else v)
                               for k, v in MP[pw].items()} for pw in MP}
out['_ORDER24'] = ("ORDER 24: R' = 1 + %g*(R-1) on the ORDER 23 wired surface; U' re-derived under "
                   "CURRENT-STATE delivery weights phi = min(gy/(6*fe),1) over the ORDER 21 harvest "
                   "population, entry-weighted mean 1.0000000000 exactly. Levels read from "
                   "engine/rl_after/pvc_curve_v2.json as committed; NOT modified." % ALPHA)
out['_ORDER24_alpha'] = ALPHA
if SURF_OUT != '-':
    json.dump(out, open(SURF_OUT, 'w'), indent=1, default=float)
    P("  wrote %s" % SURF_OUT)
