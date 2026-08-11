"""ORDER 20 — THE NATIONAL-ARM DIFF. Given two boards, report EXACTLY what moved on the national side.

    python3 nd_diff.py <BASE.json> <VARIANT.json> [label]

WHO IS NATIONAL. The engine's own classification is the authority (rl_model.py:264-268): a store row
of type ND with pick in 1..64 is national and carries _eff == pick; a national selection at pick >= 65
is POOL by the owner's ruling and carries _eff == 65. On the exported board those are `ty` and `ep`.
So:  NATIONAL  <=>  ty == 'ND' and ep <= 64.
This is stated rather than assumed because it is the exact line `daniel-butler` sits on.

WHAT IS COMPARED, per national row: every priced field the board carries —
    v      the present board price          vRaw   the pre-override model figure
    vP1/vP2 the forward boards              vM1/vM2 the backward boards
plus the NATIONAL PICK CURVE (`PVC` 1..64, `picks`, `pick_band_mean`) and the pick-side aggregates.
A single non-zero delta in any of them under a pool-only perturbation breaks the separation law.
"""
import json, sys, collections

BASE, VAR = sys.argv[1], sys.argv[2]
LABEL = sys.argv[3] if len(sys.argv) > 3 else VAR

A = json.load(open(BASE)); B = json.load(open(VAR))
PRICED = ('v', 'vRaw', 'vP1', 'vP2', 'vM1', 'vM2')


def is_national(r):
    return r.get('ty') == 'ND' and (r.get('ep') or 99) <= 64


def is_pool(r):
    return not is_national(r)


def rows(board):
    out = {}
    for sect in ('active', 'back'):
        for r in board.get(sect) or []:
            out[(sect, r.get('key') or r.get('name'))] = r
    return out


RA, RB = rows(A), rows(B)
keys = sorted(set(RA) | set(RB))

nat_movers = []; pool_movers = 0; nat_n = 0; pool_n = 0
for k in keys:
    a, b = RA.get(k), RB.get(k)
    if a is None or b is None:
        nat_movers.append((k, 'ROW APPEARED/VANISHED', None, None)); continue
    nat = is_national(a)
    nat_n += nat; pool_n += (not nat)
    moved = [(f, a.get(f), b.get(f)) for f in PRICED if a.get(f) != b.get(f)]
    if not moved: continue
    if nat:
        for f, x, y in moved: nat_movers.append((k, f, x, y))
    else:
        pool_movers += 1

# ---- the national pick curve -------------------------------------------------------------------
curve_movers = []
for pk in range(1, 65):
    x, y = A['PVC'].get(str(pk)), B['PVC'].get(str(pk))
    if x != y: curve_movers.append(('PVC', pk, x, y))
pa = {d['n']: d['v'] for d in A.get('picks') or []}
pb = {d['n']: d['v'] for d in B.get('picks') or []}
for n in sorted(set(pa) | set(pb)):
    if n <= 64 and pa.get(n) != pb.get(n): curve_movers.append(('picks', n, pa.get(n), pb.get(n)))
agg_movers = []
for key in ('pick_band_mean', 'intakePickSum', 'draftAssetTotals', 'BASEPK_REG', 'POOL', 'MIX',
            'pm_pos', 'pm_band', 'SCALE', 'REPL', 'BAND_ANCHOR', 'lensPicks'):
    if A.get(key) != B.get(key): agg_movers.append(key)

P = print
P("=" * 100)
P("ND/POOL SEPARATION DIFF   %s" % LABEL)
P("  base    %s" % BASE)
P("  variant %s" % VAR)
P("  population: national rows n=%d   pool rows n=%d   (national <=> ty=='ND' and ep<=64)" % (nat_n, pool_n))
P("=" * 100)
P("  POOL rows with a moved price   : %d  (expected non-zero — the perturbation is on the pool)" % pool_movers)
P("  NATIONAL rows with a moved price: %d  *** THE LAW SAYS THIS MUST BE 0 ***" % len({m[0] for m in nat_movers}))
P("  national PICK-CURVE points moved: %d  *** MUST BE 0 ***" % len(curve_movers))
P("  shared aggregate objects moved  : %d  %s" % (len(agg_movers), agg_movers))
P()
if nat_movers:
    P("  THE MOVED NATIONAL ROWS (every one, no truncation):")
    byrow = collections.defaultdict(list)
    for k, f, x, y in nat_movers: byrow[k].append((f, x, y))
    for k in sorted(byrow):
        r = RA.get(k) or RB.get(k)
        P("    %-34s pk=%-4s ep=%-4s ty=%-5s | %s" % (
            (r or {}).get('name', k[1]), (r or {}).get('pk'), (r or {}).get('ep'), (r or {}).get('ty'),
            "  ".join("%s %s->%s (%+d)" % (f, x, y, (y - x) if isinstance(x, int) and isinstance(y, int) else 0)
                      for f, x, y in byrow[k])))
if curve_movers:
    P("  THE MOVED CURVE POINTS:")
    for w, n, x, y in curve_movers[:80]:
        P("    %-6s %-4s %s -> %s" % (w, n, x, y))

verdict = 'SEPARATION HOLDS' if (not nat_movers and not curve_movers) else 'SEPARATION VIOLATED'
P()
P("  VERDICT: %s" % verdict)
json.dump({'label': LABEL, 'base': BASE, 'variant': VAR, 'national_n': nat_n, 'pool_n': pool_n,
           'pool_movers': pool_movers,
           'national_movers': sorted({m[0][1] for m in nat_movers}),
           'national_mover_detail': [{'key': k[1], 'field': f, 'base': x, 'variant': y}
                                     for k, f, x, y in nat_movers],
           'curve_movers': [{'where': w, 'n': n, 'base': x, 'variant': y} for w, n, x, y in curve_movers],
           'aggregate_movers': agg_movers, 'verdict': verdict},
          open(sys.argv[2].replace('.json', '') + '_NDDIFF.json', 'w'), indent=1)
sys.exit(0 if verdict == 'SEPARATION HOLDS' else 2)
