#!/usr/bin/env python3
"""ORDER S READ-ONLY — F2. THE GRADED RESET, AND THE 9-vs-10 GAMES CLIFF.

NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NO BOARD IS BUILT. NOTHING IS ADOPTED AND NO FIX IS
PROPOSED. The injury-stream design is OUT OF SCOPE: every curve here is a function of the OBSERVABLE
(games, avg-vs-bar), with no absence-cause term, so a later injured/unexplained split can re-cut this
same population by cause without re-deriving anything.

THE WIRED OBJECT. o32_delivered(p, Y, x) is binary: games >= 10*f AND avg >= o32_gate_bar. A
DELIVERED season sets the accumulated unplayed clock c_u to zero as of that season. Everything before
it is wiped and nothing partial exists.

PART A — THE REVERSAL CURVE, on history, on the house S4 ruler. For players returning from
accumulated sitting, how much of the sitting damage actually reversed, as a function of how
convincing the return season was?

    reversal(g, m) = ( V(g, m) - V_sat ) / ( V_never - V_sat )
      V_sat   = same depth, played ZERO at the return depth too (kept sitting)     -> reversal 0
      V_never = same depth, NO prior sitting at all                                -> reversal 1
      m       = season avg - o32_gate_bar(position, age)

PART B — THE THRESHOLD CENSUS, on the board, exactly. How many rows sit within two games of the
10-game delivered threshold, and what does crossing it cost or pay? The counterfactual wraps the
engine's own o32_delivered IN THE LOADED NAMESPACE for one row at a time. NO REPOSITORY FILE IS
TOUCHED and the wrapper is proved inert at its identity setting.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_f2.py
"""
import json, math, os, sys, io, contextlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_n_2026-08-18'))
import on_lib as LB                                                          # noqa: E402
import os_lib as SL                                                          # noqa: E402

SEED, B_BOOT = 32, 2000
ENTRY_CUT = 2019
Y = 2026
L = []


def P(s=''):
    print(s); L.append(str(s))


M = LB.load_matrix('OKRULED')
P('=' * 118)
P('ORDER S READ-ONLY — F2. THE GRADED RESET, AND THE 9-vs-10 GAMES CLIFF.')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NOTHING IS ADOPTED. NO FIX IS')
P('PROPOSED. Named rows are exhibits and gate nothing.')
P('ruler : the house S4 delivered-value ruler, md5 %s' % LB.check_s4_copy())
P()

# =========================================================================================================
# PART A — THE REVERSAL CURVE
# =========================================================================================================
P('=' * 118)
P('PART A — THE REVERSAL CURVE ON HISTORY')
P('=' * 118)


def seasons_by_depth(r):
    ey = int(r.get('year') or 0)
    gb = r.get('games_by') or {}
    g = {}
    for d in range(1, 7):
        if str(d) not in gb:
            break
        g[d] = float(gb[str(d)]) - (float(gb[str(d - 1)]) if d > 1 else 0.0)
    byyear = {int(s['year']): s for s in r['seasons']}
    return ey, g, byyear


ROWS = []
for k, rr in M.items():
    if k in LB.FM or rr.get('type') != 'ND':
        continue
    ey = int(rr.get('year') or 0)
    if ey < LB.ENTRY_FLOOR or ey > ENTRY_CUT:
        continue
    v0 = float(rr.get('v0') or 0.0)
    if not (v0 > 0):
        continue
    ey, g, byyear = seasons_by_depth(rr)
    if len(g) < 3:
        continue
    sv = LB.season_values(rr)
    ROWS.append(dict(key=k, name=rr.get('player'), pos=rr.get('pos'), v0=v0, ey=ey, g=g,
                     byyear=byyear, sv=sv, age=rr.get('age_draft'), rec=rr))

P('   population: %d ND entrants from %d to %d with at least three observed depths.'
  % (len(ROWS), LB.ENTRY_FLOOR, ENTRY_CUT))
