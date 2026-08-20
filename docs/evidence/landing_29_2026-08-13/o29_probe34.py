#!/usr/bin/env python3
"""ORDER 29 -- the v3.4 KERNEL-CURVE PROBE.

Imports the engine in a staged workspace and dumps, as JSON, everything the unflag-three can reach
through the engine's OWN curve (as distinct from the ORDER-28 derivation lane, which never read the
flags):

  * build_pvc_v34()          -- the pre-anchor kernel curve, picks 1..99
  * PVC[1]                   -- the pre-anchor head that BOARD_FACTOR divides by
  * BOARD_FACTOR, SCALE      -- the player-side scalars
  * _NUM                     -- the numeraire block as _load_numeraire returned it
  * the slide-up state       -- every ND-2011 row's stored pick, effective pick and slid _pvc_eff
  * the +-4 curve-sample     -- the row keys build_pvc_v34 actually consumed at each pick 1..64

Run INSIDE the staged workspace (cwd = <ws>/rl_after), with the same pinned environment as a board
build.  Writes its JSON to the path given as argv[1].
"""
import os, sys, json

sys.path.insert(0, os.getcwd())
import rl_model as MA

out = {}

# ---------------------------------------------------------------------------------------------
# THE SCALE HAZARD, AND HOW THIS PROBE CLOSES IT.
#
# rl_model.py:1371 reassigns the module global SCALE  ( SCALE = SCALE * BOARD_FACTOR )  immediately
# after BOARD_FACTOR is computed.  build_pvc_v34() reaches SCALE through _nv_bwd -> posval, so simply
# calling it again after import returns the curve ALREADY MULTIPLIED BY BOARD_FACTOR -- not the
# pre-anchor curve.  Measured, on the first version of this probe: the recomputed head read 2983
# where the true pre-anchor head is 3917, i.e. exactly the BOARD_FACTOR 0.7613 contamination.
#
# So SCALE is restored to its pre-anchor value before the curve is recomputed, and the result is
# CHECKED against an identity that does not depend on this probe being right:
#
#       BOARD_FACTOR = (_P1 / H) * s        =>        H = _P1 * s / BOARD_FACTOR
#
# _P1, s and BOARD_FACTOR are all read straight off the imported module, so the right-hand side is
# the head the ENGINE ITSELF used.  If the recomputed head disagrees with it, the probe halts rather
# than publishing a contaminated curve.
# ---------------------------------------------------------------------------------------------
H_exact = MA._P1 * MA._NUM['s'] / MA.BOARD_FACTOR          # the head the engine actually divided by
MA.SCALE = MA.SCALE / MA.BOARD_FACTOR                      # undo the line-1371 reassignment

pvc34 = MA.build_pvc_v34()
out['pvc34'] = {str(k): v for k, v in sorted(pvc34.items())}
out['pvc34_head'] = pvc34[1]
out['pvc34_head_exact_from_identity'] = H_exact
assert abs(pvc34[1] - H_exact) < 0.5, (
    "PROBE HALT: recomputed pre-anchor head %r disagrees with the engine's own head %.6f "
    "(_P1*s/BOARD_FACTOR). The SCALE restoration did not reproduce the import-time state, so this "
    "curve is not the one the engine built." % (pvc34[1], H_exact))
out['BOARD_FACTOR'] = MA.BOARD_FACTOR
out['SCALE'] = MA.SCALE
out['NUM'] = MA._NUM
out['P1'] = MA._P1
out['CURVE_H'] = MA.CURVE_H

# ---- the slide-up state, per ND-2011 row (curve attribution only; stored pick untouched)
nd11 = []
for p in MA.hist:
    if p.get('_grp') == 'ND' and p.get('year') == 2011:
        nd11.append({'key': p.get('key'), 'pick': p.get('pick'),
                     'effpk': MA.effpk(p), 'pvc_eff': p.get('_pvc_eff'),
                     'epk': MA._epk(p), 'in_pvc': MA._in_pvc(p),
                     'excluded': bool(p.get('_pvc_exclude')),
                     'teaches': bool(MA._teaches_curve(p))})
out['nd2011'] = sorted(nd11, key=lambda r: (r['pick'] is None, r['pick']))
out['nd2011_n'] = len(nd11)

# ---- the rows build_pvc_v34 consumed at each pick (its registered +-4 sample)
samp = MA._CURVE_SAMPLES.get('build_pvc_v34', {})
out['sample_keys'] = {str(k): sorted([r.get('key') for r in rows])
                      for k, rows in sorted(samp.items()) if k <= 64}
out['sample_n'] = {str(k): len(rows) for k, rows in sorted(samp.items()) if k <= 64}

# ---- the shipped curve as the engine finally holds it (artifact-sourced), for completeness
out['PVC_shipped'] = {str(k): MA.PVC[k] for k in sorted(MA.PVC) if isinstance(k, int) and k <= 64}

json.dump(out, open(sys.argv[1], 'w'), indent=1, sort_keys=False, default=str)
print("PROBE OK  head=%s  BOARD_FACTOR=%.12f  s=%.16f" % (out['pvc34_head'], out['BOARD_FACTOR'], out['NUM']['s']))
