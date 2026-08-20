#!/usr/bin/env python3
"""ORDER Q — THE TWO CENSUSES, for one dial line.

(1) THE BURN CENSUS. Hold output and games fixed, lower ONLY the entry price in 2% steps, and ask
    whether any lower entry price prices the row HIGHER.
(2) THE BIRTHDAY CENSUS. Hold everything fixed and ask what the row's price becomes when the CHARGE
    is evaluated as if he had just turned 24. Under ORDER P that is his ORDER K price, because the
    gate hands the whole charge back. Verified against the built boards: Josh Sinn 73 -> 357 is
    exactly ORDER K / ORDER P on f3101883 and 374d4e44.

BOTH ARE RUN ON THE ENGINE'S OWN OBJECTS. The price identity used is the one STEP 0 verified to
9.1e-13 on 804 of 804 rows and whose non-pedigree part was measured to move by EXACTLY ZERO across
the whole entry-price sweep on 0 of 289 rows:

    price(v) = [rho31(g)*e + age_credit]  +  pi_base * (v * _PL_F) * factor(v)

so only `factor` is recomputed per step, out of the engine's own factor function with `day0_v0`
wrapped. The full-engine sweep that PROVED this identity is oq_sweep.py; this script reproduces it
and is checked against it.

Usage: oq_census.py TAG [dial=value ...]
"""
import os, sys, io, json, math, time, contextlib, hashlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oq_lib as L

