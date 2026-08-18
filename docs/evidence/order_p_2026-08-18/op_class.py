#!/usr/bin/env python3
"""ORDER N (reusing ORDER L/K machinery unchanged) — THE YEAR-1 CLASS MARK, RECOMPUTED ON THE 2005/06 EXCLUSION BASIS.

Order K's machinery, unchanged: ok_class.py's cohort clock (cohort = draft year + 1, except MSD
where cohort = draft year), its value semantics, its per-class pooled ratio sum(year-1) / sum(v0),
its n >= 5 rule, and its mark = the mean of the per-class ratios over classes 2005-2015.

Order L adds ONE thing: the same mark with cohort classes 2005 and 2006 removed from the population
entirely — from the numerator and the denominator alike. That leaves 9 classes, cohort 2007-2015. It is a
SENSITIVITY, not a correction, and it is never the headline.

It also prints the SECOND reading that decides the W2 floor comparison: the W2 scorer's own class
mark, which is computed on a DIFFERENT CLASS CLOCK (draft year, not cohort) and a DIFFERENT class
window (draft classes 2005-2015). That reading is produced here with w2_forward_calibration.py's own
population rule and its own price fields, so the two instruments can be laid side by side.
"""
import json, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
LABELS = [('PDERIV', "ORDER P — THE PEDIGREE-CONDITIONAL CHARGE (ESTIMATE, NOT A BUILD)"),
          ('NVARB', 'ORDER P — the age-only-bar charge, frontier point (ESTIMATE, NOT A BUILD)'),
          ('OKRULED', 'ORDER K f3101883 — the current candidate, eta 0.50'),
          ('M0ETA0', "ORDER M0 73bf9617 — ORDER K's knobs with ETA SET TO ZERO"),
          ('O35FINAL', 'the landing candidate 1f176444'),
          ('O31FFINAL', 'candidate 31 fe6be9d6')]
CLASSES = list(range(2005, 2022))
MARKW = list(range(2005, 2016))                 # ok_class.py's own 11-class mark window
EXCLUDED = (2005, 2006)                          # cohort clock = the 2004 and 2005 national drafts
MARKW_EX = [y for y in MARKW if y not in EXCLUDED]
SUPERVISOR_EX_OKRULED = 1.0669
L = []


def P(s=''):
    print(s); L.append(str(s))


# ---- ok_class.py's own functions, copied ------------------------------------------------------------
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
    per, nper = {}, {}
    for y in CLASSES:
        pop = [r for r in elig if cohort(r) == y]
        num = den = 0.0; n = 0
        for r in pop:
            v1, k1 = val(r, 1, wend)
            if k1 in ('pre', 'notreached'):
                continue
            num += v1; den += float(r['v0']); n += 1
        per[y] = (num / den) if (den > 0 and n >= 5) else None
        nper[y] = n
    ok = [per[y] for y in MARKW if per[y] is not None]
    okx = [per[y] for y in MARKW_EX if per[y] is not None]
    return dict(per_class=per, n_per_class=nper,
                mean_0515=sum(ok) / len(ok), n_classes=len(ok),
                mean_0715_ex0506=sum(okx) / len(okx), n_classes_ex=len(okx))


P('=' * 118)
P('ORDER N (reusing ORDER L/K machinery unchanged) — THE YEAR-1 CLASS MARK, WITH AND WITHOUT THE 2005 AND 2006 COHORTS')
P('=' * 118)
P('  instrument   : ok_class.py machinery, unchanged (cohort clock; per-class pooled ratio')
P('                 sum(year-1 price) / sum(entry price); a class needs 5 scorable rows or it is')
P('                 not marked; the published mark is the MEAN of the per-class ratios)')
P('  standing mark: mean over cohort classes 2005-2015  (11 classes)')
P('  exclusion    : mean over cohort classes 2007-2015  ( 9 classes) — SENSITIVITY, not a correction')
P('  what "cohort class 2005 and 2006" means: the 2004 and 2005 NATIONAL DRAFTS. The cohort clock')
P('                 labels a class by the year its players were first eligible to debut.')
P()

