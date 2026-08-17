#!/usr/bin/env python3
# =====================================================================================================
# ORDER 33 SEAT W6 -- THE FROZEN q97 CEILING vs REALIZED 97th-PERCENTILE OUTCOMES.  READ-ONLY.
# PREREG: PREREG_W6.md (committed and pushed BEFORE this ran).
#
# Measures, at historical (player, year) vantages built the way the engine builds its own training
# vantages, the realized 97th-percentile of (1) subsequent peak production (fwd_best3_from -- the
# frozen model's OWN target quantity, same units) and (2) subsequent career delivered value (the
# grace-A season-valuation formula discounted to the vantage), per age x position x games cell; and
# reconstructs what the pricing path emits at those same vantages (q97m raw -> max(.,b[4]) -> the v7
# age-taper), so model ceiling and realized ceiling can be compared and the two suspects decomposed.
#
# WRITES ONLY: W6_CELLS.json / W6_VANTAGES.csv / W6_NAMED.json / W6_BOARD_IMPACT.json / W6_out.txt
# in this directory.  No engine, board, law, pin or pickle is touched.  q97m stays FROZEN; the
# deliverable is a bake-time recommendation (refit_q97m.py is the only legitimate path).
# =====================================================================================================
import os, sys, io, json, csv, math, time, random, hashlib, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
md5  = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

LOG = []
def P(s=''):
    print(s); LOG.append(str(s))

RL_MODEL_MD5 = '14000af2a46f7a3c4cdfde303f5a1aff'
STORE_MD5    = 'cb38ef1171dcf20aae66ebf12682be0d'
PVC_MD5      = '78ad9842525ae4f09875b95afc2e2b39'

P('=' * 118)
P('ORDER 33 W6 -- THE FROZEN q97 CEILING vs REALIZED 97th-PERCENTILE OUTCOMES.  PREREG_W6.md governs.')
P('=' * 118)

# ---------------------------------------------------------------- C0: identity, asserted before anything
ART = {'rl_model.py':        os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py'),
       'rl_model_data.json': os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json'),
       'pvc_curve_v2.json':  os.path.join(ROOT, 'engine', 'rl_after', 'pvc_curve_v2.json'),
       'q97m.pkl':           os.path.join(ROOT, 'data', 'q97m.pkl')}
IDENT = {k: md5(v) for k, v in ART.items()}
BOOT = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
P('C0 IDENTITY')
for k, v in sorted(IDENT.items()): P('  %-20s %s' % (k, v))
assert IDENT['rl_model.py'] == RL_MODEL_MD5, 'rl_model.py is not the candidate engine'
assert IDENT['rl_model_data.json'] == STORE_MD5, 'the store is not cb38ef11'
assert IDENT['pvc_curve_v2.json'] == PVC_MD5, 'pvc_curve_v2.json is not 78ad9842'
assert IDENT['q97m.pkl'] == BOOT.get('q97m'), 'data/q97m.pkl does not match the expected_boot pin'
P('  q97m.pkl == expected_boot pin %s  (FROZEN artefact confirmed)' % BOOT.get('q97m'))

# ---------------------------------------------------------------- load the engine read-only (S6 route)
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
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
import numpy as np
P('  engine loaded in %.1fs' % (time.time() - _t0))

cp   = NSE['cp']; rd = NSE['rd']; dp = NSE['dp']
cm   = NSE['cm']; q97m = NSE['q97m']
b6   = NSE['b6']; _b6_core = NSE['_b6_core']; price6 = NSE['price6']
_v7  = NSE['_v7']; _isreal = NSE['_isreal']
_lvlcurr = NSE['_lvlcurr']; _nqual = NSE['_nqual']
_W4V7 = NSE['_W4V7']; V7W = NSE['V7_FORM_W']
WQ6 = [float(x) for x in NSE['WQ6']]; _det_dot = NSE['_det_dot']
if not NSE.get('_O31'): sys.exit('W6 HALT: RL_O31 is not live')

# C1: the frozen pickle IS the documented object
assert type(q97m).__name__ == 'GradientBoostingRegressor'
assert q97m.loss == 'quantile' and abs(q97m.alpha - 0.97) < 1e-12, 'q97m is not the 0.97 quantile GBR'
assert int(q97m.n_features_in_) == 11, 'q97m feature width is not 11'
P('C1 q97m: GradientBoostingRegressor(loss=quantile, alpha=%.2f, n_estimators=%d, max_depth=%d, '
  'lr=%s, min_samples_leaf=%s) on %d features -- matches refit_q97m.py Q97M_KW'
  % (q97m.alpha, q97m.n_estimators, q97m.max_depth, q97m.learning_rate,
     q97m.min_samples_leaf, q97m.n_features_in_))
