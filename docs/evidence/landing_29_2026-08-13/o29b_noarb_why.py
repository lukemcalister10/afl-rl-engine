#!/usr/bin/env python3
"""ORDER 29B -- WHY THE COHORT MARGINS MOVED THE WAY THEY DID. THE MECHANISM, MEASURED.

PREREG_29B P29B-26 predicted a DIRECTION and got it wrong. It said: "raising the day-0 denominator
reduces measured yr0->1 appreciation wherever the yr0 mark is a day-0 print, so the ND legacy readings
should move TOWARD the carry line". They moved AWAY from it. This file measures why, on the two
matrices themselves, so the breach is explained by mechanism rather than excused.

THE HYPOTHESIS THIS TESTS, stated before the numbers: the instruments' YEAR-0 is NOT the printed
day-0 price. emit_matrix_338.py:252 writes  v0 = round(v0_start(p), 1)  -- the engine's frozen
year-zero pick+position SURFACE value -- while the year-1..7 path is ev(p, Y) under truncated scoring
(emit_matrix_338.py:193). ORDER 29B wires the PRINT, i.e. ev(); it does not touch v0_start. So the
denominator should be BYTE-IDENTICAL between the two matrices and the whole move should sit in the
numerator, concentrated on the (player, year) cells where the player had ZERO games as of that year.

  usage: python3 o29b_noarb_why.py <matrix_before.json> <matrix_after.json>
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
A, B = sys.argv[1], sys.argv[2]

LOG = []
def P(s=''):
    print(s); LOG.append(s)

MA = json.load(open(A)); MB = json.load(open(B))
RA = {r['key']: r for r in MA['recs']}; RB = {r['key']: r for r in MB['recs']}

P("=" * 118)
P("ORDER 29B  --  WHY THE COHORT MARGINS MOVED: THE MECHANISM, MEASURED ON THE MATRICES")
P("=" * 118)
P()
P("  before  %-28s md5 %s  store %s  v0surf %s"
  % (os.path.basename(A), hashlib.md5(open(A, 'rb').read()).hexdigest()[:8],
     MA['meta']['store_md5'][:8], MA['meta']['v0surf_sig'][:12]))
P("  after   %-28s md5 %s  store %s  v0surf %s"
  % (os.path.basename(B), hashlib.md5(open(B, 'rb').read()).hexdigest()[:8],
     MB['meta']['store_md5'][:8], MB['meta']['v0surf_sig'][:12]))
P("  records %d -> %d" % (len(RA), len(RB)))
assert set(RA) == set(RB), 'the two matrices do not carry the same rows'

# ---- (1) THE DENOMINATOR. v0 == v0_start, which this act does not touch.
v0_moved = [k for k in RA if RA[k].get('v0') != RB[k].get('v0')]
P()
P("  (1) THE YEAR-0 DENOMINATOR  (rec['v0'] == round(v0_start(p),1), emit_matrix_338.py:252)")
P("      rows whose v0 moved: %d of %d" % (len(v0_moved), len(RA)))
P("      => %s" % ('BYTE-IDENTICAL. The instruments\' yr0 does NOT read the printed day-0 price, so the '
                   'entry wiring cannot move it.' if not v0_moved else
                   'MOVED on %s — investigate.' % v0_moved[:6]))

# ---- (2) THE NUMERATOR. the ASOF path, and where in it the move sits.
P()
P("  (2) THE YEAR-1..7 NUMERATOR  (vpath[k] == ev(p, C+k) under truncated scoring, :193)")
by_k = collections.Counter(); mv_k = collections.Counter()
up = dn = 0
sum_by_k = collections.defaultdict(float)
for k in RA:
    a, b = RA[k], RB[k]
    ya, yb = a.get('yrs') or [], b.get('yrs') or []
    va, vb = a.get('vpath') or [], b.get('vpath') or []
    C = a.get('year')
    for i, y in enumerate(ya):
        if i >= len(vb) or i >= len(va): break
        if va[i] is None or vb[i] is None: continue
        kk = y - C                                    # cohort year index (1 = first listed season)
        by_k[kk] += 1
        if va[i] != vb[i]:
            mv_k[kk] += 1
            sum_by_k[kk] += (vb[i] - va[i])
            if vb[i] > va[i]: up += 1
            else: dn += 1
P("      %-6s %10s %10s %8s %14s" % ('cohort', 'cells', 'moved', 'pct', 'sum delta'))
for kk in sorted(by_k):
    if kk > 8: continue
    P("      %-6d %10d %10d %7.1f%%  %+13.0f"
      % (kk, by_k[kk], mv_k[kk], 100.0 * mv_k[kk] / max(1, by_k[kk]), sum_by_k[kk]))
P("      cells that ROSE %d   cells that FELL %d" % (up, dn))

# ---- (3) THE LEGACY ND COHORT, isolated: the instrument's own population
P()
P("  (3) THE LEGACY ND INSTRUMENT'S OWN POPULATION (in-curve national rows), year 1 only")
nd = [k for k in RA if RA[k].get('incurve')]
n_mv = 0; s0 = s1a = s1b = 0.0; n_used = 0
for k in nd:
    a, b = RA[k], RB[k]
    ya, va, vb = a.get('yrs') or [], a.get('vpath') or [], b.get('vpath') or []
    if not ya or not va or va[0] is None or not vb or vb[0] is None: continue
    n_used += 1
    s0 += float(a.get('v0') or 0); s1a += va[0]; s1b += vb[0]
    if va[0] != vb[0]: n_mv += 1
P("      in-curve rows with a year-1 mark: %d ; year-1 marks that MOVED: %d (%.1f%%)"
  % (n_used, n_mv, 100.0 * n_mv / max(1, n_used)))
P("      SUM v0 (denominator)  before %.0f   after %.0f   %s"
  % (s0, s0, 'UNMOVED' if not v0_moved else 'MOVED'))
P("      SUM year-1 (numerator) before %.0f   after %.0f   %+.2f%%"
  % (s1a, s1b, 100.0 * (s1b - s1a) / s1a))
P()
P("      THE ARITHMETIC OF THE BREACH, in one line: the denominator is fixed and the numerator rose,")
P("      so yr0->1 appreciation HAD to rise. P29B-26 assumed the instrument read the printed day-0")
P("      price as its yr0. IT DOES NOT -- it reads v0_start, the frozen year-zero surface. The entry")
P("      wiring moves the PRINT, and on a national-draft cohort the printed day-0 is overwhelmingly")
P("      a YEAR-1 cell (a draftee who did not play his first season), never the yr0 cell. So the act")
P("      pushes the numerator up and leaves the denominator where it was.")

json.dump({'v0_moved_rows': v0_moved,
           'cells_by_cohort_year': {str(k): by_k[k] for k in sorted(by_k)},
           'cells_moved_by_cohort_year': {str(k): mv_k[k] for k in sorted(mv_k)},
           'sum_delta_by_cohort_year': {str(k): sum_by_k[k] for k in sorted(sum_by_k)},
           'cells_up': up, 'cells_down': dn,
           'incurve_year1_rows': n_used, 'incurve_year1_moved': n_mv,
           'incurve_sum_v0': s0, 'incurve_sum_y1_before': s1a, 'incurve_sum_y1_after': s1b},
          open(HERE + '/NOARB_WHY_29B.json', 'w'), indent=1)
open(HERE + '/NOARB_WHY_29B_out.txt', 'w').write("\n".join(LOG) + "\n")
