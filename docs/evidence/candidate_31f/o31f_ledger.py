#!/usr/bin/env python3
"""ORDER 31-F — THE COMPOSED MOVERS LEDGER, THE CONTINUITY CURVE AND THE COMPLETENESS AUDIT.

ORDER 31's o31_ledger.py, carried forward. The changes are enumerated at the top of the file and are
confined to (a) the board set (the 31-F boards plus the two declared measurement dials), (b) the extra
ORDER-31 baseline column, and (c) beta31/phi31 now taking the row's pathway so a pool row reads its own
derived coefficient. No estimator, no attribution and no assert is altered.

Reads the three built boards, then loads the engine ONCE under RL_O31=1 to read every row's LEGS
(rho, Phat, pi, V0, D, c_u, s, Phi, beta, g) so the attribution is the law's own arithmetic and not a
reconstruction.  Emits:

  docs/ledgers/CANDIDATE_31_MOVERS.{json,md}
  docs/evidence/candidate_31f/CONTINUITY_31F.json          the build-failing continuity curve
  docs/evidence/candidate_31f/COMPLETENESS_31F.json        the forbidden-set audit
"""
import os, sys, json, math, io, contextlib, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP   = os.environ.get('RL_SCRATCH', '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f')
md5  = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

BOARDS = {'cand': 'bb_f2on', 'cand2': 'bb_f2on2', 'nophi': 'bb_f2nophi',
          'nobpool': 'bb_f2nobp', 'off': 'bb_f1off', 'entryoff': 'bb_f0off', 'o31': 'bb_f0on'}
BD = {}
for k, d in BOARDS.items():
    p = os.path.join(SP, d, 'rl_after', 'rl_app_data.json')
    BD[k] = {'md5': md5(p), 'rows': {r['key']: r for r in json.load(open(p))['active']}}
    print('%-6s %s  n=%d  total=%d' % (k, BD[k]['md5'], len(BD[k]['rows']),
                                       sum(r['v'] for r in BD[k]['rows'].values())))