P('  v7 taper: asc = interp(age, [20,22,24,27], [1.0,0.76,0.58,0.40]); bb[5] = m + asc*(bb[5]-m), '
  'm = band median bb[2]; W4 form-retention ON=%s (V7W=%s, needs lcr>4 and nqual>=1)' % (_W4V7, V7W))

# ---------------------------------------------------------------- grace-A season valuation (o26b verbatim)
BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
DISC = 1.0 + float(MA.LENS['bal'])          # flat-14 basis (the live grace-A config)
def season_raw(X, pos): return MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0
def w_sqrt(g): return min(1.0, math.sqrt(max(0.0, g) / 10.0))
def season_bar_group(pos_label, p):
    if pos_label:
        es = MA._collapse_elig(str(pos_label).replace('/', ','))
        if es: return min(es, key=lambda x: MA.REPL[x])
    try: return MA._decl_bar(p)
    except Exception: return MA.gfut(p)
def dv_from(p, Y):
    """Subsequent career delivered value from vantage Y: the grace-A observed-season formula,
    discounted to the vantage (k = y - Y). PREREG section 2, outcome 2."""
    tot = 0.0
    for s in p['scoring']:
        if s['year'] <= Y or s['year'] > 2026 or s['games'] <= 0: continue
        g = season_bar_group(s.get('pos'), p)
        if g not in BARS: continue
        raw = season_raw(s['avg'], g)
        tot += MA.SCALE * raw * w_sqrt(s['games']) / (DISC ** (s['year'] - Y))
    return tot

# ---------------------------------------------------------------- the vantage sweep
FIRST_OBS = cp.first_observable_season()
CUTS = {'primary_2019': 2019, 'sensitivity_2016': 2016}
P('')
P('VANTAGE SWEEP -- every real store player with a mapped group, Y = debutyr-1 .. min(last, 2019), '
  'T1 rule applied (first observable season %s)' % FIRST_OBS)

def in_trainpool(p):
    return not (cp.debutyr(p) > 2021 or not (p.get('pick') or p.get('_ft')) or p.get('type') == 'MSD')

def excl_reason(p):
    """WHY a row is outside the q97m training pool. Pathway-CLASS exclusions (no such pathway ever
    trains, any era) are distinguished from the debut<=2021 resolved-only window (by design)."""
    if in_trainpool(p): return None
    if p.get('type') == 'MSD': return 'pathway class MSD excluded'
    if not (p.get('pick') or p.get('_ft')): return 'pathway class (pickless pool: SSP/IRE/UNR/PD*) excluded'
    return 'debut>2021 (resolved-only window, by design)'

POOL = [p for p in MA.data if MA.GRP.get(p['pos'])]
VANT = []          # feature rows in engine context
_t0 = time.time()
for p in POOL:
    d0 = cp.debutyr(p) - 1
    last = max([x['year'] for x in p['scoring']] + [d0])
    for Y in range(d0, min(last, CUTS['primary_2019']) + 1):
        if FIRST_OBS is not None and d0 < Y < FIRST_OBS: continue
        # engine context exactly as _b6_core sets it, so features/levels are the pricing path's own
        MA.AGE_REF = Y; MA.BASE_REF = Y; MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()):
            f = cp._feat(p, Y)
            lcr = _lvlcurr(p, Y) - MA.REPL.get(MA.gfut(p), 0.0)
            nq = _nqual(p, Y)
            age = cp._age_asof(p, Y)
            gth = cp.games_through(p, Y)
            peak = cp.fwd_best3_from(p, Y, 2026)
            dv = dv_from(p, Y)
        VANT.append(dict(key=p.get('key') or MA.slug(p['player']), player=p['player'],
                         type=p.get('type'), Y=Y, pos=MA.gfut(p), age=age, games=gth,
                         tenure=Y - d0, f=[float(x) for x in f], lcr=lcr, nq=nq,
                         peak=float(peak), dv=float(dv), train=in_trainpool(p),
                         pickless=bool(not (p.get('pick') or p.get('_ft')))))
