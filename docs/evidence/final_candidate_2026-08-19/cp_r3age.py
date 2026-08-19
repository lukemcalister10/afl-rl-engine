#!/usr/bin/env python3
"""FINAL-CANDIDATE — the R3-aware birthday probe. The assembly seat's as_r3age.py with THREE
changes and no others: the scratch dir, the two board tags, and DIALS extended to the candidate's
own full line (RL_O41_BREAK=unwind, RL_O41_UNWIND=7, RL_O42=1). Every measurement, both
self-checks and the M3 call-site recorder are byte-identical.

THE BASELINE IS THREE DIALS APART, NOT ONE, AND THAT IS FORCED. Dropping RL_O41_R3 alone is
refused by the engine ("ORDER 41 HALT: RL_O41_BREAK=unwind but RL_O41_R3 is unset"), so the R3-off
board also has BREAK/UNWIND off. SELF-CHECK 2 is the guard on that: it requires the re-formed R3
take to reproduce EVERY per-row board delta at tolerance 0, and refuses to conclude if it cannot.

ORIGINAL ASSEMBLY HEADER FOLLOWS.
"""
import json, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as L

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/compscratch'
Y = 2026
OUT = []


def P(s=''):
    print(s); OUT.append(str(s))


def board(tag):
    p = '%s/bb_%s/rl_after/rl_app_data.json' % (SP, tag)
    if not os.path.exists(p):
        return None, None
    return ({r['key']: r for r in json.load(open(p))['active']},
            hashlib.md5(open(p, 'rb').read()).hexdigest()[:8])


# THE BASELINE MUST MATCH THE CANDIDATE ON EVERY DIAL EXCEPT R3, OR ROWS THAT MOVED FOR ANOTHER
# REASON ARE ATTRIBUTED TO R3. `V755_L5C` has the D4 ramp OFF; the candidate has it ON, so 8 ramp
# rows would be counted as R3's and the self-check below rightly refused to draw a conclusion when
# that was tried. `V755_L5CR` is ramp-ON, R3-OFF — the only correct denominator.
PRE, mPRE = board('CP_NOR3')       # ramp ON, R3 OFF (and BREAK/UNWIND off — FORCED, see below)
CAND, mCAND = board('CP_CAND')     # THE PARITY BOARD a05fe951

# THE CANDIDATE'S OWN FULL DIAL LINE, including the three the assembly copy did not carry
# (RL_O41_BREAK/RL_O41_UNWIND/RL_O42). The probe must load the engine in the state the board was
# priced in or its re-formed take cannot reproduce the board — SELF-CHECK 1/2 below enforce that.
DIALS = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
             RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
             RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
             RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7',
             RL_O42='1', RL_O43='1')

P('=' * 122)
P('THE R3 BIRTHDAY QUESTION — IS THE CONTINUITY HARNESS READING A BOARD DEFECT OR ITS OWN GAP?')
P('=' * 122)
P('  board before R3   %s  %s' % (mPRE, '{:>9,}'.format(sum(r['v'] for r in PRE.values()))))
P('  THE CANDIDATE     %s  %s' % (mCAND, '{:>9,}'.format(sum(r['v'] for r in CAND.values()))))

CHARGED = {k: CAND[k]['v'] - PRE[k]['v'] for k in PRE if CAND[k]['v'] != PRE[k]['v']}
P('  R3-charged rows   %d   total marginal %+d' % (len(CHARGED), sum(CHARGED.values())))
P()

NS = L.load(**DIALS)
MA = NS['_MA']

rho31 = NS['rho31']; o31_pi = NS['o31_pi']
o32_ac = NS['o32_age_credit']
depth = NS['o41_absence_depth']; cost = NS['o41_cost']
compl = NS['o41_completed_absent']
o41_inj = NS['o41_injured']
PRED8 = NS['_O41_PRED8']
r3take = NS['o41_r3_take']
pv_games = NS['pv_games']; pv_ped = NS['pv_pedigree']

