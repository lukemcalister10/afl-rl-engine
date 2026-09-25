"""TASK 6 -- DRAFT AGE (D7), FITTED TO PLAYING QUALITY ONLY, PER STREAM.

THE STANDING LAW (owner, 2026-08-11): "we don't value players on whether they play, we value them on
how they play." Availability is NEVER a valuation basis.

THE CAUTIONARY CASE ON THE RECORD: ITEM B's draft-age steps were fitted to D_rt_win, a measure that
rises when a player plays MORE as well as when he plays BETTER, and were RETIRED for exactly that
(_merged_recover.py:1810-1822; SPLIT B_PROVENANCE_AND_SPLITS.md 3.1). The knots are kept behind
RL_B_SHAPE and the shipped default is FLAT -- _b_shape == 1.0 at every age, so _b_factor == 1.0
exactly and there is NO age adjustment in force today. This task asks whether one is earned.

THE MEASURE, and why two of them are reported rather than one:

  Q_player = SUM(games * avg) / SUM(games)      -- the player's own scoring RATE. Pure quality: it is
                                                   points per game and cannot rise by playing more.

  (A) UNWEIGHTED MEAN of Q_player across players   <- PRIMARY. One player, one vote. No participation
                                                      channel of any kind.
  (B) GAMES-WEIGHTED mean across players           <- the column D7's table used. Reported for
                                                      comparability, and FLAGGED: weighting players by
                                                      games lets high-participation players dominate
                                                      the stream mean, which is a participation
                                                      channel re-entering through the weights. It is
                                                      NOT used to decide anything here.

THE UNAVOIDABLE PARTICIPATION FILTER, STATED RATHER THAN HIDDEN: a player who never played has no
scoring rate, so quality is undefined for him and he cannot enter this measure. That is a
participation-conditioned sample and it is a real limit on every conclusion below. It is not a choice
the seat made; it is what "how they play" means for someone who did not.

THE DECISION RULE, PRE-SPECIFIED HERE BEFORE THE NUMBERS WERE SEEN, so no stream is talked into or
out of a signal after the fact. A stream gets an age adjustment ONLY IF BOTH hold:
    (i)  the OLS slope of Q_player on continuous draft age is significant at |t| >= 2.0, AND
    (ii) the fitted change across that stream's own observed age range is >= 2% of its mean quality.
If either fails the stream gets NO age adjustment. That is a finding, not a failure.

READ-ONLY. No emits. Deterministic.
"""
import sys, json, os, math, collections

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']

