#!/usr/bin/env python3
"""#306 L8 — CANDIDATE BOARD BESIDE THE SAME-ENGINE BASELINE, EVERY MOVER ATTRIBUTED.

Authority: seam #306 comment 5188841840 (L8 cleared), terms 5188266553.

WHY THE BASELINE IS NOT THE COMMITTED RELEASED BOARD. The committed board f2df6e0a was built on store
6b9d00a7, engine 404e8113 and a different curve — FOUR axes differ from the candidate. Attributing a
4-axis diff against a curve/lens cause set would silently mislabel store/engine movement as curve/lens.
The correct baseline holds engine and store constant and moves only the landing's own inputs: the
pre-loop board B0 (curve e69a3f38 + surface b540833b) on the SAME engine 15525b03 / store 81d24704.

THE COMPLETENESS GATE (this is what makes the attribution non-vacuous). The named cause set is complete
IFF baseline and candidate differ ONLY in curve+surface. So the gate ASSERTS the held-constant
identities (store, engine, band) are equal. If any differs, that axis is an UNNAMED cause and the run
HALTs — a mover could then be store/engine-driven and wrongly stamped curve/lens. Run against a board
built on a different store/engine (e.g. the committed f2df6e0a), the gate HALTs by design.

Given the gate passes, the curve and surface are the ONLY inputs that moved, and they move as a single
FITTED PAIR (the engine enforces the match — a mixed curve/surface board cannot be built). So every
mover is a landing revaluation; the per-row breakdown below names its DOMINANT pricing channel
(national curve / pool / year-zero-dominant thin record), wide-channel-aware per the ledger.

USAGE: attribute_movers.py <baseline.json> <candidate.json> \
         --ids-base store,engine,band --ids-cand store,engine,band [--json out]
"""
import json, sys, collections

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
HELD = ('store', 'engine', 'band')
# #306 seam finding (5189242005): ABSENCE is an unnamed cause, same as DIFFERENCE. A held-constant
# identity that is missing on either side means the operator has not asserted it equal — so the gate
# must HALT, never silently pass on `None == None`. No false-PASS path when flags are omitted.
def _bad(k):
    av, bv = IDS_B.get(k), IDS_C.get(k)          # NB: not `a,b` — `b`/`c` are the board dicts below
    return (not av) or (not bv) or (av != bv)
unnamed = [k for k in HELD if _bad(k)]
print('L8 COMPLETENESS GATE — held-constant inputs (store, engine, band):')
for k in HELD:
    av, bv = IDS_B.get(k), IDS_C.get(k)
    tag = 'OK' if not _bad(k) else ('MISSING -> UNNAMED CAUSE' if (not av or not bv) else 'DIFFERS -> UNNAMED CAUSE')
    print('  %-8s base %s  cand %s  %s' % (k, av, bv, tag))
if unnamed:
    print('\nHALT — %s missing-or-moved between baseline and candidate. Those axes are NOT in the named cause set '
          '(curve, surface); a mover could be driven by them and wrongly stamped a curve/lens effect. '
          'The candidate must be compared against a baseline that holds them constant.' % unnamed)
    sys.exit(1)
print('  -> only the curve and the year-zero surface differ; the cause set is COMPLETE.\n')

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
print('CANDIDATE BESIDE BASELINE  (both engine %s / store %s)' % (IDS_C.get('engine'), IDS_C.get('store')))
print('  common %d | added %d | dropped %d | MOVERS %d (%.1f%%) | unchanged %d'
      % (tot, len(added), len(dropped), len(movers), 100.0*len(movers)/tot, tot-len(movers)))
print('\nDOMINANT PRICING CHANNEL per mover (curve+surface move as one fitted pair):')
for ch, n in by.most_common():
    d = [m['delta'] for m in movers if m['channel'] == ch]
    up = sum(1 for x in d if x > 0)
    print('  %-16s %5d movers  up %3d/down %3d  sum %+9d  mean %+7.1f  max|d| %5d'
          % (ch, n, up, n-up, sum(d), sum(d)/len(d), max(abs(x) for x in d)))
print('\n  every mover carries a channel; membership added/dropped: %d/%d' % (len(added), len(dropped)))
if OUT:
    json.dump({'held_gate': 'PASS', 'base_ids': IDS_B, 'cand_ids': IDS_C, 'common': tot,
               'movers': len(movers), 'added': added, 'dropped': dropped, 'by_channel': dict(by),
               'detail': movers}, open(OUT, 'w'), indent=1, sort_keys=True)
print('\nEVERY MOVER ATTRIBUTED to the landing curve+surface pair; no unnamed axis. PASS.')
sys.exit(0)
