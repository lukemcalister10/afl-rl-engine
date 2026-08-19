#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE I1 CREDIT CURVE: GUARDED vs RAW, PRICED SIDE BY SIDE. NOTHING ADOPTED.

WHY THIS EXISTS. F1 published TWO readings of the same measurement — the GUARDED isotonic curve and
the RAW per-games cells — and their intervals overlap heavily. Which one the assembly wired was a
SEAT CALL and was never put to the owner. The owner has since flagged the rows the guarded curve
marks down hardest as looking harsh. So both readings are built and the choice is his, on numbers.

THIS FILE REPORTS, IT DOES NOT CHOOSE:
  1. the two curves side by side, with F1's own intervals and the inversions named;
  2. the board total under each;
  3. the top-ten I1 movers under BOTH curves, side by side (consequences, never targets);
  4. THE MID-SEASON TIMING CENSUS — the curve was measured on COMPLETED seasons and is applied to
     in-progress rookies at fE. A census of how many I1-moved rows are in-progress first-years, and
     what their credit would be at their CURRENT games versus at plausibly-higher end-of-season
     games. A CENSUS OF THE EXPOSURE, NOT A PROJECTION OF ANY PLAYER'S SEASON.

NO ENGINE RUN HERE — pure reads over boards already built.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
FE = 0.92                      # the in-progress season fraction the engine is priced at

GUARD = [0.0, 0.1286875208353465, 0.23834489196711883, 0.23834489196711883, 0.23834489196711883,
         0.2455042373957035, 0.38568558243890977, 0.38568558243890977, 0.45188866847720316,
         0.8878514765964253, 0.8878514765964253, 1.0]
RAWC = [0.0, 0.1286875208353465, 0.4706058223361502, 0.4706058223361502, 0.4706058223361502,
        0.4706058223361502, 0.5711028628770571, 0.5711028628770571, 0.5711028628770571,
        1.0, 1.0, 1.0]
F1 = json.load(open(os.path.join(REPO, 'docs/evidence/order_s_readonly_2026-08-19/FOLLOWUP_F1.json')))
L = []


def P(s=''):
    print(s); L.append(str(s))


