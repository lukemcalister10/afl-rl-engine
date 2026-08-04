#!/usr/bin/env python3
"""#306 L-A — THE LENS ON THE SIBLING BASIS.  m(pos, age, pick) fit from #279 STRUCTURAL CAREER VALUES.

THE BASIS CHANGE THIS SCRIPT EXISTS FOR
  Every earlier version of this lens fit from the year-zero surface's own slot prior -- the
  self-referential lineage #279 measured at 0.0248% reality ("curve -> surface -> v0 -> curve").
  That target is BARRED.  The lens now fits from the same structural career values the RULED CURVE
  is built from: the positional lens and the curve are siblings, priced the same way, from outcomes.

      "We're looking at pick 4, and seeing what it'd be worth if it was a defender, midfielder,
       key forward etc. based on outcomes."

  The #279 machinery is REUSED, NEVER REINVENTED: `harness_pvc.structural_values()` on
  `harness_pvc.load_matrix()`'s population, imported from session_2026-07-30/item279/panel.
  Inherited wholesale and unmodified: class window 2004-2022 hard cut · concluded careers realized in
  full · never-established at 0.0 · active careers completed by concluded look-alikes (position x
  tenure strata, busts' zero remainders included, min stratum 20) · the model prior ONLY as a COUNTED
  fallback · McCartin/Boyd exclusions and one-pick slides as the committed matrix carries them ·
  VOR denomination.  The harness asserts its own committed identity (store 6b9d00a7, v0surf
  b781ed253bff, N=1197) and refuses an empty or wrong population.

  ANCHOR: the ruled ladder e69a3f38 (N6/N34), picks 1-64, asserted by its N32 PAYLOAD identity.

INHERITED WART, CARRIED OPENLY AND NEVER SILENTLY CORRECTED (the #279 posture)
  The completion method back-tests +4.7% to +8.4% OPTIMISTIC, touching 25.1% of the teaching rows.
  It rides the shared basis. It is printed beside every result in this file.

THE FIELD -- unchanged from the audited design, only its raw material moves
  smooth bounded field on every axis · graded locality (pick 9 informs pick 7 more than pick 14 does)
  · hierarchical confidence with the lack made visible · m in [0.5, 2.0] · local neutrality under the
  kernel at every pick · NO HARD BANDS ANYWHERE, in the model or in this output · per-pick only ·
  no-data regions faded and named.

NOT AN ENGINE FIT AND NOT AN ACCEPTANCE.  Design measurement on committed rows, for the seam's audit.
Nothing here is a gated or predicted G-Y0 (Acceptance 4).

    python3 lens_sibling_basis.py
"""
import json, hashlib, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PANEL = os.path.join(REPO, 'session_2026-07-30/item279/panel')
MATRIX279 = os.path.join(REPO, 'session_2026-07-30/item279/out/per_entrant_279_vor.json')
CURVE = os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')
CURVE_PAYLOAD = 'e69a3f38'
OPTIMISM = '+4.7% to +8.4% (completion method, touching 25.1% of teaching rows) — inherited, reported, never silently corrected'

H_PICK, H_AGE, K_CONF, B, TOL = 0.35, 1.5, 25.0, 2.00, 0.005
PICKS = list(range(1, 65))
FADE_NEFF = 5.0     # below this effective sample the estimate is NAMED as data-starved in the output


def payload_md5(c):
    return hashlib.md5(json.dumps({str(k): int(round(v)) for k, v in c.items()},
                                  sort_keys=True).encode()).hexdigest()[:8]


