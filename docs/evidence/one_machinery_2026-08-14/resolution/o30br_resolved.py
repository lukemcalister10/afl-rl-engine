#!/usr/bin/env python3
"""ORDER 30B-R -- what the preview board's named rows BECOME under the resolved configuration.

DERIVED, NOT BUILT.  No engine runs here.  This composes the three resolution artifacts
(READING.json, CLOCK.json, JOIN.json) with the committed preview legs and prints the named rows.
Every number is arithmetic on committed quantities; NOTHING IS WIRED and no board exists.

The resolved configuration, as this order's tasks close it:
  * READING  -- T1: the ADDITIVE form  price = production + beta(g) x v0  is the faithful one.
                The preview's WEIGHT form is carried beside it so the owner sees the difference.
  * CLOCK    -- T2: RAW career games is RETAINED; the recency clock LOST its own preregistered
                held-out criterion.  So the games axis is unchanged from the preview.
  * CURVE    -- T3: the JOIN.  Thin lane (<=10 games) is the cumulative backbone as a lift on the
                sitter price; 11-15 is the DECLARED bridge; 16+ is the deep lane.
  * OBJECT   -- T4: OPEN.  Both objects are printed; the seat does not choose.

  usage:  python3 o30br_resolved.py    (writes RESOLVED_ROWS.json + RESOLVED_ROWS_out.txt)
"""
import os, json, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
MOVP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')
RD = json.load(open(os.path.join(HERE, 'READING.json')))
JN = json.load(open(os.path.join(HERE, 'JOIN.json')))
MOV = json.load(open(MOVP))
BYK = {r['key']: r for r in MOV['rows']}
TAU, BETA = MOV['sigma']['tau'], MOV['sigma']['beta']

_LOG = []
def P(s=''):
    print(s)
    _LOG.append(str(s))

def sigma(g):
    return math.exp(-((max(1e-9, float(g)) / TAU) ** BETA))

BPTS = [tuple(x) for x in RD['beta_curve']['points']]
def beta_at(g):
    g = max(1e-6, float(g))
    if g <= BPTS[0][0]:
        return BPTS[0][1]
    if g >= BPTS[-1][0]:
        return BPTS[-1][1]
    for i in range(1, len(BPTS)):
        g0, b0 = BPTS[i - 1]; g1, b1 = BPTS[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(b0) + t * (math.log(b1) - math.log(b0)))
    return BPTS[-1][1]

BACKBONE = {int(k): [(int(a), float(b)) for a, b in v] for k, v in JN['backbone'].items()}
def depth_lane(c):
    return 2 if c < 2.5 else 3
def b_lift(g, c):
    pts = BACKBONE[depth_lane(c)]
    b0 = pts[0][1]
    lift = [(k, v / b0) for k, v in pts]
    if g <= 0:
        return 1.0
    x = math.log1p(float(g))
    for i in range(1, len(lift)):
        k0, l0 = lift[i - 1]; k1, l1 = lift[i]
        x0, x1 = math.log1p(k0), math.log1p(k1)
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return math.exp(math.log(l0) + t * (math.log(l1) - math.log(l0)))
    (k0, l0), (k1, l1) = lift[-2], lift[-1]
    sl = (math.log(l1) - math.log(l0)) / (math.log1p(k1) - math.log1p(k0))
    return math.exp(math.log(l1) + sl * (x - math.log1p(k1)))

NAMED = ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow', 'cooper-trembath',
         'chris-scerri', 'josh-smillie', 'harry-demattia', 'max-knobel']
ANCH = {k: v['entry_anchor'] for k, v in RD['t4']['named'].items()}

