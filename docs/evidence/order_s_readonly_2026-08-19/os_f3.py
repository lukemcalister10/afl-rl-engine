#!/usr/bin/env python3
"""ORDER S READ-ONLY — F3. THE COMBINED-TAKE CALIBRATION.

THE OWNER'S REFRAME, RECORDED AS HIS AND NOT AS THIS SEAT'S: split collection across mechanisms is
NOT a defect; the defect is an uncalibrated TOTAL. That supersedes PACKET_SRO.md sections 16 and 18,
which treated double-pricing as a defect in itself. The supersession is recorded, not quietly applied.

NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NO BOARD IS BUILT. NOTHING IS ADOPTED AND NO FIX IS
PROPOSED.

THE TWO POPULATIONS, carried over unchanged from PACKET_SRO.md:
  A · the rows where the D8 staleness cap BINDS and the sitter fade is below 1  (the double-priced)
  B · the stale(1) rows carrying D_final == 1                                    (the zero-priced)

THE TAKE, per row, on the engine's own legs:
  absence_take = ( a_fade + a_D8 ) / ( board + a_fade + a_D8 )
The ORDER P charge is NOT in the numerator: it prices production against a bar, not absence. The
total including the charge is printed beside it so both readings are visible.

THE MEASURED COST OF THE ABSENCE FACT comes from F1 section 7 — this seat's own re-measurement of
the washout evidence on the house ruler, with an interval. THE WIRED SCHEDULE IS NEVER READ BACK:
that would be circular.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_f3.py
"""
import json, math, os, sys, io, contextlib, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import os_lib as SL                                                          # noqa: E402

Y = 2026
L = []


def P(s=''):
    print(s); L.append(str(s))


F1 = json.load(open(os.path.join(HERE, 'FOLLOWUP_F1.json')))
DC = {int(k): v for k, v in F1['dcurve'].items()}

