#!/usr/bin/env python3
"""ARM 1 — THE PER-ARM NO-ARB READING (process law P12), on THIS arm's own matrices.

P12: "Every value-moving adoption carries its own arm's no-arb band reading and class check
PRE-FLIP, measured inside the prereg — a reading taken on a sibling variant does not cover the
chosen arm." The staircase adoption is the incident. This is ARM 1's own reading.

THE MEASUREMENT IS NOT RE-IMPLEMENTED. The constants and the marks() function are BYTE-CARRIED, at
run time, out of the adoption's own instrument
docs/evidence/staircase_adoption_2026-08-21/araw_noarb_class.py — the exact file that produced the
reading the owner ruled on — by slicing lines 92..141 of that file and exec'ing them. The carried
source's md5 is computed at run and PRINTED, so a drifted instrument is visible rather than silent,
and the W2 window, the cohort clock, the owner's growth floor 1.03 and the buy rail 1.14 cannot be
edited here without changing that md5.

What this file adds and nothing else: the two ARM 1 labels and where their matrices live.

Usage:  python3 arm1_noarb_class.py --sp <dir with per_entrant_*.json> [--json OUT]
"""
import argparse, hashlib, json, os, sys

CARRY_REL = os.path.join('docs', 'evidence', 'staircase_adoption_2026-08-21', 'araw_noarb_class.py')
CARRY_LINES = (92, 141)          # W2/COH/ALLC/FLOOR/RAIL + P() + cohort() + marks(); nothing else

ARM1_LABELS = [
    ('ARM1BASE', 'THE LIVE BOARD 6fd0f7de — live band/ceiling/peak, this seat\'s own emit'),
    ('ARM1CAND', '*** ARM 1 STORE-ALONE CANDIDATE 02a554b5 — incumbent constructions on store daa93053 ***'),
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
            raise SystemExit('arm1_noarb_class HALT: the carried slice does not define %r — the source '
                             'instrument moved; re-read it and re-declare CARRY_LINES.' % need)
    W2, ALLC, FLOOR, RAIL, marks = G['W2'], G['ALLC'], G['FLOOR'], G['RAIL'], G['marks']
    print('  carried constants: W2 %d..%d  floor %.2f  buy rail %.2f'
          % (W2[0], W2[-1], FLOOR, RAIL))

    print('\n%-10s %-70s %10s %10s %10s %6s'
          % ('label', 'board', 'W2 mark', 'cohort', 'max class', 'year'))
    OUT = {}
    for lab, nice in ARM1_LABELS:
        p = os.path.join(a.sp, 'per_entrant_%s.json' % lab)
        if not os.path.exists(p):
            print('%-10s MATRIX MISSING (%s)' % (lab, p))     # absent labels PRINT, never vanish
            continue
        m = marks(p)
        OUT[lab] = m
        print('%-10s %-70s %10.4f %10.4f %10.4f %6d'
              % (lab, nice, m['w2'], m['cohort'], m['max_class'], m['max_class_year']))

    if 'ARM1BASE' in OUT and 'ARM1CAND' in OUT:
        b, c = OUT['ARM1BASE'], OUT['ARM1CAND']
        print('\n%s\nTHE RAIL AND THE FLOOR — ARM 1\'s OWN READING (P12)\n%s' % ('-' * 100, '-' * 100))
        for lab, m in (('LIVE      ', b), ('CANDIDATE ', c)):
            print('  %s W2 %.4f   floor margin %+.4f (>= %.2f)   buy-rail margin %+.4f (< %.2f)   '
                  'max class %.4f (%d)   %s'
                  % (lab, m['w2'], m['w2'] - FLOOR, FLOOR, RAIL - m['max_class'], RAIL,
                     m['max_class'], m['max_class_year'],
                     'PASS' if (m['w2'] >= FLOOR and m['max_class'] < RAIL) else
                     'BREACH — the class is over the buy rail'))
        print('  MOVE candidate - live : W2 %+.4f   cohort %+.4f   max class %+.4f'
              % (c['w2'] - b['w2'], c['cohort'] - b['cohort'], c['max_class'] - b['max_class']))
        print('\n  per class, registered W2 window (draft class -> cohort year):')
        print('  %-18s %10s %10s %10s' % ('draft class', 'LIVE', 'CANDIDATE', 'move'))
        for y in W2:
            x, z = b['per_class'].get(y), c['per_class'].get(y)
            if x is None or z is None:
                continue
            print('  %-18s %10.4f %10.4f %+10.4f %s'
                  % ('%d (%d)' % (y - 1, y), x, z, z - x,
                     'BREACH' if z > RAIL else ('was-breach' if x > RAIL else '')))
        print('\n  ALL CLASSES, FULL RANGE — so a single class breaking %.2f cannot hide:' % RAIL)
        for y in ALLC:
            x, z = b['per_class'].get(y), c['per_class'].get(y)
            if x is None or z is None:
                continue
            fl = 'BREACH' if z > RAIL else ''
            print('  %-8d %10.4f %10.4f %+10.4f %s' % (y, x, z, z - x, fl))
        nb = sum(1 for y in ALLC if (c['per_class'].get(y) or 0) > RAIL)
        ob = sum(1 for y in ALLC if (b['per_class'].get(y) or 0) > RAIL)
        print('\n  classes over the %.2f buy rail : live %d   candidate %d   NEW BREACHES %d'
              % (RAIL, ob, nb, max(0, nb - ob)))
        OUT['_reading'] = {'floor': FLOOR, 'rail': RAIL,
                           'live': {k: b[k] for k in ('w2', 'cohort', 'max_class', 'max_class_year')},
                           'candidate': {k: c[k] for k in ('w2', 'cohort', 'max_class', 'max_class_year')},
                           'classes_over_rail_live': ob, 'classes_over_rail_candidate': nb,
                           'new_breaches': max(0, nb - ob),
                           'carried_instrument_md5': hashlib.md5(src).hexdigest()}
    if a.json:
        json.dump(OUT, open(a.json, 'w'), indent=1, sort_keys=True, default=float)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
