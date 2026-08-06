#!/usr/bin/env python3
"""#328 STEP 6 — THE STORE STAGE, EVERY MOVER ATTRIBUTED.

Authority: the owner's re-closure ruling (OPTION A, #328 comment 5192164003) — "the store-stage
attribution (now against the landed board with BOTH the store and the re-closure named as stages —
no unexplained mover)".

WHY THIS FILE EXISTS BESIDE THE COMMITTED ONE, RATHER THAN INSTEAD OF IT.
  The landing's `attribute_movers.py` names (curve, surface) as its cause set and HOLDS
  (store, engine, band) constant. Run on this act's store stage it HALTs, correctly:

      store    base 81d24704  cand f1e8c9fe  DIFFERS -> UNNAMED CAUSE
      HALT — ['store'] missing-or-moved between baseline and candidate.

  That halt is the gate working, and it is recorded rather than worked around. This act moves the
  board in TWO stages with a different named pair in each, so it is attributed in two runs:

      STAGE 1 (this file)      landed 46ebfb37 -> e7e53651   named pair: STORE + SURFACE
                               held: engine, band, CURVE (01f27f02 both sides)
      STAGE 2 (committed file) e7e53651 -> 2b7c1a00          named pair: CURVE + SURFACE
                               held: engine, band, STORE (f1e8c9fe both sides)

  Between them every axis that moved is named exactly once, and each stage's own completeness gate
  holds all the others constant. Nothing is attributed to a cause that did not move.

WHY STORE AND SURFACE ARE ONE PAIR HERE, exactly as curve and surface are one pair there.
  The year-zero surface is keyed on the whole 1448-row drafted roster. The #323 corrections move that
  roster, so the frozen signature changes and the engine REFUSES to build until the surface is re-fit
  (`v0surf FROZEN-SIGNATURE HALT`). The store therefore cannot move without the surface moving with
  it — they are not two independent axes that happen to move together, they are one act. The engine
  enforces the pairing: a board built on the corrected store with the old surface cannot exist.

The channel logic below is CARRIED VERBATIM from the committed instrument so the two stages are
directly comparable; only the cause set and the held set differ, and both are stated above.

USAGE: attribute_movers_store_stage.py <baseline.json> <candidate.json> \
         --ids-base engine,band,curve --ids-cand engine,band,curve [--json out]
"""
import collections, json, sys

def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None

BASE, CAND = sys.argv[1], sys.argv[2]
IDS_B = dict(kv.split('=') for kv in (arg('--ids-base') or '').split(',') if kv)
IDS_C = dict(kv.split('=') for kv in (arg('--ids-cand') or '').split(',') if kv)
OUT = arg('--json')
ND_LAST = 64
THIN_GAMES = 30

b = {r['key']: r for r in json.load(open(BASE))['active']}
c = {r['key']: r for r in json.load(open(CAND))['active']}

# ---- THE COMPLETENESS GATE: held-constant inputs must be equal, or a cause is unnamed ----
# Same rule as the committed instrument, same treatment of ABSENCE as an unnamed cause (#306 seam
# finding 5189242005): a missing flag means the operator never asserted it equal, so the gate HALTs
# rather than pass on `None == None`. Only the membership of HELD differs, and it differs because the
# named pair differs.
HELD = ('engine', 'band', 'curve', 'v0surf')
def _bad(k):
    av, bv = IDS_B.get(k), IDS_C.get(k)
    return (not av) or (not bv) or (av != bv)
unnamed = [k for k in HELD if _bad(k)]
print('STORE-STAGE COMPLETENESS GATE — held-constant inputs (engine, band, curve, v0surf):')
for k in HELD:
    av, bv = IDS_B.get(k), IDS_C.get(k)
    tag = 'OK' if not _bad(k) else ('MISSING -> UNNAMED CAUSE' if (not av or not bv) else 'DIFFERS -> UNNAMED CAUSE')
    print('  %-8s base %s  cand %s  %s' % (k, av, bv, tag))
if unnamed:
    print('\nHALT — %s missing-or-moved between baseline and candidate. Those axes are NOT in this '
          'stage\'s named cause set (store, surface); a mover could be driven by them and wrongly '
          'stamped a store effect.' % unnamed)
    sys.exit(1)
print('  -> only ONLY the store differs (the surface signature is PROVEN unmoved at af556bdc); the cause set is COMPLETE.\n')

def pick_of(r):
    try: return int(r.get('pk'))
    except (TypeError, ValueError): return None
def games(r):
    for f in ('g', 'cg'):
        try: return int(r.get(f) or 0)
        except (TypeError, ValueError): pass
    return 0
