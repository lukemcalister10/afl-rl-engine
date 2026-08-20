#!/usr/bin/env python3
"""ORDER 30B-P — THE PREVIEW MOVERS LEDGER, THE SELECTABILITY COUNTERFACTUAL AND THE CONTINUITY CURVE.

READ-ONLY toward the repo. It reads three written boards (live `88ce647f`, Step-2 `92982031`, preview
`6a392bca`) and loads the PREVIEW-STAGED engine to recover, per row, the objects that are not on the board:
the STEP-1 positional v0, the sitter fade D(c), sigma(g), and the production leg the blend consumed.

  RL_O30B_PREVIEW=1 must be set in the environment: the engine is loaded IN THE PREVIEW LANE so that
  day0_v0 / sigma30bp / pv_games / the blend are the SAME callables the board was built from.

Usage:  o30bp_movers.py LIVE.json STEP2.json PREVIEW.json OUTDIR
"""
import os, sys, io, json, math, contextlib, collections

LIVE_P, S2_P, PV_P, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
STAGE = os.environ['STAGE']; ROOT = os.environ['RL_REPO']
assert os.environ.get('RL_O30B_PREVIEW') == '1', 'this harness must run IN the preview lane'
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; cp = G['cp']
day0_v0 = G['day0_v0']; _PL_F = G['_PL_F']; sigma30bp = G['sigma30bp']; sigma30bp_raw = G['sigma30bp_raw']
pv_games = G['pv_games']; fade30b_D = G['fade30b_D']; fade30b_clock = G['fade30b_clock']
fade30b_of = G['fade30b_of']; _entry30b_price = G['_entry30b_price']; _isreal = G['_isreal']
delisted = G['delisted']; ev = G['ev']; _F = _PL_F
Y = 2026

def load(p):
    B = json.load(open(p)); return {r['key']: r for r in B['active']}
L, S2, PV = load(LIVE_P), load(S2_P), load(PV_P)
BY = {p['key']: p for p in MA.data if p.get('key')}

POOLTY = set()
rows = []
for k in sorted(set(S2) | set(PV)):
    a, b = S2.get(k), PV.get(k)
    if a is None or b is None:
        print('POPULATION CHANGE %s' % k); continue
    p = BY.get(k)
    ty = a.get('ty'); ispool = bool(p.get('_pool')) if p is not None else None
    if ispool: POOLTY.add(ty)
    d0 = _entry30b_price(p, Y) if p is not None else None
    g = pv_games(p, Y) if p is not None else None
    v0b = day0_v0(p) if p is not None else None          # STEP-1 positional v0, BOARD currency
    c = fade30b_clock(p, Y) if p is not None else None
    Dc = fade30b_of(p, Y) if p is not None else None      # 1.0 for pool: pool fade is STEP 4's
    sg = None if d0 is not None else (sigma30bp(g) if g is not None else None)
    # the production leg the blend consumed, recovered by inverting the blend on the printed price
    prod = None
    if sg is not None and sg < 1.0 and v0b is not None:
        prod = (float(b['v']) - sg * v0b) / (1.0 - sg)
    rows.append(dict(
        key=k, name=a.get('name'), pathway=ty, pool=ispool, pick=a.get('pk'), pos=a.get('gf'),
        age=a.get('age'), cg=a.get('cg'), yr=a.get('yr'),
        live=(L[k]['v'] if k in L else None), step2=a['v'], preview=b['v'],
        d_vs_step2=b['v'] - a['v'],
        pct_vs_step2=(100.0 * (b['v'] - a['v']) / a['v']) if a['v'] else None,
        d_vs_live=(b['v'] - L[k]['v']) if k in L else None,
        games_sigma_axis=g, v0_step1_board=v0b, fade_clock=c, fade_D=Dc,
        sigma=sg, sigma_raw_alt=(sigma30bp_raw(g) if (g is not None and d0 is None) else None),
        pedigree_pts=(sg * v0b if (sg is not None and v0b is not None) else None),
        production_pts=prod, day0=bool(d0 is not None),
        sat_counterfactual=(v0b * Dc if (v0b is not None and Dc is not None) else None)))

tot_l = sum(r['live'] for r in rows if r['live'] is not None)
tot_2 = sum(r['step2'] for r in rows); tot_p = sum(r['preview'] for r in rows)
mv = [r for r in rows if r['d_vs_step2'] != 0]
print('ORDER 30B-P PREVIEW MOVERS — PRE-NUMERAIRE (Step 6 has not run)')
print('  rows %d   live 88ce647f total %d   Step-2 92982031 total %d   PREVIEW total %d  (%+d, %+.4f%%)'
      % (len(rows), tot_l, tot_2, tot_p, tot_p - tot_2, 100.0 * (tot_p - tot_2) / tot_2))
print('  movers vs Step-2: %d of %d   sum delta %+d' % (len(mv), len(rows), sum(r['d_vs_step2'] for r in mv)))
print('  day-0 rows: %d   of which movers: %d  (P2: must be 0)'
      % (sum(1 for r in rows if r['day0']), sum(1 for r in mv if r['day0'])))
cls = collections.Counter(); csum = collections.Counter()
def cgc(v):
    v = v or 0
    return '0' if v == 0 else ('1-2' if v <= 2 else ('3-5' if v <= 5 else ('6-10' if v <= 10 else
           ('11-15' if v <= 15 else ('16-35' if v <= 35 else ('36-70' if v <= 70 else '71+'))))))
for r in mv: cls[cgc(r['cg'])] += 1; csum[cgc(r['cg'])] += r['d_vs_step2']
print('  by career-games class:')
for c in ('0', '1-2', '3-5', '6-10', '11-15', '16-35', '36-70', '71+'):
    if cls[c]: print('     cg %-6s movers %4d   sum %+9d' % (c, cls[c], csum[c]))
