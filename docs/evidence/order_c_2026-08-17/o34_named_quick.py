#!/usr/bin/env python3
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
A = {r['key']: r for r in json.load(open(SP + '/o34/bb_o32ctrl/rl_after/rl_app_data.json'))['active']}
S = {r['key']: r for r in json.load(open(SP + '/o34/bb_o34diag1/rl_after/rl_app_data.json'))['active']}
B = {r['key']: r for r in json.load(open(SP + '/o34/bb_final/rl_after/rl_app_data.json'))['active']}
named = ['harry-dean', 'cooper-duff-tytler', 'nick-madden', 'alix-tauru', 'jordan-croft',
         'jedd-busslinger', 'ethan-read', 'ty-gallop', 'charlie-west', 'chris-scerri',
         'thomas-burton', 'milan-murdock', 'vigo-visentini']
print('%-22s %4s %4s | %6s %6s %6s | surf alpha' % ('key', 'age', 'cg', 'C32R', 'SURF', 'C'))
for k in named:
    print('%-22s %4s %4s | %6d %6d %6d | %+4d %+4d'
          % (k, A[k].get('age'), A[k].get('cg'), A[k]['v'], S[k]['v'], B[k]['v'],
             S[k]['v'] - A[k]['v'], B[k]['v'] - S[k]['v']))
mov = [(k, A[k].get('age'), B[k]['v'] - A[k]['v']) for k in A if A[k]['v'] != B[k]['v']]
mat = [m for m in mov if (m[1] or 0) >= 24]
print('movers vs C32R:', len(mov), 'mature movers:', len(mat))
print('totals C32R %d  ORDER C %d  delta %+d' % (sum(r['v'] for r in A.values()),
                                                 sum(r['v'] for r in B.values()),
                                                 sum(r['v'] for r in B.values()) - sum(r['v'] for r in A.values())))
