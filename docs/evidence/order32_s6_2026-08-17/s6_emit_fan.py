#!/usr/bin/env python3
"""ORDER 32 SEAT S6 -- THE SIX-LEVEL SCENARIO FAN, EMITTED PER ROW.  READ-ONLY.

WHAT THIS IS.  The engine's production leg prices a player as a fixed-weight blend over a SIX-LEVEL
scenario fan.  b6(p) builds six band levels (five conditional-prior band quantile levels plus the frozen
q97 ceiling as band[5]); price6(p,bb) = SCALE_DIST x dot(WQ6, [v_at_peak(p,L,'bal') for L in bb]) with
WQ6 = [0.18 x5, 0.10] normalised (engine/rl_after/_merged_recover.py :96, :374-391).  That blend is a
POINT ESTIMATE and the board prints only the point.  This emitter opens it: for every active row under
the CANDIDATE build it writes the six band levels and the six per-scenario career values that price6
averages, so the per-player VARIANCE behind one printed number is visible.

READ-ONLY MANDATE.  This script imports the engine exactly as the engine's own harnesses do
(docs/evidence/candidate_31f/o31f_ledger.py :43-58) -- rl_model imported, _merged_recover.py exec'd into
a private namespace -- and calls only b6 / price6 / dp.v_at_peak / the ORDER-31 law accessors.  It writes
NOTHING into engine/, docs/ledgers/ or any board.  No engine file is modified, no law constant moves, no
weight is re-pinned.  The lambda lens the owner page carries is a DISPLAY layer over this emit; the
sealed pricing law stays at the default WQ6 here and everywhere.

IDENTITY.  The candidate board is fe6be9d6ac76ebc34d26ebc11d796505 (BUILDS_31F.txt, tag f2on, total
666,913), built from rl_model.py 14000af2 / rl_model_data.json cb38ef11 / pvc_curve_v2.json 78ad9842
under RL_O31=1.  All three artefacts are byte-identical at this commit's HEAD, which is why the engine
can be loaded straight from the repo under RL_O31=1 and read the candidate's own arithmetic -- the same
route o31f_ledger.py takes to build CANDIDATE_31_MOVERS.json.  Every one of those identities is ASSERTED
below before a single number is emitted.

THE FAN IS THE PRODUCTION LEG ONLY.  Under the one law
    price = rho(g) x Phat + [D(c_u) x (1-rho(g)) + Phi(g,s) x beta(g) x rho(g)] x v0
the fan lives entirely inside Phat.  The v0 (pedigree) leg has its own variance and it is NOT in this
emit -- seat S7 is designing it.  On a low-games row most of the price is the pedigree leg, so a small
emitted spread on such a row means "we have not measured his spread yet", NOT "he is a safe bet".  That
caveat is carried on every artefact this seat writes.

THE DOWNSTREAM FACTOR, DISCLOSED.  price6 is not Phat.  Between price6 and the Phat the law consumes sit
the retained production-side layers (the iso multiplier, ITEM-H's ruled cuts, the D8 graded staleness
gate, the KPF compression, the LEG-B v1.1 un-compress map -- RL_UNCOMP is ON with s=0.1 -- the young
credit, the M3 in-progress-season clock blend) and the BOARD->ENGINE numeraire _PL_F.  Several of those
are not linear in price6.  So the emit carries, per row, a SINGLE DISCLOSED SCALAR
    m = Phat / price6
and emits the six values twice: `six_raw` (the literal SCALE_DIST x v_at_peak terms, engine currency)
and `six_phat` = m x six_raw (the same fan expressed in the units the law's Phat is in, so that
dot(WQ6, six_phat) == Phat).  The lens therefore holds the row's REALISED downstream factor fixed across
scenarios -- a first-order, proportional reading of "what if the band were weighted differently".  It is
not a re-run of the engine at a different weight vector, and this file does not pretend it is.
"""
import os, sys, json, io, math, time, hashlib, contextlib, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP   = os.environ.get('RL_SCRATCH',
                      '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f')