P()
P('   A RETURNER at depth N: zero games at depths N-1 AND N-2, then g > 0 at depth N.')
P('   A KEPT-SITTING row at depth N: zero at N-2, N-1 and N.')
P('   A NEVER-SAT row at depth N: no zero-game season at any depth up to N.')
P('   The OUTCOME in all three is the discounted house-ruler value from depth N+1 onward, over v0,')
P('   so the return season\'s own output is NOT inside the outcome it is being scored against.')
P()


def outcome(r, N):
    return LB.dvrest(r['sv'], r['ey'] + N) / r['v0']


def margin(r, N):
    s = r['byyear'].get(r['ey'] + N)
    if not s or s.get('avg') is None or s.get('bar') not in LB.BARS or r['age'] is None:
        return None
    b = LB.bar(s['bar'], int(r['age']) + N)
    return float(s['avg']) - b if b is not None else None


RET, SAT, NEV = [], [], []
for r in ROWS:
    g = r['g']
    for N in range(3, 7):
        if N not in g or (N - 1) not in g or (N - 2) not in g:
            continue
        if r['ey'] + N > LB.LAST_REAL_SEASON - 2:      # need at least two observed seasons after
            continue
        prior_zero = (g[N - 1] <= 0 and g[N - 2] <= 0)
        never = all(g[d] > 0 for d in range(1, N + 1) if d in g)
        rec = dict(key=r['key'], name=r['name'], N=N, g=g[N], v0=r['v0'],
                   out=outcome(r, N), m=margin(r, N), pos=r['pos'])
        if prior_zero and g[N] > 0:
            RET.append(rec)
        elif prior_zero and g[N] <= 0:
            SAT.append(rec)
        elif never:
            NEV.append(rec)

P('   %-24s %8s %12s' % ('group', 'n rows', 'mean outcome'))
for nm, s in (('RETURNERS', RET), ('KEPT SITTING', SAT), ('NEVER SAT', NEV)):
    P('   %-24s %8d %12.4f%s' % (nm, len(s), (np.mean([x['out'] for x in s]) if s else float('nan')),
                                 ' THIN' if len(s) < 25 else ''))
V_SAT = float(np.mean([x['out'] for x in SAT])) if SAT else float('nan')
V_NEV = float(np.mean([x['out'] for x in NEV])) if NEV else float('nan')
P()
P('   the two anchors: V_sat = %.4f (n %d), V_never = %.4f (n %d). The scale between them is %.4f.'
  % (V_SAT, len(SAT), V_NEV, len(NEV), V_NEV - V_SAT))
P()


def rev(vals):
    if not vals or math.isnan(V_SAT) or math.isnan(V_NEV) or abs(V_NEV - V_SAT) < 1e-12:
        return float('nan')
    return (float(np.mean(vals)) - V_SAT) / (V_NEV - V_SAT)


def bootrev(sel, B=800, seed=SEED):
    if len(sel) < 3:
        return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    v = np.array([x['out'] for x in sel])
    bs = [(np.mean(rng.choice(v, size=len(v), replace=True)) - V_SAT) / (V_NEV - V_SAT) for _ in range(B)]
    return (float(np.percentile(bs, 5)), float(np.percentile(bs, 95)))


P('-' * 118)
P('A1 · THE REVERSAL AGAINST THE GAMES LEG — IS THERE A STEP AT TEN?')
P('-' * 118)
P('   %-12s %7s %12s %-24s %14s' % ('return games', 'n', 'reversal', '90% CI', 'wired reset'))
GB = [('1-2', 1, 2), ('3-5', 3, 5), ('6-9', 6, 9), ('10-14', 10, 14), ('15+', 15, 999)]
A1 = {}
for lab, lo, hi in GB:
    sel = [x for x in RET if lo <= x['g'] <= hi]
    r_ = rev([x['out'] for x in sel])
    l_, h_ = bootrev(sel)
    wired = 1.0 if lo >= 10 else 0.0
    A1[lab] = dict(n=len(sel), rev=r_, ci=[l_, h_], wired=wired)
    P('   %-12s %7d %12.4f [%+9.4f, %+9.4f] %14.1f%s'
      % (lab, len(sel), r_, l_, h_, wired, ' THIN' if len(sel) < 25 else ''))
