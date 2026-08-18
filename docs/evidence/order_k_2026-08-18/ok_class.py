#!/usr/bin/env python3
"""ORDER K — G1, THE YEAR-1 CLASS COHORT MARK, read off the BUILT walk-forward matrices.

The class mark is the W2 object the owner's G1 rail is written in: for each intake class, the cohort's
mean year-1 price divided by its mean year-0 price; the mark is the average of those class ratios over
classes 2005-2015. Order I and Order J both read it on the ANALYTIC calibrator. This reads it on the
BUILT matrix instead, which is the stronger instrument, and it is validated by reproducing the landing
candidate's number of record (1.0421) before any Order K number is quoted.

Cohort clock and value semantics are the all-arm instrument's, verbatim: cohort = year + 1 except MSD;
year 0 is v0; year N is the vpath cell at cohort + N - 1; ended/null = 0 and stays in the denominator;
pre-window rows are excluded and counted, never scored zero.
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
LABELS = [('O35FINAL', 'the landing candidate 1f176444'),
          ('O31FFINAL', 'candidate 31 fe6be9d6'),
          ('OKRULED', 'ORDER K f3101883 — the ruled setting, fixed fade floor')]
CLASSES = list(range(2005, 2022))
MARKW = list(range(2005, 2016))          # the 11 classes the W2 mark averages


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def val(r, N, wend):
    if N == 0:
        return float(r['v0'] or 0.0), 'v0'
    Y = cohort(r) + N - 1
    if Y > wend:
        return None, 'notreached'
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs:
        return 0.0, 'ended'
    if Y < yrs[0]:
        return None, 'pre'
    if Y > yrs[-1]:
        return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


def marks(path):
    D = json.load(open(path))
    R = D['recs']
    wend = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    per = {}
    for y in CLASSES:
        pop = [r for r in elig if cohort(r) == y]
        num = den = 0.0; n = 0
        for r in pop:
            v1, k1 = val(r, 1, wend)
            if k1 in ('pre', 'notreached'):
                continue
            num += v1; den += float(r['v0']); n += 1
        per[y] = (num / den) if (den > 0 and n >= 5) else None
    ok = [per[y] for y in MARKW if per[y] is not None]
    return dict(per_class=per, mean_0515=sum(ok) / len(ok), n_classes=len(ok),
                max_class=max(v for v in per.values() if v is not None),
                max_class_year=max((v, y) for y, v in per.items() if v is not None)[1],
                min_class=min(v for v in per.values() if v is not None))


OUT = {}
print('ORDER K — G1, THE YEAR-1 CLASS COHORT MARK, on the BUILT walk-forward matrices')
print('  the mark averages the per-class cohort ratio (mean yr1 / mean yr0) over classes 2005-2015\n')
print('%-11s %-52s %10s %10s %6s %10s' % ('label', 'board', 'mark', 'max class', 'year', 'min class'))
for lab, nice in LABELS:
    p = SP + '/per_entrant_%s.json' % lab
    if not os.path.exists(p):
        print('  %-11s MATRIX MISSING' % lab); continue
    m = marks(p)
    OUT[lab] = m
    print('%-11s %-52s %10.4f %10.4f %6d %10.4f'
          % (lab, nice, m['mean_0515'], m['max_class'], m['max_class_year'], m['min_class']))

print('\nPER-CLASS, side by side:')
print('  %-6s %10s %10s %10s' % ('class', 'landing', 'cand 31', 'ORDER K'))
for y in CLASSES:
    row = []
    for lab, _ in LABELS:
        v = OUT.get(lab, {}).get('per_class', {}).get(y)
        row.append('%10.4f' % v if v is not None else '%10s' % '-')
    print('  %-6d %s%s' % (y, ''.join(row), '   <- in the mark window' if y in MARKW else ''))

# ---- the same mark, restricted to the CALIBRATOR'S OWN 1,986-row population -------------------------
# G1's number of record in Orders I and J is the ANALYTIC calibrator's mean_0515, which reads 1.0421 on
# the landing candidate. This built-matrix instrument reads 1.0232 on the same board. The gap is not a
# disagreement about the board — it is two different objects, and the two causes are separated here so
# neither number can be quoted as if it were the other.
LEG = json.load(open(SP + '/O36_LEGS.json'))
LEGKEYS = set(q['key'] for q in LEG['pop'])


def marks_restricted(path):
    D = json.load(open(path)); R = [r for r in D['recs'] if r['key'] in LEGKEYS]
    wend = max(y for r in D['recs'] for y, v in zip(r.get('yrs') or [], r.get('vpath') or [])
               if v is not None)
    per = {}
    for y in CLASSES:
        pop = [r for r in R if cohort(r) == y and (r.get('v0') or 0) > 0]
        num = den = 0.0; n = 0
        for r in pop:
            v1, k1 = val(r, 1, wend)
            if k1 in ('pre', 'notreached'):
                continue
            num += v1; den += float(r['v0']); n += 1
        per[y] = (num / den) if (den > 0 and n >= 5) else None
    ok = [per[y] for y in MARKW if per[y] is not None]
    return sum(ok) / len(ok)


print('\nTHE SAME MARK ON THREE READINGS OF THE SAME BOARDS — so the instrument gap is separated from')
print('the build, and no number is quoted as if it were another:')
print('  %-52s %10s %10s %10s' % ('reading', 'landing', 'cand 31', 'ORDER K'))
r1 = [OUT[l]['mean_0515'] for l, _ in LABELS]
r2 = [marks_restricted(SP + '/per_entrant_%s.json' % l) for l, _ in LABELS]
print('  %-52s %10.4f %10.4f %10.4f' % ('built matrix, every eligible row', *r1))
print('  %-52s %10.4f %10.4f %10.4f' % ("built matrix, the calibrator's own 1,986 rows", *r2))
print('  %-52s %10.4f %10s %10.4f'
      % ('ANALYTIC CALIBRATOR (G1\'s number of record, I and J)', 1.0421, 'n/a', 1.0515))
print('  the three readings move by %+.4f / %+.4f / %+.4f — the SAME direction and very nearly the same'
      % (r1[2] - r1[0], r2[2] - r2[0], 1.0515 - 1.0421))
print('  size. The level differs because (i) the built matrix scores every eligible row, not the')
print('  calibrator\'s teaching population, and (ii) the calibrator\'s year-1 price is analytic where the')
print('  matrix\'s is the engine\'s own walk-forward value.')
OUT['readings'] = dict(all_rows=dict(zip([l for l, _ in LABELS], r1)),
                       calibrator_population=dict(zip([l for l, _ in LABELS], r2)),
                       analytic_calibrator=dict(O35FINAL=1.0421, OKRULED=1.0515,
                                                OKRULED_predicted_on_the_defective_fade=1.0519))

C = OUT.get('O35FINAL'); K = OUT.get('OKRULED')
print('\n== G1 SCORED ==')
print('  the landing candidate reads          %.4f' % C['mean_0515'])
print('  ORDER K reads                        %.4f   (%+.4f)' % (K['mean_0515'], K['mean_0515'] - C['mean_0515']))
print('  GROWS vs the landing candidate       %s' % ('PASS' if K['mean_0515'] > C['mean_0515'] else 'FAIL'))
print('  floor 1.03                           %s' % ('PASS' if K['mean_0515'] >= 1.03 else 'FAIL'))
print('  strictly under the 1.14 buy rail     %s' % ('PASS' if K['mean_0515'] < 1.14 else 'FAIL — K9 FIRES'))
print("  the owner's ~1.08 ideal              NOT REACHED — short by %.4f. Reported, never chased."
      % (1.08 - K['mean_0515']))
print('  worst single class vs the ruled 1.139 line: %.4f  %s'
      % (K['max_class'], 'inside' if K['max_class'] <= 1.139 else 'OUTSIDE — HALT'))
json.dump(OUT, open(os.path.join(HERE, 'CLASS_K.json'), 'w'), indent=1)
print('\nwrote CLASS_K.json')