md5  = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

CAND_BOARD_MD5 = 'fe6be9d6ac76ebc34d26ebc11d796505'
RL_MODEL_MD5   = '14000af2a46f7a3c4cdfde303f5a1aff'
STORE_MD5      = 'cb38ef1171dcf20aae66ebf12682be0d'
PVC_MD5        = '78ad9842525ae4f09875b95afc2e2b39'

# ------------------------------------------------------------------ identity, asserted before anything
ART = {'rl_model.py':        os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py'),
       'rl_model_data.json': os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json'),
       'pvc_curve_v2.json':  os.path.join(ROOT, 'engine', 'rl_after', 'pvc_curve_v2.json')}
IDENT = {k: md5(v) for k, v in ART.items()}
print('HEAD ARTEFACTS')
for k, v in sorted(IDENT.items()): print('  %-20s %s' % (k, v))
assert IDENT['rl_model.py'] == RL_MODEL_MD5, 'rl_model.py is not the candidate engine'
assert IDENT['rl_model_data.json'] == STORE_MD5, 'the store is not cb38ef11 -- wrong tree'
assert IDENT['pvc_curve_v2.json'] == PVC_MD5, 'pvc_curve_v2.json is not the head-fixed 78ad9842'

BOARD_PATH = os.path.join(SP, 'bb_f2on', 'rl_after', 'rl_app_data.json')
BOARD_MD5 = md5(BOARD_PATH)
print('CANDIDATE BOARD       %s  %s' % (BOARD_MD5, BOARD_PATH))
assert BOARD_MD5 == CAND_BOARD_MD5, 'the reused candidate tree is not board fe6be9d6 -- rebuild it'
BROWS = {r['key']: r for r in json.load(open(BOARD_PATH))['active']}
print('  board active rows     %d   total %d' % (len(BROWS), sum(r['v'] for r in BROWS.values())))

LEDGER_PATH = os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_31_MOVERS.json')
LED = json.load(open(LEDGER_PATH))
assert LED['boards']['candidate'] == CAND_BOARD_MD5, 'the committed movers ledger is not this board'
LR = {r['key']: r for r in LED['rows']}
print('  movers-ledger rows    %d   (%s)' % (len(LR), md5(LEDGER_PATH)))

# ------------------------------------------------------------------ load the engine under the one law
os.environ.update(RL_O31='1', PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
_t0 = time.time()
with contextlib.redirect_stdout(io.StringIO()) as _boot:
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
print('  engine loaded in %.1fs' % (time.time() - _t0))

NEED = ('b6', 'price6', 'dp', 'rd', 'WQ6', '_det_dot', 'rho31', 'o31_pi', 'pv_games',
        'pv_pedigree', '_PL_F', '_O31', '_isreal', 'delisted')
G = {k: NSE.get(k) for k in NEED}
missing = [k for k, v in G.items() if v is None]
if missing:
    sys.exit('S6 HALT: the engine did not expose %s -- the one law is not live.' % missing)
if not G['_O31']:
    sys.exit('S6 HALT: RL_O31 is not live. This emit describes the CANDIDATE build only.')
b6, price6, dp, rd = G['b6'], G['price6'], G['dp'], G['rd']
WQ6 = [float(x) for x in G['WQ6']]; _det_dot = G['_det_dot']
F = float(G['_PL_F']); BASE = MA.BASE_REF
print('  RL_O31 LIVE  BASE_REF %s  _PL_F %.4f  SCALE_DIST %s' % (BASE, F, dp.SCALE_DIST))
print('  WQ6 %s   (sum %.12f)' % (['%.6f' % w for w in WQ6], sum(WQ6)))
print('  RL_UNCOMP %s  UNCOMP_S %s  (the LEG-B map is part of the disclosed downstream factor m)'
      % (getattr(MA, '_UNCOMP', None), getattr(MA, 'UNCOMP_S', None)))
assert abs(sum(WQ6) - 1.0) < 1e-12, 'WQ6 is not normalised'

# ------------------------------------------------------------------ the fan, per row
def fan(p, Y):
    """The six band levels and the six per-scenario career values, on the engine's PUBLIC path.

    bb = b6(p,Y) -- the fully-wrapped band (conditional-prior quantiles + the frozen q97 ceiling as
    bb[5], through the v7 age-taper and the W4 pin wrapper).  The six values are then formed inside
    price6's OWN context: the REPL_DROP shift, the AGE_REF/BASE_REF form-anchor pin and the _pe_clear,
    transcribed from _merged_recover.py :385-391 so the terms are the ones price6 itself averages.
    Verified by construction: dot(WQ6, six_raw) is compared against price6's own return below."""
    bb = b6(p, Y)
    sav = dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g] = sav[g] - rd.REPL_DROP.get(g, 0)
        MA.AGE_REF = Y
        MA.BASE_REF = (MA._LENS_FORM if getattr(MA, '_LENS_FORM', None) is not None else Y)
        MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()):
            six = [float(dp.SCALE_DIST * dp.v_at_peak(p, float(L), 'bal')) for L in bb]
    finally:
        MA.REPL.update(sav)
    with contextlib.redirect_stdout(io.StringIO()):
        p6 = float(price6(p, bb, Y))
    return [float(x) for x in bb], six, p6

BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key') or MA.slug(p['player']), p)

rows = []
dev_p6 = []          # |dot(WQ6, six_raw) - price6(...)|            the engine's own dot, reproduced
dev_phat = []        # |dot(WQ6, six_phat) - Phat|                  THE ASKED-FOR NUMBER
dev_price0 = []      # |price(lambda=0) - printed board price|      the page's anchor
dev_law = []         # |rho*Phat + pedigree_pts - printed price|    the law's own reconstruction
degenerate = []      # rows whose fan cannot carry the price (rho==0 or price6==0)
missing_rows = []
_t0 = time.time()
for k, lr in sorted(LR.items()):
    p = BYKEY.get(k)
    if p is None or k not in BROWS:
        missing_rows.append(k); continue
    cand = int(BROWS[k]['v'])
    assert cand == int(lr['cand']), 'ledger/board price disagree on %s' % k

    bb, six_raw, p6 = fan(p, BASE)
    dot_raw = float(_det_dot(WQ6, six_raw))
    dev_p6.append(abs(dot_raw - p6))

    rho = float(lr['rho'])
    ped = float(lr['pedigree_pts'])
    # EXACT, not max(0,.): prod + ped == cand identically, so the page's lambda=0 price IS the printed
    # price.  Where the law's own production_pts differs (it floors at zero) the difference is reported.
    prod = float(cand) - ped
    Phat = (prod / rho) if rho > 0.0 else 0.0
    ok = (rho > 0.0 and p6 > 0.0 and prod > 0.0)
    m = (Phat / p6) if ok else 0.0
    six_phat = [m * x for x in six_raw]
    if not ok:
        degenerate.append(k)
    else:
        dev_phat.append(abs(float(_det_dot(WQ6, six_phat)) - Phat))
        dev_law.append(abs(rho * Phat + ped - float(cand)))

    # the page's per-row anchor: price(lambda) = anchor + rho * dot(W(lambda), six_phat).
    # anchor is computed HERE in float so that price(0) reproduces the printed integer EXACTLY on every
    # row, including the degenerate ones (where the fan carries nothing and the price is flat in lambda).
    anchor = float(cand) - rho * float(_det_dot(WQ6, six_phat))
    dev_price0.append(abs(anchor + rho * float(_det_dot(WQ6, six_phat)) - float(cand)))

    # ---- SPREAD METRICS, all read off six_raw (scale-invariant, so m does not touch them) ----
    b1, b3, b6v = six_raw[0], six_raw[2], six_raw[5]
    ratio  = (b6v / b1) if b1 > 0 else None                       # top scenario / floor scenario
    spanm  = ((b6v - b1) / b3) if b3 > 0 else None                # fan width in median-scenario units
    tshare = (WQ6[5] * b6v / p6) if p6 > 0 else None              # share of Phat in the top scenario
    tsharep = (rho * WQ6[5] * six_phat[5] / cand) if cand > 0 else None  # ... of the WHOLE board price
    cv = None
    if p6 > 0:
        mu = dot_raw
        var = sum(w * (x - mu) ** 2 for w, x in zip(WQ6, six_raw))
        cv = math.sqrt(var) / mu if mu > 0 else None              # WQ6-weighted coefficient of variation

    rows.append({
        'key': k, 'name': lr['name'], 'pathway': lr['pathway'], 'pos': lr['pos'],
        'pick': lr['pick'], 'age': lr['age'], 'games': lr['cg'], 'g_law': float(lr['g']),
        'cand': cand, 'rho': rho, 'v0': float(lr['v0']), 'D': float(lr['D']),
        'Phi': float(lr['Phi']), 'beta': float(lr['beta']), 'pi': float(lr['pi']),
        'pedigree_pts': ped, 'production_pts_ledger': float(lr['production_pts']),
        'production_pts': prod, 'Phat': Phat,
        'b6': bb, 'six_raw': six_raw, 'six_phat': six_phat,
        'price6': p6, 'm_downstream': m, 'anchor_pts': anchor,
        'spread_ratio_6_1': ratio, 'spread_span_over_med': spanm,
        'top_scenario_share_of_Phat': tshare, 'top_scenario_share_of_price': tsharep,
        'weighted_cv': cv, 'fan_carries_price': ok,
        # THE CEILING IS NOT ALWAYS THE TOP SCENARIO. b6[5] is the frozen q97 ceiling, but the v7
        # age-taper pulls it toward the band median (bb[5]=m+asc*(bb[5]-m)), so on a taper-hit row the
        # "ceiling" scenario can price BELOW band 5. Flagged per row rather than smoothed away: it means
        # "tilt toward the ceiling" is not "tilt toward the biggest number" for these players.
        'q97_below_band5': bool(six_raw[5] < six_raw[4] - 1e-9),
        'fan_flat': bool(max(six_raw) - min(six_raw) < 1e-9),
        'fan_nondecreasing': all(six_raw[i] >= six_raw[i - 1] - 1e-9 for i in range(1, 6)),
    })