MA.AGE_REF = 2026; MA.BASE_REF = 2026; MA._pe_clear()
P('  %d vantages from %d players in %.1fs' % (len(VANT), len({v["key"] for v in VANT}), time.time() - _t0))

# batch-predict the six frozen models over the vantage features
F = np.array([v['f'] for v in VANT])
_t0 = time.time()
PRED5 = {qq: cm[qq].predict(F) for qq in sorted(cm)}
PQ97 = q97m.predict(F)
P('  batch predictions in %.1fs' % (time.time() - _t0))
for i, v in enumerate(VANT):
    b = np.sort(np.array([float(PRED5[qq][i]) for qq in sorted(cm)]))
    v['b2'] = float(b[2]); v['b4'] = float(b[4])
    v['pred_raw'] = float(PQ97[i])
    v['b5_raw'] = max(v['pred_raw'], v['b4'])
    asc = float(np.interp(v['age'], [20, 22, 24, 27], [1.0, 0.76, 0.58, 0.40]))
    if _W4V7 and asc < 1.0 and v['lcr'] > 4.0 and v['nq'] >= 1:
        phi = float(np.clip((v['lcr'] - 4.0) / 26.0, 0.0, 1.0)) * min(v['nq'], 2) / 2.0 * V7W
        asc = asc + (1.0 - asc) * phi
    v['asc'] = asc
    v['b5_tap'] = v['b2'] + asc * (v['b5_raw'] - v['b2'])

# C2: pre-taper inversions are impossible by construction -- verified, able to fail
n_pre_inv = sum(1 for v in VANT if v['b5_raw'] < v['b4'] - 1e-12)
P('C2 pre-taper inversions (b5_raw < b[4]): %d of %d  (code fact: band[5]=max(pred,b[4]) -> expected 0)'
  % (n_pre_inv, len(VANT)))
if n_pre_inv: sys.exit('W6 HALT: pre-taper inversion found -- the code-fact decomposition is wrong')
n_tap_inv = sum(1 for v in VANT if v['b5_tap'] < v['b4'] - 1e-9)
P('   post-taper inversions at historical vantages: %d of %d (%.1f%%) -- ALL taper-caused by construction'
  % (n_tap_inv, len(VANT), 100.0 * n_tap_inv / len(VANT)))

# C3: the reconstruction IS the engine's own b6, sampled
random.seed(33)
BYKEY = {}
for p in MA.data: BYKEY.setdefault(p.get('key') or MA.slug(p['player']), p)
samp = random.sample(range(len(VANT)), min(200, len(VANT)))
dev_core, dev_tap = 0.0, 0.0
for i in samp:
    v = VANT[i]; p = BYKEY[v['key']]
    with contextlib.redirect_stdout(io.StringIO()):
        bbc = _b6_core(p, v['Y']); bbt = b6(p, v['Y'])
    dev_core = max(dev_core, abs(float(bbc[5]) - v['b5_raw']), abs(float(bbc[4]) - v['b4']))
    dev_tap = max(dev_tap, abs(float(bbt[5]) - v['b5_tap']))
MA.AGE_REF = 2026; MA.BASE_REF = 2026; MA._pe_clear()
P('C3 engine-reconstruction control (200 sampled vantages): max|_b6_core - (b4,b5_raw)| = %.3e   '
  'max|b6[5] - b5_tap| = %.3e' % (dev_core, dev_tap))
if dev_core > 1e-9 or dev_tap > 1e-9:
    sys.exit('W6 HALT: reconstruction does not reproduce the engine band')

# ---------------------------------------------------------------- cells
AGEB = [('<=19', 0, 19.999), ('20-21', 20, 21.999), ('22-23', 22, 23.999),
        ('24-26', 24, 26.999), ('27+', 27, 99)]
GB = [('0', 0, 0), ('1-10', 1, 10), ('11-30', 11, 30), ('31-60', 31, 60), ('61+', 61, 99999)]
POSC = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK', 'TALL', 'ALL']
def posmatch(cell, g): return cell == 'ALL' or g == cell or (cell == 'TALL' and g in ('KPD', 'KPF', 'RUCK'))

def q_interp(vs, f):
    """the project's own convention: linear interpolation between order statistics at index f*(n-1)"""
    n = len(vs)
    if n == 0: return None
    i = f * (n - 1); lo = int(math.floor(i)); hi = min(lo + 1, n - 1)
    return vs[lo] + (i - lo) * (vs[hi] - vs[lo])

