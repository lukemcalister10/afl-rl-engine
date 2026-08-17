#!/usr/bin/env python
# ORDER 32 SEAT S1 — STEP 4: apply the recommended construction (C3) to the 2026 board's young rows
# and the ten named rows. READ-ONLY: this REPLICATES o31_stall_run's logic on the season table; the
# engine is not imported and not run. Replication is exact up to one disclosed gap: the engine's
# out-for-remainder register names take season-fraction 1.0 in 2026 (games test 10.0 not 9.2); the
# register is not consumed here, and the count of rows inside the affected games band [9.2,10) is
# printed so the gap is bounded, not waved at.
import json, os, collections

OUT = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(OUT, 'SEASON_TABLE.json')))
C = json.load(open(os.path.join(OUT, 'CONSTRUCTIONS_S1.json')))
ROWS = T['rows']; BARS = T['meta']['bars']; FE26 = T['meta']['fe26']
BYK = collections.defaultdict(list)
for r in ROWS: BYK[r['key']].append(r)

def bar_at(constr, pos, age):
    if constr == 'C0' or age >= 24: return BARS[pos]
    a = max(18, min(23, age))
    return C[constr]['%s|%d' % (pos, a)]

def stall_run(key, constr):
    """o31_stall_run transcribed (engine ~3319): most-recent-first over PLAYED seasons; a season with
    games>=10*u AND avg>=bar is DELIVERED and resets; gameless seasons never appear in the table."""
    s = 0
    for r in sorted(BYK[key], key=lambda r: -r['year']):
        u = r['u']
        if r['games'] >= 10.0 * u and r['avg'] >= bar_at(constr, r['pos'], r['age']): break
        s += 1
    return s

L = []; P = L.append
P('ORDER 32 S1 STEP 4 — THE RECOMMENDED CONSTRUCTION (C3) APPLIED. Replicated gate, engine untouched.')
P('')

# board-wide young-row effect (the constituency measure): 2026 played rows, career games 1-50
cg = {k: sum(r['games'] for r in v) for k, v in BYK.items()}
young = [k for k in BYK if any(r['year'] == 2026 for r in BYK[k]) and 1 <= cg[k] <= 50]
P('BOARD EFFECT — the established constituency: players who PLAYED in 2026 with 1-50 career games (n=%d)' % len(young))
for constr in ['C0', 'C1', 'C2', 'C3']:
    ss = {k: stall_run(k, constr) for k in young}
    n1 = sum(1 for v in ss.values() if v >= 1)
    P('  %s: stall-flagged (s>=1) %d/%d = %.0f%%   s distribution: ' % (constr, n1, len(young), 100*n1/len(young)) +
      ', '.join('s=%d: %d' % (v, c) for v, c in sorted(collections.Counter(ss.values()).items())))
borderline = [k for k in young for r in BYK[k] if r['year'] == 2026 and 9.2 <= r['games'] < 10.0]
P('  register gap bound: %d of these rows have 2026 games in [9.2,10) — the only band where the' % len(set(borderline)))
P('  out-for-remainder register (u=1.0) could flip this replication\'s games test: %s' % sorted(set(borderline)))
P('')

# ages of relief: who is unflagged C0->C3
rel = [k for k in young if stall_run(k, 'C0') >= 1 and stall_run(k, 'C3') == 0]
red = [k for k in young if stall_run(k, 'C3') < stall_run(k, 'C0') and stall_run(k, 'C3') >= 1]
wor = [k for k in young if stall_run(k, 'C3') > stall_run(k, 'C0')]
P('C0 -> C3 on the constituency: fully unflagged %d, run shortened (still >=1) %d, worsened %d (cap law => must be 0)'
  % (len(rel), len(red), len(wor)))
P('  fully unflagged: ' + ', '.join(sorted(rel)))
P('')

# mature guard: no 24+-only row may change under any construction (cap law + flat at 24+)
mature_changed = []
for k in BYK:
    if all(r['age'] >= 24 for r in BYK[k]):
        if stall_run(k, 'C0') != stall_run(k, 'C3'): mature_changed.append(k)
P('MATURE GUARD: rows whose every played season is age 24+ and whose s changes under C3: %d %s'
  % (len(mature_changed), mature_changed or ''))
P('')

# the named ten
NAMED = ['harry-dean', 'kye-annand', 'cooper-duff-tytler', 'alix-tauru', 'jordan-croft',
         'jedd-busslinger', 'ethan-read', 'isaac-kako', 'nick-madden', 'milan-murdock']
P('THE NAMED TEN — season by season, gate reading under C0 (flat) and C3 (recommended):')
P('  (games test: games >= 10 x u, u=%.2f for 2026; DELIVERED = games test AND avg >= bar)' % FE26)
for k in NAMED:
    rows = sorted(BYK.get(k, []), key=lambda r: r['year'])
    if not rows:
        P('%-20s NO PLAYED SEASONS in store' % k); continue
    s0, s3 = stall_run(k, 'C0'), stall_run(k, 'C3')
    P('%-20s pos %-4s   s: C0=%d -> C3=%d%s' % (k, rows[0]['pos'], s0, s3,
      '   (also C1=%d, C2=%d)' % (stall_run(k, 'C1'), stall_run(k, 'C2'))))
    for r in rows:
        u = r['u']; gt = r['games'] >= 10.0 * u
        b0, b3 = BARS[r['pos']], bar_at('C3', r['pos'], r['age'])
        v0 = 'games-FAIL' if not gt else ('avg %.1f < %.1f STALL' % (r['avg'], b0) if r['avg'] < b0 else 'DELIVERED')
        v3 = 'games-FAIL' if not gt else ('avg %.1f < %.1f STALL' % (r['avg'], b3) if r['avg'] < b3 else 'DELIVERED')
        P('     %d age %d %-4s g=%2.0f avg %5.1f | C0: %-24s | C3 bar %5.1f: %s'
          % (r['year'], r['age'], r['pos'], r['games'], r['avg'], v0, b3, v3))
open(os.path.join(OUT, 'APPLY_S1_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