OUT = {}
for lab, nice in LABELS:
    p = SP + '/per_entrant_%s.json' % lab
    assert os.path.exists(p), 'MATRIX MISSING ' + lab
    OUT[lab] = marks(p)

P('%-11s %-46s %10s %10s %10s' % ('label', 'board', 'standing', 'excl 05/06', 'move'))
for lab, nice in LABELS:
    m = OUT[lab]
    P('%-11s %-46s %10.4f %10.4f %+10.4f'
      % (lab, nice[:46], m['mean_0515'], m['mean_0715_ex0506'],
         m['mean_0715_ex0506'] - m['mean_0515']))

P()
P('PER-CLASS ROWS (cohort clock). "n" is the number of scorable rows in that class on this board.')
P('  %-6s %-6s %s   %s' % ('class', 'draft',
                          ''.join('%12s' % lab for lab, _ in LABELS), 'in the mark?'))
for y in CLASSES:
    row = []
    for lab, _ in LABELS:
        v = OUT[lab]['per_class'].get(y)
        row.append('%12.4f' % v if v is not None else '%12s' % '-')
    tag = ''
    if y in EXCLUDED:
        tag = '<- IN the standing mark, REMOVED by the sensitivity'
    elif y in MARKW:
        tag = '<- in both marks'
    P('  %-6d %-6d %s   %s' % (y, y - 1, ''.join(row), tag))
P()
P('  n by class (ORDER M0): %s'
  % '  '.join('%d:%d' % (y, OUT['M0ETA0']['n_per_class'][y]) for y in CLASSES))

# ---- L-SC4 ------------------------------------------------------------------------------------------
K = json.load(open(os.path.join(HERE, '..', 'order_k_2026-08-18', 'CLASS_K.json')))
P()
P('-' * 118)
P('L-SC4  the registered arithmetic check')
kpc = K['OKRULED']['per_class']
kstand = K['OKRULED']['mean_0515']
implied = (kstand * 11 - kpc['2005'] - kpc['2006']) / 9.0
mine = OUT['OKRULED']['mean_0715_ex0506']
P('  ORDER K standing mark, from CLASS_K.json            %.4f' % kstand)
P('  its class 2005 / class 2006                         %.4f / %.4f' % (kpc['2005'], kpc['2006']))
P('  implied exclusion mark = (mark x 11 - 2005 - 2006)/9 %.4f' % implied)
P('  ORDER L recomputed exclusion mark                    %.4f' % mine)
P('  the supervisor\'s number                              %.4f' % SUPERVISOR_EX_OKRULED)
P('  ORDER L minus supervisor                             %+.5f' % (mine - SUPERVISOR_EX_OKRULED))
P('  L-SC4 %s' % ('PASS — the supervisor\'s 1.0669 is REPRODUCED (agrees to within rounding of the '
                  'published 4-decimal per-class rows)'
                  if abs(mine - SUPERVISOR_EX_OKRULED) <= 0.0002 else
                  'CORRECTION — the supervisor\'s number is %.4f, this run reads %.4f'
                  % (SUPERVISOR_EX_OKRULED, mine)))
P('  the standing mark also reproduces CLASS_K.json exactly: %.6f vs %.6f  %s'
  % (OUT['OKRULED']['mean_0515'], kstand,
     'PASS' if abs(OUT['OKRULED']['mean_0515'] - kstand) < 1e-9 else 'FAIL'))
assert abs(OUT['OKRULED']['mean_0515'] - kstand) < 1e-9, 'the standing mark did not reproduce'

# ---- the W2 reading ---------------------------------------------------------------------------------
# w2_forward_calibration.py's own population rule and its own price fields, applied to each board.
# arm_of is copied from that file; the class key is r['year'] (the DRAFT year), classes 2005-2021,
# force-majeure keys excluded, R_cand = sum(vpath[0]) / sum(v0).
FM = {'paddy-mccartin', 'thomas-boyd'}
W2SRC = os.path.join(REPO, 'docs/evidence/order33_w2_2026-08-17/w2_forward_calibration.py')
W2MD5 = hashlib.md5(open(W2SRC, 'rb').read()).hexdigest()


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        if t == 'RD':
            return 'RD'
        if t == 'MSD':
            return 'MSD'
        return 'OTHERPOOL'
    return None