def wilson(k, n, z=1.96):
    if n == 0: return (None, None)
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d; h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

def cellstats(rows):
    n = len(rows); out = dict(n=n, n_players=len({r['key'] for r in rows}))
    if n == 0: return out
    for nm, sel in (('peak', 'peak'), ('dv', 'dv')):
        vs = sorted(r[sel] for r in rows)
        d = dict(min=vs[0], max=vs[-1], median=q_interp(vs, .5))
        if n >= 8:
            for f, lab in ((.90, 'q90'), (.97, 'q97')):
                resolved = n * (1 - f) >= 1
                d[lab] = dict(value=(q_interp(vs, f) if resolved else vs[-1]), resolved=bool(resolved))
            d['thin_players'] = bool(out['n_players'] < 34)
        else:
            d['status'] = 'UNRESOLVED (n<8)'
        out[nm] = d
    if n >= 8:
        for nm in ('pred_raw', 'b5_raw', 'b5_tap', 'b4'):
            vs = [r[nm] for r in rows]
            out['model_' + nm] = dict(mean=sum(vs) / n, median=q_interp(sorted(vs), .5))
        out['taper_bite_mean'] = sum(r['b5_raw'] - r['b5_tap'] for r in rows) / n
        out['inversions_tap'] = sum(1 for r in rows if r['b5_tap'] < r['b4'] - 1e-9)
        for nm in ('pred_raw', 'b5_raw', 'b5_tap'):
            k = sum(1 for r in rows if r['peak'] > r[nm])
            lo, hi = wilson(k, n)
            out['exceed_' + nm] = dict(k=k, rate=k / n, wilson95=[lo, hi])
    return out

CELLS = {}
for wname, cut in CUTS.items():
    rows_w = [v for v in VANT if v['Y'] <= cut]
    for scope, rows_s in (('all', rows_w), ('trainpool', [v for v in rows_w if v['train']])):
        for anm, alo, ahi in AGEB:
            for pc in POSC:
                for gnm, glo, ghi in GB:
                    rows = [v for v in rows_s if alo <= v['age'] <= ahi and posmatch(pc, v['pos'])
                            and glo <= v['games'] <= ghi]
                    CELLS['%s|%s|%s|%s|%s' % (wname, scope, anm, pc, gnm)] = cellstats(rows)

# headline print: primary window, all scope, the early-career bands
P('')
P('=' * 118)
P('PRIMARY WINDOW (vantages <= 2019, outcomes observed to 2026).  peak units = season-avg level '
  '(the model\'s own units); dv units = board points (grace-A season valuation, vantage-discounted)')
P('  exceed = share of vantages whose realized forward best-3 EXCEEDED the model ceiling '
  '(calibrated 97th percentile target ~3%%)')
P('=' * 118)
hdr = ('%-6s %-5s %-6s | %5s %4s | %7s %8s | %8s %8s %8s | %6s %6s %6s | %7s'
       % ('age', 'pos', 'games', 'n', 'npl', 'q97pk', 'q97dv', 'pred', 'b5raw', 'b5tap',
          'x_pred', 'x_raw', 'x_tap', 'taperbite'))
for anm, _, _ in AGEB:
    P(''); P('AGE %s' % anm); P(hdr)
    for pc in POSC:
        for gnm, _, _ in GB:
            c = CELLS['primary_2019|all|%s|%s|%s' % (anm, pc, gnm)]
            if c['n'] == 0: continue
            if 'q97' not in c.get('peak', {}):
                P('%-6s %-5s %-6s | %5d %4d | UNRESOLVED (n<8)  max_pk %.1f max_dv %.1f'
                  % (anm, pc, gnm, c['n'], c['n_players'],
                     c.get('peak', {}).get('max', float('nan')), c.get('dv', {}).get('max', float('nan'))))
                continue
            pk = c['peak']['q97']; dv = c['dv']['q97']
            P('%-6s %-5s %-6s | %5d %4d | %6.1f%s %7.0f%s | %8.1f %8.1f %8.1f | %5.1f%% %5.1f%% %5.1f%% | %7.2f'
              % (anm, pc, gnm, c['n'], c['n_players'],
                 pk['value'], ('*' if not pk['resolved'] else ' '),
                 dv['value'], ('*' if not dv['resolved'] else ' '),
                 c['model_pred_raw']['mean'], c['model_b5_raw']['mean'], c['model_b5_tap']['mean'],
                 100 * c['exceed_pred_raw']['rate'], 100 * c['exceed_b5_raw']['rate'],
                 100 * c['exceed_b5_tap']['rate'], c['taper_bite_mean']))