P('=' * 116)
P('ORDER 30B-R -- THE NAMED ROWS UNDER THE RESOLVED CONFIGURATION.   *** DERIVED, NOT BUILT ***')
P('=' * 116)
P('  No engine ran.  No board exists.  NOTHING WIRES UNTIL THE OWNER RULES.')
P('  READING = additive (T1) | CLOCK = raw career games, RETAINED (T2) | CURVE = the join (T3)')
P('  | OBJECT = OPEN (T4): both printed.')
P('')
OUT = {}
P('%-17s %-4s %5s %8s %9s %9s %9s | %7s %7s | %9s %9s %9s'
  % ('row', 'path', 'g', 'lane', 'prod P', 'v0', 'anchor', 'STEP-2', 'PREVIEW',
     'RESOLVED', 'w/ anchor', 'weight-rd'))
for k in NAMED:
    r = BYK[k]
    g = r['games_sigma_axis'] or 0.0
    v0 = r['v0_step1_board']; A = ANCH.get(k); D = r['fade_D']; c = r['fade_clock']
    Pp = r['production_pts']
    note = ''
    if r['day0'] or Pp is None:
        lane = 'sitter'
        res_v0 = v0 * D; res_an = (A * D) if A else None; res_w = res_v0
        note = 'gameless -- the sitter law is untouched by every task in this order'
    elif g <= 10:
        lane = 'thin'
        res_v0 = v0 * D * b_lift(g, c)
        res_an = (A * D * b_lift(g, c)) if A else None
        res_w = res_v0
        note = 'backbone lane: production does NOT enter -- see the T3 conflict'
        if r['pool']:
            note += ' ; POOL FADE NOT DERIVED (D forced to 1.0) -- Step 4'
    elif g < 16:
        lane = 'bridge'
        j = JN['join'].get(k)
        if j:
            thin10 = v0 * D * b_lift(10, c)
            t = (math.log1p(g) - math.log1p(10)) / (math.log1p(16) - math.log1p(10))
            res_v0 = thin10 + t * (j['deep16_additive'] - thin10)
            res_w = thin10 + t * (j['deep16_weight'] - thin10)
            res_an = None
            note = 'DECLARED BRIDGE -- not a measurement'
        else:
            res_v0 = res_w = res_an = None
            note = 'bridge lane but no continuity curve committed for this row'
    else:
        lane = 'deep'
        res_v0 = Pp + beta_at(g) * v0
        res_an = (Pp + beta_at(g) * A) if A else None
        res_w = (1 - sigma(g)) * Pp + sigma(g) * v0
        if r['pool']:
            note = 'POOL -- v0 cell provisional, Step 4'
    OUT[k] = dict(name=r['name'], pathway=r['pathway'], pick=r['pick'], pos=r['pos'], games=g,
                  lane=lane, production=Pp, v0=v0, entry_anchor=A, fade_D=D, fade_clock=c,
                  live=r['live'], step2=r['step2'], preview=r['preview'],
                  resolved_v0=res_v0, resolved_anchor=res_an, resolved_weight_reading=res_w,
                  beta=(beta_at(g) if lane == 'deep' else None),
                  sigma=(sigma(g) if lane == 'deep' else None), pool=r['pool'], note=note)
    P('%-17s %-4s %5.0f %8s %9s %9.1f %9s | %7d %7d | %9s %9s %9s'
      % (k, r['pathway'], g, lane, ('%.1f' % Pp) if Pp is not None else '-', v0,
         ('%.1f' % A) if A else '-', r['step2'], r['preview'],
         ('%.0f' % res_v0) if res_v0 is not None else '-',
         ('%.0f' % res_an) if res_an is not None else '-',
         ('%.0f' % res_w) if res_w is not None else '-'))
P('')
for k in NAMED:
    if OUT[k]['note']:
        P('  %-17s %s' % (k, OUT[k]['note']))