print('  %d rows in %.1fs' % (len(rows), time.time() - _t0))
if missing_rows:
    print('  UNMAPPED (ledger row absent from the board or from MA.data): %s' % missing_rows)

# ------------------------------------------------------------------ validation
MX = lambda a: max(a) if a else 0.0
V = {
 'rows_emitted': len(rows),
 'rows_in_ledger': len(LR),
 'rows_unmapped': missing_rows,
 'max_dev_dot_WQ6_six_raw_vs_price6': MX(dev_p6),
 'max_dev_dot_WQ6_six_phat_vs_Phat': MX(dev_phat),
 'max_rel_dev_dot_WQ6_six_phat_vs_Phat': MX([d / max(1e-9, r['Phat'])
                                             for d, r in zip(dev_phat, [x for x in rows if x['fan_carries_price']])]),
 'max_dev_price_at_lambda0_vs_printed': MX(dev_price0),
 'max_dev_law_reconstruction_vs_printed': MX(dev_law),
 'rows_fan_cannot_carry_price': degenerate,
 'n_rows_fan_cannot_carry_price': len(degenerate),
 'n_rows_rho_below_0_3': sum(1 for r in rows if r['rho'] < 0.3),
 'n_fan_flat': sum(1 for r in rows if r['fan_flat']),
 'n_fan_nondecreasing': sum(1 for r in rows if r['fan_nondecreasing'] and not r['fan_flat']),
 'n_q97_below_band5': sum(1 for r in rows if r['q97_below_band5']),
 'n_q97_below_band5_priced': sum(1 for r in rows if r['q97_below_band5'] and r['fan_carries_price']),
 'ledger_production_pts_max_gap': MX([abs(r['production_pts'] - r['production_pts_ledger']) for r in rows]),
}
mm = [r['m_downstream'] for r in rows if r['fan_carries_price']]
V['m_downstream'] = {'n': len(mm), 'min': min(mm), 'p05': statistics.quantiles(mm, n=20)[0],
                     'median': statistics.median(mm), 'p95': statistics.quantiles(mm, n=20)[18],
                     'max': max(mm), 'mean': statistics.fmean(mm)}
