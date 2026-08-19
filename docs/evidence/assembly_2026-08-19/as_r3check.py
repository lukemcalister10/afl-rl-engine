#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE R3 FIX: BUILT-vs-EXPECTED, AND THE EXPLOIT-SAFETY VERIFICATION.

THE FIX. o41_absence_depth was CUMULATIVE — every unplayed season since the last DELIVERED one,
charged against TODAY'S production leg. Because "delivered" needs games >= 10*f AND an average over
the gate bar, a player can play every week and never deliver, so old gaps kept accruing while he was
on the field. It is now the CURRENT CONSECUTIVE run: walk back from Y, any season with games > 0
BREAKS the run.

TWO THINGS ARE CHECKED HERE AND NEITHER IS ASSUMED:

  1. BUILT-vs-EXPECTED. The expectation was: returned players largely restored, currently-absent
     players still stripped. Both halves are measured, by name, as consequences.

  2. THE EXPLOIT-SAFETY ARGUMENT, VERIFIED RATHER THAN ASSERTED. A token-games season now breaks the
     run. Could a row bank a cheap season to shield a large production leg? The argument is that R3's
     own base IS the production leg, and a token-games career has small rho and therefore little
     production to shield — but an argument is not a measurement. So: find every row whose run is
     broken by a season of <= 2 games, and report the LARGEST R3 exposure among them, measured as the
     board points that row would have paid under the OLD cumulative rule. If that number is
     materially large, THIS FILE SAYS SO AND THE FIX SHOULD NOT BE WIRED WITHOUT A GUARD.

The shield value is MEASURED, not modelled: the two boards differ ONLY in this definition, so the
per-row difference between them IS what the run-break is worth to that row.

