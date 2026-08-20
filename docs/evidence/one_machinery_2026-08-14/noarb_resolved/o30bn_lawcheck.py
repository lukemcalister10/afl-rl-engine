#!/usr/bin/env python3
"""ORDER 30B-N -- THE DEFINITIVE WIRING PROOF: is the WIRED law the RESOLUTION'S ARITHMETIC?

The row control compares the wired law against the DERIVED board on real rows. That comparison can
never reach zero, because the derived board's production column is a rounding-inverted quantity and
because the engine rounds at its blend site. So it cannot, on its own, distinguish "correctly wired"
from "wired with a small error".

THIS harness removes every rounding from the question by testing the FUNCTIONS, not the prices:

  1. beta30bn(g)      vs the resolution's beta_at(g)   -- EXACT float equality, dense g grid
  2. b_lift30bn(g,c)  vs the resolution's b_lift(g,c)  -- EXACT float equality, dense (g,c) grid
  3. the whole lane rule -- the engine's _pv_resolved(P,v0,D,c,g) against o30br_resolved.py::book()'s
     own branch arithmetic, over a synthetic grid spanning every lane and both depth lanes -- EXACT.

The reference side is reimplemented HERE from READING.json / JOIN.json, independently of the engine,
and is itself checked against the committed RESOLVED_ALLROWS.json before it is used as a reference.

env:   RL_O30B_RESOLVED=1  STAGE=<resolved-staged rl_after>  RL_REPO=<worktree>
"""
import os, sys, io, json, math, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'resolution')
PRV = os.path.join(HERE, '..', 'preview')

# ---- THE REFERENCE SIDE: reimplemented from the committed artifacts, engine never consulted --------
RD = json.load(open(os.path.join(RES, 'READING.json')))
JN = json.load(open(os.path.join(RES, 'JOIN.json')))
BPTS = [tuple(x) for x in RD['beta_curve']['points']]
BACKBONE = {int(k): [(int(a), float(b)) for a, b in v] for k, v in JN['backbone'].items()}


def beta_at(g):
    g = max(1e-6, float(g))
    if g <= BPTS[0][0]:
        return BPTS[0][1]
    if g >= BPTS[-1][0]:
        return BPTS[-1][1]
    for i in range(1, len(BPTS)):
        g0, b0 = BPTS[i - 1]
        g1, b1 = BPTS[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(b0) + t * (math.log(b1) - math.log(b0)))
    return BPTS[-1][1]


def b_lift(g, c):
    pts = BACKBONE[2 if c < 2.5 else 3]
    b0 = pts[0][1]
    lift = [(k, v / b0) for k, v in pts]
    if g <= 0:
        return 1.0
    x = math.log1p(float(g))
    for i in range(1, len(lift)):
        k0, l0 = lift[i - 1]
        k1, l1 = lift[i]
        x0, x1 = math.log1p(k0), math.log1p(k1)
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return math.exp(math.log(l0) + t * (math.log(l1) - math.log(l0)))
    (k0, l0), (k1, l1) = lift[-2], lift[-1]
    sl = (math.log(l1) - math.log(l0)) / (math.log1p(k1) - math.log1p(k0))
    return math.exp(math.log(l1) + sl * (x - math.log1p(k1)))


def ref_price(P, v0, D, c, g, day0):
    """The resolution's own branch arithmetic, o30br_resolved.py::book() / o30br_allrows.py."""
    if day0 or P is None:
        return v0 * D
    if g <= 10:
        return v0 * D * b_lift(g, c)
    if g < 16:
        t10 = v0 * D * b_lift(10, c)
        d16 = P + beta_at(16) * v0
        t = (math.log1p(g) - math.log1p(10)) / (math.log1p(16) - math.log1p(10))
        return t10 + t * (d16 - t10)
    return P + beta_at(g) * v0


# ---- the reference is itself checked against the committed derived board BEFORE it is used ---------
AR = json.load(open(os.path.join(RES, 'RESOLVED_ALLROWS.json')))
MOV = json.load(open(os.path.join(PRV, 'PREVIEW_MOVERS.json')))
_B = {r['key']: r for r in AR['rows']}
_worst = 0.0
for r in MOV['rows']:
    pr = ref_price(r['production_pts'], r['v0_step1_board'], r['fade_D'], r['fade_clock'],
                   r['games_sigma_axis'] or 0.0, r['day0'])
    _worst = max(_worst, abs(round(pr, 1) - _B[r['key']]['resolved']))