P('')
P('  RESOLVED  = the additive reading on the v0 object, on the joined curve.')
P('  w/ anchor = the same, with entry_anchor substituted for v0 (T4 -- the OWNER\'S word).')
P('  weight-rd = the same lane, but under the preview\'s WEIGHT reading, so the cost of T1 is visible.')
P('')
P('  Movement against the preview board:')
P('  %-17s %10s %10s %10s' % ('row', 'PREVIEW', 'RESOLVED', 'delta %'))
for k in NAMED:
    d = OUT[k]
    if d['resolved_v0'] is None:
        continue
    P('  %-17s %10d %10.0f %+9.1f%%'
      % (k, d['preview'], d['resolved_v0'], 100 * (d['resolved_v0'] / d['preview'] - 1)))
P('')
# --------------------------------------------------------------------------------------------------
# THE WHOLE BOOK under the resolved configuration -- same arithmetic, all 804 rows.
# --------------------------------------------------------------------------------------------------
P('=' * 116)
P('THE WHOLE BOOK UNDER THE RESOLVED CONFIGURATION   *** DERIVED, NOT BUILT ***')
P('=' * 116)
def book(reading, obj, joined):
    tot = 0.0
    lanes = {'sitter': [0, 0.0], 'thin': [0, 0.0], 'bridge': [0, 0.0], 'deep': [0, 0.0]}
    for r in MOV['rows']:
        v0 = r['v0_step1_board']; D = r['fade_D']; c = r['fade_clock']
        A = ANCH.get(r['key'])
        V = v0 if obj == 'v0' else (A if A else v0)
        Pp = r['production_pts']; g = r['games_sigma_axis'] or 0.0
        if r['day0'] or Pp is None:
            pr = V * D; ln = 'sitter'
        elif joined and g <= 10:
            pr = V * D * b_lift(g, c); ln = 'thin'
        elif joined and g < 16:
            thin10 = V * D * b_lift(10, c)
            d16 = (Pp + beta_at(16) * V) if reading == 'A' else ((1 - sigma(16)) * Pp + sigma(16) * V)
            t = (math.log1p(g) - math.log1p(10)) / (math.log1p(16) - math.log1p(10))
            pr = thin10 + t * (d16 - thin10); ln = 'bridge'
        else:
            pr = (Pp + beta_at(g) * V) if reading == 'A' else ((1 - sigma(g)) * Pp + sigma(g) * V)
            ln = 'deep'
        tot += pr
        lanes[ln][0] += 1; lanes[ln][1] += pr
    return tot, lanes
BOOK = {}
P('%-38s %12s %10s' % ('configuration', 'book total', 'vs preview'))
prevtot = sum(r['preview'] for r in MOV['rows'])
for lab, rdg, obj, jn in (('PREVIEW as built (weight, v0, no join)', 'W', 'v0', False),
                          ('weight reading, v0, JOINED', 'W', 'v0', True),
                          ('ADDITIVE reading, v0, no join', 'A', 'v0', False),
                          ('RESOLVED: additive, v0, JOINED', 'A', 'v0', True),
                          ('RESOLVED: additive, ANCHOR, JOINED', 'A', 'anchor', True)):
    t, lanes = book(rdg, obj, jn)
    BOOK[lab] = dict(total=t, lanes={k: dict(n=v[0], total=v[1]) for k, v in lanes.items()})
    P('%-38s %12.0f %+9.2f%%' % (lab, t, 100 * (t / prevtot - 1)))
P('')
P('  preview board as printed (integers, 804 rows): %d' % prevtot)
t, lanes = book('A', 'v0', True)
P('  RESOLVED lane populations: %s'
  % {k: (v[0], round(v[1])) for k, v in lanes.items()})
P('')
P('  THE PRE-NUMERAIRE WARNING STANDS: Step 6\'s re-pin has not run.  Read the MOVEMENT, not the level.')
P('')

json.dump(dict(order='30B-R', derived_not_built=True, greenlit=False, rows=OUT, book=BOOK,
               preview_total=prevtot),
          open(os.path.join(HERE, 'RESOLVED_ROWS.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'RESOLVED_ROWS_out.txt'), 'w').write('\n'.join(_LOG) + '\n')
P('wrote RESOLVED_ROWS.json and RESOLVED_ROWS_out.txt')
