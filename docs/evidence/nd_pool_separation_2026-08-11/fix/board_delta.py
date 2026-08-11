"""ORDER 20 — THE ONE-TIME DE-CONTAMINATION DELTA on the live board.

    python3 board_delta.py <BEFORE.json> <AFTER.json> [label]

The separation law forbids a POOL CHANGE from moving ND. It does NOT forbid the one-time correction of
removing pool rows from an ND fit — but that correction MUST be quantified in full and flagged, never
buried. This file is that quantification: it reports the whole national side and the whole pool side
separately, every mover bucketed by size, the biggest movers by name, and the totals.
"""
import json, sys, collections

A = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2]))
LABEL = sys.argv[3] if len(sys.argv) > 3 else 'fix'


def is_national(r): return r.get('ty') == 'ND' and (r.get('ep') or 99) <= 64


def rows(bd):
    o = {}
    for s in ('active', 'back'):
        for r in bd.get(s) or []: o[(s, r.get('key') or r.get('name'))] = r
    return o


RA, RB = rows(A), rows(B)
P = print
P("=" * 112)
P("ORDER 20 — ONE-TIME DE-CONTAMINATION DELTA ON THE LIVE BOARD   [%s]" % LABEL)
P("  before %s" % sys.argv[1])
P("  after  %s" % sys.argv[2])
P("=" * 112)

OUT = {'label': LABEL}
for armname, pred in (('NATIONAL (ty==ND, ep<=64)', is_national),
                      ('POOL     (everything else)', lambda r: not is_national(r))):
    sub = [k for k in RA if k in RB and pred(RA[k]) and RA[k].get('v') is not None]
    mv = [(k, RA[k]['v'], RB[k]['v']) for k in sub if RA[k]['v'] != RB[k]['v']]
    tot_a = sum(RA[k]['v'] for k in sub); tot_b = sum(RB[k]['v'] for k in sub)
    buckets = collections.Counter()
    for k, x, y in mv:
        d = abs(y - x) / max(1, x) * 100
        buckets['<=1%' if d <= 1 else ('1-5%' if d <= 5 else ('5-15%' if d <= 15 else '>15%'))] += 1
    P()
    P("  %s   n=%d" % (armname, len(sub)))
    P("    movers            %d of %d  (%.1f%%)" % (len(mv), len(sub), 100.0 * len(mv) / max(1, len(sub))))
    P("    total v           %d -> %d   delta %+d  (%+.4f%%)" % (tot_a, tot_b, tot_b - tot_a,
                                                                 100.0 * (tot_b - tot_a) / max(1, tot_a)))
    P("    mover size buckets %s" % dict(buckets))
    if mv:
        big = sorted(mv, key=lambda t: -abs(t[2] - t[1]))[:15]
        P("    the 15 largest absolute movers:")
        for k, x, y in big:
            r = RA[k]
            P("      %-30s %-5s pk%-4s ep%-4s  %6d -> %6d  (%+d, %+.2f%%)"
              % (r.get('name', k[1])[:30], r.get('ty'), r.get('pk'), r.get('ep'), x, y, y - x,
                 100.0 * (y - x) / max(1, x)))
    OUT[armname.split()[0]] = {'n': len(sub), 'movers': len(mv), 'total_before': tot_a, 'total_after': tot_b,
                               'delta': tot_b - tot_a, 'pct': 100.0 * (tot_b - tot_a) / max(1, tot_a),
                               'buckets': dict(buckets),
                               'top': [{'name': (RA[k].get('name') or k[1]), 'ty': RA[k].get('ty'),
                                        'pk': RA[k].get('pk'), 'ep': RA[k].get('ep'),
                                        'before': x, 'after': y, 'delta': y - x}
                                       for k, x, y in sorted(mv, key=lambda t: -abs(t[2] - t[1]))[:40]]}

# the national pick curve itself
cm = [(pk, A['PVC'].get(str(pk)), B['PVC'].get(str(pk))) for pk in range(1, 65)
      if A['PVC'].get(str(pk)) != B['PVC'].get(str(pk))]
pa = {d['n']: d['v'] for d in A.get('picks') or []}; pbk = {d['n']: d['v'] for d in B.get('picks') or []}
pm = [(n, pa[n], pbk.get(n)) for n in sorted(pa) if n <= 64 and pa[n] != pbk.get(n)]
P()
P("  NATIONAL PICK CURVE: PVC points moved %d of 64 | picks[] moved %d of 64" % (len(cm), len(pm)))
for n, x, y in pm[:20]: P("    pick %2d  %5s -> %5s  (%+d)" % (n, x, y, (y or 0) - (x or 0)))
OUT['curve'] = {'pvc_moved': len(cm), 'picks_moved': len(pm),
                'picks': [{'n': n, 'before': x, 'after': y} for n, x, y in pm]}
P()
P("  BOARD-LEVEL: pick 1 %s -> %s   (the numeraire law: must stay 3000)" % (A['PVC'].get('1'), B['PVC'].get('1')))
json.dump(OUT, open(sys.argv[2].replace('.json', '') + '_DELTA.json', 'w'), indent=1)