P()
P('   The wired reset column is what the engine credits: a FULL wipe (1.0) at ten games or more with')
P('   the avg leg cleared, and NOTHING (0.0) below ten however the season went.')
P()
lo9 = [x for x in RET if 6 <= x['g'] <= 9]
hi10 = [x for x in RET if 10 <= x['g'] <= 14]
sep = False
if len(lo9) >= 3 and len(hi10) >= 3:
    a, b = bootrev(lo9), bootrev(hi10)
    sep = (a[1] < b[0] or b[1] < a[0])
    P('   THE CELLS THAT STRADDLE THE THRESHOLD: 6-9 games [%.4f, %.4f] against 10-14 games'
      % (a[0], a[1]))
    P('   [%.4f, %.4f]. Separable? %s' % (b[0], b[1], 'YES' if sep else 'NO — the intervals overlap'))
P('   F2-P1 / F2-P4 verdict: %s'
  % ('a step at ten IS separable — F2-P4 FIRED, F2-P1 fired'
     if sep else 'NOT separable. F2-P4 did NOT fire: the preregistered NULL is the result.'))
P()

P('-' * 118)
P('A2 · THE REVERSAL AGAINST THE MARGIN LEG — DOES avg-vs-BAR MATTER?')
P('-' * 118)
P('   %-16s %7s %12s %-24s' % ('margin m (ppg)', 'n', 'reversal', '90% CI'))
MB = [('below -10', -1e9, -10), ('-10 to 0', -10, 0), ('0 to +10', 0, 10), ('+10 and up', 10, 1e9)]
A2 = {}
for lab, lo, hi in MB:
    sel = [x for x in RET if x['m'] is not None and lo <= x['m'] < hi]
    r_ = rev([x['out'] for x in sel])
    l_, h_ = bootrev(sel)
    A2[lab] = dict(n=len(sel), rev=r_, ci=[l_, h_])
    P('   %-16s %7d %12.4f [%+9.4f, %+9.4f]%s'
      % (lab, len(sel), r_, l_, h_, ' THIN' if len(sel) < 25 else ''))
P()
neg = [x for x in RET if x['m'] is not None and x['m'] < 0]
pos = [x for x in RET if x['m'] is not None and x['m'] >= 0]
flat = True
if len(neg) >= 3 and len(pos) >= 3:
    a, b = bootrev(neg), bootrev(pos)
    flat = not (a[1] < b[0] or b[1] < a[0])
    P('   below the bar [%.4f, %.4f] against at-or-above the bar [%.4f, %.4f]: %s'
      % (a[0], a[1], b[0], b[1], 'OVERLAP' if flat else 'SEPARABLE'))
P('   F2-P3 verdict: %s'
  % ('the outcome is FLAT in m at this sample — F2-P3 FIRED' if flat
     else 'the margin leg separates — F2-P3 did not fire'))
P()

P('-' * 118)
P('A3 · THE WIRED THRESHOLD POINT ITSELF — IS A BARE DELIVERED SEASON WORTH A FULL WIPE?')
P('-' * 118)
sel = [x for x in RET if 10 <= x['g'] <= 14 and x['m'] is not None and -5 <= x['m'] <= 5]
r_ = rev([x['out'] for x in sel])
l_, h_ = bootrev(sel)
P('   returners at 10-14 games with a margin inside +/- 5 points a game of their own bar — the')
P('   closest measurable neighbourhood of the wired threshold (g = 10, m = 0):')
P('     n = %d   reversal = %.4f   90%% CI [%.4f, %.4f]   the wired reset credits 1.0'
  % (len(sel), r_, l_, h_))
A3 = dict(n=len(sel), rev=r_, ci=[l_, h_])
if len(sel) >= 3 and not math.isnan(l_):
    P('   F2-P2 verdict: %s'
      % ('1.0 is INSIDE the interval — F2-P2 FIRED, a full wipe is not contradicted'
         if l_ <= 1.0 <= h_ else 'the interval EXCLUDES 1.0 — F2-P2 did not fire'))