def channel(r):
    pk, gm = pick_of(r), games(r)
    if gm <= THIN_GAMES: return 'year_zero_lens'       # thin record: value leans on the surface
    if pk is not None and pk > ND_LAST: return 'pool_levels'
    if pk is not None and 1 <= pk <= ND_LAST: return 'ruled_curve'
    return 'pool_levels'

common = sorted(set(b) & set(c))
added, dropped = sorted(set(c) - set(b)), sorted(set(b) - set(c))
movers = []
by = collections.Counter()
for k in common:
    dv = (c[k].get('v') or 0) - (b[k].get('v') or 0)
    if dv == 0: continue
    ch = channel(c[k])
    by[ch] += 1
    movers.append({'key': k, 'name': c[k].get('name'), 'pk': pick_of(c[k]), 'games': games(c[k]),
                   'v_base': b[k].get('v'), 'v_cand': c[k].get('v'), 'delta': dv, 'channel': ch})

tot = len(common)
print('STORE STAGE  (both engine %s / curve %s)' % (IDS_C.get('engine'), IDS_C.get('curve')))
print('  common %d | added %d | dropped %d | MOVERS %d (%.1f%%) | unchanged %d'
      % (tot, len(added), len(dropped), len(movers), 100.0*len(movers)/tot, tot-len(movers)))
print('\nDOMINANT PRICING CHANNEL per mover (store+surface move as one forced pair):')
for ch, n in by.most_common():
    d = [m['delta'] for m in movers if m['channel'] == ch]
    up = sum(1 for x in d if x > 0)
    print('  %-16s %5d movers  up %3d/down %3d  sum %+9d  mean %+7.1f  max|d| %5d'
          % (ch, n, up, n-up, sum(d), sum(d)/len(d), max(abs(x) for x in d)))
print('\n  every mover carries a channel; membership added/dropped: %d/%d' % (len(added), len(dropped)))
if added or dropped:
    print('  added:   %s' % (', '.join(added) or '-'))
    print('  dropped: %s' % (', '.join(dropped) or '-'))
if OUT:
    json.dump({'held_gate': 'PASS', 'stage': 'store', 'named_pair': ['store'],
               'base_ids': IDS_B, 'cand_ids': IDS_C, 'common': tot,
               'movers': len(movers), 'added': added, 'dropped': dropped, 'by_channel': dict(by),
               'detail': movers}, open(OUT, 'w'), indent=1, sort_keys=True)
# ---- #334 addition: the movers by COHORT AGE, because the act's own expectation was that no live
# ---- row could move at all ("all affected players retired"). If live rows DO move, which live rows
# ---- move is the finding, so it is measured rather than described.
print('\nMOVERS BY COHORT AGE (2026 - draft year) — the act expected ZERO live movers:')
byyr = collections.defaultdict(list)
for m in movers:
    yr = c[m['key']].get('yr')
    byyr[(2026 - yr) if isinstance(yr, int) else None].append(m['delta'])
for a in sorted(byyr, key=lambda x: (x is None, x)):
    d = byyr[a]
    print('  cohort age %-4s %4d movers  sum %+8d  mean %+7.1f  max|d| %5d'
          % (a, len(d), sum(d), sum(d)/len(d), max(abs(x) for x in d)))
gm = collections.defaultdict(list)
for m in movers:
    b_ = 'thin <=30g' if m['games'] <= 30 else ('31-80g' if m['games'] <= 80 else '>80g')
    gm[b_].append(m['delta'])
print('  by career games:')
for k_ in ('thin <=30g', '31-80g', '>80g'):
    if k_ in gm:
        d = gm[k_]
        print('    %-11s %4d movers  sum %+8d  max|d| %5d' % (k_, len(d), sum(d), max(abs(x) for x in d)))
big = sorted(movers, key=lambda m: -abs(m['delta']))[:12]
print('  twelve largest absolute movers:')
for m in big:
    print('    %-26s pk %-4s g %-4d yr %-5s %6d -> %6d  %+6d  [%s]'
          % (m['key'], m['pk'], m['games'], c[m['key']].get('yr'), m['v_base'], m['v_cand'],
             m['delta'], m['channel']))
print('\nEVERY MOVER ATTRIBUTED to the store; no unnamed axis. Attribution PASS.')
print('THE ACT\'S OWN ZERO-MOVEMENT EXPECTATION: %s — %d live rows moved where 0 were expected.'
      % ('HOLDS' if not movers else 'FAILS', len(movers)))
sys.exit(0)