def main():
    sys.path.insert(0, PANEL)
    import harness_pvc as H

    curve = json.load(open(CURVE))['curve']
    gotp = payload_md5(curve)
    if gotp != CURVE_PAYLOAD:
        raise SystemExit('HALT: anchor payload %s, expected %s — reconstruct the substrate.'
                         % (gotp, CURVE_PAYLOAD))
    C = {int(k): float(v) for k, v in curve.items()}

    meta, ND = H.load_matrix(MATRIX279)          # asserts store/v0surf identity and N==1197
    vals, prov = H.structural_values(ND)         # the #279 structural career values, unmodified
    byk = {r['key']: r for r in ND}

    rows = []
    for v in vals:
        r = byk[v['key']]
        pk = int(v['pick'])
        if not (1 <= pk <= 64):
            continue
        rows.append({'pos': r.get('pos'), 'ag': float(r.get('age_draft') if r.get('age_draft')
                                                      is not None else 18),
                     'pick': pk, 'lp': math.log(pk), 'a': C[pk], 'val': float(v['value']),
                     'how': v['how']})
    POS = sorted({r['pos'] for r in rows if r['pos']})
    AGES = sorted({int(r['ag']) for r in rows})

    def kern(d, h): return math.exp(-0.5 * (d / h) ** 2)

    def est(sub, lp=None, ag=None):
        sw = sw2 = swa = swv = 0.0
        for r in sub:
            w = 1.0
            if lp is not None: w *= kern(r['lp'] - lp, H_PICK)
            if ag is not None: w *= kern(r['ag'] - ag, H_AGE)
            if w < 1e-12: continue
            sw += w; sw2 += w * w; swa += w * r['a']; swv += w * r['val']
        if swa <= 0: return 1.0, 0.0
        return swv / swa, (sw * sw / sw2 if sw2 > 0 else 0.0)

    bypos = {p: [r for r in rows if r['pos'] == p] for p in POS}
    L2 = {p: est(bypos[p]) for p in POS}

    def shrink(v, n, toward):
        s = n / (n + K_CONF)
        return s * v + (1 - s) * toward

    pre, neff1 = {}, {}
    for p in POS:
        l2 = shrink(L2[p][0], L2[p][1], 1.0)
        for pk in PICKS:
            lp = math.log(pk)
            v1, k1 = est(bypos[p], lp=lp); neff1[(p, pk)] = k1
            l1 = shrink(v1, k1, l2)
            for ag in AGES:
                v0, k0 = est(bypos[p], lp=lp, ag=float(ag))
                pre[(p, ag, pk)] = shrink(v0, k0, l1)

    lam = {pk: 1.0 for pk in PICKS}; m = {}
    for _ in range(80):
        for k in pre: m[k] = min(B, max(1.0 / B, pre[k] * lam[k[2]]))
        worst = 0.0
        for pk in PICKS:
            lp = math.log(pk); num = den = 0.0
            for r in rows:
                w = kern(r['lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['a']; den += w * r['a'] * m[(r['pos'], int(r['ag']), r['pick'])]
            if den > 0:
                ratio = num / den; lam[pk] *= ratio; worst = max(worst, abs(1.0 / ratio - 1.0))
        if worst <= 1e-10: break
    for k in pre: m[k] = min(B, max(1.0 / B, pre[k] * lam[k[2]]))

    percurve, neut = {}, {}
    for p in POS:
        percurve[p] = {}
        for pk in PICKS:
            lp = math.log(pk); num = den = 0.0
            for r in bypos[p]:
                w = kern(r['lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['a'] * m[(p, int(r['ag']), r['pick'])]; den += w * r['a']
            percurve[p][pk] = (num / den) if den > 0 else None
    for pk in PICKS:
        lp = math.log(pk); num = den = 0.0
        for r in rows:
            w = kern(r['lp'] - lp, H_PICK)
            if w < 1e-12: continue
            num += w * r['a'] * m[(r['pos'], int(r['ag']), r['pick'])]; den += w * r['a']
        neut[pk] = (num / den) if den > 0 else None

    matcurve = {}
    for ag in [a for a in AGES if a >= 19]:
        matcurve[ag] = {}
        for pk in PICKS:
            lp = math.log(pk); num = den = 0.0
            for r in rows:
                if int(r['ag']) != ag: continue
                w = kern(r['lp'] - lp, H_PICK)
                if w < 1e-12: continue
                num += w * r['a'] * m[(r['pos'], ag, r['pick'])]; den += w * r['a']
            matcurve[ag][pk] = (num / den) if den > 0 else None

    sv = sum(r['val'] for r in rows); sa = sum(r['a'] for r in rows)
    w9, w14 = kern(math.log(9) - math.log(7), H_PICK), kern(math.log(14) - math.log(7), H_PICK)
    binds = {}
    for k in m:
        if abs(m[k] - B) < 1e-9 or abs(m[k] - 1.0 / B) < 1e-9:
            binds[k[0]] = binds.get(k[0], 0) + 1
    starved = {p: [pk for pk in PICKS if neff1[(p, pk)] < FADE_NEFF] for p in POS}

    out = {'what': 'm(pos,age,pick) fit from #279 STRUCTURAL CAREER VALUES against the ruled anchor',
           'BASIS': 'harness_pvc.structural_values() on load_matrix(); the surface slot prior is BARRED '
                    'as a fit target and appears only as #279\'s own counted fallback',
           'OPTIMISM_CARRIED': OPTIMISM,
           'PRESENTATION': 'per-pick only. No bands on any axis, in the model or in this output.',
           'NOT_AN_ACCEPTANCE': 'design measurement on committed rows; not an engine fit; nothing here '
                                'is a gated or predicted G-Y0',
           'identity': {'store': meta['store_md5'], 'v0surf_sig': meta['v0surf_sig'][:12],
                        'nd_rows': len(ND), 'anchor_payload': gotp},
           'provenance_279': prov,
           'constants': {'h_pick_logunits': H_PICK, 'h_age_years': H_AGE,
                         'confidence_half_weight': K_CONF, 'B': B, 'neutrality_tolerance': TOL,
                         'fade_neff_threshold': FADE_NEFF},
           'locality_ordering_test': {'w_pick9_at_pick7': round(w9, 4),
                                      'w_pick14_at_pick7': round(w14, 4), 'holds': w9 > w14},
           'basis_level_vs_anchor': {'sum_structural': round(sv, 1), 'sum_anchor': round(sa, 1),
                                     'ratio': round(sv / sa, 6), 'gap_pct': round(100 * (sv / sa - 1), 3)},
           'lens_per_pick_by_position': {p: {str(k): (round(v, 4) if v is not None else None)
                                             for k, v in percurve[p].items()} for p in POS},
           'lens_per_pick_by_draft_age_mature': {str(a): {str(k): (round(v, 4) if v is not None else None)
                                                          for k, v in matcurve[a].items()} for a in matcurve},
           'confidence_per_pick_by_position': {p: {str(pk): {'n_eff': round(neff1[(p, pk)], 2),
                                                             'own_say': round(neff1[(p, pk)] / (neff1[(p, pk)] + K_CONF), 3)}
                                                   for pk in PICKS} for p in POS},
           'data_starved_picks_neff_below_%g' % FADE_NEFF: starved,
           'local_neutrality_per_pick': {str(k): (round(v, 6) if v is not None else None)
                                         for k, v in neut.items()},
           'bound_binds_by_position': binds, 'cells': len(m)}
    with open(os.path.join(HERE, 'lens_sibling_basis.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print('BASIS  #279 structural career values · store %s · v0surf %s · ND %d rows (classes 2004-2022)'
          % (meta['store_md5'], meta['v0surf_sig'][:12], len(ND)))
    print('       provenance: %s  (fallback %.3f%% — COUNTED, never silent)'
          % (prov['counts'], prov['fallback_share_pct']))
    print('       OPTIMISM CARRIED: %s' % OPTIMISM)
    print('ANCHOR the ruled ladder %s · picks 1-64' % gotp)
    print('       structural total vs anchor total: %.4f  (%+.3f%%)  <- the basis level, not an acceptance'
          % (sv / sa, 100 * (sv / sa - 1)))
    print('       locality: pick 9 informs pick 7 at %.4f, pick 14 at %.4f -> %s'
          % (w9, w14, 'HOLDS' if w9 > w14 else 'FAILS'))
    print('       per-pick only. No bands anywhere.\n')
    print("THE LENS, PER PICK, BY POSITION — what a pick is worth AS that position (1.000 = the pick's all-in value)")
    print('  pick  ' + '  '.join('%7s' % p for p in POS) + '     local-neutrality')
    for pk in PICKS:
        cells = []
        for p in POS:
            v = percurve[p][pk]
            if v is None: cells.append('      —'); continue
            cells.append(('%7.3f' % v) + ('*' if neff1[(p, pk)] < FADE_NEFF else ' '))
        print('  %4d  %s      %.6f' % (pk, ' '.join(cells), neut[pk]))
    print("  * = data-starved at that pick (n_eff < %g): the estimate is mostly the all-in value, not its own" % FADE_NEFF)
    print('\nMATURE DIALS, PER PICK, BY DRAFT AGE (same confidence rule, no special case)')
    ages = sorted(matcurve)
    print('  pick  ' + '  '.join('%7s' % ('age%d' % a) for a in ages))
    for pk in PICKS[::6] + [64]:
        print('  %4d  ' % pk + '  '.join(('%7.3f' % matcurve[a][pk]) if matcurve[a][pk] is not None
                                         else '      —' for a in ages))
    nv = [v for v in neut.values() if v is not None]
    print('\nlocal neutrality: worst |ratio-1| over all 64 picks = %.2e (tolerance %.1f%%) -> %s'
          % (max(abs(v - 1) for v in nv), 100 * TOL,
             'HOLDS AT EVERY PICK' if max(abs(v - 1) for v in nv) <= TOL else 'FAILS'))
    print('bound binds: %s' % (', '.join('%s %d' % kv for kv in sorted(binds.items())) or 'nowhere'))
    print('\nwrote lens_sibling_basis.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