tc = collections.Counter(); ts = collections.Counter()
for r in mv: tc[r['pathway']] += 1; ts[r['pathway']] += r['d_vs_step2']
print('  by pathway: %s' % ', '.join('%s %d(%+d)' % (t, tc[t], ts[t]) for t in sorted(tc, key=str)))
print('  pool pathways on the board (PROVISIONAL — pool values pending Step 4): %s' % sorted(POOLTY))
print('\n  TOP 20 BY |delta| vs Step-2')
print('  %-24s %-22s %-5s %5s %-5s %4s %5s %8s %8s %8s %9s %8s'
      % ('key', 'name', 'path', 'pick', 'pos', 'age', 'cg', 'LIVE', 'STEP2', 'PREVIEW', 'delta', 'pct'))
for r in sorted(mv, key=lambda x: -abs(x['d_vs_step2']))[:20]:
    print('  %-24s %-22s %-5s %5s %-5s %4s %5s %8s %8d %8d %+9d %+7.1f%%'
          % (r['key'], (r['name'] or '')[:22], r['pathway'], r['pick'], r['pos'], r['age'], r['cg'],
             r['live'], r['step2'], r['preview'], r['d_vs_step2'], r['pct_vs_step2']))

# ---- the selectability counterfactual ----------------------------------------------------------------
NAMED = ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow', 'cooper-trembath', 'chris-scerri',
         'zane-duursma', 'xavier-duursma']
print('\n  THE SELECTABILITY COUNTERFACTUAL — preview price vs the SAT counterfactual (pure sitter at his clock, v0 x D(c))')
print('  %-20s %-5s %5s %-5s %5s %7s %9s %8s %9s %9s %10s %9s'
      % ('key', 'path', 'pick', 'pos', 'cg', 'sigma', 'v0(STEP1)', 'D(c)', 'SAT v0xD', 'PREVIEW', 'gap', 'gap %'))
CF = []
for k in NAMED:
    r = [x for x in rows if x['key'] == k]
    if not r: print('  MISSING %s' % k); continue
    r = r[0]
    sat = r['sat_counterfactual']
    gap = r['preview'] - sat if sat is not None else None
    CF.append(dict(r, sat=sat, gap=gap, gap_pct=(100.0 * gap / sat) if sat else None))
    print('  %-20s %-5s %5s %-5s %5s %7s %9.1f %8.4f %9.1f %9d %+10.1f %+8.1f%%'
          % (r['key'], r['pathway'], r['pick'], r['pos'], r['cg'],
             ('%.4f' % r['sigma']) if r['sigma'] is not None else '-', r['v0_step1_board'], r['fade_D'],
             sat, r['preview'], gap, 100.0 * gap / sat))

# ---- the continuity curve: price vs games 0..15 for named rows -----------------------------------------
def curve(key, gmax=15):
    p = BY[key]; out = []
    yr = [x for x in p['scoring'] if x['year'] == Y]
    if not yr:
        p['scoring'].append({'year': Y, 'games': 0, 'avg': 0.0}); yr = [p['scoring'][-1]]; made = True
    else: made = False
    row = yr[0]; g0, a0 = row['games'], row.get('avg')
    prior = sum(x['games'] for x in p['scoring'] if x['year'] < Y and x['games'])
    try:
        for gg in range(0, gmax + 1):
            row['games'] = gg
            if gg == 0: row['avg'] = 0.0
            else: row['avg'] = a0 if (a0 and a0 > 0) else 60.0
            out.append((prior + gg, int(round(ev(p, Y) / _F))))
    finally:
        row['games'], row['avg'] = g0, a0
        if made: p['scoring'].pop()
    return out
print('\n  THE CONTINUITY CURVE (ruling 6): printed price vs GAMES IN THE CURRENT SEASON, 0..15')
CURVES = {}
for k in ('isaac-kako', 'josh-smillie', 'harry-demattia', 'max-knobel', 'dyson-sharp'):
    if k not in BY: continue
    cv = curve(k); CURVES[k] = cv
    step = (cv[1][1] - cv[0][1])
    print('  %-16s %s' % (k, ' '.join('%d:%d' % (a, b) for a, b in cv)))
    print('  %-16s   FIRST-GAME STEP %+d  (%+.1f%%)   monotone-in-evidence: %s'
          % ('', step, 100.0 * step / max(1, cv[0][1]),
             all(cv[i + 1][1] >= cv[i][1] for i in range(len(cv) - 1))))

os.makedirs(OUT, exist_ok=True)
json.dump(dict(
    order='30B-P', pre_numeraire=True, greenlit=False,
    boards=dict(live='88ce647f531030d8d2e094188b258191', step2='9298203135202a0c707bb0977ba38c31',
                preview='6a392bca7ad0dee04a6b4f037c758f65'),
    totals=dict(live=tot_l, step2=tot_2, preview=tot_p, delta=tot_p - tot_2),
    sigma=dict(tau=G['SIGMA30BP_TAU'], beta=G['SIGMA30BP_BETA'], src=G['SIGMA30BP_SRC'],
               measured_bands=G['SIGMA30BP_BANDS']),
    bars=G['_O30BP_BARS'], numeraire_factor=_PL_F,
    n_movers=len(mv), rows=rows, counterfactual=CF, continuity=CURVES,
    pool_note='provisional - pool values pending Step 4'),
    open(os.path.join(OUT, 'PREVIEW_MOVERS.json'), 'w'), indent=1, sort_keys=True)
print('\n  wrote %s' % os.path.join(OUT, 'PREVIEW_MOVERS.json'))
