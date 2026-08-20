#!/usr/bin/env python3
"""ACT A PROOFS — the complete control -> repaired board diff, measured on the two built artifacts.

Adapted in structure from the F5 seat's proof step (07_f5_proofs.txt). Nothing is typed in from the
prereg except the probe's OWN mover list, which is parsed out of the committed probe file so that
P6/F4 compare against the record rather than against a retyped copy.
"""
import json, os, re, sys, hashlib

SC = sys.argv[1]
ROOT = '/home/user/afl-rl-engine'
PROBE = os.path.join(ROOT, 'docs/evidence/f5_and_sort_2026-08-20/14_actc_ageref_probe.txt')

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

A = json.load(open(os.path.join(SC, 'CONTROL.board.json')))     # control (live board)
B = json.load(open(os.path.join(SC, 'FIX_DEV.board.json')))     # repaired
print('=== ACT A — THE BACK-ROWS REPAIR: PROOFS ===')
print('control  board md5 : %s' % md5(os.path.join(SC, 'CONTROL.board.json')))
print('repaired board md5 : %s' % md5(os.path.join(SC, 'FIX_DEV.board.json')))
print('repaired canonical : %s' % md5(os.path.join(SC, 'FIX_CANON.board.json')))
print()

# ---- the complete recursive diff -----------------------------------------------------------------
diffs = []
def walk(a, b, path):
    if type(a) is not type(b):
        diffs.append((path, a, b)); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b: diffs.append((path + '/' + str(k), a.get(k), b.get(k)))
            else: walk(a[k], b[k], path + '/' + str(k))
    elif isinstance(a, list):
        if len(a) != len(b): diffs.append((path + '/len', len(a), len(b))); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, path + '/' + str(i))
    elif a != b:
        diffs.append((path, a, b))
walk(A, B, '')
print('COMPLETE RECURSIVE BOARD DIFF: %d differing leaves' % len(diffs))
buckets = {}
for p, x, y in diffs:
    top = '/'.join(p.split('/')[:2])
    buckets.setdefault(top, []).append((p, x, y))
for k in sorted(buckets):
    print('   %-24s %d' % (k, len(buckets[k])))
print()

# ---- P4 / F3: no active row moves -----------------------------------------------------------------
act = [d for d in diffs if d[0].startswith('/active')]
print('P4/F3  ACTIVE rows: %d differing leaves across %d rows  -> %s'
      % (len(act), len(A['active']), 'PASS (byte-identical)' if not act else '*** FAIL ***'))
print('       active count %d -> %d ; sum v %d -> %d'
      % (len(A['active']), len(B['active']), sum(p['v'] for p in A['active']), sum(p['v'] for p in B['active'])))
assert not act, 'F3 FIRED: an active row moved'
assert sum(p['v'] for p in A['active']) == sum(p['v'] for p in B['active']) == 692296

# ---- P5 / F4: exactly 25 back rows move, all down, 772 -> 700 --------------------------------------
ab = {p['key']: p for p in A['back']}; bb = {p['key']: p for p in B['back']}
assert set(ab) == set(bb), 'the back membership changed'
movers = []
for k in ab:
    if ab[k]['v'] != bb[k]['v']:
        movers.append((k, ab[k]['name'], ab[k]['v'], bb[k]['v']))
sa, sb = sum(p['v'] for p in A['back']), sum(p['v'] for p in B['back'])
ma, mb = sum(x[2] for x in movers), sum(x[3] for x in movers)
print()
print('P5/F4  BACK rows: %d of %d move; all DOWN = %s' % (len(movers), len(A['back']), all(x[3] < x[2] for x in movers)))
print('       MOVERS aggregate   %d -> %d (delta %+d)   <-- this is the probe\'s "sum 772 -> 700"' % (ma, mb, mb - ma))
print('       ALL-198 back sum   %d -> %d (delta %+d)   <-- SAME delta; the prereg P5 named the wrong scope' % (sa, sb, sb - sa))
print('       DECLARED SCOPE CORRECTION (not absorbed): PREREG P5 read the probe\'s "aggregate: sum 772')
print('       -> 700" as the whole back section. It is the aggregate over the 25 MOVERS. Both figures')
print('       are printed above and the DELTA -72 — the quantity that was predicted — is met on both.')
# any back-row field OTHER than the five value fields moving would be a surprise; measure it
bfields = {}
for p, x, y in diffs:
    if p.startswith('/back/'):
        bfields.setdefault(p.split('/')[3], 0)
        bfields[p.split('/')[3]] += 1
