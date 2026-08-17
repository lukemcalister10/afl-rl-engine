#!/usr/bin/env python3
"""ORDER C — THE MOVERS LEDGER (FOUR VALUE COLUMNS), THE MATURE-ROW BYTE-IDENTITY ASSERT, THE AGE
AND GAMES CONTINUITY OBJECTS, AND THE COMPLETENESS AUDIT. o32_ledger.py carried; the changes:
(a) the board set is the ORDER C ladder (repaired C32 -> +surface -> +credit scale alpha), so both
mechanism legs are REAL BOARD DELTAS; (b) EVERY row carries all four value columns the owner asked
for (live 88ce647f · Candidate 31 fe6be9d6 · repaired C32 7802ee97 · Order C); (c) the engine loads
under RL_O34=1 so the legs are the Order C law's own arithmetic; (d) the STORE-WIDE mature-row
byte-identity assert (age 24+ unmoved vs 7802ee97, milan-murdock asserted by name) is BUILD-FAILING;
(e) the AGE-CONTINUITY table (delta by integer age) is emitted beside the games-continuity curves.

Emits: docs/ledgers/ORDER_C_MOVERS.{json,md} · CONTINUITY_34.json · COMPLETENESS_34.json
"""
import os, sys, json, math, io, contextlib, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SPB = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
SP = SPB + '/o34'
SP32 = SPB + '/o32'
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

BOARDS = {'cand': (SP, 'bb_final'), 'cand2': (SP, 'bb_final2'), 'surf': (SP, 'bb_o34diag1'),
          'c32r': (SP, 'bb_o32ctrl'), 'c31': (SP32, 'bb_r0o31'), 'off': (SP32, 'bb_r0off')}
BD = {}
for k, (sp, d) in BOARDS.items():
    p = os.path.join(sp, d, 'rl_after', 'rl_app_data.json')
    BD[k] = {'md5': md5(p), 'rows': {r['key']: r for r in json.load(open(p))['active']}}
    print('%-6s %s  n=%d  total=%d' % (k, BD[k]['md5'], len(BD[k]['rows']),
                                       sum(r['v'] for r in BD[k]['rows'].values())))