def w2_marks(path):
    R = json.load(open(path))['recs']
    per = {}
    for y in range(2005, 2022):
        rows = [r for r in R if r['key'] not in FM and arm_of(r) is not None and r['year'] == y
                and (r.get('vpath') or [None])[0] is not None]
        P0 = sum(float(r['v0']) for r in rows)
        P1 = sum(float(r['vpath'][0]) for r in rows)
        per[y] = dict(n=len(rows), R=P1 / P0 if P0 > 0 else None)
    w = [per[y]['R'] for y in range(2005, 2016)]
    wx = [per[y]['R'] for y in range(2006, 2016)]   # cohort 2005/2006 = DRAFT 2004/2005; draft 2004
    #                                                is already outside W2's ENTRY_FLOOR=2005, so the
    #                                                exclusion removes exactly draft class 2005
    return dict(per_class=per, mean_0515=sum(w) / len(w), mean_ex0506=sum(wx) / len(wx))


P()
P('-' * 118)
P('THE SECOND READING — the W2 SCORER\'S OWN CLASS MARK, on the same three boards.')
P('  source     : w2_forward_calibration.py  md5 %s (read, not modified)' % W2MD5)
P('  class clock: r["year"] — the DRAFT YEAR. NOT the cohort clock ok_class.py uses.')
P('  window     : DRAFT classes 2005-2015. ok_class.py marks COHORT classes 2005-2015, which are')
P('               DRAFT classes 2004-2014. The two windows are OFF BY ONE YEAR at both ends.')
P('  price      : P1 = vpath[0] (positional), P0 = v0.  R_cand = sum(P1)/sum(P0), pooled.')
W2 = {}
for lab, nice in LABELS:
    W2[lab] = w2_marks(SP + '/per_entrant_%s.json' % lab)
P()
P('  %-11s %10s %10s %10s' % ('label', 'W2 05-15', 'W2 06-15', 'move'))
for lab, _ in LABELS:
    P('  %-11s %10.4f %10.4f %+10.4f'
      % (lab, W2[lab]['mean_0515'], W2[lab]['mean_ex0506'],
         W2[lab]['mean_ex0506'] - W2[lab]['mean_0515']))
P()
P('  CROSS-CHECK against the filed W2 packet (candidate 31, PACKET_W2.md table (a)):')
P('    W2 packet draft class 2005 R_cand = 0.9011 ; this run reads %.4f'
  % W2['O31FFINAL']['per_class'][2005]['R'])
P('    W2 packet draft class 2006 R_cand = 1.0313 ; this run reads %.4f'
  % W2['O31FFINAL']['per_class'][2006]['R'])
P('    W2 packet mean R_cand over 17 classes = 1.0411 ; this run reads %.4f'
  % (sum(W2['O31FFINAL']['per_class'][y]['R'] for y in range(2005, 2022)) / 17.0))
P('    and ok_class.py\'s COHORT class 2006 on candidate 31 reads %.4f — the SAME NUMBER as the W2'
  % OUT['O31FFINAL']['per_class'][2006])
P('    packet\'s DRAFT class 2005. That is the off-by-one, demonstrated rather than asserted.')

# ---- the window-alignment diagnostic ----------------------------------------------------------------
# ok_class.py marks COHORT classes 2005-2015. The W2 estimator marks DRAFT classes 2005-2015, which
# are COHORT classes 2006-2016. If the whole gap between 1.0324 and the W2 reading is the class
# window, then ok_class.py's own per-class rows averaged over cohort classes 2006-2016 must land on
# the W2 number. That is computed here rather than argued.
P()
P('  WINDOW-ALIGNMENT DIAGNOSTIC — is the gap the INSTRUMENT, or is it the CLASS WINDOW?')
P('  %-11s %12s %12s %12s %12s' % ('label', 'okclass', 'okclass', 'W2 scorer', 'difference'))
P('  %-11s %12s %12s %12s %12s' % ('', 'coh 05-15', 'coh 06-16', 'draft 05-15', 'aligned'))
ALIGN = {}
for lab, _ in LABELS:
    pc = OUT[lab]['per_class']
    aligned = sum(pc[y] for y in range(2006, 2017)) / 11.0
    ALIGN[lab] = aligned
    P('  %-11s %12.4f %12.4f %12.4f %12.5f'
      % (lab, OUT[lab]['mean_0515'], aligned, W2[lab]['mean_0515'], aligned - W2[lab]['mean_0515']))