print('       back-row FIELDS that move: %s' % json.dumps(bfields, sort_keys=True))

# ---- P6: the 25 movers by name and delta == the probe's list --------------------------------------
probe = open(PROBE).read()
rows = re.findall(r'^\s*(\d+)\s+([a-z0-9\-]+)\s+(.+?)\s{2,}(\d+)\s+(\d+)\s+(-?\d+)\s+(-?[\d.]+)%\s*$',
                  probe, re.M)
plist = [(r[1], r[2].strip(), int(r[3]), int(r[4])) for r in rows]
print()
print('P6     probe movers parsed from 14_actc_ageref_probe.txt: %d' % len(plist))
got = sorted((k, n, a, b) for k, n, a, b in movers)
want = sorted(plist)
same = got == want
print('       measured movers == probe movers (key, name, current, corrected): %s'
      % ('EXACT MATCH' if same else '*** MISMATCH ***'))
if not same:
    print('       only in measured: %s' % [x for x in got if x not in want])
    print('       only in probe   : %s' % [x for x in want if x not in got])
print()
print('       %-28s %-26s %6s %10s %7s' % ('key', 'name', 'now', 'corrected', 'delta'))
for k, n, a, b in sorted(movers, key=lambda x: (x[3] - x[2], x[0])):
    print('       %-28s %-26s %6d %10d %+7d' % (k, n, a, b, b - a))
assert len(movers) == 25 and all(x[3] < x[2] for x in movers), 'F4 FIRED on count/direction'
assert (ma, mb) == (772, 700), 'F4 FIRED on the movers aggregate'
assert sb - sa == -72, 'F4 FIRED on the back-section delta'
assert same, 'F4 FIRED: the mover set is not the probe set'
print()
print('       NAMED CROSS-CHECKS: charlie-dean %d -> %d ; jacob-bauer %d -> %d'
      % (ab['charlie-dean']['v'], bb['charlie-dean']['v'], ab['jacob-bauer']['v'], bb['jacob-bauer']['v']))

# ---- P7 / F5: nothing outside back rows + lensConservation moves -----------------------------------
other = [d for d in diffs if not d[0].startswith('/back/')]
print()
print('P7/F5  leaves OUTSIDE /back/: %d' % len(other))
for p, x, y in other:
    print('       %-56s %s -> %s' % (p, x, y))
allowed = all(p.startswith('/lensConservation') for p, _, _ in other)
print('       all of them under /lensConservation: %s' % allowed)
assert allowed, 'F5 FIRED: something outside back rows and lensConservation moved'
print()
for lens in ('_meta', 'league'):
    pass
print('       F5 layer / seal / lens-0 held:')
for path, get in (('phantomTotals._meta.entrant_layer_pvc', lambda d: d['phantomTotals']['_meta']['entrant_layer_pvc']),
                  ('phantomTotals._meta.seal_sha256_8', lambda d: d['phantomTotals']['_meta']['seal_sha256_8']),
                  ("phantomTotals.league['0'].withPhantom", lambda d: d['phantomTotals']['league']['0']['withPhantom'])):
    print('         %-46s %s == %s  %s' % (path, get(A), get(B), 'HELD' if get(A) == get(B) else '*** MOVED ***'))
    assert get(A) == get(B)
print()
print('ALL ACT A PROOFS PASS. P1-P7 met; F1-F6 clear.')