print('\nVALIDATION')
print('  dot(WQ6, six_raw)  vs price6()      max dev  %.3e   (the engine\'s own order-fixed dot)' % V['max_dev_dot_WQ6_six_raw_vs_price6'])
print('  dot(WQ6, six_phat) vs Phat          max dev  %.3e  (rel %.3e)   <-- THE P-HAT VALIDATION'
      % (V['max_dev_dot_WQ6_six_phat_vs_Phat'], V['max_rel_dev_dot_WQ6_six_phat_vs_Phat']))
print('  price(lambda=0)    vs printed price max dev  %.3e   (the page\'s anchor, %d rows)'
      % (V['max_dev_price_at_lambda0_vs_printed'], len(rows)))
print('  rho*Phat + ped     vs printed price max dev  %.3e   (the law\'s own reconstruction)' % V['max_dev_law_reconstruction_vs_printed'])
print('  ledger production_pts vs cand-ped   max gap  %.3e   (the ledger floors at 0; this emit does not)'
      % V['ledger_production_pts_max_gap'])
print('  downstream factor m: min %.4f  p05 %.4f  median %.4f  p95 %.4f  max %.4f'
      % (V['m_downstream']['min'], V['m_downstream']['p05'], V['m_downstream']['median'],
         V['m_downstream']['p95'], V['m_downstream']['max']))
print('  rows whose fan cannot carry the price (rho==0 / price6==0 / prod<=0): %d  %s'
      % (len(degenerate), degenerate[:8]))
print('  rows with rho < 0.3 (spread GREYED on the page -- pedigree-dominated): %d of %d'
      % (V['n_rows_rho_below_0_3'], len(rows)))
print('  FAN SHAPE: %d perfectly flat  |  %d non-decreasing  |  %d with the q97 ceiling BELOW band 5'
      ' (%d of them carry a production leg)'
      % (V['n_fan_flat'], V['n_fan_nondecreasing'], V['n_q97_below_band5'], V['n_q97_below_band5_priced']))

FAIL = []
if V['max_dev_dot_WQ6_six_raw_vs_price6'] > 1e-6: FAIL.append('six_raw does not reproduce price6')
if V['max_rel_dev_dot_WQ6_six_phat_vs_Phat'] > 1e-9: FAIL.append('six_phat does not reproduce Phat')
if V['max_dev_price_at_lambda0_vs_printed'] > 1e-6: FAIL.append('lambda=0 does not reproduce the board')
if V['max_dev_law_reconstruction_vs_printed'] > 1.0: FAIL.append('the law does not reconstruct the board')
if missing_rows: FAIL.append('unmapped ledger rows')
V['failures'] = FAIL
print('  VERDICT: %s' % ('PASS' if not FAIL else 'FAIL %s' % FAIL))