else:
    P('   F2-P2 verdict: the cell holds %d rows. NOT SCORED — too thin to rule on either way.' % len(sel))
P()

# =========================================================================================================
# PART B — THE THRESHOLD CENSUS ON THE BOARD
# =========================================================================================================
P('=' * 118)
P('PART B — THE 9-vs-10 GAMES CLIFF, COUNTED AND PRICED ON THE ACTUAL BOARD')
P('=' * 118)
NS = SL.load(RL_O37='1')
NS['_REC'] = SL.install_recorder(NS)
MA = NS['_MA']
FNUM = json.load(open(SL.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
EV = NS['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, Y)
BOARD = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        BOARD[p['key']] = int(round(EV(p, Y) / FNUM))
P('   board total (numeraire): %d over %d rows — the ORDER P dial line.'
  % (sum(BOARD.values()), len(BOARD)))
P('   the in-progress season fraction the 10-game leg is prorated by: fE = %.4f, so the effective'
  % NS['M3_FE'])
P('   threshold in the CURRENT season is %.2f games, not 10.' % (10.0 * NS['M3_FE']))
P()

DEL = NS['o32_delivered']
NEAR = []
for p in MA.players:
    r = NS['_REC'].get((p.get('key'), Y))
    if not r:
        continue
    for x in (p.get('scoring') or []):
        if x['year'] > Y or not x.get('games'):
            continue
        f = NS['_fEy'](Y, p) if x['year'] == Y else 1.0
        thr = 10.0 * f
        g = float(x['games'])
        if abs(g - thr) > 2.0:
            continue
        d = DEL(p, Y, x)
        bar = NS['o32_gate_bar'](MA.gfut(p), (x['year'] - p['_by']) if p.get('_by') else None)
        avg_ok = bar is not None and float(x.get('avg') or 0.0) >= bar
        NEAR.append(dict(key=p['key'], name=p.get('player'), year=x['year'], g=g, thr=thr,
                         delivered=bool(d), avg=float(x.get('avg') or 0.0), bar=bar,
                         avg_ok=bool(avg_ok), board=BOARD[p['key']],
                         flips_down=bool(d and g - 2.0 < thr),
                         flips_up=bool((not d) and avg_ok and g + 2.0 >= thr)))
P('-' * 118)
P('B1 · THE POPULATION WITHIN TWO GAMES OF THE THRESHOLD')
P('-' * 118)
P('   %-52s %8s' % ('cell', 'rows'))
keys = set(x['key'] for x in NEAR)
fd = set(x['key'] for x in NEAR if x['flips_down'])
fu = set(x['key'] for x in NEAR if x['flips_up'])
P('   %-52s %8d' % ('board rows with a season inside +/- 2 games of the bar', len(keys)))
P('   %-52s %8d' % ('  of those, the season DELIVERS today', len(set(x['key'] for x in NEAR if x['delivered']))))
P('   %-52s %8d' % ('  of those, it does NOT deliver today', len(set(x['key'] for x in NEAR if not x['delivered']))))
P('   %-52s %8d' % ('rows a MINUS-2-game move would flip OUT of delivered', len(fd)))
P('   %-52s %8d' % ('rows a PLUS-2-game move would flip INTO delivered', len(fu)))
P('   %-52s %8d' % ('rows on the wrong side ONLY because of the games leg', len(fu)))
P()
P('   F2-P5 — does the +/- 2 game census hold at least 20 board rows? %s (%d)'
  % ('YES — F2-P5 did not fire' if len(keys) >= 20 else 'NO — F2-P5 FIRED', len(keys)))
P()

P('-' * 118)
P('B2 · WHAT THE FLIP IS WORTH — THE ENGINE\'S OWN o32_delivered, WRAPPED FOR ONE ROW AT A TIME')
P('-' * 118)
P('   The wrapper returns the OPPOSITE verdict for the one row and the one season being tested and')
P('   the engine\'s own answer for everything else. At the identity setting it is inert and that is')
P('   asserted below. NO REPOSITORY FILE IS TOUCHED.')
P()
TGT = {'key': None, 'year': None, 'flip': False}
orig = NS['o32_delivered']


def wrapped(p, Yv, x, _o=orig):
    v = _o(p, Yv, x)
    if TGT['flip'] and p.get('key') == TGT['key'] and int(x['year']) == TGT['year']:
        return not v
    return v


NS['o32_delivered'] = wrapped
# inertness assert
TGT['flip'] = False
NS['_O37_SCACHE'].clear()
with contextlib.redirect_stdout(io.StringIO()):
    chk = {p['key']: int(round(EV(p, Y) / FNUM)) for p in MA.players}
bad = [k for k in chk if chk[k] != BOARD[k]]
assert not bad, 'F2-A1 FIRED: the wrapper is not inert at its identity setting (%d rows)' % len(bad)
P('   FALSIFIER F2-A1 did not fire: at the identity setting all %d board rows reprice bit-identically.'
  % len(BOARD))
P()
FLIPS = []
cand = [x for x in NEAR if x['flips_down'] or x['flips_up']]
byk = {}
for x in cand:
    byk.setdefault(x['key'], x)
for k, x in byk.items():
    p = [q for q in MA.players if q['key'] == k][0]
    TGT.update(key=k, year=int(x['year']), flip=True)
    NS['_O37_SCACHE'].clear()
    with contextlib.redirect_stdout(io.StringIO()):
        b2 = int(round(EV(p, Y) / FNUM))
    TGT['flip'] = False
    NS['_O37_SCACHE'].clear()
    FLIPS.append(dict(key=k, name=x['name'], year=x['year'], g=x['g'], thr=x['thr'],
                      delivered=x['delivered'], board=BOARD[k], flipped=b2, delta=b2 - BOARD[k],
                      direction='loses delivered' if x['delivered'] else 'gains delivered'))
NS['o32_delivered'] = orig
NS['_O37_SCACHE'].clear()
movers = [f for f in FLIPS if f['delta'] != 0]
P('   rows tested: %d   ·   rows whose price MOVES when the delivered verdict flips: %d'
  % (len(FLIPS), len(movers)))
if movers:
    P('   total board points at stake across them: %d   ·   worst single row: %d'
      % (sum(abs(f['delta']) for f in movers), max(abs(f['delta']) for f in movers)))
    P()
    P('   %-24s %6s %6s %7s %-18s %8s %9s %8s'
      % ('row', 'year', 'games', 'thresh', 'flip direction', 'board', 'flipped', 'delta'))
    for f in sorted(movers, key=lambda z: -abs(z['delta']))[:15]:
        P('   %-24s %6d %6.1f %7.2f %-18s %8d %9d %+8d'
          % (f['name'][:24], f['year'], f['g'], f['thr'], f['direction'], f['board'],
             f['flipped'], f['delta']))
else:
    P('   NO ROW MOVES. That is the result and it is reported as such.')
P()
P('   Rows that do not move are rows whose accumulated clock was already zero for another reason, or')
P('   whose fade was not reaching them anyway. The census counts the population at the cliff; this')
P('   table prices only the part of it the cliff actually touches.')
P()

json.dump(dict(partA=dict(n_ret=len(RET), n_sat=len(SAT), n_nev=len(NEV),
                          V_sat=V_SAT, V_never=V_NEV, games=A1, margin=A2, threshold=A3,
                          step_separable=bool(sep), margin_flat=bool(flat)),
               partB=dict(n_near=len(keys), n_flip_down=len(fd), n_flip_up=len(fu),
                          fE=NS['M3_FE'], threshold_now=10.0 * NS['M3_FE'],
                          tested=len(FLIPS), movers=len(movers),
                          points=sum(abs(f['delta']) for f in movers),
                          rows=sorted(movers, key=lambda z: -abs(z['delta']))[:30]),
               board_total=sum(BOARD.values())),
          open(os.path.join(HERE, 'FOLLOWUP_F2.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'FOLLOWUP_F2_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FOLLOWUP_F2.json and FOLLOWUP_F2_out.txt')