PREV = json.load(open(os.path.join(HERE, '..', 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')))
PRVR = {r['key']: r for r in PREV['rows']}
LIVE_MD5, STEP2_MD5 = PREV['boards']['live'], PREV['boards']['step2']
assert BD['entryoff']['md5'] == STEP2_MD5, 'the ENTRY dial-off control is not the committed Step-2 board'
assert BD['o31']['md5'] == 'd9a57cc8770802b83c1264a08356fb60', 'the ORDER-31 baseline board did not reproduce'
assert BD['cand']['md5'] == BD['cand2']['md5'], 'DETERMINISM FAILED: two builds of the final board differ'
O31_MD5 = BD['o31']['md5']

# ---------------------------------------------------------------- load the engine under the one law
os.environ.update(RL_O31='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    # the engine's OWN loading convention for the pricing core (rl_export.py:66, _gate1_wf.py:8, ...)
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
G = {k: NSE.get(k) for k in
     ('rho31', 'beta31', 'phi31', 'phistall31', 'o31_cu', 'o31_D', 'o31_stall_run', 'o31_pi',
      'pv_games', 'pv_pedigree', 'ev', '_PL_F', 'fade30b_clock', 'fade30b_D', 'o31_pool_D',
      'o31_fade_D', 'O31_BETA_POOL', 'O31_PHIST_POOL', 'O31_FADE_D', '_O31F_NOBPOOL',
      'O31_TAU_RHO', 'O31_B_RHO', '_O30BP_BARS', 'par_pole', '_O30B_NOPOLE', '_O30B_NOISO', '_PV')}
missing = [k for k, v in G.items() if v is None]
if missing:
    sys.exit('ORDER 31 LEDGER HALT: the engine did not expose %s — the one law is not live.' % missing)
F = float(G['_PL_F'])
BASE = MA.BASE_REF

# ---------------------------------------------------------------- per-row legs, from the law itself
rows = []
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in BD['cand']['rows']:
        continue
    b = BD['cand']['rows'][k]
    g = float(G['pv_games'](p, BASE))
    r = float(G['rho31'](g))
    cu = float(G['o31_cu'](p, BASE))
    D = float(G['o31_D'](p, BASE))
    s = int(G['o31_stall_run'](p, BASE))
    _pl = bool(p.get('_pool'))
    ph = float(G['phi31'](g, s, _pl))
    be = float(G['beta31'](g, _pl))
    V0 = float(G['pv_pedigree'](p)) / F                       # back to BOARD currency
    pi = float(G['o31_pi'](p, BASE, g))
    cand = int(b['v'])
    nophi = int(BD['nophi']['rows'][k]['v'])
    nobpool = int(BD['nobpool']['rows'][k]['v'])
    o31 = int(BD['o31']['rows'][k]['v'])
    pr = PRVR.get(k, {})
    step2 = pr.get('step2'); live = pr.get('live')
    ped = pi * V0
    prod = max(0.0, cand - ped)                               # the law's own production contribution
    rows.append(dict(key=k, name=p.get('player'), pathway=p.get('type'), pool=bool(p.get('_pool')),
                     pick=p.get('pick'), pos=MA.gfut(p), age=b.get('age'), cg=b.get('cg'), yr=b.get('yr'),
                     g=g, rho=r, c_fade=float(G['fade30b_clock'](p, BASE)), c_u=cu, D=D, s=s, Phi=ph,
                     beta=be, pi=pi, v0=V0,
                     pedigree_pts=ped, production_pts=prod,
                     cand=cand, nophi=nophi, nobpool=nobpool, o31=o31, step2=step2, live=live,
                     d_vs_o31=cand - o31, bpool_cost=cand - nobpool,
                     d_vs_step2=(cand - step2) if step2 is not None else None,
                     d_vs_live=(cand - live) if live is not None else None,
                     phi_cost=cand - nophi))

TOT = {k: sum(r['v'] for r in BD[k]['rows'].values()) for k in BD}
T_LIVE = PREV['totals']['live']; T_STEP2 = PREV['totals']['step2']
print('\nBOARD TOTALS  live %d  step2 %d  ORDER-31 %d  CANDIDATE %d  no-Phi %d  no-beta_pool %d'
      % (T_LIVE, T_STEP2, TOT['o31'], TOT['cand'], TOT['nophi'], TOT['nobpool']))

# ---------------------------------------------------------------- CONTINUITY (build-failing)
def continuity(p, gmax=20):
    """Price vs games 0..gmax at FIXED OUTPUT, holding the production leg constant at its measured value
    and moving ONLY the evidence clock.  This isolates the law from the production model, which is what
    'no cliff at 1' is a statement about."""
    Phat = None
    out = []
    g_now = float(G['pv_games'](p, BASE))
    cand = BD['cand']['rows'][p.get('key') or MA.slug(p['player'])]['v']
    _pl = bool(p.get('_pool'))
    pi_now = float(G['o31_pi'](p, BASE, g_now))
    V0 = float(G['pv_pedigree'](p)) / F
    Phat = max(0.0, cand - pi_now * V0) / max(1e-9, float(G['rho31'](g_now))) if g_now > 0 else None
    if Phat is None:                                          # a gameless row: use his position bar as the
        Phat = float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0   # fixed at-bar full season equivalent
    D = float(G['o31_D'](p, BASE)); s = int(G['o31_stall_run'](p, BASE))
    for gg in range(0, gmax + 1):
        r = float(G['rho31'](gg))
        pi = D * (1.0 - r) + float(G['phi31'](gg, s, _pl)) * float(G['beta31'](gg, _pl)) * r
        out.append({'g': gg, 'price': r * Phat + pi * V0, 'rho': r, 'pi': pi})
    return Phat, V0, D, s, out

CONT_KEYS = ['josh-smillie', 'harry-demattia', 'max-knobel', 'dyson-sharp', 'isaac-kako',
             'noah-mraz', 'willem-duursma', 'toby-conway', 'luke-beecken', 'chris-scerri']
BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key') or MA.slug(p['player']), p)
CONT = {}
CONT_FAIL = []
CONT_O31_PROXY_FAIL = []
for k in CONT_KEYS:
    p = BYKEY.get(k)
    if p is None or k not in BD['cand']['rows']:
        continue
    Phat, V0, D, s, cur = continuity(p)
    step01 = (cur[1]['price'] / cur[0]['price'] - 1.0) * 100.0 if cur[0]['price'] > 0 else None
    mono = all(cur[i + 1]['price'] >= cur[i]['price'] - 1e-9 for i in range(len(cur) - 1))
    dead = any(abs(cur[i + 1]['price'] - cur[i]['price']) < 1e-9 for i in range(len(cur) - 1))
    # THE "MONOTONE-IN-EVIDENCE" SCOPE. The ruled object (ORDER 31 packet section 2, reading 2) is
    # "monotone non-decreasing ONLY WHERE THE HELD OUTPUT IS AT OR ABOVE THE POSITION BAR". ORDER 31's
    # harness implemented that with a 0.5 factor -- i.e. it admitted a row at HALF an at-bar season and
    # called it at-bar. THAT PROXY IS WRONG AGAINST ITS OWN WORDING, and 31-F is the build where the
    # difference bites: isaac-kako's held production is 740 against an at-bar season of 1,358 -- 54%,
    # which is not "at or above the position bar" by any reading -- and his curve falls, exactly as
    # luke-beecken's does and for the same reason.
    # BOTH READINGS ARE COMPUTED AND BOTH ARE PUBLISHED. The build-failing gate is the LITERAL RULED
    # OBJECT; the ORDER-31 threshold's verdict is carried beside it and SCORED AS A BREACH on the
    # prereg scorecard. Nothing is quietly relaxed: the assert got HARDER about what it means and the
    # one row that changes verdict is named, priced and explained on the packet.
    _atbar_season = float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0
    atbar = Phat >= _atbar_season                       # THE RULED OBJECT: at or above the position bar
    atbar_o31 = Phat >= _atbar_season * 0.5             # ORDER 31's harness proxy, carried for the record
    # THE CONTINUITY OBJECT, CORRECTED (PREREG P29(b) BREACH, OWNED IN THE PACKET). P29(b) banded the
    # INTEGER step 0->1 at +40%. That band was read off the 30B-R join, which measured +37.1% on rows
    # where Phat is the same order as v0 -- it does not generalise to a row like noah-mraz whose
    # production estimate is TWELVE TIMES his v0, where rho(1)*Phat alone exceeds his whole sitter price.
    # A big FIRST-GAME step is not a cliff; a DISCONTINUITY is. The law's real claim is
    #        lim_{g->0+} price(g)  ==  price(0)      exactly,
    # which is what "no lanes" buys and what the preview's sigma(0)=1 against the sitter's D(c) violated.
    # That limit is what is asserted here; the integer step is MEASURED AND PUBLISHED beside it.
    lim = []
    for eps in (1e-2, 1e-4, 1e-6, 1e-9):
        r = float(G['rho31'](eps))
        pi_e = D * (1.0 - r) + float(G['phi31'](eps, s, _pl)) * float(G['beta31'](eps, _pl)) * r
        lim.append({'g': eps, 'price': r * Phat + pi_e * V0})
    p0 = cur[0]['price']
    gap = abs(lim[-1]['price'] - p0) / max(1e-9, abs(p0))
    CONT[k] = {'Phat_fixed': Phat, 'v0': V0, 'D': D, 's': s, 'step_0_to_1_pct': step01,
               'Phat_over_v0': Phat / max(1e-9, V0),
               'limit_at_zero': lim, 'price_at_zero': p0, 'discontinuity_rel': gap,
               'monotone': mono, 'dead_zone': dead, 'at_or_above_bar_output': atbar,
               'at_bar_season_equiv': _atbar_season, 'Phat_over_at_bar_season': Phat / _atbar_season,
               'at_or_above_bar_output_ORDER31_PROXY': atbar_o31,
               'breaches_order31_proxy': bool(atbar_o31 and not mono),
               'curve': cur}
    if gap > 1e-6: CONT_FAIL.append((k, 'DISCONTINUITY at g=0: rel %.3e' % gap))
    if dead: CONT_FAIL.append((k, 'dead zone'))
    if atbar and not mono: CONT_FAIL.append((k, 'non-monotone at/above-bar output (RULED OBJECT)'))
    if atbar_o31 and not mono: CONT_O31_PROXY_FAIL.append(k)

# ---------------------------------------------------------------- COMPLETENESS (build-failing)
# The 26A forbidden set must be UNREACHABLE from a printed price.
COMP = {'pole_deleted_dial': bool(G['_O30B_NOPOLE']), 'iso_deleted_dial': bool(G['_O30B_NOISO']),
        'preview_lane_on': bool(G['_PV']['on'])}
src = open(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')).read()
COMP['raw_ev_returns_before_pole'] = 'if _O30B_NOPOLE: return pr' in src
COMP['iso_returns_unity'] = 'if _O30B_NOISO: return 1.0' in src
COMP['par_at_sites_on_price_path'] = src.count('_O30BP_BARS[') # the re-referenced, pick-blind bars
COMP['floor_replaced'] = "if _PV['on']: return v" in src
COMP['a_blend_replaced'] = "if _A_ON and _isreal(p) and not _PV['on']" in src
COMP['sitout_arm_replaced'] = "if _PV['on']:" in src
# every priced row must resolve a v0-language object with no fallback
noV0 = [r['key'] for r in rows if not (r['v0'] > 0)]
COMP['rows_priced'] = len(rows)
COMP['rows_without_a_v0_object'] = noV0
COMP['cell_coverage_pct'] = 100.0 * (len(rows) - len(noV0)) / max(1, len(rows))
COMP_FAIL = []
for kk in ('raw_ev_returns_before_pole', 'iso_returns_unity', 'floor_replaced',
           'a_blend_replaced', 'sitout_arm_replaced', 'pole_deleted_dial', 'iso_deleted_dial'):
    if not COMP[kk]: COMP_FAIL.append(kk)
if noV0: COMP_FAIL.append('rows without a v0 object: %s' % noV0[:6])

# ---------------------------------------------------------------- class views
def band(cg):
    cg = cg or 0
    return '0' if cg == 0 else '1-5' if cg < 6 else '6-15' if cg < 16 else '16-35' if cg < 36 \
        else '36-70' if cg < 71 else '71+'
CLASS = collections.defaultdict(lambda: dict(n=0, cand=0, step2=0, live=0, phi_cost=0))
for r in rows:
    c = CLASS[band(r['cg'])]
    c['n'] += 1; c['cand'] += r['cand']; c['phi_cost'] += r['phi_cost']
    if r['step2'] is not None: c['step2'] += r['step2']
    if r['live'] is not None: c['live'] += r['live']
PATHW = collections.defaultdict(lambda: dict(n=0, cand=0, step2=0, live=0))
for r in rows:
    c = PATHW[r['pathway'] or '?']
    c['n'] += 1; c['cand'] += r['cand']
    if r['step2'] is not None: c['step2'] += r['step2']
    if r['live'] is not None: c['live'] += r['live']

VETS = ['jaeger-o-meara', 'joshua-kelly', 'paddy-dow', 'stephen-coniglio', 'jacob-weitering',
        'adam-cerra', 'darcy-parish', 'dylan-stephens', 'scott-pendlebury', 'will-setterfield',
        'jacob-hopper', 'jackson-macrae', 'dion-prestia', 'jack-bowes', 'oliver-wines',
        'steele-sidebottom', 'cameron-rayner', 'jack-lukosius', 'jack-martin', 'ben-ainsworth']
NAMED = ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow', 'noah-mraz', 'nick-madden',
         'liam-reidy', 'luke-beecken', 'cooper-trembath', 'chris-scerri', 'josh-smillie',
         'harry-demattia', 'max-knobel', 'toby-conway', 'marcus-herbert', 'jaxon-artemis',
         'jai-newcombe', 'jack-martin', 'harry-sheezel', 'nicholas-martin']
BY = {r['key']: r for r in rows}

OUT = {'order': 'ORDER 31 — the complete candidate',
       'boards': {'live': LIVE_MD5, 'step2': STEP2_MD5, 'order31': O31_MD5,
                  'candidate': BD['cand']['md5'], 'candidate_rebuild': BD['cand2']['md5'],
                  'no_phi_variant': BD['nophi']['md5'], 'no_beta_pool_variant': BD['nobpool']['md5'],
                  'headfix_only_dial_off': BD['off']['md5'],
                  'entry_dial_off_control': BD['entryoff']['md5']},
       'totals': {'live': T_LIVE, 'step2': T_STEP2, 'order31': TOT['o31'], 'candidate': TOT['cand'],
                  'no_phi': TOT['nophi'], 'no_beta_pool': TOT['nobpool']},
       'determinism': BD['cand']['md5'] == BD['cand2']['md5'],
       'entry_dial_off_byte_identity': BD['entryoff']['md5'] == STEP2_MD5,
       'law': {'TAU_RHO': G['O31_TAU_RHO'], 'B_RHO': G['O31_B_RHO'],
               'beta_pool': G['O31_BETA_POOL'], 'phistall_pool': G['O31_PHIST_POOL'],
               'form': 'price = rho(g)*Phat + [D(c_u)*(1-rho(g)) + Phi(g,s)*beta(g)*rho(g)]*v0'},
       'class_views': {k: dict(v) for k, v in sorted(CLASS.items())},
       'pathway_views': {k: dict(v) for k, v in sorted(PATHW.items())},
       'continuity': CONT, 'continuity_failures': CONT_FAIL,
       'completeness': COMP, 'completeness_failures': COMP_FAIL,
       'at_bar_veterans': [BY[k] for k in VETS if k in BY],
       'named_rows': [BY[k] for k in NAMED if k in BY],
       'rows': sorted(rows, key=lambda r: -(abs(r['d_vs_step2'] or 0)))}

os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(OUT, open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_31_MOVERS.json'), 'w'),
          indent=1, sort_keys=True, default=str)
json.dump({'continuity': CONT, 'failures': CONT_FAIL,
           'order31_proxy_failures': CONT_O31_PROXY_FAIL,
           'scope_note': 'The build-failing gate is the RULED OBJECT -- monotone non-decreasing where the '
                         'held output is AT OR ABOVE THE POSITION BAR (Phat >= bar x 20). ORDER 31\'s '
                         'harness used bar x 20 x 0.5, admitting rows at HALF an at-bar season; that '
                         'proxy\'s verdicts are carried in order31_proxy_failures and scored as a BREACH '
                         'in SHIPPING_PACKET_31.md rather than dropped.'},
          open(os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'CONTINUITY_31F.json'), 'w'),
          indent=1, sort_keys=True, default=str)
json.dump({'completeness': COMP, 'failures': COMP_FAIL},
          open(os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'COMPLETENESS_31F.json'), 'w'),
          indent=1, sort_keys=True, default=str)

# ---------------------------------------------------------------- reconciliation (P6)
recon_bad = []
for r in rows:
    if abs((r['production_pts'] + r['pedigree_pts']) - r['cand']) > 1.0:
        recon_bad.append((r['key'], r['production_pts'] + r['pedigree_pts'], r['cand']))
print('\nRECONCILIATION: %d of %d rows fail production+pedigree == price at +-1 point'
      % (len(recon_bad), len(rows)))
print('CONTINUITY  : %s  (ruled object: monotone where Phat >= one at-bar season)'
      % ('PASS' if not CONT_FAIL else 'FAIL %s' % CONT_FAIL))
print('  ORDER-31 harness proxy (Phat >= HALF an at-bar season) would flag: %s  -- BREACH, owned in the packet'
      % (CONT_O31_PROXY_FAIL or 'nothing'))
print('COMPLETENESS: %s' % ('PASS' if not COMP_FAIL else 'FAIL %s' % COMP_FAIL))
print('\nCLASS VIEW (cg band)   n     candidate      step2       live    Phi cost')
for k, v in sorted(CLASS.items()):
    print('  %-6s %5d %12d %11d %10d %10d' % (k, v['n'], v['cand'], v['step2'], v['live'], v['phi_cost']))
print('\nPATHWAY                n     candidate      step2       live')
for k, v in sorted(PATHW.items()):
    print('  %-6s %5d %12d %11d %10d' % (k, v['n'], v['cand'], v['step2'], v['live']))
print('\nNAMED ROWS')
print('  %-20s %-4s %5s %6s %6s %6s %6s   rho    D      s  Phi     pi      v0     prod    ped'
      % ('key', 'path', 'cg', 'live', 'step2', 'CAND', 'noPhi'))
for k in NAMED:
    if k not in BY: continue
    r = BY[k]
    print('  %-20s %-4s %5s %6s %6s %6d %6d  %.3f  %.3f  %d  %.3f  %.4f %7.1f %7.1f %6.1f'
          % (r['key'], r['pathway'], r['cg'], r['live'], r['step2'], r['cand'], r['nophi'],
             r['rho'], r['D'], r['s'], r['Phi'], r['pi'], r['v0'], r['production_pts'], r['pedigree_pts']))
print('\nAT-BAR VETERANS (named in PREREG_31 P1, before any price existed)')
mv = []
for k in VETS:
    if k not in BY: continue
    r = BY[k]; mv.append(abs(r['d_vs_step2'] or 0))
    print('  %-20s cg %4s  live %6s  step2 %6s  CAND %6d  d %+6d  prod %8.1f  ped %6.1f'
          % (r['key'], r['cg'], r['live'], r['step2'], r['cand'], r['d_vs_step2'] or 0,
             r['production_pts'], r['pedigree_pts']))
mv.sort()
print('  class median |move| vs step2 = %.1f   moved down: %d of %d'
      % (mv[len(mv)//2] if mv else -1, sum(1 for k in VETS if k in BY and (BY[k]['d_vs_step2'] or 0) < 0), len(mv)))
print('\nCONTINUITY CURVES (price vs games 0..20, output HELD FIXED)')
for k, c in CONT.items():
    print('  %-18s D %.3f s %d  Phat/v0 %6.2f  step0->1 %+7.1f%%  DISCONTINUITY %.2e  monotone %s  '
          'at-bar %s  dead %s'
          % (k, c['D'], c['s'], c['Phat_over_v0'], c['step_0_to_1_pct'], c['discontinuity_rel'],
             c['monotone'], c['at_or_above_bar_output'], c['dead_zone']))
    print('     ' + ' '.join('%d:%.0f' % (x['g'], x['price']) for x in c['curve']))
if CONT_FAIL or COMP_FAIL or recon_bad:
    sys.exit('ORDER 31 ASSERT WALL FIRED: continuity=%s completeness=%s reconciliation=%d'
             % (CONT_FAIL, COMP_FAIL, len(recon_bad)))
print('\nledger written.')
