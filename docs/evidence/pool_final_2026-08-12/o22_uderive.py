#!/usr/bin/env python3
"""ORDER 22 -- RE-DERIVE THE MEAN-PRESERVING UPLIFT U AGAINST A CANDIDATE LEVEL TABLE.

ORDER 21 handback item 4: `U` is a pure function of the pathway's sit share and mean `R`, weighted by
`e = entry_anchor`, so it MOVES when the entry levels move. `R` itself is a ratio and is
calibration-independent -- it carries UNCHANGED.

    U    = ( SUM_all e  -  SUM_sit e*R )  /  SUM_non e
    mean = ( SUM_sit e*R + SUM_non e*U )  /  SUM_all e   ==  1.0000000000  exactly (asserted; halts otherwise)

`e = pool_level(division) * _PL_F` exactly (`_b_factor == 1.0`, proven in the harvest), so this file
needs no engine run: it re-weights the harvested cells at whatever levels are handed to it.

CONTROL: run with `CHECKOUT` it must reproduce ORDER 21's published U table EXACTLY.

  usage: o22_uderive.py <ucells.json> <levels.json|CHECKOUT> <surface_in.json> <surface_out.json|-> [label]
"""
import sys, json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CELLS = json.load(open(sys.argv[1]))
LEVARG, SURF_IN, SURF_OUT = sys.argv[2], sys.argv[3], sys.argv[4]
LABEL = sys.argv[5] if len(sys.argv) > 5 else LEVARG
PL_F = float(CELLS['pl_f'])
WC = CELLS['cells']
S = json.load(open(SURF_IN))
PATHSURF = S['pathway']
PATHS = ['RD', 'ND>64', 'IRE', 'UNR', 'PDA', 'PDS', 'MSD', 'PDN', 'SSP']

CURPL = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['pool_levels']
CURVE = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))['curve']
CAPPK = int(CURPL['signed_nd65_plus']['cap_against_curve_pick'])
CAP = float(CURVE[str(CAPPK)])

if LEVARG == 'CHECKOUT':
    flat = dict(CURPL['signed_flat']); rd = dict(CURPL['signed_rd_positional'])
    nd65 = float(CURPL['signed_nd65_plus']['measured_k15'])
else:
    Lv = json.load(open(LEVARG))
    flat = dict(Lv['signed_flat']); rd = dict(Lv['signed_rd_positional'])
    nd65 = float(Lv['nd65_measured_k15'])

# THE ENGINE'S OWN LOOKUP, REPRODUCED: rl_model.py:1423-1427 -- int() truncation and the ND65+ cap law.
LEV = {k: int(float(v)) for k, v in flat.items()}
LEV['ND65+'] = int(min(nd65, CAP))
for k, v in rd.items():
    LEV['RD:' + k] = int(float(v))


def e_of(c):
    return LEV[c['div']] * PL_F


def R_of(c):
    return float(PATHSURF[c['stream']][c['cls']][min(max(c['d'], 1), 6) - 1])


P = print
P("=" * 110)
P("U RE-DERIVED   label=%s   surface=%s" % (LABEL, os.path.basename(SURF_IN)))
P("=" * 110)
P("  R carries UNCHANGED (it is a ratio). Only the entry weights move.")
P("  engine level lookup (int-truncated, ND65+ = min(stored, curve[%d]=%g)):" % (CAPPK, CAP))
P("    " + " · ".join("%s %d" % (k, LEV[k]) for k in sorted(LEV)))
P()
P("  %-9s %7s %8s %10s %12s %12s %18s" %
  ('pathway', 'cells', 'sitters', 'sit shr', 'mean R', 'U', 'post-redist mean'))
MP = {}
bad = []
for pw in PATHS + ['ALL POOL']:
    sub = WC if pw == 'ALL POOL' else [c for c in WC if c['stream'] == pw]
    tot = sitw = nonw = num = 0.0
    nsit = 0
    for c in sub:
        e = e_of(c); tot += e
        if c['sitout']:
            sitw += e; num += e * R_of(c); nsit += 1
        else:
            nonw += e
    U = (tot - num) / nonw if nonw > 0 else float('nan')
    mean = (num + nonw * U) / tot if tot > 0 else float('nan')
    meanR = num / sitw if sitw > 0 else float('nan')
    MP[pw] = dict(cells=len(sub), sitters=nsit, sit_share_w=sitw / tot, meanR=meanR, U=U, mean=mean,
                  sit_share_n=nsit / len(sub) if sub else 0.0)
    if abs(mean - 1.0) > 1e-9: bad.append(pw)
    P("  %-9s %7d %8d %10.4f %12.6f %12.6f %18.10f" % (pw, len(sub), nsit, sitw / tot, meanR, U, mean))
P()
P("  ASSERTION: pathways whose post-redistribution entry-weighted mean is not 1.0000000000: %d" % len(bad))
assert not bad, "MEAN-PRESERVATION FAILED on %s" % bad
P()

# The invariance result, DERIVED rather than asserted.
inv = [pw for pw in PATHS if len({c['div'] for c in WC if c['stream'] == pw}) == 1]
P("  PATHWAYS WHOSE `e` IS A SINGLE CONSTANT (one signed division => the level CANCELS out of U,")
P("  so their U CANNOT move when their own level moves): %s" % ", ".join(sorted(inv)))
P("  PATHWAYS WHOSE `e` VARIES WITHIN THE PATHWAY (U moves with the positional level mix): %s"
  % ", ".join(sorted(set(PATHS) - set(inv))))
P()

out = dict(S)
out['uplift'] = {pw: round(MP[pw]['U'], 10) for pw in PATHS}
out['mean_preserving'] = {pw: {k: (round(v, 10) if isinstance(v, float) else v)
                               for k, v in MP[pw].items()} for pw in MP}
out['_ORDER22_U'] = ("U RE-DERIVED at the ORDER 22 candidate levels (%s). R is unchanged from "
                     "ORDER 21's derivation -- it is a ratio and is calibration-independent." % LABEL)
if SURF_OUT != '-':
    json.dump(out, open(SURF_OUT, 'w'), indent=1, default=float)
    P("  wrote %s" % SURF_OUT)