TAG = sys.argv[1]
DIALS = dict(x.split('=', 1) for x in sys.argv[2:])
STEP, FLOOR_V0 = 0.98, 30.0
print('=== ORDER Q CENSUS  tag=%s  dials=%s ===' % (TAG, DIALS))
NS = L.load(**DIALS)
NS['_REC'] = L.install_recorder(NS)
import rl_model as MA
FNUM = json.load(open(L.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
PLF = NS['_PL_F']
EV = NS['ev']
orig = NS['day0_v0']
TGT = {'p': None, 's': 1.0}
NS['day0_v0'] = lambda p, _o=orig: (_o(p) * TGT['s'] if (_o(p) is not None and p is TGT['p']) else _o(p))
FAC = NS['o38_factor'] if NS.get('_O38') else NS['o37_factor']

with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, 2026)
ROWS = {p['key']: L.assemble(NS, p, 2026) for p in MA.players}
RAW = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        RAW[p['key']] = EV(p, 2026)
print('board total (numeraire): %d' % round(sum(int(round(RAW[k] / FNUM)) for k in RAW)))


def band(pick, pool):
    if pool or not pick: return 'pool'
    k = int(pick)
    return '1-10' if k <= 10 else '11-20' if k <= 20 else '21-30' if k <= 30 else '31-40' if k <= 40 else '41+'


# ---------- (1) THE BURN CENSUS -------------------------------------------------------------------
POP = [p for p in MA.players
       if p.get('_by') and (2026 - int(p['_by'])) < 24 and NS['pv_games'](p, 2026) > 0
       and (p.get('type') == 'ND' or p.get('_pool')) and ROWS[p['key']]['ped'] is not None]
res = []
for p in POP:
    k = p['key']; r = ROWS[k]
    v0 = orig(p); g = NS['pv_games'](p, 2026)
    nonped = r['prod_leg'] + r['credit']
    pib = r['pi_base_eff']
    TGT['p'] = p
    path = []
    s = 1.0
    while True:
        TGT['s'] = s; NS['_O37_SCACHE'].clear(); NS['_O38_PCACHE'].clear()
        f = FAC(p, 2026, g)
        path.append((s, v0 * s, nonped + pib * (v0 * s * PLF) * f, f))
        if v0 * s * STEP < FLOOR_V0: break
        s *= STEP
    TGT['p'] = None; NS['_O37_SCACHE'].clear(); NS['_O38_PCACHE'].clear()
    r0 = path[0][2]
    assert abs(r0 - RAW[k]) < 1e-6, 'identity broke on %s: %.6f vs %.6f' % (k, r0, RAW[k])
    j = max(range(len(path)), key=lambda i: path[i][2])
    best = path[j][2]
    bv, r0v = int(round(best / FNUM)), int(round(r0 / FNUM))
    res.append(dict(key=k, name=p.get('player'), pick=p.get('pick'), pool=bool(p.get('_pool')),
                    band=band(p.get('pick'), p.get('_pool')), age=2026 - int(p['_by']), g=g, v0=v0,
                    price_board=r0v, best_board=bv, best_v0=path[j][1],
                    burn=max(0.0, best - r0), burn_board=max(0, bv - r0v),
                    fK=r['f_K_eff'], fP=r['f_eff'], fP37=r.get('f_P37_eff', r['f_eff']), nsteps=len(path)))
# the supervisor's population is fixed by ORDER P's OWN factors, so it is the SAME 268 rows
# under every variant and the bands are comparable across the table.
SEL = [r for r in res if abs(r['fK'] - r['fP37']) >= 0.02]
print('\nBURN CENSUS')
for nm, POPX in (("the supervisor's population (|fK-fP|>=0.02)", SEL), ('all young rows', res)):
    print('  -- %s, n=%d' % (nm, len(POPX)))
    print('     %-8s %5s %7s %11s' % ('band', 'n', 'burned', 'pts(board)'))
    tb = tp = 0
    for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
        s = [r for r in POPX if r['band'] == b]
        bn = [r for r in s if r['burn_board'] > 0]
        print('     %-8s %5d %7d %11d' % (b, len(s), len(bn), sum(r['burn_board'] for r in bn)))
        tb += len(bn); tp += sum(r['burn_board'] for r in bn)
    print('     %-8s %5d %7d %11d' % ('TOTAL', len(POPX), tb, tp))
print('  worst five (all young rows):')
for r in sorted(res, key=lambda z: -z['burn_board'])[:5]:
    if r['burn_board'] <= 0:
        print('     (none — the census is ZERO)'); break
    print('     %-24s %-5s age %2d %4.0fg  v0 %6.0f -> %6.0f   %6d -> %6d  (+%d)'
          % (r['name'][:24], r['pick'] if not r['pool'] else 'pool', r['age'], r['g'], r['v0'],
             r['best_v0'], r['price_board'], r['best_board'], r['burn_board']))

# ---------- (2) THE BIRTHDAY CENSUS ---------------------------------------------------------------
# The charge is re-evaluated as if the row had just turned 24. Everything else is held EXACTLY fixed.
bres = []
if NS.get('_O38'):
    w0 = NS['o38_w']
    NS['o38_w'] = lambda a, _w=w0: _w(24)
else:
    w0 = None
    of = NS['o37_factor']
    NS['o37_factor'] = lambda p, Y, g, _o=of: max(0.0, 1.0 - NS['O32_ETA'] * ((float(g) / NS['O32_GAMMA_D']) * math.exp(1.0 - float(g) / NS['O32_GAMMA_D'])))
    FAC24 = NS['o37_factor']
FAC24 = NS['o38_factor'] if NS.get('_O38') else NS['o37_factor']
for p in MA.players:
    if not p.get('_by'): continue
    age = 2026 - int(p['_by'])
    if age != 23: continue
    k = p['key']; r = ROWS[k]
    if r['ped'] is None: continue
    g = NS['pv_games'](p, 2026)
    NS['_O37_SCACHE'].clear(); NS['_O38_PCACHE'].clear()
    f24 = FAC24(p, 2026, g)
    p24 = r['prod_leg'] + r['credit'] + r['pi_base_eff'] * r['ped'] * f24
    a, b = int(round(RAW[k] / FNUM)), int(round(p24 / FNUM))
    bres.append(dict(key=k, name=p.get('player'), pick=p.get('pick'), pool=bool(p.get('_pool')),
                     band=band(p.get('pick'), p.get('_pool')), g=g, at23=a, at24=b,
                     ratio=(b / a) if a > 0 else None, delta=b - a, f23=r['f_eff'], f24=f24))
if w0 is not None: NS['o38_w'] = w0
print('\nBIRTHDAY CENSUS — the price on the 24th birthday, with games and output UNCHANGED')
print('  age-23 rows with a pedigree leg: %d' % len(bres))
big = [r for r in bres if r['ratio'] is not None and r['ratio'] >= 1.5]
print('  rows that GAIN 50%% or more from the birthday alone: %d' % len(big))
print('  points handed back across all age-23 rows: NET %+d   GAINS ONLY %+d   (the two readings are\n  different objects and both are printed: the birthday RAISES some rows and LOWERS others)'
        % (sum(r['delta'] for r in bres), sum(r['delta'] for r in bres if r['delta'] > 0)))
print('  worst ratio: %.4f   rows moving at all: %d' % (max([r['ratio'] for r in bres if r['ratio']] or [1.0]),
                                                        sum(1 for r in bres if r['delta'] != 0)))
print('  %-8s %5s %8s %8s %14s %14s' % ('band', 'n', 'gain50+', 'movers', 'net points', 'gains only'))
for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
    s = [r for r in bres if r['band'] == b]
    if not s: continue
    print('  %-8s %5d %8d %8d %+14d %+14d' % (b, len(s), sum(1 for r in s if r['ratio'] and r['ratio'] >= 1.5),
                                        sum(1 for r in s if r['delta'] != 0), sum(r['delta'] for r in s),
                                        sum(r['delta'] for r in s if r['delta'] > 0)))
print('  the five largest ratios:')
for r in sorted(bres, key=lambda z: -(z['ratio'] or 0))[:5]:
    print('     %-24s %-5s %4.0fg   %6d -> %6d   x%.3f' % (r['name'][:24], r['pick'] if not r['pool'] else 'pool',
                                                           r['g'], r['at23'], r['at24'], r['ratio'] or 1.0))

json.dump(dict(tag=TAG, dials=DIALS, burn=res, birthday=bres,
               board_total=round(sum(int(round(RAW[k] / FNUM)) for k in RAW))),
          open(HERE + '/CENSUS_%s.json' % TAG, 'w'), indent=1, default=str)
print('\nwrote CENSUS_%s.json' % TAG)
