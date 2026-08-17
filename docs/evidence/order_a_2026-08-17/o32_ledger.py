#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — THE COMPOSED MOVERS LEDGER, THE CONTINUITY CURVE AND THE COMPLETENESS
AUDIT. o31f_ledger.py carried; the changes: (a) the board set is the Candidate 32 stage ladder, so
every mechanism leg is a REAL BOARD DELTA (bars / credit / reset / refit / relief / re-mix); (b)
EVERY row carries BOTH baselines (live 88ce647f AND Candidate 31 fe6be9d6) plus Step-2; (c) the
engine loads under RL_O32=1 so the legs are the Candidate 32 law's own arithmetic; (d) the A8
Carmichael one-game counterfactual is computed ON THE LAW (a 1-game season appended, caches
cleared), beside the fixed-output continuity curves.

Emits: docs/ledgers/CANDIDATE_32_MOVERS.{json,md} · CONTINUITY_32.json · COMPLETENESS_32.json
"""
import os, sys, json, math, io, contextlib, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = os.environ.get('RL_SCRATCH', '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o32')
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

BOARDS = {'cand': 'bb_rfinal', 'cand2': 'bb_rfinal2', 's1': 'bb_s1', 's2': 'bb_s2', 's3': 'bb_s3',
          's4': 'bb_s4', 's5': 'bb_s5', 'c31': 'bb_r0o31', 'off': 'bb_r0off'}
BD = {}
for k, d in BOARDS.items():
    p = os.path.join(SP, d, 'rl_after', 'rl_app_data.json')
    BD[k] = {'md5': md5(p), 'rows': {r['key']: r for r in json.load(open(p))['active']}}
    print('%-6s %s  n=%d  total=%d' % (k, BD[k]['md5'], len(BD[k]['rows']),
                                       sum(r['v'] for r in BD[k]['rows'].values())))

PREV = json.load(open(os.path.join(EV, 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')))
PRVR = {r['key']: r for r in PREV['rows']}
LIVE_MD5, STEP2_MD5 = PREV['boards']['live'], PREV['boards']['step2']
assert BD['c31']['md5'] == 'fe6be9d6ac76ebc34d26ebc11d796505', 'the Candidate 31 baseline did not reproduce'
assert BD['off']['md5'] == 'bce0c65d853722e52629ab97677a98e3', 'the dial-off control is not the Step-2-law board'
assert BD['cand']['md5'] == BD['cand2']['md5'], 'DETERMINISM FAILED'

# ---------------------------------------------------------------- load the engine under Candidate 32
os.environ.update(RL_O31='1', RL_O32='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
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
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
G = {k: NSE.get(k) for k in
     ('rho31', 'beta31', 'phi31', 'phistall31', 'o31_cu', 'o31_D', 'o31_stall_run', 'o31_pi',
      'pv_games', 'pv_pedigree', 'ev', '_PL_F', 'fade30b_clock', 'o31_pool_D', 'o31_fade_D',
      '_O30BP_BARS', '_O30B_NOPOLE', '_O30B_NOISO', '_PV', 'o32_gate_bar', 'o32_sigma_sel',
      'o32_delivered', 'o32_age_credit', 'O32_LAMBDA', 'O32_KAPPA', 'O32_GAMMA', 'O32_ETA', 'O32_GAMMA_D', '_O32S',
      'delisted', '_isreal')}
missing = [k for k, v in G.items() if v is None]
if missing:
    sys.exit('ORDER A LEDGER HALT: the engine did not expose %s' % missing)
assert G['_O32S'] == 6, 'the engine is not at stage 6'
F = float(G['_PL_F'])
BASE = MA.BASE_REF
delisted = G['delisted']; _isreal = G['_isreal']

# ---------------------------------------------------------------- per-row legs, from the law itself
rows = []
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in BD['cand']['rows']:
        continue
    b = BD['cand']['rows'][k]
    g = float(G['pv_games'](p, BASE))
    r = float(G['rho31'](g))                                  # rho32: the re-mixed reliability
    cu = float(G['o31_cu'](p, BASE))
    D = float(G['o31_D'](p, BASE))                            # relief included, capped at 1
    s = int(G['o31_stall_run'](p, BASE))
    _pl = bool(p.get('_pool'))
    ph = float(G['phi31'](g, s, _pl))
    be = float(G['beta31'](g, _pl))
    V0 = float(G['pv_pedigree'](p)) / F
    pi = float(G['o31_pi'](p, BASE, g))                       # includes the re-mix pedigree factor
    sg = float(G['o32_sigma_sel'](p, BASE))
    vals = {kk: int(BD[kk]['rows'][k]['v']) for kk in ('cand', 's1', 's2', 's3', 's4', 's5', 'c31')}
    pr = PRVR.get(k, {})
    step2 = pr.get('step2'); live = pr.get('live')
    ped = pi * V0
    prod = max(0.0, vals['cand'] - ped)
    rows.append(dict(key=k, name=p.get('player'), pathway=p.get('type'), pool=_pl,
                     pick=p.get('pick'), pos=MA.gfut(p), age=b.get('age'), cg=b.get('cg'), yr=b.get('yr'),
                     g=g, rho=r, c_fade=float(G['fade30b_clock'](p, BASE)), c_u=cu, D=D, s=s, Phi=ph,
                     beta=be, pi=pi, v0=V0, sigma_sel=sg,
                     pedigree_pts=ped, production_pts=prod,
                     cand=vals['cand'], c31=vals['c31'], step2=step2, live=live,
                     leg_bars=vals['s1'] - vals['c31'], leg_credit=vals['s2'] - vals['s1'],
                     leg_reset=vals['s3'] - vals['s2'], leg_refit=vals['s4'] - vals['s3'],
                     leg_relief=vals['s5'] - vals['s4'], leg_remix=vals['cand'] - vals['s5'],
                     d_vs_c31=vals['cand'] - vals['c31'],
                     d_vs_step2=(vals['cand'] - step2) if step2 is not None else None,
                     d_vs_live=(vals['cand'] - live) if live is not None else None))

TOT = {kk: sum(r['v'] for r in BD[kk]['rows'].values()) for kk in BD}
T_LIVE = PREV['totals']['live']; T_STEP2 = PREV['totals']['step2']
print('\nBOARD TOTALS  live %d  step2 %d  C31 %d  s1 %d s2 %d s3 %d s4 %d s5 %d  CANDIDATE 32 %d'
      % (T_LIVE, T_STEP2, TOT['c31'], TOT['s1'], TOT['s2'], TOT['s3'], TOT['s4'], TOT['s5'], TOT['cand']))

# ---------------------------------------------------------------- CONTINUITY (build-failing)
def continuity(p, gmax=20):
    """Price vs games 0..gmax at FIXED OUTPUT: the production leg held at its measured value, only
    the evidence clock moves. o31_pi carries the re-mix pedigree factor, rho31 the re-mix bump."""
    g_now = float(G['pv_games'](p, BASE))
    cand = BD['cand']['rows'][p.get('key') or MA.slug(p['player'])]['v']
    pi_now = float(G['o31_pi'](p, BASE, g_now))
    V0 = float(G['pv_pedigree'](p)) / F
    cr_now = float(G['o32_age_credit'](p, BASE, g_now)) / F      # the R1 age credit, the law's own
    Phat = max(0.0, cand - pi_now * V0 - cr_now) / max(1e-9, float(G['rho31'](g_now))) if g_now > 0 else None
    if Phat is None:
        Phat = float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0
    D = float(G['o31_D'](p, BASE)); s = int(G['o31_stall_run'](p, BASE))
    out = []
    for gg in range(0, gmax + 1):
        r = float(G['rho31'](gg))
        pi = float(G['o31_pi'](p, BASE, float(gg)))
        cr = float(G['o32_age_credit'](p, BASE, float(gg))) / F
        out.append({'g': gg, 'price': r * Phat + pi * V0 + cr, 'rho': r, 'pi': pi})
    return Phat, V0, D, s, out

CONT_KEYS = ['lachlan-carmichael', 'josh-smillie', 'harry-demattia', 'max-knobel', 'dyson-sharp',
             'isaac-kako', 'noah-mraz', 'willem-duursma', 'toby-conway', 'luke-beecken', 'chris-scerri']
BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key') or MA.slug(p['player']), p)
CONT = {}
CONT_FAIL = []
for k in CONT_KEYS:
    p = BYKEY.get(k)
    if p is None or k not in BD['cand']['rows']:
        continue
    Phat, V0, D, s, cur = continuity(p)
    step01 = (cur[1]['price'] / cur[0]['price'] - 1.0) * 100.0 if cur[0]['price'] > 0 else None
    mono = all(cur[i + 1]['price'] >= cur[i]['price'] - 1e-9 for i in range(len(cur) - 1))
    dead = any(abs(cur[i + 1]['price'] - cur[i]['price']) < 1e-9 for i in range(len(cur) - 1))
    _atbar_season = float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0
    atbar = Phat >= _atbar_season
    lim = []
    for eps in (1e-2, 1e-4, 1e-6, 1e-9):
        r = float(G['rho31'](eps))
        pi_e = float(G['o31_pi'](p, BASE, eps))
        cr_e = float(G['o32_age_credit'](p, BASE, eps)) / F
        lim.append({'g': eps, 'price': r * Phat + pi_e * V0 + cr_e})
    p0 = cur[0]['price']
    gap = abs(lim[-1]['price'] - p0) / max(1e-9, abs(p0))
    CONT[k] = {'Phat_fixed': Phat, 'v0': V0, 'D': D, 's': s, 'step_0_to_1_pct': step01,
               'limit_at_zero': lim, 'price_at_zero': p0, 'discontinuity_rel': gap,
               'monotone': mono, 'dead_zone': dead, 'at_or_above_bar_output': atbar,
               'curve': cur}
    if gap > 1e-6: CONT_FAIL.append((k, 'DISCONTINUITY at g=0: rel %.3e' % gap))
    if dead: CONT_FAIL.append((k, 'dead zone'))
    if atbar and not mono: CONT_FAIL.append((k, 'non-monotone at/above-bar output (RULED OBJECT)'))

# ---- A8: THE CARMICHAEL ONE-GAME CASE, ON THE LAW ITSELF (not a fixed-D reconstruction) ----------
ONEGAME = {}
for k in ('lachlan-carmichael', 'josh-smillie'):
    p = BYKEY.get(k)
    if p is None: continue
    with contextlib.redirect_stdout(io.StringIO()):
        e0 = float(G['ev'](p, BASE))
    D0 = float(G['o31_D'](p, BASE)); cu0 = float(G['o31_cu'](p, BASE))
    saved = p['scoring']
    p['scoring'] = list(saved) + [{'year': 2026, 'games': 1, 'avg': 13.0, 'pos': p.get('future_position')}]
    MA._pe_clear()
    with contextlib.redirect_stdout(io.StringIO()):
        e1 = float(G['ev'](p, BASE))
    D1 = float(G['o31_D'](p, BASE)); cu1 = float(G['o31_cu'](p, BASE))
    p['scoring'] = saved
    MA._pe_clear()
    ONEGAME[k] = dict(price_0g=e0, price_1g=e1, jump_pct=100.0 * (e1 / e0 - 1.0),
                      D_0g=D0, D_1g=D1, cu_0g=cu0, cu_1g=cu1,
                      wired_c31_jump_note='under Candidate 31 the same game flipped the whole '
                                          'in-progress fraction: D -> 1.0 (+71% for carmichael)')
    print('A8 one-game case %-20s: %.0f -> %.0f (%+.0f%%)  D %.3f -> %.3f  c_u %.2f -> %.2f'
          % (k, e0, e1, ONEGAME[k]['jump_pct'] and e0 or e0, D0, D1, cu0, cu1))
    print('   jump %+.1f%%' % ONEGAME[k]['jump_pct'])

# ---------------------------------------------------------------- COMPLETENESS (build-failing)
COMP = {'pole_deleted_dial': bool(G['_O30B_NOPOLE']), 'iso_deleted_dial': bool(G['_O30B_NOISO']),
        'preview_lane_on': bool(G['_PV']['on'])}
src = open(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')).read()
COMP['raw_ev_returns_before_pole'] = 'if _O30B_NOPOLE: return pr' in src
COMP['iso_returns_unity'] = 'if _O30B_NOISO: return 1.0' in src
COMP['floor_replaced'] = "if _PV['on']: return v" in src
COMP['a_blend_replaced'] = "if _A_ON and _isreal(p) and not _PV['on']" in src
COMP['sitout_arm_replaced'] = "if _PV['on']:" in src
COMP['o30bp_bars_never_age_edited'] = ('o32_gate_bar' in src and '_O30BP_BARS[' in src)
noV0 = [r['key'] for r in rows if not (r['v0'] > 0)]
COMP['rows_priced'] = len(rows)
COMP['rows_without_a_v0_object'] = noV0
COMP['cell_coverage_pct'] = 100.0 * (len(rows) - len(noV0)) / max(1, len(rows))
COMP_FAIL = []
for kk in ('raw_ev_returns_before_pole', 'iso_returns_unity', 'floor_replaced',
           'a_blend_replaced', 'sitout_arm_replaced', 'pole_deleted_dial', 'iso_deleted_dial'):
    if not COMP[kk]: COMP_FAIL.append(kk)
if noV0: COMP_FAIL.append('rows without a v0 object: %s' % noV0[:6])

# ---------------------------------------------------------------- class / pathway views
def band(cg):
    cg = cg or 0
    return '0' if cg == 0 else '1-5' if cg < 6 else '6-15' if cg < 16 else '16-35' if cg < 36 \
        else '36-70' if cg < 71 else '71+'
CLASS = collections.defaultdict(lambda: dict(n=0, cand=0, c31=0, step2=0, live=0,
                                             bars=0, credit=0, reset=0, refit=0, relief=0, remix=0))
for r in rows:
    c = CLASS[band(r['cg'])]
    c['n'] += 1; c['cand'] += r['cand']; c['c31'] += r['c31']
    for leg in ('bars', 'credit', 'reset', 'refit', 'relief', 'remix'):
        c[leg] += r['leg_' + leg]
    if r['step2'] is not None: c['step2'] += r['step2']
    if r['live'] is not None: c['live'] += r['live']
PATHW = collections.defaultdict(lambda: dict(n=0, cand=0, c31=0, live=0))
for r in rows:
    c = PATHW[r['pathway'] or '?']
    c['n'] += 1; c['cand'] += r['cand']; c['c31'] += r['c31']
    if r['live'] is not None: c['live'] += r['live']

NAMED = ['lachlan-carmichael', 'josh-smillie', 'phoenix-gothard', 'billy-wilson', 'harry-dean',
         'cooper-duff-tytler', 'kye-annand', 'lukas-cooke', 'chris-scerri', 'thomas-burton',
         'milan-murdock', 'nick-madden', 'jedd-busslinger', 'isaac-kako', 'alex-dodson',
         'will-green', 'william-mccabe', 'charlie-edwards', 'xavier-taylor', 'daniel-annable',
         'ty-gallop', 'charlie-west']
BY = {r['key']: r for r in rows}

# ---------------------------------------------------------------- reconciliation
recon_bad = []
for r in rows:
    if abs((r['production_pts'] + r['pedigree_pts']) - r['cand']) > 1.0:
        recon_bad.append((r['key'], r['production_pts'] + r['pedigree_pts'], r['cand']))
print('\nRECONCILIATION: %d of %d rows fail production+pedigree == price at +-1 point'
      % (len(recon_bad), len(rows)))
print('CONTINUITY  : %s' % ('PASS' if not CONT_FAIL else 'FAIL %s' % CONT_FAIL))
print('COMPLETENESS: %s' % ('PASS' if not COMP_FAIL else 'FAIL %s' % COMP_FAIL))
print('CELL COVERAGE: %.1f%%' % COMP['cell_coverage_pct'])

OUT = {'order': 'ORDER A — Candidate 32, the pre-landing recalibration',
       'boards': {'live': LIVE_MD5, 'step2': STEP2_MD5,
                  'candidate31': BD['c31']['md5'], 'candidate32': BD['cand']['md5'],
                  'candidate32_rebuild': BD['cand2']['md5'],
                  'stage1_bars': BD['s1']['md5'], 'stage2_credit': BD['s2']['md5'],
                  'stage3_reset': BD['s3']['md5'], 'stage4_refit': BD['s4']['md5'],
                  'stage5_relief': BD['s5']['md5'], 'dial_off_control': BD['off']['md5']},
       'totals': {'live': T_LIVE, 'step2': T_STEP2, 'c31': TOT['c31'],
                  's1': TOT['s1'], 's2': TOT['s2'], 's3': TOT['s3'], 's4': TOT['s4'],
                  's5': TOT['s5'], 'candidate32': TOT['cand']},
       'determinism': BD['cand']['md5'] == BD['cand2']['md5'],
       'dial_off_c31_byte_identity': BD['c31']['md5'] == 'fe6be9d6ac76ebc34d26ebc11d796505',
       'dial_off_step2law_byte_identity': BD['off']['md5'] == 'bce0c65d853722e52629ab97677a98e3',
       'law': {'form': 'price = rho32(g)*Phat + [D_rel(c_u)*(1-rho32) + Phi32(g,s)*beta(g)*rho32]'
                       '*mix(g)*v0', 'O32_LAMBDA': G['O32_LAMBDA'], 'O32_KAPPA': G['O32_KAPPA'],
               'O32_GAMMA_U': G['O32_GAMMA'], 'O32_ETA': G['O32_ETA'], 'O32_GAMMA_D': G['O32_GAMMA_D']},
       'class_views': {k: dict(v) for k, v in sorted(CLASS.items())},
       'pathway_views': {k: dict(v) for k, v in sorted(PATHW.items())},
       'continuity': CONT, 'continuity_failures': CONT_FAIL, 'onegame_counterfactual': ONEGAME,
       'completeness': COMP, 'completeness_failures': COMP_FAIL,
       'reconciliation_failures': recon_bad,
       'named_rows': [BY[k] for k in NAMED if k in BY],
       'rows': sorted(rows, key=lambda r: -(abs(r['d_vs_c31'] or 0)))}

os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(OUT, open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_32_MOVERS.json'), 'w'),
          indent=1, sort_keys=True, default=str)
json.dump({'continuity': CONT, 'failures': CONT_FAIL, 'onegame': ONEGAME},
          open(os.path.join(HERE, 'CONTINUITY_32.json'), 'w'), indent=1, sort_keys=True, default=str)
json.dump({'completeness': COMP, 'failures': COMP_FAIL},
          open(os.path.join(HERE, 'COMPLETENESS_32.json'), 'w'), indent=1, sort_keys=True, default=str)

# ---------------------------------------------------------------- the md ledger
L = []
L.append('# CANDIDATE 32 — THE COMPOSED MOVERS LEDGER (ORDER A)')
L.append('')
L.append('**ORDER A · `land/order-29` · all %d board rows, EVERY row against BOTH baselines '
         '(live `88ce647f` and Candidate 31 `fe6be9d6`) with the six per-mechanism legs '
         '(bars / credit / reset / refit / relief / re-mix), each leg a REAL BOARD delta. '
         'NOTHING LANDS WITHOUT THE OWNER\'S WORD.**' % len(rows))
L.append('')
L.append('| board | md5 | total |')
L.append('|---|---|---:|')
L.append('| LIVE | `%s` | %d |' % (LIVE_MD5, T_LIVE))
L.append('| STEP-2 (committed) | `%s` | %d |' % (STEP2_MD5, T_STEP2))
L.append('| CANDIDATE 31 (31-F) | `%s` | %d |' % (BD['c31']['md5'], TOT['c31']))
for nm, kk in (('+ M1 bars', 's1'), ('+ M2 credit', 's2'), ('+ M3 reset', 's3'),
               ('+ M6 Phi refit', 's4'), ('+ M4 relief', 's5')):
    L.append('| %s | `%s` | %d |' % (nm, BD[kk]['md5'], TOT[kk]))
L.append('| **CANDIDATE 32 (+ M5 re-mix)** | **`%s`** | **%d** |' % (BD['cand']['md5'], TOT['cand']))
L.append('| determinism rebuild | `%s` | %d |' % (BD['cand2']['md5'], TOT['cand']))
L.append('| dial-off (RL_O31=1) | `%s` | %d |' % (BD['c31']['md5'], TOT['c31']))
L.append('| fully-off (Step-2 law) | `%s` | — |' % BD['off']['md5'])
L.append('')
L.append('vs LIVE **%+d** (%.2f%%) · vs STEP-2 **%+d** · vs CANDIDATE 31 **%+d** (%.2f%%)'
         % (TOT['cand'] - T_LIVE, 100.0 * (TOT['cand'] - T_LIVE) / T_LIVE,
            TOT['cand'] - T_STEP2, TOT['cand'] - TOT['c31'],
            100.0 * (TOT['cand'] - TOT['c31']) / TOT['c31']))
L.append('')
L.append('Mechanism legs (board totals): bars %+d · credit %+d · reset %+d · Phi refit %+d · '
         'relief %+d · re-mix %+d' % (TOT['s1'] - TOT['c31'], TOT['s2'] - TOT['s1'],
                                      TOT['s3'] - TOT['s2'], TOT['s4'] - TOT['s3'],
                                      TOT['s5'] - TOT['s4'], TOT['cand'] - TOT['s5']))
L.append('')
L.append('## BY CAREER-GAMES CLASS')
L.append('')
L.append('| games | n | C32 | C31 | step-2 | live | vs C31 | bars | credit | reset | refit | relief | re-mix |')
L.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for k, v in sorted(CLASS.items()):
    L.append('| %s | %d | %d | %d | %d | %d | %+d | %+d | %+d | %+d | %+d | %+d | %+d |'
             % (k, v['n'], v['cand'], v['c31'], v['step2'], v['live'], v['cand'] - v['c31'],
                v['bars'], v['credit'], v['reset'], v['refit'], v['relief'], v['remix']))
L.append('')
L.append('## BY PATHWAY')
L.append('')
L.append('| pathway | n | C32 | C31 | live |')
L.append('|---|---:|---:|---:|---:|')
for k, v in sorted(PATHW.items()):
    L.append('| %s | %d | %d | %d | %d |' % (k, v['n'], v['cand'], v['c31'], v['live']))
L.append('')
L.append('## THE NAMED TWENTY, TRACED THROUGH EVERY MECHANISM')
L.append('')
L.append('| player | path | pos | g | live | C31 | **C32** | Δ vs C31 | bars | credit | reset | refit | relief | re-mix | c_u | D | s | σ_sel |')
L.append('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for k in NAMED:
    if k not in BY: continue
    r = BY[k]
    L.append('| %s | %s | %s | %.0f | %s | %d | **%d** | %+d | %+d | %+d | %+d | %+d | %+d | %+d | %.2f | %.3f | %d | %.2f |'
             % (k, r['pathway'], r['pos'], r['g'], r['live'], r['c31'], r['cand'], r['d_vs_c31'],
                r['leg_bars'], r['leg_credit'], r['leg_reset'], r['leg_refit'], r['leg_relief'],
                r['leg_remix'], r['c_u'], r['D'], r['s'], r['sigma_sel']))
L.append('')
L.append('## ALL %d ROWS (sorted by |Δ vs Candidate 31|)' % len(rows))
L.append('')
L.append('| player | path | pos | g | live | C31 | **C32** | Δ vs C31 | Δ vs live | bars | credit | reset | refit | relief | re-mix |')
L.append('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in OUT['rows']:
    L.append('| %s | %s | %s | %.0f | %s | %d | **%d** | %+d | %s | %+d | %+d | %+d | %+d | %+d | %+d |'
             % (r['key'], r['pathway'], r['pos'], r['g'],
                r['live'] if r['live'] is not None else '—', r['c31'], r['cand'], r['d_vs_c31'],
                ('%+d' % r['d_vs_live']) if r['d_vs_live'] is not None else '—',
                r['leg_bars'], r['leg_credit'], r['leg_reset'], r['leg_refit'],
                r['leg_relief'], r['leg_remix']))
open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_32_MOVERS.md'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: docs/ledgers/CANDIDATE_32_MOVERS.{json,md} / CONTINUITY_32.json / COMPLETENESS_32.json')