NS = SL.load(RL_O37='1')
NS['_REC'] = SL.install_recorder(NS)
MA = NS['_MA']
FNUM = json.load(open(SL.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
EV = NS['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, Y)
ROWS = {p['key']: SL.assemble(NS, p, Y) for p in MA.players}
BOARD = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        BOARD[p['key']] = int(round(EV(p, Y) / FNUM))

P('=' * 118)
P('ORDER S READ-ONLY — F3. THE COMBINED-TAKE CALIBRATION, ON THE OWNER\'S REFRAME.')
P('=' * 118)
P('THE OWNER\'S WORDS, RECORDED AS HIS: split collection across mechanisms is NOT a defect; the')
P('defect is an uncalibrated TOTAL. THAT SUPERSEDES PACKET_SRO.md sections 16 and 18, which treated')
P('the double-pricing as a defect in itself. This seat records the supersession rather than quietly')
P('applying it.')
P()
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NOTHING IS ADOPTED. NO FIX IS')
P('PROPOSED. board total (numeraire): %d over %d rows.' % (sum(BOARD.values()), len(BOARD)))
P()

# ---- the D8 counterfactual -----------------------------------------------------------------------------
g0 = NS['_staleness_grade']
NS['_staleness_grade'] = lambda p, Yv, pos, _o=g0: 1.0
with contextlib.redirect_stdout(io.StringIO()):
    NOD8 = {}
    for p in MA.players:
        NS['_O37_SCACHE'].clear()
        NOD8[p['key']] = int(round(EV(p, Y) / FNUM))
NS['_staleness_grade'] = g0
NS['_O37_SCACHE'].clear()
D8 = {k: NOD8[k] - BOARD[k] for k in BOARD}


def gy(p, yy):
    return sum(float(x['games'] or 0) for x in (p.get('scoring') or []) if int(x['year']) == yy)


POP = [p for p in MA.players if ROWS[p['key']] is not None and ROWS[p['key']].get('price') is not None]
CAREER = {p['key']: NS['pv_games'](p, Y) for p in POP}
A = [p for p in POP if D8[p['key']] != 0 and ROWS[p['key']]['D_final'] < 1.0 - 1e-12]
B = [p for p in POP if CAREER[p['key']] > 0 and gy(p, Y) <= 0
     and ROWS[p['key']]['D_final'] >= 1.0 - 1e-12]

P('-' * 118)
P('1 · THE TWO POPULATIONS, RECOVERED FROM THE ENGINE RATHER THAN CARRIED IN AS NUMBERS')
P('-' * 118)
P('   A · the D8 cap BINDS (the counterfactual moves the row) AND the sitter fade is below 1: %d rows'
  % len(A))
P('   B · career games > 0, zero games in %d, and the sitter fade is exactly 1.000: %d rows' % (Y, len(B)))
P('   PACKET_SRO.md reported 8 and 19. Recovered here: %d and %d.' % (len(A), len(B)))
P()

# ---- the measured cost ---------------------------------------------------------------------------------
P('-' * 118)
P('2 · THE MEASURED COST OF THE ABSENCE FACT — F1 SECTION 7, NOT THE WIRED SCHEDULE')
P('-' * 118)
P('   D_measured(c) = E[value from depth c onward / v0 | zero games in every season to depth c-1]')
P('   over E[value from depth 1 onward / v0] on the whole cohort, house S4 ruler, entry year %d or'
  % F1['entry_cut'])
P('   earlier, %d-draw bootstrap. Depth c = 2 means ONE unplayed season.' % F1['boot'])
P()
P('   %-10s %8s %12s %14s %-26s' % ('depth c', 'n', 'D_measured', 'cost 1 - D', '90% CI of the cost'))
for c in sorted(DC):
    d = DC[c]
    P('   %-10d %8d %12.4f %14.4f [%+10.4f, %+10.4f]%s'
      % (c, d['n'], d['D'], d['cost'], d['cost_ci'][0], d['cost_ci'][1],
         ' THIN' if d['n'] < 25 else ''))
P()
P('   FALSIFIER F3-P4 — is the measured cost materially above zero from depth 2 on, and')
P('   indistinguishable from zero at depth 1 or below?')
c2 = DC.get(2)
P('     at depth 2 (one unplayed season) the cost is %.4f with a 90%% CI of [%.4f, %.4f].'
  % (c2['cost'], c2['cost_ci'][0], c2['cost_ci'][1]))
P('     zero is %s that interval.' % ('INSIDE' if c2['cost_ci'][0] <= 0 <= c2['cost_ci'][1] else 'OUTSIDE'))
P('     At depth 1 the cost is ZERO BY CONSTRUCTION — depth 1 is the normaliser. The measurement')
P('     cannot speak about depth 1 and this seat does not pretend it can. What it CAN say is that')
P('     the FIRST unplayed season already costs %.1f%% of delivered value.' % (100 * c2['cost']))
P('     F3-P4 verdict: %s' % ('the first-season cost is separable from zero — the prediction HOLDS'
                              if c2['cost_ci'][0] > 0 else 'not separable from zero — F3-P4 FIRED'))
P()


def cost_at(cu):
    """The measured cost at a continuous unplayed depth, on the engine's OWN interpolation rule:
    log-linear between integer depths, 1.0 at or below depth 1, flat from the deepest scored depth."""
    ks = sorted(DC)
    if cu <= 1.0:
        return 0.0, (0.0, 0.0)
    if cu >= ks[-1]:
        d = DC[ks[-1]]
        return d['cost'], tuple(d['cost_ci'])
    n = int(math.floor(cu)); f = cu - n
    if n not in DC:
        n = min(ks)
    d0 = DC.get(n, DC[ks[0]]); d1 = DC.get(n + 1, DC[ks[-1]])
    lo0, hi0 = d0['D'], d1['D']
    D = math.exp((1 - f) * math.log(max(1e-9, lo0)) + f * math.log(max(1e-9, hi0)))
    c0 = 1 - D
    a = 1 - math.exp((1 - f) * math.log(max(1e-9, 1 - d0['cost_ci'][1])) + f * math.log(max(1e-9, 1 - d1['cost_ci'][1])))
    b = 1 - math.exp((1 - f) * math.log(max(1e-9, 1 - d0['cost_ci'][0])) + f * math.log(max(1e-9, 1 - d1['cost_ci'][0])))
    return c0, (min(a, b), max(a, b))


# ---- population A --------------------------------------------------------------------------------------
def take(p):
    r = ROWS[p['key']]
    fade = r['a_fade_total'] / FNUM
    d8 = float(D8[p['key']])
    chg = r['a_charge'] / FNUM
    base = BOARD[p['key']] + fade + d8
    return dict(key=p['key'], name=p.get('player'), board=BOARD[p['key']], fade=fade, d8=d8,
                chg=chg, cu=r['cu'], D=r['D_final'], g=CAREER[p['key']],
                absence_take=(fade + d8) / base if base > 0 else float('nan'),
                total_take=(fade + d8 + chg) / (base + chg) if (base + chg) > 0 else float('nan'))


def verdict(t, lo, hi):
    if math.isnan(t):
        return 'not scored'
    if t < lo:
        return 'UNDERSHOOTS'
    if t > hi:
        return 'OVERSHOOTS'
    return 'APPROXIMATES'


P('-' * 118)
P('3 · POPULATION A — THE DOUBLE-PRICED ROWS, ROW BY ROW')
P('-' * 118)
P('   absence_take is (fade + D8 cap) over the row\'s absence-free price. It is compared against the')
P('   measured cost at that row\'s OWN unplayed depth. The charge column is printed but is NOT in the')
P('   numerator, because it prices production against a bar and not absence.')
P()
P('   %-22s %6s %6s %7s %7s %7s %8s %9s %-26s %-13s'
  % ('row', 'g', 'c_u', 'fade', 'D8', 'charge', 'board', 'abs take', 'measured cost 90% CI', 'verdict'))
AJ = []
for p in sorted(A, key=lambda z: -BOARD[z['key']]):
    t = take(p)
    c, (lo, hi) = cost_at(t['cu'])
    v = verdict(t['absence_take'], lo, hi)
    t.update(cost=c, cost_ci=[lo, hi], verdict=v)
    AJ.append(t)
    P('   %-22s %6.0f %6.2f %7.1f %7.0f %7.1f %8d %9.4f [%+10.4f, %+10.4f] %-13s'
      % (t['name'][:22], t['g'], t['cu'], t['fade'], t['d8'], t['chg'], t['board'],
         t['absence_take'], lo, hi, v))
cnt = collections.Counter(t['verdict'] for t in AJ)
P()
P('   POPULATION A VERDICT: %s' % ', '.join('%s %d' % (k, v) for k, v in cnt.most_common()))
P('   F3-P2 — predicted APPROXIMATE or UNDERSHOOT rather than OVERSHOOT. %s'
  % ('the population OVERSHOOTS — F3-P2 FIRED' if cnt.get('OVERSHOOTS', 0) > len(AJ) / 2
     else 'the population does NOT overshoot on balance — F3-P2 did not fire'))
big = max(AJ, key=lambda z: z['d8']) if AJ else None
if big:
    P('   F3-P3 — the one row where both legs are large, reported individually as preregistered:')
    P('     %-22s fade %.1f + D8 %.0f = %.1f board points on an absence-free price of %.0f;'
      % (big['name'], big['fade'], big['d8'], big['fade'] + big['d8'],
         big['board'] + big['fade'] + big['d8']))
    P('     absence take %.4f against a measured cost of %.4f [%.4f, %.4f] at c_u %.2f — %s.'
      % (big['absence_take'], big['cost'], big['cost_ci'][0], big['cost_ci'][1], big['cu'], big['verdict']))
P()

# ---- population B --------------------------------------------------------------------------------------
P('-' * 118)
P('4 · POPULATION B — THE ZERO-PRICED ROWS')
P('-' * 118)
P('   These rows have played NO games this season and carry a sitter fade of exactly 1.000, so the')
P('   absence take is zero by construction. The question is what the missed season is measured to be')
P('   worth. TWO yardsticks are printed because they answer two different questions and merging them')
P('   would be dishonest:')
P()
P('     (i)  the cost at the row\'s OWN unplayed depth c_u. For every one of these rows c_u <= 1, so')
P('          the measured curve says ZERO — the same answer the wired schedule gives. On its own')
P('          clock the row is NOT being under-charged.')
P('     (ii) the cost of ONE unplayed season, %.4f [%.4f, %.4f] from section 2. That is what the'
  % (c2['cost'], c2['cost_ci'][0], c2['cost_ci'][1]))
P('          missed season would cost IF THE CLOCK COUNTED IT. It does not, because the row\'s earlier')
P('          played seasons and his last delivered season have already reset and credited it away.')
P()
P('   %-24s %6s %6s %7s %8s %9s %11s %-13s'
  % ('row', 'g', 'c_u', 'fade', 'board', 'abs take', 'cost (ii)', 'verdict on (ii)'))
BJ = []
for p in sorted(B, key=lambda z: -BOARD[z['key']]):
    t = take(p)
    v = verdict(t['absence_take'], c2['cost_ci'][0], c2['cost_ci'][1])
    t.update(cost=c2['cost'], cost_ci=c2['cost_ci'], verdict=v)
    BJ.append(t)
for t in BJ[:20]:
    P('   %-24s %6.0f %6.2f %7.1f %8d %9.4f %11.4f %-13s'
      % (t['name'][:24], t['g'], t['cu'], t['fade'], t['board'], t['absence_take'],
         t['cost'], t['verdict']))
if len(BJ) > 20:
    P('   ... and %d more, all with an absence take of zero.' % (len(BJ) - 20))
cntB = collections.Counter(t['verdict'] for t in BJ)
P()
P('   POPULATION B VERDICT against yardstick (ii): %s'
  % ', '.join('%s %d' % (k, v) for k, v in cntB.most_common()))
P('   F3-P1 — predicted the 19 rows UNDERSHOOT by essentially the whole measured cost. %s'
  % ('confirmed — %d of %d undershoot' % (cntB.get('UNDERSHOOTS', 0), len(BJ))
     if cntB.get('UNDERSHOOTS', 0) == len(BJ) else 'NOT confirmed — F3-P1 FIRED'))
P()
gap = sum(t['cost'] * (t['board'] / max(1e-9, 1 - t['cost'])) for t in BJ)
P('   THE SIZE OF THE GAP, on yardstick (ii). If the missed season were charged at the measured cost')
P('   of one unplayed season, these %d rows would carry about %.0f board points less between them,'
  % (len(BJ), gap))
P('   against a board of %d. THAT IS AN ARITHMETIC CONSEQUENCE OF THE MEASUREMENT AND NOT A PROPOSAL:'
  % sum(BOARD.values()))
P('   this seat is not saying the clock should count that season. It is saying what the number is.')
P()

# ---- the whole-board reading -----------------------------------------------------------------------------
P('-' * 118)
P('5 · THE SAME CALIBRATION ON EVERY ROW THE FADE ACTUALLY REACHES')
P('-' * 118)
P('   The two populations above are the edge cases. This is the middle: every board row whose sitter')
P('   fade is below 1, so the absence take is not trivially zero.')
P()
MID = [p for p in POP if ROWS[p['key']]['D_final'] < 1.0 - 1e-12 and CAREER[p['key']] > 0]
P('   %-12s %6s %11s %11s %-26s %-14s' % ('c_u band', 'rows', 'med take', 'measured', '90% CI', 'verdict on median'))
MJ = {}
for lo, hi in ((1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 99.0)):
    sel = [take(p) for p in MID if lo <= ROWS[p['key']]['cu'] < hi]
    if not sel:
        continue
    med = float(np.median([t['absence_take'] for t in sel]))
    mid = (lo + hi) / 2 if hi < 99 else 4.5
    c, (l_, h_) = cost_at(min(mid, 5.0))
    v = verdict(med, l_, h_)
    MJ['%.0f-%.0f' % (lo, hi)] = dict(n=len(sel), med=med, cost=c, ci=[l_, h_], verdict=v)
    P('   %-12s %6d %11.4f %11.4f [%+10.4f, %+10.4f] %-14s'
      % ('%.0f-%.0f' % (lo, min(hi, 9)), len(sel), med, c, l_, h_, v))
P()
P('   THIS IS THE ANSWER TO THE OWNER\'S QUESTION IN ONE TABLE. Where the fade reaches a row at all,')
P('   the combined take is compared against the measured total cost of the absence at that depth.')
P()

# ---- 6 · the structural ceiling -------------------------------------------------------------------------
P('-' * 118)
P('6 · THE DENOMINATOR PROBLEM, AND THE STRUCTURAL CEILING — READ THIS BEFORE READING SECTION 5')
P('-' * 118)
P('   THE TWO NUMBERS COMPARED ABOVE HAVE DIFFERENT DENOMINATORS AND THAT MUST BE SAID PLAINLY.')
P('   The measured cost is a fraction of DELIVERED VALUE. The absence take is a fraction of BOARD')
P('   PRICE. A row\'s price already carries a production leg that is low for its own reasons, so the')
P('   two are not the same base and the section 5 gap is NOT simply "the dial is set too low".')
P()
P('   THE QUESTION THAT MAKES IT MEANINGFUL: what is the MOST the absence mechanisms could take on')
P('   this row, at any setting, given where they sit in the price identity? The sitter fade multiplies')
P('   only the (1 - rho) share of the pedigree leg. Drive D to zero and that whole share goes; nothing')
P('   more can. Add the D8 cap at its measured size and that is the ceiling.')
P()
P('   %-12s %6s %12s %12s %12s %-24s'
  % ('c_u band', 'rows', 'med take', 'med CEILING', 'measured', '90% CI of measured'))
CEIL = {}
for lo, hi in ((1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 99.0)):
    sel = [p for p in MID if lo <= ROWS[p['key']]['cu'] < hi]
    if not sel:
        continue
    cs, ts = [], []
    for p in sel:
        r = ROWS[p['key']]
        cs_ = r['a_fade_total'] / max(1e-9, r['D_final'] and (1.0 - r['D_final']) or 1.0)
        # the whole D-sensitive share, in board points: f*(1-rho)*ped
        share = (r['a_fade_total'] / (1.0 - r['D_final'])) / FNUM if r['D_final'] < 1 else 0.0
        d8 = float(D8[p['key']])
        base = BOARD[p['key']] + r['a_fade_total'] / FNUM + d8
        cs.append((share + d8) / base if base > 0 else float('nan'))
        ts.append(take(p)['absence_take'])
    mid = (lo + hi) / 2 if hi < 99 else 4.5
    c, (l_, h_) = cost_at(min(mid, 5.0))
    CEIL['%.0f-%.0f' % (lo, hi)] = dict(n=len(sel), med_take=float(np.median(ts)),
                                        med_ceiling=float(np.median(cs)), cost=c, ci=[l_, h_])
    P('   %-12s %6d %12.4f %12.4f %12.4f [%+10.4f, %+10.4f]'
      % ('%.0f-%.0f' % (lo, min(hi, 9)), len(sel), np.median(ts), np.median(cs), c, l_, h_))
P()
below = [k for k, v in CEIL.items() if v['med_ceiling'] < v['ci'][0]]
P('   BANDS WHERE EVEN THE CEILING SITS BELOW THE MEASURED COST: %s'
  % (', '.join(below) if below else 'none'))
P()
if below:
    P('   THAT IS A STRUCTURAL FINDING, NOT A DIAL FINDING. In those bands no setting of the sitter')
    P('   fade and no size of the D8 cap can collect the measured cost of the absence, because the')
    P('   collectors act on a share of the price that is smaller than the cost is. Scaling the split,')
    P('   which is the remedy the owner\'s reframe points at when the total overshoots, cannot close a')
    P('   gap of this kind. THIS SEAT PROPOSES NOTHING; it reports that the lever and the gap are')
    P('   different sizes.')
else:
    P('   In every band the ceiling is at or above the measured cost, so the gap in section 5 is a')
    P('   question of SETTING and not of structure.')
P()
P('   AND THE LIMITATION THAT CUTS THE OTHER WAY, stated as plainly: a row whose absence has already')
P('   depressed his PRODUCTION leg has paid for the absence somewhere the attributions above do not')
P('   count, because rho and the production estimate are not absence mechanisms and were not read as')
P('   such. The section 5 gap is therefore an UPPER bound on the shortfall, not a point estimate.')
P()

json.dump(dict(popA=AJ, popB=BJ[:60], nA=len(A), nB=len(B), mid=MJ, ceiling=CEIL,
               dcurve={str(k): v for k, v in DC.items()},
               verdictA=dict(cnt), verdictB=dict(cntB), gapB=gap,
               board_total=sum(BOARD.values())),
          open(os.path.join(HERE, 'FOLLOWUP_F3.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'FOLLOWUP_F3_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FOLLOWUP_F3.json and FOLLOWUP_F3_out.txt')
