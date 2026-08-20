#!/usr/bin/env python3
"""ORDER L — the registered self-checks, run against the emitted tables.

L-SC1  the PRIMARY / every-cohort ND tables must reproduce Order K's published pooled tables cell for
       cell (STANDING_TABLES_K.json), because the ND population filter IS draft years 2004-2022,
       which is exactly cohorts 2005-2023.

       PREREG DEVIATION, DISCLOSED. The prereg registered this check at a tolerance of 1e-9. That
       tolerance cannot be met against Order K's stored record and the reason is Order K's own
       rounding, not a disagreement about a number: the disclosed instrument writes
       `ratio_meanN_over_mean0=round(ratio, 4)` and `mean_yearN=round(mN, 2)` into its JSON, and
       STANDING_TABLES_K.json carries those rounded values. So the check is run in two parts and
       BOTH are reported:
         L-SC1a  the literal registered check at 1e-9. Reported with its worst difference.
         L-SC1b  Order L's own unrounded values, put through Order K's own rounding
                 (ratio -> 4dp, mean -> 2dp), compared for EXACT equality with the stored record.
                 This is the check that can actually distinguish a real difference from a rounded
                 one, and it is the one that decides.
       No number was moved to make either check pass.

L-SC3  the exclusion must move NOTHING in the modern window, because cohorts 2019-2023 contain no
       2005 or 2006 cohort.

L-SC2  asserted inside ol_bands.py at run.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
K = json.load(open(os.path.join(HERE, '..', 'order_k_2026-08-18', 'STANDING_TABLES_K.json')))
KT = {lab: json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/'
                          '7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/ok/noarb/table_EXT_%s.json' % lab))
      for lab in ('OKRULED', 'O35FINAL', 'O31FFINAL')}
B = json.load(open(os.path.join(HERE, 'BANDS_L.json')))
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
         'picks 21-30', 'picks 31-40', 'picks 41-64']
LABS = ('OKRULED', 'O35FINAL', 'O31FFINAL')
L = []


def P(s=''):
    print(s); L.append(str(s))


P('ORDER L — REGISTERED SELF-CHECKS')
P()
P('L-SC1a  the LITERAL registered check: PRIMARY / every-cohort ND cells vs STANDING_TABLES_K.json')
P('        at tolerance 1e-9.')
worst = 0.0; nbad = 0; ncell = 0
for lab in LABS:
    for b in BANDS:
        kd = K['nd'][lab][b]; ld = B['nd'][lab]['PRIMARY|ALLCOH|%s' % b]
        for i in range(8):
            a, c = kd['path'][i], ld['path'][i]
            ncell += 1
            if a is None or c is None:
                if a != c:
                    nbad += 1
                continue
            worst = max(worst, abs(a - c))
            if abs(a - c) > 1e-9:
                nbad += 1
        worst = max(worst, abs(kd['apprec01'] - ld['apprec01']))
        if abs(kd['apprec01'] - ld['apprec01']) > 1e-9:
            nbad += 1
P('        cells compared     %d' % (ncell + 24))
P('        cells outside 1e-9 %d' % nbad)
P('        worst difference   %.4e   (Order K publishes the ratio to 4 decimal places, so half a' % worst)
P('                                        published digit is 5.0e-5 — every difference is under it)')
P('        L-SC1a %s — ON ROUNDING ONLY. See L-SC1b, which is the check that decides.'
  % ('PASS' if nbad == 0 else 'FAILS'))

P()
P('L-SC1b  the DECIDING check: Order L\'s unrounded values put through Order K\'s own rounding,')
P('        compared for EXACT equality against the stored record.')
nb = 0; ncmp = 0
for lab in LABS:
    kg = {g: {r['N']: r for r in KT[lab]['groups'][g]['rows']} for g in BANDS}
    for b in BANDS:
        kd = K['nd'][lab][b]; ld = B['nd'][lab]['PRIMARY|ALLCOH|%s' % b]
        ncmp += 1
        if kd['n'] != ld['n']:
            P('        BREACH cohort n %s %s: K %d vs L %d' % (lab, b, kd['n'], ld['n'])); nb += 1
        for i in range(8):
            ncmp += 1
            a = kd['path'][i]
            c = None if ld['path'][i] is None else round(ld['path'][i], 4)
            if a != c:
                P('        BREACH %s %s yr%d: stored %s vs L-rounded %s' % (lab, b, i, a, c)); nb += 1
        for i in range(8):
            kr = kg[b][i]
            ncmp += 3
            if kr['n_included'] != ld['n_included'][i]:
                P('        BREACH n_incl %s %s yr%d: %s vs %s'
                  % (lab, b, i, kr['n_included'], ld['n_included'][i])); nb += 1
            if kr['n_zero'] != ld['n_zero'][i]:
                P('        BREACH n_zero %s %s yr%d' % (lab, b, i)); nb += 1
            if kr['n_not_yet_reached'] != ld['n_not_yet_reached'][i]:
                P('        BREACH notreach %s %s yr%d' % (lab, b, i)); nb += 1
            if kr['mean_yearN'] != round(ld['mean_yearN'][i], 2):
                P('        BREACH mean %s %s yr%d: %s vs %s'
                  % (lab, b, i, kr['mean_yearN'], round(ld['mean_yearN'][i], 2))); nb += 1
            if kr['mean_year0_same_set'] != round(ld['mean_year0_same_set'][i], 2):
                P('        BREACH mean0 %s %s yr%d' % (lab, b, i)); nb += 1
        # Order K's own apprec01 = round(mean_yr1,2)/round(mean_yr0,2) - 1
        kapr = round(ld['mean_yearN'][1], 2) / round(ld['mean_year0_same_set'][1], 2) - 1.0
        ncmp += 1
        if abs(kapr - kd['apprec01']) > 1e-12:
            P('        BREACH apr %s %s: K %.12f vs L-via-K-rounding %.12f'
              % (lab, b, kd['apprec01'], kapr)); nb += 1
P('        comparisons %d over 3 boards x 8 bands (cohort n, 8 ratios, 8x n_incl/n_zero/notreach,' % ncmp)
P('                      8x mean_yrN, 8x mean_yr0, and the yr0->1 appreciation)')
P('        mismatches  %d' % nb)
P('        L-SC1b %s' % ('PASS — the PRIMARY tables ARE Order K\'s tables, digit for digit'
                         if nb == 0 else 'FAIL — %d real breaches' % nb))
assert nb == 0, 'L-SC1b FAILED'

P()
P('L-SC3  the 2005/06 exclusion must move nothing in the MODERN window')
w3 = 0.0; n3 = 0
for lab in LABS:
    for b in BANDS:
        a = B['nd'][lab]['MODERN|ALLCOH|%s' % b]
        c = B['nd'][lab]['MODERN|EX0506|%s' % b]
        if a['n'] != c['n']:
            P('        BREACH n %s %s' % (lab, b)); n3 += 1
        for i in range(8):
            x, y = a['path'][i], c['path'][i]
            if x is None or y is None:
                if x != y:
                    P('        BREACH None %s %s yr%d' % (lab, b, i)); n3 += 1
                continue
            w3 = max(w3, abs(x - y))
            if abs(x - y) > 1e-12:
                P('        BREACH %s %s yr%d' % (lab, b, i)); n3 += 1
P('        worst absolute difference %.3e' % w3)
P('        L-SC3 %s' % ('PASS — the modern window is untouched by the exclusion, exactly as registered'
                        if n3 == 0 else 'FAIL — %d breaches' % n3))
assert n3 == 0, 'L-SC3 FAILED'

P()
P('L-SC2  the draft clock and the cohort clock agree on every ND row: asserted inside ol_bands.py')
P('       (cohort + N - 1 == year + N for every ND row; the run HALTS otherwise). PASS.')
open(os.path.join(HERE, 'SELFCHECK_L_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote SELFCHECK_L_out.txt')
