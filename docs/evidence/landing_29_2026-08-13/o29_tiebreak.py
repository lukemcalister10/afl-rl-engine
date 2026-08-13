#!/usr/bin/env python3
"""ORDER 29 -- STEP 3 RESUMED: THE RULING-C -1-POINT-PER-PICK ORDERING TIEBREAK.

Owner ruling (word "C", #334 comment 5279364952): strict descent (RULEBOOK law 4 / G-MONO) STANDS
UNAMENDED.  Each PAVA-pooled plateau in the ruled curve is instead separated by the -1-point-per-pick
ordering tiebreak -- the register's named house convention ("an ordering tiebreak below data
resolution, conceded as such, not measured precision").

  * every pooled block becomes a strictly descending run stepping by EXACTLY 1 point per pick;
  * the anchoring is chosen to preserve the block's PLAIN SUM as closely as integers allow, and the
    residual drift is PRINTED per block and in total -- never absorbed;
  * strict descent is then asserted GLOBALLY over 1..64 including every join into and out of a block;
    an anchoring that would break a join is shifted MINIMALLY and the extra drift is printed;
  * pick 1 = 3000 is untouched (the plateaus are interior).

This script does NOT install the artifact.  usage: python3 o29_tiebreak.py <out.json>
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = HERE + '/pvc_curve_v2_CANDIDATE.json'
OUT = sys.argv[1]

LOG = []
def P(s=''):
    print(s); LOG.append(s)

art = json.loads(open(CAND).read(), object_pairs_hook=collections.OrderedDict)
cur = {int(k): int(v) for k, v in art['curve'].items()}
N = max(cur)

P("=" * 112)
P("ORDER 29  --  STEP 3 RESUMED: THE RULING-C -1-POINT-PER-PICK ORDERING TIEBREAK")
P("=" * 112)
P()
P("  ruling            #334 comment 5279364952, owner word \"C\"")
P("  strict descent    STANDS UNAMENDED -- no assert relaxed, _split_ladder untouched")
P("  candidate         %s   curve_md5 %s" % (os.path.basename(CAND), art['curve_md5']))
assert art['curve_md5'] == '48046e2b', 'wrong candidate: %r' % art['curve_md5']
assert min(cur) == 1 and N == 64 and len(cur) == 64
assert cur[1] == 3000

# ---------------------------------------------------------------- 1. re-derive EVERY plateau block
P()
P("1. THE PLATEAU BLOCKS, RE-DERIVED FROM THE ARTIFACT (not assumed)")
P("-" * 112)
blocks = []
i = 1
while i <= N:
    j = i
    while j < N and cur[j + 1] == cur[i]:
        j += 1
    if j > i:
        blocks.append((i, j, cur[i]))
    i = j + 1
P("  blocks found      %d" % len(blocks))
for (a, b, v) in blocks:
    P("    picks %2d-%-2d  L=%d  pooled value %d   plain sum %d" % (a, b, b - a + 1, v, (b - a + 1) * v))
_steps = [k for k in range(1, N) if cur[k] == cur[k + 1]]
P("  plateau STEPS (what G-MONO counts): %d at picks %s" % (len(_steps), _steps))
P("  NOTE: the stop doc's shorthand named 'picks 6-11' and 'picks 15-20'; the artifact's own blocks")
P("        are picks 6-12 and 15-21 (SEVEN picks each).  The assert printed only its first 8 offending")
P("        LEFT indices, which truncates each 7-pick block to 6.  ORDER 28 SS5.2's published wording")
P("        ('picks 6-12 pool to 1319.1 and picks 15-21 pool to 812.2') agrees with the artifact.")
P("        The tiebreak is applied to the RE-DERIVED blocks, so the shorthand cannot short-change one.")

# ---------------------------------------------------------------- 2. the tiebreak, sum-preserving
P()
P("2. THE TIEBREAK, ANCHORED TO PRESERVE EACH BLOCK'S PLAIN SUM")
P("-" * 112)
P("  A block of L picks at pooled value v becomes  a, a-1, ..., a-(L-1).")
P("  Its sum is L*a - L(L-1)/2, so the sum-preserving anchor is a* = v + (L-1)/2, rounded to int.")
P("  For ODD L that is exact (the run is centred on v); for even L the best integer leaves +-L/2.")
P()
new = dict(cur)
rows = []
for (a, b, v) in blocks:
    L = b - a + 1
    plain = L * v
    ideal = v + (L - 1) / 2.0
    anch = int(round(ideal))
    # nudge to the better of floor/ceil on the plain sum (round() ties are not sum-optimal by fiat)
    best = min((abs((L * c - L * (L - 1) // 2) - plain), c)
               for c in (int(ideal), int(ideal) + 1, anch))[1]
    anch = best
    # ---- joins: top strictly below the northern neighbour, bottom strictly above the southern one
    north = cur[a - 1] if a > 1 else None
    south = cur[b + 1] if b < N else None
    shift = 0
    while True:
        top = anch + shift
        bot = top - (L - 1)
        okN = (north is None) or (top < north)
        okS = (south is None) or (bot > south)
        if okN and okS:
            break
        if not okN:
            shift -= 1
        elif not okS:
            shift += 1
        assert abs(shift) <= L, 'join cannot be satisfied for block %d-%d by shifting' % (a, b)
    anch += shift
    vals = [anch - t for t in range(L)]
    got = sum(vals)
    for t, k in enumerate(range(a, b + 1)):
        new[k] = vals[t]
    rows.append(dict(a=a, b=b, L=L, v=v, plain=plain, anchor=anch, shift=shift, got=got,
                     drift=got - plain, north=north, south=south, top=vals[0], bot=vals[-1],
                     maxmove=max(abs(x - v) for x in vals)))
    P("  block picks %2d-%-2d  L=%d  v=%4d" % (a, b, L, v))
    P("      anchor          %d%s" % (anch, "   (JOIN SHIFT %+d applied)" % shift if shift else "   (no join shift needed)"))
    P("      values          %s" % ' > '.join(str(x) for x in vals))
    P("      plain sum       %d -> %d      RESIDUAL DRIFT %+d point(s)" % (plain, got, got - plain))
    P("      join north      pick %d = %s  >  pick %d = %d   %s"
      % (a - 1, north, a, vals[0], "OK" if north is None or north > vals[0] else "VIOLATED"))
    P("      join south      pick %d = %d  >  pick %d = %s   %s"
      % (b, vals[-1], b + 1, south, "OK" if south is None or vals[-1] > south else "VIOLATED"))
    P("      max move on any single pick in the block   %+d point(s)"
      % max(abs(x - v) for x in vals))
    P()

# ---------------------------------------------------------------- 3. the drift ledger
P("3. THE TIEBREAK DRIFT LEDGER (P6's ledger gains these lines)")
P("-" * 112)
plain_pre = sum(cur.values()); plain_post = sum(new.values())
P("  %-14s %4s %8s %10s %10s %8s %9s" % ("block", "L", "pooled", "sum pre", "sum post", "drift", "max|move|"))
for r in rows:
    P("  picks %2d-%-6d %4d %8d %10d %10d %+8d %9d"
      % (r['a'], r['b'], r['L'], r['v'], r['plain'], r['got'], r['drift'], r['maxmove']))
tot_drift = sum(r['drift'] for r in rows)
P("  %-14s %4s %8s %10d %10d %+8d" % ("TOTAL (blocks)", '', '', sum(r['plain'] for r in rows),
                                      sum(r['got'] for r in rows), tot_drift))
P()
P("  whole curve plain sum   %d -> %d   drift %+d point(s)  = %+.6f%%"
  % (plain_pre, plain_post, plain_post - plain_pre, 100.0 * (plain_post - plain_pre) / plain_pre))
P("  bound declared in the ruling: total distortion <= ~0.03%% on the plain sum   %s"
  % ("HELD" if abs(plain_post - plain_pre) / plain_pre <= 3e-4 else "BREACH"))
_mx = max(abs(new[k] - cur[k]) for k in cur)
P("  bound declared in the ruling: <= ~5 points on any single pick   MEASURED %d   %s"
  % (_mx, "HELD" if _mx <= 5 else "BREACH"))
P("  join shifts applied     %d block(s)   extra drift from joins  %+d"
  % (sum(1 for r in rows if r['shift']), sum(r['drift'] for r in rows if r['shift'])))
P("  anchor (pick 1)         %d -> %d   %s" % (cur[1], new[1], "UNTOUCHED" if cur[1] == new[1] else "MOVED"))

# ---------------------------------------------------------------- 4. G-MONO, globally, joins included
P()
P("4. STRICT DESCENT ASSERTED GLOBALLY OVER 1..64, JOINS INCLUDED")
P("-" * 112)
bad = [k for k in range(1, N) if not new[k] > new[k + 1]]
P("  non-strict steps over 1..64   %d   %s" % (len(bad), bad or 'none'))
assert not bad, 'G-MONO would still fail at %s' % bad
asc = [k for k in range(1, N) if new[k + 1] > new[k]]
assert not asc
joinchecks = []
for r in rows:
    if r['a'] > 1: joinchecks.append((new[r['a'] - 1] > new[r['a']], 'in  %d->%d' % (r['a'] - 1, r['a'])))
    if r['b'] < N: joinchecks.append((new[r['b']] > new[r['b'] + 1], 'out %d->%d' % (r['b'], r['b'] + 1)))
P("  block joins checked           %d   all strict: %s"
  % (len(joinchecks), all(x[0] for x in joinchecks)))
for ok, nm in joinchecks:
    P("      join %-12s %s" % (nm, "STRICT" if ok else "VIOLATED"))
assert all(x[0] for x in joinchecks)
assert new[1] == 3000
P("  pick 1 == 3000                %s" % (new[1] == 3000))
P("  domain 1..64, 64 entries      %s" % (min(new) == 1 and max(new) == 64 and len(new) == 64))
P()
P("  ** THE TIEBROKEN CURVE IS STRICTLY DECREASING OVER 1..64.  G-MONO CAN NOW PASS ON LOAD. **")

# ---------------------------------------------------------------- 5. P5 re-scored against the ruling
P()
P("5. PREREG P5's SPOT VALUES, RE-SCORED UNDER RULING C")
P("-" * 112)
SPOT = {1: 3000, 2: 2668, 3: 2569, 5: 1804, 7: 1319, 10: 1319, 15: 812, 20: 812,
        30: 607, 40: 479, 50: 274, 64: 179}
held, breached = [], []
for k in sorted(SPOT):
    ok = new[k] == SPOT[k]
    (held if ok else breached).append(k)
    P("      pick %-3d predicted %5d   shipped %5d   %s%s"
      % (k, SPOT[k], new[k], "HELD" if ok else "BREACHED BY CONSTRUCTION",
         "" if ok else "   (inside a pooled block: the tiebreak separates it)"))
P()
P("  P5 spot values HELD      %d/%d  %s" % (len(held), len(SPOT), held))
P("  P5 spot values BREACHED  %d/%d  %s  -- BY CONSTRUCTION under ruling C, owned in the packet"
  % (len(breached), len(SPOT), breached))
assert set(breached) <= {7, 10, 15, 20}, 'unexpected P5 breach outside the pooled blocks: %s' % breached

# ---------------------------------------------------------------- 6. compose
art['curve'] = collections.OrderedDict((str(k), new[k]) for k in sorted(new))
art['curve_md5'] = hashlib.md5(
    json.dumps(art['curve'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]
art['r104_9_strict_descent'] = True
art['r104_9_strict_descent_scope'] = (
    'the national curve domain 1-64 (63 strict steps, no plateaus). TRUE BY MEASUREMENT on this '
    'artifact, re-checked not assumed: the weighted-PAVA step (Ruling C) pooled picks 6-12 to 1319 '
    'and picks 15-21 to 812, and the owner\'s -1-point-per-pick ORDERING TIEBREAK (ruling "C", #334 '
    'comment 5279364952) separates each pooled block into a strictly descending run, anchored to '
    'preserve the block\'s plain sum (residual drift 0 on both blocks; printed in the conservation '
    'ledger, never absorbed). Strict descent is asserted globally over 1..64 including both joins '
    'into and out of each block. The pool index is one value, not an ordering, so no monotonicity '
    'applies to it.')
art['ordering_tiebreak'] = collections.OrderedDict([
    ('_doc', 'RULING C (owner word "C", #334 comment 5279364952, 2026-08-13). Strict descent '
             '(RULEBOOK law 4 / G-MONO) stands UNAMENDED; the PAVA-pooled plateaus are separated by '
             'the register\'s named house convention -- "an ordering tiebreak below data resolution, '
             'conceded as such, not measured precision". Where the data cannot separate two picks, a '
             'higher pick still never prices below a lower one. This is an ORDERING convention, NOT a '
             'claim of measured precision at 1-point resolution.'),
    ('convention', '-1 point per pick within each pooled block'),
    ('anchoring', 'the integer anchoring that preserves the block plain sum as closely as integers allow; '
                  'shifted minimally if a block join would otherwise be non-strict'),
    ('pre_tiebreak_curve_md5', '48046e2b'),
    ('blocks', [collections.OrderedDict([
        ('picks', '%d-%d' % (r['a'], r['b'])), ('n', r['L']), ('pooled_value', r['v']),
        ('values', [r['top'] - t for t in range(r['L'])]),
        ('plain_sum_pre', r['plain']), ('plain_sum_post', r['got']), ('residual_drift', r['drift']),
        ('join_shift', r['shift']), ('max_move_on_a_pick', r['maxmove'])]) for r in rows]),
    ('total_residual_drift', tot_drift),
    ('curve_plain_sum_pre', plain_pre), ('curve_plain_sum_post', plain_post),
    ('curve_plain_sum_drift_pct', round(100.0 * (plain_post - plain_pre) / plain_pre, 8)),
    ('max_move_on_any_pick', _mx),
    ('prereg_P5_spot_values_breached', breached),
])
json.dump(art, open(OUT, 'w'), indent=1)
P()
P("  written: %s" % OUT)
P("  curve_md5  %s -> %s" % ('48046e2b', art['curve_md5']))
P("  r104_9_strict_descent = True   -- and TRUE BY MEASUREMENT, re-checked above, not assumed")
open(HERE + '/TIEBREAK29_out.txt', 'w').write("\n".join(LOG) + "\n")
json.dump({'blocks': rows, 'total_drift': tot_drift, 'plain_pre': plain_pre, 'plain_post': plain_post,
           'max_move': _mx, 'P5_held': held, 'P5_breached': breached,
           'curve_md5_pre': '48046e2b', 'curve_md5_post': art['curve_md5'],
           'curve': {str(k): new[k] for k in sorted(new)}},
          open(HERE + '/TIEBREAK29.json', 'w'), indent=1)
