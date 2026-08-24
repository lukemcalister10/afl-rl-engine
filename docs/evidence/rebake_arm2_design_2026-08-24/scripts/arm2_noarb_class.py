#!/usr/bin/env python3
"""ARM 2 — THE PER-ARM NO-ARB READING (process law P12), on THIS arm's own matrices.

P12: "Every value-moving adoption carries its OWN arm's no-arb band reading and class check PRE-FLIP,
measured inside the prereg — a reading taken on a sibling variant does not cover the chosen arm." ARM 1's
reading covers ARM 1. This is ARM 2's, taken on ARM 2's own candidate, and it is deliberately a THREE-way
read: the live board, ARM 1's candidate, and this arm's — so the design's contribution to the class
picture is separable from the staleness repair's, exactly as the movers tables are.

THE MEASUREMENT IS NOT RE-IMPLEMENTED, AND THE CARRY IS ARM 1'S OWN. The constants and marks() are
BYTE-CARRIED at run time out of the adoption's instrument
docs/evidence/staircase_adoption_2026-08-21/araw_noarb_class.py — the exact file that produced the
reading the owner ruled on — by slicing lines 92..141 and exec'ing them. The carried source's md5 is
computed at run and PRINTED, so a drifted instrument is visible rather than silent, and the W2 window,
the cohort clock, the owner's growth floor 1.03 and the buy rail 1.14 cannot be edited here without
changing that md5. Identical carry to ARM 1's script; only the labels differ.
"""
import argparse, hashlib, json, os, sys

CARRY_REL = os.path.join('docs', 'evidence', 'staircase_adoption_2026-08-21', 'araw_noarb_class.py')
CARRY_LINES = (92, 141)

LABELS = [
    ('ARM2LIVE', 'THE LIVE BOARD 82fcd8bb — live band/ceiling/peak on store fb640ca0'),
    ('ARM1CAND', 'ARM 1 store-alone candidate 02a554b5 — incumbent constructions (store daa93053)'),
    ('ARM2CAND', '*** ARM 2 DESIGN CANDIDATE — the exact-monotone construction, age hill, recency weight ***'),
]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--sp', required=True)
    ap.add_argument('--repo', default=os.environ.get('RL_REPO', '.'))
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])

    carry = os.path.join(a.repo, CARRY_REL)
    src = open(carry, 'rb').read()
    print('CARRIED INSTRUMENT : %s' % CARRY_REL)
    print('  md5 (whole file) : %s' % hashlib.md5(src).hexdigest())
    lines = src.decode().splitlines(True)
    slice_ = ''.join(lines[CARRY_LINES[0] - 1:CARRY_LINES[1]])
    print('  carried lines    : %d..%d   slice md5 %s'
          % (CARRY_LINES[0], CARRY_LINES[1], hashlib.md5(slice_.encode()).hexdigest()))
    G = {'os': os, 'json': json, 'sys': sys}
    exec(slice_, G)
    for need in ('W2', 'COH', 'ALLC', 'FLOOR', 'RAIL', 'cohort', 'marks'):
        if need not in G:
            raise SystemExit('arm2_noarb_class HALT: the carried slice does not define %r — the source '
                             'instrument moved; re-read it and re-declare CARRY_LINES.' % need)
    W2, ALLC, FLOOR, RAIL, marks = G['W2'], G['ALLC'], G['FLOOR'], G['RAIL'], G['marks']
    print('  carried constants: W2 %d..%d  floor %.2f  buy rail %.2f'
          % (W2[0], W2[-1], FLOOR, RAIL))

    print('\n%-10s %-72s %10s %10s %10s %6s'
          % ('label', 'board', 'W2 mark', 'cohort', 'max class', 'year'))
    OUT = {}
    for lab, nice in LABELS:
        p = os.path.join(a.sp, 'per_entrant_%s.json' % lab)
        if not os.path.exists(p):
            print('%-10s MATRIX MISSING (%s)' % (lab, p))     # absent labels PRINT, never vanish
            continue
        OUT[lab] = marks(p)
        m = OUT[lab]
        print('%-10s %-72s %10.4f %10.4f %10.4f %6d'
              % (lab, nice, m['w2'], m['cohort'], m['max_class'], m['max_class_year']))

    if 'ARM2LIVE' in OUT and 'ARM2CAND' in OUT:
        b, c = OUT['ARM2LIVE'], OUT['ARM2CAND']
        print('\n%s\nTHE RAIL AND THE FLOOR — ARM 2\'s OWN READING (P12)\n%s' % ('-' * 104, '-' * 104))
        for lab in [l for l, _ in LABELS if l in OUT]:
            m = OUT[lab]
            print('  %-10s W2 %.4f   floor margin %+.4f (>= %.2f)   buy-rail margin %+.4f (< %.2f)   '
                  'max class %.4f (%d)   %s'
                  % (lab, m['w2'], m['w2'] - FLOOR, FLOOR, RAIL - m['max_class'], RAIL,
                     m['max_class'], m['max_class_year'],
                     'PASS' if (m['w2'] >= FLOOR and m['max_class'] < RAIL) else
                     'BREACH — the class is over the buy rail'))
        print('  MOVE candidate - live : W2 %+.4f   cohort %+.4f   max class %+.4f'
              % (c['w2'] - b['w2'], c['cohort'] - b['cohort'], c['max_class'] - b['max_class']))
        if 'ARM1CAND' in OUT:
            a1 = OUT['ARM1CAND']
            print('  MOVE candidate - ARM 1: W2 %+.4f   cohort %+.4f   max class %+.4f   '
                  '<== THE PURE DESIGN EFFECT'
                  % (c['w2'] - a1['w2'], c['cohort'] - a1['cohort'], c['max_class'] - a1['max_class']))
        print('\n  ALL CLASSES, FULL RANGE — so a single class breaking %.2f cannot hide:' % RAIL)
        hdr = '  %-8s' + ' %10s' * len([l for l, _ in LABELS if l in OUT])
        print(hdr % tuple(['class'] + [l for l, _ in LABELS if l in OUT]))
        for y in ALLC:
            vals = [OUT[l]['per_class'].get(y) for l, _ in LABELS if l in OUT]
            if any(v is None for v in vals):
                continue
            print(('  %-8d' + ' %10.4f' * len(vals) + ' %s')
                  % tuple([y] + vals + ['BREACH' if vals[-1] > RAIL else '']))
        nb = sum(1 for y in ALLC if (c['per_class'].get(y) or 0) > RAIL)
        ob = sum(1 for y in ALLC if (b['per_class'].get(y) or 0) > RAIL)
        print('\n  classes over the %.2f buy rail : live %d   ARM 2 candidate %d   NEW BREACHES %d'
              % (RAIL, ob, nb, max(0, nb - ob)))
        OUT['_reading'] = {'floor': FLOOR, 'rail': RAIL,
                           'live': {k: b[k] for k in ('w2', 'cohort', 'max_class', 'max_class_year')},
                           'candidate': {k: c[k] for k in ('w2', 'cohort', 'max_class', 'max_class_year')},
                           'arm1': ({k: OUT['ARM1CAND'][k] for k in
                                     ('w2', 'cohort', 'max_class', 'max_class_year')}
                                    if 'ARM1CAND' in OUT else None),
                           'classes_over_rail_live': ob, 'classes_over_rail_candidate': nb,
                           'new_breaches': max(0, nb - ob),
                           'carried_instrument_md5': hashlib.md5(src).hexdigest()}
    if a.json:
        json.dump(OUT, open(a.json, 'w'), indent=1, sort_keys=True, default=float)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