# overall calibration
P('')
for scope in ('all', 'trainpool'):
    rows = [v for v in VANT if v['Y'] <= 2019 and (scope == 'all' or v['train'])]
    n = len(rows)
    for nm in ('pred_raw', 'b5_raw', 'b5_tap'):
        k = sum(1 for r in rows if r['peak'] > r[nm]); lo, hi = wilson(k, n)
        P('OVERALL exceedance (%s, <=2019, n=%d)  %-8s  %5.2f%%  [%.2f%%, %.2f%%]   target ~3%%'
          % (scope, n, nm, 100 * k / n, 100 * lo, 100 * hi))

# ---------------------------------------------------------------- training-construction audit
P('')
P('=' * 118)
P('TRAINING-CONSTRUCTION AUDIT (refit_q97m.py / in-engine pool: debut<=2021, pick or _ft, not MSD; '
  'target fwd_best3_from(p,Y,2026))')
P('=' * 118)
TP = [p for p in POOL if in_trainpool(p)]
tr_rows = []
for p in TP:
    d0 = cp.debutyr(p) - 1
    last = max([x['year'] for x in p['scoring']] + [d0])
    for Y in range(d0, min(last, 2026) + 1):
        fwd = 2026 - max(Y, cp.debutyr(p)) + 1
        tr_rows.append((cp.debutyr(p), Y, fwd, MA.gfut(p), bool(not (p.get('pick') or p.get('_ft')))))
n_tr = len(tr_rows)
P('  training vantages (reconstructed): %d from %d players' % (n_tr, len(TP)))
for bar in (3, 5):
    k = sum(1 for r in tr_rows if r[2] < bar)
    P('  CENSORING: %5d rows (%.1f%%) have < %d forward seasons observable to 2026 '
      '(their best-3 target is right-censored)' % (k, 100.0 * k / n_tr, bar))
coh = collections.Counter()
cohc = collections.Counter()
for r in tr_rows:
    b = '%d-%d' % (r[0] - (r[0] - 2004) % 3, r[0] - (r[0] - 2004) % 3 + 2)
    coh[b] += 1
    if r[2] < 5: cohc[b] += 1
P('  censored(<5 fwd yrs) share by debut cohort: %s'
  % '  '.join('%s:%.0f%%' % (b, 100.0 * cohc[b] / coh[b]) for b in sorted(coh)))
pw = collections.Counter(p.get('type') for p in POOL if not in_trainpool(p))
P('  EXCLUDED from the training pool entirely (pathway counts, whole store): %s' % dict(pw))
ruck_young = sum(1 for r in tr_rows if r[3] == 'RUCK')
P('  RUCK training vantages: %d of %d (%.1f%%); min_samples_leaf=25 bounds how local the tree can get'
  % (ruck_young, n_tr, 100.0 * ruck_young / n_tr))

# ---------------------------------------------------------------- named rows + local training density
NAMED = ['nick-madden', 'ned-moyle', 'lachlan-mcandrew', 'samuel-grlj',
         'mitchell-edwards', 'jordan-croft', 'jonty-faull', 'alix-tauru']
S6 = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order32_s6_2026-08-17', 'S6_FAN_EMIT.json')))
S6R = {r['key']: r for r in S6['rows']}

def agename(a):
    for nm, lo, hi in AGEB:
        if lo <= a <= hi: return nm
def gname(g):
    for nm, lo, hi in GB:
        if lo <= g <= hi: return nm

def train_density(pos, age, expo):
    """training vantages near this feature point: same group, |age|<=1.5, exposure in [x/2, 2x+4]"""
    k = 0
    for v in VANT:
        if not v['train'] or v['pos'] != pos: continue
        if abs(v['age'] - age) > 1.5: continue
        e = v['f'][7]   # exposure feature (index 6+1: oh6 + [logpk, expo, ten, lvl, age])
        if not (expo / 2.0 <= e <= 2.0 * expo + 4.0): continue
        k += 1
    return k

