#!/usr/bin/env python3
"""CENSUS ONLY -- the INPUTS to the declared head-fix shrink rule (cell n, position levels).
No price, no surface, no board. Reproduces the ORDER-28 ND population exactly."""
import os, sys, json, collections
HERE = '/home/user/afl-rl-engine/.claude/worktrees/agent-a8ab36345dce038ee/docs/evidence/grace_adoption_2026-08-13'
IN = os.path.join(HERE, 'inputs'); sys.path.insert(0, IN)
import harness_pvc_REPINNED_pass3 as HP
import o26b_loclin as LL
L2 = json.load(open(IN + '/LAYER2.json')); L1 = json.load(open(IN + '/layer1_player_seasons.json'))
E = {e['key']: e for e in L1['entries']}; ATTR = L2['attribution']
GA = L2['grace_a']
PICKS = list(range(1, 65)); POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
nd = [dict(key=k, pick=ATTR[k]['pick'], value=GA[k]['total'], pos=E[k]['position_group'])
      for k in L2['fit_nd_keys']]
print('ND fit rows: %d' % len(nd))
ndmean = sum(r['value'] for r in nd) / len(nd)
print('ND mean value %.4f' % ndmean)
posrows = {g: [r for r in nd if r['pos'] == g] for g in POSN}
print('\nPOSITION LEVELS (pick-blind), the ALL-IN RELATIVITY the shrink targets')
print('  %-6s %6s %12s %10s' % ('pos', 'n', 'mean_value', 'level'))
for g in POSN:
    m = sum(r['value'] for r in posrows[g]) / len(posrows[g])
    print('  %-6s %6d %12.4f %10.4f' % (g, len(posrows[g]), m, m / ndmean))

# hard per-pick counts
print('\nHARD CELL COUNTS n(pos,pick) -- picks 1..24')
cnt = collections.Counter((r['pos'], r['pick']) for r in nd)
print('  pick ' + ' '.join('%5s' % g for g in POSN) + '   all')
for p in PICKS[:24]:
    tot = sum(cnt[(g, p)] for g in POSN)
    print('  %4d ' % p + ' '.join('%5d' % cnt[(g, p)] for g in POSN) + '  %4d' % tot)

# the LL estimator's OWN effective n, per position (this is the object the rule uses)
print('\nEFFECTIVE n FROM THE LL ESTIMATOR (o26b_loclin.kernel_loclin), per position')
eff = {}
for g in POSN:
    nm = min(HP.NMIN, max(8.0, len(posrows[g]) / 4.0))
    v, e, d = LL.kernel_loclin(posrows[g], PICKS, nm, HP.HMIN, HP.HMAX)
    eff[g] = {p: float(e[i]) for i, p in enumerate(PICKS)}
    print('  %-6s nmin %5.1f   effn p1 %7.2f p2 %7.2f p3 %7.2f p4 %7.2f p10 %7.2f p20 %7.2f p30 %7.2f p40 %7.2f p64 %7.2f'
          % (g, nm, eff[g][1], eff[g][2], eff[g][3], eff[g][4], eff[g][10], eff[g][20], eff[g][30], eff[g][40], eff[g][64]))
    print('        raw LL value  p1 %8.3f p2 %8.3f p3 %8.3f p4 %8.3f p20 %8.3f p30 %8.3f' %
          (v[0], v[1], v[2], v[3], v[19], v[29]))
json.dump({'effn': eff, 'ndmean': ndmean,
           'level': {g: (sum(r['value'] for r in posrows[g]) / len(posrows[g])) / ndmean for g in POSN},
           'posn': {g: len(posrows[g]) for g in POSN},
           'hard_n': {'%s|%d' % (g, p): cnt[(g, p)] for g in POSN for p in PICKS}},
          open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/census_n.json', 'w'), indent=1)
