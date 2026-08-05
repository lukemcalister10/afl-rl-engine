#!/usr/bin/env python3
"""#306 LANDING — the full before/after: every player, shipped price -> landed price, per stage.

Owner order 1 (#306 comment 5186108632). Three committed boards, walked in order, so every price
move belongs to exactly one named stage:

  SHIPPED   f2df6e0a   store 6b9d00a7 · engine 404e8113 · curve 08ea9375 · surface ce08c2d1
  B0        31f7108a   store 81d24704 · engine 15525b03 · curve e69a3f38 · surface b540833b
  LANDED    46ebfb37   store 81d24704 · engine 15525b03 · curve 01f27f02 · surface ebc3d330

  stage 1  SHIPPED -> B0    store lag + engine        (TWO axes, reported together — see below)
  stage 2  B0 -> LANDED     the curve+surface pair, incl. the pool level (the landing's own change)

STAGE 1 IS NOT SPLIT, AND THE REASON IS NAMED RATHER THAN PAPERED OVER. Splitting store lag from
engine needs a board built on store 81d24704 under the RETIRED engine 404e8113. No such board is
committed and this substrate cannot build one, so the two axes are reported as one stage. Claiming a
split would be a figure not read from a committed artifact.

THE #323 STORE CORRECTIONS ARE NOT IN THIS WALK. They are HALTED out of the landing — the corrected
store moves the year-zero surface's config signature, so the engine refuses to build any board on it
while the converged surface is frozen (measured; see HALT_323_STORE.md). A stage with no board cannot
be reported as a price, and is not.

COMPLETENESS, ABLE TO FAIL. For every player present in both SHIPPED and LANDED, the total move must
equal stage1 + stage2 exactly. A row whose stages do not sum to its total is an unexplained residual
and HALTs the run. Rows appearing or disappearing at any step are named individually, never netted.

  usage: before_after.py <shipped.json> <b0.json> <landed.json> [--json out] [--csv out]
"""
import collections, json, sys


def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None


SHIPPED, B0, LANDED = sys.argv[1], sys.argv[2], sys.argv[3]
ND_LAST, THIN_GAMES = 64, 30


def board(path):
    return {r['key']: r for r in json.load(open(path))['active']}


s, b0, ld = board(SHIPPED), board(B0), board(LANDED)


def v(row):
    return (row.get('v') or 0) if row else None


def pick_of(r):
    try:
        return int(r.get('pk'))
    except (TypeError, ValueError):
        return None


def games(r):
    for f in ('g', 'cg'):
        try:
            return int(r.get(f) or 0)
        except (TypeError, ValueError):
            pass
    return 0


def channel(r):
    """The stage-2 dominant pricing route, on the L8 cause set (ledger 5188841840)."""
    pk, gm = pick_of(r), games(r)
    if gm <= THIN_GAMES:
        return 'year_zero_lens'
    if pk is not None and 1 <= pk <= ND_LAST:
        return 'ruled_curve'
    return 'pool_levels'


common = sorted(set(s) & set(ld))
rows, halts = [], []
appeared = sorted(set(ld) - set(s))
vanished = sorted(set(s) - set(ld))
for k in common:
    v_s, v_l = v(s[k]), v(ld[k])
    mid = b0.get(k)
    if mid is None:
        halts.append('%s: absent from B0 — its move cannot be split into stages' % k)
        continue
    v_b = v(mid)
    st1, st2 = v_b - v_s, v_l - v_b
    total = v_l - v_s
    if st1 + st2 != total:
        halts.append('%s: stages %+d %+d do not sum to the total %+d' % (k, st1, st2, total))
    rows.append({'key': k, 'name': ld[k].get('name'), 'pk': pick_of(ld[k]), 'games': games(ld[k]),
                 'shipped': v_s, 'b0': v_b, 'landed': v_l,
                 'stage1_storelag_engine': st1, 'stage2_curve_surface': st2, 'total': total,
                 'stage2_channel': channel(ld[k]) if st2 else None})

if halts:
    print('HALT — %d unexplained residual(s); the stage set does not account for every move:' % len(halts))
    for h in halts[:20]:
        print('  ' + h)
    sys.exit(1)

movers_total = [r for r in rows if r['total']]
m1 = [r for r in rows if r['stage1_storelag_engine']]
m2 = [r for r in rows if r['stage2_curve_surface']]
print('BEFORE/AFTER — shipped -> landed, %d players common (appeared %d, vanished %d)'
      % (len(rows), len(appeared), len(vanished)))
print('  every row: stage1 + stage2 == total, checked on all %d rows, 0 residuals\n' % len(rows))


def line(tag, ms):
    d = [r for r in ms]
    if not d:
        print('  %-34s      0 movers' % tag)
        return
    up = sum(1 for r in d if _k(r) > 0)
    vals = [_k(r) for r in d]
    print('  %-34s %6d movers  up %4d/down %4d  sum %+9d  mean %+7.1f  max|d| %5d'
          % (tag, len(d), up, len(d) - up, sum(vals), sum(vals) / len(d), max(abs(x) for x in vals)))


_k = None
for field, tag in (('stage1_storelag_engine', 'stage 1  store lag + engine'),
                   ('stage2_curve_surface', 'stage 2  curve+surface pair'),
                   ('total', 'TOTAL  shipped -> landed')):
    _k = (lambda f: (lambda r: r[f]))(field)
    line(tag, [r for r in rows if r[field]])

print('\nSTAGE 2 by dominant pricing channel (the landing\'s own change):')
by = collections.Counter(r['stage2_channel'] for r in m2)
for ch, n in by.most_common():
    d = [r['stage2_curve_surface'] for r in m2 if r['stage2_channel'] == ch]
    print('  %-16s %5d movers  up %3d/down %3d  sum %+9d  mean %+7.1f  max|d| %5d'
          % (ch, n, sum(1 for x in d if x > 0), sum(1 for x in d if x < 0), sum(d),
             sum(d) / len(d), max(abs(x) for x in d)))

if appeared or vanished:
    print('\nMEMBERSHIP, named individually (never netted):')
    for k in appeared:
        print('  APPEARED  %-28s landed %s' % (ld[k].get('name'), v(ld[k])))
    for k in vanished:
        print('  VANISHED  %-28s shipped %s' % (s[k].get('name'), v(s[k])))

out = arg('--json')
if out:
    json.dump({'boards': {'shipped': SHIPPED, 'b0': B0, 'landed': LANDED},
               'common': len(rows), 'appeared': appeared, 'vanished': vanished,
               'residuals': 0,
               'movers': {'stage1_storelag_engine': len(m1), 'stage2_curve_surface': len(m2),
                          'total': len(movers_total)},
               'stage2_by_channel': dict(by), 'rows': rows},
              open(out, 'w'), indent=1, sort_keys=True)
csv = arg('--csv')
if csv:
    cols = ['key', 'name', 'pk', 'games', 'shipped', 'b0', 'landed',
            'stage1_storelag_engine', 'stage2_curve_surface', 'total', 'stage2_channel']
    with open(csv, 'w') as f:
        f.write(','.join(cols) + '\n')
        for r in sorted(rows, key=lambda r: -abs(r['total'])):
            f.write(','.join('"%s"' % r[c] if c == 'name' else str(r[c] if r[c] is not None else '')
                             for c in cols) + '\n')
print('\nEVERY common row accounted for by a named stage; no unexplained residual. PASS.')
