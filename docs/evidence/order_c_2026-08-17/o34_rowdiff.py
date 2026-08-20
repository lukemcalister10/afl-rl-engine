#!/usr/bin/env python3
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
A = {r['key']: r for r in json.load(open(SP + '/o34/bb_o32ctrl/rl_after/rl_app_data.json'))['active']}
B = {r['key']: r for r in json.load(open(SP + '/o34/bb_o34diag1/rl_after/rl_app_data.json'))['active']}
for k in ('josh-smillie', 'milan-murdock'):
    ra, rb = A[k], B[k]
    ks = sorted(set(ra) | set(rb))
    diffs = [(f, ra.get(f), rb.get(f)) for f in ks if ra.get(f) != rb.get(f)]
    print(k, 'field diffs:', diffs if len(diffs) < 15 else diffs[:15])
