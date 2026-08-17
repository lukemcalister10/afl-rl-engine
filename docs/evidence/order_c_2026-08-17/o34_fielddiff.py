#!/usr/bin/env python3
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
A = {r['key']: r for r in json.load(open(SP + '/o34/bb_o32ctrl/rl_after/rl_app_data.json'))['active']}
B = {r['key']: r for r in json.load(open(SP + '/o34/bb_final/rl_after/rl_app_data.json'))['active']}
allf = {}
for k in A:
    ra, rb = A[k], B[k]
    for f in sorted(set(ra) | set(rb)):
        if ra.get(f) != rb.get(f):
            allf.setdefault(f, 0)
            allf[f] += 1
print('fields differing across all rows:', allf)
for k in ('riley-thilthorpe', 'ned-moyle', 'milan-murdock'):
    ra, rb = A[k], B[k]
    d = [(f, ra.get(f), rb.get(f)) for f in sorted(set(ra) | set(rb)) if ra.get(f) != rb.get(f)]
    print(k, 'age', ra.get('age'), 'diffs:', d[:8])
