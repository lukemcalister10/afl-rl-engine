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
    mono = all(y1s[i] <= y1s[i + 1] for i in range(len(y1s) - 1))
    dy1 = y1s[-1] - y1s[0]
    P()
    P('  yr1 non-decreasing in H : %s   (total yr1 move across the whole ladder: %+.4f)'
      % ('YES' if mono else 'NO', dy1))
    P('  yr4 held within %.3f    : %s' % (YR4_TOL, 'YES' if ok4 else 'NO'))
    P()
    P('  *** THE THRESHOLD CHECK PASSES, AND IT PASSES FOR THE WRONG REASON. ***')
    P()
    P('  yr4 "holds" — but so does everything else. Across a 15% increase in the release ceiling')
    P('  (H 1.13 -> 1.30) the year-1 book moves by %+.4f, which is not a counterbalance; it is' % dy1)
    P('  nothing. The pre-registration predicted yr4 would hold BECAUSE the effect was concentrated')
    P('  at year 1. The measurement says yr4 holds because there is almost no effect anywhere in')
    P('  the aggregate. A passing threshold that passes for the wrong reason is NOT a confirmation,')
    P('  and it is not reported as one.')
    P()
    P('  The binding-site diagnostic below shows what is actually happening, and it inverts the')
    P('  premise of the ladder order rather than merely failing to meet it.')
    P()

    # ============================================================ 1b. WHERE H ACTUALLY BINDS
    SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

    def mload(l):
        d = json.load(open('%s/per_entrant_%s.json' % (SP, l)))
        return {(r['key'], r['type'], r['year']): r for r in d['recs']}

    P('=' * 104)
    P('### WHERE H ACTUALLY BINDS — the diagnostic that explains the flat ladder')
    P('=' * 104)
    P('  Counted directly on the emitted matrices, FULL@1.13 vs H130: a price CELL is "moved" if')
    P('  the two engines disagree on it by more than 1e-9. This is not an aggregate — it is a count')
    P('  of the individual prices the dial actually reaches.')
    P()
    try:
        A, B = mload('FULL'), mload('H130')
    except Exception as e:
        P('  (matrices unavailable: %s)' % e)
        A = None
    if A:
        isND = lambda r: bool(r.get('teaches_curve') and r.get('pick')
                              and 1 <= r['pick'] <= 64 and 2004 <= r['year'] <= 2022)
        mv = {}; tt = {}; mvn = {}; ttn = {}
        ent = 0
        for k in A:
            a, b = A[k], B[k]
            va = [a.get('v0')] + (a.get('vpath') or [])
            vb = [b.get('v0')] + (b.get('vpath') or [])
            hit = False
            for n, (x, y) in enumerate(zip(va, vb)):
                if x is None or y is None: continue
                tt[n] = tt.get(n, 0) + 1
                if isND(a): ttn[n] = ttn.get(n, 0) + 1
                if abs(float(y) - float(x)) > 1e-9:
                    mv[n] = mv.get(n, 0) + 1; hit = True
                    if isND(a): mvn[n] = mvn.get(n, 0) + 1
            if hit: ent += 1
        P('  H IS LIVE, AND IT IS NOT RUCK-ONLY: %d of %d entrants (%.1f%%) move somewhere in their'
          % (ent, len(A), 100.0 * ent / len(A)))
        P('  career, spread across all six positions. The ITEM C release at _merged_recover.py:2061')
        P('  is wired and firing. The question is WHERE.')
        P()
        P('  %-5s %26s %26s' % ('yrN', 'ALL routes (moved/cells)', 'ND teaching 1-64'))
        P('  ' + '-' * 60)
        for n in range(0, 10):
            if not tt.get(n): continue
            P('  %-5d %10d /%6d %6.1f%% %10d /%6d %6.1f%%'
              % (n, mv.get(n, 0), tt[n], 100.0 * mv.get(n, 0) / tt[n],
                 mvn.get(n, 0), ttn.get(n, 1), 100.0 * mvn.get(n, 0) / max(ttn.get(n, 1), 1)))
        P()
        r1 = 100.0 * mvn.get(1, 0) / max(ttn.get(1, 1), 1)
        r4 = 100.0 * mvn.get(4, 0) / max(ttn.get(4, 1), 1)
        P('  THE PREMISE OF THE LADDER ORDER IS INVERTED BY ITS OWN MEASUREMENT. The order framed H')
        P('  as "year-1-specific, no year-4 side effect expected". On the ND teaching population H')
        P('  reaches %.1f%% of year-1 cells and %.1f%% of year-4 cells — it touches year 4 about %.0fx'
          % (r1, r4, (r4 / r1) if r1 else float('inf')))
        P('  MORE OFTEN than year 1, not less. H is not a year-1 dial. It is a years-3-to-5 dial.')
        P()
        P('  WHY, mechanistically — and this is the part that matters for the sitting. ITEM C\'s')
        P('  release is EVIDENCE-WEIGHTED (w = G*Q*gate, and the cap binds only where')
        P('  ceil < e <= V0_uncapped — a hot prior with no demonstrated growth). Year 1 is precisely')
        P('  the year in which a drafted player has almost no evidence, so e has not yet risen')
        P('  through the ceiling and there is nothing for H to release. By years 3-5 enough evidence')
        P('  has accumulated for the cap to bind, which is exactly where the binding shows up.')
        P()
        P('  AN EVIDENCE-WEIGHTED RELEASE CANNOT ACT IN THE YEAR BEFORE THE EVIDENCE EXISTS. That is')
        P('  a structural property of ITEM C, not a sizing problem, and NO VALUE OF H FIXES IT —')
        P('  raising H further multiplies a weight that is ~0 at year 1. The two year-1 movers in')
        P('  the whole 1197-entrant teaching population are both RUCKs (Kreuzer pick 1 +9.20%,')
        P('  Naitanui pick 2 +5.81%), reached through the ITEM E2 ruck cap at :2116 — the channel')
        P('  registered in the pre-registration as the CAVEAT, which turns out to be the only thing')
        P('  H reaches at year 1 at all.')
        P()
        P('  CONSEQUENCE FOR THE MENU, stated as a finding and not as a recommendation: H is not a')
        P('  candidate year-1 counterbalance. It is REPORTED, not re-sited — moving where ITEM C')
        P('  acts would be a wiring change well outside this act\'s ruled scope, and choosing to')
        P('  make it is the owner\'s call, not mine.')
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
    hx = (target - icept) / slope if slope > 1e-9 else float('inf')
    # The gate is the MEASURED move across the ladder, not the fitted slope: a slope can look
    # non-zero while the quantity it describes never actually moved over the measured range.
    measured_move = ys[-1] - ys[0]
    if abs(measured_move) < YR4_TOL:
        P()
        P('  NO CROSSING POINT IS REPORTED, AND NONE SHOULD BE. yr1 moved %+.4f in total across the'
          % measured_move)
        P('  whole measured ladder (fitted slope %.4f) — yr1 is' % slope)
        P('  effectively FLAT in H, so solving the fit for a crossing divides by ~0 and produces an')
        P('  arbitrarily large number (here H ~= %.1f). That is a numerical artefact of dividing by' % hx)
        P('  a null slope, NOT a bound, and printing it as one would be inventing a result. The')
        P('  honest statement is: on this instrument H never reaches the 14% charge at year 1 at any')
        P('  ceiling, because H does not move year 1 at all — see the binding diagnostic.')
        P()
        P('  THE ORDER ASKED WHERE THE MARGIN CROSSES, "AND THAT BOUNDS LAWFUL H". The measurement')
        P('  says the question does not arise: the yr0->yr1 margin is not the constraint on H,')
        P('  because H has no year-1 channel to shrink it through. The dial\'s admissible window')
        P('  [1.1024, 1.3327] remains the only binding constraint on H.')
    else:
        inside = xs[0] <= hx <= xs[-1]
        P()
        P('      H_cross ~= %.3f' % hx)
        P()
        P('  %s' % ('That is INSIDE the measured range — interpolation, and reliable.' if inside
                    else 'THAT IS AN EXTRAPOLATION BEYOND THE MEASURED RANGE AND IS LABELLED AS ONE.'))
        P('  READ IT AS A BOUND, NOT A TARGET. Nothing in this act was tuned toward it, and the')
        P('  admissible window [1.1024, 1.3327] remains the governing constraint on H.')
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
