#!/usr/bin/env python3
"""ORDER R — THE TWO CENSUSES PLUS THE CHARGE DISTRIBUTION, for one dial line.

ORDER Q's oq_census.py, unchanged in every measurement it already made, with THREE additions the
ORDER R order asks for: (3) the CHARGE DISTRIBUTION -- the maximum charge and the counts of rows
charged more than 90%, 75% and 50% of their pedigree leg; (4) the NAMED ROWS, reported as
consequences and NEVER as acceptance criteria; (5) the effective TMAX/THETA_R/BETA_sat the board was
built on, printed so a board can never be mislabelled.

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
import or_lib as L

TAG = sys.argv[1]
DIALS = dict(x.split('=', 1) for x in sys.argv[2:])
STEP, FLOOR_V0 = 0.98, 30.0
print('=== ORDER R CENSUS  tag=%s  dials=%s ===' % (TAG, DIALS))
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

# ---------- (3) THE CHARGE DISTRIBUTION -----------------------------------------------------------
# The charge is 1 - f, where f is the factor the pedigree leg was ACTUALLY multiplied by at the blend
# site, M3-reassembled. Two populations are printed and they are different questions:
#   ALL CHARGED  -- every row with a pedigree leg and games > 0, whatever charge it carries.
#   CONDITIONAL  -- only the rows carrying the PEDIGREE-CONDITIONAL charge rather than the ORDER K
#                   fallback. That is the population these dials actually reach.
print('\nTHE EFFECTIVE CONSTANTS THIS BOARD WAS BUILT ON')
print('  BETA_sat  %.10f   (ORDER P point estimate %.10f)' % (NS['O39_BETA_SAT'], NS['O37_BETA_SAT'])
      if 'O39_BETA_SAT' in NS else '  (ORDER R constants absent — pre-ORDER R engine)')
if 'O39_BETA_SAT' in NS:
    print('  THETA_R   %.10f   (ORDER P %.10f)' % (NS['O39_THETA_R'], NS['O37_THETA_R']))
    print('  TMAX      %.10f   (ORDER P %.10f)   percentile p%d, s_pQ %+.10f'
          % (NS['O39_TMAX'], NS['O37_TMAX'], NS['_O39_PCT'], NS['O39_S_PQ'][NS['_O39_PCT']]))
    print('  LAMBDA    %.10f   HELD FIXED, NOT RE-SOLVED (disclosed on PREREG_R.md)' % NS['O37_LAMBDA'])

CH = []
for p in MA.players:
    k = p['key']; r = ROWS.get(k)
    if not r or r['ped'] is None: continue
    g = NS['pv_games'](p, 2026)
    if g <= 0: continue
    f = r['f_eff']
    if f is None: continue
    cond = (r.get('f_P37_eff') is not None and NS.get('_O37')
            and abs(r['f_K_eff'] - r['f_eff']) > 1e-12)
    # MECHANISM DIAGNOSTICS, for the whole-arc movers file. All engine objects, none recomputed here.
    #   pg     = the pedigree premium PG(ln v0, class), games-weighted across the row's own classes
    #   s_age  = production against the S1 AGE BAR alone            (does NOT move with entry price)
    #   s_ped  = production against the AGE BAR PLUS the premium    (what the charge actually reads)
    # By construction s_ped = s_age - pg, and that identity is checked below rather than assumed.
    v0r = orig(p)
    pg = s_age = None
    try:
        pr = NS['o38_parts'](p, 2026) if 'o38_parts' in NS else None
    except Exception:
        pr = None
    if pr is not None and v0r is not None:
        s_age, wT, wS = pr
        x = math.log(round(float(v0r) * PLF, 1))
        pg = wT * NS['o38_pg_at'](x, 'TALL') + wS * NS['o38_pg_at'](x, 'SMALL')
    CH.append(dict(key=k, name=p.get('player'), pick=p.get('pick'), pool=bool(p.get('_pool')),
                   band=band(p.get('pick'), p.get('_pool')),
                   age=(2026 - int(p['_by'])) if p.get('_by') else None, g=g,
                   f=f, f_K=r['f_K_eff'], charge=1.0 - f, cond=bool(cond),
                   pg=pg, s_age=s_age, s_ped=r['s_P'],
                   ped_leg=r['ped_leg'], v0=v0r,
                   pos=p.get('pos'), ty=p.get('type'), pool_arm=p.get('_pool'),
                   dy=p.get('year')))
bad_id = [c for c in CH if c['pg'] is not None and c['s_age'] is not None and c['s_ped'] is not None
          and abs((c['s_age'] - c['pg']) - c['s_ped']) > 1e-9]
print('\nDIAGNOSTIC IDENTITY  s_ped == s_age - pg : %d of %d rows disagree by more than 1e-9%s'
      % (len(bad_id), sum(1 for c in CH if c['pg'] is not None),
         '' if not bad_id else '   **worst %.3g on %s**'
         % (max(abs((c['s_age'] - c['pg']) - c['s_ped']) for c in bad_id), bad_id[0]['name'])))
print('\nCHARGE DISTRIBUTION — the share of the pedigree leg removed')
print('  %-26s %6s %10s %9s %9s %9s %14s' % ('population', 'n', 'max charge', '>90%', '>75%', '>50%', 'pts removed'))
for nm, sub in (('all rows with a leg', CH), ('carrying the new charge', [c for c in CH if c['cond']])):
    if not sub:
        print('  %-26s %6d %10s %9s %9s %9s %14s' % (nm, 0, 'n/a', 'n/a', 'n/a', 'n/a', 'n/a'))
        continue
    mx = max(c['charge'] for c in sub)
    rem = sum(c['ped_leg'] / c['f'] * c['charge'] for c in sub if c['f'] > 0)
    print('  %-26s %6d %9.2f%% %9d %9d %9d %14.0f'
          % (nm, len(sub), 100.0 * mx, sum(1 for c in sub if c['charge'] > 0.90),
             sum(1 for c in sub if c['charge'] > 0.75), sum(1 for c in sub if c['charge'] > 0.50),
             rem / FNUM))
print('  the ten most heavily charged rows (CONSEQUENCES, NEVER TARGETS):')
for c in sorted(CH, key=lambda z: -z['charge'])[:10]:
    print('     %-24s %-5s age %-3s %4.0fg  v0 %6.0f   charged %6.2f%%'
          % (c['name'][:24], c['pick'] if not c['pool'] else 'pool', c['age'], c['g'], c['v0'],
             100.0 * c['charge']))
print('  by band:')
print('  %-8s %6s %10s %9s %9s %9s' % ('band', 'n', 'max charge', '>90%', '>75%', '>50%'))
for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
    s = [c for c in CH if c['band'] == b]
    if not s:
        print('  %-8s %6d %10s %9s %9s %9s' % (b, 0, '(absent)', '-', '-', '-')); continue
    print('  %-8s %6d %9.2f%% %9d %9d %9d'
          % (b, len(s), 100.0 * max(c['charge'] for c in s),
             sum(1 for c in s if c['charge'] > 0.90), sum(1 for c in s if c['charge'] > 0.75),
             sum(1 for c in s if c['charge'] > 0.50)))

# ---------- (4) THE NAMED ROWS --------------------------------------------------------------------
# THESE ARE CONSEQUENCES AND NEVER ACCEPTANCE CRITERIA. Not one constant in this order was chosen
# with any of these rows in view. That is a standing prohibition in this project after a real error.
NAMES = ['Zane Duursma', 'Josh Sinn', 'Campbell Chesser', 'Finn O\'Sullivan', 'Zeke Uwland',
         'Harley Reid', 'Sam Darcy', 'Willem Duursma', 'Sam Lalor']
print('\nTHE NAMED ROWS — CONSEQUENCES, NEVER TARGETS')
print('  %-20s %6s %5s %6s %10s %10s %10s' % ('row', 'pick', 'age', 'games', 'price', 'charge', 'v0'))
NAMED = []
for nm in NAMES:
    hit = [p for p in MA.players if (p.get('player') or '') == nm]
    if not hit:
        print('  %-20s  NOT FOUND ON THIS BOARD — reported as absent, never as zero' % nm)
        NAMED.append(dict(name=nm, found=False)); continue
    p = hit[0]; k = p['key']; r = ROWS.get(k)
    g = NS['pv_games'](p, 2026)
    pr = int(round(RAW[k] / FNUM))
    ch = (1.0 - r['f_eff']) if (r and r['f_eff'] is not None) else None
    d = dict(name=nm, found=True, key=k, pick=p.get('pick'), pool=bool(p.get('_pool')),
             age=(2026 - int(p['_by'])) if p.get('_by') else None, g=g, price=pr,
             charge=ch, v0=orig(p), ped_leg=(r['ped_leg'] if r else None),
             s_P=(r['s_P'] if r else None))
    NAMED.append(d)
    print('  %-20s %6s %5s %6.0f %10d %9s %10.0f'
          % (nm, (p.get('pick') if not p.get('_pool') else 'pool'), d['age'], g, pr,
             ('%.2f%%' % (100.0 * ch)) if ch is not None else 'no leg', d['v0'] or 0.0))

json.dump(dict(tag=TAG, dials=DIALS, burn=res, birthday=bres, charge=CH, named=NAMED,
               constants=(dict(BETA_sat=NS['O39_BETA_SAT'], THETA_R=NS['O39_THETA_R'],
                               TMAX=NS['O39_TMAX'], pct=NS['_O39_PCT'],
                               s_pQ=NS['O39_S_PQ'][NS['_O39_PCT']], LAMBDA=NS['O37_LAMBDA'])
                          if 'O39_BETA_SAT' in NS else None),
               board_total=round(sum(int(round(RAW[k] / FNUM)) for k in RAW))),
          open(HERE + '/CENSUS_%s.json' % TAG, 'w'), indent=1, default=str)
print('\nwrote CENSUS_%s.json' % TAG)
