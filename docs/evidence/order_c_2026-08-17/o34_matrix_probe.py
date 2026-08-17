#!/usr/bin/env python3
"""Where do the two corrected sites bite in the walk-forward? Compare vpath rows 32R vs O34 and
summarize by position/age; print madden and the biggest matrix movers."""
import json
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
A = {r['key']: r for r in json.load(open(SP + '/per_entrant_O32RFINAL.json'))['recs']}
B = {r['key']: r for r in json.load(open(SP + '/per_entrant_O34FINAL.json'))['recs']}
mov = []
for k, ra in A.items():
    rb = B[k]
    va, vb = ra.get('vpath') or [], rb.get('vpath') or []
    d = sum(abs((x or 0) - (y or 0)) for x, y in zip(va, vb))
    if d > 0:
        mov.append((d, k, ra.get('pos'), ra.get('age_draft'), va, vb))
print('matrix rows with any vpath movement: %d of %d' % (len(mov), len(A)))
by_pos = {}
for d, k, pos, agd, va, vb in mov:
    by_pos.setdefault(pos, [0, 0.0])
    by_pos[pos][0] += 1
    by_pos[pos][1] += d
print('by pos:', {p: (n, round(s)) for p, (n, s) in sorted(by_pos.items())})
for d, k, pos, agd, va, vb in sorted(mov, reverse=True)[:12]:
    print('%8.0f %-24s %-4s age_draft %s' % (d, k, pos, agd))
    print('          32R %s' % [round(x) if x is not None else None for x in va[:8]])
    print('          O34 %s' % [round(x) if x is not None else None for x in vb[:8]])
k = 'nick-madden'
print('madden yrs', A[k].get('yrs'))
print('  32R', [round(x) if x is not None else None for x in A[k]['vpath']])
print('  O34', [round(x) if x is not None else None for x in B[k]['vpath']])