NROWS = {}
P('')
P('=' * 118)
P('NAMED ROWS (2026 vantage; cells matched on age x pos x games, primary window, all scope)')
P('=' * 118)
for k in NAMED:
    p = BYKEY.get(k); r6 = S6R.get(k)
    if p is None or r6 is None:
        P('  %s: MISSING (store %s, emit %s)' % (k, p is not None, r6 is not None)); continue
    with contextlib.redirect_stdout(io.StringIO()):
        bbc = _b6_core(p, 2026); bbt = b6(p, 2026)
        f26 = cp._feat(p, 2026)
        lcr = _lvlcurr(p, 2026) - MA.REPL.get(MA.gfut(p), 0.0); nq = _nqual(p, 2026)
        pr = float(q97m.predict(np.array([f26]))[0])
    MA.AGE_REF = 2026; MA.BASE_REF = 2026; MA._pe_clear()
    age = r6['age']; g = r6['games']; pos = r6['pos']
    asc = float(np.interp(age, [20, 22, 24, 27], [1.0, 0.76, 0.58, 0.40]))
    ck = 'primary_2019|all|%s|%s|%s' % (agename(age), pos, gname(g))
    ckT = 'primary_2019|all|%s|TALL|%s' % (agename(age), gname(g))
    cell = CELLS.get(ck, {}); cellT = CELLS.get(ckT, {})
    sp = [r6['anchor_pts'] + r6['rho'] * x for x in r6['six_phat']]
    NROWS[k] = dict(pos=pos, pathway=r6['pathway'], age=age, games=g, cand=r6['cand'],
                    rho=r6['rho'], m_downstream=r6['m_downstream'],
                    b6_engine=[float(x) for x in bbt], b6_pre_taper=[float(x) for x in bbc],
                    pred_raw=pr, asc_base=asc, lcr=lcr, nqual=nq,
                    scenario_prices=[float(x) for x in sp],
                    cell=ck, cell_stats={kk: cell.get(kk) for kk in
                        ('n', 'n_players', 'peak', 'dv')} if cell else None,
                    cell_tall=ckT, cell_tall_stats={kk: cellT.get(kk) for kk in
                        ('n', 'n_players', 'peak', 'dv')} if cellT else None,
                    train_density_local=train_density(pos, age, float(f26[7])),
                    excluded_from_trainpool=not in_trainpool(p),
                    trainpool_exclusion_reason=excl_reason(p))
    P('%-18s %-4s %-4s age %-4s g %-3s cand %5d | pred_raw %6.1f  b5_raw %6.1f  b5_tap %6.1f '
      '(asc %.2f, lcr %.1f, nq %d)%s'
      % (k, pos, r6['pathway'], age, g, r6['cand'], pr, float(bbc[5]), float(bbt[5]),
         asc, lcr, nq, ('  [not in training pool: %s]' % excl_reason(p)) if NROWS[k]['excluded_from_trainpool'] else ''))
    pk = (cell.get('peak') or {}) if cell else {}
    pkT = (cellT.get('peak') or {}) if cellT else {}
    P('    cell %-42s n=%-4s realized q97 peak %s   TALL-pooled n=%-4s q97 %s'
      % (ck.split('|', 2)[2], cell.get('n'),
         ('%.1f%s' % (pk['q97']['value'], '' if pk['q97']['resolved'] else '*')) if 'q97' in pk else 'n/a',
         cellT.get('n'),
         ('%.1f%s' % (pkT['q97']['value'], '' if pkT['q97']['resolved'] else '*')) if 'q97' in pkT else 'n/a'))
    dvc = (cell.get('dv') or {}) if cell else {}
    P('    realized q97 DV-from-vantage %s   |   S6 scenario prices %s'
      % (('%.0f%s' % (dvc['q97']['value'], '' if dvc['q97']['resolved'] else '*')) if 'q97' in dvc else 'n/a',
         [int(round(x)) for x in sp]))
    P('    local training density (same pos, age+-1.5, comparable exposure): %d rows'
      % NROWS[k]['train_density_local'])

