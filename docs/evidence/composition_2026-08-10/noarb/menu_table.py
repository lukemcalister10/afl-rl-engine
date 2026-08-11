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

    # ---------------------------------------------------------------- verdicts
    P()
    P('=' * 116)
    P('### CANDIDATE VERDICTS — three rows are CLOSED, one is open with a diagnosis')
    P('=' * 116)
    P()
    P('  CLOSED — H RUNGS (H120/H125/H130). H is NOT a year-1 dial and no ceiling makes it one.')
    P('    Binding diagnostic: H reaches 0.2% of ND year-1 cells against 11.0% of year-4 cells, ~66x')
    P('    more often at year 4. ITEM C\'s release is evidence-weighted and year 1 is the year with no')
    P('    evidence. Across H 1.13->1.30 the year-1 book moved +0.0002. Not a sizing problem.')
    P()
    P('  CLOSED — A-AS-FLOOR. Zero ND year-1 movers, exactly as predicted BEFORE the emit.')
    P('    ITEM A cannot act at cohort year 1 by a mutual exclusion between its own two gates:')
    P('    reaching _a_blend requires ns>=1, which at year 1 forces gy/fE>=6, which pins')
    P('    LAM_SIT[6]=1.0, which makes A\'s share EXACTLY 0. The floor is max(e_full, b) and at s=0,')
    P('    b IS e_full. Correctly implemented at a site that is structurally silent at year 1.')
    P('    It does act from year 2 (60/96/76/52 cells at yr2-yr5).')
    P()
    P('  CLOSED — A-EVIDENCE-FADED DRAG. Same exclusion, same result: zero ND year-1 movers,')
    P('    matching the filed prediction. Moves yr2-yr5 (60/96/70/48), slightly gentler than the')
    P('    floor as designed. Both A variants are sound designs wired to a year-1-silent site.')
    P()
    P('  OPEN, WITH ITS PRE-REGISTRATION BREACHED AND THE CAUSE NAMED — V4.')
    P('    The pre-registration said the age-22 rate equals the 14% baseline, so year 4 would be')
    P('    unchanged. MEASURED: yr4 1.5310 -> 1.5637, +2.1%. The breach is real and is reported as')
    P('    one. THE DIAGNOSIS, with the candidate causes tested rather than assumed:')
    P()
    P('      (c) KEYING — RULED OUT BY DIRECT TEST. Calling the engine\'s own age_disc() in-process')
    P('          under mode 4 returns EXACTLY 0.14000 at ages 22.0, 22.5 and 23.0 — identical to')
    P('          LENS[bal]=0.14. The rate function is correct and IS current-age keyed.')
    P('      (b) DENOMINATOR — RULED OUT WITH A NUMBER. sum(v0) over the population moves +0.0044%,')
    P('          and only 1 of 1197 v0 rows moves at all. The frozen year-zero surface is intact and')
    P('          the ratio denominator is not the story.')
    P('      (a) MATURE TAIL — WRONG SIGN. Entrants aged 23+ at draft are 26-31 at yr4 and see')
    P('          15-16% under V4, which CUTS. It cannot produce a lift.')
    P()
    P('      THE ACTUAL CHANNEL — THE PEAK ESTIMATE. Restricting to rows whose CONTINUOUS age at')
    P('      year 4 lies in [22,23], where V4 charges exactly the baseline rate, 721 of 815 still')
    P('      moved. For those 815 rows:')
    P('          yr4 value uplift   median +2.459%   mean +2.390%')
    P('          peak field uplift  median +2.793%   mean +5.717%')
    P('      The peak uplift TRACKS the value uplift. The direct discounting of these players is')
    P('      unchanged; what moved is the PEAK ESTIMATE they are priced against, which is itself a')
    P('      forward-discounted object computed where V4 charges 11-13% rather than 14%. So the')
    P('      age-dynamic discount does not stay inside the year it is keyed to — it propagates')
    P('      through the peak estimate into later years.')
    P()
    P('      CONSEQUENCE: V4\'s year-4 number is NOT a clean "unchanged" baseline, and the peak/yr0')
    P('      and peak/yr1 columns for every discount variant should be read knowing the peak itself')
    P('      moved. This is REPORTED, NOT REPAIRED — changing where the peak estimate takes its')
    P('      discount is a wiring decision outside this act, and it is the owner\'s call.')
    P()
    P('=' * 116)
    P('### THE DECOMPOSITION COLUMN — where the year-1 drop actually lives')
    P('=' * 116)
    P('  Single-item removal on the same instrument (full table in DECOMP.txt). Of the -0.1265')
    P('  (-11.3%) main->FULL year-1 drop:')
    P()
    P('      #336 reference layer   80.5%      (657 ND year-1 cells moved)')
    P('      the surprise law       10.8%      (269)')
    P('      ITEM A                  0.0%      (0)')
    P('      ITEM H                  0.0%      (1)')
    P('      interaction residual    8.8%      (not normalised away)')
    P()
    P('  READ THIS BESIDE THE VERDICTS. Every counterbalance ordered so far — H rungs, A-floor,')
    P('  A-drag — acts on ITEM A\'s site or ITEM C\'s. Those sites jointly own 0.0% of the year-1')
    P('  drop. The only candidate that moves year 1 at all is the discount (V4: 0.9974 -> 1.1382),')
    P('  and it does so by repricing the whole book rather than by restoring what was taken.')
    P('  A year-1 counterbalance that acts where the value was lost would have to act on #336 or')
    P('  the surprise law. THAT IS THE OWNER\'S CALL. Nothing is re-sited here.')
    P()
    P('=' * 116)
    P('### HALT-GRADE — ITEM A\'S RULED PURPOSE IS PARTLY UNDELIVERED  (full audit: A_YEAR1_AUDIT.md)')
    P('=' * 116)
    P('  D1, the defect A was ruled to fix, fires at the MOMENT OF QUALIFICATION — a player\'s first')
    P('  qualifying game, which for a first-season qualifier IS cohort year 1. At exactly that moment')
    P('  A\'s share is EXACTLY 0, so the taught year-0 correction is still discarded there, as before')
    P('  ITEM A. Built-A repairs only the years-2+, partial-season version of the defect.')
    P()
    P('  Measured over all 720 ND cells A actually moves, by games in that as-of season:')
    P('      >=6 games (full season, lam=1 pins the share to 0)     0 cells')
    P('      1-5 games (partial)                                  531')
    P('      0 games / absent, with a prior qualifying season      189')
    P('  A NEVER MOVES A >=6-GAME ROW AT ANY CAREER YEAR.')
    P()
    P('  THE FADE LADDER (v1 0.3589 -> v6 0.0038) DOES NOT CONTRADICT THIS. It was measured on a')
    P('  synthetic holding "4 games this season" — below the six-game pin — to isolate the pedigree')
    P('  fade while the games factor sat fixed. Its "v1" means career year 1 WITH 4 GAMES, not cohort')
    P('  year 1. item_a_verify.py itself reported the real-population v1 as 0.0000 and explained why;')
    P('  that disclosure was not carried into the act\'s account of what A delivers.')
    P()
    P('  Do NOT weigh A\'s contribution to the year-1 question as delivered. The decomposition already')
    P('  shows the consequence: ITEM A owns 0.0% of the year-1 drop.')
    P()
    P('=' * 116)
    P('### SPECIFIED BUT NOT BUILT — THE RAMP DE-COUPLE  (RAMP_DECOUPLE_SPEC.md)')
    P('=' * 116)
    P('  One six-game threshold currently does two jobs: ADMISSION (ns>=1 needs a qualifying season)')
    P('  and SATURATION (lam hits LAM_SIT[6]=1.0, zeroing A). At year 1 they are mutually exclusive.')
    P('  The row: KEEP the admission bar, de-couple only the saturation so the production weight')
    P('  saturates on CAREER games (~15-20) instead of the within-season six — so a qualified year-1')
    P('  row carries real anchor weight and A lives at year 1 as ruled.')
    P()
    P('  PRE-REGISTERED: measurable ONLY with A-FLOOR or A-DRAGFADE. With the SYMMETRIC blend it would')
    P('  let the anchor drag hot year-1 rows DOWN and DEEPEN the dip — expected direction filed in')
    P('  advance. One trap named: sitout_ev shares the LAM_SIT ramp for a different purpose, so only')
    P('  A\'s copy may de-couple or the whole sit-out population moves as a side effect.')
    P()
    P('  SCOPE CAVEAT: it makes A deliver its ruled purpose. It is NOT a counterbalance to the')
    P('  measured drop, which lives 80.5% in #336 and 10.8% in the surprise law. Cost if ruled in:')
    P('  2 emits plus one identity proof. NOT BUILT — no engine file touched, no dial declared.')

    json.dump({lab: {g: rr(T[lab], g) for g in GROUPS} for lab, _, _ in have},
              open(os.path.join(HERE, 'MENU.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'MENU.txt'), 'w').write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
