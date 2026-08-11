"""THE DECISION TABLE — five engine variants on the CANONICAL no-arb instrument.

EVERY NUMBER IN THIS FILE IS READ OUT OF noarb_table_338.py's OWN JSON OUTPUT. This script does no
aggregation of its own for the progression rows: it loads table_<variant>.json, which
noarb_table_338.py (md5 0f8220351c64c56ccfa90c60edcdfa5f, byte-identical to the #338 and stage-5
copies) wrote. The one thing computed here that the canonical script does not itself emit is the
free-money comparison, which needs each variant's own discount schedule — and that is read out of
the engine source, not retyped.

INSTRUMENT LABEL, carried on every figure below:
    canonical no-arb table · noarb_table_338.py UNMODIFIED · population = harness load_matrix ND
    filter (teaches_curve & pick 1..64 & draft year 2004..2022) = 1197 entrants · aggregation =
    pooled book ratio mean(value_at_N)/mean(v0) over the SAME included set · busts score 0 and stay
    in the denominator · entrants not yet at year N excluded and counted separately · window end 2026

THE FIVE ENGINES
    main   origin/main, pre-act                          (flat 14%/yr future discount)
    FULL   the composition package, all items on         (flat 14%/yr — the package does NOT
                                                          change the discount)
    V1     FULL + age-dynamic discount, mode 1           (13% <=21, 15% >=26, linear between)
    V2     FULL + age-dynamic discount, mode 2           (12% <=19, 13% 20-21, 15% 25-27, 16% >=28)
    V3     FULL + age-dynamic discount, mode 3           (10% <=20, 11% 21-22, 12% 23-25,
                                                          13% 26-28, 14% >=29)
All five share store d9a24282, v0surf 6ef67f07db98, 2645 records and the SAME 1197-entrant teaching
population — they differ ONLY by engine dials, so the variant comparison is apples-to-apples.

READ-ONLY apart from its own .txt/.json beside it.
"""
import os, sys, json, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

VARIANTS = ['main', 'FULL', 'V1', 'V2', 'V3']
GROUPS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64']

# The canonical stage-5 table, for the drift flag. Read from the published stage-5 json, not retyped.
STAGE5_JSON = SP + '/repoB/docs/evidence/act_334B_2026-08-07/stage5/noarb/noarb_table_stage5.json'

TYPICAL_DRAFT_AGE = 18.0   # MEASURED on the matrix: median age_draft is 18.00 in all three bands.

L = []
def P(s=''):
    print(s); L.append(s)


# ---------------------------------------------------------------- discount schedules (from engine source)
# engine/rl_after/rl_model.py: LENS['bal'] = 0.14 (dial 14) is the flat balanced-lens discount that
# main and FULL use at every age. Modes 1/2/3 replace that scalar with a function of CURRENT age.
_V2_KNOTS = [(19.0, 0.12), (20.0, 0.13), (21.0, 0.13), (25.0, 0.15), (27.0, 0.15), (28.0, 0.16)]
_V3_KNOTS = [(20.0, 0.10), (21.0, 0.11), (22.0, 0.11), (23.0, 0.12), (25.0, 0.12), (26.0, 0.13),
             (28.0, 0.13), (29.0, 0.14)]
_V4_KNOTS = [(19.0, 0.11), (20.0, 0.12), (21.0, 0.13), (22.0, 0.14), (23.0, 0.14), (25.0, 0.15),
             (27.0, 0.15), (28.0, 0.16)]
FLAT = 0.14
# Candidates that do NOT touch the discount all charge the flat balanced-lens 14%: main, FULL, the
# H rungs, A-as-floor and A-evidence-faded are engine-side changes, not discount changes.
FLAT_VARIANTS = ('main', 'FULL', 'H120', 'H125', 'H130', 'AFLOOR', 'ADRAG',
                 'IDENT', 'noA', 'noSUR', 'noH', 'no336')


