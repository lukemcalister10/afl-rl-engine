#!/usr/bin/env python3
"""ORDER J — WHY J-TOL FAILS, ROW BY ROW, AND WHAT THE EXCHANGE RATE ACTUALLY IS.

The gate is preregistered and is NOT touched here. This file answers the two questions the owner has
to be able to rule on:

  1. WHICH rows fail, what are they worth, and what percentage of their own value do they move?
     (Is the binding clause the 0.5% cap on real rows, or the 1.0-point floor on tiny ones?)
  2. WHAT IS THE EXCHANGE RATE — for each candidate setting, the smallest per-row tolerance under
     which it would pass. That is "how far away", stated in the gate's own units, so the owner can
     rule knowingly instead of being told "impossible".
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, 'JTOL_J.json')))
BASE = G['base']; CAPS = G['caps']; AGES = G['ages']
CH, NT = G['rule']['churn_cap'], G['rule']['net_cap']


def load_deltas():
    """the per-point deltas are stored in the ladder/shortlist entries written by the gate run"""
    raw = json.load(open(os.path.join(HERE, 'JTOL_RAW.json')))
    return raw


RAW = load_deltas()
print('ORDER J — the anatomy of the J-TOL failures.  board points throughout.\n')
print('THE GATE (PREREG_J §2.2): per row |d| <= min(25, max(1, 0.005*v)) · churn <= %.2f · net <= %.2f'
      % (CH, NT))

ORDER = ['eta 0.41 -> 0.42', 'kappa 0.24 -> 0.22', 'kappa 0.24 -> 0.26', 'lambda_rel 1.08 -> 1.00',
         'gamma_u 11 -> 12', 'gamma_d 14 -> 13']
print('\n=== 1 · THE SMALLEST KNOB STEPS: WHO ACTUALLY BREAKS, AND BY HOW MUCH OF HIS OWN VALUE ===')
for nm in ORDER:
    d = RAW.get(nm)
    if d is None:
        continue
    rows = sorted(((abs(v) / CAPS[k], k, v, BASE[k]) for k, v in d.items()),
                  reverse=True)
    over = [r for r in rows if r[0] > 1.0]
    print('\n-- %s :  %d rows move, %d over their cap --' % (nm, len(d), len(over)))
    print('   %-24s %4s %10s %9s %8s %8s  %s'
          % ('row', 'age', 'value', 'move', 'as %', 'its cap', 'clause that binds'))
    for ratio, k, v, val in over[:10]:
        cl = 'the 1.0-pt floor (row < 200)' if CAPS[k] <= 1.0 else 'the 0.5%% cap'
        print('   %-24s %4d %10.1f %+9.3f %+7.3f%% %8.3f  %s' % (k, AGES[k], val, v, 100 * v / val,
                                                                 CAPS[k], cl))
    nfloor = sum(1 for r in over if CAPS[r[1]] <= 1.0)
    print('   of the %d over-cap rows: %d are held by the 1.0-point FLOOR (value < 200 bp), '
          '%d by the 0.5%% CAP' % (len(over), nfloor, len(over) - nfloor))
    if over:
        print('   worst row moves %.3f%% of its own value; the gate allows 0.5%%'
              % (100 * abs(over[0][2]) / over[0][3]))

print('\n=== 2 · THE EXCHANGE RATE — the per-row tolerance each candidate setting would need ===')
print('   "needs p%" = the smallest flat per-row percentage-of-value cap (with the same 1.0-point')
print('   floor and 25-point ceiling) under which that setting would pass clause (a).')
print('\n   %-42s %8s %8s %9s %9s %7s'
      % ('setting', 'needs %', 'worst bp', 'churn', 'net', 'b/c ok'))
ROWS = []
for nm, d in RAW.items():
    need = 0.0
    for k, v in d.items():
        if abs(v) <= 1.0:
            continue
        need = max(need, abs(v) / max(BASE[k], 1e-9))
    churn = sum(abs(v) for v in d.values()); net = sum(d.values())
    worst = max((abs(v) for v in d.values()), default=0.0)
    ROWS.append((nm, 100 * need, worst, churn, net, (churn <= CH and abs(net) <= NT)))
for nm, need, worst, churn, net, bc in ROWS:
    if not nm.startswith('#'):
        continue
    print('   %-42s %7.2f%% %8.2f %9.1f %+9.1f %7s' % (nm, need, worst, churn, net, 'ok' if bc else 'no'))
print()
for nm, need, worst, churn, net, bc in ROWS:
    if nm.startswith('#'):
        continue
    print('   %-42s %7.2f%% %8.2f %9.1f %+9.1f %7s' % (nm, need, worst, churn, net, 'ok' if bc else 'no'))

print('\n=== 3 · THE FREE PLAY — how far each knob may move before J-TOL bites ===')
print('   read off the ladder by linearity: mature movement is very nearly proportional to the')
print('   distance from the repair point, so the admissible step is (step tested) x (cap / worst ratio)')
for ax, nm, step in (('eta', 'eta 0.41 -> 0.42', 0.01), ('kappa', 'kappa 0.24 -> 0.26', 0.02),
                     ('kappa', 'kappa 0.24 -> 0.22', -0.02), ('gamma_u', 'gamma_u 11 -> 12', 1.0),
                     ('gamma_d', 'gamma_d 14 -> 13', -1.0), ('lambda_rel', 'lambda_rel 1.08 -> 1.00', -0.08)):
    d = RAW.get(nm)
    if d is None:
        continue
    r = max((abs(v) / CAPS[k]) for k, v in d.items())
    print('   %-11s tested step %+7.3f -> worst row sits at %6.2fx its cap -> free play about %+8.4f'
          % (ax, step, r, step / r))
