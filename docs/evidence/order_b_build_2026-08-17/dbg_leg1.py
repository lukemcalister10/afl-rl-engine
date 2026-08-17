import json, collections, statistics
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33'
B = {r['key']: r for r in json.load(open(SP + '/bb_off_o32/rl_after/rl_app_data.json'))['active']}
L = {r['key']: r for r in json.load(open(SP + '/bb_leg1/rl_after/rl_app_data.json'))['active']}
moved = [(k, L[k]['v'] - B[k]['v'], B[k]['v'], (B[k].get('gf') or B[k]['grp']), B[k]['age']) for k in B if L[k]['v'] != B[k]['v']]
nt = [m for m in moved if m[3] not in ('KPD', 'KPF')]
print('moved rows:', len(moved), 'non-tall moved:', len(nt))
print(collections.Counter(m[3] for m in nt))
rel = [m[1] / m[2] for m in nt if m[2] > 100]
print('non-tall rel moves: min %.3f max %.3f mean %.3f' % (min(rel), max(rel), statistics.mean(rel)))
for m in sorted(nt, key=lambda m: -abs(m[1]))[:12]:
    print(m)
byage = collections.defaultdict(lambda: [0, 0])
for m in nt:
    byage[m[4]][0] += m[1]; byage[m[4]][1] += 1
for a in sorted(byage):
    print('age', a, 'sumdelta %+d n=%d' % (byage[a][0], byage[a][1]))
