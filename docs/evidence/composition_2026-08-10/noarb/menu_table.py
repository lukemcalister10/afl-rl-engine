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
    # ---- ROUND 3 (build brief 5248006413). Pre-registration: PREREG_ROUND3.md, filed before the emits.
    ('V5',     'discount',  "V5 — the owner's fifth ladder, 22/23=14% shelf EXPLICIT (12/12.5/13/13.5/14/14/14.5/15/15/15.5/16)"),
    ('AGSATF', 'de-couple', 'FULL + ramp de-couple (G_SAT=18) + A-FLOOR — anchor supports, never drags'),
    ('AGSATD', 'de-couple', 'FULL + ramp de-couple (G_SAT=18) + A-DRAGFADE — drag permitted, faded by proof'),
    ('C336P',  '#336 split','FULL with the #336 P-LEG reverted (RL_336_NOP=1) — counterfactual, never a candidate'),
    ('C336E',  '#336 split','FULL with the #336 DE-SURVIVORED E-LEVELS reverted (RL_336_SURVLVL=1 RL_336_CLAMP=1) — counterfactual'),
    ('C336C',  '#336 split','FULL with the #336 PAR_BUILD LEG reverted (RL_336_PARSURV=1) — counterfactual'),
    ('no336',  '#336 split','FULL with the WHOLE #336 layer reverted (whole-commit revert of 9a8bbd9) — counterfactual'),
    # ---- ORDER 4. Pre-registration: PREREG_ORDER4.md; honesty test: XW_HONESTY.txt. Cleared before wiring.
    ('XW',     'DESIGN',    'FULL + exposure-weighted par sample (RL_336_XW=1, cap 18 games) — THE #336 DESIGN, dial-gated, default OFF'),
    # ---- ORDER 5 (owner: "a stacked version"). Pre-registration: PREREG_ORDER5.md.
    ('STACK',  'STACKED',   'FULL + XW + V5 together — judged against V5\'s own 12.00% young rate, the tighter frame'),
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
    P('### THE FINAL TABLE — the owner\'s shortlist on one instrument, INCLUDING THE STACK')
    P('=' * 116)
    P('  instrument: noarb_table_338.py UNMODIFIED (md5 0f8220351c64c56ccfa90c60edcdfa5f) · population')
    P('  1197 ND teaching entrants (picks 1-64, classes 2004-2022), IDENTICAL on every row · aggregation')
    P('  pooled book ratio mean(value at year N)/mean(v0) over the same included set · busts score 0 and')
    P('  stay in the denominator. EVERY candidate is DIAL-GATED and DEFAULT OFF; none is adopted.')
    P()
    P('  EACH ROW IS JUDGED AGAINST THE RATE ITS OWN SCHEDULE CHARGES AN 18-YEAR-OLD, never another')
    P('  row\'s. A NEGATIVE margin is FREE MONEY: the book grows faster than the engine discounts, and')
    P('  holding dominates. That is the disqualifying condition, not a preference.')
    P()
    hdr = ('  %-8s %-9s' % ('row', 'family') + ''.join('%8s' % ('yr%d' % n) for n in (1, 2, 3, 4, 5))
           + '%9s%8s%9s%9s' % ('apprec', 'disc', 'margin', 'verdict'))
    P(hdr); P('  ' + '-' * (len(hdr) - 2))
    for lab, fam in (('main', 'reference'), ('FULL', 'reference'), ('V2', 'discount'), ('V5', 'discount'),
                     ('XW', 'DESIGN'), ('AGSATF', 'de-couple'), ('AGSATD', 'de-couple'), ('STACK', 'STACKED')):
        if lab not in T: continue
        r = rr(T[lab], GROUPS[0]); d = rate(lab, TYPICAL_DRAFT_AGE); ap = r[1] - 1.0; m = d - ap
        P('  %-8s %-9s' % (lab, fam) + ''.join('%8.4f' % r[n] for n in (1, 2, 3, 4, 5))
          + '%8.2f%%%7.2f%%%8.2f%%%9s' % (100*ap, 100*d, 100*m, 'ARB' if m < 0 else 'legal'))
    P()
    P('  READING THE ROWS, in one line each:')
    P('    main    the engine before this act. The frame everything else is measured against.')
    P('    FULL    the composition package as it stands. Year 1 lost 11.3% and this is where it sits.')
    P('    V2      an earlier owner ladder, kept for comparison; it has NO 14% shelf at age 22.')
    P('    V5      the owner\'s fifth ladder, 22/23 shelf explicit. Lifts year 1 and stays legal.')
    P('    XW      the #336 design: the par sample weighted by exposure. Largest single legal lift.')
    P('    AGSATF  the ramp de-couple as a FLOOR. Makes ITEM A act at year 1 at last; tiny in size.')
    P('    AGSATD  the ramp de-couple with faded drag. It LOWERS year 1 — see the de-couple section.')
    P('    STACK   XW and V5 together, on V5\'s own discount frame.')
    P()
    P('=' * 116)
    P("### ROUND 3 — V5, THE OWNER'S FIFTH LADDER  (the question it was built to answer, and the answer)")
    P('=' * 116)
    P('  The owner asked why year 4 is better under V4 than V2 "when both have 14 from 22", and proposed')
    P('  V5. THE PREMISE DOES NOT HOLD, and V5 is built on the correction. V2 has NO 14% shelf at 22: its')
    P('  knots join 21 smoothly to 25, so V2 charges 13.5% at age 22. V4 pins 22 at exactly 14%. Both')
    P('  reach 15% at 25, so the 25-vs-26 boundary the owner named is not the difference either.')
    P('  V5 states the 22/23 shelf as its OWN pair of knots, which is what distinguishes it from V2.')
    P()
    P('  age            18     19     20     21     22     23     24     25     26     27    28+')
    P('  ---------------------------------------------------------------------------------------')
    P('  V2 (%)       12.0   12.0   13.0   13.0   13.5   14.0   14.5   15.0   15.0   15.0   16.0')
    P('  V4 (%)       11.0   11.0   12.0   13.0   14.0   14.0   14.5   15.0   15.0   15.0   16.0')
    P('  V5 (%)       12.0   12.5   13.0   13.5   14.0   14.0   14.5   15.0   15.0   15.5   16.0')
    P('  (verified by direct call of the engine\'s own _pw_interp BEFORE the emit)')
    P()
    P('  V5 IS THE FIRST DISCOUNT VARIANT THAT LIFTS YEAR 1 AND STAYS LEGAL.')
    P('    yr1 1.0734   yr4 1.5665   margin +4.66% — POSITIVE, i.e. NO ARBITRAGE.')
    P('    V4 (+13.82% appreciation vs 11.00% charged) and V3 (+14.56% vs 10.00%) are both ARB. V5')
    P('    lifts year 1 by 7.6% over FULL and still charges more than the book grows.')
    P()
    P('  PRE-REGISTERED (PREREG_ROUND3.md), TWO BREACHED, REPORTED AS BREACHES:')
    P('    P1.1  yr4 in 1.555-1.570 and above FULL   MEASURED 1.5665                       HELD')
    P('    P1.2  yr1 in 1.100-1.135 (between V2/V4)  MEASURED 1.0734 — BELOW V2\'s 1.0933   BREACHED')
    P('    P1.3  margin better than V4\'s -2.82%,     MEASURED +4.66% — better than V4 but')
    P('          registered range -1.5% to +2.5%     outside the registered band           BREACHED')
    P()
    P('  THE SEAT\'S ERROR, OWNED. P1.2 assumed V5 would sit BETWEEN V2 and V4 on year 1. It cannot:')
    P('  V5 is dearer than V2 at ages 19, 21, 22 and 27 and equal everywhere else, so V5 DOMINATES V2 as')
    P('  a discount schedule and must lift year 1 LESS than V2, not more. The arithmetic was available')
    P('  before the emit from the same knot table printed above and the seat did not do it. The margin')
    P('  band in P1.3 inherited the same error. The measured numbers stand; the prediction does not.')
    P()
    P('  WHY THE yr4 SHELF WORKED. P1.1 held: V5 and V4 are IDENTICAL at ages 22-26, so a player drafted')
    P('  at 18 sees the same rate through his year-4 season, and yr4 lands 1.5665 against V4\'s 1.5637 —')
    P('  a 0.2% gap, from the young-side rate reaching year 4 through the PEAK ESTIMATE. That channel is')
    P('  the one the V4 diagnosis already named: the peak a player is priced against is itself a')
    P('  forward-discounted object, so an age-keyed discount does not stay inside the year it is keyed')
    P('  to. Read every discount variant\'s peak/yr0 and peak/yr1 column knowing the peak itself moved.')
    P()
    P('=' * 116)
    P('### ROUND 3 — THE RAMP DE-COUPLE, MEASURED  (was SPECIFIED BUT NOT BUILT; it is now built and emitted)')
    P('=' * 116)
    P('  One six-game threshold was doing two jobs: ADMISSION (ns>=1 needs a qualifying season) and')
    P('  SATURATION (lam hits LAM_SIT[6]=1.0, zeroing A). At year 1 they are mutually exclusive, so A')
    P("  moved 0 of 1197 year-1 cells. The change keeps the admission bar EXACTLY as built and de-couples")
    P('  only the saturation: the production weight now saturates on CAREER games against G_SAT.')
    P('  Dial RL_A_GSAT, default 0 (off, byte-exact). G_SAT=18 is the SEAT\'S choice inside the spec\'s')
    P('  open ~15-20 range — not an owner number, not measured-optimal.')
    P()
    P('  form                          yr1      yr4    margin   yr1 movers  (>=6g)   up/down   median move')
    P('  ' + '-' * 100)
    for lab, txt, mv, g6, up, dn, med in (
            ('FULL     (reference)', '', 0, 0, 0, 0, None),
            ('AGSATF   de-couple + A-FLOOR', '', 41, 41, 41, 0, 4.19),
            ('AGSATD   de-couple + A-DRAGFADE', '', 294, 294, 41, 253, -3.58)):
        r = rr(T[lab.split()[0]], GROUPS[0]) if lab.split()[0] in T else None
        if r is None: continue
        d = rate(lab.split()[0], TYPICAL_DRAFT_AGE)
        m = 100 * (d - (r[1] - 1.0))
        P('  %-28s %8.4f %8.4f %8.2f%% %10d %8d %6d/%-5d %s'
          % (lab, r[1], r[4], m, mv, g6, up, dn,
             ('%+.2f%%' % med) if med is not None else '   --'))
    P()
    P('  THE MOVERS ARE EXACTLY THE ROWS ITEM A COULD NEVER REACH. Every single year-1 mover in both')
    P('  forms is a FULL-SEASON row (>=6 games) — 41 of 41 and 294 of 294. Under built-A that count was')
    P('  ZERO at every career year, by the mutual exclusion. The de-couple does what it was specified to.')
    P()
    P('  PRE-REGISTERED AND HELD (PREREG_ROUND3.md, filed before the emits):')
    P('    P2.1  A-FLOOR yr1 RISES, small          predicted 1.000-1.020   MEASURED 1.0001   HELD')
    P('    P2.2  A-DRAGFADE yr1 FALLS below FULL   predicted 0.960-0.997   MEASURED 0.9822   HELD')
    P('    P2.3  yr1 full-season movers nonzero    predicted > 0           MEASURED 41 / 294 HELD')
    P('    P2.4  yr4 within +/-0.5% of FULL        predicted +/-0.5%       MEASURED +0.22% / +0.12%  HELD')
    P('    P2.6  sitout_ev byte-unchanged          md5 must match          MEASURED match     HELD')
    P()
    P('  THE SPEC\'S OWN EXPECTATION IS BREACHED FOR A-DRAGFADE, AND THE BREACH WAS FILED IN ADVANCE.')
    P('  RAMP_DECOUPLE_SPEC.md predicted "Year 1 rises, by construction" for BOTH admissible forms and')
    P('  put A-DRAGFADE "between FULL and de-couple+floor". It falls BELOW FULL instead. The reason was')
    P('  measured before the emit and written into the pre-registration: of the 416 rows that reach the')
    P('  A site at year 1, 83.2% are DRAG rows (anchor BELOW production) and the pooled anchor sits at')
    P('  0.515x production. The spec reasoned from the anchor being a support; on the real year-1')
    P('  population it is mostly a drag. A-FLOOR is inert on drag rows, which is why it still rises.')
    P()
    P('  THE sitout_ev TRAP, PROVEN CLOSED (decouple_proof_OFF.txt / decouple_proof_ON.txt):')
    P('    static  : every read of the dial is inside _a_share; sitout_ev\'s body contains no reference.')
    P('    dynamic : sitout_ev over 15,882 (player x year x e_full) evaluations hashes to')
    P('              2a11b8b17a854e33d9d51ab050581021 under RL_A_GSAT=0 AND under RL_A_GSAT=18 — IDENTICAL.')
    P('    non-vacuity: _a_share over the same pass hashes 53640643... vs 88b9c45c... — DIFFERENT. So the')
    P('              proof can tell "the dial did nothing anywhere" apart from "it did something, elsewhere".')
    P()
    P('  MRAZ, per form (board build, his pick-35 frozen ruler PVC0[35]=561):')
    P('    FULL 1649 = 2.939x   A-FLOOR 1649 = 2.939x   A-DRAGFADE 1649 = 2.939x   (V5: 1712 = 3.052x)')
    P('    He is UNMOVED by both de-couple forms: he sat out his first season, so he is on the ns==0')
    P('    sit-out arm, which this dial does not touch. Inside the owner\'s <=3.0x target in every arm')
    P('    except V5, which sits at 3.052x — inside the 3.5-3.8x slack the owner granted.')
    P()
    P('  SCOPE CAVEAT, UNCHANGED AND STILL BINDING: this makes ITEM A deliver its ruled purpose. It is')
    P('  NOT a counterbalance to the measured year-1 drop. A-FLOOR recovers +0.0027 of the -0.1265.')
    P()
    P('=' * 116)
    P('### ROUND 3 — THE #336 CHANNEL SPLIT  (the owner asked what a #336 design would look like)')
    P('=' * 116)
    P('  #336 owns 80.5% of the main->FULL year-1 drop: FULL 0.9974 -> no336 1.0992, a give-back of')
    P('  +0.1018 (about -9.1pp of the -11.3% total). Until now it was ONE LUMP with no kill-switch.')
    P('  Round 3 gives it three declared channel levers and splits the lump by counterfactual emit.')
    P()
    P('  channel                                        lever                    yr1     give-back   share')
    P('  ' + '-' * 106)
    F1 = rr(T['FULL'], GROUPS[0])[1]; W1 = rr(T['no336'], GROUPS[0])[1] - F1
    rowspec = [('(a) the P-LEG  (bust charge on picks/unresolved)', 'RL_336_NOP=1', 'C336P'),
               ('(b) the DE-SURVIVORED E-LEVELS', 'RL_336_SURVLVL=1 RL_336_CLAMP=1', 'C336E'),
               ('(c) the PAR_BUILD LEG (the fitted par sample)', 'RL_336_PARSURV=1', 'C336C')]
    tot = 0.0
    for name, lev, lab in rowspec:
        v = rr(T[lab], GROUPS[0])[1]; gb = v - F1; tot += gb
        P('  %-46s %-24s %8.4f %+10.4f %7.1f%%' % (name, lev, v, gb, 100 * gb / W1))
    P('  %-46s %-24s %8s %+10.4f %7.1f%%' % ('SUM OF THE THREE', '', '', tot, 100 * tot / W1))
    P('  %-46s %-24s %8s %+10.4f %7.1f%%' % ('INTERACTION RESIDUAL (printed, not normalised)', '', '',
                                             W1 - tot, 100 * (W1 - tot) / W1))
    P('  %-46s %-24s %8.4f %+10.4f %7.1f%%' % ('WHOLE LAYER (whole-commit revert of 9a8bbd9)',
                                               'no dial exists', rr(T['no336'], GROUPS[0])[1], W1, 100.0))
    P()
    P('  THE ANSWER, AND IT REFUTES THE SEAT\'S OWN PRE-REGISTRATION. P3.1 predicted the P-leg would be')
    P('  the LARGEST channel at over 50% of the give-back. It is the SMALLEST, at -0.2% — and the sign')
    P('  is negative, so reverting the bust charge makes year 1 very slightly WORSE. BREACHED, reported')
    P('  as a breach, and nothing was retuned to rescue it. P3.3 predicted the par leg under 20%; it is')
    P('  89.2%. BREACHED. Only P3.2 (E-levels under 20%) held, at 9.7%.')
    P()
    P('  WHY THE P-LEG IS INERT, from the code: amendment 3 already reconciled the anchor-side charge to')
    P('  D = 0.999644 ("the forward band already charges establishment failure in full"), so a REAL')
    P('  player never sees P at his anchor. What P still scales is BASEPK_REG, the PICK table — and the')
    P('  year-zero price the cohort ratio divides by comes from the FROZEN v0 surface, not from that')
    P('  table. Measured: 1 v0 mover out of 1197 in every arm, sum(v0) within 0.02%.')
    P()
    P('  THE CEILING FOR A RE-TIMING DESIGN, which is what the owner\'s question was really asking:')
    P('  bust charge that can be honestly RE-TIMED across career years is the P-leg, and the P-leg owns')
    P('  -0.2% of the -9.1pp, i.e. about -0.02pp. THE RE-TIMEABLE CHANNEL IS EMPTY. A design that')
    P('  re-times the bust charge cannot recover the year-1 drop, because the year-1 drop is not there.')
    P()
    P('  WHERE IT ACTUALLY IS: 89.2% in the par_build leg — the change to WHICH SEASONS the par surface')
    P('  is fitted to (from ">=6 games at that tenure" to "every ever-establisher\'s played season").')
    P('  That change is FRONT-LOADED by construction and the effect is reproduced independently in')
    P('  design336_probe_out.txt: the tenure-1 cell level falls to 0.897 of the old sample and the cut')
    P('  fades to 0.978 by tenure 6. Its price effect therefore lands on year 1 and washes out by year 6.')
    P()
    P('  NOT DESIGN TERRITORY, and this is the owner\'s standing ruling, not a seat opinion: channels (b)')
    P('  and (c) ARE the honesty repair. Softening the de-survivored levels re-admits survivor bias.')
    P('  Their counterfactual arms exist to BOUND the design and are not candidates. NO DESIGN SHIPS')
    P('  FROM THIS TABLE; see DESIGN_336_MEMO.md for the two mechanisms probed and their ceilings.')
    P()
    P('  ONE HONEST QUALIFICATION ON ROW (b). The amendment-2 monotonicity guard (basepk_est >= basepk)')
    P('  is ALREADY BREACHED AT THE COMPOSED BUILD in 1 cell — (KPD, band 0), by -0.4465 points')
    P('  (-0.59%). _A2_GUARD is only a computed list; nothing raises on it. Row (b)\'s arm carries 2')
    P('  breaches instead of 1, in RUCK bands 0 and 1 (-0.2515 and -0.6190). Isolated by probe: the')
    P('  v3.4 clamp alone does not cause it, the survivor sample does. Row (b) is therefore the least')
    P('  trustworthy of the three, and it is the smallest, so the reading is not sensitive to it.')
    P()
    P('=' * 116)
    P('### ORDER 4 — THE #336 DESIGN: EXPOSURE-WEIGHTED PAR  (owner word "let\'s look at your 336 design")')
    P('=' * 116)
    P('  WHAT IT IS. The par surface is a PER-GAME benchmark, and it is the denominator of ITEM C\'s')
    P('  Q = sa/par where sa is the career GAMES-WEIGHTED average. Today every observation enters the fit')
    P('  with EQUAL weight, so a one-game debut counts as much as a twenty-game season and the fit answers')
    P('  "the average of season-averages". The dial weights each observation by its own exposure,')
    P('  min(games, 18). NOTHING IS DROPPED: every row of the #336 bust-inclusive sample stays in.')
    P()
    P('  IT CLEARED A KILL TEST BEFORE IT WAS WIRED. The suspicion was that exposure weighting is survivor')
    P('  bias by another door, because busts have little exposure. Three pre-registered criteria, all')
    P('  fixed in PREREG_ORDER4.md before the grid ran (full grid: XW_HONESTY.txt):')
    P('    A  it must not reproduce the survivors-only sample. 44 informative (tenure x band) cells:')
    P('       7 coincide, 37 DIVERGE. Pooled, tenure 1 coincides and tenures 2-6 all diverge.')
    P('    B  the sub-6-game rows must keep real weight. They keep 4.8% of pooled fit weight against')
    P('       19.7% of the row count (11.5% vs 36.7% at tenure 1) — down-weighted ~4x, NOT dropped.')
    P('    C  the added rows must still move the estimate. They pull it 3.05% below the survivors-basis')
    P('       at tenure 1, fading to 0.54% at tenure 6.')
    P('  AND THE FINDING THAT SETTLES IT: at tenure 1 in the LATE pick bands the exposure-weighted par')
    P('  lands BELOW the old survivors-only par (21-27: 54.37 vs 54.75 · 28-35: 55.13 vs 56.75 · 36-48:')
    P('  54.82 vs 56.20 · 49-99: 59.78 vs 59.91). In exactly the cells where late-pick bust risk')
    P('  concentrates it is HARSHER than the sample the owner ruled out. Survivor bias cannot do that.')
    P()
    P('  THE MEASURED ROW, canonical instrument:')
    P()
    P('    row                       yr1      yr2      yr3      yr4      yr5   apprec.   disc   margin')
    P('    ' + '-' * 88)
    for lab in ('main', 'FULL', 'XW', 'C336C', 'no336'):
        if lab not in T: continue
        r = rr(T[lab], GROUPS[0]); d = rate(lab, TYPICAL_DRAFT_AGE); ap = r[1] - 1.0
        P('    %-20s %8.4f %8.4f %8.4f %8.4f %8.4f %8.2f%% %6.2f%% %7.2f%%'
          % (lab, r[1], r[2], r[3], r[4], r[5], 100*ap, 100*d, 100*(d-ap)))
    P()
    P('    yr1 movers 651 (545 up, 106 down) · v0 movers 1 of 1197 (the same pre-existing row every arm')
    P('    carries), sum(v0) +0.017% · Mraz board 1707 = 3.043x his pick-35 ruler (FULL 1649 = 2.939x),')
    P('    inside the owner\'s 3.5-3.8x slack · amendment-2 guard 1 failing cell, the SAME cell as the')
    P('    reference config, NO added failures.')
    P()
    P('  PRE-REGISTERED, ONE BREACHED:')
    P('    P4.1  yr1 in 1.05-1.11              MEASURED 1.0884                       HELD')
    P('    P4.2  yr4 within +/-1.0% of FULL    MEASURED 1.5660 = +2.29%              BREACHED')
    P('    P4.3  no new year-zero movers       MEASURED 1 mover, sum(v0) +0.017%     HELD')
    P('    P4.4  guard gains no failures       MEASURED 1 cell, same cell            HELD')
    P('    P4.5  margin stays positive/legal   MEASURED +5.16%                       HELD')
    P()
    P('  THE BREACH, AND IT WAS VISIBLE IN THE STEP-1 GRID BEFORE THE EMIT. P4.2 assumed the design was a')
    P('  year-1 fix. It is not: exposure weighting raises the par level at EVERY tenure, and at tenure 4')
    P('  it goes past the survivors-only level (fitted MID pick-7 par: built 77.36, XW 79.58, survivors')
    P('  78.10). So yr4 was always going to move more than the survivors-only revert\'s +1.3%. The')
    P('  pre-registration should have read the grid it already had. The number stands; the prediction')
    P('  does not, and it is a real cost: this design lifts the whole book, not just its young end.')
    P()
    P('  THE HONEST READ AT YEAR 1, stated because a reader will otherwise draw the wrong conclusion:')
    P('  at year 1 the design lands 1.0884 against the survivors-only revert\'s 1.0882 — INDISTINGUISHABLE,')
    P('  to 0.02%. That is Criterion A\'s "tenure 1 coincides" showing up at price level, and it means')
    P('  THE YEAR-1 NUMBER ALONE CANNOT TELL THE TWO APART. What separates them is (a) everything else on')
    P('  the row — yr2 1.3585 vs 1.3219, yr4 1.5660 vs 1.5515, yr5 1.5500 vs 1.5464 — and (b) the fact,')
    P('  proven in step 1, that one keeps every faded season in the sample and the other deletes them.')
    P('  The design is defensible on its construction, not on its year-1 number.')
    P()
    P('  WHAT IT DOES NOT SETTLE. It recovers 0.0910 of the 0.1265 main->FULL year-1 drop and leaves the')
    P('  book 3.2% below main at year 1. It moves year 4 by +2.29%, which no order asked for. NO OWNER')
    P('  RULING HAS BEEN MADE ON IT; the dial is DEFAULT OFF and nothing ships. See DESIGN_336_MEMO.md.')
    P()
    P('=' * 116)
    P('### ORDER 5 — THE STACKED ROW: TWO CANDIDATES THAT ARE LEGAL ALONE ARE ILLEGAL TOGETHER')
    P('=' * 116)
    P('  The owner asked for a stacked version. FULL + XW + V5 was emitted on the canonical instrument.')
    P()
    P('    row              yr1      yr4    apprec.   own disc.   margin   verdict')
    P('    ' + '-' * 74)
    for lab in ('FULL', 'XW', 'V5', 'STACK'):
        if lab not in T: continue
        r = rr(T[lab], GROUPS[0]); d = rate(lab, TYPICAL_DRAFT_AGE); ap = r[1]-1.0; m = d-ap
        P('    %-12s %8.4f %8.4f %9.2f%% %10.2f%% %8.2f%% %9s'
          % (lab, r[1], r[4], 100*ap, 100*d, 100*m, 'ARB' if m < 0 else 'legal'))
    P()
    P('  THE FINDING, and it is the reason a stacked row had to be emitted rather than inferred:')
    P('  XW is legal alone (+5.16%). V5 is legal alone (+4.66%). STACKED THEY ARE THE WORST ARBITRAGE ON')
    P('  THIS WHOLE MENU at -5.08% — deeper than V3 (-4.56%) and V4 (-2.82%). Two safe candidates make an')
    P('  unsafe book. Adding rows of this table together is not a valid operation and this row proves it.')
    P()
    P('  WHY IT IS WORSE THAN EITHER: the margin is a DIFFERENCE between what the book gains and what the')
    P('  schedule charges, and stacking moves BOTH terms the wrong way at once. The two lifts compound to')
    P('  +17.08% appreciation, while the stack carries V5\'s CHEAPER 12.00% young rate instead of the 14%')
    P('  XW is judged against. A bigger gain measured against a smaller charge.')
    P()
    P('  MARGIN CONVENTION, stated in the row because it decides the verdict: the stack is judged against')
    P('  V5\'S OWN young rate, 12.00% at draft age 18 — the TIGHTER frame, and the honest one, because the')
    P('  stack carries V5\'s discount schedule unchanged (XW re-weights the PAR SAMPLE and never touches')
    P('  the discount). Judged against 14% it would read -3.08%: still ARB, so the convention does not')
    P('  rescue it either way.')
    P()
    P('  PRE-REGISTERED (PREREG_ORDER5.md), TWO BREACHED:')
    P('    P5.1  stack above the larger component      MEASURED 1.1708 > 1.0884            HELD')
    P('    P5.2  SUB-additive, yr1 in 1.12-1.16        MEASURED 1.1708 — SUPER-ADDITIVE    BREACHED')
    P('    P5.4  margin -4%..+1%, expected NEGATIVE    MEASURED -5.08% — ARB, past the band BREACHED')
    P('    P5.5  yr4 in 1.585-1.615                    MEASURED 1.6027                     HELD')
    P('    P5.6  <=2 v0 movers, sum(v0) within 0.05%   MEASURED 1 mover, +0.023%           HELD')
    P('    P5.7  disagreement set non-empty            MEASURED 78 of 804 board players     HELD')
    P()
    P('  THE BREACH IS THE INTERESTING ONE. P5.2 predicted the stack would be SUB-additive — the second')
    P('  lift having less left to lift. It is SUPER-additive: the stack captures 103.8% of the naive sum')
    P('  of the two separate lifts (0.1734 against 0.1670). THE MECHANISM WAS PRE-REGISTERED IN P5.3 WITH')
    P('  ITS SIGN LEFT OPEN, and it is confirmed: XW raises the par levels, and par feeds the peak')
    P('  estimate and ITEM C\'s Q = sa/par, which is part of what V5\'s age-keyed discount is then applied')
    P('  to — so the second lever acts on a book the first has already raised. Measured per player on the')
    P('  live board: 193 of 804 rows move MORE than the sum of their two separate moves, 190 of them in')
    P('  the same direction. This is why a stack must be EMITTED and can never be read off two rows.')
    P()
    P('  SHARED-CODE ASSERTION, checked rather than assumed. The dials are read at disjoint sites')
    P('  (RL_336_XW only in par_build.py, RL_AGE_DISC_MODE only in rl_model.py). But par_build.py DID')
    P('  change between the V5 emit and this tip, so V5 was RE-EMITTED as V5B: its recs md5 is')
    P('  5c65a28f72acd0b3a83ec8dc841b0837, BYTE-IDENTICAL to the original V5 matrix. XW needed no re-emit')
    P('  (no engine or data file changed since its own emit commit). The stacked comparison is valid.')
    P()
    P('  Mraz across the four: FULL 1649 · XW 1707 · V5 1712 · STACK 1775 (3.043x/3.052x/3.164x his')
    P('  pick-35 ruler of 561) — every one inside the owner\'s 3.5-3.8x slack.')
    P()
    P('  PER-PLAYER BOARD FILES: board_compare_o5.csv (all 804 active rows) and board_compare_o5.txt')
    P('  (owner-readable). THEY ATTRIBUTE MOVERS AND DECIDE NOTHING — the live board is a cross-section')
    P('  and this table, on the cohort book, is the deciding instrument.')
    P()
    P('=' * 116)
    P('### THE IDENTITY GATE EVERY ROUND-3 NUMBER RIDES ON')
    P('=' * 116)
    P('  All five round-3 dials are DEFAULT OFF. With every one of them off, at the branch tip:')
    P('    MATRIX   the emitted per-entrant matrix (IDENT5) has recs byte-identical to per_entrant_FULL')
    P('             — recs md5 3eb4a686e36e4e299f1134e153c566bd on BOTH, 2645 records, 0 year-1 movers')
    P('             out of the 1197 teaching rows. The two FILES differ only in `meta` (engine_head md5,')
    P('             which moved because the dial and its comment block were added, and the emitter\'s')
    P('             own worktree path). That is a PRICE-LEVEL identity, not a file copy.')
    P('    BOARD    rl_export at 95dfbde and at the round-3 tip both build board md5')
    P('             846560dc1b206996005c7c9e9290207c — byte-identical, same env.')
    P('    DENOM    the year-zero surface is intact in every arm: 1 v0 mover out of 1197, sum(v0)')
    P('             within 0.02%. The ratio denominator is not carrying any of these moves.')
    P('  ORDER 4 re-proved both at its own tip: IDENT6 recs md5 3eb4a686e36e4e299f1134e153c566bd again,')
    P('  0 year-1 movers, 0 v0 movers; and with RL_336_XW=0 the fitted par surface, the KPD par surface')
    P('  and BASEPK_REG are identical to the pre-ORDER-4 reference to 1e-12 (the off path passes ws=None')
    P('  and never multiplies at all).')
    P('  ORDER 5 re-proved both again at its own tip: IDENT7 recs md5 3eb4a686e36e4e299f1134e153c566bd,')
    P('  0 year-1 movers, 0 v0 movers; and the FULL board rebuilt at the ORDER 5 tip is 846560dc1b2069')
    P('  96005c7c9e9290207c — the same board 95dfbde builds, before any of this act\'s seven dials existed.')
    P('  If either identity had failed, nothing on this table could be read. Both hold.')
    P()
    json.dump({lab: {g: rr(T[lab], g) for g in GROUPS} for lab, _, _ in have},
              open(os.path.join(HERE, 'MENU.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'MENU.txt'), 'w').write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