print('REFERENCE SELF-CHECK: independent reimplementation vs committed RESOLVED_ALLROWS.json')
print('  804 rows, max |delta| = %.10f   %s' % (_worst, 'OK' if _worst < 1e-9 else 'REFERENCE IS WRONG'))
assert _worst < 1e-9, 'the reference side does not reproduce the committed derived board'

# ---- THE ENGINE SIDE ------------------------------------------------------------------------------
assert os.environ.get('RL_O30B_RESOLVED') == '1', 'this harness must run IN the resolved lane'
STAGE = os.environ['STAGE']
ROOT = os.environ['RL_REPO']
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
beta30bn = G['beta30bn']
b_lift30bn = G['b_lift30bn']
_pv_resolved = G['_pv_resolved']
_PL_F = G['_PL_F']

fail = {}

# 1. beta
gs = [i / 4.0 for i in range(1, 4001)] + [0.0, 1e-6, 2.5, 10.5, 25.5, 53.0, 85.5, 200.0, 1e4]
d = max(abs(beta30bn(g) - beta_at(g)) for g in gs)
fail['beta_exact'] = d
print('\n1. beta30bn(g) vs beta_at(g)          %d points  max |delta| = %.3e  %s'
      % (len(gs), d, 'EXACT' if d == 0.0 else 'DIFFERS'))

# 2. b_lift
cs = [0.0, 0.5, 1.0, 1.5, 2.0, 2.4999, 2.5, 2.5001, 3.0, 3.92, 5.0, 9.0]
d = max(abs(b_lift30bn(g, c) - b_lift(g, c)) for g in gs for c in cs)
fail['blift_exact'] = d
print('2. b_lift30bn(g,c) vs b_lift(g,c)     %d points  max |delta| = %.3e  %s'
      % (len(gs) * len(cs), d, 'EXACT' if d == 0.0 else 'DIFFERS'))

# 3. the whole lane rule, through the engine's own _pv_resolved, on a synthetic grid.
#    _pv_resolved reads its inputs off the player object, so a stand-in exposes them; the callable
#    under test is the ENGINE'S, not a copy.
G['pv_games'] = lambda p, Y: p['g']
G['pv_pedigree'] = lambda p: p['v0'] * _PL_F
G['fade30b_of'] = lambda p, Y: p['D']
G['fade30b_clock'] = lambda p, Y: p['c']
_pv2 = G['_pv_resolved'].__class__(G['_pv_resolved'].__code__, G, '_pv_resolved')
worst = 0.0
worst_at = None
n = 0
for g in [0.5, 1, 2, 3, 5, 7, 9.5, 10, 10.0001, 11, 12.5, 13, 15, 15.999, 16, 20, 40, 75, 120]:
    for c in cs:
        for D in (0.2628, 0.3460, 0.5502, 1.0):
            for v0 in (85.3, 512.9, 1566.7, 4000.0):
                for P in (0.0, 120.0, 1531.3, 5000.0):
                    n += 1
                    got = _pv2({'g': g, 'v0': v0, 'D': D, 'c': c}, 2026, P * _PL_F) / _PL_F
                    want = ref_price(P, v0, D, c, g, False)
                    if abs(got - want) > worst:
                        worst, worst_at = abs(got - want), (g, c, D, v0, P)
fail['lane_rule_exact'] = worst
print('3. engine _pv_resolved vs book()      %d points  max |delta| = %.3e  %s   %s'
      % (n, worst, 'EXACT' if worst < 1e-9 else 'DIFFERS', '' if worst < 1e-9 else worst_at))

ok = fail['beta_exact'] == 0.0 and fail['blift_exact'] == 0.0 and fail['lane_rule_exact'] < 1e-9
print('\nWIRING PROOF: %s' % ('HELD — the wired law IS the resolution arithmetic, exactly.'
                             if ok else 'BREACHED — the wired law is NOT the resolution arithmetic.'))
json.dump(dict(reference_selfcheck_max_delta=_worst, checks=fail, held=bool(ok)),
          open(os.path.join(HERE, 'LAWCHECK_30BN.json'), 'w'), indent=1, sort_keys=True)
print('wrote LAWCHECK_30BN.json')
