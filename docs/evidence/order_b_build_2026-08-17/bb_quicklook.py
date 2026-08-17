#!/usr/bin/env python3
"""ORDER B: quick board comparison across the stage legs (totals + named rows)."""
import json

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33'
TAGS = [('base(C32R)', 'off_o32'), ('leg1 ladder+s*', 'leg1'), ('leg2 +fade', 'leg2'), ('full +taper', 'full1')]
D = {t: {r['key']: r for r in json.load(open('%s/bb_%s/rl_after/rl_app_data.json' % (SP, tag)))['active']}
     for t, tag in TAGS}
names = list(D)
print('totals: ' + '  '.join('%s=%d' % (t, sum(r['v'] for r in D[t].values())) for t in names))
NAMED = ['callum-wilkie', 'peter-wright', 'harris-andrews', 'josh-battle', 'harry-mckay', 'charlie-curnow',
         'ned-moyle', 'lachlan-mcandrew', 'sam-de-koning', 'tom-de-koning', 'marcus-bontempelli',
         'jack-sinclair', 'zachary-merrett', 'isaac-heeney', 'timothy-english']
print('%-22s %-5s %3s  %8s %8s %8s %8s   %8s' % ('row', 'pos', 'age', 'base', 'leg1', 'leg2', 'full', 'd_full'))
for k in NAMED:
    if k not in D[names[0]]:
        print('%-22s (absent)' % k)
        continue
    r0 = D[names[0]][k]
    vs = [D[t][k]['v'] for t in names]
    print('%-22s %-5s %3d  %8d %8d %8d %8d   %+8d' % (k, (r0.get('gf') or r0['grp']), r0['age'],
                                                      vs[0], vs[1], vs[2], vs[3], vs[3] - vs[0]))
# cohort sums
def cohort(t, pred):
    return sum(r['v'] for r in D[t].values() if pred(r))


for label, pred in [('tall 28-30', lambda r: (r.get('gf') or r['grp']) in ('KPD', 'KPF') and 28 <= r['age'] <= 30),
                    ('tall 23-26', lambda r: (r.get('gf') or r['grp']) in ('KPD', 'KPF') and 23 <= r['age'] <= 26),
                    ('tall <=24', lambda r: (r.get('gf') or r['grp']) in ('KPD', 'KPF') and r['age'] <= 24),
                    ('non-tall 31+', lambda r: (r.get('gf') or r['grp']) not in ('KPD', 'KPF') and r['age'] >= 31),
                    ('age <=22 all', lambda r: r['age'] <= 22)]:
    print('%-14s ' % label + '  '.join('%s=%d' % (t, cohort(t, pred)) for t in names))