def board(tag):
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (ASM, tag)
    if not os.path.exists(p):
        return None, None
    d = json.load(open(p))
    return ({r['key']: r for r in d['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


BASE, mB = board('V750_L4SD')          # the board I1 sits on top of
GRD, mG = board('V750_L5A')            # + I1 guarded
CAND, mC = board('V755_CAND')          # the candidate (guarded, full stack)
RAWB, mR = board('V755_RAW')           # the candidate with I1 raw
RAW2, mR2 = board('V755_RAW2')
IDP, mIDP = board('IDENT_P')           # every ORDER 41 dial off -> must be 374d4e44

P('=' * 122)
P('THE I1 CREDIT CURVE — GUARDED vs RAW, PRICED SIDE BY SIDE. NOTHING IS ADOPTED.')
P('=' * 122)
P()
P('THE TWO READINGS OF THE SAME MEASUREMENT (FOLLOWUP_F1.json). CIs are F1\'s own.')
P('  %-4s %-12s %-12s %-26s %-8s %s' % ('g', 'GUARDED', 'RAW cell', 'F1 90% CI on the raw cell',
                                        'n', 'note'))
order = [str(i) for i in range(11)] + ['11+']
for i, k in enumerate(order):
    c = F1['curve'][k]
    ci = c['ci']
    note = ''
    if k in ('3', '7', '10'):
        note = 'raw cell INVERTS here'
    if k == '9':
        note = 'raw cell reads 1.03200 — CAPPED at 1.0 (structural)'
    P('  %-4s %-12.5f %-12.5f [%+.3f, %+.3f]%s %-8s %s'
      % (k, GUARD[i], RAWC[i], ci[0], ci[1], ' ' * 6, c['n'], note))
P()
P('HOW THE RAW READING WAS MADE MONOTONE, AND WHAT WAS NOT INVENTED.')
P('  The raw cells INVERT at g = 3, 7 and 10 — a 3-game season would credit LESS than a 2-game one,')
P('  which is exactly what the guard exists to remove. The raw variant is monotonised by RUNNING')
P('  MAXIMUM, deliberately NOT by the pool-adjacent-violators guard: PAVA AVERAGES the violating')
P('  cells and therefore produces numbers that are not any measured cell (the guarded 0.23834 is a')
P('  pooled value, not an F1 reading). A running maximum carries only MEASURED CELL VALUES forward.')
P('  THE ONE NON-CELL NUMBER IS THE CAP AT 1.0 at g=9, where the raw cell reads 1.03200. That cap is')
P('  STRUCTURAL AND PRE-EXISTING — the wired law and the charter both cap a season at one full played')
P('  season — so it is applied, not invented. Nothing else was chosen.')
P()
P('  READ THE TWO COLUMNS: the raw reading is UNIFORMLY MORE GENEROUS from 2 games up. At 2 games it')
P('  credits 0.471 against the guarded 0.238; at 5 games 0.471 against 0.246; at 9 games 1.000')
P('  against 0.888. The guarded curve is the harsher of the two everywhere they differ.')
P()

# ---- boards ---------------------------------------------------------------------------------------
P('=' * 122)
P('THE BOARDS')
P('=' * 122)
TOT = {}
for nm, B, m in (('L4_SD (the board I1 sits on)', BASE, mB),
                 ('+ I1 GUARDED  (V750_L5A)', GRD, mG),
                 ('THE CANDIDATE (guarded, full stack)', CAND, mC),
                 ('THE RAW VARIANT (full stack, I1 raw)', RAWB, mR),
                 ('the raw variant, determinism repeat', RAW2, mR2),
                 ('ORDER P identity (every ORDER 41 dial OFF)', IDP, mIDP)):
    if B is None:
        P('  %-38s NO BOARD' % nm); continue
    t = sum(r['v'] for r in B.values())
    TOT[nm] = t
    P('  %-38s %s  %s' % (nm, m, '{:>9,}'.format(t)))
P()
if IDP:
    P('  DIAL-OFF IDENTITY: with every ORDER 41 dial off — the new RL_O41_CREDITFORM sub-dial'
      ' included — the board is %s %s'
      % (mIDP, 'and reproduces ORDER P 374d4e44 BYTE-EXACT. The raw form is inert when not selected.'
         if mIDP == '374d4e44' else '*** WHICH IS NOT 374d4e44 ***'))
    P('  The candidate and the raw variant differ by RL_O41_CREDITFORM ALONE — every other dial on the'
      ' two lines is identical, so the delta below is the curve choice and nothing else.')
if RAWB and RAW2:
    P('  DETERMINISM (raw variant, x2): %s'
      % ('IDENTICAL — %s' % mR if mR == mR2 else '*** FIRED *** %s vs %s' % (mR, mR2)))
if CAND and RAWB:
    d = sum(r['v'] for r in RAWB.values()) - sum(r['v'] for r in CAND.values())
    P()
    P('  *** BOARD TOTAL DELTA, RAW vs GUARDED: {:+,} board points ***'.format(d))
    mv = [k for k in CAND if CAND[k]['v'] != RAWB[k]['v']]
    up = sum(1 for k in mv if RAWB[k]['v'] > CAND[k]['v'])
    P('      %d rows differ; %d up, %d down under the raw reading.' % (len(mv), up, len(mv) - up))
P()

# ---- the I1 movers, both curves --------------------------------------------------------------------
P('=' * 122)
P('THE I1 MOVERS — TOP TEN BY THE GUARDED CURVE, WITH THE RAW READING BESIDE THEM')
P('These are CONSEQUENCES, never targets. No named row gates anything in this build.')
P('=' * 122)
STORE = {x['key']: x for x in json.load(open(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')))}
rows = []
if BASE and GRD and CAND and RAWB:
    i1mv = [k for k in BASE if BASE[k]['v'] != GRD[k]['v']]
    for k in i1mv:
        rows.append(dict(key=k, name=GRD[k].get('name'), age=GRD[k].get('age'),
                         base=BASE[k]['v'], guarded=GRD[k]['v'],
                         d_guard=GRD[k]['v'] - BASE[k]['v'],
                         cand=CAND[k]['v'], raw=RAWB[k]['v'],
                         d_raw_vs_cand=RAWB[k]['v'] - CAND[k]['v']))
    rows.sort(key=lambda r: r['d_guard'])
    P('  %-24s %4s %8s %9s %9s %10s %9s %9s'
      % ('player', 'age', 'before', 'guarded', 'I1 move', 'candidate', 'RAW', 'raw-cand'))
    for r in rows[:10]:
        P('  %-24s %4s %8d %9d %+9d %10d %9d %+9d'
          % (str(r['name'])[:24], r['age'], r['base'], r['guarded'], r['d_guard'],
             r['cand'], r['raw'], r['d_raw_vs_cand']))
    P()
    P('  I1 moved %d rows in total on the guarded curve.' % len(i1mv))
P()

# ---- the mid-season timing census -------------------------------------------------------------------
P('=' * 122)
P('THE MID-SEASON TIMING CENSUS — A CENSUS OF EXPOSURE, NOT A PROJECTION OF ANY SEASON')
P('=' * 122)
P('THE ISSUE, STATED PLAINLY. F1 measured this curve on COMPLETED seasons. The engine applies it to')
P('the 2026 season while that season is IN PROGRESS, at fE = %.2f. A first-year who has played a few' % FE)
P('games so far is being credited as though a few games were his whole season. If he goes on to play')
P('more, his credit rises steeply — the curve is at its steepest exactly where these rows sit.')
P('NOTHING IS PROJECTED BELOW. The census asks only: how many I1-moved rows are exposed to this, and')
P('how much would their credit move if the same row finished on a higher games count.')
P()


def cred(g, tab):
    g = float(g)
    if g <= 0:
        return 0.0
    if g >= 11:
        return 1.0
    n = int(g); f = g - n
    c0 = tab[n]; c1 = tab[min(n + 1, 11)]
    return c0 if f <= 0 else (1 - f) * c0 + f * c1


if rows:
    exposed = []
    for r in rows:
        s = STORE.get(r['key'])
        if not s:
            continue
        ss = {x['year']: (x.get('games') or 0) for x in (s.get('scoring') or [])}
        g26 = float(ss.get(2026) or 0)
        played_before = [y for y, g in ss.items() if y < 2026 and g > 0]
        first_year = (len(played_before) == 0)
        if g26 > 0 and first_year:
            exposed.append((r, g26))
    P('  I1-moved rows: %d' % len(rows))
    P('  of those, IN-PROGRESS FIRST-YEARS (games in 2026, none in any earlier season): %d'
      % len(exposed))
    P()
    if exposed:
        P('  %-24s %4s %7s %9s %9s   %s'
          % ('player', 'age', 'g 2026', 'cred now', 'cred @11g', 'credit still to come'))
        for r, g in sorted(exposed, key=lambda z: z[0]['d_guard'])[:15]:
            now = cred(g, GUARD); full = 1.0
            P('  %-24s %4s %7.0f %9.4f %9.4f   %+.4f'
              % (str(r['name'])[:24], r['age'], g, now, full, full - now))
        P()
        band = {}
        for r, g in exposed:
            b = ('1-2' if g <= 2 else '3-5' if g <= 5 else '6-8' if g <= 8 else '9-10' if g <= 10
                 else '11+')
            band[b] = band.get(b, 0) + 1
        P('  the exposed rows by games so far: '
          + ' · '.join('%s: %d' % (k, band[k]) for k in ('1-2', '3-5', '6-8', '9-10', '11+')
                       if k in band))
        P()
        P('  READ THIS AS THE EXPOSURE IT IS: every one of these rows sits BELOW 11 games today, so')
        P('  every one of them would gain credit — and price — if his season finished higher. The')
        P('  guarded curve makes that gap wider than the raw curve does, because it is the harsher')
        P('  reading at every games count where the two differ.')
    else:
        P('  No I1-moved row is an in-progress first-year. The timing exposure is nil on this board.')

json.dump(dict(totals=TOT, guarded=GUARD, raw=RAWC,
               md5=dict(cand=mC, raw=mR, raw2=mR2, identp=mIDP, l5a=mG, l4sd=mB),
               movers=rows[:40] if rows else []),
          open(os.path.join(HERE, 'CREDIT_FORMS.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CREDIT_FORMS_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: CREDIT_FORMS.json · CREDIT_FORMS_out.txt')