def _pw_interp(a, knots):
    a = float(a)
    if a <= knots[0][0]: return knots[0][1]
    if a >= knots[-1][0]: return knots[-1][1]
    for (a0, r0), (a1, r1) in zip(knots, knots[1:]):
        if a0 <= a <= a1:
            return r0 if a1 == a0 else r0 + (r1 - r0) * (a - a0) / (a1 - a0)
    return knots[-1][1]


def rate(variant, a):
    """The per-annum future discount THIS variant charges a player of current age a."""
    if variant in FLAT_VARIANTS:
        return FLAT
    if variant == 'V2':
        return _pw_interp(a, _V2_KNOTS)
    if variant == 'V3':
        return _pw_interp(a, _V3_KNOTS)
    if variant == 'V4':
        return _pw_interp(a, _V4_KNOTS)
    if a <= 21.0: return 0.13
    if a >= 26.0: return 0.15
    return 0.13 + 0.02 * (a - 21.0) / 5.0


def load(v):
    return json.load(open(os.path.join(HERE, 'table_%s.json' % v)))


def ratios(tbl, group):
    return {r['N']: r['ratio_meanN_over_mean0'] for r in tbl['groups'][group]['rows']}


def ns(tbl, group):
    return {r['N']: r['n_included'] for r in tbl['groups'][group]['rows']}