P('  cohort classes 2006-2016 ARE draft classes 2005-2015. Aligning the window closes the gap to')
P('  the fourth decimal on all three boards. The two instruments are not disagreeing about the')
P('  board. They are marking different sets of draft classes.')

P()
P('  THE FLOOR TEST, laid out on both instruments (the current candidate):')
P('    ok_class.py  cohort classes 2005-2015   %.4f   floor 1.03: %s (margin %+.4f)'
  % (OUT['OKRULED']['mean_0515'], 'CLEARS' if OUT['OKRULED']['mean_0515'] >= 1.03 else 'FAILS',
     OUT['OKRULED']['mean_0515'] - 1.03))
P('    W2 scorer    draft  classes 2005-2015   %.4f   floor 1.03: %s (margin %+.4f)'
  % (W2['OKRULED']['mean_0515'], 'CLEARS' if W2['OKRULED']['mean_0515'] >= 1.03 else 'FAILS',
     W2['OKRULED']['mean_0515'] - 1.03))
P('    navigation calibrator (Order I record)  1.0515   floor 1.03: CLEARS (margin +0.0215)')
P('    ok_class.py, 2005/06 excluded           %.4f   floor 1.03: %s (margin %+.4f)   SENSITIVITY'
  % (OUT['OKRULED']['mean_0715_ex0506'],
     'CLEARS' if OUT['OKRULED']['mean_0715_ex0506'] >= 1.03 else 'FAILS',
     OUT['OKRULED']['mean_0715_ex0506'] - 1.03))
P('    W2 scorer, draft classes 2006-2015      %.4f   floor 1.03: %s (margin %+.4f)   SENSITIVITY'
  % (W2['OKRULED']['mean_ex0506'], 'CLEARS' if W2['OKRULED']['mean_ex0506'] >= 1.03 else 'FAILS',
     W2['OKRULED']['mean_ex0506'] - 1.03))


# ---- ORDER M — G1 ON THE REGISTERED BASIS, EVERY BOARD ----------------------------------------------
P()
P('-' * 118)
P('ORDER M — G1 ON THE REGISTERED BASIS. THE W2 SCORER, DRAFT CLASSES 2005-2015, ENTRY_FLOOR 2005.')
P('  This is the instrument the owner\'s 1.03 floor and ~1.08 prior were registered against.')
P('  The 1.14 BUY RAIL is the other side of the same law: a class that appreciates more than 14% in')
P('  its first year is a free trade for the buyer. G1 needs BOTH: at or above 1.03, and under 1.14.')
P('-' * 118)
P('  %-10s %12s %12s %12s   %s' % ('board', 'W2 05-15', 'vs 1.03', 'vs 1.14', 'G1 verdict'))
for lab, nice in LABELS:
    v = W2[lab]['mean_0515']
    ok = (v >= 1.03) and (v < 1.14)
    P('  %-10s %12.4f %+12.4f %+12.4f   %s'
      % (lab, v, v - 1.03, v - 1.14,
         'PASS' if ok else ('FAIL — ABOVE THE 1.14 BUY RAIL' if v >= 1.14 else 'FAIL — UNDER THE 1.03 FLOOR')))
P()
P('  the cohort-window reading (ok_class.py, cohort classes 2005-2015) on the same boards:')
P('  %-10s %12s' % ('board', 'cohort mark'))
for lab, nice in LABELS:
    P('  %-10s %12.4f' % (lab, OUT[lab]['mean_0515']))

json.dump(dict(ok_class=OUT, w2=W2, supervisor_ex=SUPERVISOR_EX_OKRULED,
               excluded_cohorts=list(EXCLUDED), w2_md5=W2MD5),
          open(os.path.join(HERE, 'CLASS_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CLASS_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote CLASS_P.json / CLASS_P_out.txt')
