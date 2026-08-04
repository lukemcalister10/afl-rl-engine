#!/usr/bin/env python3
"""#306 L-A REVISED — m(pos, age, pick) AS A SMOOTH FIELD.  Design simulation on committed rows.

WHY THE FIRST DESIGN WAS WRONG, IN ONE LINE
  It read "constrained by construction" as "the lens must not vary with pick", and built m(pos, age)
  applied identically at every pick.  The defect in the OLD surface was never that the lens varied
  with pick -- it was that the variation was UNANCHORED AND UNBOUNDED, free to float 65% above the
  curve where evidence thinned.  Flattening it erased the intersections the project exists to measure.
  The owner's law is the specification:

      "A key defender at pick 6 may be, and probably should be, worth less than pick 6, but at pick 45,
       maybe it's worth more. It could be by lots, or not by much. It's that simple: we have the data."

THE CONSTRUCTION

    v0*(pos, age, pick)  =  anchor(pick)  x  m(pos, age, pick)

  m is a SMOOTH BOUNDED FIELD over the pick axis, one line per position and age, free to sit below the
  curve at one pick and above it at another, crossing wherever the data crosses.

  1. GRADED LOCALITY.  Every estimate is a kernel-weighted local one; influence decays smoothly with
     distance in log-pick and in draft age.  NO BUCKETS ON ANY AXIS -- not pick, not age.  The owner's
     ordering test is asserted numerically below: pick 9's rows must inform pick 7 MORE than pick 14's do.

  2. CONFIDENCE WEIGHTING, HIERARCHICAL.  Each local estimate is shrunk toward its broader value in
     proportion to how thin its own data is, by effective sample size:

         m  =  s0*L0 + (1-s0)*[ s1*L1 + (1-s1)*[ s2*L2 + (1-s2)*1.0 ] ]

         L0  (pos, age, pick) local     L1  (pos, pick) local, all ages
         L2  (pos) overall              1.0 the all-in slot value -- the anchor itself
         sk = n_eff_k / (n_eff_k + K)   n_eff = (SUM w)^2 / SUM w^2

     Dense data stands on its own; sparse data leans toward the all-in value and is never trusted with
     the full effect.  The mature-age dials are under this rule identically -- no special case.

  3. LOCAL NEUTRALITY -- totals preserved WITHIN THE NEIGHBOURHOOD, never by inflating the class.
     A smooth multiplier lam(pick) enforces, at every pick under the same locality kernel,

         SUM_i w_i * anchor_i * m_i * lam  ==  SUM_i w_i * anchor_i

     Neutrality is therefore LOCAL: a position sitting above the curve in a stretch is paid for by the
     others IN THAT STRETCH.  A global scalar would let the whole tail sit low to fund the head -- the
     cross-region borrowing this clause exists to forbid.

  4. BOUNDED.  m in [1/B, B] identically.  Neutrality and bound are iterated to a fixed point; where
     the bound binds, the bound wins and neutrality holds to a stated tolerance.

  5. PRESENTATION LAW.  Everything reported PER PICK.  No bands, anywhere, ever.

WHAT THIS IS NOT
  Not an engine fit and not an acceptance.  Target values are the committed matrix's `v0` -- the CURRENT
  surface's own output, the best cell-level proxy the committed evidence carries.  The engine fits from
  `_v0_raw` (pre-curve), so the fitted numbers will differ; what is being audited here is the FIELD'S
  SHAPE and the laws it obeys.  Nothing here is a gated or predicted G-Y0 (Acceptance 4).

    python3 lens_field_sim.py
"""
import json, hashlib, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
MATRIX = os.path.join(REPO, 'docs/evidence/rehearsal_290_2026-07-31/L6_convergence/pass0_matrix.json')
CURVE = os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')
MATRIX_MD5, CURVE_PAYLOAD = '9c4bca53b738452739c353d94fe99928', 'e69a3f38'

# ---- DESIGN CONSTANTS, stated here and in the artifact's record (N30). Fixed before the field was seen.
H_PICK = 0.35    # locality bandwidth in LOG-pick. Chosen so neighbours dominate: at pick 7, pick 9 carries
                 # ~0.77 weight and pick 14 ~0.14 -- the owner's ordering, asserted numerically below.
H_AGE = 1.5      # locality bandwidth in draft-age YEARS. Smooth across age; no age buckets.
K_CONF = 25.0    # confidence half-weight: n_eff = K_CONF gives the level half its own say.
B = 2.00         # m in [0.50, 2.00], held identically.
TOL = 0.005      # local-neutrality tolerance.
PICKS = list(range(1, 65))


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def payload_md5(c):
    return hashlib.md5(json.dumps({str(k): int(round(v)) for k, v in c.items()},
                                  sort_keys=True).encode()).hexdigest()[:8]


