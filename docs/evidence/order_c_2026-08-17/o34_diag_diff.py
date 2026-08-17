#!/usr/bin/env python3
"""ORDER C — surface-only diagnostic diff on FINISHED boards: bb_o34diag1 (RL_O34=1, alpha=1) vs
bb_o32ctrl (RL_O32=1, == 7802ee97). Section-level diff first, then active-row movers, MATURE movers
(must be zero), totals, top movers, named rows."""
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
JA = json.load(open(SP + '/o34/bb_o32ctrl/rl_after/rl_app_data.json'))
JB = json.load(open(SP + '/o34/bb_o34diag1/rl_after/rl_app_data.json'))
print('top-level keys equal:', set(JA) == set(JB))
for k in JA:
    if json.dumps(JA[k], sort_keys=True, default=str) != json.dumps(JB.get(k), sort_keys=True, default=str):
        print('SECTION DIFFERS:', k)
A = {r['key']: r for r in JA['active']}
B = {r['key']: r for r in JB['active']}
mov = [(k, A[k].get('age'), A[k].get('pos'), A[k]['v'], B[k]['v']) for k in A if A[k]['v'] != B[k]['v']]
print('active v movers:', len(mov), ' total ctrl', sum(r['v'] for r in JA['active']),
      ' diag', sum(r['v'] for r in JB['active']))
mat = [m for m in mov if (m[1] or 0) >= 24]
print('mature movers:', len(mat), mat[:8])
for m in sorted(mov, key=lambda t: -abs(t[4] - t[3]))[:20]:
    print(m)
named = ['harry-dean', 'cooper-duff-tytler', 'nick-madden', 'alix-tauru', 'jordan-croft',
         'jedd-busslinger', 'ethan-read', 'ty-gallop', 'charlie-west', 'chris-scerri',
         'thomas-burton', 'milan-murdock']
print('--- named (ctrl -> diag surface-only):')
for k in named:
    print(' %-22s %6d -> %6d  (age %s)' % (k, A[k]['v'], B[k]['v'], A[k].get('age')))
