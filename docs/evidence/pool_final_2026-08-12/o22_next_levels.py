#!/usr/bin/env python3
"""ORDER 22 -- ONE STEP OF THE ITERATION. Turn a derivation into the next candidate level table.

    next_level = round( level_in_force * lambda_measured )

LEVELS ARE WRITTEN AS INTEGERS, DELIBERATELY. `rl_model.py:1425-1427` builds the engine's lookup with
`int(float(v))` -- it TRUNCATES. Today's owner-signed table is therefore already read one way and
written another: 133.4 is 133 in the engine, 286.8 is 286, 294.8 is 294. Writing integers makes the
signed table and the engine's table THE SAME OBJECT, removes a silent up-to-0.9-point haircut, and
makes every number in the packet the number the machine used. THE QUANTISATION COST IS PRINTED: at a
level of 28 one integer step is 3.6%, which is coarser than the declared 1.0% convergence tolerance,
and that is a fact about the engine's storage, reported and not hidden.

SECANT ACCELERATION (declared, and switched on only from round 2).

The plain rule `L <- L * lambda` assumes the numerator is invariant to the level. IT IS NOT: a pool
entrant with a thin record is priced off the anchor, so cutting his level cuts his realised value too,
and part of every correction is eaten. Measured: PDS's gap to 1 closed by only ~32% per round under
the plain rule (0.446 -> 0.599 -> 0.737), which would not reach 1% inside the declared 8-round cap.

So from the second round the step is fitted rather than assumed. Over two consecutive rounds

    lambda ~ K * L**(-beta)   =>   beta = -(ln L2 - ln L1)**-1 * (ln lam2 - ln lam1)

and the level that solves `lambda = 1` is `L* = L2 * lam2**(1/beta)`. beta = 1 means the numerator is
invariant (the plain rule); beta < 1 means the numerator follows the level and the plain rule
under-corrects. beta is CLIPPED to [0.25, 3.0] and the per-round move is CAPPED at a factor of 2, so
a noisy pair cannot throw the iteration. Both the fitted beta and the step taken are printed every
round, so the trajectory is auditable rather than magic.

  usage: o22_next_levels.py <derive.json> <out_levels.json> [--damp F] [--accel <prev_derive.json>]
"""
import sys, json, os, math

D = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
DAMP = 1.0
if '--damp' in sys.argv:
    DAMP = float(sys.argv[sys.argv.index('--damp') + 1])
PREV = None
if '--accel' in sys.argv:
    PREV = json.load(open(sys.argv[sys.argv.index('--accel') + 1]))

INF = D['levels_in_force']
L1 = D['layer1']
SH = D['shipped']
POS6 = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
FLATP = ['SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR']


def prev_pair(key):
    """(level, lambda) from the previous round for this key, or None."""
    if PREV is None: return None
    if key.startswith('RD:'):
        p = key[3:]
        return float(PREV['levels_in_force']['signed_rd_positional'][p]), PREV['shipped']['RD']['lam'][p]
    if key == 'ND65+':
        return float(PREV['levels_in_force']['nd65_effective']), PREV['layer1']['ND>64']['lam']
    return float(PREV['levels_in_force']['signed_flat'][key]), PREV['layer1'][key]['lam']


BETAS = {}


def step(key, cur, lam):
    """plain: L*lam. accelerated: L * lam**(1/beta) with beta fitted on the last two rounds."""
    plain = cur * (1.0 + DAMP * (lam - 1.0))
    pp = prev_pair(key)
    beta = None
    if pp and lam > 0 and pp[1] > 0 and abs(math.log(cur / pp[0])) > 1e-9 and abs(lam - 1.0) > 1e-6:
        b = -(math.log(lam) - math.log(pp[1])) / (math.log(cur) - math.log(pp[0]))
        if b == b and b > 0:
            beta = min(3.0, max(0.25, b))
    BETAS[key] = beta
    if beta is None: return plain, None
    nxt = cur * (lam ** (1.0 / beta))
    return min(cur * 2.0, max(cur * 0.5, nxt)), beta


print("  %-10s %14s %12s %8s %14s %10s %12s" %
      ('key', 'in force', 'lambda', 'beta', 'raw next', 'INT next', '1-int step'))
flat = {}


def emit(key, cur, lam):
    raw, beta = step(key, cur, lam)
    iv = max(1, int(round(raw)))
    print("  %-10s %14.4f %12.6f %8s %14.4f %10d %11.2f%%" %
          (key, cur, lam, ('%.3f' % beta) if beta else 'plain', raw, iv, 100.0 / iv))
    return iv


for s in FLATP:
    flat[s] = emit(s, float(INF['signed_flat'][s]), L1[s]['lam'])
nd65 = emit('ND65+', float(INF['nd65_effective']), L1['ND>64']['lam'])
rd = {}
for p in POS6:
    rd[p] = emit('RD:' + p, float(INF['signed_rd_positional'][p]), SH['RD']['lam'][p])

json.dump(dict(signed_flat=flat, signed_rd_positional=rd, nd65_measured_k15=nd65,
               _from=os.path.basename(sys.argv[1]), _damp=DAMP, _betas=BETAS),
          open(OUT, 'w'), indent=1)
print("  wrote %s" % OUT)