def main():
    got = md5(MATRIX)
    if got != MATRIX_MD5:
        raise SystemExit('HALT: pass0_matrix.json is %s, pinned %s.' % (got, MATRIX_MD5))
    curve = json.load(open(CURVE))['curve']
    gotp = payload_md5(curve)
    if gotp != CURVE_PAYLOAD:
        raise SystemExit('HALT: installed curve payload %s, expected %s.' % (gotp, CURVE_PAYLOAD))
    C = {int(k): float(v) for k, v in curve.items()}
    recs = json.load(open(MATRIX))['recs']
    rows = [r for r in recs if r.get('teaches_curve') and r.get('v0') is not None
            and r.get('pick') is not None and 1 <= r['pick'] <= 64]
    for r in rows:
        r['_lp'] = math.log(r['pick']); r['_a'] = C[r['pick']]
        r['_ag'] = float(r.get('age_draft') if r.get('age_draft') is not None else 18)
    POS = sorted({r['pos'] for r in rows if r.get('pos')})
    AGES = sorted({int(r['_ag']) for r in rows})

    def kern(d, h): return math.exp(-0.5 * (d / h) ** 2)

    def est(sub, lp=None, ag=None):
        """value-weighted local lens + its effective sample size."""
        sw = swa = swv = sw2 = 0.0
        for r in sub:
            w = 1.0
            if lp is not None: w *= kern(r['_lp'] - lp, H_PICK)
            if ag is not None: w *= kern(r['_ag'] - ag, H_AGE)
            if w < 1e-12: continue
            sw += w; sw2 += w * w; swa += w * r['_a']; swv += w * r['v0']
        if swa <= 0: return 1.0, 0.0
        return swv / swa, (sw * sw / sw2 if sw2 > 0 else 0.0)

    bypos = {p: [r for r in rows if r.get('pos') == p] for p in POS}
    L2 = {p: est(bypos[p])[0] for p in POS}
    n2 = {p: est(bypos[p])[1] for p in POS}

    def shrink(v, n, toward):
        s = n / (n + K_CONF)
        return s * v + (1 - s) * toward

    # ---- the raw field, before neutrality
    pre = {}
    for p in POS:
        l2 = shrink(L2[p], n2[p], 1.0)
        for pk in PICKS:
            lp = math.log(pk)
            v1, k1 = est(bypos[p], lp=lp)
            l1 = shrink(v1, k1, l2)
            for ag in AGES:
                v0, k0 = est(bypos[p], lp=lp, ag=float(ag))
                pre[(p, ag, pk)] = shrink(v0, k0, l1)

    # ---- LOCAL neutrality: lam(pick) under the same kernel; iterate with the bound to a fixed point
    lam = {pk: 1.0 for pk in PICKS}
    m = {}
    for _ in range(60):
        for k in pre: m[k] = min(B, max(1.0 / B, pre[k] * lam[k[2]]))
        worst = 0.0
        for pk in PICKS:
            lp = math.log(pk)
            num = den = 0.0
            for r in rows:
                w = kern(r['_lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['_a']
                den += w * r['_a'] * m[(r['pos'], int(r['_ag']), r['pick'])]
            if den > 0:
                ratio = num / den
                lam[pk] *= ratio
                worst = max(worst, abs(1.0 / ratio - 1.0))
        if worst <= 1e-10: break
    for k in pre: m[k] = min(B, max(1.0 / B, pre[k] * lam[k[2]]))

    # ---- the realised, population-weighted lens at each pick, per position (per-pick, no bands)
    percurve = {}
    for p in POS:
        percurve[p] = {}
        for pk in PICKS:
            lp = math.log(pk)
            num = den = 0.0
            for r in bypos[p]:
                w = kern(r['_lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['_a'] * m[(p, int(r['_ag']), r['pick'])]; den += w * r['_a']
            percurve[p][pk] = (num / den) if den > 0 else None

    # ---- local neutrality achieved, per pick
    neut = {}
    for pk in PICKS:
        lp = math.log(pk); num = den = 0.0
        for r in rows:
            w = kern(r['_lp'] - lp, H_PICK)
            if w < 1e-12: continue
            num += w * r['_a'] * m[(r['pos'], int(r['_ag']), r['pick'])]; den += w * r['_a']
        neut[pk] = (num / den) if den > 0 else None

    # ---- the owner's ordering test, asserted numerically
    w9 = kern(math.log(9) - math.log(7), H_PICK); w14 = kern(math.log(14) - math.log(7), H_PICK)

    # ---- mature-age dials under the SAME rule: per-pick lens by draft age, position-pooled view
    matcurve = {}
    for ag in [a for a in AGES if a >= 19]:
        matcurve[ag] = {}
        for pk in PICKS:
            lp = math.log(pk); num = den = 0.0
            for r in rows:
                if int(r['_ag']) != ag: continue
                w = kern(r['_lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['_a'] * m[(r['pos'], ag, r['pick'])]; den += w * r['_a']
            matcurve[ag][pk] = (num / den) if den > 0 else None

    # ---- CONFIDENCE, reported beside every estimate. "Our best, most honest guess based on the
    #      information OR LACK THEREOF available" is only auditable if the lack is visible too.
    conf = {}
    for p in POS:
        conf[p] = {}
        for pk in PICKS:
            _, k1 = est(bypos[p], lp=math.log(pk))
            conf[p][pk] = {'n_eff': round(k1, 2), 'own_say': round(k1 / (k1 + K_CONF), 3)}

    binds = sum(1 for k in m if abs(m[k] - B) < 1e-9 or abs(m[k] - 1.0 / B) < 1e-9)
    bindpos = {}
    for k in m:
        if abs(m[k] - B) < 1e-9 or abs(m[k] - 1.0 / B) < 1e-9:
            bindpos[k[0]] = bindpos.get(k[0], 0) + 1
    out = {'what': 'DESIGN SIMULATION of m(pos,age,pick) as a smooth bounded field, on committed rows',
           'NOT_AN_ACCEPTANCE': 'target is the committed matrix v0 (the current surface output) as a '
                                'cell-level proxy; the engine fits from _v0_raw. Shape is what is audited. '
                                'Nothing here is a gated or predicted G-Y0.',
           'PRESENTATION': 'per-pick only. No bands on any axis, in the model or in this output.',
           'constants': {'h_pick_logunits': H_PICK, 'h_age_years': H_AGE, 'confidence_half_weight': K_CONF,
                         'B': B, 'neutrality_tolerance': TOL},
           'locality_ordering_test': {'weight_of_pick9_at_pick7': round(w9, 4),
                                      'weight_of_pick14_at_pick7': round(w14, 4),
                                      'ordering_holds': w9 > w14},
           'anchor_curve_payload': gotp, 'matrix_md5': got, 'rows': len(rows),
           'lens_per_pick_by_position': {p: {str(k): (round(v, 4) if v is not None else None)
                                             for k, v in percurve[p].items()} for p in POS},
           'lens_per_pick_by_draft_age_mature': {str(a): {str(k): (round(v, 4) if v is not None else None)
                                                          for k, v in matcurve[a].items()} for a in matcurve},
           'local_neutrality_per_pick': {str(k): (round(v, 6) if v is not None else None)
                                         for k, v in neut.items()},
           'bound_binding_cells': binds, 'bound_binds_by_position': bindpos, 'cells': len(m),
           'confidence_per_pick_by_position': {p: {str(k): conf[p][k] for k in conf[p]} for p in POS}}
    with open(os.path.join(HERE, 'lens_field_sim.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print(out['NOT_AN_ACCEPTANCE'])
    print(out['PRESENTATION'] + '\n')
    print('constants  h_pick %.2f (log units) · h_age %.1f yr · confidence half-weight n_eff=%.0f · B %.2f'
          % (H_PICK, H_AGE, K_CONF, B))
    print("locality ordering (owner's test): pick 9 informs pick 7 with weight %.4f; pick 14 with %.4f  -> %s\n"
          % (w9, w14, 'HOLDS' if w9 > w14 else 'FAILS'))
    print('THE LENS, PER PICK, BY POSITION   (1.000 = exactly the pick\'s all-in value)')
    print('  pick  ' + '  '.join('%7s' % p for p in POS) + '     local-neutrality')
    for pk in PICKS:
        cells = '  '.join(('%7.3f' % percurve[p][pk]) if percurve[p][pk] is not None else '      —'
                          for p in POS)
        print('  %4d  %s        %.6f' % (pk, cells, neut[pk]))
    print('\nMATURE DIALS, PER PICK, BY DRAFT AGE (same confidence rule, no special case)')
    ages = sorted(matcurve)
    print('  pick  ' + '  '.join('%7s' % ('age%d' % a) for a in ages))
    for pk in PICKS[::4] + [64]:
        print('  %4d  ' % pk + '  '.join(('%7.3f' % matcurve[a][pk]) if matcurve[a][pk] is not None
                                         else '      —' for a in ages))
    nv = [v for v in neut.values() if v is not None]
    print('\nlocal neutrality: worst |ratio-1| across all 64 picks = %.2e   (tolerance %.1f%%)  -> %s'
          % (max(abs(v - 1) for v in nv), 100 * TOL,
             'HOLDS AT EVERY PICK' if max(abs(v - 1) for v in nv) <= TOL else 'FAILS'))
    print('bound binds in %d of %d (pos,age,pick) cells   by position: %s'
          % (binds, len(m), ', '.join('%s %d' % (k, v) for k, v in sorted(bindpos.items()))))
    print('\nCONFIDENCE — how much say each position\'s OWN local data gets at each pick')
    print('  (own_say = n_eff/(n_eff+%.0f); the remainder is borrowed from the broader value)' % K_CONF)
    print('  pick  ' + '  '.join('%13s' % p for p in POS))
    for pk in PICKS[::6] + [64]:
        print('  %4d  ' % pk + '  '.join('%6.1f/%5.2f' % (conf[p][pk]['n_eff'], conf[p][pk]['own_say'])
                                         for p in POS))
    print('\nwrote lens_field_sim.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
