import json, collections
B = json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))
A = B['active']
print('n active', len(A))
print('sum v', sum(x['v'] for x in A))
for k in ('mraz', 'ludowyke', 'uwland'):
    for x in A:
        if k in x['key']:
            print(k, {f: x.get(f) for f in ('key', 'name', 'club', 'pk', 'ep', 'ty', 'grp', 'gf', 'age',
                                            'yr', 'g', 'cg', 'v', 'vPrev', 'track', 'unpl', 'cat')})
# year-1 cohort = drafted 2025 (yr field = draft year)
yrs = collections.Counter(x['yr'] for x in A)
print('draft years', sorted(yrs.items())[-8:])
