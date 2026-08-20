#!/usr/bin/env python3
"""ORDER S — THE YEAR-1 CLASS COHORT MARK, read off the BUILT walk-forward matrices.

TWO BASES ARE PRINTED, SIDE BY SIDE, BECAUSE CONFUSING THEM COST AN EARLIER SEAT A FULL DAY.

  THE REGISTERED W2 BASIS — the one the owner's 1.03 floor and 1.14 rail are written on.
      DRAFT classes 2005 to 2015, ENTRY_FLOOR = 2005. On the cohort clock those are cohort years
      2006 to 2016, because cohort = draft year + 1 for everything except a mid-season draftee.
      This is what ORDER P's op_step4.py calls `classmark(lam, 2006, 2016)` and reports as 1.0613.

  THE COHORT CLOCK — cohort years 2005 to 2015, i.e. DRAFT years 2004 to 2014. This is the basis
      ORDER K's own ok_class.py prints. IT IS NOT THE RAIL'S BASIS. It is carried here only so the
      two can be told apart on sight.

The mark is the average, over the classes in the window, of (that class's mean year-1 price) divided
by (that class's mean year-0 price). Value semantics are the all-arm instrument's, verbatim: year 0
is v0; year N is the vpath cell at cohort + N - 1; ended or null counts as 0 and stays in the
denominator; pre-window rows are excluded and counted, never scored zero.

The instrument is validated before any ORDER P number is quoted: it must reproduce ORDER K's own
published marks (W2 1.0513, cohort clock 1.0324) off ORDER K's own matrix.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
LABELS = [('OKRULED', 'ORDER K f3101883'),
          ('PBUILT', 'ORDER P 374d4e44'),
          ('QB1', 'ORDER Q FIX B1 1b1817f3'),
          ('QAB1', 'ORDER Q FIX A+B1 cbbb94d4'),
          ('R20A', 'ORDER R R20A 7f88f509'),
          ('SW47', 'ORDER S recency w=0.47'),
          ('SW47A', 'ORDER S recency w=0.47 + FIX A'),
          ('SC20', 'ORDER S compression p20'),
          ('SC20A', 'ORDER S compression p20 + FIX A'),
          ('SM', 'ORDER S mature premium'),
          ('SMA', 'ORDER S mature premium + FIX A'),
          ('SL56', 'ORDER S LAMBDA 0.56'),
          ('SL10', 'ORDER S LAMBDA 0.10'),
          ('SALL', 'ORDER S all four + FIX A'),
          ('ASMCAND', '*** THE ASSEMBLY CANDIDATE ***')]
LABELS = [(l, n) for l, n in LABELS if os.path.exists(os.path.join(SP, 'per_entrant_%s.json' % l))]
W2 = list(range(2006, 2017))          # DRAFT classes 2005-2015 — THE REGISTERED BASIS
COH = list(range(2005, 2016))         # DRAFT classes 2004-2014 — the cohort clock, NOT the rail
ALLC = list(range(2005, 2022))
FLOOR, RAIL = 1.03, 1.14
L = []


def P(s=''):
    print(s); L.append(str(s))


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def marks(path):
    D = json.load(open(path))
    R = D['recs']
    wend = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    per = {}
    for y in ALLC:
        pop = [r for r in elig if cohort(r) == y]
        num = den = 0.0; n = 0
        for r in pop:
            Y = y
            yrs = r.get('yrs') or []; vp = r.get('vpath') or []
            if Y > wend:
                continue
            if not yrs:
                v1 = 0.0
            elif Y < yrs[0]:
                continue
            elif Y > yrs[-1]:
                v1 = 0.0
            else:
                i = yrs.index(Y)
                v1 = 0.0 if vp[i] is None else float(vp[i])
            num += v1; den += float(r['v0']); n += 1
        per[y] = (num / den) if (den > 0 and n >= 5) else None
    def avg(ws):
        v = [per[y] for y in ws if per.get(y) is not None]
        return sum(v) / len(v), len(v)
    w2, nw2 = avg(W2); ch, nch = avg(COH)
    return dict(per_class=per, w2=w2, n_w2=nw2, cohort=ch, n_cohort=nch,
                max_class=max(v for v in per.values() if v is not None),
                max_class_year=max((v, y) for y, v in per.items() if v is not None)[1],
                min_class=min(v for v in per.values() if v is not None))


OUT = {}
P('=' * 118)
P('ORDER S — THE YEAR-1 CLASS COHORT MARK, on the BUILT walk-forward matrices')
P('=' * 118)
P('  THE REGISTERED W2 BASIS = DRAFT classes 2005-2015 = cohort years 2006-2016. THE RAIL IS ON THIS.')
P('  the cohort clock       = DRAFT classes 2004-2014 = cohort years 2005-2015. NOT the rail.')
P('  the owner\'s floor: the class must GROW, mark >= %.2f.   the buy rail: mark < %.2f.' % (FLOOR, RAIL))
P()
P('%-9s %-58s %10s %10s %10s %6s' % ('label', 'board', 'W2 mark', 'cohort', 'max class', 'year'))
for lab, nice in LABELS:
    p = SP + '/per_entrant_%s.json' % lab
    if not os.path.exists(p):
        P('%-9s MATRIX MISSING' % lab); continue
    m = marks(p); OUT[lab] = m
    P('%-9s %-58s %10.4f %10.4f %10.4f %6d'
      % (lab, nice, m['w2'], m['cohort'], m['max_class'], m['max_class_year']))
P()
# ---- the instrument is validated against ORDER K's own published numbers -----------------------------
if 'OKRULED' in OUT:
    dw = abs(OUT['OKRULED']['w2'] - 1.0513); dc = abs(OUT['OKRULED']['cohort'] - 1.0324)
    P('  INSTRUMENT VALIDATION — this file must reproduce ORDER K\'s own published marks off ORDER K\'s')
    P('  own matrix before any ORDER P number is quoted:  W2 %.4f vs 1.0513 (%.4f)  ·  cohort %.4f vs'
      % (OUT['OKRULED']['w2'], dw, OUT['OKRULED']['cohort']))
    P('  1.0324 (%.4f)   -> %s' % (dc, 'VALIDATED' if max(dw, dc) < 5e-4 else 'THE INSTRUMENT DISAGREES'))
P()
if 'PBUILT' in OUT and 'OKRULED' in OUT:
    p_, k_ = OUT['PBUILT'], OUT['OKRULED']
    P('-' * 118)
    P('THE RAIL, ON THE REGISTERED BASIS')
    P('-' * 118)
    P('  ORDER P   W2 %.4f   floor %+.4f   rail %+.4f   %s'
      % (p_['w2'], p_['w2'] - FLOOR, p_['w2'] - RAIL,
         'PASS — the class GROWS and stays under the buy rail'
         if (p_['w2'] >= FLOOR and p_['w2'] < RAIL) else 'FAIL — B5 FIRES'))
    P('  ORDER K   W2 %.4f   floor %+.4f   rail %+.4f' % (k_['w2'], k_['w2'] - FLOOR, k_['w2'] - RAIL))
    P('  ORDER P estimate published in PACKET_P: 1.0613 on this basis. BUILT: %.4f. DIFFERENCE %+.4f.'
      % (p_['w2'], p_['w2'] - 1.0613))
    P()
    P('  per class, on the registered W2 window (DRAFT class -> cohort year):')
    P('  %-14s %10s %10s %10s' % ('draft class', 'ORDER K', 'ORDER P', 'move'))
    for y in W2:
        a = k_['per_class'].get(y); b = p_['per_class'].get(y)
        if a is None or b is None: continue
        P('  %-14s %10.4f %10.4f %+10.4f' % ('%d (coh %d)' % (y - 1, y), a, b, b - a))
    P()
    P('  every class in the FULL range, so a single class breaking the 1.14 rail cannot hide:')
    P('  %-8s %10s %10s %10s %s' % ('cohort', 'ORDER K', 'ORDER P', 'move', 'over 1.14?'))
    for y in ALLC:
        a = k_['per_class'].get(y); b = p_['per_class'].get(y)
        if a is None or b is None: continue
        P('  %-8d %10.4f %10.4f %+10.4f %s' % (y, a, b, b - a, 'BREACH' if b > RAIL else ''))

P()
P('-' * 118)
P('THE PER-CLASS TABLE ACROSS EVERY BOARD, ON THE REGISTERED W2 WINDOW')
P('-' * 118)
LABS = [l for l, _ in LABELS if l in OUT]
P('  %-16s %s' % ('draft class (cohort)', ' '.join('%8s' % l for l in LABS)))
for y in W2:
    vals = [OUT[l]['per_class'].get(y) for l in LABS]
    if any(v is None for v in vals): continue
    flag = '  <- OVER 1.14 ON EVERY BOARD' if all(v > RAIL for v in vals) else (
           '  <- over 1.14 somewhere' if any(v > RAIL for v in vals) else '')
    P('  %-16s %s%s' % ('%d (%d)' % (y - 1, y), ' '.join('%8.4f' % v for v in vals), flag))
P()
P('  THE THREE CLASSES ORDER P PUT OVER THE 1.14 LINE — draft 2010 (1.1570), 2011 (1.1595) and')
P('  2015 (1.2047). Does anything in ORDER R move them off it?')
P('  %-16s %10s %s' % ('draft class', 'ORDER P', ' '.join('%9s' % l for l in LABS if l not in ('OKRULED', 'PBUILT'))))
for y in (2011, 2012, 2016):
    base = OUT['PBUILT']['per_class'].get(y)
    if base is None: continue
    row = []
    for l in LABS:
        if l in ('OKRULED', 'PBUILT'): continue
        v = OUT[l]['per_class'].get(y)
        row.append('%9.4f' % v if v is not None else '        -')
    P('  %-16s %10.4f %s' % ('%d (%d)' % (y - 1, y), base, ' '.join(row)))
P('  %-16s %10s %s' % ('  move vs ORDER P', '', ' '.join(
    '%9s' % '' for l in LABS if l not in ('OKRULED', 'PBUILT'))))
for y in (2011, 2012, 2016):
    base = OUT['PBUILT']['per_class'].get(y)
    if base is None: continue
    row = []
    for l in LABS:
        if l in ('OKRULED', 'PBUILT'): continue
        v = OUT[l]['per_class'].get(y)
        row.append('%+9.4f' % (v - base) if v is not None else '        -')
    P('  %-16s %10s %s' % ('%d (%d)' % (y - 1, y), '', ' '.join(row)))
P()
P('  ALL CLASSES, FULL RANGE, EVERY BOARD — so a single class breaking 1.14 cannot hide:')
P('  %-8s %s' % ('cohort', ' '.join('%8s' % l for l in LABS)))
for y in ALLC:
    vals = [OUT[l]['per_class'].get(y) for l in LABS]
    if any(v is None for v in vals): continue
    P('  %-8d %s %s' % (y, ' '.join('%8.4f' % v for v in vals),
                        'BREACH' if any(v > RAIL for v in vals) else ''))
P()
P('  THE RAIL AND THE FLOOR, EVERY BOARD, ON THE REGISTERED W2 BASIS:')
P('  %-9s %10s %12s %12s  %s' % ('board', 'W2 mark', 'vs 1.03', 'vs 1.14', 'verdict'))
for l in LABS:
    w = OUT[l]['w2']
    P('  %-9s %10.4f %+12.4f %+12.4f  %s'
      % (l, w, w - FLOOR, w - RAIL,
         'inside the law' if (w >= FLOOR and w < RAIL) else '**BREACH — R12 FIRES**'))

json.dump(OUT, open(os.path.join(HERE, 'CLASS_S.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CLASS_S_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote CLASS_S.json and CLASS_S_out.txt')