# ---------------------------------------------------------------- board impact bound (all 804 rows)
P('')
P('=' * 118)
P('BOARD IMPACT BOUND -- variant A (taper off) and variant B (cell-matched realized-q97 ceiling)')
P('  first-order: dPrice_row ~= rho * m_downstream * W6[5] * dSix_raw[5]  (the S6-disclosed reading)')
P('=' * 118)
IMPACT = []
dev_c4 = 0.0
_t0 = time.time()
for k, r6 in S6R.items():
    p = BYKEY.get(k)
    if p is None: continue
    with contextlib.redirect_stdout(io.StringIO()):
        bbc = _b6_core(p, 2026); bbt = b6(p, 2026)
    dev_c4 = max(dev_c4, max(abs(float(a) - float(b)) for a, b in zip(bbt, r6['b6'])))
    age = r6['age']; g = r6['games']; pos = r6['pos']
    ck = 'primary_2019|all|%s|%s|%s' % (agename(age), pos, gname(g))
    cell = CELLS.get(ck, {})
    q97cell = None; src = None
    pk = (cell.get('peak') or {})
    if 'q97' in pk and pk['q97']['resolved'] and not pk.get('thin_players'):
        q97cell = pk['q97']['value']; src = ck
    elif pos in ('KPD', 'KPF', 'RUCK'):
        ckT = 'primary_2019|all|%s|TALL|%s' % (agename(age), gname(g))
        pkT = (CELLS.get(ckT, {}).get('peak') or {})
        if 'q97' in pkT and pkT['q97']['resolved'] and not pkT.get('thin_players'):
            q97cell = pkT['q97']['value']; src = ckT
    ceilA = float(bbc[5])                                   # taper off
    ceilB = max(ceilA, q97cell) if q97cell is not None else None
    # six_raw[5] under each ceiling, in price6's own context (the S6 fan transcription)
    sav = dict(MA.REPL)
    try:
        for gg in MA.REPL: MA.REPL[gg] = sav[gg] - rd.REPL_DROP.get(gg, 0)
        MA.AGE_REF = 2026; MA.BASE_REF = 2026; MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()):
            v_now = float(dp.SCALE_DIST * dp.v_at_peak(p, float(bbt[5]), 'bal'))
            v_A = float(dp.SCALE_DIST * dp.v_at_peak(p, ceilA, 'bal'))
            v_B = float(dp.SCALE_DIST * dp.v_at_peak(p, ceilB, 'bal')) if ceilB is not None else None
    finally:
        MA.REPL.update(sav)
    rho = r6['rho']; m = r6['m_downstream']
    dA = rho * m * WQ6[5] * (v_A - v_now) if r6['fan_carries_price'] else 0.0
    dB = (rho * m * WQ6[5] * (v_B - v_now) if (v_B is not None and r6['fan_carries_price']) else None)
    IMPACT.append(dict(key=k, name=r6['name'], pos=pos, pathway=r6['pathway'], age=age, games=g,
                       cand=r6['cand'], rho=rho, ceil_now=float(bbt[5]), ceil_A=ceilA, ceil_B=ceilB,
                       cell_src=src, six5_now=v_now, six5_A=v_A, six5_B=v_B,
                       dprice_A=dA, dprice_B=dB, inverted_now=bool(r6['q97_below_band5'])))
P('C4 b6 reproduction vs the committed S6 emit: max dev %.3e over %d rows (%.1fs)'
  % (dev_c4, len(IMPACT), time.time() - _t0))
if dev_c4 > 1e-6: sys.exit('W6 HALT: this run does not reproduce the S6 emit band')

movA = [r for r in IMPACT if r['dprice_A'] > 0.5]
movB = [r for r in IMPACT if r['dprice_B'] is not None and r['dprice_B'] > 0.5]
totA = sum(r['dprice_A'] for r in movA); totB = sum(r['dprice_B'] for r in movB)
P('  VARIANT A (taper off): %d rows move > 0.5 pts, total +%.0f pts (board total 666,913 -> +%.2f%%)'
  % (len(movA), totA, 100.0 * totA / 666913))
P('  VARIANT B (cell-matched realized q97, resolved non-thin cells only): %d rows move, total +%.0f pts'
  % (len(movB), totB))
# variant B is a COARSE bound: an age x pos x games cell q97 is unconditional on current level, so on
# established veterans it swamps the model's own (correct) conditioning. Split the bound so the
# early-career reading (the seat's question) is separable from the veteran cell-coarseness artifact.
def seg(r): return 'early (age<=23 & games<=30)' if (r['age'] <= 23 and r['games'] <= 30) else 'rest'
for s in ('early (age<=23 & games<=30)', 'rest'):
    a = sum(r['dprice_A'] for r in movA if seg(r) == s)
    b = sum(r['dprice_B'] for r in movB if seg(r) == s)
    na = sum(1 for r in movA if seg(r) == s); nb = sum(1 for r in movB if seg(r) == s)
    P('    segment %-28s variant A: %3d rows +%6.0f pts   variant B: %3d rows +%6.0f pts%s'
      % (s, na, a, nb, b, '' if s.startswith('early') else '   (B here is mostly cell-coarseness, not model error)'))