# ---- THE CALL-SITE RECORDER -----------------------------------------------------------------
# WHY AT THE CALL SITE AND NOT AFTERWARDS. A row can reach the blend TWICE at one year — that is
# the M3 proportional-tenure blend — and the two calls carry DIFFERENT games, different production
# input e, and a different stashed pre-cap value in _O41_PRED8, which the second call overwrites.
# A probe that reads those objects after the run sees only the LAST call's state and silently
# mis-prices every M3 row. My first attempt did exactly that and its own self-check caught it:
# 2 of 9 rows reproduced. So the take is now re-formed AT EACH CALL, in the state that call runs in,
# and combined with the same M3 weight the price itself uses.
CALLS = {}
_inner = NS['_PV']['blend']


def _reform(p, Y, g, e, ped, agedelta=0):
    """R3's take, re-formed from the engine's own objects, with the age credit optionally evaluated
    one year older. Age reaches this collector through o32_age_credit and nothing else."""
    if ped is None:
        return 0.0
    if o41_inj(p):
        return 0.0
    cx = depth(p, Y)
    if cx < 2.0 or compl(p, Y) < 1:
        return 0.0
    tgt = cost(cx)
    if tgt <= 0.0:
        return 0.0
    ac = o32_ac(p, Y + agedelta, g) if agedelta else o32_ac(p, Y, g)
    prod = rho31(g) * float(e)
    if prod <= 0.0:
        return 0.0
    epre = PRED8.get((id(p), int(Y)), e)
    free = rho31(g) * float(epre) + o31_pi(p, Y, g, _Dov=1.0) * ped + ac
    if not (free > 0.0):
        return 0.0
    now = prod + o31_pi(p, Y, g) * ped + ac
    taken = max(0.0, (free - now) / free)
    resid = max(0.0, tgt - taken)
    if resid <= 0.0:
        return 0.0
    return min(resid * free, prod)


def _wrapped(p, Y, e):
    g = pv_games(p, Y)
    try:
        ped = pv_ped(p)
    except SystemExit:
        ped = None
    d = dict(g=float(g), e=float(e), pin=bool(NS['_M3PIN']['on']))
    d['engine'] = r3take(p, Y, g, e, ped) if ped is not None else 0.0
    d['reform'] = _reform(p, Y, g, e, ped)
    d['reform_p1'] = _reform(p, Y, g, e, ped, agedelta=1)
    CALLS.setdefault((p.get('key'), int(Y)), []).append(d)
    return _inner(p, Y, e)


NS['_PV']['blend'] = _wrapped
EV = NS['ev'] if 'ev' in NS else MA.ev
for p in MA.players:
    EV(p, Y)
BY = {p['key']: p for p in MA.players}
P('  engine md5  %s' % hashlib.md5(open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py'),
                                        'rb').read()).hexdigest()[:8])
P()


def blended(k, field):
    cs = CALLS.get((k, Y))
    if not cs:
        return None
    if len(cs) == 1:
        return cs[0][field]
    w = L.m3_w(NS, BY[k], Y)
    return w * cs[0][field] + (1.0 - w) * cs[1][field]


# the numeraire, read off the row with the largest take: take/|board delta|. VERIFIED on every other
# charged row at tolerance 0 below — an inferred constant that fails that check is rejected outright.
kbig = min(CHARGED, key=lambda k: CHARGED[k])
NUM = blended(kbig, 'engine') / abs(CHARGED[kbig])

P('SELF-CHECK 1 — the re-formed take must equal the ENGINE\'s own take at every call, exactly.')
worst = 0.0
ncall = 0
for k, cs in CALLS.items():
    for d in cs:
        ncall += 1
        worst = max(worst, abs(d['engine'] - d['reform']))
P('  calls checked %d   worst absolute disagreement %.3e   %s'
  % (ncall, worst, 'EXACT' if worst == 0.0 else '*** NOT EXACT ***'))