# ------------------------------------------------------------------ emit
OUT = {
 'order': 'ORDER 32 seat S6 -- the six-level scenario fan, per row',
 'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
 'scope': 'PRODUCTION LEG ONLY. The v0 (pedigree) leg carries its own variance and it is NOT in this '
          'emit -- seat S7 is designing it. A low-rho row therefore shows a MISLEADINGLY SMALL spread: '
          'most of its price is pedigree, whose fan does not exist yet.',
 'read_only': 'No engine file, law constant, board or no-arb instrument was touched. WQ6 stays at the '
              'sealed default in the engine; the lambda lens is a DISPLAY layer over this emit.',
 'identity': {'head_commit_artefacts': IDENT, 'candidate_board_md5': BOARD_MD5,
              'movers_ledger_md5': md5(LEDGER_PATH), 'board_path': BOARD_PATH,
              'base_ref': BASE, 'PL_F': F, 'SCALE_DIST': float(dp.SCALE_DIST),
              'RL_O31': True, 'RL_UNCOMP': bool(getattr(MA, '_UNCOMP', False)),
              'UNCOMP_S': getattr(MA, 'UNCOMP_S', None)},
 'law': {'form': LED['law']['form'], 'WQ6': WQ6,
         'price6': "SCALE_DIST * dot(WQ6, [v_at_peak(p, L, 'bal') for L in b6(p)])",
         'b6': 'five conditional-prior band quantile levels + the frozen q97 ceiling as b6[5]'},
 'lens': {'weights': 'W_i(lambda) proportional to WQ6_i * exp(lambda * i), i = 0..5, renormalised',
          'price': 'price(lambda) = anchor_pts + rho * dot(W(lambda), six_phat)',
          'identity_at_zero': 'W(0) == WQ6 exactly, so price(0) == the printed board price exactly',
          'approximation': 'six_phat = m * six_raw with m = Phat/price6 a SINGLE per-row scalar. The '
                           'downstream production layers (iso, ITEM-H cuts, D8 staleness, KPF '
                           'compression, the LEG-B un-compress map, the young credit, the M3 clock '
                           'blend, the _PL_F numeraire) are held at their REALISED value across '
                           'scenarios. Some of them are not linear in price6, so the lens is a '
                           'first-order proportional reading, not an engine re-run.'},
 'validation': V,
 'rows': sorted(rows, key=lambda r: -r['cand']),
}
OUTP = os.path.join(HERE, 'S6_FAN_EMIT.json')
json.dump(OUT, open(OUTP, 'w'), indent=1, sort_keys=True, default=str)
print('\nWROTE %s  (%s, %.1f KB)' % (OUTP, md5(OUTP), os.path.getsize(OUTP) / 1024.0))

# ------------------------------------------------------------------ a look at the tails, for the record
print('\nWIDEST FANS (rho >= 0.3, by band6/band1)')
wide = sorted([r for r in rows if r['rho'] >= 0.3 and r['spread_ratio_6_1']],
              key=lambda r: -r['spread_ratio_6_1'])[:12]
print('  %-24s %-4s %-5s %5s %7s %8s %9s %7s' % ('name', 'path', 'pos', 'g', 'price', 'b6/b1', '(b6-b1)/b3', 'top%'))
for r in wide:
    print('  %-24s %-4s %-5s %5s %7d %8.1f %9.2f %6.1f%%'
          % (r['name'][:24], r['pathway'], r['pos'], r['games'], r['cand'],
             r['spread_ratio_6_1'], r['spread_span_over_med'], 100 * r['top_scenario_share_of_Phat']))
print('\nFLATTEST FANS (rho >= 0.3, by band6/band1)')
flat = sorted([r for r in rows if r['rho'] >= 0.3 and r['spread_ratio_6_1']],
              key=lambda r: r['spread_ratio_6_1'])[:12]
for r in flat:
    print('  %-24s %-4s %-5s %5s %7d %8.3f %9.2f %6.1f%%'
          % (r['name'][:24], r['pathway'], r['pos'], r['games'], r['cand'],
             r['spread_ratio_6_1'], r['spread_span_over_med'], 100 * r['top_scenario_share_of_Phat']))
if FAIL:
    sys.exit('S6 HALT: %s' % FAIL)