PREV = json.load(open(os.path.join(EV, 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')))
PRVR = {r['key']: r for r in PREV['rows']}
LIVE_MD5, STEP2_MD5 = PREV['boards']['live'], PREV['boards']['step2']
assert BD['c31']['md5'] == 'fe6be9d6ac76ebc34d26ebc11d796505', 'the Candidate 31 baseline did not reproduce'
assert BD['off']['md5'] == 'bce0c65d853722e52629ab97677a98e3', 'the fully-off control is not the Step-2-law board'
assert BD['c32r']['md5'] == '7802ee977cd5e8972010b09f1bb1bee6', 'the repaired C32 dial-off identity broke'
assert BD['cand']['md5'] == BD['cand2']['md5'], 'DETERMINISM FAILED'

# ------------------------------------------------- ORDER C MATURE-ROW BYTE-IDENTITY (BUILD-FAILING)
MAT_BAD = []
N_MAT = 0
for k, r in BD['cand']['rows'].items():
    age = r.get('age')
    if age is not None and age >= 24:
        N_MAT += 1
        if BD['c32r']['rows'][k] != r:
            MAT_BAD.append(k)
print('\nMATURE-ROW BYTE-IDENTITY: %d age-24+ rows, %d moved vs repaired C32 -> %s'
      % (N_MAT, len(MAT_BAD), 'PASS' if not MAT_BAD else 'FAIL %s' % MAT_BAD[:8]))
assert not MAT_BAD, 'ORDER C HALT: mature rows moved'
assert BD['cand']['rows']['milan-murdock'] == BD['c32r']['rows']['milan-murdock'], 'murdock moved'
print('milan-murdock (age 26): BYTE-UNMOVED — asserted by name')

# ---------------------------------------------------------------- load the engine under ORDER C
os.environ.update(RL_O31='1', RL_O32='1', RL_O34='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
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
      'o32_delivered', 'o32_age_credit', 'O32_LAMBDA', 'O32_KAPPA', 'O32_GAMMA', 'O32_ETA',
      'O32_GAMMA_D', '_O32S', '_O34', '_o34_par', 'O34_ALPHA', 'delisted', '_isreal')}
missing = [k for k, v in G.items() if v is None and k != 'O34_ALPHA']
if missing:
    sys.exit('ORDER C LEDGER HALT: the engine did not expose %s' % missing)
assert G['_O32S'] == 6 and G['_O34'], 'the engine is not the Order C configuration'
F = float(G['_PL_F'])
BASE = MA.BASE_REF
delisted = G['delisted']; _isreal = G['_isreal']

# ---------------------------------------------------------------- per-row legs, from the law itself
rows = []
NO_BY = 0
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in BD['cand']['rows']:
        continue
    b = BD['cand']['rows'][k]
    if not p.get('_by'):
        NO_BY += 1
    g = float(G['pv_games'](p, BASE))
    r = float(G['rho31'](g))
    cu = float(G['o31_cu'](p, BASE))
    D = float(G['o31_D'](p, BASE))
    s = int(G['o31_stall_run'](p, BASE))
    _pl = bool(p.get('_pool'))
    ph = float(G['phi31'](g, s, _pl))
    be = float(G['beta31'](g, _pl))
    V0 = float(G['pv_pedigree'](p)) / F
    pi = float(G['o31_pi'](p, BASE, g))
    sg = float(G['o32_sigma_sel'](p, BASE))
    cr = float(G['o32_age_credit'](p, BASE, g)) / F
    par34 = float(G['_o34_par'](MA.gfut(p), p, BASE))
    vals = {kk: int(BD[kk]['rows'][k]['v']) for kk in ('cand', 'surf', 'c32r', 'c31')}
    pr = PRVR.get(k, {})
    live = pr.get('live')
    ped = pi * V0
    prod = max(0.0, vals['cand'] - ped)
    rows.append(dict(key=k, name=p.get('player'), pathway=p.get('type'), pool=_pl,
                     pick=p.get('pick'), pos=MA.gfut(p), age=b.get('age'), cg=b.get('cg'), yr=b.get('yr'),
                     g=g, rho=r, c_fade=float(G['fade30b_clock'](p, BASE)), c_u=cu, D=D, s=s, Phi=ph,
                     beta=be, pi=pi, v0=V0, sigma_sel=sg, credit=cr, par34=par34,
                     flat_bar=float(G['_O30BP_BARS'].get(MA.gfut(p), 0.0)),
                     pedigree_pts=ped, production_pts=prod,
                     cand=vals['cand'], c32r=vals['c32r'], c31=vals['c31'], live=live,
                     leg_surface=vals['surf'] - vals['c32r'], leg_alpha=vals['cand'] - vals['surf'],
                     d_vs_c32r=vals['cand'] - vals['c32r'], d_vs_c31=vals['cand'] - vals['c31'],
                     d_vs_live=(vals['cand'] - live) if live is not None else None))

TOT = {kk: sum(r['v'] for r in BD[kk]['rows'].values()) for kk in BD}
T_LIVE = PREV['totals']['live']; T_STEP2 = PREV['totals']['step2']
print('\nBOARD TOTALS  live %d  step2 %d  C31 %d  repaired C32 %d  +surface %d  ORDER C %d'
      % (T_LIVE, T_STEP2, TOT['c31'], TOT['c32r'], TOT['surf'], TOT['cand']))
print('rows without a birth year (flat bar kept): %d' % NO_BY)

# ---------------------------------------------------------------- AGE CONTINUITY (Order C vs C32R)
AGE_TAB = collections.defaultdict(lambda: dict(n=0, moved=0, sum_d=0, sum_abs=0))
for r in rows:
    a = r['age'] if r['age'] is not None else -1
    c = AGE_TAB[a]
    c['n'] += 1
    d = r['d_vs_c32r']
    if d != 0:
        c['moved'] += 1
    c['sum_d'] += d
    c['sum_abs'] += abs(d)
print('\nAGE CONTINUITY (delta vs repaired C32 by integer age):')
print('  %-4s %5s %6s %9s %9s' % ('age', 'n', 'moved', 'sum d', 'mean |d|'))
for a in sorted(AGE_TAB):
    c = AGE_TAB[a]
    print('  %-4s %5d %6d %+9d %9.1f' % (a, c['n'], c['moved'], c['sum_d'], c['sum_abs'] / max(1, c['n'])))

# ---------------------------------------------------------------- GAMES CONTINUITY (build-failing)
def continuity(p, gmax=20):
    g_now = float(G['pv_games'](p, BASE))
    cand = BD['cand']['rows'][p.get('key') or MA.slug(p['player'])]['v']
    pi_now = float(G['o31_pi'](p, BASE, g_now))
    V0 = float(G['pv_pedigree'](p)) / F
    cr_now = float(G['o32_age_credit'](p, BASE, g_now)) / F
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

# ---------------------------------------------------------------- COMPLETENESS (build-failing)
COMP = {'pole_deleted_dial': bool(G['_O30B_NOPOLE']), 'iso_deleted_dial': bool(G['_O30B_NOISO']),
        'preview_lane_on': bool(G['_PV']['on']), 'O34_ALPHA': float(G['O34_ALPHA'])}
src = open(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')).read()
COMP['raw_ev_returns_before_pole'] = 'if _O30B_NOPOLE: return pr' in src
COMP['iso_returns_unity'] = 'if _O30B_NOISO: return 1.0' in src
COMP['floor_replaced'] = "if _PV['on']: return v" in src
COMP['a_blend_replaced'] = "if _A_ON and _isreal(p) and not _PV['on']" in src
COMP['o34_exactly_two_sites'] = src.count('_o34_par(MA.gfut(p),p,Y)') == 1 and src.count('_o34_par(pos,p,Y)') == 1
COMP['o30bp_bars_never_edited'] = '_O30BP_BARS={_g:(MA.REPL[_g]-rd.REPL_DROP.get(_g,0.0)) for _g in MA.REPL}' in src
COMP['stall_gate_keeps_its_own_bars'] = 'o32_gate_bar' in src
noV0 = [r['key'] for r in rows if not (r['v0'] > 0)]
COMP['rows_priced'] = len(rows)
COMP['rows_without_a_v0_object'] = noV0
COMP['rows_without_birth_year'] = NO_BY
COMP['cell_coverage_pct'] = 100.0 * (len(rows) - len(noV0)) / max(1, len(rows))
COMP_FAIL = []
for kk in ('raw_ev_returns_before_pole', 'iso_returns_unity', 'floor_replaced',
           'a_blend_replaced', 'pole_deleted_dial', 'iso_deleted_dial', 'o34_exactly_two_sites',
           'o30bp_bars_never_edited', 'stall_gate_keeps_its_own_bars'):
    if not COMP[kk]: COMP_FAIL.append(kk)
if noV0: COMP_FAIL.append('rows without a v0 object: %s' % noV0[:6])

# ---------------------------------------------------------------- reconciliation + views
recon_bad = []
for r in rows:
    if abs((r['production_pts'] + r['pedigree_pts']) - r['cand']) > 1.0:
        recon_bad.append((r['key'], r['production_pts'] + r['pedigree_pts'], r['cand']))
print('\nRECONCILIATION: %d of %d rows fail production+pedigree == price at +-1 point'
      % (len(recon_bad), len(rows)))
print('GAMES CONTINUITY: %s' % ('PASS' if not CONT_FAIL else 'FAIL %s' % CONT_FAIL))
print('COMPLETENESS   : %s' % ('PASS' if not COMP_FAIL else 'FAIL %s' % COMP_FAIL))

def band(cg):
    cg = cg or 0
    return '0' if cg == 0 else '1-5' if cg < 6 else '6-15' if cg < 16 else '16-35' if cg < 36 \
        else '36-70' if cg < 71 else '71+'

CLASS = collections.defaultdict(lambda: dict(n=0, cand=0, c32r=0, c31=0, live=0, surface=0, alpha=0))
for r in rows:
    c = CLASS[band(r['cg'])]
    c['n'] += 1; c['cand'] += r['cand']; c['c32r'] += r['c32r']; c['c31'] += r['c31']
    c['surface'] += r['leg_surface']; c['alpha'] += r['leg_alpha']
    if r['live'] is not None: c['live'] += r['live']

NAMED = ['harry-dean', 'cooper-duff-tytler', 'nick-madden', 'alix-tauru', 'jordan-croft',
         'jedd-busslinger', 'ethan-read', 'ty-gallop', 'charlie-west', 'chris-scerri',
         'thomas-burton', 'milan-murdock', 'lachlan-carmichael', 'josh-smillie', 'phoenix-gothard',
         'billy-wilson', 'isaac-kako', 'xavier-taylor', 'daniel-annable', 'kye-annand']
BY = {r['key']: r for r in rows}

OUT = {'order': 'ORDER C — the age-conditional normalization (RL_O34)',
       'boards': {'live': LIVE_MD5, 'step2': STEP2_MD5,
                  'candidate31': BD['c31']['md5'], 'repaired_c32': BD['c32r']['md5'],
                  'orderC_surface_only': BD['surf']['md5'],
                  'orderC': BD['cand']['md5'], 'orderC_rebuild': BD['cand2']['md5'],
                  'fully_off_control': BD['off']['md5']},
       'totals': {'live': T_LIVE, 'step2': T_STEP2, 'c31': TOT['c31'], 'c32r': TOT['c32r'],
                  'surface_only': TOT['surf'], 'orderC': TOT['cand']},
       'determinism': BD['cand']['md5'] == BD['cand2']['md5'],
       'mature_identity': {'n_age24plus': N_MAT, 'moved': len(MAT_BAD), 'murdock_unmoved': True},
       'law': {'surface': 'par34(pos,a) = flat_bar(pos) - DELTA(class, clamp(a,18,23)), flat from 24',
               'sites': ['_c_w evidence-weight Q denominator', 'decay-gate par (pr = bestlvl/par)'],
               'O34_ALPHA': float(G['O34_ALPHA']), 'O32_KAPPA': G['O32_KAPPA'],
               'O32_GAMMA_U': G['O32_GAMMA'], 'O32_ETA': G['O32_ETA'], 'O32_GAMMA_D': G['O32_GAMMA_D']},
       'age_continuity': {str(a): dict(AGE_TAB[a]) for a in sorted(AGE_TAB)},
       'class_views': {k: dict(v) for k, v in sorted(CLASS.items())},
       'continuity': CONT, 'continuity_failures': CONT_FAIL,
       'completeness': COMP, 'completeness_failures': COMP_FAIL,
       'reconciliation_failures': recon_bad,
       'named_rows': [BY[k] for k in NAMED if k in BY],
       'rows': sorted(rows, key=lambda r: -(abs(r['d_vs_c32r'] or 0)))}

os.makedirs(os.path.join(ROOT, 'docs', 'ledgers'), exist_ok=True)
json.dump(OUT, open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_C_MOVERS.json'), 'w'),
          indent=1, sort_keys=True, default=str)
json.dump({'age_continuity': OUT['age_continuity'], 'continuity': CONT, 'failures': CONT_FAIL},
          open(os.path.join(HERE, 'CONTINUITY_34.json'), 'w'), indent=1, sort_keys=True, default=str)
json.dump({'completeness': COMP, 'failures': COMP_FAIL},
          open(os.path.join(HERE, 'COMPLETENESS_34.json'), 'w'), indent=1, sort_keys=True, default=str)

# ---------------------------------------------------------------- the md ledger
L = []
L.append('# ORDER C — THE MOVERS LEDGER (THE AGE-CONDITIONAL NORMALIZATION, RL_O34)')
L.append('')
L.append('**ORDER C · `land/order-29` · all %d board rows, EVERY row with FOUR value columns '
         '(live `88ce647f` · Candidate 31 `fe6be9d6` · repaired C32 `7802ee97` · Order C) and the '
         'two mechanism legs (surface / credit-scale α), each leg a REAL BOARD delta. '
         'NOTHING LANDS WITHOUT THE OWNER\'S WORD.**' % len(rows))
L.append('')
L.append('| board | md5 | total |')
L.append('|---|---|---:|')
L.append('| LIVE | `%s` | %d |' % (LIVE_MD5, T_LIVE))
L.append('| CANDIDATE 31 (31-F) | `%s` | %d |' % (BD['c31']['md5'], TOT['c31']))
L.append('| REPAIRED C32 | `%s` | %d |' % (BD['c32r']['md5'], TOT['c32r']))
L.append('| + the surface (two denominators) | `%s` | %d |' % (BD['surf']['md5'], TOT['surf']))
L.append('| **ORDER C (+ credit scale α=%.2f)** | **`%s`** | **%d** |' % (float(G['O34_ALPHA']), BD['cand']['md5'], TOT['cand']))
L.append('| determinism rebuild | `%s` | %d |' % (BD['cand2']['md5'], TOT['cand']))
L.append('| dial-off (RL_O32=1) | `%s` | %d |' % (BD['c32r']['md5'], TOT['c32r']))
L.append('| fully-off (Step-2 law) | `%s` | — |' % BD['off']['md5'])
L.append('')
L.append('vs repaired C32 **%+d** (%.3f%%) · vs C31 **%+d** · vs LIVE **%+d** · '
         'MATURE ROWS (age 24+): **%d of %d byte-unmoved** (murdock asserted by name)'
         % (TOT['cand'] - TOT['c32r'], 100.0 * (TOT['cand'] - TOT['c32r']) / TOT['c32r'],
            TOT['cand'] - TOT['c31'], TOT['cand'] - T_LIVE, N_MAT - len(MAT_BAD), N_MAT))
L.append('')
L.append('## DELTA BY AGE (the age-continuity object: flat from 24 = zero movement from 24)')
L.append('')
L.append('| age | n | moved | sum Δ | mean |Δ| |')
L.append('|---|---:|---:|---:|---:|')
for a in sorted(AGE_TAB):
    c = AGE_TAB[a]
    L.append('| %s | %d | %d | %+d | %.1f |' % (a, c['n'], c['moved'], c['sum_d'], c['sum_abs'] / max(1, c['n'])))
L.append('')
L.append('## BY CAREER-GAMES CLASS')
L.append('')
L.append('| games | n | Order C | C32R | C31 | live | vs C32R | surface | α |')
L.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for k, v in sorted(CLASS.items()):
    L.append('| %s | %d | %d | %d | %d | %d | %+d | %+d | %+d |'
             % (k, v['n'], v['cand'], v['c32r'], v['c31'], v['live'], v['cand'] - v['c32r'],
                v['surface'], v['alpha']))
L.append('')
L.append('## THE NAMED ROWS, TRACED')
L.append('')
L.append('| player | path | pos | age | g | live | C31 | C32R | **Order C** | Δ vs C32R | surface | α leg | credit | par34 | flat bar |')
L.append('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for k in NAMED:
    if k not in BY: continue
    r = BY[k]
    L.append('| %s | %s | %s | %s | %.0f | %s | %d | %d | **%d** | %+d | %+d | %+d | %.0f | %.1f | %.1f |'
             % (k, r['pathway'], r['pos'], r['age'], r['g'],
                r['live'] if r['live'] is not None else '—', r['c31'], r['c32r'], r['cand'],
                r['d_vs_c32r'], r['leg_surface'], r['leg_alpha'], r['credit'], r['par34'], r['flat_bar']))
L.append('')
L.append('## ALL %d ROWS (sorted by |Δ vs repaired C32|)' % len(rows))
L.append('')
L.append('| player | path | pos | age | g | live | C31 | C32R | **Order C** | Δ vs C32R | Δ vs live | surface | α leg |')
L.append('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in OUT['rows']:
    L.append('| %s | %s | %s | %s | %.0f | %s | %d | %d | **%d** | %+d | %s | %+d | %+d |'
             % (r['key'], r['pathway'], r['pos'], r['age'], r['g'],
                r['live'] if r['live'] is not None else '—', r['c31'], r['c32r'], r['cand'],
                r['d_vs_c32r'],
                ('%+d' % r['d_vs_live']) if r['d_vs_live'] is not None else '—',
                r['leg_surface'], r['leg_alpha']))
open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_C_MOVERS.md'), 'w').write('\n'.join(L) + '\n')
print('\nwritten: docs/ledgers/ORDER_C_MOVERS.{json,md} / CONTINUITY_34.json / COMPLETENESS_34.json')
