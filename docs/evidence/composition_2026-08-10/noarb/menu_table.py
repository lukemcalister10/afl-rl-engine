"""THE SITTING'S MENU — every counterbalance candidate on ONE canonical table.

All progression numbers are read out of noarb_table_338.py's own json (the unmodified canonical
script, md5 0f8220351c64c56ccfa90c60edcdfa5f). The discount schedules are imported from
decision_table.py so there is ONE implementation of each variant's rate, not a retyped copy.

INSTRUMENT LABEL, carried on every figure: canonical no-arb table, unmodified · population = harness
load_matrix ND filter (teaches_curve & pick 1..64 & draft year 2004..2022) = 1197 entrants, identical
on every candidate · aggregation = pooled book ratio mean(value at year N)/mean(v0) over the same
included set · busts score 0 and stay in the denominator · window end 2026.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from decision_table import rate, TYPICAL_DRAFT_AGE   # ONE implementation of the discount schedules

GROUPS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64']

# (label, family, description) — order is the reading order for the sitting
MENU = [
    ('main',   'reference', 'origin/main, pre-act'),
    ('FULL',   'reference', 'the composition package as it stands (C_H=1.13)'),
    ('H120',   'H rungs',   'FULL, cap-release ceiling H=1.20'),
    ('H125',   'H rungs',   'FULL, H=1.25'),
    ('H130',   'H rungs',   'FULL, H=1.30'),
    ('AFLOOR', 'ITEM A',    'A as a FLOOR — one-way borrowing, prior supports from below'),
    ('ADRAG',  'ITEM A',    'A with EVIDENCE-FADED DRAG — pull-down weakens as proof accumulates'),
    ('V4',     'discount',  'age-dynamic discount V4 (11/12/13/14, glide 14-15, 15, 16)'),
    ('V1',     'discount',  'V1 13/15 — retired to the root act unless the owner wants it'),
    ('V2',     'discount',  'V2 four-band — retired to the root act unless the owner wants it'),
    ('V3',     'discount',  'V3 10/11/12/13/14 — retired to the root act unless the owner wants it'),
]

L = []
def P(s=''):
    print(s); L.append(s)


def load(v):
    p = os.path.join(HERE, 'table_%s.json' % v)
    return json.load(open(p)) if os.path.exists(p) else None


def rr(t, g):
    return {r['N']: r['ratio_meanN_over_mean0'] for r in t['groups'][g]['rows']}


def peak_of(r):
    pk = max(r.values())
    return pk, [n for n in sorted(r) if r[n] == pk][0]


def main():
    T = {}
    for lab, _, _ in MENU:
        t = load(lab)
        if t is not None:
            T[lab] = t
    have = [x for x in MENU if x[0] in T]
    absent = [x[0] for x in MENU if x[0] not in T]

    P('=' * 116)
    P('THE SITTING\'S MENU — all counterbalance candidates, one canonical table')
    P('=' * 116)
    P('  instrument : noarb_table_338.py UNMODIFIED (md5 0f8220351c64c56ccfa90c60edcdfa5f)')
    P('  population : 1197 ND teaching entrants (picks 1-64, draft 2004-2022), IDENTICAL on every row')
    P('  aggregation: pooled book ratio, mean(value at year N)/mean(v0) over the same included set')
    if absent:
        P('  NOT PRESENT: %s (no table emitted)' % ', '.join(absent))
    P()

    # ---------------------------------------------------------------- progression + envelope
    P('-' * 116)
    P('### PROGRESSION AND ENVELOPE — %s' % GROUPS[0])
    P('-' * 116)
    hdr = ('  %-8s %-10s' % ('candidate', 'family') + ''.join('%8s' % ('yr%d' % n) for n in range(0, 6))
           + '%9s%8s%10s%10s' % ('peak', 'at', 'peak/yr0', 'peak/yr1'))
    P(hdr)
    P('  ' + '-' * (len(hdr) - 2))
    for lab, fam, _ in have:
        r = rr(T[lab], GROUPS[0]); pk, at = peak_of(r)
        P('  %-8s %-10s' % (lab, fam) + ''.join('%8.4f' % r[n] for n in range(0, 6))
          + '%9.4f%8s%10.3f%10.3f' % (pk, 'yr%d' % at, pk, pk / r[1] if r[1] else float('nan')))
    P()
    P('  Envelope reference: peak/yr0 ~ 1.40 and peak/yr1 ~ 1.30. A FRAME FOR JUDGING, NOT A TARGET.')
    P('  The peak/yr0 gap is PRE-EXISTING — already open on main before any item of this act applies.')
    P()

    # ---------------------------------------------------------------- young/peak, all bands
    P('=' * 116)
    P('### YOUNG/PEAK CONTRAST vs main — and whether the restoration lands where the cut fell')
    P('=' * 116)
    P('  The package\'s cut concentrated in picks 21-64. A candidate that restores only 1-20 has not')
    P('  restored the band that actually lost. 0.00% means main\'s contrast is exactly restored.')
    P()
    base = {}
    for g in GROUPS:
        rm = rr(T['main'], g); pk, _ = peak_of(rm); base[g] = rm[1] / pk
    P('  %-8s %-10s' % ('candidate', 'family') + ''.join('%18s' % g for g in GROUPS))
    P('  ' + '-' * 74)
    for lab, fam, _ in have:
        cells = []
        for g in GROUPS:
            r = rr(T[lab], g); pk, _ = peak_of(r)
            cells.append('%+17.2f%%' % (100 * ((r[1] / pk) / base[g] - 1)))
        P('  %-8s %-10s' % (lab, fam) + ''.join(cells))
    P()

    # ---------------------------------------------------------------- free money per candidate
    P('=' * 116)
    P('### THE FREE-MONEY MARGIN AT yr0->yr1, PER CANDIDATE, AGAINST ITS OWN DISCOUNT')
    P('=' * 116)
    P('  Typical draft age is 18.00 (MEASURED: median age_draft in every band), so the holder is 18')
    P('  at the start of the first step. Each candidate is judged against the rate ITS OWN schedule')
    P('  charges an 18-year-old — never another candidate\'s. A NEGATIVE margin is free money: the')
    P('  book grows faster than the engine discounts the future, and holding dominates.')
    P()
    P('  %-8s %-10s %12s %12s %12s %10s'
      % ('candidate', 'family', 'yr1', 'apprec.', 'own disc.', 'margin'))
    P('  ' + '-' * 70)
    for lab, fam, _ in have:
        r = rr(T[lab], GROUPS[0])
        ap = r[1] / r[0] - 1.0
        d = rate(lab, TYPICAL_DRAFT_AGE)
        mg = d - ap
        P('  %-8s %-10s %12.4f %11.2f%% %11.2f%% %9.2f%%%s'
          % (lab, fam, r[1], 100 * ap, 100 * d, 100 * mg, '   <-- ARB' if mg < 0 else ''))
    P()
    P('  NOTE ON THE DISCOUNT CANDIDATES: a lower discount is not a free win. It lifts the book AND')
    P('  narrows this margin at the same time, because the same schedule that raises young value is')
    P('  the schedule the appreciation is measured against. That is why the margin is printed beside')
    P('  the lift rather than under it.')
    P()

    # ---------------------------------------------------------------- what is not here
    P('=' * 116)
    P('### WHAT THIS TABLE DOES NOT CONTAIN')
    P('=' * 116)
    P('  MIXES ARE NOT MEASURED. The menu names mixes (e.g. A-floor + V4) as candidates, and none is')
    P('  on this table because none has been emitted. Their effects are NOT additive and must not be')
    P('  read off by adding two rows: A-floor and the discount variants both act on the young end,')
    P('  and the per-item decomposition already shows this package\'s items interact. Any mix the')
    P('  sitting wants costs one emit (~2.5 min) and gets its own row, measured, not inferred.')
    P()
    P('  H IS ON THE TABLE BUT IS NOT A YEAR-1 CANDIDATE. The H rungs are shown because they were')
    P('  ordered and run, but the binding diagnostic (H_LADDER.txt) shows H reaches 0.2% of year-1')
    P('  cells and 11.0% of year-4 cells — it is a years-3-to-5 dial, and no value of H changes that.')
    P('  Its rows are here for completeness, not as live counterbalance options.')

    json.dump({lab: {g: rr(T[lab], g) for g in GROUPS} for lab, _, _ in have},
              open(os.path.join(HERE, 'MENU.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'MENU.txt'), 'w').write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
