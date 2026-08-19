#!/usr/bin/env python3
"""ORDER S — THE OWNER'S PATH TEST, APPLIED TO EVERY BREACHING CELL.

The owner has LOOSENED the year-1 +14% buy rail. His words: a year-1 breach is acceptable PROVIDED
the path afterwards does not keep beating carry and the end destination does not keep increasing.

The rule is written on PREREG_S.md §7 (the rule is ORDER R's, carried unchanged) BEFORE any table was read, and it is restated here so it cannot
be bent to a result:

  CARRY compounds at 14% a year: 1.140 1.300 1.482 1.689 1.925 2.195 2.502 for years 1..7.
  A cell BREACHES when its year-1 appreciation exceeds +14%.
  For a breaching cell:
    limb (a) "the path afterwards does not keep beating carry"
             PASSES when the count of years k in 2..7 with path_k > carry_k is ZERO.
    limb (b) "the end destination does not keep increasing"
             PASSES when path_7 <= path_6 AND path_7 <= carry_7.
    The cell PASSES the owner's path test only when BOTH limbs pass.

EVERY RAW YEAR IS PRINTED ALONGSIDE so the owner can apply his own reading rather than this seat's.
NOTHING IS ADOPTED. This file rules on nothing; it applies a rule the owner gave and shows its work.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'STANDING_TABLES_S.json')))
BJ = json.load(open(os.path.join(HERE, 'BANDS_S.json')))['nd']
CHARGE = 0.14
CARRY = [1.0] + [round((1.0 + CHARGE) ** k, 3) for k in range(1, 8)]
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 118)
P("ORDER S — THE OWNER'S PATH TEST ON EVERY BREACHING CELL")
P('=' * 118)
P('  carry, compounding at 14%%: %s' % '  '.join('yr%d %.3f' % (k, CARRY[k]) for k in range(1, 8)))
P('  A cell BREACHES when year-1 appreciation exceeds +14.00%. Only breaching cells are tested.')
P('  limb (a) PASSES when NO year 2..7 beats carry.   limb (b) PASSES when yr7 <= yr6 AND yr7 <= carry7.')
P('  The cell PASSES only when BOTH limbs pass. Raw years are printed so the owner can read it himself.')
P()

# THE ND BANDS COME FROM BANDS_S.json, which carries BOTH WINDOWS. Reading only the primary window
# would hide the modern-window breaches, which are the ones this order moves. ALLCOH only: the
# EX0506 arm is a sensitivity and is reported in BANDS_S_out.txt, not ruled on here.
rows = []
for lab, cells in sorted(BJ.items()):
    for key, d in cells.items():
        win, arm, b = key.split('|', 2)
        if arm != 'ALLCOH':
            continue
        rows.append(('%s %s' % (win, b), lab, d))
BR = [r for r in rows if r[2]['apprec01'] > CHARGE]
P('  breaching ND cells: %d of %d' % (len(BR), len(rows)))
P()
if not BR:
    P('  (none — a NULL, reported as one)')
P('  %-26s %-8s %8s | %s | %-9s %-9s %-8s' %
  ('band', 'board', 'yr1 apr', ' '.join('%7s' % ('yr%d' % k) for k in range(0, 8)),
   'limb (a)', 'limb (b)', 'VERDICT'))
P('  %-26s %-8s %8s | %s |' % ('CARRY', '', '+14.00%', ' '.join('%7.3f' % CARRY[k] for k in range(0, 8))))
OUTR = []
for nm, lab, d in sorted(BR, key=lambda z: (z[0], z[1])):
    path = d['path']
    beat = [k for k in range(2, 8) if path[k] is not None and path[k] > CARRY[k]]
    a_ok = (len(beat) == 0)
    p7, p6 = path[7], path[6]
    b_ok = (p7 is not None and p6 is not None and p7 <= p6 and p7 <= CARRY[7])
    verd = 'PASSES' if (a_ok and b_ok) else 'FAILS'
    OUTR.append(dict(band=nm, board=lab, apprec=d['apprec01'], path=path,
                     n_included=d.get('n_included'),
                     years_beating_carry=beat, limb_a=a_ok, limb_b=b_ok, passes=bool(a_ok and b_ok)))
    P('  %-26s %-8s %+7.2f%% | %s | %-9s %-9s %-8s'
      % (nm, lab, 100 * d['apprec01'],
         ' '.join(('%7.3f' % v) if v is not None else '      -' for v in path),
         'pass' if a_ok else 'FAIL(%d)' % len(beat), 'pass' if b_ok else 'FAIL', verd))
P()
P('  WHY EACH FAILING CELL FAILS, IN WORDS:')
any_fail = False
for r in OUTR:
    if r['passes']: continue
    any_fail = True
    bits = []
    if not r['limb_a']:
        bits.append('the path beats carry again in year%s %s'
                    % ('s' if len(r['years_beating_carry']) > 1 else '',
                       ', '.join(str(k) for k in r['years_beating_carry'])))
    if not r['limb_b']:
        p = r['path']
        if p[7] is not None and p[6] is not None and p[7] > p[6]:
            bits.append('it is still RISING at the end (yr6 %.3f -> yr7 %.3f)' % (p[6], p[7]))
        if p[7] is not None and p[7] > CARRY[7]:
            bits.append('it ends ABOVE carry (yr7 %.3f against carry %.3f)' % (p[7], CARRY[7]))
        if p[7] is None or p[6] is None:
            bits.append('the path has no year-6 or year-7 cell, so limb (b) CANNOT BE READ — '
                        'reported as unmeasurable, never as a pass')
    P('    %-26s %-8s : %s' % (r['band'], r['board'], '; and '.join(bits)))
if not any_fail:
    P('    (none — every breaching cell passes the owner\'s path test. A result, reported as one.)')
P()

# ---- the pool arms ------------------------------------------------------------------------------------
P('-' * 118)
P('  THE POOL ARMS. Same rule, same carry.')
P('-' * 118)
AR = []
for lab, arms in sorted(T.get('arms', {}).items()):
    for a, d in arms.items():
        ap = d.get('apprec01') if isinstance(d, dict) else None
        if ap is None:
            continue
        if ap > CHARGE:
            AR.append((a, lab, d))
P('  breaching arm cells: %d' % len(AR))
if not AR:
    P('  (none — a NULL, reported as one)')
else:
    P('  %-10s %-8s %8s | %s | %-9s %-9s %-8s' %
      ('arm', 'board', 'yr1 apr', ' '.join('%7s' % ('yr%d' % k) for k in range(0, 8)),
       'limb (a)', 'limb (b)', 'VERDICT'))
    for a, lab, d in sorted(AR, key=lambda z: (z[0], z[1])):
        path = (d.get('path') or [None] * 8)[:8]
        while len(path) < 8:
            path.append(None)
        beat = [k for k in range(2, 8) if path[k] is not None and path[k] > CARRY[k]]
        a_ok = (len(beat) == 0)
        p7, p6 = path[7], path[6]
        b_ok = (p7 is not None and p6 is not None and p7 <= p6 and p7 <= CARRY[7])
        readable = (p7 is not None and p6 is not None)
        verd = ('PASSES' if (a_ok and b_ok) else 'FAILS') if readable else 'UNREADABLE'
        OUTR.append(dict(band='ARM ' + a, board=lab, apprec=d['apprec01'], path=path,
                         years_beating_carry=beat, limb_a=a_ok, limb_b=b_ok,
                         passes=bool(a_ok and b_ok), readable=readable))
        P('  %-10s %-8s %+7.2f%% | %s | %-9s %-9s %-8s'
          % (a, lab, 100 * d['apprec01'],
             ' '.join(('%7.3f' % v) if v is not None else '      -' for v in path),
             'pass' if a_ok else 'FAIL(%d)' % len(beat), 'pass' if b_ok else 'FAIL', verd))
P()
P('  TOTAL: %d breaching cells, %d PASS the owner\'s path test, %d FAIL.'
  % (len(OUTR), sum(1 for r in OUTR if r['passes']), sum(1 for r in OUTR if not r['passes'])))
P()
P('  A DISCLOSURE THE PATH TEST DEPENDS ON, AND IT IS NOT SMALL. The later years of these paths are')
P('  measured on FEWER ROWS than year 1. A cohort only has a year-7 cell if it drafted seven years')
P('  ago. On MODERN picks 1-20 the row counts run 100 100 100 100 100 80 60 40 across years 0 to 7.')
P('  So limb (b), which reads years 6 and 7, is read on 40 of the 100 rows that produced the year-1')
P('  breach. THAT IS A REAL WEAKNESS IN THE TEST AND IT IS STATED RATHER THAN BURIED. The per-cell')
P('  counts are in PATHTEST_S.json under n_included.')
P()
P('  THIS SEAT DOES NOT RULE ON ANY OF THESE. The rule applied is the owner\'s, written down before')
P('  the tables were read. Nothing was moved to change a verdict.')

json.dump(dict(carry=CARRY, charge=CHARGE, cells=OUTR),
          open(os.path.join(HERE, 'PATHTEST_S.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'PATHTEST_S_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote PATHTEST_S.json / PATHTEST_S_out.txt')
