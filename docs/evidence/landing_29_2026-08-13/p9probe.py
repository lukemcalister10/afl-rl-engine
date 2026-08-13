#!/usr/bin/env python3
"""P9 PROBE: who maps to an UNSIGNED pool v0 cell, under WHICH position convention, and are they
priced on this board?  Run from a staged workspace rl_after."""
import io, contextlib, json, collections
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('rl_model.py').read().split("# ===== ORDER 29 STEP 5")[0], g)
data = g['data']; GRP = g['GRP']; gfut = g['gfut']; effpk = g['effpk']
POOL_PICK = g['POOL_PICK']; ND_CURVE_LAST = g['ND_CURVE_LAST']
art = json.load(open('pvc_curve_v2.json'))
PV0 = art['pool_v0']; UNS = set(PV0['unsigned_cells'])

def division(p):
    t = p.get('type')
    if t == 'RD': return 'RD'
    if t == 'ND': return 'ND>64' if (p.get('pick') or 0) > ND_CURVE_LAST else 'ND?'
    return t
def cell(p, pos): return '%s|%s' % (division(p), pos)

pool = [p for p in data if p.get('_pool')]
print('pool entrants: %d' % len(pool))
rows = []
for p in pool:
    pos_f = gfut(p)
    pos_d = GRP.get(p.get('present_position')) or gfut(p)
    pos_dr = GRP.get(p.get('drafted_position')) or gfut(p)
    hits = {'gfut': cell(p, pos_f) in UNS, 'present': cell(p, pos_d) in UNS, 'drafted': cell(p, pos_dr) in UNS}
    if any(hits.values()):
        rows.append((p.get('player'), p.get('key'), p.get('type'), p.get('year'), p.get('pick'),
                     pos_f, pos_d, pos_dr, cell(p, pos_f), hits,
                     len(p.get('scoring') or []), sum(r['games'] for r in (p.get('scoring') or []))))
print()
print('ENTRANTS MAPPING TO AN UNSIGNED CELL (any convention): %d' % len(rows))
for r in rows:
    print('  %-20s key=%-24s type=%-4s yr=%s pick=%s' % (r[0], r[1], r[2], r[3], r[4]))
    print('      gfut=%-5s present=%-5s drafted=%-5s  cell(gfut)=%-10s hits=%s' % (r[5], r[6], r[7], r[8], r[9]))
    print('      season rows=%d  career games=%d' % (r[10], r[11]))
print()
for conv in ('gfut', 'present', 'drafted'):
    n = sum(1 for r in rows if r[9][conv])
    print('  under %-8s convention: %d entrant(s) map to an unsigned cell' % (conv, n))
print()
cnt = collections.Counter(cell(p, gfut(p)) for p in pool)
print('pool population by cell (gfut), the unsigned two and the probe cell:')
for k in sorted(UNS) + ['RD|MID']:
    print('   %-10s %d' % (k, cnt.get(k, 0)))