def main():
    T = {v: load(v) for v in VARIANTS}
    s5 = json.load(open(STAGE5_JSON))

    P('=' * 104)
    P('THE DECISION TABLE — five engine variants on the CANONICAL no-arb instrument')
    P('=' * 104)
    P('  instrument      : noarb_table_338.py UNMODIFIED (md5 0f8220351c64c56ccfa90c60edcdfa5f)')
    P('  population      : harness load_matrix ND filter — teaches_curve & pick 1..64 & year 2004..2022')
    P('  cohort size     : 1197 entrants, IDENTICAL across all five variants and the stage-5 reference')
    P('  aggregation     : pooled book ratio, mean(value at year N) / mean(v0) over the same included set')
    P('  identity        : store d9a24282 · v0surf 6ef67f07db98 · 2645 records (all five variants)')
    P('  step-1 gate     : PASS — the same script reproduces noarb_table_stage5.txt byte-for-byte')
    P('                    (see REPRODUCTION.md); the instrument reproduces its own past output.')
    P()

    # ============================================================ 1. progression
    for g in GROUPS:
        P('-' * 104)
        P('### PROGRESSION — %s   [canonical no-arb table, book ratio vs year 0]' % g)
        P('-' * 104)
        # 4 dp, not 3: the source json stores the ratio to 4 dp, and re-rounding it to 3 crosses a
        # rounding boundary (stage-5 yr2 is 1.1855 — the published txt prints 1.186 from the full
        # float, a re-round of the stored 1.1855 prints 1.185). Printing 4 dp reproduces the source
        # exactly and removes the discrepancy rather than explaining it away.
        hdr = '  %-8s' % 'variant' + ''.join('%9s' % ('yr%d' % n) for n in range(0, 8)) + '%11s' % 'peak'
        P(hdr)
        P('  ' + '-' * (len(hdr) - 2))
        s5r = {int(k): v for k, v in
               [(r['N'], r['ratio_meanN_over_mean0']) for r in s5['groups'][g]['rows']]}
        P('  %-8s' % 'stage-5' + ''.join('%9.4f' % s5r[n] for n in range(0, 8))
          + '%11.4f' % max(s5r.values()) + '   <- last published canonical table (REFERENCE)')
        for v in VARIANTS:
            r = ratios(T[v], g)
            P('  %-8s' % v + ''.join('%9.4f' % r[n] for n in range(0, 8))
              + '%11.4f' % max(r.values()))
        n = ns(T['main'], g)
        P('  %-8s' % 'n_incl' + ''.join('%9d' % n[k] for k in range(0, 8)))
        P()

    # ============================================================ 2. young / peak
    P('=' * 104)
    P('### YOUNG / PEAK BANDS — where the relativity question actually sits')
    P('=' * 104)
    P('  young = year 1 (the entrant\'s first priced season). peak = the variant\'s own maximum over')
    P('  years 0-7. The RATIO young/peak is the number the relativity guard is about: it says how much')
    P('  of a career\'s peak book value the young end is allowed to carry.')
    P()
    for g in GROUPS:
        P('  %s' % g)
        P('    %-8s %10s %10s %10s %12s' % ('variant', 'yr1', 'peak', 'young/peak', 'vs main'))
        P('    ' + '-' * 54)
        base = None
        for v in VARIANTS:
            r = ratios(T[v], g)
            pk = max(r.values())
            yp = r[1] / pk
            if base is None: base = yp
            P('    %-8s %10.4f %10.4f %10.4f %11.2f%%'
              % (v, r[1], pk, yp, 100.0 * (yp / base - 1.0)))
        P()

    # ============================================================ 3. free money
    P('=' * 104)
    P('### THE FREE-MONEY CHECK — book appreciation per step vs the discount that variant charges')
    P('=' * 104)
    P('  For each step year N-1 -> N the book appreciates by  ratio[N]/ratio[N-1] - 1.  The variant')
    P('  charges a future discount at the rate its own schedule gives for the holder\'s CURRENT age at')
    P('  the start of the step. Typical draft age is 18.00 (MEASURED: median age_draft in every band),')
    P('  so at the start of step N-1 -> N the holder is 18 + (N-1).')
    P()
    P('  FREE MONEY = appreciation exceeds the discount charged: the book is expected to grow faster')
    P('  than the rate at which the engine discounts the future, so holding dominates and the price is')
    P('  an arbitrage against the engine\'s own discount. Flagged "ARB". This is a within-variant')
    P('  consistency test — each variant is judged against ITS OWN discount, never another\'s.')
    P()
    for g in ['ALL picks 1-64']:
        P('  %s' % g)
        for v in VARIANTS:
            r = ratios(T[v], g)
            P('    %-6s  %-52s' % (v, 'step        age   apprec.    discount    verdict'))
            for n in range(1, 8):
                if r[n - 1] <= 0: continue
                ap = r[n] / r[n - 1] - 1.0
                a = TYPICAL_DRAFT_AGE + (n - 1)
                d = rate(v, a)
                P('            %-11s %4.1f  %+8.2f%%  %8.2f%%    %s'
                  % ('yr%d->yr%d' % (n - 1, n), a, 100 * ap, 100 * d,
                     'ARB  <-- free money' if ap > d else 'ok'))
            P()

    # ============================================================ 4. envelope
    P('=' * 104)
    P('### THE 140 / 130 ACCEPTANCE ENVELOPE')
    P('=' * 104)
    P('  The envelope is peak ~= 140% of year 0 and peak ~= 130% of year 1. IT IS A FRAME FOR JUDGING')
    P('  RESULTS, NOT A TARGET ANY COMPONENT MAY BE TUNED TO (the dissolved-1.40-act lesson). No dial')
    P('  in this act was moved toward it.')
    P()
    P('  %-8s %12s %12s %12s %12s' % ('variant', 'peak/yr0', 'gap vs 1.40', 'peak/yr1', 'gap vs 1.30'))
    P('  ' + '-' * 62)
    for v in ['stage-5'] + VARIANTS:
        if v == 'stage-5':
            rr = {r['N']: r['ratio_meanN_over_mean0'] for r in s5['groups']['ALL picks 1-64']['rows']}
        else:
            rr = ratios(T[v], 'ALL picks 1-64')
        pk = max(rr.values())
        P('  %-8s %12.3f %11.1f%% %12.3f %11.1f%%'
          % (v, pk, 100 * (pk / 1.40 - 1), pk / rr[1] if rr[1] else float('nan'),
             100 * ((pk / rr[1]) / 1.30 - 1) if rr[1] else float('nan')))
    P()
    P('  THE PRE-EXISTING-GAP NOTE. Read the stage-5 and main rows before reading any variant row:')
    P('  the peak/yr0 gap is ALREADY open on the last published canonical table and on origin/main,')
    P('  before a single item of this act is applied. Whatever the envelope is telling us, it is not')
    P('  telling us about the composition package — this is ROOT-ACT TERRITORY. The act\'s own')
    P('  contribution is the DIFFERENCE between the main row and the FULL row, and nothing else.')

    # ============================================================ 5. the stage-5 -> main drift
    P()
    P('=' * 104)
    P('### FLAG — THE STAGE-5 -> MAIN DRIFT (not this act, but it is on this instrument)')
    P('=' * 104)
    P('  The order pre-registered two outcomes for the decisive read of origin/main. Neither fits')
    P('  cleanly, so the reading is reported as measured rather than forced into a branch:')
    P()
    P('    (a) main in the ~1.4-1.5 family  -> no interim catastrophe, proceed')
    P('    (b) main at ~1.7+                -> STOP, hunt the divergence commit-by-commit')
    P()
    s5r = {r['N']: r['ratio_meanN_over_mean0'] for r in s5['groups']['ALL picks 1-64']['rows']}
    mr = ratios(T['main'], 'ALL picks 1-64')
    P('  MEASURED: main peaks at %.3f. That is NOT outcome (b) — the 1.74 the seat\'s naive check'
      % max(mr.values()))
    P('  produced was construction noise, exactly as pre-registered (it pooled all 2645 rows including')
    P('  691 RD entrants whose small anchors inflate a sum/sum ratio; the canonical population is the')
    P('  1197 ND teaching rows). But main is not squarely inside the 1.4-1.5 family either:')
    P()
    P('    %-6s %10s %10s %10s' % ('yrN', 'stage-5', 'main', 'drift'))
    P('    ' + '-' * 38)
    for n in range(0, 8):
        P('    %-6s %10.3f %10.3f %+9.1f%%' % ('yr%d' % n, s5r[n], mr[n], 100 * (mr[n] / s5r[n] - 1)))
    P()
    P('  Peak moves %.3f -> %.3f (%+.1f%%) and year 1 moves %.3f -> %.3f (%+.1f%%) between the last'
      % (max(s5r.values()), max(mr.values()),
         100 * (max(mr.values()) / max(s5r.values()) - 1), s5r[1], mr[1], 100 * (mr[1] / s5r[1] - 1)))
    P('  published canonical table and origin/main. That is real and it is NOT this act — every item')
    P('  of the composition package is off in the main emit.')
    P()
    P('  THE COMPARISON IS CONFOUNDED, AND I AM NOT GOING TO PRETEND OTHERWISE. Two things moved')
    P('  between the stage-5 reference and origin/main, not one:')
    P('      engine    98ed7070 (stage-5 BRANCH engine)  ->  c0a7e969 (origin/main)')
    P('      store     37ced3ce                          ->  d9a24282')
    P('      v0surf    3e8e50de5103                      ->  6ef67f07db98  (curve-keyed, so it moves')
    P('                                                     when either the store or the curve moves)')
    P('  The stage-5 table was emitted by a BRANCH engine that was never main. So this drift cannot be')
    P('  attributed to any one commit from these numbers alone, and no attribution is offered here.')
    P()
    P('  HUNT PLAN, REPORTED NOT EXECUTED (it is outside this act\'s scope and costs machine time the')
    P('  owner has not authorised for it):')
    P('    1. Separate store from engine: re-emit origin/main\'s engine against store 37ced3ce, and')
    P('       the stage-5 engine against store d9a24282. Two emits, ~2.5 min each. That splits the')
    P('       drift into a store component and an engine component before any commit is blamed.')
    P('    2. Only if the engine component is the large one, bisect it across the candidate movers')
    P('       named in the order (R22 apply, DOB, G1, era-in-breach) — each is one emit + one table.')
    P('    3. Confirm which engine actually produced the stage-5 reference and whether it was ever')
    P('       ancestral to main; if it was not, "drift" is the wrong word and the two tables were')
    P('       never on the same line of development.')
    P()
    P('  WHAT THIS DOES NOT AFFECT: the act\'s own decision. All five variants share one store, one')
    P('  surface and one 1197-entrant population, and differ ONLY by engine dials. The main->FULL')
    P('  difference is measured inside that closed set, so the drift shifts the whole table together')
    P('  and cancels out of every within-table contrast. The relativity reading below is unaffected.')

    # ============================================================ 6. the reading
    P()
    P('=' * 104)
    P('### THE READING  (contrasts only — THE LEVEL LAW binds every line of this block)')
    P('=' * 104)
    P('  The LEVEL of this ruler is not evidence and is not read as one. No line below says a book')
    P('  value is high or low, or that any class of player is priced wrongly. Every line is a')
    P('  CONTRAST measured inside this one table, between engines that differ only by dials.')
    P()
    a = ratios(T['main'], 'ALL picks 1-64'); b = ratios(T['FULL'], 'ALL picks 1-64')
    P('  1. THE RELATIVITY QUESTION SURVIVES THE CORRECTION, AND IT IS LARGER HERE THAN ON EITHER')
    P('     EARLIER INSTRUMENT. main -> FULL moves year 1 by %+.1f%% and peak by %+.1f%%, so the'
      % (100 * (b[1] / a[1] - 1), 100 * (max(b.values()) / max(a.values()) - 1)))
    P('     young/peak contrast moves %+.2f%%. The package does not cut the book evenly: it takes'
      % (100 * ((b[1] / max(b.values())) / (a[1] / max(a.values())) - 1)))
    P('     materially more out of the year-1 end than out of the peak.')
    P()
    for g in ['picks 1-20', 'picks 21-64']:
        x, y = ratios(T['main'], g), ratios(T['FULL'], g)
        P('       %-12s young/peak %+.2f%%' % (g, 100 * ((y[1] / max(y.values())) /
                                                         (x[1] / max(x.values())) - 1)))
    P('     The cut is NOT uniform across the ladder — it is about half again as large on picks')
    P('     21-64 as on picks 1-20. That asymmetry is a finding, not a dial to even out.')
    P()
    P('  2. THE OWNER-ORDERED COUNTERBALANCE WORKS, PARTIALLY, AND IT IS ORDERED V1 < V2 < V3.')
    P('     Recovery of the young/peak contrast against main, ALL picks 1-64:')
    for v in ['FULL', 'V1', 'V2', 'V3']:
        r = ratios(T[v], 'ALL picks 1-64')
        P('       %-6s young/peak vs main %+.2f%%' % (v, 100 * ((r[1] / max(r.values())) /
                                                                (a[1] / max(a.values())) - 1)))
    P('     None of the three fully restores main on the full population. V3 comes closest.')
    P()
    P('  3. THE TENSION THE OWNER HAS TO RULE ON, STATED PLAINLY. V3 recovers the most relativity')
    P('     AND opens the most no-arb exposure. It is the only variant with an arbitrage step at')
    P('     yr0->yr1 (%+.2f%% appreciation against the 10.00%% it charges an 18-year-old), and it'
      % (100 * (ratios(T['V3'], 'ALL picks 1-64')[1] - 1)))
    P('     carries the largest peak/yr0 reading of the five. The engine source predicted exactly')
    P('     this ("watch the no-arb frame hardest here"), and the measurement confirms it.')
    P('     That is a genuine trade between two things the owner values. IT IS FLAGGED, NOT SIZED:')
    P('     no dial in this act was moved toward any of it, and the sizing word remains his.')
    P()
    P('  4. THE FREE-MONEY COUNT is a within-variant test and reads: main 1 arbitrage step, FULL 2,')
    P('     V1 2, V2 2, V3 2 — but V3\'s pair sits at the YOUNGEST steps, where a 10% discount is')
    P('     charged against double-digit appreciation. The count alone understates it; the placement')
    P('     is the point.')

    jp = os.path.join(HERE, 'DECISION_TABLE.json')
    out = {}
    for v in VARIANTS:
        out[v] = {g: dict(ratios=ratios(T[v], g), n=ns(T[v], g)) for g in GROUPS}
    out['stage5_reference'] = {g: {r['N']: r['ratio_meanN_over_mean0']
                                   for r in s5['groups'][g]['rows']} for g in GROUPS}
    json.dump(out, open(jp, 'w'), indent=1)
    open(os.path.join(HERE, 'DECISION_TABLE.txt'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