T_BAR = 2.0
MAT_BAR = 0.02
ORDER = ['ND 1-64', 'RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


def quality(r):
    """Points per game over the career. Cannot rise by playing more."""
    g = a = 0.0
    for s in r.get('seasons') or []:
        gg = float(s.get('games') or 0)
        if gg <= 0: continue
        g += gg; a += gg * float(s.get('avg') or 0.0)
    return (a / g, g) if g > 0 else (None, 0.0)


def ols(xs, ys):
    n = len(xs)
    if n < 3: return None
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx <= 0: return None
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    resid = [y - (a + b * x) for x, y in zip(xs, ys)]
    dof = n - 2
    if dof <= 0: return None
    s2 = sum(e * e for e in resid) / dof
    se = math.sqrt(s2 / sxx) if sxx > 0 else float('inf')
    t = b / se if se > 0 else 0.0
    return dict(n=n, slope=b, intercept=a, se=se, t=t, mean_y=my, xmin=min(xs), xmax=max(xs))


P = print
P("=" * 118)
P("TASK 6 -- DRAFT AGE (D7), FITTED TO PLAYING QUALITY ONLY, PER STREAM")
P("=" * 118)
P("  quality = SUM(games*avg)/SUM(games) per player -- POINTS PER GAME. It cannot rise by playing more.")
P("  PRIMARY aggregate = unweighted mean across players (one player, one vote).")
P("  Shipped state today: _b_shape is FLAT (RL_B_SHAPE=0), so there is NO age adjustment in force.")
P()
P("  PRE-SPECIFIED DECISION RULE (written before the numbers): adjustment ONLY IF |t| >= %.1f AND the"
  % T_BAR)
P("  fitted change across the stream's own age range is >= %.0f%% of its mean quality." % (100 * MAT_BAR))
P()

DATA = {}
for s in ORDER:
    sub = [r for r in R if stream(r) == s]
    rows = []
    for r in sub:
        q, g = quality(r)
        a = r.get('age_draft')
        if q is None or a is None: continue
        rows.append((float(a), q, g))
    DATA[s] = (sub, rows)

P("=" * 118)
P("COVERAGE -- how much of each stream can be measured at all, and what the filter costs")
P("=" * 118)
P("  %-9s %6s %8s %8s %10s %10s" % ('stream', 'n', 'played', 'age known', 'MEASURED', 'excluded'))
P("  " + "-" * 114)
for s in ORDER:
    sub, rows = DATA[s]
    played = sum(1 for r in sub if quality(r)[0] is not None)
    aged = sum(1 for r in sub if r.get('age_draft') is not None)
    P("  %-9s %6d %8d %8d %10d %10d" % (s, len(sub), played, aged, len(rows), len(sub) - len(rows)))
P()
P("  The 'excluded' column is dominated by never-played rows. Every conclusion below is conditional")
P("  on having played, and that conditioning cannot be removed.")
P()

P("=" * 118)
P("QUALITY BY DRAFT-AGE BAND -- primary (unweighted) beside D7's games-weighted column")
P("=" * 118)
P("  %-9s %6s | %8s %8s %8s | %8s %8s %8s | %9s" %
  ('stream', 'n', '<=18', '19-20', '21+', '<=18', '19-20', '21+', 'games-wtd'))
P("  %-9s %6s | %26s | %26s |" % ('', '', '--- UNWEIGHTED (primary) ---', '--- games-weighted (D7) ---'))
P("  " + "-" * 114)


def band(a): return '<=18' if a <= 18 else ('19-20' if a <= 20 else '21+')


for s in ORDER:
    sub, rows = DATA[s]
    if not rows: continue
    bu, bw = {}, {}
    for b in ('<=18', '19-20', '21+'):
        g = [(a, q, gg) for a, q, gg in rows if band(a) == b]
        bu[b] = (sum(q for _, q, _ in g) / len(g)) if g else None
        tw = sum(gg for _, _, gg in g)
        bw[b] = (sum(q * gg for _, q, gg in g) / tw) if tw else None
    gw = sum(q * gg for _, q, gg in rows) / sum(gg for _, _, gg in rows)
    f = lambda v: ("%8.2f" % v) if v is not None else "%8s" % '-'
    P("  %-9s %6d | %s %s %s | %s %s %s | %9.2f" %
      (s, len(rows), f(bu['<=18']), f(bu['19-20']), f(bu['21+']),
       f(bw['<=18']), f(bw['19-20']), f(bw['21+']), gw))
P()

P("=" * 118)
P("THE FIT -- OLS of player quality on CONTINUOUS draft age, per stream")
P("=" * 118)
P("  %-9s %6s | %10s %9s %8s | %9s %9s | %9s" %
  ('stream', 'n', 'slope/yr', 'se', 't', 'mean Q', 'range eff', '% of mean'))
P("  " + "-" * 114)
FIT = {}
for s in ORDER:
    sub, rows = DATA[s]
    if len(rows) < 3:
        P("  %-9s %6d | %10s %9s %8s | %9s %9s | %9s" % (s, len(rows), '-', '-', '-', '-', '-', '-'))
        FIT[s] = None
        continue
    f = ols([a for a, _, _ in rows], [q for _, q, _ in rows])
    FIT[s] = f
    if f is None:
        P("  %-9s %6d | %10s" % (s, len(rows), 'degenerate')); continue
    eff = f['slope'] * (f['xmax'] - f['xmin'])
    pct = abs(eff) / f['mean_y'] if f['mean_y'] else 0.0
    P("  %-9s %6d | %10.3f %9.3f %8.2f | %9.2f %9.2f | %8.1f%%" %
      (s, f['n'], f['slope'], f['se'], f['t'], f['mean_y'], eff, 100 * pct))
P()

P("=" * 118)
P("THE VERDICT PER STREAM, against the pre-specified rule")
P("=" * 118)
P("  %-9s %8s %8s %10s %10s | %s" % ('stream', 't', '|t|>=2', '% of mean', '>=2%', 'RULING'))
P("  " + "-" * 114)
VERD = {}
for s in ORDER:
    f = FIT[s]
    if f is None:
        VERD[s] = 'NO ADJUSTMENT (insufficient sample)'
        P("  %-9s %8s %8s %10s %10s | %s" % (s, '-', '-', '-', '-', VERD[s]))
        continue
    eff = f['slope'] * (f['xmax'] - f['xmin'])
    pct = abs(eff) / f['mean_y'] if f['mean_y'] else 0.0
    c1 = abs(f['t']) >= T_BAR
    c2 = pct >= MAT_BAR
    VERD[s] = 'AGE ADJUSTMENT EARNED' if (c1 and c2) else 'NO ADJUSTMENT'
    P("  %-9s %8.2f %8s %9.1f%% %10s | %s" %
      (s, f['t'], 'yes' if c1 else 'NO', 100 * pct, 'yes' if c2 else 'NO', VERD[s]))
P()
earned = [s for s in ORDER if VERD[s] == 'AGE ADJUSTMENT EARNED']
pool_earned = [s for s in earned if s != 'ND 1-64']
P("  STREAMS EARNING AN AGE ADJUSTMENT: %s" % (', '.join(earned) if earned else 'NONE'))
P("  of which POOL pathways: %d of 9 -- %s" % (len(pool_earned), ', '.join(pool_earned) if pool_earned else 'NONE'))
P()

P("=" * 118)
P("THE ITEM B CONTRAST -- why the retired steps are not reinstated by this measure")
P("=" * 118)
P()
P("  ITEM B's retirement note records its own defect (_merged_recover.py:1810-1820): quality across")
P("  draft age read 51.47 / 52.98 / 53.33 at <=18 / 19-20 / 21+ while PARTICIPATION (career games)")
P("  read 24.7 / 31.7 / 21.6 -- the 21+ slice playing the LEAST of the three while being priced")
P("  HIGHEST by a measure that rewarded playing more. Measured here on quality alone:")
P()
P("  %-9s %8s %8s %8s | %9s %9s %9s" %
  ('stream', 'Q<=18', 'Q19-20', 'Q21+', 'games<=18', 'g19-20', 'g21+'))
P("  " + "-" * 114)
for s in ORDER:
    sub, rows = DATA[s]
    if not rows: continue
    o = []
    for b in ('<=18', '19-20', '21+'):
        g = [(a, q, gg) for a, q, gg in rows if band(a) == b]
        o.append(((sum(q for _, q, _ in g) / len(g)) if g else None,
                  (sum(gg for _, _, gg in g) / len(g)) if g else None))
    f = lambda v: ("%8.2f" % v) if v is not None else "%8s" % '-'
    f2 = lambda v: ("%9.1f" % v) if v is not None else "%9s" % '-'
    P("  %-9s %s %s %s | %s %s %s" %
      (s, f(o[0][0]), f(o[1][0]), f(o[2][0]), f2(o[0][1]), f2(o[1][1]), f2(o[2][1])))
P()
P("  Quality and participation move DIFFERENTLY across age bands. Any measure that mixes them prices")
P("  the mixture, which is precisely what retired ITEM B. Nothing above is fitted to participation.")
P()

out = dict(rule=dict(t_bar=T_BAR, material_bar=MAT_BAR),
           fits={s: FIT[s] for s in FIT}, verdicts=VERD,
           earned=earned, pool_earned=pool_earned,
           shipped_state='_b_shape FLAT (RL_B_SHAPE=0) -- no age adjustment in force')
json.dump(out, open(os.path.join(HERE, 'PHASE1_AGE.json'), 'w'), indent=1, default=float)
P("wrote PHASE1_AGE.json")
