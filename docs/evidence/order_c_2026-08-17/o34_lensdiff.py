#!/usr/bin/env python3
"""Which fields move on age-24+ rows, and is every move a lens year at which the row was UNDER 24?"""
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
A = {r['key']: r for r in json.load(open(SP + '/o34/bb_o32ctrl/rl_after/rl_app_data.json'))['active']}
B = {r['key']: r for r in json.load(open(SP + '/o34/bb_final/rl_after/rl_app_data.json'))['active']}
OFF = {'vM1': -1, 'vM2': -2, 'vP1': +1, 'vP2': +2}
bad = []
n24 = 0
lens_moves = {'vM1': 0, 'vM2': 0, 'vP1': 0, 'vP2': 0}
for k in A:
    ra, rb = A[k], B[k]
    age = ra.get('age')
    if age is None or age < 24:
        continue
    n24 += 1
    for f in sorted(set(ra) | set(rb)):
        if ra.get(f) == rb.get(f):
            continue
        if f in OFF and (age + OFF[f]) < 24:
            lens_moves[f] += 1
            continue
        bad.append((k, age, f, ra.get(f), rb.get(f)))
print('age-24+ rows:', n24)
print('LAWFUL lens moves (lens-year age < 24):', lens_moves)
print('UNLAWFUL moves (any field incl v, or a lens year at age >= 24):', len(bad), bad[:10])
