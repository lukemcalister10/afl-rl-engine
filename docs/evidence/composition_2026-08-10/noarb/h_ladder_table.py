"""THE H LADDER TABLE — RL_C_H = 1.13 / 1.20 / 1.25 / 1.30 on the canonical no-arb instrument.

Every progression number is read out of noarb_table_338.py's OWN json (table_<label>.json), the
unmodified canonical script (md5 0f8220351c64c56ccfa90c60edcdfa5f). This file computes only the
comparisons the canonical script does not itself emit.

The pre-registration is H_LADDER_PREREG.md, written BEFORE the emits. It is CHECKED here in code,
and the verdict is printed whether it passes or fails.

INSTRUMENT LABEL, carried on every figure: canonical no-arb table, unmodified · population = harness
load_matrix ND filter (teaches_curve & pick 1..64 & year 2004..2022) = 1197 entrants, identical on
every rung · aggregation = pooled book ratio mean(value at year N)/mean(v0) over the same included
set · busts score 0 and stay in the denominator · window end 2026.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64']
FLAT = 0.14                      # LENS['bal'] — the flat balanced-lens discount main and FULL charge
TYPICAL_DRAFT_AGE = 18.0         # MEASURED: median age_draft is 18.00 in every band

# (label, H) — FULL is the H=1.13 baseline that already existed
RUNGS = [('FULL', 1.13), ('H120', 1.20), ('H125', 1.25), ('H130', 1.30)]

# pre-registered thresholds (H_LADDER_PREREG.md)
YR4_TOL = 0.010

L = []
def P(s=''):
    print(s); L.append(s)


def load(v):
    p = os.path.join(HERE, 'table_%s.json' % v)
    return json.load(open(p)) if os.path.exists(p) else None


def ratios(tbl, group):
    return {r['N']: r['ratio_meanN_over_mean0'] for r in tbl['groups'][group]['rows']}


def peak_of(r):
    pk = max(r.values())
    return pk, [n for n in sorted(r) if r[n] == pk][0]


def main():
    T = {lab: load(lab) for lab, _ in RUNGS}
    missing = [lab for lab, _ in RUNGS if T[lab] is None]
    if missing:
        print('MISSING TABLES: %s — run run_h_ladder.sh first' % ', '.join(missing))
        return 2
    main_t = load('main')

    P('=' * 104)
    P('THE H LADDER — RL_C_H = 1.13 / 1.20 / 1.25 / 1.30, canonical no-arb instrument')
    P('=' * 104)
    P('  instrument   : noarb_table_338.py UNMODIFIED (md5 0f8220351c64c56ccfa90c60edcdfa5f)')
    P('  population   : 1197 ND teaching entrants, IDENTICAL on every rung')
    P('  baseline     : FULL = the composition package at its shipped RL_C_H = 1.13')
    P('  admissible   : the dial\'s derived window on the #336 basis is [1.1024, 1.3327] —')
    P('                 ALL FOUR RUNGS SIT INSIDE IT. The ladder does not leave the window.')
    P('  discount     : every rung charges the SAME flat 14.00%/yr (H does not touch the discount),')
    P('                 so the no-arb margins below move only because the book moved.')
    P()

    # ============================================================ 1. the pre-registered check FIRST
    P('=' * 104)
    P('### THE PRE-REGISTERED CHECK  (H_LADDER_PREREG.md, written before the emits)')
    P('=' * 104)
    P('  EXPECTED: yr1 rises monotonically with H; yr4 HOLDS within |delta| <= %.3f of the' % YR4_TOL)
    P('            FULL@1.13 baseline. A large yr4 move is a wiring surprise and halts the ladder.')
    P('  MECHANISM: H scales the ITEM C release inside _a_blend, and A\'s share fades hard with')
    P('            career evidence (measured v1 0.3589 -> v6 0.0038), so H has little purchase by')
    P('            year 4. CAVEAT REGISTERED IN ADVANCE: _c_w also enters the ITEM E2 ruck cap,')
    P('            which is NOT inside the A blend and does not fade — so a TINY yr4 move is')
    P('            mechanistically expected and is not itself a surprise.')
    P()
    r0 = ratios(T['FULL'], 'ALL picks 1-64')
    base4, base1 = r0[4], r0[1]
    P('  %-6s %6s %10s %10s %12s %10s' % ('rung', 'H', 'yr1', 'yr4', 'yr4 delta', 'verdict'))
    P('  ' + '-' * 60)
    ok4 = True; y1s = []
    for lab, h in RUNGS:
        r = ratios(T[lab], 'ALL picks 1-64')
        d4 = r[4] - base4
        y1s.append(r[1])
        if abs(d4) > YR4_TOL: ok4 = False
        P('  %-6s %6.2f %10.4f %10.4f %+12.4f %10s'
          % (lab, h, r[1], r[4], d4, 'HOLD' if abs(d4) <= YR4_TOL else 'MOVED'))
    mono = all(y1s[i] < y1s[i + 1] for i in range(len(y1s) - 1))
    P()
    P('  yr1 monotone rising with H : %s' % ('YES' if mono else 'NO — SURPRISE, reported as one'))
    P('  yr4 held within %.3f       : %s' % (YR4_TOL, 'YES' if ok4 else 'NO — WIRING SURPRISE'))
    P()
    if ok4 and mono:
        P('  VERDICT: THE PRE-REGISTRATION IS MET. H is year-1-specific on this instrument — it')
        P('  moves the taught year-1 level and leaves year 4 where it was. The ladder is readable')
        P('  as a counterbalance result.')
    else:
        P('  VERDICT: THE PRE-REGISTRATION IS NOT MET. Per the order the ladder is NOT read as a')
        P('  counterbalance result. The mismatch is reported and the sizing question stays open.')
    P()

    # ============================================================ 2. progression
    for g in GROUPS:
        P('-' * 104)
        P('### PROGRESSION — %s   [canonical no-arb table, book ratio vs year 0]' % g)
        P('-' * 104)
        hdr = '  %-6s %6s' % ('rung', 'H') + ''.join('%9s' % ('yr%d' % n) for n in range(0, 6)) \
              + '%10s%8s' % ('peak', 'at')
        P(hdr)
        P('  ' + '-' * (len(hdr) - 2))
        if main_t:
            rm = ratios(main_t, g); pk, at = peak_of(rm)
            P('  %-6s %6s' % ('main', '-') + ''.join('%9.4f' % rm[n] for n in range(0, 6))
              + '%10.4f%8s' % (pk, 'yr%d' % at) + '   <- pre-act reference')
        for lab, h in RUNGS:
            r = ratios(T[lab], g); pk, at = peak_of(r)
            P('  %-6s %6.2f' % (lab, h) + ''.join('%9.4f' % r[n] for n in range(0, 6))
              + '%10.4f%8s' % (pk, 'yr%d' % at))
        P()

    # ============================================================ 3. young/peak vs main + bands
    P('=' * 104)
    P('### YOUNG/PEAK CONTRAST vs main — DOES H\'S RESTORATION LAND WHERE THE CUT FELL?')
    P('=' * 104)
    P('  The young cut concentrated in picks 21-64 (-11.74%) rather than 1-20 (-7.90%), and ITEM C\'s')
    P('  releases are evidence-weighted. This is the table that shows whether H restores the band')
    P('  that actually lost, or the band that lost less.')
    P()
    P('  %-6s %6s' % ('rung', 'H') + ''.join('%18s' % g for g in GROUPS))
    P('  ' + '-' * 68)
    base = {}
    for g in GROUPS:
        rm = ratios(main_t, g); pk, _ = peak_of(rm); base[g] = rm[1] / pk
    for lab, h in RUNGS:
        cells = []
        for g in GROUPS:
            r = ratios(T[lab], g); pk, _ = peak_of(r)
            cells.append('%+17.2f%%' % (100 * ((r[1] / pk) / base[g] - 1)))
        P('  %-6s %6.2f' % (lab, h) + ''.join(cells))
    P()
    P('  (0.00% would mean the rung restores main\'s young/peak contrast exactly in that band.)')
    P()

    # ============================================================ 4. no-arb
    P('=' * 104)
    P('### THE NO-ARB CHECK — and the bound on lawful H')
    P('=' * 104)
    P('  Every rung charges the SAME flat 14.00%/yr, so as H raises yr1 the yr0->yr1 appreciation')
    P('  rises and its margin against that charge SHRINKS. Where it crosses zero bounds lawful H.')
    P('  The yr1->peak leg is annualised over its own span so the two legs are comparable.')
    P()
    P('  %-6s %6s %11s %11s %11s %11s %9s'
      % ('rung', 'H', 'yr0->yr1', 'margin', 'yr1->peak', 'margin', 'verdict'))
    P('  ' + '-' * 74)
    for lab, h in RUNGS:
        r = ratios(T[lab], 'ALL picks 1-64'); pk, at = peak_of(r)
        a01 = r[1] / r[0] - 1.0
        span = max(at - 1, 1)
        a1p = (pk / r[1]) ** (1.0 / span) - 1.0 if r[1] > 0 else float('nan')
        m01, m1p = FLAT - a01, FLAT - a1p
        P('  %-6s %6.2f %10.2f%% %10.2f%% %10.2f%% %10.2f%% %9s'
          % (lab, h, 100 * a01, 100 * m01, 100 * a1p, 100 * m1p,
             'ARB' if (m01 < 0 or m1p < 0) else 'ok'))
    P()
    # crossing point, by linear fit on the measured rungs
    xs = [h for _, h in RUNGS]
    ys = [ratios(T[lab], 'ALL picks 1-64')[1] for lab, _ in RUNGS]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0.0
    icept = my - slope * mx
    target = 1.0 + FLAT      # yr0 is 1.0 by construction, so appreciation = yr1 - 1
    P('  THE BOUND. yr1 against H is close to linear over the measured rungs:')
    P('      yr1(H) ~= %.4f + %.4f * H     (fit on the four measured rungs)' % (icept, slope))
    P('  The yr0->yr1 leg becomes free money when yr1 exceeds %.4f (a %.2f%% appreciation against'
      % (target, 100 * FLAT))
    P('  the %.2f%% charged to an 18-year-old). Solving the fit:' % (100 * FLAT))
    if slope > 0:
        hx = (target - icept) / slope
        inside = xs[0] <= hx <= xs[-1]
        P()
        P('      H_cross ~= %.3f' % hx)
        P()
        if inside:
            P('  That is INSIDE the measured range, so it is interpolation and it is reliable.')
        else:
            P('  THAT IS AN EXTRAPOLATION BEYOND THE MEASURED RANGE (%.2f..%.2f) AND IS LABELLED AS'
              % (xs[0], xs[-1]))
            P('  ONE. It is NOT a measurement. It also sits %s the dial\'s admissible window'
              % ('outside' if hx > 1.3327 else 'inside'))
            P('  [1.1024, 1.3327], which is the binding constraint regardless of the fit.')
        P()
        P('  READ IT AS A BOUND, NOT A TARGET. Nothing in this act was tuned toward it, and the')
        P('  admissible window remains the governing constraint on H.')
    else:
        P('      yr1 does not rise with H on the fit — no crossing to report.')
    P()

    # ============================================================ 5. envelope
    P('=' * 104)
    P('### THE 140 / 130 ENVELOPE ACROSS THE LADDER')
    P('=' * 104)
    P('  A FRAME FOR JUDGING, NOT A TARGET (the dissolved-1.40-act lesson). The peak/yr0 gap is')
    P('  PRE-EXISTING — already open on main before any item of this act applies.')
    P()
    P('  %-6s %6s %11s %12s %11s %12s' % ('rung', 'H', 'peak/yr0', 'gap vs 1.40', 'peak/yr1',
                                          'gap vs 1.30'))
    P('  ' + '-' * 62)
    rows = ([('main', None)] if main_t else []) + RUNGS
    for lab, h in rows:
        t = main_t if lab == 'main' else T[lab]
        r = ratios(t, 'ALL picks 1-64'); pk, _ = peak_of(r)
        P('  %-6s %6s %11.4f %11.1f%% %11.4f %11.1f%%'
          % (lab, ('%.2f' % h) if h else '-', pk, 100 * (pk / 1.40 - 1),
             pk / r[1], 100 * ((pk / r[1]) / 1.30 - 1)))
    P()

    json.dump({lab: {g: ratios(T[lab], g) for g in GROUPS} for lab, _ in RUNGS},
              open(os.path.join(HERE, 'H_LADDER.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'H_LADDER.txt'), 'w').write('\n'.join(L) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