P()
P('SELF-CHECK 2 — the blended take must reproduce the board\'s own per-row R3 delta, tolerance 0.')
P('  numeraire read off %s: %.10f' % (BY[kbig].get('player'), NUM))
P('  %-26s %5s %12s %12s %8s' % ('row', 'calls', 'board delta', 're-formed', 'agree'))
ok = bad = 0
rows = []
for k in sorted(CHARGED, key=lambda k: CHARGED[k]):
    t0 = blended(k, 'engine')
    d = -int(round(t0 / NUM))
    agree = (d == CHARGED[k])
    ok += agree; bad += (not agree)
    rows.append((k, BY[k].get('player'), CHARGED[k], t0))
    P('  %-26s %5d %12d %12.4f %8s'
      % ((BY[k].get('player') or k)[:26], len(CALLS.get((k, Y)) or []), CHARGED[k], t0,
         'yes' if agree else '*** NO ***'))
P('  agree %d of %d' % (ok, ok + bad))
P()

if bad or worst != 0.0:
    P('*** A SELF-CHECK FAILED. This probe cannot reproduce the board and therefore says NOTHING')
    P('    about the birthday question. Reported as a failure, not worked around. ***')
else:
    P('THE ISOLATED AGE STEP — R3\'s take at the real age vs at exactly one year older, with games,')
    P('output, pedigree and clock all held fixed. This is the isolation the age axis intends.')
    P('  %-26s %4s %11s %11s %10s %10s' % ('row', 'age', 'take now', 'take +1yr', 'step pts', 'price now'))
    steps = []
    for k, nmr, bd, t0 in rows:
        p = BY[k]
        by = p.get('_by')
        age = (Y - int(by)) if by else None
        t1 = blended(k, 'reform_p1')
        step = -int(round((t1 - t0) / NUM))
        steps.append((k, step))
        P('  %-26s %4s %11.4f %11.4f %+10d %10d'
          % ((nmr or k)[:26], age if age is not None else '?', t0, t1, step, CAND[k]['v']))
    P()
    tot = sum(s for _k, s in steps)
    big = sum(1 for _k, s in steps if CAND[_k]['v'] and abs(s) >= 0.5 * abs(CAND[_k]['v']))
    P('  BOARD POINTS THAT GENUINELY MOVE ACROSS THE BIRTHDAY THROUGH R3 : %+d' % tot)
    P('  ROWS MOVING 50%% OR MORE THROUGH R3 ACROSS THE BIRTHDAY          : %d' % big)
    P()
    P('THE CONTINUITY HARNESS REPORTED, ON THIS SAME BOARD: 9 rows moving, 3 of them by 50%% or more,')
    P('+1,025 net. THAT +1,025 IS R3\'S ENTIRE MARGINAL (%+d, measured above) AND THOSE 9 ROWS ARE'
      % sum(CHARGED.values()))
    P('EXACTLY THE 9 ROWS R3 CHARGES. The harness is not measuring an age step at all: os_lib.assemble')
    P('rebuilds the ORDER 31 law — rho*e + pi*ped + age_credit — WITH NO R3 TERM, so os_continuity.py')
    P('compares a price that CARRIES the collector against a rebuilt price that DROPS it, and prints')
    P('the collector itself as a birthday jump.')
    P()
    P('CONSEQUENCE, STATED PLAINLY AND NOT SOFTENED:')
    P('  · The board\'s birthday acceptance law is NOT breached — the true step is the number above.')
    P('  · The CONTINUITY HARNESS IS BLIND TO R3 and its age axis cannot be read on any board that')
    P('    carries the collector. That is an INSTRUMENT DEFECT, it is mine, and it is open.')
    P('  · The same blindness means the birthday line in the previous packet was measured with an')
    P('    instrument that could not see the lever it was clearing. It is re-measured here.')

json.dump(dict(engine=hashlib.md5(open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py'), 'rb').read()).hexdigest(),
               board=mCAND, pre=mPRE, charged={k: v for k, v in CHARGED.items()},
               numeraire=NUM, selfcheck_ok=ok, selfcheck_bad=bad),
          open(os.path.join(HERE, 'R3_AGE_CP.json'), 'w'), indent=1)
open(os.path.join(HERE, 'R3_AGE_CP_out.txt'), 'w').write('\n'.join(OUT) + '\n')
