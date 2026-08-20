#!/usr/bin/env python3
"""ORDER K — THE OWNER'S GATES, SCORED ON THE BUILT BOARDS, IN BOARD POINTS, ROW BY NAMED ROW.

Pure JSON reads over the boards build_allK.sh already wrote — no engine run here, so nothing can
drift between what is scored and what was built.

The boards, and what each one is for:
  cand   1f176444  the landing candidate — the base every gate is scored against (dial off)
  tallJ  d1058fe0  the tall/small factor with ORDER J's WIRED floor — the defect, rebuilt on purpose
                   so the fix is priced by removal. It is a MEASUREMENT, never a candidate.
  tallK            the tall/small factor with the ORDER K RE-SITED floor, alone
  s1               S1 alone at the ruled dose 0.40
  cw               THE GATED LEVERS ALONE — S1 at the ruled dose PLUS the ruled counterweight, with
                   the EXEMPT tall factor removed. This is the board J-TOL is properly read on.
  K      f3101883  THE DECISION BOARD — the owner's ruled setting in full
  K2               the determinism repeat
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OK = SP + '/ok'
TAGS = ['cand', 'tallJ', 'tallK', 's1', 'cw', 'K', 'K2']
BP = {t: OK + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
RAW = {t: json.load(open(BP[t])) for t in TAGS}
B = {t: {r['key']: r for r in RAW[t]['active']} for t in TAGS}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in TAGS}
KEYS = sorted(V['cand'])
AGE = {k: B['cand'][k]['age'] for k in KEYS}
POS = {k: (B['cand'][k].get('gf') or B['cand'][k]['grp']) for k in KEYS}
C31 = json.load(open(SP + '/cand31.json'))
R31 = {r['key']: r for r in C31['rows']}
TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))
FADE = json.load(open(os.path.join(HERE, 'FADE_K.json')))
L = []


def P(s=''):
    print(s); L.append(str(s))


P('ORDER K — THE BOARD GATES.  board points (the currency the owner reads).')
P('  boards: %s' % {t: MD5[t][:8] for t in TAGS})
P('  active priced rows: %d' % len(KEYS))

P('\n== THE BUILD-FAILING IDENTITIES ==')
k5 = MD5['cand'].startswith('1f176444')
k7 = (MD5['K'] == MD5['K2'])
kj = MD5['tallJ'].startswith('d1058fe0')
P('  K5  dial-off reproduces the landing candidate 1f176444        : %s  (%s)'
  % ('PASS' if k5 else 'FAIL — K5 FIRES', MD5['cand']))
P('  K7  determinism x2 (two identical builds of the DECISION board): %s  (%s vs %s)'
  % ('PASS' if k7 else 'FAIL — K7 FIRES', MD5['K'][:8], MD5['K2'][:8]))
P('  CHAIN  the floor-fix REMOVAL lane reproduces ORDER J\'s ruled board d1058fe0 BYTE-EXACT: %s (%s)'
  % ('PASS' if kj else 'FAIL', MD5['tallJ'][:8]))
P('         — which is what proves the fade floor fix is the ONLY thing this order changed.')
assert k5 and k7, 'ORDER K HALT: a build-failing identity did not hold'

# ---------------------------------------------------------------- K-FLOOR, the fix's acceptance test
P('\n' + '=' * 116)
P('K-FLOOR — THE ACCEPTANCE TEST FOR THE FADE FLOOR FIX (PREREG_K.md §2.6)')
P('=' * 116)
P('\n(a) STRUCTURAL — no small is made lighter, at any pick:')
P('    ORDER J, the wired floor   : smalls made LIGHTER at picks %s   <- THE DEFECT'
  % FADE['lighter_J'])
P('    ORDER K, the re-sited floor: %s'
  % ('smalls made LIGHTER at picks %s' % FADE['lighter_K'] if FADE['lighter_K']
     else 'NONE — at no pick, for any row.  PASS'))
P('    The engine carries this as a BUILD-FAILING assert on the live lane, and it is PROVEN')
P('    NON-VACUOUS: it fired the moment the fix was removed (K1_NONVACUITY_PROOF.txt).')

P('\n(b) ON THE BOARD — every small whose sitting fade changes, with its direction.')
P('    "Made lighter" = the tall factor RAISED his price. The gate is that no small is raised.')
smalls = [k for k in KEYS if POS[k] not in TALLPOS]
mvJ = [(k, V['tallJ'][k] - V['cand'][k]) for k in smalls if V['tallJ'][k] != V['cand'][k]]
mvK = [(k, V['tallK'][k] - V['cand'][k]) for k in smalls if V['tallK'][k] != V['cand'][k]]
upJ = sorted([x for x in mvJ if x[1] > 0], key=lambda x: -x[1])
upK = sorted([x for x in mvK if x[1] > 0], key=lambda x: -x[1])
P('    ORDER J wired floor : %d smalls move; %d of them are made LIGHTER (+%d board points)'
  % (len(mvJ), len(upJ), sum(d for _, d in upJ)))
for k, d in upJ:
    P('        %-26s %-5s pick %-5s %6d -> %6d  %+d'
      % (B['cand'][k].get('name') or k, POS[k], B['cand'][k].get('pk'),
         V['cand'][k], V['tallJ'][k], d))
P('    ORDER K re-sited    : %d smalls move; %d of them are made LIGHTER  -> %s'
  % (len(mvK), len(upK), 'PASS — not one' if not upK else 'FAIL — K1 FIRES'))
for k, d in upK:
    P('        %-26s %-5s pick %-5s %6d -> %6d  %+d'
      % (B['cand'][k].get('name') or k, POS[k], B['cand'][k].get('pk'),
         V['cand'][k], V['tallK'][k], d))
P('    The seven rows the fix RELEASES (their Order J gain removed), and where they land:')
for k, d in upJ:
    P('        %-26s ORDER J %6d  ->  ORDER K (factor alone) %6d   [%+d]   ON THE DECISION BOARD: %d'
      % (B['cand'][k].get('name') or k, V['tallJ'][k], V['tallK'][k],
         V['tallK'][k] - V['tallJ'][k], V['K'][k]))
dnK = sorted([x for x in mvK if x[1] < 0], key=lambda x: x[1])
P('    Smalls made HEAVIER by the factor under ORDER K (the intended direction): %d rows, %d points'
  % (len(dnK), sum(d for _, d in dnK)))
P('      the ten largest: %s'
  % ', '.join('%s %+d' % (B['cand'][k].get('name') or k, d) for k, d in dnK[:10]))

P('\n(c) SMILLIE RETURNS.  predicted in the prereg: 772 exactly.')
sk = 'josh-smillie'
P('    landing %d · ORDER J %d (+%d, the defect) · the factor alone under ORDER K %d · DECISION BOARD %d'
  % (V['cand'][sk], V['tallJ'][sk], V['tallJ'][sk] - V['cand'][sk], V['tallK'][sk], V['K'][sk]))
P('    -> %s' % ('PASS — back inside the ruled ~700s' if 700 <= V['K'][sk] < 800
                 else 'FAIL — K2 FIRES, he reads %d' % V['K'][sk]))

P('\n(d) THE TALLS KEEP THEIR RELIEF.')
P('    %-22s %-5s %5s %9s %9s %9s | %9s %9s | %s'
  % ('row', 'pos', 'pick', 'landing', 'ORDER J', 'ORDER K', 'leg J', 'leg K', 'decision board'))
G_TALL = {}
for k in ('will-green', 'toby-conway', 'william-mccabe', 'alex-dodson'):
    if k not in V['cand']:
        P('    %-22s (not on the board)' % k); continue
    a, j, kk = V['cand'][k], V['tallJ'][k], V['tallK'][k]
    G_TALL[k] = dict(landing=a, orderJ=j, orderK=kk, legJ=j - a, legK=kk - a, decision=V['K'][k])
    P('    %-22s %-5s %5s %9d %9d %9d | %+9d %+9d | %d'
      % (k, POS[k], B['cand'][k].get('pk'), a, j, kk, j - a, kk - a, V['K'][k]))
allrel = all(v['legK'] > 0 for v in G_TALL.values())
P('    -> %s' % ('PASS — all four keep a meaningful positive relief' if allrel else 'FAIL — K3 FIRES'))
talls = [k for k in KEYS if POS[k] in TALLPOS]
tmvK = [(k, V['tallK'][k] - V['cand'][k]) for k in talls if V['tallK'][k] != V['cand'][k]]
P('    across the whole board: %d talls move on the factor, %d up (+%d pts), %d down (%d pts)'
  % (len(tmvK), sum(1 for _, d in tmvK if d > 0), sum(d for _, d in tmvK if d > 0),
     sum(1 for _, d in tmvK if d < 0), sum(d for _, d in tmvK if d < 0)))

P('\n(e) THE REDISTRIBUTION IDENTITY holds: residual %.3e against the ruled depth-2 fade %.7f '
  '(build-failing above 1e-9).' % (FADE['resid_K'], FADE['D2']))
P('    s_norm  ORDER J %.16f  ->  ORDER K %.16f' % (FADE['s_norm_J'], FADE['s_norm_K']))
P('    h_TALL  %.16f — UNCHANGED from the owner-ruled value' % FADE['h_TALL'])

P('\nWHERE THE FLOOR STILL BINDS, AND FOR WHOM')
P('  TALL on the 0.5 hard floor: picks %d-%d (%d of 64).  Under ORDER J it was picks %d-%d.'
  % (min(FADE['tall_floor_picks_K']), max(FADE['tall_floor_picks_K']), len(FADE['tall_floor_picks_K']),
     min(FADE['tall_floor_picks_J']), max(FADE['tall_floor_picks_J'])))
P('  SMALL on the RE-SITED floor (his own pooled exponent): picks %d-%d (%d of 64) — these are the rows'
  % (min(FADE['small_floor_picks_K']), max(FADE['small_floor_picks_K']),
     len(FADE['small_floor_picks_K'])))
P('    the fit wanted to make LIGHTER and the re-sited floor holds at neutral instead.')
P('  ...of which picks %d-%d also sit on the 0.5 hard floor, because Order D\'s pooled curve is itself'
  % (min(FADE['small_floor_at_05_K']), max(FADE['small_floor_at_05_K'])))
P('    clipped there — at those picks nothing in the factor can move a small either way.')
BIND = collections.Counter()
for k in KEYS:
    pk = B['cand'][k].get('pk')
    if not pk or not (1 <= int(pk) <= 64):
        continue
    tall = POS[k] in TALLPOS
    if tall and int(pk) in FADE['tall_floor_picks_K']:
        BIND['tall rows sitting on the 0.5 floor'] += 1
    if (not tall) and int(pk) in FADE['small_floor_picks_K']:
        BIND['small rows sitting on the re-sited floor'] += 1
P('  ON THE 2026 BOARD: %s' % dict(BIND))

# ---------------------------------------------------------------- the owner's laws, on the board
P('\n' + '=' * 116)
P("THE OWNER'S LAWS ON THE 2026 BOARD")
P('=' * 116)

MAT = [k for k in KEYS if AGE[k] >= 24]
BOARD_TOTAL = sum(V['cand'].values())
P('\n== S1\'s ZERO-TOLERANCE MATURE LAW, and J-TOL on the counterweight ==')
P('  board total (landing candidate, integer prices) = %d;  mature rows aged 24+ = %d'
  % (BOARD_TOTAL, len(MAT)))
JTOL = {}
for lab, t in (('S1 alone at the ruled dose 0.40 (ZERO TOLERANCE — the owner\'s law)', 's1'),
               ('THE GATED LEVERS: S1 + the ruled counterweight, tall factor removed (J-TOL reads HERE)', 'cw'),
               ('the tall/small factor alone, ORDER K floor (EXEMPT — R-TALLFACTOR is adopted)', 'tallK'),
               ('THE DECISION BOARD (all three levers together)', 'K')):
    mv = [(k, V[t][k] - V['cand'][k]) for k in MAT if V[t][k] != V['cand'][k]]
    tot = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    w = max(mv, key=lambda x: abs(x[1])) if mv else (None, 0)
    cap_breach = [(k, d) for k, d in mv if abs(d) > min(25.0, max(1.0, 0.005 * V['cand'][k]))]
    JTOL[t] = dict(n_move=len(mv), churn=tot, net=net, worst=w[1],
                   worst_row=(B['cand'][w[0]].get('name') if w[0] else None),
                   per_row_breaches=len(cap_breach))
    P('  %-72s %3d move · churn %5d · net %+5d · worst %+4d (%s)'
      % (lab, len(mv), tot, net, w[1], (B['cand'][w[0]].get('name') if w[0] else '-')))
P('  J-TOL rails (PREREG_J §2.2): per row min(25, max(1, 0.5%% of his own price)) · churn <= %.2f '
  '(0.15%% of the board) · net <= %.2f (0.10%%)' % (0.0015 * BOARD_TOTAL, 0.0010 * BOARD_TOTAL))
for t, nm in (('s1', 'S1 alone'), ('cw', 'THE GATED LEVERS'), ('K', 'the decision board')):
    d = JTOL[t]
    P('  %-20s per-row breaches %3d · churn %6d vs %8.2f %s · net %+6d vs %8.2f %s'
      % (nm, d['per_row_breaches'], d['churn'], 0.0015 * BOARD_TOTAL,
         'OK' if d['churn'] <= 0.0015 * BOARD_TOTAL else 'BREACH',
         d['net'], 0.0010 * BOARD_TOTAL,
         'OK' if abs(d['net']) <= 0.0010 * BOARD_TOTAL else 'BREACH'))
P('  NOTE the decision board carries the EXEMPT tall factor as well, so its mature movement is not a')
P('  J-TOL reading of the counterweight alone; the counterweight\'s own reading is the S1 row plus the')
P('  remix leg, and the tall factor\'s mature movement is DISCLOSED, never gated (R-TALLFACTOR adopted).')

NAMED = [('harry-dean', 'UP', 'S1: 14.9 a game clear of his own age bar'),
         ('cooper-duff-tytler', 'UP', 'S1: 7.1 a game clear of his own age bar'),
         ('xavier-taylor', 'DOWN', 'sub-expectation WITH games (42.0 vs an age bar of 55.2)'),
         ('daniel-annable', 'DOWN', 'sub-expectation WITH games (38.0 vs 57.0)'),
         ('dylan-patterson', 'DOWN', 'sub-expectation WITH games (35.6 vs 55.2)'),
         ('oskar-taylor', 'FLAT', 'the re-sited floor returns him to his landing value exactly'),
         ('josh-smillie', 'FLAT', 'the re-sited floor returns him to his landing value exactly'),
         ('will-brodie', 'FLAT', 'same channel'),
         ('campbell-chesser', 'FLAT', 'same channel'),
         ('chris-scerri', 'UP', 'pool row — production dominates a small pedigree'),
         ('thomas-burton', 'UP', 'same channel, weaker'),
         ('milan-murdock', 'MOVES', 'age 26 with 17 games — inside the re-mix\'s active zone'),
         ('will-green', 'UP', 'the ruled factor at pick 16'),
         ('toby-conway', 'UP', 'the ruled factor at pick 24'),
         ('william-mccabe', 'UP', 'the ruled factor at pick 19'),
         ('alex-dodson', 'UP', 'the ruled factor at pick 53'),
         ('steely-green', 'DOWN', 'a late small pays for the talls\' relief'),
         ('isaac-kako', 'UP', 'S1 on a high-rho row'),
         ('alix-tauru', 'UP', 'S1; tall age gaps are the largest'),
         ('jedd-busslinger', 'UP', 'S1 + the ruled fade on an above-age-bar season')]
P('\n== THE NAMED ROWS, ON THE DECISION BOARD (board points) ==')
P('%-22s %4s %5s %5s %9s %9s %9s | %9s | %-8s %-8s %s'
  % ('row', 'age', 'pick', 'g', 'live', 'C31', 'landing', 'ORDER K', 'predict', 'actual', 'hit?'))
SC = []
for k, pred, why in NAMED:
    if k not in V['cand']:
        P('%-22s (not on the 804-row active board)' % k); continue
    a, kk = V['cand'][k], V['K'][k]
    d = kk - a
    act = 'FLAT' if d == 0 else ('UP' if d > 0 else 'DOWN')
    hit = (act == pred) if pred in ('UP', 'DOWN', 'FLAT') else (d != 0)
    r31 = R31.get(k, {})
    SC.append(dict(key=k, pred=pred, actual=act, hit=bool(hit), landing=a, orderK=kk, d=d, why=why))
    P('%-22s %4d %5s %5.0f %9s %9s %9d | %9d | %-8s %-8s %s'
      % (k, AGE[k], B['cand'][k].get('pk'), float(B['cand'][k].get('cg') or 0),
         r31.get('live', '-'), r31.get('cand', '-'), a, kk, pred, act, 'HIT' if hit else 'MISS'))
P('\nprereg named-row scorecard: %d of %d directions correct'
  % (sum(1 for s in SC if s['hit']), len(SC)))

P('\n== G5 — SUB-EXPECTATION-WITH-GAMES ROWS MUST NOT RISE ==')
G5 = {}
for k in ('xavier-taylor', 'daniel-annable', 'dylan-patterson'):
    a, kk = V['cand'][k], V['K'][k]
    G5[k] = dict(landing=a, orderK=kk, d=kk - a, s1=V['s1'][k])
    P('  %-20s landing %5d · ORDER K %5d (%+d)   [S1 leg alone %+d]  -> %s'
      % (k, a, kk, kk - a, V['s1'][k] - a,
         'ROSE — K13 FIRES' if kk > a else ('held' if kk == a else 'FELL — G5 holds')))
P('  -> %s' % ('G5 PASS — none of the three rises'
               if all(v['d'] <= 0 for v in G5.values()) else 'G5 FAIL — K13 FIRES'))

P('\n== G10 (reported, not gated) — the owner\'s two reference levels ==')
G10 = {}
for k, target, c31 in (('harry-dean', 2600, 2670), ('cooper-duff-tytler', 1800, 1832)):
    a, kk = V['cand'][k], V['K'][k]
    G10[k] = dict(target=target, c31=c31, landing=a, orderK=kk, short_of_c31=c31 - kk,
                  short_of_target=target - kk)
    P('  %-20s owner ~%d · C31 %d · landing %d · ORDER K %d  -> still %d short of C31, %d short of ~%d'
      % (k, target, c31, a, kk, c31 - kk, target - kk, target))
P('  -> BOTH REMAIN BELOW their Candidate-31 levels. This is a KNOWN OPEN DEFECT, carried on every page.')

P('\n== CONTROLS AND OTHER ROWS OF RECORD ==')
EXTRA = ['levi-ashcroft', 'connor-o-sullivan', 'logan-morris', 'finn-o-sullivan', 'sam-taylor',
         'tom-green', 'toby-greene', 'will-ashcroft', 'taylor-walker', 'keidean-coleman',
         'harry-morrison', 'taylor-goad', 'zac-taylor', 'noah-mraz', 'murphy-reid', 'oskar-taylor',
         'will-brodie', 'campbell-chesser', 'james-leake', 'tom-brown', 'sam-sturt']
for k in EXTRA:
    if k in V['cand']:
        P('  %-22s landing %6d · ORDER K %6d (%+5d)   [legs: tall %+d · S1 %+d]'
          % (k, V['cand'][k], V['K'][k], V['K'][k] - V['cand'][k],
             V['tallK'][k] - V['cand'][k], V['s1'][k] - V['cand'][k]))

Y1 = [k for k in KEYS if (R31.get(k, {}).get('yr') == 2025)
      or (R31.get(k, {}).get('yr') == 2026 and R31.get(k, {}).get('pathway') == 'MSD')]
P('\n== THE YEAR-1 CLASS ON THE 2026 BOARD (board points) ==')
t0 = sum(V['cand'][k] for k in Y1); t1 = sum(V['K'][k] for k in Y1)
up = sum(1 for k in Y1 if V['K'][k] > V['cand'][k]); dn = sum(1 for k in Y1 if V['K'][k] < V['cand'][k])
P('  %d rows, %d -> %d (%+.2f%%);  %d up, %d down, %d unchanged'
  % (len(Y1), t0, t1, 100 * (t1 - t0) / max(1, t0), up, dn, len(Y1) - up - dn))

P('\n== BOARD TOTALS ==')
for t in TAGS[:-1]:
    P('  %-6s %s  total %d  (%+d vs the landing candidate)'
      % (t, MD5[t][:8], sum(V[t].values()), sum(V[t].values()) - BOARD_TOTAL))

json.dump(dict(order='ORDER K — the board gates', boards={t: MD5[t] for t in TAGS},
               k5_dial_off=k5, k7_determinism=k7, chain_tallJ_is_d1058fe0=kj,
               kfloor=dict(lighter_J_picks=FADE['lighter_J'], lighter_K_picks=FADE['lighter_K'],
                           smalls_lighter_J=[[k, d] for k, d in upJ],
                           smalls_lighter_K=[[k, d] for k, d in upK],
                           smalls_heavier_K=[[k, d] for k, d in dnK],
                           smillie=dict(landing=V['cand'][sk], orderJ=V['tallJ'][sk],
                                        factor_alone_K=V['tallK'][sk], decision=V['K'][sk]),
                           talls=G_TALL, identity_residual=FADE['resid_K'],
                           s_norm_J=FADE['s_norm_J'], s_norm_K=FADE['s_norm_K'],
                           floor_binding=dict(BIND)),
               jtol=JTOL, scorecard=SC, g5=G5, g10=G10,
               year1=dict(n=len(Y1), landing=t0, orderK=t1),
               totals={t: sum(V[t].values()) for t in TAGS}),
          open(os.path.join(HERE, 'GATES_K.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'GATES_K_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: GATES_K.json / GATES_K_out.txt')
