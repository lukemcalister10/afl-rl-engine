#!/usr/bin/env python3
"""ORDER Q — THE BURN CENSUS, RUN INSIDE THE ENGINE.

THE QUESTION. Hold a row's output and games fixed and lower ONLY his entry price, in 2% steps.
Does any lower entry price price him HIGHER? If yes the row is BURNED: a higher pick is worth less
than a lower pick on identical evidence.

HOW IT IS DONE HERE. `day0_v0` is the single accessor for a row's entry price. It feeds exactly three
places: the pedigree leg `pv_pedigree`, the day-0 print predicate, and the ORDER P premium axis in
`o37_surplus`. It is wrapped for ONE row at a time and the row is RE-PRICED by the engine's own
`ev()`. Nothing is modelled and nothing is inferred. The wrapper is proved inert at scale 1.0: every
row reprices BIT-IDENTICALLY.

Usage: oq_sweep.py TAG [dial=value ...]
"""
import os, sys, io, json, math, time, contextlib, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oq_lib as L

TAG = sys.argv[1]
DIALS = dict(x.split('=', 1) for x in sys.argv[2:])
STEP, FLOOR_V0 = 0.98, 30.0
print('=== ORDER Q SWEEP  tag=%s  dials=%s ===' % (TAG, DIALS or '(ORDER K line, no O37)'))

NS = L.load(**DIALS)
NS['_REC'] = L.install_recorder(NS)
import rl_model as MA
FNUM = json.load(open(L.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
print('engine %s  store %s  players %d'
      % (hashlib.md5(open(L.ROOT + '/engine/rl_after/_merged_recover.py', 'rb').read()).hexdigest()[:8],
         hashlib.md5(open(L.ROOT + '/engine/rl_after/rl_model_data.json', 'rb').read()).hexdigest()[:8],
         len(MA.players)))
EV = NS['ev']
orig = NS['day0_v0']
TGT = {'p': None, 's': 1.0}


def patched(p):
    v = orig(p)
    return v * TGT['s'] if (v is not None and p is TGT['p']) else v


NS['day0_v0'] = patched


def price(p, s):
    TGT['p'] = p; TGT['s'] = s; NS['_O37_SCACHE'].clear(); NS['_REC'].clear()
    with contextlib.redirect_stdout(io.StringIO()):
        r = EV(p, 2026)
    a = L.assemble(NS, p, 2026)
    TGT['p'] = None; NS['_O37_SCACHE'].clear()
    return r, a


base = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        base[p['key']] = EV(p, 2026)
NS['_REC'].clear()

# inertness proof
nb = 0
for p in MA.players:
    r, _ = price(p, 1.0)
    if r != base[p['key']]:
        nb += 1
print('WRAPPER INERTNESS at scale 1.0: %d of %d rows differ (must be 0)' % (nb, len(MA.players)))
assert nb == 0, 'the v0 wrapper is not inert — HALT'

NS['_REC'].clear()
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, 2026)
ROWS = {p['key']: L.assemble(NS, p, 2026) for p in MA.players}

POP = [p for p in MA.players
       if p.get('_by') and (2026 - int(p['_by'])) < 24 and NS['pv_games'](p, 2026) > 0
       and (p.get('type') == 'ND' or p.get('_pool')) and ROWS[p['key']]['ped'] is not None]
print('young ND+pool rows, age<24, games>0: %d' % len(POP))

res = []
t0 = time.time()
for i, p in enumerate(POP):
    k = p['key']
    v0 = orig(p)
    r0, a0 = price(p, 1.0)
    path = [(1.0, v0, r0, a0['prod_leg'] + a0['credit'], a0['ped_leg'])]
    s = 1.0
    while v0 * s * STEP >= FLOOR_V0:
        s *= STEP
        r, a = price(p, s)
        path.append((s, v0 * s, r, a['prod_leg'] + a['credit'], a['ped_leg']))
    bestk = max(range(1, len(path)), key=lambda j: path[j][2]) if len(path) > 1 else None
    best = path[bestk][2] if bestk is not None else r0
    bv = int(round(best / FNUM)); r0v = int(round(r0 / FNUM))
    nonped = [x[3] for x in path]
    res.append(dict(key=k, name=p.get('player'), pick=p.get('pick'), pool=bool(p.get('_pool')),
                    age=2026 - int(p['_by']), g=NS['pv_games'](p, 2026), v0=v0,
                    price=r0, price_board=r0v, best=best, best_board=bv,
                    best_v0=path[bestk][1] if bestk is not None else v0,
                    burn=max(0.0, best - r0), burn_board=max(0, bv - r0v),
                    fK=ROWS[k]['f_K_eff'], fP=ROWS[k]['f_eff'], s_P=ROWS[k]['s_P'],
                    nonped_spread=max(nonped) - min(nonped), nonped=nonped[0],
                    nsteps=len(path)))
    if (i + 1) % 40 == 0:
        print('  ... %d/%d  %.0fs' % (i + 1, len(POP), time.time() - t0))
print('sweep done in %.0fs' % (time.time() - t0))

sp = max(r['nonped_spread'] for r in res)
print('\nIS THE NON-PEDIGREE PART OF THE PRICE INDEPENDENT OF ENTRY PRICE?')
print('  worst spread of (production leg + age credit) across a row\'s whole entry-price sweep: %.4e' % sp)
print('  rows where it moves at all (>1e-9): %d of %d'
      % (sum(1 for r in res if r['nonped_spread'] > 1e-9), len(res)))


def band(r):
    if r['pool'] or not r['pick']: return 'pool'
    k = int(r['pick'])
    return '1-10' if k <= 10 else '11-20' if k <= 20 else '21-30' if k <= 30 else '31-40' if k <= 40 else '41+'


SEL = [r for r in res if abs(r['fK'] - r['fP']) >= 0.02]
for nm, POPX in (('THE SUPERVISOR\'S POPULATION (|fK-fP| >= 0.02)', SEL), ('ALL YOUNG ROWS', res)):
    print('\nBURN CENSUS — %s   n=%d' % (nm, len(POPX)))
    print('  %-8s %5s %7s %10s %10s' % ('band', 'n', 'burned', 'pts(board)', 'pts(raw)'))
    tb = tp = tr = 0
    for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
        s = [r for r in POPX if band(r) == b]
        bn = [r for r in s if r['burn_board'] > 0]
        print('  %-8s %5d %7d %10d %10.0f' % (b, len(s), len(bn), sum(r['burn_board'] for r in bn),
                                              sum(r['burn'] for r in bn)))
        tb += len(bn); tp += sum(r['burn_board'] for r in bn); tr += sum(r['burn'] for r in bn)
    print('  %-8s %5d %7d %10d %10.0f' % ('TOTAL', len(POPX), tb, tp, tr))
    print('  WORST FIVE:')
    for r in sorted(POPX, key=lambda z: -z['burn_board'])[:5]:
        if r['burn_board'] <= 0: break
        print('    %-24s %-5s age %2d %4.0fg  v0 %6.0f -> %6.0f   %6d -> %6d  (+%d)'
              % (r['name'][:24], r['pick'] if not r['pool'] else 'pool', r['age'], r['g'],
                 r['v0'], r['best_v0'], r['price_board'], r['best_board'], r['burn_board']))

json.dump(dict(tag=TAG, dials=DIALS, rows=res), open(HERE + '/SWEEP_%s.json' % TAG, 'w'), indent=1, default=str)
print('\nwrote SWEEP_%s.json' % TAG)
