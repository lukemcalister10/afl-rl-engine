#!/usr/bin/env python3
"""ORDER 45 SELF-TEST (PREREG_ORDER45.md §4/§5): the with-net board vs the filed prediction,
at the prereg's DECLARED bands: lambda=1 rows must match EXACTLY (and must move); partial-lambda
rows within +-1 of the predicted value — which includes a predicted +1 landing at +0 (the declared
double-rounding knife-edge) — always DISCLOSED, never silent; ZERO movers outside the predicted
set. Exit 0 = PASS, non-zero = FAIL. --corrupt runs the proven-able-to-fail leg (leake altered +1;
the test MUST fail)."""
import json, sys

PRED = '/home/user/afl-rl-engine/docs/evidence/seam_fix_search_2026-08-25/NET_PREDICTION.json'
BASE = '/home/user/arm2_norec/board_final.json'      # 543bf900, the kill-switch-off board
WITH = '/home/user/arm2_norec/board_o45.json'        # the with-net board

corrupt = '--corrupt' in sys.argv
pred = json.load(open(PRED))['movers']
exp = {m['key']: (m['new'], m['lambda'], m['v']) for m in pred}
if corrupt:
    k = 'james-leake'
    exp[k] = (exp[k][0] + 1, exp[k][1], exp[k][2])
    print('[corrupt leg] expectation altered: james-leake new -> %d' % exp[k][0])

def vals(p):
    return {r['key']: r['v'] for r in json.load(open(p))['active']}

base, withb = vals(BASE), vals(WITH)
fails, disclosed = [], []
movers = {k: (base.get(k), withb.get(k)) for k in withb if k in base and base[k] != withb[k]}
extra = sorted(set(movers) - set(exp))
if extra:
    fails.append('EXTRA movers not in the prediction: %s' % [(k, movers[k]) for k in extra])
for k, (nv, lam, pv) in sorted(exp.items()):
    got = withb.get(k)
    if got is None:
        fails.append('%s: predicted row absent from the with-net board' % k)
        continue
    if lam >= 1.0:
        if got != nv:
            fails.append('%s: lambda=1 row must match EXACTLY (and move): predicted %d got %d' % (k, nv, got))
    else:
        if abs(got - nv) > 1:
            fails.append('%s: partial-lambda row outside the declared +-1: predicted %d got %d' % (k, nv, got))
        elif got != nv:
            disclosed.append('%s: partial lambda %.3f, predicted %d got %d (declared knife-edge; '
                             'reconciliation owed before the dry-run)' % (k, lam, nv, got))
lift = sum(withb[k] - base[k] for k in movers)
same = sum(1 for k in base if k in withb and base[k] == withb[k])
print('movers %d (predicted %d) · total lift %+d (predicted +923) · unmoved rows %d'
      % (len(movers), len(exp), lift, same))
for d in disclosed:
    print('DISCLOSED: ' + d)
if fails:
    print('SELF-TEST FAIL:')
    [print('  - ' + f) for f in fails]
    sys.exit(1)
print('SELF-TEST PASS (%d disclosed knife-edge deviation(s))' % len(disclosed)
      + (' — BUT THE CORRUPT LEG MUST FAIL; this is a RED' if corrupt else ''))
sys.exit(2 if corrupt else 0)
