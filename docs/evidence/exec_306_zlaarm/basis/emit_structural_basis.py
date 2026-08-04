#!/usr/bin/env python3
"""#306 L-A — EMIT THE LENS BASIS as a DECLARED INPUT ARTIFACT.  (Approval clause 1.)

THE CLAUSE THIS EXISTS FOR — the owner's live-and-breathe steer:

    "I'd like this whole system to be more flexible and dynamic. One change to one piece should
     [not] require an entire redesign and rebake. It should live and breathe as best as possible."

  So the engine's lens fit does NOT recompute the basis and does NOT carry it in code.  It CONSUMES
  this artifact as a declared input, beside the anchor ladder.  When the replacement bars move (#270),
  or the class window moves, or the completion method changes, the chain is RE-RUN and the artifact
  RE-PINNED -- no code surgery in `_merged_recover.py`.

  One scripted path, bars -> structural values -> both siblings (the ruled curve and the lens).

WHAT IT EMITS
  For every row of the #279 ND teaching population: position, draft age, pick, and its STRUCTURAL
  CAREER VALUE, plus the provenance counts and the identity of everything it was derived from.
  The #279 machinery is IMPORTED AND USED UNMODIFIED -- `harness_pvc.load_matrix` +
  `harness_pvc.structural_values`.  This file reinvents nothing.

INHERITED WHOLESALE, AND CARRIED IN THE ARTIFACT'S OWN RECORD
  class window 2004-2022 hard cut · concluded careers realized in full · never-established at 0.0 ·
  active careers = played-so-far x concluded-look-alike completion (position x tenure strata, busts'
  zero remainders included, min stratum 20) · the model prior ONLY as a COUNTED fallback ·
  McCartin/Boyd exclusions and one-pick slides as the committed matrix carries them · VOR denomination.

  THE COMPLETION WART: +4.7% to +8.4% optimistic, touching 25.1% of the teaching rows.  Stamped into
  the artifact so it travels with the numbers and cannot be quoted apart from them.

    python3 emit_structural_basis.py        # writes structural_basis_279.json beside this file
"""
import json, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
PANEL = os.path.join(REPO, 'session_2026-07-30/item279/panel')
MATRIX279 = os.path.join(REPO, 'session_2026-07-30/item279/out/per_entrant_279_vor.json')
OUT = os.path.join(HERE, 'structural_basis_279.json')

# the #279 sources, pinned by md5 so a moved input HALTs instead of quietly re-basing the lens
PINS = {'harness_pvc.py': 'e0130cc22cdf9b43cb9d79f315a33a69',
        'per_entrant_279_vor.json': '77eba4d308a27a881b36a5424d3bb389'}
OPTIMISM = ('+4.7% to +8.4% optimistic (completion method, touching 25.1% of teaching rows) — '
            'inherited from the ruled curve\'s own basis, reported beside every result, never '
            'silently corrected')


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def main():
    hp = os.path.join(PANEL, 'harness_pvc.py')
    got = {'harness_pvc.py': md5(hp), 'per_entrant_279_vor.json': md5(MATRIX279)}
    for k, want in PINS.items():
        if got[k] != want:
            raise SystemExit('HALT: %s is %s, pinned %s — the #279 basis moved. Re-pin DELIBERATELY '
                             '(that is a basis change and it re-poses the seam\'s audit), or stop.'
                             % (k, got[k], want))

    sys.path.insert(0, PANEL)
    import harness_pvc as H

    meta, ND = H.load_matrix(MATRIX279)      # asserts store / v0surf identity and N == 1197
    vals, prov = H.structural_values(ND)     # UNMODIFIED #279 machinery
    byk = {r['key']: r for r in ND}

    rows, skipped = [], 0
    for v in vals:
        r = byk[v['key']]
        pk = v['pick']
        if pk is None or not (1 <= int(pk) <= 64):
            skipped += 1
            continue
        rows.append({'key': v['key'], 'pos': r.get('pos'),
                     'age_draft': r.get('age_draft'), 'pick': int(pk),
                     'value': float(v['value']), 'how': v['how'],
                     'concluded': bool(v['concluded'])})

    missing_pos = sum(1 for r in rows if not r['pos'])
    missing_age = sum(1 for r in rows if r['age_draft'] is None)

    out = {
        '_what': 'THE LENS BASIS — #279 structural career values, emitted as a DECLARED INPUT to the '
                 'engine\'s year-zero lens fit. The engine reads this file; it does not recompute it.',
        '_clause': 'approval clause 1 (the owner\'s live-and-breathe steer): a basis change propagates '
                   'by re-running this emitter and re-pinning, never by code surgery.',
        '_inherited': ('class window 2004-2022 hard cut · concluded realized in full · never-established '
                       'at 0.0 · active = played-so-far x concluded-look-alike completion (pos x tenure '
                       'strata, busts\' zero remainders included, min stratum 20) · model prior ONLY as a '
                       'counted fallback · McCartin/Boyd exclusions + one-pick slides as the committed '
                       'matrix carries them · VOR denomination (gamma 1.0)'),
        '_OPTIMISM': OPTIMISM,
        '_population_note': ('This is the RULED CURVE\'S OWN teaching set — one population, two siblings. '
                             'It is NOT the surface fit population (drafts 2003-2025) and NOT the G-Y0 '
                             'gate population. The matrix\'s teaches_curve flag describes the surface set; '
                             'the class window applied by load_matrix is what makes this the curve\'s.'),
        'identity': {'harness_pvc_md5': got['harness_pvc.py'],
                     'matrix_md5': got['per_entrant_279_vor.json'],
                     'store_md5': meta['store_md5'], 'v0surf_sig': meta['v0surf_sig'],
                     'nd_population': len(ND), 'class_window': [H.YR_LO, H.CLASS_CUT],
                     'min_stratum': H.MIN_STRATUM, 'qual_games': H.QUAL_GAMES,
                     'nd_last_pick': H.ND_LAST},
        'provenance': prov,
        'emitted_rows': len(rows),
        'skipped_out_of_range': skipped,
        'rows_missing_position': missing_pos,
        'rows_missing_draft_age': missing_age,
        'never_established_at_zero': sum(1 for r in rows if r['value'] == 0.0),
        'rows': sorted(rows, key=lambda r: (r['pick'], r['key'])),
    }
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print('BASIS EMITTED  %s' % os.path.relpath(OUT, REPO))
    print('  sources pinned  harness_pvc %s · matrix %s' % (got['harness_pvc.py'][:8],
                                                            got['per_entrant_279_vor.json'][:8]))
    print('  identity        store %s · v0surf %s · ND %d · classes %d-%d · min stratum %d'
          % (meta['store_md5'], meta['v0surf_sig'][:12], len(ND), H.YR_LO, H.CLASS_CUT, H.MIN_STRATUM))
    print('  provenance      %s  (fallback %.3f%% — COUNTED)' % (prov['counts'], prov['fallback_share_pct']))
    print('  emitted         %d rows (picks 1-64) · skipped %d · never-established at 0.0: %d'
          % (len(rows), skipped, out['never_established_at_zero']))
    print('  missing         position %d · draft age %d  (reported, never imputed)'
          % (missing_pos, missing_age))
    print('  OPTIMISM        %s' % OPTIMISM)
    print('  artifact md5    %s' % md5(OUT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
