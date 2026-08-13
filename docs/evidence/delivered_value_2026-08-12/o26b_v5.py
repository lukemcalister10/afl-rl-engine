#!/usr/bin/env python3
"""ORDER 26B -- THE V5 APPENDIX (NOT-RULED).

The brief asks for "a dial-gated V5 age-ladder variant of Layer 2 beside flat-14, labeled NOT-RULED
-- the owner's parked decision resurfaced on real numbers (cheap: one Layer-2 re-run)".

Step 3 already produced the V5 Layer-2 scores (`LAYER2.json::v5`) through the engine's OWN
age_disc()/disc_factor() path at RL_AGE_DISC_MODE=5. This file re-runs step 4's derivations on those
scores and prints the TOP-LEVEL DELTAS: the pre-anchor scale, the anchor factor, the curve at the
headline picks, the pathway all-ins and -- the quantity PREREG §7 P7.2 named -- every pathway's
ND-pick equivalent under both ladders.

NOTHING IS RULED HERE. V5 is the owner's parked fifth ladder (open-decisions ledger entry 1); flat-14
is the live config and the only basis any 26B conclusion rests on.

  usage:  python3 o26b_v5.py     ->  V5_APPENDIX.json / V5_APPENDIX_out.txt
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
HARN_DIR = os.path.join(ROOT, 'docs', 'evidence', 'composition_2026-08-10', 'noarb')
sys.path.insert(0, HARN_DIR)
import harness_pvc_REPINNED_pass3 as HP        # the SAME shipped kernel/bandwidth rule step 4 used
sys.path.insert(0, HERE)
import o26b_loclin as LL                        # CORRECTION 26B-C2 -- the same local-linear estimator

L2 = json.load(open(os.path.join(HERE, 'LAYER2.json')))
D = json.load(open(os.path.join(HERE, 'DERIVE.json')))
L1 = json.load(open(os.path.join(ROOT, 'data/delivered_value/layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}
BASE, V5 = L2['base'], L2['v5']
PICKS = list(range(1, 65))
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
K = int(D['pool']['K'])
PIN1 = 3000.0

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


ATTR = L2['attribution']     # CORRECTION 26B-C1 -- the force-majeure slide, read not recomputed


def build(SC):
    rows = [dict(key=k, pick=ATTR[k]['pick'], value=SC[k]['total']) for k in L2['fit_nd_keys']]
    raw, _e, _d = LL.kernel_loclin(rows, PICKS, HP.NMIN, HP.HMIN, HP.HMAX)   # 26B-C2
    pre = raw[0]; af = PIN1 / pre
    allin = {p: raw[i] * af for i, p in enumerate(PICKS)}
    pool = [dict(key=k, mech=ATTR[k]['mechanism'], pos=E[k]['position_group'], value=SC[k]['total'])
            for k in L2['fit_pool_keys']]
    ap = sum(r['value'] for r in pool) / len(pool)
    path = {}
    for m in POOLM:
        sub = [r for r in pool if r['mech'] == m]
        n = len(sub); a = (sum(r['value'] for r in sub) / n) if n else 0.0
        w = n / float(n + K)
        path[m] = dict(n=n, raw=a, shrunk=w * a + (1 - w) * ap)
    return dict(pre=pre, af=af, allin=allin, path=path, all_pool=ap,
                nd_mean=sum(r['value'] for r in rows) / len(rows))


A = build(BASE); B = build(V5)


def nd_equiv(v, allin, af):
    a = v * af
    if a >= allin[1]: return 0
    for p in PICKS:
        if allin[p] <= a: return p
    return 65


P("=" * 110)
P("ORDER 26B -- THE V5 AGE-LADDER APPENDIX.  **NOT RULED.**  flat-14 is the live config.")
P("=" * 110)
P("  V5 knots (rl_model.py::_V5_KNOTS, the owner's fifth ladder, keyed on the age at pricing --")
P("  here the ENTRY age, because Ruling 2 discounts from acquisition):")
P("    18:.120  19:.125  20:.130  21:.135  22:.140  23:.140  24:.145  25:.150  26:.150  27:.155  28+:.160")
P("  Below age 22 V5's rate is BELOW flat 14%, and a lower discount RAISES present value. So the")
P("  direction for young entrants is a RISE, not a fall.")
P()
P("  TOP-LEVEL DELTAS")
P("    %-34s %14s %14s %10s" % ('', 'flat-14', 'V5', 'V5/flat'))
P("    %-34s %14.1f %14.1f %10.4f" % ('ND cohort-mean delivered value', A['nd_mean'], B['nd_mean'],
                                      B['nd_mean'] / A['nd_mean']))
P("    %-34s %14.1f %14.1f %10.4f" % ('PRE-ANCHOR SCALE at pick 1', A['pre'], B['pre'],
                                      B['pre'] / A['pre']))
P("    %-34s %14.4f %14.4f %10.4f" % ('anchoring factor to pin 3000', A['af'], B['af'],
                                      B['af'] / A['af']))
P("    %-34s %14.1f %14.1f %10.4f" % ('all-pool all-in', A['all_pool'], B['all_pool'],
                                      B['all_pool'] / A['all_pool']))
P()
P("  THE CURVE AT THE HEADLINE PICKS (both anchored at pick 1 = 3000, so this is SHAPE only)")
HEAD = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]
P("    %-12s %s" % ('pick', "".join("%8d" % p for p in HEAD)))
P("    %-12s %s" % ('flat-14', "".join("%8.0f" % A['allin'][p] for p in HEAD)))
P("    %-12s %s" % ('V5', "".join("%8.0f" % B['allin'][p] for p in HEAD)))
P("    %-12s %s" % ('V5/flat', "".join("%8.3f" % (B['allin'][p] / A['allin'][p]) for p in HEAD)))
mx = max(abs(B['allin'][p] / A['allin'][p] - 1) for p in PICKS)
P("    max |V5/flat - 1| over picks 1-64 (post-anchor SHAPE move): %.4f  (%.2f%%)" % (mx, 100 * mx))
P()
P("  PATHWAY ALL-INS AND ND-PICK EQUIVALENTS  --  the quantity PREREG §7 P7.2 named")
P("    %-7s %6s %11s %11s %8s   %9s %9s %8s" %
  ('path', 'n', 'flat-14', 'V5', 'V5/flat', 'ND eq f14', 'ND eq V5', 'move'))
MOVES = {}
for m in POOLM:
    a = A['path'][m]['shrunk']; b = B['path'][m]['shrunk']
    ea = nd_equiv(a, A['allin'], A['af']); eb = nd_equiv(b, B['allin'], B['af'])
    MOVES[m] = dict(flat=a, v5=b, ratio=b / a if a else float('nan'),
                    nd_flat=ea, nd_v5=eb, move=abs(eb - ea), n=A['path'][m]['n'])
    P("    %-7s %6d %11.1f %11.1f %8.4f   %9s %9s %8d"
      % (m, A['path'][m]['n'], a, b, b / a if a else float('nan'),
         ('>64' if ea == 65 else str(ea)), ('>64' if eb == 65 else str(eb)), abs(eb - ea)))
MAXMOVE = max(v['move'] for v in MOVES.values())
P("    MAX ND-pick-equivalent move under V5: %d picks   (PREREG P7.2 predicted <= 6)" % MAXMOVE)
P()
P("  SIGN CHECK on every §3 conclusion (PREREG P7.2's other limb)")
ordA = [m for m in sorted(POOLM, key=lambda x: -A['path'][x]['raw'])]
ordB = [m for m in sorted(POOLM, key=lambda x: -B['path'][x]['raw'])]
P("    pathway ranking flat-14 : %s" % " > ".join(ordA))
P("    pathway ranking V5      : %s" % " > ".join(ordB))
P("    ranking identical: %s" % (ordA == ordB))
P("    every pathway all-in moves in the same direction (up): %s"
  % all(MOVES[m]['ratio'] >= 1.0 for m in POOLM))

OUT = dict(note='NOT RULED. flat-14 is the live config and the basis of every 26B conclusion.',
           knots=[[18, .12], [19, .125], [20, .13], [21, .135], [22, .14], [23, .14],
                  [24, .145], [25, .15], [26, .15], [27, .155], [28, .16]],
           flat14=dict(pre_anchor=A['pre'], anchor_factor=A['af'], nd_mean=A['nd_mean'],
                       all_pool=A['all_pool'], curve={p: A['allin'][p] for p in HEAD}),
           v5=dict(pre_anchor=B['pre'], anchor_factor=B['af'], nd_mean=B['nd_mean'],
                   all_pool=B['all_pool'], curve={p: B['allin'][p] for p in HEAD}),
           max_shape_move=mx, pathways=MOVES, max_nd_pick_move=MAXMOVE,
           ranking_flat=ordA, ranking_v5=ordB, ranking_identical=(ordA == ordB))
json.dump(OUT, open(os.path.join(HERE, 'V5_APPENDIX.json'), 'w'), indent=1, sort_keys=True,
          default=float)
open(os.path.join(HERE, 'V5_APPENDIX_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote V5_APPENDIX.json / V5_APPENDIX_out.txt")