P('')
P('  TOP MOVERS, VARIANT A (taper off)')
for r in sorted(movA, key=lambda r: -r['dprice_A'])[:15]:
    P('   %-24s %-4s %-4s a%-3s g%-4s cand %5d  ceil %6.1f -> %6.1f  dprice %+7.1f%s'
      % (r['name'][:24], r['pos'], r['pathway'], r['age'], r['games'], r['cand'],
         r['ceil_now'], r['ceil_A'], r['dprice_A'], '  [was inverted]' if r['inverted_now'] else ''))
P('')
P('  TOP MOVERS, VARIANT B (realized-q97 ceiling)')
for r in sorted(movB, key=lambda r: -r['dprice_B'])[:15]:
    P('   %-24s %-4s %-4s a%-3s g%-4s cand %5d  ceil %6.1f -> %6.1f (%s)  dprice %+7.1f'
      % (r['name'][:24], r['pos'], r['pathway'], r['age'], r['games'], r['cand'],
         r['ceil_now'], r['ceil_B'], (r['cell_src'] or '').split('|', 2)[-1], r['dprice_B']))

# ---------------------------------------------------------------- emit
OUT = {'order': 'ORDER 33 seat W6 -- the frozen q97 ceiling vs realized 97th-percentile outcomes',
       'generated_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
       'prereg': 'PREREG_W6.md', 'identity': IDENT, 'q97m_pin': BOOT.get('q97m'),
       'controls': {'C2_pre_taper_inversions': n_pre_inv,
                    'C3_engine_reconstruction_maxdev': {'core': dev_core, 'tap': dev_tap},
                    'C4_s6_b6_reproduction_maxdev': dev_c4,
                    'post_taper_inversions_hist': [n_tap_inv, len(VANT)]},
       'training_audit': {'n_vantages': n_tr, 'n_players': len(TP),
                          'censored_lt3': sum(1 for r in tr_rows if r[2] < 3),
                          'censored_lt5': sum(1 for r in tr_rows if r[2] < 5),
                          'excluded_pathways': dict(pw),
                          'ruck_share': ruck_young / n_tr},
       'cells': CELLS, 'named': NROWS,
       }
json.dump(OUT, open(os.path.join(HERE, 'W6_CELLS.json'), 'w'), indent=1, sort_keys=True, default=str)
json.dump({'rows': IMPACT, 'totals': {'variant_A_pts': totA, 'variant_A_movers': len(movA),
                                      'variant_B_pts': totB, 'variant_B_movers': len(movB),
                                      'segments': {s: {'A_pts': sum(r['dprice_A'] for r in movA if seg(r) == s),
                                                       'B_pts': sum(r['dprice_B'] for r in movB if seg(r) == s)}
                                                   for s in ('early (age<=23 & games<=30)', 'rest')},
                                      'variant_B_caveat': 'cell q97 is unconditional on current level; on '
                                          'established veterans B measures cell coarseness, not model error'}},
          open(os.path.join(HERE, 'W6_BOARD_IMPACT.json'), 'w'), indent=1, sort_keys=True, default=str)
json.dump(NROWS, open(os.path.join(HERE, 'W6_NAMED.json'), 'w'), indent=1, sort_keys=True, default=str)
with open(os.path.join(HERE, 'W6_VANTAGES.csv'), 'w', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['key', 'Y', 'type', 'pos', 'age', 'games', 'tenure', 'peak_fwd', 'dv_fwd',
                'pred_raw', 'b4', 'b2', 'b5_raw', 'b5_tap', 'asc', 'in_trainpool', 'pickless'])
    for v in VANT:
        w.writerow([v['key'], v['Y'], v['type'], v['pos'], round(v['age'], 2), v['games'], v['tenure'],
                    round(v['peak'], 2), round(v['dv'], 1), round(v['pred_raw'], 2), round(v['b4'], 2),
                    round(v['b2'], 2), round(v['b5_raw'], 2), round(v['b5_tap'], 2), round(v['asc'], 3),
                    int(v['train']), int(v['pickless'])])
open(os.path.join(HERE, 'W6_out.txt'), 'w').write('\n'.join(LOG) + '\n')
print('\nWROTE W6_CELLS.json / W6_BOARD_IMPACT.json / W6_NAMED.json / W6_VANTAGES.csv / W6_out.txt')