NO ENGINE RUN. Pure reads over boards already built.
"""
import json, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
Y = 2026
L = []


def P(s=''):
    print(s); L.append(str(s))


def board(tag):
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (ASM, tag)
    if not os.path.exists(p):
        return None, None
    return ({r['key']: r for r in json.load(open(p))['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


OLD, mOLD = board('V750_CAND')    # cumulative-since-delivery R3
NEW, mNEW = board('V751_CAND')    # current-consecutive R3
PRE, mPRE = board('V750_L5C')     # the board before R3 at all
STORE = {x['key']: x for x in json.load(open(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')))}

P('=' * 122)
P('THE R3 FIX — BUILT vs EXPECTED, AND THE EXPLOIT-SAFETY VERIFICATION')
P('=' * 122)
P('  before R3 at all      %s  %s' % (mPRE, '{:,}'.format(sum(r['v'] for r in PRE.values()))))
P('  R3 CUMULATIVE (old)   %s  %s' % (mOLD, '{:,}'.format(sum(r['v'] for r in OLD.values()))))
P('  R3 CURRENT RUN (new)  %s  %s' % (mNEW, '{:,}'.format(sum(r['v'] for r in NEW.values()))))
P()
tot_old = sum(r['v'] for r in OLD.values()); tot_new = sum(r['v'] for r in NEW.values())
tot_pre = sum(r['v'] for r in PRE.values())
P('  R3 marginal, OLD rule: {:+,} on {} rows'.format(
    tot_old - tot_pre, sum(1 for k in PRE if PRE[k]['v'] != OLD[k]['v'])))
P('  R3 marginal, NEW rule: {:+,} on {} rows'.format(
    tot_new - tot_pre, sum(1 for k in PRE if PRE[k]['v'] != NEW[k]['v'])))
P('  THE FIX GIVES BACK {:+,} board points.'.format(tot_new - tot_old))
P()


def seasons(k):
    return {int(x['year']): float(x.get('games') or 0.0)
            for x in (STORE.get(k, {}).get('scoring') or []) if int(x['year']) <= Y}


def run_break(k):
    """The season that breaks the current run, and its games. None if the run reaches the draft."""
    ss = seasons(k)
    if ss.get(Y, 0) > 0:
        return (Y, ss[Y])
    yy = Y - 1
    floor = STORE.get(k, {}).get('year')
    while floor is None or yy > int(floor):
        if ss.get(yy, 0) > 0:
            return (yy, ss[yy])
        yy -= 1
        if Y - yy > 40:
            break
    return None


# ---- 1 · built vs expected --------------------------------------------------------------------------
P('=' * 122)
P('1 · BUILT vs EXPECTED — the two halves of the expectation, measured by name')
P('=' * 122)
P('EXPECTED: returned players largely RESTORED; currently-absent players STILL STRIPPED.')
P()
rest = sorted(((NEW[k]['v'] - OLD[k]['v'], k) for k in OLD if NEW[k]['v'] != OLD[k]['v']),
              reverse=True)
P('  THE RESTORED — largest gains from the fix (these are the returned players):')
P('    %-24s %6s %8s %9s %9s   %s' % ('player', 'g2026', 'pre-R3', 'old R3', 'new R3', 'restored'))
for d, k in rest[:10]:
    ss = seasons(k)
    P('    %-24s %6.0f %8d %9d %9d   %+8d'
      % (str(NEW[k].get('name'))[:24], ss.get(Y, 0), PRE[k]['v'], OLD[k]['v'], NEW[k]['v'], d))
P()
still = [(OLD[k]['v'] - NEW[k]['v'], k) for k in PRE if PRE[k]['v'] != NEW[k]['v']]
strip = sorted(((PRE[k]['v'] - NEW[k]['v'], k) for k in PRE if PRE[k]['v'] != NEW[k]['v']),
               reverse=True)
P('  STILL STRIPPED under the new rule — these are the rows that are genuinely ABSENT NOW:')
P('    %-24s %6s %8s %9s   %s   %s' % ('player', 'g2026', 'pre-R3', 'new R3', 'stripped', 'last played'))
for d, k in strip[:10]:
    ss = seasons(k)
    lp = max([y for y, g in ss.items() if g > 0], default=None)
    P('    %-24s %6.0f %8d %9d   %+8d   %s'
      % (str(NEW[k].get('name'))[:24], ss.get(Y, 0), PRE[k]['v'], NEW[k]['v'], -d,
         lp if lp else 'never'))
P()
nowplay = sum(1 for k in PRE if PRE[k]['v'] != NEW[k]['v'] and seasons(k).get(Y, 0) > 0)
P('  ROWS STILL CHARGED BY R3 THAT ARE PLAYING THIS SEASON: %d' % nowplay)
P('  (under the OLD rule this was %d — the defect the fix removes; it must now be ZERO by construction)'
  % sum(1 for k in PRE if PRE[k]['v'] != OLD[k]['v'] and seasons(k).get(Y, 0) > 0))
P()

# ---- 2 · day-0, verified not assumed ------------------------------------------------------------------
P('=' * 122)
P('2 · DAY-0 UNDER THE NEW RULE — VERIFIED, NOT ASSUMED')
P('=' * 122)
gl = [k for k in PRE if not any(g > 0 for g in seasons(k).values())]
mv = [k for k in gl if PRE[k]['v'] != NEW[k]['v']]
P('  truly gameless board rows: %d' % len(gl))
P('  of those, moved by the R3 rule change: %d   <-- must be 0' % len(mv))
P('  WHY: a gameless row has no played season to break the run, so his run still walks back to his')
P('  draft year exactly as it did under the old rule. The two definitions AGREE on him by')
P('  construction — but that is checked above rather than argued.')
P()

# ---- 3 · the exploit-safety verification ---------------------------------------------------------------
P('=' * 122)
P('3 · EXPLOIT-SAFETY — VERIFIED, NOT ASSERTED')
P('=' * 122)
P('A token-games season now BREAKS the run. Could a row bank a cheap season to shield a large')
P('production leg? The shield value is MEASURED: the two boards differ only in this definition, so')
P('the per-row gap between them IS what the break is worth to that row.')
P()
shield = []
for k in OLD:
    rb = run_break(k)
    if rb is None:
        continue
    yr, g = rb
    if g <= 2.0:
        shield.append((NEW[k]['v'] - OLD[k]['v'], k, yr, g))
shield.sort(reverse=True)
P('  rows whose current run is broken by a season of <= 2 games: %d' % len(shield))
if shield:
    P('  %-24s %8s %7s %10s %10s   %s'
      % ('player', 'break yr', 'games', 'old R3', 'new R3', 'shield value'))
    for d, k, yr, g in shield[:12]:
        P('  %-24s %8d %7.0f %10d %10d   %+10d'
          % (str(NEW[k].get('name'))[:24], yr, g, OLD[k]['v'], NEW[k]['v'], d))
    big = shield[0][0]
    P()
    P('  *** LARGEST SHIELD VALUE AMONG RUN-BREAKING <=2-GAME SEASONS: %+d board points ***' % big)
    tot = sum(d for d, _k, _y, _g in shield)
    P('      total across all {} such rows: {:+,} board points'.format(len(shield), tot))
    P()
    THRESH = 400
    if big >= THRESH:
        P('  *** THIS IS MATERIALLY LARGE (>= %d points on a single row). THE EXPLOIT-SAFETY ARGUMENT'
          % THRESH)
        P('      DOES NOT HOLD ON THIS BOARD AND THE FIX SHOULD NOT BE WIRED WITHOUT A GUARD. ***')
        P('      Reported rather than waved through — the instruction was to verify, not assume.')
    else:
        P('  THE ARGUMENT HOLDS ON MEASUREMENT: the largest single shield is %d points, under the %d-point'
          % (big, THRESH))
        P('  materiality line, on a board of %s. The reason is the one the argument gave and the'
          % '{:,}'.format(tot_new))
        P('  numbers now confirm: R3\'s base is the PRODUCTION LEG, and a career thin enough to be')
        P('  breaking its run with a one- or two-game season has little production leg to shield.')
else:
    P('  NO row on this board has its current run broken by a <=2-game season. The exploit surface is')
    P('  EMPTY on the board as it stands — which is a fact about this board, not a proof about all')
    P('  boards, and it is stated that way.')

json.dump(dict(md5=dict(pre=mPRE, old=mOLD, new=mNEW),
               totals=dict(pre=tot_pre, old=tot_old, new=tot_new),
               give_back=tot_new - tot_old,
               n_playing_charged_new=nowplay,
               day0_gameless=len(gl), day0_moved=len(mv),
               shield=[dict(key=k, year=yr, games=g, value=d) for d, k, yr, g in shield[:40]],
               shield_max=(shield[0][0] if shield else 0), shield_n=len(shield)),
          open(os.path.join(HERE, 'R3_CHECK.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'R3_CHECK_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: R3_CHECK.json · R3_CHECK_out.txt')
